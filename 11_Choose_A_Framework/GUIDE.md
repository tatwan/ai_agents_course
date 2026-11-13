# Lab 11: How to choose an agent framework

## Goal

Choose an agent framework for a job and defend the choice with evidence: what the job needs, what each framework
adds, and what each one decides for you without asking. The moment that teaches it comes in Part B. This repository
runs the same Chinook desk agent on the same question in our own loop and in seven frameworks, and every build with
one agent makes the same three model requests and returns the same three facts. The loop is the same everywhere.
What differs is what each framework does around it, and in every lab one of those things only showed up because
the lab printed what came back. Part D then scores the frameworks for the shop's support desk and shows that the
pick turns on one question: how long a refund request waits for a person's approval.

## What you will learn

- How to recognise the agent loop inside any framework, and read a framework's run as model requests, tokens and
  tool calls.
- Where you watch a run in each framework (a browser development page, a trace dashboard, an event stream, or a drawn graph).
- Why LiteLLM is not an agent framework, and how it sits under any framework to translate model provider APIs.
- How to find what a framework decides for you (which API it calls, a default model, a reasoning effort, what it
  counts) before that decision reaches production.
- What six criteria (easy to learn, control of the loop, multi-agent, pause and approve, tracing built in, any model
  vendor) mean in practice, with evidence from this repository's runs.
- How to turn a job's needs into must-haves and weights, score the frameworks for it and reach a pick.
- When your own loop is the right choice, and which answer would make you change a pick later.
- What a wrong pick costs, and which parts of an agent move to another framework and which stay behind.

## Before you start

This is a reading guide: there is no code to run, nothing to install and no key to set. You need a text editor or a
sheet of paper, because every step asks you to write something down before you read our answer.

### An everyday choice first

Before we score seven frameworks for a customer-support desk, start with a simpler choice you can make in your head:
**a homework helper that must ask a parent before it sends an email to a teacher.**

What does this job need?
1. It drafts an email to the teacher based on the child's assignment questions.
2. It must pause and wait until a parent reviews the draft, even if the parent opens the notification hours later on their phone.
3. It sends the email only after approval, and drops the draft if rejected.

How do you pick a framework for it?
- **Step 1: Answer what the job needs.** The helper waits hours for a person across a restart. That makes *Pause and approve* a **must-have**.
- **Step 2: Filter on that must-have.** Drop any framework that cannot hold a paused run in lasting storage. If a framework keeps its pause only in memory, the draft is lost when the app process stops.
- **Step 3: Pick from what survives.** Among the frameworks that pass the filter, pick the simplest one that lets the parent approve with a button and logs what was sent.

That is the whole method in miniature: turn what a job needs into must-haves, filter out the frameworks that lack them, and pick from what is left using evidence.

### The support desk requests

Now we apply that same method to the Chinook music shop support desk, using two of its requests:

- **The Helena question:** *How many invoices does Helena Holý have, what do they add up to, and who is her support
  rep?* The database says customer 6, 7 invoices, \$49.62 and Steve Johnson. Three lookups answer it:
  `find_customer`, `get_invoices` and `get_support_rep`.
- **The duplicate-charge refund:** ticket 14 reports two invoices for the same digital album on the same day, \$9.99
  each, and the shop's refund policy says to refund the later invoice in full. Nobody wants an agent to move money on
  its own, so a refund request must wait until a person approves it.

Every measured number in this guide comes from a saved run in one of this repository's labs, named beside it, so
you can open that notebook and find it. The runs used `gpt-6-luna` at reasoning effort `none`. A run of yours on
another day or another model will differ in tokens and wording; the shape of each run (which tools, in what order,
where it stops) is what to compare.

⚠️ **Framework facts change every few weeks.** Every star count, download count, version and status below carries
the date it was read and a link to where. Check one before you quote it in a meeting (the Challenge does this).

## Part A: See the same loop inside every framework

Before we compare frameworks, we need what they have in common, so that a difference has something to stand out
against.

### Step 1: Name what a framework takes over

Lab 03 wrote the agent loop by hand (`03b_agent_loop_at_the_desk.ipynb`). It does four things:

1. Send the messages and the tool schemas to the model.
2. If the reply asks for tools, run them with our own Python and append each result to the messages.
3. Repeat until the reply is an answer, or a turn cap stops the run.
4. Record what happened: each call's tokens, each tool's arguments and result.

Every framework in this guide runs these four steps for us. Each also writes the tool schemas from our functions'
type hints and docstrings: lab 07 printed the schema the Agents SDK wrote for its weather tool, and it had the
same shape as the one written by hand in Lab 02. What no framework takes over is what makes the desk ours: the three lookups, the
instructions, and every check on what the agent may do.

**Write down:** which of the four steps would you least like to write again, and why? (Ours: step 4. The loop is a
dozen lines; recording every call in a form an auditor can read is the part that grows.)

### Step 2: Read the desk agent's definition across frameworks

Here is the line that defines the desk agent in each lab, copied from its notebook. `SYSTEM` holds the
instructions, `MODEL` the model's name from `models.env`, and the tool list the three lookups.

| Framework | Lab notebook | The definition |
|---|---|---|
| OpenAI Agents SDK | `07b`, Part A | `Agent(name="Desk", instructions=SYSTEM, model=MODEL, tools=DESK_TOOLS, model_settings=SETTINGS)` |
| Google ADK | `08b`, Part A | `Agent(name="desk", model=llm, instruction=SYSTEM, tools=[find_customer, get_invoices, get_support_rep])` |
| LangChain | `09b`, Part A | `create_agent(llm, TOOLS, system_prompt=SYSTEM)` |
| LangGraph | `10b`, Part A | `StateGraph(DeskState)` (a `TypedDict` with `messages: Annotated[list, add_messages]`) with nodes `model` and `tools`, a conditional route and a checkpointer |
| LlamaIndex | `14b`, Part B | `FunctionAgent(tools=[rt_tool], system_prompt=PROMPT)` (`Settings.llm` configured in setup): a search agent over policies and tickets |
| Pydantic AI | `b3b`, Part A | `Agent(model, deps_type=Desk, output_type=DeskAnswer, instructions=..., tools=[find_customer, get_invoices, get_support_rep], model_settings=model_settings)` |
| CrewAI | `b4b`, Part C | two `Agent`s (`billing_clerk`, `refund_adviser`) with `role`, `goal` and tools, two `Task`s, and `Crew(agents=[...], tasks=[...], process=Process.sequential)` |
| Microsoft Agent Framework | `b5b`, Part A | `Agent(client=client, name="Desk", instructions=..., tools=tools, default_options=OPTIONS)` |

> [!NOTE]
> **LiteLLM is not an agent framework: it sits under any of them.** Taught in Lab 21 (`21a_meet_litellm.ipynb` and `21b_litellm_at_the_desk.ipynb`) and used in Lab 07 (`07a` Part G), LiteLLM is a translation adapter. It maps OpenAI-format requests and responses to and from other model providers (Anthropic, Gemini, Bedrock, Ollama). It does not maintain an agent loop, route between nodes, manage conversation state, or pause for approvals. An agent framework orchestrates the loop; LiteLLM adapts the model call underneath it.

**Write down before reading on:** which three things does every row ask for?

A model, instructions and tools. Most rows are one constructor call; Pydantic AI passes lookup functions in
`tools=[...]` (or adds helpers with `@agent.tool`, as in `b3a`), LangGraph wires nodes and edges into a graph, and CrewAI describes the desk as two roles with a task each, because
describing work as roles and tasks is what CrewAI is for. The extra fields say what each framework adds or needs:

- `model_settings` in the Agents SDK: without it the SDK sends no reasoning effort for our model (Part B shows what
  that costs to miss).
- `output_type` and `deps_type` in Pydantic AI: the answer is checked against a Python type, and the database
  connection is passed in as a dependency instead of sitting in a global variable.
- `client` in Microsoft Agent Framework: the model's provider is an object of its own, configured once.

**Key lesson:** an agent's definition is small and nearly the same in every framework. Moving the definition to
another framework is a few lines of work. What costs more to move is everything built around it, which Part E
comes back to.

**Checkpoint A.** You can say which four things every framework does for us, which three things every definition
asks for, why LiteLLM sits under a framework rather than acting as one, and what one extra field adds in three of the rows.

## Part B: Compare the same agent's runs across frameworks

If every framework runs the same loop, the runs should look alike. This part checks that on the Helena question (and notes where `b5b` ran the same lookups on Puja Srivastava and `b4b` Part C ran a two-agent refund advice task), then looks for what differs.

### Step 1: Put the runs side by side

| Built with | Where the saved run is | Model requests | Where you watch a run | Three facts returned |
|---|---|---|---|---|
| Our own loop, on Chat Completions | `03b`, Part A | 3 | printed transcript / terminal | yes |
| OpenAI Agents SDK | `07b`, Part A | 3 | OpenAI Traces page (or local with `set_tracing_disabled`) | yes |
| Google ADK | `08b`, Part A | 3 (5 events) | `adk web` (browser development UI) and `adk run` (CLI) | yes |
| LangChain `create_agent` | `09b`, Part A | 3 | graph drawn by library, step `stream`, or LangSmith (`B7`) | yes |
| LangGraph, the same graph built by hand | `10b`, Part A | 3 | drawn `StateGraph`, step `stream` | yes |
| Pydantic AI | `b3b`, Part A | 3 | `to_cli_sync`, `to_web`, log messages | yes |
| Microsoft Agent Framework | `b5b`, Part A | 3 | workflow event stream / session inspection | yes (Puja) |
| CrewAI, two specialists | `b4b`, Part C | 3 (5 in B4 playground) | crew terminal log / `Flow.plot()` | — (Puja refund advice) |

Read the table in two passes:

- **The requests are the same.** Every build with one agent made three model requests: `find_customer` first, then
  `get_invoices` and `get_support_rep` together in one reply, then the answer. That is Lab 03's loop, whichever
  framework runs it. In CrewAI, the desk run in `b4b` Part C takes 3 model requests because the billing clerk runs the lookups and the adviser reads them from context; in the playground (`b4a` Part E) two specialists each running their own loop took 5 requests.
- **Where you watch a run differs by design.** In our own loop, we print each turn to stdout. Google ADK provides `adk web`, an interactive browser workbench where you can inspect runs, events, and workflows visually. The OpenAI Agents SDK uploads traces directly to OpenAI's Traces dashboard. LangChain and LangGraph let you draw the compiled graph image directly in a notebook or terminal and stream node outputs step by step, or export to LangSmith (bonus B7). Pydantic AI gives instant CLI and web chat helpers (`to_cli_sync`, `to_web`). CrewAI streams verbose role-based logs to the console and draws flows with `plot()`. Microsoft Agent Framework streams workflow events from step to step.
- Token counts and costs across all these runs are gathered in the [Appendix](#appendix-tokens-requests-and-costs-across-frameworks) at the end of this guide.

**Important:** this is one question, one model and one run per framework. It shows that the loop is the same; it is
not a speed or quality benchmark, and we do not compare times, which are mostly the model's.

### Step 2: Find what each framework decided for us

The runs agree, but in every lab the framework made a choice we had not asked for, and the lab only saw it because
it printed what came back. These are the choices worth knowing before you adopt one:

| Framework | What it decided for us | Where a lab found it | What to do |
|---|---|---|---|
| OpenAI Agents SDK | No reasoning effort for our model's name, so the API ran every call at its default, `medium` | `07b`, Part A: the agent sets `ModelSettings` and prints `effort: none`; left out, this model runs at the API's default, `medium` | set `ModelSettings` on every agent |
| Google ADK | One run yields 5 events from 3 model calls, including separate function-call and function-response events | `08b`, Part A: event stream printed turn by turn | count the events that carry usage, not every event |
| LangChain | Once tools are bound, our model's calls go to the Responses API, and the answer's `content` is a list of blocks, not a string | `09b`, Part B: `.content.lower()` raises `AttributeError: 'list' object has no attribute 'lower'`; the response id starts `resp_` | read every reply with `.text` |
| LangGraph | A resume sent to a thread with nothing waiting starts a new run, with no error | `10b`, Part C: on 41 empty threads, 38 made up a customer name nobody asked for; the approval step stopped both | read `get_state(...).interrupts` before every resume |
| LlamaIndex | Left unset, `Settings` uses `gpt-3.5-turbo` and `text-embedding-ada-002`, not the models in `models.env` | `14a`, Part A: the defaults printed before ours were set | set `Settings.llm` and `Settings.embed_model` first |
| LlamaIndex | A query-engine tool makes a model call inside every search, which the agent never sees | `14b`, Going further: 5 model calls a run for query-engine tool against 3 for retriever tool | count calls inside tools with the instrumentation handler |
| Pydantic AI | A well-typed model object can still validate cleanly while containing invented customer data | `b3b`, Part B: misspelt *Helena Holy* returned a `DeskAnswer` with zero invoices and customer 0 | use a union with a `NotFound` type and check with an output validator |
| CrewAI | Two lookups in one reply run concurrently in `ThreadPoolExecutor` threads | `b4b`, Part A and README: concurrent lookups on a shared connection lock SQLite | give every tool its own database connection |
| Microsoft Agent Framework | `OpenAIChatClient` calls the Responses API, whatever its name suggests | `b5b`, Part A | read the provider's raw response, as the lab's session does |

**Key lesson:** a framework's defaults are written for its authors' usual case, not for your model, your prices or
your counts. Before you choose one, run one real request of yours through it and print the requests, the API it
used and the usage, as each of these labs did. A right answer tells you little; the run around it tells you what
you are buying.

**Checkpoint B.** You can say why every single agent made three requests, where you watch a run in each framework, and name one default that a lab had to find in each framework.

## Part C: Read the six criteria on the Chinook desk

A comparison needs criteria, and a criterion only helps when you know what it means for a real job. These six cover
what most projects ask of a framework. For each one: what it means in practice, the desk request that tests it, and
what this repository's runs show.

### 1. Easy to learn: a new developer runs a first agent in an afternoon

- **On the desk:** the Helena question, answered by someone who has never used the framework.
- **The evidence:** LangChain's `create_agent` (`09b`), and the Agents SDK's `Agent` with `Runner.run` (`07b`), each answer it in a
  few lines. Building the same agent by hand in LangGraph needs a state with a reducer, two nodes, a
  routing function and a back edge before it answers anything (`10b`, Part A). The result has the same nodes and
  edges as `create_agent`'s graph, and that is the point: LangGraph is what `create_agent` builds for you.
- **What it does not mean:** easy to start is not easy to run well. Most frameworks in Part B's second table were
  easy to start, and each still made a choice for us that a lab found only by printing the run.

### 2. Control of the loop: you can see and change every step the loop takes

- **On the desk:** stop at a turn cap; check a tool request before the tool runs; change what goes back to the model.
- **The evidence:** our own loop shows every line (`03b`). The Agents SDK stops at `max_turns` with
  `MaxTurnsExceeded` (`07a`, Part C), and a hand-built LangGraph graph routes with a function we write (`10b`,
  Part A). CrewAI hides the most: we wrote two tasks, and the crew decided how many requests to make (`b4a`, `b4b`).
- **When control matters:** an auditor asks why the agent did something, or a run fails in a way the framework's defaults do not handle.

### 3. Multi-agent: several agents can share work without code you write yourself

- **On the desk:** Puja Srivastava's question (6 invoices, \$36.64, Jane Peacock), split between an invoices
  specialist and a reps specialist.
- **The evidence:** in the Agents SDK, the two specialists used as tools answered all three facts in every run at
  8 model requests, against 3 for one agent with all three tools; wired as a handoff they lost the rep in every run
  (more than ten), because control passed to the invoices specialist, which has no rep tool (`07b`, Part C). In Google ADK, two `sub_agents` passed the conversation back and forth for 8 model calls (`08b`, Part C). Lab 18 measures when a
  second agent pays: on a request that names five customers, parallel sub-agents cost more in total, but the agent
  that writes the answer reads about a sixth of the context.
- **What it does not mean:** a framework that makes several agents easy also makes it easy to pay for agents you do
  not need. In Lab 18, one agent with three tools answered every desk request right.

### 4. Pause and approve: a run can stop, save its state, wait for a person and resume

- **On the desk:** the duplicate-charge refund. The agent proposes the refund; a person approves it; only then does
  the request reach the refund table.
- **The evidence:** five labs pause a refund, and they differ in where the pause is kept.
  - LangChain (`09b`, Part D): `HumanInTheLoopMiddleware` stops before `file_refund_request`. With a checkpointer it waits for an approval or rejection.
  - LangGraph (`10b`, Parts B, C and D): `interrupt` pauses inside the `review` node. With `SqliteSaver` the paused run survived a restart and was approved from a new graph object; with an `InMemorySaver` it was gone.
  - The Agents SDK (`b2b`, Parts C and F): a tool marked `needs_approval=True` pauses the run, and `RunState` saves the pending call so it can be restored. Approval alone wrote no row; the resumed run wrote one. `RunState.to_json()` saved the state to disk, and `RunState.from_json()` reloaded it.
  - LangGraph with durable workflows (`b1b`, Parts B, C and D): a refund review waits on disk across a real kernel restart. On resume, the paused node runs again from its first line, so the code before `interrupt()` ran twice: the review node inserted two rows into the `notices` table for `R-1001` until Part D checked the table first to make the notice safe to repeat.
  - Microsoft Agent Framework (`b5b`, Parts C, D and E): a workflow checkpoint saved to disk with `FileCheckpointStorage` restored the pending review in a new process (`resume_refund.py`); approval added one row, a repeated approval still left one row, and a rejection added none.
- **What it does not mean:** a pause that survives is not a resume that is safe to repeat. B1's duplicate notice shows code
  before the pause running twice, and B5 stayed at one row because the queue's key refuses a duplicate. The refund
  needs a key that makes a repeat harmless, whatever framework pauses it.

**Write down:** of the five pauses above, which would you trust with a refund that waits overnight, and what in its
run tells you? (Ours: Lab 10's `SqliteSaver`, B1's SQLite checkpoint or B5's file checkpoint, each approved from a
new process; B2's `RunState` too, once our code stores it in a database.)

### 5. Tracing built in: every model call and tool call is recorded without extra code

- **On the desk:** every refund the agent proposed, with the model calls and tool arguments behind it, kept for an
  audit.
- **The evidence:** the Agents SDK records a trace by default, and Lab 07 reads it on OpenAI's Traces page
  (`07a`, Part C). LlamaIndex's instrumentation handler saw every model call, including those inside a tool (`14b`, Going further). The Microsoft Agent Framework lab inspected workflow step events and session state to log each call (`b5a`, `b5b`). MLflow records OpenAI calls with one autolog line (Lab 20) and has the same for LangChain; LangSmith traces LangChain and LangGraph from environment variables (bonus B7, with an account).
- **In production:** a trace holds customer names and invoice numbers. Decide where traces may go before you turn
  one on.

### 6. Any model vendor: switching from one vendor to another is a setting

- **On the desk:** next year the shop wants to try another vendor's model on the same desk.
- **The evidence:** in this repository the model is one line in `models.env`, read by every lab. ADK, Google's
  framework, ran our OpenAI model with its own `OpenAIResponsesLlm` class (`08b`), but the lab does not
  pass the reasoning effort from `models.env` to ADK, so its agents ran at the model's default effort. The Agents
  SDK ran its weather agent on a Gemini model through LiteLLM (`07a`, Part G). A switch that works can still lose a setting you relied on.
- **What to check:** whether the framework talks to the other vendor directly or through an adapter (like LiteLLM), and which of the
  things you rely on (traces, cached-token counts, typed output) survive the switch.

### What the six criteria leave out

Some needs decide a pick on their own and are not on any scorecard:

- **The environment.** Only three labs have their own `pyproject.toml` environment in this repository: Lab 08 (`08_Google_ADK`), B4 (`bonus/B4_CrewAI_Crew`) and B5 (`bonus/B5_Microsoft_Agent_Framework`). Lab 14 (`14_LlamaIndex_RAG`) shares the root environment with the core labs. A framework comes with its dependencies, and conflicts force separate environments.
- **The team's language and cloud.** Microsoft Agent Framework serves Python and .NET; Google ADK integrates naturally with Google Cloud and Vertex AI. A TypeScript team looks at other frameworks altogether (Mastra, the Vercel AI SDK).
- **What the job is mostly about.** Answers from documents point to LlamaIndex (Lab 14). Typed answers that another
  system reads point to Pydantic AI (B3, where a validator rejected a well-typed refund decision that broke the
  policy, and the model repaired it). A chat page with one conversation per visitor fitted the Agents SDK's sessions
  (Lab 15).

**Checkpoint C.** For each criterion you can say what it means on the desk and name one run that shows it, and you
can name one need the six leave out.

## Part D: Score the frameworks for the support desk

Now we use the criteria on one job: first a scorecard, then the questions that turn a job into weights, then a
worked pick, then what would change it.

![How to choose a framework in five steps, each beside the Chinook support desk's answer: the six questions (a refund waits hours for a supervisor, every refund audited); filter on the must-haves (LangChain, LangGraph and Microsoft Agent Framework stay); weigh and add up (LangChain 33, LangGraph 32, Microsoft Agent Framework 33 of 36: the sum cannot separate them); read the evidence (a Python team, one gate, create_agent is a LangGraph graph); pick LangChain create_agent with an approval pause and a checkpointer that outlives the process](resources/lab11_choosing.png)

### Step 1: Read the scorecard

These scores are the instructor's assessment in October 2026, from building the desk in each framework (for
LlamaIndex, Lab 14's policy-search agent) and reading each one's documentation: a judgement, not a benchmark. 3 is
strong, 2 adequate, 1 weak.

| Framework | Easy to learn | Control of the loop | Multi-agent | Pause and approve | Tracing built in | Any model vendor |
|---|---|---|---|---|---|---|
| Your own loop | 3 | 3 | 1 | 1 | 1 | 3 |
| OpenAI Agents SDK | 3 | 2 | 2 | 2 | 3 | 2 |
| LangChain | 3 | 2 | 2 | 3 | 3 | 3 |
| LangGraph | 1 | 3 | 3 | 3 | 3 | 3 |
| LlamaIndex | 2 | 2 | 2 | 2 | 2 | 3 |
| CrewAI | 3 | 1 | 3 | 2 | 2 | 3 |
| Microsoft Agent Framework | 2 | 3 | 3 | 3 | 3 | 2 |
| Google ADK | 2 | 2 | 3 | 2 | 2 | 2 |
| Pydantic AI | 2 | 3 | 2 | 2 | 3 | 3 |

Read it across, not down: no framework wins every column. Your own loop is easy and fully in your hands, and weak on
the things a team needs later (several agents, a durable pause, traces). LangGraph is close to the reverse: hard to
learn, strong on control, pausing and several agents. LangChain's `create_agent` runs on LangGraph and trades some of
that control (you shape the loop through middleware instead of drawing it) for ease.

**Write down:** one score you disagree with, and the run or the documentation that supports your score. (There is no
worked answer to this one: the table is there to be argued with, and the Challenge asks you to re-score it for a
project of yours.)

### Step 2: Turn the job into must-haves and weights

Six questions turn a job into what the scorecard needs. We answer them for the desk:

| Question | The desk's answer | What it does to the scorecard |
|---|---|---|
| 1. Must a run pause for a person, or outlast one request? | Yes: a refund waits for a supervisor, who works through the queue twice a day, so a request waits hours and must survive a restart of the service | Pause and approve becomes a **must-have** |
| 2. Will several agents share the work? | Not yet: one agent, three lookups and a refund tool | Multi-agent, weight 1 |
| 3. Must it run on more than one model vendor? | No: OpenAI today | Any model vendor, weight 1 |
| 4. Who maintains it, and in which language? | Two Python developers, in this repository's environment | Easy to learn, weight 2 |
| 5. Do you need tracing from day one? | Yes: every refund is audited | Tracing built in becomes a **must-have** |
| 6. Or write your own loop? | Not here: the durable pause and the trace would be ours to build. But an auditor asks why each refund was proposed, so we still want to see each step | Control of the loop, weight 2 |

The rule: **a must-have is a filter, not a weight.** A framework that scores below 3 on a must-have needs code of
ours to fill the gap, and that code is what we wanted the framework for. In the sum, a must-have counts with weight
3, the highest weight, so a framework's total still shows how strong it is where the job needs it most.

### Step 3: Work the pick

**Filter first.** Pause and approve 3 and tracing built in 3: LangChain, LangGraph and Microsoft Agent Framework
stay. Every other row fails at least one.

**Then add up.** We add up every row anyway, to see what the filter did. Each score is multiplied by its weight
(easy to learn 2, control 2, multi-agent 1, pause and approve 3, tracing 3, any vendor 1), so the most a framework
can reach is 3 × 12 = 36. For LangChain:

$$3 \times 2 + 2 \times 2 + 2 \times 1 + 3 \times 3 + 3 \times 3 + 3 \times 1 = 6 + 4 + 2 + 9 + 9 + 3 = 33$$

| Framework | Pause and approve | Tracing built in | Passes the filter | Weighted total, out of 36 |
|---|---|---|---|---|
| Your own loop | 1 | 1 | no | 22 |
| OpenAI Agents SDK | 2 | 3 | no | 29 |
| LangChain | 3 | 3 | yes | 33 |
| LangGraph | 3 | 3 | yes | 32 |
| LlamaIndex | 2 | 2 | no | 25 |
| CrewAI | 2 | 2 | no | 26 |
| Microsoft Agent Framework | 3 | 3 | yes | 33 |
| Google ADK | 2 | 2 | no | 25 |
| Pydantic AI | 2 | 3 | no | 30 |

Notice Pydantic AI at 30 and the Agents SDK at 29: on the sum alone they would stay in the race, though neither
keeps a paused run for hours without code of ours. That is why the filter comes first.

**Then read the evidence.** The three that pass are within one point, so the sum cannot separate them. The labs'
runs and the needs the scorecard leaves out can:

- **The Agents SDK** already runs the shop's chat page (Lab 15), and that counts for it, but it failed the filter: a
  refund that waits hours needs a saved `RunState` that our own code stores and reloads (`b2b`).
- **Microsoft Agent Framework** fits on paper, but its particular strengths, .NET and Azure, are not this team's, and
  it needs an environment of its own (`b5b`). Its approval also lives in a workflow apart from the agent (`b5b`, Part D:
  `check → review → queue`, with no model inside).
- **LangGraph by hand** gives the most control, but the desk is one agent with one gate. Drawing the graph ourselves
  costs ease (a 1) for control the desk does not need yet (`10b`).
- **LangChain's `create_agent`** returns a LangGraph graph (`09b`, Part A: a `CompiledStateGraph`), pauses before
  the refund tool with `HumanInTheLoopMiddleware` (`09b`, Part D), and keeps the paused run in a checkpointer that outlives the process (`09b`, `10b`). If the refund flow grows more gates, the same graph can be written by hand without changing
  frameworks (`10b`, Part A: the hand-built graph has the same nodes and edges).

**The pick:** LangChain's `create_agent`, with `HumanInTheLoopMiddleware` in front of `file_refund_request` and a
checkpointer on a database the service keeps (`SqliteSaver` in Lab 09 and Lab 10; on a server, one such as `PostgresSaver`).

### Step 4: Say what would change the pick

A pick is only as good as the answers behind it, so write down which answer, if it changed, would change the pick.

- **If the rep approves on the spot,** in the same session, the pause no longer has to outlast the process. Pause
  and approve drops from a must-have to a weight, and the Agents SDK's `needs_approval` (`b2b`) does the job. LangChain
  still adds up higher, but only because it scores 3 on two things this version of the job does not use (a pause
  that outlives the process, and a second vendor). Points for a strength the job does not need are not a reason;
  what already runs is, and the shop's chat page already runs on the Agents SDK (Lab 15). Start there, and move to
  LangChain or LangGraph when a refund must wait overnight.
- **If the team works in .NET or on Azure,** Microsoft Agent Framework.
- **If the refund flow grows gates** (an amount above which a second person approves, a retry when the payment system
  is down), LangGraph by hand: the same kind of graph, drawn by us (`10b`).
- **If the shop wants a second model vendor,** the vendor weight rises to 3 and Microsoft Agent Framework (a 2 there)
  falls behind LangChain and LangGraph; made a must-have, it drops out.
- **Stay with your own loop** for a few tools, one vendor, every step explained to an auditor, or a loop that is
  itself the thing you need to see. Labs 16 and 19 keep their own loop for that reason: the step each one teaches (a
  file write and a test run; a check before a tool runs) is a line we need in front of us.

**Checkpoint D.** You can say why must-haves filter before the weights are added up, reproduce one weighted total,
give the desk's pick with the reason that breaks the tie, and name the one answer that turns the pick into the
Agents SDK.

## Part E: Decide what a wrong pick costs and what changes later

The framework is the part of an agent most likely to change while the job stays the same. What a change costs depends on what you built on top of it.

### Step 1: Separate what moves from what stays behind

| Part of the desk | Moves to another framework when ... | Stays behind when ... |
|---|---|---|
| The three lookups | they are plain Python functions, or behind an MCP server (Lab 06) | they are written as one framework's tool classes |
| The instructions | they are a string in your repository | they are spread over one framework's prompt templates or a crew's role texts |
| The definition | always: a model, instructions and tools (Part A) | |
| Checks and approvals | they are your own functions, called by the framework | they are written as one framework's middleware, guardrails or validators |
| Paused runs and conversations | you let them finish before the switch | they sit in one framework's checkpoint or session tables (Lab 10's `checkpoints.db`, Lab 07's `sessions.db`) |
| Traces | they are exported in an open format (OpenTelemetry's conventions for generative AI, Lab 23) | they can only be read in one framework's tracing service |
| Your tests | always, if they check facts and tool calls instead of one framework's objects (Lab 20's golden set) | |

**Key lesson:** keep the tools, the instructions and the tests outside the framework, and a wrong pick costs the glue
between them: the few lines that define the agent, and the code that pauses and traces it. Keep them inside, and it
costs a rewrite.

**Write down:** if the desk moved from LangChain to Microsoft Agent Framework in a year, which rows of this table
would have to move by hand? (Ours: the approval, rebuilt as a workflow step, and any paused refunds, approved or
rejected before the switch. The lookups, instructions and tests move as they are.)

### Step 2: Read what changed in the last year

Frameworks change faster than the jobs they serve. Some changes of the last year, from the maintainers' own pages
(checked 5 November 2026):

- [AutoGen](https://github.com/microsoft/autogen) is in maintenance mode: its README says it "will not receive new
  features or enhancements and is community managed going forward", and calls Microsoft Agent Framework "the
  enterprise-ready successor to AutoGen". [Microsoft Agent Framework](https://pypi.org/project/agent-framework/)
  reached 1.0.0 on 2 April 2026.
- [`langgraph-supervisor`](https://github.com/langchain-ai/langgraph-supervisor-py), a library for one supervisor
  agent over several others, was archived on 20 September 2026; its README now recommends "using the supervisor
  pattern directly via tools rather than this library for most use cases".
- [ADK's documentation](https://adk.dev/agents/workflow-agents/) says that from ADK 2.0 for Python and Go, its
  sequential, parallel and loop "template workflows have been superseded" by graph-based and dynamic workflows.
- OpenAI's Assistants API [shut down on 26 August 2026](https://developers.openai.com/api/docs/deprecations); Lab 23,
  Part E reads what moved to its replacement and what did not.

The versions this repository pins (in the root environment checked on 11 November 2026 and the three own environments of Labs 08, B4 and B5):
`openai-agents` 0.24.0, `langchain` 1.4.10, `langgraph` 1.2.20, `llama-index-core` 0.14.25, `google-adk` 2.14.0,
`pydantic-ai-slim` 2.68.0, `crewai` 1.15.40 and `agent-framework` 1.25.0. Two of them, `openai-agents` and
`llama-index-core`, are below 1.0 (pinned at 0.24.0 and 0.14.25),
and under [semantic versioning](https://semver.org/) a version below 1.0 promises no stable interface: a minor
release may change one.

What survived each of these changes was the definition and the tools; what was frozen, archived or rebuilt was a
framework or an add-on around them (a whole framework, a supervisor library, a template workflow, a hosted
assistant). Prefer a framework's core loop and your own code over its newest add-on, unless the add-on is the reason
you chose the framework.

### Step 3: Read popularity for what it measures

Checked 30 October 2026: stars from each project's GitHub page, downloads from [pypistats.org](https://pypistats.org/)
for the 30 days to 29 October 2026.

| Framework | Maintainer, licence | First release | GitHub stars | PyPI downloads, last 30 days |
|---|---|---|---|---|
| [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | OpenAI, MIT | Mar 2025 | 30.4k | 12.45M (`openai-agents`) |
| [LangChain](https://github.com/langchain-ai/langchain) | LangChain Inc, MIT | Oct 2022 | 148.7k | 170.46M (`langchain`) |
| [LangGraph](https://github.com/langchain-ai/langgraph) | LangChain Inc, MIT | 2024 | 44.0k | 44.77M (`langgraph`) |
| [LlamaIndex](https://github.com/run-llama/llama_index) | LlamaIndex, MIT | Nov 2022, as `gpt-index` | 52.6k | 6.57M (`llama-index-core`) |
| [CrewAI](https://github.com/crewAIInc/crewAI) | CrewAI Inc, MIT | Nov 2023 | 60.2k | 2.44M (`crewai`) |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | Microsoft, MIT | 1.0 in Apr 2026 | 14.4k | 0.19M (`agent-framework`) |
| [Google ADK](https://github.com/google/adk-python) | Google, Apache-2.0 | Mar 2025 | 22.0k | 10.11M (`google-adk`) |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | Pydantic, MIT | Oct 2024 | 20.9k | 5.38M (`pydantic-ai`) |

In the [Stack Overflow Developer Survey 2026](https://survey.stackoverflow.co/2026/ai) (published 6 October 2026),
30% of respondents reported using LangChain for agent orchestration and 24% the OpenAI Agents SDK.

Each number measures something different:

- **Stars** measure attention: how many people marked the project on GitHub, not how many run it.
- **Downloads** count every install, including those pulled in by other packages. A library that other packages
  depend on ranks high, whether or not anyone builds an agent with it.
- **A survey share** counts what respondents used, among those who answered that question.

Popularity buys real things: answers to your error message, examples, integrations, and people who already know the
framework. It does not buy fit. LangChain has about ten times the stars of Microsoft Agent Framework, and in Part D
the two tied; what separated them was the team's language and the shape of the approval.

**Checkpoint E.** For each part of the desk you can say whether it moves to another framework and on what condition,
name one change from the last year and what it left behind, and say what stars, downloads and a survey share each
measure.

## Part F: Choose for three jobs

This worksheet uses everything above on three more jobs at the shop. For each one, write: the six questions answered
in a line each, the must-haves, your pick, and the reason that breaks any tie. Some jobs have more than one
defensible answer; what matters is the reason.

1. **Policy answers for reps.** Reps ask questions such as *"Can a customer return an unopened CD after 40 days?"*
   and *"How long does a refund take?"*, answered from the shop's 20 policy files and 16 tickets, with the file
   named. The agent writes nothing. OpenAI only, a Python team.
2. **A front door for customer email.** Each incoming message goes to the one team that owns it (billing, shipping or
   technical support), and from then on that team's agent talks to the customer. Each team maintains its own agent.
   Python, OpenAI only.
3. **Month-end refund reconciliation.** The finance systems team, who write C# on Azure, want an agent that matches
   the month's refunds against invoices and proposes corrections. A controller approves each batch, often days later
   and after the service has been redeployed; every proposal is audited.

<details>
<summary><b>Worked answers</b> (open after you have written yours)</summary>

**1. Policy answers for reps.**

- Must-haves: none from the scorecard. No pause (nothing is written), one vendor, tracing useful but not a must
  (weight 2). What the job is mostly about is documents, which the scorecard leaves out.
- Pick: **LlamaIndex**, with a retriever tool. In Lab 14 (`14b`), the retriever-tool agent was right in every run
  (10 of 10 with a plain prompt, 5 of 5 with a sharper one) at about 3 to 4 model calls a run.
- Watch: the query-engine tool, LlamaIndex's other way to give an agent the documents, makes a model call inside
  every search; with a plain prompt it found the rule file in 3 of 10 runs at 5 to 6.2 calls a run.
- Also defensible: **your own loop with a search tool**, as Lab 13 builds it, if the team wants no new dependency
  (though LlamaIndex now shares the repository's root environment).

**2. A front door for customer email.**

- Must-haves: none. Several agents share the work (multi-agent, weight 3), each team maintains its own
  (easy to learn, weight 2), and tracing matters (weight 2); pause, vendor and control weigh 1.
- The sum, out of 30: Microsoft Agent Framework 27, LangChain and LangGraph 26, CrewAI 25, the Agents SDK and
  Pydantic AI 24, Google ADK 23. Seven frameworks within four points, so the evidence decides.
- Re-score one cell: "multi-agent" averages several patterns (a supervisor, a crew, a graph, a handoff). This job
  needs one of them, a **handoff**, where one specialist takes the conversation for good. In the Agents SDK a handoff
  is a first-class object, and Lab 07 measured both where it fits (the triage agent handed the rep-only question to
  the reps specialist, which answered it) and where it fails. Scored on this pattern the SDK's cell is a 3, and its
  total 27.
- Pick: **the OpenAI Agents SDK with handoffs**, level with Microsoft Agent Framework on the sum and ahead on ease,
  which matters when three teams each maintain an agent; it also runs in this repository's environment.
- Watch: a message with two destinations loses its second half after a handoff (`07b`, Part C: the rep missing in
  every run). Route such messages to a manager that calls the specialists as tools, or split them in code first.
- Also defensible: if the teams' agents run on different platforms, the agents talk over A2A (Lab 23, Part B), and
  each team chooses its own framework.

**3. Month-end refund reconciliation.**

- Must-haves: pause and approve (days, across redeploys) and tracing (every proposal audited). Language: C#.
- Filter: LangChain, LangGraph and Microsoft Agent Framework pass; of these only Microsoft Agent Framework serves
  .NET.
- Pick: **Microsoft Agent Framework**, with the approval as a workflow step and its checkpoints in storage the
  service keeps (`b5b` restored a pending review in a new process).
- Watch: restoring a checkpoint can repeat a step. Give each correction a business key so that a repeated approval
  writes nothing new (`b5b`: a repeated approval still left one row, because of the queue's key).

</details>

**Checkpoint F.** For job 1 your reason names documents, the need the scorecard leaves out; for job 2 you asked which
multi-agent pattern the job needs (a handoff) before trusting the multi-agent column; for job 3 your must-haves are
pause and tracing, and your pick is Microsoft Agent Framework or comes with a reason that names the team's
language.

## What you can do now

- Recognise the four steps of the agent loop inside any framework, and point at the model, instructions and tools in
  its agent definition.
- Read a framework's run as model requests, tokens and tool calls, and say where you watch runs in each framework.
- Explain why LiteLLM sits under frameworks to adapt model calls rather than acting as an agent framework itself.
- Find what a framework decides for you by printing what comes back, and name one such decision per framework this
  repository uses.
- Say what each of the six criteria means on a real job, with a run that shows it, and name the needs the six leave
  out.
- Turn a job into must-haves and weights, filter and add up, break a tie with evidence, and write down the answer
  that would change the pick.
- Say which parts of an agent move to another framework and which stay behind, and keep the expensive ones outside
  the framework.

## Challenge

1. **Choose for a project of yours.** Take an agent your team is building or considering. Write the six questions'
   answers, the must-haves and the weights; re-score at least two cells of the scorecard you disagree with, each with
   a run or a documentation page that supports your score; then filter, add up, break any tie with a reason, and
   write the one answer that would change your pick. *Expected outcome:* a filled-in scorecard with your weights and
   totals, a pick that passes your filter, a tie-break that names evidence or a need the scorecard leaves out (not a
   bigger total alone), and one sentence starting "We would change this pick if ...".
2. **Re-check one fact for your pick.** Open your pick's PyPI page and GitHub page. Write today's date, its latest
   version and release date, and its stars, beside the values in Part E. *Expected outcome:* each value confirmed or
   corrected with today's date, and one sentence on whether anything you found (a 1.0 release, an archived add-on, a
   new way to pause or trace) changes one of your scores.

A worked answer for both tasks, for a damaged-media desk at the Chinook shop, is in
`solved/11_choose_a_framework_solution.md`.

## Appendix: Tokens, requests and costs across frameworks

Every measured number below comes directly from the saved checkpoint in the named lab's final `README.md`. All runs
used `gpt-6-luna` at `REASONING_EFFORT=none`.

| Framework | Lab notebook | Model requests | Checkpoint input / output tokens | Measured cost | Checkpoint notes |
|---|---|---|---|---|---|
| Our own loop | `03b`, Part A | 3 | 994–1,006 in / 95 out | \$0.000148 | Helena lookup: input tokens grew per turn (259, 316, 419) on Chat Completions API |
| OpenAI Agents SDK | `07b`, Part A | 3 | 845 in / 98 out | \$0.000133 | Helena lookup: input tokens grew per request (206, 264, 375) on Responses API |
| Google ADK | `08b`, Part A | 3 | 894 in | — | Helena lookup: input tokens grew per call (221, 281, 392) across 5 events |
| LangChain | `09b`, Part A | 3 | 725 in / 98 out | \$0.000121 | Helena lookup: input tokens grew per call (166, 224, 335) across 7 messages |
| LangGraph | `10b`, Part A | 3 | 725 in / 98 out | \$0.000121 | Helena lookup: 166, 224, 335 in; 21, 52, 25 out |
| Pydantic AI | `b3b`, Part A | 3 | 872 in / 109 out | — | Helena lookup: typed `DeskAnswer` returned after `find_customer`, `get_invoices`, `get_support_rep` |
| Microsoft Agent Framework | `b5b`, Part A | 3 | 906–912 in / 103 out | — | Puja Srivastava three-fact lookup; calls Responses API |
| CrewAI | `b4b`, Part C & D | 3 (desk Part C), 4 (with guardrail) | 1,692 in / 225 out (Part D) | \$0.00028 | Two-agent refund advice for Puja's invoice 229; playground (`b4a` Part E) took 5 requests (2,872 in / 214 out) |
| LlamaIndex | `14b`, Checkpoints | 3 (retriever tool) vs 5 (query engine) | — | — | Retriever tool hands back raw text; query engine adds hidden model call per search |
| LangGraph Durable Workflows | `b1b`, Checkpoints | 0 (no model) | — | — | Demonstrates state persistence: `notices` table held 2 rows after restart until made safe to repeat |
| Agents SDK Guardrails | `b2b`, Checkpoints | — | — | — | `needs_approval=True` pauses before tool; `paused_refund.json` saved and reloaded across processes |

**Why the input tokens differ for the same three facts:**
The three lookups and the system prompt are identical. The difference comes from:
1. **The API called:** Chat Completions (`03b`: 994–1,006 tokens) formats messages and tool definitions differently from the Responses API (`07b`: 845 tokens; `09b` and `10b`: 725 tokens).
2. **Schema overhead:** Different libraries serialize function signatures and docstrings with varying verbosity.
3. **Multi-agent context multiplication:** In CrewAI (`b4b`) and multi-agent setups (`07b` Part C, `08b` Part C), passing task context or transferring turns multiplies tokens across agents (taking 4 to 8 requests instead of 3).

## Resources

- OpenAI Agents SDK: [documentation](https://openai.github.io/openai-agents-python/),
  [agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/),
  [tracing](https://openai.github.io/openai-agents-python/tracing/),
  [guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)
- LangChain and LangGraph: [agents](https://docs.langchain.com/oss/python/langchain/agents),
  [human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop),
  [checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers),
  [multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent)
- LlamaIndex: [agents](https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/),
  [instrumentation](https://developers.llamaindex.ai/python/framework/module_guides/observability/instrumentation/)
- CrewAI: [agents](https://docs.crewai.com/en/concepts/agents), [crews](https://docs.crewai.com/en/concepts/crews)
- Microsoft Agent Framework: [human input in workflows](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop),
  [workflow checkpoints](https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints),
  [migrating from AutoGen](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/)
- Google ADK: [agents](https://adk.dev/agents/llm-agents/)
- Pydantic AI: [agents](https://pydantic.dev/docs/ai/core-concepts/agent/),
  [output validators](https://pydantic.dev/docs/ai/core-concepts/output/#output-validators)
- LiteLLM: [documentation](https://docs.litellm.ai/docs/)
- [Stack Overflow Developer Survey 2026, AI](https://survey.stackoverflow.co/2026/ai) and
  [Semantic Versioning](https://semver.org/)
