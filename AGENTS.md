# AGENTS.md

Working rules for any agent session in this repo. Read this, then `BUILD_PLAN.md` (the running order), then `AUDIT.md` (why that order), then `CURRENT_STATE.md` (where we stopped). `README.md` is the public, student-facing overview — do not put wave status or instructor cut-lists there. `archive/COURSE_PROMPT.md` is the original brief — historical, but the Rules section below is lifted from it and still binds.

## What this repo is

A two-day enterprise workshop, **AI Agents in Practice**. Modules 00–11 are written, 12–17 are not. Roughly 20 technical people — developers, data scientists, technical managers — on Linux VMs with VS Code and Jupyter. They know Python. They do not necessarily know agents. Half the room has to justify this work to a risk or compliance function.

Deliverables per module: `notebook.ipynb`, `instructor.md`, `solution.ipynb`.

## Read this before you touch anything

Three failure modes have already happened here. Do not repeat them.

**1. Verify by executing, never by reading.** The module table says "Built". Two of those modules do not run. A previous audit read all ten modules, graded them, and missed both bugs entirely because it never executed a cell. If you are asserting that something works, you ran it. If you did not run it, say so.

**2. Notebook JSON is fragile.** `modules/05_context_engineering/solution.ipynb` has been unopenable for an unknown length of time because of one missing comma in a hand-edit. Use `NotebookEdit`. After **every** edit to an `.ipynb`, run `json.load()` on it. Batch all changes to a given notebook into one pass rather than opening it repeatedly.

**3. Do not invent requirements.** A previous audit graded every module against a "zero em-dashes" rule that exists nowhere in this project, and made a 211-instance sweep the second item on its checklist. That is hours of risky JSON editing for no student benefit. `AUDIT.md` §5 lists work to actively skip. If you find yourself proposing a large mechanical change, check that the rule you are enforcing is written down somewhere.

## How the room runs — design for this

1. Instructor talks. Concept and slides.
2. Instructor drives the notebook. **Students watch. Nobody types.**
3. Students run the same notebook themselves, at their own pace.
4. Challenge at the end of the notebook, attempted alone.
5. Instructor debriefs with `solution.ipynb`.

**There is no code-along, ever.** Never write anything that assumes students are typing while the instructor talks.

**One mode, not several.** Do not label modules "demo" or "lab" or "code-along". They are all the same shape. Only the weight varies.

**The notebook is used twice** — driven at the front, then run by students. One artifact, not a demo version and a lab version.

**It must be complete on its own.** No cross-notebook imports. No dependency on having run another module. A student who watched rather than typed opens it later and gets the full explanation from the notebook itself.

**Write prose, not slide notes.** Assume the concept was introduced verbally; the notebook reinforces and deepens it. It should read like a good chapter. This is the strongest thing the existing modules have — match it.

Four stages, every notebook:

1. **Learn** — the problem and the mental model. ASCII or Mermaid diagram of the message flow or state transitions.
2. **Do** — build it incrementally, commenting the non-obvious decisions.
3. **Observe** — make the invisible visible: raw protocol traffic, state snapshots, tool payloads, token counts.
4. **Challenge** — unguided, with acceptance criteria and a verification cell that asserts. The solution ships separately; it is not in the student notebook.

## Rules

**Simple wins.** The most important rule. If code can be shorter and more obvious, make it shorter and more obvious. No abstraction layers, registries, factories, or configuration systems. Do not wrap a library that is already simple. Do not solve problems the SDK already solves. When you catch yourself hand-rolling something a dependency already does, stop and use the dependency.

**No black boxes.** Never hand a student a `.py` file and say "just run this." A `.py` file is only justified when something genuinely must run as its own process — an MCP server, an HTTP endpoint, a sandbox runner. Build and test the logic in the notebook first, then write the file, then show the terminal command that runs it.

**No shared helper package.** No cross-notebook imports. A small helper defined inside the notebook that uses it is fine and often better than repetition; a `utils.py` everything imports is not.

**One LLM provider: OpenAI.** No multi-provider abstraction. `MODEL_DEFAULT` (`gpt-5.4-nano`) by default, `MODEL_STRONG` (`gpt-5.4-mini`) only where a task genuinely needs it. Read model names from `.env`, never hard-code them in a cell.

**API specifics for this model family.** `max_completion_tokens`, not `max_tokens`. Do not pass `temperature`. Pin `reasoning_effort="none"` — verified: tool calling works with `"none"` on Chat Completions, and `"low"` returns a 400.

**Cloud: Azure only**, and only in module 16 plus optional instructor demos. Instructor-provisioned. No student needs an Azure credential and no core module may depend on one. AWS and Google get one orientation sentence, no lab.

**Open source and local by default.** Chroma, not a managed vector database. Local files over hosted services. Anything requiring a per-student signup is a failure mode in a room of twenty people.

**Tooling.** `uv` (`uv venv`, `uv sync`, `uv run jupyter lab`), one shared `.venv`, dependencies in `pyproject.toml`. **Notebooks never install packages.** Credentials live in `.env`, which is gitignored and never printed.

**Before adding a dependency, dry-run it.** One shared venv means a new package can break earlier modules. `uv pip install --dry-run <pkg>` and check for downgrades of `openai`, `mcp`, `langgraph`. This is why CrewAI was dropped.

**No emoji.** Anywhere. Not in notebooks, scripts, markdown, or output.

**Cost matters.** Twenty people over two days is a lot of API calls. Keep token budgets small and show students what things cost.

**Data.** Instructor-supplied. Do not regenerate any of these files. See `data/README.md`.

- `data/chinook.db` (sqlitetutorial edition) — modules 08, 09, 10. Verified: Helena Holý 7 invoices / $49.62 / Steve Johnson; Puja Srivastava 6 / $36.64 / Jane Peacock. Open it with `check_same_thread=False`.
- `data/fun_facts.csv` (26 rows) and `data/flight_data.csv` (496 rows) — modules **02, 03, 05, 06 and 07**, including `modules/06_mcp/server.py`. Changing a row ripples across five modules; check all of them first.
- `data/corpus/` — 36 short markdown files (Chinook shop policies and tickets). Modules 11, 12 and 14. Do not regenerate. Two unanswerable questions and the planted payload are listed in `BUILD_PLAN.md`.

**Flag model-dependent modules.** Some modules only teach if the model still fails — the security module needs the agent to fall for the injection, the routing module needs the weak model to misroute. Whenever you build one, say explicitly what must be re-verified before delivery, and put it in the table in `BUILD_PLAN.md`.

## The five design calls — settled, do not relitigate

1. **MCP in the middle, not at the end.** If MCP comes last, students write a server and never consume it, so the portability claim stays a claim.
2. **Context engineering gets its own module.** Context filling up and cost climbing per turn is what actually kills enterprise pilots, and it is rarely taught.
3. **Open tool calling by killing the misconception.** The model does not call the tool. It emits a name and a JSON blob and *your code* decides whether to act. `LLM -> TOOLS` vs `SOFTWARE -> TOOLS`. Security and sandboxing only make sense afterwards.
4. **Async before frameworks.** Every framework is async-first. Meeting `await` for the first time inside a framework teaches you to copy a line, not to use the framework.
5. **Compare frameworks by re-implementing one agent**, not with a feature table. Same task, same tools, climbing from no framework to a thin SDK to a graph framework. This audience makes adoption decisions; a comparison slide cannot support one.

## Reference material

`other_content/` holds a well-regarded six-week agent course and other past material. Mine it for patterns. Do not copy it wholesale: it front-loads a framework, leaves MCP until last, has emoji throughout, and several labs need SMTP, Pushover, HuggingFace Spaces, or paid search APIs that will not work in this room. Its dependency versions are also stale — check APIs against what is actually installed before reusing code.

`archive/` is historical. `archive/CURRICULUM_REVIEW.md` was overruled and is not current guidance.

## Working style

- **One module at a time.** Build it, stop, wait for review. Do not build ahead.
- **Scope is the deliverable.** Do not quietly widen a fix into a refactor.
- **Surface conflicts rather than engineering around them.** If a request collides with a rule here, say so.
- After finishing a module or a wave, update the status table in `CURRENT_STATE.md` and the "Where we stopped" section in `BUILD_PLAN.md`. Do not put that status in `README.md`.
