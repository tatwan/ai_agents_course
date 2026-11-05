# Lab 12: How to build the same RAG agent with LlamaIndex

**CPU | API key: `OPENAI_API_KEY` | about 175 small model calls and a few embedding calls | its own environment (see Before you start)**

## Goal

Rebuild the search agent of lab 11 with LlamaIndex, and see which hand-written piece each LlamaIndex object replaces:
the files become `Document`s and `Node`s, an index searches them, a query engine answers from them, and a
`FunctionAgent` runs the loop. The moment comes in Parts F and G, on a rep's question that needs two files the
question does not name. Given a **query engine** as its tool, the agent never reads a file: it reads a sentence that
a second model call wrote about the files, and that sentence drops ticket 06's pointer to the damaged-media policy.
The agent then found the damaged-media policy in only 3 of 10 runs and gave both facts in 2. Given a **retriever tool**, which returns the files' text and names as lab 11's search
did, the same agent found the policy and gave both facts in 10 of 10 runs, with fewer model calls.

## What you will learn

- How to turn the shop's files into LlamaIndex `Document`s with metadata, and print what the embedding model and the
  LLM each read from one.
- How a splitter turns `Document`s into `Node`s, and why our files stay one node each at the default chunk size.
- How to build the LLM and the embedding model from `models.env`, what LlamaIndex uses when you set nothing, and how
  to count every model call's tokens from the usage the API reports.
- How to index the nodes, retrieve with the default top k, check the search against the same arithmetic done by
  hand, and narrow it with a metadata filter.
- How a query engine writes an answer from the nodes it retrieved, which prompt it sends, and where its
  `source_nodes` are.
- How to give a `FunctionAgent` a query-engine tool or a retriever tool, what each one lets the agent read, and what
  each costs in model calls.

## Where this lab starts

Lab 11 built a search agent by hand: a `retrieve` function over the 36 files, a JSON tool schema, and a loop that
sends the model's queries to the search and the files back to the model until it answers. This lab builds the same
agent in LlamaIndex, a framework for connecting a model to your data. The notebook restates everything it uses, so it
runs on its own; you need some Python and nothing from earlier labs.

![The LlamaIndex path: files become Documents, a splitter makes Nodes, the index stores one vector per Node, a retriever returns the nearest Nodes; a query engine writes a sentence from them (lit), a retriever tool returns their text and file names, and either one can be the agent's tool](resources/lab12_documents_to_answer.png)

## What you will do

All of it on the 36 files of `data/corpus/` (20 policies and 16 support tickets) and one rep's question: *"Ticket
06's replacement arrived warped too. What do we offer now, and how long does the refund take?"*

**Part A: Represent the files as documents.** Build ticket 06 as a `Document` by hand, print what the embedding model
and the LLM each read from it, then build all 36.
**Part B: Split documents into nodes.** Split the 36 documents with the default `SentenceSplitter`, read one node's
fields and links, and split a handbook of the 20 policies to see real cuts.
**Part C: Build the models from `Settings`.** Print what `Settings` holds by default, build the LLM and the
embedding model from `models.env`, call each once, and log every model call's usage with an instrumentation handler.
**Part D: Index and retrieve.** Index the nodes, retrieve with the default top k, check the ranking against cosine
similarity by hand on eight labelled questions, and filter the search to the policies.
**Part E: Ask a query engine.** Answer the question with a query engine, read its `source_nodes` and the prompt it
sent, then answer it again with the policy filter.
**Part F: Give an agent the query engine as a tool.** Wrap the engine in `QueryEngineTool`, read the schema the model
sees, run a `FunctionAgent` once with its events printed, then ten times.
**Part G: Give the agent a retriever tool instead.** Wrap a retriever in `RetrieverTool`, read what it returns, and
run the same agent ten times.
**Part H: Compare with the hand-built agent.** Run both tools with lab 11's prompt, compare every approach in calls,
tokens, cost and facts, and map each LlamaIndex piece to the hand-built one it replaced.
**Challenge.** A gift-card question with a query engine filtered to one file, and a second hop on ticket 10 with both
agents.

## Checkpoints

| After | You should see |
|---|---|
| Part A | 36 documents (20 policies, 16 tickets); ticket 06's embedding view is its text alone, its LLM view starts with `file_name: ticket_06_germany_warped_vinyl.md` |
| Part B | 36 nodes from 36 documents (the longest file 99 tokens, under the 1,024-token default); the handbook in 2 nodes at the default size and 16 at 128 tokens, with `SOURCE`, `PREVIOUS` and `NEXT` links |
| Part C | defaults that are not the models in `models.env`; ours after `Settings` is set; one logged call with its input and output tokens |
| Part D | 36 vectors in a `SimpleVectorStore`; default top k 2: ticket 06 and `policy_refunds.md`; the same top 3 as cosine similarity by hand for 8 of 8 questions (hit@1 4, hit@3 6); with the policy filter, `policy_refunds.md` and `policy_damaged_media.md` |
| Part E | one model call; sources ticket 06 and `policy_refunds.md`; fact 2 only (a refund offered, but not from the rule); with the policy filter, both facts |
| Part F | a schema with one `input` argument; tool results that are sentences with no file names; both facts in 2 of 10 runs, the damaged-media policy found in 3 of 10, about 6 model calls a run |
| Part G | each search returns two files, each starting with its `file_name` line; both facts in 10 of 10 runs, the policy found in 10 of 10, 4 or 5 model calls a run |
| Part H | with lab 11's prompt, the query-engine tool found the rule file in 5 of 5 runs and gave both facts in 3 of 5, the retriever tool 5 of 5 on both; the five-row comparison table |

**About the saved outputs.** They come from `gpt-6-luna` with reasoning effort `none` and from
`text-embedding-3-small`, the models named in `models.env`. Embeddings are close to deterministic, so the files each
search returns and their order should match ours, with the fourth decimal of a score free to move. The agents' queries
and replies change from run to run: in Parts F to H, read the counts as a spread and check the shape (which files
were found, how many model calls), not the wording. With the plain prompt, over the runs we have seen with this code (this notebook's ten of each and thirty more of each outside it), the retriever-tool agent found the damaged-media policy in 40 of 40 runs and the query-engine agent in 21 of 40, between 3 and 6 in each set of ten. A run of yours may land anywhere in that range; the difference between the two tools is the result to look for.

## Before you start

- **Lab 00 first.** It checks your key and the shop's data.
- ⚠️ **This lab has its own environment.** LlamaIndex's OpenAI integration (`llama-index-llms-openai` 0.8.3) requires
  version 2 of the `openai` library, and the repository's main environment pins version 3, so the two cannot be one
  `.venv`. This folder has its own `pyproject.toml`, `uv.lock` and `requirements.txt` with `llama-index-core` 0.14.25,
  `openai` 2.54.0 and nothing the lab does not use. Create it once:

  **With `uv`** (as in Lab 00), from the repository folder:

  ```bash
  cd 12_LlamaIndex_RAG
  uv sync --python 3.13
  cd ..
  ```

  **With `pip`**, where `uv` is blocked (Python 3.11 to 3.14):

  ```bash
  cd 12_LlamaIndex_RAG
  python -m venv .venv
  source .venv/bin/activate        # Windows: .venv\Scripts\activate
  pip install -r requirements.txt
  deactivate
  cd ..
  ```

- **Choose that environment as the kernel.**
  - **VS Code:** open `12_llamaindex_rag.ipynb`, click **Select Kernel**, choose **Python Environments**, then the one
    whose path is `12_LlamaIndex_RAG/.venv/bin/python` (Windows: `12_LlamaIndex_RAG\.venv\Scripts\python.exe`), not
    the `.venv` in the repository folder.
  - **JupyterLab:** register the lab's environment as a kernel once, from this folder:
    `.venv/bin/python -m ipykernel install --user --name lab12-llamaindex --display-name "Lab 12 (LlamaIndex)"`
    (Windows: `.venv\Scripts\python.exe -m ipykernel ...`); then start JupyterLab as usual and choose **Lab 12
    (LlamaIndex)** for this notebook.

  The notebook's second code cell prints the versions: `openai` must start with 2. If it says 3, the notebook is on
  the main kernel.
- **Run the cells from the top.** The config cell finds `models.env` and your key from the repository folder, as in
  every lab.
- **Data:** `data/corpus/`, read in place. The handbook in Part B is built in memory, and the index lives in memory;
  nothing is written to disk.
- **Cost:** about 175 chat calls of one to three thousand tokens and a few embedding calls, about one US cent in all at the
  prices in `models.env`. The solution notebook makes 19 more.

## Folder contents

| Path | What it is |
|---|---|
| `12_llamaindex_rag.ipynb` | the lab notebook, with saved outputs |
| `pyproject.toml`, `uv.lock` | this lab's own environment, for `uv sync` |
| `requirements.txt` | the same pins for `pip`, exported from `uv.lock` |
| `resources/lab12_documents_to_answer.mmd` | the diagram's source (mermaid) |
| `resources/lab12_documents_to_answer.png` | the diagram, exported from the source |
| `solved/12_llamaindex_rag_solution.ipynb` | the challenge, solved and run |

## Resources

- [LlamaIndex: defining and customizing Documents](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents/):
  metadata, excluding keys from the embedding or the LLM, and `MetadataMode`.
- [LlamaIndex: node parser modules](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/):
  `SentenceSplitter` and the other splitters.
- [LlamaIndex: configuring Settings](https://developers.llamaindex.ai/python/framework/module_guides/supporting_modules/settings/):
  the global LLM, embedding model and chunk settings.
- [LlamaIndex: using VectorStoreIndex](https://developers.llamaindex.ai/python/framework/module_guides/indexing/vector_store_index/):
  building an index from documents or nodes.
- [LlamaIndex: response modes](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/response_modes/):
  how a query engine turns retrieved nodes into an answer (`compact` is the default).
- [LlamaIndex: agents](https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/) and
  [tools](https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/tools/): `FunctionAgent`,
  `FunctionTool` and `QueryEngineTool`.
- [LlamaIndex: streaming agent events](https://developers.llamaindex.ai/python/framework/understanding/agent/streaming/):
  `stream_events` and `ToolCallResult`.
- [LlamaIndex: instrumentation](https://developers.llamaindex.ai/python/framework/module_guides/observability/instrumentation/):
  events and handlers, the module that replaces the legacy callbacks.

Next: [Lab 13: How to build a customer-support agent over a database](../13_Support_Desk_Agent/README.md). Back to
[the lab list](../README.md).
