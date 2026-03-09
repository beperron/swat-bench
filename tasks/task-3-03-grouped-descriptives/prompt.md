# Grouped Descriptive Statistics for Treatment Modalities

## Context
A substance abuse treatment program needs to compare client demographics and outcomes across four treatment modalities (Inpatient, Outpatient, Intensive Outpatient, MAT) for their annual report.

## Input
- `treatment_data.csv` (~160 rows, ~40 per group)
- Columns: client_id, treatment_modality, age, gender, days_in_treatment, sessions_completed, pre_score, post_score, successful_discharge (0/1)

## Task
Write a Python script (`solution.py`) using only the standard library that reads the CSV file and computes grouped descriptive statistics by treatment modality. Print all results to stdout in the exact format shown below.

## Required Output Format (stdout)
```
Total clients: <N>

By treatment modality:
Inpatient - N: <N>, Mean age: <X.X>, Mean days: <X.X>, Success rate: <X.X>%, Mean pre: <X.X>, Mean post: <X.X>, Mean change: <X.X>
Outpatient - N: <N>, Mean age: <X.X>, Mean days: <X.X>, Success rate: <X.X>%, Mean pre: <X.X>, Mean post: <X.X>, Mean change: <X.X>
IOP - N: <N>, Mean age: <X.X>, Mean days: <X.X>, Success rate: <X.X>%, Mean pre: <X.X>, Mean post: <X.X>, Mean change: <X.X>
MAT - N: <N>, Mean age: <X.X>, Mean days: <X.X>, Success rate: <X.X>%, Mean pre: <X.X>, Mean post: <X.X>, Mean change: <X.X>

Overall success rate: <X.X>%
Highest success modality: <name>
Largest mean improvement: <name>
Overall mean pre-score: <X.XX>
Overall mean post-score: <X.XX>
```

## Required Output Files
1. `group_summary.csv` — Contains modality, n, mean_age, mean_days, success_rate, mean_pre, mean_post, mean_change columns.
2. `summary.md` — A brief markdown summary of the key findings.

## Constraints
- Use only Python standard library (no pandas, numpy, scipy, etc.)
- Read data from `treatment_data.csv` in the current directory
- Print results to stdout in the exact format above
- "Mean change" = mean of (pre_score - post_score) for each client (positive means improvement since scores represent severity)
- Success rate = percentage of clients with successful_discharge = 1
- List modalities in this order: Inpatient, Outpatient, IOP, MAT
