# Concierge — Model Fleet Brief
*For: Claude Sonnet 4.6*

---

## What Concierge Is

Concierge is a personal AI task orchestration system on a homelab cluster. A five-layer pipeline (Bit → Planner → Router → Foreman → Workbee) accepts human intent, routes it through distributed inference, and returns completed work.

The core principle is **Wide Not Deep**: correctness emerges from structured disagreement across a diverse ensemble of smaller models from genuinely different training lineages. Cross-family agreement is the correctness signal. Cross-family disagreement surfaces uncertainty. **Same-family validation is explicitly forbidden** — a Llama fine-tune does not add quorum breadth if another Llama derivative is already present.

---

## Two Separate Problems

Treat these independently.

---

## Problem 1 — Ensemble Fleet (Workbee Nodes)

### Hardware
Four 16GB VRAM inference islands:
- Daemon Island 1: RTX 5060 Ti, GDDR7 — CUDA
- Daemon Island 2: Tesla P100, HBM2 — CUDA
- Daemon Island 3: Tesla P100, HBM2 — CUDA
- Kratos: RX 7800 XT, GDDR6 — **ROCm**

One resident specialist model per island. Four models total. Four genuinely distinct families.

### The family diversity requirement
Training lineage diversity — not just architectural diversity. A Llama fine-tune counts as Llama regardless of what it was fine-tuned for. The ensemble needs models that fail differently from each other: different pretraining corpora, different RLHF lineages, different architectural priors.

Target family pool: Meta Llama, Alibaba Qwen, Mistral, DeepSeek, Microsoft Phi, Google Gemma, Cohere Command R. Pick four with maximum divergence.

### Requirements per model
- **13B Q4_K_M** — fits in 16GB with KV cache headroom. This is the target size.
- **GGUF format**, runnable via llama.cpp or Ollama
- **Instruct variant only** — base models not useful here
- **ROCm compatibility** — Kratos runs ROCm via llama.cpp. Flag any model with known ROCm issues.
- Behavioral reliability matters more than benchmark scores — strong instruction following, low hallucination rate

### High Table verifier (separate from the ensemble)
The dual P100 shard (32GB combined HBM2) runs a single larger model for verification tasks. Target: **34B Q4_K_M** (~20GB, fits within 32GB with headroom). Recommend one candidate. Does not need to be from a family absent from the ensemble — this is a verifier, not a quorum voice.

### What to deliver
Five models total:
1. Four ensemble candidates — one per family slot, with rationale for family choice and specific model selection
2. One High Table verifier at ~34B

For each: confirm GGUF availability, note known behavioral quirks or quality concerns, flag ROCm uncertainty where applicable.

**Be specific and opinionated.** If you have strong views on which models best fill these slots, say so and explain why. A reasoned recommendation with stated uncertainty is more useful than a hedged non-answer. A parallel Gemini instance is doing live web research on current availability — your job is analytical depth on the selection criteria and tradeoffs.

---

## Problem 2 — Bit's Model on Logos

### Hardware
MacBook Pro M1 Max. 64GB unified memory. 24-core GPU, 16-core Neural Engine. **MLX is the primary inference backend.** GGUF via Ollama is a viable fallback.

### Role
Logos runs Bit — the human-facing application layer. This model handles all direct human dialogue: conversation, intent drafting, clarifying questions, reasoning, and disconnected-mode operation. It is **not** an ensemble member and does not pull work from the cluster. Its inference capacity is reserved entirely for the human interaction layer.

**Quality of human interaction is the primary selection criterion.** The memory budget is not a meaningful constraint at 64GB — virtually anything below ~45B Q4 fits comfortably. The question is purely: what model best serves the human in conversation?

### Performance reference on M1 Max (MLX, ~400 GB/s bandwidth)
- 13B Q4: ~20–28 t/s
- 30B Q4: ~10–14 t/s
- 34B Q4: ~8–10 t/s — still interactive

### Requirements
- Exceptional conversational quality — this is the human's primary AI interface
- Strong reasoning and planning for disconnected-mode use
- Excellent instruction following, long context handling (16K+ preferred)
- **MLX format must be available**, or GGUF via Ollama as fallback — confirm for any recommendation
- Does not need to be from a family distinct from the ensemble

### Target size
**27B–34B Q4_K_M** is the sweet spot given this hardware. A 7B is undersized for 64GB unified memory and this role. A 13B is acceptable if it genuinely outperforms larger models conversationally, but that would be surprising.

### What to deliver
- Top 2–3 candidates ranked by conversational and reasoning quality
- One clear recommendation with rationale
- MLX availability confirmed for each
- Note if the recommended model also fits an ensemble slot (useful context, not a requirement)