# Test 044: Binning Continuous Variables

## Context

A community health needs assessment collected continuous clinical measures from 150 participants. For a report to community stakeholders, these measures need to be categorized into clinically meaningful groups using standard classification thresholds. The binning must follow established clinical cutoffs for each measure.

## Input Files

- **`health_assessment.csv`** (150 rows) with columns:
  - `participant_id` — unique identifier
  - `age` — integer age (18-80)
  - `bmi` — body mass index (continuous, ~15-42)
  - `phq9_score` — Patient Health Questionnaire-9 depression screen (0-27)
  - `gad7_score` — Generalized Anxiety Disorder-7 screen (0-21)
  - `audit_c_score` — AUDIT-C alcohol use screen (0-12)
  - `systolic_bp` — systolic blood pressure (mmHg)
  - `monthly_income` — monthly income in dollars

## Task

Write `solution.py` that reads the health assessment data and creates new categorical columns by binning continuous variables according to the following clinical cutoffs:

### Binning Rules

1. **`age`** -> **`age_group`**:
   - "18-29" (age 18 to 29)
   - "30-44" (age 30 to 44)
   - "45-59" (age 45 to 59)
   - "60+" (age 60 and above)

2. **`bmi`** -> **`bmi_category`**:
   - "Underweight" (BMI < 18.5)
   - "Normal" (18.5 <= BMI <= 24.9)
   - "Overweight" (25.0 <= BMI <= 29.9)
   - "Obese" (BMI >= 30.0)

3. **`phq9_score`** -> **`depression_severity`**:
   - "None" (0-4)
   - "Mild" (5-9)
   - "Moderate" (10-14)
   - "Mod-Severe" (15-19)
   - "Severe" (20-27)

4. **`gad7_score`** -> **`anxiety_severity`**:
   - "Anxiety None" (0-4)
   - "Anxiety Mild" (5-9)
   - "Anxiety Moderate" (10-14)
   - "Anxiety Severe" (15-21)

5. **`audit_c_score`** -> **`drinking_risk`**:
   - "Low risk" (0-2)
   - "At risk" (3-7)
   - "High risk" (8+)

## Required Output

### Standard Output (stdout)

Print the following lines exactly:

```
Total participants: <N>

BMI categories:
  Underweight: <N>
  Normal: <N>
  Overweight: <N>
  Obese: <N>

Depression severity:
  None: <N>
  Mild: <N>
  Moderate: <N>
  Mod-Severe: <N>
  Severe: <N>

Anxiety severity:
  Anxiety None: <N>
  Anxiety Mild: <N>
  Anxiety Moderate: <N>
  Anxiety Severe: <N>

Drinking risk:
  Low risk: <N>
  At risk: <N>
  High risk: <N>

Obese rate: <X.X>%
Moderate+ depression rate: <X.X>%
At-risk+ drinking rate: <X.X>%
```

Where:
- "Moderate+ depression rate" = percentage of participants with Moderate, Mod-Severe, or Severe depression
- "At-risk+ drinking rate" = percentage of participants with At risk or High risk drinking

### Output Files

1. **`binned_data.csv`** — the original data with the new categorical columns appended
2. **`summary.md`** — a markdown summary of the distribution across all categories with key findings

## Constraints

- Use only Python standard library (no pandas, numpy, or other external packages)
- Read from `health_assessment.csv` in the current working directory
- Write output files to the current working directory

## Eval Criteria

- Correct total participant count
- Correct BMI category counts
- Correct depression severity counts
- Correct anxiety severity counts
- Correct drinking risk counts
- Accurate rate calculations
- Output CSV with binned columns exists
- Summary markdown file exists
