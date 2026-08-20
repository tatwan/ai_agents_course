# Bonus 06 — Instructor notes

Weight: L. Optional post-course extension. Cut first: the installed-distribution count, the detailed `wiring` object, and the full typed JSON print. Keep the four-object mental model, Crew-versus-Flow choice, explicit context edge, exact tool audit, unsafe guardrail probe, async kickoff, usage ledger, and challenge.

## The lesson

CrewAI makes a team-shaped design explicit: agents own roles and capabilities, tasks own deliverables and dependencies, a process controls coordination, and a crew owns execution and aggregate usage.

The sentence to repeat is:

> A role is prompt scaffolding; authority is application code.

Students should leave able to build a small Crew, but also able to reject one. Multiple job titles do not justify multiple model calls. Use a Crew when responsibilities genuinely differ in objective, capability, context, or evaluation. Use ordinary Python for exact steps and a Flow for auditable branching, state, retries, and side effects.

## Environment boundary

This lab does not use the core `.venv`. From `bonus/06_crewai_role_based_teams/`, run:

```bash
uv sync --locked
```

In VS Code, choose:

```text
bonus/06_crewai_role_based_teams/.venv/bin/python
```

The exact framework pin is `crewai==1.15.17`. The resolved environment uses Python 3.13.5, CrewAI 1.15.17, OpenAI 2.54.0, MCP 1.28.1, and 159 installed distributions. CrewAI requires Python below 3.14. Its dependency graph also includes Chroma, LanceDB, ONNX Runtime, PyArrow, Kubernetes, and PDF tooling even though this direct-object lab does not use those features. Keep the environment isolated from the core course.

The lab reads the repository-root `.env`. Do not create another secrets file in the bonus directory.

## Why direct Python objects

CrewAI 1.15.17 supports JSONC-first projects, the classic YAML/decorator project shape, and direct Python construction. This notebook uses direct `Agent`, `Task`, `Crew`, and `LLM` objects because the class needs to see the wiring before learning a scaffold or configuration convention.

Do not imply that direct objects are the only production layout. After students understand the objects, show the current CLI and JSONC layout from the official docs as an organizational option. Do not generate a project during this lab; it would create several files and hide the first mental model.

## Emphasise

- `Agent.role`, `goal`, and `backstory` influence the prompt. They are not authentication, identity, or access control.
- Only the evidence analyst receives `lookup_change_record`; the reviewer receives no tools.
- The model emits the tool name and `change_id`. Python performs the lookup and records the audit.
- `Task` owns `output_pydantic`, `context`, and the guardrail. Those concerns do not belong in a decorative job title.
- `context=[evidence_task]` is an explicit dependency edge. The reviewer works from the earlier task output and does not query the record again.
- Typed output validates shape. The deterministic guardrail checks owner and review policy against trusted application data.
- The unsafe probe is well typed and still rejected. This is the cleanest proof that schema validation is not policy validation.
- A failed task guardrail can send feedback back to the agent for repair. The lab permits one retry; it does not silently loop forever.
- `Process.sequential` is sufficient because task ownership is already explicit. A hierarchical process adds a manager model, autonomy, and cost.
- Jupyter has an active event loop. CrewAI 1.15.17 requires `await crew.kickoff_async(...)` here. Do not replace it with `kickoff()` plus an event-loop patch.
- One task is not one request. The verified main path used six successful model requests for two tasks because tool use and structured-output conversion add protocol turns.
- `Crew.usage_metrics` aggregates framework usage. The application audit answers a different question: which real tool operations occurred?
- `tracing=False` keeps this classroom run local. It is not a production observability strategy.
- CrewAI's own guidance favors Crews for open-ended collaboration, Flows for deterministic and auditable workflows, and a combination for controlled workflows with pockets of agency. This lab follows that boundary.

## Pause

1. At the diagram, ask which box has release authority. None; the crew returns analysis.
2. At the four-object table, ask whether a role named “approver” can approve anything. No.
3. At the autonomy table, ask where a bank transfer or production deployment belongs. Deterministic application or Flow control with an external approval gate.
4. At the environment note, point out that a small example resolved 159 distributions.
5. At the tool schema, ask which argument the model controls. Only `change_id`.
6. At the agents, ask why the reviewer has no lookup tool. The handoff is the evidence task’s responsibility and should remain observable.
7. At the tasks, locate the `context` edge in code.
8. Before the unsafe probe, predict whether Pydantic accepts it. Yes. Then predict whether policy accepts it. No.
9. Before kickoff, ask why top-level `await` is required in VS Code notebooks.
10. At the typed task outputs, distinguish the evidence handoff from the final decision.
11. At the two audits, identify the model proposals and the Python actions.
12. At usage, ask students to predict request count from task count, then show why that shortcut fails.
13. At the challenge, ask whether adding a “schedule specialist” would add a capability. No.

## The cells that matter

The core execution should show this sequence:

1. `evidence_task` prompts the evidence analyst.
2. The analyst proposes `lookup_change_record(change_id="CHG-104")`.
3. Python returns the trusted record and appends one `tool_audit` entry.
4. CrewAI converts the first task result to `ChangeEvidence`.
5. `review_task` receives that output through `context=[evidence_task]`.
6. The reviewer returns `ReleaseDecision`.
7. `enforce_release_policy` compares the proposal with trusted owner and human-review rules.
8. The final crew output is the last task’s typed decision.

The verified main path on 2026-08-20 returned:

- `CHG-104`;
- risk `high`;
- recommendation `human_approval`;
- owner `data-platform`;
- human review `True`;
- one exact application tool call;
- one accepted live guardrail evaluation;
- 3,788 prompt tokens, 364 completion tokens, 4,152 total tokens;
- six successful model requests;
- estimated course-list cost `$0.001213`.

Exact completion tokens and wording can vary. The grounded fields, tool count, policy result, and assertions are load-bearing.

## If it breaks

| Symptom | Likely cause |
|---|---|
| `crewai` import fails | The core kernel is selected. Choose the Bonus 06 `.venv`. |
| `uv sync --locked` rejects the interpreter | The selected Python is 3.14 or newer. Let `uv` select a compatible Python 3.11–3.13 interpreter. |
| `uv sync --locked` reports a stale lock | `pyproject.toml` changed. Restore the reviewed pins rather than casually regenerating before delivery. |
| `OPENAI_API_KEY` or `MODEL_DEFAULT` is missing | The repository-root `.env` is absent or incomplete. Do not add secrets to this directory. |
| OpenAI rejects `temperature`, `max_tokens`, or reasoning settings | Keep `max_completion_tokens`, omit `temperature`, and use `reasoning_effort="none"`. |
| `RuntimeError` says execution was invoked synchronously inside a running event loop | The notebook used `kickoff()`. Use `await release_crew.kickoff_async(...)`. |
| The evidence task calls the lookup more than once | Re-run once, then inspect the tool arguments. Do not weaken the exact-one-call assertion without understanding the additional call. |
| `crew_result.pydantic` is `None` | The final task lost `output_pydantic=ReleaseDecision`, or the framework conversion behavior changed. Inspect `crew_result.raw` and the task configuration. |
| The guardrail exhausts its retry | Print `guardrail_audit` and the last task output. Do not remove the owner or human-review invariant to make the model pass. |
| `inspect.getsource` fails around a task guardrail | Callable guardrail event handling changed or the function is no longer defined in a normal notebook cell. Verify against the pinned version; do not move policy into an LLM string merely to avoid the error. |
| The omitted context appears as `_NotSpecified` | That is CrewAI’s internal sentinel in 1.15.17. The notebook’s inspection cell deliberately checks for an actual list before calling `len()`. |
| A tracing preference message appears on the first run | Confirm `tracing=False` and `CREWAI_TRACING_ENABLED=false`. Do not enable a hosted trace sink for the class without reviewing data handling. |
| `successful_requests` is greater than the number of tasks | Expected. Tool loops and Pydantic conversion can use additional requests. |
| The challenge marks `CHG-205` medium/high or requests a person | Re-run once. If persistent, inspect the evidence handoff and policy text. The trusted record is schedule-only and the verifier intentionally requires `low` / `proceed` / no human review. |

## Challenge debrief

The same two-role crew handles `CHG-205`. The trusted record has a schedule-only signal, owner `analytics-engineering`, a rollback plan, and a passed schedule validation. The expected decision is low risk, `proceed`, and no human review.

The key design answer is that no new agent was needed. The responsibilities did not change; only the input did. Framework fluency includes reuse and restraint, not just adding roles.

The verifier grades typed handoff, exact tool arguments, trusted owner, policy fields, and the accepted guardrail. It does not grade prose.

## Prep

- Run `uv sync --locked` only inside this bonus directory.
- Confirm the selected kernel reports CrewAI 1.15.17, OpenAI 2.54.0, and Python below 3.14.
- Run the student notebook through the challenge stub, then run the saved-output solution.
- Confirm the unsafe probe is rejected before the live run.
- Confirm `CHG-104` calls the lookup exactly once and produces a typed high-risk human-approval decision for `data-platform`.
- Confirm the live guardrail audit ends accepted.
- Confirm the solution prints aggregate token usage, successful request count, and course-list cost.
- Confirm `CHG-205` calls the lookup exactly once and passes every challenge assertion.
- **Model-dependent:** re-run both paths after changing `MODEL_DEFAULT`, CrewAI, or OpenAI. The exact request count and tokens may change, but tool count, grounded owners, risk policy, and challenge decisions must still pass.
- Recheck CrewAI’s current Python and dependency constraints before regenerating `uv.lock`.

## Current documentation

- [CrewAI introduction and Crews-versus-Flows guidance](https://docs.crewai.com/en/introduction)
- [Agents](https://docs.crewai.com/en/concepts/agents)
- [Tasks, context, typed output, and guardrails](https://docs.crewai.com/en/concepts/tasks)
- [Crews and usage metrics](https://docs.crewai.com/en/concepts/crews)
- [Processes](https://docs.crewai.com/en/concepts/processes)
- [LLM configuration](https://docs.crewai.com/en/concepts/llms)
- [Custom tools](https://docs.crewai.com/en/concepts/tools)
