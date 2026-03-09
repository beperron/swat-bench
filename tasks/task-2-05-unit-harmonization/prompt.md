A benefits eligibility study collected income data from 3 agencies where each agency reported income in different time periods that must all be converted to annual income for eligibility analysis.

# Task: Unit Harmonization

## Input Files

- `income_data.csv` — 90 client income records with columns: client_id, agency, income_amount, income_period, hours_per_week, household_size, benefits_received
  - income_period is one of: Hourly, Weekly, Biweekly, Monthly, Annual
  - income_amount is the dollar amount for the given period
  - hours_per_week is the number of hours worked per week

## Conversion Rules

Convert all income amounts to annual income using these formulas:
- **Hourly** to Annual: `income_amount * hours_per_week * 52`
- **Weekly** to Annual: `income_amount * 52`
- **Biweekly** to Annual: `income_amount * 26`
- **Monthly** to Annual: `income_amount * 12`
- **Annual**: use as-is (no conversion needed)

## Poverty Line Calculation

The federal poverty line threshold is:
- $15,060 for a household of size 1
- Add $5,380 for each additional person
- Formula: `poverty_line = 15060 + 5380 * (household_size - 1)`

A client is "below poverty line" if their annual income (after conversion) is strictly less than their household's poverty line threshold.

## Required Output

1. **Script:** `solution.py` — Python script that reads the CSV, converts all incomes to annual, calculates poverty statistics, and produces output.

2. **Stdout:** Print the following lines exactly:
```
Total records: <N>
Records by period:
  Hourly: <N>
  Weekly: <N>
  Biweekly: <N>
  Monthly: <N>
  Annual: <N>

After conversion to annual:
Mean annual income: <X.XX>
Median annual income: <X.XX>
Min annual income: <X.XX>
Max annual income: <X.XX>

Below poverty line (annual < 15060 for size 1, +5380 per additional person): <N>
Poverty rate: <X.X>%
```

Notes:
- All income statistics (mean, median, min, max) should be formatted to exactly 2 decimal places.
- Poverty rate should be formatted to exactly 1 decimal place with a % sign.
- Records by period should be listed in the exact order shown above.
- Median: for an even number of records, use the average of the two middle values when sorted.

3. **Output file:** `harmonized.csv` — the original data with an additional column `annual_income` containing the converted annual income for each record.

4. **Summary:** `summary.md` — brief description of the conversion process and poverty analysis.

## Constraints

- Python standard library ONLY (no pandas, numpy, scipy, sklearn).
- The script must be named `solution.py` and run with `python3 solution.py`.

## Evaluation Criteria

- Correct record counts by period
- Accurate income conversion and statistics
- Correct poverty line calculation and count
- Output files exist (harmonized.csv, summary.md)
