# Lab 18: How to choose an agent design

**CPU | API key: `OPENAI_API_KEY` | Optional: Graphviz for the drawings | Practises: choosing an agent design and saying what a second agent costs and buys**

## Goal

Decide when a second agent is worth what it costs, by looking at what the agent that writes the answer has to read.
The lab has two notebooks.

**Notebook 1** asks an everyday question: a book club has five books on its shortlist, which one should it read
next? One agent reads all five blurbs and answers. Then our code starts five small agents at the same time, each
reading one blurb and returning one line, and an agent with no tools picks the book from the five lines. Both pick the
same book. The agent that wrote the answer read five whole blurbs in the first design and five lines in the second;
the second design paid for that with more model requests and nearly twice the tokens. We then draw the three ways
to connect two agents (as a tool, with a handoff, in our own code), and let plain code answer the club's chat
commands with no model.

**Notebook 2** takes the designs to the Chinook music shop's support desk. A rep asks for five customers' totals. One
agent answers it; so do five sub-agents, one per customer, whose five lines go to an agent that writes the answer, and
we print that agent's whole input. A form's labelled requests are answered by code with no model call, and a wrong
label gets a correct sentence that answers the wrong question. The notebook ends with the four reasons to add a second
agent, each beside what the lab measured.

## What you will learn

- How to see what an agent read before it answered: the last model request of a run, its input and its tokens.
- How to run several agents at the same time from your own code with `asyncio.gather`, and pass their one-line results
  to an agent that writes the answer.
- How to compare designs on one question by the answer, the model requests, the tokens in total and the tokens the
  answering request read.
- How to tell the three ways of connecting two agents apart (as a tool, with a handoff, in your own code) from their
  drawings, and say who decides the next step in each.
- How to answer labelled requests in code with no model call, send the rest to an agent, and see what a wrong label
  does.
- How to decide whether a second agent is worth it with four reasons: different permissions, a smaller context,
  parallel work, and another team or model.

## What you will do

### Notebook 1: one agent or five, on a book club's shortlist (`18a_meet_agent_designs.ipynb`)

**Part A: Read the club's wishes and the five blurbs.** The four wishes, five blurbs of about 300 words, one read in
full, and the `read_blurb` tool.
**Part B: Let one agent read all five blurbs and answer.** The answer, the two model requests, and everything the
answering request read.
**Part C: Split the reading across five sub-agents that run at the same time.** One reader, five readers with
`asyncio.gather` under one trace, the chooser's whole input, and what the split cost.
**Part D: Connect two agents as a tool, with a handoff, and in our code.** The reader as a tool, a handoff to the
reader, and our own code, each drawn with `draw_graph`, and a table of who decides the next step.
**Part E: Answer the club's chat commands in code, with no model call.** `/next` and `/pages` answered by code, and a
free-text question sent to the agent.
**Challenge.** Let a model split the work, and ask what the readers' notes leave out.

### Notebook 2: agent designs at the Chinook support desk (`18b_agent_designs_at_the_desk.ipynb`)

**Part A: Look up five customers' totals by hand.** The three lookups, each on a database connection of its own, and
the five right totals.
**Part B: Measure what one agent reads before it answers.** The desk agent's three requests and everything its
answering request read.
**Part C: Split the lookups across five sub-agents and print what the answering agent reads.** One worker, five
workers at the same time, the main agent's whole input, and what the split cost.
**Part D: Answer the form's labelled requests in code and send the rest to the agent.** The form, a handler per
label, the router, and a mislabelled request.
**Part E: Decide when a second agent is worth its cost.** The four reasons, each beside what the lab showed.
**Challenge.** Ten customers instead of five, and a new label on the form.

### Going further (`18_extra_measure_the_designs.ipynb`)

Each design run five times on both questions, in one table; a test of one database connection shared by lookups
that run at the same time, with no model; and an A2A agent card for the desk's worker, checked against the fields the
A2A specification requires.

![Three designs side by side. One agent calls read_blurb five times and writes the answer after reading five whole blurbs. Our code starts five reader agents at the same time, each reading one blurb; their five one-line notes go to a chooser agent with no tools, which writes the answer after reading five lines. In the hybrid, our code checks whether a message is a command: /next and /pages are answered by our code with no model call, and free text goes to an agent.](resources/lab18_designs.png)

## Checkpoints

| After | You should see |
|---|---|
| Notebook 1, Part A | five books of 261 to 297 words; *Salt and Saffron* at 236 pages, with a third paragraph that says readers cried at the ending; `read_blurb` returns a blurb for a known title and a sentence for an unknown one |
| Notebook 1, Part B | *The Lighthouse Bakery*; 2 requests, the first asking for `read_blurb` five times in one reply; the answering request read the question, five calls and five blurbs (ours: 2,083 input tokens) |
| Notebook 1, Part C | one reader: one line, 2 requests; five readers: five lines in about the time of one; the chooser's whole input is the question and five lines, and it picks *The Lighthouse Bakery* (ours: 320 tokens); the split took 11 requests and 4,189 input tokens against one agent's 2 and 2,295 |
| Notebook 1, Part D | `Chooser with a reader tool` with `ask_blurb_reader` and dotted arrows both ways; `Front desk` with a one-way arrow to `Blurb reader` and its own `read_blurb`; the chooser drawn alone |
| Notebook 1, Part E | `/next` and `/pages The Night Ferry` (412 pages) with 0 model requests; the free-text question answered by the agent in 2 requests |
| Notebook 2, Part A | Helena Holý \$49.62 (the most), Puja Srivastava \$36.64, Richard Cunningham \$47.62, Luis Rojas \$46.62, Manoj Pareek \$38.62 |
| Notebook 2, Part B | all five totals and Helena named; 3 requests (five `find_customer` in one reply, five `get_invoices` in the next, then the answer); the answering request read ten calls and ten results (ours: 756 input tokens) |
| Notebook 2, Part C | one worker: one line, 3 requests; five lines with the right totals; the main agent's whole input is the request and five lines (ours: 125 tokens); the split took 16 requests and 3,364 input tokens against one agent's 3 and 1,472 |
| Notebook 2, Part D | three labelled requests answered with 0 model requests; the open request sent to the agent (\$12.98 more, 3 requests); the mislabelled request answered with Helena's rep, Steve Johnson, with 0 requests |
| Notebook 2, Part E | each of the four reasons matched to the part that showed it, or marked as not run |
| Going further | every design passed its check in 5 of 5 runs, at almost fixed counts; a shared connection gets some of 1,000 lookups wrong (ours: 112) and a connection per lookup none; an agent card with no required field missing |
| Challenges | notebook 1: the chooser asks for five readers in one reply, 12 requests, and its answering request falls between the other two designs (ours: 861 tokens); the chooser cannot say which book has recipes, and the one agent names *Salt and Saffron*. Notebook 2: at ten customers one agent's answering request grows by about 100 tokens per customer (ours: 1,287) and the main agent's by about 17 (208); `country` answered by code, `refund` sent to the agent |

**About the saved outputs.** They come from `gpt-6-luna` at reasoning effort `none`, the model `models.env` names.
The model writes its replies on every run, so wording and token counts can change on yours; check the books, the
totals and the counts of requests, not the words. Over five runs of each design (the extra notebook), every design
passed its check every time, the one-agent counts did not change at all, and the readers' lines moved the chooser's
input by a few tokens (322 to 353). The split's request counts (11 and 16) did not vary over the runs either, and the
hybrid's labelled answers make no model call at all.

## Before you start

- **Lab 00 first.** It checks the environment and that your key reaches the model.
- **Run it locally:** in the repository folder, `uv sync` (or `pip install -r requirements.txt`), put
  `OPENAI_API_KEY` in `.env` (copied from `.env.example`), then open a notebook in VS Code or JupyterLab
  (`uv run jupyter lab`) with the `.venv` kernel. Run the setup cell first. Each notebook runs on its own.
- **Graphviz** (optional): notebook 1's drawings need the `dot` program (`sudo apt install -y graphviz` on Ubuntu,
  `brew install graphviz` on a Mac). Without it only the three drawing cells fail.
- **Traces:** the SDK sends a trace of every run (questions, tool results, answers) to the Traces page of the OpenAI
  account that owns the key. `set_tracing_disabled(True)` from `agents` switches that off.
- **Data:** notebook 1 reads the five blurbs in `book_club/` (made-up books, written for this lab); notebook 2 reads
  `data/chinook.db`, the Chinook sample music shop, read-only. Nothing is written to disk.
- **Cost:** about 40 model requests for the two notebooks and about 160 for the extra, each of a few hundred to a few
  thousand tokens: well under one US cent in all at the prices in `models.env`.

## Folder contents

| Path | What it is |
|---|---|
| `18a_meet_agent_designs.ipynb` | notebook 1, the book club, with saved outputs |
| `18b_agent_designs_at_the_desk.ipynb` | notebook 2, the Chinook support desk, with saved outputs |
| `18_extra_measure_the_designs.ipynb` | going further: the designs over five runs, the shared-connection test, an A2A agent card |
| `book_club/` | the five blurbs notebook 1 reads |
| `resources/lab18_designs.mmd` and `.png` | the picture of the three designs: its mermaid source and the exported image |
| `solved/18a_meet_agent_designs_solution.ipynb` | notebook 1's challenge solved, run with its outputs |
| `solved/18b_agent_designs_at_the_desk_solution.ipynb` | notebook 2's challenge solved, run with its outputs |

## Resources

- [OpenAI Agents SDK: agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/): orchestration
  by a model and by code, agents as tools, handoffs, and agents run in parallel with `asyncio.gather`
- [OpenAI Agents SDK: tools](https://openai.github.io/openai-agents-python/tools/) and
  [handoffs](https://openai.github.io/openai-agents-python/handoffs/): `function_tool`, `Agent.as_tool`, `handoffs`
- [OpenAI Agents SDK: results](https://openai.github.io/openai-agents-python/results/) and
  [usage](https://openai.github.io/openai-agents-python/usage/): `raw_responses`, `to_input_list()`, requests and
  tokens
- [OpenAI Agents SDK: tracing](https://openai.github.io/openai-agents-python/tracing/) and
  [agent visualization](https://openai.github.io/openai-agents-python/visualization/): `trace()` and `draw_graph`
- [A2A specification](https://a2a-protocol.org/latest/specification/): the agent card and how agents find each other
- [Python `asyncio`: coroutines and tasks](https://docs.python.org/3/library/asyncio-task.html): `await`, `gather`
  and `to_thread`
- [Python `sqlite3`](https://docs.python.org/3/library/sqlite3.html): connections and threads

Next: [Lab 19: How to defend an agent from untrusted text](../19_Prompt_Injection/README.md). Back to [the lab list](../README.md).
