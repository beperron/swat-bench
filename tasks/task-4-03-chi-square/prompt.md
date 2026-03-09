An MSW program director wants to know whether program track (clinical vs. community) is associated with different licensing exam pass rates.

# Task: Chi-Square Test of Independence

Analyze a dataset of MSW program outcomes to determine whether program track is associated with licensing exam pass rates using a chi-square test of independence. Compute the effect size using Cramer's V.

## Input Files

- `program_outcomes.csv` — Student records with program track, exam results, GPA, and other variables

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total students: <N>
   Programs: <list>
   ```
   Then the contingency table:
   ```
   Contingency table:
   <TRACK>: Pass=<N>, Fail=<N>
   ...
   ```
   Then chi-square results:
   ```
   Chi-square statistic: <X.XXXX>
   Degrees of freedom: <N>
   p-value: <X.XXXX>
   Significant (p<0.05): <Yes/No>
   Cramers V: <X.XXXX>
   ```
3. **Output files:** None
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Your approach and methodology
   - Key findings and results
   - A verification section with intermediate values or sample outputs that allows a human reviewer to confirm correctness

## Constraints

- Use only the Python standard library (no pandas, scipy, numpy, etc.)
- Implement the chi-square statistic calculation from the formula
- Compute Cramer's V as the effect size measure
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify it executes and produces the expected stdout format

## Evaluation Criteria

- Correct construction of the contingency table
- Correct chi-square statistic and degrees of freedom
- Reasonable p-value approximation
- Accurate Cramer's V calculation
- Clear, well-structured summary that enables human verification of results
