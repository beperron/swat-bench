# Test 041: Data Subsetting and Filtering

## Context

A grant report requires analysis of a specific subpopulation from a community behavioral health center's full client database. The evaluator needs to extract the subset of **female clients ages 18-35 with Substance Abuse as their primary diagnosis who were referred in 2024**. The filtering must be performed step-by-step so intermediate counts can be reported for data validation purposes.

## Input Files

- **`full_client_database.csv`** (~300 rows) with columns:
  - `client_id` — unique client identifier
  - `gender` — "Male", "Female", or "Non-binary"
  - `age` — integer age
  - `primary_diagnosis` — diagnosis category string
  - `referral_date` — date in YYYY-MM-DD format
  - `services_received` — type of service
  - `discharge_status` — "Completed", "Dropped Out", "Transferred", "Still Active", or "Administrative"
  - `county` — county name
  - `total_sessions` — integer count of sessions
  - `outcome_score` — numeric outcome measure (0-100)

## Task

Write `solution.py` that reads the client database and applies the following filters **sequentially**, reporting the count after each filter step:

1. **Gender**: keep only rows where `gender == "Female"`
2. **Age**: keep only rows where `18 <= age <= 35`
3. **Primary diagnosis**: keep only rows where `primary_diagnosis == "Substance Abuse"`
4. **Referral year**: keep only rows where `referral_date` is in year 2024

After filtering, compute summary statistics for the final subset.

## Required Output

### Standard Output (stdout)

Print the following lines exactly:

```
Total records in database: <N>
After filter (Female): <N>
After filter (age 18-35): <N>
After filter (Substance Abuse): <N>
After filter (2024 referrals): <N>
Final subset size: <N>
Subset mean age: <X.X>
Subset mean sessions: <X.X>
Subset mean outcome score: <X.XX>
Subset discharge rate (Completed): <X.X>%
```

### Output Files

1. **`subset.csv`** — the filtered subset with the same columns as the input
2. **`summary.md`** — a brief markdown summary describing the filtering criteria, the number of records at each step, and the final subset statistics

## Constraints

- Use only Python standard library (no pandas, numpy, or other external packages)
- Read from `full_client_database.csv` in the current working directory
- Write output files to the current working directory

## Eval Criteria

- Correct total record count from the input file
- Correct intermediate and final filter counts
- Accurate computation of mean age, mean sessions, mean outcome score
- Correct discharge rate calculation (percentage of "Completed" in subset)
- Output CSV file with the correct filtered data
- Summary markdown file exists with meaningful content
