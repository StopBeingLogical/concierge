# Model Search Audit Roadmap
## Which Models to Test, In What Order

**Add this section to MODEL_SEARCH_SESSION_SEED.md under "Next Steps"**

---

## Candidate Models & Test Order

### Phase 1: Baseline Establishment (This Week)

**Models to audit:**
1. **Gemma 4 26B** (via Ollama, local)
   - Status: Tested for planning (weak without scaffolding)
   - Purpose: Baseline for 26B class
   - Tests: Conversational (eval_bit_model.py) + Coding decomposition
   - Timeline: 1 hour (conversational) + 30 min (coding) per model

2. **Llama 2 70B** (via Ollama, if available locally)
   - Status: Not yet tested
   - Purpose: Baseline for 70B class
   - Tests: Same as Gemma 4
   - Timeline: Same

**Why these two first:**
- You already have them available locally (no licensing/API key friction)
- Cover two different size classes (26B vs. 70B)
- Establish baseline before testing frontier models

### Phase 2: Expand Candidate Set (Week 2)

**Models to consider:**
- Llama 3 70B (if different from Llama 2)
- Mistral 7B (smaller, might be faster)
- Qwen 2.5 14B (if available)
- Any others running on your Ollama instance

**Selection criteria:**
- Available locally
- Different architectures (not just size variants)
- Represent different training families

### Phase 3: Frontier Model Audit (Week 3+, if desired)

**Models to test (via API):**
- Claude Sonnet 4 (frontier baseline)
- Gemini 2.0 (frontier baseline)
- GPT-4o (if you have access)

**Why later:**
- More expensive to test via API
- You need baselines first to know what questions to ask
- Frontier models might be overkill for "can it decompose?" questions
- Focus on identifying where local models work first

---

## Test Execution Order

### For Each Model:

```
Step 1: Conversational Audit (eval_bit_model.py)
  Time: 1 hour (includes your human scoring of Test 1)
  Output: conversational/results/{model}_eval_results.json
  
Step 2: Coding Decomposition Audit
  Skeleton: stock_trading_simulator.json (from GEMMA_PLANNING_INPUT.md Stage 1)
  
  2a. Run eval_coding_decompose.py on the skeleton
      Time: 30 min
      Output: coding/results/{model}_decomposition.json
      
  2b. Run eval_coding_selfassess.py on the decomposition
      Time: 30 min
      Output: coding/results/{model}_selfassess.json
      
  2c. Analyze results
      Time: 30 min
      Output: coding/results/{model}_audit_report.json
      
Step 3: Update model registry
  Add entry to model_registry.yaml with scores from Steps 1-2
  
Total time per model: ~3.5 hours (1 hour conversational + 2.5 hours coding)
```

---

## Execution Schedule

### Week 1 (Starting Now)

| Day | Task | Models | Time |
|---|---|---|---|
| Mon | Implement eval_coding_decompose.py | N/A | 2 hours |
| Mon | Implement eval_coding_selfassess.py | N/A | 2 hours |
| Tue | Run conversational audit | Gemma 4 26B | 1 hour |
| Tue | Run coding audits | Gemma 4 26B | 2.5 hours |
| Wed | Run conversational audit | Llama 2 70B | 1 hour |
| Wed | Run coding audits | Llama 2 70B | 2.5 hours |
| Thu | Analyze & compare results | Both | 2 hours |
| Fri | Populate model registry, write comparison report | Both | 2 hours |

**Total this week:** ~16 hours (mostly script implementation + running tests)

### Week 2

| Task | Scope |
|---|---|
| Audit additional candidate models | 1-2 more models, ~4 hours each |
| Refine test cases | Better skeletons, more domain-specific tests |
| Document findings | What each model is good/bad at |

### Week 3+

| Task | Scope |
|---|---|
| Frontier model audit (optional) | If you want to compare local vs. frontier for decomposition |
| Image generation audit (if needed) | Design + implement + test |
| Integration with Concierge | Feed results into model registry |

---

## What You're Measuring

For each model, across both test suites, track:

### Conversational Audit (from eval_bit_model.py)
- **Final weighted score** (1-5)
- Per-test breakdown (reasoning, tools, instruction following, context, intent parsing)
- Human-scored reasoning quality (Test 1)

### Coding Decomposition Audit
- **Task granularity distribution** — histogram of task sizes
- **Assumption list** — what did the model assume without asking?
- **Dependency accuracy** — how many deps did it get right/wrong?
- **Self-assessment calibration** — how aware is it of its own limits?

---

## Expected Findings

### Gemma 4 26B (Prediction)

**Conversational:**
- Score: ~3.5-4.0/5
- Good at: tool calling, intent parsing, simple reasoning
- Weak at: instruction following with multiple constraints, deep context

**Coding Decomposition:**
- Task granularity: ~60% in target range (1-4 hours), ~20% too small, ~20% too large
- Assumptions: ~3-5 unstated assumptions per skeleton
- Dependency accuracy: ~70-80% (misses 20-30% of dependencies)
- Self-assessment: Somewhat aware of input/output limits, misses logical errors

### Llama 2 70B (Prediction)

**Conversational:**
- Score: ~3.8-4.2/5 (slightly better than Gemma due to size)
- Reasoning quality: Slightly more nuanced

**Coding Decomposition:**
- Task granularity: ~65% in target range (better than Gemma)
- Assumptions: Similar (not much difference from Gemma)
- Dependency accuracy: ~75-85%
- Self-assessment: Similar to Gemma

### Key Unknown

**The real question:** How much of the difference is due to model capability vs. prompt scaffolding? If you give both models the same skeleton + context, do they produce similar decompositions? Or does one genuinely handle ambiguity better?

This is worth testing.

---

## Success Metrics for Phase 1

You'll know this is working when:

1. ✅ You have repeatable audit results for Gemma 4 and Llama 2 70B
2. ✅ Results are comparable (both models tested on same skeleton)
3. ✅ You can articulate why one ranked higher (specific test differences)
4. ✅ You have concrete data (not hunches) on task granularity, assumptions, dependencies
5. ✅ Spot-check validation: ask a model to execute 3 tasks it said it could do, see if code works
6. ✅ Model registry has at least 2 entries with audit scores

---

## Data to Keep

Save all of this in the model_search project:

```
model_search/results/
├── model_registry.yaml                     [Master record]
├── conversational/
│   ├── gemma4_26b_eval_results.json
│   ├── llama2_70b_eval_results.json
│   └── comparison_conversational.md
├── coding/
│   ├── gemma4_26b_decomposition.json
│   ├── gemma4_26b_selfassess.json
│   ├── gemma4_26b_audit_report.json
│   ├── llama2_70b_decomposition.json
│   ├── llama2_70b_selfassess.json
│   ├── llama2_70b_audit_report.json
│   └── comparison_coding.md
└── spot_checks/
    ├── gemma4_task_execution_1.md
    ├── gemma4_task_execution_2.md
    └── [etc]
```

This becomes your reference database for "which model is best for what."

---

## Questions to Answer by End of Week 1

1. **Granularity:** How fine can local models decompose? (sub-1-hour tasks, or 4+ hour tasks?)
2. **Assumption surfacing:** Do they ask clarifying questions, or just assume?
3. **Dependency accuracy:** Are missing dependencies a real problem, or mostly cosmetic?
4. **Code quality:** Does confidence in their self-assessment correlate with actual code working?
5. **Model gap:** Is there a meaningful difference between 26B and 70B for this work?

Audit data will answer these empirically.

---

*Add this to MODEL_SEARCH_SESSION_SEED.md before transferring to the Model Search project.*
