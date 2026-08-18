# Current state (internal)

Author and agent status. Students should start at [README.md](README.md). After a module or a wave, update **this file** and the "Where we stopped" section in `BUILD_PLAN.md`.

**2026-08-19, corpus + module 10 done.** Modules 00–10 are written. 11–17 are not.

| | |
|---|---|
| **Next action** | Module 11 (retrieval) in [BUILD_PLAN.md](BUILD_PLAN.md). One module, then stop. |
| **Why** | `data/corpus/` is on disk. 11, 12 and 14 can start. |
| **Then** | 12–17, one at a time. |
| **Deck** | Present from `presentation/ai_agents_in_practice_v3 - Repaired.pptx` (111 slides, aligned to 00-17). Older decks are in `archive/decks/`. |
| **Do not** | Build module 12 yet. Trust the Status column below without running the module. |

Where things live:

- [BUILD_PLAN.md](BUILD_PLAN.md) — the running order (Waves 1–5). Start here.
- [AUDIT.md](AUDIT.md) — the reasoning, with what was verified and how many trials.
- [AGENTS.md](AGENTS.md) — binding working rules for any agent session.
- [README.md](README.md) — public, student-facing overview.
- `archive/presentation_outline.md` — lesson-slide brief, modules 00–03 only.

## Modules

Weight is relative effort, not minutes. **Cut first** is what to drop if the room is behind.

| # | Module | Weight | Status | Cut first |
|---|---|---|---|---|
| 00 | OpenAI API: one call, the response object, streaming, cost | S | **Built** | Cut streaming if the room already uses the SDK daily |
| 01 | What an agent is, and when it should not be one | M | **Built** | Shrink the pair exercise |
| 02 | Tool calling: the model does not call the tool | M | **Built** | Do not cut |
| 03 | The ReAct loop | L | **Built** | Do not cut |
| 04 | How a coding agent touches your files | M | **Built** | Cut the breakage segment |
| 05 | Context engineering | M | **Built** | Cut compaction; keep progressive disclosure |
| 06 | Why MCP exists | M | **Built** | Compress the protocol trace to one request |
| 07 | Async and concurrent tool calls | M | **Built** | Compress the Python primer |
| 08 | OpenAI Agents SDK | L | **Built** | Cut handoffs; keep the two graphs |
| 09 | LangGraph | L | **Built** | Cut the gate / interrupt; keep the loop graph |
| 10 | Charting agent and the sandbox | M | **Built** | Cut Docker if the daemon is down; keep the jail probe |
| 11 | Retrieval | M | Not started | Keep one retrieval path |
| 12 | Agentic RAG | M | Not started | Collapse into 11 if behind |
| 13 | Delegation | L | Not started | Cut A2A to a slide |
| 14 | Security | L | Not started | Do not cut the attack |
| 15 | Evals, traces, cost | M | Not started | Keep the cost ledger |
| 16 | Azure Foundry / platform landscape | M | Not started | Teach from captured output if down |
| 17 | Process re-engineering | L | Not started | Do not cut |

**Day 1 is 00–09. Day 2 is 10–17.**

Hard order: 00 first. 03 before 04 and 05. 07 before 08–09. 06 before a framework consumes MCP. 01 before 17. `data/corpus/` before 11, 12 and 14.

**CrewAI and LlamaIndex are not modules.** They are rungs on the framework-ladder slides, plus a ten-minute aside inside 13. Both downgrade `openai` in the shared venv.

## Verify before delivery

**Confirmed 2026-08-18 by running it.** Both model IDs exist on the class key. Tool calling with `reasoning_effort="none"` works on Chat Completions. `reasoning_effort="low"` plus tools returns a 400. Chinook facts: Helena Holý 7 / $49.62 / Steve Johnson, Puja Srivastava 6 / $36.64 / Jane Peacock.

Still outstanding — these modules only teach if the model still fails:

| Module | What must happen |
|---|---|
| 13 | The weaker router misroutes when specialist descriptions overlap |
| 14 | The unguarded RAG agent obeys the planted instruction. **nano 0/3 on 2026-08-19** — retune before delivery. |
| 04 | The `write_file` / `save_file` overlap actually causes a wrong pick |
| 05 | Fat first `create` still asks `read_skill` for a playbook it already carries |

Also confirm the `dot` (graphviz) binary is on the student VM image, or `draw_graph` degrades to a printed exception in 02, 03, 06 and 08.

Re-pin models in `.env`. Do not edit twenty notebooks. `gpt-5.4` family: `max_completion_tokens`, not `max_tokens`. Do not pass `temperature`. Pin `reasoning_effort="none"` unless a cell needs more.
