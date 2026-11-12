# Lab 23: What agent platforms sell

## Goal

Read any agent platform's product page and say which of the six layers of an agent it sells, which of those layers
you could take to another vendor, which would lock you in, and whether to build, buy or do neither. We start with
something everyone has done, changing phones, and ask what came with us and what stayed behind. Then we ask the same
question of the Chinook support desk agent. Two parts carry the lesson. In Part D the desk agent's definition fits
five products from five vendors, because every one asks for the same three things: a model, instructions and tools.
In Part F the vendors' own migration notes show what happens when a product changes: the definitions move to the next
product, and what only the vendor held (stored conversations, its own wiring, a builder's format) stays behind.

## What you will learn

- How to sort what moves to a new vendor from what stays, using a standard or an export as the test.
- How to name the six layers of an agent (model, tools, orchestration, context and memory, delegation, governance)
  on an agent such as the Chinook desk, and place a product's features on them.
- How to tell the three open standards (MCP, A2A, Agent Skills) from the products built on them, and which layer
  each one lets you move.
- How to read a hosted agent's definition in five products as the same model, instructions and tools.
- How to sort a product by the four things platforms sell (a builder, a runtime, connections or governance) and say
  for each layer whether it moves or locks you in, with the question to ask a vendor.
- How to decide build, buy or neither for an agent purchase, and which layer would lock you in if you buy.

## Before you start

This is a reading guide: there is no code to run, nothing to install and no key to set. You need a text editor or a
sheet of paper, because every step asks you to write something down before you read our answer.

From Part B on, the guide uses one agent: the support desk of the Chinook music shop, and one question asked of it:
*How many invoices does Helena Holý have, what do they add up to, and who is her support rep?* (the database says 7
invoices, $49.62, and Steve Johnson). Each piece of that agent is explained in a sentence where it appears, so you can
read the guide on its own. Part B's table names the lab in this repository that builds each piece, if you want to see
it run.

⚠️ **Product names and statuses change every few months.** Every product fact below was checked on the vendor's own
documentation on 12 November 2026, and each one links to its page. Before you quote a fact in a meeting, open the link
and check it again (the Challenge does this for one row).

## Part A: Sort what moves with you when you change phones

Moving an agent from one vendor to another is like moving from one phone maker to another. Most people have done the
second, so we start there and find the rule before we meet any agent product.

### Step 1: Mark each item as moving or staying

**Write down:** you are moving from one maker's phone to another maker's phone. For each item below, write `moves` or
`stays`, and why.

| Item | Moves or stays? |
|---|---|
| a. Your phone number | |
| b. Your charger | |
| c. Your contacts | |
| d. Your photos | |
| e. Years of chat history, backed up in the old maker's cloud | |
| f. The apps you paid for | |

### Step 2: Read what decides each answer

<details>
<summary><b>Our answers</b> (open after you have written yours)</summary>

| Item | Our answer | What decides it |
|---|---|---|
| a. Phone number | moves | in most countries, carriers must let you keep your number when you switch (number portability), a rule every carrier there follows |
| b. Charger | moves, if both phones use USB-C | USB-C is a standard plug, so any maker's phone that uses it fits |
| c. Contacts | moves, if you synced them to an account you keep or exported them | a contact file (vCard) is a standard format that phones and mail programs read |
| d. Photos | moves, but only if you copy them out | they are your files, but a large library in the old maker's cloud is a long download and upload |
| e. Chat history in the old maker's cloud | often stays | the backup is kept in a form the old maker's service restores. Without a transfer tool for that app, it stays behind |
| f. Apps you paid for | stays | each purchase lives in one maker's app store, and the other maker's store does not know about it |

</details>

Read the last column again. Everything that moved had either a **standard** (the number rule, the plug, the contact
file) or an **export you control** (copying the photos out). What stayed exists only inside the old maker's service:
the backup and the purchases.

**Key lesson:** a thing moves with you when a standard describes it or when you can export it yourself. It stays
when it exists only inside the product you are leaving.

### Step 3: Ask the same question of an agent

Now take an agent that a shop runs on a vendor's platform. In a year the shop wants to move to another vendor.

**Write down before reading on:** what would come with the agent, and what would stay behind? List anything you can
think of (the prompt, the tools, the conversations, the logs, who the agent runs as). Keep the list. Part F answers
it.

To answer it properly, we first need names for the parts an agent is made of. Part B gives them.

**Checkpoint A.** You have the six items marked, with a reason each, and you can say the rule in one sentence: what
has a standard or an export moves, and what exists only inside the product stays.

## Part B: Name the six layers of the Chinook desk agent

A vendor sells some of the parts an agent is made of. Before we read any product page, we name those parts on the
desk agent, so that we can say which part each product feature belongs to.

### Step 1: Follow one question through the desk agent

When a support rep asks the Helena question, six different things happen. Read them in order:

1. **A model** reads the question and replies with a request for a tool: look up a customer named Helena Holý. It
   never runs anything itself. A tool call is text the model writes, and our code decides whether to run it.
2. **Tools** do the work: `find_customer`, `get_invoices` and `get_support_rep` are our own Python functions that
   read the shop's database, opened read-only.
3. **Orchestration** is the loop around the model: send the messages, run the tools it asked for, send the results
   back, and stop at an answer or at a turn cap. We can write this loop in a few lines of Python, or let a framework
   run it.
4. **Context and memory** cover what the model is sent on each turn: the message list, a session that keeps each
   visitor's conversation so that "she" means Helena on the next question, the policy documents a search tool
   retrieves, and skills (folders of instructions) loaded only when a task needs them.
5. **Delegation** is one agent asking another: a manager agent calling an invoices specialist and a support-reps
   specialist, each with its own tools.
6. **Governance** is everything that makes the agent safe to run for a business: who it runs as and what it may
   touch (the read-only database), where model-written code runs (a container that cannot reach our files), what it
   does with untrusted text such as a planted line in a ticket, and the tests and traces that show what it did and
   what it cost.

**Write down:** for each of the six, one sentence in your own words saying what would break in the Helena answer if
that layer were missing. (Without tools, the model writes an answer without looking anything up, or refuses. Without
orchestration, nothing runs the tool it asked for. And so on.)

### Step 2: Put the six layers in one table

The same six, as a table you will reuse in every part. The last column names where this repository builds each
layer. The guide does not depend on them: they are there if you want to see a layer run.

| Layer | What it does on the Helena question | Built in this repository |
|---|---|---|
| 1. Model | reads the question, asks for lookups, writes "7 invoices, $49.62, Steve Johnson" | Lab 01 (one model call); Lab 21 (any model through one interface); `models.env` names the model |
| 2. Tools | the three lookups against the read-only database | Lab 02 (a tool call by hand); Lab 06 (the same three lookups behind an MCP server) |
| 3. Orchestration | the loop: call, run tools, send results, stop | Lab 03 (the loop by hand); Labs 07 to 10 (four frameworks) |
| 4. Context and memory | the message list, a session per visitor, retrieved policies, skills | Lab 05 (skills); Labs 12 to 14 (retrieval); Lab 15 (a session per visitor) |
| 5. Delegation | a manager asking two specialists | Lab 07 (specialists as tools and a handoff); Lab 18 (when a second agent pays; its extra notebook writes an A2A card) |
| 6. Governance | read-only access, a sandbox, guards on untrusted text, tests, traces, cost | Lab 17 (a sandbox); Lab 19 (untrusted text); Lab 20 (tests and traces in MLflow) |

![The six layers of the Chinook desk agent in one row: the model, tools (standard: MCP), orchestration, context and memory (standard: Agent Skills), delegation (standard: A2A) and governance; context and memory and governance are filled in lime as the two layers that lock you in](resources/lab23_six_layers.png)

The drawing shows the conclusion of this guide: three layers have an open standard, and the two lime boxes (context
and memory, and governance) are the layers that lock you in. Context and memory has a standard and still locks you in,
because the standard moves the skill files but not the stored conversations (Part C, Step 2). Parts C to F show why.

### Step 3: Compare moving the model with moving governance

Moving a layer means running it somewhere else without rewriting the rest. Take the smallest case first.

- **Moving the model in this repository.** Almost every notebook reads the model's name from one line in
  `models.env` (`MODEL_DEFAULT=...`). Change that line (and the price lines under it, which the cost cells read), and
  almost every lab uses the new model. Nothing else changes, but the answers might: the new model may call the tools in
  a different order, or answer without calling them. So the move costs one setting plus a re-run of your tests (a golden
  set: a list of questions with known answers, which Lab 20 builds).
- **Moving governance after eighteen months with a vendor.** Imagine every prompt, tool argument and reply of the last
  eighteen months sits in a vendor's trace dashboard, and the agent's identity and permissions live in that vendor's
  directory. To leave, you must export the traces in a format another tool can read, re-create the identity, and get
  the permissions approved again. That is a project of its own.

Moving the model is like keeping your phone number in Part A: one setting changes, and nothing else is rebuilt. The
traces and the identity are like the chat backup: they exist only inside one vendor's product.

**Key lesson:** a layer moves easily when what it holds is your code or a setting. It locks you in when it holds
data or decisions that only exist inside the vendor's product.

**Checkpoint B.** You have a six-row table, one sentence per layer on what breaks without it, and you can say why
moving the model costs one setting plus a test run while moving governance is a project.

## Part C: Tell the open standards from the products

In Part A the number rule, the plug and the contact file were what let things move. Three of the six layers have
the same kind of thing now: an open standard, a published format that any vendor's product can speak. Before we read
product pages we need to know which words on them are standards and which are product names.

### Step 1: Read what each standard defines

| Standard | What it defines | Layer | The Chinook example | Status, checked 12 Nov 2026 |
|---|---|---|---|---|
| [MCP](https://modelcontextprotocol.io/specification/versioning) (Model Context Protocol) | how a host lists a server's tools and calls them | Tools | the three lookups served by an MCP server, which any MCP host can call, including hosts we did not write | current revision 2026-07-28 |
| [A2A](https://a2a-protocol.org/latest/specification/) (Agent2Agent) | how one agent finds out what another agent can do, from the card the other agent publishes, and sends it a task | Delegation | the desk agent asking a shipping agent that another team runs, on another platform | specification 1.0.0; started by Google in 2025 and handed to the Linux Foundation |
| [Agent Skills](https://agentskills.io/specification) | a folder with a `SKILL.md` file (a `name`, a `description`, then instructions) that an agent loads only when a task needs it | Context and memory | the shop's `refund-requests/` skill, read only when a customer asks for money back | open specification; OpenAI's Responses and Agents APIs, Claude Managed Agents, Foundry prompt agents, AgentCore's managed agent loop and ADK all load skills in this format |

All three are projects of the [Agentic AI Foundation](https://aaif.io/), part of the Linux Foundation, so no single
vendor owns them.

A2A is the one standard this repository never runs, so here is what its card looks like. We wrote this one for an
imagined shipping agent, using the fields the A2A specification requires:

```json
{
  "name": "Shipping Agent",
  "description": "Says where a customer's parcel is and when it will arrive.",
  "version": "1.0.0",
  "supportedInterfaces": [
    {"url": "https://shipping.example.com/a2a/v1", "protocolBinding": "JSONRPC", "protocolVersion": "1.0"}
  ],
  "capabilities": {"streaming": false},
  "defaultInputModes": ["text/plain"],
  "defaultOutputModes": ["text/plain"],
  "skills": [
    {"id": "track-parcel", "name": "Track a parcel",
     "description": "Finds a parcel by order number and gives its status and delivery date.",
     "tags": ["shipping", "tracking"]}
  ]
}
```

The shipping team publishes this file at a fixed address on its server (`/.well-known/agent-card.json`). The desk
agent's code reads it, finds the agent's name, the one thing it can do (`skills`) and where to send a task
(`supportedInterfaces`), and sends the task there. The rest says how to talk to it: A2A version 1.0
(`protocolVersion`), with each request sent as JSON-RPC, a common format for calling a function on another server
(`protocolBinding`); plain text in and out (`defaultInputModes`, `defaultOutputModes`); and each reply sent whole, not
streamed in pieces (`capabilities`). Nothing in the card says which vendor runs the shipping agent, and that is what
the standard is for.

**Write down:** for each standard, the product feature it replaces. (Without MCP, each platform would need its own
connector for the shop's database. Without Agent Skills, the refund playbook would be pasted into each product's
own instructions box.)

### Step 2: Notice what a standard does not move

A standard defines an interface, not what sits behind it. The contact file moves your contacts, but not the
chat backup.

- MCP moves the **tool interface**: any host can call `find_customer`. It does not move the database, or the
  credentials a hosted platform keeps to reach it.
- A2A moves the **conversation between agents**. It does not move the other agent's memory or who it runs as.
- Agent Skills moves the **instructions file**. It does not move the conversations an agent had while using it.

Governance has no settled standard yet. The closest is OpenTelemetry, an open format for traces that most monitoring
tools read. Several products already emit traces that follow its conventions for generative AI
([semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai)). The part of those
conventions for agents (agent spans: the records of each agent step inside a trace) is still marked **Development**,
not stable, on 12 November 2026. A trace exported in that format can be read by another tool, but the format can still
change.

**Checkpoint C.** You can name the layer each standard sits on (MCP: tools; A2A: delegation; Agent Skills: context
and memory), point at the fields of an A2A card that say what an agent can do and where to reach it, say one thing
each standard leaves behind with the vendor, and say that governance has no settled standard yet (OpenTelemetry's
generative AI agent spans are still marked Development).

## Part D: Read one agent definition in five products

Every vendor in this guide sells a way to define an agent once and let their service run it. If every agent is made
of the same six layers, what you write down to define one (a model, instructions and tools) should look alike in every
product. This part checks that, first on two real definitions, then on five products.

### Step 1: Write the desk agent's definition in plain words

Strip the desk agent down to what you would have to tell any service:

```text
model:         the model named in models.env
instructions:  You help the support reps of a music shop. Look up every fact with the tools;
               never answer from memory. Answer in one or two sentences.
tools:         find_customer, get_invoices, get_support_rep  (the shop's MCP server)
```

### Step 2: Put two real definitions side by side

The first is the desk agent as this repository writes it with the OpenAI Agents SDK, an open-source framework that
runs the loop inside our own Python (we wrote it, and it runs in Lab 07):

```python
desk = Agent(
    name="Desk",
    instructions=("You help the support reps of a music shop. Look up every fact with the tools; "
                  "never answer from memory. Answer in one or two sentences."),
    model=MODEL,                  # read from models.env
    tools=DESK_TOOLS,             # find_customer, get_invoices, get_support_rep
    model_settings=SETTINGS,      # the reasoning effort
)
```

The second is from OpenAI's [Agents API overview](https://developers.openai.com/api/docs/guides/agents-api/overview),
a hosted product where OpenAI runs the loop. It is the page's Python example, shortened: `...` marks what we cut,
including the model's name.

```python
session = client.beta.agents.sessions.create(
    agent={
        "model": "...",
        "instructions": "Use the OpenAI documentation MCP and web search to answer technical questions accurately. ...",
        "tools": [
            {"type": "programmatic_tool_calling"},
            {"type": "mcp", "server_label": "openai_docs", "transport": {...}},
            {"type": "web_search"},
        ],
        "multi_agent": {"enabled": True, "max_concurrent_subagents": 4},
    },
    environment={...},
    input=[...],
)
```

**Write down:** which fields do the two share, and what does the second one have that the first does not?

<details>
<summary><b>Our answer</b> (open after you have written yours)</summary>

Both have `model`, `instructions` and `tools`, and the second one lists an MCP server as one of its tools, the same
way the desk could list the shop's MCP server. Its other two tools are ordinary tools, not new kinds of field:
`programmatic_tool_calling` lets the model write a short JavaScript program that calls the other tools, and
`web_search` searches the web. What the second one adds sits around the definition: it creates a **session** (OpenAI
keeps the conversation), an **environment** (a sandbox where the agent runs commands) and a switch for subagents
(delegation). `input` is the first user message of that session. Our version has none of these, because our own code
keeps the messages and runs the loop.

</details>

### Step 3: Find the same three fields in five products

Here is where each product asks for them, read from each product's documentation on 12 November 2026:

| Product | Status | What you define | Where the run and its state live |
|---|---|---|---|
| [OpenAI Agents API](https://developers.openai.com/api/docs/guides/agents-api/overview) | public beta since 10 Sep 2026 (see the [changelog](https://developers.openai.com/api/docs/changelog)) | an agent: `model`, `instructions`, `tools` (MCP servers are one kind), subagents switched on with one setting; skills from folders in its sandbox | sessions that OpenAI keeps (data residency in the United States only, no zero data retention); an optional sandbox, OpenAI-hosted or your own |
| [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) (Anthropic) | beta since 8 Apr 2026 (see the [release notes](https://platform.claude.com/docs/en/release-notes/overview)) | an agent: model, system prompt, tools, MCP servers, skills | sessions in an environment (Anthropic's cloud sandbox or your own); the docs say transcripts "persist until you delete them" |
| [Microsoft Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/prompt-agents), prompt agent | generally available | a prompt agent: model, instructions, tools, skills, toolboxes | a versioned agent in the Foundry project; Foundry keeps the conversations and traces; each agent can have a Microsoft Entra identity |
| [Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html), managed agent loop (AWS calls it the AgentCore harness) | generally available (see [AWS's page on it](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html)) | a model, a system prompt (instructions), tools and skills, passed in one call | each session in an isolated microVM; short- and long-term memory kept by AgentCore |
| [Google ADK](https://adk.dev/agents/llm-agents/) agent on [Agent Runtime](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime) | ADK is open source; Agent Runtime is part of Google's Gemini Enterprise Agent Platform | an `LlmAgent`: `model`, `name`, `description`, `instruction`, `tools` | Agent Runtime hosts it; an administrator can [register it in Gemini Enterprise](https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-adk-agent) for employees to use |

**Write down before reading on:** in which columns do the five rows look alike, and in which do they differ?

### Step 4: Read what the comparison shows

- **The definition is the same in every row.** A model, instructions and tools, sometimes with skills and MCP
  servers beside them. The desk agent's three lines from Step 1 fit every product, with only the field names
  changed (`instructions`, "system prompt", `instruction`).
- **The last column is where they differ.** Who keeps the conversation (a session, a project's conversations, a
  microVM with its memory, a hosted runtime), where code runs, and who the agent runs as (an Entra identity in
  Foundry, an identity from AgentCore Identity on AWS). Those are the context and memory layer and the governance
  layer.
- **The loop is not in the definition at all.** In four of the five, you hand over a definition and the vendor runs
  the loop: orchestration is part of what you buy. AgentCore's loop is built on Strands Agents, AWS's own open-source
  framework, but you still give AWS a definition, not code. With ADK on Agent Runtime you write the agent as code with
  ADK, Google's open-source framework, and Google only hosts it. In the Agents SDK definition of Step 2, the loop runs
  in our own Python.

**Key lesson:** the agent definition is the portable part: three lines you can take to any vendor, like the contact
file. What a hosted runtime sells is everything around those lines, and that is also where it holds your data.

**Important:** "the same three fields" does not mean "the same behaviour". The vendor's loop decides how many turns a
run may take, when it shortens the context and how it retries a failed tool. Moving the definition still means
re-running your tests on the new runtime.

**Checkpoint D.** You can point at the three shared fields in the two definitions and in each row of the table, name
the two layers the last column is about (context and memory; governance), and say which layer the vendor runs from
your definition in four of the five (orchestration).

## Part E: Sort products by the four things platforms sell

Product pages list dozens of features. Sorting a product by **what it sells** before comparing prices stops you
comparing a builder with a runtime. There are four things to buy:

| What it sells | What you get | Layers | Examples, checked 12 Nov 2026 |
|---|---|---|---|
| **Build** | a page where people configure an agent without writing the loop | model, tools, context and memory (configured, not coded) | [Gemini Enterprise Workflow Builder](https://docs.cloud.google.com/gemini/enterprise/docs/agents-overview) (an administrator turns it on); Foundry prompt agents made in the Foundry portal |
| **Run** | a hosted runtime that runs a loop for you | orchestration, plus storage for context and memory | OpenAI Agents API; Claude Managed Agents; Foundry Agent Service (prompt agents, and hosted agents: your own Agent Framework, LangGraph, OpenAI Agents SDK or Anthropic Agent SDK code in a container); AgentCore Runtime and its managed agent loop; Google's Agent Runtime for ADK agents |
| **Connect** | ways to reach tools and other agents | tools, delegation | [Foundry toolboxes](https://learn.microsoft.com/en-us/azure/foundry/agents/overview) (tools behind one managed MCP endpoint) and its [A2A tool](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/agent-to-agent); AgentCore Gateway (turns APIs and Lambda functions into MCP tools); Gemini Enterprise's registration of A2A agents |
| **Govern** | identity, permissions, approvals, traces and evaluations | governance | AgentCore Identity, Policy (checks every tool call before it runs), Observability and Evaluations; Foundry's Entra identities, content filters and tracing; MLflow (open source); LangSmith (needs an account) |

Notice what is missing from the table: the **open frameworks** (the OpenAI Agents SDK, Google ADK, LangChain and
LangGraph, LlamaIndex). Nobody sells them. They are open source, and they run the loop inside your own application.
A hosted runtime is often the same kind of loop, run by someone else.

**Write down:** sort these three into the four things (one product can sell two): the OpenAI Agents API, AgentCore
Gateway, Gemini Enterprise Workflow Builder.

<details>
<summary><b>Our answer</b> (open after you have written yours)</summary>

The OpenAI Agents API sells Run, AgentCore Gateway sells Connect, and Gemini Enterprise Workflow Builder sells Build.

</details>

**Checkpoint E.** You can place each product named in Part D under Run, and name one product each under Build,
Connect and Govern.

## Part F: Decide which layers move and which lock you in

Part B argued that data and decisions inside a product are what lock you in, the way the chat backup did in Part A.
The vendors' own migration notes for four recent product changes let us check that claim, because each one says what
moved to the new product and what did not.

### Step 1: Read four product changes and what each one moved

| Change, from the vendor's page | What moved | What did not |
|---|---|---|
| OpenAI's Assistants API [shut down on 26 Aug 2026](https://developers.openai.com/api/docs/deprecations); the replacement is the Responses API with the [Conversations API](https://developers.openai.com/api/docs/guides/conversation-state), which keeps a conversation on OpenAI's servers under an id | the assistant's model, instructions and tools, recreated by hand as a prompt in the dashboard ([migration guide](https://developers.openai.com/api/docs/assistants/migration)) | the conversation history: the guide says the call that read a thread's messages "no longer works; use your stored messages instead". The loop moved back into your own code too |
| Microsoft's Foundry (classic) agents are [deprecated and retire on 31 Mar 2027](https://learn.microsoft.com/en-us/azure/foundry-classic/agents/concepts/threads-runs-messages); the new Foundry Agent Service uses conversations and responses | agent definitions, with a migration tool | stored state: the [migration guide](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/migrate) says the tool "doesn't migrate state data like past runs, threads, or messages" |
| Foundry's Connected Agents feature is not in the new Foundry Agent Service; Microsoft recommends the [A2A tool](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/agent-to-agent) (generally available for A2A 1.0) | the agents themselves | the wiring between them, rebuilt on A2A, a standard |
| OpenAI's Agent Builder is [scheduled to shut down on 30 Nov 2026](https://developers.openai.com/api/docs/deprecations); OpenAI points to the Agents SDK or ChatGPT Workspace Agents ([migration guide](https://developers.openai.com/api/docs/guides/agent-builder/migrate-from-agent-builder)) | the workflow, exported as Agents SDK code | the builder's own format: the guide says the process "does not convert your workflow graph", and it does not promise that every behaviour carries over |

Read the "What did not" column again. In each case the definition could be carried over (by hand or with a tool),
and what stayed behind or had to be rebuilt was stored conversations, the vendor's own wiring, or a builder's format.
The replacement for Connected Agents is an open standard, so the next move of that layer should be cheaper.

One more detail from the same pages: the prompts that replaced OpenAI's assistants (reusable prompt objects and the
`v1/prompts` API) are themselves scheduled to shut down on 30 Nov 2026, and the Assistants migration guide now warns
about it. A definition kept only in a vendor's dashboard may have to move twice. The three lines of Part D, kept in
your own repository, stay where they are and are copied into whichever product comes next.

### Step 2: Mark each layer portable or sticky, with its condition

**Portable** means the layer moves to another vendor with little work. **Sticky** means it locks you in.

| Layer | Portable when ... | Sticky when ... | The question to ask a vendor |
|---|---|---|---|
| 1. Model | you can point the agent at another model and re-run your tests | the agent depends on a feature only one model has | "Which models can this agent use, and can I bring my own?" |
| 2. Tools | the tools sit behind your own MCP server | they exist only in the vendor's tool catalogue | "Can the agent call my MCP server, and can my other hosts call yours?" |
| 3. Orchestration | the loop is your code or an open framework you could host elsewhere | the vendor's runtime is the only place the agent runs | "If I leave, what code do I take with me?" |
| 4. Context and memory | you can export conversations, documents and saved notes in a readable format | they live in the vendor's store, with its filters and access rules | "How do I export every conversation and memory, and in what format?" |
| 5. Delegation | the agents talk over A2A | they are wired with a vendor-only feature | "Can this agent call, and be called by, an agent on another platform?" |
| 6. Governance | identities come from your own directory and traces export in an open format | identities, approvals and eighteen months of traces exist only in the vendor's product | "Whose directory holds the agent's identity, and how do I export the traces?" |

So in practice: **model, tools, orchestration and delegation move when you choose the open option; context and
memory, and governance, are the layers that lock you in**, because they hold data that only exists after the agent has run
for a while. Go back to your list from Part A, Step 3: the prompt and the tools move, while the conversations, the logs and
the agent's identity stay, unless you planned the export.

**In production:** lock-in is not always bad. A vendor's identity, filters and audit trail may be exactly what a
risk team needs to approve an agent. The point is to choose it on purpose: buy the sticky layer you need, and keep
the rest portable. Some vendors also document a way out of their own loop: AWS shows how to export an agent from
AgentCore's managed agent loop as code for Strands Agents, its open-source framework, to run on AgentCore Runtime
([AWS's page](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html)). Once the agent is
open-source code, the orchestration layer can move again.

### Step 3: Mark items on the Chinook shop portable or sticky

For each item, write `portable` or `sticky` and one reason. Some rows have more than one defensible answer, and what
matters is the reason.

| Item | Portable or sticky? |
|---|---|
| a. The model behind the desk, changed next quarter | |
| b. The three Chinook lookups behind the shop's MCP server | |
| c. The desk agent written with LangGraph, deployed as a hosted agent on a vendor's runtime | |
| d. A year of ticket embeddings (lists of numbers, called vectors, that let a search find tickets by meaning) in a vendor's managed vector store, with its metadata filters (labels on each ticket that a search can narrow by) and access rules | |
| e. The desk agent's identity in the vendor's directory, with the permissions the risk team approved | |
| f. Eighteen months of traces (every prompt and tool argument) in the vendor's dashboard | |
| g. A shipping agent another team runs, which the desk reaches over A2A | |

<details>
<summary><b>Worked answers</b> (open after you have written yours)</summary>

| Item | Answer | Why |
|---|---|---|
| a. The model | portable | one setting to change, then a re-run of the tests |
| b. Lookups behind MCP | portable | any MCP host can call them |
| c. LangGraph on a hosted runtime | portable | the code is open source and runs anywhere; only the hosting is bought (the runtime's sessions and identity are not portable, see e) |
| d. A year of embeddings in a vendor store | sticky | the vectors can be rebuilt by embedding again, but the filters, access rules and the year of metadata live in the vendor's store. If you said "portable, we can re-embed", you are right about the vectors and wrong about the access rules |
| e. The agent's identity | sticky | it lives in the vendor's directory, and the approval has to be done again elsewhere |
| f. Eighteen months of traces | sticky | the audit trail is a project to move, unless it was exported in an open format all along |
| g. The shipping agent over A2A | portable | A2A is a standard; the desk can call it from any platform |

</details>

**Checkpoint F.** For each of the six layers you can say when it moves, when it sticks, and one question to ask a
vendor; you can quote one migration note that shows stored state staying behind; and your answers to items a, b, e
and f match the worked answers.

## Part G: Decide build, buy or neither

Parts B to F tell you what a product sells and what it would keep. The last question is whether to buy anything at
all. There are three answers, and each one needs evidence before you choose it:

| Choice | What we get | What to check before choosing it |
|---|---|---|
| **Build** | our own code (the loop, the tools, a scheduled job) run on our own machines or a runtime we choose | someone who owns it and can keep it running; access to the data and tools it needs; the tests that show it works on our cases |
| **Buy** | a vendor's product that runs one or more layers for us (Build, Run, Connect or Govern) | a real quote that says whether model tokens are included; the export questions of Part F answered; a pilot on our own cases |
| **Neither** | no new system; the work stays manual, or waits | the volume is too low to repay the work, the data the step needs is not available, or nobody owns the result |

"Neither" is a complete answer. An agent that nobody owns, or one that would run three times a year, costs more to
keep than it saves.

**Write down:** for each purchase, write build, buy or neither; if buy, which of the four things (Build, Run, Connect,
Govern); and which layer would become sticky.

| Purchase | Build, buy or neither? | If buy, which of the four? | Which layer sticks? |
|---|---|---|---|
| A. Every night, export yesterday's invoices to the finance team's shared folder, the same steps every time | | | |
| B. The Helena desk for support reps: the three lookups and the loop, already running in our own code | | | |
| C. A refund agent that customers talk to directly; the risk team asks for a per-agent identity, approval before any refund, and a year's audit trail | | | |
| D. An agent that answers questions about one vinyl box set that gets three complaints a year; nobody in the shop owns its order data | | | |

<details>
<summary><b>Worked answers</b> (open after you have written yours)</summary>

| Purchase | Build, buy or neither? | If buy | Which layer sticks? | Why |
|---|---|---|---|---|
| A. Nightly invoice export | build, as a scheduled job with no agent | nothing to buy | none | the steps are known and the same every night, so no model needs to decide the next step: that is a workflow, not an agent. [Lab 22](../22_Process_Reengineering/22_process_reengineering.ipynb) makes this choice step by step for one process, the shop's refund when the same title arrives damaged twice: it maps the process as steps, finds which steps a workflow can do and which one needs an agent, and estimates whether the redesign is worth what it costs |
| B. The Helena desk | build (it is built), or buy Run if nobody can host it | Run, only if nobody can host it | only if you buy Run: context and memory (the session store) and governance (the identity the runtime gives the agent); orchestration too, but only if you move to the vendor's own loop instead of hosting your code | it already runs in our code with tools behind MCP; buying a runtime trades hosting work for two sticky layers, the session store and the runtime's identity for the agent (three if the vendor's loop replaces our code) |
| C. Customer-facing refunds | buy | Govern, and probably Run from the same vendor | governance: the identity and the audit trail | the risk team's three demands are all governance. Buying them is a sound decision when it is made on purpose, with the export questions from Part F asked first |
| D. The box-set agent | neither | nothing | none | three questions a year will not repay the work, and with nobody owning the order data the agent has nothing reliable to read; a short answer kept by the support team does the job |

Answering B with "buy Run" is not wrong: it says you want someone else to run the loop. Then ask which sticky layers
come with it: the session store and the identity the runtime gives the agent, and orchestration as well if the
vendor's loop replaces your code.

</details>

**Checkpoint G.** Your answers to purchases A and D match the worked answers; for B and C you can give a reason that
names a layer and one thing to check before buying.

## What you can do now

- Sort what moves to a new vendor from what stays, with a standard or an export as the test.
- Name the six layers of an agent such as the Chinook desk, and say what each does on one question.
- Tell MCP, A2A and Agent Skills from the products that use them, read an A2A card, and say which layer each standard
  lets you move and what it leaves behind.
- Read a hosted agent's definition in two real examples and in five products as the same model, instructions and
  tools, and see that the differences are in context and memory and in governance.
- Sort a product into Build, Run, Connect or Govern, and say for each layer when it moves and when it locks you in,
  with the question to ask a vendor.
- Decide build, buy or neither for a purchase, and name the layer that becomes sticky if you buy.

## Challenge

1. **Write a buying brief for the desk.** Your manager wants to move the Chinook desk agent to one hosted runtime
   from Part D (choose one). For each of the six layers write: keep it as it is, or buy it from that vendor; one
   question for the vendor; and the answer that would make the layer portable. *Expected outcome:* a six-row table in
   which the model, tools and delegation can stay portable (an answer such as "yes, it calls any MCP server" is
   enough), orchestration is bought with the runtime or kept if the runtime hosts your own code (the worked answer
   does this with a Foundry hosted agent), and context and memory and governance carry the export
   questions; and a one-line recommendation that names the sticky layers you would accept.
2. **Re-check one product row.** Pick one row from Part D or Part F, open its link, find the line that states its
   status or date, and write today's date beside what you found. *Expected outcome:* the row confirmed or corrected;
   if a status changed (a beta became generally available, a product was renamed or shut down), one sentence on which
   layer the change affects and whether it makes that layer more or less portable.

A worked answer for both tasks, for Microsoft Foundry Agent Service, is in `solved/23_agent_platforms_solution.md`.

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
  [Agent Runtime](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime),
  [ADK agents](https://adk.dev/agents/llm-agents/), [ADK: Deploy to Agent Runtime](https://adk.dev/deploy/agent-runtime/)
- Open standards: [MCP versioning](https://modelcontextprotocol.io/specification/versioning),
  [A2A specification](https://a2a-protocol.org/latest/specification/) (see its Agent Card section),
  [Agent Skills specification](https://agentskills.io/specification), [Agentic AI Foundation](https://aaif.io/),
  [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)
