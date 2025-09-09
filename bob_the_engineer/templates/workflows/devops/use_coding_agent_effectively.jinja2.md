# Use Coding Agent Effectively on Existing Large Code Repo

## Overview
{% if agent_type == "claude-code" -%}
This workflow enhances your Claude Code setup with advanced development workflows and MCP tools to maximize productivity and code quality.
{% elif agent_type == "cursor" -%}
This workflow enhances your Cursor setup with advanced development workflows, MCP tools, and advanced features to maximize productivity and code quality.
{% else -%}
This workflow enhances your coding agent setup with advanced development workflows and MCP tools to maximize productivity and code quality.
{% endif %}

## Prerequisites
- Completed "Start Using Coding Agent" workflow
- Bob-the-engineer installed and configured
- Repository with validated feedback mechanisms

## Workflow Steps

### 1. Install Best-Practice Development Workflows

1a. Configure proven development workflows tailored to your coding agent by running below command.

**Command**:
```bash
!bob-the-engineer configure-coding-workflows --workflows spec-driven,tdd,code-review --agent-type {{ agent_type }}
```
1b. Tell the user about the workflows and how to use them.

Available workflows:
- **spec-driven**: 6-phase iterative development
- **tdd**: Test-first development with enforcement
- **code-review**: Multi-aspect parallel review

These have been installed as:
{% if agent_type == "claude-code" -%}
- Claude Code: `.claude/commands/[workflow].md`
{% elif agent_type == "cursor" -%}
- Cursor: `.cursor/commands/[workflow].md`
{% endif %}

You can now use them by typing this in your chat:
{% if agent_type == "claude-code" -%}
- Claude Code: `/spec-driven`, `/tdd`, `/code-review`
{% elif agent_type == "cursor" -%}
- Cursor: `@spec-driven`, `@tdd`, `@code-review`
{% endif %}

1c. Verify Workflows Installed
This should list all workflows installed
{% if agent_type == "claude-code" -%}
```bash
ls -la .claude/commands/  # For Claude Code
```
{% elif agent_type == "cursor" -%}
```bash
ls -la .cursor/commands/  # For Cursor
```
{% endif %}

Troubleshooting
{% if agent_type == "claude-code" -%}
- Check file permissions in `.claude/commands/`
{% elif agent_type == "cursor" -%}
- Check file permissions in `.cursor/commands/`
{% endif %}
- Restart coding agent session
- Run `bob-the-engineer doctor --repair`


### 2. Configure MCP Servers
Set up Model Context Protocol servers for enhanced capabilities.

**Subagent**: `@configure-mcp `


## Next Steps

After setup, consider:
1. Running "Improve Code Repo" workflow for enhanced AI autonomy
2. Customizing workflows for your team's needs
