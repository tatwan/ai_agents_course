# Bonus 07 — Instructor notes

Weight: L. Optional post-course extension. Cut first: the full metadata-view print, individual persistence filenames, and the outer FunctionAgent. Keep data classification, Document-to-Node transformation, metadata filtering, raw retrieval, source-carrying synthesis, local persistence, and the non-agentic challenge.

## The lesson

LlamaIndex is a framework for data-aware LLM applications. Documents become Nodes, transformations create retrieval-ready representations, indexes connect nodes to storage and retrieval, QueryEngines add synthesis, and tools make those engines available to agents.

The sentence to repeat is:

> Follow the data from source to Node to evidence to answer.

Do not teach LlamaIndex as a five-line RAG spell or as a vector database. Its value is the common object model and integration surface. Students should leave able to use the high-level path for speed and drop to Documents, Nodes, retrievers, storage contexts, and metadata when control matters.

## Environment boundary

This lab does not use the core `.venv`. From `bonus/07_llamaindex_data_framework/`, run:

```bash
uv sync --locked
```

In VS Code, choose:

```text
bonus/07_llamaindex_data_framework/.venv/bin/python
```

The exact pins are:

- `llama-index-core==0.14.24`;
- `llama-index-llms-openai==0.7.10`;
- `llama-index-embeddings-openai==0.6.0`;
- OpenAI 2.54.0 through the lockfile.

The environment resolves 94 installed distributions. The modular packages are intentional: do not replace them with the umbrella `llama-index` package before delivery. That would add integrations the lab does not use and make the dependency boundary less teachable.

The lab reads model names, prices, and the API key from the repository-root `.env`.

## Data boundary

This lab sends only `data/corpus/policy_*.md` to OpenAI embeddings: 20 short, customer-facing policy files. It never loads `ticket_*.md`, so support-ticket examples and the planted hostile instruction do not leave the process through this lab.

Emphasise that “the framework can read it” is not approval to embed it. Production ingestion needs classification, redaction, retention, region, legal and contractual review, and a local embedding option where required.

Do not widen the glob to `*.md` for convenience. That would defeat a load-bearing lesson and include the planted payload.

## API surface note

The core course uses OpenAI Chat Completions, where this model family requires `max_completion_tokens`. This lab deliberately uses LlamaIndex's `OpenAIResponses`, where the provider field is `max_output_tokens`. `reasoning_options={"effort": "none"}` causes the integration to remove unsupported sampling fields. This is an API-surface difference, not permission to use `max_tokens` or add `temperature`.

## Emphasise

- LlamaIndex is modular: core objects and provider/storage/reader integrations are separate packages.
- A `Document` contains text, metadata, ID, and metadata-exclusion rules.
- Metadata may be included in embeddings, LLM prompts, both, or neither. Students should inspect those views.
- `excluded_embed_metadata_keys` and `excluded_llm_metadata_keys` are context controls, not data-loss-prevention guarantees.
- `IngestionPipeline` is an ordered list of transformations. Here: split, then embed.
- A `Node` is the retrieval unit. It retains metadata, a source relationship, and a vector.
- The source relationship links a Node back to its Document; it is useful provenance, not proof that the text is trustworthy.
- `Settings` propagates model, embedding, and callback defaults through indexes and query engines. It is also global mutable state. Isolate or reset it in tests and long-lived processes.
- The local token counter propagated only after `Settings.callback_manager` was set. Passing a callback solely to the LLM object did not survive every higher-level resolver in the pinned version.
- `VectorStoreIndex` is not the vector store. This lab uses `SimpleVectorStore` through its `StorageContext`.
- Retrieval returns `NodeWithScore` evidence and makes no synthesis call.
- Metadata filtering is deterministic narrowing before vector similarity. Use it for trusted tenant, region, document type, version, or topic boundaries.
- A metadata filter cannot clean malicious text inside an allowed document.
- A QueryEngine is retriever plus response synthesis. Its `Response.source_nodes` is part of the application result.
- Persistence writes the storage context's stores. Reloading still needs an embedding model for new queries.
- A QueryEngine is valuable without an agent. `QueryEngineTool` adds an outer agent loop and extra model requests.
- The challenge intentionally rejects an agent: software already knows the gift-card topic.
- The callback count is local diagnostic evidence, not durable production observability. Current LlamaIndex observability is centered on its instrumentation system and integrations.

## Pause

1. At the diagram, ask which object is actually searched. A Node.
2. At the integration explanation, ask whether a new reader is only a convenience. No; it is also dependency and data-access surface.
3. At data classification, ask why the glob is `policy_*.md`, not `*.md`.
4. At metadata views, identify which fields reach the embedding and which reach synthesis.
5. Before the pipeline, predict whether one short policy becomes one or many Nodes.
6. At the sample Node, locate its source relationship and embedding dimension.
7. At the index, ask where vectors live. The local `SimpleVectorStore` inside the storage context.
8. Before semantic retrieval, ask whether an LLM answer will be generated. No.
9. At metadata filtering, ask why software should not ask similarity search to rediscover a known topic.
10. At the QueryEngine, inspect the answer and source rows separately.
11. At persistence, name the stores written to disk.
12. Before the agent, predict the layers of model work: outer tool choice, inner synthesis, outer final answer.
13. At the usage ledger, reconcile four LLM requests: main QueryEngine once, then three requests around the agent demonstration.
14. At the challenge, ask why `FunctionAgent` is the wrong answer.

## The cells that matter

The data path should show:

1. 20 policy files become 20 `Document` objects.
2. Metadata views exclude filename and source type from embeddings while retaining topic.
3. The pipeline produces 20 Nodes with 1,536-dimensional embeddings.
4. The damaged/refund retrieval returns `policy_damaged_media.md` and `policy_refunds.md` among its top three.
5. The topic-filtered retrieval returns only `policy_student_discount.md`.
6. The QueryEngine answers refund instead of a third copy and 5–10 business days.
7. `source_nodes` proves that damaged-media and refund policies entered synthesis.
8. Persistence writes local stores and reloads the student-discount source.
9. The FunctionAgent calls `query_support_policies` exactly once.
10. The gift-card challenge stays deterministic and uses only `policy_gift_cards.md`.

The verified run on 2026-08-20 produced:

- 20 Documents and 20 Nodes;
- 1,511 embedding tokens by the local tokenizer estimate;
- 1,536 embedding dimensions;
- semantic top three: damaged media, refunds, returns;
- QueryEngine sources: damaged media, support hours, refunds;
- five persisted files;
- one agent tool call and one result;
- four LLM requests before the challenge;
- 1,199 prompt and 287 completion tokens;
- estimated LLM cost `$0.000599`, assuming all input was uncached;
- one gift-card source in the challenge.

Scores, completion wording, and token counts can vary. Source identities and policy facts are load-bearing.

## If it breaks

| Symptom | Likely cause |
|---|---|
| `llama_index` import fails | The core kernel is selected. Choose the Bonus 07 `.venv`. |
| An optional reader or vector-store import fails | It is not installed. This lab intentionally uses only core plus the OpenAI LLM and embedding integrations. |
| `uv sync --locked` reports a stale lock | `pyproject.toml` changed. Restore the reviewed pins before regenerating. |
| `OPENAI_API_KEY`, model, embedding model, or prices are missing | The repository-root `.env` is absent or incomplete. |
| An OpenAI error mentions output limits or sampling | Keep `OpenAIResponses`, `max_output_tokens`, `reasoning_options={"effort": "none"}`, and no explicit temperature. |
| More than 20 Documents load | The glob was widened. Restore `policy_*.md`; do not load tickets. |
| Node embedding length is not 1,536 | The embedding model or its dimensions changed. Revalidate the course pin before editing the assertion. |
| Embedding token count is zero | The pipeline did not receive `embed_model`, the callback manager was not attached, or cached transformations were introduced. |
| LLM token count is zero | `Settings.callback_manager` was not set before the index/query engine was built. |
| Retrieval misses damaged media or refunds | Re-run once, then inspect metadata views and embedding pin. Do not increase `top_k` until the failure is understood. |
| The answer is correct but expected source files are absent | The model inferred or used a different node. Treat that as a provenance failure; do not grade only prose. |
| Metadata filtering returns nothing | Confirm the stored topic is `student_discount` or `gift_cards`, with underscores. |
| Reload fails with an index ID error | `set_index_id("support-policies")` was omitted before persistence or the wrong ID was loaded. |
| The temporary persistence directory is missing later | Expected. `TemporaryDirectory` removes it after the cell exits. The point is the persist/reload contract, not a committed index. |
| The agent does not call the query-engine tool | Re-run once, then inspect the system prompt and current model pin. Do not force a tool choice without discussing the changed lesson. |
| The agent calls the tool more than once | Inspect event arguments and inner results. Do not weaken the exact-one-call assertion blindly. |
| Gift-card challenge uses another source | The metadata filter was omitted from `as_query_engine` or used the wrong topic. |

## Challenge debrief

The gift-card policy says cards do not expire and cannot be exchanged for cash except where law requires it. The application already knows the question belongs to the `gift_cards` topic, so the solution creates a deterministic metadata filter and a QueryEngine. No agent is justified.

The verifier grades provenance and policy facts:

- every source is `policy_gift_cards.md`;
- the answer includes no expiration;
- the answer includes cash and the legal exception.

It does not grade exact prose or similarity score.

## Prep

- Run `uv sync --locked` only inside this bonus directory.
- Confirm LlamaIndex core 0.14.24, LLM integration 0.7.10, embedding integration 0.6.0, and OpenAI 2.54.0.
- Confirm the loader selects exactly 20 policy files and zero tickets.
- Run the student notebook through the challenge stub, then run the saved-output solution.
- Confirm 20 Nodes have embeddings and source relationships.
- Confirm damaged-media and refund policies appear in retrieval and synthesis sources.
- Confirm persistence and reload pass in the temporary directory.
- Confirm the FunctionAgent emits exactly one `ToolCall` and one `ToolCallResult`.
- Confirm usage is nonzero and the ledger distinguishes embedding tokens from LLM tokens.
- Confirm the gift-card challenge uses one source and passes every assertion.
- **Model-dependent:** after changing the model, embedding model, LlamaIndex, or OpenAI, re-run retrieval, source assertions, the agent tool call, and the challenge. Do not deliver correct prose with broken provenance.
- Recheck current package compatibility before regenerating the lockfile.

## Current documentation

- [LlamaIndex documentation](https://docs.llamaindex.ai/en/stable/)
- [Documents and Nodes](https://docs.llamaindex.ai/en/stable/module_guides/loading/documents_and_nodes/)
- [Transformations and ingestion](https://docs.llamaindex.ai/en/stable/module_guides/loading/ingestion_pipeline/transformations/)
- [Indexing](https://docs.llamaindex.ai/en/stable/module_guides/indexing/)
- [Retrievers](https://docs.llamaindex.ai/en/stable/module_guides/querying/retriever/)
- [Response synthesis](https://docs.llamaindex.ai/en/stable/module_guides/querying/response_synthesizers/)
- [Storage customization and persistence](https://docs.llamaindex.ai/en/stable/module_guides/storing/customization/)
- [Tools](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/)
- [Agent workflows](https://docs.llamaindex.ai/en/stable/understanding/agent/)
