# Lab data

The labs use one music shop's database, policies and support tickets. These files are bundled so that a notebook
does not depend on a live shop system. Read them in place; do not regenerate or edit the supplied data.

## `chinook.db`

This is the public [Chinook sample database from SQLite Tutorial](https://www.sqlitetutorial.net/sqlite-sample-database/).
It describes a digital music shop. Tables use lowercase plural names such as `customers`, `invoices` and
`invoice_items`; columns retain names such as `CustomerId` and `SupportRepId`. Invoice dates run from
2009-01-01 to 2013-12-22.

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

The recurring customer checks are:

| Customer | CustomerId | Invoices | Total spent | Support representative |
|---|---|---|---|---|
| Helena Holý | 6 | 7 | $49.62 | Steve Johnson |
| Puja Srivastava | 59 | 6 | $36.64 | Jane Peacock |

The database-tool and analysis labs inspect these records before using them. Their answer checks compare with
the database, rather than treating a model's memory of this public sample as evidence of a lookup.

### Open a read-only connection

With `path` pointing to the bundled database, the notebooks use:

```python
db = sqlite3.connect(f"file:{path}?mode=ro", uri=True, check_same_thread=False)
```

`mode=ro` prevents changes to this database. `check_same_thread=False` lets a framework invoke a synchronous
lookup in a worker thread; it does not itself make a connection read-only or make concurrent writes safe.
Labs that demonstrate writes create a separate database in their own ignored output folder.

## `corpus/`

There are 36 short Markdown files: 20 shop policies and 16 support tickets for the Chinook desk. The retrieval
labs search these files; the injection lab reads a ticket as untrusted input. The notebook explains the input
record and its file name before transforming it.

Two questions have no answer in the supplied files:

- What is Chinook's revenue target for 2014?
- What is the CEO's personal mobile number?

A nearest search result does not establish that either question is answerable. One ticket contains a planted
instruction; it is deliberately not named `injection.md`. A planted-claim variant used in a notebook is made in
memory, leaving the shared file unchanged. The policies and tickets are teaching fixtures, rather than a current
shop's operating rules or customer requests.
