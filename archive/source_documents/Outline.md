# AI Agents — 2-Day Instructor Guide (Final)

**Client:** KPMG · **Audience:** Developers, Data Scientists, Technical Managers · **Format:** 2 × 8h (≈6.5h net each) · **Environment:** Ubuntu VM per attendee (VS Code, Chrome, Python)

**Design stance:** platform-agnostic by default, cloud-specific where the platform genuinely adds something. Attendees leave understanding agents well enough to build one on any stack, and knowing which vendor sells which layer.

---

## 1. The spine

Teach it as a **build-up**. Each module exists because the previous one left a problem unsolved. This is what keeps a concept-heavy course from feeling like a tour of logos, and it is what makes the content survive the next round of vendor renaming.

```
Hand-rolled ReAct loop
   → tools are ad-hoc and unportable        → MCP
   → the loop is fragile and unobservable   → frameworks
   → the model doesn't know your data       → retrieval & memory
   → one agent can't hold the whole job     → multi-agent & A2A
   → nothing here is safe or measurable     → governance
   → who sells you these layers?            → platform landscape
   → what should we actually automate?      → process re-engineering
```

Say this out loud at the start of Day 1 and put it on a slide you return to at every transition. It is the single highest-leverage thing you can do for retention.

**The anchor is your from-scratch agent.** Build it in front of them in the first two hours, and refer back to it all the way through: *"remember the twelve lines where we appended the tool result to the message list? That's what a framework's state object replaces."* Everything downstream becomes a delta against something they have already seen work.

---

## 2. The six-layer reference model

This is your one durable artifact. Put it on a slide early, return to it in the platform module, and hand it out. It answers "what applies to me?" for someone on any cloud.

| Layer | The problem it solves | Open source | Azure | AWS | Google |
|---|---|---|---|---|---|
| **Model** | Reasoning and tool selection | Llama, Qwen, Mistral via Ollama/vLLM | Microsoft Foundry model catalog | Bedrock | Vertex AI / Gemini API |
| **Tools** | Give the model hands, portably | **MCP** (open standard) | Foundry tool catalog, MCP support | **AgentCore Gateway** — wraps APIs, Lambdas, and existing MCP servers as tools | Vertex tool governance, MCP support |
| **Orchestration** | Control flow, state, retries | LangGraph, CrewAI, **Google ADK**, **AWS Strands**, Microsoft Agent Framework, Pydantic AI | Foundry Agent Service, Connected Agents | **AgentCore Runtime / Harness** | **Vertex AI Agent Engine** |
| **Context** | Memory and grounding | Chroma, pgvector, FAISS, LlamaIndex, Pinecone | Azure AI Search / Foundry IQ | **AgentCore Memory** | Vertex AI Search |
| **Delegation** | Agents talking to agents | **A2A** (Linux Foundation) | Connected Agents | AgentCore Runtime (A2A support) | ADK + A2A (Google-originated) |
| **Governance** | Identity, safety, evals, cost, traces | LangSmith, Langfuse, OpenTelemetry | Entra Agent ID, content filters / prompt shields, Foundry evaluators | **AgentCore Identity + Observability** | Vertex governance + evaluation |

**The teaching point:** the two rows in bold — MCP and A2A — are open standards, not products. Everything else is a vendor's implementation of a pattern you can build yourself. That is the whole argument for learning the pattern first.

### How to handle AWS and GCP in the room

**Reference only. No demo, no lab, no time budget.** They exist in this course for one reason: so nobody leaves thinking agents are an Azure concept. Azure is the only cloud that gets hands-on, because it's the one this crowd is likeliest to be on.

Practically, that means each cross-cloud mention is a **single sentence at the end of a concept module**, in the same shape every time: *"the pattern you just built is sold as X on Azure, Y on AWS, Z on Google."* Then move on. Four or five of these across two days, roughly thirty seconds each.

Two things to protect:

- **Don't volunteer depth you don't want to defend.** Naming a service invites a question about it, and a wrong answer about AWS in front of a KPMG architect costs more than the mention was worth. If pressed beyond the mapping table, the honest and entirely credible answer is that the layer is equivalent, the pricing and identity models differ, and you'd want to check current docs before advising — then bring it back to the pattern.
- **Don't let a cross-cloud tangent eat a module.** If someone wants to go deep on Bedrock, park it for the break. The mapping table is the artifact that satisfies that curiosity without spending class time.

The payoff line for the platform module: *every one of these clouds converged on the same two open standards within a year of each other — which tells you the pattern is the durable thing, and the products are the perishable thing.*

### Currency notes (verify the week of delivery — this space moves monthly)

- **AWS:** AgentCore went GA in October 2025 with Runtime, Gateway, Memory, Browser, Code Interpreter, Identity, and Observability as composable services. AgentCore Harness — a managed, config-driven agent loop — reached GA on 17 June 2026, and **Bedrock Agents Classic entered maintenance for new customers after 30 July 2026**. If anyone in the room says "we're on Bedrock Agents," that distinction matters to them.
- **Google:** ADK hit 1.0 GA across Python, Go, Java, and TypeScript at Cloud Next in April 2026, with 2.x lines since. It is model-agnostic despite being Google-built, and can both consume MCP servers and expose an agent *as* one.
- **A2A** is now a Linux Foundation project with 150+ backing organizations at its one-year mark in April 2026 — worth saying explicitly, because "Google protocol" is the objection you'll get otherwise.
- **Azure:** naming has moved from Azure AI Foundry toward Microsoft Foundry, and the classic agent API (threads/runs) is deprecated with a 2027 retirement. Don't teach the classic surface.

---

## 3. Where everything runs

| Tier | What | Who touches it | Cost |
|---|---|---|---|
| **T1 — Local on the VM** | Python, VS Code, MCP servers, MCP Inspector, Chroma, LlamaIndex, Docker sandbox | Everyone | $0 |
| **T2 — The OpenAI key you issue** | **Every** lab, code-along and hands-on segment | Everyone, via `.env` | ~$15–20 total |
| **T5 — Azure Foundry** | One pre-built environment, one 20-min demo block | You | ~$5 |
| **T–opt — A second provider** | Optional 3-minute instructor aside, on **your own** key | You | $0 |

> [!IMPORTANT]
> **Students touch exactly one model provider: OpenAI, on the key you issue.** No student activity depends on Gemini, Ollama, Colab, a local model, web search, or any second account. This is a deliberate narrowing — it removes every credential-provisioning failure mode from the room, and none of it costs the course anything pedagogically, because *which* model is behind the loop is not what this course teaches.

### What was dropped, and why it doesn't matter

**Ollama and local models: cut entirely.** A 4B quantized model on a CPU-only 2-vCPU VM produces 5–10 tokens/second, so a three-tool agent loop is roughly two minutes of dead air. The point it was carrying — that the pattern is model-independent — is a sentence, not a demo.

**Colab: cut entirely.** It introduces a second environment, a mid-course context switch, and a bet on whether corporate Google accounts can reach it. Not worth it for one demo.

**Gemini: demoted to optional.** If you want the model-swap moment, run it on your own key for three minutes at the M3 transition and move on. Record it during prep so you can play the recording if the room is running long or the network isn't cooperating. If you skip it entirely, nothing downstream breaks.

> [!NOTE]
> If you *do* run it live on a free Gemini tier: those terms allow prompts and responses to be used to improve Google products, with human review. For a KPMG room that is disqualifying for anything real — use synthetic data only, and **say so out loud**. It is a free, concrete governance lesson that lands harder than a slide about data handling. (EEA/Switzerland/UK users get paid-tier terms applied, which may matter depending on where attendees sit.)

### The consequence for shared helper code

Provider-swapping was the headline justification for a client factory, and it is now mostly gone. Keep the file, but scope it honestly — it is a small utility, not a signature asset. What it still earns its place doing:

- **Centralised model pinning.** `MODEL_DEFAULT` and `MODEL_STRONG` read from `.env`, so re-pinning the week of delivery is one edit rather than twenty notebooks. This matters because M12 and M13 only teach if the model still fails.
- **Shared defensive defaults** — `max_tokens` cap, retry with exponential backoff.
- **The token counter** that M13's cost segment reads back from students' own runs.
- **One seam to point at** when you say the loop doesn't care which model it calls.

**The signed datasheet names Pinecone, LangChain, LangSmith, and LlamaIndex.** Those appear in the course objectives KPMG bought. Keep them visible: LangGraph covers LangChain, LangSmith covers your tracing and evaluation demo on its free developer tier. **A named slide mention for Pinecone and LlamaIndex is too thin** — an attendee holding the signed PDF will notice the difference between "mentioned" and "shown". Lab 2 therefore runs the *same* retrieval three ways (see M10). Delivering a course with none of the four named tools is the kind of gap an attendee notices when comparing against the PDF.

### How every hands-on asset is authored

Every lab, code-along and demo ships as a **self-guided Jupyter notebook** that a student could complete alone, following the same four-stage rhythm:

```
1. LEARN         Why we are building this, and what breaks without it
2. DO               Guided implementation, annotated with the non-obvious rationale
3. OBSERVE     "What just happened?" — inspect state, wire traffic, tokens, cost
4. CHALLENGE  A concrete student task with acceptance criteria and a solution
```

Three rules make this survive contact with the clock:

- **Every stage carries a time budget in its header.** A 35-minute code-along cannot absorb the same CHALLENGE as a 60-minute lab. Budget the stages to the module, don't budget the module to the stages.
- **Every CHALLENGE is labelled `[in-class]` or `[take-home]`.** Demo modules get take-home challenges so the notebook is still a complete self-study artifact after the course, without pretending there was class time to attempt it.
- **Every CHALLENGE has a written solution** — as a collapsed `<details>` block for short tasks, or a `solution_*.ipynb` beside the starter for full labs. No task ships without one.

**Standalone services get a dual treatment.** MCP servers, the A2A endpoint, and the Docker sandbox runner are prototyped interactively in the notebook *and* extracted to clean, runnable `.py` files, with the exact terminal commands to launch and test them from the VS Code terminal. Students need to see both that it works in a cell and that it runs as a process.

---

## 4. Day 1 — Build it, then see what each layer buys you

| Time | Module | Mode | Runs on |
|---|---|---|---|
| 0:00–0:20 | **M0 · Welcome + the payoff** | Demo | T2 |
| 0:20–1:10 | **M1 · What an agent actually is** | Slides + exercise | — |
| 1:10–1:25 | Break | | |
| 1:25–2:25 | **M2 · The model layer: tool calling from first principles** | Slides + code-along | T2 |
| 2:25–3:10 | **M3 · Mini Claude Code — a real agent in 150 lines** | **Demo** | T2 |
| 3:10–4:10 | Lunch | | |
| 4:10–4:55 | **M4 · The tool layer: why MCP exists** | Slides + demo | T1 |
| 4:55–5:55 | **M5 · LAB 1 — write your own MCP server** | **Lab** | T1 + T2 |
| 5:55–6:10 | Break | | |
| 6:10–7:00 | **M6 · The orchestration layer: what frameworks add** | Slides + code-along | T2 |
| 7:00–7:35 | **M7 · Charting agent + safe code execution** | Demo + **hands-on** | T1 + T2 |
| 7:35–7:45 | Wrap | | |

*Changes from the first draft: M1 trimmed 60→50 (35 min slides + 15 min exercise — 45 minutes of slides in hour one was too much); the afternoon break restored to a real 15 minutes; M7 extended 30→35 and converted from pure demo to hands-on so that the datasheet's **BI/charting agent** gets actual student keyboard time. Net instruction: 6h15m.*

### M0 · Welcome + the payoff (20 min)
Run the finished capstone agent in front of them before you explain anything. Show it answer a business question by querying a database, retrieving a document, running code, and producing a chart. Then say: *you will have built every part of this by 4pm tomorrow.* Environment check in the same block — everyone runs one smoke-test script.

**Build the capstone on the same e-commerce database and policy corpus the labs use**, so every component on screen is one they will later build themselves and can point at. (The catalogued source for this demo, `agents/6_mcp/4_lab4.ipynb`, drives a 16-file stock-trading simulator — too much surface area for 20 minutes, and the wrong domain for this room.)

### M1 · What an agent actually is (50 min)
- Agent vs. workflow vs. chatbot vs. RPA. The distinction that matters: **who decides the control flow, you or the model?**
- Anatomy: model, instructions, tools, memory, loop, stop condition.
- The autonomy spectrum, from suggest → draft-for-approval → act-with-audit → act. Introduce this early; you'll use it as the grading scale in the Day 2 workshop.
- Where agents create value, and the three places they reliably disappoint: high-volume low-margin tasks where a deterministic script is cheaper, tasks where the cost of a wrong action is unbounded, and tasks where the required context was never written down.
- **Exercise (15 min):** four candidate processes on a slide. In pairs, score each on volume, judgment required, cost of error, and context availability. Report out. This seeds the Day 2 workshop and gets the technical managers talking in the first hour, which is when you win or lose them.

### M2 · Tool calling from first principles (60 min)
**This is the "without a framework" half of the course's central contrast.** Twenty minutes of slides on the request/response shape — tool schemas, why JSON Schema, the tool-call and tool-result message roles, why the model never executes anything itself. Then 40 minutes of code-along building a ReAct loop in roughly 80 lines: a `while` loop, a tool registry dict, a dispatcher, and a stop condition. The notebook's final cell writes `shared/agent_core.py` — the student's own file, which later modules import so nobody retypes eighty lines. That is the only shared code in the course; everything else stays inline in the notebook that teaches it.

**Teach the pattern and the API as two separate things.** Open with *text-based* ReAct — `Thought → Action → PAUSE → Observation`, parsed out of plain text with a regex, no tool-calling API involved. Then build the same loop on native function calling. The contrast is the real lesson: **the ReAct pattern is independent of the tool-calling API**, which is exactly why it predates function calling and still works on models that lack it. Students who only ever see `tools=[...]` come away thinking ReAct *is* an OpenAI feature.

Emphasise the three things everyone gets wrong the first time: returning errors to the model as text rather than raising, keeping the full message list including tool results, and having any stop condition at all.

### M3 · Mini Claude Code (45 min, demo)
Your signature demo, and the best asset you have. Five tools — `read_file`, `list_dir`, `grep`, `write_file`, `run_bash` — and the same loop from M2. Point it at a small repo with a failing test and let it read, diagnose, patch, run the test, and self-correct.

Then **break it deliberately**: remove the turn cap and let it thrash, or give it two tools with overlapping descriptions and watch it pick wrong. Ten minutes on why that happened is worth an hour of slides. This is also where you preview every Day 2 governance topic — they will have *seen* the failure mode before you name it.

**Model independence is one sentence here, not a demo.** Point at the single line where the client is constructed and say the loop doesn't care what's behind it. If you want to show it, rerun one simple task on a second provider using **your own** key — three minutes, recorded in advance as a fallback, and entirely skippable if the room is running long. Nothing downstream depends on it.

### M4 · The tool layer: MCP (45 min)
Frame it as the answer to a problem they just felt: in M3, every tool was hand-wired to one agent, in one language, in one process. MCP standardises that boundary so a tool written once is usable by any client.

Cover hosts/clients/servers, stdio vs. HTTP transports, capability discovery, and the security surface — tool poisoning, prompt injection through tool descriptions, over-broad scopes. Demo the filesystem reference server and inspect the raw JSON-RPC; five minutes of watching the actual protocol demystifies it completely.

Keep this a **demo, not a lab** — students get their hands on MCP Inspector fifteen minutes later in M5, and duplicating it here costs a module for no new learning. Use the local filesystem reference server only: the catalogued source for this module drives Playwright over `npx` and a remote hosted MCP endpoint, which on a 2-vCPU VM behind a corporate proxy is a coin flip you do not need to take in front of the room.

**Cloud callout:** AgentCore Gateway turns existing APIs, Lambda functions, and MCP servers into a single governed tool endpoint; Foundry has a tool catalog; ADK can both consume MCP and expose an agent as an MCP server. All three converged on the same standard within a year — that convergence *is* the argument for learning MCP rather than a vendor's tool format.

### M5 · LAB 1 — write your own MCP server (60 min)
Three read-only tools over a sample customer/orders/inventory SQLite database. Test with MCP Inspector **before any model is involved** — proving the tools work independently of the agent is a habit worth installing, and it is also the module's real hands-on protocol moment, which is why M4 stays a demo rather than duplicating it. Then attach the server to the M2 agent and ask a question that requires two tools chained.

This doubles as the **customer-support database agent** from the original datasheet.

> [!NOTE]
> **Authored new.** The mapped source (`agents/6_mcp/2_lab2.ipynb`) turned out to *consume* an MCP server through the OpenAI Agents SDK in 37 lines rather than *author* one — it is a tour, not a lab. The `@mcp.tool()` decorator shape from `agents/6_mcp/backend/accounts_server.py` is reused, but its domain (mutating stock trades) is replaced with read-only e-commerce queries, and the regex-validated safe-SQL pattern is lifted from `master_llm_deployments/01_Modern_Stack/lab1_part2`.

### M6 · The orchestration layer (50 min)
Twenty minutes on what frameworks actually add: state management, retries and error recovery, streaming, checkpointing and resumption, human-in-the-loop interrupts, and built-in observability. Then a 30-minute code-along porting the M2 agent to LangGraph and gaining those for free.

Comparison slide covering LangGraph, CrewAI, Google ADK, AWS Strands, Microsoft Agent Framework, and Pydantic AI — organised by *what kind of control they give you*, not by feature checklist. The honest summary: graph-based frameworks when the control flow matters, role-based when the team metaphor fits the problem, and no framework at all when the loop is genuinely simple. They have now built all three positions themselves.

### M7 · Charting agent + safe code execution (35 min, demo → hands-on)

Two datasheet items, one artifact. The agent is asked a business question about the Lab 1 database, **writes matplotlib code**, and that code has to execute somewhere — which is exactly the moment the sandboxing question becomes concrete rather than theoretical.

- **Demo (20 min):** the sandboxing spectrum — bare `subprocess` (never), Docker, gVisor/Firecracker, hosted sandboxes (E2B, Azure Container Apps dynamic sessions, AgentCore Code Interpreter). Run the same `run_bash` tool with and without a container boundary and show what an unconstrained agent can reach on the VM. Cover timeouts, resource caps, network egress, and filesystem scope as four *separate* controls.
- **Hands-on (15 min):** students run the charting agent themselves, get a PNG out, then re-run it with the container boundary removed and watch the same generated code touch the host filesystem.

This is the datasheet's **BI / charting & data analysis agent**, and it is the only place in the course where students execute model-written code themselves. Docker must be pre-pulled into the VM image — a cold `docker pull` across 20 machines on conference Wi-Fi will destroy this module.

---

## 5. Day 2 — Ground it, scale it, govern it, then decide who to buy from

| Time | Module | Mode | Runs on |
|---|---|---|---|
| 0:00–0:20 | **M8 · Recap + rebuild the spine** | Talk | — |
| 0:20–1:05 | **M9 · The context layer: memory and retrieval** | Slides + demo | T1 + T2 |
| 1:05–2:05 | **M10 · LAB 2 — agentic RAG** | **Lab** | T1 + T2 |
| 2:05–2:20 | Break | | |
| 2:20–3:05 | **M11 · The delegation layer: multi-agent and A2A** | Slides + demo | T1 + T2 |
| 3:05–3:40 | **M12 · Supervisor pattern** | Code-along | T2 |
| 3:40–4:40 | Lunch | | |
| 4:40–5:45 | **M13 · Governance: injection, identity, evals, cost** | Demo + **hands-on** | T1 + T2 |
| 5:45–5:55 | Break | | |
| 5:55–6:35 | **M14 · The platform landscape** | Slides + **Azure demo** | T5 |
| 6:35–7:30 | **M15 · Process re-engineering workshop** | Workshop | — |
| 7:30–7:45 | Close, Q&A, resources | | |

> [!WARNING]
> **The first draft of this schedule ran M13 → M14 → M15 → close as 3h05m with no break**, placing M15 — the workshop the business half of the room came for — at the fatigue trough. That is fixed above: M13 gains 5 minutes for its hands-on segment, a 10-minute break lands after it, M14 trims to 40, and the close trims to 15. Net instruction: 6h20m.

### M9 · Context: memory and retrieval (45 min)
Why single-shot RAG fails on real questions — multi-hop, ambiguous phrasing, comparative queries, and questions whose answer requires knowing what *isn't* there. The agentic alternative: rewrite → retrieve → assess → re-retrieve → cite.

Cover chunking as the decision that determines everything downstream, embedding choice, hybrid search, and reranking. Vector store landscape: Chroma and FAISS for local, pgvector when you already run Postgres, Pinecone and Weaviate as managed, LlamaIndex as the ingestion and indexing layer above all of them. **Name Pinecone and LlamaIndex here explicitly** — datasheet coverage.

Close with the slide nobody else gives them: **when not to use RAG.** If the answer lives in a database, query the database. If it lives in an API, call the API. RAG is for unstructured text you can't otherwise reach.

### M10 · LAB 2 — agentic RAG (60 min)
Local Chroma, OpenAI embeddings, a corpus of synthetic policy documents and support tickets. Build the loop, then measure it against a naive single-shot baseline on the same five questions — including two that are deliberately unanswerable from the corpus, so they see whether their agent admits it.

Running this locally is a deliberate choice: they can inspect every hop, break it, and rerun in seconds. Show the managed equivalent in M14 and make the point that the service replaces forty lines, not the reasoning pattern.

**Datasheet coverage, earned rather than asserted.** One OBSERVE section runs the *same* retrieval over the *same* corpus three ways, side by side: Chroma (run locally), **LlamaIndex** (run locally — it is pip-installable and needs no account), and **Pinecone** (code shown and explained, not executed, since it needs a signup). The teaching point writes itself — the ingestion and indexing layer is swappable, the reasoning loop above it is not. This converts two datasheet items from a slide bullet into something attendees have watched run, for roughly eight minutes of lab time and $0.

> [!NOTE]
> **Authored new.** The mapped source (`4_langchain_langgraph/community_contributions/Vagz1216/`) is a web-search deep-research agent, not retrieval over a private corpus — wrong shape, and it needs a search API key we do not issue. The corpus, the reflection-grading node, and the benchmark set are written for this course. One corpus document carries the planted injection payload that M13 detonates.

### M11 · The delegation layer (45 min)
Patterns: supervisor/orchestrator, sequential pipeline, hierarchical teams, peer network, blackboard. Trade-offs in latency, token cost, debuggability, and failure modes.

Then the contrarian slide, which is the one they'll remember: **most multi-agent systems should be one agent with more tools.** Multi-agent earns its complexity when subtasks need genuinely different tools, different models, different permissions, or independent scaling. Otherwise you have bought yourself a distributed systems problem in exchange for a metaphor.

A2A: what it standardises (agent cards, capability discovery, task delegation across vendors), and its Linux Foundation governance with 150+ organisations behind it. MCP is agent→tool; A2A is agent→agent. Attendees mix these up constantly — a single side-by-side slide fixes it permanently.

### M12 · Supervisor pattern (35 min, code-along)
Three specialists behind one orchestrator, built on the LangGraph agent from M6. Keep tool counts low and descriptions sharply distinct — a small router model routes poorly when tools overlap, and if it misroutes live, that *is* the lesson. Have a stronger model configured as a one-line switch so you can rerun the same task and let the room see the difference. It costs a few dollars and makes the case for model routing better than a slide.

> [!WARNING]
> **This demo depends on the weak router actually misrouting.** Verify it during prep against the exact model IDs you pin — if the small model has improved enough to route correctly, the module silently stops teaching anything and you need to widen the tool-description overlap until it fails again. See the model-pinning note in §6.

> [!NOTE]
> **Authored new.** The mapped source (`4_langchain_langgraph/4_lab4.ipynb`) is a `deepagents` sub-agent notebook that generates PowerPoint — it is not a supervisor graph, despite being catalogued as one.

### M13 · Governance (65 min)
- **Live demo, then hands-on (20 min at the keyboard):** indirect prompt injection. Poison a document in the Lab 2 corpus with instructions, watch their own agent obey it, then add the guardrail that stops it. Nothing else you do today will land harder — and because it is *their* Lab 2 agent that gets compromised, they should run it themselves rather than watch you run it. Students execute a small attack suite against their unguarded agent, add the layered validators, and re-run to produce a before/after table.
- Threat model: injection, tool poisoning, exfiltration via tool arguments, runaway loops, confused deputy.
- Identity: why agents need their own, not a shared service account. Entra Agent ID, AgentCore Identity, OAuth on-behalf-of. This is the topic KPMG's own risk practice will ask about.
- Human-in-the-loop: map the autonomy spectrum from M1 onto approval gates.
- **Evaluation:** the dimensions that matter — task completion, tool-call correctness, groundedness, cost per task, latency. Demo LangSmith tracing on the free developer tier (datasheet coverage), and show a trace of the multi-agent run from M12.
- **Cost:** where tokens actually go in agent loops (context regrowth every turn), caching, model routing, and why a per-task budget cap belongs in the loop itself.

### M14 · The platform landscape (40 min)
The six-layer table from section 2, walked slowly. For each layer: what you'd build yourself, what each cloud sells, and what you give up either way.

Then the **Azure demo (20 min)** on your pre-built environment — the one place a specific platform earns its own segment. Show what a managed agent service replaces: Agent Builder as the no-code surface, a Connected Agents wiring, the trace view, and the content filter configuration. Frame it explicitly as *"here is our Day 1 loop, as a managed product"* — because that framing is only available to you because you built the loop first.

Close on lock-in analysis: the model is swappable, tools are portable if you used MCP, orchestration is portable if you used an open framework, and the sticky layers are memory, identity, and observability. That is a genuinely useful thing for an architect to take back.

### M15 · Process re-engineering workshop (55 min)
The module the business half of the room came for, and the one the technical rewrite dropped.

In groups of four: pick a real process from your own function. Map it step by step. For each step assign an autonomy tier from M1. Identify where the context lives and whether it's written down anywhere an agent could read. Estimate cost of error per step. Then design the agent — or conclude it shouldn't be one.

Report out, and grade against the M1 rubric. The most valuable outcome here is a group that concludes their process *shouldn't* be automated, and can say why. Call that out as a win when it happens.

---

## 6. Prep asset inventory

Build these in this order — each depends on the one before, and the first three are 80% of the value.

1. **`agent_core.py` + `m2_react_loop.ipynb`** — the M2 ReAct loop. Everything on Day 1 is a derivative of this file.
2. **`mini_claude_code/`** — M3 demo, five tools, plus a small repo with a planted failing test.
3. **Client factory** — a small `get_client()` reading `MODEL_DEFAULT` / `MODEL_STRONG` from `.env`, plus shared retry, `max_tokens` caps and the token counter. Students only ever use the `openai` path; the optional second-provider branch exists for your three-minute aside. Scope it as a ~40-line utility, not a headline asset.
4. **Lab 1 kit** — `lab1_mcp_server.ipynb` (starter, with TODOs), `solution_lab1.ipynb`, and the extracted `server.py` / `agent_client.py` for terminal runs.
5. **Sample SQLite database** — products, orders, customers, inventory. Synthetic, no client data.
6. **Document corpus** — 30–50 synthetic policy docs and support tickets, with two questions deliberately unanswerable and one document carrying a planted injection payload for M13.
7. **`m6_langgraph_port.ipynb`** — the M6 code-along, before and after, using the Lab 1 MCP tools rather than a web-search tool (no extra API key, and it continues the story from M5).
8. **Charting + sandbox kit** — the M7 agent that writes matplotlib code, with and without a container boundary. Docker image pre-pulled into the VM.
9. **Lab 2 kit** — corpus, `lab2_agentic_rag.ipynb` (starter), `solution_lab2.ipynb`, `benchmark_questions.json`, and the three-way Chroma / LlamaIndex / Pinecone retrieval comparison.
10. **Pre-built Azure environment** — one resource group, Foundry account on **Basic** setup, one project, one model deployment, one agent, one Connected Agents wiring, tracing on.
11. **Recorded fallbacks** — for the Azure demo, the local-model demo, and anything network-dependent.

Guardrails to bake into every starter notebook and script: `max_tokens` capped, a hard turn limit, retry with exponential backoff, tool exceptions returned to the model as `role: "tool"` text rather than raised, and a per-run token counter printed at the end. The token counter pays off twice — it prevents runaway spend and it gives M13's cost section live data from their own work.

**Pin model IDs in one place.** Every notebook reads its model from a single `MODEL_DEFAULT` / `MODEL_STRONG` pair in `.env` via the client factory, so re-pinning at prep time is one edit rather than twenty. Do not hard-code a model name in a notebook cell. Note that the source repositories this course draws from already reference `gpt-5.x`-class mini models while earlier drafts of this outline named `gpt-4o-mini` — check what is current the week you deliver, and re-verify both the M12 misrouting demo and the M13 injection payload against whatever you pin, because both teach *only* if the model still fails.

---

## 7. Cost

| Item | Estimate |
|---|---|
| OpenAI tokens (`MODEL_DEFAULT`, small/mini tier, all labs, 21 people) | $10 – $15 |
| `MODEL_STRONG` for the M12 routing comparison | $3 – $5 |
| Embeddings for the corpus | < $1 |
| Optional second provider (instructor's own key, 3 min) | $0 |
| LangSmith free developer tier | $0 |
| LlamaIndex (local, in Lab 2) | $0 |
| Pinecone (code shown, not executed) | $0 |
| Docker / Chroma / MCP Inspector (local) | $0 |
| Azure Foundry (your prep + one demo block) | $3 – $8 |
| **Total** | **$20 – $30** |

Still set an Azure budget alert before provisioning, still delete the resource group the evening the class ends, and still revoke the OpenAI key that hour.

---

## 8. Prep sequence

**Two weeks out**
- [ ] Confirm with whoever owns the KPMG account that a platform-neutral delivery is expected, given the other instructor's Azure-leaning revision. If the client asked for Azure specifically, you need to know now.
- [ ] Confirm VM specs — vCPU and RAM determine whether the local-model demo is viable
- [ ] Confirm the VM can reach `api.openai.com` from the client network — that is the **only** external endpoint any student activity needs

**One week out**
- [ ] Build assets 1–9 above
- [ ] Bake into the VM image: Node (for MCP Inspector), the Docker sandbox image **pre-pulled**, and the Chroma/LlamaIndex wheels — none of these should download during class
- [ ] Confirm the VM can reach `api.openai.com` from the client network, and that nothing else is required to reach the internet
- [ ] Provision the Azure environment; confirm the demo runs end to end from a clean browser session
- [ ] Create a dedicated OpenAI project and key with rate and spend limits
- [ ] *(Optional)* If you want the M3 model-swap aside, get a second provider key **for yourself**, run it once, and record it
- [ ] Bake the starter repo into the VM image

**Day 0**
- [ ] Dry-run both labs and all four code-alongs end to end on a fresh VM, timing each
- [ ] Record fallbacks for every demo
- [ ] Verify the M13 injection payload still works against your current model — model updates sometimes patch the exact phrasing

**After**
- [ ] Revoke the OpenAI key, delete the Azure resource group, check the invoice at 48 hours and at month close
