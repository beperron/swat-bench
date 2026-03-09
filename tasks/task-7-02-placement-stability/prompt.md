# Task 7-02: Placement Stability by Child Age and Race

**Difficulty:** Advanced | **Points:** 18

## Context

A child welfare research team wants to analyze placement stability — how many times children are moved between different placements during a single removal episode. Frequent placement changes ("placement disruptions") are associated with negative child outcomes. The team wants to understand whether placement stability varies systematically by child age at removal and by race, which could indicate systemic issues in matching children with appropriate placements.

You are given four CSV files from the MiSACWIS (Michigan Statewide Automated Child Welfare Information System) administrative database:

## Input Files

1. **childpersoninfo.csv** — Demographic information for children.
   - `childpartyid` — Child party ID (primary key)
   - `genderdesc` — Gender ("m" or "f")
   - `birth_dt` — Date of birth (MM/DD/YYYY)
   - `hispanic_latino_txt` — Hispanic/Latino indicator
   - Additional fields: `src_record_id`, `urm_indicator`

2. **childrace.csv** — Race information for children.
   - `childpartyid` — Child party ID
   - `racedesc` — Race description: "White", "Black", "Hispanic", or "Other"
   - Race flag columns: `ame`, `asi`, `bla`, `haw`, `whi`, `mis` (binary indicators)

3. **removals.csv** — Child removal episodes. Each row represents one removal episode.
   - `childpartyid` — Child party ID
   - `rmvl_dt` — Removal date (MM/DD/YYYY)
   - `dschrg_dt` — Discharge date (MM/DD/YYYY), empty if still in care
   - `plcmnt_episode_id` — Placement episode ID (unique identifier for this removal episode)
   - Additional fields: `dischargereasondesc`, `removal_county_name`, `cust_start_date`, `cust_end_date`

4. **placements.csv** — Individual placement settings within removal episodes. Each row represents one placement (a child can have multiple placements per episode as they move between foster homes, group homes, etc.).
   - `childpartyid` — Child party ID
   - `placementepisodeid` — Placement episode ID
   - `provbegindt` — Placement begin date (MM/DD/YYYY)
   - `provenddate` — Placement end date (MM/DD/YYYY), empty if current
   - `livingarrangedesc` — Living arrangement type
   - `fc_placement_sequence` — Sequence number within the episode
   - `providerctgydesc` — Provider category

## Task

Write `solution.py` that analyzes placement stability — how many times children are moved between different placements during a removal episode — and whether stability varies by child age at removal and by race. The analysis should integrate data from all four input files.

### Key Definitions

- **Age at removal** is calculated in whole years (floor). A child born 01/15/2015 and removed 01/10/2020 is age 4, not 5.
- **Placement count per episode** is the number of distinct placement records associated with a given removal episode.

## Required Output

### Standard Output (stdout)

Print the following lines exactly:

```
Records loaded:
  childpersoninfo: <N>
  childrace: <N>
  removals: <N>
  placements: <N>

Merged removal episodes: <N>
Children with complete data: <N>

Age at removal distribution:
  0-2: <N>
  3-5: <N>
  6-11: <N>
  12-17: <N>

Mean placements per episode: <X.XX>
Median placements per episode: <X.X>

Placements by age group:
  0-2: mean=<X.XX>, median=<X.X>
  3-5: mean=<X.XX>, median=<X.X>
  6-11: mean=<X.XX>, median=<X.X>
  12-17: mean=<X.XX>, median=<X.X>

Placements by race:
  White: mean=<X.XX> (n=<N>)
  Black: mean=<X.XX> (n=<N>)
  Hispanic: mean=<X.XX> (n=<N>)
  Other: mean=<X.XX> (n=<N>)

Most unstable group (age): <AGE_GROUP>
Most unstable group (race): <RACE>

Episodes with 3+ placements: <N>
Episodes with 3+ placements rate: <X.X>%
```

Notes:
- Mean values formatted to 2 decimal places, median to 1 decimal place
- Rates formatted to 1 decimal place with `%` sign

### Output Files

1. `stability_report.csv` — One row per age group with columns: age_group, n, mean_placements, median_placements
2. `summary.md` — A markdown summary describing the placement stability findings, patterns by age and race, and any notable disparities

## Constraints

- Use only the Python standard library (no pandas, numpy, scipy, or other external packages)
- Read all input files from the current working directory
- Write output files to the current working directory
- After writing `solution.py`, run it (`python3 solution.py`) to verify output
