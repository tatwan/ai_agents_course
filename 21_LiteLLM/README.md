# Lab 21: How to call any model through one interface with LiteLLM

**CPU | API key: `OPENAI_API_KEY` | Optional: `GEMINI_API_KEY` for one optional part | Practises: calling models from any vendor through one interface; pricing a request; routing and fallbacks; putting a gateway between an agent and its model**

## Goal

Meet LiteLLM on an everyday job, then put it between a working agent and its model. LiteLLM is a layer between
our code and the model vendors: a Python library that makes one kind of call for every vendor, and a gateway, a
server that does the same for every program in a company. It is neither a model nor an agent framework. The lab
has two notebooks.

**Notebook 1** is a playground. We have a new kitten, and she needs a name. We ask a model through OpenAI's own
client and through `litellm.completion`, and read the two replies side by side. From there we price a reply,
ask two or three models the same question in one loop, receive a reply piece by piece, and let the model ask for a die that our own code rolls. Then we give the models
names of our own with a `Router`, break one of them on purpose, and watch a fallback answer in its place. The same
names then go behind one address, the LiteLLM gateway, which we call with the plain OpenAI client.

**Notebook 2** takes the gateway to the Chinook support desk. A desk agent answers a rep's question: *How many
invoices does Helena Holý have, what do they add up to, and who is her support rep?* We point the agent at the
gateway by changing its client and its model name, and then point the model's address at a place where nothing answers. Wired straight to that
address, the agent stops with a connection error. Behind the gateway it still gives the rep the three facts, and
the gateway's reply headers show what happened: a backup deployment answered every request, and the answer took
longer.

## What you will learn

- How `litellm.completion` mirrors the call of OpenAI's own client, and what the `openai/` in front of a model
  name says.
- How to read what a reply cost with `completion_cost`, and why that number is an estimate from a price table.
- How to ask several models the same question in one loop, and price each reply.
- How to stream a reply, and how to let the model ask for a tool that our own code runs.
- How to give models names of our own with a `Router`, add a fallback, and read which deployment answered.
- How to write a gateway's config file, start the gateway, and point an existing agent at it by changing its
  client and its model name.
- How to read from the gateway's reply headers which deployment answered each request and what it cost, and what
  a fallback hides.

## What you will do

### Notebook 1: meet LiteLLM by naming a kitten (`21a_meet_litellm.ipynb`)

**Part A: Send one question through OpenAI's client and through LiteLLM.** The same question with both, and the
two replies compared field by field.
**Part B: Read what a reply cost, and where the price comes from.** The cost by hand from `models.env`, then
`completion_cost` and the price table it reads.
**Part C: Ask several models the same question, side by side.** One loop over a list of models, the same call for
each, and the cost of each reply; a Gemini model joins when its key is present.
**Part D: Receive a reply piece by piece with `stream=True`.** Five name ideas as a stream of chunks.
**Part E: Let the model ask for a tool that our own code runs.** The model asked to pick at random, a
`roll_dice` function, its schema, and the tool round by hand.
**Part F: Call a model by a name of our own with a `Router`.** Two deployments, `quick` and `careful`, on two
models, and the id of the one that answered.
**Part G: Keep the answer coming when a deployment cannot be reached.** A call to an address where nothing
answers, then the same question through a Router with a fallback.
**Part H: Put the same names behind one address with the LiteLLM gateway.** The config file, the gateway started
and stopped from the notebook, a call with the plain OpenAI client, the reply headers, and the gateway's pages.
**Part I (optional): Fall back to another vendor's model.** The fallback pointed at a Gemini model.
**Challenge.** Roll the die while `quick` is down, and price the two replies.

### Notebook 2: LiteLLM at the Chinook desk (`21b_litellm_at_the_desk.ipynb`)

**Part A: Build the desk agent on the plain OpenAI client.** Three database lookups called by hand, their tool
schemas, and a loop on Chat Completions.
**Part B: Describe a primary and a backup deployment in the gateway's config.** The config file, and two small
functions that start and stop the gateway.
**Part C: Point the desk agent at the gateway by changing the client and the model's name.** The same question
through the gateway, with nothing inside the agent changed.
**Part D: Read which deployment answered, and what it cost, from the gateway's headers.** The headers of one
request, then of every request the agent makes.
**Part E: Break the primary on purpose, and compare the agent with and without the gateway.** The agent wired straight
to a dead address, then the agent behind a gateway whose primary points there.
**Challenge.** Give the desk a second job with its own name, and break the backup too.

![The desk agent calls the LiteLLM gateway at one address, with the gateway's key and the name desk. Inside the gateway, the deployment desk points at the primary model and the deployment desk-backup at the backup model, with a dotted fallback arrow from desk to desk-backup. The reply goes back to the agent with headers that name the deployment, the fallbacks and the cost.](resources/lab21_gateway.png)

Light green is our own code, the dark boxes are models, white and grey are LiteLLM.

## Checkpoints

| After | You should see |
|---|---|
| Notebook 1, Part A | a name for the kitten from both calls; a `ChatCompletion` from OpenAI's client and a `ModelResponse` from LiteLLM, with the same fields (ours: 24 input tokens each) |
| Notebook 1, Part B | the cost by hand and `completion_cost` print the same number (ours: $0.00000590); the table's prices match `models.env` |
| Notebook 1, Part C | one block per model, each with a name, the type `ModelResponse`, token counts and a cost; the costs differ (ours, three models with a Gemini key: $0.00000740, $0.00000615 and $0.00001070); without a Gemini key, two blocks and a line that says the Gemini model was left out |
| Notebook 1, Part D | five names with reasons; a list of a few dozen pieces (ours: 69) |
| Notebook 1, Part E | asked to pick at random, the model names one of the six (ours: Pixel; Noodle in eight of our nine runs); with the tool, a reply with no text and one call `roll_dice` with `{"sides":6}`, no `TOOL CALLED` line yet; after our code rolls, the reply names the kitten with the number the die showed |
| Notebook 1, Part F | the Router lists `quick` and `careful` with two different models; the call to `quick` prints a name, the second OpenAI model and `deployment: quick-on-openai` |
| Notebook 1, Part G | the direct call to an address where nothing answers (the dead address) prints a connection error; through the Router with a fallback, a name, the main model, `deployment: careful-on-openai` and `fallbacks attempted: 1`, after some seconds of retries (ours: 6.9) |
| Notebook 1, Part H | the config file; `gateway starting on port 4000` (or the next free port); `the gateway is up and offers: ['quick', 'careful']`; a name through the plain OpenAI client; a second reply with headers that name `quick-on-openai`, 0 fallbacks and a cost (ours: $0.00000435); `gateway stopped` |
| Notebook 1, Part I | with a Gemini key, a name, a Gemini model and `deployment: careful-on-gemini`; without one, a message that the part is skipped |
| Notebook 2, Part A | Helena Holý with `customer_id` 6, 7 invoices, $49.62 and Steve Johnson; three `lookup:` lines, `find_customer` first, and the three facts in the answer |
| Notebook 2, Part B | the config file with `desk`, `desk-backup` and the fallback; `the gateway will use port 4000` (or the next free port); `the gateway is up and offers: ['desk', 'desk-backup']` |
| Notebook 2, Part C | through the gateway, the same three lookups and the same three facts |
| Notebook 2, Part D | one request: `desk`, `desk-primary`, 0 fallbacks and a cost (ours: $0.00000330); one reply in the hook's list; the agent's question: three requests, all `desk-primary`, a total cost of a fraction of a cent (ours: $0.000147), in a few seconds (ours: 8.2) |
| Notebook 2, Part E | wired straight to the dead address: `APIConnectionError` and no lookups; behind the gateway: the three facts, three requests answered by `desk-backup-1` with 1 fallback each, and a longer wait (ours: 18.1 seconds against 8.2); `gateway stopped` |
| Challenges | notebook 1: one `TOOL CALLED` line, `careful-on-openai` on both replies, and two cost sums that agree (ours: $0.00006200). Notebook 2: the gateway offers `desk`, `desk-backup` and `notes`, and the summary's header names `notes-primary`; with both deployments broken, no lookups and an error from the gateway that says the fallback failed too (ours after 29.2 seconds) |

**About the saved outputs.** They come from `gpt-6-luna`, the model `models.env` names for both `MODEL_DEFAULT` and
`MODEL_STRONG`, and from `gpt-4o-mini` (`MODEL_COMPARE`) in notebook 1's Parts C and F to H; Parts C and I of
notebook 1 also ran `gemini-3.5-flash-lite`. The model writes its replies anew on every run, so the kitten's
names, the token counts and the costs will differ on yours, and the die is random. Check the types, the deployment
ids, the fallback counts and Helena's facts, not the words. Asked to pick one of the six names at random, the
model said Noodle in eight of the nine times we asked (Pixel in the saved run). Port 4000 was free on our machine,
so both gateways took it. The fallback answered in every run we made (more than ten), and the desk question behind
a gateway with a broken primary took between 17.9 and 21.9 seconds in our runs (18.1 in the saved one), against
2.9 to 8.2 with the primary working (8.2 in the saved one).

## When to use it

LiteLLM suits a team that uses, or may use, more than one model vendor, and wants its programs to stay the same
when the vendor or the model changes. Inside one Python program, the library and its `Router` are enough: one
call shape, names of your own, a fallback. When several programs or teams share models, the gateway adds one
place for the vendor keys, a key and a budget per program, and a record of what each request cost. It also has
costs. The gateway is one more service to run and to keep up, and its admin page needs a database. Its prices
come from a table that can be behind the vendor's price list. A fallback hides an outage from the program and
from its users, so someone has to read the logs. And LiteLLM carries requests; it does not run tools or decide
what an agent may do. The agent stays in your code or in a framework.

## Before you start

- **Lab 00 first.** It checks the environment and that your key reaches the model.
- **Run it locally:** in the repository folder, `uv sync` (or `pip install -r requirements.txt`), put
  `OPENAI_API_KEY` in `.env` (copied from `.env.example`), then open a notebook in VS Code or JupyterLab
  (`uv run jupyter lab`) with the `.venv` kernel. Run the setup cell first. Each notebook runs on its own.
- **Open the notebooks from this folder,** so that `resources/` and `outputs/` are found.
- **The gateway runs on your machine.** Both notebooks start the LiteLLM gateway as a second program on port
  4000, LiteLLM's usual port. When 4000 is busy (a LiteLLM gateway in Docker usually listens there), they take the
  next free port. A later cell stops the gateway; run it before you close a notebook or restart its kernel. The
  gateway answers only programs on your own machine (`--host 127.0.0.1`).
- **No Docker and no database** are needed. The gateway's admin page needs both; Going further in notebook 2 says
  where to start.
- **Optional Gemini key:** with `GEMINI_API_KEY` in `.env`, notebook 1 adds a Gemini model to Part C and runs
  Part I. Nothing else needs it.
- **Files it writes:** `outputs/gateway_config.yaml` (the config file the notebooks write) and
  `outputs/gateway.log` (what the gateway printed), in a folder git ignores.
- **Data:** `data/chinook.db`, the Chinook sample music shop, opened read-only.
- **Cost:** about 30 model calls in all, under one US cent.

## Folder contents

| Path | What it is |
|---|---|
| `21a_meet_litellm.ipynb` | notebook 1, the playground, with saved outputs |
| `21b_litellm_at_the_desk.ipynb` | notebook 2, the Chinook desk, with saved outputs |
| `resources/lab21_one_interface.png`, `lab21_router.png`, `lab21_gateway.png` and their `.mmd` files | the three pictures, and their sources |
| `resources/litellm_admin_page.png` | a screenshot of the gateway's admin page |
| `solved/21a_meet_litellm_solution.ipynb` | notebook 1's challenge solved, run with its outputs |
| `solved/21b_litellm_at_the_desk_solution.ipynb` | notebook 2's challenge solved, run with its outputs |

## Resources

- [LiteLLM: getting started](https://docs.litellm.ai/docs/): `completion`, the providers and the model name
  prefixes
- [Completion token usage and cost](https://docs.litellm.ai/docs/completion/token_usage): `completion_cost` and the
  price table
- [Streaming](https://docs.litellm.ai/docs/completion/stream) and
  [function calling](https://docs.litellm.ai/docs/completion/function_call): streams and tools through LiteLLM
- [Router](https://docs.litellm.ai/docs/routing): `model_list`, deployments and how a Router chooses
- [Fallbacks](https://docs.litellm.ai/docs/proxy/reliability): fallbacks, retries and cooldowns
- [Gateway quick start](https://docs.litellm.ai/docs/proxy/quick_start) and
  [the config file](https://docs.litellm.ai/docs/proxy/configs): starting the gateway and what its config holds
- [Response headers](https://docs.litellm.ai/docs/proxy/response_headers): every `x-litellm-` header
- [Virtual keys](https://docs.litellm.ai/docs/proxy/virtual_keys) and
  [budgets](https://docs.litellm.ai/docs/proxy/users): keys per program with a spending limit
- [Docker quick start](https://docs.litellm.ai/docs/proxy/docker_quick_start): a gateway with a database and the
  admin page

Previous: [Lab 20: How to evaluate and trace an agent](../20_Evals_And_Tracing/README.md). Next:
[Lab 22: How to re-engineer a process with agents](../22_Process_Reengineering/README.md). Back to
[the lab list](../README.md).
