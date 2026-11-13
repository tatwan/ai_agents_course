# Bonus B1: How to make a LangGraph workflow survive a restart

**CPU | No API key or account | Internet for two drawings | One kernel restart in each notebook | Practises: keeping a job that waits for a person across a restart, and making its steps safe to run twice**

## Goal

Keep a job that waits for a person in a file, switch Python off, and carry on from the file. The lab has two
notebooks, and neither calls a model.

**Notebook 1** is a playground. A school-trip permission slip goes home on Friday and the parent answers on
Monday. We write the job as a small LangGraph graph, pause it, and open the checkpoint file it is kept in as an
ordinary SQLite file. Then we restart the kernel, find the slip still waiting and send the answer. The job
finishes, and one line of it has run twice. We read why from the file, and change the graph.

**Notebook 2** takes the same idea to the Chinook support desk. A refund request is looked up in the shop's
database and waits for a reviewer through a real restart. After the approval the request is filed once, and
the desk's own tables show that the review node was entered twice. We make the write that sits before the pause
safe to repeat.

## What you will learn

- How to write a job that waits for a person as a LangGraph graph: a state, nodes, edges and `interrupt`.
- How to keep a paused run in a file with `SqliteSaver`, and read that file with plain `sqlite3`.
- How to build the graph again in a new Python process, read what is waiting, and resume it.
- Why the code before `interrupt` runs again on a resume, and how to tell from the tables a workflow writes to.
- Three ways to keep a write from happening twice: move it to a node of its own, move it below the
  `interrupt`, or make it safe to repeat.

## What you will do

### Notebook 1: meet the checkpoint file on a permission slip (`b1a_meet_durable_workflows.ipynb`)

**Part A: Write a job that waits for a person as a graph.** A slip as a dictionary, two nodes (one of them stops
at `interrupt`), the wiring, and the graph drawn.
**Part B: Pause the run and keep it in a file.** `SqliteSaver`, a thread id, a run that stops at the question
for the parent.
**Part C: Read the checkpoint file as an ordinary SQLite file.** Its two tables, the checkpoints of the thread,
and the child's name in the saved bytes.
**Part D: Restart the kernel and resume from the file.** The graph built again in a new process, the waiting
slip read from the file, the answer sent, and the line that ran a second time.
**Part E: Keep work that must happen once in a node of its own.** The node split in two, a second slip, and the
thread's checkpoints read in order.
**Challenge.** Show that the restart is not the cause of the second slip, and answer a slip with no.

### Notebook 2: a refund that waits at the Chinook desk (`b1b_durable_workflows_at_the_desk.ipynb`)

**Part A: Read the refund workflow one node at a time.** The workflow in `refund_workflow.py`: its state, the
invoice lookup called by hand, the review node, the filing node, the routes, and the graph drawn.
**Part B: Start a refund and leave it waiting in a file.** Puja Srivastava's request stops at `review`, with one
notice sent and nothing filed.
**Part C: Restart the kernel and approve the waiting refund.** The workflow built again from the file, the
request read from the checkpoint file, the approval, and the desk's tables afterwards.
**Part D: Make the write before the pause safe to repeat.** A review node that asks the notices table first, and
a second request that is announced once.
**Challenge.** Give the notice a node of its own, and reject a request.

![The permission slip's run on two days. On Friday the node ask_parent starts at its first line, prints SLIP SENT HOME and stops at interrupt. The checkpoint file keeps the state, the next node and the question. On Monday a new process reads the file and runs ask_parent again from its first line, so SLIP SENT HOME is printed a second time; interrupt then returns the answer and book_seat runs.](resources/what_a_resume_runs.png)

The lime boxes are the line before `interrupt`, which runs on both days. The white boxes are the other steps of
the run and the checkpoint file.

## Checkpoints

| After | You should see |
|---|---|
| Notebook 1, Part A | `book_seat` called by hand prints `SEAT BOOKED for Maya` and returns `{}`; the nodes `ask_parent` and `book_seat`, drawn in one line |
| Notebook 1, Part B | one `SLIP SENT HOME with Maya` line, the question *May Maya go to the science museum?*, `next node: ('ask_parent',)` |
| Notebook 1, Part C | the tables `checkpoints` and `writes`; two checkpoints for `slip-maya` (steps -1 and 0); four rows in `writes`, with `b'\xa4Maya'` under `child` and the question inside the bytes of `__interrupt__` |
| Notebook 1, Part D | after the restart the slip is still waiting at `ask_parent`; the resume prints `SLIP SENT HOME with Maya` a second time, then `SEAT BOOKED for Maya`, and returns `allowed: True` |
| Notebook 1, Part E | `SLIP SENT HOME with Leo` once; the resume prints only `SEAT BOOKED for Leo`; five checkpoints, and step 1 has `next: ('wait_for_parent',)` |
| Notebook 2, Part A | invoice 284 belongs to Puja Srivastava, total 8.91; invoice 9999 gives *not filed: no match for invoice 9999*; the nodes `look_up_invoice`, `review` and `file_request` |
| Notebook 2, Part B | `LOOKED UP invoice 284` and `NOTICE SENT to the reviewer for R-1001`; `next node: ('review',)`; one notice, no refund request; three checkpoints (steps -1, 0 and 1) |
| Notebook 2, Part C | after the restart `R-1001` is still waiting at `review`; the approval prints `NOTICE SENT` and `REFUND REQUEST FILED` and no `LOOKED UP` line; two notices for `R-1001`, one refund request (invoice 284, 8.91) |
| Notebook 2, Part D | Helena Holý's request `R-1002` (invoice 393, 1.98): the approval prints `NOTICE ALREADY SENT for R-1002 (not sent again)`; `notices` holds `R-1001` twice and `R-1002` once; two refund requests |
| Challenges | notebook 1: `SLIP SENT HOME with Sam` twice with no restart; `NO SEAT for Noor` and `allowed: False` after one slip. Notebook 2: one notice for `R-1003` and its request filed; `R-1004` ends *not filed: the reviewer said:* with your reason and no row in `refund_requests` |

**About the saved outputs.** No model ran: every line comes from our own Python and from LangGraph, and a run on
your machine prints the same. Two things differ from run to run and are not
shown as checkpoints: the size in bytes of a saved state, and the id inside the bytes of `__interrupt__`. The
outputs after each restart come from a second kernel, which is why the cell numbers start again at 1 there.

## When to use it

A checkpointer in a file or a database suits a job whose steps we know and that has to wait: for a reviewer, a
customer, another system. The wait can then outlast the program. In this lab a slip waited through a kernel
restart, and a refund request was approved from a new Python process that had not started it.

It has a cost that is easy to miss, because nothing fails. A resume runs the waiting node again from its first
line, so whatever sits before the `interrupt` happens twice: the reviewer got two notices for one request. Every
node that waits needs its earlier lines moved to a node of their own, moved below the `interrupt`, or made safe
to repeat. A job that never waits needs no checkpointer at all, and can stay plain Python.

## Before you start

- **Run it locally:** in the repository folder, `uv sync` (or `pip install -r requirements.txt`), then open a
  notebook from this folder in VS Code or JupyterLab (`uv run jupyter lab`) with the `.venv` kernel. No key is
  needed. Each notebook runs on its own.
- **One kernel restart in each notebook.** Run the cells one at a time, in order. Notebook 1 asks for the
  restart in Part D and notebook 2 in Part C; then carry on from the next cell. **Run All** stops at the restart
  with the message `Restart the kernel first, then run this cell.` The two solution notebooks need no restart.
- **Internet for the drawings:** `draw_mermaid_png()` sends a graph's description (node names and arrows, none
  of our data) to [mermaid.ink](https://mermaid.ink) and gets a picture back. Without internet only that one
  cell in each notebook fails; the Troubleshooting table in each notebook shows how to print the same graph as
  text.
- **Files it writes:** each notebook keeps its checkpoint file in `outputs/` in this folder (`trip.db` for
  notebook 1; `checkpoints.db` and the desk's tables in `desk.db` for notebook 2). The solutions write to
  `solved/outputs/`. Git ignores both folders, and Part B of each notebook deletes its own files before it starts
  a run.
- **Data:** notebook 2 reads `data/chinook.db`, the Chinook sample music shop, opened read-only.
- **Cost:** none. No model is called.
- **Where the ideas start:** [Lab 10](../../10_LangGraph/README.md) builds a graph, `interrupt` and a
  checkpointer from the beginning. This lab restates what it uses in a sentence each.

## Folder contents

| Path | What it is |
|---|---|
| `b1a_meet_durable_workflows.ipynb` | notebook 1, the playground, with saved outputs |
| `b1b_durable_workflows_at_the_desk.ipynb` | notebook 2, the Chinook desk, with saved outputs |
| `refund_workflow.py` | the desk's refund workflow, which notebook 2 imports before and after its restart |
| `resources/what_a_resume_runs.png` and `.mmd` | the picture of a run on two days, and its source |
| `resources/refund_workflow_and_its_files.png` and `.mmd` | the picture of the refund workflow and the files it touches, and its source |
| `solved/b1a_meet_durable_workflows_solution.ipynb` | notebook 1's challenge solved, run with its outputs |
| `solved/b1b_durable_workflows_at_the_desk_solution.ipynb` | notebook 2's challenge solved, run with its outputs |

## Going further

- **Go back in a thread.** `get_state_history(config)` returns every checkpoint of a thread, and `update_state`
  starts a new branch from an earlier one.
- **How soon a checkpoint is written.** `invoke(..., durability="sync")` writes every checkpoint before the next
  step starts; the default writes while the next step runs.
- **Another database.** `PostgresSaver`, in the package `langgraph-checkpoint-postgres`, keeps checkpoints in a
  database server for a program that runs on several machines.

## Resources

- [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts): `interrupt`, `Command(resume=...)`,
  and the rule that work before an interrupt must be safe to repeat
- [Checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers): `SqliteSaver`, `PostgresSaver`,
  threads, `get_state`, `get_state_history`, durability modes and encryption
- [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api): state, nodes, edges and conditional
  edges
- [Time travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel): going back to an earlier
  checkpoint and branching from it
- [Python `sqlite3`](https://docs.python.org/3/library/sqlite3.html): the module both notebooks open their files
  with

Back to [the bonus lab list](../README.md).
