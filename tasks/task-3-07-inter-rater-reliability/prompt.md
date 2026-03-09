You are a research assistant helping a faculty member analyze inter-rater reliability for a systematic review of literature on AI relevance.

# Task: Compute Inter-Rater Reliability

Compute Cohen's Kappa to measure inter-rater reliability between two raters in the provided dataset. One rater is a computer (LLM) and the other is a human. Both provided binary ratings (relevant or not relevant) for a set of research papers.

## Input Files

- `kappa.csv` — Papers rated by two independent raters with binary relevance judgments

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total rows: <N>
   Both True: <N>
   Both False: <N>
   LLM True Human False: <N>
   LLM False Human True: <N>
   Po: <X.XXXX>
   Pe: <X.XXXX>
   Kappa: <X.XXXX>
   Interpretation: <text>
   Rating columns: llm_relevant, human_decision
   ```
3. **Output files:** None
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Your approach and methodology
   - Key findings and results  
   - A verification section with intermediate values or sample outputs that allows a human reviewer to confirm correctness

## Constraints

- Use only the Python standard library (no pandas, scipy, sklearn, etc.)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify it executes and produces the expected stdout format

## Evaluation Criteria

- Correct identification and handling of rating columns
- Correct computation of observed agreement, expected agreement, and kappa
- Appropriate handling of any data quality issues
- Correct interpretation of kappa value
- Clear, well-structured summary that enables human verification of results
