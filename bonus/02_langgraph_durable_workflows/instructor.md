# Bonus 02 — Instructor notes

Weight: L. Optional post-course extension. Cut first: the time-travel fork. Keep the parallel reducer beat, checkpoint inspection, and interrupt restart rule.

## The lesson

LangGraph is a workflow runtime, not a requirement for every LLM application. This lab uses no model so students can see what the framework itself contributes: typed state, parallel super-steps, reducer-based merging, checkpoints, interrupts, resume, and branching history.

The sentence to repeat is:

> A checkpoint is executable state: values, metadata, and what runs next.

Module 09 already builds an agent loop. Do not reteach that loop here.

## Emphasise

- A `thread_id` identifies one workflow timeline. It is not a Python thread.
- Nodes return updates. They should not mutate the incoming state.
- The two checks share a super-step. Their reducer-backed list updates both survive.
- Reducers encode merge policy. Append is right for this audit trail, but wrong for the replaceable amount.
- `add_edge(['policy_check', 'amount_check'], 'decide')` is a fan-in barrier. `decide` waits for both.
- `InMemorySaver` is for learning and tests. Do not present it as durable production storage.
- The interrupt payload is data for an application UI or queue. The notebook is only displaying it.
- On resume, the interrupted node restarts from the beginning. Side effects before `interrupt` can happen twice.
- `update_state` creates a checkpoint branch. It does not rewrite the old snapshot.
- No model ran. The graph provides control and durability, not intelligence.

## Pause

1. At the diagram, ask which two boxes can run together.
2. At `RefundState`, ask why `amount_usd` does not use the list reducer.
3. At the node functions, find the first possible irreversible action. There is none.
4. At the graph wiring, point to the list of source nodes in the fan-in edge.
5. During the streamed low-risk case, note that the two check updates may arrive in either order.
6. In state history, read `next` before reading the values.
7. At the interrupt, ask whether a person has approved anything yet. No.
8. Before resume, repeat that the same thread ID is the cursor.
9. Before the fork, ask whether the original approved `$1,250` result will be erased. No.
10. At the boundary table, ask what still belongs to application engineering.

## The cell that matters

The paused snapshot:

- `values` is the saved business state;
- `next == ('human_review',)` identifies the parked work;
- `tasks[0].interrupts` carries the pending review request.

That is the bridge from a notebook demonstration to a service with a human-review queue.

## If it breaks

| Symptom | Likely cause |
|---|---|
| `langgraph` import fails | Run `uv sync` from the repository root. No new package was added for this bonus lab. |
| Concurrent update error | A field is being written by parallel nodes without a reducer. Check `signals` and `audit_log`. |
| `decide` runs before one check | The fan-in must be one edge with both source nodes, not two unrelated edges. |
| Invoke errors about `thread_id` | A checkpointer is enabled, so every run needs `configurable.thread_id`. |
| Resume starts a new run | The resume used a different thread ID. |
| No `__interrupt__` | The case had no signals and followed the auto-approve edge. |
| Resume repeats an external action | The action was placed before `interrupt`. Move it after the pause or make it idempotent. |
| Fork still contains `high_amount` | Fork from the checkpoint before the checks, not after their reducer update. |
| History looks backwards | `get_state_history` returns newest first. |

## Challenge debrief

`case-201` has three independent review signals. The student should not change the graph. The exercise is using the runtime:

1. invoke with a new thread;
2. read the interrupt payload;
3. inspect the snapshot;
4. resume the same thread with `Command(resume='reject')`.

Expected final decision: `rejected`. Expected final audit entry: `final:rejected`.

## Prep

- Run the complete student notebook except the challenge stub and verifier.
- Run the solution in the same kernel and save its outputs.
- Confirm both parallel check events appear; their display order is not contractual.
- Confirm the high-value case pauses with `next == ('human_review',)`.
- Confirm the corrected `$80` fork auto-approves without erasing the saved `$1,250` result held in `released`.
- Confirm the current `interrupt` rule: the node restarts from its beginning on resume.
- No OpenAI credential is needed and no model-dependent behavior needs morning re-verification.

## Current references

- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [LangGraph streaming](https://docs.langchain.com/oss/python/langgraph/streaming)

