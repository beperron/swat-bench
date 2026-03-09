# Fisher's Exact Test

## Context
You are a data analyst for a child welfare agency that wants to test whether the type of maltreatment (Physical Abuse vs Neglect) is associated with case outcome (Reunification vs Foster Care). Some cell counts in the contingency table are small, making Fisher's exact test more appropriate than the chi-square test.

## Input
- `maltreatment_outcomes.csv`: Contains data on 50 cases with the following columns:
  - `case_id`: Case identifier
  - `maltreatment_type`: "Physical Abuse" or "Neglect"
  - `child_age`: Age of the child
  - `case_outcome`: "Reunification" or "Foster Care"
  - `time_to_decision_days`: Days until case decision
  - `prior_cps_contact`: Prior CPS contact (0/1)

## Task
Using **only the Python standard library** (no numpy, pandas, scipy, or other external packages), write a Python script called `solution.py` that:

1. Reads `maltreatment_outcomes.csv`
2. Builds the 2x2 contingency table
3. Computes reunification rates by maltreatment type
4. Performs Fisher's exact test
5. Computes the odds ratio and relative risk
6. Writes a brief `summary.md` file summarizing findings

## Required Output (stdout)
Print the following to stdout with **exactly** these labels:

```
Total cases: <N>

Contingency table:
  Physical Abuse + Reunification: <N>
  Physical Abuse + Foster Care: <N>
  Neglect + Reunification: <N>
  Neglect + Foster Care: <N>

Reunification rate (Physical): <X.X>%
Reunification rate (Neglect): <X.X>%
Odds ratio: <X.XX>
Fisher's exact p-value: <X.XXXX>
Significant (p < 0.05): <Yes/No>
Relative risk: <X.XX>
```

## Notes
- Fisher's exact test computes the exact probability of observing the given table (and more extreme) under the null hypothesis of independence
- For a 2x2 table [[a,b],[c,d]] with n=a+b+c+d:
  - P = C(a+b,a) * C(c+d,c) / C(n,a+c) where C is the binomial coefficient
  - Sum probabilities of all tables as or more extreme than the observed table
- Two-sided test: sum probabilities of all tables whose probability <= the observed table's probability
- Odds ratio = (a*d) / (b*c)
- Relative risk of reunification = P(reunify|neglect) / P(reunify|physical)
- Use math.comb for binomial coefficients (Python 3.8+) and the math module for calculations
