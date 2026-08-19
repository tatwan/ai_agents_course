# Course data

## `chinook.db`

The sqlitetutorial edition of Chinook: a digital music shop.

Tables are lowercase and plural (`customers`, `invoices`, `invoice_items`, `tracks`, `albums`, `artists`, `employees`, `genres`). Columns stay PascalCase (`CustomerId`, `SupportRepId`). Invoice dates run 2009-01-01 to 2013-12-22.

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

Used from modules **08** (Agents SDK), **09** (LangGraph), **10** (charting), **13** (delegation), and **15** (evals). Tools stay read-only.

Verified answers for the recurring customers: **Helena Holy** (CustomerId 6) 7 invoices, $49.62, support rep Steve Johnson. **Puja Srivastava** (CustomerId 59) 6 invoices, $36.64, support rep Jane Peacock. Both names are unique in the table.

Open it with `check_same_thread=False`. Agent frameworks run sync tools in a worker thread, and the default connection refuses that.

Expected answers for the recurring questions live in the instructor notes for those modules. Do not regenerate this file.

## `flight_data.csv` and `fun_facts.csv`

Instructor-supplied. Read with the `csv` module. A past lab (`other_content/02_function_calling.ipynb`) loaded them through DuckDB; this course does not. No DuckDB. No live weather.

| File | Rows | Columns |
|---|---|---|
| `fun_facts.csv` | 26 | `City`, `Fun Fact` |
| `flight_data.csv` | 496 | `from_city`, `to_city`, `price`, `duration` |

These are the **only** data source for five places, not just module 02:

| Where | Uses them for |
|---|---|
| 02 tool calling | `get_fact`, `get_flight` — the first tool schemas |
| 03 ReAct loop | Same two tools, hand-rolled then official loop |
| 05 context engineering | `get_fact` / `get_flight` as the travel playbook's tools |
| 06 MCP | `modules/06_mcp/server.py` reads them in its own process |
| 07 async | The async twins `get_fact_async` / `get_flight_async` |

So a change to either file ripples across five modules and `server.py`. Check all of them before editing a row.

Not every city pair has a flight, and not every city has a fact — that is deliberate, since `no flight found` and `no fact for that city` are what the notebooks feed back to the model as an observation. Verified pairs used in the notebooks: Barcelona to Dubai 646.86 / 829, Barcelona to Amman 909.99 / 404, Sydney to Madrid 249.66 / 99, Tokyo to Moscow 259.3 / 525.

## `corpus/`

Instructor-supplied. Do not regenerate. 36 short markdown files: 20 shop policies and 16 support tickets for the same Chinook music shop that `chinook.db` uses.

Used from modules **11** (retrieval), **12** (agentic RAG), and **14** (security). Module 10 does not read this folder.

Two questions have no answer in any file (so a honest agent must say so):

- What is Chinook's revenue target for 2014?
- What is the CEO's personal mobile number?

One ticket carries a planted prompt-injection payload. It is not named `injection.md`. Do not regenerate this folder.

A change to a policy or ticket ripples across 11, 12 and 14. Check those modules before editing a paragraph.
