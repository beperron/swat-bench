# Test 042: Multi-File Merge with Validation

## Context

A program evaluation requires combining data from three separate administrative systems — client demographics, service utilization records, and outcome assessments. The `client_id` field serves as the linking key across all three files. However, real-world administrative data often has mismatches: some clients may appear in one system but not another, and the relationship between clients and services is one-to-many. The evaluator needs to document all data quality issues before proceeding with the merge.

## Input Files

1. **`demographics.csv`** (~80 rows) with columns:
   - `client_id` — unique client identifier
   - `name` — client full name
   - `age` — integer age
   - `gender` — "Male", "Female", or "Non-binary"
   - `race` — race/ethnicity category
   - `zip_code` — 5-digit ZIP code

2. **`services.csv`** (~150 rows) with columns:
   - `service_id` — unique service record identifier
   - `client_id` — client identifier (links to demographics)
   - `service_date` — date of service in YYYY-MM-DD format
   - `service_type` — type of service provided
   - `duration_minutes` — length of service in minutes
   - `provider_id` — provider identifier

3. **`outcomes.csv`** (~60 rows) with columns:
   - `assessment_id` — unique assessment identifier
   - `client_id` — client identifier (links to demographics)
   - `assessment_date` — date of assessment in YYYY-MM-DD format
   - `pre_score` — pre-intervention score
   - `post_score` — post-intervention score

## Task

Write `solution.py` that reads all three files, performs data quality checks, identifies merge issues, and creates a merged dataset.

Specifically:
1. Count records and unique clients in each file
2. Identify clients present in all three files
3. Identify clients in demographics only (not in services or outcomes)
4. Identify orphan service records — `client_id` values in services that do NOT appear in demographics
5. Create a merged dataset by inner-joining demographics and services on `client_id` (only rows where the client exists in both files)
6. Calculate mean services per client (for clients that appear in both demographics and services)

## Required Output

### Standard Output (stdout)

Print the following lines exactly:

```
Demographics records: <N>
Service records: <N>
Outcome records: <N>
Unique clients in demographics: <N>
Unique clients in services: <N>
Unique clients in outcomes: <N>
Clients in all three files: <N>
Clients in demographics only: <N>
Orphan service records (no demographics match): <N>
Merged dataset rows: <N>
Mean services per client: <X.X>
```

Note: "Orphan service records" counts the number of unique client_ids in services that have no match in demographics.

### Output Files

1. **`merged_data.csv`** — the inner-joined dataset of demographics and services (one row per service record where the client exists in demographics), including all columns from both files
2. **`summary.md`** — a markdown report documenting the data quality findings, merge statistics, and any issues found

## Constraints

- Use only Python standard library (no pandas, numpy, or other external packages)
- Read all input files from the current working directory
- Write output files to the current working directory

## Eval Criteria

- Correct record counts for each input file
- Correct identification of unique clients per file
- Correct count of clients present in all three files
- Correct identification of demographics-only clients
- Correct count of orphan service client_ids
- Correct merged dataset row count (inner join of demographics + services)
- Correct mean services per client calculation
- Output CSV and markdown files exist
