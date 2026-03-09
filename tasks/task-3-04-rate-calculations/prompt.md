# Rate Calculations for County Health Department

## Context
A county health department needs to calculate and compare rates of child abuse referrals, mental health service utilization, and substance abuse treatment admissions per 10,000 population across 6 districts.

## Input (two files)
1. `service_counts.csv` — Columns: district, referrals, mh_utilization, sa_admissions (counts per district)
2. `district_population.csv` — Columns: district, total_population, child_population, adult_population

## Task
Write a Python script (`solution.py`) using only the standard library that reads both CSV files, calculates rates per 10,000 population, and identifies key comparisons. Print all results to stdout in the exact format shown below.

## Required Output Format (stdout)
```
Districts analyzed: <N>

Referral rates per 10,000 children:
  District_1: <X.X>
  District_2: <X.X>
  District_3: <X.X>
  District_4: <X.X>
  District_5: <X.X>
  District_6: <X.X>

MH utilization rates per 10,000 adults:
  District_1: <X.X>
  District_2: <X.X>
  District_3: <X.X>
  District_4: <X.X>
  District_5: <X.X>
  District_6: <X.X>

SA admission rates per 10,000 adults:
  District_1: <X.X>
  District_2: <X.X>
  District_3: <X.X>
  District_4: <X.X>
  District_5: <X.X>
  District_6: <X.X>

Highest referral rate district: <name>
Lowest referral rate district: <name>
County-wide referral rate: <X.X>
County-wide MH rate: <X.X>
County-wide SA rate: <X.X>
Mean referral rate: <X.X>
Rate ratio (highest/lowest referral): <X.XX>
```

## Required Output Files
1. `rate_table.csv` — Contains district, referral_rate_per_10k, mh_rate_per_10k, sa_rate_per_10k columns.
2. `summary.md` — A brief markdown summary of the key findings.

## Constraints
- Use only Python standard library (no pandas, numpy, scipy, etc.)
- Read data from both CSV files in the current directory
- Print results to stdout in the exact format above
- Referral rate = (referrals / child_population) * 10,000
- MH utilization rate = (mh_utilization / adult_population) * 10,000
- SA admission rate = (sa_admissions / adult_population) * 10,000
- County-wide rates: sum all counts across districts and divide by sum of relevant populations, then multiply by 10,000
- Mean referral rate: average of the 6 district-level referral rates
- Rate ratio: highest district referral rate divided by lowest district referral rate
