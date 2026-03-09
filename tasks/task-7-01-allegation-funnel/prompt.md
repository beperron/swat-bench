# Task 7-01: Allegation-to-Removal Funnel Analysis

**Difficulty:** Advanced | **Points:** 15

## Context

A policy analyst at the Michigan Department of Health and Human Services (MDHHS) needs to understand how child welfare allegations flow through the system — from initial complaint to removal into out-of-home care. This "funnel analysis" tracks the proportion of cases that advance through each stage: allegation → screened-in for investigation → substantiated → child removed. Understanding county-level variation in these conversion rates is critical for identifying systemic differences in how counties handle child welfare cases.

You are given three CSV files from the MiSACWIS (Michigan Statewide Automated Child Welfare Information System) administrative database:

## Input Files

1. **alleghist.csv** — Allegation history records. Each row represents one allegation at the per-case, per-child, per-perpetrator, per-allegation-type level. This means a single intake (identified by `intake_id`) may generate multiple rows: one child may have multiple alleged perpetrators, and each perpetrator may have multiple allegation types.
   - `intake_id` — Intake identifier
   - `screeningdecision` — Screening decision: "Investigate", "Screen Out", or "Transfer"
   - `county_name` — Michigan county name
   - `complaint_date` — Date of complaint (MM/DD/YYYY)
   - `allegationtypedesc` — Type of allegation
   - `intakechildpartyid` — Child victim party ID
   - `intakeperppartyid` — Alleged perpetrator party ID
   - `findingdesc` — Investigation finding: "Preponderance", "No Preponderance", "No Evidence", or empty (for non-investigated cases)
   - Additional fields: `src_intake_id`, `investigation_caseid`, `srcongoingcase`, `abuseneglect`, `relationtypeperptovictim`, `child_role`

2. **allegmatch.csv** — Bridge table linking substantiated allegations to subsequent child removals. Each row represents one allegation-to-removal linkage.
   - `childpartyid` — Child party ID (corresponds to `intakechildpartyid` in alleghist)
   - `intake_id` — Intake ID (corresponds to `intake_id` in alleghist)
   - `intake_date` — Intake date (MM/DD/YYYY)
   - `rmvl_dt` — Removal date (MM/DD/YYYY)
   - `preponderance_flag` — Whether the allegation was substantiated
   - `time_to_removal` — Days from intake to removal

3. **removals.csv** — Child removal episodes. Each row represents a removal of a child from their home into out-of-home care.
   - `childpartyid` — Child party ID
   - `rmvl_dt` — Removal date (MM/DD/YYYY)
   - `dschrg_dt` — Discharge date (MM/DD/YYYY), empty if still in care
   - `dischargereasondesc` — Reason for discharge
   - `removal_county_name` — County where removal occurred
   - Additional fields: `ongoing_cse_id`, `ongoing_src_cse_id`, `plcmnt_episode_id`, `cust_start_date`, `cust_end_date`, `agency_type`, `agency_name`

## Task

Write `solution.py` that performs a funnel analysis tracking how child welfare allegations progress through the system stages — screening, substantiation, and removal — and how conversion rates vary across counties. The analysis should use all three input files.

### Key Definitions

- The unit of analysis for the funnel is the **child-intake pair** — a unique combination of (`intakechildpartyid`, `intake_id`). Because a single intake can involve multiple children, each child within an intake is tracked separately through the funnel.
- A child-intake pair is **screened in** if any of its allegation rows has a screening decision of "Investigate."
- A child-intake pair is **substantiated** if any of its screened-in allegation rows has a finding of "Preponderance" (preponderance of evidence).
- A substantiated child-intake pair is **linked to removal** when it has a corresponding record in the allegmatch bridge table (matched on both `childpartyid` and `intake_id`).

## Required Output

### Standard Output (stdout)

Print the following lines exactly:

```
Total allegation records: <N>
Unique children: <N>
Unique child-intake pairs: <N>

Screened-in child-intakes: <N>
Screening-in rate: <X.X>%
Substantiated child-intakes: <N>
Substantiation rate (of screened-in): <X.X>%
Linked to removal: <N>
Removal rate (of substantiated): <X.X>%

County funnel:
  <COUNTY>: child_intakes=<N>, screened_in=<N>, substantiated=<N>, removed=<N>, removal_rate=<X.X>%
  ...

Highest screening-in rate: <COUNTY> (<X.X>%)
Highest substantiation rate: <COUNTY> (<X.X>%)
Highest removal rate: <COUNTY> (<X.X>%)
```

Notes:
- List counties in this order: Wayne, Kent, Oakland, Genesee, Ingham
- All rates should be formatted to one decimal place with a `%` sign

### Output Files

1. `funnel_report.csv` — One row per county with columns: county, total_intakes, screened_in, substantiated, removed, screening_rate, substantiation_rate, removal_rate
2. `summary.md` — A markdown summary describing the funnel analysis findings and county-level variation

## Constraints

- Use only the Python standard library (no pandas, numpy, scipy, or other external packages)
- Read all input files from the current working directory
- Write output files to the current working directory
- After writing `solution.py`, run it (`python3 solution.py`) to verify output
