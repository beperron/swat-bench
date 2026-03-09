<div align="center">

# SWAT-Bench

**Social Work Analysis Tasks Benchmark for Evaluating Local LLMs on Structured Data Analysis**

[![Tasks](https://img.shields.io/badge/Tasks-55-blue?style=for-the-badge)](#exam-structure)
[![Points](https://img.shields.io/badge/Points-435-green?style=for-the-badge)](#exam-structure)
[![Domains](https://img.shields.io/badge/Domains-7-orange?style=for-the-badge)](#domain-distribution)
[![Top Score](https://img.shields.io/badge/Top_Score-99.3%25-brightgreen?style=for-the-badge)](#-leaderboard)

*Can a locally-hosted LLM produce correct Python code for structured data analysis tasks?*

</div>

---

## 🎯 Overview

**SWAT-Bench** (Social Work Analysis Tasks Benchmark) evaluates whether locally-hosted large language models can serve as reliable research assistants for structured data analysis. Each task provides a dataset and a clear analytical prompt — the model must write Python code that executes correctly and returns accurate, auto-scored results.

> [!NOTE]
> **Domain-general by design.** While every task is framed within a social work context (child welfare, mental health, substance use, housing, criminal justice, health equity), the benchmark deliberately avoids requiring domain expertise. The analytical tasks — data cleaning, statistical tests, rate calculations, multi-file merges — are skills that could be formulated in any applied research setting. Social work provides realistic data structures, but the computational requirements are entirely self-contained in the prompt.

### 🔒 Why Local LLMs?

Social work agencies, researchers, and doctoral students increasingly rely on data analysis for program evaluation, clinical outcome tracking, and policy research. However:

- Many social work professionals lack advanced programming skills
- Protected client information (HIPAA, FERPA, 42 CFR Part 2) raises data privacy concerns with cloud AI
- Locally-hosted LLMs run entirely on institutional hardware, never transmitting sensitive data externally

Before recommending these tools to practitioners, we need rigorous evidence of their capabilities and limitations.

---

## 🏗️ Exam Structure

<table>
<tr><td><strong>Total tasks</strong></td><td><code>55</code></td></tr>
<tr><td><strong>Total points</strong></td><td><code>435</code></td></tr>
<tr><td><strong>Domains</strong></td><td><code>7</code></td></tr>
<tr><td><strong>Standard library only</strong></td><td>46 tasks</td></tr>
<tr><td><strong>External libraries</strong></td><td>9 tasks (pandas, numpy, scipy, statsmodels, sklearn, pingouin)</td></tr>
<tr><td><strong>Completion time</strong></td><td>~30–90 min (model-dependent)</td></tr>
</table>

### ✅ What We Test

| | Capability | Description |
|:-:|:-----------|:------------|
| 1 | **Data Comprehension** | Read a CSV, understand structure, identify variables, types, and record counts |
| 2 | **Statistical Reasoning** | Select the correct procedure for a research question (e.g., non-parametric when skewed) |
| 3 | **Algorithmic Implementation** | Translate formulas into working Python, handling edge cases (ties, zeros, missing values) |
| 4 | **Output Formatting** | Produce results in a specified format for automated scoring |
| 5 | **Result Extraction** | Correctly compute and report numerical results (effect sizes, p-values, cutoffs) |

### ❌ What We Do NOT Test

- **Package installation** — 46 of 55 tasks use only the Python standard library; the remaining 9 use pre-installed libraries
- **Predictive modeling / ML** — Regression tasks examine associations; no classifiers or forecasting
- **Subjective interpretation** — Every task has objectively verifiable correct answers
- **Internet access or APIs** — All data is provided as local files
- **Data visualization** — Chart quality cannot be auto-scored deterministically
- **Unstructured text analysis** — NLP tasks (Domain 6) operate on structured/semi-structured text fields within tabular data, not on free-form documents or unstructured corpora

### 🎯 Scoring

Each task is scored automatically by `score_test.py`, which executes the model's `solution.py`, captures stdout, and checks output against expected values:

| Check Type | Description | Example |
|:-----------|:------------|:--------|
| `execution` | Code runs without error | 1 point |
| `exact` | Integer matches exactly | `Total records: 200` |
| `numeric` | Float within tolerance | `R-squared: 0.78 ± 0.05` |
| `range` | Value within bounds | `p-value in [0.01, 0.05]` |
| `regex` | Text matches pattern | Correct group name |
| `file_exists` | Output file created | `summary.md` |

### Domain Distribution

| | Domain | Tasks | Points |
|:-:|:-------|------:|-------:|
| 🧹 | Data Cleaning & Validation | 9 | 57 |
| 🔄 | Data Preparation & Transformation | 8 | 52 |
| 📏 | Descriptive Statistics & Measurement | 7 | 45 |
| 📐 | Inferential Statistics | 15 | 113 |
| 🏛️ | Applied Social Work Analytics | 8 | 56 |
| 💬 | Text & Natural Language Processing | 3 | 29 |
| 🔗 | Multi-Step Data Analysis | 5 | 83 |
| | **Total** | **55** | **435** |

---

## 📈 Benchmark Results

> [!IMPORTANT]
> **Run 1** — March 2026 · Qwen Code CLI v0.10.6 + Ollama · Temperature 0.3 · All 7 domains (55 tasks, 435 pts)
>
> Each model was evaluated across **3–4 independent runs** with different random seeds. Scores below report the **mean ± SD** across runs. Domain 7 used 3 dedicated multi-step runs per model. All models ran locally on **2x NVIDIA RTX A6000** (98 GB VRAM) via llama.cpp / Ollama — no cloud APIs.

### 🏆 Leaderboard

| Rank | Model | Params | Active | Quant | Mean Score | SD | **%** | Runs |
|:----:|:------|-------:|-------:|:-----:|-----------:|---:|------:|:----:|
| 🥇 | **Qwen3.5-27B** | 27.8B | 27.8B | Q4 | **432.9 / 435** | ±1.1 | **99.5%** | 4+3 |
| 🥈 | **Qwen3.5-122B-A10B** | 125.1B | 10.0B | Q4 | **431.2 / 435** | ±1.9 | **99.1%** | 3+3 |
| 🥉 | **Qwen3-Coder-Next** | 79.7B | 3.0B | Q4 | **428.8 / 435** | ±3.1 | **98.6%** | 3+3 |
| 4 | Qwen3.5-35B-A3B | 36.0B | 3.0B | Q4 | 424.8 / 435 | ±4.0 | 97.6% | 4+3 |
| 5 | Qwen3-Coder-30B | 30.5B | 3.3B | Q4 | 408.3 / 435 | ±5.4 | 93.9% | 4+3 |
| 6 | Qwen3.5-9B Q8 | 9.7B | 9.7B | Q8 | 406.8 / 435 | ±13.4 | 93.5% | 4+3 |
| 7 | Qwen3.5-9B Q4 | 9.7B | 9.7B | Q4 | 386.8 / 435 | ±9.0 | 88.9% | 4+3 |

> **Runs** column shows D1–6 runs + D7 runs. SD is propagated as √(SD²_D1-6 + SD²_D7).

### 📊 Score Breakdown

| Model | D1–6 Mean / 352 | D1–6 SD | D7 Mean / 83 | D7 SD | Combined / 435 |
|:------|:---:|:---:|:---:|:---:|:---:|
| Qwen3.5-27B | 349.9 | ±1.1 | **83.0** | ±0.0 | **432.9** |
| Qwen3.5-122B-A10B | 349.5 | ±1.5 | 81.7 | ±1.2 | 431.2 |
| Qwen3-Coder-Next | 347.8 | ±1.5 | 81.0 | ±2.6 | 428.8 |
| Qwen3.5-35B-A3B | 343.8 | ±3.4 | 81.0 | ±2.0 | 424.8 |
| Qwen3-Coder-30B | 331.0 | ±2.8 | 77.3 | ±4.6 | 408.3 |
| Qwen3.5-9B Q8 | 328.8 | ±12.3 | 78.0 | ±5.2 | 406.8 |
| Qwen3.5-9B Q4 | 313.5 | ±6.4 | 73.3 | ±6.4 | 386.8 |

> [!TIP]
> **Qwen3.5-27B Q4** achieved a perfect 83/83 on all 3 Domain 7 runs — the only model to do so — and had the lowest overall variability (SD ±1.1). The 9B models show the highest run-to-run variance (SD ±9–13), suggesting smaller models are more sensitive to prompt framing and random seed effects.

### ⚡ Efficiency (Domains 1–6, single representative run)

| Model | D1–6 Score | Time | Tokens | Tokens/Point | Tool Calls |
|:------|------:|-----:|-------:|-------------:|-----------:|
| Qwen3.5-27B | 99.4% | 2h 43m | 9.6M | 26,934 | 421 |
| Qwen3.5-122B-A10B | 99.3% | 3h 27m | 6.3M | 17,799 | 323 |
| Qwen3-Coder-Next | 98.8% | 3h 53m | 9.3M | 26,015 | 430 |
| Qwen3.5-35B-A3B | 97.7% | 1h 18m | 10.0M | 28,515 | 404 |
| Qwen3-Coder-30B | 94.0% | 1h 03m | 16.4M | 48,314 | 666 |
| Qwen3.5-9B Q8 | 93.4% | 1h 53m | 15.0M | 46,645 | 597 |
| Qwen3.5-9B Q4 | 89.1% | 1h 56m | 16.9M | 52,026 | 598 |

### 🚧 Hardest Tasks (Failed by 3+ Models)

| Task | Domain | Pts | Models Failed | Score Range |
|:-----|:------:|:---:|:-------------:|:------------|
| Date Cleaning | 🧹 D1 | 6 | 5/7 | 67–92% |
| One-Way ANOVA | 📐 D4 | 7 | 4/7 | 71–86% |
| Intraclass Correlation | 📐 D4 | 10 | 4/7 | 80–90% |
| Cronbach's Alpha | 🏛️ D5 | 8 | 4/7 | 25–62% |
| Outlier Detection | 🧹 D1 | 6 | 3/7 | 92% |
| Missing Data Mechanisms | 🧹 D1 | 10 | 3/7 | 90% |
| Wide to Long | 🔄 D2 | 6 | 3/7 | 0–92% |
| Mann-Whitney U | 📐 D4 | 6 | 3/7 | 75–83% |
| Keyword Frequency | 💬 D6 | 9 | 3/7 | 67–78% |

> [!NOTE]
> **Key insight:** The hardest single-step tasks involve date parsing edge cases, psychometric analyses (ICC confidence intervals, reverse-coded Cronbach's alpha), and hand-coded statistical tests requiring precise intermediate computations. These failure patterns suggest that smaller models struggle most with precision requirements in multi-step mathematical derivations.

---

## 🛡️ Design Constraints

The constraints below ensure the exam measures **analytical capability** and nothing else.

### No Dependency Installation

> [!IMPORTANT]
> **No task may require the model to install a Python package.** This is the single most important design constraint.

When a model fails because `pip install scipy` didn't work, the benchmark has measured the test environment — not the model's statistical knowledge. SWAT-Bench eliminates this variable:

- **46 of 55 tasks** use only the Python standard library (`csv`, `math`, `statistics`, `re`, `json`, `datetime`). The model must implement procedures from formulas, testing comprehension of the underlying mathematics.
- **9 tasks** permit pre-installed libraries for analyses where from-scratch implementation would be unreasonable.
- **No task requires matplotlib, seaborn, or any visualization library.**

This constraint also has a pedagogical benefit: a model that implements the Mann-Whitney U test from the formula demonstrates deeper statistical reasoning than one that calls `scipy.stats.mannwhitneyu()`.

### One Task, One Analytical Question

Each task asks one coherent analytical question. A task may involve multiple computational steps, but it does not bundle unrelated analyses into a single prompt. (Domain 7 is the exception — see [Multi-Step Tasks](#-domain-7-multi-step-data-analysis--5-tasks-83-points).)

This matters for:
- **Diagnostic precision** — if a compound task scores 6/10, which capability failed?
- **Fair scoring** — one early error shouldn't cascade through unrelated checks
- **Prompt clarity** — focused instructions produce fewer formatting errors

### Additional Constraints

| | Constraint | Detail |
|:-:|:-----------|:-------|
| 1 | **Structured data only** | CSV, JSON, or similar tabular/semi-structured files. No images, audio, or video |
| 2 | **Deterministic answers** | Every scored check has an objectively correct answer. Ambiguous methods are specified |
| 3 | **Output format specified** | Each prompt includes an exact stdout format template |
| 4 | **Social work context** | Each task provides a brief scenario framing the analysis |
| 5 | **Reproducibility** | All input data is deterministically generated (`random.seed(42)`) or from stable public datasets |
| 6 | **Reasonable tolerances** | Numeric checks account for legitimate implementation differences |
| 7 | **Task independence** | Each task is self-contained — no task depends on another |
| 8 | **Required outputs** | Every task requires `solution.py` and stdout in the specified format |

---

## 📋 Task Catalog

### 🧹 Domain 1: Data Cleaning & Validation — 9 tasks, 57 points

| ID | Task | Pts | Constraint |
|:---|:-----|:---:|:----------:|
| [1-01](tasks/task-1-01-missing-data/) | **Missing Data Assessment** | 5 | stdlib |
| [1-02](tasks/task-1-02-duplicate-detection/) | **Duplicate Detection** | 6 | stdlib |
| [1-03](tasks/task-1-03-outlier-detection/) | **Outlier Detection** | 6 | stdlib |
| [1-04](tasks/task-1-04-date-cleaning/) | **Date and Timeline Cleaning** | 6 | stdlib |
| [1-05](tasks/task-1-05-recoding-standardization/) | **Recoding and Standardization** | 6 | stdlib |
| [1-06](tasks/task-1-06-missing-data-mechanisms/) | **Missing Data Mechanisms** | 10 | pandas/scipy |
| [1-07](tasks/task-1-07-codebook-application/) | **Codebook Application** | 6 | stdlib |
| [1-08](tasks/task-1-08-skip-logic/) | **Skip Logic Validation** | 6 | stdlib |
| [1-09](tasks/task-1-09-data-validation/) | **Comprehensive Data Validation** | 6 | stdlib |

<details>
<summary>📝 Task descriptions</summary>

- **1-01 — Missing Data Assessment.** Compute total records, missing values per column, complete vs. incomplete case counts, the column with the most missing data, and overall percent complete.
- **1-02 — Duplicate Detection.** Identify exact duplicate rows and conflicting records, produce deduplication counts, and output a cleaned CSV.
- **1-03 — Outlier Detection.** Flag records with impossible total scores, invalid item scores, sum mismatches, and severity category mismatches in PHQ-9 data.
- **1-04 — Date and Timeline Cleaning.** Detect format inconsistencies, impossible dates, sequence violations, and age-entry mismatches in foster care records.
- **1-05 — Recoding and Standardization.** Harmonize gender labels, race/ethnicity labels, treatment completion coding, and satisfaction scores across sites.
- **1-06 — Missing Data Mechanisms.** Quantify missingness, classify each column's mechanism as MCAR or MAR by testing associations with observed variables.
- **1-07 — Codebook Application.** Apply a codebook CSV to recode numeric codes, count unmapped codes, and identify the most common diagnosis and housing status.
- **1-08 — Skip Logic Validation.** Count should-be-empty and should-have-data violations, identify the most violated rule, and produce a violation report.
- **1-09 — Comprehensive Data Validation.** Audit client records for 10 categories of data quality issues.

</details>

---

### 🔄 Domain 2: Data Preparation & Transformation — 8 tasks, 52 points

| ID | Task | Pts | Constraint |
|:---|:-----|:---:|:----------:|
| [2-01](tasks/task-2-01-data-filtering/) | **Data Filtering** | 5 | stdlib |
| [2-02](tasks/task-2-02-wide-to-long/) | **Wide to Long Reshape** | 6 | stdlib |
| [2-03](tasks/task-2-03-derived-variables/) | **Derived Variables** | 6 | stdlib |
| [2-04](tasks/task-2-04-multi-file-merge/) | **Multi-File Merge** | 6 | stdlib |
| [2-05](tasks/task-2-05-unit-harmonization/) | **Unit Harmonization** | 6 | stdlib |
| [2-06](tasks/task-2-06-long-to-wide/) | **Long to Wide Reshape** | 10 | stdlib |
| [2-07](tasks/task-2-07-binning-categorization/) | **Binning and Categorization** | 6 | stdlib |
| [2-08](tasks/task-2-08-aggregation/) | **Aggregation** | 7 | stdlib |

<details>
<summary>📝 Task descriptions</summary>

- **2-01 — Data Filtering.** Apply four sequential filters, report intermediate counts, and compute summary statistics.
- **2-02 — Wide to Long Reshape.** Reshape longitudinal foster care data to long format, handle missing values, compute mean scores by time point.
- **2-03 — Derived Variables.** Compute age from DOB, categorize age groups, calculate poverty ratio and weighted composite need score.
- **2-04 — Multi-File Merge.** Combine data from three administrative systems, count overlapping and orphan records, inner join, summary statistics.
- **2-05 — Unit Harmonization.** Convert income data from different reporting periods to annual amounts, compute poverty thresholds and rates.
- **2-06 — Long to Wide Reshape.** Transform student assessment records for accreditation reporting with cross-tabulations and change scores.
- **2-07 — Binning and Categorization.** Bin BMI, PHQ-9, GAD-7, and AUDIT-C scores into clinical categories using specified thresholds.
- **2-08 — Aggregation.** Compute monthly and quarterly summary statistics from 366 days of crisis hotline call logs.

</details>

---

### 📏 Domain 3: Descriptive Statistics & Measurement — 7 tasks, 45 points

| ID | Task | Pts | Constraint |
|:---|:-----|:---:|:----------:|
| [3-01](tasks/task-3-01-frequency-distributions/) | **Frequency Distributions** | 5 | stdlib |
| [3-02](tasks/task-3-02-percentiles-quartiles/) | **Percentiles and Quartiles** | 5 | stdlib |
| [3-03](tasks/task-3-03-grouped-descriptives/) | **Grouped Descriptives** | 6 | stdlib |
| [3-04](tasks/task-3-04-rate-calculations/) | **Rate Calculations** | 6 | stdlib |
| [3-05](tasks/task-3-05-weighted-disparity/) | **Weighted Disparity Analysis** | 10 | pandas |
| [3-06](tasks/task-3-06-confidence-intervals/) | **Confidence Intervals** | 6 | stdlib |
| [3-07](tasks/task-3-07-inter-rater-reliability/) | **Inter-Rater Reliability** | 7 | stdlib |

<details>
<summary>📝 Task descriptions</summary>

- **3-01 — Frequency Distributions.** Produce frequency tables with counts and percentages, compute mode and median.
- **3-02 — Percentiles and Quartiles.** Compute quartiles (linear interpolation), IQR, fences, potential outliers, and subscale means.
- **3-03 — Grouped Descriptives.** Compare client demographics and outcomes across four treatment modalities.
- **3-04 — Rate Calculations.** Compute referral, utilization, and admission rates per 10,000 population across 6 districts.
- **3-05 — Weighted Disparity Analysis.** Compute unweighted and weighted means by racial group using sampling weights.
- **3-06 — Confidence Intervals.** Compute Wilson score 95% CIs for 8 regional offices and identify the widest CI.
- **3-07 — Inter-Rater Reliability.** Compute Cohen's Kappa from binary relevance ratings between an LLM and a human rater.

</details>

---

### 📐 Domain 4: Inferential Statistics — 15 tasks, 113 points

| ID | Task | Pts | Constraint |
|:---|:-----|:---:|:----------:|
| [4-01](tasks/task-4-01-paired-t-test/) | **Paired t-Test** | 6 | stdlib |
| [4-02](tasks/task-4-02-independent-t-test/) | **Independent t-Test** | 6 | stdlib |
| [4-03](tasks/task-4-03-chi-square/) | **Chi-Square Test** | 5 | stdlib |
| [4-04](tasks/task-4-04-one-way-anova/) | **One-Way ANOVA** | 7 | stdlib |
| [4-05](tasks/task-4-05-spearman-correlation/) | **Spearman Correlation** | 5 | stdlib |
| [4-06](tasks/task-4-06-mann-whitney-u/) | **Mann-Whitney U Test** | 6 | stdlib |
| [4-07](tasks/task-4-07-multiple-regression/) | **Multiple Regression** | 10 | pandas/scipy/statsmodels/sklearn |
| [4-08](tasks/task-4-08-anova-posthoc/) | **ANOVA with Post-Hoc** | 10 | pandas/scipy/statsmodels |
| [4-09](tasks/task-4-09-wilcoxon-signed-rank/) | **Wilcoxon Signed-Rank** | 6 | stdlib |
| [4-10](tasks/task-4-10-mcnemar-test/) | **McNemar's Test** | 6 | stdlib |
| [4-11](tasks/task-4-11-fisher-exact-test/) | **Fisher's Exact Test** | 7 | stdlib |
| [4-12](tasks/task-4-12-logistic-regression/) | **Logistic Regression** | 10 | pandas/scipy/statsmodels/sklearn |
| [4-13](tasks/task-4-13-interrupted-time-series/) | **Interrupted Time Series** | 9 | pandas/scipy/statsmodels |
| [4-14](tasks/task-4-14-reliable-change-index/) | **Reliable Change Index** | 10 | stdlib |
| [4-15](tasks/task-4-15-intraclass-correlation/) | **Intraclass Correlation** | 10 | pandas/scipy/pingouin |

<details>
<summary>📝 Task descriptions</summary>

- **4-01 — Paired t-Test.** Implement a paired-samples t-test from scratch (pre/post means, SD of differences, t-statistic, Cohen's d).
- **4-02 — Independent t-Test.** Implement Welch's t-test with Welch-Satterthwaite degrees of freedom and Cohen's d.
- **4-03 — Chi-Square Test.** Build a contingency table, compute chi-square and Cramer's V.
- **4-04 — One-Way ANOVA.** Implement ANOVA from scratch (SS decomposition, F-statistic), compute eta-squared.
- **4-05 — Spearman Correlation.** Compute Spearman rank correlation with average ranks for ties and test significance.
- **4-06 — Mann-Whitney U Test.** Implement Mann-Whitney U with tied-rank handling and rank-biserial effect size.
- **4-07 — Multiple Regression.** Fit multiple linear regression, report R-squared, F-statistic, and identify the most significant factor.
- **4-08 — ANOVA with Post-Hoc.** One-way ANOVA with eta-squared and pairwise post-hoc comparisons (Bonferroni/Tukey).
- **4-09 — Wilcoxon Signed-Rank.** Implement the Wilcoxon signed-rank test with normal approximation and effect size r.
- **4-10 — McNemar's Test.** Build a transition table, compute McNemar's chi-square, odds ratio, and net change.
- **4-11 — Fisher's Exact Test.** Implement Fisher's exact test using hypergeometric probabilities, odds ratio, and relative risk.
- **4-12 — Logistic Regression.** Fit logistic regression, compute McFadden's pseudo R-squared, classification accuracy, and odds ratios.
- **4-13 — Interrupted Time Series.** Fit a segmented regression model to estimate level change and slope change.
- **4-14 — Reliable Change Index.** Compute SEM, Jacobson-Truax threshold, RCI per client, and classify outcomes.
- **4-15 — Intraclass Correlation.** Compute ICC(2,1) via two-way ANOVA decomposition with 95% confidence interval.

</details>

---

### 🏛️ Domain 5: Applied Social Work Analytics — 8 tasks, 56 points

| ID | Task | Pts | Constraint |
|:---|:-----|:---:|:----------:|
| [5-01](tasks/task-5-01-caseload-analysis/) | **Caseload Analysis** | 5 | stdlib |
| [5-02](tasks/task-5-02-pearson-correlation-matrix/) | **Pearson Correlation Matrix** | 5 | stdlib |
| [5-03](tasks/task-5-03-effect-sizes/) | **Effect Sizes for Meta-Analysis** | 6 | stdlib |
| [5-04](tasks/task-5-04-cost-effectiveness/) | **Cost-Effectiveness Analysis** | 10 | pandas |
| [5-05](tasks/task-5-05-racial-disproportionality/) | **Racial Disproportionality** | 7 | stdlib |
| [5-06](tasks/task-5-06-risk-assessment/) | **Risk Assessment Validation** | 7 | stdlib |
| [5-07](tasks/task-5-07-cronbachs-alpha/) | **Cronbach's Alpha** | 8 | stdlib |
| [5-08](tasks/task-5-08-state-level-trend-analysis/) | **State-Level Trend Analysis** | 8 | stdlib |

<details>
<summary>📝 Task descriptions</summary>

- **5-01 — Caseload Analysis.** Compute per-worker caseload counts, success rates, average days to closure, and satisfaction.
- **5-02 — Pearson Correlation Matrix.** Compute a full pairwise Pearson correlation matrix and identify the strongest correlations.
- **5-03 — Effect Sizes for Meta-Analysis.** Compute Cohen's d, Hedges' g, confidence intervals, and inverse-variance-weighted pooled Hedges' g.
- **5-04 — Cost-Effectiveness Analysis.** Calculate total and per-client costs, cost per outcome unit, and ICERs.
- **5-05 — Racial Disproportionality.** Compute referral rates by race, disproportionality indices, and relative risk ratios.
- **5-06 — Risk Assessment Validation.** Compute confusion matrix metrics, AUC via trapezoidal rule, and optimal cutoff using Youden's J.
- **5-07 — Cronbach's Alpha.** Parse a two-row header survey, identify reverse-coded items, compute alpha, item-total correlations, and alpha-if-deleted.
- **5-08 — State-Level Trend Analysis.** Analyze geographic and temporal trends in fatal police shootings.

</details>

---

### 💬 Domain 6: Text & Natural Language Processing — 3 tasks, 29 points

| ID | Task | Pts | Constraint |
|:---|:-----|:---:|:----------:|
| [6-01](tasks/task-6-01-keyword-frequency/) | **Keyword Frequency Analysis** | 9 | stdlib |
| [6-02](tasks/task-6-02-lexicon-sentiment/) | **Lexicon-Based Sentiment Analysis** | 10 | pandas |
| [6-03](tasks/task-6-03-term-pattern-matching/) | **Term Pattern Matching** | 10 | stdlib |

<details>
<summary>📝 Task descriptions</summary>

- **6-01 — Keyword Frequency Analysis.** Use regex patterns to count comments mentioning social work and nursing terms and produce daily counts.
- **6-02 — Lexicon-Based Sentiment Analysis.** Tokenize text, match against a 200-word lexicon, classify sentiment, compute mean by program.
- **6-03 — Term Pattern Matching.** Perform case-insensitive wildcard-stem regex matching against ~18 MB of conference abstracts.

</details>

---

### 🔗 Domain 7: Multi-Step Data Analysis — 5 tasks, 83 points

> [!WARNING]
> Unlike Domains 1–6 which follow a "one task, one analytical question" design, these tasks require **4–10 sequential analytical steps** that mirror the real-world complexity of child welfare administrative data analysis. An error in an early step (e.g., incorrect deduplication, wrong merge key) causes all downstream checks to fail — the **cascade effect** makes these tasks highly discriminative.

All five tasks use synthetic data modeled on the MISACWIS child welfare information system.

| ID | Task | Pts | Constraint |
|:---|:-----|:---:|:----------:|
| [7-01](tasks/task-7-01-allegation-funnel/) | **Allegation-to-Removal Funnel** | 15 | stdlib |
| [7-02](tasks/task-7-02-placement-stability/) | **Placement Stability by Age & Race** | 18 | stdlib |
| [7-03](tasks/task-7-03-time-to-permanency/) | **Time-to-Permanency with Re-entry** | 16 | stdlib |
| [7-04](tasks/task-7-04-racial-disparity/) | **Racial Disparity in Substantiation** | 16 | stdlib |
| [7-05](tasks/task-7-05-point-in-time-snapshot/) | **Point-in-Time Foster Care Snapshot** | 18 | stdlib |

<details>
<summary>📝 Task descriptions</summary>

- **7-01 — Allegation-to-Removal Funnel Analysis.** Deduplicate allegation records, compute screening-in and substantiation rates through a multi-stage funnel, merge with a bridge table to link to removals, and produce county-level conversion rates.
- **7-02 — Placement Stability by Child Age and Race.** Merge four CSV files, compute age at removal with floor logic, bin into age groups, count placements per episode, and produce two-dimensional stability metrics.
- **7-03 — Time-to-Permanency with Re-entry Flagging.** Classify episodes as discharged or still-in-care, detect re-entries within 12 months, compute median time-in-care by discharge reason, and calculate mean age at first removal.
- **7-04 — Racial Disparity in Substantiation and Removal.** Compute substantiation and removal rates by race through a multi-stage funnel with changing denominators, calculate relative risk ratios using White as the reference group.
- **7-05 — Point-in-Time Foster Care Snapshot.** Apply temporal filtering with NULL handling, determine current placements from history records, merge four tables, and produce county-level aggregations with medians and rankings.

</details>

---

## 🔧 Running the Benchmark

```bash
# From the scripts/ directory:

# Run all 55 tasks with a model
./run_exam.sh <model_name>

# Score a completed run
./score_exam.sh <run_id> [framework]
```

Results are saved to `results/<framework>/<run_id>/` with per-task transcripts, solution files, and auto-scored results.

---

## 📁 Repository Structure

```
swat-bench/
├── README.md
├── SWAT-Bench_Technical_Overview.md
├── datasets/              # All input data files (~70 files)
├── tasks/                 # 55 task definitions
│   └── task-{D}-{NN}-{name}/
│       ├── prompt.md      # Task description and output format
│       ├── input/         # Data files for this task
│       └── expected/
│           └── checks.json
├── scripts/               # Pipeline and scoring scripts
│   ├── run_exam.sh
│   ├── score_exam.sh
│   ├── score_test.py
│   ├── extract_metrics.py
│   └── ...
├── config/                # Agent & model configuration
│   ├── agent_context.md
│   ├── inference_params.json
│   └── modelfiles/
└── results/               # Runtime output (empty — .gitkeep)
```

---

## 🤝 Contributing a New Task

To propose a new task, provide:

1. **`prompt.md`** — Full task description (scenario, task statement, input files, exact output format template, constraints, evaluation criteria)
2. **`generate_data.py`** — Deterministic data generation script (seeded with `random.seed(42)`)
3. **`expected/checks.json`** — Automated scoring rubric with check types, patterns, expected values, and tolerances
4. **Input data files** — Generated by the data script, placed in the `input/` subdirectory

The task will be reviewed against the [design constraints](#-design-constraints) listed above before inclusion.

---

<div align="center">

**📊 SWAT-Bench** — 55 tasks · 435 points · 7 domains

*Evaluating local LLMs for social work research data analysis*

</div>
