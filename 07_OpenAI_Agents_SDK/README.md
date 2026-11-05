# Lab 07: How the OpenAI Agents SDK runs your loop

**CPU | API key: `OPENAI_API_KEY` | Optional: Graphviz for the drawings | Practises: building an agent in a framework and recognising the loop inside it; choosing how two agents work together**

## Goal

Rebuild the Chinook desk agent in the OpenAI Agents SDK and read what its `Runner` did, item by item and span by span,
as the loop we wrote by hand in lab 04. Every SDK call is a coroutine, so the lab starts with `await`. The moment that
teaches the framework comes in Part F, when one question needs two specialists. Asked *How many invoices does Puja
Srivastava have, what do they add up to, and who is her support rep?*, a triage agent that **hands the question off**
to the invoices specialist loses the rep every time we ran it (6 of 6 runs in the saved notebook): control moved to an agent with no
rep tool and never came back. The same two specialists **used as tools** answer all three facts (6 of 6), at
8 model requests against 3 for one agent with all three tools.

## What you will learn

- How `async def`, `await` and `asyncio.gather` work, and why two model calls made with `AsyncOpenAI` finish in
  about the time of the slower one.
- How to turn plain Python functions into tools with `function_tool`, give them to an `Agent`, and run it with
  `Runner.run`.
- How to read a run as the loop from lab 04: the `RunResult` (`new_items`, `raw_responses`, `usage`) and a trace of
  the run, kept in the notebook.
- Why every agent here sets `ModelSettings` from `models.env`, and how to read the effort the API really used.
- How to keep a conversation across runs with `SQLiteSession`.
- How to wire two specialists as tools and as a handoff, say who controls the next step in each, and what each costs.

## Coming from

Lab 04 wrote the agent loop by hand: send the messages and tools, run the tool calls, send the results back, stop on
an answer or a turn cap. Lab 05 kept the conversation and measured what it costs; lab 06 let the SDK use our tools
through MCP in a few lines. Here the SDK runs that whole loop for us, and we read what it did. The lab restates the
lookups and everything else it uses, so it runs on its own.

## What you will do

**Part A: Wait for two model calls at once with async.** From `def` to `async def`, what a coroutine is, `await`,
two waits one after the other and together with `asyncio.gather`, the blocking `time.sleep` mistake, then two real
model calls with `AsyncOpenAI`, timed both ways.
**Part B: Define the desk agent in the SDK.** The three Chinook lookups called by hand, `function_tool`'s generated
schema beside the one lab 03 wrote, the `Agent`, and its drawing with `draw_graph`.
**Part C: Read what the runner did.** The Helena question run with `Runner.run`; `new_items`, `raw_responses` and
`usage` read as lab 04's three turns; a trace of the run kept in the notebook with our own trace processor; the turn
cap as `MaxTurnsExceeded`.
**Part D: Set the reasoning effort the SDK does not set for this model.** What the SDK sends without `model_settings`,
the effort the API used read from the trace, and a lookup and an arithmetic question run at both efforts.
**Part E: Keep a conversation with a session.** A follow-up question without and with `SQLiteSession`, what the
session stored, and the same conversation found again from the file.
**Part F: Wire two specialists as tools and as a handoff.** Puja's two-part question four ways (one agent, our code
with `gather`, specialists as tools, a handoff), each run read, five runs of three of them counted, and a question
with one destination.
**Challenge.** Let the specialists hand back to the triage, and carry a conversation through the manager.

![Four ways to answer the two-part question: one agent with three tools; our code running two specialists with gather; a manager calling the specialists as tools and getting control back; a triage agent handing off to the invoices specialist, which keeps control](resources/lab07_wirings.png)

## Checkpoints

| After | You should see |
|---|---|
| Part A | two one-second sleeps: about 2 s one after the other, about 1 s gathered, results in argument order; `time.sleep` inside `async def` still about 2 s; two real calls gathered in about the time of the slower one (ours: 6.93 s against 1.95 s) |
| Part B | Helena 6, 7 invoices, $49.62, Steve Johnson; Puja 59, 6 invoices, $36.64, Jane Peacock; `function_tool`'s schema for `find_customer` matches lab 03's (strict, `name` a string with its description); a `Desk` agent with three tools, drawn |
| Part C | three model calls: `find_customer`, then `get_invoices` and `get_support_rep` in one reply, then the answer with 7, $49.62 and Steve Johnson; input tokens growing per request (206, 264 and 375); a trace `task` → `agent` → three `turn`s, each with a `response` and its `function` spans; `MaxTurnsExceeded` at `max_turns=1` |
| Part D | no SDK default for our model; the trace shows effort `medium` without `model_settings` and `none` with it; 0 reasoning tokens on the lookup at both; reasoning tokens on the comparison only at the API's default; the right numbers at both |
| Part E | without a session the follow-up does not know who "she" is and asks for her full name; with `SQLiteSession` it answers $49.62; 10 items stored, found again from the file |
| Part F | one agent: three facts, 3 requests; our code: three facts from two specialists run at once; as tools: three facts, 8 requests, specialists' runs nested in the trace, `last_agent` `Manager`; handoff: the rep missing, `last_agent` `Invoices`, no `get_support_rep` call; over five runs each: one agent 5 of 5, as tools 5 of 5, handoff 0 of 5 with all three facts; the rep-only question answered by `Support reps` |
| Challenge | handing back: handoffs `Triage -> Invoices -> Triage -> Support reps`, more requests and tokens than one agent, all three facts in 5 of 5 in the saved run (15 of 20 over all our runs); the manager with a session: Helena's three facts after *And what about Helena Holý?*, with the specialists' `input` naming Helena in full |

**About the saved outputs.** They come from `gpt-6-luna` at reasoning effort `none`, the model `models.env` names
(Part D also runs it at the API's default effort). The model chooses its tool calls and writes its replies on every
run, so wording, timings and token counts change from run to run and from model to model; Part A's sleeps and Part
D's effort settings do not. Check the facts, the tool calls and the counts, not the words. The handoff losing the
rep did not vary: it happened in every run we made on this model.

## Before you start

- **Lab 00 first.** It checks the environment and that your key reaches the model.
- **Run it locally:** in the repository folder, `uv sync` (or `pip install -r requirements.txt`), put
  `OPENAI_API_KEY` in `.env` (copied from `.env.example`), then open `07_openai_agents_sdk.ipynb` in VS Code or
  JupyterLab (`uv run jupyter lab`) with the `.venv` kernel. Run the setup cell first.
- **Graphviz** (optional): `draw_graph` needs the `dot` program (`sudo apt install -y graphviz` on Ubuntu,
  `brew install graphviz` on a Mac). Without it only the drawing cells fail; every run works.
- **Traces stay local.** The notebook replaces the SDK's trace uploader with a recorder that keeps the spans in the
  notebook, so nothing is sent to the OpenAI dashboard.
- **Files it writes:** Part E keeps its conversation in `07_OpenAI_Agents_SDK/outputs/sessions.db`, which git
  ignores (both `outputs/` and `*.db` are in `.gitignore`).
- **Data:** `data/chinook.db`, the Chinook sample music shop, opened read-only. Nothing is downloaded.
- **Cost:** about 160 model calls of a few hundred to two thousand tokens each: around two US cents at the prices in
  `models.env`.

## Folder contents

| Path | What it is |
|---|---|
| `07_openai_agents_sdk.ipynb` | the guided notebook, with saved outputs |
| `resources/lab07_wirings.mmd` and `.png` | the four wirings diagram: its mermaid source and the exported image |
| `solved/07_openai_agents_sdk_solution.ipynb` | the challenge solved, run with its outputs |

## Resources

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/): the documentation's home, with a quickstart
- [Agents](https://openai.github.io/openai-agents-python/agents/) and
  [Running agents](https://openai.github.io/openai-agents-python/running_agents/): `Agent`, `Runner.run`, the agent
  loop, `max_turns`
- [Tools](https://openai.github.io/openai-agents-python/tools/): `function_tool`, schemas from type hints and
  docstrings, agents as tools
- [Results](https://openai.github.io/openai-agents-python/results/): `final_output`, `new_items`, `raw_responses`,
  `last_agent`
- [Tracing](https://openai.github.io/openai-agents-python/tracing/): traces, spans and custom trace processors
- [Sessions](https://openai.github.io/openai-agents-python/sessions/): `SQLiteSession` and the other session classes
- [Handoffs](https://openai.github.io/openai-agents-python/handoffs/) and
  [Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/): handoffs, agents as tools and
  orchestration in code
- [Visualization](https://openai.github.io/openai-agents-python/visualization/): `draw_graph`
- [Python `asyncio`: coroutines and tasks](https://docs.python.org/3/library/asyncio-task.html): `await`, `gather`,
  `TaskGroup`
- [OpenAI: reasoning models](https://developers.openai.com/api/docs/guides/reasoning): reasoning effort and reasoning
  tokens

Next: [Lab 08: How LangChain and LangGraph run the same agent](../08_LangChain_LangGraph/README.md). Back to [the lab list](../README.md).
