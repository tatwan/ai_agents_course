# Lab 20: How to evaluate and trace an agent

**CPU | API key: `OPENAI_API_KEY` | Runs a local MLflow page on port 5020 | Practises: testing an agent with a fixed test set, reading its traces, and choosing the evidence a judge reads**

## Goal

Test an agent with questions whose right answers are written down first, read every step it took as a trace on the
MLflow page, and use a second model as a judge only when it reads the record that settles the question (at the desk,
the billing record, not the customer's ticket). The lab has two notebooks and an extra one.

**Notebook 1** works on a small library helper with one tool that reads the opening hours. Three test questions pass.
The fourth asks about a public holiday the hours never mention, and the helper answers "Yes" with Monday's usual
hours. The trace on the MLflow page shows that it read the hours and answered beyond them. Then a judge marks a wrong
quiz answer as right, because the evidence it was given came from a prank website.

**Notebook 2** takes the same tools to the Chinook support desk. The desk agent is traced, then tested on eight fixed
cases with MLflow's evaluation, and every failing case is read from its reply and its trace: a customer's name typed
without its accent ends in "no such customer". Then a judge reads ticket 16, which claims that a refund was paid.
Given the ticket as its evidence, the judge accepts a false "paid" reply and quotes the ticket back. Given the billing
record, the same judge rejects it.

## What you will learn

- How to write test cases with an answer key the agent never sees, and check each reply in code.
- How to start the MLflow page on your own machine, record every agent run as a trace with `mlflow.openai.autolog()`,
  and read a trace as a tree of spans: the run, the agent, each model call and each tool call.
- How to use a failing test and its trace together: the test says the answer is wrong, and the trace shows what the
  agent read and did before it answered.
- How to write a test set as data and run it with `mlflow.genai.evaluate`, with scorers that check the reply and
  scorers that read the trace to check which tools ran.
- How a judge marks an answer against the evidence it is given, how to build one with MLflow's `make_judge`, and why
  it must read the record that decides and not the text that makes a claim.
- How to price every model call from its usage, cached input included, and stop a run at a budget (extra notebook).

## What you will do

### Notebook 1: test, trace and judge a library helper (`20a_meet_evals_and_tracing.ipynb`)

**Part A: Test the helper with questions whose answers we wrote down first.** The opening hours, the helper agent,
one reply checked against a regular expression, three cases, then the public holiday case.
**Part B: Trace a run and read its spans on the MLflow page.** The page started on port 5020, recording switched on
with `autolog`, the holiday question traced, the trace printed as a tree, the tool's output, and the same trace on the
page.
**Part C: Mark an answer with a second model, and see that the verdict follows the evidence.** A quiz judge given a
prank website's line, then an atlas's line.
**Challenge.** Fix the holiday answer without breaking the other three cases.

### Notebook 2: test and trace the Chinook desk agent (`20b_evals_and_tracing_at_the_desk.ipynb`)

**Part A: Build the desk agent and trace one question.** Three database lookups, the refund policy, ticket 16 with a
planted claim and the billing record as tools; the agent; Helena's question traced and read as a tree.
**Part B: Run eight fixed cases with MLflow's evaluation and read the failures.** One case field by field, the set as
MLflow data, two scorers, `mlflow.genai.evaluate`, the results table, the failing cases with their tool calls, and the
evaluation on the page.

![One row of the test set in mlflow.genai.evaluate: the question goes to the desk agent, which produces a reply and a trace; the expectations go only to the two scorers, facts_in_reply and right_tools, whose scores are saved as an evaluation run on the MLflow page](resources/lab20_evaluation.png)

The drawing follows one row of Part B through `mlflow.genai.evaluate`. The dark box is the model's work, the green
boxes are our code (the two scorers), and the white boxes are data: the row, the reply, the trace and the saved run.

**Part C: Judge a reply against the ticket, then against the billing record.** A judge built with `make_judge`, a
false "paid" reply judged twice, and the same fact checked in code.
**Challenge.** Close spellings for the customer lookup, and a scorer that checks the records the tools returned.

### Going further (`20_extra_cost_and_budget.ipynb`)

Price every request of a desk agent's run from its usage, see a long instructions block written to the prompt cache
and read from it, and stop a run with a budget hook before the call that would pass the budget.

## Checkpoints

| After | You should see |
|---|---|
| Notebook 1, Part A | three ✅ lines (Saturday 4 pm, closed on Sunday, 9:00 on Wednesday), then the same three and one ❌: *Yes, Riverside Library is open next Monday from 9:00 to 20:00.* |
| Notebook 1, Part B | the page at http://127.0.0.1:5020; a tree with `AgentRunner.run`, the agent, two turns (shown as `Unknown`), two model calls and one `get_opening_hours` call; the tool's output is the opening hours, with nothing about holidays |
| Notebook 1, Part C | the prank line gives CORRECT, the atlas line gives WRONG, each with a reason that points to the evidence |
| Notebook 2, Part A | Helena: 7 invoices, $49.62, Steve Johnson; `find_customer` with the accented name returning customer 6, then `get_invoices` and `get_support_rep` with id 6 |
| Notebook 2, Part B | eight rows; ours: 6 of 8 passed, `accent` failed both scorers (`{'matches': []}` for `Helena Holy`) and `out_of_scope` failed the facts scorer with a poem. 7 of 8 is also a normal result (see below) |
| Notebook 2, Part C | with the ticket, `supported: True` and a reason repeating "approved and paid on 2013-11-03"; with billing, `supported: False`; the code check prints `None` and `False` |
| Challenges | notebook 1: four ✅ lines, the holiday reply saying the hours do not cover public holidays. Notebook 2: with close spellings `accent` passes all three scorers (the agent looks Helena up again with the accent); without them the evidence scorer fails on `accent` too |

**About the saved outputs.** They come from `gpt-6-luna` with reasoning effort `none`, the model `models.env` names.
The model writes new replies on every run, so check the ticks, the tools called and the verdicts, not the wording;
timings and trace ids differ too. How often each result repeated on this model: the helper answered the holiday
question with "Yes" in all 14 runs we made with its instructions as written; without the sentence asking it to start
with Yes or No, it said the hours do not cover holidays in all 12 runs we tried. At the desk, the `accent` case failed
in all 7 runs of the set we counted, and the agent wrote the poem in 3 of those 7 and declined it in the other 4. The
quiz judge followed the evidence in 10 of 10 calls each way, and the desk judge accepted the false reply with the
ticket as evidence and rejected it with billing in 5 of 5 calls each way.

## Before you start

- **Lab 00 first.** It checks the environment and that your key reaches the model.
- **Run it locally:** in the repository folder, `uv sync` (or `pip install -r requirements.txt`), put
  `OPENAI_API_KEY` in `.env` (copied from `.env.example`), then open a notebook in VS Code or JupyterLab
  (`uv run jupyter lab`) with the `.venv` kernel. Run the setup cell first. Each notebook runs on its own.
- **The MLflow page:** both notebooks start it themselves on http://127.0.0.1:5020 and stop it in their last code cell,
  after the Challenge. From
  a terminal, in this folder: `uv run mlflow server --host 127.0.0.1 --port 5020 --backend-store-uri
  sqlite:///outputs/mlflow.db`. The first start takes about half a minute. On a remote machine or in Codespaces, open
  the address VS Code forwards for port 5020. No account is needed.
- **Where traces go:** into `20_Evals_And_Tracing/outputs/mlflow.db` on your machine, which git ignores. With
  `autolog` on, the Agents SDK does not send these runs to the Traces page of your OpenAI account.
- **Data:** `data/chinook.db`, the Chinook sample music shop, opened read-only; `data/corpus/` for the refund policy
  and ticket 16 (the ticket's planted line is replaced in memory; the file is not changed); `resources/golden_cases.json`
  for the eight test cases.
- **Cost:** about 60 model calls across the two notebooks and the extra, well under one US cent at the prices in
  `models.env`.

## Folder contents

| Path | What it is |
|---|---|
| `20a_meet_evals_and_tracing.ipynb` | notebook 1, the library helper, with saved outputs |
| `20b_evals_and_tracing_at_the_desk.ipynb` | notebook 2, the Chinook desk, with saved outputs |
| `20_extra_cost_and_budget.ipynb` | going further: prices, the prompt cache and a budget |
| `resources/golden_cases.json` | the eight test cases notebook 2 runs |
| `resources/lab20_evaluation.png` and `.mmd` | the drawing of one row through `mlflow.genai.evaluate`, and its source |
| `resources/lab20_mlflow_trace.png` | the MLflow page with notebook 1's holiday trace open |
| `resources/lab20_mlflow_evaluation.png` | the MLflow page with notebook 2's evaluation run open |
| `solved/20a_meet_evals_and_tracing_solution.ipynb` | notebook 1's challenge solved, run with its outputs |
| `solved/20b_evals_and_tracing_at_the_desk_solution.ipynb` | notebook 2's challenge solved, run with its outputs |

## Resources

- [MLflow tracing](https://mlflow.org/docs/latest/genai/tracing/): what a trace and a span record
- [MLflow: tracing the OpenAI Agents SDK](https://mlflow.org/docs/latest/genai/tracing/integrations/listing/openai-agent/):
  `mlflow.openai.autolog()` for agents and tools
- [MLflow: set up the server](https://mlflow.org/docs/latest/genai/getting-started/connect-environment/): the page on
  your own machine
- [MLflow: evaluating agents](https://mlflow.org/docs/latest/genai/eval-monitor/running-evaluation/agents/):
  `mlflow.genai.evaluate` with an agent and trace-reading scorers
- [MLflow: code-based scorers](https://mlflow.org/docs/latest/genai/eval-monitor/scorers/custom/): `@scorer`
- [MLflow: custom judges with `make_judge`](https://mlflow.org/docs/latest/genai/eval-monitor/scorers/llm-judge/custom-judges/):
  a judge's instructions, its placeholders and its verdict type
- [OpenAI: evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices): test
  sets, scorers and judges
- [OpenAI: prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching): cached input and cache
  writes (extra notebook)

Next: [Lab 21: How to call any model through one interface with LiteLLM](../21_LiteLLM/README.md). Back to
[the lab list](../README.md).
