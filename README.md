# 🧪 SWAT-Bench

### Structured Data Analysis Benchmark for Local LLMs in Social Work Research

<p align="center">
<strong>56 tasks</strong> · <strong>444 points</strong> · <strong>7 domains</strong><br>
<em>Foundational → Intermediate → Advanced → Multi-Step</em>
</p>

---

SWAT-Bench (Social Work Analysis Tasks Benchmark) evaluates whether locally-hosted large language models can serve as reliable research assistants for structured data analysis tasks commonly encountered in social work practice and research settings.

> **Can a local LLM, given a structured dataset and a clear analytical task description, produce correct Python code that executes successfully and returns accurate results?**

## 📌 Why This Benchmark?

Social work agencies, researchers, and doctoral students increasingly rely on data analysis for program evaluation, clinical outcome tracking, needs assessments, and policy research. However, many social work professionals lack advanced programming skills, and access to commercial AI tools raises data privacy concerns when working with protected client information (HIPAA, FERPA, 42 CFR Part 2).

Locally-hosted LLMs offer a compelling solution: an AI coding assistant that runs entirely on institutional hardware, never transmitting sensitive client data to external servers. But before recommending these tools to practitioners, we need rigorous evidence of their capabilities and limitations on the specific types of data tasks social workers actually perform.

### 🔬 What we test

| # | Capability | Description |
|:-:|------------|-------------|
| 1 | **Data comprehension** | Read a CSV, understand structure, identify variables, types, and record counts |
| 2 | **Statistical reasoning** | Select the correct procedure for a research question (e.g., non-parametric when skewed) |
| 3 | **Algorithmic implementation** | Translate formulas into working Python, handling edge cases (ties, zeros, missing values) |
| 4 | **Output formatting** | Produce results in a specified format for automated scoring |
| 5 | **Result extraction** | Correctly compute and report numerical results (effect sizes, p-values, cutoffs) |

### 🚫 What we do NOT test

- **Package installation** — 42 of 56 tasks use only the Python standard library; the remaining 14 use pre-installed libraries the model is told are available
- **Predictive modeling / ML** — Regression tasks examine associations; no classifiers or forecasting
- **Subjective interpretation** — Every task has objectively verifiable correct answers
- **Internet access or APIs** — All data is provided as local files
- **Data visualization** — Chart quality cannot be auto-scored deterministically

---

## 📊 Exam Structure

| Metric | Value |
|:-------|:------|
| Total tasks | **56** |
| Total points | **444** |
| Domains | **7** |
| Difficulty levels | Foundational (9) · Intermediate (23) · Advanced (24) |
| Standard library only | 42 tasks |
| External libraries | 14 tasks (pandas, numpy, scipy, statsmodels, sklearn, pingouin, factor_analyzer) |
| Completion time | ~30–90 min (model-dependent) |

### ✅ Scoring

Each task is scored automatically by `score_test.py`, which executes the model's `solution.py`, captures stdout, and checks output against expected values:

| Check type | Description | Example |
|:-----------|:------------|:--------|
| `execution` | Code runs without error | 1 point |
| `exact` | Integer matches exactly | `Total records: 200` |
| `numeric` | Float within tolerance | `R-squared: 0.78 ± 0.05` |
| `range` | Value within bounds | `p-value in [0.01, 0.05]` |
| `regex` | Text matches pattern | Correct group name |
| `file_exists` | Output file created | `summary.md` |

### 🏗️ Domain Distribution

| | Domain | Tasks | Points | F | I | A |
|:-:|:-------|------:|-------:|:-:|:-:|:-:|
| 1️⃣ | Data Cleaning & Validation | 9 | 57 | 2 | 4 | 3 |
| 2️⃣ | Data Preparation & Transformation | 8 | 52 | 2 | 4 | 2 |
| 3️⃣ | Descriptive Statistics & Measurement | 7 | 45 | 2 | 3 | 2 |
| 4️⃣ | Inferential Statistics | 16 | 122 | 3 | 5 | 8 |
| 5️⃣ | Applied Social Work Analytics | 8 | 56 | 1 | 3 | 4 |
| 6️⃣ | Text & Natural Language Processing | 3 | 29 | 0 | 2 | 1 |
| 7️⃣ | Multi-Step Data Analysis | 5 | 83 | 0 | 0 | 5 |
| | **Total** | **56** | **444** | **9** | **23** | **24** (F/I/A) |

---

## 🏆 Benchmark Results

> **Run 1** — March 4–5, 2026 · Qwen Code CLI v0.10.6 + Ollama 0.17.6 · Temp 0.3 · Domains 1–6 (51 tasks, 361 pts)

### Leaderboard

| Rank | Model | Params | Active | Quant | Score | % | Perfect |
|:----:|:------|-------:|-------:|:-----:|------:|--:|--------:|
| 🥇 | **Qwen3-Coder-Next** | 79.7B | 3.0B | Q4 | 356.5 / 361 | **98.8%** | 47 / 51 |
| 🥈 | **Qwen3.5-27B** | 27.8B | 27.8B | Q4 | 356.0 / 361 | **98.6%** | 47 / 51 |
| 🥉 | **Qwen3.5-122B-A10B** | 125.1B | 10.0B | Q4 | 356.0 / 361 | **98.6%** | 47 / 51 |
| 4 | Qwen3.5-35B-A3B | 36.0B | 3.0B | Q4 | 352.0 / 361 | 97.5% | 45 / 51 |
| 5 | Qwen3-Coder-30B | 30.5B | 3.3B | Q4 | 339.0 / 361 | 93.9% | 37 / 51 |
| 6 | Qwen3.5-9B Q4 | 9.7B | 9.7B | Q4 | 325.5 / 361 | 90.2% | 34 / 51 |
| 7 | Qwen3.5-9B Q8 | 9.7B | 9.7B | Q8 | 322.0 / 361 | 89.2% | 37 / 51 |

> All models ran locally on 2× NVIDIA RTX A6000 (98 GB VRAM total) via llama.cpp / Ollama. No cloud APIs.

### 📈 Performance by Domain

| Domain | Q3-Coder-Next | Q3.5-27B | Q3.5-122B | Q3.5-35B | Q3-Coder-30B | Q3.5-9B Q4 | Q3.5-9B Q8 |
|:-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 — Cleaning | 97.4% | 98.2% | 96.5% | 97.4% | 93.9% | 93.9% | 93.9% |
| 2 — Preparation | 100.0% | 100.0% | 100.0% | 99.0% | 100.0% | 95.2% | 76.9% |
| 3 — Descriptive | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 81.1% | 100.0% |
| 4 — Inferential | 97.5% | 96.7% | 97.5% | 98.4% | 91.4% | 91.0% | 93.0% |
| 5 — Applied | 100.0% | 100.0% | 100.0% | 91.1% | 89.3% | 87.5% | 89.3% |
| 6 — NLP | 100.0% | 100.0% | 100.0% | 100.0% | 93.1% | 89.7% | 69.0% |

### ⚡ Efficiency

| Model | Score | Time | Tokens | Tokens/Point | Tool Calls |
|:------|------:|-----:|-------:|-------------:|-----------:|
| Qwen3-Coder-Next | 98.8% | 3h 53m | 9.3M | 26,015 | 430 |
| Qwen3.5-27B | 98.6% | 2h 43m | 9.6M | 26,934 | 421 |
| Qwen3.5-122B-A10B | 98.6% | 3h 27m | 6.3M | 17,799 | 323 |
| Qwen3.5-35B-A3B | 97.5% | 1h 18m | 10.0M | 28,515 | 404 |
| Qwen3-Coder-30B | 93.9% | 1h 03m | 16.4M | 48,314 | 666 |
| Qwen3.5-9B Q4 | 90.2% | 1h 56m | 16.9M | 52,026 | 598 |
| Qwen3.5-9B Q8 | 89.2% | 1h 53m | 15.0M | 46,645 | 597 |

### 🔍 Hardest Tasks (Failed by 3+ Models)

| Task | Domain | Diff | Pts | Models Failed | Score Range |
|:-----|:------:|:----:|:---:|:-------------:|:------------|
| Exploratory Factor Analysis | D4 | A | 9 | 7/7 | 56–89% |
| Date Cleaning | D1 | I | 6 | 5/7 | 67–92% |
| One-Way ANOVA | D4 | I | 7 | 4/7 | 71–86% |
| Intraclass Correlation | D4 | A | 10 | 4/7 | 80–90% |
| Cronbach's Alpha | D5 | A | 8 | 4/7 | 25–62% |
| Outlier Detection | D1 | I | 6 | 3/7 | 92% |
| Missing Data Mechanisms | D1 | I | 10 | 3/7 | 90% |
| Wide to Long | D2 | F | 6 | 3/7 | 0–92% |
| Mann-Whitney U | D4 | I | 6 | 3/7 | 75–83% |
| Keyword Frequency | D6 | I | 9 | 3/7 | 67–78% |

> **Key insight:** The hardest task — Exploratory Factor Analysis — stumped every model. Factor extraction and item assignment require nuanced interpretation of eigenvalues and loadings that even 122B-parameter models struggle with. The second-hardest cluster involves date parsing edge cases and p-value approximation for hand-coded statistical tests.

---

## 📐 Design Constraints

The constraints below ensure the exam measures analytical capability and nothing else.

### 🔒 No dependency installation

**No task may require the model to install a Python package.** This is the single most important design constraint.

When a model fails because `pip install scipy` didn't work, the benchmark has measured the test environment — not the model's statistical knowledge. SWAT-Bench eliminates this variable:

- **42 of 56 tasks** use only the Python standard library (`csv`, `math`, `statistics`, `re`, `json`, `datetime`). The model must implement procedures from formulas, testing comprehension of the underlying mathematics.
- **14 tasks** permit pre-installed libraries for analyses where from-scratch implementation would be unreasonable.
- **No task requires matplotlib, seaborn, or any visualization library.**

This constraint also has a pedagogical benefit: a model that implements the Mann-Whitney U test from the formula demonstrates deeper statistical reasoning than one that calls `scipy.stats.mannwhitneyu()`.

### 🎯 One task, one analytical question

Each task asks one coherent analytical question. A task may involve multiple computational steps, but it does not bundle unrelated analyses into a single prompt. (Domain 7 is the exception — see [Multi-Step Tasks](#domain-7-multi-step-data-analysis--5-tasks-83-points).)

This matters for **diagnostic precision** (if a compound task scores 6/10, which capability failed?), **fair scoring** (one early error shouldn't cascade through unrelated checks), and **prompt clarity** (focused instructions produce fewer formatting errors).

### 📏 Additional constraints

1. **Structured data only.** CSV, JSON, or similar tabular/semi-structured files. No images, audio, or video.
2. **Deterministic correct answers.** Every scored check has an objectively correct answer. Where methods could produce different valid answers, the prompt specifies which method to use.
3. **Output format is fully specified.** The prompt includes an exact stdout format template.
4. **Social work context.** Each task provides a brief scenario (child welfare, mental health, substance use, housing, criminal justice, health equity) that frames the analysis.
5. **Reproducibility.** All input data is deterministically generated (`random.seed(42)`) or sourced from stable public datasets.
6. **Reasonable tolerances.** Numeric checks account for legitimate implementation differences (e.g., different OLS solvers).
7. **Task independence.** Each task is self-contained. No task depends on the output of another.
8. **Required output files.** Every task requires `solution.py` and stdout in the specified format.

---

## 📋 Task Catalog

### Domain 1: Data Cleaning & Validation — 9 tasks, 57 points

| ID | Task | Difficulty | Pts | Constraint |
|:---|:-----|:----------:|:---:|:----------:|
| [1-01](tasks/task-1-01-missing-data/) | **Missing Data Assessment** | Foundational | 5 | stdlib |
| [1-02](tasks/task-1-02-duplicate-detection/) | **Duplicate Detection** | Foundational | 6 | stdlib |
| [1-03](tasks/task-1-03-outlier-detection/) | **Outlier Detection** | Intermediate | 6 | stdlib |
| [1-04](tasks/task-1-04-date-cleaning/) | **Date and Timeline Cleaning** | Intermediate | 6 | stdlib |
| [1-05](tasks/task-1-05-recoding-standardization/) | **Recoding and Standardization** | Intermediate | 6 | stdlib |
| [1-06](tasks/task-1-06-missing-data-mechanisms/) | **Missing Data Mechanisms** | Intermediate | 10 | pandas/scipy |
| [1-07](tasks/task-1-07-codebook-application/) | **Codebook Application** | Advanced | 6 | stdlib |
| [1-08](tasks/task-1-08-skip-logic/) | **Skip Logic Validation** | Advanced | 6 | stdlib |
| [1-09](tasks/task-1-09-data-validation/) | **Comprehensive Data Validation** | Advanced | 6 | stdlib |

<details>
<summary>📝 Task descriptions</summary>

**Task 1-01 — Missing Data Assessment.**
A community mental health center is preparing program evaluation data for a funder report. Read a CSV of program outcomes and compute total records, missing values per column, complete vs. incomplete case counts, the column with the most missing data, and overall percent complete.

**Task 1-02 — Duplicate Detection.**
A child welfare agency's intake database has accumulated duplicate entries from multiple referral sources. Identify exact duplicate rows and conflicting records (same client_id, different data), produce deduplication counts, and output a cleaned CSV.

**Task 1-03 — Outlier Detection.**
A clinical supervisor reviewing PHQ-9 depression screening data notices unusual values. Flag records with impossible total scores, invalid item scores, sum mismatches, and severity category mismatches. Compute mean, median, and population SD of clean records.

**Task 1-04 — Date and Timeline Cleaning.**
A foster care agency is preparing case records for a longitudinal study. Detect format inconsistencies, impossible dates, sequence violations (exit before entry), and age-entry mismatches. Standardize all parseable dates to YYYY-MM-DD.

**Task 1-05 — Recoding and Standardization.**
A multi-site substance abuse treatment study collected data using different coding schemes. Harmonize gender labels, race/ethnicity labels, treatment completion coding, and satisfaction scores to a common scale.

**Task 1-06 — Missing Data Mechanisms.**
A doctoral student is auditing a mental health intake dataset. Quantify missingness per column, identify columns above 10% missing, and classify each column's missing data mechanism as MCAR or MAR by testing associations with observed variables.

**Task 1-07 — Codebook Application.**
A program evaluator received data where all variables are numeric codes. Read a codebook CSV, apply it to recode all coded columns, count unmapped codes, and identify the most common diagnosis and housing status.

**Task 1-08 — Skip Logic Validation.**
A research team administered a screening survey with conditional skip logic. Read skip rules, count should-be-empty and should-have-data violations, identify the most violated rule, and produce a violation report CSV.

**Task 1-09 — Comprehensive Data Validation.**
A PhD student needs to clean a messy participant dataset. Audit client records for 10 categories of data quality issues (duplicate IDs, missing fields, invalid dates, age-DOB mismatch, invalid zip codes, future dates, negative values, out-of-range values, invalid phones, inconsistent categories).

</details>

---

### Domain 2: Data Preparation & Transformation — 8 tasks, 52 points

| ID | Task | Difficulty | Pts | Constraint |
|:---|:-----|:----------:|:---:|:----------:|
| [2-01](tasks/task-2-01-data-filtering/) | **Data Filtering** | Foundational | 5 | stdlib |
| [2-02](tasks/task-2-02-wide-to-long/) | **Wide to Long Reshape** | Foundational | 6 | stdlib |
| [2-03](tasks/task-2-03-derived-variables/) | **Derived Variables** | Intermediate | 6 | stdlib |
| [2-04](tasks/task-2-04-multi-file-merge/) | **Multi-File Merge** | Intermediate | 6 | stdlib |
| [2-05](tasks/task-2-05-unit-harmonization/) | **Unit Harmonization** | Intermediate | 6 | stdlib |
| [2-06](tasks/task-2-06-long-to-wide/) | **Long to Wide Reshape** | Intermediate | 10 | stdlib |
| [2-07](tasks/task-2-07-binning-categorization/) | **Binning and Categorization** | Advanced | 6 | stdlib |
| [2-08](tasks/task-2-08-aggregation/) | **Aggregation** | Advanced | 7 | stdlib |

<details>
<summary>📝 Task descriptions</summary>

**Task 2-01 — Data Filtering.**
A grant report requires analysis of a specific subpopulation. Apply four sequential filters (gender, age range, diagnosis, referral year), report intermediate counts after each step, and compute summary statistics for the final subset.

**Task 2-02 — Wide to Long Reshape.**
A longitudinal foster care study tracks child outcomes at 3 time points in wide format. Reshape to long format with one row per child per time point, handle missing values, and compute mean scores by time point.

**Task 2-03 — Derived Variables.**
A program evaluation needs computed variables that don't exist in the raw data. Compute age from DOB, categorize into age groups, calculate poverty ratio, compute a weighted composite need score, and report distributions.

**Task 2-04 — Multi-File Merge.**
Combine data from three administrative systems (demographics, services, outcomes) linked by client_id. Count records per file, identify overlapping and orphan records, perform an inner join, and compute summary statistics.

**Task 2-05 — Unit Harmonization.**
A benefits eligibility study collected income data from 3 agencies reporting in different time periods. Convert all amounts to annual income, compute descriptive statistics, calculate poverty thresholds by household size, and determine the poverty rate.

**Task 2-06 — Long to Wide Reshape.**
A field education coordinator needs to transform long-format student assessment records into wide-format for accreditation reporting. Produce cross-tabulations of mean scores by competency and semester with change scores.

**Task 2-07 — Binning and Categorization.**
A community health needs assessment collected continuous clinical measures. Bin BMI, PHQ-9, GAD-7, and AUDIT-C scores into clinical categories using specified thresholds and compute rates for each severity level.

**Task 2-08 — Aggregation.**
A crisis hotline manager needs monthly and quarterly summary statistics from daily call logs covering all of 2024. Compute total calls, monthly volumes, busiest/quietest months, quarterly totals, and mean wait time from 366 days of logs.

</details>

---

### Domain 3: Descriptive Statistics & Measurement — 7 tasks, 45 points

| ID | Task | Difficulty | Pts | Constraint |
|:---|:-----|:----------:|:---:|:----------:|
| [3-01](tasks/task-3-01-frequency-distributions/) | **Frequency Distributions** | Foundational | 5 | stdlib |
| [3-02](tasks/task-3-02-percentiles-quartiles/) | **Percentiles and Quartiles** | Foundational | 5 | stdlib |
| [3-03](tasks/task-3-03-grouped-descriptives/) | **Grouped Descriptives** | Intermediate | 6 | stdlib |
| [3-04](tasks/task-3-04-rate-calculations/) | **Rate Calculations** | Intermediate | 6 | stdlib |
| [3-05](tasks/task-3-05-weighted-disparity/) | **Weighted Disparity Analysis** | Intermediate | 10 | pandas |
| [3-06](tasks/task-3-06-confidence-intervals/) | **Confidence Intervals** | Advanced | 6 | stdlib |
| [3-07](tasks/task-3-07-inter-rater-reliability/) | **Inter-Rater Reliability** | Advanced | 7 | stdlib |

<details>
<summary>📝 Task descriptions</summary>

**Task 3-01 — Frequency Distributions.**
A community needs assessment surveyed 200 residents about health concerns. Produce frequency tables with counts and percentages for categorical variables, compute mode and median, and identify most/least common categories.

**Task 3-02 — Percentiles and Quartiles.**
A school social worker needs percentile ranks for students' social-emotional learning scores. Compute mean, population SD, quartiles (linear interpolation), IQR, fences, potential outliers, subscale means, and identify the lowest-performing subscale.

**Task 3-03 — Grouped Descriptives.**
A substance abuse treatment program needs to compare client demographics and outcomes across four treatment modalities. Compute per-group N, mean age, success rate, mean change, and identify best-performing modalities.

**Task 3-04 — Rate Calculations.**
A county health department needs to compare rates of child abuse referrals, mental health utilization, and substance abuse admissions per 10,000 population across 6 districts. Merge service counts with population data and compute rates.

**Task 3-05 — Weighted Disparity Analysis.**
A health equity researcher is analyzing survey data on healthcare access disparities where the survey oversampled some racial groups. Compute unweighted and weighted means by racial group using sampling weights and calculate disparity ratios.

**Task 3-06 — Confidence Intervals.**
A state agency needs to report program success rates with 95% confidence intervals for 8 regional offices. Exclude in-progress records, compute Wilson score CIs, and identify the office with the widest CI.

**Task 3-07 — Inter-Rater Reliability.**
A faculty member is analyzing inter-rater reliability between an LLM and a human rater for a systematic review. Compute Cohen's Kappa from binary relevance ratings, including observed agreement, expected agreement, and standard interpretation.

</details>

---

### Domain 4: Inferential Statistics — 16 tasks, 122 points

| ID | Task | Difficulty | Pts | Constraint |
|:---|:-----|:----------:|:---:|:----------:|
| [4-01](tasks/task-4-01-paired-t-test/) | **Paired t-Test** | Foundational | 6 | stdlib |
| [4-02](tasks/task-4-02-independent-t-test/) | **Independent t-Test** | Foundational | 6 | stdlib |
| [4-03](tasks/task-4-03-chi-square/) | **Chi-Square Test** | Foundational | 5 | stdlib |
| [4-04](tasks/task-4-04-one-way-anova/) | **One-Way ANOVA** | Intermediate | 7 | stdlib |
| [4-05](tasks/task-4-05-spearman-correlation/) | **Spearman Correlation** | Intermediate | 5 | stdlib |
| [4-06](tasks/task-4-06-mann-whitney-u/) | **Mann-Whitney U Test** | Intermediate | 6 | stdlib |
| [4-07](tasks/task-4-07-multiple-regression/) | **Multiple Regression** | Intermediate | 10 | pandas/scipy/statsmodels/sklearn |
| [4-08](tasks/task-4-08-anova-posthoc/) | **ANOVA with Post-Hoc** | Intermediate | 10 | pandas/scipy/statsmodels |
| [4-09](tasks/task-4-09-wilcoxon-signed-rank/) | **Wilcoxon Signed-Rank** | Advanced | 6 | stdlib |
| [4-10](tasks/task-4-10-mcnemar-test/) | **McNemar's Test** | Advanced | 6 | stdlib |
| [4-11](tasks/task-4-11-fisher-exact-test/) | **Fisher's Exact Test** | Advanced | 7 | stdlib |
| [4-12](tasks/task-4-12-logistic-regression/) | **Logistic Regression** | Advanced | 10 | pandas/scipy/statsmodels/sklearn |
| [4-13](tasks/task-4-13-interrupted-time-series/) | **Interrupted Time Series** | Advanced | 9 | pandas/scipy/statsmodels |
| [4-14](tasks/task-4-14-reliable-change-index/) | **Reliable Change Index** | Advanced | 10 | stdlib |
| [4-15](tasks/task-4-15-intraclass-correlation/) | **Intraclass Correlation** | Advanced | 10 | pandas/scipy/pingouin |
| [4-16](tasks/task-4-16-exploratory-factor-analysis/) | **Exploratory Factor Analysis** | Advanced | 9 | pandas/numpy/sklearn/factor_analyzer |

<details>
<summary>📝 Task descriptions</summary>

**Task 4-01 — Paired t-Test.**
A community mental health center evaluating their 12-week CBT program. Implement a paired-samples t-test from scratch, computing pre/post means, SD of differences, t-statistic, approximate p-value, and Cohen's d.

**Task 4-02 — Independent t-Test.**
A housing authority comparing stability scores between intensive case management and treatment-as-usual. Implement Welch's t-test with Welch-Satterthwaite degrees of freedom and Cohen's d using pooled SD.

**Task 4-03 — Chi-Square Test.**
An MSW program director testing whether program track is associated with licensing exam pass rates. Build a contingency table, compute chi-square and Cramer's V.

**Task 4-04 — One-Way ANOVA.**
A social service agency comparing client satisfaction across four service models. Implement one-way ANOVA from scratch (SS decomposition, F-statistic), compute eta-squared, and identify highest/lowest scoring models.

**Task 4-05 — Spearman Correlation.**
A school social worker examining the relationship between family income rank and behavioral incidents. Compute Spearman rank correlation with average ranks for ties and test significance.

**Task 4-06 — Mann-Whitney U Test.**
A housing program comparing length of prior homelessness between two program types with highly skewed data. Implement Mann-Whitney U with tied-rank handling and rank-biserial effect size.

**Task 4-07 — Multiple Regression.**
A child welfare researcher examining which case-level factors are associated with placement recurrence risk. Fit a multiple linear regression, report R-squared, F-statistic, coefficients, and identify the most significant factor.

**Task 4-08 — ANOVA with Post-Hoc.**
A substance use researcher comparing recovery outcomes across four treatment modalities. Perform one-way ANOVA with eta-squared and pairwise post-hoc comparisons with Bonferroni or Tukey correction.

**Task 4-09 — Wilcoxon Signed-Rank.**
A domestic violence shelter testing whether self-efficacy scores changed pre- to post-program with non-normal data. Implement the Wilcoxon signed-rank test with normal approximation and effect size r.

**Task 4-10 — McNemar's Test.**
A re-entry program testing whether employment status significantly changed from entry to follow-up. Build a transition table, compute McNemar's chi-square, odds ratio, and net change.

**Task 4-11 — Fisher's Exact Test.**
A child welfare agency testing whether maltreatment type is associated with case outcome with small cell counts. Implement Fisher's exact test using hypergeometric probabilities, odds ratio, and relative risk.

**Task 4-12 — Logistic Regression.**
A program evaluator examining which client characteristics are associated with program completion. Fit logistic regression, compute McFadden's pseudo R-squared, classification accuracy, and odds ratios.

**Task 4-13 — Interrupted Time Series.**
A policy researcher evaluating the impact of a caseload cap policy using 60 months of data. Fit a segmented regression model to estimate level change and slope change.

**Task 4-14 — Reliable Change Index.**
A clinical supervisor evaluating PHQ-9 treatment outcomes for 100 clients. Compute SEM, clinical threshold using Jacobson-Truax, RCI for each client, and classify into Recovered/Improved/Unchanged/Deteriorated.

**Task 4-15 — Intraclass Correlation.**
A clinical supervisor evaluating inter-rater consistency among 4 raters scoring 50 clinical vignettes. Compute ICC(2,1) via two-way ANOVA decomposition with 95% confidence interval.

**Task 4-16 — Exploratory Factor Analysis.**
A doctoral student examining the factor structure of a 20-item screening instrument. Compute KMO, Bartlett's test, eigenvalues, determine factors via Kaiser criterion, and assign items to factors.

</details>

---

### Domain 5: Applied Social Work Analytics — 8 tasks, 56 points

| ID | Task | Difficulty | Pts | Constraint |
|:---|:-----|:----------:|:---:|:----------:|
| [5-01](tasks/task-5-01-caseload-analysis/) | **Caseload Analysis** | Foundational | 5 | stdlib |
| [5-02](tasks/task-5-02-pearson-correlation-matrix/) | **Pearson Correlation Matrix** | Intermediate | 5 | stdlib |
| [5-03](tasks/task-5-03-effect-sizes/) | **Effect Sizes for Meta-Analysis** | Intermediate | 6 | stdlib |
| [5-04](tasks/task-5-04-cost-effectiveness/) | **Cost-Effectiveness Analysis** | Intermediate | 10 | pandas |
| [5-05](tasks/task-5-05-racial-disproportionality/) | **Racial Disproportionality** | Advanced | 7 | stdlib |
| [5-06](tasks/task-5-06-risk-assessment/) | **Risk Assessment Validation** | Advanced | 7 | stdlib |
| [5-07](tasks/task-5-07-cronbachs-alpha/) | **Cronbach's Alpha** | Advanced | 8 | stdlib |
| [5-08](tasks/task-5-08-state-level-trend-analysis/) | **State-Level Trend Analysis** | Advanced | 8 | stdlib |

<details>
<summary>📝 Task descriptions</summary>

**Task 5-01 — Caseload Analysis.**
An agency director needs a data-driven analysis of worker caseloads. Compute per-worker caseload counts, success rates, average days to closure, and satisfaction. Identify highest caseload and lowest success rate workers.

**Task 5-02 — Pearson Correlation Matrix.**
A field placement coordinator examining which student characteristics are associated with evaluation scores. Compute a full pairwise Pearson correlation matrix and identify the strongest correlations.

**Task 5-03 — Effect Sizes for Meta-Analysis.**
A systematic review team computing effect sizes from published parenting intervention studies. Compute Cohen's d, Hedges' g, confidence intervals, and the inverse-variance-weighted pooled Hedges' g.

**Task 5-04 — Cost-Effectiveness Analysis.**
A program director comparing cost-effectiveness of three service programs. Calculate total and per-client costs, cost per outcome unit, and Incremental Cost-Effectiveness Ratios versus the cheapest program.

**Task 5-05 — Racial Disproportionality.**
A state child welfare agency conducting a racial equity audit. Compute referral rates per 1,000 children by race, disproportionality indices, substantiation rates, and relative risk ratios.

**Task 5-06 — Risk Assessment Validation.**
A child protective services agency validating their risk assessment tool. Compute confusion matrix metrics (sensitivity, specificity, PPV, NPV, F1), AUC via trapezoidal rule, and optimal cutoff using Youden's J.

**Task 5-07 — Cronbach's Alpha.**
A faculty member validating a test anxiety instrument. Parse a two-row header survey, identify reverse-coded items, compute Cronbach's alpha, corrected item-total correlations, and alpha-if-deleted.

**Task 5-08 — State-Level Trend Analysis.**
A criminal justice researcher analyzing geographic and temporal trends in fatal police shootings. Count shootings by state and year, identify top-10 states, and compute year-over-year changes.

</details>

---

### Domain 6: Text & Natural Language Processing — 3 tasks, 29 points

| ID | Task | Difficulty | Pts | Constraint |
|:---|:-----|:----------:|:---:|:----------:|
| [6-01](tasks/task-6-01-keyword-frequency/) | **Keyword Frequency Analysis** | Intermediate | 9 | stdlib |
| [6-02](tasks/task-6-02-lexicon-sentiment/) | **Lexicon-Based Sentiment Analysis** | Intermediate | 10 | pandas |
| [6-03](tasks/task-6-03-term-pattern-matching/) | **Term Pattern Matching** | Advanced | 10 | stdlib |

<details>
<summary>📝 Task descriptions</summary>

**Task 6-01 — Keyword Frequency Analysis.**
A policy researcher analyzing public comments on a federal rulemaking. Use regex patterns with word boundaries to count comments mentioning social work and nursing terms case-insensitively and produce daily counts.

**Task 6-02 — Lexicon-Based Sentiment Analysis.**
An evaluator analyzing client satisfaction feedback from 5 programs. Tokenize text, match against a 200-word sentiment lexicon, sum scores per response, classify as positive/negative/neutral, and compute mean sentiment by program.

**Task 6-03 — Term Pattern Matching.**
A research team conducting content analysis of 20 years of conference abstracts. Read keyword stems from CSV, perform case-insensitive wildcard-stem regex matching against ~18 MB of abstracts, count each keyword at most once per abstract, and rank by frequency.

</details>

---

### Domain 7: Multi-Step Data Analysis — 5 tasks, 83 points

> **New in v2.** Unlike Domains 1–6 which follow a "one task, one analytical question" design, these tasks require **4–10 sequential analytical steps** that mirror the real-world complexity of child welfare administrative data analysis.

All five tasks use synthetic data modeled on the MISACWIS child welfare information system. A key property is the **cascade effect**: an error in an early step (e.g., incorrect deduplication, wrong merge key) causes all downstream checks to fail, making these tasks highly discriminative between models of different capability levels.

| ID | Task | Difficulty | Pts | Constraint |
|:---|:-----|:----------:|:---:|:----------:|
| [7-01](tasks/task-7-01-allegation-funnel/) | **Allegation-to-Removal Funnel** | Advanced | 15 | stdlib |
| [7-02](tasks/task-7-02-placement-stability/) | **Placement Stability by Age & Race** | Advanced | 18 | stdlib |
| [7-03](tasks/task-7-03-time-to-permanency/) | **Time-to-Permanency with Re-entry** | Advanced | 16 | stdlib |
| [7-04](tasks/task-7-04-racial-disparity/) | **Racial Disparity in Substantiation** | Advanced | 16 | stdlib |
| [7-05](tasks/task-7-05-point-in-time-snapshot/) | **Point-in-Time Foster Care Snapshot** | Advanced | 18 | stdlib |

<details>
<summary>📝 Task descriptions</summary>

**Task 7-01 — Allegation-to-Removal Funnel Analysis.**
A child welfare agency analyzing the allegation-to-removal pipeline. Load allegation-level records, deduplicate to unique child-intake pairs, compute screening-in and substantiation rates through a multi-stage funnel, merge with a bridge table to link substantiated cases to removals, and produce county-level conversion rates.

**Task 7-02 — Placement Stability by Child Age and Race.**
A federally-mandated placement stability analysis. Merge four CSV files (child info, race, removals, placements), compute age at removal using date arithmetic with floor logic, bin into age groups, count placements per episode, and produce two-dimensional stability metrics by age group and race.

**Task 7-03 — Time-to-Permanency with Re-entry Flagging.**
A federal permanency metrics analysis. Classify removal episodes as discharged or still-in-care, identify children with multiple episodes, detect re-entries within 12 months using pairwise chronological comparisons, compute median time-in-care by discharge reason, and calculate mean age at first removal.

**Task 7-04 — Racial Disparity in Substantiation and Removal.**
A state-level racial equity audit of the child welfare system. Deduplicate allegation records, merge with race data, compute substantiation and removal rates by race through a multi-stage funnel with changing denominators, calculate relative risk ratios using White as the reference group, and identify the most overrepresented group at each stage.

**Task 7-05 — Point-in-Time Foster Care Snapshot.**
An AFCARS-style point-in-time analysis of all children in foster care on October 1, 2023. Apply temporal filtering with NULL handling for open episodes, determine current placements from history records, merge four tables, compute cross-sectional demographics (age, length of stay, placement type, race), and produce county-level aggregations with medians and rankings.

</details>

---

## 🚀 Running the Benchmark

```bash
# From the scripts/ directory:

# Run all 56 tasks with a model
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
├── tasks/                 # 56 task definitions
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

<p align="center">
<strong>SWAT-Bench</strong> — 56 tasks · 444 points · 7 domains<br>
<em>Evaluating local LLMs for social work research data analysis</em>
</p>
