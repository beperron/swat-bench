# Test 043: Aggregation and Summarization

## Context

A crisis hotline manager needs monthly and quarterly summary statistics from daily call logs to include in a board report. The daily call log covers all of 2024 (a leap year, so 366 days) and includes metrics about call volume, wait times, crisis calls, and staffing.

## Input Files

- **`daily_call_log.csv`** (~366 rows, one per day for the year 2024) with columns:
  - `date` — date in YYYY-MM-DD format
  - `total_calls` — total calls received that day
  - `answered_calls` — calls answered by staff
  - `abandoned_calls` — calls where caller hung up before answer
  - `avg_wait_seconds` — average wait time in seconds for that day
  - `avg_duration_minutes` — average call duration in minutes for that day
  - `crisis_calls` — number of calls classified as crisis
  - `referrals_made` — number of referrals made
  - `staff_on_duty` — number of staff working that day

## Task

Write `solution.py` that reads the daily call log and computes:

1. Total counts for the full year (days, calls, answered, abandoned)
2. Overall abandonment rate
3. Monthly call volumes for all 12 months
4. Busiest and quietest months
5. Quarterly call totals (Q1=Jan-Mar, Q2=Apr-Jun, Q3=Jul-Sep, Q4=Oct-Dec)
6. Mean daily calls and mean daily crisis calls
7. Peak day call volume
8. Mean wait time across all days (simple average of the daily averages)

## Required Output

### Standard Output (stdout)

Print the following lines exactly:

```
Total days: <N>
Total calls: <N>
Total answered: <N>
Total abandoned: <N>
Overall abandonment rate: <X.X>%

Monthly call volumes:
  January: <N>
  February: <N>
  March: <N>
  April: <N>
  May: <N>
  June: <N>
  July: <N>
  August: <N>
  September: <N>
  October: <N>
  November: <N>
  December: <N>

Busiest month: <month name>
Quietest month: <month name>
Q1 total calls: <N>
Q2 total calls: <N>
Q3 total calls: <N>
Q4 total calls: <N>
Mean daily calls: <X.X>
Mean daily crisis calls: <X.X>
Peak day calls: <N>
Mean wait time (seconds): <X.X>
```

### Output Files

1. **`summary.md`** — a markdown report suitable for a board presentation that includes monthly trends, quarterly comparisons, and key metrics

## Constraints

- Use only Python standard library (no pandas, numpy, or other external packages)
- Read from `daily_call_log.csv` in the current working directory
- Write output files to the current working directory

## Eval Criteria

- Correct total day count
- Correct total call count
- Correct abandonment rate calculation
- Correct identification of busiest and quietest months
- Correct quarterly totals
- Accurate mean daily calls and crisis calls
- Correct peak day identification
- Correct mean wait time calculation
- Summary markdown file exists
