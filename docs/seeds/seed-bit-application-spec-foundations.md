---
title: "Seed — Bit Application Specification Design Foundations"
document_type: seed
date: "2026-04"
status: current
tags: ['bit', 'application-spec', 'prosthetic', 'protocol-translator', 'ui']
---

# Seed: Bit Application Specification — Design Foundations

*Captured from session conversations April 2026. Drop into the Bit Application Spec drafting session as the foundational design brief. These are settled decisions, not open questions.*

---

## What Bit Is

Bit is not an interface. It is a **total environment** — the surface through which everything flows between the user and Concierge in both directions.

Bit has two distinct and equally weighted jobs that must coexist in the same surface:

### 1. Prosthetic Layer
Bit models the user, adapts to their cognitive state, holds what they can't hold, and feeds information back at the right moment in the right form. The interface is shaped around the user's cognitive profile — not a generic presentation layer.

The original design motivation: offload the cognitive overhead of remembering, organizing, and tracking onto the machine so working memory isn't spent on housekeeping. The user externalizes whatever is in their head, mixed and unstructured, and the system figures out what each fragment means, where it belongs, and files it without asking for clarification.

**The canonical success criterion for this mode: zero follow-up questions from the system.** It routes, files, and confirms.

### 2. Protocol Translator
Bit converts human intent into valid Concierge inputs — structured job submissions, correctly scoped, with enough contract information for the Router to work with. It also converts Concierge outputs (job results, status updates, Planner summaries) back into human-readable form that doesn't require the user to understand what happened under the hood.

Bit absorbs the tension between these two jobs so the user doesn't feel it. The prosthetic wants to be frictionless and forgiving. The protocol translator needs precision. Bit reconciles this invisibly.

---

## Interaction Modes

### Default Mode: Freeform Dump
The user externalizes a stream of mixed, unrelated, unstructured inputs in a single entry. Bit infers intent for each fragment, routes each to the correct destination or Task Package, and confirms. No restructuring required from the user. No follow-up questions unless stakes warrant it.

Example input handled in one shot:
> "ate 3 cookies and a diet coke, slept 5 hours, add 'purple socks' to my notes for the murder mystery, remind me to call the dentist thursday"

Each fragment routes independently. Confirmation is a single summary, not per-item prompts.

### Explicit Mode: Slash Command Triggers
For high-frequency, well-defined input types where inference overhead isn't worth it, Bit exposes slash command prefixes that collapse ambiguity entirely and select the correct Task Package before any processing happens.

Example: `/foodlog ate 3 cookies and a diet coke`

The prefix signals intent with 100% confidence. No inference required. The designated Task Package handles all downstream processing (appending to log, nutrition lookup, record-keeping).

**The two modes are complementary, not competing.** Slash commands for things done repeatedly and predictably. Freeform dump for everything else.

### Ambiguity Resolution Principle
Bit resolves the tension between forgiving input acceptance and precise job contract construction through a stakes-weighted approach:

- **Low confidence + low stakes:** Pick the most likely interpretation and proceed. Do not interrupt.
- **Low confidence + high stakes:** Surface the ambiguity in the simplest possible form. Ask exactly one question.

This mirrors the Planner's gap resolution behavior at the human interface layer.

---

## Confirmation Behavior

A confirmation step is standard for anything writing to a persistent record. Low friction, single interaction, closes the loop. Not optional for record-keeping operations — the user needs to know the write happened and what was written.

---

## Output Layer: Cognitive Profile Requirements

Bit's output layer must be adaptive, not generic. It needs to maintain a cognitive profile for the user covering:

- **Output density** — how much information per response
- **Compression preference** — summary vs. full detail
- **Presentation format** — what structure aids processing
- **Timing and interrupt behavior** — when to surface results immediately vs. queue for later
- **Ambiguity threshold** — when is a question worth asking

This profile is not static configuration. It should be distilled from observed interaction patterns and explicit user feedback, and updated as behavior calibrates over time. It is loaded at the start of every session.

**Reference pattern:** The CCSS (Cognitive Architecture Protocol) concept — a JSON profile distilled by the LLM from natural language self-description, loaded before every session to shape how inputs are interpreted and outputs are formatted. Bit's onboarding should follow a similar pattern: interview the user, distill to structured profile, load on every session.

---

## Bit's Relationship to the Rest of Concierge

- Bit is the **Planner's outward face toward the user**
- Bit does not pull from the ensemble work pool — it is exclusively the human interaction layer
- Bit submits jobs to the Planner; it does not decompose them
- Bit presents Planner and Foreman outputs back to the user; it does not interpret execution internals
- Logos is Bit's host node — quality-first model selection (34B range), not CPU-fallback framing

---

## Open Design Questions (Not Yet Resolved)

These are flagged for the drafting session, not pre-answered here:

- Full slash command vocabulary — which interaction types warrant explicit triggers vs. freeform inference
- Interrupt vs. queue policy — specific rules for when Bit surfaces results proactively
- Cognitive profile onboarding flow — how the initial interview is structured
- Multi-modal input handling — voice, text, file drop — and whether mode affects routing behavior
- How Bit surfaces ambiguity from deep in the pipeline (e.g., a Workbee hits an unclear contract constraint) back to the user in plain language