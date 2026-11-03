# Lab B8 resources

`golden_cases.json` and `mlflow_run_summary.json` are byte-for-byte copies of Lab 18's
`resources/golden_cases.json` and `resources/run_summary.json`. They keep the same questions, reference checks and
recorded result so this lab runs without having to execute Lab 18. Both are repository teaching material under the
repository licence. The snapshot's model, date and rates describe that recorded run, rather than the current
settings.

The golden cases use these fields:

| Field | Meaning | Sent to the answering model? |
|---|---|---|
| `id` | Stable key for joining results | No |
| `question` | Target input | Yes |
| `facts` | Regex patterns for expected answer strings | No |
| `must`, `must_not` | Required and forbidden executed tools | No |
| `tool_facts` | Fields that must coexist in a returned tool record | No |
| `why` | Reason for this test case | No |

The MLflow snapshot contains `baseline` and `changed` results. B8 compares with `changed`, the close-name-suggestion
lookup used here. Each result has task count, pass count and rate, model-call count, token categories, total token
cost and cost per task, plus individual replies and checks. Its input total includes cached and written input.
Configured prices distinguish ordinary input, cached reads, cache writes and output. The recorded 7/8 rate covers
these eight questions and checks; it is not a production error probability.

`langsmith_run_summary.json` and `langsmith_solution_run_summary.json` retain the corresponding saved notebook's
actual evaluation rows, usage, cost and cleanup counts. Their cloud IDs name removed teaching resources. To read the
actual SDK trace fields and failure replies, open the notebook's saved outputs. A live rerun writes a new summary to
ignored `outputs/` and never overwrites these resource snapshots automatically.

`labB8_same_cases_two_tools.mmd` is the source for the diagram beside it. Ink marks the model's choice; lime marks
our execution, scoring and comparison code. Questions reach the model, while reference answers reach only the
scorer. The flow joins measurements from the same fixed tasks; it makes no platform-speed claim.

The notebook opens the public [Chinook sample database](https://www.sqlitetutorial.net/sqlite-sample-database/)
read-only, as documented in the repository's [data notes](../../../data/README.md). Policy and ticket text are
handmade teaching fixtures. The planted payment claim is constructed in memory, and the billing dictionary is an
explicit fixture. Neither comes from a live payment service.
