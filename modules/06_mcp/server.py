"""Travel tools as a local MCP stdio server.

Two tools: get_fact, get_flight. handle() is the in-process receptionist
the notebook calls first (no subprocess, no model). __main__ hands the
same functions to the official MCP SDK.
"""

from __future__ import annotations

import csv
from pathlib import Path

from mcp.server.mcpserver import MCPServer

ROOT = Path(__file__).resolve().parents[2]
FACTS = list(csv.DictReader(open(ROOT / "data" / "fun_facts.csv")))
FLIGHTS = list(csv.DictReader(open(ROOT / "data" / "flight_data.csv")))

mcp = MCPServer(name="travel")


@mcp.tool()
def get_fact(city: str) -> str:
    """Fun fact about a city."""
    needle = city.strip().lower()
    for row in FACTS:
        if row["City"].lower() == needle:
            return row["Fun Fact"]
    return "no fact for that city"


@mcp.tool()
def get_flight(from_city: str, to_city: str) -> str:
    """Flight price and duration between two cities."""
    a = from_city.strip().lower()
    b = to_city.strip().lower()
    found = []
    for row in FLIGHTS:
        if row["from_city"].lower() == a and row["to_city"].lower() == b:
            found.append(row["price"] + " dollars, " + row["duration"] + " minutes")
    return "; ".join(found) if found else "no flight found"


TOOLS = [
    {
        "name": "get_fact",
        "description": "Fun fact about a city.",
        "inputSchema": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
    {
        "name": "get_flight",
        "description": "Flight price and duration between two cities.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "from_city": {"type": "string"},
                "to_city": {"type": "string"},
            },
            "required": ["from_city", "to_city"],
        },
    },
]


def handle(req: dict) -> dict | None:
    """Receptionist: incoming method -> list, call, or hello. Not a tool."""
    method = req.get("method", "")
    req_id = req.get("id")
    params = req.get("params") or {}

    if method.startswith("notifications/"):
        return None

    if method == "initialize":
        result = {
            "protocolVersion": params.get("protocolVersion") or "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "travel", "version": "0.1"},
        }
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        name = params.get("name", "")
        args = params.get("arguments") or {}
        if name == "get_fact":
            text = get_fact(str(args.get("city", "")))
        elif name == "get_flight":
            text = get_flight(str(args.get("from_city", "")), str(args.get("to_city", "")))
        else:
            text = "unknown tool"
        result = {"content": [{"type": "text", "text": text}]}
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": "method not found: " + method},
        }

    return {"jsonrpc": "2.0", "id": req_id, "result": result}


if __name__ == "__main__":
    mcp.run("stdio")
