# Concierge — Model Fleet Context Brief
*Feed this to any chat doing model research, audition, or selection work for the Concierge project.*

---

## What Concierge Is

Concierge is a personal AI task orchestration system running on a homelab cluster. It accepts human intent through a front-end application (called Bit), routes it through a five-layer AI pipeline, and returns completed work. The human interacts only with Bit. Everything below Bit is automated.

The system is designed around one core principle: **Wide Not Deep.** Intelligence emerges from structured disagreement across a diverse ensemble of smaller, specialized models — each from a different training lineage — rather than from a single large model. Agreement across diverse models is a stronger correctness signal than confidence from any one model.

---

## The Fleet Model

The cluster runs distributed inference across heterogeneous hardware. Models are assigned to GPU islands based on their capability envelopes. There are three roles in the fleet:

**Ensemble (quorum) voices** — specialist models, each from a genuinely different model family (Llama, Qwen, Mistral, DeepSeek, Phi, Gemma, etc.). These run simultaneously on separate islands and their outputs are validated against each other. Cross-family disagreement surfaces uncertainty; cross-family agreement is the correctness signal. *Same-family validation is forbidden — it defeats the purpose.*

**High Table verifiers** — higher-parameter models used for verification and complex reasoning tasks that exceed the ensemble's ceiling. These run on sharded GPU configurations when needed.

**Bit's local model** — a separate role, described in detail below.

### Current Hardware

| Node | Hardware | Memory | Cluster Role |
|---|---|---|---|
| Logos | M1 Max, 24-core GPU, 16-core ANE | 64GB unified | Bit host — not a Workbee |
| Ergaster | i9-13900HX, Iris Xe (vestigial) | 64GB DDR5 | Router / Planner host — not a Workbee |
| Daemon Island 1 | RTX 5060 Ti | 16 GB GDDR7 | P1 hot path verifier |
| Daemon Island 2 | Tesla P100 #1 | 16 GB HBM2 | Ensemble / High Table |
| Daemon Island 3 | Tesla P100 #2 | 16 GB HBM2 | Ensemble / High Table |
| Kratos | RX 7800 XT | 16 GB GDDR6 | Ensemble |
| Dual P100 shard | Daemon Islands 2+3 | 32 GB combined | 34B High Table ceiling |
| Burst mode | All three Daemon cards | 48 GB combined | 65B ceiling, P1/P2 only |
| Noesis | i7-1185G7, Tiger Lake Xe | 32GB LPDDR4x | Candidate — background/embedding |
| Ephemera ×2 | MacBook Air M2, ANE | 8GB unified each | Candidate — small model / Pathfinder |

Each 16 GB island runs **one 13B Q4 specialist** as its resident voice. The practical operating configuration is four to five simultaneous 13B models, each from a different family, forming the quorum ensemble.

### What the Fleet Needs from Models

- **Genuine family diversity** — models must come from different training lineages, not just different sizes of the same base. Llama-based fine-tunes do not add quorum breadth if another Llama model is already in the ensemble.
- **13B Q4_K_M** is the sweet spot for 16 GB islands — fits comfortably with KV cache headroom.
- **7B Q4_K_M** as a second resident on any island with remaining headroom after the 13B is loaded.
- **34B Q4_K_M** for the dual P100 shard (High Table use) — approximately 20 GB, fits within 32 GB combined with cache headroom.
- Strong instruction following and low hallucination rate matter more than benchmark scores.
- Models must run via **llama.cpp or Ollama** — these are the Workbee backends. No CUDA-only models.

---

## Bit's Local Model — Specific Requirements

Bit is the human-facing application layer. It runs on **Logos** — a MacBook Pro M1 Max, 64GB unified memory. The inference backend is **MLX** (Apple Silicon native). The Apple Neural Engine (16-core) is also available for classification and embedding tasks.

Logos's local model is not a CPU fallback. It is the primary conversational and reasoning model for the human interaction layer. It runs in disconnected mode when the stack is unavailable, but also handles all direct human dialogue, intent drafting, clarifying questions, and light reasoning regardless of stack state. **Quality of interaction is the primary constraint, not raw speed or memory budget.**

Logos does not participate in the ensemble as a Workbee. Its inference capacity is reserved entirely for Bit. The correct question is not "what can fit" — with 64GB unified memory, almost anything can fit — but "what model best serves the human in conversation."

### Hard constraints
- Must run via **MLX** on Apple Silicon (primary) — GGUF via Ollama also viable as fallback
- Must be available in **MLX format** or **GGUF** (both supported on M1 Max)
- 64GB unified memory — effectively no practical size constraint below ~40B Q4

### Performance profile on M1 Max
- M1 Max memory bandwidth: ~400 GB/s
- 7B Q4: ~35-45 t/s via MLX
- 13B Q4: ~20-28 t/s via MLX
- 30B Q4: ~10-14 t/s via MLX
- 40B Q4: ~7-10 t/s via MLX — still interactive

### Capability requirements
- **Exceptional conversational ability** — this is the human's primary AI interface
- Strong intent drafting and disambiguation — helps refine vague requests into structured intent before they reach the Planner
- Solid reasoning and planning — handles disconnected-mode tasks at acceptable quality
- Long context handling — 16K+ preferred; the human may have extended sessions
- Good instruction following and low hallucination rate

### Model size target
Given the memory budget and MLX performance profile, the sweet spot for Bit's model on Logos is **13B–30B Q4_K_M**. This range gives genuinely capable conversational quality at speeds that feel interactive. Going larger (34B+) is viable if the quality delta is meaningful — the memory is there, and 7-10 t/s is still usable for dialogue.

A 7B model is undersized for this role given what the hardware can do. The human deserves better than a 7B when 30B runs at 12 t/s on the same machine.

### Candidate model sizes in priority order
1. **27B–30B Q4_K_M** — strong reasoning, genuinely good conversation, ~12 t/s — this is the target range
2. **13B–14B Q4_K_M** — fast, capable, good for latency-sensitive dialogue — excellent fallback
3. **34B Q4_K_M** — marginal speed (~8 t/s) but within acceptable interactive range if quality justifies it
4. **7B Q8** — only if a specific 7B significantly outperforms larger models on conversational benchmarks (unlikely)

---

## What Good Looks Like for This Research

A useful output from model audition work for Concierge:

**For the fleet (ensemble voices):**
- Candidate 13B models from genuinely distinct families, with notes on training lineage, instruction quality, and hallucination behavior
- At least one candidate per family slot: Llama-based, Qwen-based, Mistral-based, DeepSeek-based, Phi/Gemma
- GGUF availability confirmed for each

**For Bit's model on Logos:**
- Top 2–3 candidates in the 13B–34B range, ranked by: conversational quality, reasoning ability, instruction following, context handling
- MLX availability confirmed for each (GGUF acceptable as fallback)
- One clear recommendation with rationale — prioritize quality of human interaction over speed
- Note whether the recommended model doubles as an ensemble voice or is a distinct selection for the Bit role

---

*Concierge project — homelab AI orchestration system. For full technical detail, consult the project specification documents.*
