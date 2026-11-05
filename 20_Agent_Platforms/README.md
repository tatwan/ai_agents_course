# Lab 20: What agent platforms sell

**A reading guide | No code, no key, nothing to install | Practises: placing a vendor's product on the layers of an agent you built; saying what is portable and where lock-in lives**

## Goal

Read any agent platform's product page and say which of the six layers of an agent it sells, which of those layers
you could take to another vendor, and which would lock you in. The moment that teaches it is Part C: the Chinook desk
agent's definition, written for five products from five vendors, asks every time for the same three things (a model,
instructions and tools). What you are really buying is what runs around the definition: where the conversation is
stored, who the agent runs as, and where its traces live. Part E shows from the vendors' own migration notes that
definitions move from one product to the next and stored state does not.

## What you will learn

- How to name the six layers of an agent (model, tools, orchestration, context and memory, delegation, governance)
  on an agent you built, and place a product's features on them.
- How to tell the three open standards (MCP, A2A, Agent Skills) from the products built on them, and which layer
  each one lets you move.
- How to read a hosted agent's definition in five products as the same model, instructions and tools.
- How to sort a product by the four things platforms sell: a builder, a runtime, connections or governance.
- How to say which layers move between vendors and which lock you in, with the question to ask a vendor for each.
- How to classify a purchase on the six layers and decide what, if anything, to buy.

## Coming from

The other labs built the Chinook desk agent piece by piece: the model call (lab 01), tools (03), the loop (04),
context and skills (05), MCP (06), frameworks (07, 08), retrieval (10, 11), sessions behind a chat page (13), a
sandbox (15), a second agent (16), guards (17) and evaluation and traces (18). This guide names those pieces as the
six layers vendors sell. It re-teaches each one in a sentence, so it can be read on its own.

## What you will do

Open [GUIDE.md](GUIDE.md) and work through it, writing each answer down before you read ours.

**Part A: Name the six layers of the agent we built.** The Helena question followed through the desk agent, the six
layers in one table, and one layer moved by hand (the model) beside one that is hard to move (governance).
**Part B: Tell the open standards from the products.** What MCP, A2A and Agent Skills each fix, which layer each sits
on, and what a standard leaves behind with the vendor.
**Part C: Read one agent definition in five products.** The desk agent's definition in plain words, then the same
fields in the OpenAI Agents API, Claude Managed Agents, Microsoft Foundry Agent Service, Amazon Bedrock AgentCore and
Google ADK on Agent Runtime.
**Part D: Sort products by the four things platforms sell.** Build, Run, Connect and Govern, with dated examples.
**Part E: Decide which layers move and which lock you in.** Four product changes and what each one moved, then each
layer marked portable or sticky, with the question to ask a vendor.
**Part F: Classify layers and purchases.** A worksheet on the Chinook shop, with worked answers to open afterwards.
**Challenge.** A buying brief for moving the desk to one hosted runtime, and one product row re-checked on the day
you read it.

![The six layers of the Chinook desk agent in one row: the model, tools (standard: MCP), orchestration, context and memory (standard: Agent Skills), delegation (standard: A2A) and governance; context and memory and governance are lit as the two layers that lock you in](resources/lab20_six_layers.png)

## Checkpoints

| After | You should have |
|---|---|
| Part A | the six layers in a table, a sentence each on what breaks without it, and why moving the model costs one line plus a test run while moving governance is a project |
| Part B | MCP on tools, A2A on delegation, Agent Skills on context and memory; one thing each standard leaves with the vendor; governance's closest standard (OpenTelemetry's GenAI conventions) still marked Development |
| Part C | the same model, instructions and tools in all five products; the differences in context and memory and governance; orchestration run by the vendor's own loop in four of the five (ADK's open-source loop on Google's hosting in the fifth) |
| Part D | every Part C product under Run; one product each under Build, Connect and Govern |
| Part E | four migration notes in which definitions moved and stored state stayed behind; each layer portable or sticky with its condition and a vendor question |
| Part F | items a, b, e, f and purchase A as in the worked answers (portable, portable, sticky, sticky; no agent); a reason naming a layer for the rest |
| Challenge | a six-row buying brief with a one-line recommendation; one product row confirmed or corrected with today's date |

**About the product facts.** Every product name, status and date in the guide was read on the vendor's own
documentation on 30 October 2026, and each links to its page. Agent platforms change every few months: check a fact
on its page before you rely on it.

## Before you start

- Nothing to install and no key: the guide runs no code. A text editor or paper for your answers is enough.
- The guide is easiest after you have built or read a few of the other labs (any of 03, 04, 06 and 07), but each
  idea it uses is explained where it appears.

## Folder contents

| Path | What it is |
|---|---|
| `GUIDE.md` | the reading guide, with the worksheet and its worked answers |
| `resources/lab20_six_layers.mmd` and `.png` | the six layers diagram: its mermaid source and the exported image |
| `solved/20_agent_platforms_solution.md` | the Challenge worked for Microsoft Foundry Agent Service |

## Resources

- [OpenAI: Agents](https://developers.openai.com/api/docs/guides/agents): the Agents API, the Agents SDK and the
  Responses API compared
- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)
- [What is Microsoft Foundry Agent Service?](https://learn.microsoft.com/en-us/azure/foundry/agents/overview)
- [What is Amazon Bedrock AgentCore?](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)
- [Gemini Enterprise agents overview](https://docs.cloud.google.com/gemini/enterprise/docs/agents-overview) and
  [ADK: Deploy to Agent Runtime](https://adk.dev/deploy/agent-runtime/)
- [MCP](https://modelcontextprotocol.io/specification/versioning), [A2A](https://a2a-protocol.org/latest/),
  [Agent Skills](https://agentskills.io/specification) and the [Agentic AI Foundation](https://aaif.io/) that hosts
  them

This is the last core lab. Next: [the bonus labs](../bonus/README.md), each rebuilding part of the desk
with another framework or service. [Lab 19](../19_Process_Reengineering/README.md) (how to re-engineer a process with
agents) argues the build-or-buy decision for a whole process. Back to [the lab list](../README.md).
