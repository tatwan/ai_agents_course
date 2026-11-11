# Lab 13: How to give an agent a search tool

**CPU | API key: `OPENAI_API_KEY` | about 65 small model calls and 50 embedding requests**

## Goal

Give the agent search as a tool, so it can search again for what a file it has just read points to. The moment is a
rep's question: *"Ticket 06's replacement arrived warped too. What do we offer now, and how long does the refund
take?"* The ticket says only that the damaged-media policy replaces a copy once; the rule for a second time is in a
policy file the question never names. One search that returns the 2 or the 4 nearest files misses that rule. Given
the search as a tool, the agent reads ticket 06, writes its own second query for the damaged-media policy, and
answers both parts. We then measure what the agent costs, and when a single search with more results is enough.

## What you will learn

- How to turn retrieval into a tool whose query the model writes, and print every query it writes.
- How to step through the agent's turns by hand before packaging them in `run_loop` with a turn cap.
- How to tell a planned split (every query written from the question) from a dependent hop (a query written from a
  file the agent has just read).
- How to compare single-shot retrieval at k = 2, 4 and 6 with the agent in correct facts, model calls, tokens and
  cost, and say when a bigger k is enough.
- How the agent stops on a question the files cannot answer, and what the turn cap is for.

## Where this lab starts

Lab 12 built **single-shot RAG**: embed every file, store the vectors in Chroma, embed the question, take the k nearest
files and pack them into the prompt with a rule to answer only from them. Lab 03 wrote the **agent loop**: send the
messages with the tools, run every tool the model asks for, append the results, and repeat until the model writes text
or a turn cap stops it. This lab gives the loop one tool, the search. The notebook restates everything it uses, so it
runs on its own; you need some Python and nothing from earlier labs.

The question asks for two facts, and the question names neither file that holds them:

1. *What do we offer now?* A refund instead of a third copy (`policy_damaged_media.md`).
2. *How long does the refund take?* 5 to 10 business days after support approves it (`policy_refunds.md`).

It names ticket 06, and the ticket names the damaged-media policy. The way to fact 1 goes through the ticket.

![Agentic RAG: the model requests a search and writes the query, our code runs retrieve and feeds the files back, the model decides whether all facts are found; a missing fact sends it round again while turns are left](resources/lab13_agentic_rag.png)

## What you will do

All of it on the Chinook music shop's 36 policy and ticket files in `data/corpus/`, read in place and indexed in
Chroma in memory.

**Part A: See why one search misses the second fact.** Index the files, read `collection.query`'s raw result, wrap it
in `retrieve`, list the six files nearest the question, and run single-shot RAG at `k=2` and `k=4` three times each.
**Part B: Give the model search as a tool.** Write the `retrieve` tool's schema by hand, run the tool on a query
about another topic to see what the model will read, and write the system message.
**Part C: Step through the turns by hand.** Turn 1: the model asks for ticket 06. Turn 2: it reads the ticket and
searches for the policy the ticket names. Then the remaining turns until it answers.
**Part D: Package the turns in a loop with a turn cap.** The same steps in `run_loop`, with a cap of 6 and a record
of every query, call and token.
**Part E: Tell a planned split from a dependent hop.** Check which words of each query came from a file already read,
on five runs of the ticket-06 question and five of a question the model can split without reading anything.
**Part F: Compare the cost with a bigger k.** Single-shot `k=6` against the agent in facts, calls, tokens and cost;
then a reworded question that moves the refund policy out of the top six.
**Part G: Stop on a question the files cannot answer.** The CEO's mobile number, three times, and the turn cap seen
on its own.
**Challenge.** Helena's rep and the first-reply time with `run_loop`, checked by the files found; then label the run
as a planned split or a dependent hop.

## Checkpoints

| After | You should see |
|---|---|
| Part A | the six nearest files with the two policies 3rd and 5th; `k=2`: neither fact (3 of 3 runs); `k=4`: the refund time, 5 to 10 business days, but not what to offer (3 of 3) |
| Part C | turn 1 searches for ticket 06; a later query names the damaged-media policy (ours, turn 2: *damaged media policy refund*); the answer has both facts |
| Part D | `run_loop`: 4 model calls, 3 searches, stopped by `answer`, both facts |
| Part E | ticket-06 question: a later query borrows a word from ticket 06 in 5 of 5 runs, both facts 5 of 5; "damaged twice" question: no borrowed word in 5 of 5, and single-shot `k=2` answers it in one call |
| Part F | `k=6`: both facts 3 of 3 in one call at 571 input tokens; the agent: 3.6 calls and about 1,965 input tokens on average, about 3 times the cost; reworded: `policy_refunds.md` 10th, `k=6` misses the refund time 3 of 3, the agent finds both |
| Part G | the CEO question: one search per run and "I don't know" with no number (3 of 3); `max_turns=1`: stopped by `turn cap`, `final_text` `None` |

**About the saved outputs.** They come from `gpt-6-luna` with reasoning effort `none`, the model named in
`models.env`, and `text-embedding-3-small` for the embeddings. The search results are the same on every run (the fourth
decimal of a distance may move). The model's replies and queries change from run to run, and from model to model if you
change `models.env`: check the facts and the shape of each run (which files, how many searches, whether a later query
uses the ticket's words), not the wording. In ten runs of each outside this notebook, single-shot `k=2` missed both
facts every time, `k=4` missed the second-time rule every time, `k=6` found both every time, and the agent found both
every time.

## Before you start

- **Lab 00 first.** It checks the environment, your key and the shop's data.
- **Open** `13_agentic_rag.ipynb` in VS Code or JupyterLab on the repository's `.venv` kernel and run the cells from
  the top. The config cell finds `models.env` and your key from the repository folder.
- **Data:** the 36 files in `data/corpus/`, read in place. Chroma runs in memory inside the notebook: nothing is
  written to disk and no server is needed.
- **Cost:** about 65 model calls of a few hundred tokens each and about 50 small embedding requests, well under one US
  cent at the prices in `models.env`. The solution notebook makes about 12 more model calls.

## Folder contents

| Path | What it is |
|---|---|
| `13_agentic_rag.ipynb` | the lab notebook, with saved outputs |
| `resources/lab13_agentic_rag.mmd` | the agentic RAG diagram's source (mermaid) |
| `resources/lab13_agentic_rag.png` | the diagram, exported from the source |
| `solved/13_agentic_rag_solution.ipynb` | the challenge, solved and run |

## Resources

- [OpenAI: function calling](https://developers.openai.com/api/docs/guides/function-calling): tool schemas,
  `tool_calls`, parallel calls, and sending results back.
- [OpenAI: embeddings](https://developers.openai.com/api/docs/guides/embeddings): what an embedding is, and a list of
  texts embedded in one request.
- [Chroma: query and get](https://docs.trychroma.com/docs/querying-collections/query-and-get): `collection.query`,
  `n_results`, and the shape of the result.
- [LangChain: retrieval](https://docs.langchain.com/oss/python/langchain/retrieval): 2-step RAG beside agentic RAG,
  with a retrieval tool given to `create_agent`.
- [OpenAI: file search](https://developers.openai.com/api/docs/guides/tools-file-search): the hosted search tool on
  the Responses API, over a vector store OpenAI keeps.

Next: [Lab 14: How to build the same RAG agent with LlamaIndex](../14_LlamaIndex_RAG/README.md). Back to
[the lab list](../README.md).
