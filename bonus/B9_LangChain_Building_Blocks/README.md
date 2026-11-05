# Bonus B9: How to compose LangChain's building blocks

**CPU | API key: `OPENAI_API_KEY` | Environment: repository core | 14 small model calls | Practises: prompt
templates, composing steps with LCEL, typed output from a bare model, batch and streaming, choosing a workflow or an
agent**

## Goal

We build two support-desk pipelines from LangChain's smaller pieces, with no agent in them: one drafts the reply to a
ticket, the other turns a ticket into a typed record. The pieces are a prompt template that fills the same reply
instructions for any ticket, a chain written `prompt | model | parser` that hands each step's result to the next, a
model that returns a Pydantic object, and the same chain run over many tickets at once or streamed piece by piece. The
moment that teaches it is in Part C: the duplicate-charge ticket comes back as a valid `TicketRecord`, and a record
with an invoice number that appears nowhere in the ticket passes the same validation. Only a check in our own code can
say whether a value came from the ticket. Part E then asks what every pipeline meets sooner or later: our code fixed
these steps, so when is that better than an agent that chooses its own?

## What you will learn

- How to write a `ChatPromptTemplate` with variables, and read the messages it actually sends.
- How to compose `prompt | model | StrOutputParser()` into one chain, and what each step hands the next.
- How to turn a ticket into a typed record with `with_structured_output`: the request the API receives, the raw reply
  beside the parsed object, and what validation guarantees and what it does not.
- How to run one chain over several tickets with `batch`, stream one reply as it is written, and price both from the
  token counts.
- How to put a step of our own, a database lookup, inside a chain.
- When a fixed chain (a workflow) is the better choice, and when you need an agent such as lab 08's `create_agent`.

## Where this lab starts

[Lab 08](../../08_LangChain_LangGraph/README.md) Part A constructed `ChatOpenAI` from `models.env`, called it with a
list of messages and read the `AIMessage` it returned (`.text`, `usage_metadata`, `response_metadata`); the rest of
lab 08 handed that model to `create_agent`, which runs a loop. This lab stays with one model call at a time and builds
around it. It defines everything it uses, so it runs without lab 08.

![Two shapes. Top: a fixed chain, dict to ChatPromptTemplate to ChatOpenAI to StrOutputParser to a draft reply, each edge labelled with the object handed on. Bottom: lab 08's agent, where the model node's reply goes to a route that either runs the tools node and loops back, or ends with the answer](resources/labB9_chain_and_agent.png)

## What you will do

All of it on the Chinook music shop's support files (`data/corpus/`, read in place) and, in Part E, its database
(`data/chinook.db`, opened read-only).

| Part | What it teaches |
|---|---|
| Part A: Fill the same reply instructions for any ticket with a prompt template | messages by hand first, then `ChatPromptTemplate` with `{policy}` and `{ticket}`, the filled messages printed, the error for a missing variable |
| Part B: Compose prompt, model and parser into one chain | each step run alone, `StrOutputParser` on a string and on content blocks, `prompt \| llm \| parser` as a `RunnableSequence`, its steps and graph |
| Part C: Turn a ticket into a typed record with `with_structured_output` | the record by hand, a Pydantic class, the strict `json_schema` request caught on its way out, raw reply beside parsed object, a well-typed invented record and the check that catches it |
| Part D: Run many tickets with `batch`, and stream one reply | four drafts in one `batch`, tokens counted through the parser with a callback, priced from `models.env`, the same four one by one, one reply streamed piece by piece |
| Part E: Choose between a fixed chain and an agent | a ticket the chain cannot answer, a lookup step of our own inside the chain, and where a workflow stops and an agent begins |
| Challenge | three records in one `batch`; the model chooses the policy while our code keeps the steps |

## Checkpoints

| After | You should see |
|---|---|
| Part A | `variables: ['policy', 'ticket']`; a `ChatPromptValue` with a `SystemMessage` (rules and policy) and a `HumanMessage` (the ticket); `same as by hand: True`; `KeyError: Input to ChatPromptTemplate is missing variables {'policy'}` |
| Part B | `AIMessage`, `content` a `str`, an id starting `chatcmpl-`; `'Hello'` twice from the parser; steps `['ChatPromptTemplate', 'ChatOpenAI', 'StrOutputParser']` and five graph nodes in a line; the draft a `TextAccessor` with `is a str: True` |
| Part C | `RunnableSequence with 2 steps`, method `json_schema`; `POST /v1/chat/completions` with a strict `json_schema` whose `required` lists all five fields; `raw`, `parsed`, `parsing_error: None`; in our run `TicketRecord(issue_type='duplicate_charge', amount_usd=9.99, invoice_numbers=[], customer_name=None, needs_refund=True)`, field for field the record written by hand, and ✅ on both of its checks; `float_parsing` for the amount in words; the invented invoice 404 accepted by validation and ❌ on the invoice-number check |
| Part D | `4 inputs, each with keys ['policy', 'ticket']`; four drafts in input order; one usage entry for the batch (806 input and 223 output tokens in our run, 0.0001921 US dollars); `same as above: True`; the batch in about a third of the time of the same four calls one by one (2.0 s against 6.4 s in our run), at almost the same price; a stream of mostly one-word pieces separated by `|`, a few of them empty (59 pieces, 4 empty, first text after 1.42 s of 1.85 s in our run), and the usage at the end |
| Part E | the plain chain's draft for Puja, read for what it did with a question it cannot look up (in both saved runs, this notebook and the solution, it invented no number and said it could not tell from the ticket); `invoices: 6, total spent: 36.64 US dollars, support rep: Jane Peacock`; steps starting with `RunnableLambda`; ✅ on `states 6 orders and 36.64 US dollars` |
| Challenge | three `TicketRecord` objects, each checked against its own ticket; four policy choices, each checked against the corpus and shown beside `PAIRS` |

**About the saved outputs.** They come from `gpt-6-luna` with reasoning effort `none`, the model named in
`models.env`. Drafts, records, token counts and times change from run to run; check the shape of each result (types,
fields, order, which checks pass), not the wording. Whether the plain chain invents numbers for Puja in Part E is the
model's choice in each run; the lab reads what it did and does not depend on it. With another model the API route can
change too (lab 08 Part C shows when), which `.text` and `StrOutputParser` absorb.

## When to use it

The core path builds the desk as an agent that decides its own next step (lab 07 with the Agents SDK, lab 08 with
`create_agent`). This lab composed the same model into fixed chains, and the measurements say when that fits: a reply
chain made exactly one model call per ticket, so four drafts cost about the same whether they ran in a
batch (2.0 s, 0.0001921 US dollars) or one by one (6.4 s, 0.0001831 US dollars); a typed record came back in a strict schema that our own check could then hold against the ticket; and one lookup step of ours answered
Puja's question with her real numbers. Reach for `prompt | model | parser` when the steps are known and short:
drafting from a policy, extracting a record, classifying a ticket. The old chain classes such as `LLMChain` now live
in a separate `langchain-classic` package; composing Runnables with `|` is part of `langchain-core`, and it is what
LangChain's own helpers return. When a workflow needs branches, a wait for a person or saved state, build it as a
LangGraph graph ([bonus B1](../B1_LangGraph_Durable_Workflows/README.md)); when the lookups depend on the question,
use an agent ([lab 08](../../08_LangChain_LangGraph/README.md)).

## Before you start

Complete [Lab 00's setup](../../00_Environment_Check/README.md). From the repository folder, run
`uv sync --python 3.13` or `pip install -r requirements.txt`, put your OpenAI key in the root `.env` (copied from
`.env.example`), then select the repository `.venv` kernel in VS Code or JupyterLab. Open
[b9_langchain_building_blocks.ipynb](b9_langchain_building_blocks.ipynb) and run from the top. No other lab needs to
have been run; Python dictionaries, lists and functions are enough to start, and the notebook explains templates,
Runnables, Pydantic types, context managers and the SQL it uses where they appear.

This bonus uses the **root environment** and installs nothing. It reads `data/corpus/` and `data/chinook.db` in place
(the database read-only) and writes no files. Ticket 16 is left out on purpose: it carries a planted instruction,
which lab 17 studies. **Cost:** 14 model calls of a few hundred tokens each, well under one US cent at the prices in
`models.env`; the solution notebook makes 7 more.

## Folder contents

| Path | What it is |
|---|---|
| `b9_langchain_building_blocks.ipynb` | the guided notebook, with saved outputs and the challenge cells |
| `resources/labB9_chain_and_agent.mmd` | the source (Mermaid) of the diagram of the chain and the agent |
| `resources/labB9_chain_and_agent.png` | that diagram, exported from the source |
| [solved/b9_langchain_building_blocks_solution.ipynb](solved/b9_langchain_building_blocks_solution.ipynb) | the whole notebook run again with the challenge solved |

## Troubleshooting

| What you see | Why | What to do |
|---|---|---|
| `KeyError: "Input to ChatPromptTemplate is missing variables {'policy'}. ..."` | the dictionary passed to `invoke` lacks one of the template's variables | pass every name in `prompt.input_variables` |
| a `KeyError` naming a variable such as `'"reply"'` that you never meant to create | the template text holds a literal `{`, for example a JSON example | write literal braces twice: `{{` and `}}` |
| `TypeError: Expected mapping type as input to ChatPromptTemplate. Received <class 'str'>.` | a template with two variables was given a plain string | pass a dictionary: `{"policy": ..., "ticket": ...}` |
| `AttributeError: 'TextAccessor' object has no attribute 'text'` | the chain ends with `StrOutputParser`, so its output is already a string | use the string itself; `.text` belongs to messages |
| `IndexError: list index out of range` when reading the stream's usage | the stream returned no token counts: `ChatOpenAI` asks for them by default only when it talks to OpenAI directly (no `OPENAI_BASE_URL`, no own HTTP client) | construct the model with `stream_usage=True` |

## Resources

- [LangChain: Models](https://docs.langchain.com/oss/python/langchain/models): `invoke`, `stream`, `batch` with
  `max_concurrency`, and structured output with `include_raw`.
- [LangChain: Messages](https://docs.langchain.com/oss/python/langchain/messages): message objects, `.text` and
  content blocks.
- [LangChain: ChatOpenAI](https://docs.langchain.com/oss/python/integrations/chat/openai): the OpenAI chat model, its
  structured-output methods and when it uses the Responses API.
- [`ChatPromptTemplate` reference](https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate):
  `from_messages`, `input_variables` and `invoke`.
- [`RunnableSequence` reference](https://reference.langchain.com/python/langchain-core/runnables/base/RunnableSequence):
  what `|` builds.
- [`StrOutputParser` reference](https://reference.langchain.com/python/langchain-core/output_parsers/string/StrOutputParser).
- [`get_usage_metadata_callback` reference](https://reference.langchain.com/python/langchain-core/callbacks/usage/get_usage_metadata_callback):
  token counts across every call in a block.
- [OpenAI: Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs): `json_schema`
  and strict mode.
- [OpenAI: Streaming API responses](https://developers.openai.com/api/docs/guides/streaming-responses): how a reply
  arrives in pieces.
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/): fields, types and `model_validate()`.

Back to [the bonus lab list](../README.md).
