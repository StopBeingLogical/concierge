---
title: "Concierge — Session Seed Addendum (April 2026)"
document_type: seed
version: "1.0"
date: "2026-04"
status: current
tags: ['session-seed', 'ecosystem-survey', 'addendum']
---

# CONCIERGE — SESSION SEED ADDENDUM
**Version:** 1.0 — April 2026
**Purpose:** Addendum to `CONCIERGE_SESSION_SEED.md` covering ecosystem survey session. Merge into next seed version or load alongside it.

---

## Session Summary

This session surveyed the broader agentic AI ecosystem (Hermes Agent, OpenClaw, LangGraph, CrewAI, AutoGen/MAF, OpenAI Agents SDK, et al.) and extracted concepts and technical implementations relevant to Concierge. Bobby reviewed all suggestions and confirmed a set of decisions.

---

## Ecosystem Position

Hermes Agent (Nous Research) and OpenClaw are the two most prominent personal/homelab-oriented open-source agents. Both converge on: persistent memory, local-first deployment, self-hosted inference, multi-platform messaging, and skills-based tool extension.

**Where they align with Concierge:** surface goals (persistent memory, local inference, tool use, heterogeneous model routing). The convergence is genuine but shallow.

**Where Concierge is architecturally distinct:**
- No formal job state machine in either (no equivalent to Harkanza, Handanza, Tarhuili, Hašatar)
- No cluster-aware dispatch — both are single-loop synchronous executors, not distributed orchestrators
- No capability admission criterion — they gate access, not capability advertisement
- No foundation generation loop — they fail and report; Concierge holds and builds
- No contract-based Task Package execution — their "skills" are LLM documentation, not validated execution contracts
- Human-in-the-loop is an incident response mechanism for them; for Concierge it is a first-class architectural layer (Bit)

Summary framing: Hermes/OpenClaw are "a smart assistant that lives on your server." Concierge is "a cognitive operating system for a distributed inference cluster."

---

## Confirmed Decisions from This Session

### Standards Adoption (Locked)

**1. OpenTelemetry (OTel) for distributed trace correlation**
- Every layer (Bit → Planner → Router → Foreman → Workbee) emits OTel spans
- Job ID is the trace root — all spans for a job are correlated under it
- Self-hosted **Langfuse** (open-source, Docker-deployable) as the backend — fits Atlas homelab model
- Enables: post-hoc replay of any job's full execution path, state transition audit, prompt/tool call inspection
- When a job enters Harkanza, the full trace should be surfaced in Bit alongside the denial reason

**2. Google A2A Protocol conventions inform the Dispatch envelope schema**
- Concierge's internal communication remains bespoke by design
- But the Dispatch envelope JSON (currently at v0.2) should be aligned with A2A field conventions where possible
- Goal: future external agent interoperability without a schema rewrite
- Not a constraint on internal behavior — a compatibility layer at the envelope boundary

**3. Progressive disclosure for Task Package loading**
- Router advertises Task Package **summaries** to the Planner (name, capability claim, cost/resource hint, node affinity)
- Planner selects from summaries; Foreman fetches the full Package only for the selected Workbee
- Keeps Planner context window clean as the catalog grows
- Secondary benefit: forces Package authors to write accurate, informative capability summaries (emergent quality incentive)

---

## Open Items to Address During Spec Review

These were surfaced in this session and agreed as worth incorporating. They are not yet specced. Flag them when reaching the relevant sections.

**A. Typed Task Package output contracts**
- Task Packages should declare their output schema (e.g., `FileArtifact`, `TextResult`, typed struct)
- Foreman validates actual output against declared schema at job completion before marking `complete`
- This is the execution-time realization of "Constraints Are Contracts" — contracts enforced at runtime, not just at design time
- Technical path: Pydantic or equivalent for schema definition and validation

**B. Execution checkpointing at the Foreman/Workbee boundary**
- When a Workbee completes a step inside a multi-step Task Package, checkpoint state before proceeding to next step
- Enables: graceful degradation (job migrated mid-execution to another node), restart-from-checkpoint on node failure
- Natural checkpoint store: Nextcloud on Atlas (already in the interchange architecture)
- Relevant to: Node and System Management section, Scheduling section, possibly a new Resilience section

**C. Router reliability signal fed by Foreman outcome data**
- Router currently advertises static capability — what nodes *can* do
- Over time, Foreman outcome data (latency, quality signal, failure rate per node/task-type) should inform capability scoring
- Router becomes a dynamic capability advertiser, not just a static registry
- Implementation detail deferred; concept should be reflected in Router design session agenda
- Note: Bobby's confirmed position is that this is distinct from the automatic Task Package generation loop — Foreman outcomes inform *both* the Router's runtime scoring *and* the Package maker's improvement process

---

## Bobby's Confirmed Positions (For Future Reference)

- **Local models are doers, not thinkers.** Frontier models own planning, gap resolution, and contract-aware decomposition. Local models execute. The community's use of local models for planning is acknowledged but not adopted — their success cases are narrowly scoped, templated, and repetitive pattern-matching, not genuine first-principles reasoning. Concierge's Planner requires the latter.

- **Standards over bespoke, where standards exist.** Where an open standard exists for a problem Concierge needs to solve (observability, agent communication protocol), adopt it at the foundation rather than invent. The system performing and producing as intended takes priority over technical elegance of a custom solution.

- **Progressive disclosure already implicit in architecture.** The Router summary → Foreman full-fetch pattern is a better implementation of what was already intended, not a change to intent.

---

## Additions to Router Design Session Agenda

Add to the existing agenda items in the main seed:

- (f) OTel span schema for Router layer — what fields does a Router trace span carry?
- (g) A2A alignment audit of Dispatch envelope — field-by-field review against A2A conventions
- (h) Capability summary schema — what fields does a Task Package summary advertisement contain?
- (i) Reliability signal data model — how does Foreman outcome data flow back to Router scoring?

---

*Addendum created April 2026. Covers ecosystem survey session. Merge into CONCIERGE_SESSION_SEED.md v1.1 at next seed refresh.*
