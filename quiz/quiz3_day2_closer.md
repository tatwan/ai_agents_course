# The Grand Finale: Two Days, One Loop
# Score 100

# Section: Round 1: Callback
> Two ideas from Day 1, then this morning's first build.

## Q1: On Day 1, why did we choose what goes into the context on every turn?
- [ ] The model forgets the system prompt after turn 3
- [x] Every token in it is paid for on every turn
- [ ] The window keeps just the latest message
- [ ] Tool results are free, but the history is not
::time=30

## Q2: `count_invoices` and `support_rep` each take one second. Why run them with `async` and `gather`?
- [ ] To use fewer tokens on the two calls
- [ ] To make the model pick the tools faster
- [x] To wait on both at once: 1 s, not 2
- [ ] To run them on two CPUs in parallel
::time=30

## Q3: A refund paused at 3 a.m. on Saturday with an in-memory checkpointer. The server restarted on Sunday. What does the approver find on Monday?
- [x] Nothing: the paused run was lost
- [ ] The refund, paused and ready to approve
- [ ] The refund, already paid by default
- [ ] An error that names the lost thread
::time=35

# Section: Round 2: Documents and data
> Day 2, Parts 11 and 12.

## Q4: "Can I return an unopened CD after 40 days?" Where does the answer live?
- [ ] In the invoices table of chinook.db
- [ ] In the model's weights, from training
- [x] In a policy file: the returns policy
- [ ] Nowhere: the desk must refuse
::time=25

## Q5: Asked for the CEO's personal phone number, the search still returns its nearest file. Which part must say "the files do not say"?
- [x] The answer step, which can refuse
- [ ] The search, with a higher score cut-off
- [ ] The embedding model, retrained
- [ ] The vector database, with more files
::time=35

## Q6: Ticket 06 says "replace once". The rule for a second damaged copy is in another file. Why does an agent with a search tool find it when a top-2 search does not?
- [ ] Its embeddings are better than one search's
- [ ] It reads all 36 files before it answers
- [ ] It searches the policies first and skips tickets
- [x] It reads the ticket, then searches for the rule
::time=35

## Q7: A free SQL tool sits on a normal database connection. Its description says "read-only". What stops a DELETE?
- [ ] The description, which the model obeys
- [x] Nothing yet: open it read-only
- [ ] The model's safety training on SQL
- [ ] SQLite, which refuses DELETE from tools
::time=30

# Section: Round 3: Code, designs and controls
> Day 2, Parts 13 to 16.

## Q8: Model-written code runs `Path("../../.env").exists()`. Where does it run so that it cannot see your `.env` file?
- [ ] A subprocess with a timeout
- [ ] A subprocess in a separate folder
- [ ] A subprocess with no network
- [x] A container, one folder mounted
::time=35

## Q9: Lab 18 found one agent right on every request. Which is a good reason to add a second agent to the refund desk?
- [x] The refund tool writes; lookups just read
- [ ] A second agent gives more accurate answers
- [ ] Each tool should have its own agent
- [ ] Two small agents are easier to test
::time=35

## Q10: An edited ticket 16 says the refund "was approved and paid". It was not. Which defence stops the agent from believing it?
- [ ] Scan the ticket for command words
- [ ] A prompt rule: file text is data
- [x] Check the billing record in code
- [ ] Give the agent no payment tool
::time=35

## Q11: Your judge passes a reply that repeats a planted claim. What do you change first?
- [ ] Tell the judge to watch for injections
- [x] Give the judge the billing record
- [ ] Give the judge the ticket and the reply
- [ ] Use a larger model as the judge
::time=30

## Q12: Agent platforms sell six layers that you built. Which two are hardest to move to another vendor?
- [ ] The model and the tools
- [ ] Orchestration and delegation
- [ ] The tools and delegation
- [x] Memory and governance
::time=30

# Section: Grand Finale
> Ungraded. Just for the room.

## Q13: Two days in: chatbot, workflow or agent, which one are you right now?
::type=ungraded
- [x] Workflow: hand me a checklist
- [x] Agent: I pick my own next step
- [x] Chatbot: I talk, but don't ask me to act
- [x] Still loading
::time=30
