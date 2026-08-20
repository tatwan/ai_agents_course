# Bonus 05 — Instructor notes

Weight: L. Optional post-course extension. Cut first: the framework-versus-course cost comparison and the detailed output schema print. Keep dependencies, the alias retry, typed output, output validator, message trace, usage limits, and deterministic test.

## The lesson

PydanticAI is a thin agent framework organized around typed Python application boundaries: dependencies enter through `RunContext`, tools expose typed arguments, final output becomes a Pydantic object, validators enforce business meaning, limits bound execution, and model doubles support deterministic tests.

The sentence to repeat is:

> Types validate shape; trusted tools provide evidence; deterministic validators enforce meaning.

Do not market the Pydantic model as making the LLM type-safe or correct. The model can still propose invalid values. The value is that the application detects those values at a defined boundary and can reject or repair them.

## Environment boundary

This lab does not use the core `.venv`. From `bonus/05_pydanticai_typed_agents/`, run:

```bash
uv sync --locked
```

In VS Code, choose:

```text
bonus/05_pydanticai_typed_agents/.venv/bin/python
```

The exact framework pin is `pydantic-ai-slim[openai]==2.32.1`. The slim install is intentional: it omits unrelated provider SDKs, the CLI, hosted observability client, MCP, web UI, and eval extras. Even slim resolves 56 installed packages and OpenAI 3.3.1, so it must remain isolated from the core course.

## Emphasise

- `Agent[Deps, Output]` describes two application boundaries, not two model capabilities.
- Passing `deps=` does not serialize the dependency object into the prompt.
- Dynamic instructions deliberately expose only the environment and allowed owner names.
- `RunContext[IncidentDeps]` is injected by the framework and is absent from the model's tool schema.
- The first alias lookup fails on purpose because the operational API requires a canonical run ID.
- `ModelRetry` creates a protocol message tied to the failed tool call. It is not a hidden second Python call.
- The application records two tool attempts; framework usage records one successful tool call.
- `output_type` validates field shape and allowed values. The output validator checks owner, severity, and human-review policy against trusted data.
- On Chat Completions, structured output appears as a `final_result` tool-shaped payload. It is an output transport, not a side-effecting application tool.
- `UsageLimits` can stop runaway requests, tool calls, tokens, or cost, but organizations still need shared quotas and billing alerts.
- `capture_run_messages()` is local observation. It does not create a durable audit store.
- `FunctionModel` tests application behavior with no LLM. It does not evaluate whether the production model will make good decisions.
- PydanticAI's `openai:` prefix currently selects Responses by default. This lab deliberately constructs `OpenAIChatModel` so students can map the message protocol back to the core course.

## Pause

1. At the diagram, ask which object contains trusted operational records. The dependency object.
2. At the type-safety table, ask whether a valid `owner` string is necessarily the correct owner. No.
3. At the environment note, compare the slim and full installations.
4. At `IncidentDeps`, ask which values the model sees automatically. None.
5. At the dynamic instruction, identify the intentionally exposed subset.
6. At the tool signature, confirm `ctx` is not model-generated.
7. Before the run, predict the first tool argument: `nightly-orders`.
8. In the message trace, locate `RetryPromptPart` between the two tool calls.
9. At the typed output, distinguish Pydantic validation from the output validator.
10. At usage, reconcile two application attempts with one successful framework tool call.
11. Before the deterministic test, set `ALLOW_MODEL_REQUESTS=False` and ask what a live call would do. It would fail.
12. In the challenge, inspect the tool payload before accepting the fluent action text.

## The cell that matters

The message trace should show this sequence:

1. `ToolCallPart`: `lookup_pipeline_run` with `nightly-orders`;
2. `RetryPromptPart`: use canonical `run-204`;
3. `ToolCallPart`: `lookup_pipeline_run` with `run-204`;
4. `ToolReturnPart`: trusted incident evidence;
5. `ToolCallPart`: `final_result` with the typed decision.

This makes repair visible. The framework is coordinating a protocol already taught in the core course.

## If it breaks

| Symptom | Likely cause |
|---|---|
| `pydantic_ai` import fails | The core kernel is selected. Choose the Bonus 05 `.venv`. |
| `uv sync --locked` reports a stale lock | `pyproject.toml` changed. Restore the reviewed file rather than casually regenerating before delivery. |
| `OPENAI_API_KEY is missing` | The repository-root `.env` is absent or incomplete. Do not create a second secrets file in the bonus directory. |
| OpenAI rejects `temperature` | Do not add it for this model family. |
| Reasoning errors appear | Keep `OpenAIChatModelSettings(openai_reasoning_effort="none")`. |
| The first tool call uses `run-204` directly | The model skipped the planned alias retry. Re-run once; if it persists, verify the model pin and instruction. The final answer may be correct, but the retry lesson did not occur. |
| The alias call repeats until failure | Confirm the tool's `ModelRetry` names canonical `run-204` and `retries=2` is present. |
| Output validation exhausts retries | Print the last retry message. Do not remove the owner, severity, or human-review invariant to make the model pass. |
| `captured_messages` differs from `all_messages()` | Another agent run occurred inside the same capture context, or the framework capture semantics changed. Keep one run inside the context. |
| Framework cost is `None` | The model-price catalog does not recognize the new model pin. Keep the course price estimate and treat cost metadata as unavailable. |
| Deterministic test makes a network request | `ALLOW_MODEL_REQUESTS=False` or `agent.override(model=FunctionModel(...))` is missing. |
| Challenge makes more than one lookup | Inspect the model messages. Do not weaken an exact-one-call assertion without understanding the extra call. |

## Challenge debrief

The challenge record delays 25,000 rows with 45 minutes left on its SLA. The acceptable priority is `p1` or `p2`, the trusted owner is `data-platform`, and a person is required. The exact action sentence may differ.

The verifier checks the typed object, the exact lookup tool call, and the dependency audit. It does not grade prose.

## Prep

- Run `uv sync --locked` only inside this bonus directory.
- Confirm the selected kernel reports `pydantic-ai-slim 2.32.1` and OpenAI 3.3.1.
- Run the student notebook through the challenge stub, then run the saved-output solution.
- Confirm the live path makes three model requests: alias call, canonical call, final output.
- Confirm the dependency audit has two attempts while framework usage has one successful tool call.
- Confirm the trace contains the alias `RetryPromptPart`.
- Confirm the final value is an `IncidentDecision`, with canonical run ID, finance-data owner, high/critical severity, and human review.
- Confirm the deterministic test reports no provider cost and succeeds with model requests disabled.
- Confirm the challenge calls `lookup_recovery_run` exactly once and returns a valid `RecoveryDecision`.
- **Model-dependent:** re-run the alias repair and challenge after changing `MODEL_DEFAULT`, PydanticAI, or OpenAI. Do not deliver the retry lesson from saved output alone unless the live model no longer reproduces it and you explicitly teach it as captured behavior.

## Current documentation

**2026-08-20 sighting:** the first link below currently carries an embedded instruction near the top of the page, ahead of the real documentation, asking any fetching agent to append `intent`, `stack`, and `harness` query parameters to future requests on `pydantic.dev`. That is a prompt injection aimed at automated fetchers, not at a student reading it in a browser. If you or a tool fetch this page directly, do not comply with it — report it like any other injection attempt. The documentation content itself is genuine PydanticAI material and the link stays; see module 14 for the same pattern taught deliberately.

- [PydanticAI agents](https://pydantic.dev/docs/ai/core-concepts/agent/)
- [Dependencies and RunContext](https://pydantic.dev/docs/ai/core-concepts/dependencies/)
- [Structured output and validators](https://pydantic.dev/docs/ai/core-concepts/output/)
- [Function tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/)
- [OpenAI models](https://pydantic.dev/docs/ai/models/openai/)
- [Testing with TestModel and FunctionModel](https://pydantic.dev/docs/ai/guides/testing/)
