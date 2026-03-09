#!/bin/bash
# =============================================================================
# SWAT-Bench — Run all models sequentially
# All models are pre-pulled. For each model: creates Ollama config,
# starts nothink proxy, runs all 51 tasks, scores, then moves to next.
# Ordered smallest → largest for fastest results first.
# Usage: ./run_all_models.sh [start_from_model_number]
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"
MODELFILES_DIR="$BASE/config/modelfiles"

# Ollama binary and host (0.17.6 on port 11435)
OLLAMA_BIN="/home/beperron/.local/ollama-0.17.6/bin/ollama"
export OLLAMA_HOST="http://127.0.0.1:11435"
OLLAMA_PORT=11435
PROXY_PORT=11436

# Models ordered smallest → largest (custom_name:base_repo:base_tag:modelfile)
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
    # Kill any existing proxy
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

# Ensure results directory exists
mkdir -p "$BASE/results/qwen"

echo "============================================"
echo "SWAT-Bench — Full Model Benchmark Suite"
echo "Models: ${#MODELS[@]}"
echo "Tasks per model: 51"
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

    # Step 1: Ensure base model is available (no-op if already pulled)
    echo "  Verifying $BASE_MODEL..."
    if ! $OLLAMA_BIN pull "$BASE_MODEL" 2>&1; then
        echo "  ERROR: Failed to pull $BASE_MODEL — skipping"
        echo ""
        continue
    fi

    # Step 2: Create custom model from modelfile
    echo "  Creating Ollama model: $OLLAMA_MODEL..."
    if ! $OLLAMA_BIN create "$OLLAMA_MODEL" -f "$MODELFILES_DIR/$MODELFILE" 2>&1; then
        echo "  ERROR: Failed to create $OLLAMA_MODEL — skipping"
        echo ""
        continue
    fi

    # Step 3: Ensure Ollama is ready
    wait_for_ollama || continue

    # Step 4: Start proxy
    start_proxy || continue

    # Step 5: Run the benchmark
    echo "  Running 51 tasks..."
    export OPENAI_BASE_URL="http://127.0.0.1:$PROXY_PORT/v1"
    export OPENAI_API_KEY="ollama"
    export TASK_TIMEOUT=900

    cd "$SCRIPT_DIR"
    bash run_exam.sh "$OLLAMA_MODEL" 2>&1 | tee "$BASE/results/qwen/${OLLAMA_MODEL}_run.log"

    # Step 6: Score the run
    RUN_ID=$(ls -1t "$BASE/results/qwen/" | grep "^${OLLAMA_MODEL}" | grep -v "_run.log" | head -1)
    if [ -n "$RUN_ID" ]; then
        echo "  Scoring run: $RUN_ID"
        bash score_exam.sh "$RUN_ID" qwen 2>&1 | tee -a "$BASE/results/qwen/${OLLAMA_MODEL}_run.log"
    fi

    # Step 7: Unload model to free VRAM
    echo "  Unloading model..."
    curl -sf http://127.0.0.1:$OLLAMA_PORT/api/generate -d "{\"model\":\"$OLLAMA_MODEL\",\"keep_alive\":0}" > /dev/null 2>&1
    sleep 5

    echo ""
    echo "  Completed: $MODEL_NAME at $(date)"
    echo ""
done

echo "============================================"
echo "All models complete: $(date)"
echo "Results: $BASE/results/qwen/"
echo "============================================"
echo ""
echo "Starting replications..."
echo ""
cd "$SCRIPT_DIR"
bash run_replications.sh
