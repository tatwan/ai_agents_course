# Bonus 03 — Instructor notes

Weight: L. Optional post-course extension. Cut first: the hosted trace URL and cost arithmetic. Keep local context, the two guardrail boundaries, and the lifecycle event list.

## The lesson

The OpenAI Agents SDK is more than `Agent` plus `Runner`. Its production value is a set of standard control surfaces around the loop: local context, typed results, guardrails, lifecycle hooks, tracing, and aggregated usage.

The sentence to repeat is:

> Input controls can prevent work; output controls can only contain work that already happened.

Module 08 already teaches sessions, agents-as-tools, handoffs, graph drawing, and basic traces. Do not reteach those topics here.

## Emphasise

- Conversation context is what the model sees. Run context is what application code sees.
- Local context is not magical secrecy. Dynamic instructions or tools can deliberately expose values from it.
- The model sees only `category` in the tool schema. `RunContextWrapper` is supplied locally.
- `output_type` validates structure. The deterministic output guardrail validates one policy invariant.
- `run_in_parallel=False` is an intentional privacy and cost choice. The default parallel mode may start agent work before a tripwire fires.
- An output guardrail runs after model calls. Its tripwire prevents release, not billing.
- Hooks observe lifecycle events. They do not replace authorization, durable business records, or trace retention policy.
- `trace_include_sensitive_data=False` protects payload content, but trace metadata and access still need governance.
- Usage belongs to the result’s context wrapper and aggregates every model request in the run.
- Agent-level guardrails have workflow boundaries. Side-effecting tools need tool-level validation or approval where the action occurs.

## Pause

1. At the diagram, ask which branch can have zero model cost.
2. At `ExpenseContext`, ask which fields the model receives automatically. None.
3. At the tool schema, verify that `employee_id` and the approval limit are absent.
4. At the input guardrail, compare sequential and parallel execution.
5. At the output guardrail, ask whether it can recover tokens already spent. No.
6. At dynamic instructions, identify the one context value deliberately exposed: the approval limit.
7. After the safe run, confirm `final_output` is an `ExpenseDecision`, not a JSON string.
8. In the event list, find two `llm:start` entries around the policy tool.
9. At the usage ledger, count requests before counting tokens.
10. At the blocked input, confirm the event list contains only the input guardrail.
11. In the challenge, accept either a correct `review` or a contained unsafe approval. Never accept a released approval.

## The cell that matters

Put these two event lists side by side:

- safe run: guardrail, agent, model, tool, model, final guardrail;
- blocked run: `['guard:input:blocked']`.

That is concrete evidence that boundary placement changes privacy, execution, latency, and cost.

## If it breaks

| Symptom | Likely cause |
|---|---|
| `from agents import ...` fails | Run `uv sync` from the repository root. No new package is needed. |
| `.env` is not found | Open the notebook inside this repository. The setup cell searches upward for `pyproject.toml`. |
| Tool schema includes context fields | The first parameter lost its `RunContextWrapper[ExpenseContext]` annotation. |
| Sensitive example still calls the model | The input guardrail is missing `run_in_parallel=False`, is not attached to the agent, or the regex did not match. |
| Safe result is plain text | `output_type=ExpenseDecision` is missing. |
| Safe run raises output tripwire | Inspect the typed result. The model attempted an over-limit approval or extracted the wrong amount. Do not disable the guardrail. |
| Hook order differs slightly | Some callback timing may change by SDK version. Preserve the boundary assertions, not a brittle full-list equality for model runs. |
| Trace has no payloads | Expected: `trace_include_sensitive_data=False`. The workflow shape should still be useful. |
| Usage shows more than two requests | The model took extra turns. Keep the result if correct, but discuss the cost. |
| Challenge returns `blocked_unsafe_output` | Valid containment path. Show the output guardrail information rather than forcing the model to behave. |

## Challenge debrief

The preferred result is a typed travel decision for `$650` with `recommendation='review'`. On the verified pin, the run makes two requests and calls `lookup_policy` once.

The alternative safe outcome is `OutputGuardrailTripwireTriggered`: the model attempted to approve above the `$200` limit, but the application did not release it. The verification accepts both because the product invariant is containment, not model obedience.

## Prep

- Run the complete student notebook except the challenge stub and verifier.
- Run the solution in the same kernel and save its outputs.
- Confirm `openai-agents` is still the pinned version expected by the course.
- Confirm `lookup_policy.params_json_schema` exposes only `category`.
- Confirm the blocked payment-card example creates no `llm:start` event.
- Confirm the safe run returns an `ExpenseDecision`, retains both guardrail result objects, and reports aggregated usage.
- Confirm the challenge either recommends review or trips the output guardrail. Do not weaken the assertion to accept approval.
- This lab depends on current model tool use for the safe and challenge paths; re-run once after changing the model pin.

## Current OpenAI documentation

- [Agent definitions](https://developers.openai.com/api/docs/guides/agents/define-agents)
- [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)
- [Results and state](https://developers.openai.com/api/docs/guides/agents/results)
- [Integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability)

