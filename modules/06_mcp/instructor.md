# 06 — Instructor notes

Weight: M. Cut first: keep the framed `tools/list` bytes and one `tools/call`. Skip initialize talk if behind. Always prove `handle` **before** any model.

## The lesson

The tools from 02–05 are trapped in the notebook process. MCP is the open standard for **agent → tool** so the same `get_fact` can live in another process and any host can list it and call it. We are not touring Inspector or npm.

Students will open `server.py` and see more than two functions. Pause on the map in Learn: **two tools**, the rest is plumbing. `handle` is the receptionist (methods), not a third tool.

We show the wire once with `handle` (JSON-RPC, `tools/list`, `tools/call`), then let the official SDK own the process (`MCPServer` + `mcp.run("stdio")`). Say that out loud so they do not think they have to write a socket reader. On stdio we print **Content-Length** because you can count the bytes. The Agents SDK host speaks **newline-delimited JSON**. Same JSON object inside.

## Emphasise

- Host / server / stdio. HTTP is the same JSON on a port. Today stdio.
- `tools/list` is discovery. `handle` returns the two names before any host is involved.
- The wire is JSON-RPC plus an envelope. Print the `Content-Length` bytes. That cell is the demystifier. Mention the one-line form when the SDK host appears.
- `handle` in-process first. No model. Do not hand-roll `Popen`. The official SDK starts the file later.
- The official loop still decides. MCP is the address, not a new religion.
- MCP ≠ A2A. A2A is module 13.
- Descriptions travel on the wire. Plant module 14. Do not demo poisoning today.
- After Observe: the SDK as someone else's host. `MCPServerStdio` + `await Runner.run` + a named `trace` + `draw_graph` (grey box = `server.py`). Two minutes. Not a second MCP lecture.

## Pause

0. After the `subtract` JSON-RPC example. Ask: which field is the function name? (`method`) Which field matches the reply? (`id`)
0b. After "How MCP uses it." MCP is not a new envelope. It is JSON-RPC with named methods. We print a length header. The official host speaks one JSON line. Same object inside.
0c. After the `server.py` map. "How many tools?" Wait until someone says two.
1. After in-process `get_fact("Amsterdam")`. Same function as 02.
2. After `handle` `tools/list`. Ask: who owns those names now?
3. After the framed bytes. “That is MCP.” Last hand-rolled envelope.
4. Observe: function and `handle`, same Amsterdam string.
5. After the SDK cell. Project the traces URL: MCP tool spans, not a local `function_tool`. Then `draw_graph`: yellow box, grey server. Ask: who listed the tools? The SDK. Who ran `get_fact`? Still `server.py`.

## The cell that matters

Framed `tools/list` plus one `handle` `tools/call`. If short: those two, then the SDK host. The SDK host is the portability claim in one cell.

## If it breaks

| Symptom | Likely cause |
|---|---|
| `import server` runs the loop | They executed the file instead of importing. Check `if __name__`. |
| Amsterdam text differs | They pointed at a different CSV. `ROOT` must see `data/`. |
| Agent invents Istanbul | It never emitted `tool_calls`. Same override as 02, once. |
| SDK cell fails to start the server | `MCPServerStdio` cannot find `server.py` or `mcp` is missing. Run `uv sync` from the repo root. Restart the kernel if a previous hung host is still around. |
| `Request 'initialize' timed out` | Official host is speaking stdio and `server.py` did not start `mcp.run("stdio")`. Confirm `__main__`. Restart the kernel. |
| `from agents.mcp import MCPServerStdio` fails | `uv sync` from the repo root. |
| `draw_graph` errors | Missing system `dot`. Use the traces URL. |

## Challenge debrief

`n_tools` is 2. Sydney → Madrid is **249.66 dollars, 99 minutes**. In-process `handle` is the intended solution.

## Prep

- `uv sync` already pulls `openai-agents[viz]`. System `graphviz` (`dot`) is optional.
- No extra pip in the notebook. stdlib plus the course `openai` / `dotenv` / `agents`.
- Open `server.py` once. It is short. Students should too.
- Run `handle` for `tools/list` and `get_fact` Amsterdam before class.
- Optional: spawn the server from a terminal (`uv run python modules/06_mcp/server.py`) so you have seen it block on stdin.
- Cut first: extra framing talk. Keep `handle` and the SDK host.
