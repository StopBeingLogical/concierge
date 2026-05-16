---
title: "Seed — Project Map & LLM Navigator"
document_type: seed
version: "1.0"
date: "2026-05-11"
status: current
tags: ['index', 'navigation', 'local-llm', 'context-mapping', 'prd-plan']
---

# Concierge: Project Map & LLM Navigator

**Purpose:** This document serves as a "Map of the World" for local LLMs assisting with the Concierge project. It indexes the project structure, categorizes file contents, and maps existing documentation to the specific tasks in the `concierge-prd-plan.md`.

---

## 1. Project Directory Index

### 📂 /docs/specs (The "Rules")
*   `concierge-technical-spec.md`: The authoritative 5-layer architecture contract.
*   `concierge-technical-spec-addendum-01.md`: Overrides/refinements for the Verification Ladder and Pull Model.
*   `concierge-memory-spec.md`: Detailed 4-tier memory architecture and persistence rules.
*   `concierge-philosophy.md`: Core project values (Sovereignty, Constraints as Contracts, Scaffolding).
*   `concierge-hardware-appendix.md`: Guidelines for heterogeneous hardware support.

### 📂 /docs/reference (The "Why")
*   `concierge-core-purpose-and-positioning.md`: High-level purpose, market position, and neurodivergent use-case focus.
*   `concierge-architecture-faq.md`: Clarifications on model roles, offline queueing, and memory sync.
*   `concierge-project-index.md`: A cross-reference of symbols and components.

### 📂 /docs/seeds (The "Foundations")
*   `seed-bit-application-spec-foundations.md`: Initial design brief for Layer 1 (Bit).
*   `concierge-strategic-reframe.md`: The "Enterprise-D" vision and strategic pivot summary.

### 📂 /docs/plans (The "Roadmap")
*   `concierge-prd-plan.md`: The atomized checklist for reaching a finalized PRD.

---

## 2. PRD Plan Data Mapping

This section maps existing data points to the **Decision Points** in `docs/plans/concierge-prd-plan.md`.

### Phase 1: Bit Application Specification
| Plan Task | Relevant Source Files | Key Data to Extract |
| :--- | :--- | :--- |
| **1. Cognitive Profile Schema** | `seed-bit-application-spec-foundations.md` | "Output Layer" section; CCSS profile concepts. |
| **2. Slash Command Vocabulary** | `seed-bit-application-spec-foundations.md` | "Explicit Mode" section; existing /foodlog example. |
| **3. Clarification UI Flow** | `concierge-technical-spec.md` (Section 1) | "Disambiguation UI Behavior"; "NEEDS_INFO" signal (Section 2). |
| **4. Bit MVP Dashboard** | `concierge-technical-spec.md` (Section 1) | "Bit Application Surface" section; Harkanza queue description. |

### Phase 2: Router Internal Design
| Plan Task | Relevant Source Files | Key Data to Extract |
| :--- | :--- | :--- |
| **6. Registry State Store** | `concierge-technical-spec-addendum-01.md` | Section 2.1 (The Registry Interface). |
| **7. Leasing Algorithm** | `concierge-technical-spec.md` (Section 7) | "Work Pool Model"; "Pull model invariants." |
| **8. Timeout/Retry Logic** | `concierge-technical-spec.md` (Section 2) | "Step States" table; `on_failure` behaviors. |
| **9. Cross-Node Integrity** | `concierge-technical-spec-addendum-01.md` | Section 1.2 (Router Integrity Pass). |

### Phase 3: MVP Task Packages
| Plan Task | Relevant Source Files | Key Data to Extract |
| :--- | :--- | :--- |
| **11. Day Zero Packages** | `concierge-technical-spec.md` (Section 2) | Foundation Generation (Hašatar); Gap Resolution logic. |
| **12. Task Package Schemas** | `concierge-technical-spec.md` (Section 5) | Full "Task Package Schema" template. |

---

## 3. Navigation Heuristics for LLMs

1.  **Architecture Questions?** Start with `concierge-technical-spec.md` and check `addendum-01` for overrides.
2.  **Memory/Data Questions?** Go directly to `concierge-memory-spec.md`.
3.  **"How should it feel?" Questions?** Consult `concierge-philosophy.md` and the "Prosthetic" section of the Core Purpose doc.
4.  **Hardware/Node Questions?** See `concierge-hardware-appendix.md`.
5.  **Confused about a term?** Look for the "Hittite convention" names at the bottom of the Technical Spec or FAQ.

---
*Generated May 11, 2026 to support local-model PRD drafting.*
