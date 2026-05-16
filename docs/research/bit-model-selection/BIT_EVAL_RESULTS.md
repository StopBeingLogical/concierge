# Concierge Bit Layer — Model Evaluation Results
**Date:** 2026-04-05 17:14:10
**Node:** Logos (M1 Max, 64GB Unified Memory)
**Ollama:** ollama version is 0.20.2
**Context window:** 32,768 tokens

---

## Summary Comparison Matrix

| Model | Family | Conv (30%) | Tool (25%) | Instruct (20%) | Context (15%) | Latency (10%) | **Total** | Verdict |
|-------|--------|-----------|-----------|---------------|--------------|--------------|-----------|---------|
| `qwen2.5:14b` | Qwen | — | — | — | — | 2 (15 t/s) | **None** | pending review |
| `mistral-nemo:12b` | Mistral | — | — | — | — | 3 (25 t/s) | **None** | pending review |
| `qwen2.5:32b` | Qwen | — | — | — | — | 1 (6 t/s) | **None** | pending review |
| `gemma4:26b` | Gemma4 | — | — | — | — | 3 (31 t/s) | **None** | pending review |

---

## Per-Model Results

### `qwen2.5:14b`

**Family:** Qwen  
**Size:** 14B  
**Backend:** llama.cpp/MLX-auto (Q4_K_M)  
**Avg decode:** 15.4 t/s  
**Avg prefill:** 164.6 t/s  
**Thinking token leak:** no  

#### Test 1: Rubber Duck (Conversational Reasoning)

**Score:** None / 5  
**Decode:** 15.4 t/s  
**Prefill:** 164.6 t/s  
**Tokens generated:** 525  

*3 sub-prompts: 1A (Steam/vacuum), 1B (Fiction/timeline), 1C (Concierge/philosophy).*

##### Sub-prompt 1A: Steam Game Recommendation

**Score:** None / 5  
**Decode:** 18.9 t/s  
**Notes:** Docs injected: []. Prompt ~36 tokens.  

<details>
<summary>Full response</summary>

```
Sure, I’d be happy to help you narrow down your options! Here are three questions to get started:

1. What genres or types of games do you enjoy playing the most? For example, do you prefer action, strategy, RPGs, or something else?
2. How important is multiplayer or cooperative gameplay to you? Do you prefer single-player experiences, or do you enjoy playing with friends or other players online?
3. Are there any particular features or mechanics you look for in a game, such as story-driven narratives, open-world exploration, complex puzzles, or fast-paced action?
```

</details>

**Scoring guide:**
5 — Probes completion habits, current mood/headspace, AND something non-obvious (session length, difficulty tolerance, solo vs social, time-of-day patterns). Asks nothing, recommends nothing.
4 — Good questions, all fairly standard genre/preference territory.
3 — Generic (what genre, what have you played before).
2 — Ignores instruction and recommends games anyway.
1 — Off-topic or refuses.

##### Sub-prompt 1B: Fiction Timeline — Next Short Story

**Score:** None / 5  
**Decode:** 19.1 t/s  
**Notes:** Docs injected: ['timeline']. Prompt ~39 tokens.  

<details>
<summary>Full response</summary>

```
Certainly! To help pinpoint the most compelling setting for your fantasy fiction short story, let's start by narrowing down some key aspects. Here are three questions to guide us:

1. **What is the central theme or conflict of your story?** Understanding the core theme or conflict can help identify the period and location in the timeline where such issues are most prevalent or impactful.
2. **Which characters or groups do you want to feature prominently in your story?** Knowing the key players can help determine if there are specific events or locations in the timeline where these characters are most active or influential.
3. **What kind of atmosphere or setting would best enhance the mood and narrative of your story?** Consider the tone and style of your story (e.g., dark and mysterious, light and whimsical, epic and grand) to find a setting that complements these elements.
```

</details>

**Scoring guide:**
5 — Identifies the 0346-0350DE compression (Nageri discovery to Sundering in 4 years), the 0685-0688DE Phineas hunt, or the structural gap between documented events. Question shows it understood the dramatic implication, not just listed dates. Does not suggest a setting.
4 — Notices a specific period but questions are generic (tone, length).
3 — Asks about character or genre without engaging with timeline structure.
2 — Ignores instruction and suggests a setting directly.
1 — Off-topic or refuses.

##### Sub-prompt 1C: Concierge Hardware Node Evaluation

**Score:** None / 5  
**Decode:** 8.1 t/s  
**Notes:** Docs injected: ['philosophy']. Prompt ~6,159 tokens.  

<details>
<summary>Full response</summary>

```
To help you make an informed decision about adding a new inference node to your Concierge cluster, here are three key questions to consider based on the architecture philosophy:

1. **Current Queue Depth and Workload Distribution**: Can you provide details on the current queue depth for general ensemble work and the distribution of tasks across your existing nodes? Specifically, are there any bottlenecks or recurring delays in the processing of general ensemble tasks?

2. **Current Utilization of Existing Nodes**: What is the current utilization rate of your existing ensemble nodes? Are there any nodes that are consistently underutilized or nodes that are frequently at full capacity? Understanding the current state of your nodes will help determine if the addition of a new node will be beneficial.

3. **Recent Performance Metrics**: Have you observed any specific performance metrics (e.g., latency, throughput, accuracy) that indicate a need for additional capacity or improved performance? Are there any tasks or types of tasks that consistently perform poorly or take longer than expected?

Answering these questions will provide a clearer picture of your cluster's current state and help determine if and where a new node would be most beneficial.
```

</details>

**Scoring guide:**
5 — Asks about current model family coverage / training lineage diversity gaps, memory bandwidth profile of existing nodes, AND either network latency topology or current queue pressure. Demonstrates it absorbed the Wide Not Deep principle and bandwidth-as-primary-metric rule.
4 — Good distributed inference questions but misses family diversity angle.
3 — Generic compute questions (how much RAM, what GPU, what budget).
2 — Jumps straight to recommending hardware.
1 — No architectural awareness, generic or off-topic.

<details>
<summary>Full response</summary>

```

```

</details>

**Scoring guide:**
See sub-prompt scoring guides.

---

**Weighted total:** None  
**Verdict:** pending review  

---

### `mistral-nemo:12b`

**Family:** Mistral  
**Size:** 12B  
**Backend:** llama.cpp/MLX-auto (Q4_0)  
**Avg decode:** 25.1 t/s  
**Avg prefill:** 172.5 t/s  
**Thinking token leak:** no  

#### Test 1: Rubber Duck (Conversational Reasoning)

**Score:** None / 5  
**Decode:** 25.1 t/s  
**Prefill:** 172.5 t/s  
**Tokens generated:** 480  

*3 sub-prompts: 1A (Steam/vacuum), 1B (Fiction/timeline), 1C (Concierge/philosophy).*

##### Sub-prompt 1A: Steam Game Recommendation

**Score:** None / 5  
**Decode:** 33.2 t/s  
**Notes:** Docs injected: []. Prompt ~36 tokens.  

<details>
<summary>Full response</summary>

```
Sure, I'd be happy to help you find a game that suits your preferences. Here are three questions that will help me understand what you might enjoy:

1. **What types of games do you typically enjoy?** (e.g., action, adventure, RPG, strategy, puzzle, etc.)
2. **What is your preferred playstyle?** (e.g., story-driven, open-world exploration, competitive multiplayer, cooperative multiplayer, etc.)
3. **How much time do you usually spend on a single gaming session?** (e.g., short bursts, a few hours at a time, or long marathons)

Your answers to these questions will help me suggest a game that fits your preferences and can be completed within the time you have available. Once you've provided your answers, I can make a recommendation.
```

</details>

**Scoring guide:**
5 — Probes completion habits, current mood/headspace, AND something non-obvious (session length, difficulty tolerance, solo vs social, time-of-day patterns). Asks nothing, recommends nothing.
4 — Good questions, all fairly standard genre/preference territory.
3 — Generic (what genre, what have you played before).
2 — Ignores instruction and recommends games anyway.
1 — Off-topic or refuses.

##### Sub-prompt 1B: Fiction Timeline — Next Short Story

**Score:** None / 5  
**Decode:** 30.6 t/s  
**Notes:** Docs injected: ['timeline']. Prompt ~39 tokens.  

<details>
<summary>Full response</summary>

```
That sounds like an exciting project! To help identify the most dramatically interesting setting for your short story, I have a few questions:

1. What is the primary conflict or theme you'd like to explore in this story? (e.g., love, betrayal, war, magic, etc.)
2. Are there any specific characters, creatures, or factions you'd like to include or focus on?
3. What kind of tone or atmosphere are you aiming for? (e.g., lighthearted and humorous, dark and gritty, epic and sweeping, etc.)

Your answers to these questions will help guide us towards the most suitable setting within your fantasy world's timeline.
```

</details>

**Scoring guide:**
5 — Identifies the 0346-0350DE compression (Nageri discovery to Sundering in 4 years), the 0685-0688DE Phineas hunt, or the structural gap between documented events. Question shows it understood the dramatic implication, not just listed dates. Does not suggest a setting.
4 — Notices a specific period but questions are generic (tone, length).
3 — Asks about character or genre without engaging with timeline structure.
2 — Ignores instruction and suggests a setting directly.
1 — Off-topic or refuses.

##### Sub-prompt 1C: Concierge Hardware Node Evaluation

**Score:** None / 5  
**Decode:** 11.6 t/s  
**Notes:** Docs injected: ['philosophy']. Prompt ~6,159 tokens.  

<details>
<summary>Full response</summary>

```
Great, here are three questions:

1. **Current Fleet:** What is the current composition of your Concierge cluster in terms of node types, GPU models, and memory configurations? Specifically, how many iGPU nodes do you have, and what are their GPU models and memory capacities?

2. **Workload:** What is the mix of tasks your cluster currently handles? Are there any specific tasks that are consistently causing queue pressure or slowdowns? What are the most common task types and their approximate parameter count requirements?

3. **Capability Ceiling:** What is the current IQ ceiling of your cluster? In other words, what is the largest model size your cluster can handle either resident on a single node or temporarily sharded across nodes without exceeding acceptable latency for the task's SLA class?

Once I have this information, I can provide a more informed hardware recommendation.
```

</details>

**Scoring guide:**
5 — Asks about current model family coverage / training lineage diversity gaps, memory bandwidth profile of existing nodes, AND either network latency topology or current queue pressure. Demonstrates it absorbed the Wide Not Deep principle and bandwidth-as-primary-metric rule.
4 — Good distributed inference questions but misses family diversity angle.
3 — Generic compute questions (how much RAM, what GPU, what budget).
2 — Jumps straight to recommending hardware.
1 — No architectural awareness, generic or off-topic.

<details>
<summary>Full response</summary>

```

```

</details>

**Scoring guide:**
See sub-prompt scoring guides.

---

**Weighted total:** None  
**Verdict:** pending review  

---

### `qwen2.5:32b`

**Family:** Qwen  
**Size:** 32B  
**Backend:** llama.cpp/MLX-auto (Q4_K_M)  
**Avg decode:** 5.6 t/s  
**Avg prefill:** 57.6 t/s  
**Thinking token leak:** no  

#### Test 1: Rubber Duck (Conversational Reasoning)

**Score:** None / 5  
**Decode:** 5.6 t/s  
**Prefill:** 57.6 t/s  
**Tokens generated:** 594  

*3 sub-prompts: 1A (Steam/vacuum), 1B (Fiction/timeline), 1C (Concierge/philosophy).*

##### Sub-prompt 1A: Steam Game Recommendation

**Score:** None / 5  
**Decode:** 6.5 t/s  
**Notes:** Docs injected: []. Prompt ~36 tokens.  

<details>
<summary>Full response</summary>

```
Sure, I'd be happy to help you narrow down your options! Here are three questions to help me understand your preferences better:

1. What genres or types of games do you generally enjoy? For example, are you into action, adventure, role-playing, strategy, or something else?

2. How do you prefer to play your games? Do you like games with a clear storyline and character development, or do you prefer more open-ended experiences where you can explore and make your own decisions?

3. How important is multiplayer to you? Do you enjoy playing games solo, or do you prefer games that have a strong multiplayer component, whether cooperative or competitive?
```

</details>

**Scoring guide:**
5 — Probes completion habits, current mood/headspace, AND something non-obvious (session length, difficulty tolerance, solo vs social, time-of-day patterns). Asks nothing, recommends nothing.
4 — Good questions, all fairly standard genre/preference territory.
3 — Generic (what genre, what have you played before).
2 — Ignores instruction and recommends games anyway.
1 — Off-topic or refuses.

##### Sub-prompt 1B: Fiction Timeline — Next Short Story

**Score:** None / 5  
**Decode:** 6.6 t/s  
**Notes:** Docs injected: ['timeline']. Prompt ~39 tokens.  

<details>
<summary>Full response</summary>

```
Great! To help pinpoint a compelling setting for your short story within the master timeline of your fantasy world, here are three questions that can help identify a dramatically interesting period or location:

1. **Are there significant political or social changes happening in any era of the timeline?** Identifying times of transition, rebellion, or upheaval can offer rich opportunities for conflict and drama in your story.

2. **Which era or location in the timeline has the most mysterious or unexplored history?** Unraveling mysteries about the past can be a powerful narrative driver and can lead to intriguing discoveries and conflicts.

3. **Is there a specific event or period that is crucial to the lore of your world but has not been explored in detail yet?** Exploring a pivotal moment or a lesser-known aspect of a well-established event can add depth to your world and provide a fresh perspective on familiar lore.

These questions can help you focus on a setting that not only fits well with your story ideas but also enriches the overall world-building of your fantasy project.
```

</details>

**Scoring guide:**
5 — Identifies the 0346-0350DE compression (Nageri discovery to Sundering in 4 years), the 0685-0688DE Phineas hunt, or the structural gap between documented events. Question shows it understood the dramatic implication, not just listed dates. Does not suggest a setting.
4 — Notices a specific period but questions are generic (tone, length).
3 — Asks about character or genre without engaging with timeline structure.
2 — Ignores instruction and suggests a setting directly.
1 — Off-topic or refuses.

##### Sub-prompt 1C: Concierge Hardware Node Evaluation

**Score:** None / 5  
**Decode:** 3.8 t/s  
**Notes:** Docs injected: ['philosophy']. Prompt ~6,159 tokens.  

<details>
<summary>Full response</summary>

```
To help you make an informed decision about adding a new inference node to your Concierge cluster, it's important to gather some details about your current setup and workload. Here are three questions that will be helpful:

1. **Current Workload and Utilization:**
   - What is the current utilization rate of your existing nodes, particularly during peak times? Are there specific types of tasks (e.g., token generation, embedding, classification) that are more resource-intensive and frequently bottlenecked?

2. **Quorum and Model Diversity:**
   - How diverse is your current ensemble of models in terms of architectural family and training lineage? Do you have a mix of different model families and training data sources, or are most of your models from similar lineages?

3. **Priority and Task Distribution:**
   - What is the distribution of task priorities (P0, P1, P2, P3) in your current workload? Are you frequently experiencing delays or backlogs in any of these priority lanes, particularly in P1 (interactive tasks)?

Answering these questions will provide insight into whether adding another node will effectively enhance your cluster's performance and diversity, and how it might impact the overall workload distribution and task completion times.
```

</details>

**Scoring guide:**
5 — Asks about current model family coverage / training lineage diversity gaps, memory bandwidth profile of existing nodes, AND either network latency topology or current queue pressure. Demonstrates it absorbed the Wide Not Deep principle and bandwidth-as-primary-metric rule.
4 — Good distributed inference questions but misses family diversity angle.
3 — Generic compute questions (how much RAM, what GPU, what budget).
2 — Jumps straight to recommending hardware.
1 — No architectural awareness, generic or off-topic.

<details>
<summary>Full response</summary>

```

```

</details>

**Scoring guide:**
See sub-prompt scoring guides.

---

**Weighted total:** None  
**Verdict:** pending review  

---

### `gemma4:26b`

**Family:** Gemma4  
**Size:** 26B  
**Backend:** llama.cpp/MLX-auto (Q4_K_M)  
**Avg decode:** 31.4 t/s  
**Avg prefill:** 249.3 t/s  
**Thinking token leak:** no  

#### Test 1: Rubber Duck (Conversational Reasoning)

**Score:** None / 5  
**Decode:** 31.4 t/s  
**Prefill:** 249.3 t/s  
**Tokens generated:** 3623  

*3 sub-prompts: 1A (Steam/vacuum), 1B (Fiction/timeline), 1C (Concierge/philosophy).*

##### Sub-prompt 1A: Steam Game Recommendation

**Score:** None / 5  
**Decode:** 37.9 t/s  
**Notes:** Docs injected: []. Prompt ~36 tokens.  

<details>
<summary>Full response</summary>

```
To give you the best recommendation for your 40-hour window, please answer the following:

1. **Narrative vs. Mechanics:** Do you prefer a cinematic, story-driven experience where the plot is the main draw, or are you looking for tight, satisfying gameplay loops where the mechanics are the star?
2. **Intensity & Vibe:** For this specific block of time, are you looking for something relaxing and "low-stakes" (to unwind) or something high-intensity and challenging (to keep you on your toes)?
3. **The "Finish" Factor:** What are two or three games you have recently completed and loved, and—crucially—what is a game you started recently but abandoned halfway through?
```

</details>

**Scoring guide:**
5 — Probes completion habits, current mood/headspace, AND something non-obvious (session length, difficulty tolerance, solo vs social, time-of-day patterns). Asks nothing, recommends nothing.
4 — Good questions, all fairly standard genre/preference territory.
3 — Generic (what genre, what have you played before).
2 — Ignores instruction and recommends games anyway.
1 — Off-topic or refuses.

##### Sub-prompt 1B: Fiction Timeline — Next Short Story

**Score:** None / 5  
**Decode:** 33.8 t/s  
**Notes:** Docs injected: ['timeline']. Prompt ~39 tokens.  

<details>
<summary>Full response</summary>

```
I do not see the timeline attached to your message yet. Please provide it so I can analyze the specific eras, conflicts, and shifts within your world.

In the meantime, to help me identify which part of that timeline holds the most dramatic potential, please consider these three questions:

1. **The Scale of Impact:** Do you want the drama to stem from the "macro" level (the shifting of borders, the fall of empires, and the high-stakes decisions of rulers) or the "micro" level (the personal, ground-level struggle of individuals caught in the gears of history)?

2. **The Direction of Change:** Are you more interested in exploring the *onset* of a historical turning point (the mounting tension, the warning signs, and the "calm before the storm") or the *consequences* of a completed cataclysm (the struggle to rebuild, the loss of magic/knowledge, or navigating a broken world)?

3. **The Nature of the Conflict:** Do you prefer a setting of "Golden Age" stability, where the drama is driven by internal decay, political intrigue, and hidden corruption, or a setting of "Dark Age" instability, where the drama is driven by external threats, scarcity, and the raw fight for survival?
```

</details>

**Scoring guide:**
5 — Identifies the 0346-0350DE compression (Nageri discovery to Sundering in 4 years), the 0685-0688DE Phineas hunt, or the structural gap between documented events. Question shows it understood the dramatic implication, not just listed dates. Does not suggest a setting.
4 — Notices a specific period but questions are generic (tone, length).
3 — Asks about character or genre without engaging with timeline structure.
2 — Ignores instruction and suggests a setting directly.
1 — Off-topic or refuses.

##### Sub-prompt 1C: Concierge Hardware Node Evaluation

**Score:** None / 5  
**Decode:** 22.5 t/s  
**Notes:** Docs injected: ['philosophy']. Prompt ~6,159 tokens.  

<details>
<summary>Full response</summary>

```
To evaluate this addition according to the **Concierge Architecture Philosophy**, you must look past the hardware specs and focus on the node's impact on the system's equilibrium. 

Before deciding, you should be able to answer these three questions:

1.  **The Diversity Audit:** What is the current distribution of model families and training lineages represented in your resident ensemble, and does this new node provide a *genuinely distinct* architectural or lineage-based "voice" that is currently missing? (i.e., Does it satisfy the *Wide Not Deep* principle, or is it just adding redundant depth?)

2.  **The Telemetry Signal:** What does the Router’s current telemetry indicate regarding queue pressure for P1 and P2 workloads—specifically, is the bottleneck a lack of **throughput** (token generation speed for small models) or a lack of **capacity** (VRAM availability to host larger models for quorum)?

3.  **The Maintenance Contract:** Can the capability envelope of this new node be fully advertised and fulfilled via the existing **Docker Tool Zoo** without requiring custom human intervention or manual driver configuration that would increase the cluster's total orchestration cost?
```

</details>

**Scoring guide:**
5 — Asks about current model family coverage / training lineage diversity gaps, memory bandwidth profile of existing nodes, AND either network latency topology or current queue pressure. Demonstrates it absorbed the Wide Not Deep principle and bandwidth-as-primary-metric rule.
4 — Good distributed inference questions but misses family diversity angle.
3 — Generic compute questions (how much RAM, what GPU, what budget).
2 — Jumps straight to recommending hardware.
1 — No architectural awareness, generic or off-topic.

<details>
<summary>Full response</summary>

```

```

</details>

**Scoring guide:**
See sub-prompt scoring guides.

---

**Weighted total:** None  
**Verdict:** pending review  

---

## Decisions Log

| Decision | Rationale |
|----------|-----------|
| Logos runs Bit layer only | Not participating in Workbee or quorum at this stage. |
| Ollama as serving backend | Single-user interactive app on Apple Silicon. Metal/MLX path. llama.cpp belongs at Workbee layer. |
| Native function calling required | Bespoke OpenAI-compatible frontend requires proper tool-use schema. |
| ANE support deferred | GPU → CPU path sufficient for now. |
| Quorum rules do not apply | Bit's local model is advisory only. |

## Open Questions

- [ ] Does Ollama 0.19 MLX path activate for all tested models, or only Qwen3.5?
- [ ] Q8 variants tested? Note quality delta vs Q4_K_M per model.
- [ ] At what context length does M1 Max start offloading to CPU?
- [ ] Parallel tool call support confirmed per model family?

*Generated by bit_eval.py — 2026-04-05 17:14:10*