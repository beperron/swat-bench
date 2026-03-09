# Frequency Distributions for Community Needs Assessment

## Context
A community needs assessment surveyed 200 residents about their primary health concerns, barriers to services, and preferred service delivery methods. The program director needs frequency tables for grant reporting.

## Input
- `needs_assessment.csv` (~200 rows)
- Columns: respondent_id, age, gender, zip_code, primary_concern (6 categories), barrier_type (5 categories), preferred_method (4 categories), num_dependents, income_bracket (5 brackets)

## Task
Write a Python script (`solution.py`) using only the standard library that reads the CSV file and produces the following analysis. Print all results to stdout in the exact format shown below.

## Required Output Format (stdout)
```
Total respondents: <N>

Primary concern frequencies:
  Mental Health: <N> (<X.X>%)
  Substance Abuse: <N> (<X.X>%)
  Housing: <N> (<X.X>%)
  Employment: <N> (<X.X>%)
  Childcare: <N> (<X.X>%)
  Healthcare Access: <N> (<X.X>%)

Most common concern: <category>
Least common concern: <category>

Barrier frequencies:
  Transportation: <N>
  Cost: <N>
  Awareness: <N>
  Language: <N>
  Stigma: <N>

Most common barrier: <category>
Mode of num_dependents: <N>
Median num_dependents: <X.X>
```

## Required Output Files
1. `frequency_tables.csv` — Contains category_type, category, count, and percentage columns for all primary concerns and barriers.
2. `summary.md` — A brief markdown summary of the key findings.

## Constraints
- Use only Python standard library (no pandas, numpy, scipy, etc.)
- Read data from `needs_assessment.csv` in the current directory
- Print results to stdout in the exact format above
- For the mode: the most frequently occurring value of num_dependents
- For the median: standard median calculation (average of middle two values if even count)
