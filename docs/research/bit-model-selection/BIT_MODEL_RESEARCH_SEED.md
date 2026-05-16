# BIT LAYER — LOCAL MODEL RESEARCH SEED
**Version:** 1.0 — April 2026
**Purpose:** Cold-start context for a new AI session joining the Bit layer local model research. Contains all decisions, constraints, and open work needed to contribute without reading the full Concierge spec corpus.
**Scope:** This seed covers one narrow problem only. Do not expand scope without explicit instruction.

---

## What Concierge Is (Minimum Viable Context)

Concierge is a personal AI task orchestration system running on a homelab cluster. It is organized as a strict five-layer pipeline:

```
Bit → Planner → Router → Foreman → Workbee
```

Each layer communicates only with its immediate neighbors. No layer has knowledge of non-adjacent layers. This is an architectural invariant, not a guideline.

The guiding philosophy is **Wide Not Deep**: correctness emerges from structured disagreement across a diverse ensemble of smaller, specialized models from genuinely different training lineages, not from a single large model. This applies to the Workbee inference fleet. It does not apply to this research task.

---

## The Specific Problem This Seed Is For

**Bit** is Layer 1 — the human-facing application. It captures intent, translates it into typed artifacts for the layer below, surfaces results back to the human, and acts as a first-level conversational agent when the wider Concierge stack is unavailable.

Bit requires a local LLM to function. The goal of this research is to **select that model**.

This is the only problem in scope. Do not recommend models for any other layer. Do not evaluate ensemble fleet candidates here. Do not apply quorum diversity rules — Bit's local model does not participate in the quorum.

---

## Hardware

**Node:** Logos — M1 Max MacBook Pro, 64GB unified memory
**GPU:** Apple Silicon GPU (Metal)
**Inference backend:** Ollama (serving via localhost, OpenAI-compatible API)
**Acceleration priority:** Metal GPU → CPU fallback → ANE (deferred to a later phase, not in scope now)

Ollama is confirmed as the serving backend. llama.cpp is not being evaluated for this node. That decision is locked — llama.cpp is the correct backend at the Workbee layer for CUDA/ROCm nodes; it is not the right fit for a single-user interactive application on Apple Silicon.

---

## What Bit's Local LLM Must Do

**Primary role — in order of precedence:**

1. **Conversational assistant with tool use.** Act as a capable surrogate for Claude/Gemini when those services are unavailable. Rubber-duck reasoning, multi-turn dialogue, research assistance with web search and local tool calls. This is the dominant workload. It must be genuinely good at this — not a degraded fallback.

2. **Intent parsing.** Produce structured artifacts from natural language task descriptions to feed the Planner (Layer 2). This is secondary and lighter-weight than the conversational role.

**Explicitly out of scope for this model:**
- Code assistance — that will be routed to a separate specialist model
- Workbee execution tasks — Bit never executes work, only captures and translates intent
- Quorum participation — Bit's local model is advisory only, never in the ensemble

---

## Hard Requirements

| Requirement | Detail |
|-------------|--------|
| Native structured function calling | OpenAI tool-use schema (JSON). Not prompted workarounds. The bespoke frontend being built by Claude Code will rely on this. |
| Metal GPU acceleration via Ollama | Must run well on Apple Silicon. Poor Metal support is a disqualifier. |
| Interactive latency | Must feel responsive in chat. Token generation must be perceptually fast at the size tier evaluated. |
| Instruction following | Must follow multi-part, constrained instructions reliably across long sessions. |
| Multi-turn coherence | Must maintain context and reasoning quality over extended conversations. |

---

## Size Tier Guidance

64GB unified memory makes the full size range technically resident. However, interactive latency is the binding constraint for a chat assistant, not raw capability.

| Tier | Size | VRAM est. (Q4_K_M) | Assessment |
|------|------|---------------------|------------|
| Small | 7B–8B | ~5–6 GB | Viable latency reference / fallback only. Reasoning ceiling likely insufficient for surrogate role. |
| Medium | 14B | ~9–10 GB | Primary research focus. Strong latency, meaningful reasoning. |
| Large | 27B–32B | ~17–20 GB | Secondary focus. Test if reasoning delta justifies latency cost over 14B. |
| XL | 70B | ~40–45 GB | Stretch only. Resident-capable but likely too slow for chat on a single-user node. |

**Start with 14B tier. Then test one 32B candidate. Only test 70B if 32B latency is acceptable.**

---

## Candidate List

### Tier 1 — Test First

| Model (Ollama tag) | Family | Size | Notes |
|--------------------|--------|------|-------|
| `qwen2.5:14b` | Qwen (Alibaba) | 14B | Strong instruction following. Referenced in existing spec as current default. Establish as baseline. |
| `mistral-nemo:12b` | Mistral | 12B | Strong native tool use reputation. Good counter-candidate to Qwen at this tier. |
| `qwen2.5:32b` | Qwen (Alibaba) | 32B | Test reasoning delta vs 14B sibling. Latency may rule it out. |
| `phi4:14b` | Phi (Microsoft) | 14B | Different training lineage from Qwen. Strong reasoning for size. Worth comparing directly. |

### Tier 2 — Test If Time Permits

| Model (Ollama tag) | Family | Size | Notes |
|--------------------|--------|------|-------|
| `mistral-small:22b` | Mistral | 22B | Mid-tier. Compare to Qwen 32B. |
| `gemma3:12b` | Gemma (Google) | 12B | Google lineage. Good conversational reports. |
| `gemma3:27b` | Gemma (Google) | 27B | Larger Gemma. Compare against Qwen 32B. |
| `command-r:35b` | Command R (Cohere) | 35B | Purpose-built for RAG and tool use. Worth evaluating if 32B tier shows promise. |
| `llama3.1:8b` | Llama 3 (Meta) | 8B | Latency reference point only. |

### Do Not Test

- Models below 7B — too small for surrogate conversational role
- Base models (instruct variants only)
- Models without confirmed native function calling support
- Models with known poor Metal/Ollama support

---

## Evaluation Criteria (Weighted)

| Dimension | Weight | What to evaluate |
|-----------|--------|-----------------|
| Conversational reasoning | 30% | Multi-turn coherence, rubber-duck quality, nuanced response, contextual tracking |
| Structured tool calling | 25% | JSON schema adherence, parallel tool calls, error recovery on bad args |
| Instruction following | 20% | Constraint adherence across multi-part instructions, low hallucination rate |
| Context retention | 15% | Accuracy over long sessions (8K+ tokens in window) |
| Latency on Metal | 10% | Tokens/sec via Ollama on M1 Max — must feel interactive |

Score each dimension 1–5. Multiply by weight. Sum for total.

---

## Standardized Test Protocol

Run every candidate through the same five tests in order. Do not skip tests. Record results using the per-model template below.

### Test 1 — Rubber Duck
Give the model a moderately complex technical problem you are actively working on. Instruct it to help you think through it by asking questions and reflecting back — not giving answers. Evaluate: does it surface non-obvious angles? Does it track what has been said across turns without prompting?

### Test 2 — Tool Call Schema
Via the Ollama API with a defined tool schema (e.g. `search_web(query: str)` or `get_file(path: str)`), send a prompt requiring one tool call. Verify the response is a valid JSON tool invocation matching the schema exactly. Then send a prompt requiring two simultaneous tool calls. Note whether both are issued correctly in a single response.

### Test 3 — Instruction Discipline
Issue a multi-part instruction with explicit constraints (e.g. "Summarize this in exactly 3 bullet points, each starting with a verb, each under 12 words"). Evaluate whether all constraints are honoured, partially ignored, or silently dropped.

### Test 4 — Context Load
Load a long document into context (10K+ tokens). After adding substantial content after it, ask specific questions about details from early in the document. Note accuracy degradation.

### Test 5 — Intent Parsing
Give the model a natural language task description (e.g. "I want to refactor the JobManager class to decouple the approval flow from the persistence layer"). Ask it to produce a JSON object with fields: `intent_type`, `target`, `action`, `constraints[]`. Evaluate schema compliance and semantic accuracy of the parsed output.

---

## Per-Model Recording Template

Copy for each candidate tested.

```
### [model-tag:size]

**Family:**
**Tested:**
**Quantization used:** [note what Ollama defaulted to]

#### Performance on Logos (M1 Max)
- Token/sec (generation):
- Time to first token:
- Context window used in test:
- Metal GPU in use: [confirm via Activity Monitor / powermetrics]

#### Function Calling
- Single tool call schema adherence: [pass / partial / fail]
- Parallel tool calls: [supported / broken / not tested]
- Error recovery on bad args:
- Notes:

#### Conversational Quality
- Rubber-duck reasoning (Test 1): [1–5]
- Multi-turn coherence: [1–5]
- Response calibration: [too brief / calibrated / too verbose]
- Notes:

#### Instruction Following
- Constraint adherence (Test 3): [1–5]
- Hallucination tendency: [low / medium / high]
- Notes:

#### Context Retention
- Tested at [N]K tokens: [accurate / degraded / failed]
- Notes:

#### Weighted Score
| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Conversational reasoning | 30% | | |
| Structured tool calling | 25% | | |
| Instruction following | 20% | | |
| Context retention | 15% | | |
| Latency on Metal | 10% | | |
| **Total** | | | |

**Verdict:** [Shortlist / Reject / Retest at different quant]
**Reject reason (if applicable):**
```

---

## Decisions Already Made — Do Not Revisit

| Decision | Rationale |
|----------|-----------|
| Logos runs Bit layer only | Not participating in Workbee or quorum at this stage. |
| Ollama as serving backend (not llama.cpp) | Single-user interactive app on one machine. Ollama's Metal support, model management, and OpenAI-compatible API are the right fit. llama.cpp belongs at the Workbee layer. |
| Native function calling is a hard requirement | The bespoke OpenAI-compatible frontend being built by Claude Code depends on it. Prompted workarounds are not acceptable. |
| 14B and 32B as primary research tiers | 64GB gives headroom; interactive latency favours sub-32B; 70B as stretch only. |
| Code assistance is out of scope for this model | Will be routed to a separate specialist model. Bit does not perform code tasks. |
| ANE support deferred | Not in scope for initial Bit deployment. GPU → CPU path is sufficient for now. |
| Quorum rules do not apply | Bit's local model is advisory only. Training lineage diversity is irrelevant here. |

---

## Open Questions (Unresolved)

- What quantization does Ollama default to per candidate tag, and should Q8 variants be tested for meaningful quality delta?
- Does Ollama's current release support parallel tool calls for all candidates, or only specific model families?
- At what context length does the M1 Max begin offloading to CPU, and how does that affect latency profile for long sessions?
- Is there a meaningful quality gap between `qwen2.5:14b` and `qwen2.5:32b` that justifies the latency cost for the conversational role specifically?

---

## What to Produce

At the end of research, deliver:

1. A completed comparison matrix with all tested candidates scored
2. A primary recommendation with rationale
3. A fallback recommendation if the primary is ruled out by latency
4. Any open questions surfaced during testing that affect the decision

The recommendation should be specific and opinionated. A reasoned recommendation with stated uncertainty is more useful than a hedged list.

---

*Seed created: April 2026. Session: Concierge Bit Layer Model Research.*
*Companion document: `BIT_MODEL_RESEARCH.md` — full living tracker with per-model templates.*
