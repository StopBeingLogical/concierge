# Objective
Produce a finalized MVP-level Product Requirements Document (PRD) for the Concierge system, ensuring all architectural, behavioral, and interface components are fully specified before implementation begins. The PRD will act as the master index mapping user journeys to layer contracts.

# Key Files & Context
- `docs/specs/concierge-technical-spec.md` (and Addendum 01)
- `docs/specs/concierge-memory-spec.md`
- `docs/specs/concierge-hardware-appendix.md`
- `docs/seeds/seed-bit-application-spec-foundations.md`

# Implementation Steps (Atomized Decision Points)

## Phase 1: Bit Application Specification (MVP Level)
1. **Decision Point:** Define the exact schema for the "Cognitive Profile" loaded at session start.
    *   **Return Expectation:** A versioned JSON schema.
    *   **Data Points:** `output_density` (tokens/sent), `compression_preference` (summary/detail), `presentation_format` (markdown/text/table), `ambiguity_threshold` (confidence score), `preferred_model_family`.
2. **Decision Point:** Define the MVP slash command vocabulary vs. freeform inference boundaries.
    *   **Return Expectation:** A command manifest table.
    *   **Data Points:** `command_trigger` (e.g., /idea), `description`, `target_task_package_id`, `required_args`, `inference_fallback_behavior`.
3. **Decision Point:** Specify the UI/UX flow for the "Clarification First" rule.
    *   **Return Expectation:** An interaction state machine/sequence diagram.
    *   **Data Points:** `blocking_flag`, `human_prompt_text`, `input_validation_schema`, `default_assumption_handling`.
4. **Decision Point:** Define the Bit MVP Dashboard.
    *   **Return Expectation:** A list of view definitions and state-monitoring requirements.
    *   **Data Points:** `harkanza_queue_count`, `active_job_status_list`, `capability_gap_alerts`, `last_sync_timestamp`.
5. **Action:** Draft `docs/specs/concierge-bit-spec.md`.

## Phase 2: Router Internal Design (MVP Level)
6. **Decision Point:** Choose the minimal viable state store for the Registry.
    *   **Return Expectation:** Technology selection and table/document schemas.
    *   **Data Points:** `job_queue_table`, `lease_tracking_table`, `node_capability_cache`, `persistence_interval`.
7. **Decision Point:** Define the exact leasing algorithm.
    *   **Return Expectation:** Logic pseudocode and scoring rubric.
    *   **Data Points:** `priority_weight`, `capability_score_logic`, `lease_ttl_calculation`, `fairness_policy`.
8. **Decision Point:** Specify the timeout/retry logic for expired Work Chunk leases.
    *   **Return Expectation:** Error handling policy and state transition table.
    *   **Data Points:** `max_retries_per_chunk`, `backoff_intervals`, `poison_pill_threshold`, `alert_trigger_conditions`.
9. **Decision Point:** Detail the "Cross-Node Integrity Pass" logic.
    *   **Return Expectation:** A verification strategy document.
    *   **Data Points:** `family_exclusion_rules`, `verifier_compute_class_requirements`, `quorum_threshold`, `mismatch_resolution_flow`.
10. **Action:** Draft `docs/specs/concierge-router-spec.md`.

## Phase 3: MVP Task Package Definitions
11. **Decision Point:** Identify the minimum set of "Day Zero" Task Packages.
    *   **Return Expectation:** A prioritized registry list.
    *   **Data Points:** `package_id`, `core_intent_mapping`, `priority_lane_assignment`, `nidaba_enrichment_flag`.
12. **Decision Point:** Draft the JSON schemas for these MVP Task Packages.
    *   **Return Expectation:** A collection of valid Task Package JSON files.
    *   **Data Points:** `input_contract_schema`, `output_contract_schema`, `pipeline_steps`, `acceptance_criteria`.
13. **Action:** Create `docs/specs/mvp-task-packages.md`.

## Phase 4: Master PRD Compilation
14. **Decision Point:** Map the "Nugget-to-Reality" user journey.
    *   **Return Expectation:** A traceability matrix mapping the journey through all 5 layers.
    *   **Data Points:** `layer_boundary_handoffs`, `sha256_verification_checkpoints`, `memory_tier_interaction_points`, `human_approval_gates`.
15. **Action:** Draft `concierge-master-prd.md` to serve as the definitive implementation index.

# Verification & Testing
- Review all generated specs against the "Constraints are Contracts" and "Sovereign Partner" philosophies.
- Verify no single point of failure or silent dropping of context exists in the mapped user journey.
