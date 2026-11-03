# Lab 00: How to set up the lab environment

**CPU | API key: `OPENAI_API_KEY` | one small model call**

## Goal

Set up this repository once, on a class VM, in GitHub Codespaces or on your own machine, and check in one run that
the core environment is ready. This README is the setup guide; the notebook, `00_environment_check.ipynb`, is the check at the
end. When its last cell shows ✅ on every required line, you are ready for Lab 01.

## What you will learn

- How to get the repository (with `git clone` or as a ZIP) and install it with `uv`, or with `pip` where `uv` is
  blocked.
- How to open a notebook in VS Code (or JupyterLab) on the repository's own environment, the `.venv` kernel.
- Where the model settings live (`models.env`) and where your key lives (`.env`), and how to change the model in one
  line.
- Which labs need their own environment, and how to create one.
- How to read the notebook's summary and fix a failed line from the troubleshooting tables.

## Choose a route

| Route | Use it when | You need |
|---|---|---|
| **A. Ubuntu VM with VS Code** | your class gives you a VM | the VM and an OpenAI key |
| **B. GitHub Codespaces** | you cannot install software, or the VM is not available | a GitHub account and an OpenAI key |
| **C. Your own machine with `uv`** (recommended for your own machine) | you can install a command-line tool | a terminal, VS Code or a browser, and an OpenAI key |
| **D. Your own machine with `pip`** | your machine does not allow `uv`, but has Python 3.11 to 3.14 | Python, a terminal and an OpenAI key |

Every route installs the same pinned package versions, from `uv.lock` or from `requirements.txt` (exported from the
same lock). The saved outputs in every lab come from these versions on Python 3.13, so a run on your machine should
match ours.

---

## Route A: Ubuntu VM with VS Code

**1. Open a terminal.** In VS Code: **Terminal → New Terminal**.

**2. Get the repository** and move into it:

```bash
git clone https://github.com/tatwan/ai_agents_course.git
cd ai_agents_course
```

Then open the folder in VS Code (**File → Open Folder**, choose `ai_agents_course`), so the notebooks and the terminal
both start there.

**3. Install `uv`** (once per machine). [`uv`](https://docs.astral.sh/uv/) installs the right Python and the pinned
packages into a folder called `.venv` inside the repository, so nothing else on the machine changes.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close the terminal and open a new one, then check that `uv --version` prints a version.

**4. Install Python and the packages**, from the repository folder:

```bash
uv sync --python 3.13
```

This reads `pyproject.toml` and `uv.lock`, downloads Python 3.13 if the VM does not have it, and installs every pinned
package (JupyterLab and the notebook kernel included) into `.venv`. Run it again whenever `uv.lock` changes after a
`git pull`.

**5. Install the VS Code extensions** **Python** and **Jupyter** (both by Microsoft) from the Extensions panel, if they
are not there yet.

**6. Install Graphviz** (optional; lab 07 draws agents with it):

```bash
sudo apt update
sudo apt install -y graphviz
```

Then continue with [Add your key](#add-your-key-and-choose-the-model) and
[Choose the kernel](#choose-the-kernel).

---

## Route B: GitHub Codespaces

A codespace is a VS Code running on a GitHub machine (Ubuntu underneath), in your browser or attached to your desktop
VS Code.

1. On the repository's GitHub page, click **Code**, open the **Codespaces** tab and click **Create codespace on main**.
   The repository is already cloned there, and the terminal opens in its folder.
2. Follow route A from step 3: install `uv`, run `uv sync --python 3.13`, and, if you want Graphviz, the two `apt`
   lines.
3. Add your key as in [Add your key](#add-your-key-and-choose-the-model). In a codespace you can instead store it as a
   [Codespaces secret](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-your-account-specific-secrets-for-github-codespaces)
   named `OPENAI_API_KEY` (your GitHub **Settings → Codespaces → Secrets**, with access to this repository). GitHub puts
   it in the environment, and the config cell uses a key from the environment before one in `.env`.

---

## Route C: Your own machine with `uv`

**1. Install `uv`** (once per machine). macOS or Linux, in a terminal:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows, in PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close the terminal and open a new one, then check that `uv --version` prints a version.

**2. Get the repository.** With Git:

```bash
git clone https://github.com/tatwan/ai_agents_course.git
cd ai_agents_course
```

Without Git, download the [ZIP](https://github.com/tatwan/ai_agents_course/archive/refs/heads/main.zip), unzip it and
open a terminal in the unzipped folder (it is called `ai_agents_course-main`). Git makes later updates easier: `git
pull` fetches them.

**3. Install Python and the packages:**

```bash
uv sync --python 3.13
```

**4.** Add your key, then open the notebook on the `.venv` kernel in VS Code (with the Python and Jupyter extensions),
or start JupyterLab from the repository folder:

```bash
uv run jupyter lab
```

Graphviz and Docker are optional; see [Optional tools](#optional-tools).

---

## Route D: Your own machine with `pip`

Use this route when you cannot install `uv`. You manage the Python version yourself: any Python from 3.11 to 3.14
works, and 3.13 matches the saved outputs.

**1. Check your Python:** `python3 --version` (macOS or Linux) or `py --version` (Windows). An older Python stops the
install in step 3 (troubleshooting table).

**2. Get the repository**, as in route C, step 2.

**3. Create a virtual environment and install the packages.** A virtual environment is a folder that holds this
repository's packages apart from any other Python project. The commands name Python 3.13; with another version in
the range, use its name instead (for example `python3.12`, or `py -3.12` on Windows). From the repository folder,
macOS or Linux:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
py -3.13 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` holds the same pins as `uv.lock`, JupyterLab and the notebook kernel included. Your prompt shows
`(.venv)` while the environment is active; activate it again in every new terminal.

**4.** Add your key, then open the notebook on the `.venv` kernel in VS Code, or run `jupyter lab` from the repository
folder with the environment active.

---

## Add your key and choose the model

Two small files in the repository folder hold everything the labs need to know about the model:

| File | Holds | Committed to Git? |
|---|---|---|
| `models.env` | the model names (`MODEL_DEFAULT`, `MODEL_STRONG`, `EMBEDDING_MODEL`), `REASONING_EFFORT` and the prices per million tokens | yes: no secrets in it |
| `.env` | your `OPENAI_API_KEY`, and the optional bonus keys | never: `.gitignore` keeps it out |

**Add your key.** Copy the example file, then open `.env` in any editor and paste your key after `OPENAI_API_KEY=`
(no quotes, no spaces):

```bash
cp .env.example .env          # Windows: copy .env.example .env
```

Never paste a key into a notebook cell, and never print `.env`.

**Change the model in one line.** No notebook names a model in its code; every lab reads `MODEL_DEFAULT` from
`models.env`. To use another model in every lab, change that line (and the prices under it). To try a model on your
machine only, put a `MODEL_DEFAULT=...` line in your `.env`: a non-empty value there wins. A model without a reasoning
setting needs `REASONING_EFFORT=` left empty. Another model words its replies differently, so in each lab check the
facts a checkpoint names, not the wording.

## Choose the kernel

The kernel is the Python that runs a notebook's cells. It must be the repository's `.venv`, or the packages are
missing.

- **VS Code:** open `00_Environment_Check/00_environment_check.ipynb`, click **Select Kernel** at the top right, choose
  **Python Environments**, then the environment whose path is `.venv/bin/python` in the repository folder (Windows:
  `.venv\Scripts\python.exe`). VS Code remembers the choice for that notebook.
- **JupyterLab:** start it with `uv run jupyter lab` (route D: `jupyter lab` with the environment active) from the
  repository folder; its **Python 3 (ipykernel)** kernel is then the `.venv`.

Run the notebook from the top (VS Code: **Run All**), then read the last cell.

## Labs with their own environment

Four labs use libraries that need other versions of packages the main environment pins, so each has its own
`pyproject.toml`, `uv.lock` and `.venv` inside its folder. You create one only when you do that lab; the notebook
reports each as set up or "optional, not set up".

| Lab | Folder | Why it has its own environment |
|---|---|---|
| 12 | `12_LlamaIndex_RAG` | LlamaIndex needs `openai` 2.x; the main environment pins 3.x |
| B3 | `bonus/B3_Google_ADK` | Google ADK caps the LiteLLM version it accepts |
| B5 | `bonus/B5_CrewAI_Crew` | CrewAI needs `openai` 2.x and `mcp` 1.x |
| B6 | `bonus/B6_Microsoft_Agent_Framework` | Agent Framework adds over a hundred packages, kept out of the main install |

To create one, run `uv sync` inside that lab's folder, for example:

```bash
cd 12_LlamaIndex_RAG
uv sync --python 3.13
cd ..
```

Then open the lab's notebook in VS Code and choose **that folder's** `.venv` as the kernel (for example
`12_LlamaIndex_RAG/.venv/bin/python`), not the one in the repository folder. Choosing the wrong one is easy to spot:
Lab 00 run on lab 12's environment reports most packages `missing`.
Where `uv` is blocked, lab 12's README creates the same environment with `pip` from its `requirements.txt`.

## Optional tools

| Tool | Used by | Install |
|---|---|---|
| Graphviz (`dot`) | lab 07, to draw an agent's structure; only that drawing needs it | Ubuntu: `sudo apt install -y graphviz`; macOS: `brew install graphviz`; Windows and others: [graphviz.org/download](https://graphviz.org/download/) |
| Docker | lab 15's container runner; lab 15 also runs without it | [Docker Desktop](https://docs.docker.com/get-started/get-docker/) (macOS, Windows), or Docker Engine on Linux |

After installing Graphviz, restart the notebook's kernel so it sees the new program.

## Optional keys

Two bonus labs use services that need an account: Pinecone (B7) and LangSmith (B8). Their lines are in `.env.example`;
remove the `#` and paste the key after the `=` in your `.env`. Every core lab runs without them, and the notebook only
says whether each is set.

## What the notebook checks

**Part A: Read the settings every lab starts from.** The config cell every lab opens with, explained line by line:
it finds the repository folder by `models.env`, reads the settings, finds your key without printing it.
**Part B: Check Python and the pinned packages.** Python against the range in `pyproject.toml`, and every pin against
what the kernel has installed.
**Part C: Check that the key reaches the model.** One short request on `MODEL_DEFAULT`; prints the reply, the model
that answered, the tokens and the cost.
**Part D: Check the shop's database and documents.** `data/chinook.db`, opened read-only, and the 36 files in
`data/corpus/`.
**Part E: Check the optional tools, environments and keys.** Graphviz, Docker, the four own environments and the two
bonus keys, each reported as present or optional.
**Check that you are ready.** One line per check.

## Checkpoints

| After | You should see |
|---|---|
| Part A | `key found: yes`, with the model and reasoning effort from `models.env` |
| Part B | a Python inside `>=3.11,<3.15`; `19 pinned packages, 0 different` |
| Part C | a one-word reply (ours: `ready`), the model that answered, and its tokens (ours: 12 in, 4 out) |
| Part D | `59 customers, 412 invoices`; `36 files, 20 policies, 16 tickets` |
| Part E | a line per tool, environment and key: present, or optional and not set up |
| The last cell | ✅ on all five required lines |

## About the saved outputs

The saved outputs come from `gpt-6-luna`, the model in `models.env`, on Python 3.13 with the pinned packages. Your run
prints your own Python, Graphviz and Docker versions, and which optional pieces you set up.

## Troubleshooting the setup

The notebook ends with a table for failed checks. These are the problems that come before it, or while you choose the
kernel; each message was triggered on purpose and copied.

| Symptom | Cause | Fix |
|---|---|---|
| `uv: command not found` (zsh: `command not found: uv`) | the terminal was open before `uv` was installed, or `uv` is not on the `PATH` | open a new terminal; if it still fails, run the install command again and read its last lines for the folder to add to your `PATH`; if installs are blocked, use route D or B |
| `uv sync`: ``error: The requested interpreter resolved to Python 3.10.18, which is incompatible with the project's Python requirement: `>=3.11, <3.15` (from `project.requires-python`)`` | `--python` named a version outside the range | run `uv sync --python 3.13` |
| `pip install`: `ERROR: Ignored the following versions that require a different python version: ...` then `No matching distribution found for contourpy==1.3.3` | the virtual environment runs a Python older than 3.11 | delete `.venv`, install Python 3.13, create the environment again (route D, step 3) |
| Config cell: `ModuleNotFoundError: No module named 'dotenv'` | the notebook runs on a Python without the repository's packages | choose the repository's `.venv` as the kernel ([Choose the kernel](#choose-the-kernel)) |
| Part B: most packages `missing`, `openai` at `2.54.0` | the kernel is another lab's own environment (here lab 12's) | choose the `.venv` in the repository folder |
| Config cell: `StopIteration` | the notebook is not inside the repository folder (copied, downloaded alone or opened from elsewhere) | open it from the cloned or unzipped repository, where `models.env` sits |
| Config cell: `AssertionError: Put OPENAI_API_KEY in .env at the repository folder (copy .env.example).` | no `.env` beside `models.env` (or it was saved as `.env.txt`), or its key line is empty | copy `.env.example` to `.env` and paste the key; on Windows, turn on file name extensions to see the real name |
| Part E: `failed to connect to the docker API at unix:///...; check if the path is correct and if the daemon is running` | Docker is installed but not running, or `DOCKER_HOST` points to a socket that does not exist | start Docker Desktop (Linux: `sudo systemctl start docker`), or unset a stale `DOCKER_HOST` |
| Part E: `dot: not found`; lab 07: `ExecutableNotFound: failed to execute PosixPath('dot'), make sure the Graphviz executables are on your systems' PATH` | Graphviz is not installed, or not on the `PATH` the kernel sees | install it ([Optional tools](#optional-tools)), then restart the kernel |

## Resources

- [uv: installation](https://docs.astral.sh/uv/getting-started/installation/) and
  [working on projects](https://docs.astral.sh/uv/guides/projects/): `uv sync`, `uv run` and the lock file
- [Python: virtual environments](https://docs.python.org/3/library/venv.html): `python -m venv` and activation on each
  system
- [VS Code: Jupyter notebooks](https://code.visualstudio.com/docs/datascience/jupyter-notebooks): opening a notebook
  and choosing a kernel
- [GitHub: creating a codespace](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository)
- [OpenAI: models](https://developers.openai.com/api/docs/models) and
  [pricing](https://developers.openai.com/api/docs/pricing): the names and prices you can put in `models.env`

Next: [Lab 01: How to call a model and read the response](../01_Model_Call/README.md). Back to
[the lab list](../README.md).
