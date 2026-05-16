As requested, I have compiled the complete test suite into a single, copy-pasteable Markdown block. You can save this text as `BIT_MODEL_EVAL_2026.md` to guide your research on the **Logos** node.

### Answers to Your Final Checklist
* **CLI vs. Desktop:** Use the **Ollama CLI**. The April 2026 release of **Ollama 0.19** includes a preview of a native **MLX inference engine** for Apple Silicon, which can be engaged via specific environment variables to achieve nearly double the performance of the older `llama.cpp` backend.
* **Artifacts:** You will need one large technical text file (approx. 15,000–20,000 tokens) for **Test 4**. I recommend using a local copy of a complex technical manual or code documentation.

---

```markdown
# CONCIERGE: BIT LAYER MODEL EVALUATION SUITE
**Date:** April 3, 2026
**Node:** Logos (M1 Max, 64GB Unified Memory)
**Environment:** Ollama v0.19+ (MLX Engine)

---

## 0. PRE-FLIGHT SETUP (THE SEED)

To ensure your M1 Max utilizes the new MLX-native acceleration and NVFP4 quantization support, initialize your environment with these settings.

### Initialization Commands
```bash
# Force Ollama to use the preview MLX backend for peak Apple Silicon speed
export OLLAMA_MLX=1 
export OLLAMA_FLASH_ATTENTION=1

# Start the server (run in a separate terminal window)
ollama serve
```

### Recommended Parameters for All Tests
When running `ollama run <model>`, use the following flags to measure performance and ensure deterministic results for structured tests:
* `--verbose` (To see tokens/sec and generation time)
* `-p "num_ctx=32768"` (Set context window to 32k)
* `-p "temperature=0"` (For Tests 2, 3, and 5)

---

## TEST 1: THE RUBBER DUCK
**Objective:** Evaluate reasoning depth, Socratic dialogue, and technical nuance.
**Justification:** Bit must act as a high-tier research partner when cloud models are offline.

### The Prompt
> "I am refactoring a distributed job scheduler. Workers currently heartbeat to a central Redis instance, but we’re seeing connection exhaustion at 500+ nodes. I’m considering moving to a gossip-based health check. Do not provide a solution. Ask me three probing questions about my infrastructure constraints that I might have overlooked."

### Baseline Result (Target Ceiling)
* **Angle Detection:** Identifies the "Split-Brain" risk in gossip protocols or the network overhead of broadcast storms at scale.
* **Dialogue Style:** Does not jump to a solution; stays in "investigative mode."

---

## TEST 2: TOOL SCHEMA PRECISION
**Objective:** Validate strict OpenAI-compatible JSON tool calling.
**Justification:** Bit is the primary interface for tool execution; incorrect JSON breaks the pipeline.

### The Prompt
> "Available tool: `get_node_metrics(node_id: string, metric_type: 'cpu'|'thermal')`. 
> Requirement: Retrieve the CPU and thermal metrics for 'Node-Alpha-01' and 'Node-Beta-99' simultaneously."

### Baseline Result (Target Ceiling)
A valid JSON array containing exactly two distinct tool call objects:
```json
[
  {"name": "get_node_metrics", "arguments": {"node_id": "Node-Alpha-01", "metric_type": "cpu"}},
  {"name": "get_node_metrics", "arguments": {"node_id": "Node-Beta-99", "metric_type": "thermal"}}
]
```

---

## TEST 3: INSTRUCTION DISCIPLINE (GOVERNANCE)
**Objective:** Test the model's ability to follow rigid formatting and negative constraints.
**Justification:** Essential for ensuring the model doesn't drift into prose when a downstream parser is waiting for specific markers.

### The Prompt
> "Summarize your current hardware environment (M1 Max, 64GB). 
> Constraints: 
> 1. Exactly three bullet points. 
> 2. No bullet can exceed 10 words. 
> 3. Do not use the words 'Mac', 'Apple', or 'Memory'. 
> 4. Every bullet must end with a semicolon."

### Baseline Result (Target Ceiling)
* **100% adherence.** Zero forbidden words. Correct count. Every semicolon present.

---

## TEST 4: CONTEXT NEEDLE RETRIEVAL
**Objective:** Test memory stability over 15,000+ tokens.
**Justification:** Long technical sessions shouldn't lose context from the start of the chat.

### The Setup
1. Paste a large technical artifact (15k+ tokens).
2. At the very beginning of the paste, insert: `[ARCHIVE_KEY: ZULU-9-OMEGA]`.
3. Follow the paste with unrelated chat for 2-3 turns.

### The Prompt
> "What was the ARCHIVE_KEY mentioned at the very beginning of our session?"

### Baseline Result (Target Ceiling)
* Immediate, unhallucinated retrieval of `ZULU-9-OMEGA`.

---

## TEST 5: INTENT PARSING (SEMANTIC BRIDGE)
**Objective:** Mapping natural language to logic artifacts for the Planner (Layer 2).
**Justification:** Bit’s core job is intent capture.

### The Prompt
> "Deploy the 'Workbee-Alpha' image to the cluster. If thermal pressure is over 80%, abort. If it's between 60% and 80%, delay for 10 minutes and retry. Otherwise, proceed immediately."

### Baseline Result (Target Ceiling)
```json
{
  "intent": "deploy",
  "target": "Workbee-Alpha",
  "logic": [
    {"condition": ">80%", "action": "abort"},
    {"condition": "60-80%", "action": "delay", "value": "10m"},
    {"condition": "<60%", "action": "proceed"}
  ]
}
```

---

## PERFORMANCE TARGETS FOR LOGOS (M1 MAX)

| Metric | Pass Threshold | Target (Ollama 0.19 + MLX) |
| :--- | :--- | :--- |
| **Decode Speed** | >15 tokens/sec | ~110-130 tokens/sec (MoE models) |
| **Prefill Speed** | >500 tokens/sec | ~1800+ tokens/sec |
| **VRAM Usage** | <50GB | Stay within the 32GB-64GB "Interactive Zone" |
```