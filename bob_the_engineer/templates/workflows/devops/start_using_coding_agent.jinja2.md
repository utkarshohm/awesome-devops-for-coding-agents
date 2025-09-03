# Start Using Coding Agent on Existing Large Code Repo

## Overview
{% if agent_type == "claude-code" -%}
This workflow helps you onboard Claude Code to an existing large codebase. It analyzes the repository, sets up appropriate rules, and validates feedback mechanisms to ensure Claude Code can work effectively.
{% elif agent_type == "cursor" -%}
This workflow helps you onboard Cursor to an existing large codebase. It analyzes the repository, sets up appropriate rules, and validates feedback mechanisms to ensure Cursor can work effectively.
{% else -%}
This workflow helps you onboard a coding agent (Claude Code or Cursor) to an existing large codebase. It analyzes the repository, sets up appropriate rules, and validates feedback mechanisms to ensure the coding agent can work effectively.
{% endif %}

## Workflow Steps

### 1. Configure Rules

**Subagent**: `@configure-rules analyze and generate rules for this repository`

The agent will:
- Scan repository structure
- Detect languages, frameworks, and tools
{% if agent_type == "claude-code" -%}
- Generate CLAUDE.md rules file
{% elif agent_type == "cursor" -%}
- Generate .cursor/rules/ configuration files
{% else -%}
- Generate CLAUDE.md or cursor rules
{% endif %}
- Focus on DevOps practices, not application logic

### 2. Validate Feedback Mechanisms

**Subagent**: `@build-test-run test and validate all feedback mechanisms`

The agent will:
- Execute build, test, lint commands
- Classify failures as must-have or good-to-have
- Debug and fix must-have failures
- Generate comprehensive report

### 3. Configure Best-Practice Defaults
{% if agent_type == "claude-code" -%}
Set up Claude Code with best-practice defaults while preserving user customizations.
{% elif agent_type == "cursor" -%}
Set up Cursor with best-practice defaults while preserving user customizations.
{% else -%}
Set up the coding agent with best-practice defaults while preserving user customizations.
{% endif %}

**Step 3a: Review Available Templates**
First, explore the available configuration templates to understand your options:

```bash
!bob-the-engineer configure-defaults --list
```

This will display detailed information about each template:
- **solo-developer**: Streamlined for individual developers and rapid prototyping
- **development-team**: Optimized for 2-5 developers with CI/CD and code review
- **enterprise-security**: High-security for large teams and regulated environments

**Step 3b: Apply Configuration**
Choose one of these approaches:

```bash
!bob-the-engineer configure-defaults --agent-type {{ agent_type }} --template-type <user-input> --repo-path .
```

{% if agent_type == "claude-code" -%}
- Enable thinking/reasoning features appropriately
{% endif %}
- Configure tool permissions based on your tech stack
- Preserve existing user customizations

## Success Criteria

✅ Repository analyzed and stack detected
{% if agent_type == "claude-code" -%}
✅ Rules file generated (CLAUDE.md)
{% elif agent_type == "cursor" -%}
✅ Rules files generated (.cursor/rules/)
{% else -%}
✅ Rules file generated (CLAUDE.md or .cursor/rules/)
{% endif %}
✅ All must-have feedback mechanisms working
✅ Best-practice defaults configured
✅ Settings preserved user customizations

## Troubleshooting

If any step fails:
1. Check the error messages in the agent output
2. Run `bob-the-engineer doctor --repair` to fix installation issues

## Next Steps

After completing this workflow, run the "Use Coding Agent Effectively" workflow to:
- Install advanced development workflows
- Configure MCP tools
- Set up supervision and guards
