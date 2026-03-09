A research team administered a screening survey with conditional skip logic and needs to validate that respondents followed the skip patterns correctly.

# Task: Skip Logic Validation

## Input Files

1. `survey_responses.csv` — 80 survey responses with columns: respondent_id, q1_has_children (Yes/No), q2_num_children, q3_child_ages, q4_employed (Yes/No), q5_employer, q6_work_hours, q7_mental_health_dx (Yes/No), q8_dx_type, q9_in_treatment, q10_satisfaction (1-5)

2. `skip_rules.csv` — Defines the skip logic rules with columns: trigger_question, trigger_value, skip_questions
   - Each rule means: IF trigger_question == trigger_value, THEN skip_questions should be EMPTY (skipped).
   - Conversely: IF trigger_question != trigger_value, THEN skip_questions should HAVE data (not empty).

## Required Output

1. **Script:** `solution.py` — Python script that reads both files, validates skip logic, and produces output.

2. **Stdout:** Print the following lines exactly:
```
Total respondents: <N>
Total skip rules: <N>
Should-be-empty violations: <N>
Should-have-data violations: <N>
Total violations: <N>
Respondents with violations: <N>
Clean respondents: <N>
Most violated rule: <description>
```

Notes:
- **Should-be-empty violations:** Count each individual field that has data when the skip rule says it should be empty. For example, if q1_has_children=No and both q2_num_children and q3_child_ages have data, that counts as 2 violations. Count across ALL respondents and ALL rules.
- **Should-have-data violations:** Count each individual field that is empty when the skip rule says it should have data (because the trigger condition was NOT met). For example, if q4_employed=Yes but q5_employer is empty and q6_work_hours is empty, that counts as 2 violations.
- **Total violations:** Sum of should-be-empty and should-have-data violations.
- **Respondents with violations:** Number of unique respondents who have at least one violation of any type.
- **Clean respondents:** Total respondents minus respondents with violations.
- **Most violated rule:** The rule (by trigger_question) with the most total violations (both types combined). Format as: `<trigger_question>=<trigger_value> -> skip <skip_questions>`

3. **Output file:** `violation_report.csv` — A CSV listing each violation found, with columns including at minimum: respondent_id, rule (trigger question), violation_type (should_be_empty or should_have_data), field.

4. **Summary:** `summary.md` — brief description of the validation findings.

## Constraints

- Python standard library ONLY (no pandas, numpy, scipy, sklearn).
- The script must be named `solution.py` and run with `python3 solution.py`.

## Evaluation Criteria

- Correct respondent and rule counts
- Accurate violation detection for both types
- Correct identification of most violated rule
- Output files exist (violation_report.csv, summary.md)
