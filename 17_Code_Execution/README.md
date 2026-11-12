# Lab 17: How to run model-written code safely

**CPU | API key: `OPENAI_API_KEY` | Optional: Docker, for one part of notebook 2 | Practises: letting a model answer with code it writes, running that code where it cannot reach your files, and checking where its numbers came from**

## Goal

Let a model answer questions by writing Python, run that Python on OpenAI's hosted code interpreter, and read
exactly what ran. The lab has two notebooks.

**Notebook 1** starts with forty coffee receipts. Asked for the total, the model writes a confident number that is
wrong. Given the code interpreter, it writes a few lines of Python instead, the code runs in a container on OpenAI's
side, and the total is right. Then we ask what that code could have reached if it had run on our machine. A probe we write ourselves, a few lines that ask whether `.env` is there and whether the network is
reachable, answers it from a subprocess on our machine and from the hosted container.

**Notebook 2** builds a chart agent for the Chinook music shop: the model reads the database through a `run_sql`
tool that runs in our notebook, and draws with the code interpreter. The chart of revenue by year is right, and its
code shows how the numbers got there: the model typed them in. One change to `run_sql` hands the rows to the code as
a file: the model never types the numbers into its code, and sees only what that code prints. An optional part, for readers with Docker, runs code a model wrote in a
container on your own machine and takes a look inside it.

## What you will learn

- Why a model's total of a long list of numbers cannot be trusted, and how to check it with Python.
- How to give a model OpenAI's hosted code interpreter on the Responses API, and read the call it made: the
  container, the code, what the code printed, and a chart returned as an image.
- What a subprocess on your own machine can reach, read from a probe we wrote, and why code a model wrote runs only
  in an isolated place: a hosted container, or a container with no network and one mounted folder.
- How to give one agent a function that runs in your Python and the hosted code interpreter, and read a run item by
  item.
- How to check where a chart's numbers came from, and how to hand a query's rows to the code as a file so the model
  never types them.
- (Optional, with Docker) How to run model-written code in a container with no network, a read-only root, limits, a
  user who is not root and one mounted folder.

## What you will do

### Notebook 1: meet the code interpreter with a month of coffee receipts (`17a_meet_code_execution.ipynb`)

**Part A: Ask the model to add up a month of coffee receipts.** Forty prices, Python's total, and the model's total
with no tools.
**Part B: Let the model write and run the code with the code interpreter.** The tool and its container settings,
the `code_interpreter_call` read field by field, and the code the model wrote.
**Part C: Get a chart back from the same container.** A follow-up with `previous_response_id`, the same container,
and the chart decoded from an image output.
**Part D: Test what code could reach on your machine, with a probe.** The probe in a subprocess with a working
folder, a timeout and a trimmed environment, then in the hosted container.
**Challenge.** Roll two dice 10,000 times in the hosted container, and find out which user the code runs as there.

### Notebook 2: the code interpreter at the Chinook desk (`17b_code_execution_at_the_desk.ipynb`)

**Part A: Work out the answer the chart must show.** The shop's revenue by year, from our own query.
**Part B: Build a chart agent from run_sql and the code interpreter.** `run_sql` on the read-only database, the two
tools, the loop that runs only our function's calls, and the agent's chart.
**Part C: Check where the chart's numbers came from.** The chart's code, and the totals the model typed into it.
**Part D: Hand the rows to the code instead of the model.** `run_sql` uploads the rows as a CSV file for the
container and tells the model only their shape; the same question again; the uploaded files deleted.
**Part E (optional): Run model-written code in a container on your own machine.** The image, the probe in a
container, a look inside it, and the chart code from Part B run there.
**Challenge.** A second chart with the rows handed to the code, and the container's limits tested.

### Going further

Notebook 1 adds up what its requests cost and names other hosted sandboxes. Notebook 2 reads the Dockerfile line by
line, says what each container flag stops, prices a chart, explains why running your own code on the hosted
interpreter means asking the model to copy it, and shows the same choice in the OpenAI Agents SDK's sandbox agents.

![Two paths from the database to the chart. Part B: run_sql sends the rows to the model as text, and the model types the numbers into the code it sends to the code interpreter. Part D: run_sql uploads the rows as a CSV file to the container and sends the model only their shape; the model writes code that reads the file, and what that code prints goes back to the model.](resources/lab17_data_paths.png)

## Checkpoints

| After | You should see |
|---|---|
| Notebook 1, Part A | Python's total $160.35; the model's total with no tools, a confident dollar amount that differs (ours: $158.60) |
| Notebook 1, Part B | items `code_interpreter_call` then `message`; code that types the forty prices into a list and adds them; printed `160.35` and a reply of $160.35 |
| Notebook 1, Part C | `same container as Part B: True`; an `image` output; a bar chart of the forty prices with a line at the average, about $4.01 |
| Notebook 1, Part D | from the subprocess `.env there: True`, `key in environment: False`, `network: reachable`; from the hosted container `True` for the code check, `working folder: oai`, `.env there: False`, `network: blocked, gaierror` |
| Notebook 2, Part A | 2009 $449.46, 2010 $481.45, 2011 $469.58, 2012 $477.53, 2013 $450.58 |
| Notebook 2, Part B | `attempt to write a readonly database` for the delete; one `run_sql` call, then a code interpreter run with an `image` output; a chart of five years |
| Notebook 2, Part C | the five totals typed into the chart's code: `totals typed in: 5 of 5` |
| Notebook 2, Part D | `run_sql` returns `5 rows, columns year, revenue, ...`; code that reads the CSV file; `totals typed in: 0 of 5`; the same five bars; the uploaded files deleted |
| Notebook 2, Part E (optional) | Docker's version or a skip line; Python 3.13.18, matplotlib 3.11.2, user `sandbox`; the probe `.env there: False`, `network: blocked, gaierror`; `Read-only file system` for `/etc`; the chart saved by the container |
| Challenges | notebook 1: a count of sevens near 1,667 (ours 1,649), one container for both requests, the user `oai`; notebook 2: `0 of 5` country totals typed in with the USA highest at $523.06, and exit codes 124 and 137 |

**About the saved outputs.** They come from `gpt-6-luna`, the model `models.env` names, and from Docker 29.9.2 for
the optional part. The model writes different code, queries and replies on every run, so compare the shape of the
results, not the words: with no tools, the model's coffee total was wrong in every one of the eleven runs we made
(between $157.20 and $160.00), and the chart agent typed all five totals into its code in every run before the
change to `run_sql` and none after. Asked to run code exactly as written, the model usually copies it unchanged, but
not always: notebook 1's probe came back unchanged in all 4 test runs and in the saved run; a shorter probe of three lines
came back changed in 1 of 2 runs; and in a probe with the line `from pathlib import Path`, that line came back as
`from pathlib import import Path` in 10 of 11 runs. That is why notebook 1 compares `call.code` with what it sent.
The probe's answers in each place do not change from run to run.

## Before you start

- **Lab 00 first.** It checks the environment, that your key reaches the model, and whether Docker is running.
- **Run it locally:** in the repository folder, `uv sync` (or `pip install -r requirements.txt`), put
  `OPENAI_API_KEY` in `.env` (copied from `.env.example`), then open a notebook in VS Code or JupyterLab
  (`uv run jupyter lab`) with the `.venv` kernel. Run the setup cells first. Each notebook runs on its own.
- **Model-written code never runs on your machine outside a container.** In notebook 1 the only code that runs in a
  subprocess is the probe, fixed text written in the notebook, which checks whether `.env` exists and never opens
  it. Everything the model writes runs in OpenAI's hosted container, or, in notebook 2's optional Part E, in a
  Docker container with no network.
- **Docker is optional.** Only notebook 2, Part E and the second challenge task use it, and they print a skip line
  without it. With Docker running, Part E builds the image `chinook-sandbox` from `resources/Dockerfile` (about 320
  MB; the first build downloads the Python image and installs matplotlib, so it needs the internet once). To build it
  yourself, from the repository folder: `docker build -t chinook-sandbox 17_Code_Execution/resources`.
- **Stored on OpenAI's side:** notebook 2, Part D uploads small CSV files (`purpose="user_data"`) and deletes them at
  the end of the part. Run that cell. Containers expire on their own after 20 minutes without use.
- **Files it writes:** `17_Code_Execution/outputs/` (git ignores it): the probe, the charts and, in Part E, the code
  the container ran. It is the one folder mounted in the container, as `/work`. `data/chinook.db` is only ever opened
  read-only. The solutions write to `17_Code_Execution/solved/outputs/` the same way, and the second solution mounts
  that folder in the container.
- **Cost:** each request that runs code starts or reuses a container, and each container session costs
  `PRICE_CONTAINER_SESSION_USD` in `models.env` (up to $0.03 for 1 GB); the tokens add a fraction of a cent. Each
  notebook uses two sessions, at most 6 US cents, and the two solutions three more between them.

## Folder contents

| Path | What it is |
|---|---|
| `17a_meet_code_execution.ipynb` | notebook 1, the coffee receipts and the probe, with saved outputs |
| `17b_code_execution_at_the_desk.ipynb` | notebook 2, the chart agent at the Chinook desk, with saved outputs |
| `resources/Dockerfile` | the sandbox image: Python 3.13.18, matplotlib 3.11.2, a user who is not root |
| `resources/lab17_data_paths.mmd` and `.png` | the two paths from the database to the chart: its mermaid source and the exported image |
| `solved/17a_meet_code_execution_solution.ipynb` | notebook 1's challenge solved, run with its outputs |
| `solved/17b_code_execution_at_the_desk_solution.ipynb` | notebook 2's challenge solved, run with its outputs |

## Resources

- [OpenAI: code interpreter](https://developers.openai.com/api/docs/guides/tools-code-interpreter): the tool, auto
  containers and their reuse, memory sizes, the 20-minute expiry, files in the container
- [OpenAI: create a file](https://developers.openai.com/api/reference/resources/files/methods/create): `files.create`
  and its `purpose`
- [OpenAI: pricing, built-in tools](https://developers.openai.com/api/docs/pricing): the container session prices
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html): `run`, `cwd`, `env`, `timeout`
- [Docker: `docker container run`](https://docs.docker.com/reference/cli/docker/container/run/): every flag used in
  notebook 2, Part E
- [Docker: resource constraints](https://docs.docker.com/engine/containers/resource_constraints/): `--memory`,
  `--memory-swap`, `--cpus`
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/): `FROM`, `RUN`, `USER`, `ENV`, `WORKDIR`
- [OpenAI Agents SDK: sandbox agents](https://openai.github.io/openai-agents-python/sandbox_agents/) and
  [sandbox clients](https://openai.github.io/openai-agents-python/sandbox/clients/): where a sandbox agent's commands
  run, locally, in Docker or with a hosted provider
- [gVisor](https://gvisor.dev/docs/) and [Firecracker](https://firecracker-microvm.github.io/): two ways to isolate code more
  strongly than a container, without a full virtual machine

Next: [Lab 18: How to choose an agent design](../18_Agent_Designs/README.md). Back to [the lab list](../README.md).
