# AI Agents in Practice

A two-day workshop on building, running, and judging AI agents: **Foundations, Frameworks, Protocols & Production**.

You leave able to explain what an agent is, when it should not be one, how the loop actually works, and what each later layer is for — tools, context, MCP, async, a modern SDK, a graph, a sandbox, retrieval, security, and cost.

## Who it is for

Technical people who already write Python: developers, data scientists, technical managers. You do not need prior agent experience. About half the room will have to justify this work to a risk or compliance function, so the notebooks treat cost, permissions, and failure modes as part of the lesson, not an appendix.

The designed room is about twenty people on Linux VMs with VS Code and Jupyter. The same repo works on a laptop.

## How a module works

There is one shape. There is no code-along.

1. The instructor talks (slides and the idea).
2. The instructor drives `notebook.ipynb`. Students watch.
3. Students run **the same notebook** at their own pace.
4. A challenge at the end, attempted alone. Acceptance criteria and an assert live in the notebook. The answer does not.
5. The instructor debriefs with `solution.ipynb`.

Each notebook is a short chapter: **Learn**, **Do**, **Observe**, **Challenge**. It is complete on its own. You can skip a module and still open the next one. You can open a notebook later and get the explanation without having typed along.

## Setup

You need Python 3.11+, [uv](https://docs.astral.sh/uv/), and an OpenAI API key (issued for the class, or your own for self-study).

```bash
cp .env.example .env
# put OPENAI_API_KEY in .env

uv venv
uv sync
uv run jupyter lab
```

Start Jupyter from this directory. Notebooks look upward for `.env` if you opened the module folder.

Do not install packages from inside a notebook. Do not print `.env`.

Model names come from `.env` (`MODEL_DEFAULT`, `MODEL_STRONG`). Cells do not hard-code them. This model family uses `max_completion_tokens` and `reasoning_effort="none"`. Do not pass `temperature`.

## The two days

**Day 1** is the loop, from a single API call to a graph.

**Day 2** is what happens when that loop meets a database, a sandbox, a corpus, other agents, and a risk function.

| # | Module | What you actually do |
|---|---|---|
| 00 | The OpenAI API, once | One call. Walk the response object. Stream. See what the same call costs at app scale. |
| 01 | What an agent is | Chatbot vs workflow vs agent. When an agent is the wrong default. |
| 02 | Tool calling | The model does not call the tool. It emits a name and a JSON string. Your code decides. |
| 03 | The ReAct loop | Think out loud, then act. Then the silent official loop you will keep. |
| 04 | A coding agent | Five file tools, a jail that refuses `../.env`, then break the agent. |
| 05 | Context engineering | The message list is a budget. A short map vs stuffing every playbook. |
| 06 | MCP | The same two travel tools, in another process. See the wire, then let a host you did not write consume the server. |
| 07 | Async | `def` to `async def` to `gather`, then two independent tool calls at once. |
| 08 | OpenAI Agents SDK | One Chinook shop, two specialists, three wirings: your code, agents as tools, handoffs. |
| 09 | LangGraph | The same desk. You draw the arrows. Pause and resume. |
| 10 | Charting and the sandbox | The model writes matplotlib. A timeout is not a sandbox. Get a PNG. |
| 11 | Retrieval | Local Chroma over a policy corpus. One retrieve, one generate. Two questions have no answer. |
| 12 | Agentic RAG | Retrieve is a tool. The loop may search twice. |
| 13 | Delegation | One agent with three tools vs overlapping specialists. CrewAI is a page, not an install. |
| 14 | Security | Indirect injection through a retrieved ticket. A Python scan before generate. |
| 15 | Evals, traces, cost | A ledger per turn, the message list as a trace, a checker against named facts. |
| 16 | Azure Foundry | The managed path, instructor-provisioned. *(Not in the repo yet.)* |
| 17 | Process re-engineering | When this should not be an agent. *(Not in the repo yet.)* |

Modules 00–15 are in `modules/`. 16–17 are being written.

CrewAI and LlamaIndex are not installed and are not modules. They appear as names on the framework ladder, and as a short concept discussion in 13. The comparison the course actually runs is: no framework, then the OpenAI Agents SDK, then LangGraph, on the same Chinook desk.

## What each module folder contains

```
modules/NN_name/
  notebook.ipynb    # driven at the front, then run by you
  solution.ipynb    # debrief only; run it in the same kernel
```

A `.py` file appears only when something must be its own process: the MCP server in 06, the sandbox runner in 10.

## Data

Instructor-supplied. Do not regenerate these files. See [data/README.md](data/README.md).

| File | Used in |
|---|---|
| `data/fun_facts.csv`, `data/flight_data.csv` | 02, 03, 05, 06, 07 |
| `data/chinook.db` | 08, 09, 10, 13, 15 |
| `data/corpus/` | 11, 12, 14 |

## Requirements

| | |
|---|---|
| LLM | OpenAI. Shared class key in the room. |
| Vector store (later) | Chroma, local. No per-student signup. |
| Cloud | Azure only, and only in module 16 plus optional instructor demos. No Azure credential is required for 00–10. |
| Optional | The `dot` binary (graphviz) so `draw_graph` renders in 02, 03, 06, and 08. Without it, those cells print an exception and continue. |
| Optional | Docker, with `python:3.12-slim` pre-pulled, for the container cell in module 10. The rest of that module runs without it. |

## Repository layout

```
README.md                 # you are here
.env.example
pyproject.toml
data/                     # CSVs, Chinook, corpus
modules/                  # 00–15 (16–17 not started)
```
