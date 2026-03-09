# Confidence Intervals for Regional Program Success Rates

## Context
A state agency needs to report program success rates with 95% confidence intervals for 8 regional offices. Some offices have small sample sizes, making confidence intervals essential for meaningful comparison.

## Input
- `regional_outcomes.csv` (~400 rows)
- Columns: client_id, regional_office (8 offices), program_type, enrollment_date, completion_status (Completed/Not Completed/In Progress), days_enrolled

## Task
Write a Python script (`solution.py`) using only the standard library that reads the CSV file, excludes "In Progress" records, and computes success rates with Wilson score confidence intervals. Print all results to stdout in the exact format shown below.

## Required Output Format (stdout)
```
Total records: <N>
In Progress (excluded): <N>
Analyzed records: <N>

Regional success rates with 95% CI:
  Office_A: <X.X>% [<X.X>%, <X.X>%] (n=<N>)
  Office_B: <X.X>% [<X.X>%, <X.X>%] (n=<N>)
  Office_C: <X.X>% [<X.X>%, <X.X>%] (n=<N>)
  Office_D: <X.X>% [<X.X>%, <X.X>%] (n=<N>)
  Office_E: <X.X>% [<X.X>%, <X.X>%] (n=<N>)
  Office_F: <X.X>% [<X.X>%, <X.X>%] (n=<N>)
  Office_G: <X.X>% [<X.X>%, <X.X>%] (n=<N>)
  Office_H: <X.X>% [<X.X>%, <X.X>%] (n=<N>)

Overall success rate: <X.X>% [<X.X>%, <X.X>%]
Highest success office: <name>
Lowest success office: <name>
Widest CI office: <name>
```

## Required Output Files
1. `regional_report.csv` — Contains office, n, successes, success_rate, ci_lower, ci_upper, ci_width columns.
2. `summary.md` — A brief markdown summary of the key findings.

## Constraints
- Use only Python standard library (no pandas, numpy, scipy, etc.)
- Read data from `regional_outcomes.csv` in the current directory
- Print results to stdout in the exact format above
- Only "Completed" and "Not Completed" records count for success rate analysis. Exclude "In Progress" records entirely.
- Success = "Completed"
- Use the Wilson score interval for confidence intervals:
  - center = (p_hat + z^2/(2n)) / (1 + z^2/n)
  - margin = z * sqrt(p_hat*(1-p_hat)/n + z^2/(4n^2)) / (1 + z^2/n)
  - lower = center - margin, upper = center + margin
  - where z = 1.96 for 95% CI
  - Clamp bounds to [0, 100] percent
- List offices in order: Office_A through Office_H
- "Widest CI office" = office with largest (upper - lower) interval width
