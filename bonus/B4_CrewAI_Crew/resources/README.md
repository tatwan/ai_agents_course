# Bonus B4 resources

`b4_crew_tasks_and_context.mmd` is the source of `b4_crew_tasks_and_context.png`: one run of a two-task crew. In task 1
the model asks for a tool and our tool function runs; task 1's output is passed to task 2 as context; task 2's model
writes from it with no tools; our guardrail function accepts the output or sends the reason back. Ink nodes are the
model's work, lime nodes our own code, white nodes text passed along. The export command is in the source. Both
notebooks embed the PNG.

The desk notebook reads the repository's [Chinook database](../../../data/README.md) in place, read-only. The
newsroom's result sheet is made up for the lab and lives in the notebook and in `school_paper/tools/match_result.py`.
