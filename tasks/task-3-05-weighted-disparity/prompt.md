A health equity researcher is analyzing survey data on healthcare access disparities. The survey oversampled some racial groups, so sampling weights must be applied to produce population-representative estimates.

# Task: Weighted Disparity Analysis

Compute both unweighted and weighted mean health access scores by racial group, then calculate the disparity ratio between the highest and lowest scoring groups.

## Input Files

- `health_survey.csv` — 2,000 survey respondents with columns: respondent_id, race, age, income, health_access_score (0-100), mental_health_score (0-50).
- `weights.csv` — Sampling weights by race (columns: race, sampling_weight). Multiply each respondent's contribution by their race's weight for weighted estimates.

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total respondents: <N>
   Overall unweighted mean: <X.XX>
   Overall weighted mean: <X.XX>
   White mean (health access): <X.XX>
   Lowest group: <RACE> (<X.XX>)
   Disparity ratio: <X.XX>
   Unique races: <N>
   ```
   Note: "Disparity ratio" = White mean / lowest mean among Black, Hispanic, Asian, and Other groups for health_access_score.
   Weighted mean = sum(score × weight) / sum(weight) across all respondents.
3. **Output files:**
   - `disparity_results.csv` — One row per race with columns: race, n, unweighted_mean, weighted_mean, sampling_weight
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Comparison of weighted vs. unweighted estimates
   - Discussion of how sampling weights affect disparity estimates
   - Verification section with intermediate calculations

## Constraints

- Use Python 3 (standard library preferred; pandas acceptable)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify output
