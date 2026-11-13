![AI Agents in Practice Banner](images/ai_agents.png)

# AI Agents in Practice

Hands-on labs for building, running and judging AI agents. You start with one call to a model and write the agent
loop yourself, then see the same pieces inside the OpenAI Agents SDK, Google ADK, LangChain and LangGraph, LlamaIndex and
other frameworks. Then you ground an agent in a database and a document collection, run the code it writes safely, choose
between one agent and several, defend it from untrusted text, and evaluate, trace and cost it.

Every lab works on one running case: the support desk of the Chinook music shop, with its customer database
(`data/chinook.db`) and its policies and tickets (`data/corpus/`). Each lab stands alone: you can open any lab without
running the ones before it.

## Who it is for

Technical people who already write Python: developers, data scientists, technical managers. You do not need prior
agent experience. Many people who build agents have to explain them to a risk or compliance function, so the labs
treat cost, permissions and failure as part of the lesson.

## The labs

Start with Lab 00: it sets up the environment and checks that everything later labs need works.

**Part A: an agent with no framework**

| Lab | Title |
|---|---|
| 00 | [How to set up the lab environment](00_Environment_Check/) |
| 01 | [How to call a model and read the response](01_Model_Call/) |
| 02 | [How a model asks for a tool](02_Tool_Calling/) |
| 03 | [How to write the agent loop](03_Agent_Loop/) |
| 04 | [What is an agent](04_What_Is_An_Agent/) |
| 05 | [How to manage what an agent sees](05_Context_And_Skills/) |
| 06 | [How to share tools with MCP](06_MCP/) |

**Part B: frameworks and retrieval**

| Lab | Title |
|---|---|
| 07 | [How the OpenAI Agents SDK runs your loop](07_OpenAI_Agents_SDK/) |
| 08 | [How to build and run an agent with Google ADK](08_Google_ADK/) |
| 09 | [How to build an agent from LangChain's pieces](09_LangChain/) |
| 10 | [How to draw, pause and resume an agent with LangGraph](10_LangGraph/) |
| 11 | [How to choose an agent framework (a guide)](11_Choose_A_Framework/) |
| 12 | [How to answer from documents with retrieval](12_Retrieval/) |
| 13 | [How to give an agent a search tool](13_Agentic_RAG/) |
| 14 | [How to search your documents with LlamaIndex](14_LlamaIndex_RAG/) |

**Part C: business agents**

| Lab | Title |
|---|---|
| 15 | [How to build a customer-support agent over a database](15_Support_Desk_Agent/) |
| 16 | [How a coding agent edits files and runs tests](16_Coding_Agent/) |
| 17 | [How to run model-written code safely](17_Code_Execution/) |

**Part D: designs and production**

| Lab | Title |
|---|---|
| 18 | [How to choose an agent design](18_Agent_Designs/) |
| 19 | [How to defend an agent from untrusted text](19_Prompt_Injection/) |
| 20 | [How to evaluate and trace an agent](20_Evals_And_Tracing/) |
| 21 | [How to call any model through one interface with LiteLLM](21_LiteLLM/) |
| 22 | [How to re-engineer a process with agents](22_Process_Reengineering/) |
| 23 | [What agent platforms sell (a guide)](23_Agent_Platforms/) |

**Bonus labs**

| Lab | Title |
|---|---|
| B1 | [How to make a LangGraph workflow survive a restart](bonus/B1_LangGraph_Durable_Workflows/) |
| B2 | [How to put guardrails and approvals on an Agents SDK agent](bonus/B2_Agents_SDK_Guardrails/) |
| B3 | [How to build a typed agent with Pydantic AI](bonus/B3_PydanticAI_Typed_Agent/) |
| B4 | [How to build a crew with CrewAI](bonus/B4_CrewAI_Crew/) |
| B5 | [How to build an agent and a workflow with Microsoft Agent Framework](bonus/B5_Microsoft_Agent_Framework/) |
| B6 | [How to move retrieval to Pinecone](bonus/B6_Pinecone_Retrieval/) (requires a Pinecone account) |
| B7 | [How to trace and evaluate an agent with LangSmith](bonus/B7_LangSmith_Tracing_And_Evals/) (requires a LangSmith account) |

## What a lab folder holds

Most labs have two guided notebooks (an **a** playground notebook that meets the idea on an everyday problem, and a **b** notebook that puts it to work at the Chinook support desk) and their solved challenge notebooks in `solved/`:

```text
NN_Topic/
  README.md                   the goal, what you will learn, the parts and the checkpoints
  NNa_meet_topic.ipynb        the playground notebook
  NNb_topic_at_the_desk.ipynb the support desk notebook
  resources/                  diagrams and any data the lab adds
  solved/
    NNa_meet_topic_solution.ipynb
    NNb_topic_at_the_desk_solution.ipynb
```

Single-notebook labs (`00`, `01`, `04`, `16`, `22`) hold one `NN_topic.ipynb` notebook and `solved/NN_topic_solution.ipynb`. Labs 11 and 23 are reading guides (`GUIDE.md` and `solved/NN_solution.md`).

Every notebook is saved with the outputs of a real run, so you can read a lab before you run it. The README of each
lab names the model behind its saved outputs.

## Setup

Start with [Lab 00: How to set up the lab environment](00_Environment_Check/README.md). It walks through every route
and ends with a notebook that checks everything in one run.

- **Ubuntu VM with VS Code:** `git clone https://github.com/tatwan/ai_agents_course.git`, install
  [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`), then run
  `uv sync --python 3.13` in the repository folder. Optionally `sudo apt install -y graphviz` for lab 07's drawings.
- **GitHub Codespaces:** **Code → Codespaces → Create codespace on main**, then the same `uv` steps. The key can be a
  Codespaces secret named `OPENAI_API_KEY`.
- **Your own machine with `uv`:** clone the repository (or download the ZIP), install `uv`, run
  `uv sync --python 3.13`.
- **Your own machine with `pip`** (where `uv` is blocked): Python 3.11 to 3.14, `python3.13 -m venv .venv`, activate
  it, `pip install -r requirements.txt`.

Then copy `.env.example` to `.env` and paste your `OPENAI_API_KEY` into it. Model names and prices live in
`models.env`: change `MODEL_DEFAULT` there to switch every lab, or set it in `.env` for your machine only. A model
without a reasoning setting (such as `gpt-4o-mini`) also needs `REASONING_EFFORT=` empty in `models.env` itself: an
empty value in `.env` does not replace a setting. Open a
notebook in VS Code and choose the repository's `.venv` as the kernel (or run `uv run jupyter lab`). Notebooks never
install packages, and never print the key.

Labs 08, B4 and B5 have their own environment: run `uv sync --python 3.13` inside the lab folder and choose that folder's
`.venv`. Graphviz (the drawings in labs 07 and 18), Docker (the optional last part of lab 17), Node.js 22.19 or newer (lab 06's MCP Inspector), a
`GEMINI_API_KEY` (the optional cells of labs 07, 08, 09 and 21) and the Pinecone and LangSmith keys (bonus B6 and
B7) are optional.

## Data

Instructor-supplied; do not regenerate these files. See [data/README.md](data/README.md).

| Path | What it holds |
|---|---|
| `data/chinook.db` | The Chinook shop's database: customers, invoices, tracks and the support reps |
| `data/corpus/` | The shop's 20 policies and 16 support tickets, as markdown files |
| `data/documents/` | A reference guide to AI governance frameworks (PDF), read by lab 07's file search |
