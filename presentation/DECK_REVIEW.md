# Review: `ai_agents_in_practice.pptx`

Two-day workshop, 17 students, mixed technical / non-technical.
Reviewed as an AI engineering practitioner and as a presentation designer.
Original: **82 slides**. Rebuilt: **111 slides**, delivered as `ai_agents_in_practice_v3.pptx`.

---

## 1. The headline finding

The content is genuinely good. The sequencing is better than most commercial agent courses — every module is motivated by a problem the previous one left open, and that is a hard thing to get right. Two things were holding it back:

**A factual liability on slide 5.** The "88% of enterprise agent pilots never reach production" figure has no traceable primary source. Searching it returns 78%, 86%, 88%, 89% and 95% all asserted with equal confidence across content-marketing blogs. In a room where half the audience has to justify this work to a risk function, an unsourced number on the opening slide is the one thing an attendee will fact-check on their phone — and they will find it contradicted.

**A systemic layout fault.** Content was anchored to the top of every slide with nothing below it. Measured across all 82 slides: on the median slide, content stopped at **6.2 inches of an 11.25-inch canvas**. 73 of 82 slides left the bottom third or more completely empty. That is not minimalism — minimalism is deliberate negative space around a focal point. This read as a deck where the bottom half had not been filled in yet.

There were also **zero images, icons, or illustrations in the entire file** (the `.pptx` had no `ppt/media/` folder at all), and only three actual visuals across 82 slides: two bar charts and one circle diagram.

---

## 2. Content validity

### 2.1 Must fix — the 88% statistic
Replaced with Gartner's published forecast, which is citable and stronger material:

- **Over 40%** of agentic AI projects will be cancelled by end of 2027 — attributed to escalating costs, unclear business value, and inadequate risk controls
- Only **~130** of thousands of self-described agentic AI vendors are genuine; the rest is **"agent washing"** — rebranded assistants, chatbots and RPA
- **15%** of day-to-day work decisions autonomous by 2028, up from ~0% in 2024

"Agent washing" is a gift for this audience — it gives the business half of the room a phrase to use in a vendor meeting, and it sets up the "there is no settled definition" slide perfectly.

### 2.2 Module numbering does not match your repo
The deck numbered sections 01–16. `README.md` defines modules 00–17. They drift apart from section 07 onward:

| Deck said | README says |
|---|---|
| *(nothing)* | 00 — OpenAI API, response object, streaming, cost |
| 07 Async | 08 Async |
| 08 Framework ladder | 09 Three frameworks |
| 12 Security | 14 Security |
| 15 Platform landscape | 16 Azure |
| 16 Process re-engineering | 17 Process re-engineering |

Students open `modules/14_security/notebook.ipynb` while the slide footer says "12 · SECURITY". That is a live confusion cost every time you switch between deck and notebook. **Every section is renumbered to match your README folder names.**

### 2.3 MCP was the weakest technical section — and out of date
You flagged JSON-RPC yourself. It went further than that. The original had three MCP slides; the rebuild has eight, because several things in the original are now wrong or missing as of the current spec:

| Issue | Status |
|---|---|
| **JSON-RPC 2.0 never mentioned** | Added, with a real `tools/call` message on screen. This is what makes MCP stop feeling like magic. |
| **Transports vague** ("stdio for local, HTTP for remote") | Named properly: **stdio** and **Streamable HTTP**. HTTP+SSE has been deprecated since the 2025-03-26 revision. |
| **Statelessness change missing** | The 2026-07-28 revision removed protocol-level sessions and the standing GET stream. A remote MCP server that needed sticky sessions and a shared session store can now run behind a plain round-robin load balancer. This is the single most important MCP fact for a platform team and it was absent. |
| **No authorisation slide at all** | Added. Remote servers authorise as OAuth 2.0 / OpenID Connect resource servers. This is the *first* question your security people will ask and the deck had no answer. |
| **Elicitation missing** | Added — the server can pause mid-task and ask the client for input. This is human-in-the-loop as a protocol feature. |
| **Sampling / logging** | Worth knowing: both are now deprecated in MCP, in favour of calling the model provider directly and using OpenTelemetry. If you had taught "MCP has sampling," that would have aged badly. |
| **A2A governance thin** | Now named as a **Linux Foundation** project (donated by Google), 150+ participating organisations in its first year. Procurement cares that it is not one vendor's protocol. |

### 2.4 Content that was missing
Seven gaps, all now written:

1. **Module 00 entirely** — the deck had no coverage of the API call, the response object, roles, or tokens, despite `README.md` marking module 00 as built. Five slides added. The `tool_calls` field is planted on the module 00 response-object diagram as a dashed box, so module 02 becomes a callback rather than a new idea.
2. **Structured outputs / JSON Schema** — absent. This matters because a large fraction of what people bring you as "agent" use cases are actually structured extraction, needing no loop and no tools. Naming that early saves them money.
3. **Model selection for agent work** — absent. First question a real team hits. Tool-calling reliability compounds: 95% correct per turn is ~74% over six turns.
4. **Evaluation methodology** — you listed five things worth measuring but never *how*. Added: golden set, trajectory vs outcome grading, LLM-as-judge (with the calibration caveat — an uncalibrated judge is a confident random number generator), and running it in CI.
5. **Observability** — mentioned but not taught. Added a slide on OpenTelemetry GenAI semantic conventions, the trace/span shape, and the PII catch (traces contain prompts, so decide redaction before you turn tracing on).
6. **Human-in-the-loop mechanics** — you had an autonomy spectrum but never said how a gate is actually built: where it sits, what the reviewer must see, why it needs resumable runs, and approval fatigue.
7. **Framework landscape + the "when to say no" decision** — see below.

### 2.5 New: framework landscape and the no-framework decision
Drawn from the reference material in `other_content/agents`. Four new slides:

- **The names placed on the tier ladder** — Tier 1 (OpenAI Agents SDK, Pydantic AI, Strands), Tier 2 (LangGraph, Mastra), Tier 3 (CrewAI, AutoGen, Agno, Google ADK, Microsoft Agent Framework). Nine names, three ideas. It converts "which framework should we use" from an unanswerable question into a decision about how much control you want to keep.
- **No framework vs a framework — the honest trade**, with what you get and what it costs on both sides, and a "reach for it when" line each.
- **Five questions that choose the tier for you** — run length, team size, tool count, who audits it, cloud portability.
- **"Do you need an agent at all?"** — a five-question decision flow in module 17 where four of the five branches end in *stop*. Q2 ("is the context written down anywhere a tool could read it?") is where most real proposals should die, and it dies for reasons that have nothing to do with AI.

### 2.7 New: the orientation block, moved to the front
Five slides now sit between the opening and Module 00, before any technical content. The reasoning: the deck previously went straight from "most projects get cancelled" into API mechanics. That is an honest opening followed by a cold one — nothing in the first twenty minutes told the room how big or how varied this space actually is.

1. **The agentic AI landscape, in one picture** — eight categories on a dark full-bleed slide (coding, support, research, data/BI, back office, ops/SRE/security, browser & computer use, physical), each with what it does, its tool set, and a maturity read (in production / emerging / early). The teaching line at the bottom is the real payload: *same loop underneath all eight; what changes is the tools it can reach.* That makes everything in the next two days generalise instead of feeling like a coding-agent course.
2. **Coding agents got there first, and that is not a coincidence** — your point, made into a diagnostic. Software had five properties almost no other domain has: a built-in oracle (tests), cheap total undo (version control), a text-native domain, a feedback loop in seconds, and unusually tolerant users. The corollary is the useful bit: *score your own domain out of five; every property you are missing is real work you will have to build.* This is the antidote to "my developers use Claude Code, why can't finance have the same thing," and it foreshadows both module 01's wrong-default reasons and module 17's decision flow.
3. **Three ways to build one, and they fail differently** — no-code / low-code / pro-code, with who builds it, time to first agent, what you control, what it is good for, where it breaks, and the honest risk. The no-code risk is named plainly: it is where ungoverned agents appear, because they never pass through your software delivery process. But it is not sneered at — for a small departmental process with a tiny blast radius it is the right call, and some of your room is already using it.
4. **Two axes** — moved up from module 01. It is a market-orientation slide, not a definition slide, and it was competing with module 01's actual job. Paired with the slide above it now reads cleanly: that one is *how you build*, this one is *who you are*.
5. **Unattended is not the same as agentic** — the RPA aside. Side-by-side on six dimensions: who decides the next step, input it can handle, same input twice, what breaks it, cost per run, auditability. Two things it lands: RPA is a *workflow* by module 01's own test (you wrote the steps), and unattended operation is autonomy, not agency — which is exactly why it feels agentic. It closes on the honest production answer rather than a winner: judgment from the agent, execution from the deterministic bot. Every enterprise room has someone who owns an RPA estate, and this question gets asked whether or not you plan for it.

Module 01 loses the quadrant slide and is tighter for it — it now runs definition → three shapes → anatomy → autonomy → wrong defaults → exercise without a market-map detour in the middle.

### 2.9 Two file-level defects found and fixed (v3)

**PowerPoint was demanding a repair on open.** You spotted this before I did — the `- Repaired` copy in your folder was the tell. Cause: pptxgenjs emits chart XML that passes the OOXML schema, opens in python-pptx and renders in LibreOffice, but that PowerPoint refuses. Both charts (context growth, sequential-vs-concurrent) are now **drawn as native shapes** instead of embedded chart parts. The deck contains no chart parts and no embedded Excel workbooks at all, so the failure mode is gone rather than worked around. Side benefit: the charts now match the design system exactly.

**The file was 8.8 MB for no reason.** pptxgenjs writes a fresh copy of identical image bytes on every `addImage` call — 361 media parts for 52 distinct images, with the dark background PNG duplicated once per dark slide. A post-processing pass now deduplicates by content hash and rewrites the relationships. **8.76 MB → 1.34 MB**, same pixels. It also strips build-path leakage from image alt-text (37 instances of an internal filesystem path were embedded in the file's metadata).

### 2.10 Your two slide edits are preserved

You replaced the artwork on slide 18 (chatbot / workflow / agent) and slide 25 (assumed vs actual). Both are now baked into the generator, so they survive every future rebuild rather than being overwritten:

- **Slide 18** — your three illustrations, with two fixes: the "Who decides?" block was colliding with the artwork, so it now sits below a uniform image band; and the agent illustration's white background is composited onto the hero card colour so it no longer shows as a white rectangle on the tinted card.
- **Slide 25** — your rendered diagram is better than my drawn version, particularly the asks/requests and requests/result labelling on the ACTUAL panel. Kept verbatim.

One caveat: both are raster images. Slide 25's artwork is ~103 DPI at its placed size, which will look slightly soft on a large projector. Fine for a training room; if you ever want it crisp, the same diagram as vector shapes would fix it.

### 2.11 What I took from the six-week course decks

I mined all 30 decks (`Agentic Week 1`–`6`). Most of it is framework-tour material your deck deliberately doesn't do, but four things were genuinely worth taking, plus several smaller corrections:

**New slides:**

1. **Five workflow patterns** (module 09) — prompt chaining, routing, parallelisation, orchestrator–worker, evaluator–optimiser, each with a small diagram. This closed a real gap: your deck asserted "workflow" as one of the three shapes from module 01 onward but never showed what one actually looks like. These are Anthropic's published patterns and they are the standard vocabulary. The teaching line is that patterns 1–3 have a fixed path, and only 4–5 decide anything at run time — so even the dynamic ones are not yet agents.
2. **"The trap your team will fall into first"** (module 13) — the anthropomorphising red flag, drawn as the org chart people actually whiteboard (Trading Manager → Market Research / Trader / Risk Manager), with the discipline that replaces it. This now sits *before* the five topologies, so the room gets the warning before the vocabulary. Best single find in the corpus for an enterprise audience.
3. **"Every vendor sells one of three things"** (module 16) — Products / Builders / Runtimes, sorted by the verb (use / build / execute) rather than by logo, plus the observation that almost every vendor has the same three-tier business model underneath: open-source framework → free platform → paid platform. That second point is what procurement will write down and almost nobody's deck says it.
4. **A third failure mode in module 04** — the coding agent writes against the API it was trained on. Three separate frameworks in those decks warn about their own rename churn; aggregated, that becomes a real and teachable gotcha.

**Smaller additions to existing slides:** you never write the MCP client (your framework does); if a tool is only ever used by your own agent, a plain function is simpler than an MCP server — MCP earns its keep when the tool crosses a boundary; the agent-as-a-tool vs hand-off distinction (caller keeps control vs transfers it); tracing is usually a few lines of config, not a project; and the unpredictable-path / output / cost triple as the bridge from module 14 to 15. The module 17 workshop gained a paired warm-up: state the agent you want, and your partner asks "and what business problem is that solving?" — twice.

**Deliberately not taken:** pinned model version strings and framework versions (stale within a quarter), vendor benchmark claims repeated as fact, and one unsourced lineage claim about which framework inspired another. Also worth knowing — those 30 decks have essentially nothing on retrieval, agentic RAG, security, or process re-engineering. Your deck is materially stronger than that course in exactly those four places.

### 2.13 Realigned to `BUILD_PLAN.md` (which supersedes `README.md`)

The build plan is newer than the README I originally worked from, and it moves three modules. This matters more than it sounds — it is the same footer-vs-folder mismatch I flagged in §2.2, and it had crept back in:

| | README (what I built to) | BUILD_PLAN (authoritative) |
|---|---|---|
| 07 | Chinook support agent | **Async and concurrent tool calls** |
| 08 | Async | **OpenAI Agents SDK** — Chinook desk, three orchestrations |
| 09 | "The same agent, three ways" | **LangGraph** |

Sections 07–09 are rebuilt to match, which also honours two of your locked design calls: *async before frameworks*, and *Chinook is built inside a framework, not hand-rolled as its own module*. The standalone "support agent" slide is now module 08's Chinook desk rather than a module of its own.

**07 · Async** — the three async slides, unchanged, renumbered. Speaker note now says why async comes first: module 08 opens with `await Runner.run`.

**08 · Agents SDK** — divider, "no framework or a framework", the five-tier ladder, the Chinook desk (now says *read-only and no free SQL* — the model never gets a database handle), and a new slide: **"Two specialists, three ways to wire them"**. Code orchestrates / agents-as-tools / hand-offs, each with a mini wiring diagram. The dashed return arrows are the whole point — they exist for the first two and not for the hand-off. That is where the agent-as-a-tool vs hand-off control distinction now lives (it was a footnote in module 13 before; it belongs here, attached to the lab that demonstrates it).

**09 · LangGraph** — divider, five workflow patterns, plus two new slides:
- **"Three words, and the loop becomes a picture"** — State / Node / Edge. The line worth saying out loud is that the routing condition is *ordinary code reading a field*, not another model call. People assume every decision in an "agentic graph" is an LLM call, and that assumption is why they think graphs are unpredictable everywhere.
- **"The real reason to climb this rung: it can stop"** — interrupt → checkpoint → human decides → resume. This is the slide that justifies tier 2 to an engineering manager, and it ties module 01's "draft" tier to module 14's approval gates: *a promise to have a human review it is only as real as this*.

Then the framework names, the five tier-choosing questions, and the closing quote — which now lands exactly where the build plan says Day 1 should end.

**Module 16** renamed to "Azure Foundry and the platform landscape" to match the lab.

### 2.14 Module 05 now uses your own measured numbers

The build plan records a verified finding I would not have guessed, and it is better than the slide I had written. Running the fat vs thin comparison three times out of three: the **fat** prompt asked to `read_skill` — a playbook it was already carrying — while the thin one went straight to `lookup_count`. 518 vs 355 prompt tokens, 31% saved.

The slide now leads with that: *518 prompt tokens, and it behaved worse* / *355 prompt tokens, and it went straight to the answer*, with the line "the saving is the smaller half of the story; the behaviour change is the lesson." A crowded context makes a worse chooser. That is a much stronger and more surprising claim than "context is expensive", and it is yours, measured, not borrowed.

The speaker note explicitly warns against narrating the scripted version where fat context is merely more expensive.

### 2.16 The PowerPoint repair prompt — actual root cause (my earlier diagnosis was wrong)

You had to save v3 as `- Repaired` too, which meant my chart theory in §2.9 was wrong. The real cause, found by diffing my package against PowerPoint's own repaired copy:

**`pptxgenjs` declares 111 slide masters in `[Content_Types].xml` and ships one.** 110 `<Override>` entries pointed at `/ppt/slideMasters/slideMaster2.xml` … `slideMaster111.xml`, none of which exist. That manifest is the one part of the package PowerPoint validates strictly, and a declaration with no matching part is a hard integrity failure. Every other tool ignores it — which is why `validate.py` passed, python-pptx opened it and LibreOffice rendered it 111 times without complaint.

This was present in **every** version I sent you, v2 and v3 alike. It scaled with slide count, so it appeared the moment the deck got large.

The post-processor now strips manifest entries whose part does not exist, and then re-verifies. Measured against PowerPoint's own repaired copy of my file:

| | my v3 (fixed) | PowerPoint's repaired copy |
|---|---|---|
| phantom manifest entries | **0** | 0 |
| dangling relationships | **0** | 0 |

Two lessons worth recording. First, `validate.py` passing is not evidence a deck opens in PowerPoint — it checks the XSD, relationships and content types *that exist*, not whether every declaration resolves. Second, the chart rewrite in §2.9 was not the fix, but it was still worth doing: the deck is smaller, carries no embedded Excel workbooks, and the charts now match the design system. I have left it in.

### 2.17 Correction from re-reading the week decks untruncated

My first pass over those 30 decks truncated every slide at ~404 characters. 113 slides exceeded that, so their dense content — which is exactly where the value was — went unread. I re-extracted and read the full text of those 113.

The material correction: **the agent landscape taxonomy has four columns, not three.** The deck's own slide (W1D4 s3) reads *Products / Builders / Runtimes / **Frameworks***, each with its own verb — use / build / execute / **develop** — crossed with audience. My module 16 slide had three; it now has four, with Frameworks highlighted as the column the two days actually occupy, and a line noting that some products sit in two columns at once because that is the business model rather than sloppiness.

Also newly readable, and worth having in your notes: the **complete** ten-item closing principles list from W6D5 ("start with the problem not the solution / have a metric / favor workflow over autonomy initially / work bottom up / start simple / start with large frontier models then reduce / think context rather than memory / most problems are solved with prompts / look at the traces / be a scientist"), and the strongest human-in-the-loop detail in the whole corpus — an agent that does not merely pause for approval but **hands the human the browser**.

The untruncated read also **confirmed** the earlier finding rather than overturning it: across all 90,000 characters, `security` appears zero times, as do `retriev`, `embed`, `vector` and `chunk`. Your modules 11, 12 and 14 have no counterpart in that course at all.

### 2.18 Things you got right that I kept
- "The model does not call the tool" as its own module, before anything else
- Refusing to call the official `tool_calls` loop ReAct
- "Most multi-agent systems should be one agent with more tools"
- Planting a poisoned document in module 12's corpus and detonating it in module 14
- The framework ladder as the signature artifact
- The six-layer platform table — the most durable handout in the deck
- "The best outcome might be a group that concludes no"

---

## 3. Design

### 3.1 What was wrong

| # | Fault | Detail |
|---|---|---|
| 1 | **45% of every slide empty** | Median content bottom: 6.2" of 11.25". 73/82 slides. |
| 2 | **No visuals at all** | No `ppt/media/` in the file. Zero images, zero icons. Three charts/diagrams in 82 slides. |
| 3 | **Monochrome** | One purple hue on near-white lavender. No accent, no semantic colour — nothing said "this is the danger one" or "this is the answer". |
| 4 | **Truncated table headers** | "HOW FAR?" (12), "WORKLOAD"/"RIGHT TOOL" (40), "WHAT IT IS"/"YOU WRITE"/"YOU GIVE UP" (43), "PROBLEM IT SOLVES"/"OPEN PATTERN"/"WHAT A CLOUD SELLS" (74) — all clipped mid-word. |
| 5 | **Run-together text** | Slide 2: "Delegation, then governancewhat should we automate at all?" — missing space between the bold label and its descriptor. Same on the first row. |
| 6 | **Clipped title subtitle** | Slide 1: the "Day 1 · Day 2 · Concepts and demos…" line ran off the bottom edge. |
| 7 | **Stray footer** | Slide 5 had "AI Agents in Practice" bottom-right, appearing nowhere else in the deck. |
| 8 | **Quote slides had no treatment** | Nine pull-quotes (17, 22, 23, 27, 32, 44, 50, 57, 80) set in body-sized text on the same white background as everything else. Your punctuation marks were invisible. |
| 9 | **The 2×2 was not a 2×2** | Slide 6 described two axes and rendered four flat text blocks with hairlines. The axes did not exist. |
| 10 | **Type scale too flat** | 28pt titles against 14pt body is not enough contrast; captions at 10pt were unreadable from the back. |
| 11 | **Single layout, all free-floating text boxes** | One `slideLayout` in the whole file. Nothing was placeholder-driven, so nothing was consistent by construction. |

### 3.2 The new system

**Canvas.** Standard 13.333 × 7.5in widescreen (the original was a 20 × 11.25in variant — valid, but non-standard and it made font sizing unintuitive).

**Palette** — one dominant, one sharp accent, three semantic:

| Role | Hex | Use |
|---|---|---|
| Indigo (dominant) | `5B4BE8` | Structure, "your code", primary |
| Deep indigo/near-black | `0B0A22` → `3B2E8F` | Dark slides — gradient backgrounds |
| Amber (the single accent) | `F5A524` / `E08700` | "The model asks", plain-terms band, emphasis |
| Green | `0E9F6E` | Correct / safe / the fix |
| Red | `D93A3F` | Wrong / danger / the failure |

Amber is the only sharp accent and it is used sparingly, so when it appears the eye goes there. Green and red are semantic, not decorative — a red card always means "this is the failure mode".

**Type.** Cambria bold headers paired with Calibri body, Courier New for code and protocol messages. Both header and body faces ship with Office and render true-to-width, so the QA passes are trustworthy. Serif headers give the deck an editorial rather than default-template feel. Scale: 46pt section titles / 30pt slide titles / 15pt card headers / 11.5pt body — real contrast at every level.

**Motif.** Icons in filled circles, repeated on every card, section divider and process step. 52 icons rendered from `react-icons` and embedded as PNGs.

**Rhythm.** Dark/light sandwich — dark for the title, all 18 section dividers, all nine pull-quotes, the Day 2 opener and the close; light for content. The quotes are now full-bleed dark slides at 34–42pt. They are the deck's breathing points.

**Layout.** Cards auto-size to their content and centre in the available band, so a slide never has a stretched empty box or a cramped one. Content fills the canvas.

### 3.3 The mixed-audience device
Since the room is split technical / non-technical, this is built into the design rather than handled ad hoc.

Every technical slide ends with a full-width amber band: **"In plain terms — [one sentence]"**. It does three jobs at once: it gives the non-technical half a guaranteed takeaway, it lets you go deeper for the engineers without losing anyone, and it fills the dead space at the bottom of the slide that was the deck's biggest visual problem.

Slide 2 explains the convention to the room explicitly: *"Yellow line = the takeaway. If a slide gets too technical, wait nine seconds and it will be restated."* That one sentence buys you permission to go deep for the rest of the two days.

### 3.4 Real diagrams, not bullet lists
Slides that were text now draw the thing they describe:

- **Assumed vs actual tool calling** — two contrasting flow diagrams, red and green, filling the slide. This is your most important teaching moment and it was four small boxes in the top third.
- **The API call** — messages → `create()` → `ChatCompletion`, with `tool_calls` planted as a dashed amber box labelled "appears here in module 02"
- **Chatbot / workflow / agent** — three cards, each containing its own miniature flow diagram
- **The 2×2** — an actual quadrant, with axis labels and "YOU ARE HERE"
- **ReAct** — a real cycle: Thought → Action → Pause → Observation around a ring
- **MCP's N×M problem** — 12 tangled red connections beside 7 clean ones through a single MCP box
- **JSON-RPC** — an actual wire message on screen
- **The five-question decision flow** — question boxes with YES/NO branches into stop/go outcomes

### 3.5 Speaker notes
Every one of the 111 slides has notes. Where a slide is new or a fact was corrected, the note says so and says why — so you are not re-deriving my reasoning at 7am. Answer keys stay in the notes and off the student-facing slides.

---

## 4. Two things to check before you deliver

1. **Verify the failures still fail.** Your `README.md` "Verify before delivery" table is the right instinct. Module 14 has no punchline if the unguarded RAG agent stops obeying the planted instruction, and module 13's lesson evaporates if the weak router stops misrouting. Test both the morning of.
2. **Replace the illustrative numbers.** Three charts (context growth, sequential vs concurrent) use placeholder figures and say so in a footnote. Run them live and read the room's own numbers out loud — a real dollar figure changes behaviour in a way an abstract warning never does.

---

## Sources

- [Gartner Predicts Over 40% of Agentic AI Projects Will Be Canceled by End of 2027](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)
- [MCP specification — Streamable HTTP transport](https://modelcontextprotocol.io/specification/draft/basic/transports/streamable-http)
- [The 2026-07-28 MCP Specification Release Candidate](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)
- [A2A Protocol Surpasses 150 Organizations — Linux Foundation](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year)
- [Google Cloud donates A2A to the Linux Foundation](https://developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation/)
- [Best open source agent frameworks (2026)](https://www.firecrawl.dev/blog/best-open-source-agent-frameworks)
- [How OpenTelemetry traces LLM calls, agent reasoning, and MCP tools](https://greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions)
- [LLM agent evaluation metrics: tool calling, task completion, trace-based evals](https://www.confident-ai.com/blog/llm-agent-evaluation-complete-guide)
