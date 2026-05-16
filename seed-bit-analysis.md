---
title: "Concierge — Bit Application Analysis Seed"
document_type: seed
version: "1.0"
date: "2026-04-21"
status: current
tags: ['bit', 'analysis', 'roadmap', 'specification-foundations']
---

# CONCIERGE — BIT APPLICATION ANALYSIS SEED
**Version:** 1.0 — April 21, 2026
**Purpose:** Captured analysis of the Bit component (Layer 1) to guide the upcoming Go-based implementation and formal specification drafting.

---

## 1. Bit Component Overview

### Purpose: The Prosthetic and the Translator
Bit is the **Layer 1: Human Interface** of the Concierge system. It serves two primary roles:
*   **Prosthetic Layer:** Offloads cognitive overhead by allowing the user to "externalize" unstructured thoughts. It adapts to the user's cognitive state, holding what they cannot, and surfacing information at the right moment.
*   **Protocol Translator:** Converts messy human intent into deterministic, schema-validated **Intent Artifacts** for the Planner (Layer 2) and translates system outputs back into human-readable forms.

### Genesis: From Control Plane to Intent Engine
Originally conceived as the "Concierge Shell" with direct execution authority, Bit was refactored in early 2026 to enforce a strict boundary called the **Lock List**. This list forbids Bit from planning execution or invoking tools directly, ensuring it remains an intent-capture engine and "dumb" presentation layer, while the "thinking" happens in the distributed fleet.

### Expectations: MVU and Local Autonomy
*   **Architecture:** Follows the **Model-View-Update (MVU)** pattern for strict separation of UI and logic.
*   **Language:** To be implemented in **Go** using the **Bubble Tea** TUI framework for performance, portability, and native concurrency.
*   **Local Models:** Runs small, resident "Rubber Duck" (conversational) and "Deterministic" (instruction-following) models locally on the host node (Logos/Noesis) for immediate interaction without homelab dependency.
*   **Integrity:** Employs SHA256 hashing to create a cryptographic integrity chain from the moment of input.

### Current Ideation
*   **Thick Client with WAL:** Uses a Write-Ahead Log (WAL) for zero-latency persistence and crash recovery.
*   **Interactive Isolation:** Chat models are isolated from infrastructure tasks (summarization, memory writes) which are handled by background processes.
*   **Cognitive Profile:** Maintains a user profile (Output density, compression preference, etc.) to tailor the interface behavior.

---

## 2. Hitlist: Steps to the Full Vision

1.  **Go/Bubble Tea Scaffold:** Build the foundational MVU architecture in Go.
2.  **Local Model "Advisory" Integration:** Connect to local model backends (Ollama/llama.cpp) for "Rubber Duck" and "Deterministic" roles.
3.  **Omnibox & Slash Commands:** Implement the command palette for both freeform inference and deterministic `/slash` triggers.
4.  **State Visibility (Harkanza/Handanza):** Create UI views for pending revisions and pending foundation (tool-building) states.
5.  **Workspace Browser:** Build a TUI file/artifact manager restricted to the six-directory workspace boundary.
6.  **Offline Queue Manager:** Implement local intent queueing and the "reconnection handshake" logic.
7.  **Cognitive Profile Onboarding:** Create the initial "interview" flow to distill the user's CCSS (Cognitive Architecture Protocol) profile.

---

## 3. Specification Drafting Roadmap

1.  **UI State Machine:** Map all interface states (Idle, Inference, Approval, Syncing) and their transitions.
2.  **Intent Schema Definition:** Formalize the JSON structure of Intent Artifacts, including metadata and hashes.
3.  **Component Hierarchy:** Design the TUI layout and define the "MIME viewer" strategy for rich content in the terminal.
4.  **Local Model Registry:** Define the logic for selecting and swapping local models for different roles.
5.  **Persistence Policy:** Document WAL format, flush triggers (timer vs. token ceiling), and directory structures.
6.  **Approval Gate Protocol:** Define the UX for human plan approval and the signing of cryptographic attestations.

---

**Source:** Architecture synthesis session — April 21, 2026.
**Next Milestone:** Bit Application Specification drafting.
