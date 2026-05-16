# Bit Layer — Local Model Research
*Living document. Update as candidates are tested.*
*Scope: Logos (M1 Max, 64GB unified memory) · Bit Layer 1 only · No quorum participation*
*Last updated: April 2026 — COMPLETE. All tiers tested. Recommendation made.*

---

## Recommendation

**Primary: `gemma4:26b`**

The only model in the field that demonstrably reads and uses context. Dominated all three
conversational sub-prompts — best Steam question, best Concierge hardware question, and
structurally sound fiction questions despite a mild 1B hallucination. Named Wide Not Deep
explicitly in 1C, asked about Docker Tool Zoo compatibility, and distinguished throughput
vs capacity bottleneck without prompting. Perfect tool calling. Best intent parse in the
field. Fast enough at 30.9 t/s for interactive chat on Logos.

The instruction score of 3 (Test 3) is the only weakness and is likely a bullet format
detection artefact — the model's actual instruction-following in conversational testing
shows no such problem.

**Fallback: `qwen2.5:14b`**

If gemma4:26b has production issues (Gemma 4 is two days old at time of testing), the
safest fallback is qwen2.5:14b. Strongest auto-test scores in the field, perfect tool
calling, reliable instruction following. Conversational quality is weaker — it ignored
the timeline document entirely in 1B — but it is a known-stable model with mature Ollama
support and the highest prefill speed observed (7,284 t/s).

**Do not use: `qwen2.5:32b`**

Despite an exceptional 1C response and near-identical quality scores to 14b, the 32b
ran at 5.6 t/s during the conversational test under 6K token context load. In a real
session with accumulated history it will only slow further. Not suitable for interactive
chat on Logos at this time.

---

## Final Rankings — All Tests Complete

| Rank | Model | Conv (30%) | Tool (25%) | Instruct (20%) | Context (15%) | Latency (10%) | **Total** |
|------|-------|-----------|-----------|---------------|--------------|--------------|-----------|
| 1 | `gemma4:26b` | 4.67 | 5 | 3 | 5 | 3 (31.4 t/s) | **4.30** |
| 2 | `qwen2.5:32b` | 3.67 | 5 | 5 | 4 | 1 (5.6 t/s) | **4.05** |
| 3 | `qwen2.5:14b` | 2.67 | 5 | 5 | 4 | 2 (15.4 t/s) | **3.85** |
| 4 | `mistral-nemo:12b` | 3.00 | 5 | 3 | 5 | 3 (25.1 t/s) | **3.80** |

Note: latency scores in the shortlist run reflect actual decode under ~6K token context
load, which is more realistic than the baseline single-turn scores.

---

## Test 1 Sub-Prompt Scores (Shortlist Phase)

| Model | 1A Steam | 1B Fiction | 1C Concierge | Conv Avg |
|-------|---------|-----------|-------------|---------|
| `gemma4:26b` | 5 | 4 | 5 | **4.67** |
| `qwen2.5:32b` | 3 | 3 | 5 | **3.67** |
| `mistral-nemo:12b` | 3 | 2 | 4 | **3.00** |
| `qwen2.5:14b` | 3 | 2 | 3 | **2.67** |

**1A (Steam) — scoring:** 5=non-obvious probing (completion habits, abandoned-game
diagnostic); 3=generic genre/preference; 2=recommends games anyway.

**1B (Fiction) — scoring:** 5=identifies 0346-0350DE compression or 0685-0688DE Phineas
hunt; 3=no timeline engagement; 2=suggests setting directly.

**1C (Concierge) — scoring:** 5=names Wide Not Deep, asks about training lineage diversity
and bandwidth; 3=generic compute questions; 2=recommends hardware directly.

### Notable observations

**gemma4:26b 1A:** Asked narrative vs mechanics, intensity/vibe, AND the abandoned-game
question — diagnosing failure modes rather than just preferences. No other model thought
of this.

**gemma4:26b 1B:** Claimed the timeline was not attached (it was — likely a context
parsing edge case with the docx format). Despite this, the structural questions it asked
anyway — macro vs micro scale, onset vs consequences, golden age vs dark age — map
directly onto the dramatically richest periods in the timeline and are better than
competitors who had the document and ignored it.

**gemma4:26b 1C:** Named Wide Not Deep explicitly. Asked about Docker Tool Zoo
compatibility as an admission criterion. Distinguished throughput vs capacity bottleneck
in the Router telemetry question. Best response in the entire evaluation.

**qwen2.5:32b 1C:** Only Qwen model to absorb the philosophy doc. Explicitly invoked Wide
Not Deep, asked about model diversity by family AND training lineage, and asked about
priority lane distribution. Strong architectural awareness. Saved by one excellent answer.

**qwen2.5:14b and mistral-nemo:12b 1B:** Both completely ignored the timeline document,
asking questions that could have been posed with no context at all. Clear ceiling on
context utilisation for these models.

---

## Full Comparison Matrix — All Candidates

| Model | Tool (25%) | Instruct (20%) | Context (15%) | Latency (10%) | Conv (30%) | **Total** | Status |
|-------|-----------|---------------|--------------|--------------|-----------|-----------|--------|
| `gemma4:26b` | 5 | 3 | 5 | 3 (31.4 t/s) | 4.67 | **4.30** | ✓ #1 |
| `qwen2.5:32b` | 5 | 5 | 4 | 1 (5.6 t/s) | 3.67 | **4.05** | ✓ #2 |
| `qwen2.5:14b` | 5 | 5 | 4 | 2 (15.4 t/s) | 2.67 | **3.85** | ✓ #3 — recommended fallback |
| `mistral-nemo:12b` | 5 | 3 | 5 | 3 (25.1 t/s) | 3.00 | **3.80** | ✓ #4 |
| `command-r:35b` | 2 | 5 | 5 | 2 (12.9 t/s) | — | **3.50** | borderline — not tested in shortlist |
| `gemma4:31b` | 5 | 5 | 1 | 1 (5.5 t/s) | — | **3.57** | ✗ DNF — latency |
| `mistral-small:22b` | 2 | 3 | 4 | 2 (19.9 t/s) | — | **2.71** | ✗ DNF — wrong channel |
| `phi4:14b` | 1 | 4 | 1 | 2 (18.7 t/s) | — | **2.00** | ✗ DNF — tool schema error |
| `llama3.1:8b` | 1 | 3 | 4 | 3 (36.6 t/s) | — | **2.50** | ✗ DNF — tool call failures |

---

## DNF List

| Model | Failure reason |
|-------|---------------|
| `phi4:14b` | 400 error on tool schema — complete rejection by Ollama |
| `llama3.1:8b` | Three distinct failures: no parallel calls, batched node IDs, spurious call on no-call prompt |
| `mistral-small:22b` | Correct JSON delivered in prose channel — not structured tool calls. Unusable for OpenAI-compatible frontend. |
| `gemma4:31b` | 5.5 t/s decode — not interactive. Test 4 timeout at 300s. DNF on latency, not quality. |

---

## Evaluation Criteria

| Dimension | Weight | Notes |
|-----------|--------|-------|
| Conversational reasoning | **30%** | Three sub-prompts: Steam (vacuum), Fiction (timeline doc), Concierge hardware (philosophy doc). Human-scored. |
| Structured tool calling | **25%** | OpenAI tool-use schema. Parallel calls + abstain check. Auto-scored. |
| Instruction following | **20%** | 4-constraint formatting test. Auto-scored. |
| Context retention | **15%** | 15K token needle retrieval. Auto-checked. |
| Latency on Metal | **10%** | Decode t/s under realistic context load. ≥80=5, ≥50=4, ≥25=3, ≥10=2, <10=1 |

---

## Detailed Results — Shortlisted Models

### `gemma4:26b` — RECOMMENDED
Family: Gemma 4 (Google) | Size: 26B MoE (~4B active) | Backend: llama.cpp/MLX-auto

| Test | Score | Notes |
|------|-------|-------|
| Test 1A — Steam | 5 | Narrative/mechanics, intensity/vibe, abandoned-game diagnostic. Best in field. |
| Test 1B — Fiction | 4 | Mild hallucination (claimed doc not attached). Structural questions excellent anyway. |
| Test 1C — Concierge | 5 | Named Wide Not Deep, Docker Tool Zoo, throughput vs capacity. Best in field. |
| Test 2 — Tool Calling | 5 | 2 valid calls, correct args. Abstains correctly. |
| Test 3 — Instruction | 3 | Parser missed bullet format (bullet_count=0). Likely artefact not real failure. |
| Test 4 — Context | 5 | Clean bold retrieval: "The full value of the ARCHIVE_KEY was ZULU-9-OMEGA." |
| Test 5 — Intent | 5 | Best intent parse in field. Rich semantic JSON, no fences, proper conditions. |
| **Final Total** | **4.30** | |

---

### `qwen2.5:14b` — RECOMMENDED FALLBACK
Family: Qwen (Alibaba) | Size: 14B | Backend: llama.cpp/MLX-auto (Q4_K_M)

| Test | Score | Notes |
|------|-------|-------|
| Test 1A — Steam | 3 | Genre/multiplayer/mechanics — standard. |
| Test 1B — Fiction | 2 | Ignored timeline. Generic creative questions. |
| Test 1C — Concierge | 3 | Queue depth questions but no Wide Not Deep awareness. |
| Test 2 — Tool Calling | 5 | 2 valid calls, correct args. Abstains correctly. |
| Test 3 — Instruction | 5 | All 4 constraints satisfied. |
| Test 4 — Context | 4 | Correct retrieval, quoted full annotation markup. |
| Test 5 — Intent | 5 | Valid JSON, all branches. Minor markdown fences. |
| **Final Total** | **3.85** | |

---

### `qwen2.5:32b` — NOT RECOMMENDED (latency)
Family: Qwen (Alibaba) | Size: 32B | Backend: llama.cpp/MLX-auto (Q4_K_M)

| Test | Score | Notes |
|------|-------|-------|
| Test 1A — Steam | 3 | Genre/playstyle/multiplayer — generic. |
| Test 1B — Fiction | 3 | Some structural awareness (unexplored history). No specific period identified. |
| Test 1C — Concierge | 5 | Exceptional. Explicit Wide Not Deep, lineage diversity, priority lane distribution. |
| Test 2 — Tool Calling | 5 | 2 valid calls, correct args. Abstains correctly. |
| Test 3 — Instruction | 5 | All 4 constraints satisfied. |
| Test 4 — Context | 4 | Correct retrieval, bracket notation. |
| Test 5 — Intent | 5 | Valid JSON, all branches. |
| **Final Total** | **4.05** | 5.6 t/s under context load — not interactive. |

---

### `mistral-nemo:12b`
Family: Mistral | Size: 12B | Backend: llama.cpp/MLX-auto (Q4_0)

| Test | Score | Notes |
|------|-------|-------|
| Test 1A — Steam | 3 | Genre/playstyle/session-length — standard. |
| Test 1B — Fiction | 2 | No timeline engagement. Generic questions. |
| Test 1C — Concierge | 4 | IQ ceiling / capability_exceeded reference — architecturally aware. Missed lineage diversity. |
| Test 2 — Tool Calling | 5 | 2 valid calls, correct args. Abstains correctly. |
| Test 3 — Instruction | 3 | Used forbidden words 'mac' and 'memory'. 2/4 constraints. |
| Test 4 — Context | 5 | Clean exact retrieval. Fastest at 34.6 t/s baseline. |
| Test 5 — Intent | 5 | Valid JSON, all branches. |
| **Final Total** | **3.80** | |

---

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| April 2026 | Research scope locked to Bit Layer 1 only | Logos not participating in Workbee or quorum |
| April 2026 | Ollama as serving backend | Single-user interactive app on Apple Silicon. llama.cpp at Workbee layer. |
| April 2026 | Native function-calling is a hard requirement | Bespoke frontend uses OpenAI tool-use schema. Prose JSON not acceptable. |
| April 2026 | Test 1 deferred to shortlist phase | Domain knowledge required to score. Used Concierge-specific and personal prompts. |
| April 2026 | phi4:14b rejected | 400 error on tool schema. Hard requirement failure. |
| April 2026 | llama3.1:8b rejected | Three distinct tool call failures. Latency reference only. |
| April 2026 | mistral-small:22b rejected | Correct JSON in prose channel — not structured tool calls. |
| April 2026 | gemma4:31b rejected | 5.5 t/s decode — not interactive. Test 4 timeout. DNF on latency not quality. |
| April 2026 | gemma3 removed from candidate list | Superseded by Gemma 4 released April 3, 2026. |
| April 2026 | Ollama 0.20.2 required for Gemma 4 | 0.19.0 server rejects Gemma 4 pull with 412. Confirmed via brew upgrade + server restart. |
| April 2026 | OLLAMA_NEW_ENGINE=1 required for MLX | Must be set at server start. Confirmed via server config log. |
| April 2026 | gemma4:26b selected as primary recommendation | Best conversational reasoning in field. Only model that demonstrably read and used context documents. Fast enough for interactive use at 30.9 t/s. |
| April 2026 | qwen2.5:14b selected as fallback | Most stable model in field. Gemma 4 is two days old at time of testing. Known-good Ollama support. |
| April 2026 | qwen2.5:32b not recommended despite quality | 5.6 t/s under context load — not interactive. Will slow further with accumulated history. |

---

## Open Questions — Post Decision

- [ ] gemma4:26b Test 3: confirm bullet format used in actual response — if proper bullets were present the score should be revised to 4-5 before the spec is updated.
- [ ] gemma4:26b 1B hallucination: investigate whether the docx injection via pandoc is producing a format Gemma 4 doesn't parse as an attached document. May need to convert to plain text before injection.
- [ ] command-r:35b tool schema: the tool_name/parameters wrapper may be fixable via system prompt. Worth a targeted retest if gemma4:26b proves unstable in production.
- [ ] Confirm OLLAMA_NEW_ENGINE=1 persists across server restarts — add to startup config or launchd plist so it doesn't need to be set manually each session.
- [ ] Model keep-alive: consider setting OLLAMA_KEEP_ALIVE=-1 for the chosen model so it stays resident and avoids cold-start latency during normal use.
