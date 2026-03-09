# Wilcoxon Signed-Rank Test

## Context
You are a data analyst for a domestic violence shelter that runs a 6-week empowerment group program. The shelter wants to test whether participants' self-efficacy scores significantly changed from pre- to post-program. The scores are ordinal and non-normally distributed, making the Wilcoxon signed-rank test appropriate for this paired comparison.

## Input
- `empowerment_program.csv`: Contains data on 35 participants with the following columns:
  - `participant_id`: Participant identifier
  - `age`: Participant age
  - `pre_self_efficacy`: Self-efficacy score before program (1-40 scale)
  - `post_self_efficacy`: Self-efficacy score after program (1-40 scale)
  - `sessions_attended`: Number of sessions attended
  - `group_cohort`: Which cohort the participant belonged to

## Task
Using **only the Python standard library** (no numpy, pandas, scipy, or other external packages), write a Python script called `solution.py` that:

1. Reads `empowerment_program.csv`
2. Computes pre and post median self-efficacy scores
3. Computes the difference for each participant
4. Performs a Wilcoxon signed-rank test
5. Computes the effect size r = Z / sqrt(N)
6. Counts how many improved, declined, or stayed unchanged
7. Writes a brief `summary.md` file summarizing findings

## Required Output (stdout)
Print the following to stdout with **exactly** these labels:

```
Participants: <N>
Pre median: <X.X>
Post median: <X.X>
Median difference: <X.X>

Wilcoxon T statistic: <X.X>
p-value: <X.XXXX>
Significant (p < 0.05): <Yes/No>
Effect size (r): <X.XXX>
Participants improved: <N>
Participants declined: <N>
Participants unchanged: <N>
```

## Notes
- The Wilcoxon signed-rank test:
  1. Compute differences (post - pre)
  2. Remove zero differences
  3. Rank the absolute differences (use average ranks for ties)
  4. T = minimum of W+ (sum of positive ranks) and W- (sum of negative ranks)
  5. For the normal approximation: z = (T - n'(n'+1)/4) / sqrt(n'(n'+1)(2n'+1)/24), where n' is the number of non-zero differences
- Effect size r = |Z| / sqrt(N) where N is the total number of participants with non-zero differences
- Use the math module for calculations
