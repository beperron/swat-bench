# SWAT-Bench

**Structured Data Analysis Benchmark for Local LLMs in Social Work Research**

<p align="center">
<strong>55 tasks</strong> · <strong>435 points</strong> · <strong>7 domains</strong>
</p>

---

SWAT-Bench (Social Work Analysis Tasks Benchmark) evaluates whether locally-hosted large language models can serve as reliable research assistants for structured data analysis tasks commonly encountered in social work practice and research settings.

> **Can a local LLM, given a structured dataset and a clear analytical task description, produce correct Python code that executes successfully and returns accurate results?**

## Why This Benchmark?

Social work agencies, researchers, and doctoral students increasingly rely on data analysis for program evaluation, clinical outcome tracking, needs assessments, and policy research. However, many social work professionals lack advanced programming skills, and access to commercial AI tools raises data privacy concerns when working with protected client information (HIPAA, FERPA, 42 CFR Part 2).

Locally-hosted LLMs offer a compelling solution: an AI coding assistant that runs entirely on institutional hardware, never transmitting sensitive client data to external servers. But before recommending these tools to practitioners, we need rigorous evidence of their capabilities and limitations on the specific types of data tasks social workers actually perform.

**Important design note:** While every task is framed within a social work context (child welfare, mental health, substance use treatment, housing, criminal justice, health equity), the benchmark deliberately avoids requiring domain expertise to produce correct answers. The analytical tasks — data cleaning, statistical tests, rate calculations, multi-file merges — are domain-general skills that could be formulated in any applied research setting. Social work provides the contextual scaffolding and realistic data structures, but the computational requirements are entirely self-contained in the prompt. This makes SWAT-Bench's task designs readily adaptable to other fields.

### What We Test

| # | Capability | Description |
|:-:|:-----------|:------------|
| 1 | **Data Comprehension** | Read a CSV, understand structure, identify variables, types, and record counts |
| 2 | **Statistical Reasoning** | Select the correct procedure for a research question (e.g., non-parametric when skewed) |
| 3 | **Algorithmic Implementation** | Translate formulas into working Python, handling edge cases (ties, zeros, missing values) |
| 4 | **Output Formatting** | Produce results in a specified format for automated scoring |
| 5 | **Result Extraction** | Correctly compute and report numerical results (effect sizes, p-values, cutoffs) |

### What We Do NOT Test

- **Package installation** — 46 of 55 tasks use only the Python standard library; the remaining 9 use pre-installed libraries the model is told are available
- **Predictive modeling / ML** — Regression tasks examine associations; no classifiers or forecasting
- **Subjective interpretation** — Every task has objectively verifiable correct answers
- **Internet access or APIs** — All data is provided as local files
- **Data visualization** — Chart quality cannot be auto-scored deterministically

---

## Exam Structure

| Metric | Value |
|:-------|:------|
| Total tasks | **55** |
| Total points | **435** |
| Domains | **7** |
| Standard library only | 46 tasks |
| External libraries | 9 tasks (pandas, numpy, scipy, statsmodels, sklearn, pingouin) |
| Completion time | ~30–90 min (model-dependent) |

### Scoring

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
| 1 | Data Cleaning & Validation | 9 | 57 |
| 2 | Data Preparation & Transformation | 8 | 52 |
| 3 | Descriptive Statistics & Measurement | 7 | 45 |
| 4 | Inferential Statistics | 15 | 113 |
| 5 | Applied Social Work Analytics | 8 | 56 |
| 6 | Text & Natural Language Processing | 3 | 29 |
| 7 | Multi-Step Data Analysis | 5 | 83 |
| | **Total** | **55** | **435** |

---

## Benchmark Results

> **Run 1** — March 2026 · Qwen Code CLI v0.10.6 + Ollama · Temp 0.3 · All 7 domains (55 tasks, 435 pts)
>
> *Domains 1–6 scored from a single run per model. Domain 7 scored as the mean of 3 independent runs per model to account for cascade variance in multi-step tasks.*

### Leaderboard

| Rank | Model | Total Params | Active Params | Quant | D1–6 | D7 (mean of 3) | Combined | % |
|:----:|:------|-------------:|-------------:|:-----:|-----:|------:|------:|--:|
| 1 | **Qwen3.5-27B** | 27.8B | 27.8B | Q4 | 349.0 | 83.0 | **432.0 / 435** | **99.3%** |
| 2 | **Qwen3-Coder-Next** | 79.7B | 3.0B | Q4 | 349.5 | 81.0 | **430.5 / 435** | **99.0%** |
| 3 | **Qwen3.5-122B-A10B** | 125.1B | 10.0B | Q4 | 348.0 | 81.7 | **429.7 / 435** | **98.8%** |
| 4 | Qwen3.5-35B-A3B | 36.0B | 3.0B | Q4 | 344.0 | 81.0 | 425.0 / 435 | 97.7% |
| 5 | Qwen3-Coder-30B | 30.5B | 3.3B | Q4 | 333.0 | 77.3 | 410.3 / 435 | 94.3% |
| 6 | Qwen3.5-9B Q8 | 9.7B | 9.7B | Q8 | 317.0 | 78.0 | 395.0 / 435 | 90.8% |
| 7 | Qwen3.5-9B Q4 | 9.7B | 9.7B | Q4 | 319.5 | 73.3 | 392.8 / 435 | 90.3% |

> All models ran locally on 2x NVIDIA RTX A6000 (98 GB VRAM total) via llama.cpp / Ollama. No cloud APIs were used.

### Performance by Domain

| Domain | Pts | Q3.5-27B | Q3-Coder-Next | Q3.5-122B | Q3.5-35B | Q3-Coder-30B | Q3.5-9B Q8 | Q3.5-9B Q4 |
|:-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 — Cleaning | 57 | 98.2% | 97.4% | 96.5% | 97.4% | 93.9% | 93.9% | 93.9% |
| 2 — Preparation | 52 | 100.0% | 100.0% | 100.0% | 99.0% | 100.0% | 76.9% | 95.2% |
| 3 — Descriptive | 45 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 81.1% |
| 4 — Inferential | 113 | 96.7% | 97.5% | 97.5% | 98.4% | 91.4% | 93.0% | 91.0% |
| 5 — Applied | 56 | 100.0% | 100.0% | 100.0% | 91.1% | 89.3% | 89.3% | 87.5% |
| 6 — NLP | 29 | 100.0% | 100.0% | 100.0% | 100.0% | 93.1% | 69.0% | 89.7% |
| 7 — Multi-Step | 83 | **100.0%** | 97.6% | 98.4% | 97.6% | 93.2% | 94.0% | 88.4% |
| **Overall** | **435** | **99.3%** | **99.0%** | **98.8%** | **97.7%** | **94.3%** | **90.8%** | **90.3%** |

> Domain 7 percentages reflect the mean across 3 independent runs. Qwen3.5-27B Q4 achieved a perfect 83/83 on all 3 runs.

### Efficiency (Domains 1–6)

| Model | D1–6 Score | Time | Tokens | Tokens/Point | Tool Calls |
|:------|------:|-----:|-------:|-------------:|-----------:|
| Qwen3.5-27B | 99.1% | 2h 43m | 9.6M | 26,934 | 421 |
| Qwen3-Coder-Next | 99.3% | 3h 53m | 9.3M | 26,015 | 430 |
| Qwen3.5-122B-A10B | 98.9% | 3h 27m | 6.3M | 17,799 | 323 |
| Qwen3.5-35B-A3B | 97.7% | 1h 18m | 10.0M | 28,515 | 404 |
| Qwen3-Coder-30B | 94.6% | 1h 03m | 16.4M | 48,314 | 666 |
| Qwen3.5-9B Q8 | 90.1% | 1h 53m | 15.0M | 46,645 | 597 |
| Qwen3.5-9B Q4 | 90.8% | 1h 56m | 16.9M | 52,026 | 598 |

### Hardest Tasks (Failed by 3+ Models)

| Task | Domain | Pts | Models Failed | Score Range |
|:-----|:------:|:---:|:-------------:|:------------|
| Date Cleaning | D1 | 6 | 5/7 | 67–92% |
| One-Way ANOVA | D4 | 7 | 4/7 | 71–86% |
| Intraclass Correlation | D4 | 10 | 4/7 | 80–90% |
| Cronbach's Alpha | D5 | 8 | 4/7 | 25–62% |
| Outlier Detection | D1 | 6 | 3/7 | 92% |
| Missing Data Mechanisms | D1 | 10 | 3/7 | 90% |
| Wide to Long | D2 | 6 | 3/7 | 0–92% |
| Mann-Whitney U | D4 | 6 | 3/7 | 75–83% |
| Keyword Frequency | D6 | 9 | 3/7 | 67–78% |

> **Key insight:** The hardest single-step tasks involve date parsing edge cases, p-value approximation for hand-coded statistical tests, and psychometric analyses (ICC confidence intervals, reverse-coded Cronbach's alpha). Domain 7 multi-step tasks proved more discriminative at the lower end of the capability spectrum: the gap between the top model (100.0%) and the bottom model (88.4%) is 11.6 percentage points, compared to 9.2 points on Domains 1–6 alone. This confirms that cascade-dependent multi-step tasks amplify capability differences.

---

## Design Constraints

The constraints below ensure the exam measures analytical capability and nothing else.

### No Dependency Installation

**No task may require the model to install a Python package.** This is the single most important design constraint.

When a model fails because `pip install scipy` didn't work, the benchmark has measured the test environment — not the model's statistical knowledge. SWAT-Bench eliminates this variable:

- **46 of 55 tasks** use only the Python standard library (`csv`, `math`, `statistics`, `re`, `json`, `datetime`). The model must implement procedures from formulas, testing comprehension of the underlying mathematics.
- **9 tasks** permit pre-installed libraries for analyses where from-scratch implementation would be unreasonable.
- **No task requires matplotlib, seaborn, or any visualization library.**

This constraint also has a pedagogical benefit: a model that implements the Mann-Whitney U test from the formula demonstrates deeper statistical reasoning than one that calls `scipy.stats.mannwhitneyu()`.

### One Task, One Analytical Question

Each task asks one coherent analytical question. A task may involve multiple computational steps, but it does not bundle unrelated analyses into a single prompt. (Domain 7 is the exception — see [Multi-Step Tasks](#domain-7-multi-step-data-analysis--5-tasks-83-points).)

This matters for **diagnostic precision** (if a compound task scores 6/10, which capability failed?), **fair scoring** (one early error shouldn't cascade through unrelated checks), and **prompt clarity** (focused instructions produce fewer formatting errors).

### Additional Constraints

1. **Structured data only.** CSV, JSON, or similar tabular/semi-structured files. No images, audio, or video.
2. **Deterministic correct answers.** Every scored check has an objectively correct answer. Where methods could produce different valid answers, the prompt specifies which method to use.
3. **Output format is fully specified.** The prompt includes an exact stdout format template.
4. **Social work context.** Each task provides a brief scenario (child welfare, mental health, substance use, housing, criminal justice, health equity) that frames the analysis.
5. **Reproducibility.** All input data is deterministically generated (`random.seed(42)`) or sourced from stable public datasets.
6. **Reasonable tolerances.** Numeric checks account for legitimate implementation differences (e.g., different OLS solvers).
7. **Task independence.** Each task is self-contained. No task depends on the output of another.
8. **Required output files.** Every task requires `solution.py` and stdout in the specified format.

---

## Task Catalog

### Domain 1: Data Cleaning & Validation — 9 tasks, 57 points

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
<summary>Task descriptions</summary>

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

### Domain 2: Data Preparation & Transformation — 8 tasks, 52 points

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
<summary>Task descriptions</summary>

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

### Domain 3: Descriptive Statistics & Measurement — 7 tasks, 45 points

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
<summary>Task descriptions</summary>

- **3-01 — Frequency Distributions.** Produce frequency tables with counts and percentages, compute mode and median.
- **3-02 — Percentiles and Quartiles.** Compute quartiles (linear interpolation), IQR, fences, potential outliers, and subscale means.
- **3-03 — Grouped Descriptives.** Compare client demographics and outcomes across four treatment modalities.
- **3-04 — Rate Calculations.** Compute referral, utilization, and admission rates per 10,000 population across 6 districts.
- **3-05 — Weighted Disparity Analysis.** Compute unweighted and weighted means by racial group using sampling weights.
- **3-06 — Confidence Intervals.** Compute Wilson score 95% CIs for 8 regional offices and identify the widest CI.
- **3-07 — Inter-Rater Reliability.** Compute Cohen's Kappa from binary relevance ratings between an LLM and a human rater.

</details>

---

### Domain 4: Inferential Statistics — 15 tasks, 113 points

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
<summary>Task descriptions</summary>

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

### Domain 5: Applied Social Work Analytics — 8 tasks, 56 points

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
<summary>Task descriptions</summary>

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

### Domain 6: Text & Natural Language Processing — 3 tasks, 29 points

| ID | Task | Pts | Constraint |
|:---|:-----|:---:|:----------:|
| [6-01](tasks/task-6-01-keyword-frequency/) | **Keyword Frequency Analysis** | 9 | stdlib |
| [6-02](tasks/task-6-02-lexicon-sentiment/) | **Lexicon-Based Sentiment Analysis** | 10 | pandas |
| [6-03](tasks/task-6-03-term-pattern-matching/) | **Term Pattern Matching** | 10 | stdlib |

<details>
<summary>Task descriptions</summary>

- **6-01 — Keyword Frequency Analysis.** Use regex patterns to count comments mentioning social work and nursing terms and produce daily counts.
- **6-02 — Lexicon-Based Sentiment Analysis.** Tokenize text, match against a 200-word lexicon, classify sentiment, compute mean by program.
- **6-03 — Term Pattern Matching.** Perform case-insensitive wildcard-stem regex matching against ~18 MB of conference abstracts.

</details>

---

### Domain 7: Multi-Step Data Analysis — 5 tasks, 83 points

Unlike Domains 1–6 which follow a "one task, one analytical question" design, these tasks require **4–10 sequential analytical steps** that mirror the real-world complexity of child welfare administrative data analysis.

All five tasks use synthetic data modeled on the MISACWIS child welfare information system. A key property is the **cascade effect**: an error in an early step (e.g., incorrect deduplication, wrong merge key) causes all downstream checks to fail, making these tasks highly discriminative between models of different capability levels.

| ID | Task | Pts | Constraint |
|:---|:-----|:---:|:----------:|
| [7-01](tasks/task-7-01-allegation-funnel/) | **Allegation-to-Removal Funnel** | 15 | stdlib |
| [7-02](tasks/task-7-02-placement-stability/) | **Placement Stability by Age & Race** | 18 | stdlib |
| [7-03](tasks/task-7-03-time-to-permanency/) | **Time-to-Permanency with Re-entry** | 16 | stdlib |
| [7-04](tasks/task-7-04-racial-disparity/) | **Racial Disparity in Substantiation** | 16 | stdlib |
| [7-05](tasks/task-7-05-point-in-time-snapshot/) | **Point-in-Time Foster Care Snapshot** | 18 | stdlib |

<details>
<summary>Task descriptions</summary>

- **7-01 — Allegation-to-Removal Funnel Analysis.** Deduplicate allegation records, compute screening-in and substantiation rates through a multi-stage funnel, merge with a bridge table to link to removals, and produce county-level conversion rates.
- **7-02 — Placement Stability by Child Age and Race.** Merge four CSV files, compute age at removal with floor logic, bin into age groups, count placements per episode, and produce two-dimensional stability metrics.
- **7-03 — Time-to-Permanency with Re-entry Flagging.** Classify episodes as discharged or still-in-care, detect re-entries within 12 months, compute median time-in-care by discharge reason, and calculate mean age at first removal.
- **7-04 — Racial Disparity in Substantiation and Removal.** Compute substantiation and removal rates by race through a multi-stage funnel with changing denominators, calculate relative risk ratios using White as the reference group.
- **7-05 — Point-in-Time Foster Care Snapshot.** Apply temporal filtering with NULL handling, determine current placements from history records, merge four tables, and produce county-level aggregations with medians and rankings.

</details>

---

## Running the Benchmark

```bash
# From the scripts/ directory:

# Run all 55 tasks with a model
./run_exam.sh <model_name>

# Score a completed run
./score_exam.sh <run_id> [framework]
```

Results are saved to `results/<framework>/<run_id>/` with per-task transcripts, solution files, and auto-scored results.

---

## Repository Structure

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

## Contributing a New Task

To propose a new task, provide:

1. **`prompt.md`** — Full task description (scenario, task statement, input files, exact output format template, constraints, evaluation criteria)
2. **`generate_data.py`** — Deterministic data generation script (seeded with `random.seed(42)`)
3. **`expected/checks.json`** — Automated scoring rubric with check types, patterns, expected values, and tolerances
4. **Input data files** — Generated by the data script, placed in the `input/` subdirectory

The task will be reviewed against the [design constraints](#design-constraints) listed above before inclusion.

---

<p align="center">
<strong>SWAT-Bench</strong> — 55 tasks · 435 points · 7 domains<br>
<em>Evaluating local LLMs for social work research data analysis</em>
</p>
