# Bonus 04 — Instructor notes

Weight: L. Optional post-course extension. Cut first: the direct LiteLLM cost calculation and the callbacks. Keep the two-layer diagram, raw LiteLLM response, ADK event stream, session state, and exact tool payloads.

## The lesson

LiteLLM and Google ADK solve different layers. LiteLLM translates model requests and normalizes response objects. ADK supplies an agent runtime around the model: tools, runners, sessions, events, callbacks, and state.

The sentence to repeat is:

> LiteLLM adapts the model call; ADK runs the agent; application code owns the policy.

This lab intentionally introduces LiteLLM before ADK. If students first meet it inside `LiteLlm(...)`, the adapter looks like unexplained ceremony and they miss a widely used integration layer.

## Environment boundary

This lab does not use the core `.venv`. From `bonus/04_litellm_google_adk/`, run:

```bash
uv sync --locked
```

In VS Code, choose this interpreter for both notebooks:

```text
bonus/04_litellm_google_adk/.venv/bin/python
```

The exact pins are `google-adk==2.7.1` and `litellm==1.97.0`. The lockfile resolves 101 installed packages and a newer OpenAI SDK than the core course, which is why isolation is mandatory.

LiteLLM versions 1.82.7 and 1.82.8 were compromised on PyPI in March 2026. Do not relax the LiteLLM pin or regenerate the lockfile immediately before class without reviewing the current Google and LiteLLM advisories. If either compromised version was ever installed in an environment that held credentials, follow the advisory and rotate those credentials.

`LITELLM_LOCAL_MODEL_COST_MAP=true` prevents LiteLLM from fetching a mutable price map during import. The notebook still uses the course's reviewed prices from the root `.env` for its estimate.

## Emphasise

- The LiteLLM Python SDK and LiteLLM Proxy are different deployment choices. This lab uses the in-process SDK only.
- A common interface does not make model capabilities, parameters, costs, or behavior identical.
- The provider prefix is routing metadata. OpenAI still performs the inference.
- `reasoning_effort="none"` remains model-specific and must be carried through the adapter.
- ADK's `LlmAgent` defines behavior; `Runner` executes and emits events.
- `InMemorySessionService` is appropriate for learning, not durable recovery.
- `ToolContext` is injected by ADK. The model does not generate it as a tool argument.
- The model emits a function call. The runner and application execute Python.
- The refund rule lives in deterministic code, not in the prompt.
- Callbacks observe a boundary. The session state retains selected values. Events record execution. None is automatically a governed audit store.
- `output_key` writes final text into session state; it does not validate the truth of that text.
- Framework adoption can speed up standard plumbing without surrendering the lower-level mental model taught in the core course.

## Pause

1. At the diagram, ask which layer owns the refund rule. Neither library; application code does.
2. At the three-surface table, distinguish the LiteLLM library from its separately deployed proxy.
3. At the lockfile warning, ask why an exact version is necessary but insufficient.
4. After the direct completion, identify the normalized fields: message, finish reason, and usage.
5. Before ADK, ask what changes about the OpenAI provider. Nothing; ADK receives the same LiteLLM adapter.
6. At `ToolContext`, confirm it is absent from the model-generated argument object.
7. Before running, ask which object persists the conversation. The session service.
8. At the event table, locate the model tool request, application result, and final model response.
9. At the raw payloads, repeat that the model did not run the Python function.
10. At state, distinguish `last_policy_decision` from `last_answer`.
11. At usage, explain why the tool-response event has zero model tokens.
12. In the challenge, require `human_review`; do not accept a fluent approval.

## The cell that matters

Put the two raw objects side by side:

- `FunctionCall`: the model-proposed name and JSON arguments;
- `FunctionResponse`: the result returned after application execution.

That pair connects the no-framework loop from the core course to ADK's runtime without turning the framework into a black box.

## If it breaks

| Symptom | Likely cause |
|---|---|
| `google.adk` or `litellm` import fails | The core kernel is selected. Choose `bonus/04_litellm_google_adk/.venv/bin/python`. |
| `uv sync --locked` says the lock is stale | `pyproject.toml` changed. Restore the reviewed file; do not casually regenerate it before delivery. |
| A LiteLLM warning tries to fetch the remote cost map | `LITELLM_LOCAL_MODEL_COST_MAP` was set after importing LiteLLM. Restart the kernel and run setup first. |
| `OPENAI_API_KEY is missing` | The repository-root `.env` is absent or incomplete. Do not create a second secrets file inside the bonus directory. |
| The OpenAI API rejects `temperature` | Do not add it for this model family. |
| The OpenAI API rejects a token parameter | Keep the direct call's `max_completion_tokens`; ADK maps `max_output_tokens` through its LiteLLM connector. |
| The model answers without calling the tool | Re-run once, then verify the model pin and ADK tool schema. Do not weaken the verification to accept an ungrounded answer. |
| The state lacks `last_policy_decision` | The tool did not run or its `ToolContext` mutation was removed. |
| The state lacks `last_answer` | `output_key="last_answer"` is missing from the agent. |
| Event count changes | Inspect function calls and responses by meaning. Do not assert an exact full event count across framework releases. |
| Tool declarations emit an experimental warning | Expected on the verified ADK pin. Re-check after an ADK upgrade rather than suppressing an unfamiliar warning. |

## Challenge debrief

The expected product invariant is `human_review` for `$725`, regardless of the item's age or opened state. The verifier checks the actual function response and stored session state before checking the prose.

The challenge intentionally creates a new app and session. Reusing the earlier session could make a state assertion pass because of old data rather than correct challenge execution.

## Prep

- Run `uv sync --locked` only inside this bonus directory.
- Confirm the selected notebook interpreter is the bonus `.venv`, not the core `.venv`.
- Run the complete student notebook except the challenge stub and verifier.
- Run the solution and save all outputs.
- Confirm imports do not make a remote cost-map request.
- Confirm the direct LiteLLM call returns a `ModelResponse` with usage.
- Confirm the safe ADK run calls `check_refund_policy` once and records `approve`.
- Confirm the model-generated arguments do not contain `tool_context`.
- Confirm the event stream includes one function call, one function response, and a final response.
- Confirm the solution challenge records `human_review` in both the tool response and session state.
- This lab depends on current model tool use. Re-run both ADK paths after changing `MODEL_DEFAULT`, LiteLLM, or Google ADK.

## Current documentation

- [Google ADK LiteLLM connector](https://adk.dev/agents/models/litellm/)
- [Google ADK Python quickstart](https://adk.dev/get-started/python/)
- [Google ADK events](https://adk.dev/events/)
- [Google ADK sessions and state](https://adk.dev/sessions/)
- [LiteLLM completion inputs](https://docs.litellm.ai/docs/completion/input)
- [LiteLLM completion outputs](https://docs.litellm.ai/docs/completion/output)
