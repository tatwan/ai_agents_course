# 07 — Instructor notes

Weight: M. Do not cut the coroutine cell. That is why `await` exists.

## The lesson

Frameworks look like `await` because two independent tools should not take twice as long. We planted sequential dispatch in 02. Today we pay it off. Then 08 can use `Runner.run` without `await` being a mystery.

Walk the primer. Do not jump to `gather`.

## Emphasise

- `def` returns the result. `async def` returns a **coroutine** (a ticket). The body has not run.
- `await` cashes the ticket. Jupyter is the loop. `asyncio.run` is for `.py` files.
- `time.sleep` inside `async def` still blocks. The wait must be `await asyncio.sleep`.
- `gather` takes tickets, not `await pause(...)` results. Clock is the slower one, not the sum.
- Independent vs dependent. Madrid fact + Sydney–Madrid flight: gather. Landing-city fact: still sequential.
- 02 already used `await Runner.run` because Jupyter has a loop. Today you learn why the SDK is async.

## Pause

1. After `greet("Sam")`. A string.
2. After `greet_async("Sam")` **without** `await`. Someone says coroutine / not hello. The warning is the lesson.
3. After `await greet_async`. Same string as step 1.
4. After sequential `pause`. `start a` … `done a` … `start b`. ~2s.
5. After `gather`. Both `start`s first. Results `['a', 'b']`. ~1s. Ask: what if we had written `gather(await pause("a"), await pause("b"))`? Sequential again.
6. After the travel gather. Same numbers on real tools.
7. After the official loop. If `n=2` on turn 1, `dispatch seconds` ~1. If `n=1`, the model chose sequential. Either is a lesson.
8. Challenge: Istanbul + Tokyo–Moscow.

## The cell that matters

The bare `greet_async("Sam")` next to `await greet_async("Sam")`. Then the two travel clocks. If short: keep those, skip the model loop.

## If it breaks

| Symptom | Likely cause |
|---|---|
| `await` SyntaxError | Not in a notebook, or an old kernel. |
| gather ≈ sequential | They used `time.sleep` inside `async def`. Must be `await asyncio.sleep`. |
| Model asks one tool at a time | Fine. Point at it. The gather still ran a list of one. |
| Challenge gather not faster | Sleeps were 0 or they timed the wrong thing. |

## Challenge debrief

Istanbul: two continents. Tokyo–Moscow: 259.3 / 525. The assert is only the clocks.

## Prep

- Same key, same CSVs. No extra pip for this module (`openai-agents` is already in the project for 03 Part 4 / 08).
- Run the bare `greet_async` cell and the two `pause` clocks once so you know `await` works in this Jupyter.
- Cut first: the model loop. Keep the coroutine cell and the travel clocks.
