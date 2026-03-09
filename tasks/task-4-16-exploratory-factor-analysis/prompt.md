A doctoral student is examining the factor structure of a 20-item mental health screening instrument administered to 500 respondents. The items use a 1-5 Likert scale. You need to perform an exploratory factor analysis (EFA) to identify the underlying factor structure.

# Task: Exploratory Factor Analysis

Determine how many latent factors underlie the 20 screening items and identify which items load on each factor.

## Input Files

- `screening_items.csv` — 500 rows (one per respondent) with 20 columns: item_01 through item_20. Values are integers 1-5.

## Required Analysis

1. Compute the KMO (Kaiser-Meyer-Olkin) measure of sampling adequacy
2. Run Bartlett's test of sphericity
3. Compute eigenvalues of the correlation matrix
4. Determine the number of factors to retain using the Kaiser criterion (eigenvalue > 1.0)
5. Calculate total variance explained by the retained factors
6. Identify which items load primarily on each factor (assign each item to its highest-loading factor)
7. Report all 20 eigenvalues

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total respondents: <N>
   Total items: <N>
   KMO value: <X.XX>
   Bartlett p value: <X.XXXX>
   Factors retained: <N>
   Total variance explained: <X.X>%
   Factor 1 items: <comma-separated item names>
   Factor 2 items: <comma-separated item names>
   Factor 3 items: <comma-separated item names>
   Factor 4 items: <comma-separated item names>
   ```
   Note: List items by their column names (e.g., item_01, item_02). If fewer than 4 factors are retained, only print the factors you found.
3. **Output files:** None
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - KMO and Bartlett results with interpretation
   - Eigenvalue table for all 20 components
   - Factor loading matrix for retained factors
   - Discussion of factor structure and item groupings

## Constraints

- Use Python 3 (pandas and numpy acceptable; factor_analyzer or sklearn acceptable for factor extraction)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify output
