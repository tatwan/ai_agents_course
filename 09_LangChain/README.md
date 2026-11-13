# Lab 09: How to build an agent from LangChain's pieces

**CPU | API key: `OPENAI_API_KEY` | Optional: `GEMINI_API_KEY` for one optional part | Practises: building an agent in a framework and recognising the loop inside it; making a write wait for a person's approval**

## Goal

Meet LangChain one piece at a time on everyday jobs, then put the pieces to work at the Chinook support desk. The
lab has two notebooks.

**Notebook 1** is a playground: four small jobs for a friend called Maya. A birthday message needs a chat model,
a prompt template and a parser, joined into a chain. Her dinner invitation becomes a calendar entry with a typed
output. Counting the days to her birthday needs something the model does not have, so we give it two tools, make
the round trip by hand once, and let `create_agent` run the loop while we watch each step. The weather in the Grand Canyon
on her birthday needs the web, so the agent gets a ready-made search tool, run by the model's provider, beside our
own.

**Notebook 2** takes the same pieces to the desk. We build the desk agent from three database lookups. Then one
ordinary line of code, `answer.content.lower()`, crashes on the agent's answer although it works on a plain model
reply, because the agent's `.content` is a list of content blocks and not a string. A typed answer comes back
complete for a customer the shop does not have. And when the agent gets a tool that writes, LangChain's middleware
makes the refund wait for a person, who approves one request and rejects another.

## What you will learn

- How to call a chat model with `ChatOpenAI`, and join a prompt template, a model and a parser into a chain with
  `|`.
- How to get a typed object with `with_structured_output` or `response_format`, and what the type checks and does
  not check.
- How to turn a Python function into a tool, and how to make one round trip by hand: the model asks for the tool,
  our code runs it and sends the result back.
- How `create_agent` runs that round trip as a loop, how to draw the agent's graph, and how to read a run with
  `stream` and `invoke`, with its tokens and cost.
- How to give an agent a ready-made tool, web search, beside our own, and what its answer does and does not prove.
- Why a reply's `.content` can be a string or a list of content blocks, and how `.text` reads both.
- How to make a tool call wait for a person with `HumanInTheLoopMiddleware`, and what the checkpointer and the
  thread id are for in that pause.

## What you will do

### Notebook 1: meet LangChain's pieces on four small jobs (`09a_meet_langchain.ipynb`)

**Part A: Write a birthday message with a model, a prompt template and a parser.** One model call, a template with
two gaps, the parser, each run by hand, then the three joined with `|` and the chain's steps printed.
**Part B: Turn a text message into a typed calendar entry.** JSON asked for in words, a loop that goes wrong on
it, an `Event` class with `with_structured_output`, and an entry that fits the class and is not true.
**Part C: Give the model a tool, and make the round trip by hand once.** A question the model cannot answer, a
plain function that can, `tool`, the model's request, our code running the function and sending the result back.
**Part D: Let `create_agent` run the loop, and watch it work.** A second tool, the agent, its graph drawn by the
library, a run watched step by step with `stream`, and a second question that takes another path.
**Part E: Add web search, a tool that the model's provider runs.** `{"type": "web_search"}` beside
`get_birthday`, one run read message by message, the search's record and source in the answer's content blocks,
what the search adds to the input tokens, and where LangChain's other integrations live.
**Part F (optional): Swap the model in the chain for another vendor's.** The chain of Part A with a Gemini model
in the middle.
**Challenge.** A chain that returns calendar entries, and a third tool for the agent.
**Going further.** `batch`, `stream`, and the request LangChain sends for a typed output.

### Notebook 2: LangChain at the Chinook desk (`09b_langchain_at_the_desk.ipynb`)

**Part A: Build the desk agent from three database lookups.** The lookups called by hand, the agent and its graph,
its run read message by message, and what the run cost.
**Part B: Read the agent's answer, whose `.content` can be a list of blocks.** `.content.lower()` on a plain reply
and on the agent's answer, the content block, the two APIs behind it, and `.text`.
**Part C: Ask for a typed answer, and check where its facts came from.** A `DeskAnswer` for Helena, the same
question with her name misspelled, and a check in code on what the lookup returned.
**Part D: Make a refund wait for a person.** A tool that writes, the agent filing a refund with nobody watching,
then the same request stopped by `HumanInTheLoopMiddleware`, checked against the shop's record and approved, and
a second request rejected.
**Challenge.** A typed answer that can say "not found", and a refund edited before it is filed.

![At the top, a chain: a dictionary goes into ChatPromptTemplate, then ChatOpenAI, then StrOutputParser, and a birthday message comes out. Below, an agent: messages go to the model; if the reply has tool calls the tools run and go back to the model, and if not the reply is the answer.](resources/lab09_chain_and_agent.png)

Lime is our own code, the dark boxes are the model.

## Checkpoints

| After | You should see |
|---|---|
| Notebook 1, Part A | an `AIMessage` with a birthday message for Maya; `ChatPromptTemplate` with variables `['hobby', 'name']`; a `KeyError` that names `{'hobby'}`; a `RunnableSequence` with the steps `['ChatPromptTemplate', 'ChatOpenAI', 'StrOutputParser']`; a message for Sam that mentions chess |
| Notebook 1, Part B | JSON in words: a dictionary whose `tell` is the string `'Sam'`, so the loop prints three letters; `with_structured_output(Event)`: an `Event` with `time='19:00'` and `tell=['Sam']`; a hand-made entry with a number for the time refused with two problems; a hand-made entry with Lina accepted, and our own check printing `False` |
| Notebook 1, Part C | without a tool the model says it does not know Maya's birthday; with the tool bound, empty text and one tool call, `get_birthday` with `{'name': 'Maya'}`, and no `TOOL CALLED` line yet; after our code runs the tool and sends the result back, 14 March |
| Notebook 1, Part D | `days_until(14, 3)` gives the days from today (ours: 121); a `CompiledStateGraph` drawn with the nodes `model` and `tools`; the steps `model`, `tools`, `model`, `tools`, `model`, with `get_birthday` first and `days_until` called with day 14 and month 3; for the second question, two `get_birthday` calls in one reply and no `days_until` |
| Notebook 1, Part E | one `TOOL CALLED` line, for `get_birthday(Maya)`, and no `tool` message for the search; an answer with the usual weather in the Grand Canyon in March and at least one link (yours will differ); a `web_search_call` block before the `text` block; two model calls, the first already carrying thousands of input tokens (ours: 4,548 and 14,374) |
| Notebook 1, Part F | with a Gemini key, a birthday message from the Gemini model; without one, a message that the part is skipped |
| Notebook 2, Part A | Helena Holý: `customer_id` 6, 7 invoices, $49.62, rep Steve Johnson; Puja Srivastava: `customer_id` 59, 6 invoices, $36.64, rep Jane Peacock; nodes `['__start__', 'model', 'tools', '__end__']`; seven messages: `find_customer`, then `get_invoices` and `get_support_rep` together, then the answer; 3 model calls with input tokens growing per call (ours: 166, 224 and 335; 725 in and 98 out in all, $0.000121) |
| Notebook 2, Part B | `.content.lower()` works on the plain reply and gives `AttributeError: 'list' object has no attribute 'lower'` on the agent's answer; one content block of type `text`; ids starting `chatcmpl-` and `resp_`; with `.text`, `names the rep: True` |
| Notebook 2, Part C | `DeskAnswer(customer_name='Helena Holý', invoice_count=7, total_usd=49.62, support_rep='Steve Johnson')` and an average invoice of $7.09; for *Helena Holy*, `[]` from the lookup and still a complete `DeskAnswer` (ours: 0 invoices and the rep *None*, after a call with an invented `customer_id`); `customer_found` gives `True`, then `False` |
| Notebook 2, Part D | with no middleware, one refund request filed at once; with it, one interrupt for `file_refund_request` (invoice 393, amount 1.98), its `id` printed, and an empty `REFUND_REQUESTS` list; the shop's record `(393, 'Helena Holý', '2013-10-03', 1.98)`; after `approve`, one request in the list; the second request stopped the same way, the record `(175, 'Helena Holý', '2011-02-15', 1.98)`, and after `reject` a tool message with status `error`, a reply that says the request was not filed, and still one request in the list |
| Challenges | notebook 1: `Event`s with `18:00` and `['Leo', 'Lina']`, and with `11:00` and an empty `tell`; three `TOOL CALLED` lines with `get_birthday` before `days_until`. Notebook 2: for *Helena Holy*, `found=False`, one tool call, and empty or zero values in the other fields; for *Helena Holý*, `found=True` with 7 invoices, a total of 49.62 and the rep Steve Johnson; a waiting call with the amount 18.36, a tool message that starts with a note about the reviewer's change, and after the edit one request for invoice 229 with the amount 13.86 |

**About the saved outputs.** They come from `gpt-6-luna`, the model `models.env` names; notebook 1's optional Part F
also ran `gemini-3.5-flash-lite`. The web search of notebook 1, Part E finds whatever pages the web holds on the day
you run it, so its answer and its link will differ from ours; the agent searched in all 5 runs we made. The model
writes its replies and chooses its tool calls on every run, so wording and token counts will differ on yours, and
`days_until` counts from the day you run it. Check the tool calls, the types and the facts, not the words. What we
saw over repeated runs on this model: asked for JSON in words, it returned `tell` as a string every time (13 runs);
the birthday agent called `get_birthday` and then `days_until` every time (9 runs); asked directly how many days
were left until New Year, the model was one day short in 4 of 5 tries, which is why counting is a Python function.
At the desk, the typed agent returned a complete record for *Helena Holy* in all 12 runs, each after a lookup with a
`customer_id` no tool had returned: in 9 the id was a real customer's and the record held that customer's numbers,
in 3 (the saved run is one) it was not and the record held zeros. The refund request for Puja with Helena's invoice
was proposed as asked in all 5 runs.

## When to use it

LangChain suits a team that wants ready-made pieces and the freedom to swap them: one `invoke` on models,
templates, parsers, chains and agents, a typed output in one call, and `create_agent` with middleware for steps
such as an approval. Its agent is a LangGraph graph, so a team that outgrows the ready-made loop can write the
graph itself (Lab 10) without changing library. What it cost us here: what a reply holds depends on the API
`ChatOpenAI` picks for each call, so we read `.text` and never `.content`; and a tool that returns an empty list
sends the model an empty result, which this model answered by inventing a `customer_id`.

## Before you start

- **Lab 00 first.** It checks the environment and that your key reaches the model.
- **Run it locally:** in the repository folder, `uv sync` (or `pip install -r requirements.txt`), put
  `OPENAI_API_KEY` in `.env` (copied from `.env.example`), then open a notebook in VS Code or JupyterLab
  (`uv run jupyter lab`) with the `.venv` kernel. Run the setup cell first. Each notebook runs on its own.
- **Open the notebooks from this folder,** so that `resources/` is found.
- **Web search:** notebook 1, Part E asks OpenAI to search the web. The search runs on OpenAI's side with your
  OpenAI key; no other account is needed. OpenAI charges for each search, on top of the tokens (see its pricing page).
- **Internet for the drawings:** the two cells that draw an agent's graph send the graph's node names to the
  mermaid.ink web service, which returns the picture. Nothing else is sent, and every other cell works without it.
- **Optional Gemini key:** Part F of notebook 1 runs only when `GEMINI_API_KEY` is in `.env`. Nothing else needs it.
- **Files it writes:** none. The refund requests of notebook 2 are kept in a Python list, and the paused runs in
  the notebook's memory.
- **Data:** `data/chinook.db`, the Chinook sample music shop, opened read-only.
- **Cost:** about 50 model calls in the two notebooks, a fraction of one US cent in tokens, plus OpenAI's fee for
  the web search of notebook 1, Part E.

## Folder contents

| Path | What it is |
|---|---|
| `09a_meet_langchain.ipynb` | notebook 1, the playground, with saved outputs |
| `09b_langchain_at_the_desk.ipynb` | notebook 2, the Chinook desk, with saved outputs |
| `resources/lab09_chain_and_agent.png` and `.mmd` | the picture of a chain beside an agent, and its source |
| `resources/lab09_refund_approval.png` and `.mmd` | the picture of a refund that waits for a person, and its source |
| `solved/09a_meet_langchain_solution.ipynb` | notebook 1's challenge solved, run with its outputs |
| `solved/09b_langchain_at_the_desk_solution.ipynb` | notebook 2's challenge solved, run with its outputs |

## Resources

- [LangChain: overview](https://docs.langchain.com/oss/python/langchain/overview): the documentation's home
- [Models](https://docs.langchain.com/oss/python/langchain/models): chat models, `invoke`, `batch` and `stream`
- [Messages](https://docs.langchain.com/oss/python/langchain/messages): message objects, `.text` and content blocks
- [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output): `with_structured_output`
  and `response_format`
- [Tools](https://docs.langchain.com/oss/python/langchain/tools): `tool`, docstrings and type hints as the
  description
- [Agents](https://docs.langchain.com/oss/python/langchain/agents): `create_agent`, its loop and its middleware
- [Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop): the approval middleware,
  its decisions and the two interrupt modes
- [ChatOpenAI](https://docs.langchain.com/oss/python/integrations/chat/openai): the OpenAI model class, when it
  uses the Responses API, and the tools OpenAI runs, such as web search
- [Integrations](https://docs.langchain.com/oss/python/integrations/providers/overview): every service LangChain
  connects to, and the package for each

Back: [Lab 08: How to build and run an agent with Google ADK](../08_Google_ADK/README.md). Next:
[Lab 10: How to draw, pause and resume an agent with LangGraph](../10_LangGraph/README.md). Back to [the lab list](../README.md).
