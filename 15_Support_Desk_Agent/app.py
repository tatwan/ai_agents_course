"""The Chinook support desk as a chat page, run from the terminal.

From the repository folder:   uv run python 15_Support_Desk_Agent/app.py
or from this folder:          uv run python app.py
Then open http://127.0.0.1:7861 in a browser. Stop the page with Ctrl+C.

The lookups, the instructions, the agent and respond are the ones 15b_chat_pages_at_the_desk.ipynb builds and tests.
Models come from models.env, the key from the environment or .env (never printed), and the shop database is opened
read-only.
"""
import difflib
import os
import sqlite3
import warnings
from pathlib import Path

from dotenv import dotenv_values

warnings.filterwarnings("ignore", message="IProgress not found")   # a progress-bar notice printed on import
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"                   # Gradio sends usage statistics unless told not to

import gradio as gr  # noqa: E402
from agents import Agent, ModelSettings, Runner, SQLiteSession, function_tool, set_tracing_disabled  # noqa: E402
from openai.types.shared import Reasoning  # noqa: E402

# The repository folder is the first folder above this file that holds models.env
LAB = Path(__file__).resolve().parent
ROOT = next(p for p in LAB.parents if (p / "models.env").exists())

# Models come from models.env; a non-empty value in .env replaces one of them; the key is never printed
settings = dotenv_values(ROOT / "models.env")
local = dotenv_values(ROOT / ".env")
settings.update({name: value for name, value in local.items() if name in settings and value})
os.environ.setdefault("OPENAI_API_KEY", local.get("OPENAI_API_KEY") or "")
assert os.environ["OPENAI_API_KEY"], "Put OPENAI_API_KEY in .env at the repository folder (copy .env.example)."
MODEL = settings["MODEL_DEFAULT"]
EFFORT = settings["REASONING_EFFORT"] or None

# A page that many reps use should not upload their conversations as traces
set_tracing_disabled(True)

# The shop database, read-only; the conversations in a file git ignores
DB_PATH = ROOT / "data" / "chinook.db"
conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True, check_same_thread=False)
ALL_NAMES = [row[0] for row in conn.execute("SELECT FirstName || ' ' || LastName FROM customers")]
SESSIONS_DB = LAB / "outputs" / "app_sessions.db"
SESSIONS_DB.parent.mkdir(exist_ok=True)
PORT = 7861


def find_customer(name: str) -> dict:
    """Find a Chinook customer by first and last name. Returns the matching customers with their customer_id;
    when none matches exactly, up to three close names to try."""
    rows = conn.execute(
        "SELECT CustomerId, FirstName || ' ' || LastName, Country FROM customers "
        "WHERE FirstName || ' ' || LastName = ?", (name,)).fetchall()
    if rows:
        return {"matches": [{"customer_id": r[0], "name": r[1], "country": r[2]} for r in rows]}
    return {"matches": [], "close_names": difflib.get_close_matches(name, ALL_NAMES, n=3, cutoff=0.8)}


def get_invoices(customer_id: int) -> dict | str:
    """Count a customer's invoices and add up their totals in US dollars."""
    if conn.execute("SELECT 1 FROM customers WHERE CustomerId = ?", (customer_id,)).fetchone() is None:
        return f"No customer has customer_id {customer_id}."
    count, total = conn.execute(
        "SELECT COUNT(*), ROUND(SUM(Total), 2) FROM invoices WHERE CustomerId = ?", (customer_id,)).fetchone()
    return {"customer_id": customer_id, "invoice_count": count, "total": total}


def get_support_rep(customer_id: int) -> dict | str:
    """Name the support rep assigned to a customer."""
    row = conn.execute(
        "SELECT e.FirstName || ' ' || e.LastName FROM customers c "
        "LEFT JOIN employees e ON e.EmployeeId = c.SupportRepId WHERE c.CustomerId = ?", (customer_id,)).fetchone()
    if row is None:
        return f"No customer has customer_id {customer_id}."
    return {"customer_id": customer_id, "support_rep": row[0]}


INSTRUCTIONS = ("You help the support reps of a music shop. Look up every fact with the tools; never answer from "
                "memory. If the tools cannot answer a question, say so. Answer in one or two sentences.")

desk = Agent(
    name="Chinook desk",
    instructions=INSTRUCTIONS,
    model=MODEL,
    tools=[function_tool(f) for f in (find_customer, get_invoices, get_support_rep)],
    model_settings=ModelSettings(reasoning=Reasoning(effort=EFFORT)),
)


async def respond(message, history, request: gr.Request):
    session = SQLiteSession(request.session_hash, SESSIONS_DB)
    result = await Runner.run(desk, message, session=session)
    return result.final_output


if __name__ == "__main__":
    print("model:", MODEL, "| reasoning effort:", EFFORT, "| key found: yes")
    print(f"Support desk page at http://127.0.0.1:{PORT} (Ctrl+C to stop)", flush=True)
    page = gr.ChatInterface(
        respond,
        title="Chinook support desk",
        description="For Chinook support reps: customers, invoices and support reps, looked up read-only. "
                    "Fictional data from the Chinook sample database.",
        examples=["How many invoices does Helena Holý have, and who is her support rep?",
                  "Who is Puja Srivastava's support rep?"],
        run_examples_on_click=False,
    )
    page.launch(server_name="127.0.0.1", server_port=PORT, quiet=True)
