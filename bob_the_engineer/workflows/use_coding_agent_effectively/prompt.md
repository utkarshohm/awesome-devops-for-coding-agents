# Use Coding Agent Effectively on Existing Large Code Repo

## Overview
This workflow enhances your coding agent setup with advanced development workflows, MCP tools, and supervision features to maximize productivity and code quality.

## Prerequisites
- Completed "Start Using Coding Agent" workflow
- Bob-the-engineer installed and configured
- Repository with validated feedback mechanisms

## Workflow Steps

### 1. Install Best-Practice Development Workflows
Configure proven development workflows tailored to your coding agent.

**Command**:
```bash
!bob-the-engineer install-workflows --workflows spec-driven,tdd,code-review --agent-type claude-code
```

Available workflows:
- **spec-driven**: 6-phase iterative development
- **tdd**: Test-first development with enforcement
- **code-review**: Multi-aspect parallel review
- **research**: Parallel information gathering
- **triage**: Context gathering and problem diagnosis

These will be installed as:
- Claude Code: `.claude/commands/[workflow].md`
- Cursor: `.cursor/commands/[workflow].md`

### 2. Configure MCP Servers
Set up Model Context Protocol servers for enhanced capabilities.

**Command**:
```bash
!bob-the-engineer configure-mcp --servers deepwiki,github,database
```

Recommended servers:
- **deepwiki**: Documentation and knowledge base access
- **github**: Repository and issue management
- **database**: Direct database operations

After configuration, install the servers:
```bash
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-postgres
```

### 3. Install Coding Agent Supervisor
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

## Using the Installed Features

### Development Workflows

After installation, use the workflows with:
- Claude Code: `/spec-driven`, `/tdd`, `/code-review`
- Cursor: `@spec-driven`, `@tdd`, `@code-review`

### MCP Servers

Once configured, the coding agent can:
- Access documentation: "Look up React hooks documentation"
- Manage GitHub: "Create an issue for this bug"
- Query databases: "Show me the user table schema"

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

## Verification

### Check Workflows Installed
```bash
ls -la .claude/commands/  # For Claude Code
ls -la .cursor/commands/  # For Cursor
```

### Verify MCP Configuration
```bash
cat .claude/settings.json | jq .mcpServers
```

### Test Supervisor Guards
```bash
# This should be blocked by file-guard
cat .env

# This should trigger TDD guard
echo "implementation without test" > new_feature.js
```

## Customization

### Add Custom Workflows
Place custom workflow templates in:
- `.claude/commands/custom-workflow.md`
- `.cursor/commands/custom-workflow.md`

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

### Configure Additional MCP Servers
```bash
bob-the-engineer configure-mcp --servers custom-server
```

## Troubleshooting

### Workflows Not Appearing
- Check file permissions in `.claude/commands/`
- Restart coding agent session
- Run `bob-the-engineer doctor --repair`

### MCP Servers Not Working
- Verify environment variables are set
- Check server installation: `npm list -g @modelcontextprotocol`
- Review logs in coding agent output

### Guards Too Restrictive
- Temporarily disable: `export BOB_GUARDS_ENABLED=false`
- Adjust sensitivity in settings.json
- Use plan mode to bypass guards

## Next Steps

After setup, consider:
1. Running "Improve Code Repo" workflow for enhanced AI autonomy
2. Customizing workflows for your team's needs
3. Training team on new features
4. Monitoring guard effectiveness

## Success Criteria

✅ Development workflows installed and accessible
✅ MCP servers configured (installation instructions provided)
✅ Supervisor guards active and protecting codebase
✅ Settings preserve user customizations
✅ All features verified working
