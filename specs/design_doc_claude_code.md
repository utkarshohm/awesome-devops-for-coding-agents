# Bob-the-Engineer: Design Document

## 1. Executive Summary

### Product Vision
Bob-the-Engineer is a highly reliable DevOps agent that integrates with popular coding agents (Claude Code, Cursor) to help engineers onboard and effectively use AI assistance on existing large codebases. By combining deterministic code execution with agentic reasoning, Bob ensures reliability while leveraging AI capabilities where they add the most value.

### Key Abstractions
Bob operates on three core abstractions:
1. **Workflow**: A sequence of deterministic and agentic tasks designed to achieve a DevOps goal
2. **Task**: Either deterministic (Python code) or agentic (coding agent with custom tools)
3. **Tool**: Mechanical subtasks within agentic tasks, implemented as Python functions

### Reliability Philosophy
Bob achieves high reliability through three levels of determinism:
1. **Workflow Level**: Prescribed sequence of tasks based on proven DevOps practices
2. **Task Level**: Mechanical operations (file I/O, command execution) implemented in Python
3. **Subtask Level**: Within agentic tasks, mechanical subtasks (hashing, time, DB queries) use code

### Supported Coding Agents
- **Claude Code**: Commands + hooks for workflows, subagents for agentic tasks
- **Cursor**: Commands for workflows and agentic tasks
- Future: GitHub Copilot, Cline

### Distribution Strategy
1. User installs via pip: `pip install bob-the-engineer`
2. User runs init: `bob init --coding-agent claude-code`
3. Bob analyzes repository and installs appropriate templates
4. Bob installs CLI commands that subagents can invoke via Bash tool
5. User commits configurations to repository
6. Team members get Bob workflows automatically


This design doc provides comprehensive specifications for both workflows with clear separation of deterministic and agentic tasks, specific tool definitions, and adapter implementations for both Claude Code and Cursor coding agents.

## 2. Technical Architecture

### File Structure
```
awesome-devops-for-coding-agents/
├── specs/
│   └── prd.md                      # This document
├── bob_the_engineer/
    ├── cli/
    │   ├── __init__.py
    │   └── app.py                 # Typer CLI entry point
    ├── workflows/
    │   ├── start_using_coding_agent/
    │   │   ├── prompt.md               # Workflow prompt
    │   │   ├── manifest.json           # name, version, inputs, requirements
    │   │   ├── agents/
    │   │   │   ├── code_analyzer.yaml  # policy: tools/limits/scopes
    │   │   │   ├── failure_analyst.yaml
    │   │   │   ├── setup_improver.yaml
    │   │   │   └── prompts/
    │   │   │       ├── code_analyzer.md
    │   │   │       ├── failure_analyst.md
    │   │   │       └── setup_improver.md
    │   │   ├── tasks/                  # deterministic tasks (python)
    │   │   │   ├── repo_scanner.py
    │   │   │   ├── feedback_validator.py
    │   │   │   ├── rule_generator.py
    │   │   │   └── config_writer.py
    │   │   └── tools/                  # custom tools callable by subagents
    │   │       ├── ast_parser.py
    │   │       ├── config_reader.py
    │   │       └── dependency_analyzer.py
    │   └── use_coding_agent_effectively/
    │       ├── prompt.md               # Workflow prompt
    │       ├── manifest.json           # name, version, inputs, requirements
    │       ├── agents/
    │       │   ├── guardrail_author.yaml
    │       │   ├── doc_writer.yaml
    │       │   ├── conflict_detector.yaml
    │       │   └── prompts/
    │       │       ├── guardrail_author.md
    │       │       ├── doc_writer.md
    │       │       └── conflict_detector.md
    │       ├── tasks/                  # deterministic tasks
    │       │   ├── supervisor_installer.py
    │       │   ├── tdd_setup.py
    │       │   ├── mcp_configurator.py
    │       │   └── command_consolidator.py
    │       └── tools/                  # custom tools
    │           ├── failure_mode_detector.py
    │           ├── log_instrumentor.py
    │           └── command_analyzer.py
    ├── core/                           # common code
    │   ├── __init__.py
    │   ├── models.py                  # shared data models
    │   └── utils.py                   # shared utilities
    ├── adapters/                       # agent-specific adapters
    │   ├── claude/
    │   │   ├── __init__.py
    │   │   ├── workflow_installer.py
    │   │   └── hook_manager.py
    │   ├── cursor/
    │   │   ├── __init__.py
    │   │   ├── workflow_installer.py
    │   │   └── mode_manager.py
    │   └── common/
    │       ├── __init__.py
    │       └── base_adapter.py
├── .claude/                        # end-state examples for target repo
│   ├── commands/
│   │   ├── start-using-coding-agent.md
│   │   └── use-coding-agent-effectively.md
│   ├── agents/
│   │   ├── code-analyzer.md
│   │   ├── failure-analyst.md
│   │   └── setup-improver.md
│   └── settings.json
├── .cursor/                        # end-state examples for target repo
│   └── commands/
│       ├── start-using-coding-agent.md
│       └── use-coding-agent-effectively.md
├── tests/
├── pyproject.toml
└── README.md
```

### CLI and Coding Agent Integration Points

#### CLI Commands
Bob's deterministic tasks and tools are exposed through a comprehensive CLI that coding agents can invoke:

```bash
# Repository analysis
bob repo-scan --path . --output-format json
```

This approach ensures:
- **Reliability**: Deterministic Python code handles mechanical tasks
- **Integration**: Coding agents use familiar Bash tool to invoke Bob commands
- **Transparency**: All operations are visible in agent conversation history
- **Debuggability**: Users can run the same commands manually for troubleshooting

#### Adapters for each Coding Agent
```python
# bob_the_engineer/adapters/base.py

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any

class CodingAgentAdapter(ABC):
    """Base adapter for coding agents"""

    @abstractmethod
    def install_workflow(self, workflow_name: str, repo_path: Path) -> None:
        """Install workflow for this coding agent"""
        pass

    @abstractmethod
    def configure_supervision(self, repo_path: Path, config: Dict[str, Any]) -> None:
        """Setup supervision for this coding agent"""
        pass

```


### Agentic Task Design


Agentic tasks require specialized tools that bridge the gap between high-level reasoning and deterministic execution. These tools are provided to coding agents via CLI commands that execute Python-based deterministic functions.


#### Tool Implementation via CLI Commands

Tools are exposed to agentic tasks through Bob's CLI interface:

```python
# bob_the_engineer/cli/tools.py
@app.command("repo-scan")
def repo_scanner(
    path: str = typer.Option(".", help="Repository path"),
    ignore_patterns: List[str] = typer.Option(None, help="Additional ignore patterns"),
    output_format: str = typer.Option("json", help="Output format: json, yaml, table")
) -> None:
    """Scan repository structure with gitignore support"""

    result = {
        "files_by_extension": scan_file_types(Path(path)),
        "directory_structure": build_directory_tree(Path(path)),
        "size_metrics": calculate_repo_metrics(Path(path)),
        "ignored_patterns": ignore_patterns or []
    }

    if output_format == "json":
        typer.echo(json.dumps(result, indent=2))
    elif output_format == "yaml":
        typer.echo(yaml.dump(result, indent=2))
    else:
        display_table(result)

```

### Deterministic Task Logic

Deterministic tasks handle mechanical operations where the exact sequence of steps is known. They prioritize reliability and predictability over flexibility.

Examples

**Settings Configuration Logic**:
```python
def configure_coding_agent_settings(agent_type: str, repo_path: Path) -> Dict[str, Any]:
    """Generate agent-specific settings with hooks and defaults"""

    if agent_type == "claude-code":
        return {
            "defaultMode": "plan",
            "tools": {
                "thinking": True,
                "allowedTools": ["Read", "Write", "Edit", "Bash", "Task"]
            },
            "hooks": generate_claude_hooks(repo_path),
            "environment": {
                "BOB_REPO_PATH": str(repo_path)
            }
        }
    elif agent_type == "cursor":
        return {
            "chat.mode": "plan-first",
            "agent.alwaysConfirm": True,
            "commands": generate_cursor_commands(repo_path)
        }
```

## 3. Workflow Specifications

### A. Start Using Coding Agent on Existing Large Code Repo

This workflow helps developers onboard coding agents to existing codebases by analyzing the repository, setting up rules, and validating feedback mechanisms.

#### Workflow Orchestration
```yaml
name: start-using-coding-agent
version: 1.0.0
description: Onboard coding agent to existing large codebase
tasks:
  - id: configure-rules
    type: agentic
    agent: rule-configurator
    inputs:
      repo_path: "${REPO_PATH}"
    outputs:
      - CLAUDE.md or .cursor/rules/*.mdc
    verification:
      command: bob-the-engineer verify-rules --repo-path ${REPO_PATH}

  - id: validate-feedback
    type: agentic
    agent: feedback-validator
    depends_on: [configure-rules]
    inputs:
      rules_file: "${configure-rules.output}"
    outputs:
      - validation_report.md
    verification:
      command: bob-the-engineer check-feedback-status --repo-path ${REPO_PATH}

  - id: configure-defaults
    type: deterministic
    command: bob-the-engineer configure-defaults
    inputs:
      agent_type: "${AGENT_TYPE}"
    outputs:
      - settings.json updates
```

#### Task 1: Configure Rules (Agentic)

**Agent**: rule-configurator
**Objective**: Analyze repository and generate comprehensive DevOps-focused rules

**Process**:
1. Scan repository structure using `bob-the-engineer repo-scan`
2. Detect languages, frameworks, and tools
3. Generate CLAUDE.md or cursor rules based on findings
4. Focus on DevOps practices, not application logic

**Available Tools**:
- `bob-the-engineer repo-scan --output-format json`
- `bob-the-engineer detect-stack --repo-path .`
- `bob-the-engineer analyze-deps --frameworks`
- `bob-the-engineer discover-commands --repo-path .`

**Output Schema**:
```markdown
# CLAUDE.md / .cursor/rules/devops.mdc

## Project Stack
- Language: [detected]
- Framework: [detected]
- Package Manager: [detected]
- Build Tool: [detected]

## Development Commands
- Install: [command]
- Build: [command]
- Test: [command]
- Lint: [command]
- Format: [command]

## DevOps Guidelines
[Generated rules based on stack]

## Anti-patterns to Avoid
[Stack-specific anti-patterns]
```

#### Task 2: Validate Feedback Mechanisms (Agentic)

**Agent**: feedback-validator
**Objective**: Test all feedback mechanisms and classify failures

**Process**:
1. Read rules from previous task
2. Execute each feedback mechanism
3. Classify failures as must-have or good-to-have
4. Debug must-have failures until fixed
5. Generate comprehensive report

**Available Tools**:
- `bob-the-engineer exec-with-analysis "[command]" --timeout 120`
- `bob-the-engineer classify-failure --type [build|lint|test]`
- `bob-the-engineer debug-failure --command "[command]" --error "[error]"`

**Failure Classification Logic**:
- **Must-Have**: Build failures, missing dependencies, environment issues
- **Good-to-Have**: Lint warnings, non-critical test failures, formatting issues

**Output Format**:
```markdown
# Feedback Mechanism Validation Report

## Summary
- Total mechanisms tested: X
- Passed: Y
- Must-fix failures: Z
- Optional fixes: W

## Must-Have Failures (Fixed)
1. [Issue]: [Resolution]

## Good-to-Have Issues (Pending)
1. [Issue]: [Recommendation]

## Verification Commands
- Build: `[command]` ✅
- Test: `[command]` ⚠️ (3 optional failures)
- Lint: `[command]` ✅
```

#### Task 3: Configure Best-Practice Defaults (Deterministic)

**CLI Command**: `bob-the-engineer configure-defaults`

**Implementation**:
```python
def configure_defaults(agent_type: str, repo_path: Path) -> Dict[str, Any]:
    """Configure agent with best practices while preserving user customizations"""

    existing_config = load_existing_config(agent_type, repo_path)

    if agent_type == "claude-code":
        defaults = {
            "defaultMode": "plan",  # Start in plan mode
            "thinking": True,
            "environment": {
                "BOB_REPO_PATH": str(repo_path),
                "BOB_INSTALLED": "true"
            }
        }
        # Merge strategy: preserve user settings, add new defaults
        merged = deep_merge(existing_config, defaults, prefer_existing=True)

    elif agent_type == "cursor":
        defaults = {
            "chat.mode": "ask-first",
            "agent.alwaysConfirm": True
        }
        merged = deep_merge(existing_config, defaults, prefer_existing=True)

    return merged
```

### B. Use Coding Agent Effectively on Existing Large Code Repo

This workflow enhances the coding agent setup with advanced workflows, MCP tools, and supervision.

#### Workflow Orchestration
```yaml
name: use-coding-agent-effectively
version: 1.0.0
description: Configure advanced features for effective coding agent usage
tasks:
  - id: configure-workflows
    type: deterministic
    command: bob-the-engineer install-workflows
    inputs:
      workflows: ["spec-driven", "tdd", "code-review"]
    outputs:
      - .claude/commands/* or .cursor/commands/*

  - id: configure-mcp
    type: deterministic
    command: bob-the-engineer configure-mcp
    inputs:
      servers: ["deepwiki", "github", "database"]
    outputs:
      - settings.json updates

  - id: configure-supervisor
    type: deterministic
    command: bob-the-engineer install-supervisor
    inputs:
      guards: ["file-guard", "tdd-guard", "self-review"]
    outputs:
      - hooks in settings.json
```

#### Task 4: Configure Best-Practice Development Workflows (Deterministic)

**CLI Command**: `bob-the-engineer install-workflows`

**Available Workflows**:
1. **Spec-Driven Development**: 6-phase iterative workflow
2. **TDD Workflow**: Test-first development with enforcement
3. **Code Review**: Multi-aspect parallel review
4. **Research Expert**: Parallel information gathering
5. **Triage Expert**: Context gathering and problem diagnosis

**Implementation**:
```python
def install_workflows(workflows: List[str], agent_type: str, repo_path: Path):
    """Install workflow templates for coding agent"""

    workflow_templates = {
        "spec-driven": load_template("workflows/spec_driven.md"),
        "tdd": load_template("workflows/tdd.md"),
        "code-review": load_template("workflows/code_review.md"),
        "research": load_template("workflows/research.md"),
        "triage": load_template("workflows/triage.md")
    }

    for workflow in workflows:
        template = workflow_templates[workflow]
        # Customize template for repo
        customized = customize_for_repo(template, repo_path)

        if agent_type == "claude-code":
            dest = repo_path / ".claude/commands" / f"{workflow}.md"
        else:
            dest = repo_path / ".cursor/commands" / f"{workflow}.md"

        write_preserving_user_content(dest, customized)
```

#### Task 5: Configure MCP Tools (Deterministic)

**CLI Command**: `bob-the-engineer configure-mcp`

**MCP Server Recommendations**:
- **Essential**: deepwiki (documentation), github (version control)
- **Recommended**: database (PostgreSQL/MongoDB), browser (testing)
- **Optional**: cloud providers, project management

**Implementation**:
```python
def configure_mcp(servers: List[str], repo_path: Path) -> Dict:
    """Configure MCP servers in settings.json"""

    mcp_configs = {
        "deepwiki": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"}
        },
        "database": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres"],
            "env": {"CONNECTION_STRING": "${DB_CONNECTION}"}
        }
    }

    settings = load_settings(repo_path / ".claude/settings.json")

    if "mcpServers" not in settings:
        settings["mcpServers"] = {}

    for server in servers:
        if server in mcp_configs and server not in settings["mcpServers"]:
            settings["mcpServers"][server] = mcp_configs[server]
            print(f"Added {server} MCP server configuration")
            print(f"To install: npm install -g @modelcontextprotocol/server-{server}")

    return settings
```

#### Task 6: Configure Coding Agent Supervisor (Deterministic)

**CLI Command**: `bob-the-engineer install-supervisor`

**Guard Priority Order**:
1. **file-guard**: Protect sensitive files (highest priority)
2. **tdd-guard**: Enforce test-first development
3. **self-review**: Catch implementation shortcuts

**Hook Conflict Resolution**:
- Disable guards in plan/ask mode
- Allow user to toggle guards via commands
- Provide clear feedback when guards block actions

**Implementation**:
```python
def install_supervisor(guards: List[str], repo_path: Path):
    """Install supervision hooks with proper priority and conflict resolution"""

    settings = load_settings(repo_path / ".claude/settings.json")

    hook_configs = {
        "file-guard": {
            "hook": "preToolUse",
            "script": "bob-the-engineer check-file-access --tool ${TOOL_NAME} --params '${TOOL_PARAMS}'",
            "priority": 1
        },
        "tdd-guard": {
            "hook": "preToolUse",
            "script": "bob-the-engineer check-tdd --enabled ${BOB_TDD_ENABLED:-true}",
            "priority": 2,
            "condition": "${CLAUDE_MODE} != 'plan'"  # Disable in plan mode
        },
        "self-review": {
            "hook": "postResponse",
            "script": "bob-the-engineer trigger-self-review --probability 0.3",
            "priority": 3
        }
    }

    if "hooks" not in settings:
        settings["hooks"] = {}

    # Sort by priority and install
    sorted_guards = sorted(guards, key=lambda g: hook_configs[g]["priority"])

    for guard in sorted_guards:
        config = hook_configs[guard]
        hook_type = config["hook"]

        if hook_type not in settings["hooks"]:
            settings["hooks"][hook_type] = []

        # Check for conflicts
        if not has_conflict(settings["hooks"][hook_type], config):
            settings["hooks"][hook_type].append({
                "name": guard,
                "script": config["script"],
                "condition": config.get("condition")
            })
```

### C. Improve Code Repo to Give Coding Agent More Autonomy

These workflows analyze the codebase and suggest improvements for better AI collaboration.

#### Task 7: Improve Feedback Mechanisms (Agentic)

**Agent**: feedback-improver
**Objective**: Analyze and improve build, test, and lint configurations

**Process**:
1. Scan current feedback mechanisms
2. Compare against best practices
3. Generate prioritized suggestions
4. Upon approval, implement improvements

**Available Tools**:
- `bob-the-engineer analyze-feedback-gaps --repo-path .`
- `bob-the-engineer suggest-linter-rules --language [lang]`
- `bob-the-engineer generate-precommit-config`

**Suggestion Format**:
```markdown
# Feedback Mechanism Improvements

## Critical (Blocking Issues)
1. **No formatter configured**
   - Impact: Inconsistent code style
   - Solution: Add prettier/black to pre-commit
   - Command: `bob-the-engineer add-formatter --language [lang]`

## High Priority
1. **Weak linter rules**
   - Current: 5 rules enabled
   - Recommended: 25+ rules
   - Solution: Enable recommended ruleset

## Medium Priority
[Grouped suggestions]
```

#### Task 8: Mitigate Conflicting Instructions (Agentic)

**Agent**: conflict-detector
**Objective**: Find and resolve conflicting or duplicate commands/configurations

**Process**:
1. Scan for duplicate command definitions
2. Identify outdated documentation
3. Find conflicting configurations
4. Propose consolidation strategy

**Available Tools**:
- `bob-the-engineer find-duplicate-commands`
- `bob-the-engineer check-doc-freshness`
- `bob-the-engineer analyze-config-conflicts`

**Detection Patterns**:
```python
CONFLICT_PATTERNS = {
    "duplicate_commands": [
        "Multiple test commands (npm test, yarn test, jest)",
        "Multiple lint commands with different configs",
        "Build commands in package.json vs Makefile"
    ],
    "outdated_docs": [
        "README instructions don't match actual commands",
        "Setup guide references deprecated dependencies",
        "API docs don't match implementation"
    ],
    "config_conflicts": [
        "ESLint vs Prettier rules conflict",
        "tsconfig.json vs babel.config.js conflicts",
        "Multiple .env files with different vars"
    ]
}
```

#### Task 9: Improve Debuggability (Agentic)

**Agent**: debuggability-improver
**Objective**: Enhance error handling, logging, and test feedback

**Process**:
1. Analyze error handling patterns
2. Review logging instrumentation
3. Assess test failure messages
4. Generate improvement plan
5. Implement approved changes in phases

**Available Tools**:
- `bob-the-engineer analyze-error-handling --repo-path .`
- `bob-the-engineer check-logging-coverage --verbosity [level]`
- `bob-the-engineer assess-test-quality --focus error-messages`

**Analysis Patterns**:
```python
DEBUGGABILITY_PATTERNS = {
    "error_handling": {
        "good": [
            "try/catch with specific error types",
            "Error messages with context",
            "Stack traces preserved"
        ],
        "bad": [
            "Silently swallowed exceptions",
            "Generic error messages",
            "Lost error context"
        ]
    },
    "logging": {
        "good": [
            "Entry/exit logging for key functions",
            "Structured logging with context",
            "Appropriate log levels"
        ],
        "bad": [
            "Console.log in production code",
            "Missing correlation IDs",
            "No request/response logging"
        ]
    },
    "test_quality": {
        "good": [
            "Descriptive test names",
            "Clear assertion messages",
            "Helpful failure output"
        ],
        "bad": [
            "assert(false) without message",
            "Cryptic test names",
            "No arrange-act-assert structure"
        ]
    }
}
```

**Implementation Phases**:
1. **Phase 1**: Add error context (non-breaking)
2. **Phase 2**: Improve logging (backwards compatible)
3. **Phase 3**: Enhance test messages (test-only changes)
4. **Verify**: Run feedback mechanisms after each phase

## 4. CLI Implementation Details

### Core CLI Structure

```python
# bob_the_engineer/cli/app.py
import typer
from typing import Optional, List
from pathlib import Path

app = typer.Typer(
    name="bob-the-engineer",
    help="DevOps automation for coding agents"
)

# Repository Analysis Commands
@app.command("repo-scan")
def repo_scan(
    path: Path = typer.Option(Path("."), "--path", "-p"),
    output_format: str = typer.Option("json", "--output-format", "-o"),
    ignore_patterns: Optional[List[str]] = typer.Option(None, "--ignore", "-i")
):
    """Scan repository structure and detect stack"""
    pass

@app.command("detect-stack")
def detect_stack(
    repo_path: Path = typer.Option(Path("."), "--repo-path", "-r")
):
    """Detect languages, frameworks, and tools"""
    pass

@app.command("discover-commands")
def discover_commands(
    repo_path: Path = typer.Option(Path("."), "--repo-path", "-r")
):
    """Discover build, test, lint commands"""
    pass

# Feedback Mechanism Commands
@app.command("exec-with-analysis")
def exec_with_analysis(
    command: str,
    timeout: int = typer.Option(120, "--timeout", "-t"),
    working_dir: Path = typer.Option(Path("."), "--working-dir", "-w")
):
    """Execute command and analyze output"""
    pass

@app.command("classify-failure")
def classify_failure(
    failure_type: str,
    error_message: str,
    context: Optional[str] = None
):
    """Classify failure as must-have or good-to-have"""
    pass

# Configuration Commands
@app.command("configure-defaults")
def configure_defaults(
    agent_type: str = typer.Option(..., "--agent-type", "-a"),
    repo_path: Path = typer.Option(Path("."), "--repo-path", "-r")
):
    """Configure agent with best practices"""
    pass

@app.command("install-workflows")
def install_workflows(
    workflows: List[str],
    agent_type: str = typer.Option(..., "--agent-type", "-a"),
    repo_path: Path = typer.Option(Path("."), "--repo-path", "-r")
):
    """Install workflow templates"""
    pass

@app.command("configure-mcp")
def configure_mcp(
    servers: List[str],
    repo_path: Path = typer.Option(Path("."), "--repo-path", "-r")
):
    """Configure MCP servers"""
    pass

@app.command("install-supervisor")
def install_supervisor(
    guards: List[str],
    repo_path: Path = typer.Option(Path("."), "--repo-path", "-r")
):
    """Install supervision hooks"""
    pass

# Analysis Commands
@app.command("analyze-feedback-gaps")
def analyze_feedback_gaps(
    repo_path: Path = typer.Option(Path("."), "--repo-path", "-r")
):
    """Analyze gaps in feedback mechanisms"""
    pass

@app.command("find-duplicate-commands")
def find_duplicate_commands(
    repo_path: Path = typer.Option(Path("."), "--repo-path", "-r")
):
    """Find duplicate or conflicting commands"""
    pass

@app.command("analyze-error-handling")
def analyze_error_handling(
    repo_path: Path = typer.Option(Path("."), "--repo-path", "-r"),
    language: Optional[str] = None
):
    """Analyze error handling patterns"""
    pass

# Health Check
@app.command("doctor")
def doctor(
    repair: bool = typer.Option(False, "--repair", "-r"),
    verbose: bool = typer.Option(False, "--verbose", "-v")
):
    """Check Bob installation health and repair if needed"""
    pass

# Init Command
@app.command("init")
def init(
    coding_agent: str = typer.Option(..., "--coding-agent", "-c"),
    repo_path: Path = typer.Option(Path("."), "--repo-path", "-r"),
    workflows: Optional[List[str]] = typer.Option(None, "--workflows", "-w")
):
    """Initialize Bob in a repository"""
    pass

if __name__ == "__main__":
    app()
```

### Configuration Merge Strategy

```python
# bob_the_engineer/core/config_manager.py
from typing import Dict, Any
import json
from pathlib import Path

def deep_merge(existing: Dict[str, Any], new: Dict[str, Any],
               prefer_existing: bool = True) -> Dict[str, Any]:
    """
    Deep merge two dictionaries with conflict resolution

    Args:
        existing: Current user configuration
        new: New configuration to merge
        prefer_existing: If True, preserve user customizations
    """
    result = existing.copy()

    for key, value in new.items():
        if key not in result:
            # Add new key
            result[key] = value
        elif isinstance(value, dict) and isinstance(result[key], dict):
            # Recursively merge nested dicts
            result[key] = deep_merge(result[key], value, prefer_existing)
        elif isinstance(value, list) and isinstance(result[key], list):
            # Merge lists (avoid duplicates)
            if prefer_existing:
                # Add new items that don't exist
                for item in value:
                    if item not in result[key]:
                        result[key].append(item)
            else:
                # Replace with new list
                result[key] = value
        else:
            # Conflict: decide based on preference
            if not prefer_existing:
                result[key] = value
            # else keep existing value

    return result

def load_settings(settings_path: Path) -> Dict[str, Any]:
    """Load settings.json with error handling"""
    if not settings_path.exists():
        return {}

    try:
        with open(settings_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Backup corrupted file
        backup = settings_path.with_suffix('.json.backup')
        settings_path.rename(backup)
        return {}

def save_settings(settings_path: Path, settings: Dict[str, Any]):
    """Save settings with pretty printing and validation"""
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2, sort_keys=True)
```

### Doctor Command Implementation

```python
# bob_the_engineer/cli/doctor.py
from pathlib import Path
from typing import List, Tuple
import subprocess
import sys
import os

class HealthCheck:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.issues: List[Tuple[str, str]] = []

    def check_installation(self) -> bool:
        """Check if Bob is properly installed"""
        checks = [
            self.check_cli_accessible(),
            self.check_python_version(),
            self.check_dependencies(),
            self.check_templates(),
            self.check_permissions()
        ]
        return all(checks)

    def check_cli_accessible(self) -> bool:
        """Check if bob-the-engineer command is in PATH"""
        try:
            result = subprocess.run(
                ["which", "bob-the-engineer"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                self.issues.append((
                    "CLI not in PATH",
                    "Run: pip install -e . or add to PATH"
                ))
                return False
            return True
        except Exception as e:
            self.issues.append(("CLI check failed", str(e)))
            return False

    def check_python_version(self) -> bool:
        """Check Python version compatibility"""
        if sys.version_info < (3, 8):
            self.issues.append((
                "Python version too old",
                f"Found {sys.version}, need >= 3.8"
            ))
            return False
        return True

    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed"""
        required = ["typer", "pyyaml", "jsonschema"]
        missing = []

        for dep in required:
            try:
                __import__(dep)
            except ImportError:
                missing.append(dep)

        if missing:
            self.issues.append((
                "Missing dependencies",
                f"Run: pip install {' '.join(missing)}"
            ))
            return False
        return True

    def check_templates(self) -> bool:
        """Check if workflow templates are present"""
        template_dir = Path(__file__).parent.parent / "workflows"

        if not template_dir.exists():
            self.issues.append((
                "Templates directory missing",
                "Reinstall Bob or check installation"
            ))
            return False

        required_templates = [
            "start_using_coding_agent/prompt.md",
            "use_coding_agent_effectively/prompt.md"
        ]

        for template in required_templates:
            if not (template_dir / template).exists():
                self.issues.append((
                    f"Missing template: {template}",
                    "Reinstall Bob or check installation"
                ))
                return False

        return True

    def check_permissions(self) -> bool:
        """Check file permissions for Bob directories"""
        bob_dir = Path.home() / ".bob-the-engineer"

        if bob_dir.exists() and not os.access(bob_dir, os.W_OK):
            self.issues.append((
                "Permission denied for Bob directory",
                f"Run: chmod -R u+w {bob_dir}"
            ))
            return False

        return True

    def repair(self) -> bool:
        """Attempt to repair found issues"""
        repaired = []

        for issue, solution in self.issues:
            if "pip install" in solution:
                # Auto-install missing dependencies
                cmd = solution.split("Run: ")[1]
                result = subprocess.run(cmd, shell=True)
                if result.returncode == 0:
                    repaired.append(issue)

            elif "chmod" in solution:
                # Fix permissions
                cmd = solution.split("Run: ")[1]
                result = subprocess.run(cmd, shell=True)
                if result.returncode == 0:
                    repaired.append(issue)

        # Remove repaired issues
        self.issues = [
            (issue, solution)
            for issue, solution in self.issues
            if issue not in repaired
        ]

        return len(self.issues) == 0
```

## 5. Error Handling and Recovery

### Workflow Error Handling

```python
# bob_the_engineer/core/workflow_executor.py
from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class TaskResult:
    status: TaskStatus
    output: Optional[Any] = None
    error: Optional[str] = None
    reason: Optional[str] = None
    verification_failed: bool = False
    verification_output: Optional[str] = None

@dataclass
class WorkflowResult:
    success: bool
    task_results: Dict[str, TaskResult]

class WorkflowExecutor:
    def __init__(self, workflow_config: Dict[str, Any]):
        self.config = workflow_config
        self.task_results: Dict[str, TaskResult] = {}

    def execute(self) -> WorkflowResult:
        """Execute workflow with dependency-aware error handling"""

        tasks = self.config["tasks"]
        task_graph = self.build_dependency_graph(tasks)

        for task in self.topological_sort(task_graph):
            # Check if dependencies succeeded
            if not self.can_execute(task):
                self.task_results[task.id] = TaskResult(
                    status=TaskStatus.SKIPPED,
                    reason="Dependency failed"
                )
                continue

            try:
                result = self.execute_task(task)
                self.task_results[task.id] = result

                # Run verification if specified
                if task.verification:
                    self.verify_task(task, result)

            except Exception as e:
                self.task_results[task.id] = TaskResult(
                    status=TaskStatus.FAILED,
                    error=str(e)
                )

                # Continue with non-dependent tasks
                if not task.critical:
                    continue
                else:
                    # Critical task failed, stop workflow
                    break

        return WorkflowResult(
            success=self.all_critical_succeeded(),
            task_results=self.task_results
        )

    def can_execute(self, task: Any) -> bool:
        """Check if task dependencies are satisfied"""
        if not task.get('depends_on'):
            return True

        for dep_id in task['depends_on']:
            if dep_id not in self.task_results:
                return False
            if self.task_results[dep_id].status != TaskStatus.SUCCESS:
                return False

        return True

    def verify_task(self, task: Any, result: TaskResult):
        """Run verification command for task output"""
        if task.get('verification'):
            verify_result = subprocess.run(
                task['verification']['command'],
                shell=True,
                capture_output=True,
                text=True
            )

            if verify_result.returncode != 0:
                result.verification_failed = True
                result.verification_output = verify_result.stderr
```

## 6. Integration Testing Strategy

### Test Structure

```python
# tests/integration/test_workflows.py
import pytest
from pathlib import Path
import tempfile
import shutil
import subprocess
import json

@pytest.fixture
def test_repo():
    """Create a test repository with common patterns"""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)

        # Create typical repo structure
        (repo_path / "src").mkdir()
        (repo_path / "tests").mkdir()
        (repo_path / "package.json").write_text("""{
            "scripts": {
                "test": "jest",
                "lint": "eslint src/",
                "build": "tsc"
            }
        }""")

        yield repo_path

def test_start_using_coding_agent_workflow(test_repo):
    """Test the complete onboarding workflow"""

    # Initialize Bob
    result = subprocess.run([
        "bob-the-engineer", "init",
        "--coding-agent", "claude-code",
        "--repo-path", str(test_repo)
    ], capture_output=True)

    assert result.returncode == 0

    # Check created files
    claude_dir = test_repo / ".claude"
    assert claude_dir.exists()
    assert (claude_dir / "CLAUDE.md").exists()
    assert (claude_dir / "settings.json").exists()

    # Verify settings content
    settings = json.loads((claude_dir / "settings.json").read_text())
    assert settings["defaultMode"] == "plan"
    assert "BOB_REPO_PATH" in settings.get("environment", {})

def test_feedback_validation(test_repo):
    """Test feedback mechanism validation"""

    result = subprocess.run([
        "bob-the-engineer", "exec-with-analysis",
        "npm test",
        "--working-dir", str(test_repo),
        "--timeout", "30"
    ], capture_output=True, text=True)

    # Parse result
    output = json.loads(result.stdout)
    assert "status" in output
    assert "classification" in output

    if output["status"] == "failed":
        assert output["classification"] in ["must-have", "good-to-have"]
```

## 7. Performance Considerations

### Optimization Strategies

```python
# bob_the_engineer/core/performance.py
from functools import lru_cache
from typing import Dict, Any
import hashlib
import json

class PerformanceOptimizer:
    def __init__(self):
        self.cache = {}

    @lru_cache(maxsize=128)
    def get_repo_analysis(self, repo_path: str) -> Dict[str, Any]:
        """Cache repository analysis results"""

        # Generate cache key based on repo state
        cache_key = self.generate_repo_hash(repo_path)

        if cache_key in self.cache:
            return self.cache[cache_key]

        # Perform analysis
        analysis = self.analyze_repository(repo_path)
        self.cache[cache_key] = analysis

        return analysis

    def generate_repo_hash(self, repo_path: str) -> str:
        """Generate hash of repo structure for caching"""

        hasher = hashlib.md5()

        # Hash key files that indicate repo state
        key_files = [
            "package.json", "pyproject.toml", "Cargo.toml",
            "go.mod", "pom.xml", "build.gradle"
        ]

        for file in key_files:
            file_path = Path(repo_path) / file
            if file_path.exists():
                hasher.update(file_path.read_bytes())

        return hasher.hexdigest()

    def parallel_task_execution(self, tasks: List[Any]) -> Dict[str, TaskResult]:
        """Execute independent tasks in parallel"""

        from concurrent.futures import ThreadPoolExecutor, as_completed

        # Group tasks by dependencies
        independent_tasks = [t for t in tasks if not t.get('depends_on')]

        results = {}

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self.execute_task, task): task
                for task in independent_tasks
            }

            for future in as_completed(futures):
                task = futures[future]
                try:
                    results[task['id']] = future.result()
                except Exception as e:
                    results[task['id']] = TaskResult(
                        status=TaskStatus.FAILED,
                        error=str(e)
                    )

        return results
```
