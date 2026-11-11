# Lab 12: How to answer from documents with retrieval

**CPU | API key: `OPENAI_API_KEY` | about 22 small chat calls and 60 embedding calls | port 8000 for a local Chroma server**

## Goal

Answer a support rep's question from the shop's policy files: turn every file into an embedding, find the files
nearest to the question, and let the model answer only from those files, or say it does not know. The moment comes
in Part E. "When is support staffed?" puts `policy_support_reps.md` first and the file that holds the hours,
`policy_support_hours.md`, second. A search that keeps only the nearest file hands the model the wrong one, and the
model then says, politely and without any error, that the documents do not say. A question no file can answer, the
CEO's mobile number, still gets three "nearest" files. Nearest is not the same as relevant.

## What you will learn

- How to read an embedding: one vector of 1,536 numbers per text, of length 1.
- How to compute cosine similarity and squared distance by hand, and why, for vectors of length 1, they always put
  files in the same order (squared distance = 2 − 2 × cosine).
- How to split a long document into chunks whose ids point back to their source, and what a split by size breaks.
- How to store and search vectors in Chroma, reading the raw query result before a helper wraps it.
- How to answer only from the retrieved files and refuse otherwise, and how to narrow a search with a metadata
  filter.
- How to measure retrieval with hit@1 and hit@3 on labelled questions, and how to run Chroma as a server that keeps
  its data on disk.

## Where this lab starts

Labs 02 to 06 answered questions about a customer with lookups on the shop's database. A return window is not a row
in a table: it is a sentence in a policy file, and there is nothing to query. This lab finds the file and answers
from it. It needs nothing from earlier labs; the notebook restates what it uses.

![Retrieve, then generate: once, every file is embedded and stored; for every question, embed it, search the nearest k files, pack them with their names, and answer from them or say "I don't know"](resources/lab12_retrieve_then_generate.png)

## What you will do

All of it on the 36 files of `data/corpus/`: 20 policies (the shop's rules) and 16 support tickets.

**Part A: Represent a policy as an embedding.** Print `policy_returns.md`, embed it with `client.embeddings.create`,
and read the vector: its type, its 1,536 numbers and its length.
**Part B: Compare two embeddings by hand.** Compute cosine similarity and squared distance on three two-number
vectors, then on a question and two other sentences, check that squared distance = 2 − 2 × cosine, and search all 36
files with one matrix product.
**Part C: Split a long document into chunks that keep their source.** Join the 20 policies into one handbook in
memory, split it every 300 characters and see a rule cut in half, then split it at its headings with ids that point
back to the source.
**Part D: Store and search the files in Chroma.** Add the 36 files with ids, texts, labels and vectors, query the
collection directly and read the raw result, then wrap it in `retrieve`.
**Part E: Answer only from what was retrieved.** Pack the files with their names, answer from them with a rule to
refuse, run the CEO question ten times, and answer "When is support staffed?" with one file and with three.
**Part F: Filter the search by metadata.** Search only the policies with `where={"kind": "policy"}`, and see a
question that the filter makes impossible to answer.
**Part G: Measure retrieval on labelled questions.** Write ten questions with the file that answers each before
searching, compute hit@1 and hit@3 with and without the filter, and see why a score threshold is a weak guard.
**Part H: Run Chroma as a database server.** Start `chroma run` from the notebook, store and search through
`HttpClient`, stop the server, and read the same data from disk with `PersistentClient`.
**Challenge.** Split the policies into paragraphs, measure again, and make the answers cite chunks that a check in
code verifies.

## Checkpoints

| After | You should see |
|---|---|
| Part A | a `list` of 1,536 numbers, length 0.9999 (1 to about four decimals) |
| Part B | 0.40 = 2 − 2 × 0.8 on the small vectors; for the paraphrase, cosine 0.6280 and squared distance 0.7444 against 2 − 2 × cosine = 0.7440; `D` of shape (36, 1536); `policy_returns.md` first at cosine 0.6134 |
| Part C | 23 chunks by size, with the damaged-twice rule cut between `handbook[600:900]` and `handbook[900:1200]`; 20 chunks by heading, `handbook#02` holding *Damaged media* whole |
| Part D | `stored: 36`, distance `l2`; the raw result's keys, each field a list with one inner list per question; `policy_returns.md` first at 0.7736 (by hand 0.7721: the file was embedded twice) |
| Part E | the 30-day rule from a 290-token prompt; the CEO question refused with no number in 10 of 10 runs; "When is support staffed?" with `k=1`: only `policy_support_reps.md`, and "I don't know" in 5 of 5; with `k=3`: Monday to Friday, 09:00 to 17:00 |
| Part F | with the filter, no ticket in the results and `policy_digital_downloads.md` first at the same distance (0.9909) |
| Part G | over all files hit@1 4 of 8, hit@3 6 of 8; policies only hit@1 5 of 8, hit@3 6 of 8; unanswerable best scores 0.2035 and 0.3036, against 0.4147 and up for the answerable ones, three of which point at the wrong file |
| Part H | `stored on the server: 36`, the same three ids from the server and from memory, `exit code: 0`, then `read from disk: 36` with the same ids |

**About the saved outputs.** They come from `gpt-6-luna` with reasoning effort `none` and from `text-embedding-3-small`,
the models named in `models.env`. Embeddings are close to deterministic but not exactly: the same text embedded twice
can differ in the third or fourth decimal, so check the order of the files and the shape of each result, not the last
digits. Chat replies change from run to run, and from model to model if you change `models.env`: check what each
reply says (a refusal with no number, the hours or "I don't know"), not its wording.

## Before you start

- **Lab 00 first.** It checks the environment, your key and the shop's data.
- **Open** `12_retrieval.ipynb` in VS Code or JupyterLab on the repository's `.venv` kernel and run the cells from the
  top. The config cell finds `models.env` and your key from the repository folder.
- **Data:** `data/corpus/`, read in place. The handbook in Part C is built in memory; nothing is written to `data/`.
- **Part H** starts a Chroma server on port 8000 and stops it at the end of the part. It keeps its data in
  `.chroma/lab12/` inside this folder, with its log in `.chroma/server.log`; the repository ignores `.chroma/`. If
  port 8000 is taken, change `PORT` in the first cell of Part H.
- **Cost:** about 22 chat calls of a few hundred tokens and 60 embedding calls, well under one US cent at the prices
  in `models.env`. The solution notebook makes 3 chat calls and a few embedding calls.

## Folder contents

| Path | What it is |
|---|---|
| `12_retrieval.ipynb` | the lab notebook, with saved outputs |
| `resources/lab12_retrieve_then_generate.mmd` | the pipeline diagram's source (mermaid) |
| `resources/lab12_retrieve_then_generate.png` | the pipeline diagram, exported from the source |
| `resources/lab12_chunks_keep_their_source.mmd` | the chunking diagram's source (mermaid) |
| `resources/lab12_chunks_keep_their_source.png` | the chunking diagram, exported from the source |
| `solved/12_retrieval_solution.ipynb` | the challenge, solved and run |

## Resources

- [OpenAI: vector embeddings](https://developers.openai.com/api/docs/guides/embeddings): the embedding models, their
  1,536 dimensions, and why their vectors have length 1.
- [Chroma: query and get](https://docs.trychroma.com/docs/querying-collections/query-and-get): `query`, its
  `n_results` and `include`, and the shape of the result.
- [Chroma: metadata filtering](https://docs.trychroma.com/docs/querying-collections/metadata-filtering): `where` and
  its operators.
- [Chroma: configure a collection](https://docs.trychroma.com/docs/collections/configure): the distance functions
  (`l2`, `cosine`, `ip`) and how to choose one.
- [Chroma: client-server mode](https://docs.trychroma.com/docs/run-chroma/client-server): `chroma run` and
  `HttpClient`.
- [Lewis and others, Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (2020)](https://arxiv.org/abs/2005.11401):
  the paper that named RAG.

Next: [Lab 13: How to give an agent a search tool](../13_Agentic_RAG/README.md). Back to
[the lab list](../README.md).
