A clinical supervisor reviewing PHQ-9 depression screening data notices some unusual values that may indicate data entry errors, and the data needs to be cleaned before quarterly reporting.

# Task: Outlier Detection in PHQ-9 Clinical Assessment Data

You are given a CSV file containing PHQ-9 (Patient Health Questionnaire-9) depression screening scores. The PHQ-9 has 9 items, each scored 0-3, for a total valid range of 0-27. Severity categories are: Minimal (0-4), Mild (5-9), Moderate (10-14), Moderately Severe (15-19), Severe (20-27). Some records contain data entry errors that need to be identified and flagged.

## Input Files
- `phq9_scores.csv` — PHQ-9 assessment records with columns: client_id, clinician_id, assessment_date, item_1 through item_9, total_score, severity_category

## Required Output
1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total records: <N>
   Clean records: <N>
   Total flagged records: <N>

   Issues found:
   Impossible total scores (outside 0-27): <N>
   Invalid item scores (outside 0-3): <N>
   Sum mismatches (total != sum of items): <N>
   Category mismatches: <N>
   Total issues: <N>

   After cleaning:
   Valid records: <N>
   Mean total score: <X.XX>
   Median total score: <X.X>
   Std total score: <X.XX>
   ```
   - Each issue type is checked independently (a single row can have multiple issues)
   - "Total flagged records" = number of unique rows that have at least one issue
   - "Clean records" = total records minus flagged records
   - "Category mismatches" counts rows where the total_score is within the valid 0-27 range but the severity_category does not match the expected category for that score. Rows with impossible total scores (outside 0-27) should NOT be counted as category mismatches — they are already captured under "Impossible total scores."
   - "Total issues" = sum of all individual issue counts
   - "After cleaning" statistics are computed using ONLY clean records (those with zero issues)
   - Standard deviation should use the population formula (divide by N, not N-1)
3. **Summary:** Save a human-readable summary as `summary.md` describing the issues found and recommendations

## Constraints
- Use only the Python standard library (no pandas, scipy, sklearn, etc.)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify

## Evaluation Criteria
- Correctly count total, clean, and flagged records
- Correctly identify impossible total scores outside the valid 0-27 range
- Correctly identify individual item scores outside the valid 0-3 range
- Correctly identify rows where total_score does not equal the sum of item scores
- Correctly identify rows where severity_category does not match the total_score
- Accurately compute mean, median, and standard deviation of clean records
- Provide a clear summary of data quality issues
