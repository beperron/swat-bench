#!/bin/bash
# =============================================================================
# SWAT-Bench Exam — Master Runner
# Runs exam tasks sequentially using Qwen Code CLI in YOLO mode
# Includes retry logic (up to 3 attempts) for stream errors and timeouts
# Usage: ./run_exam.sh [model_name] [run_id_to_resume]
# Set TASK_FILTER env var to restrict which tasks run (e.g. "task-7-*")
# =============================================================================

MODEL="${1:-gpt-oss:20b}"
# If RUN_ID passed (resume), reuse it; otherwise generate a new one
if [ -n "$2" ]; then
    RUN_ID="$2"
else
    RUN_ID="${MODEL}_$(date +%Y-%m-%d_%H%M)"
    # Sanitize RUN_ID for use as directory name
    RUN_ID=$(echo "$RUN_ID" | tr ':' '-')
fi
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"
TASKS_DIR="$BASE/tasks"

echo "============================================"
echo "SWAT-Bench Exam — LLM Benchmark Suite (Qwen)"
echo "Model: $MODEL"
echo "Run ID: $RUN_ID"
echo "Started: $(date)"
echo "============================================"
echo ""

FRAMEWORK="qwen"
mkdir -p "$BASE/results/$FRAMEWORK/$RUN_ID"

TOTAL_TESTS=0
COMPLETED_TESTS=0
GRAND_INPUT_TOKENS=0
GRAND_OUTPUT_TOKENS=0
GRAND_DURATION=0
# Task filter: set TASK_FILTER="task-7-*" to run only Domain 7, etc.
TASK_GLOB="${TASK_FILTER:-task-*}"
NUM_TESTS=$(ls -d "$TASKS_DIR"/$TASK_GLOB/ 2>/dev/null | wc -l | tr -d ' ')

for T in "$TASKS_DIR"/$TASK_GLOB/; do
    NAME=$(basename "$T")
    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    echo "=== [$TOTAL_TESTS/$NUM_TESTS] $NAME ==="
    echo "  Setting up workspace..."

    # Clean and create workspace
    rm -rf "$T/workspace"
    mkdir -p "$T/workspace"

    # Copy input files (follow symlinks)
    if [ -d "$T/input" ] && [ "$(ls -A "$T/input" 2>/dev/null)" ]; then
        cp -L "$T"/input/* "$T/workspace/" 2>/dev/null
        FILE_COUNT=$(ls "$T/workspace/" | wc -l | tr -d ' ')
        echo "  Copied $FILE_COUNT input file(s)"
    else
        echo "  No input files (API-only task)"
    fi

    # Copy context file as QWEN.md
    if [ -f "$BASE/config/agent_context.md" ]; then
        cp "$BASE/config/agent_context.md" "$T/workspace/QWEN.md"
    fi

    # Create results directory for this task
    RESULT_DIR="$BASE/results/$FRAMEWORK/$RUN_ID/$NAME"
    mkdir -p "$RESULT_DIR"

    # CHECKPOINT: skip tasks that completed successfully
    # Must have transcript AND solution.py (a bare transcript from a killed run shouldn't count)
    if [ -f "$RESULT_DIR/transcript.json" ] && [ -f "$RESULT_DIR/solution.py" ]; then
        echo "  CHECKPOINT: Already completed — skipping"
        if [ -f "$RESULT_DIR/run_meta.json" ]; then
            TOKENS_IN=$(python3 -c "import json; print(json.load(open('$RESULT_DIR/run_meta.json'))['tokens']['input'])" 2>/dev/null || echo 0)
            TOKENS_OUT=$(python3 -c "import json; print(json.load(open('$RESULT_DIR/run_meta.json'))['tokens']['output'])" 2>/dev/null || echo 0)
            ELAPSED=$(python3 -c "import json; print(int(json.load(open('$RESULT_DIR/run_meta.json'))['duration_seconds']))" 2>/dev/null || echo 0)
            GRAND_INPUT_TOKENS=$((GRAND_INPUT_TOKENS + TOKENS_IN))
            GRAND_OUTPUT_TOKENS=$((GRAND_OUTPUT_TOKENS + TOKENS_OUT))
            GRAND_DURATION=$((GRAND_DURATION + ELAPSED))
        fi
        COMPLETED_TESTS=$((COMPLETED_TESTS + 1))
        echo ""
        continue
    fi

    # Health check: wait for Ollama before launching qwen
    # Always check Ollama directly (not the proxy) for health
    HEALTH_WAITED=0
    while ! curl -sf "http://127.0.0.1:11435/api/tags" > /dev/null 2>&1; do
        if [ $HEALTH_WAITED -ge 120 ]; then
            echo "  SKIP: Ollama not responding after 120s"
            echo ""
            continue 2
        fi
        [ $HEALTH_WAITED -eq 0 ] && echo "  Waiting for Ollama..."
        sleep 5
        HEALTH_WAITED=$((HEALTH_WAITED + 5))
    done

    # ── Retry loop: up to 3 attempts per task ──────────────────────────
    # Retries handle infrastructure failures (stream errors, timeouts)
    # where the model never got a fair chance to produce code.
    # Each retry uses an increasingly direct prompt prefix that changes
    # the model's trajectory (effectively acting as a different "seed").
    # Retry metadata is saved so both first-attempt and retry-adjusted
    # scores can be reported.
    MAX_ATTEMPTS=3
    ATTEMPT=0
    RETRY_REASONS=()
    while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
        ATTEMPT=$((ATTEMPT + 1))
        if [ $ATTEMPT -gt 1 ]; then
            echo "  ── Retry $ATTEMPT/$MAX_ATTEMPTS ──"
        fi

        # Clean workspace for each attempt
        rm -rf "$T/workspace"
        mkdir -p "$T/workspace"
        if [ -d "$T/input" ] && [ "$(ls -A "$T/input" 2>/dev/null)" ]; then
            cp -L "$T"/input/* "$T/workspace/" 2>/dev/null
        fi
        if [ -f "$BASE/config/agent_context.md" ]; then
            cp "$BASE/config/agent_context.md" "$T/workspace/QWEN.md"
        fi

        # Build prompt — add retry prefix on attempts 2+
        PROMPT_TEXT=$(cat "$T/prompt.md")
        if [ $ATTEMPT -eq 2 ]; then
            PROMPT_TEXT="IMPORTANT: Write your solution.py file as your very first action. Do not spend time reading files or planning — write working code immediately, then refine.

${PROMPT_TEXT}"
        elif [ $ATTEMPT -ge 3 ]; then
            PROMPT_TEXT="CRITICAL: Your previous attempt failed due to a timeout. You MUST create solution.py immediately as your first tool call. Write the complete solution in a single file write — do not read input files first, use the filenames from the prompt directly. Keep your solution simple and direct.

${PROMPT_TEXT}"
        fi

        echo "  Running qwen (YOLO mode, attempt $ATTEMPT)..."
        START_TIME=$(date +%s)

        # Run the LLM with timeout
        cd "$T/workspace"
        qwen "$PROMPT_TEXT" --yolo --output-format json --model "$MODEL" \
          --auth-type openai \
          --openai-base-url "${OPENAI_BASE_URL:-http://127.0.0.1:11436/v1}" \
          --openai-api-key "${OPENAI_API_KEY:-ollama}" \
          > "$RESULT_DIR/transcript.json" 2>&1 &
        QWEN_PID=$!

        # Wait up to TASK_TIMEOUT seconds, then kill the process tree
        TIMEOUT=${TASK_TIMEOUT:-300}
        WAITED=0
        while kill -0 "$QWEN_PID" 2>/dev/null; do
            if [ $WAITED -ge $TIMEOUT ]; then
                echo "  Timeout after ${TIMEOUT}s — killing qwen (PID $QWEN_PID)..."
                pkill -P "$QWEN_PID" 2>/dev/null
                kill "$QWEN_PID" 2>/dev/null
                sleep 2
                kill -9 "$QWEN_PID" 2>/dev/null
                pkill -9 -P "$QWEN_PID" 2>/dev/null
                EXIT_CODE=142
                break
            fi
            sleep 5
            WAITED=$((WAITED + 5))
        done
        if [ $WAITED -lt $TIMEOUT ]; then
            wait "$QWEN_PID"
            EXIT_CODE=$?
        fi

        END_TIME=$(date +%s)
        ELAPSED=$((END_TIME - START_TIME))

        # Copy workspace output to results
        cp -r "$T/workspace/"* "$RESULT_DIR/" 2>/dev/null

        # ── Decide whether to retry ──────────────────────────────────
        NEEDS_RETRY=false
        RETRY_REASON=""

        # Detect stream errors in transcript
        HAS_STREAM_ERR=false
        if grep -qE "Streaming request timeout|stream ended" "$RESULT_DIR/transcript.json" 2>/dev/null; then
            HAS_STREAM_ERR=true
        fi

        # Case 1: No solution.py at all
        if [ ! -f "$RESULT_DIR/solution.py" ]; then
            if [ "$HAS_STREAM_ERR" = true ]; then
                NEEDS_RETRY=true
                RETRY_REASON="stream_error_no_solution"
                echo "  Stream error — no solution.py produced (${ELAPSED}s)"
            elif [ $EXIT_CODE -eq 142 ]; then
                NEEDS_RETRY=true
                RETRY_REASON="timeout_no_solution"
                echo "  Timeout — no solution.py produced (${ELAPSED}s)"
            elif [ ! -s "$RESULT_DIR/transcript.json" ]; then
                NEEDS_RETRY=true
                RETRY_REASON="empty_transcript"
                echo "  Empty transcript — runner crash (${ELAPSED}s)"
            fi
        # Case 2: solution.py exists but stream error truncated it
        elif [ "$HAS_STREAM_ERR" = true ]; then
            # Test if the solution actually runs
            SOLUTION_RUNS=false
            python3 -c "import py_compile; py_compile.compile('$RESULT_DIR/solution.py', doraise=True)" 2>/dev/null && SOLUTION_RUNS=true
            if [ "$SOLUTION_RUNS" = false ]; then
                NEEDS_RETRY=true
                RETRY_REASON="stream_error_truncated_solution"
                echo "  Stream error — solution.py has syntax errors from truncation (${ELAPSED}s)"
            fi
        fi

        # If no retry needed (success or genuine failure), stop
        if [ "$NEEDS_RETRY" = false ]; then
            break
        fi

        # Record retry reason
        RETRY_REASONS+=("$RETRY_REASON")

        # If more attempts remain, clean up and continue
        if [ $ATTEMPT -lt $MAX_ATTEMPTS ]; then
            echo "  Cleaning up for retry..."
            rm -f "$RESULT_DIR/transcript.json" "$RESULT_DIR/run_meta.json"
            rm -f "$RESULT_DIR/solution.py" "$RESULT_DIR/summary.md"
            # Remove any generated output files
            find "$RESULT_DIR" -maxdepth 1 -name "*.csv" -newer "$RESULT_DIR" -delete 2>/dev/null
            sleep 3
        else
            echo "  All $MAX_ATTEMPTS attempts exhausted"
        fi
    done

    # Save retry metadata
    if [ $ATTEMPT -gt 1 ] || [ ${#RETRY_REASONS[@]} -gt 0 ]; then
        python3 -c "
import json
meta = {
    'attempts_used': $ATTEMPT,
    'max_attempts': $MAX_ATTEMPTS,
    'retry_reasons': $(python3 -c "import json; print(json.dumps('${RETRY_REASONS[*]:-}'.split()))"),
    'final_has_solution': $([ -f "$RESULT_DIR/solution.py" ] && echo 'True' || echo 'False'),
}
with open('$RESULT_DIR/retry_meta.json', 'w') as f:
    json.dump(meta, f, indent=2)
" 2>/dev/null
    fi

    if [ $EXIT_CODE -eq 124 ]; then
        echo "  Exit code: $EXIT_CODE (TIMEOUT after 900s)"
        echo "  Wall time: ${ELAPSED}s"
        echo "  Status: TIMEOUT"
    else
        echo "  Exit code: $EXIT_CODE"
        echo "  Wall time: ${ELAPSED}s"
    fi

    # Extract metrics from transcript
    python3 "$SCRIPT_DIR/extract_metrics.py" "$RESULT_DIR/transcript.json" "$NAME" "$MODEL" "$EXIT_CODE"

    # Patch wall time into run_meta.json (extract_metrics may not capture it)
    if [ -f "$RESULT_DIR/run_meta.json" ]; then
        python3 -c "
import json
with open('$RESULT_DIR/run_meta.json') as f:
    d = json.load(f)
if d.get('duration_seconds', 0) == 0:
    d['duration_seconds'] = $ELAPSED
    d['duration_ms'] = $ELAPSED * 1000
with open('$RESULT_DIR/run_meta.json', 'w') as f:
    json.dump(d, f, indent=2)
" 2>/dev/null
    fi

    # Accumulate totals from run_meta.json
    if [ -f "$RESULT_DIR/run_meta.json" ]; then
        TOKENS_IN=$(python3 -c "import json; print(json.load(open('$RESULT_DIR/run_meta.json'))['tokens']['input'])" 2>/dev/null || echo 0)
        TOKENS_OUT=$(python3 -c "import json; print(json.load(open('$RESULT_DIR/run_meta.json'))['tokens']['output'])" 2>/dev/null || echo 0)
        GRAND_INPUT_TOKENS=$((GRAND_INPUT_TOKENS + TOKENS_IN))
        GRAND_OUTPUT_TOKENS=$((GRAND_OUTPUT_TOKENS + TOKENS_OUT))
    fi
    GRAND_DURATION=$((GRAND_DURATION + ELAPSED))

    if [ $EXIT_CODE -eq 0 ]; then
        COMPLETED_TESTS=$((COMPLETED_TESTS + 1))
        echo "  Status: COMPLETED"
    elif [ $EXIT_CODE -ne 124 ]; then
        echo "  Status: FAILED (exit code $EXIT_CODE)"
    fi
    echo ""
done

cd "$SCRIPT_DIR"

# Generate run summary
GRAND_TOTAL_TOKENS=$((GRAND_INPUT_TOKENS + GRAND_OUTPUT_TOKENS))
python3 -c "
import json, os, glob

run_dir = '$BASE/results/$FRAMEWORK/$RUN_ID'
tasks = []
for f in sorted(glob.glob(os.path.join(run_dir, 'task-*/run_meta.json'))):
    tasks.append(json.load(open(f)))

summary = {
    'run_id': '$RUN_ID',
    'model': '$MODEL',
    'framework': '$FRAMEWORK',
    'total_tasks': len(tasks),
    'completed': sum(1 for t in tasks if t['exit_code'] == 0),
    'total_duration_seconds': sum(t['duration_seconds'] for t in tasks),
    'total_tokens': {
        'input': sum(t['tokens']['input'] for t in tasks),
        'output': sum(t['tokens']['output'] for t in tasks),
        'total': sum(t['tokens']['total'] for t in tasks),
    },
    'total_tool_calls': sum(t['tools']['total_calls'] for t in tasks),
    'total_lines_added': sum(t['files']['lines_added'] for t in tasks),
    'tasks': [{
        'task': t['test'],
        'duration_s': t['duration_seconds'],
        'tokens': t['tokens']['total'],
        'tools': t['tools']['total_calls'],
        'lines': t['files']['lines_added'],
        'error': t['is_error'],
    } for t in tasks]
}

with open(os.path.join(run_dir, 'run_summary.json'), 'w') as f:
    json.dump(summary, f, indent=2)

# Print summary table
print()
print(f'{\"Task\":<45} {\"Time\":>7} {\"Tokens\":>10} {\"Tools\":>6} {\"Lines\":>6}')
print('-' * 80)
for t in summary['tasks']:
    print(f'{t[\"task\"]:<45} {t[\"duration_s\"]:>6.1f}s {t[\"tokens\"]:>10,} {t[\"tools\"]:>6} {t[\"lines\"]:>6}')
print('-' * 80)
st = summary['total_tokens']
print(f'{\"TOTAL\":<45} {summary[\"total_duration_seconds\"]:>6.1f}s {st[\"total\"]:>10,} {summary[\"total_tool_calls\"]:>6} {summary[\"total_lines_added\"]:>6}')
"

echo ""
echo "============================================"
echo "Run complete: $COMPLETED_TESTS/$TOTAL_TESTS tasks finished"
echo "Total wall time: ${GRAND_DURATION}s ($((GRAND_DURATION / 60))m $((GRAND_DURATION % 60))s)"
echo "Total tokens: $GRAND_TOTAL_TOKENS ($GRAND_INPUT_TOKENS in / $GRAND_OUTPUT_TOKENS out)"
echo "Results: $BASE/results/$FRAMEWORK/$RUN_ID"
echo "Finished: $(date)"
echo "============================================"
echo ""
echo "Next step: ./score_exam.sh $RUN_ID $FRAMEWORK"
