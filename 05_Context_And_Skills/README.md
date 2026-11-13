# Lab 05: How to manage what an agent sees

**CPU | API key: `OPENAI_API_KEY` | Practises: how an agent works from the inside (our code decides what the model reads on each call); costing an agent**

## Goal

A model keeps nothing between calls: everything it needs has to be in the request, and we pay for every token of
it, every time. Learn to choose what goes in. The lab has two notebooks and two extra ones.

**Notebook 1** is a playground. We are away for the weekend, a friend looks after the flat and the cat, and a model
answers her questions from our notes. First it has no notes and cannot say how much to feed the cat. Then it gets
every note in its system prompt, and every question pays for all of them. Then it gets a short list and one tool,
`open_note`, and asks for the one note it needs. Give the notes names that say nothing and it opens notes it does
not need. Last, a note becomes an **Agent Skill**: a folder with a `SKILL.md`, in the format coding agents read.

**Notebook 2** takes skills to the Chinook music shop's support desk. The shop's rules are three skills. From
three one-line descriptions the model asks for the refund skill, reads it, and then asks on its own for the
reference file the skill points to. A question about a customer's invoices loads no skill at all. At the end the
same agent is set beside one that carries every rule in its system prompt.

## What you will learn

- How to read from `usage.prompt_tokens` what one call sent to the model, and why a long system prompt is paid for
  on every call.
- How to give a model a list and one tool, and write the small loop that runs what it asks for.
- Why the names and descriptions in the list decide what the model opens.
- How to write and read an Agent Skill: the `SKILL.md` frontmatter with `name` and `description`, the body, and
  reference files.
- How to load skills in three levels (the list in every call, a body on request, a reference when the body points
  to it), beside an agent's ordinary lookup tools.
- How to compare a prompt that lists skills with one that carries every rule, and say what each cannot do.

## What you will do

### Notebook 1: meet context and skills on a house-sitter's notes (`05a_meet_context_and_skills.ipynb`)

**Part A: Ask a question the model cannot answer alone.** One model call with no notes, and the input tokens it
sent.
**Part B: Put every note in the system prompt, and count what each question costs.** The nine notes, all of them
in one system prompt (the **fat prompt**), two questions and their input tokens.
**Part C: Keep a list on the fridge and let the model open one note.** The list, `open_note` called by hand, its
tool schema, the **thin prompt** (the rules and the list, with no note in it), the model's request, our code
sending the note back, then the same steps in a loop.
**Part D: See what the model opens when the list says nothing.** The same notes relabelled `note-1` to `note-9`.
**Part E: Turn a note into an Agent Skill folder.** The folder, `SKILL.md` read in Python, the list built from the
folders, the three levels, and the model loading the cat skill.
**Challenge.** A question that reaches level 3, and a skill of your own.

### Notebook 2: context and skills at the Chinook desk (`05b_context_and_skills_at_the_desk.ipynb`)

**Part A: Read the desk's rules as three skills.** The `skills/` folder, the skill list built from it, and the two
functions that load the rest.
**Part B: Watch the model go from the list to a skill to its reference file.** The duplicate-charge question, one
call at a time.
**Part C: Ask a question that needs a lookup and no skill.** The three database lookups beside the skill tools,
the loop, and Helena's invoices.
**Part D: Compare the skill list with every rule in the system prompt.** The fat prompt on the same question, and
the input tokens of both.
**Part E: Ask both agents about a rule that no skill covers.** Support hours, a question the fat prompt answers and
the thin prompt cannot.
**Challenge.** A fourth skill, and how much of the model's choice the name carries.

### Going further

- `house_agent/`: the house-sitter's three skills set up for any coding agent, with an `AGENTS.md` that
  says how to use them. Open your coding agent in that folder and begin the prompt with *Start by reading AGENTS.md.* The
  full prompt and what to expect are in notebook 1, Going further.
- `05_extra_prompt_caching.ipynb`: what the API charges when the same long prompt is sent again (cache writes and
  reads, the 1,024-token minimum), and what a fat prompt costs over five questions.
- `05_extra_compaction.ipynb`: replacing old messages with a summary, what that keeps and loses, and which
  messages must stay so that the agent does not load its skills again.

Each of the four notebooks runs on its own.

![The three levels of an Agent Skill: the skill list in every call, the SKILL.md body on request, a reference file when the body points to it](resources/lab05_three_levels.png)

## Checkpoints

| After | You should see |
|---|---|
| Notebook 1, Part A | a reply that says it does not have the feeding instructions; about 47 input tokens |
| Notebook 1, Part B | half a cup at 7 in the morning and at 6 in the evening; the wifi password `mochi-2019`; about 995 input tokens on each call |
| Notebook 1, Part C | first reply with no text and one request, `open_note` with `{"name":"cat"}`; about 370 input tokens, then about 535 with the note; the loop opening only `wifi` for the wifi question |
| Notebook 1, Part D | notes opened that the question does not need (ours: all nine, three calls, 1,536 input tokens on the last), and the same answer |
| Notebook 1, Part E | the frontmatter as a dictionary with `name` `cat`; a list of three skills; `load_skill` with `cat` and no `read_skill_file` for the feeding question |
| Notebook 2, Part A | three skill folders and one reference file; three lines in the list; `No such file in this skill.` for a path that leaves the folder |
| Notebook 2, Part B | call 1: `load_skill` with `refund-requests`; call 2: `read_skill_file` with `references/duplicate-charges.md`; call 3: refund the later invoice in full, both numbers on the request (ours: 499, 750 and 1,003 input tokens) |
| Notebook 2, Part C | Helena Holý: customer 6, 7 invoices, $49.62, Steve Johnson; `find_customer`, then `get_invoices` and `get_support_rep`; no `load_skill` |
| Notebook 2, Part D | the same three facts from both agents; input tokens per call about 600 to 760 with the thin prompt and about 2,440 to 2,600 with the fat one (ours: 2,005 against 7,525 for the question) |
| Notebook 2, Part E | support hours (Monday to Friday, 09:00 to 17:00) answered by the fat agent only; the thin agent says its rules do not cover it |
| Prompt caching | first call: `cache_write_tokens` 1,453 of 1,456 and `cached_tokens` 0; second call the other way round; a sentence in front of the prompt: nothing cached; a 48-token prompt: never cached; five questions: 65% of the input cost saved |
| Compaction | the summary names invoices 58217 and 58211 and 9.99; after the summary alone, and with the skill text pasted in, `load_skill` and `read_skill_file` again; with the original load messages kept, no tool call and one call |
| Challenges | notebook 1: `load_skill` with `cat`, then `read_skill_file` with `references/when-she-is-ill.md`; the bins question loads only `bins`. Notebook 2: the download question loads only `digital-downloads`; with numbered skill names the model loads all three skills, five calls instead of three |

**About the saved outputs.** They come from `gpt-6-luna` with reasoning effort `none`, as set in `models.env`. The
model chooses its tool calls and writes its replies on every run, so wording will differ on yours, and token counts
can move by a few. Check the tool calls and the facts. What did not vary in our runs: the cat's note alone for the
feeding question (10 of 10), and the refund skill followed by its reference for the duplicate charge (11 of 11).
What did: with numbered labels the model opened all nine notes in 4 runs of 7 and six of them, one at a time, in
the other 3. In the compaction notebook the agent loaded the refund skill again after the summary alone and after
the pasted text (6 of 6 each), never with the original load messages kept (0 of 6), and in 4 runs of 6 even with
the whole conversation.

## Before you start

- **Lab 00 first.** It checks the environment and that your key reaches the model.
- **Run it locally:** in the repository folder, `uv sync` (or `pip install -r requirements.txt`), put
  `OPENAI_API_KEY` in `.env` (copied from `.env.example`), then open a notebook in VS Code or JupyterLab
  (`uv run jupyter lab`) with the `.venv` kernel. Run the setup cell first.
- **`REASONING_EFFORT=none` in `models.env`.** On the Chat Completions API this model calls tools only with that
  setting.
- **Data:** the house-sitter's notes in `house_notes/` and `house_skills/`, the desk's skills in `skills/`, and for
  notebook 2 `data/chinook.db` (opened read-only) and the 20 policy files in `data/corpus/`. Nothing is written.
- **Cost:** about 55 model calls over the four notebooks, under one US cent with the prices in `models.env`.

## Folder contents

| Path | What it is |
|---|---|
| `05a_meet_context_and_skills.ipynb` | notebook 1, the playground, with saved outputs |
| `05b_context_and_skills_at_the_desk.ipynb` | notebook 2, the Chinook desk, with saved outputs |
| `05_extra_prompt_caching.ipynb` | going further: what a repeated long prompt costs |
| `05_extra_compaction.ipynb` | going further: compacting a conversation and keeping loaded skills |
| `house_notes/` | the nine notes of notebook 1, one file per subject |
| `house_skills/` | three of those notes as Agent Skills: `cat` (with `references/when-she-is-ill.md`), `plants`, `wifi` |
| `house_agent/` | the same three skills in `.agents/skills/`, with an `AGENTS.md` that tells a coding agent how to use them (notebook 1, Going further) |
| `skills/` | the desk's three skills: `refund-requests` (with `references/duplicate-charges.md`), `damaged-media`, `account-changes` |
| `resources/house_skill_three_levels.mmd`, `.png` | the three levels on the cat skill, source and exported image |
| `resources/lab05_three_levels.mmd`, `.png` | the three levels on the duplicate-charge question, source and exported image |
| `solved/05a_meet_context_and_skills_solution.ipynb` | notebook 1's challenge solved, run with its outputs |
| `solved/05b_context_and_skills_at_the_desk_solution.ipynb` | notebook 2's challenge solved, run with its outputs |
| `solved/my_house_skills/bins/SKILL.md`, `solved/my_skills/digital-downloads/SKILL.md` | the skills the two solutions add |

## Resources

- [Agent Skills: what skills are](https://agentskills.io/what-are-skills) and
  [the specification](https://agentskills.io/specification): the folder, the frontmatter fields and their limits,
  the three levels
- [Agent Skills: adding skills support to an agent](https://agentskills.io/client-implementation/adding-skills-support):
  the skill list, the loading tool, and protecting loaded skills from compaction
- [Claude Code: skills](https://code.claude.com/docs/en/skills),
  [Codex: skills](https://developers.openai.com/codex/skills) and
  [VS Code: agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills): where three coding
  agents read skill folders from
- [AGENTS.md](https://agents.md) and [Claude Code: AGENTS.md](https://code.claude.com/docs/en/memory#agents-md): the
  instruction file coding agents look for in a project, and when Claude Code reads it
- [OpenAI: skills](https://developers.openai.com/api/docs/guides/tools-skills): the same folders used by a hosted
  agent on the Responses API
- [OpenAI: function calling](https://developers.openai.com/api/docs/guides/function-calling): tool schemas and tool
  calls
- [OpenAI: prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching): the 1,024-token minimum,
  cache writes and reads, `prompt_cache_key`
- [OpenAI: compaction](https://developers.openai.com/api/docs/guides/compaction): compaction on the server
- [OpenAI: Chat Completions API reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create):
  `messages`, `tools`, `usage`

Next: [Lab 06: How to share tools with MCP](../06_MCP/README.md). Back to [the lab list](../README.md).
