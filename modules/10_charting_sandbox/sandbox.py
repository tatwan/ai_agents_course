"""Run one Python file in the charts folder, with a timeout.

The notebook builds this jail first. The file exists because a container
must start a process. It does not add logic the notebook skipped.

This is still not a filesystem sandbox. The child can walk up to the repo
unless you put the same file in Docker with only /work mounted.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHARTS = HERE / "charts"
IMAGE = "python:3.12-slim"


def run_jailed(code: str, timeout: int = 15) -> str:
    CHARTS.mkdir(exist_ok=True)
    mpl = CHARTS / ".mpl"
    mpl.mkdir(exist_ok=True)
    script = CHARTS / "_run.py"
    script.write_text(code)
    env = {
        "PATH": os.environ.get("PATH", ""),
        "MPLCONFIGDIR": str(mpl),
        "HOME": str(CHARTS),
    }
    try:
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(CHARTS),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return "timed out"
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        return "error: " + out[-800:]
    return (out[-800:] if out.strip() else "ok")


def run_docker(code: str, timeout: int = 20) -> str:
    """Same snippet, host disk not mounted except CHARTS -> /work."""
    CHARTS.mkdir(exist_ok=True)
    script = CHARTS / "_run.py"
    script.write_text(code)
    inspect = subprocess.run(
        ["docker", "image", "inspect", IMAGE],
        capture_output=True,
        text=True,
    )
    if inspect.returncode != 0:
        return "docker image missing: " + IMAGE + " (pre-pull into the VM; do not pull in class)"
    try:
        proc = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "--network",
                "none",
                "-v",
                f"{CHARTS}:/work",
                "-w",
                "/work",
                IMAGE,
                "python",
                "_run.py",
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        return "docker client not installed"
    except subprocess.TimeoutExpired:
        return "timed out"
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        return "error: " + out[-800:]
    return (out[-800:] if out.strip() else "ok")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: uv run python sandbox.py jailed|docker <file.py>")
        raise SystemExit(2)
    mode = sys.argv[1]
    source = Path(sys.argv[2]).read_text() if len(sys.argv) > 2 else ""
    if mode == "jailed":
        print(run_jailed(source))
    elif mode == "docker":
        print(run_docker(source))
    else:
        print("mode must be jailed or docker")
        raise SystemExit(2)
