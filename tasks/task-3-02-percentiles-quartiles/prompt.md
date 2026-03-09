# Percentiles and Quartiles for Student SEL Scores

## Context
A school social worker needs to compute percentile ranks for students' social-emotional learning (SEL) assessment scores to identify those in the bottom quartile who may need additional support.

## Input
- `student_sel_scores.csv` (~100 rows)
- Columns: student_id, grade, gender, sel_total_score (0-100), self_awareness (0-25), self_management (0-25), social_awareness (0-25), relationship_skills (0-25)

## Task
Write a Python script (`solution.py`) using only the standard library that reads the CSV file and computes percentile-based statistics. Print all results to stdout in the exact format shown below.

## Required Output Format (stdout)
```
Total students: <N>

SEL Total Score:
  Mean: <X.XX>
  Std: <X.XX>
  Min: <N>
  Max: <N>
  Q1 (25th percentile): <X.XX>
  Q2 (median): <X.XX>
  Q3 (75th percentile): <X.XX>
  IQR: <X.XX>
  Lower fence: <X.XX>
  Upper fence: <X.XX>
  Potential outliers: <N>

Students below Q1 (need support): <N>
Students above Q3 (high performers): <N>

Subscale means:
  Self-Awareness: <X.XX>
  Self-Management: <X.XX>
  Social-Awareness: <X.XX>
  Relationship-Skills: <X.XX>

Lowest subscale: <name>
```

## Required Output Files
1. `summary.md` — A brief markdown summary of the key findings.

## Constraints
- Use only Python standard library (no pandas, numpy, scipy, etc.)
- Read data from `student_sel_scores.csv` in the current directory
- Print results to stdout in the exact format above
- For standard deviation: use population standard deviation (divide by N, not N-1)
- For percentiles: use linear interpolation method. Sort the data, compute index = (n-1) * p / 100, then linearly interpolate between floor and ceiling positions.
- Lower fence = Q1 - 1.5 * IQR; Upper fence = Q3 + 1.5 * IQR
- Potential outliers: count of values below lower fence or above upper fence
- "Students below Q1" = students with score strictly less than Q1
- "Students above Q3" = students with score strictly greater than Q3
