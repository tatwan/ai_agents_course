# 03 — Instructor notes

Weight: L. Do not cut. Part 1 is ReAct. Part 2 is the same idea inside an object. Part 3 is the silent loop they will ship. Do not call Part 3 ReAct.

## Emphasise

- ReAct = think out loud, then act. The Thought is the product, not decoration.
- The official loop is more reliable and less visible. That is a trade, not an upgrade of ReAct.
- Frameworks wrap the loop you already wrote. Part 2 is the same `for` as Part 1, pointed at live weather, with a running cost. Part 4 is the real wrap: OpenAI Agents SDK. Same question, `await Runner.run`, a named `trace`, and `draw_graph`. They met the SDK in 02. Module 08 is the full treatment.
- Thoughts are completion tokens. Read the running cost out loud after Prague.
- Sequential question: cheaper of Barcelona → Dubai vs Barcelona → Amman, then a fact about the winner. Parallel cannot know which city wins until both flights return. Dubai is 646.86; Amman is 909.99.
- Parse by walking lines. Errors come back as text. Always a turn cap.

## Pause

1. After the three prints of Barcelona → Dubai, Barcelona → Amman, and the Dubai fact. Cover those. Dubai is cheaper.
2. After the first raw Thought/Action. Someone points at the two lines before `parse_action`.
3. After the second thought (`text2`). The plan should ask for the other flight, or name the cheaper city. This is the ReAct cell.
4. After the assembled ReAct `for`. Count observations. Honest chain is three.
5. After `print(get_weather("Prague"))`. Module 00 invented this. Today it is a number from a station.
6. After the weather `for` starts. Ask: where are `messages`? Still a list you can print. A framework will hide that later.
7. After the weather loop finishes. Read `thought tokens` and the dollar line. A chatty plan is a bill.
8. After the first official `create`, before we run tools. Same stop as module 02. No Thought on the page. Ask: do you miss it?
8b. After `await Runner.run`. Ask: where did `messages` go? Inside `Runner`. Same loop. Project the traces URL: three spans, two flights then a fact. Then `draw_graph`: one yellow box, two green ellipses. Do not start a second SDK lecture. Point at 07 (why `await`) and 08 (handoffs).
9. After official `n_tools`. 0 / 1 / 2 / 3. Three is the honest chain.
10. Challenge: Tokyo → Moscow vs Tokyo → Berlin, official loop only.

## The cell that matters

The second text thought, after the first observation. If short on time: keep Part 1 through that cell, skip the assembled text `for`, keep the Prague `for` if Open-Meteo works, keep the official assembled `for`. Cut Part 2 entirely if the VM cannot reach Open-Meteo.

If nano ignores the three-line format, retry that cell on `MODEL_STRONG`. Do not rewrite Part 3.

## If it breaks

| Symptom | Likely cause |
|---|---|
| Text reply has no `Action:` | Format miss. Point at the example. One retry or `MODEL_STRONG`. |
| Open-Meteo timeout / DNS | Skip Part 2. ReAct already landed. |
| `subtract` gets city names | The thought skipped a look-up. The observation should say it needs two numbers. |
| Official `n_tools` is 0 | Guessed Dubai or Amman. Chatbot. |
| Official `n_tools` is 1 | Skipped the comparison. The landing city was not the lesson; the cheaper city is. |
| `from agents import ...` fails | `uv sync` from the repo root. The extra is `openai-agents[viz]`. |
| `run_sync` / event loop already running | Same as 02. Use `await Runner.run`. |
| `draw_graph` errors | Missing system `dot` (graphviz). The run still happened. Use the traces URL. |

## Challenge debrief

Tokyo → Moscow is **259.3 dollars, 525 minutes**. Tokyo → Berlin is **346.16 / 609**. Moscow wins. Moscow fact: *Moscow's metro stations are often referred to as 'underground palaces'.*

`n_lookups` of 3 means both flights and the fact. 2 is a comparison without a fact, or one flight plus a fact. 1 means it skipped the comparison. 0 means it never left module 01.

Show the official solution. That is the file they copy into module 04.

## Prep

- Same class key. Same two CSVs. `requests` is in `pyproject.toml` — `uv sync` on a fresh VM.
- Guided flight answers: Barcelona → Dubai **646.86 / 829**, Barcelona → Amman **909.99 / 404**. Dubai wins. Dubai: Burj Khalifa.
- Challenge: Tokyo → Moscow **259.3 / 525**, Tokyo → Berlin **346.16 / 609**. Moscow wins. Moscow: underground palaces.
- Confirm the VM can reach `geocoding-api.open-meteo.com` and `api.open-meteo.com`. If not, Part 2 is skipped.
- Run the first text `create`, `get_weather("Prague")`, and the first official `create` once before class.
- `openai-agents[viz]` is already in `uv sync`. System `graphviz` (`dot`) is optional; the traces URL is the replay if the picture fails.
- Cut first: skip the assembled text `for` and/or all of Part 2. Keep Part 4 if you kept Part 3.
