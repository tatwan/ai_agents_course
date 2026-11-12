# Lab 15: How to build a customer-support agent over a database

**CPU | API key: `OPENAI_API_KEY` | Practises: grounding an agent in business data, a database behind a chat page that several people use at once**

## Goal

Put an agent behind a chat page that several people use at the same time, and keep each person's conversation their
own. The lab has two notebooks.

**Notebook 1** is a café. A bot behind a chat page takes an order from one visitor: *"A flat white with oat milk,
please."* A second visitor, in another browser tab, asks *"What did I order?"* and is told about the first visitor's
coffee, because our code keeps one list of messages for the whole page. Keyed by the visitor's session, the second
visitor is told there is no order yet.

**Notebook 2** takes the same page to the Chinook support desk. The agent looks customers up in the shop's database
through a connection that refuses every write, and keeps each conversation in a session file. Rep A asks about
Helena Holý; rep B, who has said nothing yet, asks *"Which customer were we talking about?"* and is told *"We were
talking about Helena Holý."* One line, the session id, gives each rep their own conversation. Then the same page runs
as a program from a terminal.

## What you will learn

- How to put a Python function behind a Gradio `ChatInterface`, and test the page from code as two visitors with
  `gradio_client`.
- Why one list in the code behind a page is shared by every visitor, and how `request.session_hash` gives each
  visitor their own conversation.
- How to build a desk agent from lookups that read a database through a read-only connection, and make a lookup say
  in words when it finds nothing.
- How to prove that the connection refuses a write, whatever a model sends.
- How the Agents SDK's `SQLiteSession` keeps a conversation in a file, and how to key it per visitor behind a page.
- How to run the page as its own program from a terminal with `app.py`.

## What you will do

### Notebook 1: meet chat pages on a café order (`15a_meet_chat_pages.ipynb`)

**Part A: Put a function behind a chat page.** An `echo` function, called by hand, then behind `gr.ChatInterface`
and opened in the browser.
**Part B: Visit the page from code as two visitors.** The page's API description ("Use via API" and `view_api()`),
two `gradio_client` visitors, and the `history` the page passes.
**Part C: Let a model take the order, with one list for the whole page.** The café bot on Chat Completions; visitor
A orders, visitor B asks what they ordered.
**Part D: Tell visitors apart with `gr.Request`.** `gr.Request` and `request.session_hash`, compared with each client's own id.
**Part E: Keep one conversation per visitor.** A dictionary keyed by the session id; two new visitors on a fresh page.
**Challenge.** A `start over` message, and a table number for every visitor.

### Notebook 2: a support desk agent behind a chat page (`15b_chat_pages_at_the_desk.ipynb`)

**Part A: Build the desk agent from read-only lookups.** The database opened read-only, what a query returns when
nothing matches, three lookups that say so in words, and the agent run once.
**Part B: Prove that the database refuses a write.** A `DELETE` on the agent's connection, and the same statement on
a writable copy.
**Part C: Keep a conversation in a session file.** `SQLiteSession`, what one run stores, and the file's rows per
session.
**Part D: Put the desk agent behind a page with one session for everyone.** Two reps on a page whose session id is a
constant.
**Part E: Give every rep their own session.** `request.session_hash` as the session id; rep A and rep B again, as two
new visitors.
**Part F: Run the desk page from a terminal.** `app.py` read, then started from a terminal and visited in two tabs.
**Challenge.** A named tool for a question the lookups do not cover, and a conversation keyed by the rep's name.
**Going further.** Named lookups against one free SQL tool, one run each; the agent's tool steps shown while it works;
a check that the lookups, `respond` and `INSTRUCTIONS` in `app.py` are the text the notebook tested.

![The support desk page: a rep's message goes to respond, which names the session after the rep's open page; the Agents SDK's runner reads that SQLiteSession, calls the model and the three lookups on the read-only database, and the reply goes back to the same rep](resources/lab15_page_flow.png)

## Checkpoints

| After | You should see |
|---|---|
| Notebook 1, Part A | `echo` by hand counts 0 messages before; the page at `http://127.0.0.1:7860/` (the next free port if 7860 is busy) |
| Notebook 1, Part B | `view_api()` lists one endpoint, `/echo`, with one parameter, `message`; visitor A counts 0 then 2 messages before, visitor B 0 |
| Notebook 1, Part C | visitor B, who never ordered, is told about a flat white with oat milk; the list holds five messages, both visitors' turns |
| Notebook 1, Part D | one id for both of A's messages, another for B's, each equal to its client's `session_hash` |
| Notebook 1, Part E | B is told there is no order yet, A is told the flat white with oat milk; two conversations, 5 messages for A and 3 for B |
| Notebook 2, Part A | customer 6, Helena Holý; 7 invoices, $49.62, Steve Johnson; `No customer has customer_id 75.`; the agent calls `find_customer`, then `get_invoices` and `get_support_rep` |
| Notebook 2, Part B | `OperationalError \| attempt to write a readonly database` and invoice 404 still there; on the writable copy 412 invoices, then 411 |
| Notebook 2, Part C | 8 items stored for one turn (the question, three tool calls, three results, the reply); one `session_id`, `notebook` |
| Notebook 2, Part D | rep B, who asked nothing before, is told *"We were talking about Helena Holý."*; one `page` session with 12 items |
| Notebook 2, Part E | rep B is asked which customer they mean; one session per rep, named by their session ids |
| Notebook 2, Part F | in the terminal, the setup line and `Support desk page at http://127.0.0.1:7861 (Ctrl+C to stop)`; two tabs with their own conversations |
| Challenges | notebook 1: after `start over` A has no order and B keeps the cappuccino; A at table 1, B at table 2. Notebook 2: `top_billing_countries` called once, the USA and $523.06; a second client named Ana is told Helena Holý, Omar is asked for a name |
| Going further | the named lookups decline the country question, free SQL answers the USA and $523.06; each tool step pending, then done, the reply last; five ✅ and the program's exit code 0 |

**About the saved outputs.** They come from `gpt-6-luna` at reasoning effort `none`, the model `models.env` names.
The pages, the clients, the session ids and the sessions file behave the same on every run; the model's wording,
its tool calls and the timings vary, so check who was told what and the facts, not the words. Visitor B was told the
first visitor's coffee in 10 of 10 runs with one list, rep B was told about Helena Holý in 16 of 16 with one session
for the page, and neither happened with a session per visitor.
Given `(0, None)` as the tool result for customer 75, the agent answered *"Customer 75 has 0 invoices"* in 8 of 8
runs, which is why the lookups say in words when a customer does not exist.

## Before you start

- **Lab 00 first.** It checks the environment and that your key reaches the model.
- **Run it locally:** in the repository folder, `uv sync` (or `pip install -r requirements.txt`), put
  `OPENAI_API_KEY` in `.env` (copied from `.env.example`), then open a notebook in VS Code or JupyterLab
  (`uv run jupyter lab`) with the `.venv` kernel. Run the setup cell first. Each notebook runs on its own.
- **Pages and ports:** the notebooks start their pages on `http://127.0.0.1:7860` (the next free port if that one is
  busy), one at a time, and close each; `app.py` uses port 7861. Open an address in your browser while its page is
  running to try it by hand.
- **On a remote VM or in Codespaces:** `127.0.0.1` is the remote machine, not yours. VS Code forwards the ports for
  you (see its **Ports** panel; add the port there if it is missing): open the forwarded address instead.
- **Data:** notebook 2 reads `data/chinook.db`, the Chinook sample music shop, and only ever opens it read-only.
- **Files it writes:** `15_Support_Desk_Agent/outputs/` (git ignores it): notebook 2's sessions file, a writable copy
  of the database for Part B, and `app.py`'s own sessions file.
- **Traces:** notebook 2's agent runs are recorded on the Traces page of the OpenAI account that owns the key, as
  every Agents SDK run is; `app.py` switches that off.
- **Cost:** about 30 short model calls for the two notebooks, well under one US cent at the prices in `models.env`.

## Run the page from the terminal

From the repository folder:

```
uv run python 15_Support_Desk_Agent/app.py
```

Then open `http://127.0.0.1:7861` in your browser, in two tabs to see two conversations. Ctrl+C stops it.

## Folder contents

| Path | What it is |
|---|---|
| `15a_meet_chat_pages.ipynb` | notebook 1, the café, with saved outputs |
| `15b_chat_pages_at_the_desk.ipynb` | notebook 2, the Chinook support desk, with saved outputs |
| `app.py` | the support desk page as a program: the same lookups, agent and `respond` as notebook 2 |
| `resources/lab15_one_list_or_per_visitor.mmd` and `.png` | notebook 1's picture: one list for the page against one list per visitor |
| `resources/lab15_page_flow.mmd` and `.png` | notebook 2's picture of the desk page |
| `solved/15a_meet_chat_pages_solution.ipynb` | notebook 1's challenge solved, run with its outputs |
| `solved/15b_chat_pages_at_the_desk_solution.ipynb` | notebook 2's challenge solved, run with its outputs |

## Resources

- [Gradio: `ChatInterface`](https://www.gradio.app/docs/gradio/chatinterface): the function's arguments,
  `additional_inputs` and streaming with `yield`
- [Gradio: `Request`](https://www.gradio.app/docs/gradio/request): `session_hash`, and `username` once a page has
  sign-in
- [Gradio: the API page](https://www.gradio.app/guides/view-api-page): what the "Use via API" link shows
- [Gradio: the Python client](https://www.gradio.app/guides/getting-started-with-the-python-client): `Client`,
  `view_api`, `predict` and `submit`
- [OpenAI Agents SDK: sessions](https://openai.github.io/openai-agents-python/sessions/): `SQLiteSession` and the
  other session classes
- [OpenAI Agents SDK: tools](https://openai.github.io/openai-agents-python/tools/): `function_tool` and the schema it
  writes from a function
- [SQLite: URI filenames](https://www.sqlite.org/uri.html): `mode=ro` and the other query parameters

Next: [Lab 16: How a coding agent edits files and runs tests](../16_Coding_Agent/README.md). Back to [the lab list](../README.md).
