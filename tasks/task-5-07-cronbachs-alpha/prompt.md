A faculty member is validating a test anxiety instrument and needs to compute reliability statistics before submitting a manuscript.

# Task: Compute Scale Reliability and Score a Survey Instrument

Compute Cronbach's alpha for a test anxiety survey instrument. The survey contains both positively and negatively worded items on a 4-point Likert scale that must be identified and reverse-coded before computing reliability and total scores.

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

## Constraints

- Use only the Python standard library (no pandas, scipy, numpy, etc.)
- Identify reverse-coded items by reading the question text — positively worded items should be reverse-scored. Positive wording includes expressions of calmness, confidence, competence, lack of difficulty, lack of worry, or positive coping (e.g., "I feel confident," "I have less difficulty," "does not cause me to worry," "feel challenged rather than panicky"). There are approximately 8-10 such items in this instrument.
- Handle the two-row header structure
- Exclude respondents with missing Likert data from reliability calculations
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify it executes and produces the expected stdout format

## Evaluation Criteria

- Correct identification of the two-row header structure
- Correct identification of which items need reverse coding
- Accurate Cronbach's alpha computation (raw and with reverse coding)
- Corrected item-total correlations computed for each item
- Alpha-if-item-deleted computed for each item
- Clear, well-structured summary that enables human verification of results
