---
title: "Concierge — Project Store Index"
document_type: index
version: "1.1"
date: "2026-04-13"
status: current
tags: [index, project-store, navigation]
---

# CONCIERGE — PROJECT STORE INDEX
**Version:** 1.1 — April 12, 2026
**Purpose:** Quick reference for every file in the Claude.ai project store — what it is, why it exists, when to load it, and what not to expect from it.

---

## File Inventory

### `../seeds/concierge-session-seed.md`
**Size:** ~11KB | **Status:** Current

**What it is:** The master context primer for starting a new session. Designed to replace the several large dump files that used to be in the project store. Single file that restores enough context to resume work without reading all four spec documents.

**What it contains:** Stack overview, all locked naming conventions (Hittite names and their meanings), locked architectural decisions, spec document status table, open questions and deferred items, infrastructure reference (Atlas, Forgejo, PCIe topology), tool/workflow notes, archive index of retired files.

**When to load it:** Every session. Load this first, before anything else. If you only load one file, load this one.

**What it does NOT contain:** Full spec content, schemas, or implementation detail. It tells you what decisions were made, not how to implement them. For implementation, load the relevant spec doc alongside it.

**Related files:** `../seeds/concierge-session-seed-addendum.md` (April 2026 ecosystem additions), `../specs/concierge-technical-spec.md` (implementation reference)

---

### `../seeds/concierge-session-seed-addendum.md`
**Size:** ~7KB | **Status:** Current — pending merge into seed v1.1

**What it is:** An addendum to the session seed covering decisions made during the April 2026 ecosystem survey session. Exists as a separate file because the seed hadn't been updated yet when this session concluded.

**What it contains:** Comparative analysis of Hermes Agent and OpenClaw vs. Concierge (where they align, where Concierge is distinct). Three locked standards adoption decisions: OpenTelemetry/Langfuse for distributed tracing, A2A Protocol alignment for the Dispatch envelope, and progressive disclosure for Task Package loading. Three open spec review items: typed Task Package output contracts, execution checkpointing at Foreman/Workbee boundary, Router reliability signal. Bobby's confirmed positions on local vs. frontier model roles. Four new agenda items for the Router design session.

**When to load it:** Load alongside the main session seed when returning to spec work, until this content is merged into seed v1.1. Can be skipped for hardware-only sessions.

**What it does NOT contain:** Full ecosystem analysis source material. The decisions are here; the reasoning behind them is in the session chat history.

---

### `../specs/concierge-philosophy.md`
**Size:** ~55KB | **Status:** Complete and locked

**What it is:** The "why" document. Written to be read when the ideas have gone cold and need rekindling. Not a technical reference — a recontextualization document.

**What it contains:**
- Central thesis: Wide Not Deep — ensemble diversity over monolithic depth
- Constraints Are Contracts philosophy (the foundational principle behind everything)
- The node admission criterion (contribution > orchestration cost) and its three sub-components
- The Docker Tool Zoo concept and RonCo onboarding philosophy
- The five-layer stack narrative (Bit through Workbee, each layer's purpose in plain language)
- Bit's full history — how it evolved from the original Concierge Shell v0.1 through the Lock List redesign
- Bit's current state as a Python package (~85 source files, CLI + TUI)
- The High Table quorum architecture — quorum breadth vs. verifier depth
- Physical Async Speculative Decoding (PASD) — how Daemon's heterogeneous GPU islands work
- Node fleet roles (Daemon, Ergaster, Kratos, Noesis, Gramma, Atlas, Logos)
- Seshat context seed system

**When to load it:** When you've lost the thread of *why* an architectural decision was made the way it was. When onboarding someone new to the project. When writing documentation or external-facing content. Not needed for routine spec work if you have the session seed loaded.

**What it does NOT contain:** Schemas, interface contracts, or implementation specifications. For those, see `../specs/concierge-technical-spec.md`.

---

### `../specs/concierge-technical-spec.md`
**Size:** ~83KB | **Status:** Complete — 2,032 lines, 9 sections, all Hittite names in place

**What it is:** The implementation reference. The "what it does and how the pieces fit together" document. Schemas before code. Contracts before implementation.

**What it contains (9 sections):**
1. **Layer Interface Contracts** — full schemas for Intent Artifact, Execution Plan, Job Spec, Work Chunk, Work Result, Approval Signal, ExecutionState; layer-by-layer emits/receives; Bit's Lock List; disambiguation UI behavior; all Hittite job states
2. **Task Package Registry** — Task Package schema, Registry query protocol, confidence threshold matching, Tarhuili (unregistered approximation) activation, Task Package Creation Wizard
3. **Gap Resolver and Foundation Generation** — capability gap detection, Handanza state, Hašatar tag, foundation generation loop, `capability_exceeded` handling
4. **Node and System Management** — system/node distinction, node admission, capability advertisement schema, health monitoring, degradation handling
5. **Scheduling and Priority** — P1/P2/P3/P4 priority classes, scheduling algorithm, burst mode, Daemon island topology, PASD mechanics
6. **Approved Sources** — source registry schema, trust tiers, fetch policy, content validation
7. **WorkbeeSim** — test harness design, fixture scenarios, deterministic response protocol, API surface (8 endpoints)
8. **Integrity Chain** — SHA256-only hashing, canonical JSON requirements, cross-language consistency requirement, `integrity_violation` terminal state, integrity event schema, invariants
9. **Memory System Interface Contract** — tier definitions (Tier 0–3), layer read/write rules table, `context_refs` schema, memory system invariants

**When to load it:** When actively working on spec content, reviewing schemas, or implementing any layer. This is the working document for spec sessions.

**What it does NOT contain:** Internal memory system implementation (that's `../specs/concierge-memory-spec.md`). Router internal design (explicitly deferred — separate doc/session). Bit application surface detail (separate Bit Application Specification, in progress).

---

### `../specs/concierge-memory-spec.md`
**Size:** ~28KB | **Status:** Complete

**What it is:** The internal implementation spec for the Concierge memory system. Sits below `../specs/concierge-technical-spec.md`'s Section 9 interface contract — Section 9 defines the boundary, this document defines what's behind it.

**What it contains:**
- Tier 0 (Active Context) — in-process session state, full schema, lifetime and discard rules
- Tier 1 (Event Log) — append-only execution audit trail, event schema, retention policy (integrity violations retained indefinitely)
- Tier 2 (Structured Facts) — user preferences, settings, named entities, behavioral patterns; write discipline (human-confirmed only); schema; promotion/demotion protocol
- Tier 3 (Vector Archive) — semantic search index, NIDABA enrichment protocol, SQLite + FTS5 backend (no vector database dependency), query interface
- Reference resolution protocol — how `context_refs` in Intent Artifacts are resolved by the Planner
- Write discipline invariants for each tier
- Memory lifecycle management

**One open design decision (flagged, not yet confirmed):** Tier 3 content reaches the Planner via a direct query during plan generation — not through `context_refs`, which is Tier 2 only. This needs explicit confirmation before the Memory Spec is considered truly locked.

**When to load it:** When working on memory system design, NIDABA enrichment, or Planner/Bit integration points involving memory. Not needed for routine spec work on other sections.

**What it does NOT contain:** The interface contract (that's Section 9 in `../specs/concierge-technical-spec.md` — this doc defers to it on boundary definitions). NIDABA enrichment pipeline internals (TBD separately).

---

### `../specs/concierge-hardware-appendix.md`
**Size:** ~31KB | **Status:** Complete and locked

**What it is:** Hardware fleet reference for node acquisition and routing decisions. The tier classifications will go stale; the principles behind them won't.

**What it contains:**
- Acquisition principles (Speed < Capacity, iGPU + RAM over dGPU for ensemble, dGPU as specialist nodes, RonCo onboarding philosophy)
- Node tier taxonomy (Tier 1–5) with representative chips, routing notes, and use-case assignments
- NPU architecture reference — comparative characterization of AMD XDNA 2, Intel NPU generations, Apple ANE, Rockchip NPU — by workload fit, not TOPS
- Current fleet roster with per-node roles, specs, and Concierge assignment
- Daemon corrected PCIe topology (April 2026): RTX 5060 Ti at x16, P100 #1 at x8, P100 #2 at x4; three operating modes (Island A, Island B, Burst)
- Ergaster (i9-13900HX, Windows) — control plane candidate
- Acquisition target guidance — what to look for when expanding the cluster

**When to load it:** When making hardware acquisition decisions, when the Router design session addresses island capability advertisement, or when reviewing node admission for a specific candidate machine.

**What it does NOT contain:** Software configuration. Implementation detail for any layer. Current prices (those go stale immediately).

---

### `hardware-inventory.md`
**Size:** ~4KB | **Status:** Current — April 12, 2026

**What it is:** Canonical homelab hardware state. Quick reference for the actual machines, their specs, and current roles. Complements `../specs/concierge-hardware-appendix.md` (which is about principles and tier taxonomy) with concrete data about your fleet.

**What it contains:**
- Active fleet roster: Logos (M1 Max 10/24, 64GB), Atlas (Ryzen 5700G, 64GB, 3x12TB RaidZ1), Daemon (i7-12700F, 32GB, 2x P100, 1x 5060 Ti), Ergaster (i9-13900HX, 64GB), Kratos (Ryzen 7600X, RX 7800 XT, 32GB)
- On-bench status: Noesis (active as dev laptop), Ephemera (unused under desk), Praxis (gaming only), Gramma (out of scope)
- Fleet topology summary by compute tier
- Service inventory (TrueNAS, Nextcloud, Forgejo, Nisaba, planned Ollama/Open WebUI/Homarr)
- Changelog tracking updates to hardware state
- Acquisition pipeline status (currently no pending acquisitions)

**When to load it:** When you need to know actual hardware specs, current node roles, or what services are running where. Reference for spinup/config tasks. Update whenever hardware changes, services are added, or nodes are repurposed.

**What it does NOT contain:** Principles or tier taxonomy (that's `../specs/concierge-hardware-appendix.md`). Implementation detail. Software configuration instructions.

---

### `searxng-openwebui-integration.md`
**Size:** ~7KB | **Status:** Current — April 13, 2026

**What it is:** Integration guide for connecting SearXNG (self-hosted metasearch) to Open WebUI v0.8.12 for zero-cost web search capability.

**What it contains:**
- Overview: SearXNG running on Atlas port 8888, zero API fees, aggregates Google/Bing/DuckDuckGo in parallel
- Step-by-step installation (create Filter function in Open WebUI)
- Complete Python function code with proper headers to bypass botdetection (X-Forwarded-For, X-Real-IP)
- How it works: intercepts messages with search keywords, queries SearXNG, injects results into model context
- Troubleshooting for 403 Forbidden errors (botdetection) and rate limiting
- Cost breakdown (~$5/month for infrastructure, $0 for API)

**When to load it:** When setting up web search in Open WebUI, or when troubleshooting SearXNG integration. Reference for debugging botdetection blocks.

**What it does NOT contain:** SearXNG configuration detail (that's the SearXNG docs). Open WebUI advanced features. Model-specific optimization.

---

## Documents NOT In the Project Store (Archived or Pending)

| Document | Location | Notes |
|---|---|---|
| Router Design Specification | Not yet written | Requires dedicated multi-model peer review session. Do not start without it. |
| Bit Application Specification | Not yet written | Scope definition was in progress as of April 2026. Bobby indicated scope adjustments were needed before drafting. |
| `CONCIERGE_TECHNICAL_POSTMORTEM.md` | Forgejo / Nextcloud | 916KB retrospective. Historical only. All live decisions are in v5 docs. |
| `CONCIERGE_EVOLUTIONARY_DUMP.md` | Forgejo / Nextcloud | 333KB NIDABA raw export. Not curated. |
| `CONCIERGE_CORE_DUMP.md` | Forgejo / Nextcloud | 338KB NIDABA raw export. Titles only. |
| `CONCIERGE_CONTRACTS_COMPILATION.md` | Forgejo / Nextcloud | 290KB NIDABA contract export. Mixed with non-Concierge content. |
| Earlier session snapshots (1, 2, 3) | Forgejo / Nextcloud | Superseded by v5 spec set and session seed. |
| `concierge_concept_v5.md` | Forgejo / Nextcloud | 55KB early concept doc. Superseded by Technical Spec and Philosophy doc. |

---

## Recommended Load Sets by Session Type

**General spec work / resuming where you left off:**
→ `../seeds/concierge-session-seed.md` + `../seeds/concierge-session-seed-addendum.md` + `../specs/concierge-technical-spec.md`

**Memory system work:**
→ `../seeds/concierge-session-seed.md` + `../specs/concierge-memory-spec.md` + `../specs/concierge-technical-spec.md` (Section 9)

**Hardware / node acquisition decisions:**
→ `../seeds/concierge-session-seed.md` + `../specs/concierge-hardware-appendix.md` + `hardware-inventory.md`

**Bit Application Specification drafting (when ready):**
→ `../seeds/concierge-session-seed.md` + `../seeds/concierge-session-seed-addendum.md` + `../specs/concierge-technical-spec.md` + `../specs/concierge-philosophy.md` (for Lock List history)

**Router design session (when scheduled):**
→ `../seeds/concierge-session-seed.md` + `../seeds/concierge-session-seed-addendum.md` + `../specs/concierge-technical-spec.md` + `../specs/concierge-hardware-appendix.md`

**Lost the thread / need to reconnect with the "why":**
→ `../specs/concierge-philosophy.md` (standalone — it's written for exactly this purpose)

---

*Index updated April 13, 2026. Added SEARXNG_OPENWEBUI_INTEGRATION.md (remote access scaffold Phase 3 support). Infrastructure table updated with full service listing. Session seed and project index both reflect April 13 remote access scaffold completion (Tailscale, Homarr, Open WebUI, SearXNG, zero-cost web search).*
