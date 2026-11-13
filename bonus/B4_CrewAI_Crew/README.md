# Bonus B4: How to build a crew with CrewAI

**CPU | API key: `OPENAI_API_KEY` | Own environment | Practises: splitting work between agents with their own tools; passing one task's output to another; checking a task's output in code**

## Goal

Meet CrewAI in a school newsroom, then put it to work at the Chinook support desk. The lab has two notebooks.

**Notebook 1** is a playground. A school paper needs a headline for Friday's match, which the Falcons lost 2 to 3.
Asked alone, a headline writer gives the Falcons a win. A sports reporter with a `match_result` tool looks the result
up, and once the headline task gets the report through `context`, the headline carries the real score. A guardrail
function sends back a headline with football slang the readers would not know, and the writer tries again. Then the
same crew is kept as files, the way `crewai create crew` lays out a project, loaded with `load_crew` and run with
`crewai run`.

**Notebook 2** takes the same pattern to the desk. *Puja Srivastava says invoice 229 was charged to her card twice
and asks for her money back.* A billing clerk with two database lookups finds the facts; a refund adviser with no
tools gets them through `context` and advises a refund of $13.86 as a typed `RefundAdvice`. The advice is well typed
and breaks the shop's rule that the desk refunds at most $10 itself: a guardrail in our code refuses it, and the
adviser corrects it to `human_review`.

## What you will learn

- What CrewAI's `LLM`, `Agent`, `Task` and `Crew` do, and what an agent's role, goal and backstory become in the
  request the model receives.
- How to switch on the crew's own log and read it, and read a run from its `CrewOutput`.
- How a task passes its output to a later task through `context`, so an agent with no tool works from another
  agent's facts, and what a sequential crew does when `context` is left out.
- How a guardrail function refuses a task's output and sends the reason back, and how it enforces a rule a typed
  output (`output_pydantic`) cannot.
- Why every database lookup opens its own connection: CrewAI runs the tool calls of one reply at the same time, in
  threads.
- Why one task is not one model request, and how to count and price a crew's requests.
- How a crew is kept as a project (`crew.jsonc`, agent files, a `tools/` folder) and run with `crewai run`.

## What you will do

### Notebook 1: meet CrewAI in a school newsroom (`b4a_meet_crewai.ipynb`)

**Part A: Ask the headline writer with no facts.** One plain call through CrewAI's `LLM`, and a headline with the
wrong winner.
**Part B: Run one agent and one task as a crew.** The `match_result` tool called by hand, the reporter and its task,
the crew's log, the `CrewOutput`, and the messages built from the role, goal and backstory.
**Part C: Pass the report to the headline writer with `context`.** Two tasks and three model requests, the context
the writer was given, and what happens with `context=[]`.
**Part D: Refuse a headline in code with a guardrail.** `check_headline` tried by hand, then on the task: a refused
headline and the second attempt.
**Part E: Keep the crew as files and run it with `crewai run`.** The `school_paper/` project, `load_crew`, and the
terminal command.
**Challenge.** Add a social media editor whose task reads both earlier tasks.
**Going further.** A `Flow` of two steps in an order our code sets, drawn with `plot`.

### Notebook 2: CrewAI at the Chinook desk (`b4b_crewai_at_the_desk.ipynb`)

**Part A: Build the clerk's two lookups and call them by hand.** `find_customer` and `get_invoice`, each with its own
read-only connection.
**Part B: Ask the refund adviser with no facts.** A `RefundAdvice` example, its Pydantic model, and the adviser's
advice with no amount.
**Part C: Pass the clerk's lookup to the adviser with `context`.** Two lookups running in two threads, the context
the adviser was given, and a refund of $13.86.
**Part D: Refuse advice that breaks the refund policy.** `check_advice` by hand and on the task, then what the run
cost.
**Challenge.** A refund under the limit (invoice 284, $8.91).

![One run of a two-task crew. Our code starts the crew. In task 1 the model asks for the tool, our tool function runs and returns the result, and the model writes it up. Task 1's output is passed on as context to task 2, where the model writes from the context with no tools. Our guardrail function then accepts the output, which becomes the CrewOutput, or refuses it and sends the reason back to task 2's model.](resources/b4_crew_tasks_and_context.png)

Dark boxes are the model's work, light green is our own code, white is text passed along.

## Checkpoints

| After | You should see |
|---|---|
| Notebook 1, Part A | one headline without the real result (ours: *Falcons Soar Past Otters in Friday Night Football Showdown*) |
| Notebook 1, Part B | the result sheet's JSON for the Falcons and a "no match" sentence for another team; a schema with one string, `team`; the log with a `match_result` call and the report (the Falcons lost 2–3, Lina Haddad scored both goals); 2 model requests; five messages, the system message built from the role, backstory and goal |
| Notebook 1, Part C | with `context=[report_task]`, a headline with the real score (ours: *Haddad's Brace Can't Keep Falcons from Falling 3–2 to Otters*), `prompt_context` equal to the report, 3 model requests; with `context=[]`, an empty `prompt_context` and a win again (ours: *Falcons Soar to a Big Win!*) |
| Notebook 1, Part D | Part C's headline refused by hand for *brace*; on the task, a ❌ line, then a ✅ line for a headline with *two goals*, and 4 model requests |
| Notebook 1, Part E | `crew.jsonc` with `"context": ["report_task"]`; two agent files and the `MatchResult` tool class; `load_crew` returns a `Crew` and `{'team': 'Northside Falcons'}`; the log, a headline with the score, 3 model requests |
| Notebook 2, Part A | Puja Srivastava, customer 59, India; invoice 229, customer 59, 2011-09-30, $13.86; "no match for invoice 9999"; every line in `MainThread` |
| Notebook 2, Part B | the example accepted by `RefundAdvice`; the adviser alone: amount 0.0, `human_review`, a reason saying the amount is not verified; 1 model request |
| Notebook 2, Part C | `find_customer` and `get_invoice` in two `ThreadPoolExecutor` threads; tools on the clerk only; the adviser's context equal to the clerk's lookup; `refund` of 13.86; 3 model requests |
| Notebook 2, Part D | the refund refused by hand; on the task, ❌ for the refund and ✅ for `human_review` of 13.86; 4 model requests; ours: 1,692 input and 225 output tokens, $0.00028 |
| Challenges | notebook 1: three task outputs, a post that names Lina Haddad with the score, accepted at once (ours: 103 characters), 4 model requests; notebook 2: one ✅ line for a refund of $8.91, 3 model requests |

**About the saved outputs.** They come from `gpt-6-luna` at reasoning effort `none`, as `models.env` sets it, with
`crewai` 1.15.40. The model writes every headline, report and piece of advice on each run, so the wording differs on
yours; check the facts, the ✅ and ❌ lines and the request counts. What we counted before saving: the headline
writer alone named a Falcons win in 16 of 17 runs (the other named no winner); with `context=[]` it named a win in 6
of 6; with the report as context the headline carried the real score in every run (more than 20). With the backstory
line *You love the words football fans use.* the first headline said *brace* and was refused in 10 of 10 runs, and
the second attempt passed every time; without that line, the first headline said *brace* and was refused in 15 of
19 runs. At the desk, the adviser alone gave the amount
0.0 and `human_review` in 6 of 6 runs; with the clerk's lookup as context it advised a refund of $13.86 in 6 of 6;
with the guardrail, that refund was refused and the second advice was `human_review` in 6 of 6, at 4 requests. The
two lookups of one reply ran in two threads in 13 of 13 runs.

## Before you start

- **Lab 00 first.** It checks the environment and that your key reaches the model.
- **This lab has its own environment.** CrewAI needs other `openai` and `mcp` versions than the core labs. In the
  repository folder:

  ```bash
  cd bonus/B4_CrewAI_Crew
  uv sync --locked --python 3.13
  ```

  Then open a notebook in VS Code or JupyterLab with `bonus/B4_CrewAI_Crew/.venv` as the kernel. For the pip route,
  make a Python 3.13 virtual environment in this folder and `pip install -r requirements.txt`. No notebook cell
  installs packages.
- **The key** goes in `.env` at the repository folder (copied from `.env.example`). Run each notebook's setup cell
  first; each notebook runs on its own.
- **CrewAI's switches.** Each notebook turns off CrewAI's anonymous usage statistics (`CREWAI_DISABLE_TELEMETRY`),
  its hosted tracing (`CREWAI_TRACING_ENABLED=false`) and its version check, prints the log without colours
  (`NO_COLOR`), and keeps CrewAI's own files in `outputs/`. CrewAI's hosted platform needs an account; this lab does
  not use it.
- **`crewai run`** (notebook 1, Part E) runs in a terminal, not in the notebook. Its first run installs the
  project's own environment in `school_paper/.venv` (about 850 MB). Set `MODEL` first, as Part E shows: without it
  the agent files run on CrewAI's default model, not the one in `models.env`.
- **Files it writes:** `outputs/` (CrewAI's record of the last run, `latest_kickoff_task_outputs.db`), and, after
  `crewai run`, `school_paper/.venv` and `school_paper/uv.lock`. Git ignores all of them.
- **Data:** `data/chinook.db`, the Chinook sample music shop, opened read-only.
- **Cost:** about 25 model requests for both notebooks, well under one US cent at the `models.env` prices.

## Folder contents

| Path | What it is |
|---|---|
| `b4a_meet_crewai.ipynb` | notebook 1, the playground, with saved outputs |
| `b4b_crewai_at_the_desk.ipynb` | notebook 2, the Chinook desk, with saved outputs |
| `school_paper/` | the newsroom as a CrewAI project: `crew.jsonc`, `agents/`, `tools/match_result.py`, `pyproject.toml`, `.gitignore` (notebook 1, Part E) |
| `resources/b4_crew_tasks_and_context.mmd` and `.png` | the picture of a two-task crew with context and a guardrail |
| `solved/b4a_meet_crewai_solution.ipynb` | notebook 1's challenge solved, run with its outputs |
| `solved/b4b_crewai_at_the_desk_solution.ipynb` | notebook 2's challenge solved, run with its outputs |
| `pyproject.toml`, `uv.lock`, `requirements.txt` | this lab's own environment |

## Resources

- [CrewAI documentation](https://docs.crewai.com/): the home page, with a quickstart
- [Agents](https://docs.crewai.com/en/concepts/agents) and [Tasks](https://docs.crewai.com/en/concepts/tasks): role,
  goal, backstory, tools; `context`, `output_pydantic`, guardrails
- [Crews](https://docs.crewai.com/en/concepts/crews): `kickoff`, `akickoff`, `verbose`, usage
- [LLMs](https://docs.crewai.com/en/concepts/llms): the `LLM` object and its settings
- [Tools](https://docs.crewai.com/en/concepts/tools): `@tool` and `BaseTool`
- [CLI](https://docs.crewai.com/en/concepts/cli): `crewai create crew` and `crewai run`
- [Flows](https://docs.crewai.com/en/concepts/flows): `@start`, `@listen`, `plot`
- [Telemetry](https://docs.crewai.com/en/telemetry): what CrewAI collects and the switches that turn it off

Compare with [Lab 18](../../18_Agent_Designs/README.md), which measures one agent against specialists on the same
desk. Back to [the bonus lab list](../README.md).
