# 02 — Instructor notes

Weight: M. Do not cut. This is the misconception the rest of the course stands on.

## Emphasise

- The model emits a name and a JSON **string**. It does not run Python.
- Contrast the two Amsterdam calls: no tools → `finish_reason=stop` and a guessed sentence; with tools → `tool_calls` and empty `content`.
- `messages` is the list. `message` is one assistant reply. `result` is what our function returned. Say the three names when you append.
- The schema is a named dict (`get_fact_json`). `tools` is just the list we send. Lab-4 style: two dicts, one list.
- A lie in the `tool` message becomes a confident sentence. The model cannot tell.
- Two calls in one reply: inner `for`, sequential. A second turn if it only asked for one: outer cap of 3. Concurrent is 07. The named loop is 03.
- After the hand-written loop: a first look at the OpenAI Agents SDK. Two ideas: `@function_tool` vs the JSON they typed (`params_json_schema`), then `Agent` + `await Runner.run` on Amsterdam with one printed trace URL. Sessions and `draw_graph` wait for module 08.
- `model=` is a string. We stay on the class key. Other hosts exist; we do not call them. Azure is module 16.

## Pause

1. After `print(get_fact("Amsterdam"))`. The tool works with no model in sight.
2. After the **no-tools** `create`. Read `finish_reason=stop` and the guessed fact. Ask: did we touch the CSV?
3. After the **with-tools** `create`, **before** anyone runs the function. Empty `content`, `tool_calls` present. That is the cell that matters.
4. After `type of arguments`. Wait until someone says string.
5. After we call `get_fact` ourselves. Ask: has the model seen this yet? No.
6. After we print the three roles on `messages`. User / assistant / tool.
7. After the final Amsterdam sentence. Then: if we had sent back a fake fact, it would have repeated it.
8. After `print([t["function"]["name"] for t in tools])`. Two names, one list.
9. After the Sydney–Madrid + Madrid-fact loop. How many `tool_calls` in turn 1? If two, the inner `for` did the work. If one, the outer cap did. Either is correct.
9a. After `fact_tool.params_json_schema`. Put it next to `get_fact_json`. Ask: who typed this? The decorator.
9b. After `await Runner.run` on Amsterdam. Project the traces URL. Find the `fact_tool` span. If anyone used `run_sync`, that is the event-loop error. Jupyter already has a loop.
10. Challenge: they copy the Amsterdam round trip onto Istanbul. Still the hand-written loop, not the SDK.

## The cell that matters

The first `create` with `tools=`, stopped before the function runs — next to the no-tools call. If you are short on time, keep that pair, the parse-and-run cell, and skip the second tool. The misconception is already dead.

SDK first look: if late, keep `params_json_schema` next to `get_fact_json`. Cut the Amsterdam `Runner.run` if you must. Do not cut the decorator — that is why the SDK is in this module.

If nano answers Amsterdam in `content` even with `tools=`, say so. Then rerun that one cell with `tool_choice={"type": "function", "function": {"name": "get_fact"}}`. Do not add `tool_choice` to every cell — auto failing is itself a lesson.

## If it breaks

| Symptom | Likely cause |
|---|---|
| With tools, still `stop` and a fact in `content` | Model guessed. `tool_choice` on that cell, once. |
| `json.loads` fails | Bad arguments string. Print it. That is why we parse, not trust. |
| `get_fact` returns `no fact for that city` | Spelling. Istanbul / Amsterdam / Madrid are in the file. |
| Second `create` errors about tool_call_id | The `tool` message id does not match. Use `call.id`. |
| Two-part question only fetches the flight | Normal. Turn 2 should ask for the fact. If it writes a guessed Madrid fact, point at it. |
| Unexpected keyword `temperature` / `max_tokens` | Same as module 00. This notebook already avoids them. |
| Model not found | Re-pin `MODEL_DEFAULT`. |
| `from agents import ...` fails | `uv sync` from the repo root. The extra is `openai-agents[viz]`. |
| `run_sync` / “event loop is already running” | Jupyter already has a loop. Use `await Runner.run`. That cell is the lesson. |
| Bare `Runner.run` “never awaited” warning | They dropped `await`. The cell should use `await Runner.run`. |

## Challenge debrief

Same five lines as Amsterdam, city changed.

Istanbul fact, from the file: *Istanbul is the only city in the world that spans two continents: Europe and Asia.*

If someone got a sentence without calling `get_fact`, they built a chatbot. Show the solution and point at `asked_name`.

If they ran the function and never sent the `tool` message, they have the fact and no `final_text`. The model still does not know.

## Prep

- Same class key as module 00.
- Confirm `data/fun_facts.csv` and `data/flight_data.csv` are next to `chinook.db`.
- Amsterdam: more bicycles than people. Madrid: oldest restaurant, Sobrino de Botín. Sydney–Madrid: **249.66 dollars, 99 minutes** (one row). Istanbul: two continents.
- Run the no-tools call and the with-tools call once before class. If this pin of nano will not emit `tool_calls` with `reasoning_effort="none"`, that is the README warning about Chat Completions vs the Responses API. Try the same cell without `reasoning_effort` before you rewrite the notebook.
- `uv sync` already pulls `openai-agents[viz]`. Optional: system `graphviz` (`dot`) so `draw_graph` renders. The traces URL works without it.
- No extra pip. No DuckDB. No live weather. The VM only needs `api.openai.com` and the two CSVs.
