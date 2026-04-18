---
title: "Concierge — Session Seed"
document_type: seed
version: "1.0"
date: "2026-03"
status: current
tags: ['session-seed', 'context', 'onboarding']
---

# CONCIERGE — SESSION SEED
**Version:** 1.0 — March 2026
**Purpose:** Single-file context primer for new chat sessions. Replaces CORE_DUMP, EVOLUTIONARY_DUMP, POSTMORTEM, CONTRACTS_COMPILATION, and SNAPSHOTS 1–2.
**Usage:** Paste into project store. Load at session start. Read alongside active spec docs.

---

## What Concierge Is

Concierge is a personal AI task orchestration system designed for a homelab cluster. It accepts human intent through a front-end application, routes it through a layered AI pipeline, and returns completed work. It is designed to be published on GitHub for others to fork and adapt to their own hardware.

The guiding philosophy is: **constraints are contracts**. Every boundary between layers is enforced by a typed, versioned, schema-validated artifact. Nothing crosses a layer boundary informally.

Companion documents (full content, keep in project store):
- `Concierge_Philosophy_v5.md` — what it is and why
- `Concierge_Technical_Spec_v5.md` — what it does and how (COMPLETE, 1,852 lines)
- `Concierge_Hardware_Appendix_v5.md` — hardware fleet reference
- `Concierge_Memory_Spec_v5.md` — memory system internals (COMPLETE)

---

## The Stack

```
Bit → Planner → Router → Foreman → Workbee
```

Each layer communicates only with its immediate neighbors. No layer has knowledge of non-adjacent layers. This is an architectural invariant, not a guideline.

| Layer | Job |
|---|---|
| **Bit** | Human-facing application. Captures intent, emits Intent Artifacts, surfaces plans for approval, delivers results. |
| **Planner** | Receives intent, matches Task Packages, queries Router for tool availability, generates Execution Plans, owns Gap Resolver. |
| **Router** | Receives approved Job Specs, schedules work across nodes. Internal design deferred to dedicated peer review session. |
| **Foreman** | One per physical system. Manages execution on its system's nodes. |
| **Workbee** | Executes individual work chunks. One per schedulable compute surface (node). |

---

## Naming Conventions (Locked)

| Domain | Scope |
|---|---|
| Greek / Latin | Hardware nodes (Logos, Atlas, Daemon, etc.) |
| Sumerian | Top-level software projects (NISABA, NIDABA, ENKI, Concierge) |
| Egyptian | AI context / seed documents (Seshat) |
| **Hittite** | **Internal components of Concierge** |

Hittite chosen because Hittites are the civilization most associated with formal written contracts and treaty law — maps directly to "Constraints Are Contracts."

Each project gets its own civilization domain for internal components.

---

## Hittite Named Components (Locked)

| Hittite Name | Internal Concept | Description |
|---|---|---|
| **Harkanza** | `pending_revision` | Denied job holding state. Job sits here after human denies a plan, awaiting revision and resubmit. Not discarded, not failed. Human may edit intent, request new plan, resubmit, or cancel explicitly. Nothing in Harkanza acts automatically. |
| **Handanza** | `pending_foundation` | Job waiting for tool build. Queued but cannot execute until missing tools are created by foundation generation. |
| **Tarhuili** | unregistered approximation mode | "YOLO mode." Planner approximates a pipeline without a registered Task Package. Still requires human confirmation. Activates when no Task Package matches above threshold. |
| **Hašatar** | `foundation_generation` | Task status tag. Indicates the system is actively building tools to service a queued request. Enabled by the Foundation Generation Mechanism. |

---

## Locked Architectural Decisions

### Terminology
- **System** = physical device (one Foreman per system)
- **Node** = individually schedulable compute surface within a system (one Workbee per node)

### Layer Design
- **Unified tool pool** — replaces the retired Lane A/B concept. Tools are registered globally; scheduling assigns them to nodes.
- **Bit** is a full-featured application with connected and disconnected operating modes.
- **Reconnection handshake** — queued intents surface to human for review before any automatic flush. Nothing flushes without human approval.
- **Ranked multi-intent disambiguation** — current spec requirement, not deferred. Bit presents ranked candidates; top-ranked is pre-selected; full list available via disclosure control.
- **Planner owns the Gap Resolver** and queries Router for tool availability *before* plan generation.
- **`capability_exceeded`** includes missing recommended models or tools that would degrade output quality at high confidence — not just hard capability gaps.
- **Harkanza** (`pending_revision`) is a named holding state visible in Bit's dashboard. Denied jobs go here, not to `failed`.
- **Router internal design** explicitly deferred — dedicated multi-model peer review session required.
- **Foundation Generation Mechanism** enables self-directed tool building (Hašatar tag, Handanza state).

### Integrity
- SHA256 only. Every artifact crossing a layer boundary carries a hash. Receiving layer verifies before processing. Mismatch is always a hard failure (`integrity_violation` terminal state). No recovery, no retry. Integrity violation events retained indefinitely.

### Onboarding
- Tool packages are self-sourcing — they specify their own dependencies and install them.

---

## Spec Document Status

| Document | Status | Notes |
|---|---|---|
| `Concierge_Technical_Spec_v5.md` | **COMPLETE** | 1,852 lines, 9 sections. All Hittite names in place. |
| `Concierge_Memory_Spec_v5.md` | **COMPLETE** | Covers all four memory tiers, schemas, write protocols, reference resolution. |
| `Concierge_Philosophy_v5.md` | **COMPLETE** | Working canon. |
| `Concierge_Hardware_Appendix_v5.md` | **COMPLETE** | Working canon. |
| Router Design Specification | **NOT STARTED** | Separate document. Requires dedicated peer review session. |
| Bit Application Specification | **IN PROGRESS** | Separate document. Scope being defined. |

### Technical Spec Section Status
All 9 sections complete:
1. Layer Interface Contracts
2. Task Package Registry
3. Gap Resolver and Foundation Generation
4. Node and System Management
5. Scheduling and Priority
6. Approved Sources
7. WorkbeeSim (test harness)
8. Integrity Chain
9. Memory System Interface Contract

---

## Open Questions / Deferred Items

1. **Remediation tooling and operator workflow** for node degradation — defined in spec, not yet fully operationalized.
2. **Approved Sources List initial population** — deployment decision not yet made.
3. **Router deep design session** — multi-model peer review, separate session. Internal design of Router is deliberately unspecced. Open agenda items from April 2026 hardware session: (a) island capability advertisement schema for dual operating modes (normal vs burst); (b) burst mode drain protocol and timeout handling; (c) tensor split parameter ownership — Router vs Foreman; (d) burst mode SLA classification during P1 execution; (e) Daemon-only burst ceiling vs cross-node shard decision boundary.
4. **Bit Application Specification** — scope definition in progress. Drafting next.
5. **NIDABA enrichment protocol** — Memory Spec defines the interface; enrichment pipeline detail TBD.

---

## Infrastructure Reference

| System | Role | Notes |
|---|---|---|
| **Atlas** | TrueNAS Scale, Ryzen 5700G, 64GB | Runs Nextcloud (`nextcloud.damnaliens.us`), Forgejo (`forgejo.damnaliens.us`), Nisaba, Homarr (7575), Open WebUI (3001), SearXNG (8888), Tailscale, nginx-proxy-manager |
| **Logos** | MacBook Pro M1 Max, 64GB | Bit workstation, Tailscale client. Exclusive human interaction layer. Not a Workbee. |
| **Kratos** | Ryzen 7600X, RX 7800 XT, 32GB | Ollama inference (ROCm, 192.168.3.138:11434) |
| **Ergaster** | i9-13900HX, 64GB | Router/Planner control plane. Ollama (CPU-only, TBD) |
| **Daemon** | i7-12700F, 32GB | Inference cluster: RTX 5060 Ti (x16), Tesla P100 ×2 (x8, x4). Burst mode architecture. |
| Claude.ai | AI interface | Pro plan |

### Daemon Corrected PCIe Topology (April 2026)

| Card | Slot | PCIe Speed | Practical BW | VRAM |
|---|---|---|---|---|
| RTX 5060 Ti | PCIe 3.0 x16 | x16 | ~16 GB/s | 16 GB GDDR7 |
| Tesla P100 #1 | PCIe 3.0 x8 | x8 | ~8 GB/s | 16 GB HBM2 |
| Tesla P100 #2 | PCIe 3.0 x4 | x4 | ~4 GB/s | 16 GB HBM2 |

Three operating modes: Island A (5060 Ti alone, P1 hot path), Island B (dual P100 shard, 32 GB, 34B ceiling), Burst (all three, 48 GB, 65B ceiling — Islands A+B suspended for independent work). Inter-P100 all-reduce bounded by x4 slot. Full detail in `Concierge_Hardware_Appendix_v5.md`.

### Working File Interchange Architecture
Claude produces documents in project chat → handoff packet pasted into Claude Desktop → desktop app executes and writes to locally synced folder → Nextcloud on Atlas → iOS via Files app.

**Handoff contract schema v0.2:** JSON envelope with payload, execution manifest, and return contract.

**Nextcloud MCP path:** `cbcoutinho/nextcloud-mcp-server` identified as the path to bidirectional file sync from Claude Desktop. Not yet configured.

### Tool Notes
- `web_fetch` works reliably on `raw.githubusercontent.com` URLs. `github.com` repo pages are blocked at network level.
- Google Drive connector reads native Google Docs only — uploaded `.docx`, `.pdf`, `.md` files are metadata-searchable only, content not readable.
- `ask_user_input_v0`: takes `questions` as list of objects with `type` (`single_select` or `multi_select`), `options` array, `question` string.

---

## Archive Index
The following files were retired from the project store to reduce context load. They live in Forgejo / Nextcloud. Fetch from archive only if you need to reconstruct pre-v5 decision history.

| File | What It Was | Why Archived |
|---|---|---|
| `CONCIERGE_TECHNICAL_POSTMORTEM.md` | 916K retrospective analysis of pre-v5 architecture | Historical. All live decisions are in the v5 spec. |
| `CONCIERGE_EVOLUTIONARY_DUMP.md` | 333K NIDABA semantic atom dump of evolutionary history | Raw vector export. Not a curated decision record. |
| `CONCIERGE_CORE_DUMP.md` | 338K NIDABA semantic atom dump | Raw vector export. Titles only, no curated content. |
| `CONCIERGE_CONTRACTS_COMPILATION.md` | 290K NIDABA contract atom dump | Raw vector export. Mixed with non-Concierge project contracts. |
| `CONCIERGE_SPEC_SESSION_SNAPSHOT.md` | 34K session handoff — pre-v5 assembly | Superseded by Snapshot 3. |
| `CONCIERGE_SPEC_SESSION_SNAPSHOT_2.md` | 34K session handoff — mid-assembly | Superseded by Snapshot 3. |
| `concierge_concept_v5.md` | 55K early concept document | Superseded by Technical Spec and Philosophy doc. |

---

*Seed updated April 13, 2026. Remote access scaffold (Phases 1-3) complete. Tailscale VPN operational (Atlas 100.101.158.93, Logos 100.88.51.60). Homarr dashboard live on port 7575. Open WebUI + Ollama integration verified with Gemma 4 26B MoE model. SearXNG self-hosted web search deployed (port 8888, zero API cost). Integration guides created. Next: Bit Application Specification scope definition, then drafting.*
