#!/usr/bin/env python3
"""
Auto-scorer for Tier 1 benchmark tests.
Runs solution.py, captures stdout, and checks against expected values in checks.json.

Usage:
    python3 score_test.py <test_dir> <results_dir>

Example:
    python3 score_test.py test-001-cohens-kappa results/qwen3-coder_2026-02-21/test-001-cohens-kappa
"""

import json
import os
import re
import subprocess
import sys


def run_solution(results_dir):
    """Run solution.py in the results directory and capture stdout."""
    solution_path = os.path.join(results_dir, "solution.py")
    if not os.path.exists(solution_path):
        return None, "solution.py not found"

    try:
        result = subprocess.run(
            [sys.executable, "solution.py"],
            cwd=results_dir,
            capture_output=True,
            text=True,
            timeout=300,
        )
        return result.stdout, result.stderr if result.returncode != 0 else None
    except subprocess.TimeoutExpired:
        return None, "Timed out after 300 seconds"
    except Exception as e:
        return None, str(e)


def check_execution(stdout, error):
    """Check if code ran successfully."""
    return stdout is not None and error is None


def check_exact(stdout, pattern, expected):
    """Check for an exact integer match in stdout."""
    match = re.search(pattern, stdout, re.MULTILINE)
    if not match:
        return False, f"Pattern not found: {pattern}"
    try:
        value = int(match.group(1))
        if value == expected:
            return True, f"{value} == {expected}"
        return False, f"{value} != {expected}"
    except (ValueError, IndexError):
        return False, f"Could not parse value from: {match.group(0)}"


def check_numeric(stdout, pattern, expected, tolerance, absolute_value=False):
    """Check for a numeric match within tolerance.

    If *expected* is a list, the check passes when the value is within
    tolerance of **any** element (useful when multiple correct answers exist,
    e.g. U1 vs U2 in Mann-Whitney).  When *absolute_value* is True the
    comparison uses abs(value) so the sign is ignored.
    """
    match = re.search(pattern, stdout, re.MULTILINE)
    if not match:
        return False, f"Pattern not found: {pattern}"
    try:
        value = float(match.group(1))
        cmp_value = abs(value) if absolute_value else value

        targets = expected if isinstance(expected, list) else [expected]
        for tgt in targets:
            if abs(cmp_value - tgt) <= tolerance:
                return True, f"{value} within {tolerance} of {tgt}"
        if len(targets) == 1:
            return False, f"{value} not within {tolerance} of {targets[0]}"
        return False, f"{value} not within {tolerance} of any of {targets}"
    except (ValueError, IndexError):
        return False, f"Could not parse value from: {match.group(0)}"


def check_range(stdout, pattern, min_val, max_val):
    """Check if a value falls within a range."""
    match = re.search(pattern, stdout, re.MULTILINE)
    if not match:
        return False, f"Pattern not found: {pattern}"
    try:
        value = float(match.group(1))
        if min_val <= value <= max_val:
            return True, f"{value} in [{min_val}, {max_val}]"
        return False, f"{value} not in [{min_val}, {max_val}]"
    except (ValueError, IndexError):
        return False, f"Could not parse value from: {match.group(0)}"


def check_regex_match(stdout, pattern, expected_pattern):
    """Check if extracted text matches an expected regex pattern."""
    match = re.search(pattern, stdout, re.MULTILINE)
    if not match:
        return False, f"Pattern not found: {pattern}"
    value = match.group(1).strip()
    if re.search(expected_pattern, value, re.IGNORECASE):
        return True, f"'{value}' matches '{expected_pattern}'"
    return False, f"'{value}' does not match '{expected_pattern}'"


def check_file_exists(results_dir, filename):
    """Check if an output file exists."""
    filepath = os.path.join(results_dir, filename)
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        return True, f"Exists ({size} bytes)"
    return False, f"{filename} not found"


def _detect_stream_error(results_dir):
    """Check if a stream error occurred during this task's run."""
    transcript_path = os.path.join(results_dir, "transcript.json")
    if not os.path.exists(transcript_path):
        return False
    try:
        with open(transcript_path) as f:
            content = f.read()
        return ("stream ended" in content
                or "Streaming request timeout" in content)
    except Exception:
        return False


def _get_retry_info(results_dir):
    """Load retry metadata if present."""
    retry_path = os.path.join(results_dir, "retry_meta.json")
    if os.path.exists(retry_path):
        try:
            with open(retry_path) as f:
                return json.load(f)
        except Exception:
            pass
    return None


def classify_error(results, results_dir):
    """Classify the primary error using the SWAT-Bench Error Taxonomy.

    Categories are applied in order (first match wins):
      0   - Pass: full marks
      1   - No Solution Produced: solution.py missing
      1.1 - No Solution (Stream Error): stream died before code was written
      1.2 - No Solution (Timeout): wall-clock limit exceeded
      2   - Execution Failure: code crashes with traceback
      2.1 - Execution Failure (Stream Truncation): stream error left broken code
      5   - Incomplete Generation: code exists, runs (exit 0), but no/empty stdout
      3   - Output Format Mismatch: code runs, has stdout, but labels don't match
      4   - Analytical Error: labels match but values are wrong
      6   - Constraint Violation: missing required output files

    Sub-categories (x.1, x.2) are stored as floats and indicate infrastructure
    failures vs. genuine model limitations.  The integer part is the primary
    category for aggregation.
    """
    if results.get("auto_score", 0) == results.get("auto_points_possible", 0):
        return 0, "Pass"

    checks = results.get("checks", [])
    has_stream_error = _detect_stream_error(results_dir)

    # Category 1: No Solution Produced
    solution_path = os.path.join(results_dir, "solution.py")
    if not os.path.exists(solution_path):
        if has_stream_error:
            return 1.1, "No Solution Produced (Stream Error)"
        # Check for timeout (exit code 142 in run_meta)
        run_meta_path = os.path.join(results_dir, "run_meta.json")
        if os.path.exists(run_meta_path):
            try:
                with open(run_meta_path) as f:
                    meta = json.load(f)
                if meta.get("exit_code") == 142:
                    return 1.2, "No Solution Produced (Timeout)"
            except Exception:
                pass
        # Check for empty transcript (runner crash)
        transcript_path = os.path.join(results_dir, "transcript.json")
        if not os.path.exists(transcript_path) or os.path.getsize(transcript_path) < 10:
            return 1.1, "No Solution Produced (Runner Crash)"
        return 1, "No Solution Produced"

    # Category 2: Execution Failure
    code_runs_check = next((c for c in checks if c["label"] == "code_runs"), None)
    if code_runs_check and not code_runs_check["passed"]:
        error_msg = results.get("execution_error", "")
        if has_stream_error:
            return 2.1, f"Execution Failure (Stream Truncation): {error_msg[:100] if error_msg else 'unknown'}"
        return 2, f"Execution Failure: {error_msg[:120] if error_msg else 'unknown error'}"

    # Category 5: Incomplete Generation
    # Code exists and didn't crash, but produced no stdout (empty output)
    non_exec_checks = [c for c in checks if c["type"] != "execution" and c["type"] != "file_exists"]
    all_no_output = all(
        "did not produce output" in c.get("detail", "") or "Pattern not found" in c.get("detail", "")
        for c in non_exec_checks
    ) if non_exec_checks else False
    if all_no_output and non_exec_checks:
        # Verify it's truly empty stdout vs. format mismatch by checking if ANY pattern was found
        any_pattern_found = any(
            "Pattern not found" not in c.get("detail", "") and c["type"] not in ("execution", "file_exists")
            for c in checks if not c["passed"]
        )
        if not any_pattern_found:
            return 5, "Incomplete Generation"

    # Category 3 vs 4: Check failed non-execution, non-file checks
    failed_checks = [c for c in checks if not c["passed"] and c["type"] not in ("execution", "file_exists")]
    format_mismatches = [c for c in failed_checks if "Pattern not found" in c.get("detail", "")]
    value_errors = [c for c in failed_checks if "Pattern not found" not in c.get("detail", "") and c.get("detail", "")]

    # Category 3: Output Format Mismatch — majority of failures are pattern-not-found
    if format_mismatches and len(format_mismatches) >= len(value_errors):
        labels = ", ".join(c["label"] for c in format_mismatches[:3])
        return 3, f"Output Format Mismatch: {labels}"

    # Category 4: Analytical Error — patterns found but values wrong
    if value_errors:
        labels = ", ".join(c["label"] for c in value_errors[:3])
        return 4, f"Analytical Error: {labels}"

    # Category 6: Constraint Violation — failed file_exists checks
    failed_files = [c for c in checks if not c["passed"] and c["type"] == "file_exists"]
    if failed_files:
        filenames = ", ".join(c.get("filename", c["label"]) for c in failed_files)
        return 6, f"Constraint Violation: missing {filenames}"

    # Fallback — format mismatches that were outnumbered by value errors
    if format_mismatches:
        labels = ", ".join(c["label"] for c in format_mismatches[:3])
        return 3, f"Output Format Mismatch: {labels}"

    return 4, "Analytical Error: unclassified point loss"


def score_test(test_dir, results_dir):
    """Score a single test using its checks.json."""
    checks_path = os.path.join(test_dir, "expected", "checks.json")
    if not os.path.exists(checks_path):
        return {"error": f"No checks.json found at {checks_path}", "tier": 2}

    with open(checks_path) as f:
        config = json.load(f)

    # Run solution
    stdout, error = run_solution(results_dir)

    results = {
        "test_id": config["test_id"],
        "tier": config.get("tier", 1),
        "total_points": config.get("total_points", 10),
        "auto_points_possible": config.get("auto_points", 8),
        "human_points_possible": config.get("human_points", 2),
        "checks": [],
        "auto_score": 0,
        "execution_error": error,
    }

    for check in config["checks"]:
        label = check["label"]
        check_type = check["type"]
        points = check.get("points", 1)
        passed = False
        detail = ""

        if check_type == "execution":
            passed = check_execution(stdout, error)
            detail = "Executed successfully" if passed else f"Error: {error}"

        elif check_type == "file_exists":
            passed, detail = check_file_exists(
                results_dir, check["filename"]
            )

        elif stdout is None:
            detail = "Cannot check — solution did not produce output"

        elif check_type == "exact":
            passed, detail = check_exact(
                stdout, check["pattern"], check["expected"]
            )

        elif check_type == "numeric":
            passed, detail = check_numeric(
                stdout,
                check["pattern"],
                check["expected"],
                check.get("tolerance", 0.01),
                absolute_value=check.get("absolute_value", False),
            )

        elif check_type == "range":
            passed, detail = check_range(
                stdout, check["pattern"], check["min"], check["max"]
            )

        elif check_type == "regex":
            passed, detail = check_regex_match(
                stdout,
                check["pattern"],
                check["expected_pattern"],
            )

        score = points if passed else 0
        results["auto_score"] += score
        results["checks"].append(
            {
                "label": label,
                "type": check_type,
                "points": points,
                "passed": passed,
                "score": score,
                "detail": detail,
            }
        )

    # Classify error
    error_cat, error_desc = classify_error(results, results_dir)
    results["error_category"] = error_cat
    results["error_category_int"] = int(error_cat)  # primary category for aggregation
    results["error_description"] = error_desc

    # Include retry metadata if present
    retry_info = _get_retry_info(results_dir)
    if retry_info:
        results["attempts_used"] = retry_info.get("attempts_used", 1)
        results["retry_reasons"] = retry_info.get("retry_reasons", [])
    else:
        results["attempts_used"] = 1
        results["retry_reasons"] = []

    return results


ERROR_CATEGORY_NAMES = {
    0: "Pass",
    1: "No Solution Produced",
    1.1: "No Solution (Stream/Infra)",
    1.2: "No Solution (Timeout)",
    2: "Execution Failure",
    2.1: "Execution Failure (Stream Truncation)",
    3: "Output Format Mismatch",
    4: "Analytical Error",
    5: "Incomplete Generation",
    6: "Constraint Violation",
}


def print_results(results):
    """Pretty-print scoring results."""
    print(f"\n{'='*60}")
    print(f"Test: {results['test_id']}")
    print(f"Tier: {results['tier']}")
    print(f"{'='*60}")

    if results.get("error"):
        print(f"ERROR: {results['error']}")
        return

    for check in results["checks"]:
        status = "PASS" if check["passed"] else "FAIL"
        print(
            f"  [{status}] {check['label']}: "
            f"{check['score']}/{check['points']} — {check['detail']}"
        )

    print(f"\n  Auto Score: {results['auto_score']}/{results['auto_points_possible']}")
    print(f"  Human Review: /{results['human_points_possible']}")
    print(f"  Total Possible: {results['total_points']}")

    error_cat = results.get("error_category", -1)
    error_desc = results.get("error_description", "")
    cat_name = ERROR_CATEGORY_NAMES.get(error_cat, "Unknown")
    attempts = results.get("attempts_used", 1)
    if error_cat == 0:
        attempt_note = f" (after {attempts} attempts)" if attempts > 1 else ""
        print(f"  Classification: PASS{attempt_note}")
    else:
        attempt_note = f" [{attempts} attempts]" if attempts > 1 else ""
        print(f"  Classification: Cat {error_cat} — {cat_name}{attempt_note}")
        print(f"  Detail: {error_desc}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 score_test.py <test_dir> <results_dir>")
        print(
            "Example: python3 score_test.py test-001-cohens-kappa "
            "results/run_id/test-001-cohens-kappa"
        )
        sys.exit(1)

    test_dir = sys.argv[1]
    results_dir = sys.argv[2]

    results = score_test(test_dir, results_dir)
    print_results(results)

    # Save results
    output_path = os.path.join(results_dir, "auto_score.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved to: {output_path}")


if __name__ == "__main__":
    main()
