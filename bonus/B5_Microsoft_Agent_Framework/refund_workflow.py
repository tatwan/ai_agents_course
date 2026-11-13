"""The Chinook desk's refund workflow: read the invoice, wait for a reviewer, write the refund.

The steps live in this file, not in a notebook, so that another Python process can import
the same code and build the same workflow again from a checkpoint.
"""
from contextlib import closing
from pathlib import Path
import sqlite3
from typing import Never

from agent_framework import (
    Executor, FileCheckpointStorage, WorkflowBuilder, WorkflowContext,
    executor, handler, response_handler,
)

LAB = Path(__file__).resolve().parent
CHINOOK = LAB.parent.parent / "data" / "chinook.db"

# Everything the workflow writes goes here (git ignores every outputs/ folder)
FOLDER = LAB / "outputs" / "refund_desk"
REFUNDS = FOLDER / "refunds.db"


@executor(id="check_invoice")
async def check_invoice(invoice_id: int, ctx: WorkflowContext[dict, str]):
    """Step 1: read the invoice from the shop's database. Our code reads the amount, so nobody types it."""
    # One read-only connection per lookup
    with closing(sqlite3.connect(f"file:{CHINOOK}?mode=ro", uri=True)) as con:
        row = con.execute(
            "SELECT CustomerId, Total FROM invoices WHERE InvoiceId = ?", (invoice_id,)
        ).fetchone()

    if row is None:
        await ctx.yield_output(f"No match for invoice {invoice_id}. Nothing to refund.")
    else:
        await ctx.send_message({"invoice_id": invoice_id, "customer_id": row[0], "amount": row[1]})


class Review(Executor):
    """Step 2: ask a person, and wait for the answer."""

    @handler
    async def ask(self, refund: dict, ctx: WorkflowContext[dict]):
        await ctx.request_info(request_data=refund, response_type=bool)

    @response_handler
    async def decide(self, refund: dict, approved: bool, ctx: WorkflowContext[dict, str]):
        if approved:
            await ctx.send_message(refund)
        else:
            await ctx.yield_output(f"Refund for invoice {refund['invoice_id']} rejected. Nothing written.")


@executor(id="file_refund")
async def file_refund(refund: dict, ctx: WorkflowContext[Never, str]):
    """Step 3: write the refund. The invoice number is the table's key, so a second write is ignored."""
    with closing(sqlite3.connect(REFUNDS)) as con, con:
        written = con.execute(
            "INSERT OR IGNORE INTO refunds VALUES (?, ?, ?)",
            (refund["invoice_id"], refund["customer_id"], refund["amount"]),
        ).rowcount

    if written:
        await ctx.yield_output(f"Refund for invoice {refund['invoice_id']} written.")
    else:
        await ctx.yield_output(f"Refund for invoice {refund['invoice_id']} is already on file. Nothing written.")


def build_workflow():
    """Build the workflow: the same three steps, names and edges every time."""
    FOLDER.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(REFUNDS)) as con, con:
        con.execute(
            "CREATE TABLE IF NOT EXISTS refunds "
            "(invoice_id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL)"
        )

    review = Review(id="review")
    storage = FileCheckpointStorage(FOLDER / "checkpoints")

    builder = WorkflowBuilder(name="refund", start_executor=check_invoice, checkpoint_storage=storage)
    builder.add_edge(check_invoice, review)
    builder.add_edge(review, file_refund)
    return builder.build(), storage


def refund_rows():
    """Every row of the refunds table, as a list of tuples."""
    with closing(sqlite3.connect(REFUNDS)) as con:
        return con.execute("SELECT invoice_id, customer_id, amount FROM refunds").fetchall()
