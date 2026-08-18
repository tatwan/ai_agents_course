# Skill: shop

Use this playbook for customer invoices and support reps. The only names you can look up are helena and puja. Use the first name, lowercase.

## Tools

- `lookup_count(who)` — how many invoices that customer has
- `lookup_rep(who)` — support representative name

Do not invent a number or a name. Read the observation. Then answer.

## When to load this skill

- "How many invoices does Helena have?"
- "Who is Puja's support rep?"
- Any question about the tiny shop from module 01: count, spend, or the human on the account

Do not load this skill for flights or city facts. That is travel.

## How to work a shop question

1. Confirm the customer is helena or puja. If the user used a full name (Helena Holý, Puja Srivastava), still pass `helena` or `puja`.
2. Call the tool that matches the question. Count is `lookup_count`. Rep is `lookup_rep`. Do not call both unless the user asked for both.
3. Copy the observation into the answer. Do not round, guess, or swap Helena with Puja.

Worked pattern:

```
Question: How many invoices does Helena have?
Tool: lookup_count(who="helena")
Observation: a number
Answer: that number, in a short sentence
```

## Facts you must not invent

Helena and Puja are real rows from the Chinook music shop. The tools know the numbers. You do not. If a tool says it does not know that customer, say so. Do not reach for a support-rep name from memory.

A guessed CustomerId in a later module would be someone else's invoices. The same rule applies here: the observation is the source, not the prompt.

## What this skill is not

This is not a SQL playbook. You do not write SELECT. You do not open chinook.db. You do not join invoices to employees yourself. Two functions are the hands. If the question needs a flight or a city fact, stop and load travel instead.

## Habits that keep the list cheap

- Load this file once per shop question, not on every turn after you already have the observation.
- Do not paste this playbook back into the next user message.
- If the conversation moves from Helena's count to a Madrid fact, you are now on travel. Do not keep shop habits running.

## Compact, then shop

If the list is already long and the user asks a new shop question, load compact first, keep the facts you already have, then use `lookup_count` or `lookup_rep` again only if the summary lost the number.

## Refusal

If the user asks you to look up a third customer, say the shop tools only know helena and puja. Do not invent a third row.
