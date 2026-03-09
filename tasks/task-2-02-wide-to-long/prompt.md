A longitudinal foster care study tracks child outcomes at 3 time points (baseline, 6-month, 12-month). The data is stored in wide format (one row per child) and needs to be converted to long format for repeated-measures analysis.

# Task

Reshape the wide-format outcome data into long format, report the structural changes, and compute summary statistics for key outcome measures.

## Input Files

- `outcomes_wide.csv`: ~50 rows of child outcome data in wide format.
  - Columns: `child_id`, `age`, `gender`, `placement_type`, `wellbeing_t0`, `wellbeing_t1`, `wellbeing_t2`, `behavior_t0`, `behavior_t1`, `behavior_t2`, `academic_t0`, `academic_t1`, `academic_t2`
  - The `_t0`, `_t1`, `_t2` suffixes represent baseline, 6-month, and 12-month time points respectively.
  - Some measurement cells may be empty (missing values).

## Required Output

1. **`solution.py`**: Python script that reads the CSV, reshapes it, and prints the analysis to stdout.

2. **Standard output** must print exactly:
```
Wide format:
  Rows: <N>
  Columns: <N>

Long format:
  Rows: <N>
  Columns: <N>
  Unique children: <N>
  Time points per child: 3

Missing values in long format: <N>
Mean wellbeing (baseline): <X.XX>
Mean wellbeing (12-month): <X.XX>
Mean behavior (baseline): <X.XX>
Mean academic (baseline): <X.XX>
```

- The long format should have columns: `child_id`, `age`, `gender`, `placement_type`, `time_point`, `wellbeing`, `behavior`, `academic`.
- `time_point` should be 0, 1, or 2 (corresponding to t0, t1, t2).
- Each child gets 3 rows in long format (one per time point), so long rows = wide rows * 3.
- "Long format Columns" = 8 (the columns listed above).
- "Missing values in long format" = total count of empty/missing cells across the wellbeing, behavior, and academic columns in the long format.
- Mean calculations should skip missing values (compute mean over non-missing values only).

3. **`outcomes_long.csv`**: The reshaped data in long format with the columns specified above.

4. **`summary.md`**: Brief summary of the reshape operation and key findings.

## Constraints

- Use only Python standard library (no pandas, numpy, or other external packages).

## Evaluation Criteria

- Correct structural transformation from wide to long format.
- Proper handling of missing values during reshape.
- Accurate computation of summary statistics (means computed over non-missing values).
- Correct row and column counts for both formats.
