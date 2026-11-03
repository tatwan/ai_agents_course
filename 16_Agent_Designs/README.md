# Lab 16: How to choose an agent design

**CPU | API key: `OPENAI_API_KEY` | Practises: choosing an agent design and saying what a second agent costs**

## Goal

Decide when a second agent pays for itself, by running the support desk's own requests through five designs and
measuring each one: model requests, tokens, seconds, cost, and whether the answer holds every fact. The moment comes
when the table is filled in. On Puja's two-part question, specialists used as tools are right in every run at 8
model requests against 3 for one agent, and a handoff loses the second half in every run (3 of 3). On the request
that names five customers, parallel sub-agents cost more in total (3,364 input tokens against 2,383 to 2,918), but
the agent that writes the answer reads 125 tokens instead of 760 to 791. A second agent is worth its cost only for a
job like that one.

## What you will learn

- How to run one request through one agent, specialists as tools, a handoff, parallel sub-agents and a hybrid of code
  and agent, and read requests, tokens, seconds and cost for each from the SDK's usage.
- How to measure the **final context**, what the agent that writes the answer has to read, and why parallel
  sub-agents keep it small.
- Why the tool descriptions are the router, by printing what the manager agent reads and measuring vague ones.
- How a hybrid lets our code answer labelled requests with no model call, and what it cannot do.
- How to decide with four reasons to split: different permissions, a smaller context, parallel work, another team or
  model.
- What A2A describes, from an agent card printed beside an MCP `tools/list` entry, and how CrewAI's roles, tasks and
  process map onto the same pieces.

## Coming from

Lab 04 wrote the agent loop by hand, and lab 07 rebuilt it in the OpenAI Agents SDK and wired two specialists four
ways on Puja's two-part question (one agent at 3 requests and 858 input tokens, the specialists as tools at 8 and
about 1,800, a handoff that lost the rep in every run). This lab measures again in its own run, adds parallel
sub-agents and a hybrid of code and agent, and asks when a second agent is worth it. It restates the lookups and the
SDK pieces it uses, so it runs on its own.

## What you will do

**Part A: Write the desk's requests and their right answers.** The three lookups on the read-only database, five
customers' totals by hand, four requests of different shapes (one destination, two parts, five independent parts, an
open question) with the facts a right reply must contain, and the five designs drawn.
**Part B: Measure one agent with all the tools.** One run read by hand (requests, input and output tokens, final
context, cost), then `measure`, which records every later run the same way, and the baseline on three requests.
**Part C: Measure specialists as tools.** Billing and Support agents with their own tools, a manager that asks them,
exactly what the manager's model reads, and what vague descriptions cost.
**Part D: Measure a handoff.** A triage agent, the transfer tools it sees, a run read item by item, and the second
half lost on the two-part request.
**Part E: Measure parallel sub-agents.** `asyncio.gather` on two waits, one worker per customer run at once, the main
agent's whole input printed, and its context against one agent's.
**Part F: Measure a hybrid of code and agent.** Requests from a form with a label, a handler per label, a router that
sends the rest to the agent, and a mislabelled request the code cannot see.
**Part G: Compare the designs and decide when to split.** The measured table, the failing replies, four reasons to
split and the designs we did not run.
**Part H: Read what A2A and CrewAI describe.** An MCP `tools/list` entry built in process, an A2A 1.0 agent card
checked for its required fields, and a CrewAI crew mapped onto the same agents, questions and wiring.
**Challenge.** Let a lead agent split the work, and grow the request to ten customers.

![Five agent designs: one agent with all the tools; a manager with specialists as tools; a triage agent handing off to one specialist; our code starting parallel workers whose one-line answers a main agent reads; and a hybrid where our code answers labelled requests and sends open ones to an agent](resources/lab16_designs.png)

## Checkpoints

| After | You should see |
|---|---|
| Part A | Helena 6, 7 invoices, $49.62, Steve Johnson; Puja 59, 6, $36.64, Jane Peacock; five different totals with Helena's ($49.62) the largest; `facts_found` gives `[True, True, True]` and `[True, True, False]` on the two test replies |
| Part B | one agent right on R1, R2 and R3 in every run; R1 3 requests and 727 input tokens, R2 3 and 846; R3 more requests and tokens that change from run to run (ours: 5 to 7 requests, 2,383 to 2,918 tokens) and the largest final context (ours: 760 to 791) |
| Part C | the manager reads two tools, each a name, a description and an `input` argument; right on R1 and R2 in every run at 5 and 8 requests; with vague descriptions it asked both specialists on R1 in every run (ours: 8 or 9 requests) |
| Part D | two `transfer_to_` tools; R1 right, last agent Support; R2 with the invoices and without the rep in every run, two handoffs asked and *Multiple handoffs detected, ignoring this one.* for the second |
| Part E | two one-second waits gathered in about 1 second; one worker 3 requests and one line; the main agent's context 125 tokens against one agent's 760 to 791; parallel sub-agents right at 16 requests and 3,364 input tokens every run |
| Part F | 0 model requests on the three labelled requests, every fact right; OPEN sent to the agent ($12.98, 4 requests); the mislabelled request answered with the rep, not the total |
| Part G | one block per request; one agent right on every request; the handoff the only design that missed (R2, every run); specialists as tools about twice one agent's requests and tokens on R2; the hybrid at 0 requests on labelled requests |
| Part H | the MCP entry with `name`, `description`, `inputSchema`, `outputSchema`; the agent card with no required field missing; CrewAI's `role`, `Task` and `Process` mapped onto instructions, the question and the wiring |
| Challenge | a lead agent asks five workers in one reply: 17 requests, final context between the code split's and one agent's (ours: 358); ten customers: one agent's final context grows about 105 tokens per customer (ours: 1,278), the main agent's about 16 (205), one agent still cheaper in total |

**About the saved outputs.** They come from `gpt-6-luna` at reasoning effort `none`, the model `models.env` names.
The model chooses its tool calls and writes its replies on every run, so wording, timings and token counts change
from run to run and from model to model; the hybrid's labelled answers and the request counts our code fixes (the
parallel design) do not. Check the facts and the counts, not the words. The handoff losing the rep did not vary: it
happened in every run we made on this model. One agent's path through the five-customer request did vary: from 3 to
8 requests.

## Before you start

- **Lab 00 first.** It checks the environment and that your key reaches the model.
- **Run it locally:** in the repository folder, `uv sync` (or `pip install -r requirements.txt`), put
  `OPENAI_API_KEY` in `.env` (copied from `.env.example`), then open `16_agent_designs.ipynb` in VS Code or JupyterLab
  (`uv run jupyter lab`) with the `.venv` kernel. Run the setup cell first.
- **Nothing is uploaded or written.** The notebook turns the SDK's trace upload off and writes no files.
- **Data:** `data/chinook.db`, the Chinook sample music shop, opened read-only. Nothing is downloaded.
- **Cost:** about 50 agent runs of a few hundred to a few thousand tokens each: under one US cent at the prices in
  `models.env`.

## Folder contents

| Path | What it is |
|---|---|
| `16_agent_designs.ipynb` | the guided notebook, with saved outputs |
| `resources/lab16_designs.mmd` and `.png` | the five designs diagram: its mermaid source and the exported image |
| `solved/16_agent_designs_solution.ipynb` | the challenge solved, run with its outputs |

## Resources

- [OpenAI Agents SDK: agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/): orchestration
  by a model and by code, agents as tools, handoffs, running agents in parallel
- [OpenAI Agents SDK: tools](https://openai.github.io/openai-agents-python/tools/) and
  [handoffs](https://openai.github.io/openai-agents-python/handoffs/): `as_tool`, `function_tool`, `handoff`
- [OpenAI Agents SDK: usage](https://openai.github.io/openai-agents-python/usage/): `context_wrapper.usage` and
  per-request entries
- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents): workflows
  and agents, and the patterns between them
- [A2A specification](https://a2a-protocol.org/latest/specification/): the agent card (section 4.4), tasks and
  messages; [A2A and MCP](https://a2a-protocol.org/latest/topics/a2a-and-mcp/): how the two protocols fit together
- [MCP specification: tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools): what a
  `tools/list` entry holds
- [CrewAI: agents](https://docs.crewai.com/en/concepts/agents), [tasks](https://docs.crewai.com/en/concepts/tasks)
  and [processes](https://docs.crewai.com/en/concepts/processes): `role`, `goal`, `backstory`, `Task`, sequential and
  hierarchical; [bonus lab B5](../bonus/B5_CrewAI_Crew/) runs the desk as a crew
- [Python `asyncio`: coroutines and tasks](https://docs.python.org/3/library/asyncio-task.html): `await`, `gather`

Next: [Lab 17: How to defend an agent from untrusted text](../17_Prompt_Injection/README.md). Back to [the lab list](../README.md).
