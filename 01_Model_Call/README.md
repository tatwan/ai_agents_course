# Lab 01: How to call a model and read the response

**CPU | API key: `OPENAI_API_KEY` | Practises: how an agent works from the inside (the model writes text; our code
holds the conversation), and what each call costs**

## Goal

Send one message list to the Chat Completions API, read every field of the response, and turn its usage into
dollars. Two moments teach it. A call that finishes without any error can hand back half a sentence, and only
`finish_reason: "length"` says so. And a second call has forgotten the order number we gave the first one, until our
code sends the history itself.

## What you will learn

- How to build a message list with `system` and `user` roles and send it with `client.chat.completions.create`.
- How to read a `ChatCompletion` field by field (`choices`, `message`, `finish_reason`, `usage`) and say what each
  field is for.
- What a token is, and how to price a call from `models.env`, including cached input and cache writes.
- Why the API keeps no memory between calls, and how sending the history makes a conversation.
- How to stream a reply and read its usage from the last chunk.
- How the same call looks on the Responses API, and why these labs start on Chat Completions.

## Coming from

Lab 00 set up the environment and showed the config cell every lab starts with. You need a little Python; no earlier
use of the OpenAI API is assumed. This lab is the first rung of the agent: one call, with no memory and no tools.

## What you will do

**Part A: Send a message list and read the response.** Build a two-message list for the Chinook shop's support desk,
send it, print the whole `ChatCompletion` and read it field by field.
**Part B: Read why a call stopped.** Cap the reply at 20 tokens and see `finish_reason` turn to `length` with no error;
see reasoning take the whole budget at effort `low` when reasoning is enabled; read the 400 the API returns for a tool at effort `low`.
**Part C: Price a call from its usage.** Count tokens on three short messages, read the four prices in `models.env`,
substitute this run's numbers in the price formula, then scale to 100,000 calls and keep the formula in `price()`.
**Part D: Keep a conversation by sending the history.** Give the model Helena's order number, ask for it in a new
call, then send the whole history and compare the answers and the prompt tokens.
**Part E: Stream a reply.** Look at one chunk, collect the stream piece by piece, then ask for the usage on the last
chunk.
**Part F: Make the same call on the Responses API.** The same question with `client.responses.create`, its output
items, the field names side by side, and Part D's conversation with `previous_response_id`.
**Challenge.** Price a streamed turn of the conversation, and keep a two-turn conversation within a 180-token budget.

![Two calls: our code sends the whole list each time; the API keeps nothing between them](resources/lab01_message_list.png)

## Checkpoints

| After | You should see |
|---|---|
| Part A | `finish_reason` `stop`; 36 prompt tokens and about 25 to 50 completion tokens (ours: 28); `reasoning_tokens` 0; `tool_calls` `None` |
| Part B | at 20 tokens, `length` and half a sentence; at effort `low`, an empty reply with 20 reasoning tokens; with a tool at `low`, a 400 whose message names `/v1/responses` |
| Part C | "Hello" is 7 prompt tokens; the Part A call costs $0.0000176 and 100,000 of them $1.76 |
| Part D | the new call does not know the order number; with the history it answers 46, with about 110 prompt tokens instead of 36 (ours: 109) |
| Part E | the first chunk has a `delta` with role `assistant`; a plain stream has no usage; with `include_usage` the last chunk has empty `choices` and the usage (36 prompt tokens) |
| Part F | `output_text` with 36 input tokens and one `message` item; with `previous_response_id`, turn 2 answers 46 and is billed about as many input tokens as Part D's history (ours: 111) |

**About the saved outputs.** The saved outputs come from `gpt-6-luna` at reasoning effort `none`, the model in
`models.env`. Replies and token counts change a little from run to run, and more if `models.env` names another model:
check the shape of each result (`stop` or `length`, 46 or not, which call has more prompt tokens), not the wording.

## Before you start

- **Lab 00 first.** It checks that the environment is installed and that your key reaches the model.
- **Open the notebook** `01_model_call.ipynb` in VS Code or JupyterLab (`uv run jupyter lab`) and choose the
  repository's `.venv` kernel.
- **Data:** none. The questions are written in the notebook; the shop is the same Chinook support desk as in the
  other labs.
- **Cost:** about twenty short calls, well under one US cent at the prices in `models.env`.

## Folder contents

| Path | What it is |
|---|---|
| `01_model_call.ipynb` | The guided notebook, with saved outputs |
| `resources/lab01_message_list.mmd`, `.png` | The two-call diagram: its mermaid source and the exported picture |
| `solved/01_model_call_solution.ipynb` | The challenge, solved and run |

## Resources

- [OpenAI: Chat Completions API reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create): every argument of `create`, including `max_completion_tokens`, `reasoning_effort` and `stream_options`
- [OpenAI: text generation](https://developers.openai.com/api/docs/guides/text): messages, roles and instructions
- [OpenAI: reasoning models](https://developers.openai.com/api/docs/guides/reasoning): reasoning effort, reasoning tokens and the output budget
- [OpenAI: prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching): the 1,024-token minimum, cached input and cache writes
- [OpenAI: pricing](https://developers.openai.com/api/docs/pricing): the prices `models.env` copies
- [OpenAI: conversation state](https://developers.openai.com/api/docs/guides/conversation-state): sending the history yourself, and `previous_response_id`
- [OpenAI: migrate to the Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses): the Chat Completions and Responses fields side by side

Next: [Lab 02: How a model asks for a tool](../02_Tool_Calling/README.md). Back to [the lab list](../README.md).
