"""A shopping list as an MCP server, run over stdio.

A host starts this file as its own process:
    python 06_MCP/shopping_server.py
It then reads JSON-RPC messages from stdin and writes its replies to stdout, one per line.
"""

from pathlib import Path

from mcp.server import MCPServer

# The list is a text file in outputs/ beside this file, one item per line
LIST_FILE = Path(__file__).resolve().parent / "outputs" / "shopping_list.txt"

mcp = MCPServer("shopping")


@mcp.tool()
def add_item(item: str) -> str:
    """Add one item to the shopping list."""
    LIST_FILE.parent.mkdir(exist_ok=True)
    with open(LIST_FILE, "a", encoding="utf-8") as file:
        file.write(item + "\n")
    return f"Added {item}."


@mcp.tool()
def list_items() -> list[str]:
    """List every item on the shopping list, in the order they were added."""
    if not LIST_FILE.exists():
        return []
    return LIST_FILE.read_text(encoding="utf-8").splitlines()


if __name__ == "__main__":
    mcp.run("stdio")
