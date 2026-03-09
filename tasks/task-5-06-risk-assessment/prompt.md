A child protective services agency wants to validate their structured decision-making (SDM) risk assessment tool against actual case outcomes over a 2-year period.

# Task: Risk Assessment Instrument Validation

## Input Files

- `risk_assessment_outcomes.csv` (~200 rows)
  - Columns: case_id, risk_score (0-20 integer), risk_category (Low/Moderate/High/Very High), child_age, num_prior_referrals, substantiated_within_2yr (0/1), new_maltreatment_within_2yr (0/1)

The risk_score is the instrument output. substantiated_within_2yr is the actual outcome (truth label).

## Required Output

1. **Script**: `solution.py`
2. **Stdout** must print the following exact format:

```
Total cases: <N>
Positive outcome (substantiated): <N>
Negative outcome: <N>
Base rate: <X.X>%

At cutoff score >= 10:
True positives: <N>
False positives: <N>
True negatives: <N>
False negatives: <N>
Sensitivity (recall): <X.XXX>
Specificity: <X.XXX>
Positive predictive value: <X.XXX>
Negative predictive value: <X.XXX>
Accuracy: <X.XXX>
F1 score: <X.XXX>

AUC (trapezoidal): <X.XXX>
Optimal cutoff (Youden's J): <N>
```

3. **Output files**: None required beyond solution.py
4. **Summary**: `summary.md` -- narrative interpretation of the risk assessment tool's validity, including clinical implications of the sensitivity/specificity trade-off and recommendations for cutoff adjustment.

## Formulas

Use a cutoff of score >= 10 for "positive screen":
- **True Positive (TP)**: score >= 10 AND substantiated_within_2yr == 1
- **False Positive (FP)**: score >= 10 AND substantiated_within_2yr == 0
- **True Negative (TN)**: score < 10 AND substantiated_within_2yr == 0
- **False Negative (FN)**: score < 10 AND substantiated_within_2yr == 1
- **Sensitivity (recall)**: TP / (TP + FN)
- **Specificity**: TN / (TN + FP)
- **Positive Predictive Value (PPV)**: TP / (TP + FP)
- **Negative Predictive Value (NPV)**: TN / (TN + FN)
- **Accuracy**: (TP + TN) / Total
- **F1 score**: 2*TP / (2*TP + FP + FN)

For **AUC (trapezoidal)**:
- Compute TPR and FPR at every unique risk_score threshold (plus one above the max and one below the min)
- Sort by FPR ascending
- Use trapezoidal rule to compute area under the ROC curve

For **Optimal cutoff (Youden's J)**:
- For each unique risk_score threshold, compute J = sensitivity + specificity - 1
- The optimal cutoff is the score that maximizes J

## Constraints

- Python standard library ONLY (no numpy, pandas, scipy, sklearn, etc.)
- Read input from `risk_assessment_outcomes.csv`
- Run `python3 solution.py` from the test directory to verify output
- All numeric values to 3 decimal places where shown as X.XXX

## Evaluation Criteria

- Correct confusion matrix values at cutoff >= 10
- Correct sensitivity, specificity, PPV, NPV computation
- Correct AUC using trapezoidal method
- Correct Youden's J optimal cutoff
- summary.md file created with clinical interpretation
