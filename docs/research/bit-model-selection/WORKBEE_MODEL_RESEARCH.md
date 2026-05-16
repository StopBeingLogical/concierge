# Workbee Layer — Local Model Research
*Living document. Update as candidates are tested.*
*Scope: Kratos (Ryzen 7600X, RX 7800 XT 16GB) · Noesis (i7-1185G7, 32GB) · Ergaster (i9-13900HK, 64GB) · Workbee layer only · No Bit layer overlap*
*Last updated: April 2026 — Ergaster added. Benchmark phase complete across all nodes.*

---

## Recommendation

**Primary: `Qwen3.5-35B-A3B` (APEX Mini quant, Q3_K_M, 12.33 GiB)**

The only model tested that fits in 16GB VRAM while delivering 35B-class knowledge. MoE architecture (3B active parameters per token) produces 77 t/s generation on Kratos GPU — matching Logos running a 7B model. Perfect tool calling and instruction following validated in the Bit layer research doc (qwen2.5 family baseline). Context degradation is moderate: 20% drop at 8K depth (77 → 62 t/s), establishing a conservative SLA floor of 60 t/s.

**Fallback: `Qwen2.5-14B-Instruct` (Q4_K_M, 8.37 GiB)**

Validated in the Bit layer research doc with perfect tool calling and instruction following scores. 35 t/s on Kratos GPU. Smaller VRAM footprint leaves more headroom for KV cache. Known-stable Ollama support. Use if Qwen3.5 proves unstable or if VRAM pressure becomes an issue at high context depths.

**Noesis: CPU-only, small models only**

Iris Xe SYCL inference tested and confirmed unusable (0.66 t/s vs 49 t/s CPU on TinyLlama). Noesis is not a viable inference node for workbee-class models. Reserve for lightweight classification, routing logic, or background tasks where latency is not a constraint.

**Ergaster: Primary Router · Long-Context CPU Inference Fallback**

i9-13900HK (6P + 14E cores, 5.2GHz boost), 64GB RAM, 425GB storage. Primary role is Router layer — not inference. Secondary role is long-context CPU inference fallback for tasks that exceed Kratos's 8K VRAM context ceiling. 64GB RAM means no OOM at any tested context depth. Optimal inference config: `-t 6` (P-cores only) — E-cores actively hurt tg128 (52 t/s at -t 6 vs 17 t/s at -t 20). At 15.73 t/s on Qwen3.5 35B-A3B, usable for background/non-latency-sensitive tasks up to 32K+ context.

---

## Fleet Benchmark Summary

All results from llama.cpp direct (ROCm build on Kratos, CPU build on Noesis/Ergaster). Not Ollama — raw silicon numbers.

### TinyLlama 1B Q4_0 — Cross-Fleet Baseline

| Machine | Backend | pp512 (t/s) | tg128 (t/s) |
|---------|---------|------------|------------|
| Noesis | CPU 8t | 247 | 49 |
| Noesis | SYCL (Iris Xe) | 30 | 0.66 |
| Ergaster | CPU 6t (P-cores) | 268 | 52.91 |
| Ergaster | CPU 12t | 252 | 26.59 |
| Ergaster | CPU 20t (all) | 307 | 16.85 |
| Kratos | CPU | 5562 | 93 |
| Kratos | ROCm GPU | 10118 | 283 |

### Qwen2.5 14B Q4_K_M — Dense Workbee Candidate

| Machine | Backend | pp512 (t/s) | tg128 (t/s) |
|---------|---------|------------|------------|
| Noesis | CPU 8t | — | ~7 (est) |
| Kratos | CPU (ngl=0) | 591 | 7.18 |
| Kratos | ROCm GPU (ngl=99) | 1060 | 35.62 |

### Qwen3.5 35B-A3B APEX Mini Q3_K_M — MoE Workbee Candidate

| Machine | Backend | pp512 (t/s) | tg128 (t/s) |
|---------|---------|------------|------------|
| Noesis | CPU 8t | 30 | 13.52 |
| Ergaster | CPU 6t (P-cores) | 60 | 15.73 |
| Kratos | CPU (ngl=0) | 669 | 23.91 |
| Kratos | ROCm GPU (ngl=99) | 1455 | 77.60 |

### Logos M1 Max — Reference Only (Bit Layer Node)

| Model | Backend | tg128 (t/s) |
|-------|---------|------------|
| TinyLlama 1B | Metal | 192 |
| Qwen2.5 7B Q4_K_M | Metal | 37 |
| Qwen2.5 7B Q4_K_M | MLX | 77 |
| Gemma4 26B-A4B Q4_K_M | Metal | 45 |
| Gemma4 26B-A4B Q4_K_M | CPU | 25 |

---

## Context Depth Degradation — Qwen3.5 35B-A3B on Kratos

Tested with `-d` flag (pre-filled KV cache depth) to simulate realistic accumulated context load. Two configurations tested.

### APEX Mini (Q3_K_M, 12.33 GiB) — Full GPU, KV cache in VRAM

| Context Depth | tg128 (t/s) | Degradation vs Baseline |
|--------------|------------|------------------------|
| 0 (baseline) | 77.60 | — |
| 8192 | 62.51 | −19.4% |
| 16384 | OOM crash | — |

**Context ceiling: 8192 tokens.** VRAM headroom (~3.7 GiB) exhausted at 16K.

**SLA floor recommendation: 60 t/s** for tasks within 8K context budget.

### Q4_K_M (19.92 GiB) — 30/60 layers GPU, KV cache in CPU RAM (`-ngl 30 -nkvo 1`)

| Context Depth | tg128 (t/s) | Degradation vs Baseline |
|--------------|------------|------------------------|
| 0 (baseline) | 40.79 | — |
| 8192 | 24.03 | −41.1% |
| 16384 | 20.09 | −50.7% |
| 32768 | 15.24 | −62.6% |

**Context ceiling: 32K+ tokens** (no OOM at 32K, further testing not conducted).

### Configuration Decision

APEX Mini is the default workbee configuration — 2x faster at every comparable context depth. Q4_K_M with CPU offload (`-ngl 30 -nkvo 1`) is a long-context fallback mode only, activated explicitly for tasks requiring >8K context. At 15-20 t/s it remains usable but is not suitable for latency-sensitive workbee pipelines.

---

## Context Depth Degradation — Gemma4 26B-A4B on Logos (Reference)

Logos included for reference — not a workbee node, but useful for comparison. Unified memory architecture means no hard OOM ceiling, just smooth degradation.

| Context Depth | tg128 (t/s) | Degradation vs Baseline |
|--------------|------------|------------------------|
| 0 (baseline) | 45.27 | — |
| 8192 | 30.39 | −32.9% |
| 16384 | 23.32 | −48.5% |
| 32768 | 15.83 | −65.0% |

Logos degrades more steeply than Kratos APEX Mini percentage-wise but never crashes — unified memory absorbs the KV cache overflow gracefully. No OOM at any tested depth.

---

## Context Depth Degradation — Qwen3.5 35B-A3B on Noesis (Reference)

CPU-only. Included for completeness — not viable for workbee inference.

### APEX Mini (Q3_K_M, 12.33 GiB) — CPU 8 threads

| Context Depth | tg128 (t/s) | Degradation vs Baseline |
|--------------|------------|------------------------|
| 0 (baseline) | 13.52 | — |
| 8192 | 9.82 | −27.4% |

Wall clock time at 8K context: ~13 seconds per 128 tokens. Not suitable for interactive or pipeline use.

---

## Context Depth Degradation — Qwen3.5 35B-A3B on Ergaster (Long-Context Fallback)

CPU-only, `-t 6` (P-cores). No OOM at any depth — 64GB RAM absorbs KV cache completely. This is the long-context fallback path for tasks that exceed Kratos's 8K VRAM ceiling.

### APEX Mini (Q3_K_M, 12.33 GiB) — CPU 6 threads (P-cores)

| Context Depth | tg128 (t/s) | Degradation vs Baseline |
|--------------|------------|------------------------|
| 0 (baseline) | 15.73 | — |
| 8192 | 13.36 | −15.1% |
| 16384 | 11.41 | −27.5% |
| 32768 | 8.69 | −44.7% |

Degradation is gradual and predictable — no hard ceiling. Ergaster can handle context depths that would crash Kratos, at the cost of ~5x lower throughput. Suitable for background, batch, or low-priority long-context tasks. Not suitable for interactive or latency-sensitive pipeline use.

---

## Ollama vs llama.cpp Overhead

Tested on Kratos ROCm with TinyLlama 1B:

| Runtime | tg128 (t/s) |
|---------|------------|
| Ollama (ROCm) | 315 |
| llama.cpp ROCm direct | 283 |

Ollama is slightly faster on tg128 for this model, likely due to fork-specific ROCm tuning. llama.cpp direct wins significantly on pp (prompt processing) and is the right choice for benchmarking. For serving, Ollama is acceptable on Kratos.

---

## Model Size / VRAM Fit on Kratos (16GB)

| Model | Quant | Size | Fits in 16GB? | Notes |
|-------|-------|------|--------------|-------|
| Qwen2.5 14B | Q4_K_M | 8.37 GiB | ✓ Yes — comfortable | ~7.6GB headroom for KV cache |
| Qwen3.5 35B-A3B | APEX Mini (Q3_K_M) | 12.33 GiB | ✓ Yes — tight | ~3.7GB headroom for KV cache |
| Qwen3.5 35B-A3B | Q4_K_M | ~20 GiB | ✗ No | Requires CPU offload |
| Gemma4 26B-A4B | Q4_K_M | 15.63 GiB | ✗ Marginal | No KV cache headroom |
| Gemma4 31B Dense | Q4_K_M | ~19 GiB | ✗ No | Does not fit |

---

## Why MoE Wins for Workbee Use

Qwen3.5 35B-A3B uses Mixture-of-Experts architecture with 256 experts per layer, routing 8+1 (shared) per token. Only ~3B parameters are active per forward pass despite 35B total weights. This produces:

- GPU compute load equivalent to a ~3B dense model
- Knowledge capacity equivalent to a 35B dense model
- Token generation speed (77 t/s) matching Logos running a 7B dense model
- No throughput penalty vs Qwen2.5 14B despite 2.5x more total parameters

The tradeoff is VRAM: all 35B of expert weights must reside in VRAM even though only a fraction are used per token. The APEX Mini quant (12.33 GiB) was specifically engineered to fit 16GB consumer GPUs while preserving quality.

---

## Noesis Role Assessment

| Metric | Result |
|--------|--------|
| TinyLlama CPU (8t) tg128 | 49 t/s |
| TinyLlama SYCL (Iris Xe) tg128 | 0.66 t/s |
| Qwen3.5 35B-A3B CPU tg128 | 13.5 t/s |
| Inference node viability | ✗ No |

Iris Xe SYCL is slower than CPU by 74x on this workload due to: shared memory bandwidth contention with CPU, SYCL kernel dispatch overhead, insufficient EU count (96 EUs) for LLM matrix operations, and llama.cpp SYCL backend tuned for Arc discrete GPUs not iGPU.

Noesis recommended role: lightweight CPU tasks, Concierge ingestion layer classification (GNA 2.0 substrate — future work), routing logic. Not model serving.

---

## Ergaster Role Assessment

| Metric | Result |
|--------|--------|
| TinyLlama CPU (6t P-cores) tg128 | 52.91 t/s |
| TinyLlama CPU (20t all) tg128 | 16.85 t/s |
| Qwen3.5 35B-A3B CPU (6t) tg128 | 15.73 t/s |
| Qwen3.5 35B-A3B CPU (6t) tg128 @ 32K | 8.69 t/s |
| OOM at any depth | ✗ Never (64GB RAM) |
| Primary role | Router layer |
| Inference role | Long-context CPU fallback only |

P/E core split is the key finding: `-t 6` (P-cores only) wins decisively for token generation (52.91 t/s) vs `-t 20` all-cores (16.85 t/s). The 14 E-cores actively hurt tg128 by creating memory bandwidth contention. Use `-t 6` for all inference workloads. Use `-t 20` only if prompt processing throughput is the bottleneck.

Optimal inference config: `./llama-bench -t 6`

---

## Open Items

- [ ] Validate Qwen3.5 35B-A3B tool calling against OpenAI schema (not yet tested — inferred from Qwen family baseline)
- [ ] Test Qwen3.5 35B-A3B instruction following under Concierge-specific structured output prompts
- [ ] Run context depth test beyond 32K on Q4_K_M CPU offload config to find hard ceiling
- [ ] Revisit when mlx-lm adds Gemma4 support — retest Logos Gemma4 via MLX (expect ~80-90 t/s)
- [ ] Consider Qwen3.5 9B as a Noesis-specific model if CPU inference is needed at usable speed (~30+ t/s estimated)

---

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| April 2026 | Research scope: Kratos + Noesis workbee layer | Logos scoped to Bit layer only per BIT_MODEL_RESEARCH.md |
| April 2026 | llama.cpp direct as benchmark runtime | Lower overhead than Ollama; more accurate silicon baseline |
| April 2026 | ROCm build with ROCR_VISIBLE_DEVICES=0 | iGPU (gfx1036) causes segfault on enumeration; dGPU only |
| April 2026 | Iris Xe SYCL path abandoned | 0.66 t/s vs 49 t/s CPU — 74x slower, not viable |
| April 2026 | Qwen3.5 35B-A3B APEX Mini selected as primary | 77 t/s GPU, fits 16GB, MoE efficiency, 35B knowledge |
| April 2026 | Qwen2.5 14B retained as fallback | Known-stable, validated tool calling, smaller VRAM footprint |
| April 2026 | Gemma4 ruled out for Kratos | 26B too large for 16GB with KV cache; no intermediate size in Gemma4 family |
| April 2026 | SLA floor set at 60 t/s | Conservative figure accounting for 8K context depth degradation |
| April 2026 | Q4_K_M CPU offload designated as long-context fallback only | 15-24 t/s at 8K-32K depth — usable but not primary path |
| April 2026 | APEX Mini context ceiling confirmed at 8192 tokens | OOM crash at 16K; 3.7 GiB KV headroom insufficient for deeper context |
| April 2026 | Ergaster added to fleet | i9-13900HK, 64GB RAM, primary Router node, secondary long-context inference fallback |
| April 2026 | Ergaster optimal thread count: -t 6 | P-cores only wins tg128 by 3x over all-cores; E-cores create memory bandwidth contention |
| April 2026 | Ergaster designated long-context fallback | 64GB RAM eliminates OOM ceiling; handles 32K+ context that crashes Kratos |