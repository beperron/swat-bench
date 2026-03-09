A multi-site substance abuse treatment study collected data from 3 sites that each used different coding schemes. The data must be harmonized before pooled analysis can be performed.

# Task: Variable Recoding and Standardization

You are given a CSV file containing substance abuse treatment data from three sites (Site A, Site B, Site C), each with 30 participants. Each site used different coding conventions for categorical variables (gender, race/ethnicity, treatment completion) and different scales for satisfaction scores. Your task is to identify the coding inconsistencies, standardize all variables to a common scheme, and produce a cleaned dataset.

## Input Files

- `multisite_data.csv` — 90 records with columns: record_id, site, participant_id, age, gender, race_ethnicity, education, employment, substance_primary, treatment_type, satisfaction_score, days_in_treatment, completed_treatment

### Coding Differences to Discover and Harmonize

**Gender** — Sites use different representations (e.g., "Male" vs "M" vs "male"). Standardize to: Male, Female, Non-binary.

**Race/Ethnicity** — Sites use different labels for the same categories (e.g., "Black" vs "African American" vs "black/african american"). Standardize to 5 categories: White, Black, Hispanic, Asian, Other.

**Treatment Completion** — Sites use different representations (e.g., "Yes"/"No" vs 1/0 vs "TRUE"/"FALSE"). Standardize to numeric: 1 (completed), 0 (not completed).

**Satisfaction Score** — Sites use different scales:
- Site A: 1-5 scale (already standard)
- Site B: 0-4 scale (add 1 to convert to 1-5)
- Site C: 0-10 scale (rescale to 1-5 using formula: 1 + (score/10) * 4)

## Required Output

1. **Script**: Save your solution as `solution.py`

2. **Stdout**: Print the following to stdout with these EXACT labels:
```
Total records: <N>
Sites: <N>

Raw unique gender values: <N>
Raw unique race values: <N>
Raw unique completion values: <N>

Standardized unique gender values: <N>
Standardized unique race values: <N>
Standardized unique completion values: <N>

Gender distribution:
  Male: <N>
  Female: <N>
  Non-binary: <N>

Race distribution:
  White: <N>
  Black: <N>
  Hispanic: <N>
  Asian: <N>
  Other: <N>

Completion rate: <X.X>%
Mean satisfaction (standardized 1-5): <X.XX>
```

3. **Output file**: Save the standardized dataset as `standardized.csv` with the same columns but all values recoded to the standard scheme.

4. **Summary**: Write a brief summary of findings and transformations applied as `summary.md`

## Constraints

- Python standard library only (no pandas, numpy, scipy, sklearn, or other external packages)
- Use only the `csv`, `collections`, `math`, `os`, and `sys` modules as needed
- Your script must be runnable with `python3 solution.py` from the test directory

## Evaluation Criteria

- Correct identification of coding inconsistencies across sites
- Accurate standardization of all categorical variables
- Correct rescaling of satisfaction scores to a common 1-5 scale
- Accurate computation of summary statistics after standardization
- Production of a clean, standardized output CSV
