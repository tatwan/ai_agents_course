# Skill: compact

Use this playbook when the message list has grown and the next turn would pay for old tool dumps again. The job is to keep the facts and drop the traces.

## When to load this skill

- The conversation has more than a handful of turns.
- A tool result was a long file, a playbook, or a repeated schema.
- The user asks to "summarise so far" or "start fresh but keep the numbers."
- You are about to ask a new question and the middle of the list is mostly observations you no longer need verbatim.

Do not compact on the first turn. There is nothing to drop.

## What to keep

Write a short summary with four headings, a few lines each:

- **Goal** — what the user is trying to find out
- **Facts already found** — numbers, names, prices, cities. Copy them exactly.
- **What is still open** — the next tool or the unanswered part
- **What to drop** — playbook text, raw tool dumps, repeated schemas

After this, the next turn should keep the summary and drop the old observations.

## What you must not do

- Do not invent a fact that was not on the list. If Helena's count is gone, say it is gone and look it up again.
- Do not keep the full shop or travel playbook in the summary. That is the whole point of compacting.
- Do not paste raw JSON, schemas, or stack traces into the summary.
- Do not compact so hard that the next model has to guess. A missing number is better than a wrong number, but a kept number is better than both.

## Shape of a good summary

```
Goal: Helena invoice count, then a fact about Amsterdam.
Facts: Helena has 7 invoices. Amsterdam has more bicycles than people.
Still open: none, unless the user asks a follow-up.
Dropped: shop.md, travel.md, the tool traces that produced those two facts.
```

A few lines. No raw tool dumps. The next create() should be cheaper than the last one.

## How this sits next to the map

The map says when to load a playbook. Compact says when to throw a playbook away. They are the same budget, two directions.

If a new question needs shop or travel after you compact, load that one playbook again. Do not reload all four.

## Habits

- Compact once, then continue. Do not compact every turn.
- If the summary is longer than the list it replaced, you failed. Try again with only the facts.
- Forgetting is a valid outcome. Say what you no longer know instead of filling the gap from training.
