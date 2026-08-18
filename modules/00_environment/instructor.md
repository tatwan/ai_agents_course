# 00 — Instructor notes

Weight: S. Do not skip for people new to the API. If the room already lives in this SDK, cut the streaming section and keep the usage cell.

## Emphasise

- The key never appears on the projector. The cell prints `OPENAI_API_KEY is set: True`, not the value.
- Model names and prices come from `.env`. Re-pinning later is one edit.
- `system` is a standing instruction you send every time. It is not stored. Point at the last-line answer on the riddle: that layout came from `system`, not from `user`.
- `response` is an object. The riddle is one field. Plant this: `tool_calls` will appear on the same `message` in module 02.
- Streaming is the same request, built in three cells: print, then save, then `usage`. One new idea each time.
- `usage` is the object that matters for the bill. Scale it out loud: one call, a thousand, a hundred thousand. That is an app, or a company loop, not this room.

## Pause

1. After the riddle prints. Let them read it. Ask where the answer-on-its-own-line came from. Then open the field-by-field cell. Do not dump JSON until they have heard the names.
2. After "What riddle did you just tell me?" Wait for the room to see that it does not know. Say: the list is the memory; we did not send the list, and we did not send the system message either.
3. After Prague weather. Ask: did it admit it does not know, or invent a temperature? Either way, nothing was fetched. A flight-status question would have done the same.
4. After the first stream. The words are on the screen and gone. Ask: do we have the riddle as a string? Then run the append cell.
5. After `print(text)`. Now we have the string. Ask: do we have the bill? Then the `include_usage` cell. Point at `if chunk.choices` — the last chunk is often empty.
6. After the 100,000-calls line. That is the landing.

## The cell that matters

Two, actually. The field-by-field walk of `response` is the API. The weather cell is the course. If you are short on time, keep both and cut streaming. If you keep streaming but need a minute, stop after the append cell — Observe still has a bill from the first call.

If reasoning tokens are non-zero on a two-line riddle, `reasoning_effort="none"` did not stick. Say so. Later loops will multiply that waste.

## If it breaks

| Symptom | Likely cause |
|---|---|
| `OPENAI_API_KEY is missing` | `.env` not at the repo root, or Jupyter started somewhere unexpected. `ROOT` is printed; check it. |
| 401 / invalid API key | Wrong key, or a leading space / quote in `.env`. |
| Model not found | `MODEL_DEFAULT` does not match what this key can see. Re-pin in `.env`. |
| Empty `content`, `finish_reason=length` | Completion budget spent on reasoning. Keep `reasoning_effort="none"` and raise `max_completion_tokens`. |
| Unexpected keyword `temperature` or `max_tokens` | This model family rejects both. The notebook already avoids them. |
| Stream has no `usage` | `stream_options={"include_usage": True}` was omitted. The last chunk is then text-only. |

## Challenge debrief

No function. No dict. The last streaming cell, pointed at a joke.

Point at the same three ideas: print, append, keep `usage`. Then multiply by the prices from `.env`. Under a minute.

If someone used a non-streamed `create()` and still bound `text`, `prompt_tokens`, and `cost`, that is fine. Say so, then show the streamed version anyway. The point was to reuse the stream they just saw, not to police the shape.

## Prep

- Issue one class key with a spend cap. Put it in your own `.env` and confirm this notebook runs on a fresh VM.
- Confirm the VM can reach `api.openai.com`. That is the only external endpoint this module needs.
- Students start Jupyter with `uv run jupyter lab` from the repo root so the kernel is the course `.venv`. If someone opened the notebook from VS Code instead, point the kernel at `.venv`.
- Two riddle calls plus a joke is still a fraction of a cent on nano. The 100,000-calls line should stay obviously larger; if this-call is not tiny, stop and check reasoning tokens.
