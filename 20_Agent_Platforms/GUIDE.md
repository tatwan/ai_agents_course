# Lab 20: What agent platforms sell

## Goal

Read any agent platform's product page and say which of the six layers of an agent it sells, which of those layers
you could take to another vendor, and which would lock you in. The moment that teaches it comes in Part C: we write
the Chinook desk agent's definition for five products from five vendors, and every one asks for the same three
things, a model, instructions and tools. What differs, and what you are really buying, is what runs around that
definition: where the conversation is stored, who the agent runs as, and where its traces live. Part E then shows,
from the vendors' own migration notes, that definitions move from one product to the next and stored state does not.

## What you will learn

- How to name the six layers of an agent (model, tools, orchestration, context and memory, delegation, governance)
  on an agent you built, and place a product's features on them.
- How to tell the three open standards (MCP, A2A, Agent Skills) from the products built on them, and which layer
  each one lets you move.
- How to read a hosted agent's definition in five products as the same model, instructions and tools.
- How to sort a product by the four things platforms sell: a builder, a runtime, connections or governance.
- How to say which layers move between vendors and which lock you in, with the question to ask a vendor for each.
- How to classify a purchase on the six layers and decide what, if anything, to buy.

## Before you start

This is a reading guide: there is no code to run, nothing to install and no key to set. You need a text editor or a
sheet of paper, because every step asks you to write something down before you read our answer.

The guide uses the agent this course builds, the support desk of the Chinook music shop, and one question asked of
it: *How many invoices does Helena Holý have, what do they add up to, and who is her support rep?* (the database says
7 invoices, $49.62, and Steve Johnson). Where an idea was built in an earlier lab, the guide names the lab and
re-teaches what it needs in a sentence, so you can read it on its own.

⚠️ **Product names and statuses change every few months.** Every product fact below was checked on the vendor's own
documentation on 30 October 2026, and each one links to its page. Before you quote a fact in a meeting, open the link
and check it again (the Challenge does this for one row).

## Part A: Name the six layers of the agent we built

A vendor never sells you "an agent". It sells some of the parts an agent is made of, and you already have every one
of them. Before we read any product page, we name those parts on the desk agent, so that a product's feature list has
somewhere to land.

### Step 1: Follow one question through the desk agent

When a support rep asks the Helena question, six different things happen. Read them in order:

1. **A model** reads the question and replies with a request for a tool: look up a customer named Helena Holý. It
   never runs anything itself (lab 03 showed that a tool call is only text the model writes).
2. **Tools** do the work: `find_customer`, `get_invoices` and `get_support_rep` are our own Python functions that
   read the shop's database, opened read-only.
3. **Orchestration** is the loop around the model: send the messages, run the tools it asked for, send the results
   back, and stop at an answer or a turn cap (lab 04 wrote this loop by hand; the Agents SDK's `Runner` in lab 07 and
   LangChain's `create_agent` in lab 08 run the same loop for you).
4. **Context and memory** decide what the model sees on each turn: the message list, a session that remembers who
   "she" is on the next question (lab 13 keeps one per visitor), the policy documents a search tool retrieves (labs 10
   and 11), and skills loaded only when a task needs them (lab 05).
5. **Delegation** is one agent asking another: a manager agent calling an invoices specialist and a reps specialist
   (lab 07 wired them as tools and as a handoff; lab 16 measures when a second agent pays).
6. **Governance** is everything that makes the agent safe to run for a business: who it runs as and what it may
   touch (the read-only database), where model-written code runs (lab 15's container), what it does with untrusted
   text (lab 17), and the tests and traces that show what it did and what it cost (lab 18 keeps them in MLflow).

**Write down:** for each of the six, one sentence in your own words saying what would break in the Helena answer if
that layer were missing. (Without tools, the model answers from memory or refuses; without orchestration, nothing
runs the tool it asked for; and so on.)

### Step 2: Put the six layers in one table

The same six, as a table you will reuse in every part:

| Layer | What it does on the Helena question | Where this course builds it |
|---|---|---|
| 1. Model | reads the question, asks for lookups, writes "7 invoices, $49.62, Steve Johnson" | lab 01 (one call); `models.env` names it |
| 2. Tools | the three lookups against the read-only database | lab 03 (the tool call as data); lab 06 (the same three behind an MCP server) |
| 3. Orchestration | the loop: call, run tools, send results, stop | lab 04 (by hand); labs 07 and 08 (frameworks) |
| 4. Context and memory | the message list, a session per visitor, retrieved policies, skills | labs 05, 10, 11, 13 |
| 5. Delegation | a manager asking two specialists | labs 07 and 16 |
| 6. Governance | read-only access, a sandbox, guards on untrusted text, tests, traces, cost | labs 13, 15, 17, 18 |

![The six layers of the Chinook desk agent in one row: the model, tools (standard: MCP), orchestration, context and memory (standard: Agent Skills), delegation (standard: A2A) and governance; context and memory and governance are lit as the two layers that lock you in](resources/lab20_six_layers.png)

The drawing already shows where this guide ends up: three layers have an open standard, and two layers (lit) are
where lock-in lives. Parts B to E show why.

### Step 3: Move one layer by hand, then imagine moving another

Moving a layer means running it somewhere else without rewriting the rest. Take the smallest case first.

- **Moving the model in this repository.** Every notebook reads the model's name from one line in `models.env`
  (`MODEL_DEFAULT=...`). Change that line and every lab uses the new model. Nothing else changes, but the answers
  might: the new model may call the tools in a different order, or answer from memory. So the move costs one line
  plus a re-run of your tests (lab 18's golden set exists for exactly this).
- **Moving governance after a year with a vendor.** Imagine every prompt, tool argument and reply of the last
  eighteen months sits in a vendor's trace dashboard, and the agent's identity and permissions live in that vendor's
  directory. To leave, you must export the traces in a format another tool can read, re-create the identity, and get
  the permissions approved again. That is a project, not a line.

**Key lesson:** a layer moves easily when what it holds is your code or a setting. It locks you in when it holds
data or decisions that only exist inside the vendor's product.

**Checkpoint A.** You have a six-row table, one sentence per layer on what breaks without it, and you can say why
moving the model costs one line plus a test run while moving governance is a project.

## Part B: Tell the open standards from the products

Three of the six layers now have an open standard: a published format that any vendor's product can speak. A
standard is what lets a layer move, so before we read product pages we need to know which words on them are
standards and which are product names.

### Step 1: Read what each standard fixes

| Standard | What it fixes | Layer | The Chinook example | Status, checked 30 Oct 2026 |
|---|---|---|---|---|
| [MCP](https://modelcontextprotocol.io/specification/versioning) (Model Context Protocol) | how a host lists a server's tools and calls them | 2. Tools | lab 06's `chinook_server.py`: the three lookups, called by a host we did not write (the Agents SDK) in a few lines | current revision 2026-07-28 |
| [A2A](https://a2a-protocol.org/latest/) (Agent2Agent) | how one agent finds out what another agent can do (from the other agent's published card) and sends it a task | 5. Delegation | the desk agent asking a shipping agent that another team runs, on another platform | specification v1.0.0; started by Google and given to the Linux Foundation |
| [Agent Skills](https://agentskills.io/specification) | a folder with a `SKILL.md` file (a `name`, a `description`, then instructions) that an agent loads only when a task needs it | 4. Context and memory | lab 05's three skills, such as `refund-requests/` | open specification; OpenAI's Responses and Agents APIs, Claude Managed Agents, Foundry prompt agents, AgentCore and ADK all load skills in this format |

All three are projects of the [Agentic AI Foundation](https://aaif.io/), part of the Linux Foundation, so no single
vendor owns them.

**Write down:** for each standard, the product feature it replaces. (Without MCP, each platform would need its own
connector for the shop's database; without Agent Skills, the refund playbook would be pasted into each product's
own instructions box.)

### Step 2: Notice what a standard does not move

A standard fixes an interface, not what sits behind it.

- MCP moves the **tool interface**: any host can call `find_customer`. It does not move the database, or the
  credentials a hosted platform keeps to reach it.
- A2A moves the **conversation between agents**. It does not move the other agent's memory or who it runs as.
- Agent Skills moves the **instructions file**. It does not move the conversations an agent had while using it.

Governance has no settled standard yet. The closest is OpenTelemetry's conventions for generative AI traces
([semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai)), which several products
already emit; their agent spans are still marked **Development**, not stable, on 30 October 2026. A trace exported
in that format can be read by another tool, but the conventions can still change.

**Checkpoint B.** You can name the layer each standard sits on (MCP: tools; A2A: delegation; Agent Skills: context),
and say one thing each standard leaves behind with the vendor.

## Part C: Read one agent definition in five products

Every vendor in this guide sells a way to define an agent once and let their service run it. If the six layers are
real, the definitions should look alike. This part checks that on the desk agent.

### Step 1: Write the desk agent's definition in plain words

Strip the desk agent down to what you would have to tell any service:

```text
model:         the model named in models.env
instructions:  You help the support reps of a music shop. Look up every fact with the tools;
               never answer from memory. Answer in one or two sentences.
tools:         find_customer, get_invoices, get_support_rep  (lab 06's MCP server)
```

This is lab 07's desk agent: `Agent(name="Desk", instructions=SYSTEM, model=MODEL, tools=DESK_TOOLS, ...)`, the
same three things plus a name and the model settings.

### Step 2: Find the same three fields in five products

Here is where each product asks for them, read from each product's documentation on 30 October 2026:

| Product | Status | What you define | Where the run and its state live |
|---|---|---|---|
| [OpenAI Agents API](https://developers.openai.com/api/docs/guides/agents-api/overview) | public beta since 10 Sep 2026 | an agent: `model`, `instructions`, `tools` (including MCP servers), sub-agents | a session that OpenAI keeps; an optional sandbox (OpenAI-hosted or your own) |
| [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) (Anthropic) | beta since 8 Apr 2026 | an agent: model, system prompt, tools, MCP servers, skills | a session in an environment (Anthropic's cloud sandbox or your own); transcripts persist until you delete them |
| [Microsoft Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/prompt-agents), prompt agent | generally available | a prompt agent: model, instructions, tools, skills | conversations and responses, kept in the Foundry project; each agent can have a Microsoft Entra identity |
| [Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html), managed agent loop | generally available | a model, a system prompt (instructions), tools and skills, passed in one call | each session in an isolated microVM; AgentCore Memory for short- and long-term memory |
| [Google ADK](https://adk.dev/agents/llm-agents/) agent on [Agent Runtime](https://adk.dev/deploy/agent-runtime/) | ADK is open source; Agent Runtime is part of Google's Gemini Enterprise Agent Platform | an `LlmAgent`: `model`, `name`, `description`, `instruction`, `tools` | Agent Runtime hosts it; an administrator can [register it in Gemini Enterprise](https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-adk-agent) for employees to use |

**Write down before reading on:** in which columns do the five rows look alike, and in which do they differ?

### Step 3: Read what the comparison shows

- **The definition is the same in every row.** A model, instructions and tools, sometimes with skills and MCP
  servers beside them. The desk agent's three lines from Step 1 fit every product, with only the field names
  changed (`instructions`, "system prompt", `instruction`).
- **The last column is where they differ.** Who keeps the conversation (a session, a conversation object, a
  microVM, a hosted runtime), where code runs, and who the agent runs as (an Entra identity in Foundry, an identity
  from AgentCore Identity on AWS). Those are layers 4 and 6: context and memory, and governance.
- **The loop is not in the definition at all.** In four of the five, the vendor's own loop runs orchestration (layer
  3). With ADK on Agent Runtime the loop is ADK's open-source code, hosted by Google. In this course you ran the loop
  yourself, in your own code (lab 04) or an open framework (labs 07 and 08).

**Key lesson:** the agent definition is the portable part: three lines you can take to any vendor. What a hosted
runtime sells is everything around those lines, and that is also where it holds your data.

**Important:** "the same three fields" does not mean "the same behaviour". The vendor's loop decides how many turns a
run may take, when it compacts the context and how it retries a failed tool. Moving the definition still means
re-running your tests on the new runtime.

**Checkpoint C.** You can point at the three shared fields in each row, name the two layers the last column is about
(context and memory; governance), and say which layer the vendor's loop runs in four of the five (orchestration).

## Part D: Sort products by the four things platforms sell

Product pages list dozens of features. Sorting a product by **what it sells** before comparing prices stops you
comparing a builder with a runtime. There are four things to buy:

| What it sells | What you get | Layers | Examples, checked 30 Oct 2026 |
|---|---|---|---|
| **Build** | a page where people configure an agent without writing the loop | 1, 2, 4 (configured, not coded) | [Gemini Enterprise Workflow Builder](https://docs.cloud.google.com/gemini/enterprise/docs/agents-overview) (an administrator turns it on); Foundry prompt agents built in the Foundry portal |
| **Run** | a hosted runtime that runs a loop for you | 3, plus storage for 4 | OpenAI Agents API; Claude Managed Agents; Foundry Agent Service (prompt agents, and hosted agents: your own LangGraph, Agents SDK or Agent Framework code in a container); AgentCore Runtime and its managed agent loop; Google's Agent Runtime for ADK agents |
| **Connect** | ways to reach tools and other agents | 2, 5 | [Foundry toolboxes](https://learn.microsoft.com/en-us/azure/foundry/agents/overview) (tools behind one managed MCP endpoint) and its [A2A tool](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/agent-to-agent); AgentCore Gateway (turns APIs and Lambda functions into MCP tools); Gemini Enterprise's registration of A2A agents |
| **Govern** | identity, permissions, approvals, traces and evaluations | 6 | AgentCore Identity, Policy (checks every tool call before it runs), Observability and Evaluations; Foundry's Entra identities, content filters and tracing; MLflow (open source, lab 18); LangSmith (bonus B8) |

Notice what is missing from the table: the **open frameworks** this course used (the OpenAI Agents SDK, LangChain
and LangGraph, LlamaIndex, Google ADK). Nobody sells them; they are open source, and they run the loop inside your own
application. A hosted runtime is often the same kind of loop, run by someone else.

**Write down:** sort these three into the four things (one product can sell two): the OpenAI Agents API, AgentCore
Gateway, Gemini Enterprise Workflow Builder. (Ours: Run; Connect; Build.)

**Checkpoint D.** You can place each product named in Part C under Run, and name one product each under Build,
Connect and Govern.

## Part E: Decide which layers move and which lock you in

Part A argued that data and decisions inside a product are what lock you in. The vendors' own migration notes for
four recent product changes let us check that claim, because each one says what moved to the new product and what
did not.

### Step 1: Read four product changes and what each one moved

| Change, from the vendor's page | What moved | What did not |
|---|---|---|
| OpenAI's Assistants API [shut down on 26 Aug 2026](https://developers.openai.com/api/docs/deprecations); the replacement is the Responses API with the [Conversations API](https://developers.openai.com/api/docs/guides/conversation-state), which keeps a conversation on OpenAI's servers under an id | the assistant's model, instructions and tools, recreated by hand as a prompt in the dashboard ([migration guide](https://developers.openai.com/api/docs/assistants/migration)) | the conversation history: after the shutdown the call that read a thread's messages stopped working, and the guide says to use the messages your own application stored. The loop moved back into your code too |
| Microsoft's Foundry (classic) agents are [deprecated and retire on 31 Mar 2027](https://learn.microsoft.com/en-us/azure/foundry-classic/agents/concepts/threads-runs-messages); the new Foundry Agent Service uses conversations and responses | agent definitions, with a migration tool | stored state: the [migration guide](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/migrate) says the tool "doesn't migrate state data like past runs, threads, or messages" |
| Foundry's Connected Agents feature is not in the new Foundry Agent Service; the guide recommends the [A2A tool](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/agent-to-agent) (generally available for A2A 1.0) or workflows | the agents themselves | the wiring between them, rebuilt on A2A, a standard |
| OpenAI's Agent Builder [shuts down on 30 Nov 2026](https://developers.openai.com/api/docs/deprecations); OpenAI points to the Agents SDK or ChatGPT Workspace Agents ([migration guide](https://developers.openai.com/api/docs/guides/agent-builder/migrate-from-agent-builder)) | what the builder described | the builder itself: a Build product's agents must be rebuilt somewhere else |

Read the "What did not" column again. In each case the definition could be carried over (by hand or with a tool),
and what stayed behind or had to be rebuilt was stored state, the vendor's own wiring, or a builder's format. The replacement for Connected Agents
is an open standard, so the next move of that layer should be cheaper.

One more detail from the same pages: the prompts that replaced OpenAI's assistants (the `v1/prompts` API) are
themselves scheduled to shut down on 30 Nov 2026. A definition kept only in a vendor's dashboard may have to move
twice; the three lines of Part C, kept in your own repository, stay where they are and are copied into whichever
product comes next.

### Step 2: Mark each layer portable or sticky, with its condition

| Layer | Moves (portable) when ... | Locks you in (sticky) when ... | The question to ask a vendor |
|---|---|---|---|
| 1. Model | you can point the agent at another model and re-run your tests | the agent depends on a feature only one model has | "Which models can this agent use, and can I bring my own?" |
| 2. Tools | the tools sit behind your own MCP server | they exist only in the vendor's tool catalogue | "Can the agent call my MCP server, and can my other hosts call yours?" |
| 3. Orchestration | the loop is your code or an open framework you could host elsewhere | the vendor's runtime is the only place the agent runs | "If I leave, what code do I take with me?" |
| 4. Context and memory | you can export conversations, documents and saved notes in a readable format | they live in the vendor's store, with its filters and access rules | "How do I export every conversation and memory, and in what format?" |
| 5. Delegation | the agents talk over A2A | they are wired with a vendor-only feature | "Can this agent call, and be called by, an agent on another platform?" |
| 6. Governance | identities come from your own directory and traces export in an open format | identities, approvals and a year of traces exist only in the vendor's product | "Whose directory holds the agent's identity, and how do I export the traces?" |

So in practice: **model, tools, orchestration and delegation move when you choose the open option; context and memory,
and governance, are where lock-in lives**, because they hold data that only exists after the agent has run for a
while.

**In production:** lock-in is not always bad. A vendor's identity, filters and audit trail may be exactly what a
risk team needs to approve an agent. The point is to choose it on purpose: buy the sticky layer you need, and keep
the rest portable. Some vendors also build an exit door: AWS documents exporting its managed agent configuration
to code for its open-source Strands Agents framework, to run it on AgentCore Runtime.

**Checkpoint E.** For each of the six layers you can say when it moves, when it sticks, and one question to ask a
vendor; and you can quote one migration note that shows stored state staying behind.

## Part F: Classify layers and purchases

This worksheet uses everything above on the Chinook shop. Write your answers before you open the worked answers
below it. Some rows have more than one defensible answer; what matters is the reason.

**1. Portable or sticky?** For each item, write `portable` or `sticky` and one reason.

| Item | Portable or sticky? |
|---|---|
| a. The model behind the desk, changed next quarter | |
| b. The three Chinook lookups behind lab 06's MCP server | |
| c. The desk agent written with LangGraph (lab 08), deployed as a hosted agent on a vendor's runtime | |
| d. A year of ticket embeddings in a vendor's managed vector store, with its metadata filters and access rules | |
| e. The desk agent's identity in the vendor's directory, with the permissions the risk team approved | |
| f. Eighteen months of traces (every prompt and tool argument) in the vendor's dashboard | |
| g. A shipping agent another team runs, which the desk reaches over A2A | |

**2. What would you buy?** For each purchase, write which of the four things (Build, Run, Connect, Govern) you would
buy, if any, and which layer would become sticky.

| Purchase | Buy what? | Which layer sticks? |
|---|---|---|
| A. Every night, export yesterday's invoices to the finance team's shared folder, the same steps every time | | |
| B. The Helena desk for support reps: the three lookups and the loop, already running in our own code | | |
| C. A refund agent that customers talk to directly; the risk team asks for a per-agent identity, approval before any refund, and a year's audit trail | | |

<details>
<summary><b>Worked answers</b> (open after you have written yours)</summary>

**1. Portable or sticky?**

| Item | Answer | Why |
|---|---|---|
| a. The model | portable | one setting to change, then a re-run of the tests |
| b. Lookups behind MCP | portable | any MCP host can call them; that is what lab 06 showed |
| c. LangGraph on a hosted runtime | portable | the code is open source and runs anywhere; only the hosting is bought (the runtime's sessions and identity are not, see e) |
| d. A year of embeddings in a vendor store | sticky | the vectors can be rebuilt by embedding again, but the filters, access rules and the year of metadata live in the vendor's store. If you said "portable, we can re-embed", you are right about the vectors and wrong about the access rules |
| e. The agent's identity | sticky | it lives in the vendor's directory, and the approval has to be done again elsewhere |
| f. Eighteen months of traces | sticky | the audit trail is a project to move, unless it was exported in an open format all along |
| g. The shipping agent over A2A | portable | A2A is a standard; the desk can call it from any platform |

**2. What would you buy?**

| Purchase | Buy what? | Which layer sticks? | Why |
|---|---|---|---|
| A. Nightly invoice export | nothing: no agent | none | the steps are known and the same every night: that is a scheduled workflow, not an agent (lab 02's test: who decides the next step?) |
| B. The Helena desk | nothing new, or Run if nobody can host it | orchestration and memory, only if you buy Run | it already runs in our code with tools behind MCP; buying a runtime trades hosting work for a sticky session store |
| C. Customer-facing refunds | Govern (and probably Run from the same vendor) | governance: the identity and the audit trail | the risk team's three demands are all layer 6. Buying them is a sound decision as long as it is made on purpose, with the export questions from Part E asked first |

Answering B with "Run" is not wrong: it says you want someone else to run the loop. Then ask which sticky layer comes
with it (the sessions, and the identity the runtime gives the agent).

</details>

**Checkpoint F.** Your answers to items a, b, e and f, and to purchase A, match the worked answers; for the others
you can give a reason that names a layer.

## What you can do now

- Name the six layers on an agent you built, and say what each does on one question.
- Tell MCP, A2A and Agent Skills from the products that use them, and say which layer each lets you move and what it
  leaves behind.
- Read a hosted agent's definition in five products as the same model, instructions and tools, and see that the
  differences are in context and governance.
- Sort a product into Build, Run, Connect or Govern before comparing it with another.
- Say for each layer when it moves and when it locks you in, and ask a vendor the question that tells you which.
- Classify a purchase on the six layers, and say what to buy, or that no agent is needed.

## Challenge

1. **Write a buying brief for the desk.** Your manager wants to move the Chinook desk agent to one hosted runtime
   from Part C (choose one). For each of the six layers write: keep it as it is, or buy it from that vendor; one
   question for the vendor; and the answer that would make the layer portable. *Expected outcome:* a six-row table in
   which the model, tools and delegation can stay portable (an answer such as "yes, it calls any MCP server" is
   enough), orchestration is bought with the runtime, and context and memory and governance carry the export
   questions; and a one-line recommendation that names the sticky layers you would accept.
2. **Re-check one product row.** Pick one row from Part C or Part E, open its link, find the line that states its
   status or date, and write today's date beside what you found. *Expected outcome:* the row confirmed or corrected;
   if a status changed (a beta became generally available, a product was renamed or shut down), one sentence on which
   layer the change affects and whether it makes that layer more or less portable.

A worked answer for both tasks, for Microsoft Foundry Agent Service, is in `solved/20_agent_platforms_solution.md`.

## Resources

- OpenAI: [Agents](https://developers.openai.com/api/docs/guides/agents) (the Agents API, the Agents SDK and the
  Responses API compared), [Agents API overview](https://developers.openai.com/api/docs/guides/agents-api/overview),
  [Conversation state](https://developers.openai.com/api/docs/guides/conversation-state) (the Conversations API),
  [Skills](https://developers.openai.com/api/docs/guides/tools-skills), [Deprecations](https://developers.openai.com/api/docs/deprecations)
  and the [changelog](https://developers.openai.com/api/docs/changelog)
- Anthropic: [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)
- Microsoft: [What is Microsoft Foundry Agent Service?](https://learn.microsoft.com/en-us/azure/foundry/agents/overview),
  [Prompt agents](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/prompt-agents),
  [Connect to an A2A agent endpoint](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/agent-to-agent),
  [Migrate to the new Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/migrate)
- AWS: [What is Amazon Bedrock AgentCore?](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)
- Google: [Gemini Enterprise agents overview](https://docs.cloud.google.com/gemini/enterprise/docs/agents-overview),
  [ADK agents](https://adk.dev/agents/llm-agents/), [Deploy to Agent Runtime](https://adk.dev/deploy/agent-runtime/)
- Open standards: [MCP versioning](https://modelcontextprotocol.io/specification/versioning),
  [A2A](https://a2a-protocol.org/latest/), [Agent Skills specification](https://agentskills.io/specification),
  [Agentic AI Foundation](https://aaif.io/),
  [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)
