A field education coordinator needs to transform long-format student assessment records into a wide-format summary for accreditation reporting.

# Task: Reshape Long-Format Data and Produce Cross-Tabulations

Transform a long-format student assessment dataset into wide format and produce cross-tabulation summaries. The data contains competency scores for social work students across multiple semesters.

## Input Files

- `student_assessments.csv` — Assessment scores in long format with columns for student, semester, competency, score, and assessor

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total records: <N>
   Unique students: <N>
   Students with complete data: <N>
   Semesters: <comma-separated list>
   Competencies: <N>
   ```
   Then print the cross-tabulation of mean scores (competency x semester):
   ```
   Cross-tabulation:
   Mean scores by competency and semester:
   <COMPETENCY>: <SEMESTER1>=<X.XX>, <SEMESTER2>=<X.XX>, change=<+/-X.XX>
   ...
   ```
   Then print students needing remediation (any score below 3). Print the count on the first line, then list each instance:
   ```
   Students below threshold: <N>
   <STUDENT_ID> (<NAME>): <COMPETENCY> (<SEMESTER>) = <SCORE>
   ...
   ```
3. **Output files:**
   - `wide_format.csv` — one row per student, columns for each competency-semester combination
   - `competency_summary.csv` — mean, median, min, max for each competency by semester

4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Your approach and methodology
   - Key findings and results  
   - A verification section with intermediate values or sample outputs that allows a human reviewer to confirm correctness

## Constraints

- Use only the Python standard library (no pandas, numpy, etc.)
- Handle missing data (not all students have all scores — a student has "complete data" if they have scores for all competencies in both semesters)
- Sort output consistently (by student ID, by competency name)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify it executes and produces the expected stdout format

## Evaluation Criteria

- Correct long-to-wide transformation
- Accurate cross-tabulation with mean scores per competency per semester
- Correct identification of students below threshold
- Proper handling of missing data in the reshape
- Well-structured output files
- Clear, well-structured summary that enables human verification of results
