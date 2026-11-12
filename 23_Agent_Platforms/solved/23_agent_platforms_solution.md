# Lab 23 Challenge: worked answer

A worked answer for both Challenge tasks, using Microsoft Foundry Agent Service as the hosted runtime. Every product
fact was read on Microsoft's documentation on 12 November 2026; the links are in the guide's Parts D, E and F. Your
own answer may choose another vendor or keep different layers; what matters is that each row names a layer, a
question and the answer that would keep it portable.

## Task 1: A buying brief for moving the Chinook desk to Foundry Agent Service

Foundry offers two ways to run the desk: a **prompt agent** (we give the model, instructions and tools; Foundry runs
the loop) or a **hosted agent** (our own code, for example the desk written with the OpenAI Agents SDK or LangGraph,
in a container that Foundry runs with an endpoint, scaling and an identity). The choice decides the orchestration
layer, so the brief starts there.

| Layer | Keep or buy | Question for the vendor | The answer that keeps it portable |
|---|---|---|---|
| 1. Model | keep: the model stays a setting | "Can the agent use a model we choose, and change it without rebuilding the agent?" | "Yes: the model is one field (prompt agent) or one setting in your code (hosted agent)." |
| 2. Tools | keep: the three lookups stay behind our MCP server | "Can the agent call our own remote MCP server?" | "Yes: the agent calls any remote MCP server." Foundry documents remote MCP servers. Note that the shop's MCP server talks over stdio, a local pipe; a hosted agent needs it served over MCP's Streamable HTTP transport |
| 3. Orchestration | keep, by choosing a hosted agent | "If we leave, what code do we take with us?" | "All of it: the container is your own code and open framework." With a prompt agent the answer is "the definition", and the loop stays with Foundry |
| 4. Context and memory | buy (the conversations Foundry stores) | "How do we export every conversation, with its tool calls, and in what format?" | "Every conversation's items can be read through the API and saved in your own store." Foundry's own migration tool did not carry over past threads and messages, so we plan the export from the first day. Foundry also lets a project keep conversation state in its own Azure Cosmos DB account, which is worth asking about |
| 5. Delegation | keep: other agents over A2A | "Can the desk call, and be called by, an agent on another platform?" | "Yes: the A2A tool speaks A2A 1.0 to any compatible endpoint." Foundry's A2A tool is generally available for A2A 1.0 |
| 6. Governance | buy (the agent's Microsoft Entra identity, tracing, content filters) | "Whose directory holds the agent's identity, and can traces be exported in an open format?" | "Your Entra tenant holds it, and traces can be sent to a store you own." If the traces can only be read in the vendor's product, this layer is sticky |

**Recommendation.** Buy Run and Govern from Foundry, and build the rest. Run the desk as a Foundry hosted agent, so
the loop stays our open-source code; keep the tools behind our MCP server and the delegation on A2A. Accept two sticky
layers on purpose: the conversation store (with an export planned from day one) and governance, because a risk team
that asks for a per-agent identity and an audit trail (purchase C in the guide's Part G) gets both from an Entra
identity and Foundry's tracing.

## Task 2: Re-check one product row

We re-checked the Part F row on Foundry's Connected Agents and the A2A tool, on 12 November 2026:

- **Where:** [Connect to an A2A agent endpoint from Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/agent-to-agent),
  last updated 28 October 2026.
- **What it says:** the `a2a` tool type is generally available for A2A protocol version 1.0; the older `a2a_preview`
  type stays in preview for A2A 0.3 integrations; the Connected Agents tool from the classic Agents API is not
  available in the new Foundry Agent Service.
- **Confirmed or corrected:** confirmed (the guide says "generally available for A2A 1.0").
- **Which layer, and in which direction:** delegation. Moving from Connected Agents (a Foundry-only feature) to an A2A
  tool that is generally available makes delegation **more portable**: the desk's calls to another agent now use a
  standard that agents on other platforms also speak.
