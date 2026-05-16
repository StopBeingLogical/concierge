# Model Search Project — Session Seed
**Created:** April 13, 2026  
**Purpose:** Ground truth for model evaluation work

## What We're Doing

Testing where local language models (Gemma 4 26B, Llama 2 70B, etc.) can be used 
effectively vs. where they hit capability ceilings. Results feed Concierge's model 
registry.

## Current Understanding

### What We Know Works (Tested)

- **Frontier model reasoning:** Claude and Gemini can collaboratively sketch complex 
  software architecture. They can produce alternatives and debate trade-offs.
- **Gemma's planning weaknesses:** Without explicit decision criteria, Gemma defaults 
  to middle-ground choices and doesn't reason about trade-offs.
- **Gemma's required scaffolding:** Needs decision context (timeline, priority, 
  success metrics) to plan effectively. With it, performance improves.

### What We're About to Test

- **Coding decomposition:** Can Gemma break a project skeleton into atomic tasks? 
  At what granularity does it break down?
- **Self-awareness:** Can Gemma predict its own failure modes? Does it ask questions 
  when specs are ambiguous?
- **Model comparison:** How do Gemma, Llama, and others differ in decomposition accuracy 
  and self-assessment calibration?

### Test Framework Status

## ENKI v2.0 Implementation Status

**Vulnerabilities Identified:**
- Gemma 4 26B audited the test suite and identified 6 vulnerabilities
- Severity range: Medium to Critical (but mostly fixable)
- Gemini provided implementation spec to address all of them

**v2.0 Changes Required (before Phase 1):**
1. Diagnostic logging (track *why* models fail, not just that they fail)
2. JSON auto-repair (try-except-capture pattern)
3. Multi-tiered scaffolding (zero-shot → schema+fewshot → CoT)
4. Infrastructure controls (timeouts, token budgets, temperature tuning)

**Timeline:** Implement v2.0 improvements Week 1, then run Phase 1 audits with v2.0 framework

**Files to implement:**
- `enki/utils/diagnostics.py` (NEW)
- `enki/utils/json_repair.py` (NEW)
- `enki_stage2b_semantic_evaluator.py` (NEW)
- Updates to existing stage scripts

See ENKI_V2_IMPLEMENTATION_ROADMAP.md for task breakdown (~11 hours work).

**Conversational (COMPLETE):**
- Test suite: eval_bit_model.py (5 tests, weighted scoring)
- Tests: reasoning, tool calling, instruction following, context depth, intent parsing
- Status: Ready to run on any local model

**Coding Decomposition (PLANNED):**
- Framework: three-stage funnel (frontier sketch → local decompose → self-assess)
- Stage 1 (frontier sketch): Manual, use templates in GEMMA_PLANNING_INPUT.md
- Stage 2 (local decompose): eval_coding_decompose.py (needs implementation)
- Stage 3 (self-assess): eval_coding_selfassess.py (needs implementation)
- Status: Documented, needs implementation

**Image Generation (PLANNED):**
- Status: Not yet designed. Deferred.

## Files in This Project

### Documentation
- `GEMMA_RECOMMENDATION_ASSESSMENT.md` — Analysis of Gemma's initial recommendations
- `GEMMA_PLANNING_ANALYSIS.md` — What we learned about Gemma's planning capability
- `MODEL_AUDIT_FRAMEWORK.md` — Blueprint for all three categories
- `GEMMA_PLANNING_INPUT.md` — Reusable template for frontier-model planning input

### Code
- `eval_bit_model.py` — Conversational eval suite (working)
- `eval_coding_decompose.py` — [Needs implementation]
- `eval_coding_selfassess.py` — [Needs implementation]
- `analyze_coding_audit.py` — [Needs implementation]

### Results
- `conversational/results/` — Test results from eval_bit_model.py
- `coding/results/` — Test results from decomposition audits
- `project_skeletons/` — Test cases (stock trading simulator, etc.)

## Concierge Integration

Model audit results populate the Concierge model registry:
```yaml
model: gemma4:26b
category: conversational
audit_score: [score from eval_bit_model.py]
strengths: [...]
weaknesses: [...]
best_for: [conversational interaction, structured output]
avoid_for: [multi-constraint problems, deep reasoning]
```

Router uses this to route work to appropriate models.

## Next Steps

1. **Implement eval_coding_decompose.py** — Start with stock trading simulator skeleton
2. **Run conversational evals on all candidate models** — Gemma 4, Llama 2 70B, others
3. **Run coding decomposition audits** — Same models, same skeleton
4. **Compare results** — Rank models by category
5. **Populate Concierge model registry** — Feed audit data back to main project
6. **Iterate** — As new models become available, audit them

## References to Concierge Core

For system context, see:
- Concierge Philosophy: `/mnt/project/Concierge_Philosophy_v5.md`
- Technical Spec: `/mnt/project/Concierge_Technical_Spec_v5.md`
- Hardware context: `/mnt/project/Concierge_Hardware_Appendix_v5.md`
- Session seed: `/mnt/project/CONCIERGE_SESSION_SEED.md`

These are shared references; changes there should be noted here.

## Key Insight

The model audit work is NOT separate from Concierge — it's foundational. Concierge's 
architecture assumes local models can execute atomic tasks if plans are explicit. 
These audits test that assumption empirically.

---

*Seed created April 13, 2026. Transfer from Concierge project to Model Search project.*