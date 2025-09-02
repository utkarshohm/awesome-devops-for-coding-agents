
awesome-devops-for-coding-agents/
├── specs/
│   └── prd.md                      # This document
├── bob_the_engineer/
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   └── app.py                      # Main Typer CLI entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py                   # Data models (Workflow, Task, etc.)
│   │   ├── workflow_engine.py          # Core workflow execution logic
│   │   └── utils.py                    # Shared utilities
│   ├── commands/       # all commands irrespective of whether they are used as deterministic tasks or tools for agentic tasks are added here
│   │   ├── __init__.py
│   │   ├── base.py                     # Base command classes
│   │   ├── file_operations.py      # File read/write/copy tasks
│   │   ├── validation.py           # Build/lint/test validation
│   │   └── config_management.py    # JSON/YAML config updates
│   │   ├── repo_analysis.py        # Code repo analysis tools
│   │   └── feedback_tools.py       # Tools for feedback mechanisms
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── base.py                     # Base adapter interface
│   │   ├── claude/
│   │   │   ├── __init__.py
│   │   │   ├── command_manager.py   # Install workflows as commands
│   │   │   ├── subagent_manager.py   # Install agentic tasks as subagents
│   │   │   ├── setting_manager.py     # Manage .claude/settings.json
│   │   │   └── rules_manager.py        # Manage .cursor/rules
│   │   │   └── hook_manager.py         # Manage Claude Code hooks
│   │   ├── cursor/
│   │   │   ├── __init__.py
│   │   │   ├── command_manager.py    # Install as cursor commands
│   │   │   └── rules_manager.py        # Manage .cursor/rules
│   │   └── factory.py                  # Adapter factory
│   ├── templates/
│   │   ├── workflows/
│   │   │   └── start_using_coding_agent.jinja2
│   │   ├── subagents/
│   │   │   └── configure_rules.jinja2
