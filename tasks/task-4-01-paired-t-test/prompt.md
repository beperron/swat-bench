A community mental health center wants to evaluate whether their 12-week cognitive-behavioral therapy (CBT) program reduces depression symptoms, measured by PHQ-9 scores at intake and discharge.

# Task: Pre-Post Program Evaluation Using a Paired t-Test

Analyze a dataset of CBT program outcomes to determine whether there is a statistically significant reduction in PHQ-9 depression scores from pre-treatment to post-treatment using a paired-samples t-test.

## Input Files

- `cbt_outcomes.csv` — Client records with pre- and post-treatment PHQ-9 depression scores, along with demographic and program participation information

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Participants: <N>
   Pre-treatment mean: <X.XX>
   Pre-treatment std: <X.XX>
   Post-treatment mean: <X.XX>
   Post-treatment std: <X.XX>
   Mean difference (pre - post): <X.XX>
   Std of differences: <X.XX>
   t-statistic: <X.XX>
   Degrees of freedom: <N>
   p-value: <X.XXXX>
   Significant (p < 0.05): <Yes/No>
   Cohen's d: <X.XX>
   Effect interpretation: <Negligible/Small/Medium/Large>
   ```
3. **Output files:** None
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Your approach and methodology
   - Key findings and clinical interpretation
   - A verification section with intermediate values or sample outputs that allows a human reviewer to confirm correctness

## Constraints

- Use only the Python standard library (no pandas, scipy, numpy, etc.)
- Implement the paired t-test from scratch using the formula: t = (mean_diff) / (std_diff / sqrt(n))
- Compute the standard deviation of differences using the sample standard deviation (ddof=1)
- Compute Cohen's d for paired samples as: d = mean_diff / std_diff
- Interpret effect size: |d| < 0.2 = Negligible, 0.2-0.5 = Small, 0.5-0.8 = Medium, >= 0.8 = Large
- Approximate the two-tailed p-value from the t-distribution (you may use a numerical approximation)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify it executes and produces the expected stdout format

## Evaluation Criteria

- Correct computation of pre- and post-treatment descriptive statistics
- Correct paired t-test statistic and degrees of freedom
- Reasonable p-value approximation for the t-distribution
- Accurate Cohen's d calculation and effect size interpretation
- Clear, well-structured summary that enables human verification of results
