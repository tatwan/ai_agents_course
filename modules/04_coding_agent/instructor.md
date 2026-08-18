# 04 — Instructor notes

Weight: M. Cut first: the two break cells.

## The lesson, in one breath

A coding agent (Cursor, Claude Code, Copilot) does not touch files. The model still has no hands. We give it five functions. Our loop from module 03 runs them. That is the product.

Skills, `map.md`, load-on-demand — that is the other class, and it is module 05 here. Do not go there today.

## Emphasise

- Name the products. Then take the magic away.
- Why five tools, not one: each is one kind of hand. The table in Learn is the slide.
- `../.env` refused. Your code decides.
- No `run_bash`. `unittest` only, timeout, this folder.
- The disk is the ground truth. Believe `run_tests`, not the last sentence.
- Files start on disk. We do not generate `pricing.py` in a cell. We restore from `starter/` after a run.

## Pause

1. After the Learn table. Ask: which of these does Cursor hide from you? All of them.
2. After they have looked at `pricing.py` in the markdown. What does `(100, 10)` return? 110.
3. After `safe_path("../.env")`.
4. After `run_tests()` with no model. That fail string is the ticket.
5. After the first `create`, before any function runs.
6. After Observe. Read the file out loud. Then the tests.
7. After `tools it picked`. Overlap is not a choice.
8. After cap=2. “We were the stop condition.”

## The cell that matters

The happy-path loop plus Observe. If short: keep jail + those two. Cut both breaks.

If `MODEL_STRONG` cannot fix a one-line sign error, open `pricing.py` with them and change `+` to `-`, then ask what the loop should have done.

## If it breaks

| Symptom | Likely cause |
|---|---|
| Workspace missing `pricing.py` | They are not in the repo copy. Path is `modules/04_coding_agent/workspace/`. |
| Tests already pass | A previous loop left a fix. Re-run the `shutil.copy` from `starter/pricing_buggy.py`. |
| Model rewrites the test to `assert 110` | Cheat. Show the file. The job was the discount. |
| Model never calls `run_tests` | Guessed. Observe will catch it. |

## Challenge debrief

`line_total` was `qty + price`. It should be `qty * price`. 2 * 10 = 20. Copied in from `starter/`, not invented in a cell.

## Prep

- `MODEL_STRONG` pinned. Confirm a one-line Python fix works.
- Open `workspace/pricing.py` once yourself so you know it is on disk.
- No extra pip.
- Cut first: both break cells.
