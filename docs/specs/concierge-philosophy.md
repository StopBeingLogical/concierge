---
title: "Concierge — Architecture, Philosophy, and the Ballet Beneath"
document_type: spec
version: "5.0"
date: "2026-03"
status: current
tags: ['philosophy', 'wide-not-deep', 'ensemble', 'constraints-are-contracts']
---

# Concierge: Architecture, Philosophy, and the Ballet Beneath

*A recontextualization document — written to be read when the ideas have gone cold and need rekindling.*

*v5 — March 2026*

---

## The Central Thesis

Concierge is not an AI assistant. It is not a chatbot with extra steps. It is a **continuously operating cognitive infrastructure** whose purpose is to think on your behalf at all times — not waiting for questions, but pre-positioning answers before questions are formed.

The philosophy is captured in three words: **Wide Not Deep.**

Intelligence in Concierge does not emerge from a single enormous model reasoning alone. It emerges from **structured disagreement** across a diverse ensemble of smaller, specialized models — each with different training lineages, different architectural priors, different failure modes — whose outputs are continuously validated against each other. Agreement across that diversity is a far stronger signal than confidence from any individual model. Disagreement is itself informative: it surfaces uncertainty that monolithic systems would hide behind false confidence.

This is not a compromise made because large models are expensive. It is the deliberate architectural choice that makes the system trustworthy.

### Wide Not Deep — The Correct Formulation

This principle is frequently misread as "prefer larger RAM capacity so nodes can hold larger models." That is wrong. The correct formulation:

**A node that adds a unique specialist voice contributes more than a node that runs a larger version of a model already present.**

A 64GB node running four resident 7B specialists from genuinely different model families contributes four quorum voices. That same node running one 32B generalist contributes one. The ensemble gets smarter from breadth, not depth. Model diversity is the architectural goal. Model size is a secondary concern that only matters when a specific capability genuinely requires larger parameter counts.

The acquisition target for new nodes follows from this: not "how much RAM can hold the biggest model" but "how much RAM can hold the most diverse resident specialist fleet simultaneously."

---

## Constraints Are Contracts

Before describing any component, this principle must be stated clearly because it governs everything else:

**Hardware limits are treated as fixed contracts. All software, routing, and workload definitions must respect them.**

This is not a constraint to be engineered around. It is the design philosophy that makes the architecture coherent. A node's VRAM ceiling, its memory bandwidth, its thermal envelope, its supported instruction sets — these are not problems. They are the terms of the contract that node offers to the system. The Router reads those terms. The Foreman writes work orders that respect them. The Workbee executes within them.

The corollary: **vendor-specific limitations are not architectural issues.** If a vendor or toolchain is problematic for a given task, it is simply not used. No attempt is made to support everything everywhere. The system routes around constraints rather than fighting them.

The deepest expression of this principle: **architecture defines the contract. Implementation fulfills the contract. The concern is contract validity, not fulfillment mechanics.** Whether a Workbee uses CUDA, MLX, ROCm, OpenVINO, or Vulkan to execute a work chunk is irrelevant to the layers above it. Those layers issued a contract. The Workbee's job is to fulfill it.

**Corollary on software ecosystems:** The Workbee backend is an implementation detail. MLX on Apple Silicon, ROCm on AMD, CUDA on NVIDIA, OpenVINO on Intel — all are valid fulfillment mechanisms for the same contract. The Router evaluates contribution against orchestration cost, not ecosystem allegiance. A node running MLX with 614 GB/s unified memory bandwidth is a better High Table verifier candidate than a node running CUDA with 200 GB/s VRAM bandwidth. Bandwidth is the metric. The backend is the plumbing.

---

## The Distributed Fleet

Concierge's original conceit — and its correct one — is that it runs distributed across virtually any hardware that can run the onboarding and execution package.

**The node admission criterion is: contribution > orchestration cost.**

Any machine, regardless of how slow, is a net positive node if it can contribute more value than it costs to coordinate. A Raspberry Pi running a 1B intent classifier at acceptable latency is a legitimate cluster member. A vestigial NPU doing local speculative decoding is a legitimate cluster member. The Strix Halo sovereign node and the RK3588 SBC are architecturally equivalent in spirit — both are black boxes that advertise a capability envelope, accept work chunks appropriate to that envelope, and return results. The Router doesn't care about the brand. It cares about the contract.

This framing inverts the conventional approach to cluster design. You do not acquire nodes based on peak theoretical performance. You ask: what contract can this node fulfill, and does fulfilling that contract contribute more than the Router spends coordinating it?

### The Full Admission Criterion

The admission criterion has three cost components, all of which must be cleared:

**Compute contribution > compute orchestration cost.** Token generation, embedding, classification — the node's output must exceed the Router's scheduling and coordination overhead for that node.

**Maintenance cost must be near zero.** A node that requires ongoing human intervention — custom driver work, manual configuration on each update, persistent troubleshooting — fails the admission criterion on total cost even if its compute contribution is positive. The practical test: is this node zoo-compatible? If the Docker tool zoo can onboard and maintain it automatically, maintenance cost is near zero. If it requires custom human work outside the zoo, that cost is added to the orchestration side of the ledger.

**The node must not introduce correctness risk.** A node that produces subtly wrong outputs that pass quorum validation is worse than a node that fails outright. Nodes with unverified inference backends or known quantization accuracy problems must be validated before admission.

Two corollaries follow from the admission criterion:

**Speed < Capacity.** For general inference ensemble members, RAM capacity is more valuable than token speed. A node that can hold a 32B model resident and serve it at 8 t/s contributes more to the ensemble than a node that screams through a 7B at 30 t/s but cannot touch anything larger. The Router fills the schedule — slow nodes get assigned latency-tolerant P2/P3 work. They are never idle. They just get appropriately matched work chunks. Speed is the metric only for dGPU verifier nodes and the P1 interactive hot path, where the user is actively waiting.

**dGPU nodes are acquired reactively, not speculatively.** Add dGPU capacity when telemetry surfaces queue pressure indicating the iGPU ensemble is the bottleneck. Not before. The Router generates this signal. Trust it.

The hardware already owned is the cluster. The onboarding package self-surveys the hardware it runs on, pulls precompiled tooling matched to the specific capability envelope detected, and advertises that envelope to the Router. New architectures are cross-generated as needed. The system can bootstrap new node types without manual intervention.

Onboarding is designed to be set-and-forget. A node is configured once. After that it is a black box — it surveys its own hardware, pulls its own tooling, advertises its own contract, pulls work it can handle, returns results. The operator does not manage it. The Router does not need to know what's inside it. This is the RonCo principle applied to cluster membership: the node joins, contributes, and disappears into the fabric of the system.

### The Fleet Is Already There

The existing fleet — Logos, Daemon, Atlas, Ergaster, Kratos, Noesis, Gramma, Praxis — is not a collection of machines waiting for Concierge to exist. It is a distributed inference cluster waiting for an orchestration layer. Every node has a role it can fulfill today given the right contracts:

- **Daemon** — Pure AI Processor. Heterogeneous GPU islands for inference and speculative decoding.
- **Ergaster** — Control plane candidate. High CPU core count for Router and Foreman logic.
- **Kratos** — Mid-tier inference worker. ROCm-capable iGPU for 7B–13B batch workloads.
- **Noesis** — Pathfinder node. Tiger Lake Xe iGPU, AVX-512 CPU, always-on background inference.
- **Gramma** — Edge Pathfinder candidate. M3 ANE for classification and embedding.
- **Atlas** — Canonical storage. NIDABA indices, cold corpus, artifact persistence.
- **Logos** — Human surface and MVP validation target.

---

## The Docker Tool Zoo

The RonCo onboarding philosophy requires a concrete implementation mechanism. That mechanism is the Docker tool zoo.

The tool zoo is a curated, versioned pool of containerized inference backends, quantization tools, driver packages, and Workbee adapters. On node onboarding, the self-survey output feeds an automated package selection task that pulls the appropriate container image from the zoo — Ollama with ROCm for AMD iGPU nodes, llama.cpp with CUDA for NVIDIA dGPU nodes, OpenVINO for Intel NPU nodes, MLX for Apple Silicon nodes, RKLLM for RK3588 nodes. The Workbee adapter is baked into the image. No custom human configuration per node.

**The periodic evaluation task** runs on a P3 background schedule — a small specialist model scanning the zoo for new releases, assessing upgrade feasibility against known compatibility matrices for each hardware class, and flagging hard uncertainty cases for human review. Everything that clears the uncertainty threshold ships automatically. Human review is reserved for genuine ambiguity. This task is well within the capability of a small classifier model and does not require a human in the loop except for hard uncertainty cases.

**Zoo-compatibility as the admission criterion test:** A node is zoo-compatible if the onboarding and maintenance process requires no human intervention beyond initial physical setup. If a node requires custom tooling outside the zoo, that maintenance burden is explicitly added to its orchestration cost. Nodes that cannot be zoo-onboarded without persistent human maintenance fail the admission criterion unless their compute contribution is exceptional enough to justify the overhead — and that exception must be explicitly documented as a known deviation.

---

## The Five-Layer Stack

Concierge is organized as a strict layered architecture. Each layer speaks only to the layer directly above or below it. This is not a convention — it is an enforced isolation boundary. A layer that reaches past its neighbors introduces coupling that defeats the entire purpose of the design.

```
┌─────────────────────────────────────┐
│  Bit          (L1 — Interaction)    │
├─────────────────────────────────────┤
│  Planner      (L2 — Intent)         │
├─────────────────────────────────────┤
│  Router       (L3 — Routing)        │
├─────────────────────────────────────┤
│  Foreman      (L4 — Execution)      │
├─────────────────────────────────────┤
│  Workbee      (L5 — Labor)          │
└─────────────────────────────────────┘
```

The isolation property gives the system an important characteristic: **Bit never has to care about how much VRAM a specific node has. A Workbee never has to care about what the user actually asked for.** Each layer is maximally ignorant of the concerns of non-adjacent layers. This is the custom OSI model for distributed AI execution.

**Bit** is the eyes and ears. The only layer that touches the human. It captures intent, manages session and context, operates across four modes (chat, code, snap, xform), and translates human expression into the typed Intent artifact the Planner consumes. Bit has its own local model assistance for initial intent parsing before any work leaves the machine. Bit and the Planner maintain a bidirectional channel — when the Planner detects ambiguity, clarification requests surface back through Bit to the user. Bit is not a dumb terminal. It is an intent interpretation engine with an explicit hard boundary: Bit shall never plan execution, select tools, or invoke work directly. Those are Lock List violations.

**Planner** is the architect of execution. It receives the Intent artifact from Bit and produces Task Packages — fully specified blueprints that define what needs to happen without specifying how or where. It does not know which node will execute a package. It does not know what VRAM any node has. It knows what the work is. The Planner also hosts the Gap Resolver capability — described in its own section below.

**Router** is the brain. Described fully in its own section below.

**Foreman** is the executor's supervisor. It receives routed work from the Router, manages the assignment of work chunks to specific nodes, monitors execution state, handles retries, and assembles partial results into complete outputs. It knows where work is running and whether it is succeeding. On nodes with heterogeneous on-chip hardware, the Foreman also manages local scheduling between NPU and iGPU independently. The Foreman manages the async buffer between draft and verifier streams in Physical Async Speculative Decoding — variable jitter in the RDMA path affects the magnitude of diversity pressure between draft streams, not the correctness of the mechanism. The Foreman's buffer absorbs jitter variance without stalling the verifier.

**Workbee** is the laborer. A stateless executor on a specific node, calling the tools that node provides. It accepts work chunks, runs them using whatever local acceleration is available, and returns results. It is disposable, swappable, and capability-identical within its node class. The Workbee does not reason about routing, priority, or the broader task. It fulfills the contract it was handed.

---

## Bit: The Human Surface

### History

Bit began in late January 2026 as a more ambitious system called the Concierge Shell — an execution control plane that would directly run tool calls, manage a ToolRunner, and interface with a separate Router allocator for worker selection. The original v0.1 spec defined a nine-state machine from IDLE through COMPLETE/FAILED, four execution-oriented mode presets (plan_then_act, act_only, verify_only, chat_only), and direct Bit authority over tool invocation. Bit was the system.

This design was reconceived through a series of architecture synthesis sessions in late January 2026, ultimately producing the v1.1 canonical spec and the Lock List. The critical architectural shift was stripping all execution authority from Bit and assigning it entirely to Workbee. Bit went from execution control plane to human-facing shell only. The Lock List formalized this as a hard constraint: violations are architecture errors, not bugs.

The second major evolution was the adoption of the Intent artifact as a spec-first foundation for job creation. In v0.1, JobSpec was authored directly from user text with intent as a classification field. By v0.2, the schema was restructured to require a separately authored, mode-neutral Intent artifact as a mandatory precursor to any job. This enforced the principle that a job spec must be derived from a deterministic artifact, not from mode-conditioned conversation. The IntentSynthesizer was implemented as a fully rule-based engine to guarantee this determinism, explicitly rejecting LLM-driven synthesis — whose output cannot be hashed to a stable identifier.

The transition from concept to code began in early February 2026. Most source files carry modification dates of 2026-02-04 through 2026-02-07, indicating a focused initial implementation sprint. A 10-task sequential roadmap with estimated 64-80 hours of effort guided this phase. Tasks 1-9 were substantially completed. Task 10, the full TUI, is partial. A WorkbeeSim was built concurrently to enable end-to-end testing of the full loop without a real Workbee service.

### Current State

Bit is a Python package of approximately 85 source files providing both a CLI (Typer-based) and a TUI (Textual-based) as the human-facing surface of the Concierge system. The core loop — workspace bootstrap, mode selection, intent synthesis, job creation, plan retrieval, user approval, execution monitoring, artifact browsing — is implemented and exercised against a local WorkbeeSim that simulates Workbee responses with deterministic fixture scenarios.

The primary components are:

- **Workspace** — the hard authority boundary. Creates and validates a six-subdirectory structure (context, jobs, artifacts, logs, cache, scratch). No process reads or writes outside it without explicit mount approval. Provides SHA256 hash_content() as the canonical hashing utility for all artifact identity operations.
- **IntentSynthesizer** — rule-based, not LLM-driven. Produces deterministic Intent artifacts from user text. Three-component weighted confidence score: keyword match (0.3), semantic clarity (0.4), mode category fit (0.3).
- **SessionManager** — mode state, recent jobs, 0600-secured JSON persistence.
- **JobManager** — YAML persistence, lifecycle state machine, approval audit trail.
- **Planner** — local package matching for WorkbeeSim use. Flags ambiguity when multiple packages match within 0.1 confidence delta.
- **LLMClient** — async adapter supporting Ollama (qwen2.5:14b default, localhost:11434) and llama.cpp (OpenAI-compatible, localhost:8000). Output is always advisory — it may draft and suggest, never execute or commit.
- **ApprovalLog** — append-only approval records providing the client-side audit trail.

The CLI is the primary interaction surface and is more complete. The TUI implements the cockpit layout — chat viewport, context panel, job status panel, action bar, modal overlays — but is partially implemented. 21 test files provide substantial unit and integration coverage.

The four defined interaction modes are: **chat**, **code**, **snap**, and **xform**.

### Technical Architecture

The most architecturally significant technical choice in Bit is the two-layer identity scheme for Intent artifacts. The `intent_hash` (SHA256 of canonical content) provides content addressability — the same intent text always produces the same hash. The `intent_id` (UUID v5 derived from that hash) provides a stable, opaque identifier for cross-references in job specs.

This scheme creates a cryptographic integrity chain: intent → job spec → approval → execution. `JobManager.verify_intent_hash()` performs this check at job creation time. Any tampering with an artifact at rest breaks the verification. The same pattern applies to job specs via `job_spec_hash`.

When the Foreman receives a run start request, it receives the full approval attestation (approved_at, approved_by, approval_note) in the POST body. The approval decision made in Bit's local approval gate is cryptographically attested in the run start request, creating a verifiable audit record on both the client (job.yaml approvals list) and the server (run start request body).

The Bit↔Workbee interface is HTTP JSON over localhost with eight defined endpoints: health check, submit job, create plan, start run, get run state, stream events, stream logs, and list/fetch artifacts.

### The Lock List

The Lock List is the formal expression of what Bit is not allowed to do. Violations are architecture errors, not implementation bugs.

- Bit shall never plan execution
- Bit shall never select tools for a task
- Bit shall never invoke work directly
- Bit shall never mutate memory or state owned by layers below it
- Local LLM output in Bit is always advisory — it may draft and suggest, never execute or commit

### Known Gaps and Open Questions

The current implementation is behind the spec in several areas representing the known delta between Phase 1 and the full design: Intent model missing candidate_inputs, candidate_outputs, and provenance object; ranked multi-intent structure with clarification questions not implemented; several Job schema fields from v0.2 not yet present; JobStatus.BLOCKED undefined; workspace.json/bit.toml discrepancy; no Apple ANE/MLX backend; no Siri integration stub.

An open boundary concern: bit/worker.py imports WorkerNode and start_worker from the Workbee layer. If start_worker is ever invoked from Bit-owned code paths, this is a Lock List violation requiring resolution before transitioning from WorkbeeSim to real Workbee.

---

## The Hardware Topology

Concierge runs on a heterogeneous hardware fleet. Heterogeneity is not a limitation to be designed around — it is the substrate the architecture requires. Different nodes have genuinely different performance profiles suited to different roles, and the system routes to the right substrate for each task type rather than pretending all nodes are equivalent.

**Daemon** is the Pure AI Processor. Headless, never touched after setup. Three genuinely distinct compute islands:

- **Discrete GPU islands** — the workhorses. Heavy concurrent inference, verifier nodes for speculative decoding. Tesla P100s carry HBM2 with a 4096-bit memory bus — enormous bandwidth advantage for large-context memory-bound workloads. RTX 5060 Ti carries GDDR7 suited to rapid speculative drafting.
- **iGPU / background async island** — embarrassingly parallel, latency-tolerant background work. Continuous NIDABA embedding generation, cold corpus annotation passes.
- **NPU — the Pathfinder** — tiny models entirely on-die. No memory round-trips. Intent tagging, routing, cache envelope matching, pre-warming GPU attention windows.

**Logos** (M1 Max MacBook Pro) is the human surface and MVP validation target. Also the first full-stack deployment target — the entire five-layer suite must run end-to-end here before scaling to the homelab.

**Atlas** is canonical storage — system memory layers, NIDABA vector indices, the cold corpus.

### Node Self-Advertisement and the Pull Model

Nodes advertise their own capability envelope to the Router on boot: CPU cores and speed, GPU VRAM and compute capability, NPU or ANE availability, supported instruction sets, local spec-dec capability class, and supported backends. The Router collects these into a live worker capability registry.

The capability envelope includes:

- **Compute class** — iGPU tier, dGPU tier, CPU-only, Apple Silicon unified memory tier
- **Memory capacity** — total addressable RAM for inference
- **Memory bandwidth** — GB/s, the binding metric for token generation
- **NPU class** — none / vestigial / capable / strong
- **Local spec-dec** — available or unavailable, and drafter quality class
- **Supported backends** — CUDA, ROCm, Vulkan, OpenVINO, RKLLM, ONNX, MLX
- **Zoo compatibility class** — the Docker tool zoo package that onboards this node

Work distribution follows a **pull model**: the Router populates a task chunk pool and workers pull chunks appropriate for their declared capacity. The system adapts to real hardware state rather than assumed hardware state.

### Network Topology Principles

Work chunks are metadata-heavy and payload-light. The Router is sending job contracts and small context payloads, not streaming model weights per task. Models load once and stay resident. At this payload profile, latency and reliability are the binding network constraints — not throughput. A low-latency 1 GbE link is more valuable than a high-throughput 2.5 GbE link with higher baseline round-trip time.

The exception is artifact egress — completed jobs producing large outputs that need to move to Atlas. This is an async P2/P3 path, not the hot scheduling loop, so throughput matters there but does not affect interactive SLA.

---

## The Pathfinder Role

The Pathfinder role is not sovereign-node-specific. It is a role any node can fulfill, and it operates independently at the node level when an NPU or ANE is available.

The Pathfinder handles: intent classification, embedding generation, routing pre-computation, cache envelope matching, and pre-warming iGPU or GPU attention windows before full models are engaged. It answers the question "what kind of work is this?" before any expensive compute is committed.

**Any node with an NPU or ANE can run Pathfinder work regardless of TOPS rating.** A node that cannot contribute meaningfully to 13B inference can own Pathfinder for the cluster and be net positive without ever running a large model.

**Pathfinder and Wake-on-LAN:** The Pathfinder's always-on status gives it the responsibility for node readiness management. When a high-priority intent is classified, the Pathfinder triggers Wake-on-LAN signals for Tier 1 nodes that may be in low-power states — before the job reaches the Router. This eliminates the cold-start penalty on P1 bursts. By the time the Router assigns the work, the target node is already initializing. The Pathfinder acts as a forward scout for the Router, not just a classification engine.

For individual nodes with both NPU and iGPU, the local Foreman schedules Pathfinder work on the NPU and inference work on the iGPU independently — they operate on separate hardware with separate schedulers.

---

## Local Async Speculative Decoding on Every Node

Any node with an NPU — including nodes with vestigial 13 TOPS NPUs — is capable of running local async speculative decoding without any cluster-level coordination.

The mechanism: the local Foreman loads a small draft model on the NPU and runs it asynchronously alongside the iGPU verifier. The NPU and iGPU operate on independent hardware with independent schedulers. The physical latency difference between them creates natural desynchronization. No software synchronization primitives are needed. No seed management. No mutex contention.

*The local hardware latency differential is the lock.*

From the Router's perspective, nothing has changed. The node accepted a work chunk and returns a result. Whether that result was produced by iGPU-only or NPU+iGPU local async spec-dec is an implementation detail of the Workbee, invisible to the layers above.

The break-even threshold is very low. Even a bad drafter with high token rejection rate is net positive if it occasionally proposes an acceptable token that saves an iGPU generation step — at near-zero additional power cost, almost any positive acceptance rate clears the bar.

---

## The Router: The Most Important Component

The Router is not a dispatcher. It does not round-robin. It is the brain of the entire system, and everything else is an appliance it operates.

The Router holds simultaneously:

- Real-time measured latency state for every compute island
- Rolling history for prediction accuracy and self-correction
- SLA contracts for every in-flight task
- Drain state awareness — which islands are mid-swap and unavailable
- Cross-island validation chain state — which model family generated what, which have validated, what is still pending
- Predictive flush logic — anticipating model swap needs before they become urgent
- SLA violation escalation paths
- A feedback loop comparing predicted versus actual latency, continuously refining its own world model
- The live node capability registry built from self-reported worker advertisements
- Local spec-dec capability class per node for SLA prediction accuracy
- **Capability ceiling awareness** — the Router knows the maximum model size the current fleet can serve, either on a single node or via temporary sharding. When a task exceeds the fleet's capability ceiling, the Router returns a graceful incapability signal rather than attempting the task with inadequate capability and producing a confidently wrong answer.
- **Training lineage metadata** — for quorum validation, the Router tracks the known training lineage of each model in the ensemble. Cross-family is necessary but not sufficient. The Router preferentially assigns quorum validation to models with genuinely distinct training lineages, not just different model family names. Disagreement between models with distinct lineages carries more epistemic weight than disagreement between models that share heavy training data overlap.

The CPU is the Router, and the GPUs are its instruments. The performance cores on Daemon's i7-12700F belong to the Router, pinned and process-isolated, treated as near-realtime. A stalled Router under load causes cascading backlog across all islands simultaneously.

**The Router's prediction accuracy is the ceiling of the entire system's performance.**

---

## Jobs Are State Machines

Every unit of work in Concierge is a **state machine**, not a function call.

```
planned → queued → running → progress → paused → resumed → completed
                                                           → failed
                                                           → cancelled
                                                           → capability_exceeded
```

The `capability_exceeded` terminal state is new in v5. When the Router determines that a task requires reasoning depth or model size that the current fleet cannot provide — either on a single node or via temporary sharding — the job transitions to `capability_exceeded` with a structured explanation. The system does not attempt the task with inadequate capability. Graceful incapability is better than confident mediocrity.

Priority lanes:

- **P0 — Control Plane:** Router instructions, node health checks, drain signals. Always runs.
- **P1 — Interactive:** Anything the human is actively waiting for. Preempts P2 and P3.
- **P2 — Batch:** Background processing, corpus analysis, prefill generation. Yields to P1.
- **P3 — Experiment:** Speculative computation, autonomous synthesis, self-improvement. Slack capacity only.

Failures are legible. The system does not produce wrong answers when a node fails — it produces incomplete jobs with failure states. Correctness and capability are explicitly decoupled.

---

## The Degradation Principle

**Loss of an AI node reduces performance or capability, not system correctness.**

When a node goes offline, the Router's capability registry updates immediately. Tasks reroute, queue, or fail gracefully with explicit state. The system explicitly reduces what it can do while maintaining the validity of what it does do.

You do not add nodes to increase correctness. You add nodes to increase the speed and capability ceiling. Each additional node raises the performance floor without changing the correctness floor.

---

## The IQ Ceiling

The maximum model size that the fleet can serve — either resident on a single node or temporarily sharded across nodes with acceptable inter-node latency — defines the system's reasoning ceiling for tasks that require deep parameter-count-dependent capabilities.

**This is a hard architectural limit that the system lives within honestly.**

Four 7B models in quorum cannot perform causal inference that requires 70B parameter depth. No amount of ensemble diversity changes this. The system does not hide this limitation — it surfaces it explicitly via the `capability_exceeded` job state.

**Temporary sharding as a practical ceiling raiser:** The Router maintains a shard candidate pool calculation — which nodes can be combined to host a model that exceeds any single node's capacity, at what inter-node latency cost, and whether that latency cost is within acceptable bounds for the task's SLA class. When the IQ ceiling check fires, the Router first attempts temporary sharding before returning `capability_exceeded`. If a 34B model can be sharded across Daemon's P100s and Kratos at acceptable latency, the effective ceiling rises to 34B for that task without any hardware change.

The IQ ceiling is not a failure. It is an honest contract term. The system knows what it can do and says so.

---

## The Task Package: Atomic Unit of Work

The Task Package is what the Planner produces and the Foreman consumes — a fully specified contract for a unit of work. Nothing downstream should need to ask the Planner for clarification.

A complete Task Package contains: identity and versioning, intent matching, preconditions and feasibility, inputs, defaults and preferences binding, approval policy, pipeline with dependency declarations, artifacts and output specification, verification and acceptance criteria, logging and provenance, memory hooks, security and constraints, and failure handling and recovery.

Two invariants apply to all packages: runtime JSON must validate against the package's declared schema, and runtime JSON may not override package contract rules.

**Prompts are system-fed, not human-authored at runtime.** By the time a Workbee sees a prompt, it has been through the full specification pipeline.

---

## Quorum: The Validation Mechanism

No output from Concierge is accepted on the authority of a single model.

**No same-family validation.**

A generation from Model Family A must be validated by Model Family B or C before Family A can provide tertiary validation. Different families fail in different directions. When two genuinely different families agree, that agreement carries real epistemic weight. When they disagree, the disagreement is signal — an uncertainty flag surfaced rather than papered over.

### Cross-Family Is Necessary But Not Sufficient

Architectural diversity across model families is necessary but does not guarantee epistemic independence. Multiple model families trained heavily on the same open-source datasets — Common Crawl, The Pile, and similar massive corpora — may agree on the same false facts because they learned from the same sources. Architectural diversity does not immunize against training data homogeneity.

The quorum rule therefore has two requirements:

**Architectural diversity:** No same-family validation. This is the hard constraint.

**Training lineage diversity:** The Router preferentially selects quorum validators with genuinely distinct training data emphasis. Models with known distinct lineages — different domain emphasis, different language mix, different curation philosophy — are preferred over models that share heavy training data overlap even if they are different architectural families. This is a soft preference expressed through the Router's model selection, not a hard prohibition. When training lineage metadata is uncertain, the Router falls back to architectural family diversity alone.

### High Table Escalation on Uncertainty

The High Table verifier tier is not fixed. When quorum validation produces a high uncertainty signal — strong disagreement between validators, low confidence across the ensemble, or task complexity signals that exceed the ensemble's confident capability — the Router escalates to a larger High Table verifier.

The escalation path: Council of Squires (7B-13B specialists) → High Table verifier (32B+) → capability ceiling check. The escalation is triggered by the quorum uncertainty signal, not by task type alone. The Router decides dynamically which verifier tier the current task warrants.

The quorum is the system's immune response. It is the structural solution to correlated hallucination — the failure mode where architectural biases produce confident wrong outputs that another model from the same family will enthusiastically confirm.

---

## Speculative Decoding: The Speed Mechanism

A draft model generates candidate tokens ahead of the verifier. The verifier checks them in parallel with a single forward pass. Accepted tokens advance the sequence at drafter cost. Net result: output at approaching drafter speed while maintaining verifier quality.

### Physical Async Speculative Decoding

Two draft models feeding one verifier — one local (zero latency), one remote (RDMA, 10-30 microseconds). Those streams are naturally desynchronized by a physical constant.

*The latency is the lock.*

Conceptually, this is a hardware timer used as a randomizer seed. The propagation delay of a signal across a wire is a physical constant — deterministic from physics, free, requiring no coordination, producing exactly the diversity pressure needed. The remote draft operates on marginally stale verifier state, exploring a slightly different probability neighborhood.

**On variable jitter:** Consumer-grade hardware exhibits variable RDMA latency, not static latency. This is not a vulnerability in the PASD mechanism — it is irrelevant to the mechanism's correctness. PASD does not require static latency. It requires that latency exists and is non-zero. Variable jitter means variable staleness, which means variable diversity pressure magnitude — not stalling, not correctness errors. The Foreman manages the async buffer between draft and verifier streams, absorbing jitter variance without blocking the verifier. A wider jitter envelope produces more diversity pressure on average, not less. The mechanism degrades gracefully toward zero diversity pressure only if jitter approaches zero, which is not a realistic failure mode on consumer networking.

The entire distributed speculative decoding literature treats network latency as overhead to minimize. Concierge inverts this: latency is the designed synchronization mechanism. This inversion does not appear in the published literature.

### Multi-Drafter Speculative Decoding (MDSD)

The Council of Squires. Multiple specialist drafters propose simultaneously. The High Table verifier selects from a richer candidate distribution. Acceptance rate goes up. Verifier idle time goes down. The system gets smarter as the ensemble gets more diverse.

MDSD applies at both cluster level (multiple nodes as drafters) and node level (NPU as local drafter, iGPU as local verifier). The same architectural primitive operates at both scales.

---

## The Gap Resolver

When the Planner receives a task it cannot fully specify — because knowledge or tooling required to complete it is missing from the current corpus or capability envelope — it does not return an error. It returns a Gap Resolution Plan.

**Two gap types:**

**Knowledge gap:** The corpus doesn't contain information required to complete the task. The Gap Resolver identifies the relevant domain, selects the appropriate sources from the approved sources list, queues a corpus population task at P2/P3 priority, and either waits for population to complete before proceeding (for P1 interactive tasks) or proceeds with available knowledge and flags the gap in the output. The corpus is richer after the resolution. The same gap does not recur.

**Capability gap:** The system cannot complete the task with current tooling. The Gap Resolver surveys the capability landscape — existing open source projects, forkable codebases, relevant libraries, available APIs — and presents structured options to the human: fork an existing project and add the requested components, begin a distributed build task across the cluster as P3 background work, recommend an alternative approach given current constraints. The human makes the decision. The system did the legwork.

**The approved sources list** is a first-class configuration artifact — curated, versioned, human-maintained. The Gap Resolver never reaches outside the approved sources list without explicit human authorization. No dark web accidents. No hallucinated citations. The boundaries are defined and auditable.

**Priority assignment:** Gap resolution work follows standard P0-P3 lanes. Background by default. The human can escalate resolution work to P1 if the gap is blocking an interactive task.

**NIDABA enrichment as a side effect:** Every resolved knowledge gap enriches the personalized corpus. The resolution result persists in the knowledge base at the appropriate relevance weighting for this user. The system becomes incrementally smarter through use, not just through explicit corpus curation.

**Capability gap build tasks** that involve distributed code synthesis across the cluster are inherently P3 workloads — all hands on deck only when explicitly escalated by the user. The cluster runs the build in background slack capacity and surfaces results when complete.

---

## The Ballet: Maximum Utilization as Architecture

Idle compute is wasted compute. Automatic reassignment to MDSD during latency interleave SLA periods eliminates idle as a scheduling artifact. There is no idle state.

*Every dancer has a default movement they return to when not in a named sequence. The choreography fills the stage continuously. External cues redirect dancers into named sequences without interrupting the overall flow. When the cue resolves, they return to the default movement seamlessly.*

The chaos is not actual chaos. It is a very deep schedule that never has a gap.

### The VRAM Fragmentation Problem — A Concrete Illustration

A P100 running a 13B model consumes 12GB of its 16GB HBM2. The remaining 4GB sits idle — too small for a 7B model that needs 5GB. A 7B task waits three minutes while 4GB of the fastest memory in the cluster goes unused.

The Router sees the queue depth growing. The recommendation surfaces: add small 8GB relief cards to absorb the 7B queue. The P100s run 13B work continuously. The small cards handle small work. No node blocks any other node.

This is how hardware acquisition decisions are made — by observing actual queue pressure through telemetry and adding capacity targeted at exactly that bottleneck.

---

## NIDABA: The Personalized Knowledge System

Standard RAG retrieves what is semantically similar for an average person. NIDABA retrieves what is relevant for this specific person — indexed against a personalized embedding space derived from the user's own corpus, thinking patterns, and decision history over time.

**Cold corpus** — Wikipedia, documentation, research papers. Does not need to be kept warm. Cold retrieval is a vector lookup — microseconds. The warmth value was always in the index quality, not the residency.

**Directed second-pass annotation** — the prefill cache process continuously annotates the cold corpus based on current trajectory. Queries hit a pre-narrowed candidate set.

**Hot context cache** — continuously updated KV cache for the most likely next queries. Perceived latency approaches zero on anything correctly anticipated.

### The Knowledge Boundary Contract

External data may be consulted at runtime but not persisted beyond derived values. Only embeddings, summaries, extracted facts, and relevance scores persist. Raw external documents do not enter the canonical knowledge store. This is both a privacy boundary and a data hygiene principle.

### NIDABA and the Gap Resolver

The Gap Resolver enriches NIDABA as a side effect of every resolved knowledge gap. This creates a continuous learning loop: the user encounters a task, the system identifies a knowledge gap, the gap is resolved from approved sources, the resolved knowledge is indexed into NIDABA at appropriate personal relevance weighting. The next time the user encounters a related task, the gap no longer exists. The system's personalized knowledge base grows through use rather than requiring explicit curation.

---

## The Inbox Problem and Its Resolution

A single human user cannot generate enough interactive demand to keep a fully-loaded inference system at high occupancy. The resolution: decouple human interaction rate from hardware utilization rate with continuous autonomous background work.

Natural sources that do not manufacture busywork:

- **Corpus analysis** — continuous embedding and annotation passes over the cold corpus
- **Speculative prefill generation** — continuously computing likely next queries and pre-positioning answers
- **Autonomous code synthesis** — exploring solution spaces speculatively, parking results for the user's return
- **Self-generated training signal** — building a local dataset of what works on these specific workloads
- **Gap Resolver background tasks** — resolving knowledge gaps queued from previous sessions, enriching NIDABA

The interactive exchange is the last mile of a much longer pre-computation that has been running in the background.

---

## The Brutal Critique Pipeline

A purpose-built adversarial critique pipeline that forces ego-detached, failure-oriented analysis of high-stakes specifications before they become implementation commitments. It runs on proposed contracts, not on running code. By the time implementation begins, the contract has survived adversarial scrutiny.

This is not a safety net. It is a design discipline.

---

## The MVP Strategy: Logos First

The full five-layer stack targets a single-machine deployment on Logos as its first milestone. A single-node system is treated architecturally as multi-node in waiting. When the homelab comes online, the deployment changes but the architecture does not.

The schema and contracts come before the code. Every interface, every message format, every state machine transition is specified as a contract before a line of implementation is written. The contracts are the system. The code fulfills them.

---

## Transcript Contributions

### Inference Benchmarks and Hardware Characterization

The Tesla P100 outperforms the RTX 5060 Ti on token generation (approximately +22%) due to HBM2's 4096-bit memory bus — despite being a decade-older architecture. Token generation is almost entirely memory-bandwidth-bound, not compute-bound. This is why memory bandwidth is the primary metric for evaluating verifier and High Table nodes — not TOPS, not clock speed, not generation architecture.

### Physical Async Speculative Decoding — Origin

The most architecturally novel concept in the Concierge canon emerged from analyzing a dual-machine Apple Silicon topology. Instead of trying to synchronize two draft streams, let the RDMA latency naturally desynchronize them. The physical delay becomes the async separator. The two draft streams explore different probability neighborhoods not because of seeded randomness but because one operates on verifier state that is 10-30 microseconds stale. That staleness introduces natural diversity pressure. This was later generalized into Physical Async Speculative Decoding as an architectural primitive applicable wherever hardware latency exists between draft and verifier paths.

### Local NPU Async Spec-Dec — Origin

The insight that vestigial NPUs are viable local drafters emerged from asking whether the Pathfinder role could operate locally on each node rather than as a cluster-wide assignment. The answer was yes — and further, that any NPU regardless of TOPS rating provides free local speculative decoding because the local hardware latency differential between NPU and iGPU is itself the async separator. Same primitive, two scales.

### Wide Not Deep — Correction

The correct formulation of Wide Not Deep was clarified: model diversity is the goal, not model size. Four resident 7B specialists from different families contribute four quorum voices. One 32B generalist contributes one. The ensemble gets smarter from breadth.

### Apple Silicon as High Table Verifier Candidates

Apple Silicon M-series chips — specifically M4 Max and future M5 Max — are legitimate High Table verifier candidates. The M4 Max delivers approximately 614 GB/s unified memory bandwidth, the highest bandwidth of any consumer node class evaluated. For memory-bandwidth-bound token generation on large models, this bandwidth advantage makes Apple Silicon the fastest available verifier hardware at the consumer scale. The MLX backend is a valid Workbee fulfillment mechanism. The Router evaluates bandwidth and unified memory capacity — not software ecosystem. An M4 Max or M5 Max Mac Studio at 128GB unified memory running MLX is the strongest single High Table verifier node available at consumer scale as of 2026.

### Gemini Adversarial Critique — Response Summary

A structured adversarial critique identified six vulnerability areas. The v5 canon addresses each:

**PASD variable jitter** — addressed by the Foreman async buffer clarification. Jitter affects diversity magnitude, not correctness.

**Quorum data homogeneity** — addressed by the two-requirement quorum rule. Cross-family architectural diversity is necessary but not sufficient. Training lineage diversity is the deeper goal.

**Reasoning threshold ceiling** — addressed by the High Table escalation mechanism and the IQ ceiling principle. The system escalates dynamically on uncertainty signals and surfaces incapability honestly rather than hiding it.

**Orchestration cost of heterogeneity** — addressed by the Docker tool zoo and the expanded admission criterion. Zoo-compatibility is the practical test for maintenance cost.

**Cold-start penalty on P1 bursts** — addressed by the Pathfinder WoL responsibility. The always-on Pathfinder triggers wake signals on high-priority intent classification before the job reaches the Router.

**Living Compiler** — reframed as the Gap Resolver. Not arbitrary driver generation — structured capability and knowledge gap resolution from approved sources, with the human making decisions on capability gaps. More conservative, more buildable, more honest.

---

## The True Benchmark

The correct benchmark for Concierge is not: *can it run a 70B model faster than a single large GPU?*

The correct benchmark is: *can it run any model that produces the same output quality at comparable or better speeds across a diverse workload portfolio?*

A mesh running twenty resident 14B specialist models is not competing against one 70B model. It is competing on quality achievable at a given speed budget across a given workload distribution. The resident specialist ensemble achieves comparable quality through diversity rather than raw parameter count, across twenty parallel streams rather than one sequential stream.

---

## What Concierge Is

Concierge is a **continuously self-utilizing cognitive infrastructure** with:

- Contracts as the primary design artifact — schemas before code, always
- Five-layer strict isolation — Bit through Workbee, each layer ignorant of non-adjacent concerns
- Bit as a hard-bounded human surface — intent capture and translation only, never execution
- The Lock List as an enforced architectural boundary on Bit's authority
- SHA256 integrity chain — intent → job spec → approval → execution
- Distributed fleet architecture — any node whose contribution exceeds orchestration cost is a valid member
- Hardware constraints treated as contract terms, not problems to solve
- Backend ecosystem irrelevant to architecture — the Workbee fulfills the contract using whatever the hardware provides
- Wide Not Deep as model diversity, not model size — breadth of quorum voices over depth of individual capability
- Personalized knowledge retrieval calibrated to a specific cognitive fingerprint
- Speculative pre-computation running permanently ahead of human attention
- Cross-family quorum as structural hallucination prevention — same-family validation forbidden
- Training lineage diversity as the deeper quorum goal — architectural diversity necessary but not sufficient
- High Table escalation on uncertainty signals — verifier tier is dynamic, not fixed
- IQ ceiling as architectural honesty — capability_exceeded is a valid job state, graceful incapability over confident mediocrity
- Temporary sharding as a practical ceiling raiser before returning capability_exceeded
- Jobs as explicit state machines with lifecycle, priority lanes, and legible failure
- Automatic idle elimination through MDSD backfill during SLA interleave windows
- Local async spec-dec on every NPU-equipped node regardless of TOPS rating
- The Pathfinder role distributed across any capable node, responsible for WoL readiness management
- Cold corpus with hot index paths rather than expensive warm residency
- Physical async synchronization using hardware latency as a structural primitive — the latency is the lock
- Foreman async buffer absorbing RDMA jitter without blocking the verifier
- Network latency over throughput — work chunks are metadata-heavy, payload-light
- Node self-advertisement and pull-based work distribution with extended capability envelope
- Docker tool zoo as the onboarding mechanism — zoo-compatibility as the maintenance cost test
- Periodic tool zoo evaluation at P3 — automated upgrade assessment, human review for hard cases only
- Gap Resolver as a named Planner capability — knowledge gaps and capability gaps handled structurally
- Approved sources list as a first-class versioned configuration artifact
- NIDABA enrichment as a side effect of every resolved knowledge gap
- Graceful capability degradation without correctness degradation
- Telemetry-driven hardware acquisition decisions based on observed queue pressure
- Logos-first single-node validation before homelab scale-out
- Sovereign node window shopping as a useful detour that confirmed the distributed fleet was always the correct architecture

The chaos visible from the outside — dozens of models running simultaneously, work passing between hardware islands, continuous background processing with no clear trigger — resolves, when viewed from above, into a ballet. Every dancer has a default movement. The choreography fills the stage continuously. The schedule has no gaps.

The mainframe instinct is correct: expensive hardware justifies itself through continuous utilization. Every idle cycle is waste. The inbox feeds itself.

---

*Document compiled from architecture conversations, hardware research sessions, contract design sessions, code analysis, adversarial critique responses, and philosophy discussions spanning early 2026. Core concepts: Wide Not Deep · Constraints Are Contracts · Backend Ecosystem Irrelevance · Distributed Fleet · Node Admission Criterion (Compute + Maintenance + Correctness) · Zoo-Compatibility · Docker Tool Zoo · Five-Layer Isolation · Bit Lock List · Intent Artifact as Deterministic Foundation · SHA256 Integrity Chain · Physical Async Speculative Decoding · Latency-as-Lock · PASD Jitter Tolerance · Local NPU Async Spec-Dec · NIDABA Personalized Retrieval · Router Centrality · Training Lineage Diversity · Cross-Family Quorum · High Table Escalation on Uncertainty · IQ Ceiling Honesty · Temporary Sharding · capability_exceeded Job State · Gap Resolver · Knowledge Gap · Capability Gap · Approved Sources List · NIDABA Gap Enrichment · Jobs as State Machines · Task Package Schema · MDSD Idle Elimination · Pathfinder Role Distributed · Pathfinder WoL Readiness · Pull Model Node Advertisement · Extended Capability Envelope · Network Latency Over Throughput · Degradation Without Correctness Loss · Wide Not Deep as Quorum Voice Diversity · The Ballet Scheduling Metaphor · Logos-First MVP · Brutal Critique Pipeline · Apple Silicon as High Table Verifier.*
