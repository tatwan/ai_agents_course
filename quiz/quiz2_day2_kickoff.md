# Day 2 Kickoff: The Day 1 Rewind
# Score 100

# Section: Warm-up
> Just for fun. No wrong answer here, but pick one.

## Q1: True or False — you learned at least one thing yesterday you didn't know walking in.
::type=ungraded
- [ ] False
- [x] True
::time=15

# Section: Day 1 Rewind
> Graded. One point each. Same words the notebooks used — no trick questions.

## Q2: What is an LLM actually doing, one call at a time?
- [x] Predicting the next token, given everything so far
- [ ] Looking up the answer in a curated database
- [ ] Executing Python code behind the scenes
- [ ] Browsing the web in real time for the answer
::time=30

## Q3: True or false — an LLM remembers what you said in a previous, separate `create()` call.
- [x] False
- [ ] True
::time=25

## Q4: When the model "calls a tool," what actually happens first?
- [ ] It runs the matching Python function right away, no check needed
- [x] It emits a name and JSON arguments for your code to run
- [ ] It opens the database and pulls the matching row itself
- [ ] It sends its own request straight to the tool's server
::time=40

## Q5: So how does a chatbot seem to "remember" the conversation?
- [ ] The model saves your session on OpenAI's servers
- [ ] The API auto-caches your last few turns for you
- [x] Your code resends the whole message history on every turn
- [ ] It doesn't — the illusion has no real mechanism
::time=35

## Q6: True or false — an LLM can list a folder, read a disk, or run a test on its own.
- [ ] True
- [x] False
::time=25

## Q7: In the ReAct pattern, what's the loop order?
- [ ] Action, then Thought, then a Final Answer
- [ ] Observation, then Thought, then Action, then stop
- [ ] Plan once, then Execute, then Done
- [x] Thought, then Action, then Observation, then repeat
::time=35

## Q8: What's the real difference between ReAct and the official tool-calling loop?
- [x] Same loop shape — ReAct narrates the reasoning as text; the official loop hides it inside the model
- [ ] ReAct doesn't use any tools at all
- [ ] The official loop is one call, not a loop
- [ ] ReAct only works for coding agents
::time=45

## Q9: What's the one question that decides chatbot vs workflow vs agent?
- [ ] How many tools are wired up?
- [x] Who decides the next step — you, or the model?
- [ ] Which programming language it's written in?
- [ ] How expensive each API call runs?
::time=35

## Q10: An LLM on its own — one call, no loop, no tools — is best described as...
- [ ] Always an agent, by definition
- [ ] A workflow
- [ ] A database with extra steps
- [x] A stateless text predictor, not an agent
::time=30

## Q11: What does the OpenAI Agents SDK's `@function_tool` decorator actually give you?
- [ ] It runs your function inside the model itself
- [ ] It gives the model direct access to your Python interpreter
- [ ] It replaces the need for a `Runner` loop entirely
- [x] It writes the JSON schema from your function so you stop hand-typing it
::time=40

## Q12: In the SDK, what is `Runner` actually doing under the hood?
- [x] It's the same official tool-calling loop you already wrote by hand
- [ ] It's a database connector for your tools
- [ ] It swaps the API call for a local model
- [ ] It only draws the trace diagram
::time=35

## Q13: Why does MCP exist, in one sentence?
- [ ] To make API calls run faster
- [x] So a tool's implementation can live in another process, instead of copy-pasted into every project
- [ ] To replace the Chat Completions API entirely
- [ ] To give the model direct internet access
::time=40

## Q14: True or false — MCP is basically function calling, except the "your code decides and runs it" part is hosted by someone else's process.
- [x] True
- [ ] False
::time=30

# Section: Spot the Shape
> Same scenarios as yesterday's challenge. Chatbot, workflow, agent, automation, plain code, or nothing at all — pick the right tool for the job.

## Q15: A script has to rename 10,000 files every night by stripping a fixed prefix. What's the right call?
- [ ] Chatbot — ask it nicely for each filename
- [x] Plain code — a deterministic script, no model involved at all
- [ ] Agent with file tools, deciding the pattern each run
- [ ] One LLM call per filename to generate the new name
::time=40

## Q16: A visitor types a free-form question and just wants a conversational answer pulled from a short, fixed FAQ. What's the right call?
- [ ] A workflow with fixed, numbered steps
- [ ] An agent that plans across several tools
- [ ] Automation that runs with no model in the loop
- [x] A chatbot — talking is the whole job here
::time=40

## Q17: A customer emails a messy ticket mixing a billing question, an address change, and a complaint. You won't know the right next step until you've read it. What's the right call?
- [x] An agent — the model reads it and decides what to do next
- [ ] A workflow with the steps written out in advance
- [ ] Plain if-else code with one fixed branch per email
- [ ] A chatbot that just replies with a canned message
::time=45
