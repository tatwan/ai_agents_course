# Lab 10: How to draw, pause and resume an agent with LangGraph

**CPU | API key: `OPENAI_API_KEY` | Internet for the drawings | Practises: writing an agent as a graph; pausing a write for a person's decision and resuming it safely**

## Goal

Meet LangGraph on a pizza order, then put it to work at the Chinook support desk. The lab has two notebooks.

**Notebook 1** is a playground. We write a pizza order as a graph with no model in it: a state, three nodes and
the edges between them. Two nodes write to the same list of toppings and one wipes out the other's work, until a
reducer fixes it. A route sends big orders down another path, the program stops in the middle to ask the customer
a question, and it carries on when the answer comes. Then one node becomes a model call, and we find the same
kind of graph inside an agent made with `create_agent`.

**Notebook 2** takes LangGraph to the desk. We write the desk agent's loop as a graph ourselves and put a step of
our own inside it: a refund request stops in a `review` node until a person decides. Then we resume a thread
whose paused run is gone, as it would be after a restart. LangGraph raises no error. It starts a new run with no
request in it, and the model, given nothing to answer, makes something up. Reading what is waiting before a
resume, and keeping the threads in a file, prevents it.

## What you will learn

- How to write a program as a graph (a state, nodes that return updates, and edges), draw it, and watch it run
  step by step.
- Why a node's update replaces a value by default, and how a reducer lets several nodes add to the same list.
- How to choose the next node in our own code with a conditional edge.
- How to pause a run inside a node with `interrupt`, and resume it with `Command`, a checkpointer and a thread id.
- How the agent loop maps onto a graph, and how to put a review step of our own between the model and a write.
- What a resume does on a thread with nothing waiting, how to check `get_state(config).interrupts` first, and how
  to keep paused runs in a file with `SqliteSaver`.

## What you will do

### Notebook 1: meet LangGraph on a pizza order (`10a_meet_langgraph.ipynb`)

**Part A: Write a program as a graph with a state, nodes and edges.** Three plain functions run by hand, then the same
functions as a `StateGraph`, drawn, run with `invoke` and watched with `stream`.
**Part B: Merge two nodes' updates to one key with a reducer.** A second node returns toppings and the first
node's are gone; `Annotated[list, operator.add]` keeps both.
**Part C: Choose the next node with a route.** A conditional edge that refuses orders over 18 dollars.
**Part D: Pause in a node with `interrupt` and resume with `Command`.** The graph asks the customer first, with
and without a checkpointer, and carries on after a yes.
**Part E: Make one node a model call.** A model turns the customer's sentence into an order form, and the rest of
the graph stays plain Python.
**Part F: Find the same kind of graph inside `create_agent`.** The agent's `model` and `tools` nodes, its loop,
and a run watched step by step.
**Challenge.** Say no to a big order, and charge for delivery with a receipt.

### Notebook 2: LangGraph at the Chinook desk (`10b_langgraph_at_the_desk.ipynb`)

**Part A: Write the agent loop by hand, then as a graph.** Three database lookups, the loop in plain Python on
Helena Holý's question, then the same loop as a model node, a tools node, a route and a back edge.
**Part B: Pause a refund in a node of our own and wait for a person.** A write tool, a `review` node with
`interrupt`, a request that waits, and an approval.
**Part C: See what a resume does when the paused run is gone.** What the checkpointer keeps for a waiting thread,
a desk restarted with an empty memory, and a resume that starts a new run.
**Part D: Check what is waiting before resuming, and keep threads in a file.** `get_state(config).interrupts`
before every resume, and `SqliteSaver` so that a second graph object finds the waiting call.
**Challenge.** Reject a refund with a reason, and let small refunds through without a review.

![The desk agent as a graph. The state, a list of messages, enters at START and goes to the model node. A route reads the model's reply: a lookup goes to the tools node and back to the model, a refund request goes to the review node, and a reply with no tool request ends the run. In the review node the run stops and waits for a person; an approval sends it on to the tools node, a rejection back to the model. A checkpointer saves the state after every step, per thread id.](resources/desk_graph_with_review.png)

The dark box is the model's work, the lime boxes are our own Python, and the checkpointer is LangGraph's.

## Checkpoints

| After | You should see |
|---|---|
| Notebook 1, Part A | by hand and as a graph, one `ORDER PLACED` line and an order with five keys, `price` 11.0; the nodes `__start__`, `take_order`, `price`, `place_order`, `__end__`; three steps in the stream |
| Notebook 1, Part B | without a reducer the order is placed with `['mushrooms', 'olives']` only; with `Annotated[list, operator.add]` it is placed with all four toppings; 14.00 dollars both times |
| Notebook 1, Part C | `route` returns `place_order` for 12.50 and `refuse` for 20.00; two dotted arrows leave `price`; the party order ends with `not placed: over 18 dollars` and no `ORDER PLACED` line |
| Notebook 1, Part D | without a checkpointer the run stops at *This order comes to $20.00. Go ahead?* and a resume raises `Cannot use Command(resume=...) without checkpointer`; with `InMemorySaver`, `next` is `('ask_first',)`; after `Command(resume=True)`, one `ORDER PLACED` line with six toppings and `next` empty |
| Notebook 1, Part E | an `OrderForm` with the size `large` and the extras the sentence names (ours: four); the graph stops at the question and places the order after a yes; the model is called in `read_request` only |
| Notebook 1, Part F | a `CompiledStateGraph` with the nodes `__start__`, `model`, `tools`, `__end__`; `model` asks for `quote_price`, one `TOOL CALLED` line, `tools` returns 17.0, `model` answers |
| Notebook 2, Part A | Helena Holý is customer 6 (7 invoices, $49.62, support rep Steve Johnson) and Puja Srivastava is customer 59 (6 invoices, $36.64, support rep Jane Peacock); a first reply with empty `.text` and one tool call; `find_customer` first, then `get_invoices` and `get_support_rep`, then the answer; three model calls (ours: 166, 224 and 335 input tokens, 21, 52 and 25 output tokens); the same four nodes as `create_agent`'s graph |
| Notebook 2, Part B | a `review` node between `model` and `tools`; Puja's request waits on `file_refund_request` for invoice 284 and 8.91, `next` is `('review',)` and the table is empty; after `Command(resume="approve")`, one row |
| Notebook 2, Part C | Helena's request waits at `review` (ours: 4 messages, 5 checkpoints); on the restarted desk the resume raises no error, the thread starts with an `ai` message and has no `human` message, nothing in it is about Helena, and the table still has one row (ours: 15 messages, seven lookups of a made-up name) |
| Notebook 2, Part D | `❌ nothing is waiting on this thread: not resumed` and `None` on a desk with an empty memory; with `SqliteSaver`, a second graph object on the same file finds the call for invoice 393 and 1.98 waiting, and after the approval the table has two rows |
| Challenges | notebook 1: after `Command(resume=False)`, no `ORDER PLACED` line, `approved` `False` and no `status`; a medium placed at 16.50 with a two-line receipt, and a large that stops at 19.50. Notebook 2: a `tool` message starting *Not run. The reviewer rejected it:* and no row for invoice 229 (the solved file starts from an empty table, so there it stays empty); a refund of 1.98 filed without a stop, and one of 8.91 waiting at `review` |

**About the saved outputs.** They come from `gpt-6-luna`, the model `models.env` names. Parts A to D of notebook
1 call no model and print the same on every run. Elsewhere the model chooses its tool calls and writes its
replies on every run, so wording, reasons and token counts will differ on yours. Check the tool calls, the nodes
and the facts, not the words. Every refund request we sent stopped at `review` (17 of 17), and every approval
wrote its row. The resume on a lost thread started a new run without an error in all 41 runs we made. What the
model did next varied: in 38 it made up a customer name and looked it up, in 3 it asked what to look up, and in 17
of the 38 it reported a real customer's invoice figures under the made-up name. It never proposed a refund.

## When to use it

LangGraph suits a job where our code must control some of the steps: a rule that always holds, a step that waits
for a person, a run that has to continue after a restart. It gave this lab two things the ready-made loop does
not show: a node of our own inside the loop, and a checkpointer we could read. It has two costs. The agent took
about twenty lines where `create_agent` takes one, so write the graph by hand only when a step of your own is
needed. And a resume on a thread with nothing waiting does not fail, so every resume needs a check first.

## Before you start

- **Lab 00 first.** It checks the environment and that your key reaches the model.
- **Run it locally:** in the repository folder, `uv sync` (or `pip install -r requirements.txt`), put
  `OPENAI_API_KEY` in `.env` (copied from `.env.example`), then open a notebook from this folder in VS Code or
  JupyterLab (`uv run jupyter lab`) with the `.venv` kernel. Run the setup cell first. Each notebook runs on its
  own.
- **Internet for the drawings:** `draw_mermaid_png()` sends a graph's description (node names and arrows, none of
  our data) to [mermaid.ink](https://mermaid.ink) and gets a picture back. Without internet only the drawing
  cells fail; each notebook's Troubleshooting table shows how to print the same graph as text.
- **No kernel restart.** Notebook 2 imitates a restart with a new checkpointer object, so every cell runs top to
  bottom in one kernel.
- **Files it writes:** notebook 2 keeps its refund table in `10_LangGraph/outputs/refund_requests.db` and its
  checkpoints in `10_LangGraph/outputs/checkpoints.db`. Git ignores the `outputs/` folder.
- **Data:** `data/chinook.db`, the Chinook sample music shop, opened read-only.
- **Cost:** about 40 model calls in all, a fraction of one US cent. Parts A to D of notebook 1 call no model.

## Folder contents

| Path | What it is |
|---|---|
| `10a_meet_langgraph.ipynb` | notebook 1, the playground, with saved outputs |
| `10b_langgraph_at_the_desk.ipynb` | notebook 2, the Chinook desk, with saved outputs |
| `resources/desk_graph_with_review.png` and `.mmd` | the picture of the desk graph with its review step, and its source |
| `resources/resume_on_a_thread.png` and `.mmd` | the picture of what a resume does on a thread, and its source |
| `solved/10a_meet_langgraph_solution.ipynb` | notebook 1's challenge solved, run with its outputs |
| `solved/10b_langgraph_at_the_desk_solution.ipynb` | notebook 2's challenge solved, run with its outputs |

## Going further

- **A real restart.** Bonus lab B1 restarts the kernel, resumes a workflow from its checkpoint file, and shows
  what runs twice when a node has code before its `interrupt`.
- **LangGraph Studio.** `langgraph dev` starts a local server and a browser page that draws a graph and steps
  through a run. It needs the `langgraph-cli[inmem]` package and a LangSmith API key (a free account), which this
  repository does not install or ask for, so the lab draws its graphs in the notebook.

## Resources

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview): what LangGraph is for
- [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api): state, reducers, nodes, edges,
  conditional edges and `Command`
- [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts): `interrupt`, `Command(resume=...)` and
  the rules for code around an interrupt
- [Checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers): `InMemorySaver`, `SqliteSaver`, threads,
  `get_state` and `get_state_history`
- [Streaming](https://docs.langchain.com/oss/python/langgraph/streaming): `stream` and its modes
- [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents): `create_agent`, the ready-made loop
- [LangChain human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop):
  `HumanInTheLoopMiddleware`, the ready-made review step
- [Run a local server](https://docs.langchain.com/oss/python/langgraph/local-server): `langgraph dev` and Studio

Back: [Lab 09: How to build an agent from LangChain's pieces](../09_LangChain/README.md). Next: [Lab 11: How to choose an agent framework](../11_Choose_A_Framework/README.md). Back to [the lab list](../README.md).
