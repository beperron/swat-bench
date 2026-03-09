A community mental health center is preparing program evaluation data for a funder report, but the dataset has systematic gaps that need to be characterized before analysis can proceed.

# Task: Missing Data Assessment for Program Outcomes

You are given a CSV file containing program outcome data from a community mental health center. The dataset has missing values across several columns, and you need to perform a comprehensive missing data assessment. Empty cells in the CSV represent missing values.

## Input Files
- `program_outcomes.csv` — Program outcome records with columns: client_id, age, gender, race_ethnicity, referral_source, primary_diagnosis, pre_score, post_score, sessions_attended, discharge_type, satisfaction_rating, follow_up_score

## Required Output
1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total records: <N>
   Total columns: 12
   Total missing cells: <N>
   Complete cases (no missing): <N>
   Records with 1+ missing: <N>

   Missing by column:
   client_id: <N>
   age: <N>
   gender: <N>
   race_ethnicity: <N>
   referral_source: <N>
   primary_diagnosis: <N>
   pre_score: <N>
   post_score: <N>
   sessions_attended: <N>
   discharge_type: <N>
   satisfaction_rating: <N>
   follow_up_score: <N>

   Column with most missing: <column_name>
   Percent complete overall: <X.X>
   ```
   - A cell is "missing" if it is empty (zero-length string after parsing the CSV)
   - "Percent complete overall" = (total non-missing cells / total cells) * 100, rounded to one decimal place
   - Print the column names in the exact order shown above
3. **Summary:** Save a human-readable summary as `summary.md` that describes the patterns of missing data and any recommendations

## Constraints
- Use only the Python standard library (no pandas, scipy, sklearn, etc.)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify

## Evaluation Criteria
- Correctly count total records and total missing cells
- Correctly identify complete vs. incomplete cases
- Correctly count missing values per column
- Correctly identify the column with the most missing data
- Accurately compute the overall percent complete
- Provide a clear summary of missing data patterns
