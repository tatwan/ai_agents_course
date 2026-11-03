"""The notebook's toy refund executors, reconstructed by a fresh process."""
import json
import os
from pathlib import Path
import sqlite3

from agent_framework import (
    Executor, FileCheckpointStorage, WorkflowBuilder, WorkflowContext,
    handler, response_handler,
)


class CheckRequest(Executor):
    @handler
    async def check(self, request: dict, ctx: WorkflowContext[dict, dict]):
        # This small teaching policy is invented; it is not Chinook shop policy.
        if request['duplicate_confirmed'] and 0 < request['amount'] <= 50:
            await ctx.send_message(request)
        else:
            await ctx.yield_output({'request_id': request['request_id'], 'status': 'ineligible'})


class HumanReview(Executor):
    @handler
    async def ask(self, request: dict, ctx: WorkflowContext[dict, dict]):
        await ctx.request_info(request_data=request, response_type=bool)

    @response_handler
    async def decide(self, original_request: dict, response: bool,
                     ctx: WorkflowContext[dict, dict]):
        if response:
            await ctx.send_message(original_request)
        else:
            await ctx.yield_output({'request_id': original_request['request_id'], 'status': 'rejected'})


class QueueRequest(Executor):
    def __init__(self, queue_path: Path):
        super().__init__(id='queue')
        self.queue_path = queue_path
        with sqlite3.connect(queue_path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS requests '
                       '(request_id TEXT PRIMARY KEY, customer_id INTEGER, amount REAL)')

    @handler
    async def queue(self, request: dict, ctx: WorkflowContext[dict, dict]):
        with sqlite3.connect(self.queue_path) as db:
            db.execute('INSERT OR IGNORE INTO requests VALUES (?, ?, ?)',
                       (request['request_id'], request['customer_id'], request['amount']))
        await ctx.yield_output({'request_id': request['request_id'], 'status': 'queued'})


def build_workflow(run_dir: Path):
    """Recreate the same graph and executor IDs used in the notebook."""
    check = CheckRequest(id='check')
    review = HumanReview(id='review')
    queue = QueueRequest(run_dir / 'queue.db')
    storage = FileCheckpointStorage(run_dir / 'checkpoints')
    builder = WorkflowBuilder(name='refund', start_executor=check, checkpoint_storage=storage)
    builder.add_edge(check, review)
    builder.add_edge(review, queue)
    return builder.build(), storage


async def resume(run_dir: Path, checkpoint_id: str, decision: bool):
    workflow, storage = build_workflow(run_dir)
    restored = await workflow.run(checkpoint_id=checkpoint_id)
    pending = restored.get_request_info_events()
    assert len(pending) == 1, 'Expected one pending review.'
    result = await workflow.run(responses={pending[0].request_id: decision})
    with sqlite3.connect(run_dir / 'queue.db') as db:
        rows = db.execute('SELECT * FROM requests ORDER BY request_id').fetchall()
    print(json.dumps({'pid': os.getpid(), 'restored_requests': len(pending),
                      'outputs': result.get_outputs(), 'queue': rows}))

