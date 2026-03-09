A field placement coordinator wants to understand which student characteristics are most strongly associated with field placement evaluation scores.

# Task: Compute Pearson Correlation Matrix

Analyze a dataset of MSW student field placement outcomes. Compute the full pairwise Pearson correlation matrix for all numeric variables and identify the strongest associations.

## Input Files

- `field_placement_outcomes.csv` — Student records with GPA, practice hours, supervision hours, prior experience, self-efficacy scores, and evaluation scores

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total students: <N>
   Variables: <comma-separated list>
   ```
   Then print descriptive statistics:
   ```
   Descriptive statistics: mean, median, std for each variable
   <VARIABLE>: mean=<X.XX>, median=<X.XX>, std=<X.XX>, min=<X.XX>, max=<X.XX>
   ...
   ```
   Then print the correlation matrix:
   ```
   Correlation matrix:
              <VAR1>  <VAR2>  <VAR3>  ...
   <VAR1>     1.00    <X.XX>  <X.XX>  ...
   <VAR2>     <X.XX>  1.00    <X.XX>  ...
   ...
   ```
   Then print the strongest correlations:
   ```
   Strongest correlations:
   <VAR_A> -- <VAR_B>: r=<X.XX>
   ...
   ```
3. **Output files:** None
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Your approach and methodology
   - Key findings and results
   - A verification section with intermediate values or sample outputs that allows a human reviewer to confirm correctness

## Constraints

- Use only the Python standard library (no pandas, scipy, numpy, sklearn, etc.)
- Implement Pearson correlation from the formula
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify it executes and produces the expected stdout format

## Evaluation Criteria

- Correct computation of all pairwise Pearson correlations
- Properly formatted correlation matrix
- Correct identification of strongest correlations
- Accurate descriptive statistics for all variables
- Clear, well-structured summary that enables human verification of results
