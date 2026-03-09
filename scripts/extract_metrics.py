#!/usr/bin/env python3
"""
Extract metrics from a Qwen Code CLI transcript JSON.
Produces a run_meta.json with timing, token, and tool-call stats.

Usage:
    python3 extract_metrics.py <transcript.json> <test_name> <model> <exit_code>
"""

import json
import sys


def extract(transcript_path, test_name, model, exit_code):
    meta = {
        "test": test_name,
        "model": model,
        "exit_code": exit_code,
        "duration_seconds": 0,
        "duration_ms": 0,
        "is_error": False,
        "tokens": {
            "input": 0,
            "output": 0,
            "cached": 0,
            "total": 0,
        },
        "tools": {
            "total_calls": 0,
            "total_success": 0,
            "total_fail": 0,
            "tool_duration_ms": 0,
            "by_name": {},
        },
        "files": {
            "lines_added": 0,
            "lines_removed": 0,
        },
        "api_requests": 0,
        "api_errors": 0,
        "api_latency_ms": 0,
    }

    try:
        with open(transcript_path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return meta

    if not isinstance(data, list):
        return meta

    # Find the result message
    result_msg = None
    for item in data:
        if isinstance(item, dict) and item.get("type") == "result":
            result_msg = item
            break

    if not result_msg:
        return meta

    meta["duration_ms"] = result_msg.get("duration_ms", 0)
    meta["duration_seconds"] = round(meta["duration_ms"] / 1000, 1)
    meta["is_error"] = result_msg.get("is_error", False)

    # Token usage
    usage = result_msg.get("usage", {})
    meta["tokens"]["input"] = usage.get("input_tokens", 0)
    meta["tokens"]["output"] = usage.get("output_tokens", 0)
    meta["tokens"]["cached"] = usage.get("cache_read_input_tokens", 0)
    meta["tokens"]["total"] = usage.get("total_tokens", 0)

    # Stats
    stats = result_msg.get("stats", {})

    # Model-level API stats
    for model_name, model_stats in stats.get("models", {}).items():
        api = model_stats.get("api", {})
        meta["api_requests"] += api.get("totalRequests", 0)
        meta["api_errors"] += api.get("totalErrors", 0)
        meta["api_latency_ms"] += api.get("totalLatencyMs", 0)

    # Tool stats
    tools = stats.get("tools", {})
    meta["tools"]["total_calls"] = tools.get("totalCalls", 0)
    meta["tools"]["total_success"] = tools.get("totalSuccess", 0)
    meta["tools"]["total_fail"] = tools.get("totalFail", 0)
    meta["tools"]["tool_duration_ms"] = tools.get("totalDurationMs", 0)

    for tool_name, tool_stats in tools.get("byName", {}).items():
        meta["tools"]["by_name"][tool_name] = {
            "count": tool_stats.get("count", 0),
            "success": tool_stats.get("success", 0),
            "fail": tool_stats.get("fail", 0),
            "duration_ms": tool_stats.get("durationMs", 0),
        }

    # File stats
    files = stats.get("files", {})
    meta["files"]["lines_added"] = files.get("totalLinesAdded", 0)
    meta["files"]["lines_removed"] = files.get("totalLinesRemoved", 0)

    return meta


def main():
    if len(sys.argv) < 5:
        print("Usage: python3 extract_metrics.py <transcript.json> <test_name> <model> <exit_code>")
        sys.exit(1)

    transcript_path = sys.argv[1]
    test_name = sys.argv[2]
    model = sys.argv[3]
    exit_code = int(sys.argv[4])

    meta = extract(transcript_path, test_name, model, exit_code)

    # Print summary to stdout
    print(f"  Tokens: {meta['tokens']['input']:,} in / {meta['tokens']['output']:,} out / {meta['tokens']['total']:,} total")
    print(f"  Tools: {meta['tools']['total_calls']} calls ({meta['tools']['total_success']} ok, {meta['tools']['total_fail']} fail)")
    print(f"  Files: +{meta['files']['lines_added']} / -{meta['files']['lines_removed']} lines")
    print(f"  API: {meta['api_requests']} requests, {meta['api_latency_ms']/1000:.1f}s latency")

    # Write to JSON (same directory as transcript)
    import os
    out_path = os.path.join(os.path.dirname(transcript_path), "run_meta.json")
    with open(out_path, "w") as f:
        json.dump(meta, f, indent=2)


if __name__ == "__main__":
    main()
