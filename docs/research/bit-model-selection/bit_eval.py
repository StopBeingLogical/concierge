#!/usr/bin/env python3
"""
Concierge Bit Layer — Model Evaluation Suite
Node: Logos (M1 Max, 64GB Unified Memory)
Backend: Ollama 0.19+ (MLX engine — activates automatically on Apple Silicon)

Usage:
    python bit_eval.py                        # run all candidates
    python bit_eval.py --models qwen2.5:14b   # run specific model(s)
    python bit_eval.py --skip-download        # skip pull, only test what's present
    python bit_eval.py --test 2               # run a single test number
    python bit_eval.py --context-file doc.txt             # use specific file for Test 4
    python bit_eval.py --timeline-file Timeline.docx       # inject fiction timeline for Test 1B
    python bit_eval.py --philosophy-file Philosophy_v5.md  # inject Concierge philosophy for Test 1C
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests

# ── Configuration ─────────────────────────────────────────────────────────────

OLLAMA_BASE_URL = "http://localhost:11434"

CANDIDATES = [
    # Tier 1 — COMPLETE
    {"tag": "qwen2.5:14b",        "family": "Qwen",      "tier": 1, "size_b": 14},
    {"tag": "mistral-nemo:12b",   "family": "Mistral",   "tier": 1, "size_b": 12},
    {"tag": "qwen2.5:32b",        "family": "Qwen",      "tier": 1, "size_b": 32},
    {"tag": "phi4:14b",           "family": "Phi",       "tier": 1, "size_b": 14},   # REJECTED — tool call 400 error
    # Tier 2 — in progress
    {"tag": "mistral-small:22b",  "family": "Mistral",   "tier": 2, "size_b": 22},
    {"tag": "command-r:35b",      "family": "Command-R", "tier": 2, "size_b": 35},
    {"tag": "llama3.1:8b",        "family": "Llama",     "tier": 2, "size_b": 8},
    {"tag": "gemma4:26b",         "family": "Gemma4",    "tier": 2, "size_b": 26},   # MoE, ~4B active — requires Ollama 0.20.2+
    {"tag": "gemma4:31b",         "family": "Gemma4",    "tier": 2, "size_b": 31},   # Dense — requires Ollama 0.20.2+
    # Tier 3 — watch/defer
    # gemma4:e4b — revisit if gemma4:26b shortlists (faster MoE variant)
    # llama3.3:70b — only if 70B latency proves viable
    # deepseek-r1:14b — reasoning-focused, may be overkill
    # gemma3:12b / gemma3:27b — superseded by Gemma 4, skip
]

# Weights for final score (must sum to 1.0)
WEIGHTS = {
    "conversational": 0.30,
    "tool_calling":   0.25,
    "instruction":    0.20,
    "context":        0.15,
    "latency":        0.10,
}

NUM_CTX = 32768

# ── Test definitions ───────────────────────────────────────────────────────────

TESTS = {

    1: {
        "name": "Rubber Duck (Conversational Reasoning)",
        "dimension": "conversational",
        "temperature": 0.7,   # intentional — want natural reasoning, not greedy decode
        "tool_schema": None,

        # Three sub-prompts. Documents injected at runtime by run_test_1().
        # {TIMELINE_DOC} and {PHILOSOPHY_DOC} are replaced before sending.
        "sub_prompts": [
            {
                "id": "1A",
                "name": "Steam Game Recommendation",
                "inject_docs": [],   # no documents — vacuum test
                "prompt": (
                    "I\'m trying to decide what to buy next on Steam. I have about 40 hours "
                    "banked for the next few weeks and I want something I\'ll actually finish. "
                    "Don\'t recommend anything yet — ask me three questions about my preferences "
                    "and habits that would help you narrow it down."
                ),
                "scoring_guide": (
                    "5 — Probes completion habits, current mood/headspace, AND something "
                    "non-obvious (session length, difficulty tolerance, solo vs social, "
                    "time-of-day patterns). Asks nothing, recommends nothing.\n"
                    "4 — Good questions, all fairly standard genre/preference territory.\n"
                    "3 — Generic (what genre, what have you played before).\n"
                    "2 — Ignores instruction and recommends games anyway.\n"
                    "1 — Off-topic or refuses."
                ),
            },
            {
                "id": "1B",
                "name": "Fiction Timeline — Next Short Story",
                "inject_docs": ["timeline"],   # timeline doc injected at top
                "prompt": (
                    "I\'m working on a fantasy fiction project. The master timeline for the "
                    "world is provided above.\n\n"
                    "I want to write a new short story set somewhere in this timeline. "
                    "Don\'t suggest a setting yet — ask me three questions that would help "
                    "identify where the most dramatically interesting story could be set."
                ),
                "scoring_guide": (
                    "5 — Identifies the 0346-0350DE compression (Nageri discovery to Sundering "
                    "in 4 years), the 0685-0688DE Phineas hunt, or the structural gap between "
                    "documented events. Question shows it understood the dramatic implication, "
                    "not just listed dates. Does not suggest a setting.\n"
                    "4 — Notices a specific period but questions are generic (tone, length).\n"
                    "3 — Asks about character or genre without engaging with timeline structure.\n"
                    "2 — Ignores instruction and suggests a setting directly.\n"
                    "1 — Off-topic or refuses."
                ),
            },
            {
                "id": "1C",
                "name": "Concierge Hardware Node Evaluation",
                "inject_docs": ["philosophy"],   # philosophy doc injected at top
                "prompt": (
                    "I\'m evaluating whether to add a new inference node to my Concierge "
                    "cluster. The role would be a general ensemble worker — a quorum voice, "
                    "not a verifier. The architecture philosophy document is provided above.\n\n"
                    "Don\'t make a hardware recommendation yet. Ask me three questions about "
                    "my cluster\'s current state and workload that I should be able to answer "
                    "before making this decision."
                ),
                "scoring_guide": (
                    "5 — Asks about current model family coverage / training lineage diversity "
                    "gaps, memory bandwidth profile of existing nodes, AND either network "
                    "latency topology or current queue pressure. Demonstrates it absorbed the "
                    "Wide Not Deep principle and bandwidth-as-primary-metric rule.\n"
                    "4 — Good distributed inference questions but misses family diversity angle.\n"
                    "3 — Generic compute questions (how much RAM, what GPU, what budget).\n"
                    "2 — Jumps straight to recommending hardware.\n"
                    "1 — No architectural awareness, generic or off-topic."
                ),
            },
        ],
    },

    2: {
        "name": "Tool Schema Precision (Structured Function Calling)",
        "dimension": "tool_calling",
        "temperature": 0.0,
        "prompt": (
            "Available tool: get_node_metrics(node_id: string, metric_type: 'cpu'|'thermal').\n"
            "Requirement: Retrieve the CPU metrics for 'Node-Alpha-01' AND the thermal metrics "
            "for 'Node-Beta-99' simultaneously in a single response."
        ),
        "tool_schema": [
            {
                "type": "function",
                "function": {
                    "name": "get_node_metrics",
                    "description": "Retrieve performance metrics for a cluster node.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "node_id": {
                                "type": "string",
                                "description": "The node identifier."
                            },
                            "metric_type": {
                                "type": "string",
                                "enum": ["cpu", "thermal"],
                                "description": "The type of metric to retrieve."
                            }
                        },
                        "required": ["node_id", "metric_type"]
                    }
                }
            }
        ],
        "tool_schema_2b": {
            # Second prompt: should NOT trigger a tool call
            "prompt": (
                "What time is it right now?"
            ),
            "expect_no_call": True,
        },
        "scoring_guide": (
            "5 — Two valid tool calls, correct node IDs, correct metric types, no extra fields. "
            "Abstains correctly on the no-call follow-up.\n"
            "4 — Two valid calls but follow-up also triggers a spurious call.\n"
            "3 — One valid call, misses the second. Or both calls present but wrong metric_type.\n"
            "2 — Produces JSON but malformed or wrong structure.\n"
            "1 — No tool calls, just prose. Or completely wrong tool name/args."
        ),
    },

    3: {
        "name": "Instruction Discipline (Constraint Following)",
        "dimension": "instruction",
        "temperature": 0.0,
        "prompt": (
            "Summarize your current hardware environment (M1 Max, 64GB unified memory).\n"
            "Hard constraints — all must be satisfied:\n"
            "1. Exactly three bullet points.\n"
            "2. No bullet may exceed 10 words.\n"
            "3. Do not use the words: Mac, Apple, or Memory.\n"
            "4. Every bullet must end with a semicolon."
        ),
        "tool_schema": None,
        "scoring_guide": (
            "5 — All four constraints satisfied. Zero forbidden words. Correct count. Semicolons present.\n"
            "4 — Three of four constraints met.\n"
            "3 — Two of four constraints met.\n"
            "2 — One constraint met.\n"
            "1 — Ignores constraints entirely."
        ),
    },

    4: {
        "name": "Context Needle Retrieval (Long Context)",
        "dimension": "context",
        "temperature": 0.0,
        "prompt_setup": (
            "The following is a large technical document. Read it carefully.\n\n"
            "{context_document}\n\n"
            "---\n"
            "Now let's talk about something else for a moment. "
            "What are three general best practices for distributed system design?"
        ),
        "prompt_retrieval": (
            "Earlier in this document there was a short tagged annotation embedded "
            "in the text — a line beginning with ARCHIVE_KEY. "
            "What was the full value of that ARCHIVE_KEY?"
        ),
        "tool_schema": None,
        "scoring_guide": (
            "5 — Immediate, exact retrieval of ZULU-9-OMEGA with no hallucination.\n"
            "4 — Retrieves correctly but with hedging ('I think it was...').\n"
            "3 — Retrieves partially or with minor error (e.g. ZULU-9-OMEGA vs ZULU-9).\n"
            "2 — Hallucinates a different key.\n"
            "1 — Claims no key was mentioned or found."
        ),
    },

    5: {
        "name": "Intent Parsing (Semantic Bridge to Planner)",
        "dimension": "conversational",  # contributes to conversational score
        "temperature": 0.0,
        "prompt": (
            "Parse the following natural language task into a structured JSON object.\n\n"
            "Task: \"Deploy the 'Workbee-Alpha' image to the cluster. "
            "If thermal pressure is over 80%, abort. "
            "If it's between 60% and 80%, delay for 10 minutes and retry. "
            "Otherwise, proceed immediately.\"\n\n"
            "Output ONLY valid JSON with fields: intent, target, logic (array of condition/action objects). "
            "No prose, no markdown fences, no explanation."
        ),
        "tool_schema": None,
        "scoring_guide": (
            "5 — Valid JSON, correct intent/target, all three logic branches present with correct "
            "conditions and actions. Parseable by json.loads().\n"
            "4 — Valid JSON, all branches present, minor semantic error (e.g. '>80' vs '>80%').\n"
            "3 — Valid JSON, missing one branch or extra fields.\n"
            "2 — JSON present but malformed or unparseable.\n"
            "1 — Returns prose or markdown instead of raw JSON."
        ),
    },
}

# ── Helpers ────────────────────────────────────────────────────────────────────

def print_header(text: str) -> None:
    width = 72
    print("\n" + "═" * width)
    print(f"  {text}")
    print("═" * width)

def print_step(text: str) -> None:
    print(f"\n▸ {text}")

def print_ok(text: str) -> None:
    print(f"  ✓ {text}")

def print_warn(text: str) -> None:
    print(f"  ⚠ {text}")

def print_err(text: str) -> None:
    print(f"  ✗ {text}", file=sys.stderr)


def check_ollama_running() -> bool:
    try:
        r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        return r.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def get_local_models() -> list[str]:
    try:
        r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
        r.raise_for_status()
        return [m["name"] for m in r.json().get("models", [])]
    except Exception:
        return []


def normalize_tag(tag: str) -> str:
    """Normalize model tag for comparison — add :latest if no version specified."""
    return tag if ":" in tag else f"{tag}:latest"


def model_is_local(tag: str, local_models: list[str]) -> bool:
    normalized = normalize_tag(tag)
    return any(normalize_tag(m) == normalized or m == tag for m in local_models)


def pull_model(tag: str) -> bool:
    print_step(f"Pulling {tag} ...")
    try:
        result = subprocess.run(
            ["ollama", "pull", tag],
            capture_output=False,
            text=True,
        )
        return result.returncode == 0
    except FileNotFoundError:
        print_err("ollama CLI not found in PATH")
        return False


def detect_thinking_tokens(text: str) -> bool:
    """Check for leaked thinking/reasoning tokens in model output."""
    patterns = [
        r"<\|channel\>thought",
        r"<\|think\>",
        r"<thinking>",
        r"<\|im_start\|>think",
        r"\[THINKING\]",
        r"<reasoning>",
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def detect_backend(model_info: dict) -> str:
    """Best-effort backend detection from model details."""
    details = model_info.get("details", {})
    families = details.get("families", [])
    quantization = details.get("quantization_level", "unknown")
    # MLX models served through Ollama 0.19 don't expose a direct flag yet
    # We note quantization and flag NVFP4 as a likely MLX path
    if "nvfp4" in quantization.lower():
        return f"MLX/NVFP4 ({quantization})"
    return f"llama.cpp/MLX-auto ({quantization})"


def get_model_info(tag: str) -> dict:
    try:
        r = requests.post(
            f"{OLLAMA_BASE_URL}/api/show",
            json={"name": tag},
            timeout=15,
        )
        r.raise_for_status()
        return r.json()
    except Exception:
        return {}


def chat(
    model: str,
    messages: list[dict],
    temperature: float = 0.7,
    tools: Optional[list] = None,
    num_ctx: int = NUM_CTX,
) -> tuple[str, dict]:
    """
    Send a chat request to Ollama. Returns (response_text, perf_metrics).
    perf_metrics includes eval_count, eval_duration, prompt_eval_count, prompt_eval_duration.
    """
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_ctx": num_ctx,
        },
    }
    if tools:
        payload["tools"] = tools

    t_start = time.time()
    try:
        r = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=300,
        )
        r.raise_for_status()
        elapsed = time.time() - t_start
        data = r.json()

        message = data.get("message", {})
        content = message.get("content", "") or ""
        tool_calls = message.get("tool_calls", [])

        # Build perf metrics
        eval_count = data.get("eval_count", 0)
        eval_duration_ns = data.get("eval_duration", 1)
        prompt_eval_count = data.get("prompt_eval_count", 0)
        prompt_eval_duration_ns = data.get("prompt_eval_duration", 1)

        decode_tps = (eval_count / (eval_duration_ns / 1e9)) if eval_duration_ns > 0 else 0
        prefill_tps = (prompt_eval_count / (prompt_eval_duration_ns / 1e9)) if prompt_eval_duration_ns > 0 else 0

        perf = {
            "decode_tps": round(decode_tps, 1),
            "prefill_tps": round(prefill_tps, 1),
            "total_tokens": eval_count,
            "prompt_tokens": prompt_eval_count,
            "wall_time_s": round(elapsed, 2),
            "tool_calls": tool_calls,
        }
        return content, perf

    except requests.exceptions.Timeout:
        return "[TIMEOUT — model did not respond within 300s]", {}
    except Exception as e:
        return f"[ERROR — {e}]", {}


def generate_context_document(target_tokens: int = 15000, output_path: str = "test4_context.txt") -> str:
    """
    Generate a randomised technical reference document for Test 4.

    The document is built from shuffled sections drawn from multiple technical
    domains so the content is coherent prose but non-repetitive. Token count is
    approximated at ~0.75 words-per-token (conservative for English technical text).

    The ARCHIVE_KEY needle IS embedded here, approximately 750 tokens into the
    document body — past the opening header but well before the bulk of the content.
    This avoids the position-zero attention sink and tests genuine mid-context retrieval.
    The needle line is: [ARCHIVE_KEY: ZULU-9-OMEGA]

    The generated file is saved to output_path so it can be inspected or reused.
    Subsequent runs reuse the file if it already exists, keeping test conditions
    stable across model comparisons.
    """
    import random

    target_words = int(target_tokens / 0.75)

    # ── Section templates ──────────────────────────────────────────────────────
    # Each entry is (title, body). Bodies are ~200-350 words each.
    # Domains: distributed systems, networking, OS internals, storage, security.

    sections = [
        ("Consensus Algorithms", """
Consensus algorithms enable a distributed cluster to agree on a single value despite
partial failures. The canonical approach, Paxos, operates in two phases. During the
Prepare phase a proposer broadcasts a proposal number; acceptors reply with a promise
not to accept lower-numbered proposals. During the Accept phase the proposer broadcasts
its chosen value, which acceptors record unless they have since promised a higher number.
Multi-Paxos extends this with a stable leader to amortise the cost of the first phase
across many rounds.

Raft was designed to be more understandable than Paxos by decomposing the problem into
leader election, log replication, and safety. A Raft cluster maintains exactly one leader
at a time. Leaders replicate log entries to followers before committing them. Followers
that do not receive a heartbeat within a randomised timeout start an election. Randomised
timeouts prevent simultaneous elections in most practical cases. Once a candidate receives
votes from a majority of nodes it becomes the new leader and begins accepting client
requests.

Viewstamped Replication predates both Paxos and Raft and introduced several concepts
later adopted elsewhere, including the notion of a view number to track leadership changes
and a prepare-commit two-phase log replication protocol. Its recovery protocol handles
the case where a new primary must reconstruct state from the most up-to-date replica
before resuming normal operation.
        """),

        ("Memory Management and Virtual Address Spaces", """
Modern operating systems provide each process with a private virtual address space mapped
to physical pages through a multi-level page table. On x86-64 the canonical four-level
table structure (PML4, PDPT, PD, PT) allows a 48-bit virtual address space with 4 KB
pages, expandable to 57 bits with five-level paging. Each table entry carries permission
bits controlling read, write, and execute access, along with a present bit that triggers
a page fault on access to unmapped regions.

The Translation Lookaside Buffer caches recent virtual-to-physical translations to avoid
walking the full page table on every memory access. A TLB miss causes the CPU to perform
a hardware page-table walk, loading the result into the TLB. Operating system context
switches flush the TLB unless the processor supports Address Space Identifiers, which tag
entries with a per-process identifier and allow entries from different processes to coexist.

Huge pages reduce TLB pressure by covering 2 MB or 1 GB of physical memory per entry.
Linux supports transparent huge pages, which the kernel may promote silently to reduce
page-table overhead for large anonymous mappings. The downside is memory fragmentation:
a 2 MB huge page that contains even a single mapped byte cannot be reclaimed or split
without first demoting it to base pages.

Demand paging allows pages to be loaded lazily from backing store. When a process first
accesses a page the fault handler allocates a physical frame, reads the data, updates the
page table entry, and resumes execution. Copy-on-write forks share parent pages until one
process writes, at which point the kernel faults in a private copy.
        """),

        ("Network Congestion Control", """
TCP congestion control balances throughput against fairness and loss avoidance by
maintaining a congestion window that limits the number of unacknowledged segments in
flight. The slow-start phase grows the window exponentially until a threshold is reached
or a loss event occurs. Congestion avoidance then increases the window linearly, one
maximum segment size per round-trip time. A timeout resets the window to one segment and
restarts slow start. A triple duplicate ACK triggers fast retransmit and fast recovery,
halving the window and threshold without restarting slow start.

CUBIC replaces the linear growth function with a cubic curve centred on the last
congestion event. This allows the window to grow aggressively after a loss while
approaching the previous maximum cautiously, which improves fairness in high-bandwidth
long-delay networks. Linux has used CUBIC as its default since kernel 2.6.19.

BBR takes a different approach by modelling the bottleneck bandwidth and round-trip
propagation delay directly rather than inferring congestion from packet loss. It
periodically probes for additional bandwidth and maintains a pacing rate that keeps the
network pipe full without building excessive queue. BBR performs well on paths with
shallow buffers and in high-loss wireless environments where loss-based algorithms
interpret corruption as congestion.

QUIC moves congestion control to user space, allowing faster iteration and per-connection
algorithm selection. Its packet-number space separates retransmitted and original data,
eliminating the TCP retransmission ambiguity that complicates RTT estimation. Connection
migration lets a client maintain a session across IP address changes, which is common on
mobile devices moving between WiFi and cellular networks.
        """),

        ("Storage Engine Internals", """
Log-structured storage engines write all mutations as sequential appends to an
append-only log, periodically compacting old segments to reclaim space. This design
converts random writes into sequential I/O, which is substantially faster on rotational
media and avoids write amplification on flash. LevelDB and RocksDB implement a
log-structured merge tree where data is organised into multiple levels. Level zero
contains recently flushed memtable data. Higher levels hold progressively larger sorted
runs merged during compaction.

B-tree storage engines organise data in a balanced tree of fixed-size pages. Each update
performs a read-modify-write on one or more pages, which can be expensive on flash due to
erase-before-write semantics. Write-ahead logging provides crash recovery: every
modification is first recorded in the log before being applied to the tree. On recovery
the engine replays uncommitted log entries to restore a consistent state.

Copy-on-write B-trees, used in systems like LMDB and the btrfs filesystem, never modify
pages in place. Instead, each write creates a new page and updates the path from root to
leaf by creating new copies of all ancestor pages. The old root remains valid until
explicitly discarded, enabling multiversion concurrency control without a separate lock
manager. Readers access a consistent snapshot by pinning the root at the start of their
transaction.

Bloom filters allow storage engines to skip disk reads for keys that do not exist in a
given SSTable or B-tree file. A bloom filter stores a compact probabilistic summary of
the key set with a controllable false positive rate. A false positive wastes one I/O; a
false negative is impossible. Typical deployments target one to two percent false positive
rates, which requires roughly ten bits per key.
        """),

        ("Public Key Infrastructure and Certificate Chains", """
Public key infrastructure establishes trust hierarchies that allow parties who have never
communicated to authenticate each other. A certificate authority signs certificates that
bind a public key to an identity. Relying parties trust a root CA by including its
self-signed certificate in a trust store maintained by the operating system or browser.
Intermediate CAs sit between the root and end-entity certificates, reducing risk by
keeping the root key offline.

X.509 certificates carry the subject name, public key, validity period, issuer name,
and a signature over all fields computed by the issuing CA. Extensions add constraints:
the Basic Constraints extension marks CA certificates; the Subject Alternative Name
extension lists hostnames and IP addresses; the Key Usage and Extended Key Usage
extensions restrict what a key may be used for.

Certificate Transparency requires CAs to log all issued certificates in append-only Merkle
trees maintained by independent log operators. Browsers reject certificates that are not
accompanied by a signed certificate timestamp proving inclusion in a known log. This allows
domain owners and security researchers to detect misissued certificates quickly. The CT
ecosystem has uncovered several CA incidents within hours of certificate issuance.

Online Certificate Status Protocol and Certificate Revocation Lists allow relying parties
to check whether a certificate has been revoked before its natural expiry. OCSP stapling
lets the server attach a recent OCSP response to the TLS handshake, eliminating the
need for the client to contact the OCSP responder directly. Hard-fail OCSP requires a
valid stapled response before allowing a connection, preventing revocation bypass.
        """),

        ("Containerisation and Namespace Isolation", """
Linux namespaces partition global kernel resources so that processes in different
namespaces see isolated views. The PID namespace gives a container its own process ID
space, with PID 1 being the container init. The network namespace provides a private
network stack including interfaces, routing tables, firewall rules, and socket tables.
The mount namespace controls the filesystem hierarchy visible to a process. The user
namespace maps container UIDs to host UIDs, allowing unprivileged users to run root
inside a container without real host privileges.

Control groups limit and account for resource usage. A cgroup hierarchy assigns processes
to groups that share resource limits. The CPU controller caps CPU time or sets relative
weights. The memory controller enforces memory limits and triggers the OOM killer when a
cgroup exceeds its allocation. The blkio controller throttles block I/O bandwidth and
limits IOPS per device.

The union filesystem layers used by container runtimes compose a container image from
multiple read-only layers plus a writable overlay. When a process writes to a file that
exists in a lower layer, the runtime copies it up to the writable layer before the write
proceeds. This copy-on-write approach keeps the base layers immutable and shareable
across containers running the same image, saving storage and download time.

seccomp filters restrict which system calls a process may make. A filter is a BPF program
that runs in the kernel before each system call and either allows, traps, or kills the
calling thread. Container runtimes install a default seccomp profile that blocks
dangerous calls like ptrace, mount, and kexec while permitting everything needed for
normal application operation.
        """),

        ("Distributed Tracing and Observability", """
Distributed tracing captures the causal chain of operations across service boundaries.
A trace represents the end-to-end execution of a single user request, decomposed into
spans that record individual operations. Each span carries a trace ID shared across all
spans in the trace, a span ID unique within the trace, and a parent span ID that encodes
the call graph. Timing data shows where latency is concentrated. Contextual tags attach
metadata such as service name, host, and error codes.

The W3C Trace Context standard defines HTTP headers for propagating trace context between
services: traceparent carries the trace ID, parent span ID, and sampling flags; tracestate
carries vendor-specific fields. By adopting a common propagation format, heterogeneous
services from different vendors can participate in the same trace without custom
integration.

Exemplars link metrics to traces by embedding a trace ID in a metric sample. When
investigating a latency spike in a histogram, an exemplar points to a specific trace that
contributed to the high-latency bucket, allowing the operator to drill from aggregate
metrics into a concrete execution. OpenMetrics and Prometheus support exemplars in the
text exposition format and in remote write.

Continuous profiling extends tracing to CPU and memory profiles, capturing stack traces
across a fleet of services at low overhead. Unlike one-shot profiles, continuous profilers
aggregate data over time, allowing engineers to compare profiles before and after a
deployment or correlate CPU regressions with code changes. Parca, Pyroscope, and Polar
Signals are open-source implementations that store profiles in object storage for
long-term retention.
        """),

        ("Scheduling in Operating Systems", """
The CPU scheduler decides which runnable process executes next and for how long.
Completely Fair Scheduler, the default Linux process scheduler since 2.6.23, models
fairness as equal virtual runtime. Each process accumulates virtual runtime proportional
to its wall-clock CPU usage divided by its weight. The scheduler always runs the process
with the lowest accumulated virtual runtime, approximating ideal work-conserving fair
queuing. A red-black tree ordered by virtual runtime allows O(log n) insertion and
O(1) extraction of the minimum.

Real-time scheduling policies bypass CFS for latency-sensitive workloads. SCHED_FIFO
runs a task until it yields or is preempted by a higher-priority real-time task.
SCHED_RR is similar but adds a time quantum after which the task is moved to the end of
its priority queue. Both policies require root privileges to set priorities above zero
because a misbehaving high-priority task can starve the entire system.

NUMA-aware scheduling places threads on the CPU socket closest to the memory they access.
The scheduler tracks the NUMA node of each process's memory allocations and prefers to
schedule it on a CPU with local access to that node. Periodic NUMA balancing unmaps pages
and retraps the faulting access to detect which node is actually accessing which memory,
then migrates pages and tasks to reduce remote accesses.

Energy-aware scheduling extends NUMA awareness to heterogeneous CPU topologies like ARM
big.LITTLE, where high-performance cores and high-efficiency cores coexist on the same
chip. The scheduler maintains a power model for each CPU and routes foreground tasks to
performance cores while parking idle threads on efficiency cores to reduce power draw
during light workloads.
        """),

        ("Hash Functions and Integrity Verification", """
Cryptographic hash functions map arbitrary-length inputs to fixed-length digests with
three security properties. Pre-image resistance makes it computationally infeasible to
find an input that hashes to a given digest. Second pre-image resistance makes it
infeasible to find a different input with the same hash as a given input. Collision
resistance makes it infeasible to find any two distinct inputs with the same hash.

SHA-256 produces a 256-bit digest through a Merkle-Damgård construction operating on
512-bit message blocks. The compression function applies 64 rounds of mixing using
message schedule words derived from the input block and eight state variables initialised
to the square roots of the first eight prime numbers. SHA-3 uses a sponge construction
with a 1600-bit state, absorbing input in 1088-bit chunks and squeezing output after
applying the Keccak permutation.

BLAKE3 is a modern cryptographic hash designed for software performance. It combines a
binary tree of BLAKE2 compression functions with a streaming mode that allows incremental
updates and parallel computation across multiple CPU cores. BLAKE3 is faster than
SHA-256 and SHA-3 on modern hardware with SIMD extensions and matches their security
levels.

Message authentication codes extend hash functions with a shared secret key to provide
integrity and authenticity simultaneously. HMAC constructs a MAC by hashing the key
concatenated with the message twice with different key derivations. KMAC, defined in
NIST SP 800-185, is a purpose-built MAC based on SHA-3 that avoids the length-extension
vulnerability present in HMAC-SHA-256 when used carelessly.
        """),

        ("gRPC and Protocol Buffers", """
gRPC is a high-performance RPC framework that uses HTTP/2 as its transport and Protocol
Buffers as its default serialisation format. HTTP/2 multiplexes multiple streams over a
single TCP connection, eliminating head-of-line blocking at the HTTP layer. Each RPC
maps to a stream, with request and response messages framed as DATA frames. Trailers carry
the gRPC status code and metadata after the response body is complete.

Protocol Buffers encode structured data as a sequence of tag-value pairs. Each field has
a field number assigned in the .proto schema and a wire type that encodes the length or
format of the value. Varint encoding compresses small integers efficiently, using the
most significant bit of each byte as a continuation flag. This binary format is
substantially more compact than JSON for numeric-heavy payloads and avoids the overhead
of text parsing.

Bidirectional streaming RPCs allow both the client and server to send an arbitrary
sequence of messages over the same stream. This enables server-push scenarios, long-lived
subscriptions, and chunked upload protocols without polling. The gRPC framework handles
flow control by mapping HTTP/2 window updates to back-pressure on the message send queue,
preventing fast producers from overwhelming slow consumers.

gRPC-Web is a browser-compatible subset that wraps gRPC messages in a modified framing
protocol compatible with HTTP/1.1, since browsers cannot access the raw HTTP/2 framing
layer. A proxy such as Envoy or grpc-web-proxy translates between the browser and a
standard gRPC backend, allowing web applications to call backend services using the same
generated client code as native gRPC clients.
        """),
    ]

    random.seed(42)  # reproducible shuffle — same document every run unless seed changes
    random.shuffle(sections)

    # Build the document, cycling through sections until we hit the word target
    header_line1 = "TECHNICAL REFERENCE COMPENDIUM — SYSTEMS ENGINEERING SERIES"
    header_line2 = "Volume 3: Core Infrastructure Concepts"
    header_line3 = "=" * 72
    parts = [header_line1 + "\n", header_line2 + "\n", header_line3 + "\n\n"]

    section_index = 0
    word_count = sum(len(p.split()) for p in parts)

    # Target needle position: ~750 tokens = ~1000 words into the document.
    # We write one full section first (~250-350 words), then embed the needle,
    # then continue with the remaining sections. This puts the needle past the
    # header and opening section but well before the bulk of the corpus.
    NEEDLE_AFTER_WORDS = 1000
    needle_embedded = False

    while word_count < target_words:
        title, body = sections[section_index % len(sections)]
        # Add a section number to break repetition when cycling
        cycle = section_index // len(sections)
        suffix = f" (Continued — Part {cycle + 1})" if cycle > 0 else ""
        block = f"\n## {section_index + 1}. {title}{suffix}\n{body.strip()}\n"
        parts.append(block)
        word_count += len(block.split())
        section_index += 1

        # Embed needle once we have enough leading content
        if not needle_embedded and word_count >= NEEDLE_AFTER_WORDS:
            needle_block = (
                "\n<!-- internal annotation -->\n"
                "[ARCHIVE_KEY: ZULU-9-OMEGA]\n"
                "<!-- end annotation -->\n"
            )
            parts.append(needle_block)
            word_count += len(needle_block.split())
            needle_embedded = True

    document = "\n".join(parts)
    actual_words = len(document.split())
    approx_tokens = int(actual_words * 0.75)

    # Save to file
    out = Path(output_path)
    out.write_text(document, encoding="utf-8")

    return document, actual_words, approx_tokens, str(out.resolve())


def load_context_document(path: Optional[str], target_tokens: int = 15000) -> str:
    """
    Load or generate the context document for Test 4.

    Priority:
    1. --context-file path if provided and exists
    2. Previously generated test4_context.txt in current directory (stable across runs)
    3. Generate a new document at target_tokens length and save it
    """
    # Option 1: explicit path provided
    if path and Path(path).exists():
        text = Path(path).read_text(encoding="utf-8")
        words = len(text.split())
        approx_tokens = int(words * 0.75)
        print_ok(f"Loaded context document: {path}")
        print_ok(f"  {words:,} words ≈ {approx_tokens:,} tokens")
        if approx_tokens < 8000:
            print_warn(f"Document is short ({approx_tokens:,} tokens). "
                       "Test 4 is more meaningful with 12k+ tokens.")
        return text

    # Option 2: previously generated file exists
    default_path = Path("test4_context.txt")
    if default_path.exists():
        text = default_path.read_text(encoding="utf-8")
        words = len(text.split())
        approx_tokens = int(words * 0.75)
        print_ok(f"Reusing existing generated context document: {default_path.resolve()}")
        print_ok(f"  {words:,} words ≈ {approx_tokens:,} tokens")
        return text

    # Option 3: generate
    print_step(f"Generating Test 4 context document (~{target_tokens:,} tokens) ...")
    document, words, approx_tokens, saved_path = generate_context_document(
        target_tokens=target_tokens,
        output_path=str(default_path),
    )
    print_ok(f"Generated: {words:,} words ≈ {approx_tokens:,} tokens")
    print_ok(f"Saved to:  {saved_path}")
    print_ok("Subsequent runs will reuse this file for stable test conditions.")
    return document


# ── Test runners ───────────────────────────────────────────────────────────────

def load_text_file(path: str, label: str) -> str:
    """Load a plain text or markdown file for document injection."""
    p = Path(path)
    if not p.exists():
        print_warn(f"{label} file not found: {path}")
        return ""
    text = p.read_text(encoding="utf-8")
    print_ok(f"Loaded {label}: {path} ({len(text.split()):,} words)")
    return text


def load_docx_file(path: str, label: str) -> str:
    """Extract plain text from a .docx file using pandoc."""
    p = Path(path)
    if not p.exists():
        print_warn(f"{label} file not found: {path}")
        return ""
    try:
        import subprocess as sp
        result = sp.run(
            ["pandoc", str(p), "-t", "plain"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            print_warn(f"pandoc failed for {label}: {result.stderr[:200]}")
            return ""
        text = result.stdout.strip()
        print_ok(f"Loaded {label}: {path} ({len(text.split()):,} words)")
        return text
    except FileNotFoundError:
        print_warn("pandoc not found — cannot extract .docx. Install with: brew install pandoc")
        return ""
    except Exception as e:
        print_warn(f"Failed to load {label}: {e}")
        return ""


def build_test1_prompt(sub: dict, docs: dict) -> str:
    """
    Build the full prompt for a Test 1 sub-prompt by injecting
    requested documents at the top, followed by the task instruction.
    """
    parts = []
    for doc_key in sub.get("inject_docs", []):
        doc_text = docs.get(doc_key, "")
        if doc_text:
            label = {
                "timeline": "FICTION PROJECT TIMELINE",
                "philosophy": "CONCIERGE ARCHITECTURE PHILOSOPHY",
            }.get(doc_key, doc_key.upper())
            parts.append(f"--- {label} ---\n{doc_text}\n--- END {label} ---")
    parts.append(sub["prompt"])
    return "\n\n".join(parts)


def run_test_1(model: str, docs: Optional[dict] = None) -> dict:
    """Rubber Duck — three sub-prompts covering Steam, fiction, and Concierge hardware."""
    t = TESTS[1]
    docs = docs or {}
    print_step(f"Test 1: {t['name']}")

    sub_results = []
    all_perf = []
    any_thinking_leak = False

    for sub in t["sub_prompts"]:
        print_step(f"  Sub-prompt {sub['id']}: {sub['name']}")

        # Warn if required docs are missing
        for doc_key in sub.get("inject_docs", []):
            if not docs.get(doc_key):
                print_warn(f"  Document '{doc_key}' not loaded — {sub['id']} will run without it.")
                print_warn(f"  Pass --{'timeline-file' if doc_key == 'timeline' else 'philosophy-file'} to inject context.")

        full_prompt = build_test1_prompt(sub, docs)
        prompt_tokens_approx = int(len(full_prompt.split()) * 0.75)
        print_ok(f"  Prompt size: ~{prompt_tokens_approx:,} tokens")

        response, perf = chat(
            model,
            [{"role": "user", "content": full_prompt}],
            temperature=t["temperature"],
        )

        thinking_leak = detect_thinking_tokens(response)
        if thinking_leak:
            print_warn(f"  Thinking token leak in {sub['id']}.")
            any_thinking_leak = True

        print(f"\n  Response preview:\n  {response[:300].replace(chr(10), chr(10)+chr(32)*4)}\n  ...")

        if perf.get("decode_tps"):
            all_perf.append(perf)

        sub_results.append({
            "sub_id": sub["id"],
            "name": sub["name"],
            "prompt": full_prompt[:300] + "... [truncated]",
            "response": response,
            "perf": perf,
            "thinking_leak": thinking_leak,
            "scoring_guide": sub["scoring_guide"],
            "score": None,   # human-scored
            "notes": f"Docs injected: {sub.get('inject_docs', [])}. Prompt ~{prompt_tokens_approx:,} tokens.",
        })

    avg_perf = {
        "decode_tps": round(sum(p["decode_tps"] for p in all_perf) / len(all_perf), 1) if all_perf else 0,
        "prefill_tps": round(sum(p["prefill_tps"] for p in all_perf) / len(all_perf), 1) if all_perf else 0,
        "total_tokens": sum(p.get("total_tokens", 0) for p in all_perf),
    }

    return {
        "test_id": 1,
        "name": t["name"],
        "dimension": t["dimension"],
        "sub_results": sub_results,
        "perf": avg_perf,
        "thinking_leak": any_thinking_leak,
        "scoring_guide": "See sub-prompt scoring guides.",
        "score": None,   # human-scored — average of 1A, 1B, 1C after shortlist phase
        "notes": f"3 sub-prompts: 1A (Steam/vacuum), 1B (Fiction/timeline), 1C (Concierge/philosophy).",
    }


def run_test_2(model: str) -> dict:
    """Tool schema precision — parallel calls + abstain check."""
    t = TESTS[2]
    print_step(f"Test 2: {t['name']}")

    # Part A: parallel tool calls
    response_a, perf_a = chat(
        model,
        [{"role": "user", "content": t["prompt"]}],
        temperature=t["temperature"],
        tools=t["tool_schema"],
    )

    tool_calls = perf_a.get("tool_calls", [])
    call_count = len(tool_calls)

    # Validate calls
    valid_calls = []
    for call in tool_calls:
        fn = call.get("function", {})
        args = fn.get("arguments", {})
        if fn.get("name") == "get_node_metrics" and "node_id" in args and "metric_type" in args:
            valid_calls.append(args)

    print_ok(f"Tool calls received: {call_count} (valid: {len(valid_calls)})")
    if valid_calls:
        for c in valid_calls:
            print(f"    node_id={c.get('node_id')}  metric_type={c.get('metric_type')}")

    # Part B: no-call check (should NOT trigger tool use)
    no_call_prompt = t["tool_schema_2b"]["prompt"]
    response_b, perf_b = chat(
        model,
        [{"role": "user", "content": no_call_prompt}],
        temperature=t["temperature"],
        tools=t["tool_schema"],
    )
    spurious_calls = perf_b.get("tool_calls", [])
    abstains_correctly = len(spurious_calls) == 0
    if abstains_correctly:
        print_ok("Correctly abstained from tool call on no-call prompt.")
    else:
        print_warn(f"Spurious tool call triggered on no-call prompt: {spurious_calls}")

    thinking_leak = detect_thinking_tokens(response_a) or detect_thinking_tokens(response_b)

    return {
        "test_id": 2,
        "name": t["name"],
        "dimension": t["dimension"],
        "prompt": t["prompt"],
        "response": json.dumps(tool_calls, indent=2) if tool_calls else response_a,
        "response_nocall": response_b,
        "perf": perf_a,
        "tool_calls_received": tool_calls,
        "valid_calls": valid_calls,
        "call_count": call_count,
        "abstains_correctly": abstains_correctly,
        "spurious_calls": spurious_calls,
        "thinking_leak": thinking_leak,
        "scoring_guide": t["scoring_guide"],
        "score": None,
        "notes": "",
    }


def run_test_3(model: str) -> dict:
    """Instruction discipline — constraint following."""
    t = TESTS[3]
    print_step(f"Test 3: {t['name']}")

    response, perf = chat(
        model,
        [{"role": "user", "content": t["prompt"]}],
        temperature=t["temperature"],
    )

    # Auto-check constraints
    bullets = [line.strip() for line in response.split("\n")
               if line.strip().startswith(("•", "-", "*", "–")) or
               (line.strip() and line.strip()[0].isdigit() and "." in line.strip()[:3])]
    forbidden = ["mac", "apple", "memory"]
    found_forbidden = [w for w in forbidden if w in response.lower()]
    ends_semicolons = [b for b in bullets if b.rstrip().endswith(";")]
    word_counts = [len(b.split()) for b in bullets]
    over_limit = [b for b, wc in zip(bullets, word_counts) if wc > 10]

    checks = {
        "bullet_count": len(bullets),
        "correct_count": len(bullets) == 3,
        "forbidden_words_found": found_forbidden,
        "no_forbidden_words": len(found_forbidden) == 0,
        "bullets_end_semicolon": len(ends_semicolons),
        "all_end_semicolon": len(ends_semicolons) == len(bullets) and len(bullets) > 0,
        "over_word_limit": over_limit,
        "all_within_word_limit": len(over_limit) == 0,
    }

    # Auto-score
    passing = sum([
        checks["correct_count"],
        checks["no_forbidden_words"],
        checks["all_end_semicolon"],
        checks["all_within_word_limit"],
    ])
    auto_score = passing  # 0-4, map to 1-5
    score_map = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5}
    auto_score_5 = score_map[passing]

    print_ok(f"Auto-check: {passing}/4 constraints satisfied → provisional score {auto_score_5}/5")
    if found_forbidden:
        print_warn(f"Forbidden words found: {found_forbidden}")

    thinking_leak = detect_thinking_tokens(response)

    return {
        "test_id": 3,
        "name": t["name"],
        "dimension": t["dimension"],
        "prompt": t["prompt"],
        "response": response,
        "perf": perf,
        "constraint_checks": checks,
        "auto_score": auto_score_5,
        "thinking_leak": thinking_leak,
        "scoring_guide": t["scoring_guide"],
        "score": auto_score_5,  # auto-scored
        "notes": f"Auto-scored: {passing}/4 constraints passed.",
    }


def run_test_4(model: str, context_document: str) -> dict:
    """Context needle retrieval."""
    t = TESTS[4]
    print_step(f"Test 4: {t['name']}")

    # Needle is embedded in the document body by generate_context_document,
    # ~750 tokens in. The prompt template just wraps the document — no injection here.
    setup_content = t["prompt_setup"].replace("{context_document}", context_document)
    needle_position = context_document.find("ARCHIVE_KEY: ZULU-9-OMEGA")
    if needle_position == -1:
        print_warn("ARCHIVE_KEY not found in context document — was it generated by this script?")
        print_warn("Delete test4_context.txt and rerun to regenerate with the needle embedded.")
    else:
        approx_token_pos = int(len(context_document[:needle_position].split()) * 0.75)
        print_ok(f"Needle confirmed at ~token {approx_token_pos:,} in context document.")

    messages = [
        {"role": "user", "content": setup_content},
    ]

    # Get a response to the setup (establishes context)
    setup_response, perf_setup = chat(
        model,
        messages,
        temperature=t["temperature"],
        num_ctx=NUM_CTX,
    )

    # Now ask for retrieval
    messages.append({"role": "assistant", "content": setup_response})
    messages.append({"role": "user", "content": t["prompt_retrieval"]})

    retrieval_response, perf_retrieval = chat(
        model,
        messages,
        temperature=t["temperature"],
        num_ctx=NUM_CTX,
    )

    # Auto-check
    retrieved = "ZULU-9-OMEGA" in retrieval_response.upper()
    hallucinated = not retrieved and bool(re.search(r"[A-Z]{2,}-\d+-[A-Z]+", retrieval_response))

    if retrieved:
        print_ok("ZULU-9-OMEGA correctly retrieved.")
    elif hallucinated:
        print_warn(f"Hallucinated a different key: {retrieval_response[:100]}")
    else:
        print_warn("Key not found in response.")

    thinking_leak = detect_thinking_tokens(retrieval_response)

    return {
        "test_id": 4,
        "name": t["name"],
        "dimension": t["dimension"],
        "setup_prompt": setup_content[:200] + "... [truncated]",
        "retrieval_prompt": t["prompt_retrieval"],
        "setup_response_preview": setup_response[:300],
        "response": retrieval_response,
        "perf": perf_retrieval,
        "retrieved_correctly": retrieved,
        "hallucinated_key": hallucinated,
        "context_tokens_approx": len(setup_content.split()),
        "thinking_leak": thinking_leak,
        "scoring_guide": t["scoring_guide"],
        "score": None,  # human review recommended
        "notes": "Auto-check: " + ("PASS — key retrieved." if retrieved else "FAIL — key not retrieved."),
    }


def run_test_5(model: str) -> dict:
    """Intent parsing — JSON output for Planner."""
    t = TESTS[5]
    print_step(f"Test 5: {t['name']}")

    response, perf = chat(
        model,
        [{"role": "user", "content": t["prompt"]}],
        temperature=t["temperature"],
    )

    # Auto-validate JSON
    # Strip markdown fences if present (penalise but still parse)
    clean = re.sub(r"```(?:json)?", "", response).strip()
    fenced = clean != response.strip()

    parsed = None
    parse_error = None
    try:
        parsed = json.loads(clean)
    except json.JSONDecodeError as e:
        parse_error = str(e)

    if parsed:
        has_intent = "intent" in parsed
        has_target = "target" in parsed
        has_logic = "logic" in parsed and isinstance(parsed["logic"], list)
        logic_count = len(parsed.get("logic", []))
        all_branches = logic_count >= 3
        print_ok(f"Valid JSON. intent={has_intent} target={has_target} logic={logic_count} branches")
        if fenced:
            print_warn("Response wrapped in markdown fences — penalise slightly.")
    else:
        print_warn(f"JSON parse failed: {parse_error}")
        has_intent = has_target = has_logic = all_branches = False
        logic_count = 0

    # Auto-score
    if parsed and has_intent and has_target and has_logic and all_branches and not fenced:
        auto_score = 5
    elif parsed and has_intent and has_target and has_logic and all_branches:
        auto_score = 4
    elif parsed and has_intent and has_target and has_logic:
        auto_score = 3
    elif parsed:
        auto_score = 2
    else:
        auto_score = 1

    thinking_leak = detect_thinking_tokens(response)

    return {
        "test_id": 5,
        "name": t["name"],
        "dimension": t["dimension"],
        "prompt": t["prompt"],
        "response": response,
        "parsed_json": parsed,
        "parse_error": parse_error,
        "fenced": fenced,
        "perf": perf,
        "auto_score": auto_score,
        "thinking_leak": thinking_leak,
        "scoring_guide": t["scoring_guide"],
        "score": auto_score,
        "notes": f"Auto-scored. JSON valid: {parsed is not None}. Fenced: {fenced}.",
    }


# ── Report generator ───────────────────────────────────────────────────────────

def latency_score(decode_tps: float) -> int:
    """Convert tokens/sec to 1–5 latency score."""
    if decode_tps >= 80:  return 5
    if decode_tps >= 50:  return 4
    if decode_tps >= 25:  return 3
    if decode_tps >= 10:  return 2
    return 1


def compute_weighted_score(results: list[dict], decode_tps: float) -> Optional[float]:
    """Compute weighted total if all scores are present."""
    dimension_scores = {}
    for r in results:
        dim = r["dimension"]
        score = r.get("score")
        if score is None:
            return None
        if dim not in dimension_scores:
            dimension_scores[dim] = []
        dimension_scores[dim].append(score)

    # Average multi-test dimensions
    averaged = {dim: sum(v) / len(v) for dim, v in dimension_scores.items()}
    averaged["latency"] = latency_score(decode_tps)

    total = sum(averaged.get(dim, 0) * weight for dim, weight in WEIGHTS.items())
    return round(total, 2)


def generate_markdown_report(all_results: dict, run_meta: dict) -> str:
    ts = run_meta["timestamp"]
    lines = [
        "# Concierge Bit Layer — Model Evaluation Results",
        f"**Date:** {ts}",
        f"**Node:** Logos (M1 Max, 64GB Unified Memory)",
        f"**Ollama:** {run_meta.get('ollama_version', 'unknown')}",
        f"**Context window:** {NUM_CTX:,} tokens",
        "",
        "---",
        "",
        "## Summary Comparison Matrix",
        "",
        "| Model | Family | Conv (30%) | Tool (25%) | Instruct (20%) | Context (15%) | Latency (10%) | **Total** | Verdict |",
        "|-------|--------|-----------|-----------|---------------|--------------|--------------|-----------|---------|",
    ]

    for tag, data in all_results.items():
        results = data["test_results"]
        meta = data["model_meta"]

        # Gather scores
        scores = {}
        for r in results:
            scores[r["test_id"]] = r.get("score", "—")

        # Average tests 1 and 5 for conversational
        conv_scores = [scores.get(i) for i in [1, 5] if scores.get(i) is not None]
        conv = round(sum(conv_scores) / len(conv_scores), 1) if conv_scores else "—"
        tool = scores.get(2, "—")
        instruct = scores.get(3, "—")
        context = scores.get(4, "—")

        # Latency from test 1 (warmest path)
        avg_tps = data.get("avg_decode_tps", 0)
        lat_score = latency_score(avg_tps) if avg_tps else "—"
        lat_display = f"{lat_score} ({avg_tps:.0f} t/s)" if avg_tps else "—"

        total = data.get("weighted_total", "—")
        verdict = data.get("verdict", "pending")
        family = meta.get("family", "?")

        lines.append(
            f"| `{tag}` | {family} | {conv} | {tool} | {instruct} | {context} | {lat_display} | **{total}** | {verdict} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Per-Model Results",
        "",
    ]

    for tag, data in all_results.items():
        results = data["test_results"]
        meta = data["model_meta"]
        info = data.get("model_info", {})

        lines += [
            f"### `{tag}`",
            "",
            f"**Family:** {meta.get('family', '?')}  ",
            f"**Size:** {meta.get('size_b', '?')}B  ",
            f"**Backend:** {data.get('backend', 'unknown')}  ",
            f"**Avg decode:** {data.get('avg_decode_tps', 0):.1f} t/s  ",
            f"**Avg prefill:** {data.get('avg_prefill_tps', 0):.1f} t/s  ",
            f"**Thinking token leak:** {'⚠ YES' if data.get('any_thinking_leak') else 'no'}  ",
            "",
        ]

        for r in results:
            score_display = r.get("score", "— (needs human score)")
            lines += [
                f"#### Test {r['test_id']}: {r['name']}",
                "",
                f"**Score:** {score_display} / 5  ",
                f"**Decode:** {r.get('perf', {}).get('decode_tps', '?')} t/s  ",
                f"**Prefill:** {r.get('perf', {}).get('prefill_tps', '?')} t/s  ",
                f"**Tokens generated:** {r.get('perf', {}).get('total_tokens', '?')}  ",
                "",
            ]

            if r.get("notes"):
                lines.append(f"*{r['notes']}*\n")

            if r.get("thinking_leak"):
                lines.append("⚠ **Thinking token leak detected in this response.**\n")

            # Test-specific details
            if r["test_id"] == 1 and r.get("sub_results"):
                for sr in r["sub_results"]:
                    sr_score = sr.get("score", "— (needs human score)")
                    lines += [
                        f"##### Sub-prompt {sr['sub_id']}: {sr['name']}",
                        "",
                        f"**Score:** {sr_score} / 5  ",
                        f"**Decode:** {sr.get('perf', {}).get('decode_tps', '?')} t/s  ",
                        f"**Notes:** {sr.get('notes', '')}  ",
                        "",
                    ]
                    if sr.get("thinking_leak"):
                        lines.append("⚠ **Thinking token leak in this sub-prompt.**\n")
                    lines += [
                        "<details>",
                        "<summary>Full response</summary>",
                        "",
                        "```",
                        sr.get("response", "")[:2000],
                        "```",
                        "",
                        "</details>",
                        "",
                        "**Scoring guide:**",
                        sr.get("scoring_guide", ""),
                        "",
                    ]

            elif r["test_id"] == 2:
                calls = r.get("valid_calls", [])
                abstains = r.get("abstains_correctly", False)
                lines += [
                    f"**Valid tool calls:** {len(calls)} / 2 expected  ",
                    f"**Abstains on no-call prompt:** {'yes' if abstains else '⚠ NO — spurious call'}  ",
                    "",
                ]
                if calls:
                    lines.append("```json")
                    lines.append(json.dumps(calls, indent=2))
                    lines.append("```\n")

            elif r["test_id"] == 3:
                checks = r.get("constraint_checks", {})
                lines += [
                    f"**Bullet count:** {checks.get('bullet_count', '?')} (expected 3)  ",
                    f"**Forbidden words:** {checks.get('forbidden_words_found', []) or 'none'}  ",
                    f"**Semicolons:** {checks.get('bullets_end_semicolon', '?')} / {checks.get('bullet_count', '?')}  ",
                    f"**Over word limit:** {checks.get('over_word_limit', []) or 'none'}  ",
                    "",
                ]

            elif r["test_id"] == 4:
                lines += [
                    f"**Key retrieved correctly:** {'✓ yes' if r.get('retrieved_correctly') else '✗ no'}  ",
                    f"**Hallucinated key:** {'⚠ yes' if r.get('hallucinated_key') else 'no'}  ",
                    f"**Context tokens (approx):** {r.get('context_tokens_approx', '?')} words  ",
                    "",
                ]

            elif r["test_id"] == 5:
                lines += [
                    f"**JSON parseable:** {'yes' if r.get('parsed_json') is not None else '✗ no'}  ",
                    f"**Markdown fences:** {'⚠ yes' if r.get('fenced') else 'no'}  ",
                    "",
                ]
                if r.get("parsed_json"):
                    lines.append("```json")
                    lines.append(json.dumps(r["parsed_json"], indent=2))
                    lines.append("```\n")

            lines += [
                "<details>",
                "<summary>Full response</summary>",
                "",
                "```",
                r.get("response", "")[:2000],
                "```",
                "",
                "</details>",
                "",
                "**Scoring guide:**",
                r.get("scoring_guide", ""),
                "",
                "---",
                "",
            ]

        lines += [
            f"**Weighted total:** {data.get('weighted_total', '— (pending human scores)')}  ",
            f"**Verdict:** {data.get('verdict', 'pending')}  ",
            "",
            "---",
            "",
        ]

    lines += [
        "## Decisions Log",
        "",
        "| Decision | Rationale |",
        "|----------|-----------|",
        "| Logos runs Bit layer only | Not participating in Workbee or quorum at this stage. |",
        "| Ollama as serving backend | Single-user interactive app on Apple Silicon. Metal/MLX path. llama.cpp belongs at Workbee layer. |",
        "| Native function calling required | Bespoke OpenAI-compatible frontend requires proper tool-use schema. |",
        "| ANE support deferred | GPU → CPU path sufficient for now. |",
        "| Quorum rules do not apply | Bit's local model is advisory only. |",
        "",
        "## Open Questions",
        "",
        "- [ ] Does Ollama 0.19 MLX path activate for all tested models, or only Qwen3.5?",
        "- [ ] Q8 variants tested? Note quality delta vs Q4_K_M per model.",
        "- [ ] At what context length does M1 Max start offloading to CPU?",
        "- [ ] Parallel tool call support confirmed per model family?",
        "",
        f"*Generated by bit_eval.py — {ts}*",
    ]

    return "\n".join(lines)


# ── Ollama version check ───────────────────────────────────────────────────────

def get_ollama_version() -> str:
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return "unknown"


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    global OLLAMA_BASE_URL

    parser = argparse.ArgumentParser(description="Concierge Bit Layer Model Evaluation Suite")
    parser.add_argument("--models", nargs="+", help="Specific model tags to test")
    parser.add_argument("--tier", type=int, choices=[1, 2], help="Only test Tier 1 or Tier 2 candidates")
    parser.add_argument("--skip-download", action="store_true", help="Skip pull, only test locally present models")
    parser.add_argument("--test", type=int, choices=[1, 2, 3, 4, 5], help="Run a single test number only")
    parser.add_argument("--context-file", type=str, help="Path to text file for Test 4 (15k+ tokens recommended)")
    parser.add_argument("--timeline-file", type=str, help="Path to timeline .docx or .txt for Test 1B (fiction prompt)")
    parser.add_argument("--philosophy-file", type=str, help="Path to Concierge philosophy .md for Test 1C (hardware prompt)")
    parser.add_argument("--output", type=str, default="BIT_EVAL_RESULTS.md", help="Output markdown filename")
    parser.add_argument("--ollama-url", type=str, default=OLLAMA_BASE_URL, help="Ollama base URL")
    args = parser.parse_args()

    OLLAMA_BASE_URL = args.ollama_url

    print_header("Concierge Bit Layer — Model Evaluation Suite")
    print(f"  Node: Logos (M1 Max, 64GB)")
    print(f"  Ollama: {OLLAMA_BASE_URL}")
    print(f"  Context window: {NUM_CTX:,} tokens")
    print(f"  Output: {args.output}")

    # Check Ollama is running
    print_step("Checking Ollama server ...")
    if not check_ollama_running():
        print_err("Ollama is not running. Start it with: ollama serve")
        sys.exit(1)
    print_ok("Ollama server is up.")

    ollama_version = get_ollama_version()
    print_ok(f"Ollama version: {ollama_version}")
    if "0.19" not in ollama_version and "0.2" not in ollama_version:
        print_warn(
            "Ollama 0.19+ recommended for MLX backend on Apple Silicon. "
            "Performance targets in this suite assume MLX is active."
        )

    # Determine which models to test
    candidates = CANDIDATES
    if args.models:
        candidates = [c for c in CANDIDATES if c["tag"] in args.models]
        # Add any specified models not in the default list
        known_tags = {c["tag"] for c in CANDIDATES}
        for tag in args.models:
            if tag not in known_tags:
                candidates.append({"tag": tag, "family": "unknown", "tier": 1, "size_b": 0})
    elif args.tier:
        candidates = [c for c in CANDIDATES if c["tier"] == args.tier]

    # Determine which tests to run
    test_ids = [args.test] if args.test else list(TESTS.keys())

    # Load context document for Test 4
    context_document = None
    if 4 in test_ids:
        context_document = load_context_document(args.context_file)

    # Load documents for Test 1 sub-prompts
    test1_docs = {}
    if 1 in test_ids:
        print_step("Loading Test 1 documents ...")

        # Timeline (1B — fiction prompt)
        if args.timeline_file:
            p = Path(args.timeline_file)
            if p.suffix.lower() == ".docx":
                test1_docs["timeline"] = load_docx_file(args.timeline_file, "Timeline")
            else:
                test1_docs["timeline"] = load_text_file(args.timeline_file, "Timeline")
        else:
            print_warn("No --timeline-file provided. Test 1B will run without fiction context.")
            print_warn("Pass --timeline-file path/to/Timeline.docx for the full test.")

        # Philosophy doc (1C — Concierge hardware prompt)
        if args.philosophy_file:
            test1_docs["philosophy"] = load_text_file(args.philosophy_file, "Philosophy")
        else:
            print_warn("No --philosophy-file provided. Test 1C will run without Concierge context.")
            print_warn("Pass --philosophy-file path/to/Concierge_Philosophy_v5.md for the full test.")

        # Report context sizes
        for key, text in test1_docs.items():
            if text:
                approx_tokens = int(len(text.split()) * 0.75)
                print_ok(f"  {key}: ~{approx_tokens:,} tokens injected into prompt")

    # Model availability check
    print_step("Checking model availability ...")
    local_models = get_local_models()
    print_ok(f"Found {len(local_models)} models locally.")

    to_pull = []
    to_skip = []
    for c in candidates:
        if model_is_local(c["tag"], local_models):
            print_ok(f"{c['tag']} — already downloaded")
        else:
            if args.skip_download:
                print_warn(f"{c['tag']} — not local, skipping (--skip-download)")
                to_skip.append(c["tag"])
            else:
                print_warn(f"{c['tag']} — not local, will pull")
                to_pull.append(c)

    candidates = [c for c in candidates if c["tag"] not in to_skip]

    # Pull missing models
    if to_pull:
        print_step(f"Pulling {len(to_pull)} model(s) ...")
        for c in to_pull:
            success = pull_model(c["tag"])
            if not success:
                print_err(f"Failed to pull {c['tag']} — skipping.")
                candidates = [x for x in candidates if x["tag"] != c["tag"]]

    if not candidates:
        print_err("No models available to test. Exiting.")
        sys.exit(1)

    print_ok(f"\nReady to test {len(candidates)} model(s): {[c['tag'] for c in candidates]}")
    print(f"\n  Tests to run: {test_ids}")

    # ── Run evaluation ──
    all_results = {}
    run_meta = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ollama_version": ollama_version,
    }

    for candidate in candidates:
        tag = candidate["tag"]
        print_header(f"Evaluating: {tag}")

        model_info = get_model_info(tag)
        backend = detect_backend(model_info)
        print_ok(f"Backend detected: {backend}")

        test_results = []
        decode_tps_list = []
        prefill_tps_list = []
        any_thinking_leak = False

        for test_id in test_ids:
            if test_id == 1:
                result = run_test_1(tag, docs=test1_docs)
            elif test_id == 2:
                result = run_test_2(tag)
            elif test_id == 3:
                result = run_test_3(tag)
            elif test_id == 4:
                result = run_test_4(tag, context_document)
            elif test_id == 5:
                result = run_test_5(tag)

            test_results.append(result)

            tps = result.get("perf", {}).get("decode_tps", 0)
            if tps:
                decode_tps_list.append(tps)
            ptps = result.get("perf", {}).get("prefill_tps", 0)
            if ptps:
                prefill_tps_list.append(ptps)
            if result.get("thinking_leak"):
                any_thinking_leak = True

        avg_decode = sum(decode_tps_list) / len(decode_tps_list) if decode_tps_list else 0
        avg_prefill = sum(prefill_tps_list) / len(prefill_tps_list) if prefill_tps_list else 0

        weighted_total = compute_weighted_score(test_results, avg_decode)

        all_results[tag] = {
            "model_meta": candidate,
            "model_info": model_info,
            "backend": backend,
            "avg_decode_tps": round(avg_decode, 1),
            "avg_prefill_tps": round(avg_prefill, 1),
            "any_thinking_leak": any_thinking_leak,
            "test_results": test_results,
            "weighted_total": weighted_total,
            "verdict": "pending review" if weighted_total is None else (
                "shortlist" if weighted_total >= 3.5 else
                "borderline" if weighted_total >= 2.5 else
                "reject"
            ),
        }

        print_step(f"Summary for {tag}:")
        print_ok(f"Avg decode: {avg_decode:.1f} t/s")
        print_ok(f"Avg prefill: {avg_prefill:.1f} t/s")
        if any_thinking_leak:
            print_warn("Thinking token leak detected — pipeline risk.")
        if weighted_total is not None:
            print_ok(f"Weighted total: {weighted_total} / 5.0")
        else:
            print_warn("Some tests need human scoring — weighted total pending.")

    # ── Generate report ──
    print_header("Generating Report")
    report_md = generate_markdown_report(all_results, run_meta)

    output_path = Path(args.output)
    output_path.write_text(report_md, encoding="utf-8")
    print_ok(f"Report written to: {output_path.resolve()}")

    # Also save raw JSON for further analysis
    json_path = output_path.with_suffix(".json")
    with open(json_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print_ok(f"Raw results JSON: {json_path.resolve()}")

    print_header("Done")
    print(f"\n  Models tested: {len(all_results)}")
    for tag, data in all_results.items():
        total = data.get("weighted_total", "pending")
        verdict = data.get("verdict", "?")
        leak = " ⚠ thinking leak" if data.get("any_thinking_leak") else ""
        print(f"  {tag:30s}  total={total}  [{verdict}]{leak}")

    if any(d.get("weighted_total") is None for d in all_results.values()):
        print(
            "\n  ⚠ Some scores are 'pending' — Tests 1 and 4 require human review.\n"
            "    Open the markdown report, add your scores, and re-run to get final weighted totals.\n"
            "    Or edit the JSON file directly and re-generate the report."
        )


if __name__ == "__main__":
    main()
