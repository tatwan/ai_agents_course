# Bonus 08 — Instructor notes

Weight: M. Optional post-course extension. Cut first: the migration-inventory list, the per-message token rows, and the reset/resume/replay comparison. Keep the maintenance-status warning, raw tool events, composed termination, application audit, state governance, and restore/resume challenge.

## The lesson

AutoGen is a message-driven framework for agents and teams. AgentChat supplies high-level agents, teams, messages, termination, and state; Core supplies the lower-level event-driven runtime; Extensions supply provider clients and other integrations.

The sentence to repeat is:

> A multi-agent team is a stateful protocol, not a group of model personalities.

The lab is also deliberately honest about product direction. AutoGen 0.7.5 is in maintenance mode, and Microsoft directs new projects toward Microsoft Agent Framework. Teach AutoGen as current literacy for systems students may inherit, plus a concrete migration case. Do not present it as the automatic greenfield choice.

## Environment boundary

This lab does not use the core `.venv`. From `bonus/08_autogen_message_driven_teams/`, run:

```bash
uv sync --locked
```

In VS Code, choose:

```text
bonus/08_autogen_message_driven_teams/.venv/bin/python
```

The exact direct pins are:

- `autogen-agentchat==0.7.5`;
- `autogen-ext[openai]==0.7.5`;
- `ipykernel==7.1.0`;
- `python-dotenv==1.2.2`.

The lockfile resolves AutoGen Core 0.7.5 and OpenAI 3.3.1. The verified environment contains 58 installed distributions. It reads the model, prices, and API key from the repository-root `.env`.

## Current-status boundary

Three generations are easy to confuse:

| Surface | Clues | Course position |
|---|---|---|
| AutoGen 0.2 | `ConversableAgent`, `UserProxyAgent`, `initiate_chat` | historical API; many search results still use it |
| AutoGen AgentChat 0.7 | `AssistantAgent`, `RoundRobinGroupChat`, `run_stream` | API used in this lab; maintained, no new feature work |
| Microsoft Agent Framework | successor from Microsoft | evaluate first for new Microsoft-centered systems |

Do not spend the lab teaching old 0.2 syntax. The point of naming it is to make students version-literate when they encounter examples or inherited code.

## API surface note

The pinned AutoGen integration does not recognize the newer course model alias in its static capability table, so the notebook supplies `model_info` explicitly. It uses Chat Completions with `max_completion_tokens=500`, no temperature, and `reasoning_effort="none"`.

Do not add client-level `parallel_tool_calls=False`. Live verification found that AutoGen also forwards this option for the drafter, which has no tools, and the current OpenAI API rejects that request. The reviewer exposes only one tool and has `max_tool_iterations=1`, so no global parallel-tool option is needed.

The provider resolves the model alias to a dated snapshot. The notebook suppresses only the corresponding AutoGen alias-mismatch warning so the event trace remains readable.

## Scenario and safety boundary

The release record is synthetic and inline. The only tool, `evaluate_release_policy`, is read-only and accepts one exact change ID. It returns a deterministic policy decision and adds an application-owned audit row. It cannot approve, deploy, write a file, or access a network service.

The team has two roles:

- `drafter` turns supplied facts into a release brief and has no tools;
- `reviewer` calls policy once, writes the review, and returns control with `READY_FOR_HUMAN`.

The marker does not grant approval. It means the framework has stopped and the application can hand the artifact to a person.

## Emphasise

- AgentChat, Core, and Extensions are different abstraction layers.
- The framework coordinates messages; the model does not execute Python.
- Role prompts are task boundaries, not authorization boundaries.
- `RoundRobinGroupChat` makes turn order explicit and predictable for this example.
- `run_stream` exposes `TextMessage`, `ToolCallRequestEvent`, `ToolCallExecutionEvent`, and the final `TaskResult`.
- The application audit is independent of the framework trace and should be durable in production.
- `TextMentionTermination` is scoped to `reviewer`; a user or drafter cannot stop the team by echoing the marker.
- The expected marker stop is composed with a five-message cap, and the team also has `max_turns=4`.
- Termination conditions reset after a completed run. Team conversation state does not disappear unless reset.
- Model usage accumulates on the client and appears on model-produced message events.
- The cost estimate assumes all prompt tokens are uncached and excludes infrastructure.
- `save_state()` is called only after the team stops.
- Saved team state can contain prompts, messages, tool results, and workflow position. It is governed application data.
- Loading state requires fresh objects with compatible participant names and structure.
- Resume is not deterministic replay. Side-effecting tools need idempotency keys and durable execution records.
- Behavioral assertions are migration assets: tool arguments, stop reason, state shape, and human-control invariant should survive a framework change.
- A framework can accelerate team coordination, but a thin SDK or explicit loop may be better when the workflow is small and every transition must remain obvious.

## Pause

1. At the product-status table, ask which API a `UserProxyAgent` tutorial represents. AutoGen 0.2.
2. At the layer table, ask whether AgentChat is the runtime or a high-level API over it.
3. At the diagram, ask who executes the policy function. The AutoGen runtime in the student's Python process, not the model.
4. Before the tool, ask which release action it can perform. None.
5. At the team factory, ask why a helper is justified here. State must be loaded into fresh, structurally identical objects.
6. At termination, ask why the marker is source-scoped to `reviewer`.
7. Before running, predict the event sequence.
8. At the tool request event, inspect the exact name and JSON arguments.
9. At the execution event, locate the deterministic decision and `is_error` flag.
10. At `TaskResult`, distinguish the stop reason from the review text.
11. At usage, reconcile the drafter request, reviewer tool-selection request, and reviewer reflection request.
12. At state, ask why the API key is absent but the snapshot is still sensitive.
13. Before the challenge, distinguish restoring state from reusing the original team.
14. After the challenge, ask what would make resume dangerous if the tool deployed a release.
15. End by asking what should migrate even if every framework class name changes. The behavioral contract and controls.

## The cells that matter

The verified path should show:

1. AgentChat, Core, and Extensions are all 0.7.5 in an isolated environment.
2. The team has `drafter` and `reviewer`, a marker-or-message termination condition, and four maximum turns.
3. The stream contains six objects: user text, drafter text, tool request, tool execution, reviewer text, and `TaskResult`.
4. The policy audit contains exactly one successful lookup for CHG-77.
5. The reviewer, not the drafter or user, emits `READY_FOR_HUMAN`.
6. The stop reason is the marker condition, not the hard cap.
7. Usage is nonzero and its price assumption is stated.
8. Saved state has `type`, `version`, and `agent_states`, with entries for both participants and the manager.
9. The serialized snapshot does not contain the API key.
10. The challenge creates a fresh team, loads state, preserves CHG-77 context, applies 02:00 UTC feedback, calls policy once, and stops for a human again.

The verified solution run on 2026-08-20 produced:

- 58 installed distributions;
- six first-run stream objects;
- one `ToolCallRequestEvent` and one `ToolCallExecutionEvent`;
- one application-audit row for CHG-77;
- marker-based termination before the hard ceiling;
- 888 prompt and 360 completion tokens in the first run;
- estimated first-run cost `$0.000628`, assuming all input was uncached;
- an 8,462-byte serialized state snapshot with three named state entries and no API key;
- one policy lookup after restore;
- CHG-77 reissued at 02:00 UTC and returned with `READY_FOR_HUMAN`.

Exact prose, token counts, cost, and serialized byte size can vary. Event types, tool count and arguments, stop ownership, state entry names, and human-control outcome are load-bearing.

## If it breaks

| Symptom | Likely cause |
|---|---|
| `autogen_agentchat` import fails | The core kernel is selected. Choose the Bonus 08 `.venv`. |
| Examples mention `ConversableAgent` or `UserProxyAgent` | They target AutoGen 0.2, not this lab's AgentChat 0.7 API. |
| `uv sync --locked` reports a stale lock | `pyproject.toml` changed. Restore the reviewed pins before regenerating. |
| `.env` values are missing | Start VS Code from inside the repository and keep the root `.env` present. |
| AutoGen says the model family is unknown | The explicit `model_info` block was removed or the model family changed. Re-verify before editing it. |
| OpenAI rejects `parallel_tool_calls` when no tools are specified | A global `parallel_tool_calls` option was added. Remove it. |
| An error mentions `max_tokens`, temperature, or reasoning | Keep `max_completion_tokens`, no temperature, and `reasoning_effort="none"`. |
| The reviewer never calls the tool | Inspect its prompt, registered tool, and event stream. Re-run once before changing assertions. |
| The reviewer calls the tool more than once | Confirm only one tool is exposed and `max_tool_iterations=1`; inspect request events before weakening the verifier. |
| The drafter stops the team | It emitted the marker, but the source-scoped termination should ignore it. Confirm `sources=["reviewer"]`. |
| The run reaches a message or turn cap | Inspect prompts and events. Do not increase ceilings until the nontermination cause is understood. |
| `save_state()` fails or captures partial work | The team was still running. Save only after `TaskResult`. |
| `load_state()` reports incompatible participants | Rebuild with the same participant and team-manager names and compatible framework version. |
| The restored drafter forgets CHG-77 | State was not loaded before the follow-up, or the original team was reset instead of a fresh team being restored. |
| The restored run keeps 01:00 UTC | Human feedback was omitted or phrased ambiguously. Inspect the resumed drafter message. |
| The verifier sees two audit rows | `tool_audit.clear()` was omitted before the resumed run. |
| The client is closed before the challenge | Move `await model_client.close()` back to the final cleanup cell. |

## Challenge debrief

The solution deliberately constructs a new team, then loads the prior snapshot. Reusing the original team would not prove that state is portable. The follow-up task contains only the changed window and the change ID; prior owner, summary, risks, and rollback come from restored conversation state.

The verifier grades behavior rather than prose:

- a fresh team exists;
- the final object is a `TaskResult`;
- exactly one application-audited lookup targets CHG-77;
- the drafter retains CHG-77 and emits 02:00;
- the reviewer emits `READY_FOR_HUMAN`;
- the stop reason confirms the expected marker.

It does not grade headings, bullet style, exact wording, token count, or state byte size.

## Prep

- Run `uv sync --locked` only inside this bonus directory.
- Confirm AgentChat, Core, and Extensions 0.7.5 and OpenAI 3.3.1.
- Run the student notebook through the challenge prompt, then run the saved-output solution.
- Confirm the trace has one tool request and one tool execution with `change_id="CHG-77"`.
- Confirm the application audit also has exactly one lookup.
- Confirm the marker condition stops the first run before either hard ceiling.
- Confirm usage and estimated cost are nonzero.
- Confirm saved state has both agent names and `RoundRobinGroupChatManager`, but no API key.
- Confirm restore/resume changes the window to 02:00 UTC and returns to a human.
- Confirm the model client closes only after the verifier.
- **Model-dependent:** after changing the model, AutoGen, or OpenAI, re-run both tool-call paths, termination, state restore, and challenge assertions.
- Recheck AutoGen's official maintenance status and migration guidance before delivery; product direction can change.

## Current documentation

- [AutoGen repository and status](https://github.com/microsoft/autogen)
- [AgentChat user guide](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/)
- [Agents tutorial](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/agents.html)
- [Teams tutorial](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
- [Termination conditions](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/termination.html)
- [State management](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/state.html)
- [Human-in-the-loop patterns](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/human-in-the-loop.html)
- [Migration from AutoGen to Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/)
