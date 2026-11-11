# Lab 22 resources

These files support a local process-design exercise. Running the notebook calls no model or service.

| File | Source and use |
|---|---|
| `lab20_run_summary.json` | Unchanged copy of `20_Evals_And_Tracing/resources/run_summary.json`, recorded on 2026-11-01 from `20_evals_and_tracing.ipynb`. Bundled so no prior notebook run is required. Teaching data supplied with this repository; no separate data licence is specified. |
| `lab22_process_map.mmd` and `.png` | Lab-authored before/after drawing of the damaged-media refund process. The source includes its export command. |

The notebook reads the supplied `data/corpus/policy_returns.md`, `policy_damaged_media.md` and `policy_refunds.md` in place. These are Chinook teaching-policy fixtures supplied with this repository; no separate data licence is specified. The same-title-damaged-twice case, human-effort figures, volume, wage, rework rate, build/operations costs and buying prices in this lab are illustrative assumptions. They do not describe actual shop operations. Ticket 06 records a shipped replacement; the new design case does not change it.

## Recorded snapshot fields

- `source_notebook` and `recorded_on` identify the source and date of the fixed measurement.
- `baseline` and `changed` describe the same eight teaching questions under the original lookup and the close-name-suggestion variant.
- `tasks`, `passed` and `pass_rate` count the task checks. Both variants pass 7/8 = 0.875. These checks are not a production error probability.
- `model_calls` counts model requests within the eight tasks: 20 for the changed set. One task can contain several model calls.
- `tokens.input` includes ordinary input, cached reads and cache writes. Subtract `cached` and `written` before pricing ordinary input. The changed set has 9,048 input tokens, zero cached/written and 581 output tokens.
- `prices_per_million_tokens_usd` records the four configured token rates used for this measurement, independently of future settings changes.
- `total_model_token_cost_usd` is $0.00119530 for the changed set; `cost_per_task_usd` is $0.0001494125, divided by all eight tasks including the failure. Human review, hosting, tax and provider discounts are excluded.
- `cases` retains per-case questions, actual replies, checks, tokens and trace IDs. The one failed changed case answers an unrelated poem request; it is not a failed refund payment.
- `limits` states the measurement boundary. The business calculator borrows token cost as an editable lookup-equivalent proxy. It never derives its rework assumption from `1 - pass_rate`.

The recorded snapshot is fixed. Re-running Lab 20 does not update this copy; measure your actual proposed workflow before making a business commitment.
