A program director is comparing the cost-effectiveness of three social service programs to inform resource allocation decisions. You have cost breakdowns and per-client outcome data for each program.

# Task: Cost-Effectiveness Analysis

Calculate total costs, per-client costs, cost per outcome unit, and identify the most cost-effective program. Also compute Incremental Cost-Effectiveness Ratios (ICERs) comparing each program to the cheapest one.

## Input Files

- `costs.csv` -- Cost breakdowns by program and category. Columns: program, program_label, cost_category, amount, clients_served. Each program has 4 cost categories (staff, training, supplies, overhead).
- `cea_outcomes.csv` -- Per-client outcome data. Columns: client_id, program, improvement_score (0-50 scale), completed (0 or 1).

## Required Output

1. **Script:** Save your code as `solution.py`
2. **Stdout:** Print results in this exact format:
   ```
   Program A total cost: <N>
   Program B total cost: <N>
   Program C total cost: <N>
   Program A cost per client: <X.XX>
   Program B cost per client: <X.XX>
   Program C cost per client: <X.XX>
   Program A cost per outcome unit: <X.XX>
   Program B cost per outcome unit: <X.XX>
   Program C cost per outcome unit: <X.XX>
   Most cost-effective: <PROGRAM>
   ICER A vs reference: <X.XX>
   ICER B vs reference: <X.XX>
   ```

   Definitions:
   - **Total cost** = sum of all cost categories for a program
   - **Cost per client** = total cost / clients_served
   - **Cost per outcome unit** = total cost / (clients_served x mean_improvement_score)
     where mean_improvement_score is the average improvement_score from cea_outcomes.csv for that program
   - **Most cost-effective** = the program with the lowest cost per outcome unit
   - **ICER** (Incremental Cost-Effectiveness Ratio) = (Cost_X - Cost_ref) / (Effect_X - Effect_ref)
     where the reference is the cheapest program (lowest total cost) and Effect = mean improvement score.
     Only print ICER lines for non-reference programs (A and B if C is cheapest).

3. **Output files:**
   - `cea_results.csv` -- One row per program with columns: program, total_cost, clients_served, mean_improvement, cost_per_client, cost_per_outcome_unit
4. **Summary:** Save a human-readable summary as `summary.md` that includes:
   - Overview of each program's costs and outcomes
   - Comparison of cost-effectiveness across programs
   - ICER interpretation and recommendation
   - Verification section with intermediate calculations

## Constraints

- Use Python 3 (standard library preferred; pandas acceptable)
- Do not hardcode file paths -- read from the current directory
- After writing solution.py, run it (`python3 solution.py`) to verify output
