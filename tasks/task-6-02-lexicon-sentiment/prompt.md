An evaluator is analyzing client satisfaction feedback from 5 programs using a custom sentiment lexicon. Each feedback entry is a short text, and the lexicon provides sentiment scores for specific words. You need to compute sentiment scores for each feedback and summarize results by program.

# Task: Lexicon-Based Sentiment Analysis

Score each client feedback text using the provided sentiment lexicon, classify feedback as positive/negative/neutral, and compare sentiment across programs.

## Input Files

- `feedback.csv` — 1,000 rows with columns: feedback_id, program, date, text. Each text is a short client feedback (15-40 words).
- `lexicon.csv` — ~200 words with columns: word, sentiment_score. Scores range from -3 (very negative) to +3 (very positive).

## Required Analysis

1. For each feedback text:
   - Tokenize the text into words (lowercase, split on non-alphabetic characters)
   - Match each word against the lexicon
   - Sum the sentiment scores of all matched words to get the feedback's sentiment score
2. Classify each feedback: positive (score > 0), negative (score < 0), neutral (score == 0)
3. Compute the overall mean sentiment score across all feedback
4. Compute mean sentiment score by program
5. Identify the top-scoring and bottom-scoring programs
6. Count total lexicon matches across all feedback

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Total feedback: <N>
   Positive count: <N>
   Negative count: <N>
   Neutral count: <N>
   Overall mean score: <X.XX>
   Top program: <PROGRAM> (<X.XX>)
   Bottom program: <PROGRAM> (<X.XX>)
   Lexicon matches: <N>
   ```
3. **Output files:**
   - `sentiment_results.csv` — One row per feedback with columns: feedback_id, program, sentiment_score, classification (positive/negative/neutral), num_matches
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Overall sentiment distribution (counts and percentages)
   - Program-level comparison table
   - Top 10 most frequently matched positive and negative words
   - Discussion of patterns across programs

## Constraints

- Use Python 3 (standard library preferred; pandas acceptable)
- Do not hardcode file paths — read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify output
