A PhD student needs help cleaning and validating a messy participant dataset before analysis for their dissertation.

# Task: Audit a Client Database for Data Quality Issues

Scan a social work agency client records file for data quality problems. Identify and categorize all issues found, produce a quality report with counts per issue type, and export a cleaned version of the dataset.

## Input Files

- `client_records.csv` — Agency client database with demographic, case, and contact information

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total records: <N>
   Total issues found: <N>

   Issues by category:
   Duplicate IDs: <N>
   Missing required fields: <N>
   Invalid dates: <N>
   Age-DOB mismatch: <N>
   Invalid zip codes: <N>
   Future dates: <N>
   Negative values: <N>
   Out-of-range values: <N>
   Invalid phone numbers: <N>
   Inconsistent categories: <N>

   Records with no issues: <N>
   Records with 1+ issues: <N>
   ```
3. **Output files:**
   - `quality_report.md` — detailed markdown report listing each issue with the affected row and field
   - `cleaned_records.csv` — the dataset with issues flagged or corrected where possible

4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Your approach and methodology
   - Key findings and results  
   - A verification section with intermediate values or sample outputs that allows a human reviewer to confirm correctness

## Constraints

- Use only the Python standard library (no pandas, numpy, etc.)
- Check for at least these issue types: duplicates, missing fields, invalid formats, logical inconsistencies, out-of-range values
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify it executes and produces the expected stdout format

## Evaluation Criteria

- Correct identification of duplicate record IDs
- Detection of missing required fields
- Validation of date formats and logical consistency (age matches DOB)
- Detection of invalid zip codes, phone numbers, and out-of-range values
- Identification of inconsistent categorical values
- Well-structured quality report and cleaned output
- Clear, well-structured summary that enables human verification of results
