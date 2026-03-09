A program evaluator is examining which client characteristics are associated with program completion in a community-based diversion program. The goal is to understand the strength and direction of associations using logistic regression, so the agency can better understand patterns in their data and inform program design.

# Task: Logistic Regression — Associations with Program Completion

Fit a logistic regression model with `completed` (0/1) as the outcome variable and numeric client characteristics as independent variables. Report model fit statistics and compute odds ratios to describe the strength of association for each variable.

## Input Files

- `program_completion.csv` — 1,000 clients with columns: client_id, age, prior_arrests (0-10), employment (0/1), mental_health_score (0-50), risk_level (low/medium/high), completed (0/1 outcome).

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total clients: <N>
   Completion rate: <X.X>%
   Accuracy: <X.X>%
   Pseudo R-squared: <X.XXXX>
   employment odds ratio: <X.XX>
   prior_arrests odds ratio: <X.XX>
   Estimated probability (age=30, prior_arrests=2, employment=1, mental_health=25): <X.XX>
   ```
   Notes:
   - Use numeric variables only (age, prior_arrests, employment, mental_health_score). Exclude risk_level from the model.
   - "Pseudo R-squared" = McFadden's pseudo R-squared: 1 - (log-likelihood / null log-likelihood).
   - "Accuracy" = percentage of correctly classified cases using 0.5 probability threshold.
   - Odds ratio = exp(coefficient).
   - For the estimated probability, use these variable values: age=30, prior_arrests=2, employment=1, mental_health_score=25.
3. **Output files:**
   - `logistic_results.csv` — One row per variable with columns: predictor, coefficient, odds_ratio, p_value
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Interpretation of odds ratios for each variable
   - Discussion of model fit (pseudo R-squared, classification accuracy)
   - Discussion of which client characteristics show the strongest associations with completion

## Constraints

- Use Python 3 (standard library preferred; pandas, numpy, scipy, statsmodels, or sklearn acceptable)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify output
