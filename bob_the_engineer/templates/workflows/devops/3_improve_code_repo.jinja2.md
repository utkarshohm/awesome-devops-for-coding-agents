# Improve Code Repo to Give Coding Agent More Autonomy

## Overview
{% if agent_type == "claude-code" -%}
This workflow analyzes your codebase and implements improvements that help Claude Code work more autonomously by enhancing feedback mechanisms, resolving conflicts, and improving debuggability.
{% elif agent_type == "cursor" -%}
This workflow analyzes your codebase and implements improvements that help Cursor work more autonomously by enhancing feedback mechanisms, resolving conflicts, and improving debuggability.
{% else -%}
This workflow analyzes your codebase and implements improvements that help coding agents work more autonomously by enhancing feedback mechanisms, resolving conflicts, and improving debuggability.
{% endif %}

## Prerequisites
- Completed previous Bob workflows
- Working feedback mechanisms (build, test, lint)
{% if agent_type == "claude-code" -%}
- Claude Code configured and operational
{% elif agent_type == "cursor" -%}
- Cursor configured and operational
{% else -%}
- Coding agent configured and operational
{% endif %}

## Workflow Structure

This workflow consists of three independent subagents that can be run together:

### Available Subagents
1. **@feedback-improver** - Enhance build, test, and lint configurations
2. **@conflict-detector** - Find and resolve conflicting instructions
3. **@debuggability-improver** - Improve error handling and logging

## Running the Workflow

### Option 1: Run All Improvements
```bash
# Run all three improvement agents in sequence
@feedback-improver analyze and improve feedback mechanisms
@conflict-detector find and resolve conflicts
@debuggability-improver enhance error handling and logging
```

### Option 2: Run Specific Improvements
```bash
# Run only the improvements you need
@feedback-improver analyze and improve feedback mechanisms
```

## Subagent Details

### 1. Feedback Improver Agent

**Purpose**: Strengthen feedback mechanisms for better AI autonomy

**What it does**:
- Analyzes current build, test, lint setup
- Compares against best practices
- Generates prioritized suggestions
- Implements approved improvements

**Example improvements**:
- Add missing formatter configuration
- Strengthen linter rules
- Set up pre-commit hooks
- Improve test coverage requirements
- Add type checking

**Usage**:
```bash
@feedback-improver analyze and improve feedback mechanisms
```

The agent will:
1. Generate a suggestions report
2. Ask for approval on changes
3. Implement improvements in phases
4. Verify each phase before continuing

### 2. Conflict Detector Agent

**Purpose**: Eliminate confusion from conflicting instructions

**What it detects**:
- Duplicate command definitions (npm vs yarn)
- Outdated documentation
- Conflicting configuration files
- Multiple ways to do the same task

**Example conflicts resolved**:
- Consolidate test commands
- Update stale README instructions
- Align linter and formatter rules
- Standardize environment configurations

**Usage**:
```bash
@conflict-detector find and resolve conflicts
```

The agent will:
1. Scan for conflicts and duplicates
2. Generate consolidation recommendations
3. Update configurations and documentation
4. Verify changes don't break existing workflows

### 3. Debuggability Improver Agent

**Purpose**: Make debugging easier for coding agents

**What it improves**:
- Error handling patterns
- Logging instrumentation
- Test failure messages
- Stack trace preservation

**Example enhancements**:
- Add context to error messages
- Implement structured logging
- Improve test descriptions
- Add debug entry/exit points

**Usage**:
```bash
@debuggability-improver enhance error handling and logging
```

The agent will:
1. Analyze current patterns
2. Identify improvement opportunities
3. Generate implementation plan
4. Apply changes in safe phases

## Workflow Execution Strategy

### Phase-Based Implementation
Each agent implements changes in phases to maintain stability:

**Phase 1**: Non-breaking additions
- Add new configuration files
- Enhance error messages
- Add logging statements

**Phase 2**: Backwards-compatible updates
- Update existing configurations
- Improve test assertions
- Standardize patterns

**Phase 3**: Optional breaking changes
- Remove deprecated code
- Enforce strict rules
- Require new standards


## Review Process

### 1. Suggestion Review
Each agent generates a suggestions file for review:
- `.bob/suggestions/feedback-improvements.md`
- `.bob/suggestions/conflict-resolutions.md`
- `.bob/suggestions/debuggability-enhancements.md`

### 2. Approval Workflow
```markdown
## Suggested Improvements

### Critical Priority
☐ Add formatter configuration
☐ Fix conflicting lint rules
☐ Add error context in API handlers

### High Priority
☐ Improve test descriptions
☐ Add structured logging
☐ Update outdated README

### Medium Priority
☐ Add debug logging
☐ Enhance error messages
☐ Standardize naming conventions
```

Reply with the items you want implemented.

### 3. Implementation Tracking
The agent tracks progress:
```markdown
## Implementation Progress

✅ Phase 1: Non-breaking additions (Complete)
- Added prettier configuration
- Enhanced error messages
- Added debug logging

⏳ Phase 2: Updates (In Progress)
- Updating test descriptions...
- Standardizing error handling...

⏸️ Phase 3: Breaking changes (Pending Approval)
```

## Success Criteria

### Feedback Improvements
✅ Formatter configured and working
✅ Linter rules comprehensive
✅ Pre-commit hooks active
✅ All mechanisms have clear commands

### Conflict Resolution
✅ No duplicate commands
✅ Documentation matches reality
✅ Single source of truth for configs
✅ Clear command hierarchy

### Debuggability Enhancements
✅ Errors include context
✅ Logging at appropriate levels
✅ Test failures are descriptive
✅ Stack traces preserved

## Best Practices

1. **Review Before Approving**: Check each suggestion carefully
2. **Test After Each Phase**: Ensure nothing breaks
3. **Commit Frequently**: Create restore points
4. **Document Changes**: Update team on new standards
5. **Gradual Adoption**: Don't enforce everything at once

## Troubleshooting

### If Improvements Break Something
```bash
# Revert to previous state
git checkout -- .

# Or selectively revert
git checkout -- [specific-file]
```

### If Suggestions Seem Wrong
- The agent might misunderstand your setup
- Provide more context about your requirements
- Skip suggestions that don't apply

### If Implementation Fails
```bash
# Check what went wrong
bob-the-engineer check-feedback-status --verbose

# Try implementing manually
bob-the-engineer [specific-command] --dry-run
```

## Next Steps

After improvements are implemented:
1. Commit the changes to version control
2. Update team documentation
{% if agent_type == "claude-code" -%}
3. Monitor Claude Code effectiveness
{% elif agent_type == "cursor" -%}
3. Monitor Cursor effectiveness
{% else -%}
3. Monitor coding agent effectiveness
{% endif %}
4. Consider custom improvements for your specific needs

## Notes

- These improvements are suggestions, not requirements
- You can run agents multiple times as your repo evolves
- Each run builds on previous improvements
- The goal is gradual enhancement, not perfection
