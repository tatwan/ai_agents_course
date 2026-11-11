# Day 2 Kickoff: The Day 1 Rewind
# Score 100

# Section: Warm-up
> Just for fun. No wrong answer here, but pick one.

## Q1: True or false: you learned at least one thing yesterday that you did not know before.
::type=ungraded
- [x] True
- [x] False
::time=15

# Section: Round 1: Who decides, and what one call holds
> Day 1, Parts 1 to 4. Graded, one point each.

## Q2: Which question tells a chatbot, a workflow and an agent apart?
- [ ] How many tools it can call
- [ ] Which framework runs it
- [x] Who decides the next step
- [ ] How long its prompt is
::time=20

## Q3: In Chat Completions, how does a chatbot seem to remember the conversation?
- [x] Your code resends the whole list each call
- [ ] The model stores past turns in its weights
- [ ] The API keeps your session for an hour
- [ ] The model saves a summary after each reply
::time=25

## Q4: The model asks for a tool. What has your code received at that moment?
- [ ] The tool's result, already computed
- [ ] A query the database has already run
- [ ] A Python function to execute as written
- [x] A tool name, JSON arguments and an id
::time=25

## Q5: The model asks for `refund_invoice(404, 250)`. Invoice 404 totals $25.86. What does your code do?
- [ ] Run it, since the model chose it
- [x] Refuse it and send the reason back to the model
- [ ] Refund $25.86 instead, without telling the model
- [ ] Stop the run and show the customer an error
::time=35

# Section: Round 2: The loop and what it sees
> Day 1, Parts 5 and 6.

## Q6: The model has asked for `count_invoices` six times in a row. What stops the loop?
- [ ] The model notices the repeat and stops
- [ ] The tool refuses a seventh call
- [x] The turn cap, with a stop reason that says so
- [ ] The API ends the conversation after six calls
::time=30

## Q7: ReAct and tool calling run the same loop. What differs between them?
- [ ] ReAct: the model runs the tool; tool calling: your code
- [ ] ReAct: one model call; tool calling: one per tool
- [ ] ReAct hides its reasoning; tool calling writes it out
- [x] ReAct: text your code parses; tool calling: a field
::time=30

## Q8: Four playbooks sit in the system prompt. What changes when you move them into Agent Skills?
- [x] Each playbook loads when a task needs it
- [ ] The model stops paying for the system prompt
- [ ] The playbooks are cached, so they cost nothing
- [ ] The tool descriptions become shorter
::time=30

# Section: Round 3: MCP and the SDK
> Day 1, Parts 7 and 8.

## Q9: Your `count_invoices` tool must work from VS Code and from your Python agent. How many MCP servers do you write?
- [ ] Two: one for each host
- [ ] Two: a local one and a remote one
- [x] One: each host runs its own MCP client
- [ ] None: VS Code reads your Python directly
::time=30

## Q10: True or false: with MCP, the model sends its tool request straight to the server, and your code never sees it.
- [ ] True
- [x] False
::time=20

## Q11: In the OpenAI Agents SDK, what is `Runner.run` doing?
- [ ] Running your tools inside the model
- [x] Running the loop you wrote in Lab 03
- [ ] Training the model on your tools
- [ ] Drawing the trace of the run
::time=25

# Section: Round 4: Spot the shape
> Like yesterday's challenge, with new jobs. Pick the simplest option that does the job.

## Q12: Every night, 10,000 files must be renamed by stripping the same fixed prefix. What fits best?
- [x] A script
- [ ] An RPA bot
- [ ] A workflow with an LLM step
- [ ] An agent
::time=25

## Q13: Refund requests arrive on a fixed template and must be typed into an old ERP screen that has no API. What fits best?
- [ ] A script
- [x] An RPA bot
- [ ] A workflow with an LLM step
- [ ] An agent
::time=30

## Q14: One customer email mixes a billing question, an address change and a complaint. You cannot know the next step until you read it. What fits best?
- [ ] A script
- [ ] An RPA bot
- [ ] A workflow with an LLM step
- [x] An agent
::time=30
