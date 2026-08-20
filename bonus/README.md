# Bonus labs

These optional labs extend the two-day course without changing modules 00–17 or their delivery order.

They use the same room rules as the core course:

1. learn the mental model;
2. build the idea incrementally;
3. observe protocol objects, state, and cost;
4. attempt a challenge with a separate solution.

Each lab is standalone. Students do not need to run an earlier bonus lab first.

Bonus 01–03 use the core course environment. Bonus 04–08 are deliberately isolated because their frameworks resolve large, fast-moving dependency sets that would change the OpenAI SDK or MCP version used by the core modules. Run `uv sync --locked` inside the selected lab directory and choose that lab's local `.venv` in VS Code.

## Available

| Lab | Focus |
|---|---|
| [01](01_langchain_foundations/) | LangChain foundations for data engineers: integrations, messages, prompts, structured output, runnables, and batching |
| [02](02_langgraph_durable_workflows/) | LangGraph durable workflows: parallel reducers, checkpoints, interrupts, resume safety, and time-travel forks |
| [03](03_openai_agents_production_controls/) | OpenAI Agents SDK production controls: local context, guardrails, hooks, typed output, trace privacy, usage, and cost |
| [04](04_litellm_google_adk/) | LiteLLM foundations into Google ADK: model adaptation, tools, runner, sessions, events, callbacks, state, usage, and dependency isolation |
| [05](05_pydanticai_typed_agents/) | PydanticAI typed agent boundaries: dependencies, RunContext, tool and output repair, validators, usage limits, message inspection, and deterministic model tests |
| [06](06_crewai_role_based_teams/) | CrewAI role-based teams: agents, tasks, explicit context, sequential process, scoped tools, typed handoffs, deterministic guardrails, async kickoff, usage, cost, and framework restraint |
| [07](07_llamaindex_data_framework/) | LlamaIndex as a data framework: Documents, Nodes, transformations, metadata views and filters, indexing, retrieval, synthesis with sources, persistence, QueryEngine tools, agent events, usage, and data-egress boundaries |
| [08](08_autogen_message_driven_teams/) | AutoGen message-driven teams and migration literacy: AgentChat/Core/Extensions, visible tool events, composed termination, usage, governed state, restore/resume, and current Microsoft Agent Framework direction |

The core course remains the recommended live path. Bonus labs are for self-study, an extended course, or instructor-selected depth.
