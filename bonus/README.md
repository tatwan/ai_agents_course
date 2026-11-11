# Bonus labs

These labs build the same Chinook support desk with other frameworks and tools, so you can compare them with the
core labs. Each lab stands alone: you do not need to run another bonus lab first. Each one has a **When to use it**
section that compares what it measured with the core path (the Agents SDK of lab 07, LangChain and LangGraph of
lab 08, Chroma of lab 10, MLflow of lab 18). [Lab 09](../09_Choose_A_Framework/README.md) sets the frameworks side by
side.

B1, B2, B4, B7, B8 and B9 use the repository's environment. B3, B5 and B6 have their own `pyproject.toml`, because
their frameworks need other versions of libraries the core labs share; each README says how to create that
environment and choose its kernel. B7 and B8 require accounts (Pinecone, LangSmith); check their current plan
terms. Every core lab runs without those two services.

| Lab | Title |
|---|---|
| B1 | [How to make a LangGraph workflow survive a restart](B1_LangGraph_Durable_Workflows/) |
| B2 | [How to put guardrails and approvals on an Agents SDK agent](B2_Agents_SDK_Guardrails/) |
| B3 | [How to build and run an agent with Google ADK](B3_Google_ADK/) |
| B4 | [How to build a typed desk agent with Pydantic AI](B4_PydanticAI_Typed_Agent/) |
| B5 | [How to build the desk as a CrewAI crew](B5_CrewAI_Crew/) |
| B6 | [How to build the desk agent with Microsoft Agent Framework](B6_Microsoft_Agent_Framework/) |
| B7 | [How to move retrieval to Pinecone](B7_Pinecone_Retrieval/) |
| B8 | [How to trace and evaluate the same agent with LangSmith](B8_LangSmith_Tracing_And_Evals/) |
| B9 | [How to compose LangChain's building blocks](B9_LangChain_Building_Blocks/) |

Back to [the lab list](../README.md).
