# Lab 09: How to choose an agent framework

**A reading guide | No code, no key, nothing to install | Practises: comparing frameworks on runs of the same agent; turning a job's needs into a scored, defended choice**

## Goal

Choose an agent framework for a job and defend the choice with evidence: what the job needs, what each framework
adds, and what each one decides for you without asking. The moment that teaches it is Part B: the Chinook desk
agent, run on the same question in our own loop and in seven frameworks across this repository's labs, makes the same
three model requests and returns the same three facts in every build with one agent. The loop is the same
everywhere; what differs is what each framework does around it, and in every lab one of those things only showed up
because the lab printed what came back. Part D scores the frameworks for the shop's support desk and shows that the
pick turns on one question: how long a refund request waits for a person's approval.

## What you will learn

- How to recognise the agent loop inside any framework, and read a framework's run as model requests, tokens and
  tool calls.
- How to find what a framework decides for you (which API it calls, a default model, a reasoning effort, what it
  counts) before that decision reaches production.
- What six criteria (easy to learn, control of the loop, multi-agent, pause and approve, tracing built in, any model
  vendor) mean in practice, with the evidence from this repository's runs.
- How to turn a job's needs into must-haves and weights, score the frameworks for it and reach a pick.
- When your own loop is the right choice, and which answer would make you change a pick later.
- What a wrong pick costs, and which parts of an agent move to another framework and which stay behind.

## Coming from

Lab 04 wrote the agent loop by hand; lab 07 ran the same desk agent in the OpenAI Agents SDK and lab 08 in LangChain
and LangGraph. Lab 12 rebuilt a search agent in LlamaIndex, lab 16 measured when a second agent pays, and the bonus
labs built the desk again in Google ADK (B3), Pydantic AI (B4), CrewAI (B5) and Microsoft Agent Framework (B6), with
durable pauses in LangGraph (B1) and approvals in the Agents SDK (B2). This guide reads their saved runs side by side.
It re-teaches each idea it uses in a sentence, so it can be read on its own, and it names the lab and part behind
every number so you can open the run.

## What you will do

Open [GUIDE.md](GUIDE.md) and work through it, writing each answer down before you read ours.

**Part A: See the same loop inside every framework.** The four things every framework does for us, then the desk
agent's definition in seven frameworks: a model, instructions and tools in every one.
**Part B: Compare the same agent's runs across frameworks.** The Helena question's requests and tokens in eight
builds, then the decision each framework made for us that a lab had to find.
**Part C: Read the six criteria on the Chinook desk.** What each criterion means on a real request, the runs that
show it, and the needs the six leave out.
**Part D: Score the frameworks for the support desk.** The scorecard, the six questions that turn the desk into
must-haves and weights, the worked pick, and the answers that would change it.
**Part E: Decide what a wrong pick costs and what changes later.** What moves to another framework and what stays
behind, what changed in the last year, and what popularity measures.
**Part F: Choose for three jobs.** A worksheet on three more jobs at the shop, with worked answers to open
afterwards.
**Challenge.** Score and choose for a project of yours, and re-check one fact for your pick.

![How to choose a framework in five steps, each beside the Chinook support desk's answer: the six questions; filter on the must-haves; weigh and add up; read the evidence; pick and write down what would change it. The desk's pick is LangChain create_agent with an approval pause and a checkpointer that outlives the process](resources/lab09_choosing.png)

## Checkpoints

| After | You should have |
|---|---|
| Part A | the four things every framework does for us; a model, instructions and tools in all seven definitions; what `model_settings`, `output_type`, `deps_type` and `output_key` each add |
| Part B | 3 model requests for every build with one agent and 5 for the CrewAI crew; input tokens of 1,006, 845 and 1,127 for the same instructions in labs 04, 07 and B3, all fractions of a cent; one default found by a lab in each of three frameworks |
| Part C | each criterion's meaning on the desk with one run that shows it; one need the six leave out (an environment of its own, the team's language, documents) |
| Part D | the filter keeping LangChain, LangGraph and Microsoft Agent Framework; LangChain's total of 33 out of 36 worked by hand; the pick, LangChain's `create_agent` with an approval pause and a lasting checkpointer; the Agents SDK when a rep approves on the spot |
| Part E | each part of the desk marked as moving or staying behind, with its condition; one change of the last year and what it left behind; what stars, downloads and a survey share each measure |
| Part F | job 1 decided by documents, job 2 by the multi-agent pattern it needs (a handoff), job 3 by the team's language, as in the worked answers |
| Challenge | a scorecard re-scored and weighted for your project, a pick that passes your filter with a tie-break that names evidence, and one fact re-checked with today's date |

**About the numbers.** Every measured number comes from a saved run in the lab named beside it, made with
`gpt-6-luna` at reasoning effort `none`; tokens and wording change from run to run and model to model, the shape of
each run does not. The scorecard is the instructor's assessment in October 2026, a judgement and not a benchmark.
Framework facts (stars, downloads, versions, statuses) carry the date they were read and a link; check one before you
rely on it.

## Before you start

- Nothing to install and no key: the guide runs no code. A text editor or paper for your answers is enough.
- The guide is easiest after you have built or read one framework lab (07 or 08), but each idea it uses is explained
  where it appears. To see a run it quotes, open the notebook of the lab it names; the saved outputs are in the file.

## Folder contents

| Path | What it is |
|---|---|
| `GUIDE.md` | the reading guide, with the worksheet and its worked answers |
| `resources/lab09_choosing.mmd` and `.png` | the five-step choice with the desk's answers: its mermaid source and the exported image |
| `solved/09_choose_a_framework_solution.md` | the Challenge worked for a damaged-media desk at the Chinook shop |

## Resources

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) and its
  [guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)
- [LangChain: agents](https://docs.langchain.com/oss/python/langchain/agents),
  [human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) and
  [LangGraph checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers)
- [LlamaIndex: agents](https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/)
- [CrewAI: crews](https://docs.crewai.com/en/concepts/crews)
- [Microsoft Agent Framework: workflow checkpoints](https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints)
- [Google ADK: agents](https://adk.dev/agents/llm-agents/)
- [Pydantic AI: agents](https://pydantic.dev/docs/ai/core-concepts/agent/)
- [Stack Overflow Developer Survey 2026, AI](https://survey.stackoverflow.co/2026/ai)

Next: [Lab 10: How to answer from documents with retrieval](../10_Retrieval/README.md). Back to [the lab list](../README.md).
