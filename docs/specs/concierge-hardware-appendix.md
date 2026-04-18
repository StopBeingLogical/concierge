---
title: "Concierge — Hardware Reference Appendix"
document_type: reference
version: "5.0"
date: "2026-03"
status: current
tags: ['hardware', 'fleet', 'inference', 'gpu', 'npu', 'acquisition']
---

# Concierge: Hardware Reference Appendix

*Reference material for node acquisition and routing decisions. The tier classifications and specific hardware entries will go stale as the market evolves. The principles behind them will not.*

*Companion to: Concierge: Architecture, Philosophy, and the Ballet Beneath (v4)*

---

## Acquisition Principles

Before the taxonomy, the principles that generated it. These are durable regardless of which specific chips are current.

**Speed < Capacity for general inference nodes.** Token generation is memory-bandwidth-bound, not compute-bound. A node that can hold a 32B model resident and serve it at 8 t/s contributes more to the ensemble than a node that screams through a 7B at 30 t/s but can't touch anything larger. The Router fills the schedule — slow nodes get assigned latency-tolerant P2/P3 work and are never idle. They just get appropriately matched work chunks.

**iGPU + RAM over dGPU for ensemble members.** Unified memory means every GB is addressable for model weight residency with no separate VRAM ceiling. A dGPU node has two separate pools — system RAM for orchestration, VRAM for inference — and VRAM is almost always the binding constraint. An iGPU node with 96GB has 96GB of inference-addressable memory. A dGPU node with 32GB system RAM and 16GB VRAM has 16GB of inference-addressable memory for the model.

**dGPU nodes are specialist nodes.** High VRAM, high bandwidth, high speed — these are verifier nodes and P1 interactive hot path nodes. Speed is the metric here because these are the hot path. iGPU nodes are the ensemble breadth. dGPU nodes are the ensemble depth and validation tier.

**NPU is secondary and additive.** Ollama and llama.cpp don't use NPUs for LLM inference on x86 today. For Concierge specifically, the NPU is addressable via OpenVINO (Intel), ONNX/XRT (AMD), RKLLM (Rockchip), and CoreML (Apple). The NPU contribution is: Pathfinder role (intent classification, embedding generation, routing pre-computation) and local async speculative decoding drafter. Both are available at any TOPS level — even vestigial NPUs clear the break-even threshold for local spec-dec at near-zero marginal power cost.

**Buy pre-configured RAM during a RAM crisis.** The DRAM market is subject to severe pricing disruptions driven by AI hyperscaler demand. When DDR5 SO-DIMM kits are at 3-5x their baseline price, sourcing RAM separately from a bare-bones node is often more expensive than buying a pre-configured system that includes RAM at OEM pricing. Check the delta before assuming the bare-bones option is cheaper.

**RonCo onboarding.** Nodes are black boxes. The onboarding package self-surveys the hardware, pulls precompiled tooling matched to the detected capability envelope, and advertises that envelope to the Router. The operator sets it up once and forgets it. The node's internal implementation is its own business. The Router sees a contract. The Workbee fulfills it.

---

## Node Tier Taxonomy

Nodes are classified by iGPU inference capability and NPU presence. Within each tier, RAM capacity determines the practical inference ceiling more than any other single factor.

### Tier 1 — Strong NPU + Capable iGPU (≥12 CU / ≥8 Xe2)

The premium inference node tier. Full Pathfinder capability plus strong iGPU inference. AMD XDNA 2 specifically has hardware primitives for KV-cache streaming that make it the most architecturally interesting NPU for transformer workloads — prefill acceleration, attention mechanism optimization, and hybrid NPU+iGPU execution where the NPU handles the compute-intensive prefill phase and the iGPU handles the memory-intensive decode phase.

Representative chips: AMD Ryzen AI Max+ 395 / Max 390 (Strix Halo, 40 CU RDNA 3.5, ~215 GB/s, 50 TOPS XDNA 2, up to 128GB), AMD Ryzen AI 9 HX 370 / AI 7 350 (Strix Point, 16 CU Radeon 890M, ~102 GB/s, 50 TOPS XDNA 2, up to 96GB), Intel Core Ultra 9 285H / 7 255H (Arrow Lake-H, 8×Xe2 Arc 140T, 13 TOPS NPU 3, up to 96GB), Intel Core Ultra 9 288V (Lunar Lake, 8×Xe2 Arc 140V, 48 TOPS NPU 4, 32GB max on-package).

**Routing notes:** Tier 1 nodes are the natural home for the largest resident specialist models and for the highest-quality inference workloads. The Strix Halo variants (395/390) are in a class of their own for memory capacity — 128GB unified memory makes them viable for models that no other consumer tier can run. Lunar Lake (200V) has the strongest NPU of any Intel mobile platform but the 32GB on-package RAM ceiling is a hard constraint that limits resident model fleet size.

### Tier 2 — Weak/Vestigial NPU + Capable iGPU

The bread-and-butter inference node. The 780M RDNA 3 iGPU in this tier delivers 10-15 t/s on 7B Q4 models, comfortable with 13B, and is the most common iGPU in mini PCs in the $300-600 range. The XDNA NPU at 16 TOPS is below the threshold for serious hybrid prefill acceleration but still useful for Pathfinder classification tasks and local async spec-dec.

Representative chips: AMD Ryzen 9 7940HS / 7 7840HS (Phoenix, 12 CU Radeon 780M, ~88 GB/s DDR5, 16 TOPS XDNA), AMD Ryzen 9 8945HS / 7 8845HS (Hawk Point, 12 CU Radeon 780M, 16 TOPS XDNA v2), AMD Ryzen AI 5 340 (Hawk Point refresh, 12 CU Radeon 780M, 16 TOPS).

**Routing notes:** These nodes are the workhorse inference tier. The 7840HS and 8845HS are architecturally identical for inference purposes — same 12 CU 780M, same DDR5 bandwidth ceiling. The NPU delta between them (XDNA vs XDNA v2) is minor for Concierge workloads. Max RAM config (96GB on some platforms) is significantly more valuable than the NPU generation difference.

**Special case — AMD Ryzen 7 255:** China-market Hawk Point chip with NPU disabled at the hardware level (lower-quality die). Architecturally identical iGPU to the 8845HS. Since Ollama doesn't use the NPU for inference anyway, this chip delivers Tier 2 iGPU inference capability at reduced price. The NPU absence eliminates the Pathfinder bonus and local async spec-dec option. Worth acquiring pre-configured with maximum RAM when available at a discount over equivalent 8845HS systems.

### Tier 3 — NPU Present + Framebuffer-Class iGPU

NPU is present but iGPU is limited. The primary value of these nodes is CPU throughput for orchestration work and NPU availability for Pathfinder/classification tasks. Not primary inference nodes.

Representative chips: Intel Core Ultra 9 285HX / 7 255HX (Arrow Lake-HX, 4×Xe-LPG framebuffer iGPU, 13 TOPS NPU, up to 192GB — strong CPU core count for Router/Foreman duty), AMD Ryzen 7 8700G / 5 8600G (Phoenix desktop, 12 CU Radeon 760M RDNA3, 16 TOPS XDNA, up to 192GB DDR5 — large RAM ceiling is the standout feature for embedding/batch node duty).

**Routing notes:** Arrow Lake-HX nodes are better understood as control plane nodes than inference nodes. 24 CPU cores, up to 192GB RAM, vestigial iGPU — this is Ergaster territory. Assign Router, Foreman, and Planner work here. The Ryzen 8700G desktop APU is interesting specifically for the 192GB RAM ceiling with a usable RDNA3 iGPU — it can hold a large embedding model fleet in RAM even if token generation speed is modest.

### Tier 4 — No NPU + Capable iGPU

Solid inference nodes with no Pathfinder bonus. The iGPU does inference work. The CPU does whatever the CPU does. No local async spec-dec available.

Representative chips: AMD Ryzen 9 7940HX / 7845HX (Dragon Range, 12 CU Radeon 680M RDNA2, no NPU), AMD Ryzen 5 5600H / 7 5800H (Cezanne Zen 3, 8 CU Vega RDNA1, no NPU — very common in used hardware), Intel Core i7-1185G7 / i5-1135G7 (Tiger Lake, 96EU Xe iGPU, ~68 GB/s, no NPU — Noesis class), Intel Core i9-13900HX / i7-13700H (Raptor Lake-HX, 32EU Iris Xe framebuffer, no NPU — Ergaster class, best used as control plane).

**Routing notes:** Noesis (i7-1185G7, 32GB LPDDR4x) is the reference example for this tier in the existing fleet. AVX-512 support on Tiger Lake gives CPU inference a slight edge. The Xe iGPU at ~68 GB/s is viable for 3B embedding models and Pathfinder-class classification tasks running on CPU+iGPU. Best assigned: always-on background embedding generation, intent routing, corpus annotation passes.

### Tier 5 — ARM Non-Apple (SBC / Edge)

Edge nodes with real NPU silicon but fundamentally different software ecosystems. The inference toolchain (RKLLM, CoreML equivalents) is separate from Ollama/llama.cpp and requires model conversion. These are legitimate cluster members for fixed-function workloads.

**Rockchip RK3588:** 6 TOPS NPU (3-core), Mali-G610 MP4 GPU, up to 32GB, 10-15 t/s on 1.1B via RKLLM, ~5-6W under AI load, ~$180. The NPU only supports W8A8 quantization — not W4A16 which most modern llama.cpp targeting uses. Requires RKLLM model conversion. Best assigned: always-on Pathfinder classification, embedding generation for small models, intent routing relay.

**Raspberry Pi 5 (8GB):** No NPU, VideoCore VII GPU, CPU-only inference, 8-12 t/s on 1-3B models, 4W idle, ~$80. Coordinator and relay node only. With the AI HAT+ 2 ($130, Hailo-10H, 8GB on-board LPDDR4): adds 1.5B LLM inference via Hailo-Ollama REST API at ~6-7 t/s, but the Pi 5's own CPU matches or beats this for most models. The HAT+ 2's value is in freeing Pi system RAM for other tasks and enabling simultaneous vision+LLM in power-constrained deployments.

**CIX CP8180 (Minisforum MS-R1):** 12-core ARMv9.2-A, 28.8 TOPS NPU, Immortalis-G720 MC10 GPU, up to 64GB LPDDR5 ECC, dual 10GbE, PCIe x16 (x8 electrical). Interesting hardware profile undermined by immature ecosystem — requires official OS image, driver merging still in progress as of early 2026. Watch-and-revisit in 12-18 months.

---

## NPU Architecture Reference

NPU silicon varies significantly in architectural design, on-chip memory, and optimal workload types. TOPS is the least useful comparison metric. The following characterizations inform Router workload assignment by NPU class.

### AMD XDNA / XDNA 2

**Architecture:** 2D grid of compute tiles, memory tiles, and shim tiles. XDNA 2 (Strix Point) has 12 independent compute clusters, each with four 256-bit wide vector ALU lanes, 512-bit ring interconnect, 4MB shared weight SRAM, 128KB scratchpad per compute core, 8MB L2-style buffer. On-chip SRAM achieves ~800 GB/s bandwidth vs ~120 GB/s off-chip LPDDR5.

**Key architectural property:** Hardware primitives for softmax, layer norm, and KV-cache streaming engines for transformers. KV-cache streaming is a silicon-level feature, not a software optimization. The prefill phase (compute-intensive) runs on the NPU; the decode phase (memory-intensive) runs on the iGPU. AMD's OGA hybrid mode orchestrates this split automatically.

**Best for:** Transformer prefill acceleration, KV-cache management, hybrid NPU+iGPU execution, anything that benefits from low-latency on-chip weight residency. The most architecturally interesting NPU for Concierge's Pathfinder and prefill roles.

**Toolchain:** Linux kernel driver mainlined (amdxdna). ONNX Runtime with XRT backend. AMD Quark for quantization. Open-source path functional but fragmented — firmware compatibility issues between kernel versions documented.

### Intel NPU 3 (Arrow Lake / Meteor Lake)

**Architecture:** Simple fixed-function accelerator, ~13 TOPS INT8. Same generation as Meteor Lake. Primarily targets Windows Studio Effects workloads (background blur, eye contact, transcription). No published detailed architectural documentation comparable to XDNA.

**Key architectural property:** Functional but limited. No KV-cache streaming primitives. No hybrid execution framework comparable to AMD OGA. Addressable via OpenVINO on Linux for fixed-function classification and embedding tasks.

**Best for:** Pathfinder classification tasks via OpenVINO. Local async spec-dec drafter loading small fixed models. Not useful for dynamic transformer workloads.

**Toolchain:** OpenVINO on Linux. Mature toolchain, good documentation. The most practically accessible NPU toolchain for non-Windows deployment.

### Intel NPU 4 (Lunar Lake)

**Architecture:** Two parallel NPUs, each with its own independent inference pipeline and multiply-accumulate array. 48 TOPS INT8. On-package LPDDR5X-8533 memory at 32GB max.

**Key architectural property:** Dual independent pipelines enable concurrent execution of two separate models without contention. Run a Whisper model and a small LLM simultaneously without either blocking the other. This is the standout architectural differentiation of NPU 4.

**Best for:** Dual concurrent model execution — simultaneous speech-to-text and intent classification, or vision pipeline plus routing model. The 32GB on-package RAM ceiling limits resident model fleet size but the NPU architecture compensates for mixed workloads.

**Toolchain:** OpenVINO on Linux. Same toolchain as NPU 3, better hardware.

### Hailo-8

**Architecture:** Pure on-chip SRAM, no external DRAM interface. All model weights, activations, and intermediate results live on-chip. Proprietary dataflow design — compute, memory, and control blocks distributed across the die, allocated to specific neural network layers at compile time. Models are essentially burned into the dataflow graph at compile time.

**Key architectural property:** Elimination of DRAM round-trips entirely. For vision workloads that fit on-chip, latency is extraordinarily low and deterministic. For anything that doesn't fit on-chip, it literally cannot run — hard capability ceiling determined by on-chip SRAM capacity.

**Best for:** Fixed-function always-on vision tasks — object detection, pose estimation, scene segmentation, face recognition — running 24/7 at near-zero power. The best available option for this specific workload profile. Not suitable for LLMs. Not suitable for dynamic model loading.

**Toolchain:** Hailo Dataflow Compiler for model conversion. Models compile once, run deterministically. Mature toolchain for vision workloads, limited for generative AI.

### Hailo-10H

**Architecture:** Same proprietary dataflow design as Hailo-8 but adds external DRAM interface — 4GB or 8GB LPDDR4 on-module. Compile-time allocation still applies. 2048-token KV-cache context window is a hard architectural limit. Supports W4A8 quantization maintaining near-FP16 accuracy for small language models.

**Key architectural property:** The compile-time dataflow allocation means the Hailo-10H is excellent for fixed, known-in-advance deployments and poor for dynamic model loading or experimental workloads. Deploy a 1.5B intent classifier once, run it forever — ideal. Hot-swap models based on Router assignment — not supported.

**LLM performance reality:** The Hailo-10H is slower than the Raspberry Pi 5's own CPU for LLM token generation in most tested configurations. The Pi CPU runs at 10W; the Hailo is power-capped at 3W. The 8GB on-board RAM frees Pi system RAM for other work, which is the primary practical benefit. The HAT+ 2 is the S3 ViRGE of the NPU world for LLM workloads — technically a generative AI accelerator, slower than what you already had. For vision tasks it remains solid.

**Best for:** Fixed small LLM pipelines where the model is known at deploy time and never changes. Simultaneous vision + small LLM in power-constrained deployments (the mixed-mode use case). Not suited for dynamic Concierge workloads where the Router assigns different models based on capability envelope.

### Rockchip RK3588 NPU

**Architecture:** Three-core NPU, 6 TOPS. Supports INT8, INT16, FP16 natively. Only supports W8A8 quantization for LLM inference — not W4A16 which most modern llama.cpp quantization targets, meaning larger model footprint at equivalent parameter count. RKLLM is the inference stack, separate from Ollama/llama.cpp and requiring model conversion.

**Best for:** Always-on 1B-class model inference for Pathfinder tasks at ~5W total system power. Best power efficiency per inference operation of any option at this price point (~$180). Not suitable for models above ~1.1B parameters at usable speeds.

---

## Fleet Acquisition Priority Stack

For adding nodes to the Concierge cluster, in priority order:

**1. RAM capacity** — more addressable memory means more resident specialists means more quorum voices. This is the primary metric.

**2. iGPU class** — RDNA 3 (780M), RDNA 3.5 (890M/8060S), or Xe2 (Arc 140T/140V). All viable for 7B inference. RDNA 3.5 and Xe2 preferred but not required.

**3. NPU class** — XDNA 2 for maximum architectural benefit. Intel NPU 4 for dual concurrent model execution. Intel NPU 3 or XDNA for Pathfinder-only benefit. None acceptable — still a valid inference node, no Pathfinder bonus.

**4. Connectivity** — 2.5 GbE minimum preferred. Latency matters more than throughput for work chunk delivery. OCuLink or USB4 useful for future dGPU expansion path.

**5. Pre-configured RAM vs bare bones** — during DRAM pricing crises, pre-configured systems often provide better total cost. Verify the delta before sourcing RAM separately.

**Not a priority for general inference nodes:** Raw token speed, peak TOPS, marketing AI PC certifications, NPU TOPS count.

**dGPU nodes are acquired separately** when the Router identifies queue pressure that requires faster verification or hot-path P1 throughput. The telemetry surfaces this — add dGPU capacity when 7B queue depth and P1 latency metrics indicate the iGPU ensemble is the bottleneck, not before.

---

## Sovereign Node Window Shopping — What It Was For

A period of investigation into whether Concierge could run on a single high-capability node (Strix Halo, Framework Desktop Mainboard, Beelink GTi15 Ultra) rather than a distributed fleet.

The conclusion: the distributed fleet was always the correct architecture. The sovereign node investigation was useful because it established concrete reference points for what a high-end node looks like — specifically the Strix Halo as the reference tier for unified memory inference — which clarifies reasoning about the rest of the spectrum. The Corsair AI Workstation 300 (Ryzen AI Max+ 395, 128GB) and Framework Desktop Mainboard (same chip, $2,459+ in current RAM market) are useful benchmarks. They are not the target.

The fleet is already there. The hardware already owned is the cluster. The investigation confirmed that the distributed approach is philosophically correct and practically superior for the actual workload profile — diverse specialist ensemble rather than single large model capacity.

---

## Current Fleet Baseline

*Companion to: Concierge: Architecture, Philosophy, and the Ballet Beneath (v5)*

The following characterizes the existing fleet as a Concierge cluster — quorum voice count, High Table ceiling, control plane capacity, and known topology constraints. This is the baseline from which all future acquisition decisions are measured.

### Daemon — Pure AI Processor

Three heterogeneous GPU islands on a single headless node. The islands are genuinely asymmetric in PCIe topology, which has specific routing implications.

**Island 1 — RTX 5060 Ti (PCIe 3.0 x16)**
16GB GDDR7, ~448 GB/s internal bandwidth. PCIe 3.0 x16 = ~16 GB/s bidirectional to system RAM — fastest external link on Daemon. Primary role: fast verifier, P1 interactive hot path, primary shard anchor in burst mode. Aggressive model rotation acceptable — fastest load of the three islands at ~1s for a 13B Q4.

**Island 2 — Tesla P100 #1 (PCIe 3.0 x8)**
16GB HBM2, ~732 GB/s internal bandwidth. PCIe 3.0 x8 = approximately 8 GB/s bidirectional to system RAM. Model load for a 13B Q4 (~8GB) takes approximately 1 second. Role: capacity inference, sustained token generation on large models, High Table verification candidate, primary P100 shard leg.

**Island 3 — Tesla P100 #2 (PCIe 3.0 x4)**
16GB HBM2, ~732 GB/s internal bandwidth. PCIe 3.0 x4 = approximately 4 GB/s bidirectional to system RAM — half the bandwidth of Island 2 for model loading. Model load for a 13B Q4 takes approximately 2 seconds. Role: same as Island 2, but Router should prefer stable long-resident model assignments to minimize swap frequency. Inter-P100 all-reduce during shard operation is bounded by the slower of the two slots — effectively ~4 GB/s for synchronization traffic.

**Daemon topology note:** All three cards connect to the same PCIe root complex on the i7-12700F. The PCIe bandwidth asymmetry between islands affects model swap window duration and inter-card shard synchronization, not sustained inference throughput. Once a model is resident, HBM2 bandwidth dominates and both P100 islands perform equivalently for token generation. Inter-P100 all-reduce during dual-shard operation adds approximately 0.2ms synchronization overhead per token across 60 layers — real but not a wall. The Router's predictive flush logic should weight Island 3 toward stability — assign workloads likely to remain needed for extended periods rather than rotating aggressively. Model swaps happen during scheduled drain-and-reload maintenance windows: degrade node, swap model, promote back. At these bus speeds, a maintenance window is under ten seconds for any realistic model size.

**Daemon system RAM:** 32GB DDR5. Router and Foreman CPU processes are pinned to the i7-12700F performance cores. System RAM is not used for inference — the GPU islands are the inference substrate.

### Kratos — Mid-Tier Inference

RX 7800 XT 16GB GDDR6, ~576 GB/s. Ryzen 7600X, 32GB system RAM. ROCm backend. One additional inference island — 1-2 quorum voices at 7B-13B depending on resident model configuration.

### Ergaster — Control Plane

i9-13900HX, 64GB DDR5. 24 cores, 32 threads. Iris Xe framebuffer iGPU — not useful for inference. This is the Router and Foreman node. CPU performance cores handle scheduling, prediction, and orchestration. No inference contribution.

### Noesis — Lower Tier

i7-1185G7, 32GB LPDDR4x. Tiger Lake Xe iGPU at ~68 GB/s. 13 TOPS GNA — OpenVINO only, no transformer hardware primitives. Pathfinder classification via OpenVINO is viable but limited. CPU inference viable for models up to approximately 3B. AVX-512 present, slight CPU inference advantage. Role: always-on background corpus annotation, light embedding generation, intent routing relay.

### Ephemera ×2 — Edge Nodes

Two MacBook Air M2, 8GB unified memory each. Approximately 6GB usable after OS overhead. MLX backend, Apple Neural Engine available. Memory constraint limits to 3B-7B Q4 models — tight on 7B. Primary role: Pathfinder classification and embedding duty via ANE, small model inference for non-latency-sensitive background tasks. Two units does not materially change the voice count — each contributes one small-model voice at best.

---

### Fleet Quorum Voice Count

Under the Wide Not Deep principle, quorum voices = simultaneously resident specialist models from genuinely different training lineages across the fleet.

At Q4_K_M quantization, conservative sizing:
- 7B model: ~5GB VRAM
- 13B model: ~9GB VRAM
- 30B model: ~20GB VRAM

| Island | VRAM | Practical Resident Config | Quorum Voices |
|---|---|---|---|
| Daemon 5060 Ti | 16GB | One 13B, or two 7B | 1-2 |
| Daemon P100 #1 | 16GB | One 13B, or two 7B | 1-2 |
| Daemon P100 #2 | 16GB | One 13B, or two 7B | 1-2 |
| Kratos 7800 XT | 16GB | One 13B, or two 7B | 1-2 |
| Noesis Xe iGPU | ~4GB usable | Small model only | 0-1 |
| Ephemera ×2 ANE | ~6GB each | 3B-7B only | 0-1 each |

**Total quorum voices at baseline: 4-8 depending on model size mix.**

The practical operating configuration is five — one 13B per island on the four dGPU nodes, each from a genuinely different model family: Llama, Qwen, Mistral, DeepSeek, Phi or Gemma. Five voices across five families with cross-family quorum is a real immune system. This is not a toy setup.

---

### High Table Ceiling — Temporary Sharding

The Router maintains a shard candidate pool calculation for tasks that exceed single-island VRAM. Before returning `capability_exceeded`, the Router attempts temporary sharding.

**Interactive High Table ceiling (P1 viable) — Dual P100 shard:**

Islands 2 and 3 combined — 32GB HBM2, fits a 34B model at Q4. Inter-island all-reduce is PCIe bus internal to Daemon, bounded by the x4 slot (~4 GB/s). Shard load is asymmetric: Island 2 loads via x8 (~8 GB/s), Island 3 loads via x4 (~4 GB/s). Total shard load time for a 34B model approximately 5–8 seconds during the maintenance window. Once resident, HBM2 bandwidth dominates — synchronization overhead adds ~12ms total per token across all layers, which is real but not a wall. This is the practical interactive High Table ceiling — fast enough for P1 SLA, correct for tasks up to 34B. Island 1 (5060 Ti) remains available for independent P1 work during dual P100 shard operation.

**Extended ceiling — Burst mode (all three cards):**

All three islands combined — 48GB total VRAM, fits 34B–65B Q4. Island 1 (5060 Ti, x16) is the shard anchor; Islands 2 and 3 extend its reach. Recommended tensor split: 60/20/20 (weighted toward 5060 Ti to minimize time spent waiting on the x4 leg). Activation sequence: Router pre-flight determines job exceeds Island 2+3 ceiling; Router drains in-flight jobs on all islands; Router suspends all three islands' independent availability contracts; shard coordinator activates across all three cards; job executes; Router restores independent island operation on completion. Viable for P1 and P2. Island 1 is not available for independent work during burst.

**Batch High Table ceiling (P2/P3 only) — Cross-node shard:**

Full cluster shard across Daemon and Kratos — 48GB + 16GB = 64GB total VRAM across the 2.5GbE network link. Cross-node latency makes this viable only for P2/P3 background tasks. Not viable for P1 interactive work. Practical ceiling approximately 65B at Q4.

**Above 65B:** `capability_exceeded` is the honest response until fleet expansion adds higher-VRAM nodes. The Mac Studio M4/M5 Max at 128GB unified memory is the natural High Table ceiling raiser when acquired.

**The unified slowness principle:** Larger models are always slower regardless of hardware — token generation is memory-bandwidth-bound, and parameter count is the numerator. PCIe all-reduce overhead is not a special penalty on top of this; it is another term in the same equation. When evaluating whether to trigger burst mode, the Router does not ask "will this be slower." It will always be slower than a smaller model on a faster card. The Router asks whether the intelligence delta from the larger model justifies the latency cost for this specific job's SLA. That is a clean, single decision boundary.

---

### dGPU vs Unified Memory — Cluster Contribution Analysis

When adding nodes to an existing cluster, the question of whether to add a large VRAM dGPU or an equivalent-cost unified memory device has a clear Concierge answer.

**A dGPU adds one fast verifier voice.** A B70 at $949 contributes one High Table verifier island — fast, high bandwidth, high VRAM. It raises the interactive High Table ceiling. It does not add quorum breadth.

**A unified memory device adds two to four ensemble voices.** A MACO 8845 at $599 with 32GB contributes two to three resident 7B-13B specialists simultaneously. At 64GB after RAM upgrade it contributes four. Each is a distinct quorum voice from a different model family. The ensemble's immune system gets stronger. NIDABA gets more diverse retrieval signals. The anti-echo-chamber architecture functions as designed.

**The correct acquisition sequence under Concierge philosophy:**

Build quorum breadth first. The current fleet has 4-8 voices — adequate but thin for confident cross-family quorum. The next two to three acquisitions should be ensemble breadth nodes (MACO class) to reach a robust 8-12 voice quorum. Only after the quorum is robust does the dGPU verifier become the right next acquisition — and the Router's telemetry will surface that signal when it's true.

Do not buy ahead of the Router's signal.

---

### Reference Value Node — MACO 8845

The Aoostar MACO 8845 is the reference Tier S acquisition as of March 2026.

**Why it holds the top position:**

- AMD Ryzen 7 PRO 8845HS — PRO variant with AMD Memory Guard encryption, DASH manageability, longer platform longevity
- 12 CU Radeon 780M RDNA3 — solid Tier 2 iGPU inference
- 16 TOPS XDNA v2 — Pathfinder duty and local async spec-dec
- 2×DDR5 SO-DIMM, max 128GB — highest upgrade ceiling in the Tier 2 class
- OCuLink — native PCIe x4, best dGPU expansion path available
- Dual USB4 — flexible secondary expansion
- Dual 2.5GbE Intel I226V — traffic separation between Router work chunks and artifact egress, unique in sub-$700 tier
- $599 for 32GB+1TB from US warehouse, $349 barebones

**In cluster configuration:** The dual 2.5GbE is the standout. One NIC carries Router traffic and work chunk delivery. The other carries Atlas synchronization and NIDABA index updates. These are genuinely different traffic patterns and separating them removes artifact egress competition from interactive SLA latency. No other sub-$700 machine in the survey has this.

**In sovereign node configuration:** Viable at 64GB after RAM upgrade with OCuLink B70 attached. At 32GB the quorum is thin — two voices is below the minimum meaningful ensemble. The sovereign node story becomes compelling at 64GB plus a dGPU verifier.

**The PRO chip advantage for a continuously running cluster node:** AMD Memory Guard means all inference work is encrypted in transit through unified memory. DASH manageability means the node can be administered out-of-band. The PRO platform longevity commitment matters when acquiring multiples of the same node over time — the platform stays available.

---

### Fleet Expansion Research — dGPU Verifier Candidates (April 2026)

Captured as research context. Not a pending acquisition decision. Value matrix not yet completed — deferred to dedicated session.

**Intel Arc Pro B70** (launched March 25, 2026)
32 Xe2 cores, 256 XMX engines, 367 INT8 TOPS. 32GB GDDR6, 256-bit bus, 608 GB/s. TDP: 230W reference, 160–290W AIB range. Price: ~$949. Software: OpenVINO/oneAPI — GGUF Q4 via Vulkan/IPEX-LLM works; FP8/INT4 via Intel LLM Scaler vLLM fork (Docker, Ubuntu 25.04); pre-quantized AWQ broken (CUDA codepath issue). Fleet role if acquired: one fast verifier island, raises interactive High Table ceiling. Does not add quorum breadth.

**AMD Radeon AI PRO R9700** (launched October 2025)
Full Navi 48 die, 64 CU RDNA4, 128 AI accelerators. 1,531 INT4 TOPS — approximately 4× the B70's INT8 TOPS on comparable workloads. 32GB GDDR6, 256-bit bus, ~640 GB/s. TDP: 300W. Price: ~$1,299. Software: ROCm 7.0.2 — mature, first-class vLLM/llama.cpp support, native INT4/FP8/AWQ/GPTQ, no vendor fork required. Fleet role if acquired: same as B70 but stronger inference throughput and zero toolchain friction. $350 premium per card.

**Acquisition note:** Both cards raise the interactive High Table ceiling but add only one verifier voice each — they do not address quorum breadth. Under current fleet philosophy, ensemble breadth nodes (MACO class) remain the higher-priority acquisition until the Router's telemetry signals verifier bottleneck. Do not buy ahead of the signal.

---

*This appendix documents hardware decisions and reference taxonomy as of early 2026. Specific chip recommendations will age. The tier structure, acquisition principles, and fleet baseline will not.*

*Last updated: April 2026 — v5 (Daemon PCIe topology corrected; burst mode architecture added; fleet expansion research notes added)*
