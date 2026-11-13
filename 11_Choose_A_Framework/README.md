# Lab 11: How to choose an agent framework

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
- Where you watch a run in each framework (a browser development UI, a trace page, an event stream, or a drawn graph).
- Why LiteLLM is not an agent framework, and how it sits under any framework to translate model provider APIs.
- How to find what a framework decides for you (which API it calls, a default model, a reasoning effort, what it
  counts) before that decision reaches production.
- What six criteria (easy to learn, control of the loop, multi-agent, pause and approve, tracing built in, any model
  vendor) mean in practice, with the evidence from this repository's runs.
- How to turn a job's needs into must-haves and weights, score the frameworks for it and reach a pick.
- When your own loop is the right choice, and which answer would make you change a pick later.
- What a wrong pick costs, and which parts of an agent move to another framework and which stay behind.

## Coming from

Lab 03 wrote the agent loop by hand; Lab 07 ran the same desk agent in the OpenAI Agents SDK, Lab 08 in Google ADK,
Lab 09 in LangChain, and Lab 10 in LangGraph. Lab 14 rebuilt a search agent in LlamaIndex, Lab 18 measured when a second agent pays, and the bonus
labs built the desk again in Pydantic AI (B3), CrewAI (B4) and Microsoft Agent Framework (B5), with
durable pauses in LangGraph (B1) and approvals in the Agents SDK (B2). This guide reads their saved runs side by side.
It re-teaches each idea it uses in a sentence, so it can be read on its own, and it names the lab and part behind
every number so you can open the run.

## What you will do

Open [GUIDE.md](GUIDE.md) and work through it, writing each answer down before you read ours.

**Opening: an everyday choice first.** A homework helper that must ask a parent before it sends an email: one must-have (it waits for a person), one filter, a pick. Then the desk's refund.
**Part A: See the same loop inside every framework.** The four things every framework does for us, then the desk
agent's definition across frameworks: a model, instructions and tools in every one. LiteLLM as an adapter underneath them.
**Part B: Compare the same agent's runs across frameworks.** The Helena question's requests and where you watch a run across builds, then the decision each framework made for us that a lab had to find. Measured tokens and costs gathered in the Appendix.
**Part C: Read the six criteria on the Chinook desk.** What each criterion means on a real request, the runs that
show it, and the needs the six leave out (environment isolation, team language, document retrieval).
**Part D: Score the frameworks for the support desk.** The scorecard, the six questions that turn the desk into
must-haves and weights, the worked pick, and the answers that would change it.
**Part E: Decide what a wrong pick costs and what changes later.** What moves to another framework and what stays
behind, what changed in the last year, and what popularity measures.
**Part F: Choose for three jobs.** A worksheet on three more jobs at the shop, with worked answers to open
afterwards.
**Challenge.** Score and choose for a project of yours, and re-check one fact for your pick.
**Appendix.** Measured token and cost checkpoints from Labs 03, 07–10, 14, and B1–B5.

![How to choose a framework in five steps, each beside the Chinook support desk's answer: the six questions; filter on the must-haves; weigh and add up; read the evidence; pick and write down what would change it. The desk's pick is LangChain create_agent with an approval pause and a checkpointer that outlives the process](resources/lab11_choosing.png)

## Checkpoints

| After | You should have |
|---|---|
| Part A | the four things every framework does for us; a model, instructions and tools in all definitions; why LiteLLM sits under a framework; what `model_settings`, `output_type` and `deps_type` each add |
| Part B | 3 model requests for every build with one agent; where you watch a run in each framework; one default found by a lab in each framework |
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
- The guide is easiest after you have built or read one framework lab (07 to 10), but each idea it uses is explained
  where it appears. To see a run it quotes, open the notebook of the lab it names; the saved outputs are in the file.

## Folder contents

| Path | What it is |
|---|---|
| `GUIDE.md` | the reading guide, with the worksheet, worked answers and token appendix |
| `resources/lab11_choosing.mmd` and `.png` | the five-step choice with the desk's answers: its mermaid source and the exported image |
| `solved/11_choose_a_framework_solution.md` | the Challenge worked for a damaged-media desk at the Chinook shop |

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
- [LiteLLM](https://docs.litellm.ai/docs/)
- [Stack Overflow Developer Survey 2026, AI](https://survey.stackoverflow.co/2026/ai)

Next: [Lab 12: How to answer from documents with retrieval](../12_Retrieval/README.md). Back to [the lab list](../README.md).
