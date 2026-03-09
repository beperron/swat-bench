A policy researcher is evaluating the impact of a caseload cap policy on monthly social work caseloads. The policy was implemented at month 31, creating a natural pre/post comparison over 60 months of data. They want to use an interrupted time series (ITS) design to estimate the immediate level change and any change in trend slope after the intervention.

# Task: Interrupted Time Series Analysis of Caseload Cap Policy

Fit a segmented regression model to estimate the level change and slope change caused by the intervention.

## Input Files

- `monthly_caseload.csv` — 60 monthly observations with columns: month (1-60), date (YYYY-MM), caseload (count), period (pre/post).
  - The intervention occurs between month 30 and month 31.

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total months: <N>
   Pre-period mean: <X.XX>
   Post-period mean: <X.XX>
   Level change (beta2): <X.XX>
   Slope change (beta3): <X.XX>
   Pre slope (beta1): <X.XX>
   Level change significant (p<0.05): Yes/No
   ```
   Notes:
   - The segmented regression model is: caseload = beta0 + beta1*time + beta2*intervention + beta3*time_since_intervention + error
   - `time` = month number (1-60)
   - `intervention` = 0 for months 1-30, 1 for months 31-60
   - `time_since_intervention` = 0 for months 1-30; for months 31-60, it equals months since intervention (1, 2, ..., 30)
   - "Level change (beta2)" is the immediate shift in caseload at the intervention point.
   - "Slope change (beta3)" is the change in monthly trend after vs. before intervention.
   - "Pre slope (beta1)" is the monthly trend before the intervention.
3. **Output files:** None
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Interpretation of the level change and slope change
   - Whether the policy achieved its intended effect
   - Pre-intervention vs. post-intervention trends
   - Statistical significance of findings

## Constraints

- Use Python 3 (standard library preferred; pandas, numpy, scipy, statsmodels acceptable)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify output
