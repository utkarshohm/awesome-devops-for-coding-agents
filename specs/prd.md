
## Decisions

### Abstractions

Bob has 4 key abstractions: A `workflow` consists of `deterministic tasks` and `agentic tasks`. The latter uses `tools`.

1. A workflow consists of deterministic tasks and agentic tasks, defined by prompt.
2. Deterministic tasks are defined by python code.
3. Agentic tasks are done via coding agent, defined by prompt, config for off-the-shelf tools (both built-in like ls, grep etc as well as third-party like github mcp server, aws cli etc) and python code for custom tools (defined specially for this agentic task). Let's call these subagents.

### Approach for high reliability

Mechanical tasks are defined by code to increase reliability of workflows. While agents are very promising, you don't need them for everything. Often, you know exactly what the system should do. That's why Bob relies on three levels of determinism.

1. For a dev ops goal to be achieved, the exact list and maybe even sequence of tasks is clear. Hence workflow prompts often prescribe sequence of tasks.
2. Some tasks are very mechanical like read from a file or run the linter. They are also defined by python code.
3. The tasks that require reasoning and agency will use a coding agent. However some of the subtasks are mechnical like computing hash, getting current time, copying contents from one file to another or querying a database. They can be done more reliably by code.

### Design details

#### Workflow and agentic tasks defined using coding agent abstractions

Workflow and agentic tasks will be defined in a way that uses abstractions of that CA, mostly an md file containing prompt, available tools.

1. claude code: [commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands) for workflows, [subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents) for agentic tasks.
2. cursor agent: [commands](https://docs.cursor.com/en/agent/chat/commands) for both.
3. DO LATER: gh copilot agent: agents for agentic tasks.
4. DO LATER: cline: workflows for both workflows and agentic tasks. dont use commands or slash commands.

**Let's start with claude code and cursor agent only for now.**

#### Python code for mechnical parts

Deterministic tasks and tools available to subagents will be defined in python and available to the coding agent via CLI commands.

#### Hook workflows with coding agent

Claude code uniquely exposes [hooks](https://docs.anthropic.com/en/docs/claude-code/hooks-guide) that can be used to configure certain workflows/agentic tasks to be run on certain events like tool use, start of session or claude code finishes responding to user. Other coding agents don't have this abstraction so they will need to be run explicitly by the user. Note that claude code hooks can't invoke subagents or mcp tools. It can only invoke good old cli commands.

### User experience

The user can use bob in 2 modes:
1. Without the cli: Copy the subagents/commands/workflow specs into their .claude or .cursor dir directly. Subagents that need their own MCP tools may not be work in this mode. Claude code hooks won't work either.
2. With the cli: Install the cli. When you init the CLI in a code repo you can choose which all workflows to install and for which coding agent. The relevant adapters are configured into the coding agent by writing to .claude/ or .cursor/ or .github/ dirs of the code repo. The user is encouraged to commit the changes.


## Workflow specs

### A. Start using coding agent on existing large code repo

This will consist of following tasks:

1. **configure rules**: write rules.mdc/agents.md/claude.md files at root with a heavy focus on devops and not application logic. figure out which of the following are used in the repo: languages, frameworks, package manager, build tool, test tool, lint tool and so on. Focus on understanding the instructions to install the packages and the feedback mechanisms (build, lint/format, unit-test, run).  Leverage init commands of CA (`/init` in claude code, `/generate cursor rules` in cursor). Do not write rules files specific to the application logic or within code subdirs because they may get out of date as the code evolves. You can depend on the agentic search to find and understand the code effectively.
   - task type: agentic
   - output: CLAUDE.md or .cursor/rules/*.mdc

2. **validate feedback mechanisms**: use the output of previous subagent. run the feedback mechanisms and report outstanding failures/violations in them: build, pre-commit check/lint/format, unit test and run. classify the failures into must-haves and good-to-haves. debug the must-haves until you have fixed them. generate a report at the end showing the pending failures.
   - task type: agentic
   - output: .claude/reports/validate-feedback-mechanisms.md or equivalent for cursor

3. **configure best-practice defaults**: always start in plan mode (claude code) or ask mode (cursor).
   - task type: deterministic
   - output: updated settings.json in .claude or equivalent for cursor

### B. Use coding agent effectively on existing large code repo

4. **configure best-practice development workflows**: existing subagents/commands like spec driven development, tdd can be added to your coding agent.
   - task type: deterministic
   - output: add md files in .claude/agents or equivalent

5. **configure necessary mcp tools**: docs (deepwiki)
   - task type: deterministic
   - output: update settings.json in .claude or equivalent

6. **configure coding agent supervisor**: this is not to review the code generated by the CA but to supervise that CA is following instructions given to it specially catch common failure modes. for eg, in their eagerness to pass tests CA may mock the very function it is supposed to test. Learn from impl of ~/projects/coding-agent-prompts/tdd-guard.
   - task type: deterministic
   - output: update hook in settings.json in .claude. can't be implemented in each other coding agents.

### C. Improve code repo to give coding agent more autonomy

7. **improve feedback mechanisms**: suggest improvements in setup by comparing against bare minimum needed for coding agent. for eg, no formatter in pre-commit check, too few rules enabled in linter, too many security exceptions. seek confirmation to implement improvements using subagent.
   - task type: agentic
   - output: updates in code repo

8. **mitigate conflicting instructions**: coding agents will get confused if there are two ways to do the same thing. for eg, run the linter or unit tests, or if the repo has outdated docs
   - task type: agentic
   - output: updates in code repo

9. **improve debuggability**: CA is effective at coding when it is able to debug failures effeciently.
   - task type: agentic
   - output: updates in code repo

That requires finding instances of following in the code repo:
  - errors caught and thrown at the right places with the informative message and necessary context
  - errors propagated up the call stack
  - log lines instrumented at the right places with appropriate level (error, warning, info and debug), message and necessary context passed to it.
  - tests fail with actionable message and errors propagated up to it.


### Others - to be done later

- Prepare Engineering Knowledge Graph
- Setup security scanning in existing large code repo
- **Learn production guardrails from past incident RCAs**: Ingest RCAs to derive guardrail policies and patterns.
- **Review generated code using production guardrails**: Apply learned guardrails to review AI-generated diffs.
- Debug CI/CD failures


## Guidance on designing

### Workflows

Design: Use !<bash command> to run deterministic tasks. Reference @ or / to reference subagents or commands. What's important is that after each task the workflow should verify that the objective of the task was achieved or further work/re-running/debugging is required to achieve it.

Create a md file in a templated manner so that claude code agent/command or cursor command can be created from it via a simple cli command. The md file should be created as part of the design phase. Follow the proposed dir structure in the design_doc.md when saving the prompts.

### Agentic tasks

Design: Read coding agent docs for agent/command definitions. Think about the objective of the task before writing the prompt and params of agent/command definitions like tools, model, description etc. Does the task need some custom tools that need to be implemented as cli commands? Iterate on the prompt to make it better.

Create a md file in a templated manner so that claude code agent/command or cursor command can be created from it via a simple cli command. The md file should be created as part of the design phase. Follow the proposed dir structure in the design_doc.md when saving the prompts.

### Determinisitc tasks

Design: These tasks require writing python code in impl phase. In design phase you need to define following
1. the cli command interface needed by the deterministic task or tool
2. the class/function interfaces
3. sample json if json needs to be generated in the task

### Tasks 3, 4, 6
Design: You will be writing python code to update json files. Give thought to how you would read json file so that you dont write duplicate fields, write valid json etc etc. Use a good library.

### Tasks 3-5
Design: Go through the sources listed to find more useful defaults, dev workflows and mcp servers. Spend time search through them. Prepare a candidate list of suggestions that I can pick from.

### Tasks 7-9
Design: These tasks are multi-step and interactive. They require very detailed prompts, reasoning to identify the patterns described for each task along with examples of each and output format.

1. They will generate a list of suggestions in a md file such that the user can review them quickly, decide which ones should be done and tell the agent. The suggestions should be summarized succintly to meet this goal. Group similar suggestions for easy review.
2. Next, the coding agent will plan its edits breaking it into phases such that feedback mechanisms (build, lint, test) can be run after every phase to ensure that the code edits aren't introducing new issues. This was planning.
3. Next is executing the plan: make code edits in phases and verifying each one before moving to next one.

### Good sources

The following repositories have been cloned to ~/projects/coding-agent-prompts so that you can search over them freely.

https://github.com/davila7/claude-code-templates
https://github.com/carlrannaberg/claudekit
https://github.com/nizos/tdd-guard
https://github.com/PatrickJS/awesome-cursorrules

https://github.com/hesreallyhim/awesome-claude-code has a laundry list of other libraries that may require web fetches.
