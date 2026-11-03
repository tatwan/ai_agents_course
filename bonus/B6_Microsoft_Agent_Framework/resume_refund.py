"""Resume the notebook's paused workflow in a fresh Python process."""
import asyncio
from pathlib import Path
import sys

from refund_workflow import resume

if __name__ == "__main__":
    asyncio.run(resume(Path(sys.argv[1]), sys.argv[2], sys.argv[3] == "approve"))
