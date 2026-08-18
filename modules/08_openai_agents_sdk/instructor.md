# 08 — Instructor notes

Weight: L. Do not cut the three graphs. Cut first: Part 3 (handoffs) if behind. Keep code + agents-as-tools.

## The lesson

Who decides the next step — you, or a desk model? Same two Chinook specialists, three wirings. `draw_graph` before every run. The arrows *are* the lesson.

## Emphasise

- Named tools. No free SQL. Helena is **7 / $49.62 / Steve Johnson**. Cover it before any model.
- Draw, then run, then the traces URL. That order.
- Code: you `gather` two `Runner.run`s. No manager box. Module 07.
- Agents as tools: dotted arrows **both ways**. Control comes back. Desk writes the sentence.
- Handoffs: solid arrows **one way**. `last_agent` is a specialist. The two-part question should be incomplete. The people-only question should work.
- One `Runner.run` forgets. `SQLiteSession` remembers. Do that once, before Chinook, then do not linger.
- Do not start module 13. Do not start a lecture on other model hosts.

## Pause

0. After the two Helena session prints. First pair forgets. Second pair remembers. Then Chinook.
1. After the three tool prints. 7, 49.62, Steve. Ask: did a model run? No. Then ask a volunteer for "Steve". The tool should refuse: more than one customer matches that name. That is the no-guessed-CustomerId point.
2. After `show_graph(invoices_agent)`. Yellow box, two green ellipses, dotted both ways.
3. After the `gather` cell. Two sentences. You joined them. Project the trace: sibling spans.
4. After `show_graph(desk_tools)`. Dotted both ways on `ask_invoices` / `ask_people`. Ask: who writes the final sentence? The desk.
5. After the as-tools run. All three facts? If nano skipped one, `model_strong` on that cell only.
6. After `show_graph(desk_handoff)`. Solid one way. Rounded yellow specialists.
7. After the two-part handoff. Read `last_agent`. Which fact is missing?
8. After the people-only handoff. `last_agent` is People. Steve Johnson. This is the shape handoffs are for.
9. Challenge: Puja via agents as tools. 6 / 36.64 / Jane Peacock.

## The cell that matters

The two graphs next to each other: `desk_tools` (dotted, both ways) and `desk_handoff` (solid, one way). If you only have time for one run, run as-tools on Helena.

## If it breaks

| Symptom | Likely cause |
|---|---|
| `from agents import ...` fails | `uv sync` from the repo root. |
| `run_sync` / event loop | Use `await Runner.run`. Same as 02/03/06. |
| `draw_graph` errors | Missing system `dot`. The run still happened. Use the traces URL. |
| Tools return `no customer` | Spelling. `find_customer` folds accents (`Holy` == `Holý`). First name `Helena` is unique. |
| Tools return `more than one customer matches that name` | Expected for `Steve`. Not a bug. |
| Desk skips a specialist | Nano. Rerun that cell with `model=model_strong`. |
| Two-part handoff answers everything | Rare. Point at `last_agent` anyway. If it is Desk, the handoff never fired — instructions. |
| Challenge `6` assert | They wrote a sentence with `36.64` but not the count. The regex wants a lone `6`. |

## Challenge debrief

Puja Srivastava: **6** invoices, **$36.64**, rep **Jane Peacock**.

Same `desk_tools` (or a copy). Same `await Runner.run`. If they used code-orchestration `gather` instead, that is a valid understanding — still show the as-tools solution. If they used a handoff, they will miss a fact. That is the debrief.

## Prep

- `uv sync` already pulls `openai-agents[viz]`. Optional: system `graphviz` (`dot`).
- Run the three tool prints and `show_graph(desk_tools)` before class so you have a picture.
- Run the two-part handoff once so you have seen which specialist this pin of nano picks.
- Cut first: Part 3. Keep the two graphs of Part 2 vs Part 3 if you can, even without the handoff runs.
