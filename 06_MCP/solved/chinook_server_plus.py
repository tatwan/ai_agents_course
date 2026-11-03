"""Lab 06 challenge: the Chinook server with a fourth tool, get_recent_invoices.

A copy of 06_MCP/chinook_server.py; only the RecentInvoice shape and the new tool are added.
"""

import sqlite3
from pathlib import Path
from typing import TypedDict

from mcp.server import MCPServer

# The repository folder is the first folder above this file that holds data/chinook.db
ROOT = next(p for p in Path(__file__).resolve().parents if (p / "data" / "chinook.db").exists())
DB = ROOT / "data" / "chinook.db"

# Read-only: every write fails, whatever a host asks for
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, check_same_thread=False)

mcp = MCPServer("chinook")


# The shapes the tools return. MCPServer turns them into each tool's outputSchema.
class Customer(TypedDict):
    customer_id: int
    name: str
    country: str


class Invoices(TypedDict):
    customer_id: int
    invoice_count: int
    total: float


class SupportRep(TypedDict):
    customer_id: int
    support_rep: str | None


class RecentInvoice(TypedDict):
    invoice_id: int
    date: str
    total: float


@mcp.tool()
def find_customer(name: str) -> list[Customer]:
    """Find a Chinook customer by full name. Returns a list of matches, each with its customer_id."""
    rows = con.execute(
        "SELECT CustomerId, FirstName || ' ' || LastName, Country FROM customers "
        "WHERE FirstName || ' ' || LastName = ?",
        (name,),
    ).fetchall()
    return [{"customer_id": r[0], "name": r[1], "country": r[2]} for r in rows]


@mcp.tool()
def get_invoices(customer_id: int) -> Invoices:
    """Count a customer's invoices and add up their total in US dollars."""
    count, total = con.execute(
        "SELECT COUNT(*), SUM(Total) FROM invoices WHERE CustomerId = ?", (customer_id,)
    ).fetchone()
    return {"customer_id": customer_id, "invoice_count": count, "total": round(total or 0, 2)}


@mcp.tool()
def get_support_rep(customer_id: int) -> SupportRep:
    """Name the support rep assigned to a customer."""
    found = con.execute(
        "SELECT e.FirstName || ' ' || e.LastName FROM customers c "
        "JOIN employees e ON e.EmployeeId = c.SupportRepId WHERE c.CustomerId = ?",
        (customer_id,),
    ).fetchone()
    return {"customer_id": customer_id, "support_rep": found[0] if found else None}


@mcp.tool()
def get_recent_invoices(customer_id: int, limit: int = 3) -> list[RecentInvoice]:
    """List a customer's most recent invoices, newest first, with their date and total in US dollars."""
    rows = con.execute(
        "SELECT InvoiceId, date(InvoiceDate), Total FROM invoices WHERE CustomerId = ? "
        "ORDER BY InvoiceDate DESC LIMIT ?",
        (customer_id, limit),
    ).fetchall()
    return [{"invoice_id": r[0], "date": r[1], "total": r[2]} for r in rows]


if __name__ == "__main__":
    mcp.run("stdio")
