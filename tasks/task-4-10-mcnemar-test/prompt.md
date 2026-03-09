# McNemar's Test

## Context
You are a data analyst for a re-entry program serving formerly incarcerated individuals. The program wants to test whether employment status significantly changed from program entry to 6-month follow-up. Since this involves matched pre-post binary data (same individuals measured twice), McNemar's test is the appropriate statistical method.

## Input
- `reentry_employment.csv`: Contains data on 80 participants with the following columns:
  - `client_id`: Client identifier
  - `age`: Client age
  - `gender`: Client gender
  - `offense_type`: Type of offense
  - `pre_employed`: Employment status at entry (0=unemployed, 1=employed)
  - `post_employed`: Employment status at 6-month follow-up (0=unemployed, 1=employed)
  - `program_hours`: Hours of program participation
  - `housing_status`: Current housing status

## Task
Using **only the Python standard library** (no numpy, pandas, scipy, or other external packages), write a Python script called `solution.py` that:

1. Reads `reentry_employment.csv`
2. Computes pre and post employment rates
3. Builds the 2x2 contingency table of transitions
4. Performs McNemar's test (without continuity correction)
5. Computes the odds ratio for discordant pairs
6. Writes a brief `summary.md` file summarizing findings

## Required Output (stdout)
Print the following to stdout with **exactly** these labels:

```
Total participants: <N>
Pre-employment rate: <X.X>%
Post-employment rate: <X.X>%

Contingency table:
  Employed→Employed: <N>
  Employed→Unemployed: <N>
  Unemployed→Employed: <N>
  Unemployed→Unemployed: <N>

McNemar chi-square: <X.XX>
p-value: <X.XXXX>
Significant (p < 0.05): <Yes/No>
Odds ratio (discordant): <X.XX>
Net change: <N> more employed
```

## Notes
- McNemar's chi-square (without continuity correction) = (b - c)^2 / (b + c), where:
  - b = count of Employed→Unemployed transitions
  - c = count of Unemployed→Employed transitions
- The p-value comes from a chi-square distribution with 1 degree of freedom
- Odds ratio for discordant pairs = c / b
- Net change = c - b (number of additional people employed)
- Use the math module for calculations
- For the chi-square CDF, you can use the relationship with the incomplete gamma function or the normal approximation
