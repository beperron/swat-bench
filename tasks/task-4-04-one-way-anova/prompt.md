A social service agency operates four different service delivery models and wants to compare client satisfaction scores across them to determine whether the delivery model affects client satisfaction.

# Task: Multi-Program Comparison Using One-Way ANOVA

Analyze a dataset of client satisfaction scores across four service delivery models (In-Person, Telehealth, Hybrid, Group) using a one-way analysis of variance (ANOVA) to determine whether there are statistically significant differences between groups.

## Input Files

- `service_satisfaction.csv` — Client records with service model, satisfaction scores, and demographic information

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total participants: <N>
   Number of groups: 4

   Group means:
   In-Person: <X.XX> (n=<N>)
   Telehealth: <X.XX> (n=<N>)
   Hybrid: <X.XX> (n=<N>)
   Group: <X.XX> (n=<N>)

   Grand mean: <X.XX>
   F-statistic: <X.XX>
   Degrees of freedom (between): <N>
   Degrees of freedom (within): <N>
   p-value: <X.XXXX>
   Significant (p < 0.05): <Yes/No>
   Eta-squared: <X.XXX>
   Highest scoring model: <name>
   Lowest scoring model: <name>
   ```
3. **Output files:** None
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Your approach and methodology
   - Key findings and practical interpretation
   - A verification section with intermediate values or sample outputs that allows a human reviewer to confirm correctness

## Constraints

- Use only the Python standard library (no pandas, scipy, numpy, etc.)
- Implement one-way ANOVA from scratch:
  - SS_between = sum(n_j * (mean_j - grand_mean)^2) for each group j
  - SS_within = sum of (x_ij - mean_j)^2 for all observations
  - MS_between = SS_between / df_between, where df_between = k - 1
  - MS_within = SS_within / df_within, where df_within = N - k
  - F = MS_between / MS_within
- Compute eta-squared = SS_between / SS_total, where SS_total = SS_between + SS_within
- Approximate the p-value from the F-distribution (you may use a numerical approximation)
- Compute standard deviations using sample standard deviation (ddof=1)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify it executes and produces the expected stdout format

## Evaluation Criteria

- Correct computation of group means and sample sizes
- Correct ANOVA sum of squares decomposition
- Correct F-statistic and degrees of freedom
- Reasonable p-value approximation for the F-distribution
- Accurate eta-squared calculation
- Correct identification of highest and lowest scoring models
- Clear, well-structured summary that enables human verification of results
