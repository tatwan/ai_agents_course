# Bonus 01 — Instructor notes

Weight: M. Optional self-study or post-course extension. Cut first: the direct Part 1 model call. Keep prompt inspection, structured output, and the raw/parsed observation.

## The lesson

LangChain is useful before anyone builds an agent. For a data engineer, its most legible value is a set of interfaces and adapters around messages, prompts, models, structured records, and execution modes.

The sentence to repeat is:

> This is a fixed transformation, so it should remain a pipeline.

The lab deliberately avoids tools, retrieval, memory, agents, and LangGraph. Module 09 already shows what happens when control flow becomes the lesson.

## Emphasise

- `langchain-core` is contracts and primitives. `langchain-openai` is the provider adapter.
- The course still uses OpenAI only. Mentioning provider packages is architecture orientation, not permission to build a multi-provider layer.
- Formatting a prompt is local. Pause after `prompt.invoke` and ask whether an API call happened.
- `with_structured_output` validates shape and types. It does not validate truth.
- `include_raw=True` is the key observability choice. Keep token metadata and parsing errors visible.
- The `|` operator builds a `RunnableSequence`; it does not add planning or autonomy.
- `.batch()` is client-side concurrency, not the provider's offline Batch API.
- The final review queue is ordinary Python. The model does not own policy.

## Pause

1. After the package versions. Point to the independent packages.
2. After the direct message call. Walk the `AIMessage` and usage metadata.
3. After formatting the prompt. Ask: did a model run? No.
4. After printing pipeline steps. Two stages, no loop.
5. After the batch. Input order is preserved even if calls complete out of order.
6. At `raw` / `parsed` / `parsing_error`. This is the cell that matters.
7. At the review queue. Policy belongs to software.
8. At the interface methods. Common shape does not guarantee identical provider behaviour.

## If it breaks

| Symptom | Likely cause |
|---|---|
| `ChatOpenAI` import fails | Run `uv sync` from the repository root. |
| `OPENAI_API_KEY is missing` | The root `.env` was not copied or filled. |
| `json_schema` is rejected | The model pin or integration version changed. Verify current `langchain-openai` and model support. Do not silently switch to free-form JSON. |
| `parsed` is `None` | Print `parsing_error` and `raw`. The failure is part of the boundary. |
| Rate-limit errors during batch | Lower `max_concurrency` to 1 and rerun. |
| A field is factually wrong but validates | Expected distinction: schema validation is not an eval. Correct the prompt or add a deterministic check. |
| Unexpected keyword `temperature` | Do not add it for this model family. |

## Challenge debrief

The expected shape is:

- `record_id="case-004"`
- customer includes Puja Srivastava
- `issue_type="refund_request"`
- `amount_usd=36.64`
- `needs_human=True`

The exact summary sentence may differ. The verification cell intentionally tests the typed facts, not prose.

## Prep

- Run the entire student notebook except the challenge stub and verifier.
- Run the solution in the same kernel and save its outputs.
- Confirm `raw.usage_metadata` still contains input, output, and total tokens.
- Confirm provider-native `method="json_schema"` still works on `MODEL_DEFAULT`.
- No new dependency is introduced; the core course already pins LangChain for module 09.

