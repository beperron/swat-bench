A systematic review team is computing effect sizes from published studies on parenting interventions for child welfare-involved families.

# Task: Effect Size Computation for Meta-Analysis

## Input Files

- `study_summaries.csv` (~12 rows) -- each row is a published study providing summary statistics
  - Columns: study_id, authors, year, intervention_type, n_treatment, mean_treatment, sd_treatment, n_control, mean_control, sd_control, outcome_measure

## Required Output

1. **Script**: `solution.py`
2. **Stdout** must print the following exact format:

```
Total studies: <N>

Study-level effect sizes:
Study 1: Cohen's d = <X.XXX>, Hedges' g = <X.XXX>, 95% CI = [<X.XXX>, <X.XXX>]
Study 2: Cohen's d = <X.XXX>, Hedges' g = <X.XXX>, 95% CI = [<X.XXX>, <X.XXX>]
... (all studies)

Summary:
Mean Cohen's d: <X.XXX>
Mean Hedges' g: <X.XXX>
Median effect size (d): <X.XXX>
Range: [<X.XXX>, <X.XXX>]
Studies with large effect (d > 0.8): <N>
Studies with medium effect (0.5 <= d <= 0.8): <N>
Studies with small effect (d < 0.5): <N>
Pooled Hedges' g (inverse variance): <X.XXX>
```

3. **Output files**: None required beyond solution.py
4. **Summary**: `summary.md` -- a brief narrative summarizing the meta-analytic findings, including which intervention types showed the strongest effects and clinical implications.

## Formulas

Use these exact formulas:

- **Pooled SD**: pooled_sd = sqrt(((n1-1)*sd1^2 + (n2-1)*sd2^2) / (n1+n2-2))
- **Cohen's d**: d = (mean_treatment - mean_control) / pooled_sd
- **Hedges' g**: g = d * (1 - 3/(4*(n1+n2)-9))
- **95% CI for d**: d +/- 1.96 * sqrt((n1+n2)/(n1*n2) + d^2/(2*(n1+n2)))
- **Pooled Hedges' g** (inverse variance weighted): sum(wi*gi) / sum(wi), where wi = 1/variance_i and variance_i = (n1+n2)/(n1*n2) + g^2/(2*(n1+n2))

## Constraints

- Python standard library ONLY (no numpy, pandas, scipy, etc.)
- Read input from `study_summaries.csv`
- Run `python3 solution.py` from the test directory to verify output
- All numeric values to 3 decimal places where shown as X.XXX

## Evaluation Criteria

- Correct computation of Cohen's d and Hedges' g for each study
- Correct 95% confidence intervals
- Accurate summary statistics (mean, median, range, effect size categories)
- Correct inverse-variance pooled Hedges' g
- summary.md file created with narrative interpretation
