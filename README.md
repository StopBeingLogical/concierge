# Concierge: Personal Cognitive Infrastructure

**Version:** 5.0 (Specification Phase) | **Last Updated:** April 21, 2026 | **Status:** Architecture locked, implementation beginning

---

## What Is Concierge?

Concierge is a **distributed, multi-model cognitive infrastructure system** designed to think on your behalf continuously, not conversationally. It runs across heterogeneous hardware (GPUs, iGPUs, NPUs, Apple Silicon) and uses ensemble validation through cross-family quorum voting to ensure trustworthy inference.

**Key distinction:** Not a chatbot. A thinking system. Conversational interaction (Bit) is the human-facing layer; distributed work orchestration (Planner/Router/Workbee) is the engine.

### Core Idea

- **Bit** (Layer 1): Interactive chat interface on your personal machines (Logos, Noesis)
- **Planner** (Layer 2): Decomposes complex requests into executable plans
- **Router** (Layer 3): Orchestrates work across the homelab fleet
- **Workbee** (Layer 5): Executes tasks on whatever hardware is available
- **Memory** (Pervasive): Four-tier system from session-only to vector-archived knowledge

**Design philosophy:** Wide, not deep. Four 7B specialists voting + one 32B verifier beats one 70B generalist. Hardware constraints are first-class contracts, not obstacles.

---

## Project Status (April 2026)

| Component | Status | Notes |
|-----------|--------|-------|
| **Philosophy & Vision** | ✅ Locked | `docs/specs/concierge-philosophy.md` — 9 locked architectural principles |
| **Technical Spec (v5)** | ✅ Locked | `docs/specs/concierge-technical-spec.md` — Layer contracts, schemas, state machines |
| **Memory Spec** | ✅ Locked | `docs/specs/concierge-memory-spec.md` — Four tiers, NIDABA enrichment, persistence model |
| **Hardware Appendix** | ✅ Locked | `docs/specs/concierge-hardware-appendix.md` — Fleet reference, PCIe topology, acquisition guidance |
| **Bit App Design** | 🟡 Drafting | `docs/design/concierge-bit-application-design-notes.md` — Architecture rationale, design decisions, open questions |
| **Bit App Spec** | ⏳ Queued | Not yet written. Foundations exist in `docs/seeds/seed-bit-application-spec-foundations.md`. |
| **Router Design** | ⏳ Queued | Deliberately unspecced. Requires dedicated peer review session. |
| **Implementation Code** | ⏳ Not started | Bit (Go/Bubble Tea TUI) to begin after spec consensus. |

---

## Quick Start: By Role

### 🧠 "I want to understand the architecture"
**Read in this order:**
1. This README (you're here)
2. `docs/specs/concierge-philosophy.md` — Why these choices were made
3. `docs/reference/concierge-architecture-faq.md` — Implementation questions answered

**Time commitment:** 30 minutes

---

### 💻 "I'm resuming work on Concierge"
**Load these files:**
1. `docs/seeds/concierge-session-seed.md` — Compressed context (always load first)
2. `docs/seeds/concierge-session-seed-addendum.md` — Latest April 2026 decisions
3. `docs/reference/concierge-project-index.md` — Full file inventory and load sets

**Then:** Navigate by task type (see "Load Sets by Task Type" below).

**Time commitment:** 15 minutes to get oriented

---

### 🎨 "I'm designing Bit (the chat interface)"
**Load in this order:**
1. `docs/seeds/seed-bit-application-spec-foundations.md` — The brief
2. `docs/design/concierge-bit-application-design-notes.md` — Rationale and tradeoffs
3. `docs/reference/concierge-architecture-faq.md` — Implementation Q&A
4. `docs/specs/concierge-technical-spec.md` — Layer contracts and interfaces

**Then:** Add to design docs or draft the Bit Application Specification.

**Time commitment:** 1–2 hours deep dive

---

### 🔨 "I'm implementing something"
**Load:**
1. `docs/specs/concierge-technical-spec.md` — What must be true (schemas, contracts)
2. `docs/specs/concierge-memory-spec.md` — If touching persistence
3. `docs/specs/concierge-hardware-appendix.md` — If touching hardware/routing
4. `docs/reference/concierge-architecture-faq.md` — For implementation details

**Note:** Bit implementation hasn't started yet. Other layers are specification-only.

**Time commitment:** Depends on scope

---

### 📊 "I need hardware/acquisition decisions"
**Load:**
1. `docs/specs/concierge-hardware-appendix.md` — Current guidance
2. `docs/reference/hardware-inventory.md` — What you have now
3. `docs/seeds/concierge-session-seed.md` → Hardware section

**Time commitment:** 20 minutes

---

### 🔍 "I'm lost. Reconnect me with the *why*."
**Read:**
- `docs/specs/concierge-philosophy.md` (standalone, written for exactly this)

**Time commitment:** 30 minutes, reconnects entire vision

---

## Architecture Overview

### Five-Layer Stack (Strict Isolation)

```
┌─────────────────────────────────────────────────────────┐
│ Bit (Layer 1) — Human Interface                         │
│ Chat, approval gate, local reasoning fallback           │
│ Runs on: Logos (M1 Max), Noesis (portable)             │
├─────────────────────────────────────────────────────────┤
│ Planner (Layer 2) — Intent → Execution Plan            │
│ Decomposes requests, queries Router, detects gaps       │
│ Runs on: Ergaster (beastly CPU, 64GB RAM)              │
├─────────────────────────────────────────────────────────┤
│ Router (Layer 3) — Orchestration Brain                  │
│ Node registry, work decomposition, scheduling           │
│ Runs on: Ergaster                                       │
├─────────────────────────────────────────────────────────┤
│ Foreman (Layer 4) — Local Coordinator                   │
│ Heartbeat, capability advertisement, work dispatch      │
│ Runs on: Each headless node                            │
├─────────────────────────────────────────────────────────┤
│ Workbee (Layer 5) — Stateless Executor                 │
│ Runs tasks using available hardware backend             │
│ Runs on: Any node with remaining capacity              │
└─────────────────────────────────────────────────────────┘
```

### Key Architectural Principles

**SHA256 Integrity Chain:** Every artifact crossing layer boundaries carries a hash. Hash mismatch = job terminates. Prevents silent corruption.

**Jobs as State Machines:** Not function calls. Draft → Pending Approval → Approved → Queued → Running → Completed/Partial/Failed. Legible failures.

**Gap Resolver:** Knowledge and capability gaps are detected and structured, not hallucinated. Human confirms resolution before proceeding.

**Graceful Incapability:** New `capability_exceeded` job state. System says "I can't do this well" rather than confidently producing wrong answers.

**Physical Async Speculative Decoding (PASD):** Uses network latency as natural synchronization primitive. Two draft streams naturally desynchronize by 10–30 microseconds.

**Four-Tier Memory:**
- **Tier 0** — Session-only active context
- **Tier 1** — Append-only immutable event log
- **Tier 2** — Structured facts (human-confirmed writes)
- **Tier 3** — Vector archive (NIDABA semantic search)

**Pull Model, Not Push:** Nodes advertise capability. Router pulls work matching declared capacity. Never pushes or names specific nodes.

**Wide Not Deep:** Four 7B specialists from different families + one 32B generalist. Ensemble smarter from breadth, not depth.

---

## Hardware Setup (Current Homelab)

### Interactive Surfaces
| Machine | Role | Specs | Notes |
|---------|------|-------|-------|
| **Logos** | Primary workstation | M1 Max 64GB, MBP | Runs Bit; can escalate to distributed work |
| **Noesis** | Portable dev machine | Latitude laptop (TBD specs) | Runs Bit; grab-n-go for coffee shop work; queues offline tasks |

### Headless Compute Nodes
| Machine | Role | Hardware | Primary Use |
|---------|------|----------|-------------|
| **Daemon** | Worker | 2× Tesla P100 (32GB), RTX 5060 Ti (16GB), iGPU | Inference (inference-class models, burst work) |
| **Kratos** | Worker | CPU-based, Ollama node | Inference (various model sizes) |
| **Ergaster** | Planner/Router | Beastly CPU, 64GB RAM, vestigial iGPU | Planning, orchestration, CPU-intensive work (embeddings) |
| **Atlas** | Cold Storage | TrueNAS, 8× HDD array | Knowledge base, archived sessions, vector store |

### Model Distribution
- **Logos/Noesis Bit:** Primary 30B chat model + secondary 4–7B for intent translation/deterministic work
- **Distributed:** 7B ensemble (4 different families) + 32B verifier + specialized models as needed
- **Ergaster:** CPU embedding models for NIDABA enrichment

---

## How to Navigate This Project

### Document Structure
```
docs/
├─ specs/           Canonical, locked specifications
├─ seeds/           Session handoff primers
├─ design/          Design rationale & working notes
├─ analysis/        Comparative analysis of other systems
├─ reference/       Quick lookup docs, FAQ, index
└─ research/        Model evaluation, hardware audits, validation studies
    └─ bit-model-selection/  Bit layer model research & evaluation results
```

**Key document:** `docs/reference/concierge-project-index.md` — Complete file inventory with what each doc contains and when to load it.

### Finding What You Need

| I want to... | Load... |
|---|---|
| Understand core vision | `docs/specs/concierge-philosophy.md` |
| See all layer contracts & schemas | `docs/specs/concierge-technical-spec.md` |
| Understand memory architecture | `docs/specs/concierge-memory-spec.md` |
| Get context fast (resuming work) | `docs/seeds/concierge-session-seed.md` |
| Design/implement Bit | `docs/design/concierge-bit-application-design-notes.md` + FAQ |
| See hardware specs | `docs/specs/concierge-hardware-appendix.md` |
| Find a specific file | `docs/reference/concierge-project-index.md` |
| Get implementation Q&A | `docs/reference/concierge-architecture-faq.md` |
| Understand design tradeoffs | `docs/design/concierge-bit-application-design-notes.md` |
| Review Bit model selection research | `docs/research/bit-model-selection/` (evaluation results, model audit framework) |

---

## Current Constraints & Key Decisions

### Hardware Constraints (First-Class)
- **Logos:** 64GB shared with macOS. Bit uses local models; complex work escalates.
- **Daemon:** 16GB VRAM per GPU. Single-digit jobs/day; no sustained high load.
- **Ergaster:** CPU-optimized for planning, not inference (iGPU vestigial).
- **Network:** Tailscale-based homelab. PASD relies on 10–30µs latency jitter.

### Model Roles (Not Specific Models)
- **Rubber Duck (Primary):** 30B-class conversational models (domain-flexible, 2–3 variants available)
- **Deterministic (Secondary):** 4–7B-class instruction-following models (intent translation, copilot tasks, 2–3 variants)
- **Verifier:** 32B+ for High Table escalation (ensemble disagreement resolution)

### Software Decisions (Locked)
- **Language:** Go (Bit implementation)
- **UI Framework:** Bubble Tea (TUI)
- **Architecture:** MVU (Model-View-Update) for strict UI/backend separation
- **Memory:** WAL + background flush (not real-time database)
- **Persistence:** NDJSON event logs + Vector DB for semantic search

### Offline Operation
- Bit can operate fully offline on Logos/Noesis
- Complex job requests are queued locally as JSON
- Queue drains to Planner when Tailscale reconnects (FIFO or priority)
- Session prefill (25% frequent, 75% recent topics) cached locally for continuity

---

## What's Next?

### Immediate (This Sprint)
- [ ] Finalize hard contract JSON schema for Bit → Planner escalation
- [ ] Design slash command registry and routing table
- [ ] Sketch TUI layout and MIME viewer approach

### Near-Term (Next 2–4 Weeks)
- [ ] Draft Bit Application Specification (builds on design notes)
- [ ] Begin Go scaffold implementation with training unit methodology
- [ ] Model selection for Bit's dual roles (rubber duck + deterministic)

### Deferred (Requires Dedicated Sessions)
- [ ] Router detailed design (deliberately unspecced, needs peer review)
- [ ] Foreman/Workbee implementation (post-Bit)
- [ ] NIDABA retrieval optimization

**For detailed TODOs and action items:** See `docs/reference/concierge-project-index.md` (search for "Open Questions" or "Next Steps" sections).

---

## Key Files at a Glance

| File | Size | Purpose | When to Load |
|------|------|---------|--------------|
| `docs/specs/concierge-philosophy.md` | 55KB | Vision, principles, rationale | When lost; when onboarding |
| `docs/specs/concierge-technical-spec.md` | 83KB | Layer contracts, schemas, interfaces | Implementation work |
| `docs/specs/concierge-memory-spec.md` | ~30KB | All four memory tiers, persistence | Memory/persistence work |
| `docs/specs/concierge-hardware-appendix.md` | ~30KB | Hardware reference, acquisition | Hardware decisions |
| `docs/seeds/concierge-session-seed.md` | 11KB | Compressed context | Every session (load first) |
| `docs/design/concierge-bit-application-design-notes.md` | ~15KB | Design rationale, tradeoffs | Bit design/implementation |
| `docs/reference/concierge-architecture-faq.md` | ~8KB | Implementation Q&A | Implementation questions |
| `docs/reference/concierge-project-index.md` | ~12KB | Complete file inventory | Navigation, finding documents |

---

## For Models & Agents Reading This

**You are probably reading this because:** A human asked you to help with Concierge in a new session. You have no prior context.

**What to do:**
1. **Read this README** (you're doing it) — 10 minutes
2. **Load the session seed** — `docs/seeds/concierge-session-seed.md` — 10 minutes
3. **Navigate by your task** — Use the "Quick Start: By Role" section above to find the right docs
4. **Ask questions** — If something is unclear, check `docs/reference/concierge-architecture-faq.md`
5. **Understand before proposing** — Don't suggest changes to locked specs without reading the philosophy doc first

**Key principle:** Specs are locked. Design is open. Reference is for clarity. Seeds are for context.

---

## Related Projects & Tools

**Enki** (`../enki/`) — Model evaluation framework used to validate Bit layer model candidates. v1.0 is production-ready; v2.0 adds semantic evaluation and resilience improvements. See `../enki/README.md` for details.

---

## Contact & Context

**Project lead:** Bobby (senrew@gmail.com)  
**Repository:** Forgejo instance + GitHub mirror (StopBeingLogical/concierge)  
**Last major update:** April 21, 2026 (document organization, Bit design notes, FAQ)  
**Previous snapshots:** See archived docs in `docs/reference/concierge-project-index.md` (superseded by v5 spec set)

---

## License & Status

Concierge is a **personal research project** in active specification phase. Architecture is locked. Implementation is not yet started (Bit layer to begin soon).

All documentation is owned by Bobby. Use for reference, learning, or discussion; do not assume this is production-ready code or finished research.

---

**Last updated:** April 21, 2026 | **Project version:** 5.0 (Specification, Locked) | **Next milestone:** Bit Application Spec draft
