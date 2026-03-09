A program evaluator received client assessment data where all variables are stored as numeric codes and needs to apply the study codebook to convert codes to human-readable labels for reporting.

# Task: Codebook Application

## Input Files

1. `assessment_data.csv` — 100 client assessment records with columns: client_id, q1_diagnosis, q2_severity, q3_housing, q4_employment, q5_education, q6_insurance, score_total
   - All q1 through q6 columns contain numeric codes (1-5)
   - score_total is a numeric score (not a code) and should NOT be recoded

2. `codebook.csv` — Maps variable names to code-label pairs with columns: variable, code, label
   - Each row maps a specific variable + numeric code to its human-readable label
   - Example: variable=q1_diagnosis, code=1, label="Major Depressive Disorder"

## Required Output

1. **Script:** `solution.py` — Python script that reads both files, applies the codebook to recode all q_ columns, and produces output.

2. **Stdout:** Print the following lines exactly:
```
Total records: <N>
Total variables to recode: <N>
Unmapped codes found: <N>
Records with all codes mapped: <N>

Value counts for q1_diagnosis:
  Major Depressive Disorder: <N>
  Generalized Anxiety: <N>
  PTSD: <N>
  Substance Use Disorder: <N>
  Adjustment Disorder: <N>

Most common diagnosis: <label>
Most common housing status: <label>
Mean total score: <X.XX>
```

Notes:
- "Total variables to recode" = the number of distinct variable names in the codebook (the q_ columns).
- "Unmapped codes found" = total number of individual cells across all q_ columns where the code did not have a matching entry in the codebook. Count each cell, not each row.
- "Records with all codes mapped" = number of rows where every q_ column had a valid codebook mapping.
- "Most common diagnosis" = the q1_diagnosis label with the highest count.
- "Most common housing status" = the q3_housing label with the highest count.
- "Mean total score" = mean of score_total column, formatted to 2 decimal places.
- Value counts for q1_diagnosis should be listed in the exact order shown above.

3. **Output file:** `labeled_data.csv` — the assessment data with all q_ columns replaced by their human-readable labels. score_total remains numeric.

4. **Summary:** `summary.md` — brief description of the recoding process and any findings.

## Constraints

- Python standard library ONLY (no pandas, numpy, scipy, sklearn).
- The script must be named `solution.py` and run with `python3 solution.py`.

## Evaluation Criteria

- Correct record count and variable count
- Accurate unmapped code detection
- Correct most common diagnosis and housing status
- Accurate mean score calculation
- Output files exist (labeled_data.csv, summary.md)
