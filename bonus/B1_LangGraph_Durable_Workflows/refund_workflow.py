"""The Chinook desk's refund workflow for bonus lab B1.

It is kept in a file so that a program that starts again can build the same workflow again.
No model is called: a request is looked up, waits for a reviewer, and is filed after an approval.
"""
from contextlib import closing
from pathlib import Path
import sqlite3

from typing_extensions import TypedDict
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

# The shop's database, found from this file's own location and opened read-only
CHINOOK = Path(__file__).resolve().parents[2] / "data" / "chinook.db"

# The desk's own tables, in the outputs/ folder beside the notebook that runs the workflow
DESK_DB = Path("outputs") / "desk.db"

# What a reviewer is shown about a request
PACKET_FIELDS = ["request_id", "customer", "invoice_id", "invoice_total", "amount", "reason"]


class Refund(TypedDict):
    request_id: str         # the desk's number for this request
    invoice_id: int
    amount: float
    reason: str
    customer: str           # added by look_up_invoice
    invoice_total: float    # added by look_up_invoice
    decision: str           # added by review
    status: str             # how the request ended, in words


def create_desk_tables():
    """Create the two tables the workflow writes to, if they are not there yet."""
    with closing(sqlite3.connect(DESK_DB)) as desk:
        desk.execute("CREATE TABLE IF NOT EXISTS notices (request_id TEXT, message TEXT)")
        desk.execute("CREATE TABLE IF NOT EXISTS refund_requests "
                     "(request_id TEXT, invoice_id INTEGER, amount REAL, reason TEXT)")
        desk.commit()


def show_desk():
    """Print what the two tables hold."""
    with closing(sqlite3.connect(DESK_DB)) as desk:
        notices = desk.execute("SELECT request_id FROM notices").fetchall()
        requests = desk.execute("SELECT request_id, invoice_id, amount FROM refund_requests").fetchall()
    print("notices sent:   ", [row[0] for row in notices] or "none")
    print("refund_requests:", requests or "empty")


def look_up_invoice(state):
    """Read the invoice from the shop's database: who it belongs to and its total."""
    print("LOOKED UP invoice", state["invoice_id"])
    with closing(sqlite3.connect(f"file:{CHINOOK}?mode=ro", uri=True)) as shop:
        row = shop.execute(
            "SELECT c.FirstName || ' ' || c.LastName, i.Total FROM invoices i "
            "JOIN customers c ON c.CustomerId = i.CustomerId WHERE i.InvoiceId = ?",
            (state["invoice_id"],)).fetchone()
    if row is None:
        return {"status": f"not filed: no match for invoice {state['invoice_id']}"}
    return {"customer": row[0], "invoice_total": row[1]}


def after_lookup(state):
    """A request whose invoice was not found ends here. Every other request goes to review."""
    if state.get("status"):
        return END
    return "review"


def notify_reviewer(state):
    """Tell the reviewer that a request is waiting: one new row in the notices table."""
    message = (f"Refund request {state['request_id']} is waiting for you: "
               f"invoice {state['invoice_id']}, {state['amount']} US dollars")
    with closing(sqlite3.connect(DESK_DB)) as desk:
        desk.execute("INSERT INTO notices (request_id, message) VALUES (?, ?)", (state["request_id"], message))
        desk.commit()
    print("NOTICE SENT to the reviewer for", state["request_id"])


def review(state):
    """Tell the reviewer, then stop and wait for the decision."""
    notify_reviewer(state)
    decision = interrupt({field: state[field] for field in PACKET_FIELDS})
    if decision == "approve":
        return {"decision": "approve"}
    return {"decision": "reject", "status": f"not filed: the reviewer said: {decision}"}


def after_review(state):
    """Only an approved request is filed."""
    if state["decision"] == "approve":
        return "file_request"
    return END


def file_request(state):
    """Write the refund request: one new row in the refund_requests table."""
    with closing(sqlite3.connect(DESK_DB)) as desk:
        desk.execute("INSERT INTO refund_requests (request_id, invoice_id, amount, reason) VALUES (?, ?, ?, ?)",
                     (state["request_id"], state["invoice_id"], state["amount"], state["reason"]))
        desk.commit()
    print("REFUND REQUEST FILED for", state["request_id"])
    return {"status": "filed"}


def build_graph(checkpointer, review_node=review):
    """Wire the workflow and attach the checkpointer that keeps its runs."""
    builder = StateGraph(Refund)

    builder.add_node("look_up_invoice", look_up_invoice)
    builder.add_node("review", review_node)
    builder.add_node("file_request", file_request)

    builder.add_edge(START, "look_up_invoice")
    builder.add_conditional_edges("look_up_invoice", after_lookup, ["review", END])
    builder.add_conditional_edges("review", after_review, ["file_request", END])
    builder.add_edge("file_request", END)

    return builder.compile(checkpointer=checkpointer)
