A researcher in child welfare is examining which case-level factors are associated with placement recurrence risk. They have data on 500 child welfare cases and want to run a multiple linear regression to understand the relative strength and direction of association for each factor.

# Task: Multiple Linear Regression — Factors Associated with Placement Recurrence

Fit a multiple linear regression model with `recurrence_risk` as the outcome variable and five case-level factors as independent variables. Report model fit statistics and identify the most statistically significant factor.

## Input Files

- `cw_placements.csv` — 500 cases with columns: case_id, prior_placements (0-5), parental_substance_use (0/1), poverty_index (0-10), child_age (0-17), service_hours (0-100), recurrence_risk (0-100, continuous outcome).

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total cases: <N>
   R-squared: <X.XXXX>
   Adjusted R-squared: <X.XXXX>
   F statistic: <X.XX>
   P value (F): <X.XXXX>
   Most significant factor: <NAME>
   prior_placements coefficient: <X.XX>
   parental_substance_use coefficient: <X.XX>
   poverty_index coefficient: <X.XX>
   ```
   Notes:
   - "Most significant factor" = the independent variable with the largest absolute t-statistic.
   - Report unstandardized (raw) regression coefficients.
   - R-squared, Adjusted R-squared, and F statistic are for the overall model.
3. **Output files:**
   - `regression_results.csv` — One row per variable with columns: predictor, coefficient, std_error, t_statistic, p_value
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Interpretation of the regression coefficients
   - Discussion of model fit (R-squared, F-test)
   - Which factors are statistically significant at p < 0.05

## Constraints

- Use Python 3 (standard library preferred; pandas, numpy, scipy, statsmodels, or sklearn acceptable)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify output
