# Prompt: Build the "AI Agents in Practice" course

You are an expert AI engineer and curriculum designer. Build the hands-on materials for a two-day enterprise workshop called **AI Agents in Practice: Foundations, Frameworks, Protocols & Production**.

Work module by module. Build one, stop, let me review it, then move to the next. Do not build everything at once.

---

## Audience and environment

- 20 technical professionals from a large enterprise: developers, data scientists, technical managers.
- Each has a Linux VM running VS Code and Jupyter.
- They know Python. They do not necessarily know agents.
- Half the room will need to justify what they build to a risk or compliance function.

---

## What the course covers

**The architectural spine.** This is what the course is actually built on, and it is not negotiable:

Function calling → ReAct loop → context engineering → MCP → async and concurrency → agent frameworks → retrieval and agentic RAG → multi-agent delegation → security → evals and cost → cloud platforms → business value.

**Business-facing outcomes.** The room includes technical managers, so the course must also deliver:

- A customer support agent over a database — hands-on lab
- A BI / charting agent — hands-on
- Safe execution of model-generated code, and sandboxing
- Business process re-engineering with agents, as a working session

**Named tools — not requirements.** An early sales datasheet named LangChain, LangSmith, LlamaIndex, and Pinecone. A later revision of the same course already dropped LangSmith entirely and reduced Pinecone to one line of landscape commentary. So treat that list as background, and choose tools on their merits.

**Vector storage: use Chroma.** Open source, local, persistent, metadata filtering, no signup. Its API is the same mental model the managed products sell, so it transfers.

Do not build a lab on Pinecone. It is proprietary, needs a per-student signup, and teaches nothing Chroma does not. If a managed vector store is worth showing at all, the right one for this course is **Azure AI Search**, since Azure is already the one cloud here — adding Pinecone would mean a third vendor in a course deliberately narrowed to one cloud and one LLM provider.

Where a named tool conflicts with the rules below, the rules win. Surface the conflict rather than engineering around it.

---

## Structure

Roughly 15-18 modules. **Each module is one self-guided lab: a single Jupyter notebook.**

Sequence them so each module solves a problem the previous one left open. Build the agent loop by hand first, then show what frameworks add — the room cannot evaluate an abstraction they have never worked without.

**No fixed clock times, no rigid day-by-day schedule.** Give each module a relative weight and note what to cut first if the room runs behind. Modules should be reorderable and skippable.

---

## How I teach — design for this

Every module runs the same way:

1. **I talk.** Concept and slides.
2. **I show.** I run the code or demo it at the front. **Students watch. Nobody types.**
3. **Their turn.** They open the notebook and run it themselves, at their own pace. Same ground I just covered, but now it is their hands and their screen, and the notebook explains as it goes.
4. **Challenge.** At the end of the notebook, a task they attempt on their own.
5. **I debrief.** I walk through the challenge and show the solution.

**There is no code-along, ever.** Do not write anything that assumes students are typing while I talk. Code-along kills pace and half the room falls behind. The whole point is that watching and doing are separate: they watch me once, then do it themselves without pressure.

So there is **one mode, not several.** Do not label modules "demo" or "code-along" or "lab" — they are all the same shape. The only thing that varies is weight.

### What this means for the notebook

**The notebook is used twice**: I drive it at the front of the room, then students run the same file themselves. Do not build separate demo and lab versions — one artifact, used twice. Simpler for me, and what they run is exactly what they saw.

It must be **complete on its own**. A student who watched rather than typed opens it later and gets the full explanation from the notebook itself, with no cross-notebook imports and no dependency on having run any other module.

Write the prose accordingly: assume the concept has been introduced, and that the notebook is reinforcing and deepening it rather than teaching it cold. It should read like a good chapter, not like slide notes and not like a bare script.

Four stages in each notebook:

1. **Learn** — the problem being solved and the mental model. Include an ASCII or Mermaid diagram of the message flow or state transitions.
2. **Do** — build it incrementally, with comments explaining the non-obvious decisions.
3. **Observe** — inspection cells that make the invisible visible: raw protocol traffic, state snapshots, tool payloads, token counts.
4. **Challenge** — an unguided task with clear acceptance criteria and a verification cell that asserts.

The solution is not in the student notebook. It ships separately, because I present it during the debrief.

---

## Rules

**Simple wins.** This is the most important rule. If code can be shorter and more obvious, make it shorter and more obvious. Do not build abstraction layers, registries, factories, or configuration systems. Do not wrap a library that is already simple. Do not solve problems the SDK already solves.

**No black boxes.** Never hand a student a `.py` file and say "just run this." If a `.py` file is not necessary, do not create one. It is only justified when something genuinely must run as its own process — an MCP server, an HTTP endpoint, a sandbox runner. In that case, build and test the logic in the notebook first, then write the file out, then show the terminal command that runs it.

**Open source by default.** Prefer open, local, free tools. Chroma over a managed vector database. Local files over hosted services. Anything requiring a student signup is a failure mode in a room of twenty people — avoid it.

**One LLM provider: OpenAI.** No multi-provider abstraction. Use `gpt-5.4-nano` by default and `gpt-5.4-mini` only where a task genuinely needs more capability. Verify these model IDs exist before relying on them. Read model names from `.env`, never hard-code them in a cell.

**Cloud: Azure only.** If a module touches a cloud platform, it is Azure. Mention AWS and Google once on a slide for orientation and go no further. Anything driven through the Azure portal ships as a Markdown walkthrough; anything driven through an SDK ships as a notebook. Azure is instructor-provisioned — no student needs an Azure credential, and no core module may depend on it.

**Tooling.** `uv` for the environment (`uv venv`, `uv sync`, `uv run jupyter lab`), one shared `.venv`, dependencies in `pyproject.toml`. Notebooks never install packages. Credentials live in `.env`, which is gitignored and never printed.

**No emoji.** Anywhere. Not in notebooks, scripts, markdown, or output.

**Cost matters.** Twenty people over two days is a lot of API calls. Keep the token budget small and show students what things cost.

---

## Course data

**Use the Chinook SQLite database.** I have a copy. Do not generate a synthetic database — Chinook is a real, well-known sample schema (customers, invoices, invoice lines, tracks, albums, artists, genres, employees), it needs no build script, and students may already recognise it. One less thing to maintain and one less file to run on trust.

Work out what it can support and tell me. Some questions naturally need multi-table joins — revenue by artist has to cross artist, album, track, and invoice line — which is exactly the tool-chaining behaviour the database agent lab needs. Explore it first and pick real questions rather than inventing requirements it cannot meet.

Then tell me the expected answers, so I can check a student's output against yours.

**The retrieval modules need a small text corpus** — a few dozen short documents. Chinook has no free-text column, so this is separate. Build it, and keep it small and synthetic.

Two things the corpus must contain:

- Two questions that are deliberately **unanswerable** from it, so students can see whether their agent admits that or invents an answer.
- One document carrying a **prompt-injection payload** for the security module.

The corpus is the right home for the injection, not the database: indirect injection through retrieved content is the realistic attack, and it means the security module attacks the agent students built in the retrieval lab.

---

## Deliverables

Per module:

- **The notebook** — the self-guided lab, which is also what I drive at the front of the room.
- **Instructor notes** — short. What to emphasise while showing it, where to pause, and which cell is the moment that matters. A few bullets, not a script.
- **The solution** — a separate notebook or file, since I present it in the debrief rather than shipping it to students up front.

Overall:

- A `README.md` you write yourself: the module list, what each covers, and build status, so work can be resumed later. There is no existing scaffolding to inherit — the repo is empty apart from the reference material and the outlines. You choose the layout.
- A note wherever a module depends on the model behaving a particular way — the security module only teaches if the agent actually falls for the injection, and a routing demo only teaches if the weaker model actually misroutes. Tell me what to verify before delivery.

---

## Reference material

`other_content/` contains a well-regarded six-week agent course (`agents/`) and other past material. Mine it for patterns and working examples, but do not copy it wholesale: it front-loads a framework and leaves MCP until the end, it has emoji throughout, and several labs depend on SMTP, Pushover, HuggingFace Spaces, or paid search APIs that will not work in this room.

---

## Five design calls worth considering

You decide the module list, the numbering, and the layout. But these five are non-obvious, and I would argue for them. Disagree if you have a better reason.

**1. Teach MCP in the middle, not at the end.** Most agent courses save it for last as the advanced payoff. That is backwards for a two-day workshop: if MCP comes last, students write a server and then never consume it from anything, so the portability claim stays a claim. Put it before the framework modules and the same tools drive every framework — which means comparing frameworks isolates one variable instead of three.

**2. Give context engineering its own module.** The usual spine goes loop, tools, frameworks, retrieval, and steps straight past the thing that actually kills enterprise pilots: context filling up, cost climbing with every turn, the agent degrading the longer it works. Progressive disclosure and compaction are cheap to demonstrate and rarely taught.

**3. Open tool calling by killing the common misconception.** Nearly everyone believes the model calls the tool. It does not — it emits a name and a JSON blob, and *your code* decides whether to act on it. Two diagrams side by side, `LLM -> TOOLS` versus `SOFTWARE -> TOOLS`. Security, sandboxing, and the loop itself all only make sense afterwards: prompt injection is not the model doing something, it is your code doing something because the model asked.

**4. Cover async before the frameworks.** Every agent framework is async-first. A student meeting `await` for the first time inside a framework learns to copy a line, not to use the framework. It also pays off immediately: a single model response can carry several tool calls, and running them concurrently is a real, measurable win.

**5. Compare frameworks by re-implementing one agent, not with a feature table.** Same task, same tools, climbing from no framework to a thin SDK to a graph framework to a managed runtime. Let the room measure lines of code, tokens, and whether it can pause mid-run and resume. This audience has to make adoption decisions, and a comparison slide cannot support one.

---

## Start here

Propose the module list and the order, briefly, and say which of the five above you are keeping. Once I approve, build the first module and stop for review.
