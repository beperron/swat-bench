#!/bin/bash
# =============================================================================
# SWAT-Bench Exam — Score All Tasks
# Runs auto-scoring for all 51 exam tasks and prints a summary with metrics
# Usage: ./score_exam.sh <run_id> [framework]
#   framework: "qwen" (default) or "goose"
# Example: ./score_exam.sh gpt-oss-20b_2026-03-01_1430 qwen
# =============================================================================

if [ -z "$1" ]; then
    echo "Usage: ./score_exam.sh <run_id> [framework]"
    echo "  framework: qwen (default) or goose"
    echo ""
    echo "Available runs:"
    echo "  Qwen:"
    ls ../results/qwen/ 2>/dev/null || echo "    (none)"
    echo "  Goose:"
    ls ../results/goose/ 2>/dev/null || echo "    (none)"
    exit 1
fi

RUN_ID="$1"
FRAMEWORK="${2:-qwen}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"
TASKS_DIR="$BASE/tasks"
RESULTS_BASE="$BASE/results/$FRAMEWORK/$RUN_ID"

if [ ! -d "$RESULTS_BASE" ]; then
    echo "Error: Results directory not found: $RESULTS_BASE"
    exit 1
fi

echo "============================================"
echo "SWAT-Bench Exam — Scoring run: $RUN_ID ($FRAMEWORK)"
echo "============================================"
echo ""

TOTAL_AUTO=0
TOTAL_AUTO_POSSIBLE=0

for T in "$TASKS_DIR"/task-*/; do
    NAME=$(basename "$T")
    RESULT_DIR="$RESULTS_BASE/$NAME"

    if [ ! -d "$RESULT_DIR" ]; then
        echo "[$NAME] No results found — skipping"
        continue
    fi

    # Score the task
    if [ -f "$T/expected/checks.json" ]; then
        echo "--- Scoring: $NAME ---"
        python3 "$SCRIPT_DIR/score_test.py" "$T" "$RESULT_DIR"

        # Extract auto score
        if [ -f "$RESULT_DIR/auto_score.json" ]; then
            AUTO=$(python3 -c "import json; d=json.load(open('$RESULT_DIR/auto_score.json')); print(d['auto_score'])")
            POSSIBLE=$(python3 -c "import json; d=json.load(open('$RESULT_DIR/auto_score.json')); print(d['auto_points_possible'])")
            TOTAL_AUTO=$(python3 -c "print($TOTAL_AUTO + $AUTO)")
            TOTAL_AUTO_POSSIBLE=$(python3 -c "print($TOTAL_AUTO_POSSIBLE + $POSSIBLE)")
        fi
    else
        echo "--- $NAME (No checks.json — manual scoring required) ---"
    fi
    echo ""
done

echo ""
echo "============================================"
echo "AUTO-SCORE SUMMARY ($FRAMEWORK): $TOTAL_AUTO / $TOTAL_AUTO_POSSIBLE"
echo "============================================"

# Print combined scorecard with domain groupings
python3 -c "
import json, os, glob
from collections import OrderedDict

run_dir = '$RESULTS_BASE'
tasks_dir = '$TASKS_DIR'

# Define domain order for grouping
DOMAIN_ORDER = [
    'Data Cleaning & Validation',
    'Data Preparation & Transformation',
    'Descriptive Statistics & Measurement',
    'Inferential Statistics',
    'Applied Social Work Analytics',
    'Text & Natural Language Processing',
    'Multi-Step Data Analysis',
]

# Collect all task info grouped by domain
domains = OrderedDict()
for d in DOMAIN_ORDER:
    domains[d] = []

all_tasks = sorted(glob.glob(os.path.join(tasks_dir, 'task-*/')))

for t_dir in all_tasks:
    name = os.path.basename(t_dir.rstrip('/'))
    # Extract domain number from task-X-NN format
    parts = name.split('-')
    task_prefix = f'{parts[0]}-{parts[1]}-{parts[2]}'
    result_dir = os.path.join(run_dir, name)

    # Read checks.json to get domain info
    checks_path = os.path.join(t_dir, 'expected', 'checks.json')
    domain = 'Unknown'
    task_label = name
    if os.path.exists(checks_path):
        cd = json.load(open(checks_path))
        domain = cd.get('domain', 'Unknown')
        task_label = cd.get('task_name', name)

    # Get auto score
    auto = 0
    possible = 0
    auto_str = '--'
    score_file = os.path.join(result_dir, 'auto_score.json')
    if os.path.exists(score_file):
        sd = json.load(open(score_file))
        auto = sd.get('auto_score', 0)
        possible = sd.get('auto_points_possible', 0)
        auto_str = f'{auto}/{possible}'

    # Get metrics
    meta_file = os.path.join(result_dir, 'run_meta.json')
    time_s = 0
    tokens = 0
    tools = 0
    lines = 0
    if os.path.exists(meta_file):
        md = json.load(open(meta_file))
        time_s = md.get('duration_seconds', 0)
        tokens = md.get('tokens', {}).get('total', 0)
        tools = md.get('tools', {}).get('total_calls', 0)
        lines = md.get('files', {}).get('lines_added', 0)

    entry = {
        'id': task_prefix,
        'name': name,
        'task_label': task_label,
        'auto': auto,
        'possible': possible,
        'auto_str': auto_str,
        'time_s': time_s,
        'tokens': tokens,
        'tools': tools,
        'lines': lines,
    }

    if domain in domains:
        domains[domain].append(entry)
    else:
        domains.setdefault('Unknown', []).append(entry)

# Print scorecard
print()
print(f'{\"ID\":<10} {\"Task\":<40} {\"Score\":>8} {\"Time\":>7} {\"Tokens\":>10} {\"Tools\":>6} {\"Lines\":>6}')
print('=' * 85)

grand_auto = 0
grand_possible = 0
grand_time = 0
grand_tokens = 0
grand_tools = 0
grand_lines = 0

for domain, tasks in domains.items():
    if not tasks:
        continue
    print(f'  {domain}')
    print(f'  {\"─\" * 83}')

    domain_auto = 0
    domain_possible = 0

    for t in tasks:
        print(f'{t[\"id\"]:<10} {t[\"name\"]:<40} {t[\"auto_str\"]:>8} {t[\"time_s\"]:>6.1f}s {t[\"tokens\"]:>10,} {t[\"tools\"]:>6} {t[\"lines\"]:>6}')
        domain_auto += t['auto']
        domain_possible += t['possible']
        grand_time += t['time_s']
        grand_tokens += t['tokens']
        grand_tools += t['tools']
        grand_lines += t['lines']

    grand_auto += domain_auto
    grand_possible += domain_possible
    print(f'           {\"Subtotal:\":<39} {domain_auto}/{domain_possible}')
    print()

print('=' * 85)
print(f'           {\"TOTAL\":<39} {grand_auto}/{grand_possible}  {grand_time:>6.1f}s {grand_tokens:>10,} {grand_tools:>6} {grand_lines:>6}')
print()
print(f'Overall: {grand_auto} / {grand_possible} (out of 361 total points)')
if grand_possible > 0:
    print(f'Percentage: {grand_auto/grand_possible*100:.1f}%')
"

# Write score_summary.json for programmatic access
python3 -c "
import json, os, glob

run_dir = '$RESULTS_BASE'
tasks_dir = '$TASKS_DIR'

total_earned = 0
total_possible = 0
task_scores = []
error_counts = {}
retry_count = 0
total_attempts = 0

for t_dir in sorted(glob.glob(os.path.join(tasks_dir, 'task-*/'))):
    name = os.path.basename(t_dir.rstrip('/'))
    score_file = os.path.join(run_dir, name, 'auto_score.json')
    if os.path.exists(score_file):
        sd = json.load(open(score_file))
        earned = sd.get('auto_score', 0)
        possible = sd.get('auto_points_possible', 0)
        total_earned += earned
        total_possible += possible
        cat = sd.get('error_category_int', sd.get('error_category', -1))
        attempts = sd.get('attempts_used', 1)
        total_attempts += attempts
        if attempts > 1:
            retry_count += 1
        task_scores.append({
            'task': name, 'earned': earned, 'possible': possible,
            'error_category': sd.get('error_category', -1),
            'attempts_used': attempts,
        })
        cat_key = str(int(cat)) if cat == int(cat) else str(cat)
        error_counts[cat_key] = error_counts.get(cat_key, 0) + 1

summary = {
    'total_earned': total_earned,
    'total_possible': total_possible,
    'percentage': round(total_earned / total_possible * 100, 1) if total_possible > 0 else 0,
    'error_distribution': error_counts,
    'tasks_with_retries': retry_count,
    'total_attempts': total_attempts,
    'tasks': task_scores,
}
with open(os.path.join(run_dir, 'score_summary.json'), 'w') as f:
    json.dump(summary, f, indent=2)

# Print error distribution
cat_names = {
    '0': 'Pass', '1': 'No Solution', '2': 'Exec Failure',
    '3': 'Format Mismatch', '4': 'Analytical Error',
    '5': 'Incomplete Gen', '6': 'Constraint Violation',
}
print()
print('Error Distribution:')
for cat_key in sorted(error_counts.keys(), key=float):
    name = cat_names.get(cat_key, f'Cat {cat_key}')
    print(f'  Cat {cat_key:>3}: {error_counts[cat_key]:>3}  {name}')
if retry_count > 0:
    print(f'  Retries: {retry_count} tasks needed multiple attempts ({total_attempts} total)')
print(f'Score summary written to {run_dir}/score_summary.json')
"

echo ""
echo "Results directory: $RESULTS_BASE"
