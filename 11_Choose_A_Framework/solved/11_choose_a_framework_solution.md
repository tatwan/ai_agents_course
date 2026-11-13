# Lab 11 Challenge: worked answer

A worked answer for both Challenge tasks, for one project at the Chinook shop. Your own project will have other
answers; what matters is that every weight comes from an answer to one of the six questions, every re-scored cell
names its evidence, and the tie-break is a reason, not a bigger total alone.

## Task 1: Choose a framework for the damaged-media desk

**The project.** A customer writes that a vinyl record arrived warped. The agent finds the customer and the
invoice, reads the damaged-media and refund policies, and proposes what the policies allow: one free replacement, or
a refund when the same title arrives damaged twice (ticket 06 is such a case). A replacement is sent at once; a
refund waits for a supervisor, who works through the queue twice a day. Every proposal is audited. The shop has
signed with a second model vendor and wants the desk to run on either from next quarter. Two Python developers
maintain it, in this repository's environment.

**The six questions.**

| Question | Answer | Effect |
|---|---|---|
| 1. Pause for a person, or outlast one request? | Yes: a refund waits hours and must survive a restart | Pause and approve: must-have |
| 2. Several agents? | No: one agent with five tools: three lookups, a policy search and the refund tool | Multi-agent: weight 1 |
| 3. More than one model vendor? | Yes, from next quarter | Any model vendor: must-have |
| 4. Who maintains it, in which language? | Two Python developers, in the core environment | Easy to learn: weight 2 |
| 5. Tracing from day one? | Yes: every proposal is audited | Tracing built in: must-have |
| 6. Or your own loop? | Not here: the durable pause, the trace and the second vendor would all be our code. But every proposal is audited, so we still want to see each step | Control of the loop: weight 2 |

Must-haves count with weight 3, so the weights are 2, 2, 1, 3, 3, 3 and the most a framework can reach is
3 × 14 = 42.

**Two re-scored cells.**

- **Google ADK, any model vendor: 2 → 1 for this job.** Lab 08 ran ADK on an OpenAI model, and it
  worked, but the reasoning effort set in `models.env` was not passed to ADK, so its agents ran at the model's
  default effort (notebook 1's setup note). This desk's monthly cost report assumes the effort we set, on both
  vendors. The switch works; it loses a setting this job uses.
- **OpenAI Agents SDK, pause and approve: 2 → 1 for this job.** In B2 a tool with `needs_approval` paused the run and
  `RunState` saved the pending call, but keeping that saved state somewhere that survives a restart, and loading only
  trusted state back, is our code's job. For a pause that lasts hours, that is the part we wanted from a framework.

Neither re-score changes the pick: both frameworks already failed the filter. That is worth knowing too: the pick
does not hang on a cell we were unsure of.

**The filter.** Pause and approve 3, tracing built in 3 and any model vendor 3: only **LangChain** (3, 3, 3) and
**LangGraph** (3, 3, 3) pass. Microsoft Agent Framework fails on the vendor (2), Pydantic AI on the pause (2), the
Agents SDK on the pause and the vendor.

**The totals.**

$$\text{LangChain} = 3 \times 2 + 2 \times 2 + 2 \times 1 + 3 \times 3 + 3 \times 3 + 3 \times 3 = 6 + 4 + 2 + 27 = 39$$

$$\text{LangGraph} = 1 \times 2 + 3 \times 2 + 3 \times 1 + 3 \times 3 + 3 \times 3 + 3 \times 3 = 2 + 6 + 3 + 27 = 38$$

**Reading the evidence.** One point apart, both on the same engine: `create_agent` returns a LangGraph graph
(Lab 09, Part A; `09b`). The evidence decides how much of that graph we write ourselves:

- The flow is one agent with one gate before one tool, which is what `HumanInTheLoopMiddleware` does (Lab 09,
  Part D; `09b`). Drawing the graph by hand buys control this flow does not use yet.
- The documents do not call for a document framework: the shop's 36 policy and ticket files are short enough that
  each stays one node at LlamaIndex's default chunk size (Lab 14, Part B; `14b`). A search function over a vector store, as
  Lab 13 builds, becomes the fourth tool.
- The resume check the desk needs is known: read `get_state(...).interrupts` before every resume, because a resume
  on a thread with nothing waiting starts a new run (Lab 10, Parts C and D; `10b`).

**The pick.** LangChain's `create_agent` with the three lookups, a policy search tool and `file_refund_request`
behind `HumanInTheLoopMiddleware`, a checkpointer on a database the service keeps, and the model behind LangChain's
chat-model interface so that the second vendor is a change of model object.

**We would change this pick if** refunds above an amount needed a second approver, or a retry when the payment
system is down: then the flow has branches beyond one gate, and we would write the same graph by hand in LangGraph.

## Task 2: Re-check one fact for the pick

We re-checked LangChain's row of Part E's table against the repository pin on 13 November 2026:

| Fact | Part E (30 Oct 2026) | Repository pin check (13 Nov 2026) | Where |
|---|---|---|---|
| Latest version | the 1.4 line (this repository pins 1.4.10) | 1.4.10 matches the pinned 1.4 line | [PyPI: langchain](https://pypi.org/project/langchain/) |
| GitHub stars | 148.7k | 148.7k | [GitHub: langchain-ai/langchain](https://github.com/langchain-ai/langchain) |
| Licence | MIT | MIT | the same GitHub page |
| Downloads, last 30 days | 170.46M | 170,457,766 | [pypistats: langchain](https://pypistats.org/packages/langchain) |

**Confirmed or corrected:** confirmed. The repository pin stays inside 1.4 (`1.4.10` vs earlier `1.4.x` releases). Under semantic versioning a patch release fixes bugs without changing the interface, so none of LangChain's scores moves; before upgrading the desk we would still read the release notes and re-run the desk's tests.
