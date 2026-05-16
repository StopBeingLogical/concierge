---
title: Concierge Architecture — Frequently Asked Questions
document_type: reference
version: "1.0"
date: "2026-04-21"
status: drafting
tags: ['faq', 'bit-layer', 'memory', 'model-roles', 'offline-queueing', 'planner-interface', 'implementation']
---

# Concierge Architecture FAQ

## Bit Layer & Intent Translation

**Q: When does Bit talk to the Planner, and what does that conversation look like?**

A: Bit initiates a conversation with the Planner only when there is a need to escalate work beyond the Bit layer's local capabilities. The intent translation component (the secondary model role in Bit) converts user input into a hard contract JSON schema for the Planner. This is the sole interface between Bit and Layer 2. Everything else stays local to Bit.

---

**Q: What is the output format for intent translation?**

A: Hard contract JSON schema. This is the next specification bullet point to address during actual project work. The schema will define the contract between Bit and the Planner, ensuring deterministic routing and no ambiguity in work decomposition.

---

## Offline Queueing & Sync

**Q: What happens when I create a task on Noesis at a coffee shop with no connection?**

A: Tasks are stored locally as JSON files in an offline queue. When communication is reestablished (Tailscale reconnects), the queued jobs are fed to the Planner exactly as they would have been had you been connected. FIFO ordering is the default.

---

**Q: Can I set priorities on queued tasks?**

A: Yes, priority is optional on a per-job basis. If no priority is specified, FIFO ordering applies. Priority levels are specified in the task JSON when creating the job.

---

**Q: Are there caps on how many tasks can be queued?**

A: No arbitrary caps. Tasks are JSON files, so storage is not a constraint in a homelab context. Queue size is limited only by available disk space on the device running Bit.

---

**Q: How does the Planner know the task was queued offline vs. submitted directly?**

A: The Planner doesn't care. When connection is reestablished, queued tasks are fed to the Planner sequentially, and the Planner processes them identically to tasks submitted directly. There's no distinction at the Planner layer.

---

## Model Loading & Concurrency

**Q: How does Bit handle concurrent requests when both model roles are busy?**

A: Bit uses timeslicing under load. If multiple requests arrive and both model roles are occupied, Bit context-switches between them rather than queuing. Under normal load (single requests, idle periods), processing is serial.

---

**Q: What's the VRAM budget for running two models on Logos (M1 Max 64GB)?**

A: This is not yet specified and will depend on:
- OS overhead (macOS + running applications)
- Which specific models fill each role (30B class vs. 7B class)
- Whether both models are loaded simultaneously or one is swapped out

This will be calibrated during implementation based on observed memory usage.

---

## Model Roles (Not Specific Models)

**Q: Are there "rubber duck" and "deterministic work" models, or are these just roles?**

A: These are **roles, not specific models**. You may rotate different models through each role depending on context:
- **Rubber duck role** (primary LLM): 2–3 different 30B-class models, potentially domain-specific
- **Deterministic work role** (intent translation, copilot-style jobs): 2–3 different 4–7B-class models

Model selection for each role can be switched based on the current task or your intent.

---

**Q: Can I have knowledge-domain-specific models in the rubber duck role?**

A: Yes. For example, you might load a 30B model fine-tuned on software engineering contexts for code-related rubber duck sessions, and a different 30B model for research or writing sessions. Role-based switching allows this flexibility.

---

## Prefill Packages (Topic Packages)

**Q: What format are Topic Packages stored in?**

A: The same format as the Write-Ahead Log (WAL). Unless a specific format emerges during implementation that better serves the use case, Topic Packages use the same structure as WAL entries for consistency and simplified parsing.

---

**Q: How often are Topic Packages generated?**

A: Two triggers:
1. **Default (daily)**: After each day's sessions are analyzed by the background process, a fresh Topic Package is generated.
2. **High-activity (continuous)**: If activity reaches a specific threshold (e.g., X sessions, Y total turns, Z memory size), Topic Package generation is triggered immediately rather than waiting for the daily cycle.

Exact thresholds will be calibrated based on observed runtime characteristics when implementation begins.

---

**Q: Is the prefill package mirrored to Bit as a static copy?**

A: Yes. Bit maintains a static cached copy of the prefill package as a contingency for power loss, network unavailability, or homelab outages. This ensures context continuity even when Ergaster or the wider fleet is unreachable.

---

**Q: How often is the static prefill package in Bit updated?**

A: Synchronized with Topic Package generation frequency. When a new Topic Package is generated on Ergaster, the static copy in Bit is updated (via sync when Noesis/Logos reconnect, or immediately if always connected).

---

## Local Deterministic Jobs

**Q: What kinds of jobs run entirely on Bit without escalating to the Planner?**

A: Jobs that are deterministic and local-only:
- "Lint/cleanup this text document"
- "Tell me how to better layout this Excel sheet"
- Refactoring suggestions (copilot-style)
- Code formatting and style fixes
- Any task closer to deterministic than generative

These use the deterministic work model role and never leave Bit.

---

**Q: Can a deterministic job escalate to the Planner if it's too complex?**

A: The boundary is strict: if a task falls under "deterministic + local," it stays in Bit. Tasks that require Planner involvement are recognized at intent-translation time and routed explicitly. There's no auto-escalation from a local job.

---

**Q: How does Bit know if a task is deterministic or generative?**

A: The user's intent and the secondary model's analysis determine this. If the secondary model (intent translation role) can structure the request as a deterministic operation, it stays local. If it requires planning, decomposition, or distributed work, it escalates via the hard contract JSON schema to the Planner.

---

## Topic Packages & Memory

**Q: What are Topic Packages specifically used for?**

A: Topic Packages are generated from session analysis and used to support rubber duck (primary chat) sessions. The 25% frequent + 75% recent prefill mix gives context to subsequent chat sessions without requiring full history.

---

**Q: Can the rubber duck model read Topic Packages during a session?**

A: Yes. Topic Packages (cached locally in Bit) can be loaded on-demand during a chat session if you request context for a specific topic. This is a user-initiated action, not automatic.

---

**Q: Are Topic Packages meant to update Tier 0 (session-only memory)?**

A: Topic Packages seed the prefill for a session, but session context itself (Tier 0) is managed separately via the WAL + background flush process. Topic Packages are read-only inputs to inform the rubber duck model; they don't directly update memory tiers.

---

**Q: How do I load a specific Topic Package during a chat?**

A: This is TBD during implementation. Likely candidates:
- A slash command: `/load_topic <topic_name>`
- An interactive selector in the Bit UI
- Automatic loading based on detected context

The mechanism will be specified in the Bit implementation docs.

---

## Next Steps

Questions not yet answered or require implementation decisions should be filed against the project and addressed during the next specification sprint. This FAQ is a living document and will be updated as answers become concrete.
