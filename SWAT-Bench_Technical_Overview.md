# SWAT-Bench: Technical Overview of the Agentic Testing Pipeline

## What SWAT-Bench Measures

SWAT-Bench evaluates whether a local language model, operating as an autonomous coding agent, can independently complete structured data analysis tasks drawn from social work research. The benchmark contains 55 tasks across seven domains (data cleaning, transformation, descriptive statistics, inferential statistics, applied analytics, NLP, and multi-step data analysis), worth a combined 435 points.

Each task requires the model to read a natural-language research prompt, write a complete Python solution, execute it against real data, and produce output in a specified format. The entire process is fully automated with no human interaction at any stage: no prompt engineering, no manual correction, no evaluation rubrics. Scoring is deterministic.

---

## The Agentic Framework: Qwen Code CLI

SWAT-Bench uses [Qwen Code CLI](https://github.com/QwenLM/qwen-code) (v0.10.6) as the agent framework. Qwen Code is a terminal-based coding agent that provides a language model with tool-use capabilities: it can read files, write files, and execute shell commands. The model decides which tools to call and in what order; the framework handles execution and feeds results back to the model in a multi-turn loop.

### How Models Are Loaded

Each model under test is served locally through [Ollama](https://ollama.com) (v0.17.6). Ollama manages GGUF-quantized model weights and exposes an OpenAI-compatible API. For each model, the pipeline:

1. **Pulls the base weights** from Ollama's registry (e.g., `qwen3.5:27b` for the 27B dense model).
2. **Creates a custom model configuration** from an Ollama Modelfile that sets inference parameters:
   ```
   FROM qwen3.5:27b
   PARAMETER num_ctx 128000
   PARAMETER temperature 0.3
   ```
   The context window (`num_ctx`) and temperature are fixed per model. Temperature is set to 0.3 across all models to reduce output variance while preserving some generation diversity.
3. **Starts a translation proxy** between Qwen Code and Ollama. This proxy intercepts API calls to disable Qwen/DeepSeek "thinking mode" (`"think": false`), which would otherwise inject hundreds of reasoning tokens that are incompatible with tool-use parsing. The proxy also handles retries for Ollama's occasional JSON-parsing failures.

Qwen Code connects to this proxy as if it were an OpenAI-compatible endpoint:
```
OPENAI_BASE_URL=http://127.0.0.1:11436/v1
OPENAI_API_KEY=ollama
```

---

## What the Agent Receives

For each of the 55 tasks, the pipeline constructs an isolated workspace from scratch. The agent receives exactly three things:

### 1. System Context (`QWEN.md`)

A 7-line instruction file placed in the workspace root. It is deliberately minimal:

```
1. Read prompt.md in this directory for the full task description.
2. Write your solution as solution.py using only the Python standard library.
3. Run solution.py to verify it executes without errors.
4. Print all required outputs to stdout in the exact format specified in prompt.md.
5. Save any required output files (CSV, summary.md, etc.) in the current directory.
6. Do not install external packages. Do not access the internet.
7. If your code produces an error, debug and fix it before finishing.
```

This is the only guidance the model receives about how to behave. It does not see the scoring criteria, the expected answers, or any information about how its output will be evaluated.

### 2. Task Prompt (`prompt.md`)

A natural-language research scenario that describes:

- The research context (e.g., "A researcher in child welfare is examining which case-level factors are associated with placement recurrence risk")
- The analysis to perform (e.g., "Fit a multiple linear regression model with `recurrence_risk` as the outcome variable")
- Input file names and column descriptions
- The exact stdout format required (labeled lines like `R-squared: <X.XXXX>`)
- Any output files to produce (e.g., `regression_results.csv`, `summary.md`)

The prompt specifies the output format precisely because deterministic scoring depends on parseable output. The model must match the format exactly or the scorer cannot extract its answers.

### 3. Input Data Files

CSV or JSON files copied into the workspace. These are real (synthetically generated) datasets, not toy examples. For instance, the multiple regression task includes a 500-row CSV with six columns of plausible child welfare data. The NLP tasks use a 3,000-paper subset of conference abstracts.

### What the Agent Does NOT Receive

- Expected answers or scoring criteria
- Information about check types or tolerances
- Examples of correct output
- Feedback from previous attempts (except on infrastructure retries)
- Any human guidance during execution

---

## What the Agent Does

Qwen Code operates autonomously through a tool-use loop. A typical execution trace looks like this:

1. **Reads `prompt.md`** to understand the task (file read tool)
2. **Reads the input data** to inspect its structure (file read tool)
3. **Writes `solution.py`** with the complete analysis (file write tool)
4. **Executes `solution.py`** via `python3 solution.py` (shell command tool)
5. **Inspects the output** and fixes errors if the code crashed (read + edit + re-execute)
6. **Generates output files** like `regression_results.csv` and `summary.md`

The model chooses these steps on its own. Some models write code immediately; others read the data first and plan. Some debug iteratively through multiple execution cycles; others produce working code on the first attempt. This variation is itself a signal the benchmark captures.

### Retry Logic

The pipeline includes infrastructure-level retries (up to 3 attempts per task) for failures outside the model's control:

- **Stream errors**: Ollama drops the connection mid-generation (common with large context windows)
- **Timeouts**: The task exceeds the time limit (default 900 seconds for replication runs)
- **Empty transcripts**: The runner process crashes before any output

On retry, the prompt is prepended with an urgency prefix (e.g., "Write your solution.py as your very first action") to steer the model toward a faster solution path. Retry metadata is saved separately so both first-attempt and retry-adjusted results can be reported.

Genuine model failures (wrong answers, code errors, incomplete output) are never retried. Only infrastructure failures trigger retries.

### Execution Metrics Captured

For every task, the pipeline records:

| Metric | Source |
|--------|--------|
| Wall-clock time | Bash timer |
| Input/output/total tokens | Qwen CLI transcript |
| Tool calls (count, success, failure) | Qwen CLI transcript |
| Lines of code written | Qwen CLI transcript |
| API requests and latency | Qwen CLI transcript |
| Exit code | Process status |

---

## How Scoring Works

### No Rubrics, No Judges

Scoring is **not** rubric-based, LLM-as-judge, or human-evaluated. Every check is a deterministic assertion against the model's stdout or filesystem output. The scorer runs the model's `solution.py` in the workspace, captures stdout, and applies a series of pattern-matching checks defined in `checks.json`.

### Check Types

Each task's `checks.json` defines a list of checks. There are six types:

#### 1. `execution` — Did the code run?
```json
{ "type": "execution", "points": 1 }
```
Passes if `solution.py` exists and `python3 solution.py` returns exit code 0.

#### 2. `exact` — Integer matching
```json
{ "type": "exact", "pattern": "Total cases: (\\d+)", "expected": 500, "points": 1 }
```
A regex extracts a value from stdout. The extracted value must equal the expected value exactly. No tolerance.

#### 3. `numeric` — Float matching with tolerance
```json
{
  "type": "numeric",
  "pattern": "R-squared: ([\\d.]+)",
  "expected": 0.7831,
  "tolerance": 0.05,
  "points": 1
}
```
A regex extracts a floating-point value. The check passes if the value falls within `expected +/- tolerance`. This accommodates minor numerical differences arising from floating-point arithmetic, matrix inversion methods, or iterative solvers. The tolerance is set per-check based on what range of values would be considered analytically correct.

Some numeric checks accept multiple correct values:
```json
{ "expected": [8.33, 8.34], "tolerance": 1.5 }
```

An optional `absolute_value: true` flag ignores sign (useful for statistics that can be reported as positive or negative).

#### 4. `range` — Bounds checking
```json
{ "type": "range", "pattern": "KMO value: ([\\d.]+)", "min": 0.7, "max": 1.0, "points": 1 }
```
Passes if the extracted value falls within [min, max]. Used when the exact value depends on implementation details (e.g., factor analysis rotation method) but a valid result must fall within a known range.

#### 5. `regex` — Pattern matching on text
```json
{
  "type": "regex",
  "pattern": "Most significant factor: (.+)",
  "expected_pattern": "(?i)parental_substance_use|prior_placements",
  "points": 1
}
```
A regex extracts text from stdout, then a second regex validates it. The example above accepts either of two variable names (case-insensitive). Used for categorical answers where multiple formulations are correct.

#### 6. `file_exists` — Output file validation
```json
{ "type": "file_exists", "filename": "regression_results.csv", "points": 1 }
```
Passes if the specified file exists in the workspace after execution.

### A Concrete Example

For the multiple regression task (task-4-07), the checks validate:

| Check | Type | Expected | Tolerance | Points |
|-------|------|----------|-----------|--------|
| Code runs without error | execution | exit 0 | — | 1 |
| Reports 500 cases | exact | 500 | none | 1 |
| R-squared | numeric | 0.7831 | +/- 0.05 | 1 |
| F statistic | numeric | 356.6 | +/- 5.0 | 1 |
| Identifies most significant predictor | regex | `parental_substance_use` or `prior_placements` | — | 1 |
| `prior_placements` coefficient | numeric | 8.33 | +/- 1.5 | 1 |
| `parental_substance_use` coefficient | numeric | 12.13 | +/- 2.0 | 1 |
| `poverty_index` coefficient | numeric | 2.99 | +/- 1.0 | 1 |
| `regression_results.csv` exists | file_exists | — | — | 1 |
| `summary.md` exists | file_exists | — | — | 1 |

Total: 10 points, all deterministic. The expected values were computed by running the analysis independently and are properties of the fixed input dataset.

### Why This Works

The scoring is deterministic because:

1. **Input data is fixed.** Every model analyzes the same CSV/JSON files. The datasets are synthetic but internally consistent, so the correct statistical results are known in advance.
2. **Output format is prescribed.** The prompt specifies exactly what labels and format to print (e.g., `R-squared: <X.XXXX>`). The scorer's regex patterns match these labels.
3. **Tolerances absorb implementation variance.** Floating-point arithmetic, library differences (statsmodels vs. hand-coded OLS), and iterative algorithms can produce slightly different values. The tolerances are wide enough to accept any correct implementation but narrow enough to reject wrong answers.
4. **No subjective criteria.** There are no points for "code quality," "explanation clarity," or "approach elegance." Either the model produces the right number or it doesn't.

### Error Classification

When a check fails, the scorer classifies the failure into a taxonomy:

| Category | Meaning |
|----------|---------|
| 0 | Pass |
| 1 | No `solution.py` produced |
| 1.1 | No solution due to stream error (infrastructure) |
| 1.2 | No solution due to timeout (infrastructure) |
| 2 | Code crashes with an exception |
| 2.1 | Code truncated by stream error (infrastructure) |
| 3 | Output format mismatch (pattern not found) |
| 4 | Pattern found, but values are wrong (analytical error) |
| 5 | Code runs but produces no output |
| 6 | Missing required output files |

Integer categories (1-6) represent model failures; decimal subcategories (1.1, 1.2, 2.1) represent infrastructure failures where the model never had a fair chance. This distinction matters for separating model capability from system reliability.

---

## Replication Design

To measure score stability, each model is run three additional times with different random seeds (42, 123, 456) set via Ollama's `PARAMETER seed`. This changes the model's sampling trajectory while keeping all other variables fixed (same prompts, same data, same temperature, same scoring). The variance across seeds indicates how sensitive each model's performance is to random sampling.

---

## Summary of the Pipeline

```
Ollama (serves GGUF weights)
    |
    v
NoThink Proxy (disables reasoning mode, handles retries)
    |
    v
Qwen Code CLI (autonomous coding agent)
    |  Receives: system context + task prompt + data files
    |  Actions:  reads data -> writes solution.py -> executes -> debugs
    |  Produces: stdout output, CSV files, summary.md
    |
    v
Auto-Scorer (score_test.py)
    |  Runs solution.py, captures stdout
    |  Applies regex + tolerance checks from checks.json
    |  Produces: auto_score.json (per-check pass/fail + points)
    |
    v
Results: deterministic score out of 435 points
```

No human touches the pipeline between pressing "start" and reading the final scores.
