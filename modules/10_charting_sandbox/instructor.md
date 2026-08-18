# 10 — Instructor notes

Weight: M. Cut first: the Docker cell if the daemon is down. Keep the jail and the planted `.env` probe.

## The lesson

The model writes matplotlib. Your code starts the process. A timeout plus `cwd=` is not a sandbox — the child can still walk up to `.env`. Docker with one volume and `--network none` is the first real filesystem boundary. We do not pull images in this room.

## Emphasise

- Same Chinook, named queries. USA **523.06** / 91 invoices. Years 2009–2012 **83** each, 2013 **80**.
- You plot first, no model. Then the model writes the same kind of file.
- Pause on the first `run_python` arguments. Read the code out loud before the loop runs it. That is module 02 again.
- The child has no database. If the bars are right, the numbers came from the query observation.
- Print `env_exists`. Never print `.env`.
- `sandbox.py` is the jail they just wrote, extracted so Docker can start a process. Open it. Do not treat it as a black box.

## Pause

1. After the two printed tables. Cover USA and the five years.
2. After the hand plot. That PNG is the product. The rest of the module is where it came from.
3. After `run_jailed("print(2 + 2)")`. Ask: did a model run? No.
4. After the planted snippet. Jail says `env_exists True`. That is the cell that matters.
5. After Docker, if it ran. `False`. Same snippet. Different disk.
6. After the first `create`, before the loop. Read `code` if it asked `run_python`.
7. After the agent PNG. Compare it to the hand plot.
8. Challenge: invoice **count** by year, `invoices_by_year.png`.

## The cell that matters

The planted snippet in the jail. If short: hand plot + jail probe + official loop. Cut Docker.

If nano writes broken matplotlib, rerun the loop cell on `MODEL_STRONG`. This module already prefers `MODEL_STRONG` when it is set.

## If it breaks

| Symptom | Likely cause |
|---|---|
| `import sandbox` fails | Kernel cwd is not the repo, or they skipped the boot cell (`sys.path`). |
| `matplotlib` missing | `uv sync` from the repo root. |
| Agent plot missing | It never called `run_python`, or `savefig` used the wrong name. Print `generated_code`. |
| `savefig` path is absolute | Child cwd is `charts/` but they saved under `/tmp`. Show the code. |
| Docker `Cannot connect` | Daemon down. Skip. Do not start Docker in front of the room. |
| Docker `image missing` | Not pre-pulled. Skip. `docker pull python:3.12-slim` is a VM-image step. |
| Probe says `env_exists False` in the jail | They started Jupyter from `modules/10_charting_sandbox/`. `../../../.env` is then wrong. Use the unconstrained `ROOT / ".env"` line and walk the path on the board. |

## Challenge debrief

`invoices_by_year.png`. Counts: 83, 83, 83, 83, 80. The assert is only "file exists and is not empty."

If they plotted spend instead of count, the file still passes. Say so, then show the counts.

## Prep

- `uv sync` (matplotlib is in `pyproject.toml`).
- `MODEL_STRONG` pinned if you can. Confirm nano or mini will emit `run_python` with `savefig`.
- On the **student VM image**: `docker pull python:3.12-slim` and leave the daemon running. A cold pull across 20 machines will destroy the Docker cell.
- Run the hand plot and the planted snippet once.
- Do not print `.env`.
- Cut first: Docker.
