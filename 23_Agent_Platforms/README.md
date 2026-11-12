# Lab 23: What agent platforms sell

**A reading guide | No code, no key, nothing to install | Practises: placing a vendor's product on the layers of an agent; saying which layers are portable and which lock you in; deciding build, buy or neither**

## Goal

Read any agent platform's product page and say which of the six layers of an agent it sells, which of those layers
you could take to another vendor, which would lock you in, and whether to build, buy or do neither. The guide starts
with changing phones (what comes with you, and what stays in the old maker's cloud), then asks the same question of
the Chinook support desk agent. Two parts carry the lesson. In Part D the desk agent's definition
fits five products from five vendors, because every one asks for the same three things: a model, instructions and
tools. In Part F the vendors' own migration notes show that definitions move to the next product, and what only the
vendor held (stored conversations, its own wiring, a builder's format) stays behind.

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

## What you will do

Open [GUIDE.md](GUIDE.md) and work through it, writing each answer down before you read ours.

**Part A: Sort what moves with you when you change phones.** Six things on an old phone, marked moves or stays, and
the rule behind them: a standard or an export moves; what exists only inside the maker's service stays.
**Part B: Name the six layers of the Chinook desk agent.** The Helena question followed through the desk agent, the
six layers in one table (with the lab in this repository that builds each one), and what it takes to move one layer
(the model) beside one that is hard to move (governance).
**Part C: Tell the open standards from the products.** What MCP, A2A and Agent Skills each define, which layer each
sits on, an A2A agent card read field by field, and what a standard leaves behind with the vendor.
**Part D: Read one agent definition in five products.** Two real definitions side by side (the desk agent in the
OpenAI Agents SDK, and an example from OpenAI's Agents API documentation), then the same fields in the OpenAI Agents
API, Claude Managed Agents, Microsoft Foundry Agent Service, Amazon Bedrock AgentCore and Google ADK on Agent Runtime.
**Part E: Sort products by the four things platforms sell.** Build, Run, Connect and Govern, with dated examples.
**Part F: Decide which layers move and which lock you in.** Four product changes and what each one moved, each layer
marked portable (it moves with little work) or sticky (it locks you in), with the question to ask a vendor, and seven
items on the Chinook shop to mark yourself.
**Part G: Decide build, buy or neither.** What each choice needs before you make it, and four purchases with worked
answers.
**Challenge.** A buying brief for moving the desk to one hosted runtime, and one product row re-checked on the day
you read it.

![The six layers of the Chinook desk agent in one row: the model, tools (standard: MCP), orchestration, context and memory (standard: Agent Skills), delegation (standard: A2A) and governance; context and memory and governance are filled in lime as the two layers that lock you in](resources/lab23_six_layers.png)

## Checkpoints

| After | You should have |
|---|---|
| Part A | the six phone items marked; the number, charger and contacts moving through a standard, the photos through your own copy, the chat backup and the bought apps staying; the rule in one sentence |
| Part B | the six layers in a table, a sentence each on what breaks without it, and why moving the model costs one setting plus a test run while moving governance is a project |
| Part C | MCP on tools, A2A on delegation, Agent Skills on context and memory; in the A2A card, `skills` as what the agent can do and `supportedInterfaces` as where to reach it; one thing each standard leaves with the vendor; no settled standard for governance (OpenTelemetry's generative AI agent spans still marked Development) |
| Part D | `model`, `instructions` and `tools` in both definitions, and the hosted one adding a session, an environment and subagents; the same three fields in all five products; the differences in context and memory and in governance; orchestration run by the vendor from your definition in four of the five (with ADK on Agent Runtime you write the agent's code and Google hosts it) |
| Part E | every Part D product under Run; one product each under Build, Connect and Govern |
| Part F | four migration notes in which the definition carried over, while stored conversations, the vendor's wiring or a builder's format stayed behind; each layer portable or sticky with its condition and a vendor question; items a, b, e and f as in the worked answers (portable, portable, sticky, sticky) |
| Part G | purchase A as a scheduled job with no agent, and D as neither; a reason naming a layer for B and C |
| Challenge | a six-row buying brief with a one-line recommendation; one product row confirmed or corrected with today's date |

**About the product facts.** Every product name, status and date in the guide was read on the vendor's own
documentation on 12 November 2026, and each links to its page. Agent platforms change every few months: check a fact
on its page before you rely on it.

## Before you start

- Nothing to install and no key: the guide runs no code. A text editor or paper for your answers is enough.
- The guide explains each piece of the desk agent where it uses it. It reads more easily if you have built an agent
  with tools and a loop in any of the earlier labs, but you do not need to.

## Folder contents

| Path | What it is |
|---|---|
| `GUIDE.md` | the reading guide, with the worksheets and their worked answers |
| `resources/lab23_six_layers.mmd` and `.png` | the six layers diagram: its mermaid source and the exported image |
| `solved/23_agent_platforms_solution.md` | the Challenge worked for Microsoft Foundry Agent Service |

## Resources

- [OpenAI: Agents](https://developers.openai.com/api/docs/guides/agents): the Agents API, the Agents SDK and the
  Responses API compared
- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)
- [What is Microsoft Foundry Agent Service?](https://learn.microsoft.com/en-us/azure/foundry/agents/overview)
- [What is Amazon Bedrock AgentCore?](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)
- [Gemini Enterprise agents overview](https://docs.cloud.google.com/gemini/enterprise/docs/agents-overview) and
  [Agent Runtime](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime)
- [MCP](https://modelcontextprotocol.io/specification/versioning), [A2A](https://a2a-protocol.org/latest/specification/),
  [Agent Skills](https://agentskills.io/specification) and the [Agentic AI Foundation](https://aaif.io/) that hosts
  them

Next: [the bonus labs](../bonus/README.md), each rebuilding part of the desk with another framework or service. Back
to [the lab list](../README.md).
