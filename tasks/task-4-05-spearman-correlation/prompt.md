# Spearman Rank Correlation Analysis

## Context
You are a data analyst working with a school social worker who wants to examine the relationship between family income rank and student behavioral incident frequency. Both variables are non-normal (one is ordinal, one is a count), making Spearman rank correlation the appropriate measure.

## Input
- `student_behavior.csv`: Contains data on 60 students with the following columns:
  - `student_id`: Student identifier
  - `grade`: Grade level (6-12)
  - `family_income_rank`: Ordinal ranking of family income (1-60, where 1 is lowest)
  - `behavioral_incidents`: Count of behavioral incidents (0-15)
  - `attendance_rate`: School attendance percentage
  - `gpa`: Grade point average

## Task
Using **only the Python standard library** (no numpy, pandas, scipy, or other external packages), write a Python script called `solution.py` that:

1. Reads `student_behavior.csv`
2. Computes descriptive statistics (total students, mean incidents, mean income rank)
3. Computes Spearman rank correlation between family income rank and behavioral incidents
4. Tests significance of the correlation (p < 0.05)
5. Writes a brief `summary.md` file summarizing findings

## Required Output (stdout)
Print the following to stdout with **exactly** these labels:

```
Total students: <N>
Mean incidents: <X.XX>
Mean income rank: <X.XX>

Spearman correlation (income rank vs incidents): <X.XXXX>
p-value: <X.XXXX>
Significant (p < 0.05): <Yes/No>
Direction: <Negative/Positive>
```

## Notes
- Spearman correlation can be computed by ranking the data and then computing the Pearson correlation on the ranks
- For tied ranks, use average ranks
- For p-value, you can use the t-distribution approximation: t = r * sqrt((n-2)/(1-r^2)) with n-2 degrees of freedom
- Use the math module for sqrt and the statistics module as needed
