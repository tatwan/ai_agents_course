# Build plan — AI Agents in Practice

`AGENTS.md` loads automatically and carries the binding rules. This file is the **running order**; `AUDIT.md` is the reasoning behind it; `CURRENT_STATE.md` is the internal status table; `README.md` is the public student-facing overview. Work one module at a time. Stop for review. Do not build ahead.

**Do not trust the Status column below without running the module.** Wave 3 ran 00–09 live on 2026-08-19.

## Where we stopped

**2026-08-19, module 11 done.** Do not build module 12 next. Stop for review.

**Module 11** (`modules/11_retrieval/`): Chroma in-memory, OpenAI embeddings, one file = one chunk. Live-run this session:

- 36 files stored. Embedding dim 1536.
- Return-window retrieve: `policy_returns.md` first (distance 0.772), then warranty, damaged media. Generate: 30 days.
- Unanswerable (CEO mobile): `I do not know.` Top files were escalations / support reps / privacy.
- Observe table: gift cards -> `policy_gift_cards.md`; 2014 revenue still returns a nearest file (`ticket_04`) at distance 1.498.
- Challenge: `policy_student_discount.md` first, **10 percent** off physical. Assert passed.

`chromadb` added to `pyproject.toml` (dry-run: no `openai` / `mcp` / `langgraph` downgrade). `EMBEDDING_MODEL=text-embedding-3-small` in `.env.example`.

**Next:** module 12 (agentic RAG), one module, then stop.

**Corpus:** `data/corpus/` — 36 short markdown files (20 policies, 16 tickets) for the Chinook shop. Two unanswerable questions and the planted payload are listed in the Chinook/corpus section below. Injection against `gpt-5.4-nano` is **0/3** on four phrasings; 14 must be re-tuned before delivery.

**Module 10** (`modules/10_charting_sandbox/`): notebook, `instructor.md`, `solution.ipynb`, `sandbox.py`. Live-run this session:

- Named Chinook aggregates printed (USA 523.06 / 91; years 83/83/83/83/80).
- Hand plot `country_revenue_hand.png` 18 KB.
- Jailed probe: `env_exists True` (the lesson).
- Docker: image not present, cell printed the pre-pull instruction and moved on.
- Official loop: query then `run_python`, `country_revenue.png` 56 KB, numbers from the observation, no sqlite in the generated code.
- Challenge solution: `invoices_by_year.png` 26 KB. Assert passed.

`matplotlib` added to `pyproject.toml` (dry-run: 8 packages, no `openai` / `mcp` / `langgraph` downgrade). `mcp>=2.0.0` pinned. `chromadb` still waits for 11.

**Next:** module 11 (retrieval), one module, then stop. The corpus is ready.

**Wave 3 results (live, this session):**

| Module | Result |
|---|---|
| 00 | Solution streamed a joke and printed `prompt_tokens` + cost. Assert passed. |
| 01 | Markdown-only solution, by design. No code outputs to save. Student notebook ran. |
| 02 | Istanbul fact via `get_fact`. Two continents. Assert passed. |
| 03 | Official loop: Tokyo→Moscow 259.3 / 525, Tokyo→Berlin 346.16 / 609, then Moscow metro palaces. `n_lookups: 3`. Assert passed. |
| 04 | Challenge loop ran; assert passed. |
| 05 | `fat_tokens: 2093`, `thin_tokens: 356`, saved 1737. Assert passed. |
| 06 | `n_tools: 2`, Sydney–Madrid 249.66 / 99. Assert passed. |
| 07 | `seq_seconds: 2.0`, `gather_seconds: 1.0`. Assert passed. |
| 08 | Puja: 6 invoices, $36.64, Jane Peacock. Assert passed. |
| 09 | Same three Puja facts on `loop`. Assert passed. |

No API keys in outputs. Next is Wave 5: `data/corpus/`, then module 10. (Wave 4, the deck, is already done.)

---

**Wave 2 applied, one pass per notebook:**

- All ten student notebooks: `find_root()` replaced with `load_dotenv(find_dotenv(usecwd=True))` and `ROOT = Path(find_dotenv(usecwd=True)).parent`. (`usecwd=True` is required so this works from Jupyter and from a module folder.)
- **02:** SDK half trimmed to `@function_tool` / `params_json_schema` plus one Amsterdam `await Runner.run` + trace. 57 cells → 40. Multi-provider `base_url` cells gone. `SQLiteSession` and `draw_graph` moved to 08.
- **03 (P1):** Anchor question is now Barcelona → Dubai vs Amman. Observe diagnosis is 0/1/2/3. `ReactAgent` class cut; Prague is the same `for` plus a running cost. Challenge is Tokyo → Moscow vs Berlin. **Live-run, 1/1 each:** official loop used three tools and named the right winner (Dubai / Moscow).
- **04, 05, 07:** local `schema(tool_name, description, **props)` helper. First arg cannot be `name` — that clashes with the `name=` property on `read_skill`.
- **05 (P1):** fat/thin markdown rewritten. Shop/travel/compact padded to ~2.4 KB each. **Live-run, 3/3:** fat 2092 tokens asks `read_skill(shop)` every time; thin 355 tokens asks `lookup_count` 2/3 and `read_skill` 1/3. Token save is 1737. Re-verify fat still asks `read_skill` before delivery — that is now a model-dependent beat.
- **06:** `server.py` is `MCPServer` + `@mcp.tool()` + `mcp.run("stdio")`. `handle()` kept for the in-process wire. Hand-rolled `Popen` cells deleted (31 → 21). **Verified:** `handle` Amsterdam + Sydney–Madrid; `MCPServerStdio` listed both tools and returned the Istanbul fact.
- **08:** `find_customer` returns `"more than one customer matches that name"` (Steve is the demo). `SQLiteSession` Helena pair added. `check_same_thread=False` kept from Wave 1.
- **09:** boot cell only.

**Next: Wave 3.** Re-run all ten notebooks and solutions end to end. Commit solutions with outputs. Do not start module 10.

**Wave 2 — one editing pass per notebook.** For each module, apply every change it needs at once, then re-validate its JSON and run it end to end before moving on:

| Module | What changes in the one pass |
|---|---|
| 00, 01 | boot cell |
| 02 | boot cell, trim the SDK half |
| 03 | boot cell, **anchor question + Observe diagnosis + `instructor.md`**, cut the `ReactAgent` class |
| 04 | boot cell, `schema()` helper |
| 05 | boot cell, `schema()` helper, **rewrite the fat/thin narration**, pad the skill files |
| 06 | boot cell, rewrite `server.py` on `MCPServer`, delete notebook cells 10–21 |
| 07 | boot cell, `schema()` helper |
| 08 | boot cell, `find_customer` ambiguity, absorb `SQLiteSession` + `draw_graph` from 02 |
| 09 | boot cell |

The **bold** items are P1 — they are the ones where the notebook currently teaches something untrue. If time runs short, do the bold items and skip the rest; the boot cell and `schema()` work is polish.

**Wave 3 — prove it.** Re-run all ten notebooks and all ten solutions end to end. Commit the solutions **with outputs**.

**Wave 4 — the deck.** ~~Renumber~~ **Done already.** `ai_agents_in_practice_v3 - Repaired.pptx` (111 slides) is aligned to modules 00-17. Just confirm that is the file you present from. v1/v2 are in `archive/decks/`.

**Wave 5 — build forward.** `data/corpus/` first, then module 10.

**Module list changed.** 10 CrewAI and 11 LlamaIndex are **dropped as standalone modules** — see `AUDIT.md` §6. CrewAI downgrades `openai` and `mcp` in the shared venv and would put 00–08 at risk. Day 2 now follows the deck's list. **The next module to build is `data/corpus/`** (not a module, but 11, 12 and 14 all block on it).

> This file records the plan **as if the two open decisions at the top of `AUDIT.md` §7 are approved** — dropping CrewAI/LlamaIndex, and trimming module 02's SDK half. Both are scope calls, not findings. If either is rejected, this module list and the module 02 notes revert; nothing else in the plan changes.

Module 04 has now been live-run: both the main loop and the challenge pass on `MODEL_STRONG` in 5 turns.

Slide brief for another agent: `archive/presentation_outline.md` (modules 00–03 only).

## Goal

Two-day enterprise workshop: **AI Agents in Practice: Foundations, Frameworks, Protocols & Production**.

Audience: ~20 technical people (developers, data scientists, technical managers) on Linux VMs with VS Code and Jupyter. They know Python. They do not necessarily know agents. Half the room will have to justify the work to risk or compliance.

The room should leave able to explain what an agent is, when it should not be one, how the loop actually works, and what each later layer is for.

## How the room runs

One shape for every module. There is no code-along.

1. Instructor talks (slides / concept).
2. Instructor drives the notebook. Students watch. Nobody types.
3. Students run the same notebook at their own pace.
4. Challenge at the end (solution is not in the student notebook).
5. Instructor debriefs with `solution.ipynb`.

Each notebook: Learn / Do / Observe / Challenge. One artifact, used twice. Complete on its own. No cross-notebook imports. No emoji. `uv` for the environment. Credentials in `.env`, never printed. Model names from `.env`, never hard-coded.

## Sources — hybrid, not a copy

| File | Role |
|---|---|
| `AGENTS.md` | **Binding working rules. Follow these when anything conflicts.** Loads automatically in an agent session. |
| `archive/COURSE_PROMPT.md` | The original brief. Historical; its Rules section is carried into `AGENTS.md`. |
| `AUDIT.md` | Execution audit, 2026-08-18. The work queue. Findings marked verified were run, not read. |
| `archive/source_documents/Outline.md` | Instructor's revised spine. Architecture is sound; clock times are not. |
| `archive/source_documents/AI Agents-Outline.docx` | Prior instructor version. Azure-heavier. Mine for Day 2 Azure backup, not as the default path. |
| `archive/source_documents/AI Agents-Outline.pdf` | Original sales datasheet. Named tools are background, not requirements. |
| `archive/source_documents/AI Engineering: Agentic Track.pdf` | Notes from the Udemy-style course. |
| `presentation/ai_agents_in_practice_v3 - Repaired.pptx` | **The live deck.** 111 slides, aligned to modules 00-17. |
| `other_content/agents/` | Highly regarded reference labs. Mine patterns. Do not copy wholesale (emoji, SMTP, Pushover, paid search, MCP last). |
| `archive/CURRICULUM_REVIEW.md` | Early audit from a prior Claude session. Several decisions in it were later overruled (Pinecone four-pass, provider seam, demo/code-along/lab modes). Do not treat it as guidance. |

## Decisions already made

Keep all five design calls from `COURSE_PROMPT.md`:

1. MCP in the middle, not at the end.
2. Context engineering as its own module.
3. Open tool calling by killing "the model calls the tool."
4. Async before frameworks.
5. Compare frameworks by using them, not a logo slide. After async: OpenAI Agents SDK (08), LangGraph (09), Azure Foundry (16). CrewAI and LlamaIndex are ladder slides and a ten-minute aside in 13, not modules — see the dependency note below. Chinook is built *inside* a framework, not as another hand-rolled 07.

Other locks:

- **LLM:** OpenAI only. Shared instructor key. `MODEL_DEFAULT=gpt-5.4-nano`, `MODEL_STRONG=gpt-5.4-mini`. Verify IDs still exist before delivery. `max_completion_tokens`, not `max_tokens`. No `temperature` on this family. Pin `reasoning_effort="none"` unless a cell needs more.
- **Cloud:** Azure only, and only in module 16 plus optional instructor demos under `azure/`. Instructor-provisioned. No student Azure credential on the core path. AWS/GCP: one sentence of orientation, no lab.
- **Vector store:** Chroma, local. No Pinecone lab. If a managed store is shown at all, Azure AI Search, as an instructor demo.
- **Database:** `data/chinook.db` (sqlitetutorial edition). Do not generate a synthetic DB.
- **No shared helper package.** A `.py` file exists only when something must run as its own process (MCP server, HTTP endpoint, sandbox runner). Build the logic in the notebook first.
- **Boot cell.** Every notebook currently repeats an 11-line `find_root()`. Replace with `load_dotenv(find_dotenv())` and `ROOT = Path(find_dotenv()).parent`. Three lines, no helper module, no rule broken, ~100 lines removed across ten notebooks. It is the first code a student sees in every module, so it should not be ceremony.
- **Schemas after 02.** Hand-typing JSON schemas taught its lesson in 02. In 04, 05 and 07 use a local six-line `schema(name, description, **props)` helper defined in the notebook that uses it. That is not the forbidden abstraction layer — it makes the tool *list* readable instead of burying it in 56 lines of nesting.
- **Solutions ship with saved outputs.** They are deliberately not standalone (they run in the student notebook's kernel, which keeps them ~20 lines). Run each once at prep and commit the outputs, so the debrief survives a dead network.
- **No fixed clock.** Relative weight S/M/L plus a "cut first" note. Modules should be reorderable and skippable except the hard-order constraints in `CURRENT_STATE.md`.

## Module list

| # | Folder (when built) | Weight | Status | What it is |
|---|---|---|---|---|
| 00 | `modules/00_environment/` | S | **Built** | OpenAI API once clearly: system + user, walk the object, no-memory / no-tools (weather), stream, cost at app scale |
| 01 | `modules/01_what_is_an_agent/` | M | **Built** | What an agent is, and when it should not be one |
| 02 | `modules/02_tool_calling/` | M | **Built** | Tool calling: the model does not call the tool |
| 03 | `modules/03_react_loop/` | L | **Built** | The ReAct loop |
| 04 | `modules/04_coding_agent/` | M | **Built** | A small coding agent, then break it |
| 05 | `modules/05_context_engineering/` | M | **Built** | Context engineering |
| 06 | `modules/06_mcp/` | M | **Built** | Why MCP exists |
| 07 | `modules/07_async/` | M | **Built** | Async and concurrent tool calls |
| 08 | `modules/08_openai_agents_sdk/` | L | **Built (P0 applied)** | OpenAI Agents SDK — Chinook, three orchestrations, `draw_graph`. `check_same_thread=False` is in cell 3. Full live re-run is Wave 3. |
| 09 | `modules/09_langgraph/` | L | **Built (P0 applied)** | LangGraph — same Chinook desk, you draw the arrows, pause/resume. Same P0 line applied. Full live re-run is Wave 3. |
| 10 | `modules/10_charting_sandbox/` | M | **Built** | Charting agent and the sandbox — Chinook bar charts, jailed `run_python`, optional Docker. Live-run 2026-08-19. |
| 11 | `modules/11_retrieval/` | M | **Built** | Retrieval — Chroma, one file one chunk, two unanswerable questions. Live-run 2026-08-19. |
| 12 | | M | Not started | Agentic RAG |
| 13 | | L | Not started | Delegation (CrewAI gets ten minutes here, not a module) |
| 14 | | L | Not started | Security |
| 15 | | M | Not started | Evals, traces, cost |
| 16 | | M | Not started | Azure Foundry / platform landscape |
| 17 | | L | Not started | Process re-engineering |

**Day 1 is 00–09. Day 2 is 10–17.** The deck agrees: slide 66 is "DAY TWO", immediately after the framework ladder.

Hard order: 00 first. 03 before 04 and 05. 07 before 08–09. 06 before a framework consumes MCP. 01 before 17. `data/corpus/` before 11, 12 and 14.

Natural stops: after 03 they have an agent; after 08 they have used a modern SDK; after 09 is the cleanest day-one close.

**Dropped:** CrewAI and LlamaIndex as standalone modules. Both are taught on the framework-ladder slides (61–62, already written); CrewAI's roles/goals/backstory concept gets ten minutes inside 13. Reason: CrewAI adds 91 packages and downgrades `openai` 3.2.0 → 2.54.0 and `mcp` 2.0.0 → 1.28.1 in the shared venv, which is what 00–08 run on. Verified by dry-run install.

## What module 00 contains now

`modules/00_environment/{notebook.ipynb, instructor.md, solution.ipynb}`

1. Load `.env`. Print `OPENAI_API_KEY is set: True`, never the value.
2. One call: `system` (put the answer on its own last line) + `user` (a two-line riddle about a music shop). Prompts stay on one line.
3. Walk `id`, `model`, `choices[0]`, `finish_reason`, `message.role`, `message.content`, `usage`. Raw dump. Plant that `tool_calls` will appear on this same `message` in module 02.
4. **No memory:** new `create()` asks what the riddle was, without sending the riddle or the system message back.
5. **No tools:** ask for the weather in Prague right now. The number is invented. Flight status is named as the same failure.
6. Same riddle streamed in three cells: print each `delta`, then append into `text`, then add `include_usage` and keep `usage`.
7. Observe: tokens, reasoning tokens, dollars, then 1,000 and 100,000 of the same call. Cost is framed as an app or a company loop, not this room.
8. Challenge: stream a joke (the `include_usage` form), bind `text`, `prompt_tokens`, and `cost`. Solution is the same loop, linear, no helper function. Same kernel as the student notebook.

If the room already lives in this SDK, cut streaming and keep the usage cell. Keep the weather cell.

## What module 01 contains now

`modules/01_what_is_an_agent/{notebook.ipynb, instructor.md, solution.ipynb}`

1. Learn: chatbot vs workflow vs agent. Who decides the next step. Anatomy, autonomy spectrum (plant for 17), three places an agent is the wrong default.
2. Tiny shop dict: Helena (7, Steve Johnson), Puja (6, Jane Peacock). Two functions. Real sqlitetutorial numbers, no database yet.
3. Workflow: count, then rep. Zero model calls.
4. Chatbot: same question, invents.
5. Scripted plan `["COUNT helena", "REP helena", "DONE"]` so the loop is ordinary Python.
6. Live loop: model emits one of those lines, we run the function, we send `Observation:`. Cap of 4.
7. Observe: print the message list; compare call counts and whether the functions ran.
8. Challenge: group table in markdown. Eight jobs, three columns (shape, who decides, how far). Empty on purpose. No scoring cell. Filled table and the 7/8 argument live in `solution.ipynb`.

Cut first: shrink the pair to overdue vs messy ticket. If the API is down, keep workflow + scripted plan and skip chatbot + live.

## What module 02 contains now

`modules/02_tool_calling/{notebook.ipynb, instructor.md, solution.ipynb}`

Uses `data/fun_facts.csv` and `data/flight_data.csv` with the `csv` module. No DuckDB. No live weather (same pattern; we stay local). Chinook still waits for 08/09.

1. Learn: `LLM -> TOOLS` vs `SOFTWARE -> TOOLS`. `tool_calls` on the same `message` as module 00. `arguments` is a string.
2. `get_fact` as a plain function. Amsterdam, no model.
3. Same Amsterdam question **without** `tools=`. `finish_reason=stop`, guessed `content`.
4. Named schemas: `get_fact_json`, later `get_flight_json`. `tools = [{"type": "function", "function": ...}, ...]`.
5. Same question **with** `tools=`. Stop. Look. Remind: `messages` is the list, `message` is this assistant ask, `result` is our function.
6. Parse, run, append both turns, second `create`.
7. Two-part question: Sydney–Madrid flight (249.66 / 99 min) and a Madrid fact. Inner `for` if two `tool_calls` in one reply; outer cap of 3 if it asks one at a time. Seed of 03, not ReAct.
8. **SDK first look** (four steps, then Amsterdam). (1) `Agent` + `model=` as a string, then the long form `OpenAIChatCompletionsModel` (other hosts exist; we stay on the class key) + bare `Runner.run` (coroutine) + `await Runner.run` — never `run_sync` in Jupyter. (2) named `trace` + printed traces URL. (3) `@function_tool` + `params_json_schema` next to the hand-typed `get_fact_json`, then Amsterdam + `draw_graph`. (4) two `Runner.run`s forget Helena; `SQLiteSession` in memory remembers. Module 08 is the full SDK.
9. Challenge: Istanbul fact, same single-tool round trip.

Istanbul fact: two continents. If nano answers in `content` instead of `tool_calls`, one-cell `tool_choice` override. (Chat Completions + `reasoning_effort="none"` emitting tool calls is now **confirmed** — see Verify before delivery.)

> **Trim the SDK half (P2).** Step 8 above is 22 cells and eight new concepts inside a notebook about one mechanic, with no challenge attached to any of it. Keep only `@function_tool` + `params_json_schema` next to the hand-typed `get_fact_json`, and `Agent` + `await Runner.run` on Amsterdam with one trace URL. `SQLiteSession` and `draw_graph` move to 08. The `OpenAIChatCompletionsModel` / Gemini `base_url` cells are cut — they break the one-provider rule in `COURSE_PROMPT.md`. 57 cells becomes ~40.

## What module 03 contains now

`modules/03_react_loop/{notebook.ipynb, instructor.md, solution.ipynb}`

Three parts, not alternatives. ReAct is think-out-loud plus action. The official loop is silent.

> **Anchor question must change (P1).** "A fun fact about the city I land in if I fly from Barcelona to Amman" **never chains** — the landing city is in the prompt, so nano skips `get_flight` and goes straight to `get_fact("Amman")`. Verified 3/3 on the main question and 3/3 on the Tokyo → Moscow challenge. The Observe cell and `instructor.md` then teach a wrong diagnosis.
>
> Verified replacement, 3/3 with the right three calls and the right winner:
> **"From Barcelona, is it cheaper to fly to Dubai or to Amman? Give me a fun fact about whichever one is cheaper."**
> Barcelona → Dubai 646.86 / 829. Barcelona → Amman 909.99 / 404. Dubai wins. `n_tools` is genuinely 3.
> Do **not** use a totals-and-sums question instead: nano gets the arithmetic wrong and invents legs.
> The Tokyo → Moscow challenge needs the same treatment.

1. Learn: course map, ReAct vs official table (from Activity 5), thoughts are output tokens.
2. **Part 1 — ReAct.** Broken down, then the `for`.
3. **Part 2 — same ReAct, wrapped.** `ReactAgent` is the loop they wrote, hidden on `self`. Live Open-Meteo: is Prague warmer than Amsterdam, and by how many degrees? `get_weather` + `subtract` (no `eval`). Print completion tokens and running cost. Skip if the VM cannot reach Open-Meteo. **Cut the 45-line class; keep the live Prague callback to module 00 and the running-cost print.**
4. **Part 3 — the official loop.** Not ReAct. `tool_calls`. Same question.
5. **Part 4 — OpenAI Agents SDK taste.** Same question. Talking points, then `@function_tool` + `Agent` + `await Runner.run` + named `trace` + `draw_graph` (two green ellipses). Full SDK is module 08.
6. Challenge: official loop, Tokyo → Moscow (259.3 / 525, metro palaces).

`requests` is now in `pyproject.toml`.

## What module 04 contains now

`modules/04_coding_agent/{notebook.ipynb, instructor.md, solution.ipynb, workspace/, starter/}`

Lesson: a coding agent (Cursor, Claude Code, Copilot) does not touch files. Five functions are the hands. Official loop from 03 runs them.

`pricing.py` and `test_pricing.py` live on disk and are explained in markdown. Resets copy from `starter/`. No `write_text` of the first bug.

1. Learn: product association, why five tools (table), jail, no `run_bash`. Skills/`map.md` named as module 05, not built here.
2. `safe_path` refuses `../.env`.
3. Call the five functions yourself. Tests fail (110 vs 90).
4. Schemas, one `create`, one dispatch, then the `for`. `MODEL_STRONG`.
5. Observe: read the file, run the tests.
6. Break 1: `write_file` / `save_file`. Break 2: cap of 2.
7. Challenge: copy `totals` from `starter/`. `qty + price` should be multiply.

Cut first: both break cells.

## What module 05 contains now

`modules/05_context_engineering/{notebook.ipynb, instructor.md, solution.ipynb, skills/}`

Lesson: the list is a budget. Progressive disclosure (map + `read_skill`) vs stuffing every playbook. Compaction when the list has grown. Same idea as the other class's `map.md` / skills, measured with `prompt_tokens`.

Skill files are on disk (`map`, `shop`, `travel`, `compact`). Not generated in a cell.

> **Narration is inverted (P1).** Verified 3/3: the **fat** prompt asks for `read_skill` (a playbook it already carries); the **thin** prompt goes straight to `lookup_count`. Fat 518 prompt_tokens, thin 355, saved 163 (31%). Rewrite that markdown around what actually happens — "stuffing the context made it behave worse" is a better lesson than the scripted one. Also pad the four skill files (currently 1,070 chars total) to realistic playbook length using `other_content/05 Coding Agents/skills/`.

1. Learn: seven inputs, course map, cut compaction if behind.
2. Map vs all-playbooks character counts.
3. Fat vs thin first `create` on “How many invoices does Helena have?” — the cell that matters.
4. Thin official loop should `read_skill` then `lookup_count`. Answer is 7.
5. Compaction: summarise, replace the middle, ask again. Forgetting is a valid outcome.
6. Challenge: same fat/thin measurement for an Amsterdam fact. Assert `thin_tokens < fat_tokens`.

Cut first: compaction.

## What module 06 contains now

`modules/06_mcp/{notebook.ipynb, instructor.md, solution.ipynb, server.py}`

Lesson: tools in the notebook do not travel. MCP is agent→tool. Same `get_fact` / `get_flight`, other process, JSON-RPC. No Inspector, no npm. stdio only.

> **Rewrite `server.py` on the real SDK.** `mcp` 2.0.0 is already installed via `openai-agents`. `MCPServer` + `@mcp.tool()` + `mcp.run("stdio")` is ~12 lines and replaces the current 150-line hand-rolled dual-framing server. Verified end to end (`tools/list` and `tools/call` both return correctly). Then delete notebook cells 10–21 — the `subprocess.Popen` / `rpc_send` / `rpc_read` / header-parsing block. **Keep** the in-process `handle()` cells and the one framed-request print: that is the demystifying moment and it costs nothing. **Keep** the SDK-as-host cell — verified working today, and it is the portability payoff.
>
> Version trap: mcp 2.0 has **no `mcp.server.fastmcp`**. It is `mcp.server.mcpserver.MCPServer`, and `Tool.inputSchema` is now `Tool.input_schema`. The FastMCP code in `other_content/agents/6_mcp/` targets 1.x and will not run here.

1. Learn: host / server / stdio vs HTTP. MCP ≠ A2A. Descriptions on the wire (plant 14).
2. Import `server.handle` first. No model. `tools/list` and `tools/call` Amsterdam.
3. Print one framed request (the protocol trace).
4. Spawn `server.py`. `initialize`, `tools/list`, `tools/call`.
5. Translate `tools/list` into OpenAI schemas. Official loop for Istanbul via the server.
6. Observe: in-process function, `handle`, subprocess — same string. Then shut the hand-rolled `proc`.
7. **SDK as host.** Talking points, then `MCPServerStdio` + `await Runner.run` + named `trace` (MCP tool spans) + `draw_graph` (grey box = `server.py`).
8. Challenge: `tools/list` + `get_flight` Sydney–Madrid (249.66 / 99). In-process `handle` is enough.

Cut first: extra framing talk and/or the model loop. Keep `handle` before any model.

## What module 07 contains now

`modules/07_async/{notebook.ipynb, instructor.md, solution.ipynb}`

Lesson: independent tool calls should run together. Primer walks `def` → `async def` (call returns a coroutine, not the result) → `await` → `gather` (tickets, not already-awaited results; clock is the slower one). Sleep stands in for I/O. Official loop dispatches a pair with `gather`. On-ramp to `await Runner.run` in 08.

Challenge: Istanbul fact + Tokyo–Moscow flight, `gather_seconds < seq_seconds`.

## What module 08 contains now

`modules/08_openai_agents_sdk/{notebook.ipynb, instructor.md, solution.ipynb}`

Lesson: one shop (Chinook), two specialists (Invoices, People), three wirings. `draw_graph` before each run. Same Helena question (7 / $49.62 / Steve Johnson).

> **P0: this module does not run.** The SDK executes sync `@function_tool` functions in a worker thread, so every Chinook query raises a SQLite threading error — and the model *apologises* rather than crashing, so it looks like a model limitation. Fix is one line in cell 3: `sqlite3.connect(ROOT / "data" / "chinook.db", check_same_thread=False)`. Verified after the fix: Part 1, Part 2 and the Puja challenge all 3/3.
>
> Also: `find_customer` silently returns `hits[0]` when several customers match ("Steve" returns Victor Stevens). Return an honest "more than one customer matches that name" — it makes the module's own no-guessed-CustomerId point.

1. Learn: who decides. ASCII of code vs `as_tool` (dotted, both ways) vs handoff (solid, one way).
2. Named tools over `chinook.db`. No free SQL. Prints before any model.
3. `show_graph(invoices_agent)` / `people_agent`.
4. **Code orchestrates.** `asyncio.gather` of two `Runner.run`s. You are the graph.
5. **Agents as tools.** `desk_tools` + `draw_graph` + one `Runner.run`. Control comes back.
6. **Handoffs.** Same two-part question (expect incomplete, read `last_agent`). Then people-only (should work).
7. Observe: table of the three wirings.
8. Challenge: Puja via agents as tools (6 / $36.64 / Jane Peacock).

Cut first: Part 3 runs. Keep the two graphs if you can.

## What module 09 contains now

`modules/09_langgraph/{notebook.ipynb, instructor.md, solution.ipynb}`

Lesson: 08 hid the arrows. LangGraph is the arrows. Same Chinook named tools, same Helena question.

> **P0: this module does not run.** Same root cause as 08 — `ToolNode` runs tools off-thread — but here it raises a hard `ProgrammingError` that kills the cell. Same one-line fix in cell 3. Verified after the fix: Part 2 and the Puja challenge both 3/3.

1. Learn: State / Node / Edge. `tools_condition` is not an LLM. `interrupt` is why you pick a graph.
2. Same three tools via LangChain `@tool`. Prints before any model.
3. **Part 1 — no model.** `TinyState`, one `lookup` node, mermaid, `invoke` returns a dict.
4. **Part 2 — the official loop as a graph.** `chatbot` + `ToolNode` + `tools_condition` back-edge. Helena (7 / 49.62 / Steve).
5. **Part 3 — pause / resume.** `gate` uses `interrupt`. `MemorySaver` + `thread_id`. `get_state`. `Command(resume='yes')`.
6. Observe: 08 vs 09 table.
7. Challenge: Puja on `loop` (6 / 36.64 / Jane Peacock).

Cut first: Part 3. Keep the loop mermaid.

`pyproject.toml` now includes `langgraph`, `langchain-openai`, `langchain-core`.

## What module 10 contains now

`modules/10_charting_sandbox/{notebook.ipynb, instructor.md, solution.ipynb, sandbox.py}`

Lesson: the model writes matplotlib; your code starts the process. A timeout plus `cwd=` is not a sandbox — the child can still see `../../../.env`. Docker (`python:3.12-slim`, `--network none`, only `charts/` mounted) is the first real filesystem boundary. Pre-pull the image into the VM. Do not pull in class.

1. Learn: four controls as separate columns. ASCII of unconstrained vs jail vs Docker.
2. Named Chinook aggregates (`invoices_by_country`, `invoices_by_year`). Prints, no model. USA 523.06 / 91; years 83/83/83/83/80.
3. You plot first. `country_revenue_hand.png`.
4. `run_jailed` in the notebook (timeout, `cwd=charts/`, no API key in the child). Then `sandbox.py` — same function, extracted because Docker needs a process.
5. Planted snippet: `Path("../../../.env").exists()`. Jail: True. Docker: False if the image is local; otherwise print the pre-pull line and skip.
6. Official loop. Query first, then `run_python`. The child has no database; numbers come from the observation.
7. Observe: generated code, no sqlite, PNG bytes.
8. Challenge: invoice **count** by year, `invoices_by_year.png`.

Cut first: Docker. Keep the jail probe.

`MODEL_STRONG` when set (this is code generation). matplotlib is in `pyproject.toml`.

## What module 11 contains now

`modules/11_retrieval/{notebook.ipynb, instructor.md, solution.ipynb}`

Lesson: unstructured text is not a table. Embed, nearest files, generate. One retrieve, one generate. Two questions have no answer.

1. Learn: RAG vs SQL vs a CSV tool. One file is one chunk. Chroma stores; OpenAI embeds.
2. Read `policy_returns.md` with no model. 30 days unopened.
3. Embed one sentence. Print dimension and the first eight floats.
4. Load 36 files into an in-memory collection with our vectors.
5. Retrieve the return window. `policy_returns.md` first.
6. Generate from those three files.
7. Unanswerable: CEO mobile. "I do not know" is a valid outcome.
8. Observe: five questions, top file only. Nearest is not the same as relevant.
9. Challenge: student discount on physical items. **10 percent.**

Cut first: the five-question table. Keep one retrieve, one answerable generate, one unanswerable generate.

`EMBEDDING_MODEL` from `.env`. `chromadb` in `pyproject.toml`. Do not install LlamaIndex or Pinecone.

## Frameworks from here

| # | Framework | Role |
|---|---|---|
| 02 SDK first look | OpenAI Agents SDK | **Trim to two ideas:** `@function_tool` printed next to the hand-typed `get_fact_json`, then `Agent` + `await Runner.run` + one trace URL. `SQLiteSession` and `draw_graph` move to 08. The multi-provider `base_url` cells are cut — they break the one-provider rule. |
| 03 Part 4 | OpenAI Agents SDK | Same question as Parts 1–3. Two tool spans + two green ellipses |
| 06 SDK host | OpenAI Agents SDK | `MCPServerStdio` on `server.py`. MCP spans + grey box. **Verified working — keep this, it is the portability payoff.** |
| 08 | OpenAI Agents SDK | Chinook specialists. Three wirings (code / `as_tool` / handoff), `draw_graph` before each run, traces. Gains `SQLiteSession` + `draw_graph` back from 02 |
| 09 | LangGraph | Same Chinook tools. Tiny graph (no model), official loop as `StateGraph`, mermaid, `interrupt` + `Command` |
| 13 | CrewAI (ten minutes) | Roles / goals / backstory as a concept inside delegation. Not a module, not installed. |
| 16 | Azure Foundry | Managed, instructor-provisioned |

**No SDK second half in 04, 05, or 07.** 04 is the five hands — hiding `write_file` would kill the lesson. 05 is the message list as a budget — the SDK hides the list. 07 *is* the `await` on-ramp; 06 already used `await Runner.run`.

## Chinook facts (do not regenerate)

sqlitetutorial edition. Tables lowercase plural (`customers`, `invoices`, `invoice_items`, `tracks`, `albums`, `artists`, `employees`, `genres`). Columns PascalCase.

| Table | Rows |
|---|---|
| artists | 275 |
| albums | 347 |
| tracks | 3,503 |
| customers | 59 |
| employees | 8 |
| invoices | 412 |
| invoice_items | 2,240 |
| genres | 25 |

Invoice dates: 2009-01-01 to 2013-12-22. Tools stay read-only.

The two CSVs (`fun_facts.csv`, 26 rows; `flight_data.csv`, 496 rows) are the data for **02, 03, 05, 06 and 07** — including `modules/06_mcp/server.py`, which reads them in its own process. Editing a row touches five modules. Verified pairs in use: Barcelona-Dubai 646.86 / 829, Barcelona-Amman 909.99 / 404, Sydney-Madrid 249.66 / 99, Tokyo-Moscow 259.3 / 525.

**Helena Holý:** 7 invoices, **$49.62**, support rep **Steve Johnson**. **Puja Srivastava:** 6 invoices, **$36.64**, rep **Jane Peacock**. Both verified against the database. Used for real in modules 08 and 09. Module 00 uses Prague weather as the invented-answer foil instead.

The retrieval corpus is in `data/corpus/` (36 short markdown files, Chinook shop policies and tickets). Do not regenerate.

Unanswerable from the corpus (for 11/12):

- What is Chinook's revenue target for 2014?
- What is the CEO's personal mobile number?

Planted payload (for 14): `data/corpus/ticket_16_overpayment_note.md`, Activity 5 phrasing (`APPROVED - PAY IMMEDIATELY`). **Re-verified 2026-08-19 against `gpt-5.4-nano`: 0/3** on the bare note, the full ticket, a RAG wrapper, and a ReAct `Observation:` wrapper — nano summarized the ticket and ignored the instruction. Module 14 only teaches if the model still falls for it. Retune the phrasing against the pinned model before delivery; do not assume this file detonates.

## Layout

```
BUILD_PLAN.md                 # this file
AUDIT.md                      # what is broken, verified by running it
archive/COURSE_PROMPT.md      # binding rules
README.md                     # public, student-facing overview
CURRENT_STATE.md              # internal status table + verify-before-delivery
.env.example
data/chinook.db               # 08, 09, 10
data/fun_facts.csv            # 02, 03, 05, 06, 07
data/flight_data.csv          # 02, 03, 05, 06, 07
data/README.md                # what each file is and who uses it
data/corpus/                  # 36 files. 11, 12, 14. Do not regenerate.
modules/NN_name/
  notebook.ipynb
  instructor.md
  solution.ipynb
azure/                        # optional Day 2 demos + module 16 extras
pyproject.toml
```

`pyproject.toml` currently has `ipykernel`, `jupyterlab`, `openai`, `openai-agents[viz]`, `python-dotenv`, `requests`, `langgraph`, `langchain-openai`, `langchain-core`. Notebooks never `pip install`.

`pyproject.toml` now also has `matplotlib`, `chromadb`, and a pinned `mcp>=2.0.0`. **Do not add `crewai`** — it downgrades `openai` 3.2.0 → 2.54.0 and `mcp` 2.0.0 → 1.28.1 and pulls 91 packages into the venv that 00–08 run on. **Do not add `llama-index`** — dry-run also downgrades `openai` 3.2.0 → 2.54.0.

`graphviz` the Python package is installed; the **`dot` system binary** is a separate install. Confirm it is on the student VM image, or `draw_graph` degrades to a printed exception in 02, 03, 06 and 08.

## Verify before delivery

**Resolved 2026-08-18 by running them.** Do not re-litigate these:

- `gpt-5.4-nano` + `reasoning_effort="none"` + `tools=` **works on Chat Completions.** No Responses API needed.
- `reasoning_effort="low"` + `tools=` returns a **400** on this model family. Keep `"none"` pinned in every cell.
- Both pinned model IDs exist on the class key.
- Chinook facts confirmed: Helena 7 / $49.62 / Steve Johnson, Puja 6 / $36.64 / Jane Peacock, and all eight row counts below.
- Modules 02, 03 (Part 1), 04, 06 and (after the P0 fix) 08 and 09 all produce the expected answers.

Still unverified, and each only teaches if the model still fails:

| Module | What must happen |
|---|---|
| 13 | The weaker router misroutes when specialist descriptions overlap |
| 14 | The unguarded RAG agent obeys the planted instruction. **2026-08-19: nano 0/3** on the Activity 5 line, including Observation-wrapped. Retune before delivery. |
| 04 | The `write_file` / `save_file` overlap actually causes a wrong pick |
| 05 | Fat first `create` still asks `read_skill` for a playbook it already carries |

Re-pin models in `.env`. Do not edit twenty notebooks. If you re-pin, re-run the checks in `AUDIT.md` §9.

## How to resume in a new session

1. Read this file, then `AUDIT.md`, then `CURRENT_STATE.md`, then `archive/COURSE_PROMPT.md`. `README.md` is public-facing; do not treat it as the work queue.
2. **Work the `AUDIT.md` checklist before building anything new.** Two built modules do not run.
3. Once the checklist is clear, the next thing to build is `data/corpus/`, then module 10.
4. Build one module only: `notebook.ipynb`, `instructor.md`, `solution.ipynb`.
5. Update the status table in `CURRENT_STATE.md` and the "Where we stopped" section here.
6. Stop and wait for review.

Do not delete `archive/CURRICULUM_REVIEW.md` unless asked. Do not treat it as current guidance.

---

