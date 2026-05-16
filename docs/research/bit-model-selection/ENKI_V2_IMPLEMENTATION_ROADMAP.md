# ENKI v2.0 Implementation Roadmap
## Gemini's Spec → Executable Tasks

**Source:** Gemini's "ENKI v2.0: Implementation Specification & Claude Code Directives"  
**Status:** Ready for Claude Code execution  
**Priority:** Phase 1 (this week), Phase 2 (next week), Phase 3 (infrastructure)

---

## What Gemini Did Right

Gemini took the abstract vulnerabilities Gemma identified and **translated them into concrete code tasks**. This is the missing link between "the framework is vulnerable" and "here's how to fix it."

**Gemini's structure:**
1. **Phase 1:** Diagnostic logging (why models fail, not just that they fail)
2. **Phase 2:** Pipeline resilience (handle errors without crashing, discover required scaffolding)
3. **Phase 3:** Infrastructure controls (execution parameters, timeouts, token budgets)

This maps directly to the v2 improvements:
- Gemma's "diagnostic metadata" → Gemini's Phase 1 (diagnostic logger)
- Gemma's "try-except-repair" → Gemini's Phase 2.1 (JSON auto-repair)
- Gemma's "format vs. content split" → Gemini's Phase 2.2 (multi-tiered scaffolding)
- Gemma's "delimited anchoring" → Gemini's Phase 3 (execution parameters)

---

## Phase 1: The "Goodhart's Law" Defense — PRIORITY: HIGH

### Task 1.1: Create `enki/utils/diagnostics.py`

**What to track:**
```python
# Track failure modes, not just scores
diagnostics = {
    "preamble_injection_rate": 0.4,  # "Here is your JSON..." prefix
    "markdown_fence_rate": 0.3,       # ```json ``` wrapping
    "truncation_rate": 0.1,           # Hit token limit
    "parsing_error_type": "JSONDecodeError",
    "json_repair_method": "regex_extract",
    "formatting_penalty": True,
    "latency_ms": 1450
}
```

**Why:** Without this, you see "Gemma scored 3.2" but don't know if it's because:
- The decomposition was bad, OR
- The model adds preamble 40% of the time (format issue, not reasoning)

**Implementation approach:**
- Log every model response before parsing
- Track what breaks parsing (preamble, markdown, truncation, etc.)
- Append to output: `{"score": 3.2, "diagnostics": {...}}`

**Integration point:**
- `analyze_coding_audit.py` should ingest diagnostics and produce a report like:
  ```
  Model: Gemma 4 26B
  Reasoning Score: 85/100
  Format Compliance: 50/100 (preamble 40% of time)
  Recommendation: Good decomposer; fix prompts with delimited anchoring
  ```

---

### Task 1.2: Create `enki_stage2b_semantic_evaluator.py`

**What it does:**
Evaluates the *content* of a decomposition independently from format/style.

**Key prompt requirement (Gemini's insight):**
> "Do not penalize stylistic choices. Grade ONLY on the functional viability, completeness, and logical sequencing of the decomposed tasks."

**Output schema:**
```json
{
  "functional_viability_score": 4,
  "completeness_score": 4,
  "logical_sequencing_score": 3,
  "dependency_awareness_score": 3,
  "explanation": "Tasks are reasonable but dependencies are incomplete (missed 2 critical blockers)"
}
```

**Why:** This separates "does the decomposition make sense?" from "is it formatted nicely?"

**Integration:**
- Can be optional (human review) or automated (send decomposition to Claude/Gemini for structured evaluation)
- Stage 2 output includes both: task count + semantic scores

---

## Phase 2: Pipeline Resilience — PRIORITY: HIGH

### Task 2.1: Create `enki/utils/json_repair.py`

**What it does:**
Aggressively recover JSON from malformed output.

**Implementation (ordered attempts):**

```python
def repair_json(response: str) -> tuple[dict, dict]:
    """
    Attempt 1: Standard json.loads()
    Attempt 2: Strip markdown fences and retry
    Attempt 3: Extract content between { and } and retry
    Attempt 4: Capture raw response and flag error
    """
    
    # Attempt 1: Standard
    try:
        return json.loads(response), {"method": "standard", "success": True}
    except JSONDecodeError:
        pass
    
    # Attempt 2: Strip markdown fences
    cleaned = response.replace("```json", "").replace("```", "")
    try:
        return json.loads(cleaned), {"method": "fence_strip", "success": True}
    except JSONDecodeError:
        pass
    
    # Attempt 3: Extract {...}
    import re
    match = re.search(r'\{.*\}', response, re.DOTALL)
    if match:
        try:
            return json.loads(match.group()), {"method": "regex_extract", "success": True}
        except JSONDecodeError:
            pass
    
    # Attempt 4: Capture
    return {
        "raw_response": response,
        "parsing_error": True
    }, {"method": "capture", "success": False}
```

**Output:**
- If repair succeeds: flag `formatting_penalty: true` but continue pipeline
- If repair fails: capture raw response, continue with limited data

**Why:** Stop losing data. Now you can analyze preamble patterns, markdown frequency, etc.

---

### Task 2.2: Implement Multi-Tiered Scaffolding in `enki_stage2_decompose.py`

**What it does:**
If a model fails with zero-shot, retry with increasing scaffolding.

**Three tiers:**

```python
def decompose_with_scaffolding(skeleton, model, max_tiers=3):
    """
    Attempt 1 (Zero-Shot): Standard prompt
    Attempt 2 (Schema + Few-Shot): Add JSON schema + example
    Attempt 3 (Chain-of-Thought): Add "Think step-by-step"
    """
    
    tier_used = 0
    
    # Tier 1: Zero-shot
    response = call_model(model, prompt=PROMPT_STANDARD, skeleton=skeleton)
    if is_valid_structure(response):
        tier_used = 1
        return parse_response(response), {"tier_used": 1}
    
    if max_tiers >= 2:
        # Tier 2: Schema + Few-shot
        response = call_model(
            model,
            prompt=PROMPT_SCHEMA_FEWSHOT,
            skeleton=skeleton,
            example=EXAMPLE_DECOMPOSITION
        )
        if is_valid_structure(response):
            tier_used = 2
            return parse_response(response), {"tier_used": 2}
    
    if max_tiers >= 3:
        # Tier 3: Chain-of-thought
        response = call_model(
            model,
            prompt=PROMPT_COT,
            skeleton=skeleton
        )
        tier_used = 3
        return parse_response(response), {"tier_used": 3}
    
    return None, {"tier_used": 3, "failed": True}
```

**Output includes:**
```json
{
  "decomposition": {...},
  "scaffolding": {
    "tier_used": 2,
    "reason": "Zero-shot produced malformed JSON; Schema+FewShot succeeded"
  }
}
```

**Why:** This tells Concierge's Router: "Gemma needs schema + few-shot scaffolding in production prompts"

---

## Phase 3: Infrastructure Controls — PRIORITY: MEDIUM

### Task 3.1: Update Execution Parameters

**File:** `enki_stage2_decompose.py` and `enki_stage3_selfassess.py`

**Changes:**

```python
# Temperature: Lower for Stage 2 (more consistent), normal for Stage 3
TEMPERATURE_STAGE2 = 0.1  # ← More deterministic
TEMPERATURE_STAGE3 = 0.5  # ← More exploratory

# Add CLI arguments
parser.add_argument("--timeout", type=int, default=600, help="Request timeout in seconds")
parser.add_argument("--max-tokens", type=int, default=8192, help="Max tokens to generate")

# Ollama API payload
ollama_payload = {
    "model": model_name,
    "messages": messages,
    "options": {
        "temperature": temperature,
        "num_predict": 8192  # ← Explicit token budget
    }
}
```

**Why:**
- Lower temperature in Stage 2 ensures consistent decomposition (not wildly different outputs each run)
- Explicit token budget prevents context window exhaustion on large skeletons
- Timeout prevents hung requests

---

## Complete File Structure for v2.0

```
enki/
├── README.md (updated with v2 features)
├── utils/
│   ├── diagnostics.py (NEW — Task 1.1)
│   ├── json_repair.py (NEW — Task 2.1)
│   └── __init__.py
├── enki_stage2_decompose.py (UPDATE — Task 2.2, 3.1)
├── enki_stage2b_semantic_evaluator.py (NEW — Task 1.2)
├── enki_stage3_selfassess.py (UPDATE — Task 3.1)
├── analyze_coding_audit.py (UPDATE — Task 1.1 integration)
└── prompts/
    ├── stage2_zero_shot.md
    ├── stage2_schema_fewshot.md (NEW — Task 2.2)
    └── stage2_cot.md (NEW — Task 2.2)
```

---

## Implementation Timeline

### Week 1 (This Week)

| Day | Task | File(s) | Time | Dependency |
|---|---|---|---|---|
| Mon | Create `diagnostics.py` | enki/utils/diagnostics.py | 1h | None |
| Mon | Create `json_repair.py` | enki/utils/json_repair.py | 1.5h | None |
| Tue | Update Stage 2 with repair utility | enki_stage2_decompose.py | 1h | json_repair.py |
| Tue | Implement multi-tiered scaffolding | enki_stage2_decompose.py | 2h | Stage 2 update |
| Wed | Create semantic evaluator | enki_stage2b_semantic_evaluator.py | 1.5h | None |
| Wed | Update `analyze_coding_audit.py` | analyze_coding_audit.py | 1h | diagnostics.py |
| Thu | Update execution parameters | Both stage files | 0.5h | All above |
| Fri | Test all changes, document | README, tests | 2h | All above |

**Total:** ~11 hours (split across team or extended across week)

### Week 2 (Phase 1 of Audit Roadmap)

Run full audits with v2.0 framework:
- Gemma 4 26B (conversational + coding)
- Llama 2 70B (conversational + coding)
- Collect diagnostic data
- Generate comparison report

### Week 3+

Use diagnostic data to inform:
- Which models need more scaffolding?
- Which fail consistently on format vs. reasoning?
- What do the Concierge Router's prompts need to look like?

---

## How This Feeds Into Concierge

**Before (v1):**
```yaml
model: gemma4:26b
score: 3.2
recommendation: "Maybe use this model?"
```

**After (v2):**
```yaml
model: gemma4:26b
score: 3.2
diagnostics:
  reasoning_quality: 85/100
  format_compliance: 50/100
  preamble_injection_rate: 0.4
  required_scaffolding: 2  # Needs schema + few-shot
  semantic_score: 4.1/5.0
recommendation: |
  Good decomposer (85/100 reasoning). 
  Weakness: adds preamble 40% of the time.
  Fix: Use delimited anchoring in production prompts.
  Requires: Schema + few-shot scaffolding (Tier 2)
  Deploy as: Foreman task decomposer (not Bit layer)
```

This data lets the Router make **informed decisions** about which model to use for which task.

---

## What's Missing from Gemini's Spec

Gemini provided a solid foundation but didn't specify:

1. **Prompt templates for scaffolding** (Schema + FewShot, CoT versions)
2. **Semantic evaluator prompt** (exact grading rubric)
3. **Test cases** (which skeleton variations to test?)
4. **Spot-check validation** (how to verify a model's self-assessment?)

**Recommendation:** These should be filled in during implementation (Week 1). They're straightforward but need context-specific tuning.

---

## Summary: What You Have Now

**From Gemma:** Vulnerabilities identified, fixes suggested  
**From Gemini:** Vulnerabilities → Code tasks → Implementation spec  
**From Claude (me):** Implementation spec → Roadmap with timing  

**You now have:**
- ✅ Three-stage audit funnel (frontier sketch → local decompose → self-assess)
- ✅ Conversational test suite (eval_bit_model.py, working)
- ✅ v2.0 framework improvements (Gemini's spec, ready to implement)
- ✅ Phase 1 audit roadmap (Gemma 4 + Llama 2, this week)
- ✅ Model Search project structure (ready to transfer)

**Next step:** Execute Gemini's implementation spec (Week 1 tasks above) before running Phase 1 audits.

This is a **complete evaluation framework** ready for production use.
