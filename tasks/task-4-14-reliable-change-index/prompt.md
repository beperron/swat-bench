A clinical supervisor is evaluating PHQ-9 treatment outcomes for 100 clients to determine which clients showed statistically reliable improvement, recovery, or deterioration using the Jacobson-Truax Reliable Change Index method.

# Task: Compute Reliable Change Index and Clinical Significance

Calculate the Reliable Change Index (RCI) for each client's PHQ-9 scores and classify their clinical outcomes using the Jacobson-Truax method.

## Input Files

- `treatment_outcomes.csv` — 100 clients with columns: client_id, pre_phq9, post_phq9, age, gender, treatment_group

## Given Parameters

- **Cronbach's alpha (α)** for the PHQ-9: **0.89**
- **Normative population values**: M_norm = 3.3, SD_norm = 3.8

## Required Computations

1. **Descriptive statistics**: Compute the mean and standard deviation (population formula, ddof=0) for pre and post PHQ-9 scores.

2. **Standard Error of Measurement (SEM)**:
   SEM = SD_pre × sqrt(1 - α)

3. **Standard Error of the Difference (S_diff)**:
   S_diff = sqrt(2 × SEM²)

4. **Clinical threshold (c)** using the weighted midpoint formula:
   c = (SD_clin × M_norm + SD_norm × M_clin) / (SD_clin + SD_norm)
   where M_clin = pre mean, SD_clin = pre SD

5. **RCI for each client**:
   RCI = (post_score - pre_score) / S_diff

6. **Classification** for each client:
   - **Recovered**: RCI < -1.96 AND post_score < c
   - **Improved**: RCI < -1.96 AND post_score ≥ c
   - **Unchanged**: -1.96 ≤ RCI ≤ 1.96
   - **Deteriorated**: RCI > 1.96

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total clients: <N>
   Pre mean: <X.XX>
   Post mean: <X.XX>
   SEM: <X.XX>
   Clinical threshold: <X.XX>
   Recovered: <N>
   Improved: <N>
   Unchanged: <N>
   Deteriorated: <N>
   ```
3. **Output files:**
   - `classification_results.csv` — One row per client with columns: client_id, pre_phq9, post_phq9, rci, classification
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Your approach and methodology
   - Key findings and results
   - A verification section with intermediate values or sample outputs that allows a human reviewer to confirm correctness

## Constraints

- Use only the Python standard library (no pandas, numpy, scipy, etc.)
- Use the population standard deviation formula (ddof=0) for all SD calculations
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify it executes and produces the expected stdout format

## Evaluation Criteria

- Correct computation of SEM and S_diff from given alpha
- Correct clinical threshold using weighted midpoint formula
- Accurate RCI calculation for each client
- Correct four-category classification
- Complete CSV output with all client classifications
- Clear, well-structured summary that enables human verification of results
