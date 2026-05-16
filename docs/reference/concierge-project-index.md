---
title: "Concierge — Project Store Index"
document_type: index
version: "1.2"
date: "2026-04-18"
status: current
tags: [index, project-store, navigation]
---

# CONCIERGE — PROJECT STORE INDEX
**Version:** 1.2 — April 18, 2026
**Purpose:** Quick reference for every file in the Claude.ai project store — what it is, why it exists, when to load it, and what not to expect from it.

---

## Document Categories & Organization

The project documentation is organized into five categories, each serving a distinct purpose in the design and implementation lifecycle:

### `/specs/` — Canonical Specifications
**Status:** Locked and immutable (or change via formal review only)

Authoritative layer contracts, schemas, and interface definitions. These are the "what we build" documents. Specs are written first, before implementation. All implementation must conform to specs or trigger a formal spec update.

**Contents:**
- `concierge-philosophy.md` — Strategic vision and architectural principles
- `concierge-technical-spec.md` — Layer contracts, schemas, and interface definitions
- `concierge-memory-spec.md` — Memory tier architecture and persistence models
- `concierge-hardware-appendix.md` — Hardware fleet reference and acquisition guidance

### `/seeds/` — Session Handoff Primers
**Status:** Current but evolving (updated after significant sessions)

Compressed context for resuming work after a hiatus. Seeds contain enough information to start working without reading all the specs, but point to specs for details. Each seed is tied to a specific type of work.

**Contents:**
- `concierge-session-seed.md` — Master primer; load this first
- `concierge-session-seed-addendum.md` — Latest decisions pending merge
- `concierge-strategic-reframe.md` — Scope clarification (Concierge vs. Bit)
- `concierge-filesystem-organization-seed.md` — Atlas migration primer
- `seed-bit-application-spec-foundations.md` — Bit design brief

### `/design/` — Design Evolution & Rationale
**Status:** Working documents (ideas in progress)

Captures design decisions, alternatives considered, and implementation approach notes before they crystallize into specs. Design notes explain *why* choices were made and what was rejected. This is where architectural debates happen; specs are the conclusions.

**Contents:**
- `concierge-bit-application-design-notes.md` — Bit UI architecture, memory system, implementation approach
- `concierge-memory-system-design-notes.md` — Memory layer design evolution
- (Future design docs as work progresses)

**Usage:** Load when understanding the rationale behind a spec decision. Load when contributing to ongoing design discussions. Reference from seeds when a design decision needs explaining.

### `/analysis/` — Comparative & External Analysis
**Status:** Reference (not authoritative)

Analysis of external systems, prior art, and related projects. Used to validate Concierge's architectural choices and learn from others' design decisions. Not part of the spec but informs it.

**Contents:**
- `analysis-ernos-agent-vs-concierge.md`
- `analysis-eric-michaud-claude-obsidian-vs-concierge.md`
- `analysis-karpathy-llm-wiki-vs-concierge.md`
- `analysis-reddit-cognitive-os-vs-concierge.md`
- `analysis-karpathy-loop-vs-concierge.md`
- `gemma-planning-analysis.md`

### `/reference/` — Lookup & Quick Reference
**Status:** Current (updated as needed)

Not authoritative specs, not design documents, not seeds. Reference docs are lookups and implementation aids: hardware inventory, integration guides, FAQs, edit recommendations, and this index.

**Contents:**
- `concierge-project-index.md` — This file
- `concierge-architecture-faq.md` — Implementation-phase Q&A
- `hardware-inventory.md` — Current fleet status
- `atlas-filesystem-audit-and-plan.md` — Migration plan
- `searxng-openwebui-integration.md` — Integration guide
- `model-audit-framework.md` — Model evaluation protocol
- `edit-recommendations-karpathy-loop.md` — Specific spec edits

---

## How to Use This Organization

**Starting a new session:** Load `/seeds/concierge-session-seed.md` first. It points to the relevant specs.

**Implementing a feature:** Load the relevant `/specs/` doc. If you need design rationale, load `/design/`. If you hit an implementation question, check `/reference/concierge-architecture-faq.md`.

**Revisiting an old decision:** Check `/design/` first (why was this chosen?), then `/specs/` (what exactly was decided?).

**Contributing to design work:** Discussions live in `/design/`. Once consensus emerges, conclusions move to `/specs/`.

**Onboarding someone new:** `/seeds/concierge-session-seed.md` → `/specs/concierge-philosophy.md` → `/reference/concierge-architecture-faq.md`.

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

### `../seeds/concierge-strategic-reframe.md`
**Size:** ~8KB | **Status:** Current

**What it is:** A reframing document that clarifies the two-part nature of Concierge: the infrastructure pipeline vs. Bit as the human-facing cognitive interface. Written to resolve conceptual confusion about scope.

**What it contains:** The distinction between Concierge-as-infrastructure and Bit-as-interface; the harness layer concept (OpenClaw/similar as RonCo execution for well-defined tasks); the layer contract principle; what OpenClaw actually is and what it cannot do; why Bit is not a dumb terminal.

**When to load it:** When the scope distinction between Bit and the rest of Concierge needs clarifying, or when evaluating third-party agent frameworks.

**What it does NOT contain:** Implementation detail. Schema definitions.

---

### `../seeds/concierge-filesystem-organization-seed.md`
**Size:** ~5KB | **Status:** Reference

**What it is:** Handoff seed for the TrueNAS dataset planning and filesystem consolidation session.

**What it contains:** Problem statement (pre-RAG filesystem state), current infrastructure inventory, tasks for the consolidation session, proposed canonical storage structure.

**When to load it:** When resuming Atlas filesystem consolidation work (Phase 2 data migration not yet executed as of April 2026).

---

### `../seeds/concierge-remote-access-seed.md`
**Size:** ~4KB | **Status:** Reference — work complete

**What it is:** Handoff seed for the remote access scaffold session (Tailscale, Homarr, Open WebUI, SearXNG setup).

**When to load it:** Rarely — work is complete. Load only if troubleshooting the remote access stack.

---

### `../seeds/seed-bit-application-spec-foundations.md`
**Size:** ~4KB | **Status:** Current — active design seed

**What it is:** Foundational design decisions for the Bit Application Specification, captured from April 2026 session conversations.

**What it contains:** Bit's dual role (prosthetic layer + protocol translator); freeform dump as default interaction mode; slash command triggers as explicit mode selectors; ambiguity resolution principle (stakes-weighted); confirmation behavior for persistent record writes; cognitive profile requirements for output layer; CCSS onboarding pattern reference; Bit's relationship to the rest of Concierge.

**When to load it:** At the start of any Bit Application Specification drafting session. This is the brief.

---

### `../seeds/seed-antigravity-opencode-integration.md`
**Size:** ~unknown | **Status:** Current

**What it is:** Seed for integrating Antigravity/OpenCode into the Concierge workflow.

**When to load it:** When working on Claude Code / OpenCode integration topics.

---

### `../seeds/seed-llm-wiki-todo-items.md`
**Size:** ~2KB | **Status:** Current — actionable todo

**What it is:** Three concrete spec additions surfaced by the Karpathy LLM Wiki pattern analysis.

**What it contains:** (1) Memory Spec — add lint pass as a named scheduled Planner job with enumerated failure modes; (2) Memory Spec — add supersession model to Tier 3 entry schema; (3) Technical Spec — add backfiling decision to Foreman job-close sequence.

**When to load it:** At the start of a Memory Spec or Technical Spec revision session.

---

### `../specs/concierge-philosophy.md`
**Size:** ~55KB | **Status:** Complete and locked

**What it is:** The "why" document. Written to be read when the ideas have gone cold and need rekindling. Not a technical reference — a recontextualization document.

**What it contains:** Central thesis (Wide Not Deep), Constraints Are Contracts philosophy, node admission criterion, Docker Tool Zoo concept, five-layer stack narrative, Bit's full history, High Table quorum architecture, Physical Async Speculative Decoding (PASD), node fleet roles, Seshat context seed system.

**When to load it:** When you've lost the thread of *why* an architectural decision was made. When onboarding someone new. When writing external-facing content.

**What it does NOT contain:** Schemas, interface contracts, or implementation specifications.

---

### `../specs/concierge-technical-spec.md`
**Size:** ~83KB | **Status:** Complete — 2,032 lines, 9 sections, all Hittite names in place

**What it is:** The implementation reference. Schemas before code. Contracts before implementation.

**What it contains (9 sections):** Layer Interface Contracts; Task Package Registry; Gap Resolver and Foundation Generation; Node and System Management; Scheduling and Priority; Approved Sources; WorkbeeSim; Integrity Chain; Memory System Interface Contract.

**When to load it:** Any session involving implementation work, schema review, or contract definitions.

**What it does NOT contain:** Router internal design (deliberately unspecced, awaiting dedicated session). Bit Application Specification (separate document, not yet drafted).

---

### `../specs/concierge-memory-spec.md`
**Size:** ~unknown | **Status:** Complete

**What it is:** The memory system design specification covering all four tiers.

**What it contains:** Tier 0–3 definitions, schemas, write protocols, reference resolution, NIDABA enrichment interface.

**When to load it:** Memory system work, Tier 2/3 implementation, NIDABA pipeline design.

---

### `../specs/concierge-hardware-appendix.md`
**Size:** ~unknown | **Status:** Complete

**What it is:** Hardware fleet reference — node specs, PCIe topology, inference capabilities, acquisition research.

**When to load it:** Hardware decisions, node acquisition, model selection for specific nodes.

---

### `../analysis/analysis-ernos-agent-vs-concierge.md`
**Date:** 2026-04-11 | **Status:** Reference

**What it is:** Conceptual comparison of ErnOS Agent vs Concierge. ErnOS = single self-sovereign AI person. Concierge = task execution fabric. Philosophically orthogonal despite surface vocabulary overlap.

**Key finding:** ErnOS's Observer (17-rule output audit) maps onto Concierge's typed output contract validation. ErnOS's checkpoint system maps onto execution checkpointing at Foreman/Workbee boundary.

---

### `../analysis/analysis-eric-michaud-claude-obsidian-vs-concierge.md`
**Date:** 2026-04-11 | **Status:** Reference

**What it is:** Analysis of Eric Michaud's Claude Code + Obsidian vault system vs Concierge.

**Key finding:** Eric's system is a single-node Concierge implementation. His slash command + daily brief pattern is prior art for Bit's interaction surface. Human/machine write-permission split is a concrete answer to Concierge's memory write-permission question.

---

### `../analysis/analysis-karpathy-llm-wiki-vs-concierge.md`
**Date:** 2026-04-11 | **Status:** Reference

**What it is:** Analysis of Karpathy's LLM Wiki pattern vs Concierge.

**Key finding:** LLM Wiki is a named instance of Concierge's continuous index/cache-prefill prep task. Three operational details added as Memory Spec todos (see `seed-llm-wiki-todo-items.md`).

---

### `../analysis/analysis-reddit-cognitive-os-vs-concierge.md`
**Date:** 2026-04-12 | **Status:** Reference

**What it is:** Analysis of a Reddit "cognitive OS" post and comments vs Concierge.

**Key finding:** WillowEmberly's negentropic drift evaluation extends the lint pass concept. CCSS profile pattern is prior art for Bit's cognitive profile onboarding. "Cognitive OS" is the vocabulary the audience already uses for this category.

---

### `../analysis/analysis-karpathy-loop-vs-concierge.md`
**Date:** 2026-04-18 | **Status:** Reference

**What it is:** Analysis of the Karpathy Loop / auto-agent pattern vs Concierge.

**Key finding:** Meta-agent/task-agent split validates Planner/Workbee architecture. Cross-family quorum confirmed as correct (model empathy finding applies to self-improvement loops, not correctness verification). OTel elevated to strategic asset — traces are the substrate for future self-optimization. "Local hard takeoff" added as vocabulary for Concierge's value proposition. Six specific edits recommended across Philosophy doc, Technical Spec, and Session Seed Addendum (see `../reference/edit-recommendations-karpathy-loop.md`).

---

### `../analysis/gemma-planning-analysis.md`
**Date:** 2026-04 | **Status:** Reference

**What it is:** Gemma 4 26B planning analysis — part of the model audit framework evaluation.

---

## Design Documents (Working / In-Progress)

### `../design/concierge-bit-application-design-notes.md`
**Date:** 2026-04-21 | **Status:** Drafting — active design phase

**What it is:** Design-phase notes capturing rationale, tradeoffs, and open questions for the Bit application architecture.

**What it contains:** Hardware constraint analysis, memory architecture (WAL + background flush), language/framework choice rationale (Go + Bubble Tea), MVU pattern explanation, model roles (rubber duck vs. deterministic), slash command routing, Topic Package strategy, offline operation, development methodology, and open design questions awaiting resolution.

**When to load it:** When understanding why architectural decisions were made, or when contributing to ongoing design discussions. These notes will feed into the future `../specs/concierge-bit-application-spec.md` once design consensus is reached.

**Related:** Precedes `../reference/concierge-architecture-faq.md` (questions about design) and `../seeds/seed-bit-application-spec-foundations.md` (brief).

---

## Reference Documents (Lookup & Quick Reference)

### `../reference/hardware-inventory.md`
**Status:** Current

**What it is:** Current hardware fleet inventory. Maintained separately from the Hardware Appendix for quick reference without loading the full spec.

---

### `../reference/atlas-filesystem-audit-and-plan.md`
**Status:** Current — Phase 2 (data migration) pending execution

**What it is:** Full TrueNAS filesystem consolidation plan — current state audit, proposed canonical structure, 5-phase migration plan with downtime estimates, rollback strategy.

---

### `../reference/searxng-openwebui-integration.md`
**Status:** Current — work complete

**What it is:** Integration guide for SearXNG + Open WebUI zero-cost web search on Atlas.

---

### `../reference/model-audit-framework.md`
**Status:** Current

**What it is:** Multi-category model evaluation protocol (ENKI framework). Five-test suite for Bit layer model selection. Extensible to additional task categories.

---

### `../reference/edit-recommendations-karpathy-loop.md`
**Date:** 2026-04-18 | **Status:** Actionable — pending application

**What it is:** Six specific additive edits to project documents derived from the Karpathy Loop analysis.

**What it contains:** Edit A — OTel as institutional memory (Philosophy); Edit B — human-in-the-loop role framing (Philosophy); Edit C — "local hard takeoff" vocabulary (Philosophy); Edit D — OTel as strategic asset (Technical Spec); Edit E — same-family vs cross-family model pairing note (Technical Spec); Edit F — OTel strategic framing addendum (Session Seed Addendum).

**When to load it:** At the start of a Philosophy doc or Technical Spec editing session.

---

### `../reference/concierge-architecture-faq.md`
**Date:** 2026-04-21 | **Status:** Current — active drafting

**What it is:** Frequently asked questions about Concierge architecture, Bit layer design, model roles, memory system, and implementation decisions.

**What it contains:** Q&A across 8 topic areas: Bit Layer & Intent Translation, Offline Queueing & Sync, Model Loading & Concurrency, Model Roles, Prefill Packages (Topic Packages), Local Deterministic Jobs, Topic Packages & Memory, Next Steps for implementation questions.

**When to load it:** When questions about architectural design decisions arise during Bit implementation or infrastructure work. Complements the spec documents with concrete answers to implementation-phase questions.

---

### `../reference/concierge-project-index.md`
**Status:** Current — this file

---

## Documents NOT In the Project Store (Archived or Pending)

| Document | Location | Notes |
|---|---|---|
| Router Design Specification | Not yet written | Requires dedicated multi-model peer review session. Do not start without it. |
| Bit Application Specification | Not yet written | Foundations seed exists (`seed-bit-application-spec-foundations.md`). Ready to draft. |
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

**Bit Application design & specification work:**
→ `../seeds/concierge-session-seed.md` + `../seeds/seed-bit-application-spec-foundations.md` + `../design/concierge-bit-application-design-notes.md` + `../reference/concierge-architecture-faq.md` + `../specs/concierge-technical-spec.md`

*(Use design notes to understand rationale; use FAQ for implementation questions; use technical spec for layer contracts.)*

**Router design session (when scheduled):**
→ `../seeds/concierge-session-seed.md` + `../seeds/concierge-session-seed-addendum.md` + `../specs/concierge-technical-spec.md` + `../specs/concierge-hardware-appendix.md`

**Memory Spec revision (lint pass, supersession model, backfiling):**
→ `../seeds/concierge-session-seed.md` + `../seeds/seed-llm-wiki-todo-items.md` + `../specs/concierge-memory-spec.md`

**Philosophy / Technical Spec editing:**
→ `../seeds/concierge-session-seed.md` + `../reference/edit-recommendations-karpathy-loop.md` + target spec doc

**Lost the thread / need to reconnect with the "why":**
→ `../specs/concierge-philosophy.md` (standalone — written for exactly this purpose)

---

*Index updated April 18, 2026. Added analysis-karpathy-loop-vs-concierge.md and edit-recommendations-karpathy-loop.md. Updated to v1.2. Repo now synced to GitHub (StopBeingLogical/concierge) with push mirror. Project store sourced from GitHub integration. All 26 files present.*
