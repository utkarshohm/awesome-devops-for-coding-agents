# Use Coding Agent Effectively on Existing Large Code Repo

## Overview
{% if agent_type == "claude-code" -%}
This workflow enhances your Claude Code setup with advanced development workflows, MCP tools, and supervision features to maximize productivity and code quality.
{% elif agent_type == "cursor" -%}
This workflow enhances your Cursor setup with advanced development workflows, MCP tools, and advanced features to maximize productivity and code quality.
{% else -%}
This workflow enhances your coding agent setup with advanced development workflows, MCP tools, and supervision features to maximize productivity and code quality.
{% endif %}

## Prerequisites
- Completed "Start Using Coding Agent" workflow
- Bob-the-engineer installed and configured
- Repository with validated feedback mechanisms

## Workflow Steps

### 1. Install Best-Practice Development Workflows
{% if agent_type == "claude-code" -%}
Configure proven development workflows tailored to Claude Code.
{% elif agent_type == "cursor" -%}
Configure proven development workflows tailored to Cursor.
{% else -%}
Configure proven development workflows tailored to your coding agent.
{% endif %}

**Command**:
```bash
!bob-the-engineer configure-coding-workflows --workflows spec-driven,tdd,code-review --agent-type {{ agent_type }}
```

Available workflows:
- **spec-driven**: 6-phase iterative development
- **tdd**: Test-first development with enforcement
- **code-review**: Multi-aspect parallel review
- **research**: Parallel information gathering
- **triage**: Context gathering and problem diagnosis

These will be installed as:
{% if agent_type == "claude-code" -%}
- Claude Code: `.claude/commands/[workflow].md`
{% elif agent_type == "cursor" -%}
- Cursor: `.cursor/commands/[workflow].md`
{% else -%}
- Claude Code: `.claude/commands/[workflow].md`
- Cursor: `.cursor/commands/[workflow].md`
{% endif %}

### 2. Configure MCP Servers
Set up Model Context Protocol servers for enhanced capabilities.

**Subagent**: `@configure-mcp `

{% if agent_type == "claude-code" -%}
### 3. Install Coding Agent Supervisor (for claude code only)
Set up guards and hooks to prevent common AI coding mistakes.

**Command**:
```bash
!bob-the-engineer install-supervisor --guards file-guard,tdd-guard,self-review
```

Guards installed (in priority order):
1. **file-guard**: Protects sensitive files from AI access
2. **tdd-guard**: Enforces test-first development
3. **self-review**: Catches implementation shortcuts

**Note**: Guards are automatically disabled in plan/ask mode to avoid conflicts.
{% elif agent_type == "cursor" -%}
### 3. Configure Advanced Cursor Features
Set up enhanced Cursor-specific features for improved development experience.

**Command**:
```bash
!bob-the-engineer configure-cursor-features --enable-advanced-rules --setup-context-optimization
```

Features configured:
1. **Advanced Rules**: Enhanced context-aware rule processing
2. **Context Optimization**: Improved codebase understanding
3. **Smart Suggestions**: Repository-specific intelligent suggestions
{% endif %}

## Using the Installed Features

### Development Workflows

After installation, use the workflows with:
{% if agent_type == "claude-code" -%}
- Claude Code: `/spec-driven`, `/tdd`, `/code-review`
{% elif agent_type == "cursor" -%}
- Cursor: `@spec-driven`, `@tdd`, `@code-review`
{% else -%}
- Claude Code: `/spec-driven`, `/tdd`, `/code-review`
- Cursor: `@spec-driven`, `@tdd`, `@code-review`
{% endif %}

### MCP Servers

{% if agent_type == "claude-code" -%}
Once configured, Claude Code can:
{% elif agent_type == "cursor" -%}
Once configured, Cursor can:
{% else -%}
Once configured, the coding agent can:
{% endif %}
- Access documentation: "Look up React hooks documentation"
- Manage GitHub: "Create an issue for this bug"
- Query databases: "Show me the user table schema"

{% if agent_type == "claude-code" -%}
### Supervisor Guards

The guards work automatically:
- **file-guard**: Blocks access to .env, secrets, credentials
- **tdd-guard**: Requires failing test before implementation
- **self-review**: Randomly triggers self-review after changes

To temporarily disable guards:
```bash
export BOB_TDD_ENABLED=false  # Disable TDD guard
export BOB_GUARDS_ENABLED=false  # Disable all guards
```
{% elif agent_type == "cursor" -%}
### Advanced Cursor Features

The enhanced features work seamlessly:
- **Advanced Rules**: Provide more context-aware suggestions
- **Context Optimization**: Better understanding of large codebases
- **Smart Suggestions**: Repository-specific intelligent recommendations

To adjust feature settings, edit `.cursor/settings.json`.
{% endif %}

## Verification

### Check Workflows Installed
```bash
{% if agent_type == "claude-code" -%}
ls -la .claude/commands/  # For Claude Code
{% elif agent_type == "cursor" -%}
ls -la .cursor/commands/  # For Cursor
{% else -%}
ls -la .claude/commands/  # For Claude Code
ls -la .cursor/commands/  # For Cursor
{% endif %}
```

### Verify MCP Configuration
```bash
{% if agent_type == "claude-code" -%}
cat .claude/settings.json | jq .mcpServers
{% elif agent_type == "cursor" -%}
cat .cursor/settings.json | jq .mcpServers
{% else -%}
cat .claude/settings.json | jq .mcpServers
{% endif %}
```

{% if agent_type == "claude-code" -%}
### Test Supervisor Guards
```bash
# This should be blocked by file-guard
cat .env

# This should trigger TDD guard
echo "implementation without test" > new_feature.js
```
{% endif %}

## Customization

### Add Custom Workflows
Place custom workflow templates in:
{% if agent_type == "claude-code" -%}
- `.claude/commands/custom-workflow.md`
{% elif agent_type == "cursor" -%}
- `.cursor/commands/custom-workflow.md`
{% else -%}
- `.claude/commands/custom-workflow.md`
- `.cursor/commands/custom-workflow.md`
{% endif %}

{% if agent_type == "claude-code" -%}
### Modify Guard Behavior
Edit `.claude/settings.json` hooks section:
```json
{
  "hooks": {
    "preToolUse": [
      {
        "name": "file-guard",
        "script": "bob-the-engineer check-file-access",
        "condition": "${CLAUDE_MODE} != 'plan'"
      }
    ]
  }
}
```
{% endif %}

### Configure Additional MCP Servers
```bash
bob-the-engineer configure-mcp --servers custom-server
```

## Troubleshooting

### Workflows Not Appearing
{% if agent_type == "claude-code" -%}
- Check file permissions in `.claude/commands/`
{% elif agent_type == "cursor" -%}
- Check file permissions in `.cursor/commands/`
{% else -%}
- Check file permissions in `.claude/commands/`
{% endif %}
- Restart coding agent session
- Run `bob-the-engineer doctor --repair`

### MCP Servers Not Working
- Verify environment variables are set
- Check server installation: `npm list -g @modelcontextprotocol`
- Review logs in coding agent output

{% if agent_type == "claude-code" -%}
### Guards Too Restrictive
- Temporarily disable: `export BOB_GUARDS_ENABLED=false`
- Adjust sensitivity in settings.json
- Use plan mode to bypass guards
{% endif %}

## Next Steps

After setup, consider:
1. Running "Improve Code Repo" workflow for enhanced AI autonomy
2. Customizing workflows for your team's needs
3. Training team on new features
{% if agent_type == "claude-code" -%}
4. Monitoring guard effectiveness
{% elif agent_type == "cursor" -%}
4. Optimizing Cursor settings for your workflow
{% endif %}

## Success Criteria

✅ Development workflows installed and accessible
✅ MCP servers configured (installation instructions provided)
{% if agent_type == "claude-code" -%}
✅ Supervisor guards active and protecting codebase
{% elif agent_type == "cursor" -%}
✅ Advanced Cursor features configured and working
{% endif %}
✅ Settings preserve user customizations
✅ All features verified working
