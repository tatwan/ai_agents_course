# 01 — Instructor notes

Weight: M. Do not skip. This is the vocabulary the rest of the course reuses, and it is how you win the risk half of the room in the first hour.

## Emphasise

- The test is one sentence: **who decides the next step — you, or the model?**
- The workflow cell is the hero, not the live loop. Helena's ticket should stay a script.
- The scripted `plan = [...]` loop is the agent, emptied of mystery. Ordinary Python.
- The live loop is the same loop with the list deleted. Your code still runs the tool. Your code still stops it.
- Autonomy (`suggest` / `draft` / `act`) is a plant for module 17. They reuse those words in the table.

## Pause

1. After the workflow prints `7` and `Steve Johnson`. Ask: is this an agent? Wait until someone says no.
2. After the chatbot. Read the invented number next to the workflow's 7.
3. After the scripted plan. Point at the `for`. That is the whole trick.
4. After the live loop. Trace one `model:` / `saw:` pair out loud.
5. After the call-count cell. The agent spent money to rediscover an order you already knew.
6. Challenge: groups of two or three. They edit the markdown table in the notebook. Five to seven minutes. Then debrief from `solution.ipynb`. If the room is behind, do rows 1, 3, 7 only.

## The cell that matters

The scripted plan, then the call-count compare. If you are short on time, keep those two and cut the live loop. The workflow-versus-chatbot pair still teaches. The live loop is the payoff, not the definition.

If the live model ignores `COUNT` / `REP` and guesses, do not restart it. Read the transcript. That is module 00 again, and it is why 02 and 03 exist.

## If it breaks

| Symptom | Likely cause |
|---|---|
| Chatbot "gets it right" | Luck. The functions were never called. Say that. |
| Live loop prints `unknown action` | The model wrote a sentence. Point at the system message. One more turn often recovers. |
| Live loop `DONE` on turn 1 with a made-up number | Same as the chatbot. Cap already saved you. |
| `helena` / `puja` KeyError | The parse picked up a word that is not a key. The `who in SHOP` guard should prevent this; if you edited it away, put it back. |

## Challenge debrief

No scoring cell. The table is empty on purpose. Open `solution.ipynb` and walk the rows. Do not read every cell if time is short — land on 7 and 8.

- **1, 4, 5** — workflow, `act`. Steps fit on a slide.
- **2** — chatbot. Talking is the job.
- **3, 6** — agent. Next step depends on what they find. Keep 6 on `suggest`.
- **7** — looks like an agent, must not `act`. A wrong $5,000 refund is the risk sentence. `draft`, or a small rules workflow.
- **8** — let the room split. Classifier plus queues is a workflow. The leftovers that do not fit are an agent.

If someone wants a long `if` tree for row 3, ask how they will write the tree before they have seen the email.

## Prep

- Same class key as module 00.
- Confirm Helena is 7 invoices, Steve Johnson, and Puja is 6 invoices, Jane Peacock. Those are sqlitetutorial facts; do not invent new ones.
- Run the live loop once before class. If nano stops emitting `COUNT` / `REP`, tighten the system message that morning. Do not rewrite twenty later notebooks.
- Cut first: shrink the table to rows 1, 3, 7. If the API is down, skip chatbot + live and keep workflow + scripted plan + the table.
