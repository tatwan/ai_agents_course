"""Answer a waiting refund review from a new Python process.

Run it from this folder:  python resume_refund.py CHECKPOINT_ID approve   (or: reject)
"""
import asyncio
import os
import sys

from refund_workflow import build_workflow, refund_rows


async def main(checkpoint_id: str, decision: str):
    print("process id:", os.getpid())

    # Build the workflow again and load the saved state. Nothing here comes from the notebook's memory.
    workflow, storage = build_workflow()
    restored = await workflow.run(checkpoint_id=checkpoint_id)

    waiting = restored.get_request_info_events()
    print("reviews waiting:", len(waiting))
    review = waiting[0]
    print("the question:", review.data)

    # Answer it
    print("answer:", decision)
    result = await workflow.run(responses={review.request_id: decision == "approve"})
    print("workflow output:", result.get_outputs())
    print("refunds table:", refund_rows())


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))
