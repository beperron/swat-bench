A child welfare agency's intake database has accumulated duplicate entries from multiple referral sources over the past year and needs to be cleaned before analysis.

# Task: Duplicate Detection in Client Intake Records

You are given a CSV file containing client intake records from a child welfare agency. Some records are exact duplicates (identical rows entered more than once), while others share the same client ID but have different data fields (e.g., referred from two different sources on different dates). Your job is to identify and quantify these duplicates, then produce a deduplicated dataset.

## Input Files
- `client_intake.csv` — Client intake records with columns: client_id, first_name, last_name, dob, ssn_last4, referral_source, referral_date, case_type, assigned_worker, phone, zip_code

## Required Output
1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total records: <N>
   Unique client IDs: <N>
   Duplicate client IDs: <N>
   Exact duplicate rows: <N>
   Conflicting records (same ID, different data): <N>
   Records after removing exact duplicates: <N>
   Records after keeping first per client ID: <N>
   ```
   - "Duplicate client IDs" = number of distinct client_id values that appear more than once
   - "Exact duplicate rows" = number of rows that are perfect copies of another row (count the extras, not the originals)
   - "Conflicting records (same ID, different data)" = total number of rows belonging to client IDs where not all rows are identical — i.e., at least two rows for that client_id differ in one or more fields (count all rows for those IDs, including originals). Do NOT include client IDs whose duplicate rows are all exact copies of each other.
   - "Records after removing exact duplicates" = number of distinct rows (keeping one copy of each identical row)
   - "Records after keeping first per client ID" = number of rows when keeping only the first occurrence of each client_id
3. **Output files:** Save the deduplicated dataset (one row per client_id, keeping the first occurrence) as `deduplicated.csv`
4. **Summary:** Save a human-readable summary as `summary.md`

## Constraints
- Use only the Python standard library (no pandas, scipy, sklearn, etc.)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify

## Evaluation Criteria
- Correctly count total records, unique client IDs, and duplicate client IDs
- Correctly identify exact duplicate rows (all fields identical)
- Correctly identify conflicting records (same client_id, different field values)
- Correctly compute post-deduplication record counts
- Produce a valid deduplicated CSV output file
- Provide a clear summary of findings
