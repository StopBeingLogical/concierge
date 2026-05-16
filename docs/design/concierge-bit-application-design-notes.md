---
title: "Concierge Bit Application — Architecture & Design Notes"
document_type: design
version: "1.0"
date: "2026-04-21"
status: drafting
tags: ['bit-layer', 'ui-architecture', 'memory-system', 'go-implementation', 'design-notes']
---

# Concierge Bit Application: Architecture & Design Notes

**Status:** Design-phase notes capturing rationale and alternatives. These notes inform and precede the Bit Application Specification. Once design consensus is reached, conclusions will be codified into `/specs/concierge-bit-application-spec.md`.

---

## 1. Hardware Constraints & Interactive Model Isolation

### Context
Initial tests with a local LLM (`gemma4:26b`) revealed a critical constraint: running a ~26B parameter model with a 32k context window on a 16GB VRAM GPU (Daemon rig) leaves virtually zero overhead. This means:
- The interactive model cannot be saddled with state management, summarization, or tool calling
- Background tasks (memory persistence, enrichment, analysis) must run separately
- The conversational prompt must remain isolated from infrastructure concerns

### Design Decision
**Interactive models are strictly decoupled from background tasks.** The model that handles chat does not handle state, and the system that handles state does not consume the model's context.

### Implications
- Tool calling and intent translation happen via a separate model role (not the primary chat model)
- No self-summarization by the primary model; instead, the system summarizes on its own
- Memory writes are batched and processed by background Workbee processes
- Primary model context is sacrosanct: conversation only

---

## 2. Memory Architecture: Thick Client with Write-Ahead Log

### Design Pattern
**Thick Client** architecture utilizing In-Memory State with Background Flush:

```
┌─────────────────────────────────────────┐
│ Bit Application (Thick Client)          │
├─────────────────────────────────────────┤
│ Hot Context (Active Memory)             │ ← Session state in RAM
│ ↓                                       │
│ Write-Ahead Log (WAL) ← Local file     │ ← Durability for crash recovery
│ ↓                                       │
│ Background Flush (Idle or Token Ceiling)
│ ↓                                       │
│ Cold Context (Master DB + Vector Store)│ ← Persistent storage
└─────────────────────────────────────────┘
```

### Components

**Hot Context (Active Memory):** The active chat session lives entirely in the application's local RAM. Fast, responsive, zero latency to model.

**Write-Ahead Log (WAL):** As turns are generated, they are appended to a temporary local file (e.g., `session_active.jsonl`). Ensures zero-latency persistence and crash recovery. No database round-trip during chat.

**Background Flush:** Triggered by:
1. **Idle Timer** — After 10 minutes of inactivity
2. **Token Ceiling** — When session context approaches 32k limit

On trigger:
1. Background Workbee ingests the WAL
2. Pushes data to permanent database (SQLite or Vector DB)
3. Generates a "Topic Package" summary
4. Clears the temp WAL file

### Advantages
- **Zero-latency chat:** No database I/O during conversation
- **Crash-safe:** WAL survives power loss
- **Offline-capable:** Bit can operate without homelab connectivity
- **Prefill efficiency:** Topic Packages seed the next session without full history

### Tradeoffs
- **Eventual consistency:** Cold storage may lag behind session state briefly
- **Single-session memory:** Tier 0 (session-only) doesn't persist; Topic Packages bridge this gap
- **Implementation complexity:** Needs careful synchronization of WAL → cold storage

---

## 3. Desktop Application & UI Framework

### Context
Need: Cross-platform (macOS/Windows), low-boilerplate, avoids Electron bloat, supports native concurrency.

### Decision: Go + Bubble Tea TUI

**Language:** Go (Golang)
- Statically compiled, cross-platform binaries
- Zero external runtime dependencies
- Native concurrency (goroutines for background tasks)
- Strong typing catches errors at compile-time

**UI Framework:** Bubble Tea (Go TUI framework)
- Event-driven, reactive model
- Lightweight, no web stack overhead
- Terminal-native, accessible anywhere
- Integrates cleanly with backend logic

**UX Paradigm:** Omnibox / Command Palette pattern
- `/` prefix triggers slash commands
- Conversational input flows to chat
- Slash commands route to deterministic backend functions
- Avoids token waste on LLM-driven UI logic

### Advantages
- Single codebase, portable across machines (Logos, Noesis, future platforms)
- Native performance without Electron overhead
- Terminal-friendly for remote work and coffee shop environments
- Clear separation between UI and backend

### Tradeoffs
- Terminal UI limits richness (MIME viewers require creative solutions)
- Learning curve for Bubble Tea (new framework compared to web stacks)
- TUI paradigm may feel unfamiliar to web-centric developers

---

## 4. Software Architecture: Model-View-Update (MVU)

### Design Pattern
Strict **Separation of Concerns** using MVU (Unidirectional Data Flow):

```
┌─────────────────────────────────────────────┐
│ The Client (TUI)                            │
│ - Captures keystrokes                       │
│ - Renders interface                         │
├─────────────────────────────────────────────┤
│ The State (Shared)                          │
│ - Bulletin board for data                   │
│ - Single source of truth                    │
├─────────────────────────────────────────────┤
│ The Engine (Backend)                        │
│ - Headless orchestrator                     │
│ - Database I/O, API calls, transformations │
│ - Zero knowledge of the TUI                 │
└─────────────────────────────────────────────┘

Flow: TUI emits event → Engine processes → State updates → TUI redraws
```

### Responsibilities

**The Engine (Backend):**
- Database I/O (SQLite, Vector Store)
- LLM API calls (Ollama, local models)
- Data transformations (embeddings, summarization)
- WAL management
- Integration with Layer 2 (Planner)
- **Has no knowledge of the TUI.** Can be tested without UI.

**The Client (TUI):**
- Keystroke capture
- Interface rendering
- Command parsing
- **Purely presentation logic.** Dumb renderer.

**The State (Middle Layer):**
- Central data store
- Shared by Client and Engine
- Unidirectional updates
- Engine reads State, emits updates; Client reads State, renders

### Advantages
- **Decoupling:** Engine is testable in isolation; TUI is interchangeable
- **Clarity:** Data flow is explicit and predictable
- **Portability:** Engine logic can be reused by other UIs (web, API, etc.)
- **Concurrency-friendly:** Goroutines in Engine don't interfere with TUI rendering

### Tradeoffs
- **Indirection:** Three layers instead of direct client-server calls
- **Learning curve:** MVU pattern is common in frontend (React, Elm) but less familiar in Go
- **Initial scaffolding overhead:** More boilerplate to set up cleanly

---

## 5. Model Roles: Rubber Duck vs. Deterministic Work

### Context
Two distinct types of work in Bit:
1. **Chat/rubber duck** — Freeform conversation, exploration, synthesis
2. **Deterministic operations** — Intent translation, formatting, copilot-style refactoring

These have different requirements and should not compete for the same model.

### Design Decision
**Two model roles, not two specific models:**

- **Rubber Duck Role:** 30B-class models, conversational, domain-flexible
  - May rotate 2–3 different models based on domain (e.g., code-focused vs. research)
  - Stays in Bit entirely
  - Optimized for fluency and exploration

- **Deterministic Work Role:** 4–7B-class models, instruction-following, structured output
  - May rotate 2–3 different models for task specialization
  - Handles intent translation, formatting, copilot jobs
  - Optimized for accuracy and compliance with structured schemas

### Concurrency Model
- **Under normal load:** Serial processing (request → model → response)
- **Under load:** Timeslicing between roles if both have pending requests
- **Future optimization:** Parallel inference if VRAM permits

### Advantages
- **Resource efficiency:** Right-sized models for each task
- **Flexibility:** Can swap models without changing architecture
- **Fallback:** If one role's model is slow/unavailable, the other still works
- **Domain specialization:** Can use task-specific models (e.g., code-focused 7B for refactoring)

### Tradeoffs
- **Complexity:** Requires model management and role-switching logic
- **Memory footprint:** Two models in VRAM (or careful unload/reload strategy)
- **Cold start:** Loading a different model incurs latency

---

## 6. Slash Commands & Deterministic Routing

### Design Pattern
Explicit mode selection via slash commands:

```
User input:
  "/memory" → Direct to backend, bypass LLM
  "/embed_session" → Deterministic function
  "/save" → System operation
  "How do I refactor this?" → Chat model

Result:
  - Deterministic operations are guaranteed (no hallucination)
  - LLM focus is on chat, not on control flow
  - Token efficiency (no LLM overhead for system operations)
```

### Advantages
- **Predictability:** Slash commands always do the same thing
- **Token efficiency:** System operations don't consume model context
- **Discoverability:** `/help` shows available commands
- **Debugging:** Deterministic paths are easy to trace

### Tradeoffs
- **UX friction:** User must learn command syntax
- **Less natural:** Requires explicit mode selection instead of intent inference

---

## 7. Topic Packages & Prefill Strategy

### Purpose
Topic Packages are compressed summaries of past sessions, grouped by conceptual topic. They seed the next session with:
- **25% most-frequently-discussed topics** — Recurring concerns
- **75% most-recent topics** — Active work

This balance keeps context relevant without overwhelming the model with stale history.

### Format
Same as WAL format (JSONL or similar), allowing consistent parsing and streaming.

### Generation Frequency
- **Default:** Daily, after analyzing that day's sessions
- **High-activity:** Continuous, if activity threshold is exceeded

Thresholds calibrated during implementation based on observed runtime.

### Storage
**Static cache in Bit** — Topic Packages are mirrored locally as a power-out contingency. If the homelab is unavailable, Bit still has context from the last sync.

### Usage
- **Automatic:** On session start, 25/75 prefill is loaded
- **On-demand:** User can request specific topic packages during a session (mechanism TBD: slash command or UI selector)

### Advantages
- **Context efficiency:** Don't reload entire history; load summaries
- **Offline resilience:** Works without homelab connection
- **Session continuity:** Frequent topics are always available

### Tradeoffs
- **Staleness:** Cached prefill can drift from current state if offline long
- **Summary loss:** Compression loses fine-grained details
- **Generation cost:** Summarization itself requires compute (Workbee task)

---

## 8. Offline Operation & Task Queueing

### Design Decision
When Noesis (or any Bit instance) loses connection to Ergaster (Planner/Router):

1. **Bit continues operating locally** — Chat stays available, deterministic jobs run
2. **Complex jobs are queued** — Tasks requiring Router/distributed work are saved as JSON
3. **Automatic sync on reconnect** — Queued tasks feed to Planner as if user never disconnected

### Queue Behavior
- **Default order:** FIFO (first in, first out)
- **Priority:** Optional per-job; if specified, overrides FIFO
- **Storage:** Local JSON files; no size cap (disk-dependent)
- **Sync:** When Tailscale reconnects, queue is drained to Planner

### Advantages
- **No work loss:** Tasks survive network outages
- **User awareness:** Queue status visible to user
- **Transparent recovery:** Reconnection is automatic

### Tradeoffs
- **Eventual consistency:** Tasks processed later than submitted
- **User responsibility:** Must understand queue may persist if offline long
- **Capacity planning:** Large queues may take time to drain if Planner is busy

---

## 9. Development Methodology

### Training Unit Approach
The Bit implementation serves as a live-fire training ground for Go and software engineering principles. Development breaks into repeatable **Training Units**:

1. **Concept Translation:** Map software concepts to known systems engineering patterns
2. **The Scaffold:** Generate minimal, heavily commented code shells
3. **Implementation:** Write and test the logic
4. **Code Review:** Refine syntax, analyze design choices, integrate

### Obsidian Vault Structure
Documentation and spec drafting live in Obsidian with a **Single Vault, Top-Down Organization:**

```
Obsidian Vault/
├─ 00_System/          (Templates, Attachments, Config)
├─ 01_Homelab/         (Infrastructure docs, hardware specs)
├─ 02_Projects/        (Concierge_Engine, Bespoke_TUI)
├─ 03_Knowledge/       (Go syntax, MVU patterns, design notes)
└─ 04_Work/            (Session notes, implementation journal)
```

This structure allows cross-pollination of ideas and avoids root-level clutter.

### Advantages
- **Structured learning:** Training units build on each other
- **Documentation-first:** Obsidian as single source of truth
- **Portable:** Knowledge is organized, searchable, and transferable

---

## 10. Open Design Questions (To Resolve Before Implementation)

1. **Hard contract JSON schema for intent translation** — Format and examples needed
2. **Slash command registry** — Full list of supported commands and their routing
3. **MIME viewer strategy** — How to display rich content (images, PDFs, etc.) in TUI
4. **Model swap mechanism** — How/when does Bit load/unload different models?
5. **Topic Package on-demand loading** — UI mechanism and latency expectations
6. **Cold context reconstruction** — How does Bit rebuild session context from archived data?
7. **Offline UX for Noesis** — How does user understand queue status and reconnection state?
8. **Memory tier persistence** — What survives a Bit restart? What's ephemeral?

These will be resolved during the Bit Application Specification phase.

---

## Next Steps

1. Formalize the hard contract JSON schema for Layer 1 → Layer 2 escalation
2. Design the slash command registry and routing table
3. Sketch out the TUI layout and MIME viewer approach
4. Create the Bit Application Specification document
5. Begin Go scaffold implementation with training unit framework
