# Task 7-04: Racial Disparity in Substantiation and Removal

**Difficulty:** Advanced | **Points:** 16

## Context

Racial disproportionality in the child welfare system is a well-documented concern. Black children are overrepresented at nearly every decision point — from investigation to substantiation to removal. A policy equity team needs to quantify racial disparities at two critical stages: (1) the rate at which investigated allegations are substantiated, and (2) the rate at which substantiated allegations lead to child removals. By computing relative risk ratios compared to White children, the team can identify which racial groups experience the greatest disparities.

You are given three CSV files from the MiSACWIS (Michigan Statewide Automated Child Welfare Information System) administrative database:

## Input Files

1. **alleghist.csv** — Allegation history records. Each row represents one allegation at the per-case, per-child, per-perpetrator level. Multiple rows may exist per intake for the same child.
   - `intake_id` — Intake identifier
   - `screeningdecision` — Screening decision: "Investigate" or "Screen Out"
   - `county_name` — Michigan county name
   - `complaint_date` — Date of complaint (MM/DD/YYYY)
   - `allegationtypedesc` — Type of allegation
   - `intakechildpartyid` — Child victim party ID
   - `intakeperppartyid` — Alleged perpetrator party ID
   - `findingdesc` — Investigation finding: "Preponderance", "No Preponderance", "No Evidence", or empty
   - Additional fields: `abuseneglect`, `child_role`

2. **childrace.csv** — Race information for children.
   - `childpartyid` — Child party ID (corresponds to `intakechildpartyid` in alleghist)
   - `racedesc` — Race description: "White", "Black", "Hispanic", or "Other"
   - Race flag columns: `ame`, `asi`, `bla`, `haw`, `whi`, `mis` (binary indicators)

3. **allegmatch.csv** — Bridge table linking substantiated allegations to child removals.
   - `childpartyid` — Child party ID (corresponds to `intakechildpartyid` in alleghist)
   - `intake_id` — Intake ID (corresponds to `intake_id` in alleghist)
   - `intake_date` — Intake date (MM/DD/YYYY)
   - `rmvl_dt` — Removal date (MM/DD/YYYY)
   - `preponderance_flag` — Whether the allegation was substantiated ("Y")
   - `time_to_removal` — Days from intake to removal

## Task

Write `solution.py` that quantifies racial disparities in child welfare outcomes at the substantiation and removal stages, computing rates by race and relative risk ratios with White children as the reference group. The analysis should use all three input files.

### Key Definitions

- The unit of analysis is the **child-intake pair** — a unique combination of (`intakechildpartyid`, `intake_id`). Because a single intake can involve multiple children, each child within an intake is tracked separately. Because one child-intake pair can generate multiple allegation rows (one per perpetrator per allegation type), you must deduplicate to unique child-intake pairs before counting.
- A child-intake pair is **screened in** if any of its allegation rows has a screening decision of "Investigate."
- A child-intake pair is **substantiated** if any of its screened-in allegation rows has a finding of "Preponderance."
- A substantiated child-intake pair is **linked to removal** when it has a corresponding record in the allegmatch bridge table (matched on both `childpartyid` and `intake_id`).
- Each child-intake pair's **race** is determined by joining the child's `intakechildpartyid` to the `childpartyid` in childrace.csv.
- **Relative Risk (RR)** = rate for comparison group / rate for reference group (White).

## Required Output

### Standard Output (stdout)

Print the following lines exactly:

```
Total allegation records: <N>
Unique child-intake pairs: <N>
Child-intake pairs matched to race data: <N>
Child-intake pairs not matched: <N>

Child-intake pairs by race:
  White: <N> (<X.X>%)
  Black: <N> (<X.X>%)
  Hispanic: <N> (<X.X>%)
  Other: <N> (<X.X>%)

Substantiation rates by race:
  White: <X.X>% (n=<N>)
  Black: <X.X>% (n=<N>)
  Hispanic: <X.X>% (n=<N>)
  Other: <X.X>% (n=<N>)

Removal rates by race (of substantiated):
  White: <X.X>% (n=<N>)
  Black: <X.X>% (n=<N>)
  Hispanic: <X.X>% (n=<N>)
  Other: <X.X>% (n=<N>)

Relative risk (vs White):
  Black substantiation RR: <X.XX>
  Black removal RR: <X.XX>
  Hispanic substantiation RR: <X.XX>
  Hispanic removal RR: <X.XX>
  Other substantiation RR: <X.XX>
  Other removal RR: <X.XX>

Most overrepresented (substantiation): <RACE>
Most overrepresented (removal): <RACE>
```

Notes:
- "n=" in substantiation rates refers to the denominator (screened-in count for that race)
- "n=" in removal rates refers to the denominator (substantiated count for that race)
- RR formatted to 2 decimal places
- All rates to 1 decimal place with `%` sign
- Report races in order: White, Black, Hispanic, Other

### Output Files

1. `disparity_report.csv` — One row per race with columns: race, total_child_intakes, screened_in, substantiated, removed, substantiation_rate, removal_rate
2. `summary.md` — A markdown summary describing the racial disparity findings and policy implications

## Constraints

- Use only the Python standard library (no pandas, numpy, scipy, or other external packages)
- Read all input files from the current working directory
- Write output files to the current working directory
- After writing `solution.py`, run it (`python3 solution.py`) to verify output
