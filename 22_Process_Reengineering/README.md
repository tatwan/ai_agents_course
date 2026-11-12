# Lab 22: How to re-engineer a process with agents

**CPU | No API key | No model calls | Practises: mapping a process as steps, choosing a workflow or an agent per step, setting autonomy, and estimating what a redesign is worth**

## Goal

Decide, step by step, which parts of a process to hand to software, how far each part may act before a person
looks, and whether the redesign is worth what it costs. The notebook starts with a Friday team lunch and then takes
the same method to a damaged-media refund at the Chinook music shop's support team, where one step needs an agent and
the payment waits for a person. In both, the lesson comes from a check a person adds after work is handed to
software. At lunch, reading every order back makes the organiser's Friday longer than before. On the refund, when a
reviewer re-checks the agent's work, the redesign still frees hours every month but costs more than those hours are
worth.

## What you will learn

- How to write a process down as steps, with the minutes a person spends on each step and the evidence it reads.
- How to ask five questions of each step, and tell a step for a fixed workflow from a step where an agent fits.
- How to set an autonomy level (suggest, draft, act with audit, act) for each step, with a reason, and why a payment
  stays at draft even when every step of it is known.
- How to count a redesign's minutes, including the review and the rework it adds.
- How to turn the minutes a redesign frees into dollars at a wage, set them against what the system costs, and
  change one assumption to see what moves.

## What you will do

One notebook, `22_process_reengineering.ipynb`: a Friday lunch first (Parts A and B), then the shop's refund
(Parts C to G).

**Part A: Decide which steps of a Friday team lunch to hand over.** Four steps and their minutes, two questions per
step, the four autonomy levels, and the payment kept at draft.
**Part B: Count the minutes a read-back adds to the lunch.** The organiser reads every order back after a missed
allergy, and lunch takes longer than before the handover.
**Part C: Map the damaged-media refund as steps.** The customer's email, the policy's "damaged twice" rule, six
steps with their evidence and minutes, and the before-and-after drawing.
**Part D: Ask five questions of each step, and find the step that needs an agent.** The five questions (the path,
the evidence, undoing a mistake, the volume and the owner), the earlier damage ticket that names no album, and `route`
run on every step.
**Part E: Set how far each step may go on its own.** An autonomy level and a reason per step.
**Part F: Redesign the refund and count its minutes.** Handling and review counted apart.
**Part G: Estimate what the redesign is worth each month, and raise the review time.** Minutes first, then dollars,
by hand and as `estimate`, and the same redesign with a longer review.
**Challenge.** A shorter read-back at lunch, a refund case with no photo, and the review time where the redesign
stops paying.

![The damaged-media refund before and after the redesign: six steps by hand at 18 minutes a case on top; below, our code logs and checks, an agent finds the earlier damage report, our code applies the policy, one model call drafts the reply, a person reviews for 2 minutes and a person approves the refund in 2 minutes](resources/lab22_process_map.png)

## Checkpoints

| After | You should see |
|---|---|
| Part A | 4 steps and 12 minutes of the organiser's time; 1 minute after the handover, the payment at draft |
| Part B | 13 minutes with the read-back, against 12 before the handover |
| Part C | 6 steps, 18 minutes a case, the evidence each step reads; the drawing |
| Part D | `route` on the refund: `('workflow', ['a person approves'])`; five workflows and one agent (`history`) |
| Part E | `log` and `check` act with audit, `history` suggests, `decide`, `reply` and `refund` are drafts |
| Part F | 2 minutes of handling and 2 of review, 4 in all, against 18 |
| Part G | base scenario: 12.8 minutes saved a case, 3,840 minutes (64 hours) freed a month, worth 1,920 USD; system cost 1,203 USD, of which the model calls are 3 USD; net +717 USD a month. With 8 minutes of review: 2,040 minutes (34 hours) freed and −183 USD a month |
| Challenge | 4 minutes for lunch with 3 orders read back; with no photo, `('workflow', ['fix the record first'])`; the net falls 150 USD per minute of review and turns negative between 6 minutes (+117) and 7 (−33) |

The scenario's numbers are assumptions, written in one dictionary in Part G: 300 cases a month, 30 US dollars an
hour, one case in ten reworked for 12 minutes, 1 US cent of model calls a case, 200 dollars a month to run and a
12,000-dollar build spread over 12 months. Change any of them and run `estimate` again.

**About the saved outputs.** The notebook calls no model and every number is written in the notebook, so the outputs
are the same on every run. The model cost, like every number in the scenario, is an assumption we chose.

## Before you start

- **Run it locally:** in the repository folder, `uv sync` (or `pip install -r requirements.txt`), then open
  `22_process_reengineering.ipynb` in VS Code or JupyterLab (`uv run jupyter lab`) with the `.venv` kernel, and run
  it from the top.
- **No key needed.** The notebook calls no model and does not read `.env`.
- **Data:** it reads two files of the shop's corpus in place, `data/corpus/policy_damaged_media.md` and
  `data/corpus/ticket_06_germany_warped_vinyl.md`, and writes nothing.

| What you see | Why | Fix |
|---|---|---|
| `StopIteration` in the setup cell | no folder above the notebook holds `models.env`, so the notebook was opened outside the repository | open the notebook from inside the cloned repository folder |

## Folder contents

| Path | What it is |
|---|---|
| `22_process_reengineering.ipynb` | the notebook, with saved outputs |
| `resources/lab22_process_map.png` and `.mmd` | the before-and-after drawing and its source |
| `solved/22_process_reengineering_solution.ipynb` | the challenge solved, run with its outputs |

## Resources

- [Python tutorial: data structures](https://docs.python.org/3/tutorial/datastructures.html): lists, tuples and
  dictionaries, and looping over a dictionary with `.items()`.
- [Python tutorial: unpacking argument lists](https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists):
  what the `*` in `route(*answers["refund"])` does.
- [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents): workflows
  (predefined code paths) against agents (the model directs its own steps), and when each fits.
- [OpenAI: A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf):
  the section "When should you build an agent?" on complex decisions, rules that are hard to maintain, and
  unstructured data.

Next: [Lab 23: What agent platforms sell](../23_Agent_Platforms/README.md). Back to [the lab list](../README.md).
