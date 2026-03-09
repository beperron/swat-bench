A research team is conducting a content analysis of 20 years of social work conference abstracts to map the prevalence of key practice areas and research methodologies over time.

# Task: Keyword Frequency Analysis with Wildcard Matching

Read a list of 20 keyword stems from a CSV file and perform wildcard matching against abstracts in a large JSON dataset of conference presentations. Each keyword stem should match all words that begin with that stem (e.g., "disparit" matches "disparity", "disparities"). Count each keyword match only once per abstract and rank keywords by overall frequency.

## Input Files

- `keyword_stems.csv` — A CSV file with a single column `Keyword` containing 20 keyword stems or phrases to search for
- `sswr_abstracts_sample.json` — Conference abstracts dataset (large JSON file with papers containing an `abstract` field)

## Matching Rules

Each keyword is matched using **case-insensitive wildcard-stem matching**:
- Place a word boundary (`\b`) at the start of the keyword
- Allow any additional word characters (`\w*`) after the last word of the keyword
- This means "child welfare" matches "child welfare", "child welfare's", etc.
- And "disparit" matches "disparity", "disparities"
- Escape any special regex characters in the keyword (e.g., hyphens in "evidence-based") with `re.escape()` before building the pattern
- Count each keyword at most once per abstract regardless of how many times it appears

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total keywords loaded: <N>
   Total papers with abstracts: <N>
   Papers with at least one match: <N>
   Total matches (keyword-paper pairs): <N>
   ```
   Then print a match table grouped by keyword in descending order of frequency:
   ```
   Keyword match counts (descending):
   1. <KEYWORD>: <N> abstracts
   2. <KEYWORD>: <N> abstracts
   ...
   20. <KEYWORD>: <N> abstracts
   ```
3. **Output files:**
   - `keyword_matches.csv` — Complete match table with columns: keyword, paper_id, title, year (one row per keyword-paper match)
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Your approach and methodology
   - Key findings and results
   - A verification section with intermediate values or sample outputs that allows a human reviewer to confirm correctness

## Constraints

- Use only the Python standard library (no pandas, numpy, etc.)
- The JSON file is large (~18 MB). Compile regex patterns once and reuse them rather than recompiling per abstract
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify it executes and produces the expected stdout format

## Evaluation Criteria

- Correct parsing of all 20 keywords from the CSV
- Correct loading and traversal of the JSON dataset
- Accurate wildcard-stem matching with word boundaries and `\w*` suffix
- Each keyword counted at most once per abstract
- Complete CSV output with all matches
- Clear, well-structured summary that enables human verification of results
