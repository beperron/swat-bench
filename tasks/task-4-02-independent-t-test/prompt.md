A housing authority wants to compare housing stability scores between clients who received intensive case management (ICM) versus treatment-as-usual (TAU) to determine whether ICM leads to better outcomes.

# Task: Quasi-Experimental Group Comparison Using an Independent Samples t-Test

Analyze a dataset of housing stability outcomes to determine whether there is a statistically significant difference in housing stability scores between clients in the ICM and TAU groups, using Welch's t-test (which does not assume equal variances).

## Input Files

- `housing_stability.csv` — Client records with group assignment, housing stability scores, and demographic information

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total participants: <N>
   ICM group: <N>
   TAU group: <N>
   ICM mean: <X.XX>
   ICM std: <X.XX>
   TAU mean: <X.XX>
   TAU std: <X.XX>
   Mean difference (ICM - TAU): <X.XX>
   t-statistic: <X.XX>
   Degrees of freedom: <N>
   p-value: <X.XXXX>
   Significant (p < 0.05): <Yes/No>
   Cohen's d: <X.XX>
   ```
3. **Output files:** None
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Your approach and methodology
   - Key findings and practical interpretation
   - A verification section with intermediate values or sample outputs that allows a human reviewer to confirm correctness

## Constraints

- Use only the Python standard library (no pandas, scipy, numpy, etc.)
- Implement Welch's t-test (do NOT assume equal variances): t = (mean1 - mean2) / sqrt(s1^2/n1 + s2^2/n2)
- Compute Welch-Satterthwaite degrees of freedom: df = (s1^2/n1 + s2^2/n2)^2 / ((s1^2/n1)^2/(n1-1) + (s2^2/n2)^2/(n2-1)), rounded to the nearest integer for display
- Compute standard deviations using sample standard deviation (ddof=1)
- Compute Cohen's d using pooled standard deviation: pooled_sd = sqrt(((n1-1)*s1^2 + (n2-1)*s2^2) / (n1+n2-2))
- Approximate the two-tailed p-value from the t-distribution (you may use a numerical approximation)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify it executes and produces the expected stdout format

## Evaluation Criteria

- Correct computation of group descriptive statistics
- Correct Welch's t-test statistic and degrees of freedom
- Reasonable p-value approximation for the t-distribution
- Accurate Cohen's d calculation
- Clear, well-structured summary that enables human verification of results
