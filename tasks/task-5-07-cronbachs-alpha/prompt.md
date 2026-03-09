A faculty member is validating a test anxiety instrument and needs to compute reliability statistics before submitting a manuscript.

# Task: Compute Scale Reliability and Score a Survey Instrument

Compute Cronbach's alpha for a test anxiety survey instrument. The survey contains both positively and negatively worded items on a 4-point Likert scale. Positively worded items must be reverse-coded before computing reliability and total scores.

## Input Files

- `survey-data.csv` — Survey responses with a two-row header (short codes and full question text) followed by respondent data. The instrument consists of 21 Likert items in columns Q13 through Q33. Columns Q7–Q12 are demographic/intake questions and should NOT be included in the reliability analysis.

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total items: <N>
   Complete cases: <N>
   Reverse-coded items: <N>
   Alpha (raw): <X.XXXX>
   Alpha (with reverse coding): <X.XXXX>
   Mean total score (reverse coded): <X.XX>
   Std dev total score: <X.XX>
   ```
   Then print item-level statistics:
   ```
   Item-total correlations:
   <ITEM>: mean=<X.XX>, corrected_item_total_r=<X.XX>, alpha_if_deleted=<X.XXXX>, reverse=<yes/no>
   Alpha-if-deleted:
   ```
3. **Output files:** None
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Your approach and methodology
   - Key findings and results  
   - A verification section with intermediate values or sample outputs that allows a human reviewer to confirm correctness

## Reverse-Coded Items

The following 9 items are positively worded and must be reverse-scored on the 4-point scale (1↔4, 2↔3) before computing reliability and total scores:

- **Q15** — "I have less difficulty than the average college student in getting test instructions straight."
- **Q17** — "I am less nervous about tests than the average college student."
- **Q20** — "The prospect of taking a test is one of my courses would not cause me to worry."
- **Q21** — "I am more calm in test situations than the average college student."
- **Q22** — "I have less difficulty than the average college student in learning assigned chapters in textbooks."
- **Q25** — "I will do well in speed tests in which there are time limits."
- **Q29** — "Before taking a test, I feel confident and relaxed."
- **Q30** — "While taking a test, I feel confident and relaxed."
- **Q33** — "Finding unexpected questions on a test causes me to feel challenged rather than panicky."

## Constraints

- You may use pandas, numpy, and/or scipy if helpful
- Handle the two-row header structure
- Exclude respondents with missing Likert data from reliability calculations
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify it executes and produces the expected stdout format

## Evaluation Criteria

- Correct identification of the two-row header structure
- Correct application of reverse coding to the specified items
- Accurate Cronbach's alpha computation (raw and with reverse coding)
- Corrected item-total correlations computed for each item
- Alpha-if-item-deleted computed for each item
- Clear, well-structured summary that enables human verification of results
