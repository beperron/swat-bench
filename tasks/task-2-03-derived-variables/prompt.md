A program evaluation needs several computed variables that do not exist in the raw data -- age groups, risk categories, service intensity levels, and a composite need score -- before analysis can begin.

# Task

Create derived variables from client assessment data using the specified formulas, then report the distributions and summary statistics.

## Input Files

- `client_assessment.csv`: ~100 rows of client assessment data.
  - Columns: `client_id`, `dob`, `assessment_date`, `income`, `household_size`, `mental_health_score` (0-40), `substance_score` (0-20), `housing_stability` (1-5), `employment_status` (0/1), `num_services`, `service_hours`

## Derived Variable Definitions

Create the following variables:

1. **age** = years between `dob` and `assessment_date` (integer, floor -- i.e., if the birthday has not yet occurred in the assessment year, subtract 1).

2. **age_group**: Based on age:
   - "18-25" if 18 <= age <= 25
   - "26-35" if 26 <= age <= 35
   - "36-45" if 36 <= age <= 45
   - "46-55" if 46 <= age <= 55
   - "56+" if age >= 56

3. **poverty_ratio** = `income / (15060 + 5380 * (household_size - 1))`
   - The denominator is the federal poverty level for the given household size.

4. **poverty_level**: Based on poverty_ratio:
   - "Deep poverty" if poverty_ratio < 0.5
   - "Poverty" if 0.5 <= poverty_ratio <= 1.0
   - "Near poverty" if 1.0 < poverty_ratio <= 1.5
   - "Above poverty" if poverty_ratio > 1.5

5. **composite_need** = `(mental_health_score/40)*0.3 + (substance_score/20)*0.3 + ((5-housing_stability)/4)*0.2 + (1-employment_status)*0.2`
   - This is a weighted composite where each component is normalized to 0-1, and higher values indicate greater need.

6. **need_category**: Based on composite_need:
   - "Low" if composite_need < 0.3
   - "Moderate" if 0.3 <= composite_need <= 0.6
   - "High" if composite_need > 0.6

7. **service_intensity** = `service_hours / num_services` if num_services > 0, else 0.

## Required Output

1. **`solution.py`**: Python script that reads the CSV, creates derived variables, and prints the analysis to stdout.

2. **Standard output** must print exactly:
```
Total records: <N>

Age group distribution:
  18-25: <N>
  26-35: <N>
  36-45: <N>
  46-55: <N>
  56+: <N>

Poverty level distribution:
  Poverty level - Deep poverty: <N>
  Poverty level - Poverty: <N>
  Poverty level - Near poverty: <N>
  Poverty level - Above poverty: <N>

Need category distribution:
  Need category - Low: <N>
  Need category - Moderate: <N>
  Need category - High: <N>

Mean composite need score: <X.XXX>
Mean poverty ratio: <X.XXX>
Mean service intensity: <X.XX>
```

Note: The "Poverty level -" and "Need category -" prefixes are required to ensure unique labels.

3. **`enriched.csv`**: The original data with all derived variables added as new columns (age, age_group, poverty_ratio, poverty_level, composite_need, need_category, service_intensity).

4. **`summary.md`**: Brief summary of the derived variable distributions and notable findings.

## Constraints

- Use only Python standard library (no pandas, numpy, or other external packages).

## Evaluation Criteria

- Correct implementation of all derived variable formulas.
- Accurate age calculation (accounting for whether birthday has occurred).
- Proper categorization into groups/levels.
- Correct computation of summary statistics.
