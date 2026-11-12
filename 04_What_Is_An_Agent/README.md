# Lab 04: What is an agent

**CPU | API key: `OPENAI_API_KEY` | Practises: telling a chatbot, a workflow and an agent apart; choosing how far an agent may act, and when not to use one**

## Goal

Ask one everyday question three ways, to a chatbot, a workflow and an agent, and see that they differ in one thing:
**who decides the next step**. That test gives us the definition of an agent. Then the same three shapes answer a
question at the Chinook music shop's support desk. The chatbot answers about a customer at once, fluently, with
nothing looked up, and only the database can say which parts of its answer are true. The agent then answers a
question nobody wrote steps for. The lab ends by deciding how far an agent should be allowed to act on its own.

The lab is one notebook: a playground on a two-order shop, then the desk.

## What you will learn

- How to tell a chatbot, a workflow and an agent apart by asking who decides the next step.
- How to write a workflow (fixed steps in our code; ours makes no model call), and what it does with a question it
  was not written for.
- How a small agent works: the model asks for a lookup, our code runs it, the model answers from the result.
- The definition of an agent, and where its six parts are in code we have just run.
- Why an answer the model writes with nothing looked up is no evidence, even when part of it is right.
- How to choose an autonomy level (suggest, draft, act with audit, act) for a job, and when not to use an agent.

## What you will do

The notebook is `04_what_is_an_agent.ipynb`.

**Part A: Ask a chatbot about an order it cannot see.** *What is the status of order B22?* sent to the model in one
call with no tools, while the shop's two orders sit in a Python dictionary the model never sees.
**Part B: Answer the same question with a workflow.** Three fixed steps in our code and no model call; then a
question with two orders in it.
**Part C: Let an agent look the order up.** The lookup as a tool, a small loop that runs what the model asks for,
and the two questions again.
**Part D: Define an agent by who decides the next step.** The three shapes side by side, the definition, and the six
parts of an agent found in our code.
**Part E: Answer a customer question with each of the three shapes.** *How many invoices does Helena Holý have,
what do they add up to, and who is her support rep?*, answered by a workflow, a chatbot and an agent over
`data/chinook.db`, each checked against the database.
**Part F: Ask a question the workflow was not written for.** Which of two customers has spent more, asked of the
same agent with the same tools.
**Part G: Choose how far an agent may act.** The four autonomy levels on a refund email, three cases where an agent
is the wrong choice, and six jobs to place.
**Challenge.** Give the agent a fourth tool, for a customer's latest invoice.

The drawing shows the three shapes. In the agent, a turn is one call to the model. The loop ends with a reply when
the model answers, or with no answer (`None`) when it reaches the cap on turns that our code sets.

![A chatbot, a workflow and an agent side by side. In the chatbot the model writes one reply; in the workflow our code runs fixed steps and fills in a fixed reply; in the agent the model asks for a tool or answers, our code runs the tool and sends the result back, and the loop ends with a reply when the model answers or with no answer, None, at the turn cap](resources/lab04_three_shapes.png)

## Checkpoints

| After | You should see |
|---|---|
| Part A | one reply and no order status (ours said it had no access to the order records) |
| Part B | `Order B22: waiting for stock.` with no model call; for *Have orders A17 and B22 shipped yet?*, `Order A17: shipped on 3 November.` and nothing about B22 |
| Part C | `get_order_status` asked for with `{"order_id":"B22"}`, one `TOOL CALLED` line, and an answer that B22 is waiting for stock, in two model calls; for the two-order question, two `TOOL CALLED` lines and an answer about both |
| Part D | your answers to the two questions: which part changes to let the agent cancel an order, and where a check belongs |
| Part E | the workflow: 7 invoices, \$49.62, Steve Johnson, no model call. The chatbot: one reply with nothing looked up (ours: 12 invoices, \$49.62 and Jane Peacock, so only the total right). The agent: `find_customer`, then `get_invoices` and `get_support_rep` in one reply, then the three right facts, in three model calls |
| Part F | `find_customer` and `get_invoices` for both customers, no `get_support_rep`, and Helena ahead by \$12.98 (\$49.62 against \$36.64), in three or four model calls (ours: four) |
| Part G | the six-job table filled in and compared with the solution's answers |
| Challenge | without the new tool, `find_customer`, `get_invoices` and a reply that the date cannot be found; with `get_latest_invoice`, `find_customer`, `get_latest_invoice` and an answer with 13 November 2013 and \$25.86 |

**About the saved outputs.** They come from `gpt-6-luna`, the model `models.env` names, at reasoning effort `none`.
The model writes its replies and chooses its tool calls on every run, so wording will differ on yours; check the
tool calls and the facts, not the words. We asked each chatbot question 15 times. The model always said it had no
access to order B22. About Helena it always gave \$49.62 and Jane Peacock, and the invoice count changed: 12 in 11
runs, 7 in 3 and 11 in 1. In 4 of those 15 runs the system message did not name the shop, and the total and the
rep were the same. The agents took the same path every time, except that the two-customer question took four
model calls in 5 of 6 runs and three in the other.

## Before you start

- **Lab 00 first.** It checks the environment and that your key reaches the model.
- **Run it locally:** in the repository folder, `uv sync` (or `pip install -r requirements.txt`), put
  `OPENAI_API_KEY` in `.env` (copied from `.env.example`), then open `04_what_is_an_agent.ipynb` in VS Code or
  JupyterLab (`uv run jupyter lab`) with the `.venv` kernel. Run the setup cell first.
- **Reasoning effort:** `REASONING_EFFORT=none` in `models.env`, as shipped. On Chat Completions the model calls
  tools only at that setting.
- **Data:** Parts A to D use a dictionary of two orders, made in the notebook. Parts E and F read `data/chinook.db`,
  the Chinook sample music shop, opened read-only. Part G quotes one rule from `data/corpus/policy_refunds.md`.
- **Cost:** about 13 small model calls in the notebook and 6 in the solution, well under one US cent.

## Folder contents

| Path | What it is |
|---|---|
| `04_what_is_an_agent.ipynb` | the guided notebook, with saved outputs |
| `resources/lab04_three_shapes.png` and `.mmd` | the drawing of the three shapes and its source |
| `solved/04_what_is_an_agent_solution.ipynb` | the challenge solved and run with its outputs, and our answers to Part D's two questions and Part G's six jobs |

## Resources

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents): workflows
  (steps set in code) and agents (the model directs its own steps), and when to use neither
- [OpenAI: A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf):
  the parts of an agent, when one fits, and where people stay in the loop
- [OpenAI: function calling](https://developers.openai.com/api/docs/guides/function-calling): tool schemas, tool calls
  and sending results back
- [OpenAI: Chat Completions API reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create):
  `messages`, `tools`, `tool_calls` and `reasoning_effort`
- [Python: `re`](https://docs.python.org/3/library/re.html): `re.findall` and the pattern syntax

Next: [Lab 05: How to manage what an agent sees](../05_Context_And_Skills/README.md). Back to [the lab list](../README.md).
