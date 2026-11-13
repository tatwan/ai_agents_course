# Bonus B3: How to build a typed agent with Pydantic AI

**CPU | API key: `OPENAI_API_KEY` | Practises: getting an agent's answer as a typed object, and checking that answer in code before accepting it**

## Goal

Meet Pydantic AI on an everyday question, then put it to work at the Chinook support desk. Pydantic AI is an agent
framework built around one idea: the answer of an agent is a Python object with named, typed fields, and our code
can check that object before it accepts it. The lab has two notebooks.

**Notebook 1** is a playground. We ask for a scary film for movie night. A plain agent answers with a paragraph.
With `output_type` the same agent answers with a `MoviePick` object, and the pick has every field of the right type
and is still the wrong film, because a 9-year-old is watching and nobody told the model. We pass that fact in with
`deps`, check every pick with an output validator, and watch the validator send the first pick back with the reason.
Then a tool lets the model ask for the rule first, a test model checks the validator with no API call, and the agent
runs as a terminal chat and a web chat.

**Notebook 2** takes the same library to the desk. The agent answers a rep's question with a typed record built from
three database lookups. Then two requests show what a type cannot check. Asked about a customer the shop does not
have, the agent returns a complete record anyway. Told by a rep to approve a refund, it approves. A second output
type fixes the first, and an output validator that reads the invoice from the database fixes the second.

## What you will learn

- How to describe an answer as a Pydantic model and get it back from an agent with `output_type`, and how to read
  from a run's messages how it arrived.
- How to pass facts our code has to a run with `deps`, and read them through `RunContext` in tools and
  validators.
- How to refuse a well-typed answer with an output validator and `ModelRetry`, and find the correction the model
  was sent.
- How to let an agent answer "not found" with a second output type.
- How to check a decision against a database record before accepting it.
- How to test a validator with `TestModel` and no API call, and how to chat with an agent in a terminal and a
  browser.

## What you will do

### Notebook 1: meet Pydantic AI on movie night (`b3a_meet_pydantic_ai.ipynb`)

**Part A: Ask for a film and read what comes back.** The smallest agent, one question, and a reply that is a
paragraph.
**Part B: Describe the pick as a Pydantic model and get it back as an object.** A `MoviePick` built by hand, what
Pydantic refuses, the same type as the agent's `output_type`, the `final_result` call that carried it, and a pick
that is typed and wrong.
**Part C: Pass who is watching with `deps`, and check the pick with an output validator.** A `Viewer`, the house
rule in plain Python, the same rule as a validator, and the correction found in the messages.
**Part D: Let the model ask for the rule with a tool that reads `deps`.** `@agent.tool`, the tool beside the
validator, and one run drawn.
**Part E: Test the validator with no API call.** `TestModel`, a case the rule must block and a case it must pass.
**Part F: Chat with the agent in a terminal and in a browser.** The agent in one file, `to_cli_sync` and `to_web`.
**Challenge.** A second rule: the film has to end before bedtime.

### Notebook 2: Pydantic AI at the Chinook desk (`b3b_pydantic_ai_at_the_desk.ipynb`)

**Part A: Build a typed desk agent from three database lookups.** The database passed through `deps`, a connection
per lookup, the lookups called by hand, a typed `DeskAnswer`, and the lookups read from the messages.
**Part B: Give the agent a typed way to say it found nothing.** A name the shop does not have, the record the agent
returns anyway, and a second output type.
**Part C: Check a refund decision against the invoice with an output validator.** A rep who writes *Approve it*, a
limit in `deps`, and a validator that reads the invoice from the database.
**Part D: Test the refund rule with no API call.** Four decisions, two that must be blocked and two that must be
returned.
**Challenge.** Puja at the desk, and a rule that a refund's invoice must belong to its customer.

![One run of a typed agent. The model writes a tool call or the fields of an answer. Our code runs the tool, Pydantic checks the fields and types, and our output validator either passes the answer on as result.output or sends it back to the model with a reason. Deps reach the tool and the validator from our code.](resources/b3_typed_run.png)

In the picture the dark box is the model, and the lime boxes run in our Python: the tool, Pydantic's check of the
types, the validator, and the `deps` our code passes to them.

## Checkpoints

| After | You should see |
|---|---|
| Notebook 1, Part A | the reply is a `str` that names a film |
| Notebook 1, Part B | two validation problems for the hand-made bad pick (`age_rating`, `minutes`); a `MoviePick` from the agent rated `PG-13` or `R` (ours: *The Conjuring*, `R`, 112 minutes); a `final_result` tool call in the messages |
| Notebook 1, Part C | two `validator saw` lines, the second rated `G` or `PG` (ours: *The Thing*, then *Coraline*); 2 model requests; the reply to the first `final_result` is our `ModelRetry` text |
| Notebook 1, Part D | `TOOL CALLED: allowed_ratings`, then one `validator saw` line; tools called `allowed_ratings`, `final_result`; 2 model requests |
| Notebook 1, Part E | `RuntimeError` for a real run with requests switched off; `Exceeded maximum output retries (1)` for the 9-year-old; *The Conjuring* returned for the 17-year-old |
| Notebook 1, Part F | `movie_night.py` printed; health check `200 {'ok': True}`; a typed pick in the terminal chat and on the page; `web chat stopped` |
| Notebook 2, Part A | Helena 6, 7 invoices, \$49.62, Steve Johnson; Puja 59, 6 invoices, \$36.64, Jane Peacock; a `DeskAnswer` with Helena's values after `find_customer`, `get_invoices` and `get_support_rep`, in 3 model requests |
| Notebook 2, Part B | `no match for 'Helena Holy'`; a `DeskAnswer` with customer 0, 0 invoices and 0.0; then `NotFound(searched_for='Helena Holy')` through `final_result_NotFound`, and Helena Holý still answered in full |
| Notebook 2, Part C | invoice 404: customer 6, \$25.86; `validator saw: approve \| 25.86`, then `draft \| 25.86`; the draft returned in 3 model requests |
| Notebook 2, Part D | four ✅ lines: blocked, returned, returned, blocked |
| Challenges | notebook 1: an `R` pick and a `PG` pick that is too long are refused, the run stops at one retry, and with `retries=3` a `PG` film of 95 minutes or less passes (ours: *ParaNorman*, 92); notebook 2: a `DeskAnswer` for Puja and a `NotFound` for the misspelt name, a draft of \$13.86 after one correction, one blocked and one returned test |

**About the saved outputs.** They come from `gpt-6-luna`, the model `models.env` names. The model picks its own films
and writes its own values on every run, so titles and wording will differ on yours; check the types, the ratings,
the tool calls and the customer facts. What we counted on this model, ten runs each: asked for a scary film, the
first pick was rated `R` or `PG-13` in 20 of 20 runs, and with the validator the second pick was rated `PG` in 10
of 10. With the viewer's age (9) typed into the question, the model picked a `G` or `PG` film 10 of 10 times: telling
the model works. The age still reaches the run through `deps` and not through the question, because the validator
needs it, and the validator holds when the model is not told or gets it wrong. With the `allowed_ratings` tool the model
called it first in 10 of 10 runs. At the desk, the question about *Helena Holy* returned a filled-in record with
zeros in 10 of 10 runs, and `NotFound` in 10 of 10 once the second type was there. The refund request ending
*Approve it* was approved first and drafted after one correction in 10 of 10 runs; the same request ending
*What do we do?* was drafted the first time in 10 of 10.

## Before you start

- **Lab 00 first.** It checks the environment and that your key reaches the model.
- **Run it locally:** in the repository folder, `uv sync` (or `pip install -r requirements.txt`), put
  `OPENAI_API_KEY` in `.env` (copied from `.env.example`), then open a notebook in VS Code or JupyterLab
  (`uv run jupyter lab`) with the `.venv` kernel. Run the setup cell first. Each notebook runs on its own.
- **No other account.** Both notebooks need only the OpenAI key.
- **A local page:** notebook 1, Part F starts a web chat on `http://127.0.0.1:7932` and stops it two cells later.
  The page's files are downloaded from the internet the first time and kept in `~/.cache/pydantic-ai/`. The
  terminal chat keeps the prompts you typed in `~/.pydantic-ai/prompt-history.txt`.
- **Data:** `data/chinook.db`, the Chinook sample music shop, opened read-only. Nothing in this lab writes to it,
  and no refund is paid: a decision is an object our code receives.
- **Cost:** about 20 model requests across the two notebooks, well under one US cent.

## Folder contents

| Path | What it is |
|---|---|
| `b3a_meet_pydantic_ai.ipynb` | notebook 1, the playground, with saved outputs |
| `b3b_pydantic_ai_at_the_desk.ipynb` | notebook 2, the Chinook desk, with saved outputs |
| `movie_night.py` | notebook 1's agent in one file, for the terminal chat and the web chat |
| `resources/b3_typed_run.png`, `.mmd` | the picture of one run, and its source |
| `solved/b3a_meet_pydantic_ai_solution.ipynb` | notebook 1's challenge solved, run with its outputs |
| `solved/b3b_pydantic_ai_at_the_desk_solution.ipynb` | notebook 2's challenge solved, run with its outputs |

## Resources

- [Pydantic AI](https://pydantic.dev/docs/ai/): the documentation's home
- [Agents](https://pydantic.dev/docs/ai/core-concepts/agent/): `Agent`, `run`, the result and its messages
- [Output](https://pydantic.dev/docs/ai/core-concepts/output/): `output_type` with one type or several, output
  validators
- [Dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/): `deps_type`, `deps=` and `RunContext`
- [Function tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/): `@agent.tool`, `tools=[...]`
- [Retries](https://pydantic.dev/docs/ai/core-concepts/retries/): `ModelRetry` and how many tries a run gets
- [Testing](https://pydantic.dev/docs/ai/guides/testing/): `TestModel`, `FunctionModel`, `Agent.override`
- [Command line interface](https://pydantic.dev/docs/ai/integrations/cli/) and
  [Web chat UI](https://pydantic.dev/docs/ai/guides/web/): the terminal chat and the web chat
- [Pydantic: models](https://docs.pydantic.dev/latest/concepts/models/): `BaseModel`, fields and validation errors

Back to [the bonus labs](../README.md) and [the lab list](../../README.md).
