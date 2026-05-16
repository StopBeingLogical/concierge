# Assessment: Gemma 4 26B Recommendation vs. Current Concierge State

**Date:** April 13, 2026  
**Context:** Gemma 4 26B via Open WebUI assessed "next critical step" for Concierge project

---

## Gemma's Recommendation Summary

Gemma identified a "specification gap regarding the execution logic (the 'How')" and recommended a three-phase roadmap:

1. **Immediate:** Task Lifecycle & State Machine Protocol specification
2. **Short-term:** Node Registry Schema (discovery)
3. **Long-term:** Orchestrator logic (Router brain)

---

## Assessment: Current State vs. Recommendation

### Phase 1: Task Lifecycle & State Machine — **ALREADY COMPLETE**

Gemma's suggested document `Protocol: Task Lifecycle and State Transitions` is **substantially already written**. The `Concierge_Technical_Spec_v5.md` contains:

| Gemma's "Must Define" | Current Location | Status |
|---|---|---|
| **Task anatomy / Unit of Work schema** | `Concierge_Technical_Spec_v5.md`, Section 1 (Work Chunk Schema, lines 298–321) | ✅ Complete with `chunk_id`, `job_id`, `step_id`, `action`, compute requirements, timeout, etc. |
| **State machine with all transitions** | `Concierge_Technical_Spec_v5.md`, Section 2 (Job State Machine, lines 404–509) | ✅ Complete with 13 states, 28+ documented transitions, event payloads |
| **Ingestion pipeline (Bit → PENDING)** | Section 1 (Bit layer contract, lines 23–128) | ✅ Complete with Intent Artifact schema, disambiguation UI, queuing behavior |
| **Orchestration (Planner dispatch)** | Section 2 (Planner job lifecycle, lines 131–265) | ✅ Complete with tool availability queries, plan generation, approval gates |
| **Execution (Worker/Node dispatch)** | Section 4 & 5 (Foreman & Workbee contracts, lines 330–385) | ✅ Complete with Work Chunk dispatch, Work Result schema, heartbeat responsibility |
| **Validation/Verifier phase** | Section 2 (Planner validation on return path, line 179) + Section 8 (Integrity Chain, lines 388–400) | ✅ Complete with SHA256 chain verification, integrity violation terminal state |
| **Result persistence** | Section 9 (Memory System Interface, entire section) | ✅ Complete with tiered memory architecture, write protocols, reference resolution |

**What Gemma Missed:** Concierge's spec is already at a **deeper level of formalization** than Gemma suggested. Every layer has:
- Typed schemas (JSON with invariants)
- State machines (not just linear pipelines)
- Integrity verification (SHA256 chain across layer boundaries)
- Error handling (terminal vs. conditional terminal states)
- Priority lanes (P0–P3 preemption rules)

### Phase 2: Node Registry Schema — **PARTIALLY DEFERRED, DESIGN LOCKED**

Gemma's second task: "Registry Schema for node discovery."

**Current state:**
- `Concierge_Hardware_Appendix_v5.md` explicitly describes the **onboarding pattern** (line 23): nodes are black boxes that self-survey hardware, advertise capability envelope, and register with the Router
- `Concierge_Technical_Spec_v5.md` Section 4 (Node and System Management) defines system and node terminology
- **No formal Registry schema document yet written**, but the pattern is locked
- **Three open design questions** exist (in session seed, line 120):
  - Island capability advertisement schema for dual operating modes (normal vs. burst)
  - Burst mode drain protocol and timeout handling
  - Tensor split parameter ownership — Router vs. Foreman

**Why registry design is deferred:** Bobby's position (confirmed in ecosystem survey session) is that Daemon's burst-mode architecture introduces complexity that a generic registry schema should not burden. The registry schema design requires the Router deep-design session (which is explicitly scheduled as a separate multi-model peer review).

### Phase 3: Orchestrator Logic (Router) — **EXPLICITLY DEFERRED**

Gemma's third phase: implement the "brain" (Router scheduling).

**Current state:**
- Section 3 (`Concierge_Technical_Spec_v5.md`, lines 263–297) defines **only the Router's contract boundary**:
  - What it receives: Approved Job Specs from Planner
  - What it emits: Work Chunks to Foreman
  - Invariants: zero knowledge of hardware identity, must respond to tool availability queries
- **Internal scheduling logic explicitly deferred** (line 267): "The Router is the operational core of the Concierge system. Its internal scheduling logic is the subject of a dedicated design session with multi-model peer review. What is specified here is the Router's contract boundary only."

**Why deferred:** Bobby's architectural position is that Router design is complex enough to warrant structured peer review with multiple frontier models, not a single Claude session. Open agenda items from the April 2026 hardware session include burst mode SLA classification, cross-node shard decision boundaries, and capability summary schemas.

---

## What Gemma Correctly Identified

1. **IPC and lifecycle are foundational** — Yes, and they are already formally specified
2. **Task schema must come before implementation** — Yes, this has been done
3. **State machine clarity unlocks development** — Confirmed; Concierge has an unusually explicit state machine
4. **Capability discovery is a prerequisite** — Correct; it's flagged as an open item pending Router design session

---

## What Gemma Got Wrong

1. **Assumed the existence of specs meant they were incomplete** — The Technical Spec is complete and production-ready
2. **Overestimated the work remaining in "lifecycle definition"** — The work here is done
3. **Underestimated the complexity of node registry design** — Daemon's burst architecture makes this non-trivial; it cannot be solved in isolation from the Router
4. **Suggested implementing in the order: State Machine → Registry → Router** — This is backwards relative to discovery order, but the state machine and lifecycle are already finalized

---

## The Real "Specification Gap" Gemma Sensed (But Mislabeled)

Gemma was correct that there is a gap, but it is **not** in the lifecycle or state machine. The gaps are:

### A. **Typed Task Package Output Contracts** (Session Seed Addendum, Item A)
- Task Packages should declare output schema (e.g., `FileArtifact`, `TextResult`, typed struct)
- Foreman validates actual output against schema at runtime before marking complete
- **Status:** Identified but not yet specced. Would appear in Task Package Registry documentation.

### B. **Execution Checkpointing** (Session Seed Addendum, Item B)
- Workbee should checkpoint state after completing a step in a multi-step Task Package
- Enables graceful degradation and restart-from-checkpoint on failure
- **Status:** Identified but not specced. Would appear in Node and System Management section or a new Resilience section.

### C. **Router Reliability Signal** (Session Seed Addendum, Item C)
- Foreman outcome data (latency, quality, failure rate per node/task) should inform Router capability scoring over time
- **Status:** Identified but not specced. Deferred to Router design session.

### D. **Bit Application Specification** (Session Seed, line 100)
- Scope and detailed design not yet begun
- **Status:** In progress; next major deliverable after core stack clarification

---

## Recommended Next Steps (Revised Priority)

### **Immediate (This Month)**

1. **Write the Node Registry Schema Specification** (2–3 hours)
   - **What:** Document the onboarding protocol, capability envelope schema, and island-mode advertisement rules for Daemon
   - **Why:** Unblocks Router design review session. Converts the prose in Hardware Appendix into a schema document.
   - **Owner:** Bobby to define; Claude to draft
   - **Scope:** 300–500 lines. Document structure:
     - Onboarding flow (self-survey, package matching, registration)
     - Capability envelope schema (compute class, memory, accelerator features, latency bounds)
     - Island mode rules for Daemon (normal vs. burst advertisement)
     - Heartbeat schema (what does a node's periodic check-in contain?)

2. **Clarify Tier 3 Memory Access Pattern** (30 min)
   - **What:** Decide: Does Planner query Tier 3 directly, or use `context_refs` mechanism?
   - **Why:** Blocks Memory Spec v5 lockdown. This is a known open item.
   - **Owner:** Bobby decision; Claude to document rationale
   - **Scope:** One decision note, <100 lines

3. **Merge Session Seed Addendum into v1.1** (30 min)
   - **What:** Fold the April 2026 ecosystem survey decisions into the main seed
   - **Why:** Seeds should stay lean but current. Addendum is now canonical context.
   - **Owner:** Claude to execute based on Bobby's review

### **Short-term (April–May)**

1. **Draft the Router Deep-Design Session Agenda** (1 hour)
   - **What:** Formalize the open questions (island capability advertising, burst SLA classification, OTel span schema, A2A alignment audit, reliability signal data model)
   - **Why:** Clarifies what a Router design session should cover. Makes peer review structured and efficient.
   - **Scope:** Agenda document with 6–8 topic areas, each with 2–3 sub-questions. ~200–300 lines.

2. **Typed Task Package Output Contract Specification** (2–3 hours)
   - **What:** Document how Task Packages declare output schema and how Foreman validates at runtime
   - **Why:** Locks down the execution-time enforcement of "Constraints Are Contracts"
   - **Scope:** Appears in Task Package Registry section or as extension to Section 2. ~400–600 lines.
   - **Technical path:** Pydantic or JSON Schema for schema definition

3. **Execution Checkpointing Specification** (2 hours)
   - **What:** Document checkpoint format, store location (Nextcloud), resumption protocol
   - **Why:** Enables graceful degradation and node failure recovery
   - **Scope:** New subsection in Node and System Management. ~300–400 lines.

### **Long-term (Post-Router Session)**

1. **Bit Application Specification** (5–8 hours)
   - **What:** Full design of the Bit application surface — UI/UX, local resource management, queue interfaces
   - **Why:** Bit is Layer 1 and the human interface; its design must be locked before implementation begins
   - **Scope:** Separate document, 2,000+ lines. Covers intent disambiguation UI, dashboard surfaces, notification model, offline queuing, reconnection handshake

2. **Router Internal Design Specification** (4–6 hours, post peer-review)
   - **What:** Scheduling algorithm, capability scoring, multi-model selection, burst mode coordination
   - **Why:** Locks down the operational heart of the system
   - **Scope:** Separate document, ~2,000 lines

3. **Implementation Reference Architecture** (3–4 hours)
   - **What:** Translate specs into code patterns and project structure (e.g., "Here's how to implement Harkanza in a job state machine")
   - **Why:** Bridges the gap between specification and first implementation
   - **Scope:** ~1,000 lines with code examples

---

## Gemma's Actual Value

Even though Gemma misidentified the gap, the **framing was helpful**:

- ✅ Correctly identified that the architecture is mature but the implementation path is not yet explicit
- ✅ Correctly suggested focusing on the lifecycle before building the orchestrator
- ✅ Correctly emphasized that "protocol before code" is the right approach
- ✅ Correctly noted that node registry is prerequisite to distributed scheduling

**Where to direct Gemma next:**

Instead of "write the task lifecycle doc," ask Gemma to:
> "Review the Job State Machine and Task Lifecycle sections of the Technical Spec. Identify any gaps in the state model, missing transitions, or edge cases not covered by the current 13 states and 28 transitions. Suggest additions if any."

Or:
> "The system must move multi-step Task Packages from one node to another mid-execution if the first node fails. Sketch the checkpointing protocol and state transitions required to make this work without losing work."

---

## Summary Table: Spec Completeness

| Component | Spec Location | Status | Known Gaps |
|---|---|---|---|
| **Intent → Job ingestion** | Sec. 1 (Bit) | ✅ Complete | None known |
| **Plan generation** | Sec. 2 (Planner) | ✅ Complete | Gap Resolver full logic (not critical) |
| **Job state machine** | Sec. 2 | ✅ Complete (13 states, 28 transitions) | None known |
| **Work dispatch** | Sec. 3–4 (Router, Foreman) | ⚠️ Contract boundary only | Router internal algorithm deferred |
| **Execution** | Sec. 5 (Workbee) | ✅ Complete | None known |
| **Integrity chain** | Sec. 8 | ✅ Complete | None known |
| **Memory system** | Sec. 9 + Memory Spec v5 | ✅ Complete | Tier 3 access pattern (needs decision) |
| **Task Package registry** | Task Package spec (separate doc) | ⚠️ Partial | Output schema contracts not yet specced |
| **Node registry** | Hardware Appendix (prose) | ⚠️ Partial | Schema document not yet written |
| **Foundation generation** | Sec. 3 | ✅ Complete | Implementation pattern not yet shown |
| **Bit application** | Separate doc (in progress) | ❌ Not started | Scope being defined |

---

## Conclusion

**Gemma was not wrong; he was imprecise.** The "specification gap" he sensed is real, but it is not in the lifecycle protocol. It is in:

1. **Node registry formalization** (should be next)
2. **Output contract typing** (should follow)
3. **Execution checkpointing** (should follow)
4. **Router internal algorithm** (scheduled for peer review)
5. **Bit application design** (largest remaining deliverable)

The current state of Concierge specs is **production-grade** for the layer contracts, state machines, and memory system. What remains is the **operational detail** — how nodes join the cluster, how the Router makes decisions, and how the human application surfaces the whole system to the user.

This is excellent news: it means the foundation is sound, and the next work is focused and well-scoped.
