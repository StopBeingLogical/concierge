# Concierge: Planning Input for Gemma 4 26B
**Purpose:** Routing decision — which specification gap should be closed next?  
**Context:** Your prior recommendation was assessed against existing state. The core architecture is solid. Three refinement routes remain. Your task: decide which to pursue and justify why.

---

## Current State Summary

**Concierge** is a personal AI task orchestration system for a homelab cluster. Five-layer stack: `Bit → Planner → Router → Foreman → Workbee`.

**What's locked:**
- Job state machine (13 states, 28 transitions)
- Layer interface contracts (Intent Artifact, Execution Plan, Job Spec, Work Chunk, Work Result, all with SHA256 integrity)
- Memory tier architecture (Tier 0–3, write protocols, reference resolution)
- Priority lanes (P0–P3 with preemption rules)
- Workbee and Bit layer contracts

**What's deferred by design:**
- Router internal scheduling algorithm (pending dedicated peer review session)

**What's partially done:**
- Node registry (prose in Hardware Appendix, no formal schema)
- Task Package output contracts (identified as needed, not specced)
- Execution checkpointing (identified as needed, not specced)

---

## Three Routes Forward

### Route A: Node Registry Schema

**Scope:** Formalize how nodes onboard, self-survey hardware, advertise capability, and register.

**Includes:**
- Onboarding flow — what does a node do at boot?
- Capability envelope schema — what fields describe a node's capacity?
- Island-mode rules — Daemon has three GPU islands (normal, burst, all-three). How does each island advertise itself?
- Heartbeat protocol — what does periodic node check-in contain?

**Deliverable:** ~300–500 lines. Schema document suitable for Router design review.

**Dependencies:**
- *Upstream:* None. Can be written independently.
- *Downstream:* Router design session cannot proceed without this. Every scheduling decision depends on knowing what capabilities are available.

**Why it matters:**
- Unblocks the Router design review (scheduled but not yet started)
- Converts Hardware Appendix prose into executable schema
- Clarifies what "capability envelope" means operationally

**Risk/complexity:** Medium. Daemon's burst mode adds complexity — three operating modes that must be advertised differently without confusing the Router.

---

### Route B: Typed Task Package Output Contracts

**Scope:** Define how Task Packages declare their output schema and how Foreman validates at runtime.

**Includes:**
- Output schema declaration language (JSON Schema? Pydantic? TypeScript?)
- Validation trigger — when exactly does validation happen? Before writing to memory?
- Failure semantics — if output doesn't match schema, is the job `failed`, `partial`, or `capability_exceeded`?
- Contract examples — 3–4 real Task Package outputs (text completion, image generation, file transformation, etc.)

**Deliverable:** ~400–600 lines. Extension to Task Package Registry section of Technical Spec, plus schema examples.

**Dependencies:**
- *Upstream:* None. Can be written independently.
- *Downstream:* Task Package authors need this before they can write packages. Foreman implementation depends on this. Bit dashboard needs to display schema validation failures intelligently.

**Why it matters:**
- Execution-time enforcement of "Constraints Are Contracts" philosophy
- Without this, Task Packages are advisory. With it, they're binding contracts.
- Prevents malformed outputs from corrupting downstream work

**Risk/complexity:** Low. Straightforward schema formalization. Precedent exists (Pydantic, JSON Schema ecosystem is mature).

---

### Route C: Execution Checkpointing Protocol

**Scope:** Define how Workbee checkpoints state after completing a step in a multi-step Task Package, enabling resumption if the node fails.

**Includes:**
- Checkpoint format — what data is captured? Outputs only, or intermediate state?
- Store location — where does the checkpoint live? Nextcloud on Atlas? Local filesystem? Both?
- Resumption protocol — how does Foreman signal "resume from checkpoint"?
- Failure modes — checkpoint write fails, corruption, node crash, etc. State machine implications?
- Node migration — can node B pick up a checkpoint left by node A and resume?

**Deliverable:** ~300–400 lines. New subsection in Node and System Management section, or new Resilience section.

**Dependencies:**
- *Upstream:* Requires clarity on Nextcloud MCP integration (already identified in session seed, not yet configured)
- *Downstream:* Long-running inference jobs (multi-step Task Packages) depend on this for resilience. Node failure recovery depends on this.

**Why it matters:**
- Enables graceful degradation — currently, node failure = restart entire job
- Supports long-running multi-step inference pipelines without brittleness
- Differentiator from stateless serverless paradigm — Concierge is stateful and resilient

**Risk/complexity:** Medium-high. Adds complexity to Job Record schema, Foreman logic, and state machine transitions. Checkpointing failure scenarios are non-trivial.

---

## Coupling and Constraints

**Can they be done in parallel?**
- A and B are independent. Could start both.
- C depends on A (needs to know node topology/heartbeat before designing checkpoint store coordination)

**Which unblocks the most downstream work?**
- A unblocks Router design review (highest organizational impact — it's a scheduled session waiting for this)
- B unblocks Task Package ecosystem (needed before any packages are authored)
- C unblocks production reliability (needed for long-running jobs)

**Which is prerequisites for others?**
- A is prerequisite for Router review, which is prerequisite for C (checkpoint coordination across nodes requires Router awareness)
- B is independent but benefits from A (Router's capability scoring will inform which nodes Task Package summaries recommend)

**Implementation readiness:**
- A: Low implementation risk, high documentation clarity needed
- B: Low implementation risk, schema language choice needed
- C: High implementation risk, requires careful state machine analysis

---

## Your Task

**Given this context, which route should be pursued next, and why?**

Reasoning should include:
1. **Dependency analysis** — which unblocks what?
2. **Risk/complexity** — what's the effort-to-clarity ratio?
3. **Organizational impact** — what enables the most follow-up work?
4. **Your assessment of what's missing** — if none of these three feels right, what should be done instead?

You may also propose a **sequencing** (e.g., "A first, then B in parallel with C") or a **hybrid approach** (e.g., "start A, but pause to spike on Router's burst-mode capability advertisement because that's the crux").

---

## Background Context (For Reference)

**Hardware:**
- **Logos** (MacBook Pro M1 Max, 64GB) — Bit workstation, not a compute node
- **Ergaster** (i9-13900HX, 64GB) — Router/Planner control plane
- **Daemon** (i7-12700F, 32GB, three GPUs) — Burst-mode inference node. Has three PCIe islands:
  - Island A: RTX 5060 Ti (x16, 16GB)
  - Island B: Tesla P100 #1 (x8, 16GB)
  - Island C: Tesla P100 #2 (x4, 16GB)
  - Can run Island A alone, or Islands B+C in parallel, or all three in burst mode (ceiling 65B model, 48GB total)
- **Kratos** (Ryzen 7600X, RX 7800 XT, 32GB) — Inference node
- **Atlas** (Ryzen 5700G, 64GB, TrueNAS Scale) — Infrastructure: Nextcloud, Forgejo, Open WebUI, Ollama, Langfuse, SearXNG

**Stack Details:**
- Intent Artifact schema ✅ (UUID v5, confidence, blocking questions, ranked disambigations)
- Execution Plan schema ✅ (steps, dependencies, compute requirements, timeout, on_failure modes)
- Job state machine ✅ (13 states: draft → pending_approval → approved → queued → running → completed/partial/failed, plus Harkanza, Handanza, paused, capability_exceeded, integrity_violation, cancelled)
- Work Chunk schema ✅ (chunk_id, step_id, compute_class, memory_requirement_gb, lease_ttl_ms, on_failure)
- Work Result schema ✅ (result_id, status, output, duration_ms, retries_used, SHA256)
- Memory system ✅ (Tier 0: live job records; Tier 1: recent completions; Tier 2: indexed corpus; Tier 3: long-term archive)
- Integrity chain ✅ (SHA256 from Intent through Result)
- Task Package Registry ⚠️ (concept exists, output contracts not yet defined)
- Node Registry ⚠️ (prose exists, schema not formalized)
- Checkpointing ⚠️ (identified as needed, not specced)
- Router internal algorithm ❌ (deliberately deferred to peer review)
- Bit Application ❌ (scope definition in progress)

**Design Principles:**
- "Constraints Are Contracts" — every layer boundary enforced by typed, versioned, schema-validated artifact
- "Local models are doers, not thinkers" — frontier models own planning; local models execute
- "Wide not deep" — heterogeneous ensemble preferred over single-node depth
- "Each machine runs its own Foreman" — no centralized Foreman; per-system coordination only

---

*Input prepared for: Gemma 4 26B via Open WebUI (no system prompt, default model settings)*
