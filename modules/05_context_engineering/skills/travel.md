# Skill: travel

Use this playbook for flights between cities and fun facts about a city. City names as the user wrote them (Amsterdam, Madrid, Istanbul, Dubai, Amman).

## Tools

- `get_flight(from_city, to_city)` — price in dollars and duration in minutes
- `get_fact(city)` — one fun fact from the local file

If a flight is missing, say so. Do not invent a price. If a city has no fact, say so. Do not invent a landmark.

## When to load this skill

- "Give me a fun fact about Amsterdam."
- "What does a flight from Sydney to Madrid cost?"
- "From Barcelona, is it cheaper to fly to Dubai or to Amman?"

Do not load this skill for invoice counts or support reps. That is shop.

## How to work a fact question

1. Call `get_fact` with the city the user named.
2. Answer with the observation. One sentence is enough.

## How to work a flight question

1. Call `get_flight` with both cities.
2. Read price and minutes from the observation.
3. If the file has more than one row for that pair, report what the tool returned. Do not pick a favourite.

## How to work a comparison

The cheaper city is not known until both flights return. Do not skip a lookup because the destination is written in the question.

1. `get_flight` for the first pair.
2. `get_flight` for the second pair.
3. Compare the prices from the observations, not from memory.
4. If the user also asked for a fact, `get_fact` on the winner only.

Worked pattern:

```
Question: From Barcelona, cheaper to Dubai or Amman, then a fact about the winner.
Tool: get_flight(Barcelona, Dubai)
Tool: get_flight(Barcelona, Amman)
Compare the two prices.
Tool: get_fact on the cheaper city
Answer: the winner, the two prices, the fact
```

Do not add the prices yourself if the user only asked which is cheaper. Do not invent a third leg.

## What this skill is not

This is not a live weather playbook and not a booking system. There is no seat map, no passport, no Open-Meteo. Two functions, a CSV, a fact file. If the user asks who Helena's support rep is, stop and load shop.

## Habits that keep the list cheap

- Load this file once per travel question.
- Do not stuff every city fact you have ever seen into the next turn.
- After you have the observation, answer. Do not reload travel to "be sure."

## Compact, then travel

If the list is already long, load compact, keep the prices and facts you already fetched, and only call a tool again if the summary dropped them.
