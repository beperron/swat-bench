A clinical supervisor is evaluating inter-rater consistency among 4 raters who scored 50 clinical vignettes on a 1-10 clinical severity scale. You need to compute the Intraclass Correlation Coefficient (ICC) to assess agreement.

# Task: Intraclass Correlation Coefficient (ICC) Analysis

Compute ICC(2,1) — two-way random effects, single measures — to evaluate the consistency of ratings across all raters and vignettes.

## Input Files

- `rater_scores.csv` — 50 rows (one per vignette) with columns: vignette_id, rater_1, rater_2, rater_3, rater_4. Scores are on a 1-10 scale with 1 decimal place.

## Required Analysis

1. Compute a two-way ANOVA decomposition:
   - MS_between_subjects (between vignettes)
   - MS_between_raters (between raters)
   - MS_residual (error)
2. Calculate ICC(2,1) using the formula:
   - ICC(2,1) = (MS_subjects - MS_residual) / (MS_subjects + (k-1)*MS_residual + k*(MS_raters - MS_residual)/n)
   - Where k = number of raters, n = number of subjects
3. Compute the F ratio: MS_subjects / MS_residual
4. Compute 95% confidence interval for the ICC
5. Interpret the ICC: >0.75 excellent, 0.60-0.75 good, 0.40-0.60 moderate, <0.40 poor

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total vignettes: <N>
   Number of raters: <N>
   ICC value: <X.XXXX>
   F ratio: <X.XX>
   95% CI lower: <X.XX>
   95% CI upper: <X.XX>
   Interpretation: <excellent/good/moderate/poor>
   Mean score across all: <X.XX>
   ```
3. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Explanation of the ICC model used (two-way random, single measures)
   - ANOVA decomposition table (SS, df, MS for each source)
   - Interpretation of results in clinical supervision context
   - Discussion of rater agreement quality

## Constraints

- Use Python 3 (standard library preferred; pingouin or scipy acceptable)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify output
