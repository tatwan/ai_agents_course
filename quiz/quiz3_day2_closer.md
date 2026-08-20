# The Grand Finale: Two Days, One Loop
# Score 100

# Section: Foundations Callback
> One last lap through Day 1 before we close the book.

## Q1: The question that separates a chatbot, a workflow, and an agent is...
- [x] Who decides the next step — you, or the model?
- [ ] How many tools are wired up?
- [ ] Whether it's built with a framework?
- [ ] How long the system prompt is?
::time=30

## Q2: When the model "calls a tool," what actually happens first?
- [ ] It runs the Python function itself, right away
- [x] It emits a name and a JSON string — your code decides whether to run anything
- [ ] It writes directly to your database
- [ ] It sends its own request to the tool's server
::time=35

## Q3: The ReAct loop, in order, is...
- [ ] Action, Observation, Thought, stop
- [ ] Plan, Execute, Done
- [x] Thought, Action, Observation, repeat
- [ ] Observation, Action, Thought, repeat
::time=30

## Q4: Why does MCP exist?
- [ ] To make the OpenAI API cheaper
- [ ] To replace tool calling entirely
- [ ] To give models direct internet access
- [x] So a tool's implementation can live in another process or host, instead of copy-pasted into every project
::time=35

# Section: Day 2 Deep Cuts
> The last twenty-four hours, compressed into one grueling gauntlet.

## Q5: Context engineering's core lesson was...
- [x] The message list is a budget — every turn's history costs tokens, so you manage what stays on it
- [ ] Longer prompts always produce better answers
- [ ] Context windows are effectively unlimited
- [ ] The system prompt is free and doesn't count toward cost
::time=40

## Q6: Why did we go from `def` to `async def` to `gather`?
- [ ] To make the code shorter
- [x] To run independent tool calls concurrently instead of waiting on each one in turn
- [ ] To avoid needing an API key
- [ ] To reduce the number of tokens used
::time=35

## Q7: What does LangGraph add on top of the plain SDK loop?
- [ ] It removes the need for tools entirely
- [ ] It's just a faster HTTP client
- [x] An explicit graph you draw yourself, with the ability to pause and resume a run
- [ ] It only works with open-source models
::time=40

## Q8: The key lesson about letting a model write and run its own code was...
- [ ] Model-written matplotlib code is always safe to run directly
- [ ] Models can only write code, never execute it
- [ ] Sandboxing charting code is unnecessary
- [x] A timeout is not a sandbox — you need real isolation
::time=35

## Q9: A basic retrieval (RAG) pipeline works by...
- [x] Retrieving relevant chunks, then generating an answer grounded in them
- [ ] Fine-tuning the model on your documents
- [ ] Pasting every document into the system prompt
- [ ] Letting the model guess from training data alone
::time=35

## Q10: True or false — every question we asked against the policy corpus in the retrieval module had a findable answer.
- [ ] True
- [x] False
::time=25

## Q11: What makes agentic RAG different from plain retrieval?
- [ ] It skips retrieval entirely
- [x] Retrieval becomes a tool the agent can call, possibly more than once
- [ ] It requires a larger vector database
- [ ] It removes the LLM from the loop
::time=35

## Q12: The delegation module compared...
- [ ] CrewAI installed side by side with LangGraph
- [ ] Azure hosting versus AWS hosting
- [x] One agent with three tools versus multiple overlapping specialist agents
- [ ] Sync tool calls versus async tool calls
::time=35

## Q13: The attack demonstrated in the security module was...
- [ ] A SQL injection against the Chinook database
- [ ] A brute-force attack on the API key
- [ ] A denial-of-service against the MCP server
- [x] Indirect prompt injection hidden inside a retrieved document
::time=40

## Q14: The evals module built...
- [x] A per-turn cost ledger, plus a checker that verifies named facts
- [ ] A leaderboard ranking employees
- [ ] A single pass/fail flag with no detail
- [ ] A billing dashboard hosted by OpenAI
::time=40

## Q15: What's true about Azure in this course?
- [ ] Every module requires an Azure account
- [x] It's used only in the platform-landscape module and optional instructor demos — no student needs a credential
- [ ] Azure replaces OpenAI as the LLM provider from that module on
- [ ] AWS is the primary cloud used throughout the course
::time=35

# Section: Grand Finale
> Ungraded. Just for the room.

## Q16: Two days in — chatbot, workflow, or agent: which one are you right now?
::type=ungraded
- [ ] Workflow — someone please hand me a checklist
- [x] Agent — I'll decide my next step, thanks
- [ ] Chatbot — I can talk, don't ask me to do anything
- [ ] Still loading
::time=20
