---
title: "Analysis: Claude + Obsidian as AI Operating System (Eric Michaud)"
document_type: analysis
date: "2026-04-11"
status: reference
tags: ['obsidian', 'claude-code', 'personal-os', 'memory', 'bit-application', 'vault-architecture']
---

# Analysis: Eric Michaud — Claude + Obsidian as AI Operating System

*Analyzed through the lens of Concierge architecture. Source is a YouTube tutorial transcript demonstrating a personal productivity OS built by wiring Claude Code into an Obsidian vault.*

---

## What This Actually Is

Eric's setup is a **personal productivity OS** using Claude Code as an intelligent file agent operating inside an Obsidian vault. The core insight is that Obsidian provides persistent local storage and Claude Code provides the intelligence to navigate and write to it — solving Claude Code's fundamental amnesia problem (all context lost between sessions).

### Core Components

**Obsidian** — local markdown file store, structured vault, wiki-links, plugin ecosystem. All storage is local files; no cloud dependency.

**Claude Code** — agentic CLI that reads and writes to the vault, runs slash commands, routes inputs to the correct locations. Runs via integrated terminal inside Obsidian.

**claude.md** — the "brain file." A root-level document that Claude reads first on every session to understand vault structure, behavioral rules, and conventions. Equivalent to a persistent system prompt that the agent itself can update.

**Slash commands** — user-defined workflows (`/today`, `/new`, `/comments`) that trigger multi-step automated routines without requiring the user to write a full prompt each time.

**Human/Machine vault split** — a deliberate architectural decision to separate content the AI can read but not write (personal voice, raw journal, daily notes) from content the AI owns (SOPs, templates, research output, scripts, workflows).

---

## Architectural Pattern

```
User types slash command or freeform input
        │
        ▼
Claude Code reads claude.md (brain file / system context)
        │
        ▼
Agent routes input → correct vault folder / file / project
        │
        ├── Human side (read-only for AI): journal, relationships, daily notes
        └── Machine side (AI read/write): SOPs, templates, research, scripts
        │
        ▼
Output written to vault; user sees result in Obsidian UI
```

The `/today` workflow is the most fully realized example: Claude reads email, calendar, daily notes, and project files across the entire vault, then synthesizes a prioritized task list — surfacing slipping commitments and items that have been deferred too long.

---

## Relevance to Concierge

### Conceptual Overlap

The mapping to Concierge components is surprisingly direct. This is essentially a single-node, single-user Concierge implementation — without the distributed inference cluster, job contracts, or Router layer.

| Eric's System | Concierge Equivalent |
|---|---|
| `claude.md` brain file | Session seed / CONCIERGE_SESSION_SEED.md |
| Vault folder structure | Tier 1–3 memory (working context, episodic, semantic) |
| Human/machine folder split | User-input separation from agent-writable context |
| Slash commands | Task Package dispatch |
| `/today` workflow | Planner morning brief job |
| Input routing to correct files | Router + Foreman decomposition |
| Templates and SOPs | Task Package schemas |
| "swap Claude for Gemini if rate-limited" | Router fallback / capability-based selection |

### What Concierge Does That This Doesn't

- Multi-node distributed inference across heterogeneous hardware
- Job contracts with typed output schemas (Constraints Are Contracts)
- Router capability scoring and Workbee selection
- Foreman-level job decomposition and parallel execution
- OTel distributed tracing and Langfuse correlation
- Harkanza / Handanza job state management
- Execution checkpointing and graceful degradation

Eric's fallback strategy when rate-limited (manually switch to a different agent) is the ad hoc version of what Concierge's Router handles automatically and transparently.

### What This Does That Concierge Hasn't Designed Yet

**This is the more actionable direction.**

The Bit Application Specification is still unwritten. Eric's system is a working reference implementation for what Bit's interaction surface could look like in practice:

1. **Slash command dispatch as a UX primitive.** The user types `/today` or `/new` and gets a full multi-step workflow executed without constructing a prompt. This is the interaction model Bit should expose — the user should never think about the pipeline underneath. The slash command is the contract surface at the human layer.

2. **Brain file as living system prompt.** The `claude.md` file is user-editable, agent-updatable, and read at the start of every session. It encodes behavioral rules, vault conventions, and context. This is a working implementation of what Concierge's session seed does — but with the additional property that the agent itself can write to it as understanding evolves. Worth considering whether Bit should maintain a similar living context document distinct from the static session seed.

3. **Human/machine write-permission split.** This is a concrete answer to a memory architecture question Concierge hasn't fully resolved: *who can write where in persistent memory?* Eric's model is clean — human-authored content is a protected namespace; agent-authored content lives separately. The boundary is enforced by convention (and by explicit instruction in claude.md) rather than by access control. Concierge could formalize this as a Tier boundary property: certain memory tiers are agent-readable but not agent-writable without explicit user authorization.

4. **Freeform input routing as the default interaction mode.** The `/new` command accepts a stream of mixed, unstructured inputs ("send a message to X, I had 4 cups of coffee, 30 minutes on the bike, I'm filming the video now, look into templatizing the email campaign") and routes each item to the correct destination autonomously. This is the Bit experience that the current spec doesn't yet describe in detail — the user dumps context and the system figures out what to do with all of it.

---

## Key Insight for Concierge

Eric's setup demonstrates that **the memory problem and the UX problem are the same problem.** Obsidian-as-persistent-vault solves memory; slash-commands-as-workflow-dispatch solves UX. Both are expressions of the same underlying need: a stable, navigable context that the agent can read fluently and write to predictably, exposed to the user through a frictionless interaction surface.

Concierge has a more sophisticated answer to the memory problem (four-tier architecture, OTel tracing, distributed context) but has not yet written the answer to the UX problem. The Bit Application Spec should treat Eric's slash command + daily brief pattern as a concrete prior art reference for what the human interaction layer needs to feel like.

---

## Honest Assessment of Eric's Approach

The setup works well for a single-user personal productivity context and Eric's demonstration is genuine — not a polished demo. The human/machine split is a thoughtful design decision that most people building similar systems skip.

Limitations relative to Concierge's scope:
- No parallelism; all inference is sequential through one Claude Code session
- No capability routing; model selection is manual
- No typed output contracts; correctness depends on prompt conventions
- Memory is flat markdown files; no semantic retrieval, no embedding search, no structured graph
- Self-contained to one machine; no fleet coordination

These are not criticisms of Eric's system — it is solving a different problem at a different scale. They are the precise gaps that Concierge was designed to address.