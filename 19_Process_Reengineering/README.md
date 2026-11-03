# Lab 19: How to re-engineer a process with agents

**CPU | No API key | No model calls | Practises: process design, per-step autonomy and impact estimates**

## Goal

Decide which steps of a damaged-media refund process need automation, set how far each may act, and estimate the impact of a redesign. The refund stays at **draft** for a person to approve; the calculator shows how review and rework consume the capacity we hoped to release.

## What you will learn

- Map steps and the evidence each needs, including informal copying and handoffs.
- Apply five questions without confusing a known path with available context.
- Set autonomy separately for each step and retain a payment-approval gate.
- Redesign the work and calculate capacity and dollar equivalents with explicit units and assumptions.
- Defend a build, buy or neither decision, then use the worksheet for your own process.

## Run first

From the repository folder run `uv sync` (or `pip install -r requirements.txt`), then open `19_process_reengineering.ipynb` in VS Code or JupyterLab with the `.venv` kernel. Run top to bottom. No key or secret-file loading is needed. The notebook reads supplied policy files and a bundled measurement snapshot; it writes no files and starts no server. It requires basic Python lists, dictionaries and arithmetic, all explained where they carry the decision.

The worked solution in `solved/` repeats all parts and runs independently. No earlier lab has to be run.

## What you will do

**Part A: Map the process.** Read the policies and an illustrative case, inspect one step dictionary, then map six steps and their human effort.

**Part B: Ask the five questions of each step.** Separate path, evidence, recoverability, value and ownership; print every answer with a plain reason.

**Part C: Set how far each step may go.** Choose autonomy per step, keeping payment at draft and closure dependent on a receipt.

**Part D: Redesign the process.** Remove retyping, move evidence checks earlier, join eligibility and reply preparation, and add a review queue.

**Part E: Estimate the impact.** Reconstruct a recorded token charge, separate it from business assumptions, and vary review and rework to find where the benefit disappears.

**Part F: Decide build, buy or neither.** Compare illustrative system costs and identify the operating evidence that the decision still needs.

**Part G: Apply it to your own process.** Use a worksheet with a missing-photo fallback and a solo path.

**Challenge.** Recalculate with more review/rework, block the payment step on unavailable context, and write an owned decision. The worked notebook shows every result and reason.

![Before and after the damaged-media refund process, with bounded checks, optional drafting, human review and receipt-based closure](resources/lab19_process_map.png)

## Checkpoints

| After | You should see |
|---|---|
| Part A | Six ordered steps, 18.0 human min/case in the assumed baseline |
| Part B | Five explained answers per step; Q1 Yes for all six; refund/Q3 No |
| Part C | Three steps at draft, three at act with audit; refund waits for human approval |
| Part D | Five redesigned steps, 6 handling + 2 review = 8 human min/case before extra rework |
| Part E | 8,800 min/month released; $3,779.85 USD/month net capacity-value estimate; break-even review 9.56 min/case at the base assumptions |
| Sensitivity | At 10 review min/case and 10% rework: 800 min/month released but −$220.15 USD/month net value |
| Part F | Illustrative build $3,779.85 and buy $3,199.85 USD/month; compare access, ownership and observed quality before choosing |
| Part G | A missing photo blocks context; request evidence before deciding eligibility |
| Solved challenge | At 6 review min/case and 30% rework: 2,400 min/month and $579.85 USD/month; unavailable payment evidence adds a context block without changing the workflow or human gate |

The base assumptions are 1,000 cases/month, 18 before and 6 non-review after min/case, 2 review min/case, 10% extra rework at 12 min/affected case, wage 30 USD/hour (1.0 USD per wage-currency unit), one recorded lookup-equivalent model task/case, $120 operations/month and a $6,000 build allocated over 12 months. These are illustrative business assumptions. Capacity valued at a wage becomes cash savings only through an actual staffing or redeployment decision. The calculator excludes queue delays, wrong-payout losses, customer harm and compliance work.

**About the saved outputs.** This notebook calls no model. Its bundled Lab 18 snapshot records `gpt-6-luna` at reasoning effort `none`, source notebook `18_evals_and_tracing.ipynb`, recorded on 2026-11-01. The changed eight-case set passed 7/8 = 0.875, as did the baseline; changed usage was 20 model calls, 9,048 input tokens, zero cached reads/writes and 581 output tokens, costing $0.00119530 total or $0.0001494125/task. The eight-case score is not a refund-error probability. We use only its token cost as an editable proxy and vary the business rework assumption separately. Each notebook's arithmetic outputs come from its own complete local run.

## Folder contents

| Path | What it is |
|---|---|
| `19_process_reengineering.ipynb` | Guided process-design notebook with real local outputs |
| `solved/19_process_reengineering_solution.ipynb` | All parts and a fully worked challenge, run independently |
| `resources/lab18_run_summary.json` | Fixed recorded measurement; no prior run required |
| `resources/README.md` | Snapshot fields, policy provenance and limits |
| `resources/lab19_process_map.mmd` and `.png` | Source and exported before/after diagram |

## Resources

- [Python data structures](https://docs.python.org/3/tutorial/datastructures.html): dictionaries and lists.
- [Python JSON](https://docs.python.org/3/library/json.html): loading the recorded measurement.
- [Python copies](https://docs.python.org/3/library/copy.html): independent challenge assessments.
- [NIST AI Risk Management Framework](https://airc.nist.gov/airmf-resources/airmf/): governance, context, measurement and ongoing management.

Next: [Lab 20: What agent platforms sell](../20_Agent_Platforms/README.md). Back to [the lab list](../README.md).
