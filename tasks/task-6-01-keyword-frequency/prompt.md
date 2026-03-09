A policy researcher at a social work school needs to analyze public comments on a federal rulemaking about clinical practice requirements.

# Task: Analyze Federal Comments for Professional Mentions

Analyze public comments on federal rulemaking to identify and count mentions of social work and nursing professionals. Produce daily counts of each.

## Input Files

- `FederalComment.csv` — Public comments submitted to federal agencies, with comment text and posting dates

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total comments: <N>
   Social work mentions: <N>  (number of comments containing at least one social work match)
   Nursing mentions: <N>  (number of comments containing at least one nursing match)
   Both mentions: <N>  (number of comments containing both social work AND nursing matches)
   Date range: <YYYY-MM-DD> to <YYYY-MM-DD>
   ```
   Then print daily counts as:
   ```
   <YYYY-MM-DD>: total=<N>, social_work=<N>, nursing=<N>
   ```
3. **Output files:**
   - `daily_counts.json` — daily breakdown in JSON format

4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Your approach and methodology
   - Key findings and results  
   - A verification section with intermediate values or sample outputs that allows a human reviewer to confirm correctness

## Constraints

- Use the Python standard library for analysis
- Social work pattern should match: social work/worker/workers, social welfare/service/services, and credentials (MSW, LCSW, LMSW, BSW)
- Nursing pattern should match: nurse/nurses/nursing, and credentials (RN, LPN, NP, APRN, DNP, CNS, CRNA)
- Use case-insensitive matching with word boundaries (`\b`) around credential abbreviations (e.g., `\bRN\b`, `\bMSW\b`) to avoid false positives from partial matches inside other words
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify it executes and produces the expected stdout format

## Evaluation Criteria

- Correct identification of the comment text column in the CSV
- Accurate regex pattern construction for both professions
- Correct daily aggregation using the posting date field
- Accurate total counts
- Clear, well-structured summary that enables human verification of results
