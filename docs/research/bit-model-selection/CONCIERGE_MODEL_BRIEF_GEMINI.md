# Concierge — Model Fleet Brief
*For: Gemini 3 Flash (Pro / Thinking mode)*

---

## What Concierge Is

Concierge is a personal AI task orchestration system on a homelab cluster. A five-layer pipeline (Bit → Planner → Router → Foreman → Workbee) accepts human intent, routes it through distributed inference, and returns completed work.

The core principle is **Wide Not Deep**: correctness emerges from structured disagreement across a diverse ensemble of smaller models from genuinely different training lineages. Cross-family agreement is the correctness signal. Cross-family disagreement surfaces uncertainty. **Same-family validation is explicitly forbidden** — a Llama fine-tune does not add quorum breadth if another Llama derivative is already present.

---

## Two Separate Problems

Treat these independently. **Use your web search and Google Search grounding for both** — current model availability, recent releases, and MLX/GGUF port status are the most important things to verify live.

---

## Problem 1 — Ensemble Fleet (Workbee Nodes)

### Hardware
Four 16GB VRAM inference islands:
- Daemon Island 1: RTX 5060 Ti, GDDR7 — CUDA backend
- Daemon Island 2: Tesla P100, HBM2 — CUDA backend
- Daemon Island 3: Tesla P100, HBM2 — CUDA backend
- Kratos: RX 7800 XT, GDDR6 — **ROCm backend** (llama.cpp ROCm build)

One resident specialist model per island. Four models total. Four genuinely distinct families.

### The family diversity requirement
Training lineage diversity — not just architectural variety. A Llama fine-tune counts as Llama. The ensemble needs models that fail differently: different pretraining corpora, different RLHF lineages, different architectural priors.

Target family pool to draw from: Meta Llama, Alibaba Qwen, Mistral, DeepSeek, Microsoft Phi, Google Gemma, Cohere Command R. Four families with maximum divergence from each other.

### Requirements per model
- **13B Q4_K_M** — fits in 16GB with KV cache headroom. This is the target size.
- **GGUF format**, runnable via llama.cpp or Ollama
- **Instruct variant only** — base models not useful
- **ROCm compatibility required for at least one model** — Kratos runs ROCm. Verify llama.cpp ROCm support for any model assigned to Kratos.
- Behavioral reliability over benchmark scores — strong instruction following, low hallucination rate

### High Table verifier (separate from the ensemble)
The dual P100 shard (32GB combined HBM2) runs a single larger model for verification. Target: **34B Q4_K_M** (~20GB, fits within 32GB). One candidate. Does not need to be from a family absent from the ensemble.

### What to research and deliver

**Search for:**
- Current best-regarded 13B instruct models by family (Llama 3.x, Qwen 2.5, Mistral/Mixtral, DeepSeek, Phi-4, Gemma 3, Command R)
- GGUF availability on HuggingFace (Bartowski and TheBloke/lmstudio-community are the primary GGUF sources)
- Any notable 13B releases in the last 6 months that have strong community reputation
- ROCm compatibility notes for llama.cpp with any recommended models
- Best available 34B Q4_K_M GGUF for the High Table verifier slot

**Deliver:**
1. Four ensemble candidates — one per family, with rationale and GGUF source link if possible
2. One High Table verifier at ~34B with GGUF source
3. Flag any models with known ROCm issues or GGUF quality concerns

---

## Problem 2 — Bit's Model on Logos

### Hardware
MacBook Pro M1 Max. 64GB unified memory. 24-core GPU, 16-core Neural Engine. **MLX is the primary inference backend.** GGUF via Ollama is a viable fallback but MLX is preferred on Apple Silicon.

### Role
Logos runs Bit — the human-facing application layer. This model handles all direct human dialogue: conversation, intent drafting, clarifying questions, reasoning, and disconnected-mode operation when the cluster is unavailable. It is **not** an ensemble member. Its inference capacity is reserved entirely for human interaction.

**Quality of human interaction is the only selection criterion that matters.** At 64GB unified memory, virtually anything below ~45B Q4 fits. Speed is not a constraint — even 34B runs at ~8–10 t/s via MLX on M1 Max, which is interactive.

### Performance reference on M1 Max (MLX)
- 13B Q4: ~20–28 t/s
- 30B Q4: ~10–14 t/s
- 34B Q4: ~8–10 t/s

### Requirements
- Exceptional conversational quality — this is the human's primary AI interface
- Strong reasoning and planning
- Excellent instruction following, 16K+ context preferred
- **MLX port must exist** — check mlx-community on HuggingFace for availability
- GGUF via Ollama is acceptable fallback if MLX port unavailable

### Target size
**27B–34B Q4_K_M.** A 7B is undersized for this hardware. A 13B is acceptable only if it substantially outperforms larger models conversationally, which is uncommon.

### What to research and deliver

**Search for:**
- Current best conversational/instruction-following models in the 27B–34B range
- MLX ports on HuggingFace (mlx-community namespace) for any candidates
- Recent community reputation for conversational quality — Reddit r/LocalLLaMA, HuggingFace discussions
- Any strong 27B–34B releases in the last 6 months

**Deliver:**
- Top 2–3 candidates ranked by conversational quality
- One clear recommendation with rationale
- MLX availability confirmed (with HuggingFace link if possible)
- GGUF fallback source if MLX is unavailable for the top pick

---

## Research Notes

A parallel Claude Sonnet 4.6 instance is working this same brief from its training knowledge. It will provide analytical depth on selection criteria and tradeoffs. Your contribution is **current availability and recent releases** — verify what actually exists on HuggingFace today, what the community is running, and whether recommended models have known issues that have emerged recently. Cross-reference your findings with the Claude instance's recommendations where useful.
