# Task 7-05: Point-in-Time Foster Care Snapshot

**Difficulty:** Advanced | **Points:** 18

## Context

Federal reporting requirements mandate that states produce an annual "point-in-time" snapshot of all children in foster care on a specific date. This snapshot provides a cross-sectional view of the foster care population — who is in care, where they are placed, how long they have been in care, and the demographic composition. A data analyst needs to determine which children were in care on October 1, 2023, link them to their current placement type, compute demographics, and produce county-level summary statistics.

You are given four CSV files from the MiSACWIS (Michigan Statewide Automated Child Welfare Information System) administrative database:

## Input Files

1. **removals.csv** — Child removal episodes.
   - `childpartyid` — Child party ID
   - `rmvl_dt` — Removal date (MM/DD/YYYY)
   - `dschrg_dt` — Discharge date (MM/DD/YYYY), empty if child is still in care
   - `dischargereasondesc` — Reason for discharge, empty if still in care
   - `removal_county_name` — County where removal occurred
   - `plcmnt_episode_id` — Placement episode ID
   - Additional fields: `responsible_county_name`, `cust_start_date`, `cust_end_date`

2. **placements.csv** — Individual placement settings within removal episodes. A child can have multiple placements per episode as they move between care settings.
   - `childpartyid` — Child party ID
   - `placementepisodeid` — Placement episode ID
   - `provbegindt` — Placement begin date (MM/DD/YYYY)
   - `provenddate` — Placement end date (MM/DD/YYYY), empty if this is the current placement
   - `livingarrangedesc` — Living arrangement type: "Family Foster Care", "Relative Foster Care", "Group Home", "Institutional Care", "Pre-Adoptive Home"
   - `fc_placement_sequence` — Sequence number within the episode

3. **childpersoninfo.csv** — Demographic information for children.
   - `childpartyid` — Child party ID
   - `birth_dt` — Date of birth (MM/DD/YYYY)
   - Additional fields: `src_record_id`, `genderdesc`, `hispanic_latino_txt`, `urm_indicator`

4. **childrace.csv** — Race information for children.
   - `childpartyid` — Child party ID
   - `racedesc` — Race description: "White", "Black", "Hispanic", or "Other"
   - Race flag columns: `ame`, `asi`, `bla`, `haw`, `whi`, `mis`

## Task

Write `solution.py` that produces a point-in-time foster care snapshot for **October 1, 2023** — identifying all children who were in out-of-home care on that date, determining their current placement type, computing demographic and length-of-stay statistics, and producing county-level summaries. The analysis should integrate data from all four input files.

### Key Definitions

- **Age** on the snapshot date is calculated in whole years (floor).
- **Length of stay** is the number of days from the child's removal date to the snapshot date.

## Required Output

### Standard Output (stdout)

Print the following lines exactly:

```
Snapshot date: 10/01/2023

Total removal records: <N>
Total placement records: <N>

Children in care on snapshot date: <N>
Children matched to demographics: <N>
Children matched to placements: <N>

Overall snapshot:
  Median age: <X.X>
  Mean age: <X.XX>
  Median length of stay (days): <N>
  Mean length of stay (days): <X.XX>

Placement type distribution:
  Family Foster Care: <N> (<X.X>%)
  Relative Foster Care: <N> (<X.X>%)
  Group Home: <N> (<X.X>%)
  Institutional Care: <N> (<X.X>%)
  Pre-Adoptive Home: <N> (<X.X>%)

Race distribution:
  White: <N> (<X.X>%)
  Black: <N> (<X.X>%)
  Hispanic: <N> (<X.X>%)
  Other: <N> (<X.X>%)

County summary (ranked by caseload):
  <COUNTY>: n=<N>, median_age=<X.X>, median_los=<N>, pct_family_foster=<X.X>%
  ...

Largest county: <COUNTY>
Smallest county: <COUNTY>
County with longest median LOS: <COUNTY>
County with highest family foster rate: <COUNTY>
```

Notes:
- The snapshot date is **10/01/2023**
- Median length of stay reported as an integer (whole days)
- Placement type percentages use matched-to-placement count as denominator
- Race percentages use total in-care count as denominator
- Counties ranked from largest to smallest caseload
- All percentages to 1 decimal place

### Output Files

1. `snapshot_report.csv` — One row per county with columns: county, n, median_age, median_los, pct_family_foster
2. `summary.md` — A markdown summary describing the snapshot findings, demographics, county variation, and placement patterns

## Constraints

- Use only the Python standard library (no pandas, numpy, scipy, or other external packages)
- Read all input files from the current working directory
- Write output files to the current working directory
- After writing `solution.py`, run it (`python3 solution.py`) to verify output
