# Bonus B5: How to build an agent and a workflow with Microsoft Agent Framework

**CPU | API key: `OPENAI_API_KEY` | Own environment | Practises: building an agent in a framework; setting the path in code so that a person must approve; keeping a waiting step across a restart**

## Goal

Meet Microsoft Agent Framework on an everyday request, then put it to work at the Chinook support desk. The
framework has two ways to run work: an **agent**, where a model chooses the next step, and a **workflow**, where
our code fixes the steps and the edges between them. The lab has two notebooks.

**Notebook 1** is a playground with a leave request. Sara asks for three days off, a step asks her manager and
waits, and only a yes books the days. The framework saves the waiting question in a checkpoint file. We answer that
one saved question twice, count the bookings, and then make the booking safe to repeat. In the last part an agent
writes the note to the manager as the first step, and the edges still send every request to the manager before anything is booked.

**Notebook 2** takes the same framework to the desk. A desk agent looks up a customer's facts. Asked for a refund,
it can only ask: a workflow reads the invoice, waits for a reviewer, and writes the refund. The reviewer answers
from a new Python process that is given only a checkpoint id, and we read the refunds table after one approval and
after a second.

## What you will learn

- How to write a workflow step, join steps with edges, run the workflow and read its events.
- How a step asks a person a question and waits, and how our code sends the answer back.
- How to save a waiting workflow in a checkpoint file, read the file, and continue from it with new objects and
  from a new process.
- Why answering one checkpoint twice repeats the write, and how to make the write safe to repeat.
- How to build an `Agent` with tools, read which tools a run called, and keep a conversation with a session.
- How to give an agent a tool that starts a workflow, so that a model can ask for an action and cannot skip its
  review.

## What you will do

### Notebook 1: meet the framework on a leave request (`b5a_meet_agent_framework.ipynb`)

**Part A: Write one step and run it as a workflow.** The request, a step that books the days, the workflow built
and run, its events read one by one.
**Part B: Add a step that asks a person and waits.** `request_info` and `@response_handler`, an edge, the workflow
printed as diagram text, the waiting question read, the answer sent.
**Part C: Save the waiting question in a checkpoint file.** `FileCheckpointStorage`, the file opened, the workflow
built again and continued from the checkpoint id.
**Part D: Answer one checkpoint twice, and make the booking safe to repeat.** The same answer sent again, the
calendar counted, the bookings keyed by request.
**Part E: Let an agent write the note, and keep the edges in our code.** The model client called once, a tool, an
`Agent`, its messages read, and the agent as the first step of the workflow.
**Challenge.** A manager who says no, and a step that stops a request before anyone is asked.

### Notebook 2: Agent Framework at the Chinook support desk (`b5b_agent_framework_at_the_desk.ipynb`)

**Part A: Build the desk agent from three database lookups.** The lookups called by hand, the agent, and the tools
its run called.
**Part B: Keep a follow-up question in the same conversation with a session.** A follow-up without and with a
session, and what the session holds.
**Part C: Read the refund workflow and run it by hand.** `refund_workflow.py` read step by step, an invoice that
does not exist, and a real one that stops at the reviewer.
**Part D: Give the agent a tool that asks for a refund.** A tool that starts the workflow, and a rep who tries to
skip the review.
**Part E: Answer the review from a new Python process.** `resume_refund.py` started as its own process, the refunds
table read, and the same answer sent a second time.
**Challenge.** Reject a refund, and ask twice for the same invoice.

![The desk agent asks for a refund through the request_refund tool. The workflow's first step reads the invoice and the review step asks and waits; the question is saved in a checkpoint file. A new Python process, given the checkpoint id, builds the review step again from the file, takes the reviewer's answer, and on approve the file_refund step writes one row per invoice to the refunds table.](resources/labB5_refund_desk.png)

The dark box is where a model chooses the next step. Light green boxes are steps where our code decides. White
shapes are people, files and tables.

## Checkpoints

| After | You should see |
|---|---|
| Notebook 1, Part A | one `STEP RAN: book_days` line; five events, three of them for `book_days`; the output `Booked 3 days for Sara.`; one entry in `BOOKED` |
| Notebook 1, Part B | two boxes and one arrow in the diagram text; the first run prints only `ask_manager asks`, ends in `IDLE_WITH_PENDING_REQUESTS` and books nothing; one question waiting, asked by `ask_manager`; after the answer `True`, one entry in `BOOKED` |
| Notebook 1, Part C | two checkpoint files; ours has `workflow_name` `leave`, `iteration_count` 1 and one waiting question; a new workflow finds the same question from the checkpoint id, with no `STEP RAN` line; one entry after the answer |
| Notebook 1, Part D | the same checkpoint answered again: 2 entries for `leave-1`; with the bookings keyed by `id`, two answers give 1 booking and the second output says `already booked` |
| Notebook 1, Part E | with no tool the model says it does not have Sara's days; the agent prints `TOOL CALLED: days_left(Sara)` and writes 12 days; Omar's request stops at `ask_manager` with a note that has his 4 days; `leave-2` is booked only after the answer `True` |
| Notebook 2, Part A | customer 59, 6 invoices, $36.64, Jane Peacock, and `No match` for the misspelt name; the agent gives the same three facts after `find_customer`, `get_invoices` and `get_support_rep` (ours: 906 input tokens) |
| Notebook 2, Part B | without a session the follow-up is answered with a question about who is meant; with one, Jane Peacock; the session's state is empty and its id starts with `resp_` |
| Notebook 2, Part C | invoice 9284: `No match for invoice 9284. Nothing to refund.` and the state `IDLE`; invoice 284: a question from `review` with `{'invoice_id': 284, 'customer_id': 59, 'amount': 8.91}` and an empty refunds table |
| Notebook 2, Part D | `request_refund({"invoice_id":284})` among the tool calls; a reply that says the refund is waiting for a reviewer; the refunds table `[]`; one checkpoint id waiting |
| Notebook 2, Part E | a process id different from the notebook's; one review waiting; `Refund for invoice 284 written.` and the table `[(284, 59, 8.91)]`; on the second run `already on file` and the same one row |
| Challenges | notebook 1: `Not approved. Nothing booked for Sara.` and no booking; `Not enough days: Omar asks for 6 and has 4 left.` with no question waiting. Notebook 2: `Refund for invoice 229 rejected. Nothing written.` for $13.86; a second review for invoice 284, then `already on file` and one row |

**About the saved outputs.** They come from `gpt-6-luna`, the model `models.env` names. The model chooses its tool
calls and writes its replies on every run, so wording and token counts will differ on yours; ids, process ids and
checkpoint file names are new on every run. Check the steps that ran, the tool calls and the tables, not the words.
Everything a workflow does here is our code and repeats exactly: the double booking, the single row and the waiting
review come out the same on every run. The model's part was steady too. Asked for the note with no tool, it said it
did not have Sara's days in 10 of 10 runs and never invented a number; with the tool it wrote 12 days in 10 of 10.
At the desk it gave Puja's three facts in 10 of 10 runs, asked who was meant in 5 of 5 follow-ups without a session
and answered Jane Peacock in 5 of 5 with one. Asked for the refund, it called `request_refund` for invoice 284 in 20
of 20 runs, ten of them with the rep's "skip the review" message, and the refunds table stayed empty every time. In
the saved run of notebook 1, the note about Omar repeats his comment as a fact ("his manager has approved"); yours
may word it differently.

## When to use it

Microsoft Agent Framework suits a team that wants an agent and a workflow from one library: a model that chooses
its tools where the path depends on what it finds, and steps with fixed edges where a rule decides the path, with a
question to a person that can wait in a file. Microsoft describes it as the next generation of its two earlier agent libraries,
AutoGen and Semantic Kernel, and publishes a migration guide from each, so it is the natural move for a team with
code on either. It also connects to Azure services, none of which this lab needs. Its
cost here: it needs an environment of its own, and a checkpoint that is answered twice writes twice, so the write
has to carry its own key.

## Before you start

- **Lab 00 first.** It checks the repository, Python, `uv` and that your key in `.env` reaches the model.
- **This lab has its own environment,** because the framework pins other versions of some packages than the core
  labs use. From the repository folder:

  ```bash
  cd bonus/B5_Microsoft_Agent_Framework
  uv sync --locked --python 3.13
  ```

  With pip, create and activate a virtual environment in this folder and run `pip install -r requirements.txt`.
  Then open a notebook in VS Code or JupyterLab and select this folder's `.venv` as the kernel. Each notebook runs on
  its own.
- **Key:** `OPENAI_API_KEY` in `.env` at the repository folder (copied from `.env.example`). No Microsoft or Azure
  account is needed, and the lab signs in nowhere. Parts A to D of notebook 1 call no model.
- **What leaves your machine:** the model requests to OpenAI, and nothing else. The framework adds its name and
  version to the `User-Agent` header of those requests; set the environment variable
  `AGENT_FRAMEWORK_USER_AGENT_DISABLED=true` before starting Jupyter to leave that out. It records traces with
  OpenTelemetry only when you set up an exporter, and this lab sets up none. In notebook 2, Part B, the session's
  conversation is stored on OpenAI's side.
- **Files it writes:** checkpoint files and one small SQLite file under this folder's `outputs/`, which git ignores.
  Notebook 1 empties its folder there in Part C, and notebook 2 in Parts C and D, so each run of a notebook starts
  clean.
- **Data:** `data/chinook.db`, the Chinook sample music shop, opened read-only. The refunds are written to the lab's
  own table and never to the shop's database.
- **Cost:** about 20 model calls in the two notebooks, a fraction of a US cent.

## Folder contents

| Path | What it is |
|---|---|
| `b5a_meet_agent_framework.ipynb` | notebook 1, the playground, with saved outputs |
| `b5b_agent_framework_at_the_desk.ipynb` | notebook 2, the Chinook desk, with saved outputs |
| `refund_workflow.py` | the desk's refund workflow: three steps, two edges, and the function that builds it; read in notebook 2, Part C |
| `resume_refund.py` | answers a waiting review from a new Python process; read and run in notebook 2, Part E |
| `resources/labB5_leave_workflow.png` and `.mmd` | the picture of the leave workflow, and its source |
| `resources/labB5_refund_desk.png` and `.mmd` | the picture of the desk agent and the refund workflow, and its source |
| `solved/b5a_meet_agent_framework_solution.ipynb` | notebook 1's challenge solved, run with its outputs |
| `solved/b5b_agent_framework_at_the_desk_solution.ipynb` | notebook 2's challenge solved, run with its outputs |
| `pyproject.toml`, `uv.lock`, `requirements.txt` | this lab's own environment |

## Resources

- [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/): the documentation's home
- [Overview](https://learn.microsoft.com/en-us/agent-framework/overview/): what the framework is, and how it relates
  to AutoGen and Semantic Kernel
- [Agents](https://learn.microsoft.com/en-us/agent-framework/agents/): `Agent` and its tools
- [Sessions](https://learn.microsoft.com/en-us/agent-framework/concepts/agents/conversations/session):
  `create_session` and what a session stores
- [OpenAI with Agent Framework](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/model-providers/openai):
  the OpenAI clients
- [Workflows](https://learn.microsoft.com/en-us/agent-framework/workflows/): executors, edges, events
- [Human-in-the-loop in workflows](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop):
  `request_info` and `@response_handler`
- [Checkpoints](https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints): checkpoint storage and
  continuing from a checkpoint
- [Workflow visualization](https://learn.microsoft.com/en-us/agent-framework/workflows/visualization): `WorkflowViz`
- [DevUI](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/devui/): the developer
  page. Its package, `agent-framework-devui`, is a pre-release that is installed with `agent-framework`; the lab does not use it.

Back to [the bonus lab list](../README.md) or [the full lab list](../../README.md).
