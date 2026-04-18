---
title: "Model Audit Framework — Multi-Category Evaluation Protocol"
document_type: reference
date: "2026-04-13"
status: current
tags: ['model-audit', 'eval', 'enki', 'bit', 'framework']
---

# Model Audit Framework: Multi-Category Evaluation Protocol
**Purpose:** Establish empirical model ceiling discovery across task categories relevant to Concierge  
**Status:** Extensible blueprint based on existing conversational eval script  
**Date:** April 13, 2026

---

## Architecture

```
Model Audit Framework
├── Category: Conversational Tasks
│   ├── Test Suite: eval_bit_model.py (existing, 5 tests)
│   ├── Models: Gemma 4 26B, Llama 2 70B, others
│   └── Output: Weighted score (1-5), per-test breakdown
│
├── Category: Coding Project Decomposition
│   ├── Test Suite: three-stage funnel (frontier → local → self-assess)
│   ├── Models: Gemma 4 26B, Llama 2 70B, others
│   └── Output: Task granularity histogram, assumption list, dependency graph
│
├── Category: Image Generation
│   ├── Test Suite: [To be designed]
│   ├── Models: [TBD]
│   └── Output: [TBD]
│
└── [Additional categories as needed]
```

---

## Category 1: Conversational Tasks (EXISTING)

### Test Suite
**File:** `eval_bit_model.py`  
**Status:** Implemented and operational

**Tests:**
1. **Test 1 (30%)** — Conversational Reasoning (human-scored)
   - 1A: Steam game recommendations (probing, not direct recommendations)
   - 1B: Fiction — timeline analysis (identifies periods of dramatic richness)
   - 1C: Hardware spec questions (cites philosophy, asks about training diversity)

2. **Test 2 (25%)** — Tool Calling
   - Parallel tool calls (multiple nodes simultaneously)
   - Correct function selection
   - Abstention when tools don't apply

3. **Test 3 (20%)** — Instruction Following (4 constraints)
   - Forbidden word list
   - Exact bullet count
   - Capital letters
   - Format compliance

4. **Test 4 (15%)** — Needle Retrieval (~15K context)
   - Embedded value in padded text
   - Deep context search

5. **Test 5 (10%)** — Intent Parsing to JSON
   - Structured output
   - Schema compliance
   - No markdown fences

### Scoring Model
- **Weighted average:** Test 1 (30%) + Test 2 (25%) + Test 3 (20%) + Test 4 (15%) + Test 5 (10%)
- **Scale:** 1-5, where 1 = fails all, 5 = aces all
- **Output:** JSON with per-test breakdown and final score

### Running This Category
```bash
python eval_bit_model.py --model gemma4:26b --host http://localhost:11434 --output results_gemma4.json
```

### Key Insight
This test suite reveals:
- **Where the model can reason** (Test 1 — probing vs. direct answers)
- **Where it gets mechanical tasks wrong** (Test 3 — constraint counting)
- **Where it hits context limits** (Test 4 — 15K needle)
- **Where it can structure output** (Test 5 — JSON)

---

## Category 2: Coding Project Decomposition (NEW)

### Test Structure

**Three-stage funnel:**

```
Stage 1: Frontier Models (Claude, Gemini)
  Input: User intent ("Build a stock trading simulator with $1 starting capital")
  Process: Interview → Skeleton generation → Synthesis
  Output: Unified project skeleton (architecture, modules, tech stack)
  
  ↓
  
Stage 2: Local Model (Gemma 4 26B, Llama 2, etc.)
  Input: Project skeleton from Stage 1
  Process: Decomposition → Atomization → Milestone generation
  Output: Task list with dependencies, granularity, assumptions
  
  ↓
  
Stage 3: Local Model (self-assessment)
  Input: Task list from Stage 2
  Process: Model predicts what it would output if executing each task
  Output: Self-awareness report (risks, capabilities, limitations)
```

### Stage 1: Frontier Model Synthesis

**Input Prompt Template:**
```markdown
# Project Brief: Stock Trading Simulator

User Intent: "Build a web app for simulating stock market day trading with 
absolutely minimal initial investment; $1 starting capital and see where it goes."

Your task:
1. Interview the user (via this prompt) to clarify:
   - Real market data or simulated?
   - Time horizon (1 day, 1 week, 1 month simulations)?
   - Strategy constraints (buy/hold, shorting allowed, leverage?)?
   - User interface (web, CLI, mobile)?
   - Cost constraints ($0, or willing to spend $10/month on infrastructure)?

2. Produce a project skeleton including:
   - High-level architecture (API, database, worker, frontend)
   - Core modules (market data ingestion, portfolio engine, backtesting, UI)
   - Tech stack recommendation (language, framework, database, hosting)
   - Critical assumptions and trade-offs

Output as JSON with "architecture", "modules", "tech_stack", "assumptions" keys.
```

**Process:**
1. Send to Claude (Sonnet 4) — get Claude skeleton
2. Send to Gemini (latest) — get Gemini skeleton
3. **You synthesize** — combine, resolve conflicts, produce unified skeleton

**Output:** `project_skeleton.json` containing:
```json
{
  "title": "Stock Trading Simulator",
  "architecture": "...",
  "modules": ["market_data_fetcher", "portfolio_engine", "backtest_runner", "web_ui"],
  "tech_stack": { "backend": "Python FastAPI", "database": "PostgreSQL", ... },
  "assumptions": ["Real market data", "30-day backtest horizon", "No shorting", ...],
  "critical_decisions": [...]
}
```

### Stage 2: Local Model Decomposition

**Input:** `project_skeleton.json` from Stage 1

**Prompt Template:**
```markdown
# Project Decomposition Task

You are given the skeleton of a stock trading simulator project. Your task is to:

1. **Break down each module into sub-modules.** For example:
   - market_data_fetcher → [data_source_adapter, cache_layer, validator]
   
2. **List atomic tasks for each sub-module.** Atomic = can be completed in 1-4 hours.
   Examples:
   - "Implement PostgreSQL schema for portfolio holdings (includes foreign keys, indexes)"
   - "Write unit tests for portfolio balance calculation"
   - "Create Flask route for user login (JWT-based)"

3. **Generate a task dependency graph.** Which tasks must complete before others?

4. **Estimate milestones.** When would you expect each major module to be done?

---

## Project Skeleton

[skeleton from Stage 1 inserted here]

---

## Output Format

Generate a JSON file with:

{
  "modules": {
    "module_name": {
      "sub_modules": [...],
      "atomic_tasks": [
        {
          "id": "task_001",
          "name": "...",
          "description": "...",
          "estimated_hours": 2,
          "dependencies": ["task_prev"],
          "assumptions": ["..."]
        }
      ]
    }
  },
  "dependency_graph": { "task_001": ["task_002", "task_003"], ... },
  "milestones": [
    { "name": "MVP data layer", "target_date": "week 1", "blocking_tasks": [...] }
  ]
}
```

**What to track:**
- Task granularity distribution (histogram of estimated_hours)
- Embedded assumptions (what did the model assume without asking?)
- Dependency accuracy (test against a true DAG)
- Module decomposition consistency (are sub-modules actually separate?)

---

### Stage 3: Local Model Self-Assessment

**Input:** Task list from Stage 2

**Prompt Template:**
```markdown
# Self-Assessment: Model Capability Audit

You have just produced a task decomposition for a stock trading simulator.
Now assess: **If you were asked to execute each atomic task, what would you produce?**

For each task category (API endpoints, database schema, business logic, tests),
answer:

1. **Can you produce working code?** (Yes/No/Partial)
2. **What assumptions must hold for your code to work?**
3. **What would you need to assume about inputs/outputs?**
4. **What tests would you skip or struggle with?**
5. **What external constraints (APIs, libraries, runtime) would block you?**
6. **Overall confidence: 1-5**

---

## Task Categories

- API Endpoints (REST, HTTP)
- Database Schema (SQL DDL)
- Business Logic (calculations, state machines)
- Web UI (HTML/CSS/JS)
- Tests (unit, integration)
- DevOps (Docker, deployment)

Generate a JSON risk assessment for each category.
```

**What to track:**
- Self-awareness accuracy (do Gemma's risk assessments match real failures?)
- Confidence calibration (does high confidence correlate with code quality?)
- Reason for refusals (are they technical or operational?)

---

## Test Execution Workflow

### Running the Full Test

```bash
# Stage 1: Get frontier model skeletons
# (Manual: send the user intent to Claude and Gemini via API/chat)
# Synthesize → project_skeleton.json

# Stage 2: Run local model decomposition
python eval_coding_decompose.py \
  --model gemma4:26b \
  --skeleton project_skeleton.json \
  --output decomposition_gemma4.json

# Stage 3: Run self-assessment
python eval_coding_selfassess.py \
  --model gemma4:26b \
  --decomposition decomposition_gemma4.json \
  --output selfassess_gemma4.json

# Analyze results
python analyze_coding_audit.py \
  --skeleton project_skeleton.json \
  --decomposition decomposition_gemma4.json \
  --selfassess selfassess_gemma4.json \
  --output audit_report_gemma4.json
```

### Metrics to Extract

1. **Task Granularity Histogram**
   ```
   < 1 hour:    10%
   1-4 hours:   65%   ← target
   4-8 hours:   20%
   > 8 hours:   5%
   ```
   If bimodal: Gemma struggled with decomposition.

2. **Assumption List**
   - Tech stack assumptions (Flask, PostgreSQL, etc.)
   - Architectural assumptions (sync vs. async, caching policy)
   - Constraint assumptions (no shorting, 30-day backtest)
   - Unmet questions (should have asked but didn't)

3. **Dependency Graph Accuracy**
   - Count: true positives (correct), false positives (wrong), false negatives (missed)
   - Connectivity: are all truly atomic tasks actually independent?

4. **Self-Assessment Calibration**
   - For 5-10 tasks, actually ask Gemma to execute them
   - Compare Gemma's confidence ("I can do this") vs. code quality
   - Measure: does "confidence 5" code actually work?

---

## Category 3: Image Generation (TEMPLATE)

### Test Structure (To Be Designed)

**Similar three-stage approach but for image generation:**

1. **Frontier models** → Prompt engineering, style guides, composition rules
2. **Local/open-source model** → Generate images, evaluate adherence
3. **Self-assessment** → Model predicts what it can/can't render

**Candidates:**
- Stable Diffusion 3 (open)
- FLUX.1 (open)
- Others

**Tests to consider:**
- Prompt coherence (does image match prompt?)
- Style consistency (can it maintain style across batch?)
- Text rendering (can it render readable text in images?)
- Constraint adherence (no people, specific aspect ratio, etc.)

---

## Meta-Evaluation: Which Category Tests What?

| Category | Tests | Reveals |
|---|---|---|
| **Conversational** | Reasoning, tool use, context, structure | Where does the model understand vs. pattern-match? |
| **Coding** | Decomposition, atomic task creation, self-awareness | Can it break down ambiguous specs? Aware of its limits? |
| **Image Gen** | [TBD] | Can it follow visual constraints? Maintain coherence? |

---

## Integration with Concierge

These audit results feed directly into Concierge's model registry:

```yaml
# Concierge Model Registry Entry

model: gemma4:26b
category: conversational
audit_score: 3.8/5.0
test_results:
  conversational: 4.2
  tooling: 3.5
  instruction_following: 3.0
  context_depth: 4.0
  intent_parsing: 3.5

model: gemma4:26b
category: coding
audit_score: 3.2/5.0
test_results:
  decomposition: 3.0
  task_granularity: 3.2
  dependency_accuracy: 2.8
  self_awareness: 3.5

strengths: [conversational_reasoning, tool_calling, intent_parsing]
weaknesses: [constraint_counting, deep_context, task_granularity]
best_for: [conversational_interaction, structured_output_generation]
avoid_for: [multi_constraint_problems, long_context_reasoning]
```

**Planner uses this to route work:**
- High conversational score → use for interactive disambiguation
- High coding decomposition score → use for breaking down Task Packages
- Low constraint counting → don't use for validation tasks

---

## Roadmap

| Phase | Task | Timeline | Owner |
|---|---|---|---|
| **Now** | Implement `eval_coding_decompose.py` (Stage 2) | 1-2 days | Python script |
| **Now** | Implement `eval_coding_selfassess.py` (Stage 3) | 1-2 days | Python script |
| **This week** | Run full coding audit on Gemma 4, Llama 2 70B | 1 day (2 models × 1 model-run time) | You |
| **This week** | Design image generation test suite (Stage 1-3) | 1 day | You |
| **Next week** | Implement image generation eval script | 1-2 days | Python script |
| **Next week** | Run full image generation audit | 1 day | You |
| **Ongoing** | Update Concierge model registry with results | As evals complete | You |

---

## Files to Create

```
eval_framework/
├── README.md (this file, expanded)
├── conversational/
│   └── eval_bit_model.py (existing, no changes needed)
├── coding/
│   ├── eval_coding_decompose.py (NEW)
│   ├── eval_coding_selfassess.py (NEW)
│   ├── analyze_coding_audit.py (NEW)
│   ├── templates/
│   │   ├── frontier_interview_template.md
│   │   ├── skeleton_schema.json
│   │   └── decomposition_schema.json
│   └── results/
│       ├── project_skeleton.json
│       ├── decomposition_gemma4.json
│       └── audit_report_gemma4.json
├── image_gen/
│   ├── eval_image_gen.py (TBD)
│   └── results/
│       └── [image audit results]
└── model_registry.yaml (Concierge integration)
```

---

## Success Criteria

**You'll know this framework is working when:**

1. ✅ You can run a full conversational audit on any local model in ~10 min
2. ✅ You can run a full coding decomposition audit in ~30 min
3. ✅ Results are reproducible (same model, same skeleton → consistent task list)
4. ✅ You can compare two models side-by-side (Gemma vs. Llama in same skeleton)
5. ✅ Results feed into the Concierge model registry (Router uses them to route)
6. ✅ Self-assessment predictions correlate with actual code quality (spot-check validation)

---

## Next Steps

1. **Create `eval_coding_decompose.py`** — Start with template in Stage 2 above
2. **Run on test skeleton** — Use the stock trading simulator as your first test case
3. **Compare Gemma vs. Llama** — See how different models decompose the same problem
4. **Track metrics** — Task granularity histogram, assumptions, dependency accuracy
5. **Integrate with Concierge** — Use results to populate model registry

This framework will show you exactly where each model belongs in Concierge's stack.
