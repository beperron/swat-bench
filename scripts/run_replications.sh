#!/bin/bash
# =============================================================================
# SWAT-Bench — Replication Runner (breadth-first)
# Loops SEEDS first, MODELS second — so you get one full comparison run
# across all models before starting the next seed.
# Usage: ./run_replications.sh [start_from_combo_number]
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"
MODELFILES_DIR="$BASE/config/modelfiles"

OLLAMA_BIN="/home/beperron/.local/ollama-0.17.6/bin/ollama"
export OLLAMA_HOST="http://127.0.0.1:11435"
OLLAMA_PORT=11435
PROXY_PORT=11436

SEEDS=(42 123 456)

# Models ordered smallest → largest (custom_name:base_repo:base_tag:modelfile_base)
MODELS=(
    "qwen3.5-9b-q4:qwen3.5:9b:Modelfile.qwen3.5-9b-q4-256k"
    "qwen3.5-9b-q8:qwen3.5:9b-q8_0:Modelfile.qwen3.5-9b-q8-256k"
    "qwen3.5-27b-q4:qwen3.5:27b:Modelfile.qwen3.5-27b-q4-128k"
    "qwen3-coder-30b-q4:qwen3-coder:30b:Modelfile.qwen3-coder-30b-256k"
    "qwen3.5-35b-q4:qwen3.5:35b:Modelfile.qwen3.5-35b-q4-128k"
    "qwen3-coder-next-q4:qwen3-coder-next:q4_K_M:Modelfile.qwen3-coder-next-q4-256k"
    "qwen3.5-122b-q4:qwen3.5:122b:Modelfile.qwen3.5-122b-q4-128k"
)

START_FROM=${1:-1}
PROXY_PID=""

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

# Check if a seed run is already complete (51 scored tasks)
is_run_complete() {
    local seeded_model="$1"
    local run_dir
    run_dir=$(ls -1dt "$BASE/results/qwen/${seeded_model}_"* 2>/dev/null | grep -v "_run.log" | head -1)
    if [ -z "$run_dir" ]; then
        return 1
    fi
    local scored
    scored=$(ls "$run_dir"/task-*/auto_score.json 2>/dev/null | wc -l)
    [ "$scored" -ge 51 ]
}

TOTAL_COMBOS=$(( ${#SEEDS[@]} * ${#MODELS[@]} ))
mkdir -p "$BASE/results/qwen"

echo "============================================"
echo "SWAT-Bench — Replication Suite (breadth-first)"
echo "Seeds: ${SEEDS[*]}"
echo "Models: ${#MODELS[@]}"
echo "Total runs: $TOTAL_COMBOS (${#SEEDS[@]} seeds x ${#MODELS[@]} models)"
echo "Tasks per run: 51"
echo "Started: $(date)"
echo "============================================"
echo ""

COMBO_NUM=0
for SEED in "${SEEDS[@]}"; do
    echo ""
    echo "======== SEED $SEED — All models ========"
    echo ""

    for entry in "${MODELS[@]}"; do
        COMBO_NUM=$((COMBO_NUM + 1))

        IFS=':' read -r MODEL_NAME BASE_REPO BASE_TAG BASE_MODELFILE <<< "$entry"
        BASE_MODEL="$BASE_REPO:$BASE_TAG"
        SEEDED_MODEL="${MODEL_NAME}-seed${SEED}"

        if [ $COMBO_NUM -lt $START_FROM ]; then
            echo "[$COMBO_NUM/$TOTAL_COMBOS] $SEEDED_MODEL — SKIPPING (start_from=$START_FROM)"
            echo ""
            continue
        fi

        # Skip if already completed
        if is_run_complete "$SEEDED_MODEL"; then
            echo "[$COMBO_NUM/$TOTAL_COMBOS] $SEEDED_MODEL — ALREADY COMPLETE, skipping"
            echo ""
            continue
        fi

        SEEDED_MODELFILE="/tmp/Modelfile.${SEEDED_MODEL}"

        echo "============================================"
        echo "[$COMBO_NUM/$TOTAL_COMBOS] $SEEDED_MODEL"
        echo "  Base: $BASE_MODEL"
        echo "  Seed: $SEED"
        echo "  Started: $(date)"
        echo "============================================"

        # Create seeded modelfile by appending PARAMETER seed
        cp "$MODELFILES_DIR/$BASE_MODELFILE" "$SEEDED_MODELFILE"
        echo "PARAMETER seed $SEED" >> "$SEEDED_MODELFILE"

        # Ensure base model is available
        echo "  Verifying $BASE_MODEL..."
        if ! $OLLAMA_BIN pull "$BASE_MODEL" 2>&1; then
            echo "  ERROR: Failed to pull $BASE_MODEL — skipping"
            echo ""
            continue
        fi

        # Create seeded custom model
        echo "  Creating Ollama model: $SEEDED_MODEL..."
        if ! $OLLAMA_BIN create "$SEEDED_MODEL" -f "$SEEDED_MODELFILE" 2>&1; then
            echo "  ERROR: Failed to create $SEEDED_MODEL — skipping"
            echo ""
            continue
        fi

        wait_for_ollama || continue
        start_proxy || continue

        echo "  Running 51 tasks..."
        export OPENAI_BASE_URL="http://127.0.0.1:$PROXY_PORT/v1"
        export OPENAI_API_KEY="ollama"
        export TASK_TIMEOUT=900

        cd "$SCRIPT_DIR"
        bash run_exam.sh "$SEEDED_MODEL" 2>&1 | tee "$BASE/results/qwen/${SEEDED_MODEL}_run.log"

        # Score the run
        RUN_ID=$(ls -1t "$BASE/results/qwen/" | grep "^${SEEDED_MODEL}" | grep -v "_run.log" | head -1)
        if [ -n "$RUN_ID" ]; then
            echo "  Scoring run: $RUN_ID"
            bash score_exam.sh "$RUN_ID" qwen 2>&1 | tee -a "$BASE/results/qwen/${SEEDED_MODEL}_run.log"
        fi

        # Unload model
        echo "  Unloading model..."
        curl -sf http://127.0.0.1:$OLLAMA_PORT/api/generate -d "{\"model\":\"$SEEDED_MODEL\",\"keep_alive\":0}" > /dev/null 2>&1

        # Clean up seeded model (base stays)
        $OLLAMA_BIN rm "$SEEDED_MODEL" 2>/dev/null || true
        rm -f "$SEEDED_MODELFILE"
        sleep 3

        echo ""
        echo "  Completed: $SEEDED_MODEL at $(date)"
        echo ""
    done

    echo ""
    echo "======== SEED $SEED — Complete at $(date) ========"
    echo ""
done

echo "============================================"
echo "All replications complete: $(date)"
echo "Results: $BASE/results/qwen/"
echo "============================================"
