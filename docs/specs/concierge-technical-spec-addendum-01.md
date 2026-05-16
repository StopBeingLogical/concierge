---
title: "Concierge Technical Spec Addendum: Verification Ladder & Registry Refinements"
document_type: spec_addendum
version: "1.0"
date: "2026-05-11"
status: current
tags: ['verification-ladder', 'registry-pull', 'standing-orders', 'cross-node-verification']
---

# Addendum: Verification Ladder & Registry Refinements

This addendum formalizes the high-level conceptual model refined in the May 11, 2026 session. It updates and overrides relevant sections of `concierge-technical-spec.md` v5.0.

---

## 1. The Verification Ladder (The Trust Ladder)

Concierge operates on a "Chain of Verification" where each layer validates the work of its subordinates before passing results upward.

### 1.1 Layer 4 (Foreman) — Sanity Pass
- **Job:** Verification of "Mechanical Completion."
- **Logic:** The Foreman ensures that the Workbee produced a result that matches the data type requested (e.g., "The model generated an image file," "The code compiled," "The text is not an empty string").
- **Verification Bound:** Limited to the local system. It does not evaluate "Intent Alignment."

### 1.2 Layer 3 (Router) — Cross-Node Integrity Pass
- **Job:** Verification of "Instruction Adherence."
- **Logic:** For high-stakes or complex chunks (e.g., Image Generation, Logic Proofs), the Router generates a secondary **Verification Chunk**.
- **Cross-Node Requirement:** The Verification Chunk **must** be assigned to a different Node/Family than the one that produced the original result.
- **Example:** Node A (NVIDIA) generates an image. Node B (Apple Silicon) runs a Vision model to verify the image contains the "10 required elements" specified in the contract.
- **Aggregation:** The Router does not release the result to the Planner until the Verification Chunk returns a "Match" signal.

### 1.3 Layer 2 (Planner) — Intent Validation Pass
- **Job:** Verification of "Project Coherence."
- **Logic:** Once the Router provides a complete set of verified chunks, the Planner evaluates the aggregate result against the **Fleshed-Out Intent**.
- **Recourse:** If the Planner detects a coherence failure, it may generate a new "Correction Job" to the Router or surface the failure to Bit.

### 1.4 Layer 1 (Human/Bit) — Final Approval
- **Job:** Final Arbiter of "Rightness."
- **Logic:** Bit presents the results (e.g., "Here are your 10 concept art mockups"). The human provides a Yes/No/Iterate signal.

---

## 2. Registry-Based Pull Model (Refined)

### 2.1 The Registry Interface
- **Job:** The Router maintains a **Stateful Registry** (implemented as an in-memory queue or local DB).
- **Advertisement:** The Router "advertises" chunks by writing them to the Registry with a **Minimum Capability Tag** (VRAM, Instruction Set, Model Family).
- **Leasing:** Foremen monitor the Registry and "Lease" chunks they are capable of handling.
- **Capability Filtering:** Foremen from weaker nodes are architecturally required to ignore chunks whose Metadata Tags exceed their local Node Envelopes. This allows for heterogeneous fleet scaling without "Lowest Common Denominator" limitations.

---

## 3. Standing Order: Clarification First

### 3.1 The "Sovereign Partner" Rule
- **Logic:** The system is a thinking partner, not a slave. To prevent "Wrong Answers" derived from ambiguity, the system operates under a **Standing Order for Clarification**.
- **Trigger:** If the Planner's "Confidence Weight" for an Intent Match is below a configurable threshold (Default: 0.85), or if a Task Package declares a `needs_info_trigger`, the Planner **must** pause and ask Bit for clarification.
- **Iterative Refinement:** Intent is not a one-shot command; it is a conversation in Bit until the contract is precise.

---

## 4. Learned Patterns & Memory Integration

### 4.1 Intent Mapping to Memory
- **Logic:** The system utilizes **Tier 2 (Structured Facts)** to learn where things belong (e.g., "The Idea List lives in /docs/seeds/idealist.md").
- **Resolution:** When an intent like "Add to the idea list" is received, the Planner first queries Tier 2 to resolve the location and filing pattern. If unresolved, it triggers the **Clarification Rule**.

---
*End of Addendum*
