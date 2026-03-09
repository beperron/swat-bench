An agency director needs a data-driven analysis of worker caseloads and outcomes to inform staffing decisions and identify workers who may need additional support.

# Task: Caseload and Workload Analysis

## Input Files

- `case_assignments.csv` (~200 rows -- each row is a case)
  - Columns: case_id, worker_id, worker_name, case_type (Child Welfare/Mental Health/Substance Abuse/Housing), open_date, close_date, status (Open/Closed/Transferred), days_open, successful_closure (0/1), client_satisfaction (1-5)

## Required Output

1. **Script**: `solution.py`
2. **Stdout** must print the following exact format:

```
Total cases: <N>
Total workers: <N>
Total case types: <N>

Caseload by worker:
<WorkerName>: <N> cases, <X.X> avg days, <X.X>% success
... (one line per worker, sorted alphabetically by name)

Overall statistics:
Mean caseload per worker: <X.X>
Median caseload per worker: <X.X>
Max caseload: <N>
Min caseload: <N>
Caseload std: <X.X>
Overall success rate: <X.X>%
Mean days to closure: <X.X>
Mean satisfaction: <X.XX>
Highest caseload worker: <name>
Lowest success rate worker: <name>
```

3. **Output files**: None required beyond solution.py
4. **Summary**: `summary.md` -- narrative interpretation including staffing recommendations, identification of overloaded workers, and outcome patterns.

## Formulas

- **Caseload per worker**: count of cases assigned to each worker
- **Mean caseload**: sum of all worker caseloads / number of workers
- **Median caseload**: middle value of sorted worker caseloads
- **Caseload std**: population standard deviation of worker caseloads (divide by N, not N-1)
- **Overall success rate**: (total successful closures / total closed cases) * 100 -- only count cases with status "Closed"
- **Mean days to closure**: average days_open for cases with status "Closed" only
- **Mean satisfaction**: average client_satisfaction across ALL cases
- **Success % per worker**: (successful closures / closed cases) * 100 for that worker's closed cases
- **Highest caseload worker**: worker with the most cases
- **Lowest success rate worker**: worker with lowest success rate among those who have at least one closed case

## Constraints

- Python standard library ONLY (no numpy, pandas, scipy, etc.)
- Read input from `case_assignments.csv`
- Run `python3 solution.py` from the test directory to verify output
- Workers in "Caseload by worker" section must be sorted alphabetically by worker name

## Evaluation Criteria

- Correct case counts and worker counts
- Correct per-worker caseload statistics
- Correct overall summary statistics (mean, median, max, min, std)
- Correct success rate computation (closed cases only)
- Correct identification of highest caseload and lowest success rate workers
- summary.md file created with staffing recommendations
