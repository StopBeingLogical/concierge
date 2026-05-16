#!/usr/bin/env python3
"""
Quick benchmark harness for Qwen 3.6 on Ollama.

Tests PP (prompt processing) and TG (token generation) throughput across various prompt sizes.
Outputs results in tabular format similar to oMLX benchmarks.

Usage:
  python test_qwen36_benchmark.py --host http://192.168.3.138:11434 --model qwen3.6:35b-a3b

Install requirements:
  pip install requests
"""

import argparse
import json
import time
import requests
from statistics import mean, stdev

def benchmark(host, model, prompt_size, gen_tokens=128, num_runs=3):
    """Run a single benchmark test."""

    # Create padding prompt of approximate size
    # ~4 chars per token average
    padding = "x" * (prompt_size * 4)
    prompt = f"Generate a response. Context: {padding}\n\nYour response:"

    results = {
        "ttft": [],      # Time to first token (ms)
        "tpot": [],      # Time per output token (ms)
        "pp_tps": [],    # Prompt processing tokens/sec
        "tg_tps": [],    # Token generation tokens/sec
    }

    url = f"{host}/api/generate"

    for run in range(num_runs):
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
            }
        }

        start = time.time()
        response = requests.post(url, json=payload, timeout=300)
        total_time = time.time() - start

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return None

        data = response.json()

        # Extract metrics from Ollama response
        eval_count = data.get("eval_count", gen_tokens)  # tokens generated
        prompt_eval_count = data.get("prompt_eval_count", len(prompt.split()))
        total_duration = data.get("total_duration", 0) / 1e9  # convert ns to seconds
        eval_duration = data.get("eval_duration", 0) / 1e9
        prompt_eval_duration = data.get("prompt_eval_duration", 0) / 1e9

        # Calculate metrics
        if prompt_eval_duration > 0:
            pp_tps = prompt_eval_count / prompt_eval_duration
        else:
            pp_tps = 0

        if eval_duration > 0:
            tg_tps = eval_count / eval_duration
        else:
            tg_tps = 0

        # TTFT is time until first token (prompt eval time)
        ttft_ms = (prompt_eval_duration * 1000) if prompt_eval_duration > 0 else 0

        # TPOT is average time per output token
        tpot_ms = (eval_duration * 1000 / eval_count) if eval_count > 0 else 0

        results["ttft"].append(ttft_ms)
        results["tpot"].append(tpot_ms)
        results["pp_tps"].append(pp_tps)
        results["tg_tps"].append(tg_tps)

        print(f"  Run {run+1}: PP {pp_tps:.1f} tok/s | TG {tg_tps:.1f} tok/s | TTFT {ttft_ms:.1f}ms")

    return {
        "ttft_ms": mean(results["ttft"]),
        "tpot_ms": mean(results["tpot"]),
        "pp_tps": mean(results["pp_tps"]),
        "tg_tps": mean(results["tg_tps"]),
    }

def main():
    parser = argparse.ArgumentParser(description="Benchmark Qwen 3.6 on Ollama")
    parser.add_argument("--host", default="http://192.168.3.138:11434", help="Ollama host URL")
    parser.add_argument("--model", default="qwen3.6:35b-a3b", help="Model name")
    parser.add_argument("--runs", type=int, default=3, help="Number of runs per test")
    args = parser.parse_args()

    prompt_sizes = [1024, 4096, 8192, 16384, 32768]
    gen_tokens = 128

    print(f"\nBenchmarking {args.model} on {args.host}")
    print(f"Generating {gen_tokens} tokens per test, {args.runs} runs each\n")
    print("=" * 90)
    print(f"{'Test':<20} {'TTFT(ms)':>12} {'TPOT(ms)':>12} {'PP TPS':>12} {'TG TPS':>12}")
    print("=" * 90)

    for ps in prompt_sizes:
        print(f"\npp{ps}/tg{gen_tokens}")
        result = benchmark(args.host, args.model, ps, gen_tokens, args.runs)

        if result:
            print(f"  {'':20} {result['ttft_ms']:>12.1f} {result['tpot_ms']:>12.2f} "
                  f"{result['pp_tps']:>12.1f} {result['tg_tps']:>12.1f}")

    print("=" * 90)
    print("\nNote: PP TPS = tokens/sec during prompt processing")
    print("      TG TPS = tokens/sec during generation")
    print("      TTFT = time to first token (prompt processing latency)")
    print("      TPOT = time per output token (generation latency)")

if __name__ == "__main__":
    main()
