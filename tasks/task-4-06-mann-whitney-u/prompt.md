# Mann-Whitney U Test

## Context
You are a data analyst for a housing program that wants to compare the length of prior homelessness (in days) between clients who received Rapid Rehousing versus Transitional Housing. The duration data is highly right-skewed (not normally distributed), making the Mann-Whitney U test more appropriate than a t-test.

## Input
- `housing_program.csv`: Contains data on 70 clients with the following columns:
  - `client_id`: Client identifier
  - `program_type`: "Rapid Rehousing" or "Transitional Housing"
  - `days_homeless_prior`: Number of days homeless before program entry
  - `age`: Client age
  - `gender`: Client gender
  - `has_children`: Whether client has children (0/1)
  - `employed_at_exit`: Whether employed at program exit (0/1)

## Task
Using **only the Python standard library** (no numpy, pandas, scipy, or other external packages), write a Python script called `solution.py` that:

1. Reads `housing_program.csv`
2. Separates data by program type
3. Computes median days homeless for each group
4. Performs a Mann-Whitney U test (two-sided)
5. Computes the rank-biserial effect size: r = 1 - 2U/(n1*n2)
6. Writes a brief `summary.md` file summarizing findings

## Required Output (stdout)
Print the following to stdout with **exactly** these labels:

```
Total clients: <N>
Rapid Rehousing: <N>
Transitional Housing: <N>

Rapid Rehousing - Median days homeless: <X.X>
Transitional Housing - Median days homeless: <X.X>

Mann-Whitney U statistic: <X.X>
p-value: <X.XXXX>
Significant (p < 0.05): <Yes/No>
Effect size (rank-biserial r): <X.XXX>
Median difference: <X.X>
```

## Notes
- The Mann-Whitney U test ranks all observations together and compares sum of ranks between groups
- U = n1*n2 + n1*(n1+1)/2 - R1 (where R1 is sum of ranks for group 1)
- For large samples (n > 20), use the normal approximation: z = (U - n1*n2/2) / sqrt(n1*n2*(n1+n2+1)/12)
- Handle tied ranks by using average ranks
- The median difference is Transitional median minus Rapid Rehousing median
- Use the math module for calculations
