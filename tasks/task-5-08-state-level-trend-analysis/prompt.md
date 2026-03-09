A criminal justice researcher is analyzing geographic and temporal trends in fatal police shootings to inform policy recommendations on use of force.

# Task: State-Level Trend Analysis of Fatal Police Shootings

Analyze the provided Washington Post fatal police shootings dataset. Count shootings by state and year for 2020-2023, identify the states with the highest counts, and compute year-over-year changes to assess whether shootings are increasing or decreasing.

## Input Files

- `fatal-police-shootings-data.csv` — Washington Post v2 dataset of fatal police shootings in the United States

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:

   ```
   Total records: <N>  (count of ALL records in the dataset, before any filtering)
   Records 2020-2023: <N>
   ```
   Then for each year (2020, 2021, 2022, 2023):
   ```
   Year: <YYYY>
   Total shootings: <N>
   1. <STATE>: <N>
   2. <STATE>: <N>
   ...
   10. <STATE>: <N>
   Top state: <STATE>
   ```
   Then year-over-year trends:
   ```
   Year-over-year change:
   2020-2021: <+/-N> (<+/-X.X>%)
   2021-2022: <+/-N> (<+/-X.X>%)
   2022-2023: <+/-N> (<+/-X.X>%)
   ```
3. **Output files:**
   - `shootings_by_state.csv` — all state-year counts (not just top 10), with columns: year, state, count

4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Your approach and methodology
   - Key findings and results
   - A verification section with intermediate values or sample outputs that allows a human reviewer to confirm correctness

## Constraints

- Use only the Python standard library (no pandas, numpy, etc.)
- Filter to calendar years 2020, 2021, 2022, and 2023 only for the analysis
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify it executes and produces the expected stdout format

## Evaluation Criteria

- Correct date parsing and year filtering
- Accurate counts per state per year
- Correct ranking (top 10 by count, descending)
- Correct year-over-year trend calculations
- Well-structured CSV output file
- Clear, well-structured summary that enables human verification of results
