A foster care agency is preparing case records for a longitudinal study. The records contain dates in inconsistent formats, impossible dates, and logical violations that must be identified and cleaned.

# Task: Date and Timeline Cleaning

You are given a CSV file containing foster care case records. The date fields contain multiple quality issues: inconsistent formats (some rows use MM/DD/YYYY, some use "Month Day, Year", some use DD-MM-YYYY instead of the standard YYYY-MM-DD), impossible dates (e.g., month 13, February 30), logical violations (exit date before entry date), and age-entry mismatches (where age_at_entry does not match the difference between DOB and entry_date). Your task is to identify, count, and flag all date-related issues.

## Input Files

- `foster_care_records.csv` — 100 records with columns: case_id, child_name, dob, age_at_entry, entry_date, exit_date, placement_type, caseworker, review_date, permanency_goal, status

### Date Issues to Detect

1. **Format inconsistencies** — Rows where date fields are not in YYYY-MM-DD format (e.g., MM/DD/YYYY, "Month Day, Year", DD-MM-YYYY). Count each ROW with format issues as one inconsistency, not each field.

2. **Impossible dates** — Date strings that cannot represent a valid calendar date (e.g., "2024-13-45", "2024-02-30", month=0). Count each ROW with an impossible date as one issue.

3. **Sequence violations** — Rows where exit_date is before entry_date (a logical impossibility). Only check rows where both dates are parseable.

4. **Age-entry mismatches** — Rows where age_at_entry differs from the computed age (years between DOB and entry_date) by more than 1 year. Only check rows where both DOB and entry_date are parseable valid dates.

## Required Output

1. **Script**: Save your solution as `solution.py`

2. **Stdout**: Print the following to stdout with these EXACT labels:
```
Total records: <N>
Total date fields checked: <N>

Format inconsistencies: <N>
Impossible dates: <N>
Sequence violations (exit before entry): <N>
Age-entry mismatches: <N>
Total date issues: <N>

Records with no date issues: <N>
Records with 1+ date issues: <N>

Dates standardized to YYYY-MM-DD: <N>
```

Note: "Total date fields checked" counts the number of non-empty date fields across all records (dob, entry_date, exit_date, review_date). "Dates standardized to YYYY-MM-DD" counts the number of individual date fields (not rows) that were in a non-standard but parseable format and converted to YYYY-MM-DD.

3. **Output file**: Save the cleaned records as `cleaned_records.csv` with all parseable dates converted to YYYY-MM-DD format and a new column `date_issues` listing any issues found for that row (or empty if clean).

4. **Summary**: Write a brief summary of findings as `summary.md`

## Constraints

- Python standard library only (no pandas, numpy, scipy, sklearn, or other external packages)
- Use only the `csv`, `datetime`, `re`, `os`, and `sys` modules as needed
- Your script must be runnable with `python3 solution.py` from the test directory

## Evaluation Criteria

- Correct identification of all date format inconsistencies
- Correct detection of impossible/invalid dates
- Correct detection of logical sequence violations
- Correct detection of age-entry mismatches
- Accurate total counts of all issue types
- Production of a cleaned output CSV with standardized dates
