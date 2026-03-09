#!/bin/bash
# =============================================================================
# SWAT-Bench — Domain 7: Multi-Step Tasks Runner (3 runs per model)
# Runs the 5 multi-step tasks (task-7-*) against all models, 3 times each.
# Usage: ./run_multistep.sh [start_from_model_number]
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"
MODELFILES_DIR="$BASE/config/modelfiles"

OLLAMA_BIN="/home/beperron/.local/ollama-0.17.6/bin/ollama"
export OLLAMA_HOST="http://127.0.0.1:11435"
OLLAMA_PORT=11435
PROXY_PORT=11436

# Models ordered smallest → largest (custom_name:base_repo:base_tag:modelfile)
MODELS=(
    "qwen3.5-9b-q4:qwen3.5:9b:Modelfile.qwen3.5-9b-q4-256k"
    "qwen3.5-9b-q8:qwen3.5:9b-q8_0:Modelfile.qwen3.5-9b-q8-256k"
    "qwen3.5-27b-q4:qwen3.5:27b:Modelfile.qwen3.5-27b-q4-128k"
    "qwen3.5-27b-q8:qwen3.5:27b-q8_0:Modelfile.qwen3.5-27b-q8-128k"
    "qwen3-coder-30b-q4:qwen3-coder:30b:Modelfile.qwen3-coder-30b-256k"
    "qwen3.5-35b-q4:qwen3.5:35b:Modelfile.qwen3.5-35b-q4-128k"
    "qwen3-coder-next-q4:qwen3-coder-next:q4_K_M:Modelfile.qwen3-coder-next-q4-256k"
    "qwen3.5-122b-q4:qwen3.5:122b:Modelfile.qwen3.5-122b-q4-128k"
)

NUM_RUNS=3
START_FROM=${1:-1}
PROXY_PID=""

# Only run task-7-* tasks
export TASK_FILTER="task-7-*"

cleanup() {
    echo "Cleaning up..."
    if [ -n "$PROXY_PID" ] && kill -0 "$PROXY_PID" 2>/dev/null; then
        kill "$PROXY_PID" 2>/dev/null
        wait "$PROXY_PID" 2>/dev/null
    fi
}
trap cleanup EXIT

start_proxy() {
    if [ -n "$PROXY_PID" ] && kill -0 "$PROXY_PID" 2>/dev/null; then
        kill "$PROXY_PID" 2>/dev/null
        wait "$PROXY_PID" 2>/dev/null
        sleep 1
    fi
    pkill -f "ollama_nothink_proxy" 2>/dev/null || true
    sleep 1

    echo "  Starting nothink proxy on port $PROXY_PORT -> $OLLAMA_PORT..."
    python3 "$SCRIPT_DIR/ollama_nothink_proxy.py" "$PROXY_PORT" "$OLLAMA_PORT" &
    PROXY_PID=$!
    sleep 2

    if ! kill -0 "$PROXY_PID" 2>/dev/null; then
        echo "  ERROR: Proxy failed to start"
        return 1
    fi
    echo "  Proxy running (PID $PROXY_PID)"
}

wait_for_ollama() {
    local waited=0
    while ! curl -sf "http://127.0.0.1:$OLLAMA_PORT/api/tags" > /dev/null 2>&1; do
        if [ $waited -ge 60 ]; then
            echo "  ERROR: Ollama not responding after 60s"
            return 1
        fi
        [ $waited -eq 0 ] && echo "  Waiting for Ollama..."
        sleep 5
        waited=$((waited + 5))
    done
}

# Check if a specific run is already complete (5 scored tasks)
is_run_complete() {
    local run_dir="$1"
    if [ ! -d "$run_dir" ]; then
        return 1
    fi
    local scored
    scored=$(ls "$run_dir"/task-*/auto_score.json 2>/dev/null | wc -l)
    [ "$scored" -ge 5 ]
}

mkdir -p "$BASE/results/qwen"

echo "============================================"
echo "SWAT-Bench — Domain 7: Multi-Step Tasks"
echo "Models: ${#MODELS[@]}"
echo "Runs per model: $NUM_RUNS"
echo "Tasks per run: 5 (83 points)"
echo "Started: $(date)"
echo "============================================"
echo ""

MODEL_NUM=0
for entry in "${MODELS[@]}"; do
    MODEL_NUM=$((MODEL_NUM + 1))

    IFS=':' read -r MODEL_NAME BASE_REPO BASE_TAG MODELFILE <<< "$entry"
    BASE_MODEL="$BASE_REPO:$BASE_TAG"
    OLLAMA_MODEL="$MODEL_NAME"

    if [ $MODEL_NUM -lt $START_FROM ]; then
        echo "[$MODEL_NUM/${#MODELS[@]}] $MODEL_NAME — SKIPPING (start_from=$START_FROM)"
        echo ""
        continue
    fi

    echo "============================================"
    echo "[$MODEL_NUM/${#MODELS[@]}] $MODEL_NAME"
    echo "  Base: $BASE_MODEL"
    echo "  Modelfile: $MODELFILE"
    echo "  Started: $(date)"
    echo "============================================"

    # Ensure base model is available
    echo "  Verifying $BASE_MODEL..."
    if ! $OLLAMA_BIN pull "$BASE_MODEL" 2>&1; then
        echo "  ERROR: Failed to pull $BASE_MODEL — skipping"
        echo ""
        continue
    fi

    # Create custom model from modelfile
    echo "  Creating Ollama model: $OLLAMA_MODEL..."
    if ! $OLLAMA_BIN create "$OLLAMA_MODEL" -f "$MODELFILES_DIR/$MODELFILE" 2>&1; then
        echo "  ERROR: Failed to create $OLLAMA_MODEL — skipping"
        echo ""
        continue
    fi

    wait_for_ollama || continue
    start_proxy || continue

    export OPENAI_BASE_URL="http://127.0.0.1:$PROXY_PORT/v1"
    export OPENAI_API_KEY="ollama"
    export TASK_TIMEOUT=1800

    # Run 3 consecutive runs for this model
    for RUN_NUM in $(seq 1 $NUM_RUNS); do
        RUN_LABEL="${MODEL_NAME}-multistep-run${RUN_NUM}"
        RUN_DIR="$BASE/results/qwen/$RUN_LABEL"

        # Skip if this specific run is already complete
        if is_run_complete "$RUN_DIR"; then
            echo "  [Run $RUN_NUM/$NUM_RUNS] ALREADY COMPLETE, skipping"
            continue
        fi

        echo ""
        echo "  ── Run $RUN_NUM/$NUM_RUNS ──────────────────────────────────"
        echo "  Run ID: $RUN_LABEL"
        echo "  Started: $(date)"

        cd "$SCRIPT_DIR"
        bash run_exam.sh "$OLLAMA_MODEL" "$RUN_LABEL" 2>&1 | tee "$BASE/results/qwen/${RUN_LABEL}_run.log"

        # Score the run
        if [ -d "$RUN_DIR" ]; then
            echo "  Scoring run: $RUN_LABEL"
            bash score_exam.sh "$RUN_LABEL" qwen 2>&1 | tee -a "$BASE/results/qwen/${RUN_LABEL}_run.log"
        fi

        echo "  Run $RUN_NUM completed: $(date)"
    done

    # Unload model to free VRAM
    echo "  Unloading model..."
    curl -sf http://127.0.0.1:$OLLAMA_PORT/api/generate -d "{\"model\":\"$OLLAMA_MODEL\",\"keep_alive\":0}" > /dev/null 2>&1
    sleep 5

    echo ""
    echo "  All $NUM_RUNS runs completed for $MODEL_NAME at $(date)"
    echo ""
done

echo "============================================"
echo "Domain 7 multi-step tasks complete: $(date)"
echo "Results: $BASE/results/qwen/"
echo "============================================"

# Print summary
echo ""
echo "=== MULTI-STEP RESULTS SUMMARY ==="
python3 << 'PYEOF'
import json, glob, os
from collections import defaultdict

base = os.environ.get("BASE", ".")
models = defaultdict(list)

for d in sorted(glob.glob(os.path.join(base, "results/qwen/*-multistep-run*"))):
    if not os.path.isdir(d):
        continue
    dirname = os.path.basename(d)
    # Parse: model-multistep-runN
    parts = dirname.rsplit("-multistep-run", 1)
    if len(parts) != 2:
        continue
    model_name = parts[0]
    run_num = parts[1]

    scores = glob.glob(os.path.join(d, "task-*/auto_score.json"))
    if not scores:
        continue
    total = sum(json.load(open(f))["auto_score"] for f in scores)
    possible = sum(json.load(open(f))["auto_points_possible"] for f in scores)
    models[model_name].append({"run": run_num, "earned": total, "possible": possible})

if models:
    print(f"{'Model':<25} {'Run1':>8} {'Run2':>8} {'Run3':>8} {'Mean':>8} {'Range':>8}")
    print("=" * 70)
    for model in sorted(models.keys()):
        runs = sorted(models[model], key=lambda x: x["run"])
        scores = [r["earned"] for r in runs]
        possible = runs[0]["possible"] if runs else 83
        row = f"{model:<25}"
        for r in runs:
            row += f"{r['earned']:>5.1f}/{possible:<2}"
        # Pad missing runs
        for _ in range(3 - len(runs)):
            row += f"{'--':>8}"
        if len(scores) > 1:
            mean = sum(scores) / len(scores)
            rng = max(scores) - min(scores)
            row += f"  {mean:>5.1f}  {rng:>5.1f}"
        print(row)
else:
    print("No results yet.")
PYEOF
