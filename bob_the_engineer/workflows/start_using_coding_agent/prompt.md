# Start Using Coding Agent on Existing Large Code Repo

## Overview
This workflow helps you onboard a coding agent (Claude Code or Cursor) to an existing large codebase. It analyzes the repository, sets up appropriate rules, and validates feedback mechanisms to ensure the coding agent can work effectively.

## Workflow Steps

### 1. Configure Rules
Use the @rule-configurator agent to analyze the repository and generate DevOps-focused rules.

**Command**: `@rule-configurator analyze and generate rules for this repository`

The agent will:
- Scan repository structure
- Detect languages, frameworks, and tools
- Generate CLAUDE.md or cursor rules
- Focus on DevOps practices, not application logic

**Verification**:
```bash
!bob-the-engineer verify-rules --repo-path .
```

### 2. Validate Feedback Mechanisms
Use the @feedback-validator agent to test all feedback mechanisms and fix critical issues.

**Command**: `@feedback-validator test and validate all feedback mechanisms`

The agent will:
- Execute build, test, lint commands
- Classify failures as must-have or good-to-have
- Debug and fix must-have failures
- Generate comprehensive report

**Verification**:
```bash
!bob-the-engineer check-feedback-status --repo-path .
```

### 3. Configure Best-Practice Defaults
Set up the coding agent with best-practice defaults while preserving user customizations.

**Command**:
```bash
!bob-the-engineer configure-defaults --agent-type claude-code --repo-path .
```

This will:
- Set default mode to plan/ask
- Enable thinking/reasoning features
- Configure environment variables
- Preserve existing user settings

## Success Criteria

✅ Repository analyzed and stack detected
✅ Rules file generated (CLAUDE.md or .cursor/rules/)
✅ All must-have feedback mechanisms working
✅ Best-practice defaults configured
✅ Settings preserved user customizations

## Troubleshooting

If any step fails:
1. Check the error messages in the agent output
2. Run `bob-the-engineer doctor --repair` to fix installation issues
3. Manually verify commands using `bob-the-engineer exec-with-analysis "[command]"`

## Next Steps

After completing this workflow, run the "Use Coding Agent Effectively" workflow to:
- Install advanced development workflows
- Configure MCP tools
- Set up supervision and guards
