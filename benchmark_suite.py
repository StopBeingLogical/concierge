#!/usr/bin/env python3
"""
Interactive benchmark suite for LLM inference (Ollama, llama.cpp, ROCm).

Tests single-request and batching performance across various prompt sizes.
Features interactive menu on startup for easy configuration.

Install requirements:
  pip install requests
"""

import argparse
import json
import time
import requests
import sys
from statistics import mean
from concurrent.futures import ThreadPoolExecutor, as_completed

class BenchmarkConfig:
    def __init__(self):
        self.host = "http://192.168.3.138:11434"
        self.backend = "ollama"
        self.model = "qwen3.6:35b-a3b"
        self.test_type = "all"
        self.num_runs = 3
        self.gen_tokens = 128
        self.prompt_sizes = [1024, 4096, 8192, 16384, 32768]
        self.batch_sizes = [2, 4]

    def interactive_menu(self):
        """Show interactive configuration menu."""
        print("\n" + "="*70)
        print("LLM INFERENCE BENCHMARK SUITE")
        print("="*70)

        # Backend
        print("\nBackend types:")
        print("  1) Ollama")
        print("  2) llama.cpp (OpenAI-compatible)")
        choice = input("Select backend [1-2, default 1]: ").strip()
        backend_map = {"1": "ollama", "2": "llamacpp", "": "ollama"}
        self.backend = backend_map.get(choice, "ollama")

        # Host
        default_host = "http://192.168.3.138:11434" if self.backend == "ollama" else "http://192.168.3.143:8000"
        print(f"\nCurrent host: {self.host}")
        user_host = input(f"Enter host [press Enter for {default_host}]: ").strip()
        if user_host:
            self.host = user_host
        else:
            self.host = default_host

        # Model
        print(f"\nCurrent model: {self.model}")
        user_model = input("Enter model name [press Enter to keep]: ").strip()
        if user_model:
            self.model = user_model

        # Test type
        print("\nTest types:")
        print("  1) Single-request only")
        print("  2) Batching only")
        print("  3) Both (default)")
        choice = input("Select test type [1-3, press Enter for 3]: ").strip()
        test_map = {"1": "single", "2": "batch", "3": "all", "": "all"}
        self.test_type = test_map.get(choice, "all")

        # Runs
        print(f"\nNumber of runs per test: {self.num_runs}")
        user_runs = input("Enter number of runs [press Enter to keep]: ").strip()
        if user_runs.isdigit():
            self.num_runs = int(user_runs)

        print("\n" + "="*70)
        print(f"Backend: {self.backend.upper()}")
        print(f"Host: {self.host}")
        print(f"Model: {self.model}")
        print(f"Tests: {self.test_type}")
        print(f"Runs per test: {self.num_runs}")
        print("="*70 + "\n")

        # Verify connection
        try:
            if self.backend == "ollama":
                response = requests.head(f"{self.host}/api/tags", timeout=5)
            else:
                response = requests.head(f"{self.host}/v1/models", timeout=5)

            if response.status_code == 200:
                print("✓ Connection to inference server successful\n")
            else:
                print(f"⚠ Server returned status {response.status_code}\n")
        except Exception as e:
            print(f"✗ Cannot reach server: {e}\n")
            sys.exit(1)

def ollama_request(host, model, prompt_size, gen_tokens=128):
    """Run a single Ollama inference request."""
    padding = "x" * (prompt_size * 4)
    prompt = f"Generate a response. Context: {padding}\n\nYour response:"

    url = f"{host}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7},
    }

    try:
        response = requests.post(url, json=payload, timeout=300)
        if response.status_code != 200:
            return None

        data = response.json()
        eval_count = data.get("eval_count", gen_tokens)
        prompt_eval_count = data.get("prompt_eval_count", len(prompt.split()))
        eval_duration = data.get("eval_duration", 0) / 1e9
        prompt_eval_duration = data.get("prompt_eval_duration", 0) / 1e9

        if prompt_eval_duration > 0:
            pp_tps = prompt_eval_count / prompt_eval_duration
        else:
            pp_tps = 0

        if eval_duration > 0:
            tg_tps = eval_count / eval_duration
        else:
            tg_tps = 0

        ttft_ms = (prompt_eval_duration * 1000) if prompt_eval_duration > 0 else 0
        tpot_ms = (eval_duration * 1000 / eval_count) if eval_count > 0 else 0

        return {
            "ttft_ms": ttft_ms,
            "tpot_ms": tpot_ms,
            "pp_tps": pp_tps,
            "tg_tps": tg_tps,
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def llamacpp_request(host, model, prompt_size, gen_tokens=128):
    """Run a single llama.cpp inference request."""
    padding = "x" * (prompt_size * 4)
    prompt = f"Generate a response. Context: {padding}\n\nYour response:"

    url = f"{host}/v1/completions"
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": gen_tokens,
        "temperature": 0.7,
    }

    try:
        start_time = time.time()
        response = requests.post(url, json=payload, timeout=300)
        total_time = time.time() - start_time

        if response.status_code != 200:
            return None

        data = response.json()

        # Extract token counts from usage
        usage = data.get("usage", {})
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", gen_tokens)

        # For llama.cpp, we only have wall-clock time, not detailed timing
        # Calculate overall throughput
        total_tokens = prompt_tokens + completion_tokens
        overall_tps = total_tokens / total_time if total_time > 0 else 0

        # Estimate TG as the bottleneck (conservative estimate)
        tg_tps = completion_tokens / total_time if total_time > 0 else 0
        pp_tps = prompt_tokens / total_time if total_time > 0 else 0  # Also wall-clock based

        # TTFT is hard to measure without detailed timing; use total time as proxy
        ttft_ms = total_time * 1000
        tpot_ms = (total_time * 1000 / completion_tokens) if completion_tokens > 0 else 0

        return {
            "ttft_ms": ttft_ms,
            "tpot_ms": tpot_ms,
            "pp_tps": pp_tps,
            "tg_tps": tg_tps,
            "total_tps": overall_tps,
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def single_request(config, prompt_size, gen_tokens=128):
    """Run a single inference request (backend-agnostic)."""
    if config.backend == "ollama":
        return ollama_request(config.host, config.model, prompt_size, gen_tokens)
    else:
        return llamacpp_request(config.host, config.model, prompt_size, gen_tokens)

def batch_request(config, prompt_size, batch_size, gen_tokens=128):
    """Run multiple concurrent inference requests."""
    padding = "x" * (prompt_size * 4)
    prompt = f"Generate a response. Context: {padding}\n\nYour response:"

    if config.backend == "ollama":
        url = f"{config.host}/api/generate"
        payload = {
            "model": config.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7},
        }
    else:
        url = f"{config.host}/v1/completions"
        payload = {
            "model": config.model,
            "prompt": prompt,
            "max_tokens": gen_tokens,
            "temperature": 0.7,
        }

    results = []
    total_tokens_generated = 0
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        futures = [
            executor.submit(requests.post, url, json=payload, timeout=300)
            for _ in range(batch_size)
        ]

        for future in as_completed(futures):
            try:
                response = future.result()
                if response.status_code == 200:
                    data = response.json()

                    if config.backend == "ollama":
                        eval_count = data.get("eval_count", gen_tokens)
                        eval_duration = data.get("eval_duration", 0) / 1e9
                        if eval_duration > 0:
                            tg_tps = eval_count / eval_duration
                            results.append(tg_tps)
                            total_tokens_generated += eval_count
                    else:
                        # For llama.cpp, we only have token counts, not timing
                        usage = data.get("usage", {})
                        completion_tokens = usage.get("completion_tokens", gen_tokens)
                        results.append(completion_tokens)
                        total_tokens_generated += completion_tokens
            except Exception:
                pass

    total_time = time.time() - start_time

    if config.backend == "ollama":
        # Ollama results contain actual TPS values
        avg_tg_tps = mean(results) if results else 0
        aggregate_tps = (len(results) * gen_tokens) / total_time if total_time > 0 else 0
    else:
        # llama.cpp results contain token counts; calculate TPS from wall time
        avg_tokens_per_request = mean(results) if results else 0
        avg_tg_tps = avg_tokens_per_request / total_time if total_time > 0 else 0
        aggregate_tps = total_tokens_generated / total_time if total_time > 0 else 0

    return {
        "avg_tg_tps": avg_tg_tps,
        "aggregate_tps": aggregate_tps,
        "requests_completed": len(results),
        "total_time": total_time,
    }

def run_single_tests(config):
    """Run single-request benchmark tests."""
    print("\n" + "="*100)
    print("SINGLE-REQUEST TESTS")
    print("="*100)
    print(f"{'Test':<20} {'TTFT(ms)':>12} {'TPOT(ms)':>12} {'PP TPS':>12} {'TG TPS':>12}")
    print("="*100)

    for ps in config.prompt_sizes:
        print(f"\npp{ps}/tg{config.gen_tokens}")

        results = {"ttft": [], "tpot": [], "pp_tps": [], "tg_tps": []}

        for run in range(config.num_runs):
            result = single_request(config, ps, config.gen_tokens)
            if result:
                print(f"  Run {run+1}: PP {result['pp_tps']:.1f} tok/s | "
                      f"TG {result['tg_tps']:.1f} tok/s | TTFT {result['ttft_ms']:.1f}ms")
                results["ttft"].append(result["ttft_ms"])
                results["tpot"].append(result["tpot_ms"])
                results["pp_tps"].append(result["pp_tps"])
                results["tg_tps"].append(result["tg_tps"])

        if results["pp_tps"]:
            avg_ttft = mean(results["ttft"])
            avg_tpot = mean(results["tpot"])
            avg_pp_tps = mean(results["pp_tps"])
            avg_tg_tps = mean(results["tg_tps"])
            print(f"  {'AVERAGE':<20} {avg_ttft:>12.1f} {avg_tpot:>12.2f} "
                  f"{avg_pp_tps:>12.1f} {avg_tg_tps:>12.1f}")

    print("="*100)

def run_batch_tests(config):
    """Run batching benchmark tests."""
    print("\n" + "="*100)
    print("BATCHING TESTS (Concurrent Requests)")
    print("="*100)
    print(f"{'Batch':<15} {'Prompt Size':<15} {'Avg TG TPS':>15} {'Aggregate TPS':>15} {'Time(s)':>12}")
    print("="*100)

    for ps in [1024, 4096]:
        for bs in config.batch_sizes:
            print(f"\npp{ps}/batch{bs}")

            times = []
            agg_tps_list = []
            avg_tg_list = []

            for run in range(config.num_runs):
                result = batch_request(config, ps, bs, config.gen_tokens)
                if result and result["requests_completed"] > 0:
                    print(f"  Run {run+1}: {result['requests_completed']} requests | "
                          f"Avg TG {result['avg_tg_tps']:.1f} tok/s | "
                          f"Aggregate {result['aggregate_tps']:.1f} tok/s | "
                          f"Time {result['total_time']:.1f}s")
                    times.append(result["total_time"])
                    agg_tps_list.append(result["aggregate_tps"])
                    avg_tg_list.append(result["avg_tg_tps"])

            if agg_tps_list:
                print(f"  {'AVERAGE':<15} {mean(avg_tg_list):>15.1f} {mean(agg_tps_list):>15.1f} {mean(times):>12.1f}")

    print("="*100)
    print("\nNote: Aggregate TPS = total tokens/sec across all concurrent requests")
    print("      Avg TG TPS = average generation speed per request\n")

def main():
    parser = argparse.ArgumentParser(description="Interactive LLM inference benchmark suite")
    parser.add_argument("--no-menu", action="store_true", help="Skip interactive menu")
    parser.add_argument("--backend", choices=["ollama", "llamacpp"], help="Inference backend")
    parser.add_argument("--host", help="Server host URL")
    parser.add_argument("--model", help="Model name")
    parser.add_argument("--test", choices=["single", "batch", "all"], help="Test type")
    args = parser.parse_args()

    config = BenchmarkConfig()

    if not args.no_menu:
        config.interactive_menu()
    else:
        if args.backend:
            config.backend = args.backend
        if args.host:
            config.host = args.host
        if args.model:
            config.model = args.model
        if args.test:
            config.test_type = args.test

    if config.test_type in ["single", "all"]:
        run_single_tests(config)

    if config.test_type in ["batch", "all"]:
        run_batch_tests(config)

    print("\nBenchmark complete!")

if __name__ == "__main__":
    main()
