# Task 7-03: Time-to-Permanency with Re-entry Flagging

**Difficulty:** Advanced | **Points:** 16

## Context

Federal child welfare policy emphasizes "permanency" — achieving a stable, lasting living arrangement for children removed from their homes. Key outcome measures include the time it takes to reach permanency (discharge from foster care) and whether children re-enter care after discharge (indicating the permanency arrangement failed). A policy research team needs to compute time-to-permanency metrics by discharge type and flag children who re-entered foster care within 12 months of a prior discharge.

You are given two CSV files from the MiSACWIS (Michigan Statewide Automated Child Welfare Information System) administrative database:

## Input Files

1. **removals.csv** — Child removal episodes. Each row represents one removal of a child into out-of-home care. A child may have multiple rows if they were removed more than once.
   - `childpartyid` — Child party ID
   - `rmvl_dt` — Removal date (MM/DD/YYYY)
   - `dschrg_dt` — Discharge date (MM/DD/YYYY), empty if child is still in care
   - `dischargereasondesc` — Reason for discharge: "Reunification", "Adoption", "Guardianship", "Emancipation", "Transfer to Another Agency", or empty if still in care
   - `removal_county_name` — County where removal occurred
   - Additional fields: `responsible_county_name`, `plcmnt_episode_id`, `cust_start_date`, `cust_end_date`

2. **childpersoninfo.csv** — Demographic information for children.
   - `childpartyid` — Child party ID (primary key)
   - `birth_dt` — Date of birth (MM/DD/YYYY)
   - Additional fields: `src_record_id`, `genderdesc`, `hispanic_latino_txt`, `urm_indicator`

## Task

Write `solution.py` that computes time-to-permanency metrics for children in foster care, analyzes outcomes by discharge reason, and identifies children who re-entered care after a prior discharge. The analysis should use both input files.

### Key Definitions

- A **re-entry** occurs when a child has a subsequent removal after being discharged from a prior episode. The re-entry interval is the number of days between the prior episode's discharge date and the next episode's removal date.
- A **re-entry within 12 months** is one where the re-entry interval is ≤ 365 days.
- **Age at first removal** is calculated in whole years (floor).

## Required Output

### Standard Output (stdout)

Print the following lines exactly:

```
Total removal records: <N>
Unique children: <N>
Discharged episodes: <N>
Still in care: <N>

Children with multiple removals: <N>
Total re-entries (any interval): <N>
Re-entries within 12 months: <N>
Re-entry rate (12-month): <X.X>%

Median days in care (all discharged): <X.X>
Mean days in care (all discharged): <X.XX>

Time to discharge by reason:
  Reunification: median=<X.X> days (n=<N>)
  Adoption: median=<X.X> days (n=<N>)
  Guardianship: median=<X.X> days (n=<N>)
  Emancipation: median=<X.X> days (n=<N>)
  Transfer to Another Agency: median=<X.X> days (n=<N>)

Shortest median time: <REASON>
Longest median time: <REASON>

Mean age at first removal: <X.X>
```

Notes:
- "Total re-entries (any interval)" counts every consecutive episode pair where the prior episode was discharged
- "Re-entries within 12 months" counts only those with interval ≤ 365 days
- Re-entry rate denominator is total discharged episodes
- Median and mean formatted as shown (1 or 2 decimal places)

### Output Files

1. `summary.md` — A markdown summary describing the permanency findings, re-entry patterns, and time-to-discharge by reason

## Constraints

- Use only the Python standard library (no pandas, numpy, scipy, or other external packages)
- Read all input files from the current working directory
- Write output files to the current working directory
- After writing `solution.py`, run it (`python3 solution.py`) to verify output
