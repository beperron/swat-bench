A doctoral student in social work is auditing a mental health intake dataset before running their dissertation analyses. They need to understand the missing data patterns to determine the appropriate handling strategy.

# Task: Missing Data Pattern Assessment

Analyze a mental health intake dataset to identify columns with substantial missing data, quantify the missingness, and classify the likely missing data mechanism (MCAR vs. MAR).

## Input Files

- `mh_intake.csv` — 800 client intake records with 13 columns including demographics (age, gender, race), clinical measures (phq9_score, gad7_score, bdi_score), and service variables (sessions_attended, diagnosis, insurance, education, income).

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total rows: <N>
   Total columns: <N>
   Overall missing: <X.X>%
   Columns above 10% missing: <N>
   Highest missing column: <COLUMN_NAME> (<X.X>%)
   income missing: <X.X>%
   education missing: <X.X>%
   bdi_score missing: <X.X>%
   MCAR columns: <col1>, <col2>, <col3>
   MAR columns: <col1>, <col2>
   ```
   Note: "Overall missing" = total missing cells / total cells × 100.
   MCAR = missing completely at random (no relationship to other variables).
   MAR = missing at random (missingness related to observed variables).
   To classify: for each column with >5% missing, test whether missingness is associated with other variables (e.g., chi-square or t-test between missing/not-missing groups). If no significant association found, classify as MCAR; otherwise MAR.
3. **Output files:** None required beyond solution.py and summary.md
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Missing data percentages per column
   - Evidence for MCAR vs. MAR classification (statistical tests)
   - Recommendations for missing data handling

## Constraints

- Use Python 3 (standard library preferred; pandas/scipy acceptable)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify output
