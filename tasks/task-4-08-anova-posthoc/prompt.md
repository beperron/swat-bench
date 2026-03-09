A substance use researcher is comparing recovery outcomes across four treatment modalities: Cognitive Behavioral Therapy (CBT), Motivational Interviewing (MI), Twelve-Step facilitation, and Treatment as Usual (TAU). They need to determine whether recovery scores differ significantly across groups and which specific group pairs differ.

# Task: One-Way ANOVA with Post-Hoc Pairwise Comparisons

Perform a one-way ANOVA on recovery scores by treatment group, followed by post-hoc pairwise comparisons to identify which groups differ significantly.

## Input Files

- `su_outcomes.csv` — 300 clients (75 per group) with columns: client_id, treatment_group (CBT/MI/Twelve_Step/TAU), recovery_score (0-100), sessions, age.

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total clients: <N>
   Number of groups: <N>
   CBT mean: <X.XX>
   MI mean: <X.XX>
   Twelve_Step mean: <X.XX>
   TAU mean: <X.XX>
   F statistic: <X.XX>
   P value: <X.XXXX>
   Significant (p<0.05): Yes/No
   Eta squared: <X.XXXX>
   Significant pairs: <N>
   ```
   Notes:
   - "Eta squared" = SS_between / SS_total (effect size for ANOVA).
   - "Significant pairs" = the number of pairwise comparisons that are statistically significant at p < 0.05 after correction for multiple comparisons (e.g., Bonferroni or Tukey HSD).
   - Group means are arithmetic means of recovery_score within each treatment_group.
3. **Output files:**
   - `posthoc_results.csv` — One row per pair with columns: group1, group2, mean_diff, p_value, significant
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - ANOVA results interpretation
   - Which treatment groups differ significantly from each other
   - Effect size interpretation (eta squared)
   - Practical implications for treatment selection

## Constraints

- Use Python 3 (standard library preferred; pandas, numpy, scipy, statsmodels acceptable)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify output
