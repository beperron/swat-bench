A state child welfare agency is conducting a mandatory racial equity audit, comparing referral and substantiation rates across racial/ethnic groups relative to the general child population.

# Task: Racial Disproportionality Analysis

## Input Files

1. `cw_referrals.csv` (~500 rows) -- individual child welfare referral records
   - Columns: case_id, child_race, child_age, referral_type, screened_in (0/1), investigated (0/1), substantiated (0/1), placement (0/1), county

2. `county_population.csv` (~5 rows, one per race group)
   - Columns: race_group, child_population (count of children in county by race)

Race groups: White, Black, Hispanic, Asian, Other

## Required Output

1. **Script**: `solution.py`
2. **Stdout** must print the following exact format:

```
Total referrals: <N>
Total child population: <N>

Referral rates per 1000 children:
White referral rate per 1000: <X.X>
Black referral rate per 1000: <X.X>
Hispanic referral rate per 1000: <X.X>
Asian referral rate per 1000: <X.X>
Other referral rate per 1000: <X.X>

Disproportionality Index (referrals vs population):
White disproportionality index: <X.XX>
Black disproportionality index: <X.XX>
Hispanic disproportionality index: <X.XX>
Asian disproportionality index: <X.XX>
Other disproportionality index: <X.XX>

Substantiation rates by race:
White substantiation rate: <X.X>%
Black substantiation rate: <X.X>%
Hispanic substantiation rate: <X.X>%
Asian substantiation rate: <X.X>%
Other substantiation rate: <X.X>%

Relative Risk Ratio (Black vs White referral rate): <X.XX>
Relative Risk Ratio (Black vs White substantiation rate): <X.XX>
Most overrepresented group: <race>
```

3. **Output files**: `disproportionality_report.csv` -- a table with columns: race_group, referral_count, population, referral_rate_per_1000, disproportionality_index, substantiation_rate
4. **Summary**: `summary.md` -- narrative interpretation of findings, equity implications, and recommended actions.

## Formulas

- **Referral rate per 1000**: (number of referrals for race / population for race) * 1000
- **Disproportionality Index**: (% of referrals for race) / (% of population for race). DI > 1 means overrepresented.
- **Substantiation rate**: (substantiated count / investigated count) * 100 for each race group (only among investigated cases)
- **Relative Risk Ratio**: rate_Black / rate_White (computed separately for referral rates and substantiation rates)
- **Most overrepresented group**: the race with the highest Disproportionality Index

## Constraints

- Python standard library ONLY (no numpy, pandas, scipy, etc.)
- Read inputs from `cw_referrals.csv` and `county_population.csv`
- Run `python3 solution.py` from the test directory to verify output
- IMPORTANT: Each output label must be unique. Use the prefixed format shown above (e.g., "Black referral rate per 1000:", "Black disproportionality index:", "Black substantiation rate:") to avoid ambiguity.

## Evaluation Criteria

- Correct referral rate computation per 1000 children
- Correct disproportionality index for each group
- Correct substantiation rates (substantiated / investigated)
- Correct relative risk ratios
- Identification of most overrepresented group
- disproportionality_report.csv and summary.md files created
