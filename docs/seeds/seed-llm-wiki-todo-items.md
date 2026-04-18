---
title: "Seed — LLM Wiki Pattern Concierge Todo Items"
document_type: seed
date: "2026-04"
status: current
tags: ['llm-wiki', 'karpathy', 'memory-spec', 'lint', 'todo']
---

# Seed: LLM Wiki Pattern — Concierge Todo Items

*Drop this into the Concierge working chat to queue the following spec additions.*

---

## Context

Reviewed Karpathy's LLM Wiki pattern (viral, ~1 week old). Confirmed it is not a competing architecture — it is a named instance of the continuous index/analysis/cache-prefill prep task already designed into Concierge. However, it surfaces three concrete operational details that the Memory Spec currently lacks. These should be added as spec work items.

---

## Todo Items

### 1. Memory Spec — Add the Lint Pass as a Named Scheduled Job

The lint pass is a periodic, low-priority Planner job (not continuous, not user-initiated) that health-checks Tier 3 semantic memory for:
- Contradictions between entries
- Stale claims superseded by newer sources
- Orphan entries with no inbound references
- Concepts referenced but lacking their own entry
- Missing cross-references
- Data gaps fillable by external search

This is the operational answer to "how does Tier 3 stay healthy over time." Needs to be a named job type in the spec with a typed output contract enumerating detected issues.

### 2. Memory Spec — Add Supersession Model to Tier 3 Entry Schema

When a new source contradicts an existing Tier 3 entry, the old entry should be archived rather than deleted. Required additions to Tier 3 entry schema:
- `status` field: `current` / `superseded` / `deprecated`
- `superseded_by` reference (link to the entry that replaced it)
- Timestamp of supersession event

Archive-not-delete is the correct behavior. This preserves provenance and allows rollback if the superseding entry is later found to be incorrect.

### 3. Technical Spec — Add Backfiling Decision to Foreman Job-Close Sequence

After a job closes, the Foreman (or Planner on review) should run a quality-scored gate: *does this job's output contain durable knowledge worth promoting to Tier 3?*

This is the mechanism by which completed jobs compound into semantic memory rather than aging out of working context into logs. Needs a threshold/scoring model and a defined promotion path from job output → Tier 3 entry.
