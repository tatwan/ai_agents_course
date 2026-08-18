# 09 — Instructor notes

Weight: L. Do not cut the loop graph. Cut first: Part 3 (gate / interrupt). Keep the mermaid of the loop.

## The lesson

08 hid the arrows. Today the students **draw** them. Same Chinook tools, same Helena facts. The new sentence is: a graph can **stop** and **resume**.

## Emphasise

- Five steps: state, builder, nodes, edges, compile. The tiny graph has no model. That cell is the demystifier.
- `add_messages` appends. Without it, a node would wipe the list.
- `tools_condition` is not an LLM. It looks at `tool_calls`. Module 02.
- `ToolNode` is the inner `for` from 02. The model still does not open the database.
- Draw mermaid **before** invoke.
- `interrupt` needs `MemorySaver` and a `thread_id`. Resume is `Command(resume=...)` on the **same** config.
- We are not signing up for LangSmith.

## Pause

1. After the three tool prints. 7, 49.62, Steve. Ask: did a model run? No.
2. After `show_graph(tiny)`. One box. Then `tiny.invoke`. A dict, not a `RunResult`.
3. After `show_graph(loop)`. Point at the back-edge `tools --> chatbot`. That is the `for`.
4. After the Helena invoke. All three facts? If nano skipped one, `model_strong` on that rebuild only.
5. After `show_graph(gated)`. `gate` sits where `END` was.
6. After the first gated invoke. Someone finds `__interrupt__`. Ask: has anything been 'sent'? No.
7. After `get_state`. `next` is `('gate',)` or similar.
8. After `Command(resume='yes')`. The run finishes.
9. Challenge: Puja on `loop`, not on `gated`.

## The cell that matters

`show_graph(loop)` next to the 08 `desk_tools` graph in your head. Same job. You own the arrows here.

If short: tiny graph + loop graph + Helena invoke. Cut the gate.

## If it breaks

| Symptom | Likely cause |
|---|---|
| `from langgraph ...` fails | `uv sync` from the repo root. New extras: `langgraph`, `langchain-openai`. |
| PNG not drawn | Expected on some VMs. Read the mermaid text. |
| `tools_condition` / missing messages | State must use `messages` and `add_messages`. |
| `interrupt` errors about a checkpointer | They compiled `loop` without `MemorySaver`, or used a new `thread_id` on resume. |
| Resume starts over | Different `thread_id`. Must be `helena-1` both times. |
| Nano invents Helena | It never took the tools path. Rebuild with `model_strong`. |
| Unexpected keyword `temperature` | `ChatOpenAI` in this notebook does not pass one. Do not add it. |

## Challenge debrief

Puja Srivastava: **6** invoices, **$36.64**, rep **Jane Peacock**.

`loop.invoke` with a new messages list. If they used `gated` and forgot to resume, `final_text` will be empty or an interrupt. Show the Part 2 invoke.

## Prep

- `uv sync` after the new dependencies.
- Run the tiny graph and `show_graph(loop)` before class.
- Run the gated invoke once so you have seen `__interrupt__` on this pin of nano.
- Optional: system `dot` for PNG. Not required.
- Cut first: Part 3.
