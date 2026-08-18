# Slide brief — AI Agents in Practice (modules 00–03)

Give this file to an agent that will build the lesson slides. Do not invent later modules. Do not invent APIs, model names, or lab facts. If something is not in this brief or in the notebooks, leave it off the slide.

**Course:** AI Agents in Practice: Foundations, Frameworks, Protocols & Production  
**Audience:** ~20 enterprise people (developers, data scientists, technical managers). They know Python. They do not necessarily know agents. Half the room will have to justify the work to risk or compliance.  
**Room:** Instructor talks from these slides, then drives the notebook while nobody types, then students run the same notebook. There is **no code-along**. Slides teach the idea. The notebook is the proof.

**Source of truth (read these, do not contradict them):**

- `COURSE_PROMPT.md` — how the room runs
- `README.md` — module list and spine
- `modules/00_environment/` `notebook.ipynb` + `instructor.md`
- `modules/01_what_is_an_agent/` `notebook.ipynb` + `instructor.md`
- `modules/02_tool_calling/` `notebook.ipynb` + `instructor.md`
- `modules/03_react_loop/` `notebook.ipynb` + `instructor.md`

**Deliverable.** One slide deck (or four short decks that share a look), one section per module below. Widescreen 16:9. Speaker notes on every slide.

---

## Design rules for the slide agent

- **No emoji.** Anywhere.
- **No walls of code.** A slide may show 4–8 lines if they are the point. Full loops stay in the notebook.
- **One idea per slide.** If you need two ideas, make two slides.
- **Diagrams over bullets.** Recreate the ASCII diagrams from the notebooks as clean visuals. Keep the same names (`messages`, `message`, `tool_calls`, Thought / Action / Observation).
- **Do not look like a vendor pitch.** No logo tours. Azure is Day 2. AWS and Google get one orientation sentence on the course-open slide, then disappear.
- **Do not say “the model calls the tool.”** That is the misconception module 02 kills.
- **Do not call the official `tool_calls` loop “ReAct.”** ReAct is think-out-loud plus action. The official loop is silent. Module 03 is explicit about this.
- **Do not invent Chinook queries, prices, or facts.** Use only the numbers in this brief.
- **Dark or light is fine.** High contrast. Readable from the back of a training room. Large type. Few words.
- **Title slide for the course, then a spine slide, then module sections.** Each module section starts with a divider: number, title, one sentence.
- **Footer:** module number and short title, so the instructor can jump.
- **Speaker notes** say what to say and when to switch to the notebook. Mark those moments as `NOTEBOOK`.

**How slides and notebook share the hour**

| Phase | Who | Slides? |
|---|---|---|
| I talk | Instructor | Yes. This deck. |
| I show | Instructor drives the notebook. Room watches. | No new slides mid-demo except a parked diagram if they need to look up. |
| Their turn | Students run the same notebook | Deck stays on a “your turn” slide. |
| Challenge | Students | Challenge slide (the table or the prompt only). |
| Debrief | Instructor | Solution talking points, not a dump of `solution.ipynb`. |

---

## Deck 0 — Open the course (5–7 slides)

### 0.1 Title
**On slide:** AI Agents in Practice. Foundations, Frameworks, Protocols & Production. Two-day enterprise workshop.

**Notes:** Welcome. VMs, VS Code, Jupyter. Shared OpenAI key. No student Azure credential on the core path.

### 0.2 Who is in the room
**On slide:** Developers. Data scientists. Technical managers. Half of you will have to explain this to risk.

**Notes:** Managers are not an afterthought. Module 01 is for them as much as for the people who will type.

### 0.3 How every module runs
**On slide:** five steps, one shape.

1. I talk (these slides).
2. I show. You watch. Nobody types.
3. Your turn. Same notebook.
4. Challenge.
5. Debrief.

**Notes:** There is no code-along. Watching and doing are separate on purpose.

### 0.4 The spine
**On slide:**

```
00  one API call
01  what an agent is — and when it should not be
02  the model does not call the tool
03  think out loud, then act; then the silent loop
04  coding agent, then break it
05  the list gets expensive
06  MCP
07  Chinook support agent
08  concurrent tools
09  the same agent, three frameworks
10  charts and a sandbox
11–12  retrieval, then agentic RAG
13  delegation
14  security
15  evals and cost
16  Azure
17  process re-engineering
```

Highlight 00–03 as “today / this block.” Grey the rest.

**Notes:** Each module exists because the previous one left a problem open. After 03 they have an agent. After 07 the support agent. After 09 is the cleanest day-one close.

### 0.5 One business, deepening
**On slide:** Chinook is a digital music shop. Later labs stay in that shop. Today we also use flights, city facts, and (in 03) live weather.

**Notes:** Do not open `chinook.db` in 00–03. Helena’s numbers are real and will come back.

### 0.6 Rules of the room
**On slide:**

- One LLM provider: OpenAI. Names come from `.env`.
- Key never on the projector.
- Open source and local by default.
- Cloud, when we touch it, is Azure, instructor-provisioned.
- Cost is part of the design.

**Notes:** `MODEL_DEFAULT` is `gpt-5.4-nano`. Re-pin in `.env`, never in twenty notebooks.

---

## Module 00 — The OpenAI API, seen once clearly

**Notebook:** `modules/00_environment/notebook.ipynb`  
**Weight:** S  
**Job of the slides:** The response is an object. No memory. No hands. Tokens are money. Then `NOTEBOOK`.

### 00.1 Divider
The API, once clearly.

### 00.2 What a call is
**On slide:** You send a list of messages. The service returns one object. That is the whole Chat Completions API.

**Visual:** `user` / `system` / `assistant` as three labelled boxes feeding `create()`, returning `ChatCompletion`.

### 00.3 Three roles
**On slide:**

- `system` — standing instruction. Not stored. Send it again if you want it.
- `user` — this turn.
- `assistant` — what it said last time. You send that back once you have a loop.

**Notes:** The riddle’s last line will come from `system`, not from `user`. Ask them that after the first cell.

### 00.4 The object
**On slide:** `id`, `model`, `choices[0].message.content`, `finish_reason`, `usage`. Plant: `tool_calls` will appear on this same `message` in module 02.

**Notes:** Do not dump raw JSON on a slide. Names only.

### 00.5 Two holes
**On slide:** This call has no memory. This call has no tools.

**Visual:** two gaps. (1) New `create()`, new `messages` — the riddle is gone. (2) “Weather in Prague right now” — no network, no clock.

**Notes:** `NOTEBOOK`. After the forget cell: the list *is* the memory. After Prague: whatever number they got was not fetched. Flight status would fail the same way. True weather arrives in module 03.

### 00.6 Streaming, one idea at a time
**On slide:** three steps only.

1. Print the words.
2. Save them into a string.
3. Ask for `usage` (`include_usage`).

**Notes:** A bare stream throws the bill away. `NOTEBOOK` for the three cells. Do not put the full stream loop on a slide.

### 00.7 Cost is a multiplier
**On slide:** one call is a fraction of a cent. 1,000 of these. 100,000 of these. An app on every page load, or a company loop that retries.

**Notes:** Landing slide. Reasoning tokens are billed as output even when they never appear. `reasoning_effort="none"` on a two-line riddle.

### 00.8 Your turn
**On slide:** Open `modules/00_environment/notebook.ipynb`. Challenge: stream a one-sentence joke about invoices. Bind `text`, `prompt_tokens`, `cost`.

**Notes:** Stay on this slide while they work. Debrief: print, append, keep `usage`.

---

## Module 01 — What an agent is, and when it should not be one

**Notebook:** `modules/01_what_is_an_agent/notebook.ipynb`  
**Weight:** M  
**Job of the slides:** One test. Three shapes. How far is a separate question. Then `NOTEBOOK`. Then the group table.

### 01.1 Divider
Who decides the next step?

### 01.2 The sentence
**On slide:** **Who decides the next step — you, or the model?**

**Notes:** This is the vocabulary the rest of the course reuses. Risk will hear it again in module 17.

### 01.3 Three shapes
**On slide:** recreate the notebook diagram.

```
chatbot     user --> your code --> LLM --> text
            No tools. No loop.

workflow    user --> your code --> step 1 --> step 2 --> done
            You wrote the steps. Maybe no model at all.

agent       user --> your code --> LLM --chooses--> your code runs a tool
                              ^                         |
                              +------ observation ------+
            Until the model is done, or you hit a cap.
```

**On slide, one line each:**

- chatbot — talk only.
- workflow — you wrote the steps.
- agent — the model chooses the next step; your code runs the tools.

**Notes:** RPA is a workflow that drives a UI. Same test: you wrote the steps.

### 01.4 Anatomy
**On slide:** model, instructions, tools, memory (the message list), a loop you wrote, a cap.

**Notes:** The model never runs the tool. Module 00 already showed that.

### 01.5 How far (separate question)
**On slide:**

| Word | Meaning |
|---|---|
| suggest | It recommends. A human does the thing. |
| draft | It writes the action and waits. A human approves or edits. |
| act | It does the thing. No one is in the loop. If it acts, log it. |

**Notes:** Shape is what it is. How far is how much rope. A chatbot is usually `suggest`. A nightly export is usually `act`. An agent that can move money should not be `act`. These words come back in module 17.

### 01.6 When an agent is the wrong default
**On slide:** three bullets only.

1. The steps are already known. A script is cheaper and testable.
2. A wrong action is expensive or hard to undo. Do not put that on `act`.
3. The facts were never written down. A tool cannot fetch what nobody stored.

### 01.7 What you will see in the notebook
**On slide:** a two-customer toy shop (Helena, Puja). Real Chinook numbers, no database yet.

- Workflow: count, then rep. Zero model calls. **This is the hero.**
- Chatbot: same question, invents.
- Scripted `plan = ["COUNT helena", "REP helena", "DONE"]` — ordinary Python.
- Live loop: the model emits the next line. Cap of 4.

**Notes:** `NOTEBOOK`. Pause after the workflow: “Is this an agent?” Wait for no. Pause after the scripted `for`: that is the whole trick. Helena: **7 invoices, Steve Johnson**. Puja: **6 invoices, Jane Peacock**. Do not invent other numbers.

### 01.8 Challenge — group table
**On slide:** the eight jobs, empty columns. Do not fill the answers.

| # | Job | Shape | Who decides? | How far? |
|---|-----|-------|--------------|----------|
| 1 | Same overdue reminder to every 30-day account | | | |
| 2 | Visitor asks what jazz fusion is | | | |
| 3 | Messy email: invoice, address, then a recommendation | | | |
| 4 | Helena: count, then rep, always that order | | | |
| 5 | Nightly invoice CSV to a file share | | | |
| 6 | Why is Q3 revenue down? | | | |
| 7 | Auto-refund up to $5,000 from email, no one in the loop | | | |
| 8 | Route email to billing, shipping, or product | | | |

**Notes:** Twos and threes. Five to seven minutes. They edit the table in the notebook. If behind: rows 1, 3, 7 only. **Do not put the answer key on this slide.**

### 01.9 Debrief (instructor only — after they work)
**On slide:** still no full key if you can help it. Or reveal row by row.

**Notes (not on the student-facing slide if you can hide it):**

- 1, 4, 5 → workflow, `act`
- 2 → chatbot
- 3, 6 → agent; keep 6 on `suggest`
- 7 → looks like an agent, must not `act`. `draft` or a rules workflow. This is the risk sentence.
- 8 → let the room split. Classifier plus queues is a workflow. Leftovers are an agent.

---

## Module 02 — The model does not call the tool

**Notebook:** `modules/02_tool_calling/notebook.ipynb`  
**Weight:** M  
**Job of the slides:** Kill the misconception. Then `NOTEBOOK`.

### 02.1 Divider
The model does not call the tool.

### 02.2 The misconception
**On slide:** two diagrams, side by side, same as the notebook.

```
assumed     user --> software --> LLM --> tools

actual      user --> software --> LLM
                              |
                              +------> tools   (your code decides)
```

**Notes:** Security, sandboxing, and the loop only make sense after this. Prompt injection is not the model doing something. It is your code doing something because the model asked.

### 02.3 Same object, new field
**On slide:** module 00’s `message` had `role` and `content`. Today it can have `tool_calls`. `content` is often empty. `finish_reason` is `tool_calls` instead of `stop`.

**Visual:** `tool_calls[0]`: `name`, `arguments` (a **string**), `id`.

### 02.4 Three Python names
**On slide:**

- `messages` — the list every `create` sends
- `message` — this one assistant reply (the ask)
- `result` — what *our* function returned (not on the list until we append it)

### 02.5 Schema is a description, not a hook
**On slide:** a named dict, then a list. Recreate this exactly:

```
get_fact_json = { name, description, parameters }
get_flight_json = { ... }

tools = [
    {"type": "function", "function": get_fact_json},
    {"type": "function", "function": get_flight_json},
]
```

**Notes:** Nothing runs because the dict exists. We call `get_fact("Amsterdam")` ourselves first, with no model.

### 02.6 What you will see
**On slide:**

1. Amsterdam, **no** `tools=` → `finish_reason=stop`, guessed sentence.
2. Same question **with** `tools=` → stop. Look. Do not run yet.
3. Parse `arguments`, run `get_fact`, send a `tool` message back.
4. If we had sent a lie, the model would have repeated it.
5. Two tools. One question that needs both (Sydney → Madrid **and** a Madrid fact). Inner `for` if two `tool_calls` in one reply. Cap of 3 if it asks one at a time.

**Notes:** `NOTEBOOK`. The cell that matters is (2). Amsterdam fact: more bicycles than people. Sydney–Madrid: **249.66 dollars, 99 minutes** (one row). Madrid: oldest restaurant, Sobrino de Botín. Concurrent is module 08. The named loop is module 03.

### 02.7 You can refuse
**On slide:** Nothing forces you to run `get_flight` just because the model asked.

**Notes:** Plant for module 14.

### 02.8 Your turn
**On slide:** Give me a fun fact about Istanbul. One round trip. Bind `asked_name`, `fact`, `final_text`.

**Notes:** Do not put the Istanbul fact on the slide. Debrief only: *Istanbul is the only city in the world that spans two continents: Europe and Asia.*

---

## Module 03 — The ReAct loop

**Notebook:** `modules/03_react_loop/notebook.ipynb`  
**Weight:** L  
**Job of the slides:** ReAct is think out loud plus act. A class is a wrap of that loop. The official loop is silent and is what they will ship. Then `NOTEBOOK`.

### 03.1 Divider
Think out loud, then act.

### 03.2 What ReAct is
**On slide:** Reason + Act. Not “another way to call tools.”

1. Thought — written out loud
2. Action — one tool, fixed text
3. PAUSE — it waits on purpose
4. Observation — your code writes this; the model cannot see the tool otherwise

**Visual:** the Thought → Action → Observation cycle from the notebook.

**Notes:** In module 02 the official loop was silent. The reasoning happened. Only `tool_calls` surfaced. ReAct makes the thought readable. That is the product.

### 03.3 Two things, not alternatives
**On slide:**

| | ReAct | Official loop |
|---|---|---|
| How it asks for a tool | A text line: `Action:` | `finish_reason == tool_calls` |
| How you detect it | Walk the lines | A field on the response |
| Reasoning visible? | Yes, `Thought:` | No, inside the model |
| Breaks if the model rambles? | Yes | No |
| Works on any chat model? | Yes | Only with a tool-calling API |

**Notes:** Most frameworks use `tool_calls` and still borrow ReAct’s idea (think before you act) in the prompt. Do not label the official column “ReAct.”

### 03.4 Thoughts are tokens
**On slide:** Every `Thought:` line is billed as output. A chatty plan is a bill. Same `usage` object as module 00.

### 03.5 Part 1 — ReAct in the open
**On slide:** The question is sequential on purpose.

> What is a fun fact about the city I land in if I fly from Barcelona to Amman?

The second tool needs the first result. A parallel burst cannot know the city yet.

**Notes:** `NOTEBOOK` for Part 1. Cover the true answers until after they run: **909.99 dollars, 404 minutes**, then *Amman, the capital of Jordan, is built on seven hills, each known as a Jabal.* The cell that matters is the **second thought**, after the first observation. If it names Amman, ReAct worked.

Build order to mention (do not paste the loop on a slide): prompt → one raw reply → parse by walking lines (no regex) → run → append observation → second thought → only then the `for`.

### 03.6 Part 2 — same ReAct, wrapped
**On slide:**

```
agent = ReactAgent(system, run_action)
agent.ask("Is Prague warmer than Amsterdam right now, and by how many degrees?")
```

**On slide, under that:** `ask` is the `for` you already wrote. `messages` moved onto `self`. That is what a framework is selling. Module 09 gives you three of those.

**Notes:** `NOTEBOOK`. Live Open-Meteo. No API key. This is the Prague hole from module 00, closed. If the VM cannot reach Open-Meteo, skip Part 2. After `ask`, read thought tokens and the dollar line out loud.

Tools on a slide, names only: `get_weather(city)`, `subtract(a, b)`. No `eval`.

### 03.7 Part 3 — the official loop
**On slide:** This is not a second ReAct. The API takes `Action`. The thought goes quiet. You keep the loop. You lose the narration.

**Notes:** `NOTEBOOK`. Same Amman question. Pause after the first official `create`, before tools run: “Do you miss the Thought?” This loop is the file modules 04 and 09 wrap.

### 03.8 Observe
**On slide:** How many tool results landed on `messages`?

- 0 — guessed. Chatbot.
- 1 — flew, then invented the fact.
- 2 — the observation did its job.

### 03.9 Your turn
**On slide:** Official loop only.

> What is a fun fact about the city I land in if I fly from Tokyo to Moscow?

Bind `n_lookups` and `final_text`.

**Notes:** Do not put 259.3 / 525 or the metro palaces on this slide. Debrief only: Tokyo → Moscow **259.3 dollars, 525 minutes**; *Moscow's metro stations are often referred to as 'underground palaces'.* `n_lookups` of 2 is the win.

### 03.10 Three things that go wrong
**On slide:**

1. No turn cap.
2. Dropping `messages`.
3. Raising when a tool fails — send the error back as text.

---

## Facts the slide agent may print (and no others)

| Item | Value |
|---|---|
| Helena Holý | 7 invoices, Steve Johnson |
| Puja Srivastava | 6 invoices, Jane Peacock |
| Amsterdam fact | more bicycles than people |
| Istanbul fact | only city that spans two continents |
| Madrid fact | oldest restaurant, Sobrino de Botín |
| Sydney → Madrid | 249.66 dollars, 99 minutes (one row) |
| Barcelona → Amman | 909.99 dollars, 404 minutes |
| Amman fact | seven hills, each a Jabal |
| Tokyo → Moscow | 259.3 dollars, 525 minutes |
| Moscow fact | metro stations as underground palaces |
| Default model | `gpt-5.4-nano` from `.env` |
| Vector store (later) | Chroma, not Pinecone |
| Database (later) | `data/chinook.db` |

Do not put challenge answers on the student-facing challenge slides. They belong in speaker notes or a hidden debrief slide.

---

## What not to build

- Slides for modules 04–17. The spine slide may list them. No content.
- A “LangChain vs Crew vs AutoGen” comparison. That is module 09, not yet written.
- Pinecone, LangSmith, multi-provider diagrams, Ollama.
- Code-along cue cards (“now you type…”).
- Separate demo vs lab decks.
- Emoji, stock robot art, or a generated agent mascot.
- Full `ReactAgent` class listing. The two-line `agent =` / `agent.ask` is enough.

---

## After the slides exist

Name the file `slides/00-03.pptx` (or four files under `slides/`). Keep this outline next to them. When module 04 is approved, extend this brief — do not let the slide agent free-write the rest of the course.
