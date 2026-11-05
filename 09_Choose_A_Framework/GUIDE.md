# Lab 09: How to choose an agent framework

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
- How to find what a framework decides for you (which API it calls, a default model, a reasoning effort, what it
  counts) before that decision reaches production.
- What six criteria (easy to learn, control of the loop, multi-agent, pause and approve, tracing built in, any model
  vendor) mean in practice, with the evidence from this repository's runs.
- How to turn a job's needs into must-haves and weights, score the frameworks for it and reach a pick.
- When your own loop is the right choice, and which answer would make you change a pick later.
- What a wrong pick costs, and which parts of an agent move to another framework and which stay behind.

## Before you start

This is a reading guide: there is no code to run, nothing to install and no key to set. You need a text editor or a
sheet of paper, because every step asks you to write something down before you read our answer.

The guide uses the agent this course builds, the support desk of the Chinook music shop, and two of its requests:

- **The Helena question:** *How many invoices does Helena Holý have, what do they add up to, and who is her support
  rep?* The database says customer 6, 7 invoices, $49.62 and Steve Johnson. Three lookups answer it:
  `find_customer`, `get_invoices` and `get_support_rep`.
- **The duplicate-charge refund:** ticket 14 reports two invoices for the same digital album on the same day, $9.99
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

Lab 04 wrote the agent loop by hand. It does four things:

1. Send the messages and the tool schemas to the model.
2. If the reply asks for tools, run them with our own Python and append each result to the messages.
3. Repeat until the reply is an answer, or a turn cap stops the run.
4. Record what happened: each call's tokens, each tool's arguments and result.

Every framework in this guide runs these four steps for us. Each also writes the tool schemas from our functions'
type hints and docstrings: lab 07 printed the Agents SDK's schema for `find_customer` beside the one lab 03 wrote by
hand, and they matched. What no framework takes over is what makes the desk ours: the three lookups, the
instructions, and every check on what the agent may do.

**Write down:** which of the four steps would you least like to write again, and why? (Ours: step 4. The loop is a
dozen lines; recording every call in a form an auditor can read is the part that grows.)

### Step 2: Read the desk agent's definition in seven frameworks

Here is the line that defines the desk agent in each lab, copied from its notebook. `SYSTEM` holds the
instructions, `MODEL` the model's name from `models.env`, and the tool list the three lookups.

| Framework | Lab | The definition |
|---|---|---|
| OpenAI Agents SDK | 07, Part B | `Agent(name="Desk", instructions=SYSTEM, model=MODEL, tools=DESK_TOOLS, model_settings=SETTINGS)` |
| LangChain | 08, Part B | `create_agent(llm, TOOLS, system_prompt=SYSTEM)` |
| Google ADK | B3, Part C | `LlmAgent(name="Desk", model=adapter, instruction=SYSTEM, tools=[find_customer, get_invoices, get_support_rep], output_key="last_answer", ...)` |
| Pydantic AI | B4, Part C | `Agent(model, name="Chinook desk", deps_type=DeskDeps, output_type=DeskAnswer, instructions=..., model_settings=model_settings, retries=2)`, then `desk.tool(...)` for each lookup |
| Microsoft Agent Framework | B6, Part B | `Agent(client=client, name="Desk", instructions=..., tools=tools, default_options=OPTIONS)` |
| LlamaIndex | 12, Part G | `FunctionAgent(tools=[rt_tool], llm=llm, system_prompt=PROMPT)`: a search agent over the shop's policies, not the lookups |
| CrewAI | B5, Part C | two `Agent`s, each with a `role`, a `goal` and its own tools, two `Task`s, and `Crew(agents=[billing, support], tasks=[invoices_task, support_task], process=Process.sequential)` |

**Write down before reading on:** which three things does every row ask for?

A model, instructions and tools. Five of the seven rows are one constructor call; Pydantic AI adds each lookup
afterwards with `desk.tool(...)`, and CrewAI describes the same desk as two roles with a task each, because
describing work as roles and tasks is what CrewAI is for. The extra fields say what each framework adds or needs:

- `model_settings` in the Agents SDK: without it the SDK sends no reasoning effort for our model (Part B shows what
  that costs to miss).
- `output_type` and `deps_type` in Pydantic AI: the answer is checked against a Python type, and the database
  connection is passed in as a dependency instead of sitting in a global variable.
- `output_key` in ADK: the final answer is also saved in the session's state, under that key.
- `client` in Microsoft Agent Framework: the model's provider is an object of its own, configured once.

**Key lesson:** an agent's definition is small and nearly the same in every framework. Moving the definition to
another framework is a few lines of work. What costs more to move is everything built around it, which Part E
comes back to.

**Checkpoint A.** You can say which four things every framework does for us, which three things every definition
asks for, and what one extra field adds in three of the rows.

## Part B: Compare the same agent's runs across frameworks

If every framework runs the same loop, the runs should look alike. This part checks that on the Helena question,
then looks for what differs.

### Step 1: Put the runs side by side

| Built with | Where the saved run is | Model requests | Input / output tokens | All three facts |
|---|---|---|---|---|
| Our own loop, on Chat Completions | lab 04, Parts B and D | 3 | 1,006 / 95 | yes |
| OpenAI Agents SDK | lab 07, Part C | 3 | 845 / 98 | yes |
| LangChain `create_agent` | lab 08, Part B | 3 (counted from the messages) | not printed in that lab | yes |
| LangGraph, the same graph built by hand | lab 08, Part D | same nodes and edges as `create_agent` | not printed | yes |
| Google ADK, through LiteLLM | B3, Part D | 3 | 1,127 / 95 | yes |
| Pydantic AI | B4, Part C | 3 | 872 / 109 | yes |
| Microsoft Agent Framework | B6, Part C | 3 | 912 / 103 | yes |
| CrewAI, two specialists | B5, Part E | 5 | 2,872 / 214 | yes |

Read the table in three passes.

- **The requests are the same.** Every build with one agent made three model requests: `find_customer` first, then
  `get_invoices` and `get_support_rep` together in one reply, then the answer. That is lab 04's loop, whichever
  framework runs it. CrewAI's five come from its design: two specialists, each running its own loop over its own
  tools, and a step that turns the last answer into a typed object. Two tasks are not two requests.
- **The tokens differ, by more than you might expect.** Labs 04, 07 and B3 send the same instructions and the same
  three lookups, yet their input totals are 1,006, 845 and 1,127. The difference is what each one sends around our
  text: the API it calls (Chat Completions in lab 04, the Responses API in lab 07), the form of the schemas it writes,
  and in B3 the LiteLLM adapter between ADK and the model. (B4, B5 and B6 write their own instructions, so their
  tokens are not compared here.)
- **The cost difference decides nothing here.** At the prices in `models.env` these three runs cost $0.000148
  (lab 04), $0.000133 (lab 07) and $0.000160 (B3): fractions of a cent. Tokens matter at volume, and Part C shows
  where a design multiplies them (a second agent); a third more tokens on one request is not a reason to choose a
  framework.

**Important:** this is one question, one model and one run per framework. It shows that the loop is the same; it is
not a speed or quality benchmark, and we do not compare times, which are mostly the model's.

### Step 2: Find what each framework decided for us

The runs agree, but in every lab the framework made a choice we had not asked for, and the lab only saw it because
it printed what came back. These are the choices worth knowing before you adopt one:

| Framework | What it decided for us | Where a lab found it | What to do |
|---|---|---|---|
| OpenAI Agents SDK | No reasoning effort for our model's name, so the API ran every call at its default, `medium` | lab 07, Part D: the effort read from each response in the trace, `medium` without `model_settings` and `none` with it | set `ModelSettings` on every agent, and read the effort used from the trace |
| LangChain | Once tools are bound, our model's calls go to the Responses API, and the answer's `content` is a list of blocks, not a string | lab 08, Part C: `.content.lower()` raises `AttributeError: 'list' object has no attribute 'lower'`; the response id starts `resp_` | read every reply with `.text` |
| LangGraph | A resume sent to a thread with nothing waiting starts a new run, with no error | lab 08, Part G: on five empty threads, two proposed a refund nobody asked for; the approval step stopped both | read `get_state(...).interrupts` before every resume |
| LlamaIndex | Left unset, `Settings` uses `gpt-3.5-turbo` and `text-embedding-ada-002`, not the models in `models.env` | lab 12, Part C: the defaults printed before ours were set | set `Settings.llm` and `Settings.embed_model` first |
| LlamaIndex | A query-engine tool makes a model call inside every search, which the agent never sees | lab 12, Part H, plain prompt: 6.2 model calls a run against 4.1 for a retriever tool, and the rule file found in 3 of 10 runs against 10 of 10 | count calls inside tools with the instrumentation handler |
| Google ADK | One run yields 5 events and stores 6, from 3 model requests | B3, Part D | count requests from the usage records, not from events |
| CrewAI | Two tasks made 5 model requests, and its usage summary leaves out cache-write tokens | B5, Part E and its README | price the run from the requests, with a bound for cache writes |
| Microsoft Agent Framework | `OpenAIChatClient` calls the Responses API, whatever its name suggests | B6, Part A | read the provider's raw response, as the lab's middleware does |

**Key lesson:** a framework's defaults are written for its authors' usual case, not for your model, your prices or
your counts. Before you choose one, run one real request of yours through it and print the requests, the API it
used and the usage, as each of these labs did. A right answer tells you little; the run around it tells you what
you are buying.

**Checkpoint B.** You can say why every single agent made three requests and the CrewAI desk five, why the same
instructions cost 845 to 1,127 input tokens in three builds, and name one default that a lab had to find in each of
three frameworks.

## Part C: Read the six criteria on the Chinook desk

A comparison needs criteria, and a criterion only helps when you know what it means for a real job. These six cover
what most projects ask of a framework. For each one: what it means in practice, the desk request that tests it, and
what this repository's runs show.

### 1. Easy to learn: a new developer runs a first agent in an afternoon

- **On the desk:** the Helena question, answered by someone who has never used the framework.
- **The evidence:** LangChain's `create_agent`, and the Agents SDK's `Agent` with `Runner.run`, each answer it in a
  few lines (labs 08 and 07). Building the same agent by hand in LangGraph needs a state with a reducer, two nodes, a
  routing function and a back edge before it answers anything (lab 08, Part D). The result has the same nodes and
  edges as `create_agent`'s graph, and that is the point: LangGraph is what `create_agent` builds for you.
- **What it does not mean:** easy to start is not easy to run well. Most frameworks in Part B's second table were
  easy to start, and each still made a choice for us that a lab found only by printing the run.

### 2. Control of the loop: you can see and change every step the loop takes

- **On the desk:** stop at a turn cap; check a tool request before the tool runs; change what goes back to the model.
- **The evidence:** our own loop shows every line (lab 04). The Agents SDK stops at `max_turns` with
  `MaxTurnsExceeded` (lab 07, Part C), and a hand-built LangGraph graph routes with a function we write (lab 08,
  Part D). CrewAI hides the most: we wrote two tasks, and the crew decided they took five requests (B5).
- **Why it matters:** control is what you need when an auditor asks why the agent did something, and when a run goes
  wrong in a way the framework's defaults do not cover.

### 3. Multi-agent: several agents can share work without code you write yourself

- **On the desk:** Puja Srivastava's question (6 invoices, $36.64, Jane Peacock), split between an invoices
  specialist and a reps specialist.
- **The evidence:** in the Agents SDK, the two specialists used as tools answered all three facts in 5 of 5 runs at
  8 model requests, against 3 for one agent with all three tools; wired as a handoff they lost the rep in 5 of 5,
  because control passed to the invoices specialist, which has no rep tool (lab 07, Part F). Lab 16 measures when a
  second agent pays: on a request that names five customers, parallel sub-agents cost more in total, but the agent
  that writes the answer reads about a sixth of the context.
- **What it does not mean:** a framework that makes several agents easy also makes it easy to pay for agents you do
  not need. In lab 16, one agent with three tools answered every desk request right.

### 4. Pause and approve: a run can stop, save its state, wait for a person and resume

- **On the desk:** the duplicate-charge refund. The agent proposes the refund; a person approves it; only then does
  the request reach the refund table.
- **The evidence:** four labs pause a refund, and they differ in where the pause is kept.
  - LangChain and LangGraph (lab 08, Parts F and G): `HumanInTheLoopMiddleware` stops before `file_refund_request`.
    With a `SqliteSaver` the paused run survived a kernel restart and was approved from the new kernel; with an
    `InMemorySaver` it was gone.
  - The Agents SDK (B2): a tool marked `needs_approval` pauses the run, and `RunState` saves the pending call so it
    can be restored. Approval alone wrote no row; the resumed run wrote one. Where that saved state is kept is our
    code's job.
  - LangGraph with no model (B1): a refund review waits on disk across a restart, and on resume the paused node runs
    again from its first line, so the code before `interrupt()` ran twice (its counter went from 1 to 2).
  - Microsoft Agent Framework (B6): a workflow checkpoint restored the pending review in a new process; approval
    added one row, a repeated approval still left one row, and a rejection added none.
- **What it does not mean:** a pause that survives is not a resume that is safe to repeat. B1's counter shows code
  before the pause running twice, and B6 stayed at one row because the queue's key refuses a duplicate. The refund
  needs a key that makes a repeat harmless, whatever framework pauses it.

**Write down:** of the four pauses above, which would you trust with a refund that waits overnight, and what in its
run tells you? (Ours: lab 08's `SqliteSaver`, B1's SQLite checkpoint or B6's file checkpoint, each approved from a
new process; B2's `RunState` too, once our code stores it.)

### 5. Tracing built in: every model call and tool call is recorded without extra code

- **On the desk:** every refund the agent proposed, with the model calls and tool arguments behind it, kept for an
  audit.
- **The evidence:** the Agents SDK records a trace by default; lab 07 kept it in the notebook with its own trace
  processor (a `task`, an `agent`, then one `turn` per model call with its tool spans). LlamaIndex's instrumentation
  handler saw every model call, including those inside a tool (lab 12). The Microsoft Agent Framework lab added a chat
  middleware to log each provider call (B6). MLflow records OpenAI calls with one autolog line (lab 18) and has the
  same for LangChain; LangSmith traces LangChain from environment variables (bonus B8, with an account).
- **In production:** a trace holds customer names and invoice numbers. Decide where traces may go before you turn
  one on.

### 6. Any model vendor: switching from one vendor to another is a setting

- **On the desk:** next year the shop wants to try another vendor's model on the same desk.
- **The evidence:** in this repository the model is one line in `models.env`, read by every lab. ADK ran our OpenAI
  model through LiteLLM, an adapter (B3), and the run worked, but the adapter kept no cache-write count, so the
  lab's cost became an upper estimate. A switch that works can still lose something you were measuring.
- **What to check:** whether the framework talks to the other vendor directly or through an adapter, and which of the
  things you rely on (traces, cached-token counts, typed output) survive the switch.

### What the six criteria leave out

Some needs decide a pick on their own and are not on any scorecard:

- **The environment.** Four frameworks could not share one Python environment with the rest of this repository: lab
  12 (LlamaIndex's OpenAI integration needs version 2 of the `openai` library, and the core environment pins version
  3), B3 (ADK), B5 (CrewAI) and B6 (Microsoft Agent Framework) each have their own. A framework comes with its
  dependencies.
- **The team's language and cloud.** Microsoft Agent Framework serves Python and .NET; Google ADK deploys to Google
  Cloud. A TypeScript team looks at other frameworks altogether (Mastra, the Vercel AI SDK).
- **What the job is mostly about.** Answers from documents point to LlamaIndex (lab 12). Typed answers that another
  system reads point to Pydantic AI (B4, where a validator rejected a well-typed refund decision that broke the
  policy, and the model repaired it). A chat page with one conversation per visitor fitted the Agents SDK's sessions
  (lab 13).

**Checkpoint C.** For each criterion you can say what it means on the desk and name one run that shows it, and you
can name one need the six leave out.

## Part D: Score the frameworks for the support desk

Now we use the criteria on one job: first a scorecard, then the questions that turn a job into weights, then a
worked pick, then what would change it.

![How to choose a framework in five steps, each beside the Chinook support desk's answer: the six questions (a refund waits hours for a supervisor, every refund audited); filter on the must-haves (LangChain, LangGraph and Microsoft Agent Framework stay); weigh and add up (LangChain 33, LangGraph 32, Microsoft Agent Framework 33 of 36: the sum cannot separate them); read the evidence (a Python team, one gate, create_agent is a LangGraph graph); pick LangChain create_agent with an approval pause and a checkpointer that outlives the process](resources/lab09_choosing.png)

### Step 1: Read the scorecard

These scores are the instructor's assessment in October 2026, from building the desk in each framework (for
LlamaIndex, lab 12's policy-search agent) and reading each one's documentation: a judgement, not a benchmark. 3 is
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

- **The Agents SDK** already runs the shop's chat page (lab 13), and that counts for it, but it failed the filter: a
  refund that waits hours needs a saved `RunState` that our own code stores and reloads (B2).
- **Microsoft Agent Framework** fits on paper, but its particular strengths, .NET and Azure, are not this team's, and
  it needs an environment of its own (B6). Its approval also lives in a workflow apart from the agent (B6, Part D:
  `check → review → queue`, with no model inside).
- **LangGraph by hand** gives the most control, but the desk is one agent with one gate. Drawing the graph ourselves
  costs ease (a 1) for control the desk does not need yet.
- **LangChain's `create_agent`** returns a LangGraph graph (lab 08, Part B: a `CompiledStateGraph`), pauses before
  the refund tool with one middleware, and keeps the paused run in a checkpointer that outlives the process (lab 08,
  Parts F and G). If the refund flow grows more gates, the same graph can be written by hand without changing
  frameworks (lab 08, Part D: the hand-built graph has the same nodes and edges).

**The pick:** LangChain's `create_agent`, with `HumanInTheLoopMiddleware` in front of `file_refund_request` and a
checkpointer on a database the service keeps (`SqliteSaver` in lab 08; on a server, one such as `PostgresSaver`).

### Step 4: Say what would change the pick

A pick is only as good as the answers behind it, so write down which answer, if it changed, would change the pick.

- **If the rep approves on the spot,** in the same session, the pause no longer has to outlast the process. Pause
  and approve drops from a must-have to a weight, and the Agents SDK's `needs_approval` (B2) does the job. LangChain
  still adds up higher, but only because it scores 3 on two things this version of the job does not use (a pause
  that outlives the process, and a second vendor). Points for a strength the job does not need are not a reason;
  what already runs is, and the shop's chat page already runs on the Agents SDK (lab 13). Start there, and move to
  LangChain or LangGraph when a refund must wait overnight.
- **If the team works in .NET or on Azure,** Microsoft Agent Framework.
- **If the refund flow grows gates** (an amount above which a second person approves, a retry when the payment system
  is down), LangGraph by hand: the same kind of graph, drawn by us.
- **If the shop wants a second model vendor,** the vendor weight rises to 3 and Microsoft Agent Framework (a 2 there)
  falls behind LangChain and LangGraph; made a must-have, it drops out.
- **Stay with your own loop** for a few tools, one vendor, every step explained to an auditor, or a loop that is
  itself the thing you need to see. Labs 14 and 17 keep their own loop for that reason: the step each one teaches (a
  file write and a test run; a check before a tool runs) is a line we need in front of us.

**Checkpoint D.** You can say why must-haves filter before the weights are added up, reproduce one weighted total,
give the desk's pick with the reason that breaks the tie, and name the one answer that turns the pick into the
Agents SDK.

## Part E: Decide what a wrong pick costs and what changes later

Why spend this effort on a choice? Because the framework is the part of an agent most likely to change while the job
stays the same, and what a change costs depends on what you built on top of it.

### Step 1: Separate what moves from what stays behind

| Part of the desk | Moves to another framework when ... | Stays behind when ... |
|---|---|---|
| The three lookups | they are plain Python functions, or behind an MCP server (lab 06) | they are written as one framework's tool classes |
| The instructions | they are a string in your repository | they are spread over one framework's prompt templates or a crew's role texts |
| The definition | always: a model, instructions and tools (Part A) | |
| Checks and approvals | they are your own functions, called by the framework | they are written as one framework's middleware, guardrails or validators |
| Paused runs and conversations | you let them finish before the switch | they sit in one framework's checkpoint or session tables (lab 08's `checkpoints.db`, lab 07's `sessions.db`) |
| Traces | they are exported in an open format (OpenTelemetry's conventions for generative AI, lab 20) | they can only be read in one framework's tracing service |
| Your tests | always, if they check facts and tool calls instead of one framework's objects (lab 18's golden set) | |

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
- OpenAI's Assistants API [shut down on 26 August 2026](https://developers.openai.com/api/docs/deprecations); lab 20,
  Part E reads what moved to its replacement and what did not.

The versions this repository pins (in `pyproject.toml` and the own environments of labs 12, B3, B5 and B6):
`openai-agents` 0.24.0, `langchain` 1.4.7, `langgraph` 1.2.19, `llama-index-core` 0.14.25, `google-adk` 2.13.0,
`pydantic-ai-slim` 2.64.0, `crewai` 1.15.34 and `agent-framework` 1.24.0. Two of them, `openai-agents` and
`llama-index-core`, are below 1.0 (their latest releases on PyPI on 5 November 2026 were still 0.24.0 and 0.14.25),
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
- Pick: **LlamaIndex**, with a retriever tool. In lab 12, Part H the retriever-tool agent was right in every run
  (10 of 10 with a plain prompt, 5 of 5 with a sharper one) at about 4 model calls a run.
- Watch: the query-engine tool, LlamaIndex's other way to give an agent the documents, makes a model call inside
  every search; with a plain prompt it found the rule file in 3 of 10 runs at 6.2 calls a run.
- Also defensible: **your own loop with a search tool**, as lab 11 builds it, if the team wants no new dependency
  (LlamaIndex needs an environment of its own in this repository).

**2. A front door for customer email.**

- Must-haves: none. Several agents share the work (multi-agent, weight 3), each team maintains its own
  (easy to learn, weight 2), and tracing matters (weight 2); pause, vendor and control weigh 1.
- The sum, out of 30: Microsoft Agent Framework 27, LangChain and LangGraph 26, CrewAI 25, the Agents SDK and
  Pydantic AI 24, Google ADK 23. Seven frameworks within four points, so the evidence decides.
- Re-score one cell: "multi-agent" averages several patterns (a supervisor, a crew, a graph, a handoff). This job
  needs one of them, a **handoff**, where one specialist takes the conversation for good. In the Agents SDK a handoff
  is a first-class object, and lab 07 measured both where it fits (the triage agent handed the rep-only question to
  the reps specialist, which answered it) and where it fails. Scored on this pattern the SDK's cell is a 3, and its
  total 27.
- Pick: **the OpenAI Agents SDK with handoffs**, level with Microsoft Agent Framework on the sum and ahead on ease,
  which matters when three teams each maintain an agent; it also runs in this repository's environment.
- Watch: a message with two destinations loses its second half after a handoff (lab 07, Part F: the rep missing in 5
  of 5 runs). Route such messages to a manager that calls the specialists as tools, or split them in code first.
- Also defensible: if the teams' agents run on different platforms, the agents talk over A2A (lab 20, Part B), and
  each team chooses its own framework.

**3. Month-end refund reconciliation.**

- Must-haves: pause and approve (days, across redeploys) and tracing (every proposal audited). Language: C#.
- Filter: LangChain, LangGraph and Microsoft Agent Framework pass; of these only Microsoft Agent Framework serves
  .NET.
- Pick: **Microsoft Agent Framework**, with the approval as a workflow step and its checkpoints in storage the
  service keeps (B6 restored a pending review in a new process).
- Watch: restoring a checkpoint can repeat a step. Give each correction a business key so that a repeated approval
  writes nothing new (B6: a repeated approval still left one row, because of the queue's key).

</details>

**Checkpoint F.** For job 1 your reason names documents, the need the scorecard leaves out; for job 2 you asked which
multi-agent pattern the job needs (a handoff) before trusting the multi-agent column; for job 3 your must-haves are
pause and tracing, and your pick is Microsoft Agent Framework or comes with a reason that names the team's
language.

## What you can do now

- Recognise the four steps of the agent loop inside any framework, and point at the model, instructions and tools in
  its agent definition.
- Read a framework's run as model requests, tokens and tool calls, and say why the same agent costs different tokens
  in different frameworks.
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
`solved/09_choose_a_framework_solution.md`.

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
- Google ADK: [agents](https://adk.dev/agents/llm-agents/), [LiteLLM models](https://adk.dev/agents/models/litellm/)
- Pydantic AI: [agents](https://pydantic.dev/docs/ai/core-concepts/agent/),
  [output validators](https://pydantic.dev/docs/ai/core-concepts/output/#output-validators)
- [Stack Overflow Developer Survey 2026, AI](https://survey.stackoverflow.co/2026/ai) and
  [Semantic Versioning](https://semver.org/)
