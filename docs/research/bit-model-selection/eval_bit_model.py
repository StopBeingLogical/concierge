#!/usr/bin/env python3
"""
Bit Layer Model Evaluation Suite
Evaluates a model against the five-test framework from BIT_MODEL_RESEARCH.md

Tests:
  Test 1 (30%) — Conversational reasoning (human scored)
  Test 2 (25%) — Structured tool calling via OpenAI schema
  Test 3 (20%) — Instruction following, 4-constraint formatting
  Test 4 (15%) — 15K token needle retrieval
  Test 5 (10%) — Intent parsing to structured JSON

Usage:
  python eval_bit_model.py --model <ollama_model_name> [--host http://localhost:11434]

Requirements:
  pip install requests

Before running:
  - Set CONTEXT_DOC_PATH to your Concierge philosophy doc path
  - Set TIMELINE_DOC_PATH to your Empire of Branoch timeline doc path
  - Fill in the Test 1 sub-prompts with your actual domain content
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

import requests

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────

CONTEXT_DOC_PATH = "/Volumes/Shuttle/Concierge Working Canon/Concierge_Philosophy_v5.md"
TIMELINE_DOC_PATH = "/Volumes/Shuttle/projects/Empire_of_Branoch/Empire of Branoch/07_Inbound_Processing/Raw_Corpus_Dumps/Prose/sources/Worldbuilding/Timeline/Timeline_2024.docx"

# Needle for Test 4 — embed this string somewhere in the 15K padding
NEEDLE_KEY = "ARCHIVE_KEY"
NEEDLE_VALUE = "ZULU-9-OMEGA"

# ─────────────────────────────────────────────
# Ollama client
# ─────────────────────────────────────────────

def chat(host: str, model: str, messages: list, tools: list = None, temperature: float = 0.7) -> dict:
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature},
    }
    if tools:
        payload["tools"] = tools
    resp = requests.post(f"{host}/api/chat", json=payload, timeout=300)
    resp.raise_for_status()
    return resp.json()


def load_text_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return f"[FILE NOT FOUND: {path}]"
    return p.read_text(encoding="utf-8", errors="replace")


# ─────────────────────────────────────────────
# Test 2 — Tool Calling
# ─────────────────────────────────────────────

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_node_status",
            "description": "Retrieve the current status and load metrics for a named cluster node.",
            "parameters": {
                "type": "object",
                "properties": {
                    "node_name": {
                        "type": "string",
                        "description": "The name of the cluster node, e.g. 'kratos' or 'ergaster'.",
                    }
                },
                "required": ["node_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_pending_jobs",
            "description": "List all pending jobs in the Concierge job queue, optionally filtered by priority lane.",
            "parameters": {
                "type": "object",
                "properties": {
                    "priority_lane": {
                        "type": "string",
                        "enum": ["p0", "p1", "p2", "p3"],
                        "description": "Filter jobs by priority lane.",
                    }
                },
                "required": [],
            },
        },
    },
]

TOOL_CALL_PROMPT = (
    "The user wants to know the status of both the 'kratos' node and the 'ergaster' node. "
    "Use the available tools to retrieve their status."
)

ABSTAIN_PROMPT = (
    "What is the weather like in Miami today?"
)


def run_test2(host: str, model: str) -> dict:
    results = {}

    # 2a: parallel tool calls
    resp = chat(host, model, [{"role": "user", "content": TOOL_CALL_PROMPT}], tools=TOOLS_SCHEMA, temperature=0.0)
    msg = resp.get("message", {})
    tool_calls = msg.get("tool_calls", [])

    called_nodes = set()
    for tc in tool_calls:
        fn = tc.get("function", {})
        if fn.get("name") == "get_node_status":
            args = fn.get("arguments", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    pass
            if isinstance(args, dict):
                called_nodes.add(args.get("node_name", "").lower())

    results["parallel_calls"] = "kratos" in called_nodes and "ergaster" in called_nodes
    results["correct_function"] = all(
        tc.get("function", {}).get("name") == "get_node_status" for tc in tool_calls
    ) if tool_calls else False
    results["call_count"] = len(tool_calls)

    # 2b: abstain check — should NOT call tools for weather question
    resp2 = chat(host, model, [{"role": "user", "content": ABSTAIN_PROMPT}], tools=TOOLS_SCHEMA, temperature=0.0)
    msg2 = resp2.get("message", {})
    abstain_calls = msg2.get("tool_calls", [])
    results["abstain_correct"] = len(abstain_calls) == 0

    passed = results["parallel_calls"] and results["correct_function"] and results["abstain_correct"]
    results["score"] = 5 if passed else (3 if results["parallel_calls"] else 0)
    return results


# ─────────────────────────────────────────────
# Test 3 — Instruction Following
# ─────────────────────────────────────────────

INSTRUCTION_PROMPT = """Write a short paragraph (exactly 3 sentences) about distributed AI systems.
Constraints you MUST follow:
1. Do not use the words 'mac', 'apple', or 'memory' anywhere in the response.
2. The paragraph must contain exactly 3 sentences — no more, no less.
3. Every sentence must begin with a capital letter.
4. Format the output as a bullet list with exactly 3 bullet points, one sentence per bullet."""


def run_test3(host: str, model: str) -> dict:
    resp = chat(host, model, [{"role": "user", "content": INSTRUCTION_PROMPT}], temperature=0.0)
    content = resp.get("message", {}).get("content", "")

    results = {}
    lower = content.lower()

    # Constraint 1: forbidden words
    forbidden = ["mac", "apple", "memory"]
    results["no_forbidden_words"] = not any(w in lower for w in forbidden)

    # Constraint 2: bullet count
    bullets = [l.strip() for l in content.split("\n") if l.strip().startswith(("-", "*", "•"))]
    results["bullet_count"] = len(bullets)
    results["correct_bullet_count"] = len(bullets) == 3

    # Constraint 3: capital letter starts
    results["capitals_ok"] = all(b.lstrip("-*• ")[0].isupper() for b in bullets) if bullets else False

    # Constraint 4: exactly 3 bullets already covered
    constraints_met = sum([
        results["no_forbidden_words"],
        results["correct_bullet_count"],
        results["capitals_ok"],
    ])
    results["constraints_met"] = constraints_met
    results["score"] = constraints_met + 1 if constraints_met == 3 else constraints_met  # max 4 → map to 5
    results["score"] = min(5, results["score"])
    results["raw_response"] = content
    return results


# ─────────────────────────────────────────────
# Test 4 — Needle Retrieval
# ─────────────────────────────────────────────

PADDING = (
    "The distributed system routes tasks based on node capability envelopes. "
    "Each envelope contains hardware specifications, available tools, and expected latency bands. "
    "The Router maintains a registry of all active envelopes and matches incoming work chunks against them. "
    "When a node's capability changes, its envelope hash changes and the Router reindexes it. "
    "The integrity chain ensures every artifact crossing a layer boundary carries a verified SHA256 hash. "
) * 200  # ~roughly 15K tokens of padding


def run_test4(host: str, model: str) -> dict:
    # Insert needle at ~75% through the padding
    split_point = int(len(PADDING) * 0.75)
    needle_sentence = f" The full value of the {NEEDLE_KEY} was {NEEDLE_VALUE}. "
    context = PADDING[:split_point] + needle_sentence + PADDING[split_point:]

    question = f"What is the full value of the {NEEDLE_KEY} mentioned in the document? Quote it exactly."

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Answer questions based only on the provided context."},
        {"role": "user", "content": f"Context:\n\n{context}\n\nQuestion: {question}"},
    ]

    resp = chat(host, model, messages, temperature=0.0)
    content = resp.get("message", {}).get("content", "")

    found = NEEDLE_VALUE in content
    results = {
        "needle_found": found,
        "score": 5 if found else 0,
        "raw_response": content[:500],
    }
    return results


# ─────────────────────────────────────────────
# Test 5 — Intent Parsing
# ─────────────────────────────────────────────

INTENT_PROMPT = """Parse the following user request into a structured intent JSON object.

User request: "Can you search the web for recent papers on mixture of experts architectures, summarize the top three, and save the summaries to a file called moe_summary.txt? Also remind me about this tomorrow at 9am."

Return ONLY a valid JSON object with these fields:
- intent_type: string
- actions: array of objects, each with "action" and "parameters" fields
- conditions: array of any conditional triggers
- artifacts: array of any files or outputs to be created

No markdown fences. No explanation. Just the JSON."""


def run_test5(host: str, model: str) -> dict:
    resp = chat(host, model, [{"role": "user", "content": INTENT_PROMPT}], temperature=0.0)
    content = resp.get("message", {}).get("content", "").strip()

    # Strip markdown fences if present
    content_clean = re.sub(r"^```(?:json)?\s*", "", content)
    content_clean = re.sub(r"\s*```$", "", content_clean).strip()

    results = {"raw_response": content[:500]}

    try:
        parsed = json.loads(content_clean)
        results["valid_json"] = True
        results["has_intent_type"] = "intent_type" in parsed
        results["has_actions"] = "actions" in parsed and isinstance(parsed["actions"], list)
        results["has_artifacts"] = "artifacts" in parsed
        results["action_count"] = len(parsed.get("actions", []))
        results["no_fences"] = "```" not in content

        score = sum([
            results["valid_json"],
            results["has_intent_type"],
            results["has_actions"],
            results["has_artifacts"],
            results["no_fences"],
        ])
        results["score"] = score
    except json.JSONDecodeError as e:
        results["valid_json"] = False
        results["parse_error"] = str(e)
        results["score"] = 0

    return results


# ─────────────────────────────────────────────
# Test 1 — Conversational Reasoning (human scored)
# ─────────────────────────────────────────────

def run_test1(host: str, model: str) -> dict:
    """
    Runs the three conversational sub-prompts and prints responses for human scoring.
    Scores are entered interactively (1-5 per sub-prompt).
    """
    print("\n" + "="*60)
    print("TEST 1 — CONVERSATIONAL REASONING (Human Scored)")
    print("="*60)
    print("Score each response 1-5 based on the criteria below.\n")

    philosophy_doc = load_text_file(CONTEXT_DOC_PATH)
    timeline_doc = load_text_file(TIMELINE_DOC_PATH)

    sub_prompts = [
        {
            "id": "1A",
            "name": "Steam Recommendations",
            "weight": "Scoring: 5=non-obvious probing (completion habits, abandoned-game diagnostic); 3=generic genre/preference; 2=recommends games directly",
            "system": "You are a helpful conversational assistant.",
            "user": "I'm trying to figure out what game to play next on Steam. I have a huge backlog and I'm not sure where to start. Can you help?",
            "context": None,
        },
        {
            "id": "1B",
            "name": "Fiction — Empire of Branoch Timeline",
            "weight": "Scoring: 5=identifies 0346-0350DE compression or 0685-0688DE Phineas hunt; 3=no timeline engagement; 2=suggests setting directly",
            "system": "You are a helpful creative writing assistant.",
            "user": "I'm working on a fantasy novel set in a world called the Empire of Branoch. I have a detailed timeline document I'd like you to read. Based on it, what questions would you ask me to help develop the most dramatically rich period to write about?",
            "context": timeline_doc,
        },
        {
            "id": "1C",
            "name": "Concierge Hardware — Philosophy Doc",
            "weight": "Scoring: 5=names Wide Not Deep, asks about training lineage diversity and bandwidth; 3=generic compute questions; 2=recommends hardware directly",
            "system": "You are a helpful technical assistant.",
            "user": "I'm designing a homelab AI orchestration system. I've attached a philosophy document that describes the architecture and design principles. Based on this, what questions would you ask me to help spec out the hardware for the cluster?",
            "context": philosophy_doc,
        },
    ]

    scores = {}
    responses = {}

    for sp in sub_prompts:
        print(f"\n{'─'*60}")
        print(f"Sub-prompt {sp['id']}: {sp['name']}")
        print(f"Scoring criteria: {sp['weight']}")
        print(f"{'─'*60}")

        messages = [{"role": "system", "content": sp["system"]}]
        if sp["context"]:
            messages.append({
                "role": "user",
                "content": f"[Document attached]\n\n{sp['context']}\n\n{sp['user']}"
            })
        else:
            messages.append({"role": "user", "content": sp["user"]})

        print("Running...", end="", flush=True)
        start = time.time()
        resp = chat(host, model, messages, temperature=0.7)
        elapsed = time.time() - start
        content = resp.get("message", {}).get("content", "")
        print(f" done ({elapsed:.1f}s)\n")

        print("RESPONSE:")
        print("-" * 40)
        print(content)
        print("-" * 40)

        responses[sp["id"]] = content

        while True:
            try:
                score = int(input(f"\nScore for {sp['id']} (1-5): ").strip())
                if 1 <= score <= 5:
                    scores[sp["id"]] = score
                    break
                print("Enter a number between 1 and 5.")
            except (ValueError, KeyboardInterrupt):
                print("Skipping — defaulting to 3.")
                scores[sp["id"]] = 3
                break

    avg_score = sum(scores.values()) / len(scores)
    return {
        "scores": scores,
        "average": round(avg_score, 2),
        "score": round(avg_score, 2),
        "responses": responses,
    }


# ─────────────────────────────────────────────
# Weighted final score
# ─────────────────────────────────────────────

WEIGHTS = {
    "test1": 0.30,
    "test2": 0.25,
    "test3": 0.20,
    "test4": 0.15,
    "test5": 0.10,
}


def compute_final_score(results: dict) -> float:
    total = 0.0
    for test, weight in WEIGHTS.items():
        score = results.get(test, {}).get("score", 0)
        total += score * weight
    return round(total, 2)


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Bit layer model evaluation suite")
    parser.add_argument("--model", required=True, help="Ollama model name, e.g. gemma4:26b")
    parser.add_argument("--host", default="http://localhost:11434", help="Ollama host URL")
    parser.add_argument("--skip-test1", action="store_true", help="Skip conversational test (requires human scoring)")
    parser.add_argument("--skip-test2", action="store_true", help="Skip tool calling test (use for models without Ollama tool support)")
    parser.add_argument("--output", default=None, help="Save results to JSON file")
    args = parser.parse_args()

    print(f"\nBit Layer Model Evaluation")
    print(f"Model : {args.model}")
    print(f"Host  : {args.host}")
    print(f"{'='*60}\n")

    all_results = {"model": args.model, "host": args.host}

    # Test 2
    if not args.skip_test2:
        print("Running Test 2 — Tool Calling...", end="", flush=True)
        t2 = run_test2(args.host, args.model)
        all_results["test2"] = t2
        print(f" score: {t2['score']}/5")
        print(f"  parallel_calls={t2['parallel_calls']}, abstain_correct={t2['abstain_correct']}, call_count={t2['call_count']}")
    else:
        print("Test 2 skipped (--skip-test2). Scoring as 0.")
        all_results["test2"] = {"score": 0, "skipped": True}

    # Test 3
    print("Running Test 3 — Instruction Following...", end="", flush=True)
    t3 = run_test3(args.host, args.model)
    all_results["test3"] = t3
    print(f" score: {t3['score']}/5")
    print(f"  constraints_met={t3['constraints_met']}/3, bullets={t3['bullet_count']}, no_forbidden={t3['no_forbidden_words']}")

    # Test 4
    print("Running Test 4 — Needle Retrieval (~15K context)...", end="", flush=True)
    t4 = run_test4(args.host, args.model)
    all_results["test4"] = t4
    print(f" score: {t4['score']}/5")
    print(f"  needle_found={t4['needle_found']}")

    # Test 5
    print("Running Test 5 — Intent Parsing...", end="", flush=True)
    t5 = run_test5(args.host, args.model)
    all_results["test5"] = t5
    print(f" score: {t5['score']}/5")
    print(f"  valid_json={t5.get('valid_json')}, has_actions={t5.get('has_actions')}, no_fences={t5.get('no_fences')}")

    # Test 1 (human scored — run last)
    if not args.skip_test1:
        t1 = run_test1(args.host, args.model)
        all_results["test1"] = t1
    else:
        print("\nTest 1 skipped (--skip-test1). Weighted score will exclude it.")
        all_results["test1"] = {"score": 0, "skipped": True}

    # Final score
    final = compute_final_score(all_results)
    all_results["final_weighted_score"] = final

    print(f"\n{'='*60}")
    print(f"FINAL WEIGHTED SCORE: {final}/5.00")
    print(f"{'='*60}")
    print(f"  Test 1 (conv 30%):    {all_results.get('test1', {}).get('score', 'N/A')}")
    print(f"  Test 2 (tools 25%):   {all_results.get('test2', {}).get('score', 'N/A')}")
    print(f"  Test 3 (instruct 20%): {all_results.get('test3', {}).get('score', 'N/A')}")
    print(f"  Test 4 (needle 15%):  {all_results.get('test4', {}).get('score', 'N/A')}")
    print(f"  Test 5 (intent 10%):  {all_results.get('test5', {}).get('score', 'N/A')}")

    if args.output:
        out_path = Path(args.output)
        # Strip raw responses before saving to keep file manageable
        save_results = {k: {ck: cv for ck, cv in v.items() if ck != "responses"} if isinstance(v, dict) else v
                       for k, v in all_results.items()}
        out_path.write_text(json.dumps(save_results, indent=2))
        print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
