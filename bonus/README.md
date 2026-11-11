# Bonus labs

These labs build the same Chinook support desk with other frameworks and tools, so you can compare them with the
core labs. Each lab stands alone: you do not need to run another bonus lab first. Each one has a **When to use it**
section that compares what it measured with the core path (the Agents SDK of lab 07, LangChain and LangGraph of
labs 09 and 10, Chroma of lab 12, MLflow of lab 20). [Lab 11](../11_Choose_A_Framework/README.md) sets the frameworks side by
side.

B1, B2, B3, B6 and B7 use the repository's environment. B4 and B5 have their own `pyproject.toml`, because
their frameworks need other versions of libraries the core labs share; each README says how to create that
environment and choose its kernel. B6 and B7 require accounts (Pinecone, LangSmith); check their current plan
terms. Every core lab runs without those two services.

| Lab | Title |
|---|---|
| B1 | [How to make a LangGraph workflow survive a restart](B1_LangGraph_Durable_Workflows/) |
| B2 | [How to put guardrails and approvals on an Agents SDK agent](B2_Agents_SDK_Guardrails/) |
| B3 | [How to build a typed desk agent with Pydantic AI](B3_PydanticAI_Typed_Agent/) |
| B4 | [How to build the desk as a CrewAI crew](B4_CrewAI_Crew/) |
| B5 | [How to build the desk agent with Microsoft Agent Framework](B5_Microsoft_Agent_Framework/) |
| B6 | [How to move retrieval to Pinecone](B6_Pinecone_Retrieval/) |
| B7 | [How to trace and evaluate the same agent with LangSmith](B7_LangSmith_Tracing_And_Evals/) |

Back to [the lab list](../README.md).
