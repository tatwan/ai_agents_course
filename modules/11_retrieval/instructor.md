# 11 — Instructor notes

Weight: M. Cut first: the five-question retrieve table. Keep one retrieve, one answerable generate, one unanswerable generate.

## The lesson

Unstructured text is not a database. You embed, you find nearest files, you put those files in the prompt. That is single-shot RAG. Two questions in this corpus have no answer. The honest output is "I do not know." Inventing a 2014 target is a chatbot with a vector store.

This is not agentic RAG. One retrieve, one generate. Module 12 adds the loop. Module 14 shows a retrieved file can carry instructions. Do not open that door today.

## Emphasise

- When not to RAG: Helena's invoice count is SQL (08). A flight price is the CSV (02). A return window is these files.
- One file is one chunk. The files are already short. Splitting is a later decision, not a library.
- Students see the embedding: a list of floats, a length. Chroma only stores and ranks.
- Top hit for "return window" should be `policy_returns.md` (30 days, unopened).
- Unanswerable: 2014 revenue target, CEO mobile. Cover whatever the model says. If it invents a number, that is the lesson.
- LlamaIndex and Pinecone are names on a slide. We do not install them. Same retrieval, different store.

## Pause

1. After the printed `policy_returns.md`. 30 days unopened. No model.
2. After the embedding dump. Ask: is this a sentence? It is 1536 numbers.
3. After `n documents`. 36. One id per file.
4. After the return-window retrieve. Filenames and distances. Who is first?
5. After the generated 30-day answer. Cite the file if it did.
6. After the CEO mobile generate. Did it admit it, or invent a number? The 2014 target is in the retrieve table only.
7. Challenge: student discount on physical items. **10 percent.** Digital is not discounted.

## The cell that matters

Retrieve for the return window, then generate. If short: that pair plus one unanswerable. Cut the five-row table.

## If it breaks

| Symptom | Likely cause |
|---|---|
| `EMBEDDING_MODEL is missing` | Copy the line from `.env.example` into `.env`. |
| `chromadb` import fails | `uv sync` from the repo root. |
| Collection name error | Name must be at least 3 characters. The notebook uses `corpus`. |
| Empty retrieve | They pointed at the wrong folder. `ROOT / "data" / "corpus"` should have 36 `.md` files. |
| Invented 30 days with no retrieve | They skipped `tools` / stuffed the policy by hand. Show `top` filenames. |
| Challenge assert on `"10"` | Wording without the digit. Show the policy: 10 percent, physical only. |

## Challenge debrief

Physical items, 10 percent, student email. Digital albums are not discounted. Applied at checkout, not after the invoice.

If they retrieved `policy_student_discount.md` and still invented a different number, the generate step ignored the document. That is single-shot RAG failing, which is why 12 exists.

## Prep

- `uv sync` (chromadb is in `pyproject.toml`).
- `EMBEDDING_MODEL=text-embedding-3-small` in `.env`.
- 36 files under `data/corpus/`. Do not regenerate them.
- Run the return-window retrieve once so you know the top hit.
- Do not demo the planted ticket. That is 14.
- Cut first: the five-question table.
