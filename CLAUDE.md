**Non-technical PM actually building things

---
***Core Tools and Structure
- GPT Projects/ Claude Projects
	- Shared folder of chats and knowledge base
	- Projects allow you to compartmentalize
	- Products (bolt/loveable)
		- Built in a way to write code first
		- When things got more complex, this backfired
		- Organization matters more than anything
		- Phrasing of prompts
			- I own the problem, I own the user perspective
			- You're the complete own of how it's supposed to be built
			- Do not be a people pleaser
			- Challenge me
	- **Cursor and Claude
		- Look into cursor
		- Bolt first -> graduated to cursor
			- Claude runs within cursor
----
**Cursor Overview
- Slash Commands
	- Reusable commands
		- Prompts Claude with the right context to help
			- Embeds context into agent
	- Create-issue
		- Captures issue from user
	- Exploration-phase
		- Only explore what we want to solve
		- Analyze and understand the issue, asking clarifying questions
	- Create-plan
		- Template for creating a plan
			- Markdown file that has an executable plan that we can build with code
	- Execute-plan
		- AI agent builds from markdown file
	- Review and peer review
	- Update docs
----
**Slash Command Workflow
1. Create issue in linear
2. create-issue
3. explore
4. create-plan
5. execute-plan
6. review
7. peer-review
---
**Example
1. create-issue (actually in linear: https://linear.app)
	1. asks brief questions
	2. provide detailed context of what needs to happen
		1. this can actually create an issue in linear
			1. beginning of an idea, no necessarily for work
				1. we will explore this later
			2. can this be done with Jira
2. exploration-phase (takes an argument as extra context)
	1. references linear ticket just created
	2. fetches ticket
		1. ideate on the idea
		2. CTO to deeply understand problem to be solved
		3. what is the best way to solve this problem
	3. comes back with a number of questions about how this should be analyzed
3. create-plan
	1. AI agent creates a plan.md file
	2. contains
		1. TLDR
		2. plan
		3. tasks
		4. phases
4. execute (tag plan.md file)
	1. using cursor
		1. composer (very fast)
			1. execute and tag file (using @)
			2. most cutting edge features of models
5. review
	1. AI reviews its own code
		1. Play into strengths of models
			1. CODEX -> Best code
			2. Claude -> Great CTO
			3. Gemini -> Great designs
	2. Do it a number of times with other AI feedback into other AI models
---
**Documentation
- When AI continuously does not do what you want it to do, ask what prompted it to make that decision
- Once identified, update tooling and documentation so that mistake never happens again
	- Update slash-command prompts, but could be more than that as well
---
**Advice
1. Make code base AI native
	1. Needs to be done by technical people
	2. Lots of markdown files
		1. Provides AI navigation
	3. Create PR -> Dev to clean up

