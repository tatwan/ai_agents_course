# 05 — Instructor notes

Weight: M. Cut first: compaction. Keep the fat vs thin first request.

## The lesson

The list is a budget. Coding agents (and enterprise pilots) die when every playbook rides along on every turn. Progressive disclosure: a short map, load one skill when asked. Compaction: when the list has already grown, keep the facts, drop the dumps.

This is the `map.md` / skill-file idea from the other coding-agent class, stripped to what we can measure in one hour.

## Emphasise

- Seven inputs, one window. Retrieval will want a seat later. Isolation is context, not an org chart.
- Open the four markdown files in the editor. They are short. We did not generate them in a cell.
- The cell that matters is **fat vs thin `prompt_tokens`** on the first `create`. Same question: Helena's invoice count.
- Fat often asks `read_skill` for a playbook it is already carrying. Thin often goes straight to `lookup_count`. Stuffing the context costs more **and** can make the model behave worse. Both can still get 7.
- Thoughts and playbooks are tokens. Same `usage` as module 00.
- Compaction can forget. That is the other failure mode. Say it.

## Pause

1. After `map chars` vs `all playbooks chars`. The ratio is the slide.
2. After fat vs thin `prompt_tokens`. Read `saved` out loud. Times a company day.
3. After `fat asked` / `thin asked` on the first create. Point at fat requesting `read_skill` and thin going to `lookup_count`. That inversion is the lesson.
4. After compact: still 7? The summary carried the fact. Forgot? The compact was too thin.
5. Challenge: Amsterdam fact, same measurement. Thin must be smaller.

## The cell that matters

Fat vs thin first request. If short: keep that and the thin loop. Cut compaction.

If thin never calls `read_skill` and still asks `lookup_count`, that is the map doing its job — do not "correct" it toward a load. If fat asks `read_skill`, that is stuffing making it worse. The token save still landed either way.

## If it breaks

| Symptom | Likely cause |
|---|---|
| `unknown skill` | Name not in `{map, shop, travel, compact}`. |
| Thin `prompt_tokens` not smaller | Fat and thin accidentally the same string. Print `len(FAT_SYSTEM)`. |
| Thin never loads shop, invents 7 | Guess. Still count tokens. Then show a forced `read_skill` if you want the load on screen. |
| Compact answer is not 7 | Summary dropped the number. That is the lesson, not a broken cell. |

## Challenge debrief

Amsterdam fact is *more bicycles than people*. You do not need it for the assert. The assert is only `thin_tokens < fat_tokens`.

If someone finished the thin loop and also bound the tokens, good. The measurement was the job.

## Prep

- Same key. Same two CSVs. Skill files committed under `skills/`.
- Helena is 7. Puja is 6, Jane Peacock.
- Run the fat/thin cell once so you know `saved` is obviously positive.
- Cut first: compaction.
