# Lab 16: How a coding agent edits files and runs tests

**CPU | API key: `OPENAI_API_KEY` | Practises: agents that act on files and run code (a coding agent, the checks around it and what those checks do not stop)**

## Goal

Build a small coding agent and judge its work by what it leaves on disk. A model cannot open a file: it replies with
text, or with a request for a tool, and our code does the reading, the writing and the test runs. We start with a
to-do list the model cannot see, give it two file tools, and then a bill-splitting function whose test fails. The
agent's first fix looks right and still fails, and the test report our code sends back shows it what the fix
missed. Then we take the same agent to the Chinook music shop's pricing code, with the shop's rules in an
`AGENTS.md` file, a check on every file name, and our own checks of the result. The last part shows what that
check cannot stop: running the tests runs whatever code the model wrote, on your machine.

## What you will learn

- How a model works on files it cannot open: file tools as plain Python functions, described to the model as
  schemas and run by our loop.
- How a test report guides the agent: the failure our code returns tells the model what its first fix missed.
- How to keep file tools inside one folder with a path check (`resolve()` and `is_relative_to()`).
- How coding agents load a project's rules from `AGENTS.md` into their instructions.
- How to judge an agent's change on disk: the patch, your own test run, the tests unchanged, the rules followed.
- Why running the tests runs the model's code, and what a path check does not stop.

## What you will do

One notebook, `16_coding_agent.ipynb`. Parts A to C work on a to-do list and a bill; Parts D to G on the Chinook
shop's code.

**Part A: Ask a model to tidy a file it cannot see.** Copy `practice_start/` to a fresh `workspace/`, read the
to-do list, and ask the model to tidy it with no tools.
**Part B: Give the model two file tools, and watch the file change.** `read_file` and `write_file` as plain
functions, called by hand, their schemas, the agent loop with a turn cap, and the file read back from disk.
**Part C: Fix a failing test, and see how the test report leads to the second fix.** `split_bill` and its test, the tests
run with `subprocess.run`, a `run_tests` tool, and an agent run whose first fix fails by a tiny amount.
**Part D: Keep the file tools inside the workspace with a path check.** The shop's folder, three file names
resolved, `check_path`, and the file tools rewritten to refuse names that leave the workspace, plus `list_files`.
**Part E: Load the shop's rules from AGENTS.md, and fix the pricing bug.** The shop's `AGENTS.md` added to the
system message by our code, and the agent run on `pricing.py`, which adds a discount instead of taking it off.
**Part F: Judge the change by the files on disk, not by the model's reply.** The whole file the model sent beside the same change as
a patch, our own test run, the test file against its starting copy, and `CHANGES.md`.
**Part G: See that running the tests runs the model's code.** A `pricing.py` with a four-line probe, written by
us in place of a model: the path check refuses `../../.env`, and the probe finds it anyway.
**Challenge.** The agent on a second project (`challenge_start/`), with its `AGENTS.md` loaded, then left in the
folder and not loaded.
**Going further.** Codex CLI, a real coding agent, on the same folder; approvals; an edit tool that sends only the
change.

![The coding agent: our code builds the system message from our instructions and AGENTS.md; the model replies with the next tool call; our loop runs it; read_file and write_file go through the path check into workspace/; list_files takes no file name; run_tests runs the code in workspace/, and that code can reach the rest of the machine](resources/lab16_coding_agent.png)

## Checkpoints

| After | You should see |
|---|---|
| Part A | three files in `workspace/`; `todo.txt` with eight lines and five tasks; with no tools, a reply that asks you to upload or paste the file |
| Part B | `There is no file named shopping.txt in the workspace.` from the hand call; in the agent's run, `read_file(todo.txt)`, `write_file(todo.txt)` and an answer in three turns; `todo.txt` on disk with five lines, one per task |
| Part C | by hand, `AssertionError: 100 != 25` and `AssertionError: 180.89999999999998 != 20.1`; in the agent's run, a first write of `total / people`, `AssertionError: 20.099999999999998 != 20.1`, a second write with `round(..., 2)`, then `OK` (ours: 7 turns) |
| Part D | `pricing.py` allowed; `../../.env` and `/etc/hosts` refused; `list_files` gives `AGENTS.md`, `pricing.py` and `test_pricing.py`; refusal sentences for a read and a write outside |
| Part E | the two rules of `AGENTS.md` at the end of the system message; `AssertionError: 10.989 != 8.99` at the start; the agent fixes `pricing.py`, gets `OK` and writes one line in `CHANGES.md` (ours: 5 turns, rounding in the first write; usually two writes, the first failing with `8.991 != 8.99`) |
| Part F | a patch that replaces `price + price * percent / 100` with `round(price - price * percent / 100, 2)`; `OK` from our own run; `test_pricing.py unchanged: True`; one line in `CHANGES.md` naming `pricing.py` and `apply_discount` |
| Part G | `read_file("../../.env")` refused; the probe prints `.env file at the repository folder: True` and `OPENAI_API_KEY in the environment: True`; the tests still pass |
| Challenge | two failing tests at the start (`2.99 != 1.99`, `2.99 != 1.98`); loaded, `unit_price * quantity`, the tests passing and unchanged and a `CHANGES.md` line; not loaded, the tests pass and `CHANGES.md` may be missing (ours: `AGENTS.md` opened in 1 of 3 runs, `CHANGES.md` written in 0 of 3 runs; how often varies from run to run) |

**About the saved outputs.** They come from `gpt-6-luna` at reasoning effort `none`, the model `models.env` names.
Parts D and G call no model and print the same on every run (Part G's first line says `False` if your key is set
only in your environment, with no `.env` file). In the other parts the model's tool calls, turn counts and wording
vary from run to run: check the shape (two tool calls for the to-do list, a first fix that fails before a second
that rounds, passing tests with the test file unchanged, a `CHANGES.md` line), not the words. In our runs the bill's
first fix failed every time and the shop's first fix failed in 17 of 18, so the saved Part E, which rounded at once,
is the rare case.

## Before you start

- **Lab 00 first.** It checks the environment and that your key reaches the model.
- **Run it locally:** in the repository folder, `uv sync` (or `pip install -r requirements.txt`), put
  `OPENAI_API_KEY` in `.env` (copied from `.env.example`), then open `16_coding_agent.ipynb` in VS Code or
  JupyterLab (`uv run jupyter lab`) with the `.venv` kernel. Run the setup cells first.
- **Reasoning effort:** `REASONING_EFFORT=none` in `models.env`, as shipped. On Chat Completions the model calls
  tools only at that setting.
- **Files it writes:** `16_Coding_Agent/workspace/` (git ignores it). Every part deletes it and copies a start
  folder there again (`practice_start/`, `workspace_start/` or `challenge_start/`), so the starting files stay as
  committed.
- ⚠️ **It runs code a model wrote, on your machine.** `run_tests` runs whatever the agent put in `workspace/`, with
  your permissions; Part G shows what that can reach. Run it on this lab's files only. Lab 17 runs model-written code
  in OpenAI's hosted code interpreter and, as an option, in a Docker container with no network.
- **Cost:** one plain call and three agent runs, 16 short model calls in our run, well under one US cent at the
  prices in `models.env`. Parts D and G call no model.

## Folder contents

| Path | What it is |
|---|---|
| `16_coding_agent.ipynb` | the guided notebook, with saved outputs |
| `practice_start/` | Parts A to C's files: `todo.txt`, `split_bill.py` (it multiplies where it should divide) and `test_split_bill.py` |
| `workspace_start/` | the shop's files, committed with the bug: `pricing.py`, `test_pricing.py` and `AGENTS.md` |
| `challenge_start/` | the Challenge's project: `totals.py`, `test_totals.py` and `AGENTS.md` |
| `resources/lab16_coding_agent.mmd` and `.png` | the coding agent diagram: its mermaid source and the exported image |
| `solved/16_coding_agent_solution.ipynb` | the challenge solved, run with its outputs |

## Resources

- [OpenAI: function calling](https://developers.openai.com/api/docs/guides/function-calling): tool schemas, strict
  mode, tool calls and sending results back
- [OpenAI: the apply_patch tool](https://developers.openai.com/api/docs/guides/tools-apply-patch): edits as
  structured diffs that your code applies
- [AGENTS.md](https://agents.md): the open format for a project's instructions to coding agents
- [Codex: custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md): how
  Codex finds `AGENTS.md` files and adds them to its instructions
- [Codex: sandboxing](https://learn.chatgpt.com/docs/sandboxing): how a coding agent limits the commands it runs,
  test runners included, and how the sandbox and approvals work together
- [Codex: non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode): `codex exec` and its
  `--sandbox` settings
- [Python: `pathlib`](https://docs.python.org/3/library/pathlib.html): `resolve()`, `is_relative_to()` and joining
  paths with `/`
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html): `run()` with `cwd`, `capture_output`,
  `timeout`, and the environment a child process gets
- [Python: floating-point arithmetic](https://docs.python.org/3/tutorial/floatingpoint.html): why `60.30 / 3` is
  not exactly `20.1`
- [Python: `unittest`](https://docs.python.org/3/library/unittest.html) and
  [`difflib`](https://docs.python.org/3/library/difflib.html): test cases, `assertEqual` and `unified_diff`

Next: [Lab 17: How to run model-written code safely](../17_Code_Execution/README.md). Back to [the lab list](../README.md).
