# Lab 00: How to set up the lab environment

**CPU | API key: `OPENAI_API_KEY` | one small model call**

## Goal

Set up this repository once, on a class VM, in GitHub Codespaces or on your own machine, and check in one run that
the core environment is ready. This README is the setup guide; the notebook, `00_environment_check.ipynb`, is the
checklist at the end: one cell per check, each with what a pass looks like. When its last cell shows ✅ on every
required line, you are ready for Lab 01.

## What you will learn

- How to get the repository (with `git clone` or as a ZIP) and install it with `uv`, or with `pip` where `uv` is
  blocked.
- How to open a notebook in VS Code (or JupyterLab) on the repository's own environment, the `.venv` kernel.
- Where the model settings live (`models.env`) and where your key lives (`.env`), and how to change the model in one
  line.
- Which labs need their own environment, and how to create one; which optional tools and keys exist, and which lab
  uses each.
- How to read the notebook's summary and fix a failed line from the troubleshooting tables.

## Choose a route

| Route | Use it when | You need |
|---|---|---|
| **A. Ubuntu VM with VS Code** | your class gives you a VM | the VM and an OpenAI key |
| **B. GitHub Codespaces** | you cannot install software, or the VM is not available | a GitHub account and an OpenAI key |
| **C. Your own machine with `uv`** (recommended for your own machine) | you can install a command-line tool | a terminal, VS Code or a browser, and an OpenAI key |
| **D. Your own machine with `pip`** | your machine does not allow `uv`, but has Python 3.11 to 3.14 | Python, a terminal and an OpenAI key |

Every route installs the same pinned package versions, from `uv.lock` or from `requirements.txt` (exported from the
same lock). The saved outputs in every lab come from these versions on Python 3.13, so your packages match the ones
behind them; the model's replies can still differ in wording.

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

A codespace is VS Code running on a GitHub machine with Ubuntu. You open it in your browser or from your desktop VS
Code.

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

Graphviz, Docker and Node.js are optional; see [Optional tools](#optional-tools).

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

Two small files in the repository folder hold the model settings and the key that every lab reads:

| File | Holds | Committed to Git? |
|---|---|---|
| `models.env` | the model names (`MODEL_DEFAULT`, `MODEL_STRONG`, `EMBEDDING_MODEL`; `GEMINI_MODEL` for the optional Gemini cells; `MODEL_COMPARE`, lab 21's second OpenAI model), `REASONING_EFFORT`, the prices per million tokens and lab 17's price per hosted container session | yes: no secrets in it |
| `.env` | your `OPENAI_API_KEY`, and the optional keys | never: `.gitignore` keeps it out |

**Add your key.** Copy the example file, then open `.env` in any editor and paste your key after `OPENAI_API_KEY=`
(no quotes, no spaces):

```bash
cp .env.example .env          # Windows: copy .env.example .env
```

Never paste a key into a notebook cell, and never print `.env`.

**Change the model in one line.** No notebook names a model in its code; every lab reads `MODEL_DEFAULT` from
`models.env`. To use another model in every lab, change that line (and the prices under it). To try a model on your
machine only, put a `MODEL_DEFAULT=...` line in your `.env`: a non-empty value there wins. A model without a reasoning
setting (such as `gpt-4o-mini`) also needs `REASONING_EFFORT=` empty in `models.env` itself: an empty value in `.env`
does not replace a setting. Another model words its replies differently, so in each lab check the facts a checkpoint
names, not the wording.

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

Three labs use libraries that need other versions of packages the main environment pins, so each has its own
`pyproject.toml`, `uv.lock` and `.venv` inside its folder. You create one only when you do that lab; the notebook
reports each as set up or "optional, not set up".

| Lab | Folder | Why it has its own environment |
|---|---|---|
| 08 | `08_Google_ADK` | Google ADK's OpenAI support needs `openai` 2.x; the main environment pins 3.x |
| B4 | `bonus/B4_CrewAI_Crew` | CrewAI needs `openai` 2.x and `mcp` 1.x, and a Python from 3.11 to 3.13 |
| B5 | `bonus/B5_Microsoft_Agent_Framework` | Agent Framework adds over a hundred packages, kept out of the main install |

To create one, run `uv sync --python 3.13` inside that lab's folder, for example:

```bash
cd 08_Google_ADK
uv sync --python 3.13
cd ..
```

Then open the lab's notebook in VS Code and choose **that folder's** `.venv` as the kernel (for example
`08_Google_ADK/.venv/bin/python`), not the one in the repository folder. Choosing the wrong one is easy to spot:
Lab 00 run on lab 08's environment says `not the repository's .venv` and reports most packages `missing`.
Where `uv` is blocked, each of the three labs' READMEs shows how to create the same environment with `pip` from that
lab's own `requirements.txt`.

## Optional tools

| Tool | Used by | Install |
|---|---|---|
| Graphviz (`dot`) | lab 07, to draw an agent's structure; only the drawing cells need it | Ubuntu: `sudo apt install -y graphviz`; macOS: `brew install graphviz`; Windows and others: [graphviz.org/download](https://graphviz.org/download/) |
| Docker | the optional last part of lab 17, which runs model-written code in a container on your machine; the rest of lab 17 runs on OpenAI's hosted code interpreter | [Docker Desktop](https://docs.docker.com/get-started/get-docker/) (macOS, Windows), or Docker Engine on Linux |
| Node.js 22.19 or newer (`node`, `npx`) | lab 06, to open its MCP server in the MCP Inspector; without it, two cells print one line and skip | [nodejs.org/en/download](https://nodejs.org/en/download) for every system; macOS: `brew install node`. A Linux distribution's own package can be older than 22.19: check with `node --version` |

After installing Graphviz or Node.js, restart the notebook's kernel so it sees the new program.

## Optional keys

Three keys are optional, and their lines are in `.env.example`: remove the `#` and paste the key after the `=` in
your `.env`.

| Key | Used by |
|---|---|
| `GEMINI_API_KEY` | the cells marked optional in labs 07, 08, 09 and 21, which run an agent or a call on a Google Gemini model |
| `PINECONE_API_KEY` | bonus B6, which needs a Pinecone account |
| `LANGSMITH_API_KEY` | bonus B7, which needs a LangSmith account |

Every core lab runs without them, and the notebook only says whether each is set, never its value.

## What the notebook checks

**Part A: Read the settings every lab starts from.** The config cell every lab opens with: it finds the repository
folder by `models.env`, reads the settings and finds your key without printing it. Then it prints every setting it
read, with what each one is for.

**Part B: Check the notebook's Python and the pinned packages.** Which Python runs the notebook (a pass is the
repository's `.venv`), its version against the range in `pyproject.toml`, and every pin against what that Python has
installed.

**Part C: Check that the key reaches the model.** It sends one short request to `MODEL_DEFAULT` and prints the reply,
the model that answered, the tokens and the cost.

**Part D: Check the shop's database and documents.** `data/chinook.db`, opened read-only, the 36 files in
`data/corpus/`, and the PDF in `data/documents/`.

**Part E: Check the optional tools, environments and keys.** Graphviz, Docker, Node.js, the three own environments
and the three optional keys, each reported as present or optional.

**Check that you are ready.** One line per check.

**What the config cell does.** A note under the checks that explains the config cell line by line.

## Checkpoints

| After | You should see |
|---|---|
| Part A | `key found: yes`, with the model and reasoning effort from `models.env`; twelve settings, `MODEL_DEFAULT` first |
| Part B | `kernel: .venv/bin/python \| the repository's .venv` (Windows: `.venv\Scripts\python.exe`); a Python inside `>=3.11,<3.15`; `23 pinned packages, 0 different` |
| Part C | a short greeting (ours: `Hello, welcome to our class today!`), the model that answered, and its tokens (ours: 16 in, 11 out) |
| Part D | `59 customers, 412 invoices`; `36 files, 20 policies, 16 tickets`; the governance guide `found` |
| Part E | a line per tool, environment and key: present, or optional and not set up |
| The last cell | ✅ on all seven required lines |

## About the saved outputs

The saved outputs come from `gpt-6-luna`, the model in `models.env`, on Python 3.13 with the pinned packages. Your run
prints your own Python, Graphviz, Docker and Node.js versions, and which optional pieces you set up.

## Troubleshooting the setup

The notebook ends with its own table for failed checks. This one starts with the problems that come before the
notebook runs (installing `uv` or the packages), then repeats the notebook's rows for the kernel, the config cell and
the optional tools. Each message is shown as the error prints it, with `...` where a long part is cut.

| Symptom | Cause | Fix |
|---|---|---|
| `uv: command not found` (zsh: `command not found: uv`) | the terminal was open before `uv` was installed, or `uv` is not on the `PATH` | open a new terminal; if it still fails, run the install command again and read its last lines for the folder to add to your `PATH`; if installs are blocked, use route D or B |
| `uv sync`: ``error: The requested interpreter resolved to Python 3.10.18, which is incompatible with the project's Python requirement: `>=3.11, <3.15` (from `project.requires-python`)`` | `--python` named a version outside the range | run `uv sync --python 3.13` |
| `pip install`: `ERROR: Ignored the following versions that require a different python version: ...` then `No matching distribution found for contourpy==1.3.3` | the virtual environment runs a Python older than 3.11 | delete `.venv`, install Python 3.13, create the environment again (route D, step 3) |
| Config cell: `ModuleNotFoundError: No module named 'dotenv'` | the notebook runs on a Python without the repository's packages | choose the repository's `.venv` as the kernel ([Choose the kernel](#choose-the-kernel)) |
| Part B: `kernel: .../08_Google_ADK/.venv/bin/python \| not the repository's .venv`, then most packages `missing` and `openai` at `2.54.0` | the kernel is not the `.venv` in the repository folder: another lab's own environment (here lab 08's), a system Python, or a conda environment or venv under another name | choose the `.venv` in the repository folder |
| Config cell: `StopIteration` | the notebook is not inside the repository folder (copied, downloaded alone or opened from elsewhere) | open it from the cloned or unzipped repository, where `models.env` sits |
| Config cell: `AssertionError: Put OPENAI_API_KEY in .env at the repository folder (copy .env.example).` | no `.env` beside `models.env` (or it was saved as `.env.txt`), or its key line is empty | copy `.env.example` to `.env` and paste the key; on Windows, turn on file name extensions to see the real name |
| Part E: `failed to connect to the docker API at unix:///...; check if the path is correct and if the daemon is running` | Docker is installed but not running, or `DOCKER_HOST` points to a socket that does not exist | start Docker Desktop (Linux: `sudo systemctl start docker`), or unset a stale `DOCKER_HOST` |
| Part E: `dot: not found`; lab 07: `ExecutableNotFound: failed to execute PosixPath('dot'), make sure the Graphviz executables are on your systems' PATH` | Graphviz is not installed, or not on the `PATH` the kernel sees | install it ([Optional tools](#optional-tools)), then restart the kernel |
| Part E: `node v20.11.0 \| older than 22.19, which the MCP Inspector needs` | the installed Node.js is too old for lab 06's MCP Inspector | install a current Node.js ([Optional tools](#optional-tools)), then restart the kernel |

## Resources

- [uv: installation](https://docs.astral.sh/uv/getting-started/installation/) and
  [working on projects](https://docs.astral.sh/uv/guides/projects/): `uv sync`, `uv run` and the lock file
- [Python: virtual environments](https://docs.python.org/3/library/venv.html): `python -m venv` and activation on each
  system
- [VS Code: Jupyter notebooks](https://code.visualstudio.com/docs/datascience/jupyter-notebooks): opening a notebook
  and choosing a kernel
- [GitHub: creating a codespace](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository)
- [Node.js: download](https://nodejs.org/en/download): the optional Node.js for lab 06's MCP Inspector
- [OpenAI: models](https://developers.openai.com/api/docs/models) and
  [pricing](https://developers.openai.com/api/docs/pricing): the names and prices you can put in `models.env`

Next: [Lab 01: How to call a model and read the response](../01_Model_Call/README.md). Back to
[the lab list](../README.md).
