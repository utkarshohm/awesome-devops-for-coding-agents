# Bob-the-Engineer: Comprehensive Design Document

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

### Distribution Strategy
1. User installs via pip: `pip install bob-the-engineer`
2. User runs init: `bob init --coding-agent claude-code`
3. Bob analyzes repository and installs appropriate templates
4. Bob installs CLI commands that subagents can invoke via Bash tool
5. User commits configurations to repository
6. Team members get Bob workflows automatically

## 2. Technical Architecture

### File Structure
```
bob_the_engineer/
├── cli/
│   ├── __init__.py
│   └── app.py                 # Typer CLI entry point
├── workflows/
│   ├── start_using_coding_agent/
│   │   ├── workflow.md               # Workflow prompt
│   │   ├── manifest.json           # name, version, inputs, requirements
│   │   ├── agents/
│   │   │   ├── configure_rules.md
│   │   │   ├── validate_feedback.md
│   │   │   └── configure_defaults.md
│   │   ├── tasks/                  # deterministic tasks (python)
│   │   │   ├── repo_scanner.py
│   │   │   ├── feedback_validator.py
│   │   │   ├── rule_generator.py
│   │   │   └── config_writer.py
│   │   └── tools/                  # custom tools callable by subagents
│   │       ├── ast_parser.py
│   │       ├── config_reader.py
│   │       └── dependency_analyzer.py
│   ├── use_coding_agent_effectively/
│   │   ├── workflow.md               # Workflow prompt
│   │   ├── manifest.json           # name, version, inputs, requirements
│   │   ├── agents/
│   │   │   ├── configure_workflows.md
│   │   │   ├── configure_mcp.md
│   │   │   └── configure_supervisor.md
│   │   ├── tasks/                  # deterministic tasks
│   │   │   ├── supervisor_installer.py
│   │   │   ├── tdd_setup.py
│   │   │   ├── mcp_configurator.py
│   │   │   └── command_consolidator.py
│   │   └── tools/                  # custom tools
│   │       ├── failure_mode_detector.py
│   │       ├── log_instrumentor.py
│   │       └── command_analyzer.py
│   └── improve_coding_agent_autonomy/
│       ├── workflow.md               # Workflow prompt
│       ├── manifest.json           # name, version, inputs, requirements
│       ├── agents/
│       │   ├── improve_feedback.md
│       │   ├── mitigate_conflicts.md
│       │   └── improve_debuggability.md
│       ├── tasks/                  # deterministic tasks
│       │   ├── feedback_analyzer.py
│       │   ├── conflict_detector.py
│       │   └── debuggability_enhancer.py
│       └── tools/                  # custom tools
│           ├── pattern_matcher.py
│           ├── code_analyzer.py
│           └── suggestion_generator.py
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
├── templates/                      # end-state examples for target repo
│   ├── claude/
│   │   ├── commands/
│   │   │   ├── start-using-coding-agent.md
│   │   │   ├── use-coding-agent-effectively.md
│   │   │   └── improve-coding-agent-autonomy.md
│   │   ├── agents/
│   │   │   ├── configure-rules.md
│   │   │   ├── validate-feedback.md
│   │   │   ├── configure-defaults.md
│   │   │   ├── configure-workflows.md
│   │   │   ├── configure-mcp.md
│   │   │   ├── configure-supervisor.md
│   │   │   ├── improve-feedback.md
│   │   │   ├── mitigate-conflicts.md
│   │   │   └── improve-debuggability.md
│   │   └── settings.json
│   └── cursor/
│       └── commands/
│           ├── start-using-coding-agent.md
│           ├── use-coding-agent-effectively.md
│           └── improve-coding-agent-autonomy.md
```

## 3. Workflow Implementations

### Workflow A: Start Using Coding Agent on Existing Large Code Repo

#### Overview
This workflow onboards teams to use coding agents effectively on existing codebases by configuring essential rules, validating feedback mechanisms, and setting best-practice defaults.

#### Workflow Prompt
```markdown
# Start Using Coding Agent

This workflow helps you configure a coding agent for effective use on an existing large codebase.

## Objectives
1. Configure coding agent with repository-specific rules
2. Validate all feedback mechanisms work correctly
3. Set best-practice defaults for agent behavior

## Tasks Sequence
1. !bob configure-rules --repo-path . --agent {agent_type}
2. @configure-rules
3. !bob validate-feedback --repo-path .
4. @validate-feedback
5. !bob configure-defaults --repo-path . --agent {agent_type}

## Success Criteria
- All feedback mechanisms (build, lint, test) pass
- Agent has comprehensive repository context
- Default settings promote good development practices

## Inputs
- Repository path
- Coding agent type (claude-code, cursor)

## Outputs
- CLAUDE.md or .cursor/rules/*.mdc files
- Validation report showing feedback mechanism status
- Updated settings.json with best practices
```

#### Task 1: Configure Rules (Agentic)

**Agent Definition (configure-rules.md)**:
```markdown
---
name: configure-rules
description: Analyze repository structure and generate coding agent rules focused on DevOps practices, not application logic
tools: [repo-scan, analyze-deps, discover-commands, generate-rules]
model: claude-3-5-sonnet-20241022
max_tokens: 8192
---

You are a DevOps Configuration Expert specializing in analyzing codebases and generating optimal coding agent rules.

## Objective
Analyze the repository structure, languages, frameworks, and development tools to generate comprehensive coding agent rules that focus on DevOps practices rather than application logic.

## Available Tools
- `bob repo-scan`: Scan repository structure and file types
- `bob analyze-deps`: Analyze dependencies and frameworks
- `bob discover-commands`: Find build, test, lint commands
- `bob generate-rules`: Generate rules based on analysis

## Process
1. **Repository Analysis**: Use repo-scan to understand codebase structure
2. **Technology Stack Detection**: Use analyze-deps to identify languages/frameworks
3. **Command Discovery**: Use discover-commands to find existing workflows
4. **Rule Generation**: Use generate-rules to create comprehensive rules

## Rule Categories to Generate
1. **Development Workflow**: Installation, build, test, lint commands
2. **Code Quality**: Formatting, linting, type checking standards
3. **Project Structure**: Directory conventions, file organization
4. **DevOps Practices**: CI/CD, deployment, monitoring patterns
5. **Anti-patterns**: Common mistakes to avoid for this tech stack

## Output Format
Generate rules in the appropriate format for the target coding agent:
- Claude Code: CLAUDE.md file at repository root
- Cursor: Multiple .mdc files in .cursor/rules/ directory

## Success Criteria
- Rules cover all detected technologies and frameworks
- Focus on mechanical DevOps tasks, not application logic
- Include specific commands for common workflows
- Avoid duplicating built-in coding agent capabilities
```

**CLI Commands**:
```bash
# Repository scanning
bob repo-scan --path <path> --output-format json
bob analyze-deps --path <path> --detect-frameworks --detect-build-tools
bob discover-commands --repo-path <path> --command-types build,test,lint,format

# Rule generation
bob generate-rules --analysis-file <analysis.json> --agent-type <agent> --output-path <path>
```

**Python Interfaces**:
```python
@dataclass
class RepoAnalysis:
    languages: Dict[str, float]  # language -> percentage
    frameworks: List[str]
    build_tools: List[str]
    test_frameworks: List[str]
    linters: List[str]
    formatters: List[str]
    package_managers: List[str]
    ci_platforms: List[str]
    directory_structure: Dict[str, Any]
    file_counts: Dict[str, int]

@dataclass
class CommandDiscovery:
    build_commands: List[str]
    test_commands: List[str]
    lint_commands: List[str]
    format_commands: List[str]
    install_commands: List[str]
    run_commands: List[str]

def repo_scanner(path: Path, ignore_patterns: List[str] = None) -> RepoAnalysis:
    """Scan repository structure with gitignore support"""

def analyze_dependencies(path: Path, detect_frameworks: bool = True) -> RepoAnalysis:
    """Analyze package files to detect dependencies and frameworks"""

def discover_commands(repo_path: Path, command_types: List[str]) -> CommandDiscovery:
    """Discover build, test, lint commands from package.json, Makefile, etc"""

def generate_rules(analysis: RepoAnalysis, agent_type: str, output_path: Path) -> None:
    """Generate coding agent rules based on repository analysis"""
```

#### Task 2: Validate Feedback Mechanisms (Agentic)

**Agent Definition (validate-feedback.md)**:
```markdown
---
name: validate-feedback
description: Run all feedback mechanisms and debug must-have failures to ensure coding agent can work effectively
tools: [run-feedback-checks, analyze-failures, debug-failures, generate-report]
model: claude-3-5-sonnet-20241022
max_tokens: 8192
---

You are a DevOps Validation Expert specializing in testing and debugging development feedback mechanisms.

## Objective
Run all discovered feedback mechanisms (build, lint, test, format) and debug critical failures to ensure a coding agent can work effectively in this repository.

## Available Tools
- `bob run-feedback-checks`: Execute all discovered commands
- `bob analyze-failures`: Categorize failures by severity
- `bob debug-failures`: Attempt to fix must-have failures
- `bob generate-report`: Create validation report

## Process
1. **Execute All Checks**: Run build, lint, test, format commands
2. **Analyze Results**: Categorize failures as must-have vs nice-to-have
3. **Debug Critical Issues**: Fix must-have failures iteratively
4. **Generate Report**: Document remaining issues and fixes applied

## Failure Classification
- **Must-Have**: Failures that prevent basic development workflow
- **Nice-to-Have**: Style, optimization, or enhancement issues

## Output
Generate a comprehensive validation report showing:
- Status of each feedback mechanism
- List of fixed issues with explanations
- Remaining issues categorized by priority
- Recommendations for manual fixes
```

**CLI Commands**:
```bash
# Feedback validation
bob run-feedback-checks --repo-path <path> --timeout 300 --output-format json
bob analyze-failures --results-file <results.json> --categorize-severity
bob debug-failures --failure-file <failures.json> --max-attempts 3
bob generate-report --results <results.json> --fixes <fixes.json> --output <report.md>
```

**Python Interfaces**:
```python
@dataclass
class FeedbackResult:
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration: float
    timestamp: datetime

@dataclass
class FailureAnalysis:
    failure_type: str  # build, lint, test, format
    severity: str  # must_have, nice_to_have
    description: str
    suggested_fix: str
    auto_fixable: bool

def run_feedback_checks(repo_path: Path, timeout: int = 300) -> List[FeedbackResult]:
    """Execute all discovered feedback commands"""

def analyze_failures(results: List[FeedbackResult]) -> List[FailureAnalysis]:
    """Categorize failures by type and severity"""

def debug_failures(failures: List[FailureAnalysis], max_attempts: int = 3) -> List[Dict[str, Any]]:
    """Attempt to automatically fix critical failures"""
```

#### Task 3: Configure Best-Practice Defaults (Deterministic)

**CLI Command**:
```bash
bob configure-defaults --agent-type <claude-code|cursor> --repo-path <path> --enable-plan-mode
```

**Python Interface**:
```python
def configure_defaults(agent_type: str, repo_path: Path, enable_plan_mode: bool = True) -> None:
    """Configure best-practice defaults for coding agent"""

@dataclass
class AgentDefaults:
    default_mode: str  # plan, ask
    allowed_tools: List[str]
    hooks: Dict[str, Any]
    permissions: Dict[str, List[str]]
    environment: Dict[str, str]
```

**JSON Schemas**:
```json
// Claude Code Settings Schema
{
  "type": "object",
  "properties": {
    "defaultMode": {"type": "string", "enum": ["plan", "ask", "code"]},
    "tools": {
      "type": "object",
      "properties": {
        "thinking": {"type": "boolean"},
        "allowedTools": {"type": "array", "items": {"type": "string"}}
      }
    },
    "hooks": {"type": "object"},
    "environment": {"type": "object"},
    "permissions": {
      "type": "object",
      "properties": {
        "allow": {"type": "array", "items": {"type": "string"}},
        "deny": {"type": "array", "items": {"type": "string"}}
      }
    }
  }
}
```

### Workflow B: Use Coding Agent Effectively on Existing Large Code Repo

#### Overview
This workflow configures advanced development workflows, necessary MCP tools, and supervision to maximize coding agent effectiveness.

#### Workflow Prompt
```markdown
# Use Coding Agent Effectively

This workflow configures advanced capabilities for effective coding agent use on large codebases.

## Objectives
1. Configure proven development workflows (TDD, spec-driven development)
2. Install necessary MCP tools for enhanced capabilities
3. Configure coding agent supervision to catch common failure modes

## Tasks Sequence
1. !bob configure-workflows --repo-path . --agent {agent_type}
2. @configure-workflows
3. !bob configure-mcp --repo-path . --agent {agent_type}
4. @configure-mcp
5. !bob configure-supervisor --repo-path . --agent {agent_type}
6. @configure-supervisor

## Success Criteria
- Development workflows are accessible to coding agent
- MCP tools provide enhanced capabilities
- Supervisor catches common failure modes

## Inputs
- Repository path
- Coding agent type
- Selected workflow templates
- MCP server preferences

## Outputs
- Workflow command/agent files
- Updated settings.json with MCP configuration
- Supervisor hooks configuration
```

#### Task 4: Configure Best-Practice Development Workflows (Deterministic)

**CLI Command**:
```bash
bob configure-workflows --repo-path <path> --agent-type <agent> --workflows tdd,spec-driven,pr-review
```

**Python Interface**:
```python
@dataclass
class WorkflowTemplate:
    name: str
    description: str
    agent_type: str  # claude-code, cursor, both
    file_content: str
    dependencies: List[str]

def configure_workflows(repo_path: Path, agent_type: str, workflows: List[str]) -> None:
    """Install selected workflow templates for the coding agent"""

def get_available_workflows() -> List[WorkflowTemplate]:
    """Return list of available workflow templates"""
```

#### Task 5: Configure Necessary MCP Tools (Deterministic)

**Recommended MCP Servers**:
Based on research, here are the most useful MCP servers for development:

1. **GitHub Integration**: `@modelcontextprotocol/server-github`
2. **Filesystem Access**: `@modelcontextprotocol/server-filesystem`
3. **Database Access**: `@modelcontextprotocol/server-postgresql`, `@modelcontextprotocol/server-mysql`
4. **Web Search**: `@modelcontextprotocol/server-web-search`
5. **Documentation**: `deepgraph-mcp` for code documentation
6. **Browser Automation**: `@modelcontextprotocol/server-playwright`

**CLI Command**:
```bash
bob configure-mcp --repo-path <path> --agent-type <agent> --servers github,filesystem,docs
```

**Python Interface**:
```python
@dataclass
class MCPServer:
    name: str
    package: str
    description: str
    required_env: List[str]
    recommended_for: List[str]  # frameworks/languages

def configure_mcp_tools(repo_path: Path, agent_type: str, servers: List[str]) -> None:
    """Configure MCP servers in coding agent settings"""

def get_recommended_mcp_servers(repo_analysis: RepoAnalysis) -> List[MCPServer]:
    """Recommend MCP servers based on repository characteristics"""
```

**MCP Configuration Templates**:
```json
// GitHub MCP Server
{
  "mcpServers": {
    "github": {
      "description": "GitHub API integration for repository management",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
      }
    }
  }
}

// Filesystem MCP Server
{
  "mcpServers": {
    "filesystem": {
      "description": "Secure filesystem access with directory permissions",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    }
  }
}
```

#### Task 6: Configure Coding Agent Supervisor (Deterministic)

**Language-Agnostic Supervisor Design**:
Based on TDD Guard patterns but generalized for any language/framework.

**CLI Command**:
```bash
bob configure-supervisor --repo-path <path> --agent-type <agent> --rules <rules.json>
```

**Python Interface**:
```python
@dataclass
class SupervisorRule:
    name: str
    description: str
    trigger_patterns: List[str]  # regex patterns for file paths/content
    violation_patterns: List[str]  # patterns that indicate violations
    languages: List[str]  # applicable languages, empty = all
    frameworks: List[str]  # applicable frameworks, empty = all
    severity: str  # error, warning, info

@dataclass
class SupervisorConfig:
    enabled: bool
    rules: List[SupervisorRule]
    model: str
    max_tokens: int
    timeout: int

def configure_supervisor(repo_path: Path, agent_type: str, rules_file: Path = None) -> None:
    """Configure language-agnostic coding agent supervisor"""
```

**Supervisor Hook Template**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bob supervisor-check --file \"$CLAUDE_TOOL_FILE_PATH\" --content \"$CLAUDE_TOOL_CONTENT\""
          }
        ]
      }
    ]
  }
}
```

### Workflow C: Improve Code Repo to Give Coding Agent More Autonomy

#### Overview
This workflow analyzes and improves the codebase to enable greater coding agent autonomy through better feedback mechanisms, conflict resolution, and debuggability.

#### Workflow Prompt
```markdown
# Improve Coding Agent Autonomy

This workflow improves the codebase to enable greater coding agent autonomy.

## Objectives
1. Improve feedback mechanisms for coding agent effectiveness
2. Mitigate conflicting instructions that confuse agents
3. Improve debuggability for efficient failure analysis

## Tasks Sequence
1. !bob analyze-feedback --repo-path .
2. @improve-feedback
3. !bob detect-conflicts --repo-path .
4. @mitigate-conflicts
5. !bob analyze-debuggability --repo-path .
6. @improve-debuggability

## Success Criteria
- Feedback mechanisms provide clear, actionable results
- No conflicting development instructions
- Errors are informative and traceable

## Inputs
- Repository path
- Improvement preferences
- Risk tolerance levels

## Outputs
- Updated codebase with improved practices
- Conflict resolution changes
- Enhanced error handling and logging
```

#### Task 7: Improve Feedback Mechanisms (Agentic)

**Agent Definition (improve-feedback.md)**:
```markdown
---
name: improve-feedback
description: Analyze and improve development feedback mechanisms to provide clearer, more actionable results for coding agents
tools: [analyze-feedback, suggest-improvements, implement-improvements]
model: claude-3-5-sonnet-20241022
max_tokens: 8192
---

You are a DevOps Feedback Expert specializing in improving development feedback mechanisms.

## Objective
Analyze current feedback mechanisms and suggest improvements to make them more effective for coding agent workflows.

## Available Tools
- `bob analyze-feedback`: Analyze current feedback quality
- `bob suggest-improvements`: Generate improvement suggestions
- `bob implement-improvements`: Apply approved improvements

## Analysis Areas
1. **Linter Configuration**: Coverage, rules, output format
2. **Test Setup**: Coverage, reporting, performance
3. **Build Process**: Speed, clarity, error messages
4. **Pre-commit Hooks**: Completeness, reliability
5. **CI/CD Pipeline**: Feedback speed, clarity

## Improvement Categories
1. **Missing Tools**: Formatters, linters, test runners
2. **Poor Configuration**: Too few rules, unclear output
3. **Security Gaps**: Missing security checks
4. **Performance Issues**: Slow feedback loops

## Output Format
Generate structured improvement suggestions with:
- Priority level (high, medium, low)
- Implementation complexity (easy, medium, hard)
- Expected benefit description
- Specific implementation steps
```

#### Task 8: Mitigate Conflicting Instructions (Agentic)

**Agent Definition (mitigate-conflicts.md)**:
```markdown
---
name: mitigate-conflicts
description: Detect and resolve conflicting development instructions that confuse coding agents
tools: [detect-conflicts, analyze-conflicts, resolve-conflicts]
model: claude-3-5-sonnet-20241022
max_tokens: 8192
---

You are a DevOps Conflict Resolution Expert specializing in identifying and resolving conflicting development instructions.

## Objective
Find instances where there are multiple ways to do the same thing and consolidate to single, clear approaches.

## Available Tools
- `bob detect-conflicts`: Find conflicting instructions/commands
- `bob analyze-conflicts`: Analyze impact and resolution options
- `bob resolve-conflicts`: Implement conflict resolutions

## Conflict Types to Detect
1. **Multiple Build Commands**: npm vs yarn, make vs cmake
2. **Duplicate Linters**: Multiple linters for same language
3. **Conflicting Documentation**: README vs wiki vs comments
4. **Outdated Instructions**: Old vs new processes
5. **Tool Redundancy**: Multiple tools for same purpose

## Resolution Strategies
1. **Consolidation**: Choose single tool, update all references
2. **Documentation**: Update to single source of truth
3. **Deprecation**: Remove outdated approaches
4. **Standardization**: Enforce consistent patterns

## Output Format
Generate conflict resolution plan with:
- Detected conflicts with examples
- Recommended resolution for each
- Implementation steps
- Risk assessment
```

#### Task 9: Improve Debuggability (Agentic)

**Agent Definition (improve-debuggability.md)**:
```markdown
---
name: improve-debuggability
description: Enhance error handling, logging, and test failure messages to improve coding agent debugging efficiency
tools: [analyze-debuggability, suggest-logging, improve-error-handling, enhance-test-messages]
model: claude-3-5-sonnet-20241022
max_tokens: 8192
---

You are a DevOps Debuggability Expert specializing in improving error handling and diagnostic capabilities.

## Objective
Analyze and improve error handling, logging, and test failure messages to enable coding agents to debug issues efficiently.

## Available Tools
- `bob analyze-debuggability`: Analyze current error handling patterns
- `bob suggest-logging`: Recommend logging improvements
- `bob improve-error-handling`: Enhance error messages and propagation
- `bob enhance-test-messages`: Improve test failure diagnostics

## Analysis Areas
1. **Error Handling**: Catch/throw patterns, message quality
2. **Error Propagation**: Call stack preservation
3. **Logging**: Placement, levels, context
4. **Test Messages**: Failure clarity, actionable information

## Improvement Patterns
1. **Informative Errors**: Include context, cause, suggested actions
2. **Structured Logging**: Consistent format, appropriate levels
3. **Error Propagation**: Preserve stack traces, add context
4. **Test Diagnostics**: Clear assertions, helpful failure messages

## Output Format
Generate debuggability improvement plan with:
- Current patterns analysis
- Specific improvement suggestions by file/function
- Implementation priority
- Code examples and templates
```

## 4. CLI Command Specifications

### Repository Analysis Commands

```bash
# bob repo-scan
bob repo-scan [OPTIONS]

OPTIONS:
  --path TEXT             Repository path to scan [default: .]
  --ignore-patterns TEXT  Additional gitignore patterns
  --output-format TEXT    Output format: json, yaml, table [default: json]
  --include-metrics       Include size and complexity metrics
  --max-depth INTEGER     Maximum directory depth to scan [default: 10]

OUTPUT:
{
  "languages": {"python": 65.2, "typescript": 30.1, "yaml": 4.7},
  "frameworks": ["fastapi", "react", "pytest"],
  "build_tools": ["npm", "pip"],
  "package_managers": ["npm", "pip"],
  "directory_structure": {...},
  "file_counts": {"total": 1247, "source": 892, "test": 156, "config": 199},
  "metrics": {"total_size_bytes": 12458790, "avg_file_size": 999.1}
}
```

```bash
# bob analyze-deps
bob analyze-deps [OPTIONS]

OPTIONS:
  --path TEXT              Repository path [default: .]
  --detect-frameworks      Detect web/app frameworks
  --detect-build-tools     Detect build tools
  --detect-test-tools      Detect testing frameworks
  --output-format TEXT     Output format [default: json]

OUTPUT:
{
  "dependencies": {
    "runtime": {"fastapi": "^0.104.0", "pydantic": "^2.0.0"},
    "dev": {"pytest": "^7.4.0", "black": "^23.0.0"}
  },
  "frameworks": ["fastapi", "pydantic"],
  "build_tools": ["pip", "setuptools"],
  "test_frameworks": ["pytest"],
  "linters": ["black", "isort", "mypy"],
  "package_files": ["pyproject.toml", "requirements.txt"]
}
```

### Feedback Validation Commands

```bash
# bob run-feedback-checks
bob run-feedback-checks [OPTIONS]

OPTIONS:
  --repo-path TEXT         Repository path [default: .]
  --timeout INTEGER        Command timeout in seconds [default: 300]
  --parallel              Run checks in parallel
  --output-format TEXT     Output format [default: json]
  --save-results TEXT      Save results to file

OUTPUT:
{
  "timestamp": "2024-01-15T10:30:00Z",
  "results": [
    {
      "command": "npm run build",
      "exit_code": 0,
      "duration": 12.3,
      "stdout": "Build completed successfully",
      "stderr": "",
      "status": "passed"
    },
    {
      "command": "npm run lint",
      "exit_code": 1,
      "duration": 3.1,
      "stdout": "",
      "stderr": "Error: 5 linting errors found",
      "status": "failed"
    }
  ],
  "summary": {"passed": 3, "failed": 2, "total": 5}
}
```

### Configuration Commands

```bash
# bob generate-rules
bob generate-rules [OPTIONS]

OPTIONS:
  --analysis-file TEXT     JSON file with repository analysis
  --agent-type TEXT        Target agent: claude-code, cursor
  --output-path TEXT       Where to write rules file
  --template TEXT          Base template to use
  --focus TEXT            Focus areas: devops, quality, structure

OUTPUT:
# Writes CLAUDE.md or .cursor/rules/*.mdc files
```

```bash
# bob configure-mcp
bob configure-mcp [OPTIONS]

OPTIONS:
  --repo-path TEXT         Repository path [default: .]
  --agent-type TEXT        Target agent type
  --servers TEXT           Comma-separated MCP servers to install
  --recommend             Show recommended servers for this repo
  --env-template          Generate environment variable template

OUTPUT:
# Updates settings.json with MCP configuration
```

### Supervisor Commands

```bash
# bob configure-supervisor
bob configure-supervisor [OPTIONS]

OPTIONS:
  --repo-path TEXT         Repository path [default: .]
  --agent-type TEXT        Target agent type
  --rules-file TEXT        Custom supervisor rules JSON file
  --enable-defaults        Enable default language-agnostic rules
  --severity TEXT          Minimum severity to enforce [default: error]

OUTPUT:
# Updates settings.json with supervisor hooks
```

```bash
# bob supervisor-check
bob supervisor-check [OPTIONS]

OPTIONS:
  --file TEXT              File being modified
  --content TEXT           New file content
  --operation TEXT         Operation type: edit, write, create
  --rules-config TEXT      Supervisor rules configuration file

OUTPUT:
{
  "violations": [
    {
      "rule": "test-before-implementation",
      "severity": "error",
      "message": "Implementation added without corresponding tests",
      "suggestion": "Add tests for the new functionality before implementing"
    }
  ],
  "action": "block" | "warn" | "allow"
}
```

## 5. Python Class and Function Interfaces

### Core Models

```python
# bob_the_engineer/core/models.py

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
from enum import Enum

class TaskType(Enum):
    DETERMINISTIC = "deterministic"
    AGENTIC = "agentic"

class AgentType(Enum):
    CLAUDE_CODE = "claude-code"
    CURSOR = "cursor"

@dataclass
class WorkflowManifest:
    name: str
    version: str
    description: str
    inputs: Dict[str, Any]
    requirements: List[str]
    tasks: List['Task']

@dataclass
class Task:
    id: str
    name: str
    description: str
    type: TaskType
    dependencies: List[str]
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]

    # For agentic tasks
    agent_file: Optional[str] = None
    tools: Optional[List[str]] = None

    # For deterministic tasks
    python_module: Optional[str] = None
    function_name: Optional[str] = None

@dataclass
class RepoAnalysis:
    languages: Dict[str, float]
    frameworks: List[str]
    build_tools: List[str]
    test_frameworks: List[str]
    linters: List[str]
    formatters: List[str]
    package_managers: List[str]
    ci_platforms: List[str]
    directory_structure: Dict[str, Any]
    file_counts: Dict[str, int]

@dataclass
class CommandDiscovery:
    build_commands: List[str]
    test_commands: List[str]
    lint_commands: List[str]
    format_commands: List[str]
    install_commands: List[str]
    run_commands: List[str]

@dataclass
class FeedbackResult:
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration: float
    timestamp: datetime
    working_directory: str

@dataclass
class FailureAnalysis:
    failure_type: str  # build, lint, test, format
    severity: str  # must_have, nice_to_have
    description: str
    suggested_fix: str
    auto_fixable: bool
    files_affected: List[str]

@dataclass
class MCPServer:
    name: str
    package: str
    description: str
    command: str
    args: List[str]
    required_env: List[str]
    recommended_for: List[str]

@dataclass
class SupervisorRule:
    name: str
    description: str
    trigger_patterns: List[str]
    violation_patterns: List[str]
    languages: List[str]
    frameworks: List[str]
    severity: str
    example_violation: str
    example_fix: str
```

### Repository Analysis Functions

```python
# bob_the_engineer/workflows/start_using_coding_agent/tasks/repo_scanner.py

from pathlib import Path
from typing import Dict, List, Optional
import json
import yaml
from bob_the_engineer.core.models import RepoAnalysis, CommandDiscovery

def repo_scanner(
    path: Path,
    ignore_patterns: Optional[List[str]] = None,
    include_metrics: bool = False,
    max_depth: int = 10
) -> RepoAnalysis:
    """
    Scan repository structure with gitignore support.

    Args:
        path: Repository path to scan
        ignore_patterns: Additional patterns to ignore
        include_metrics: Whether to include size/complexity metrics
        max_depth: Maximum directory depth to scan

    Returns:
        RepoAnalysis with detected languages, frameworks, structure
    """

def analyze_dependencies(
    path: Path,
    detect_frameworks: bool = True,
    detect_build_tools: bool = True,
    detect_test_tools: bool = True
) -> Dict[str, Any]:
    """
    Analyze package files to detect dependencies and frameworks.

    Args:
        path: Repository path
        detect_frameworks: Whether to detect web/app frameworks
        detect_build_tools: Whether to detect build systems
        detect_test_tools: Whether to detect testing frameworks

    Returns:
        Dictionary with dependencies, frameworks, and tools
    """

def discover_commands(
    repo_path: Path,
    command_types: Optional[List[str]] = None
) -> CommandDiscovery:
    """
    Discover build, test, lint commands from package.json, Makefile, etc.

    Args:
        repo_path: Repository root path
        command_types: Types to discover (build, test, lint, format)

    Returns:
        CommandDiscovery with found commands by type
    """

def calculate_repo_metrics(path: Path) -> Dict[str, Any]:
    """Calculate repository size and complexity metrics"""

def build_directory_tree(path: Path, max_depth: int = 10) -> Dict[str, Any]:
    """Build nested dictionary representing directory structure"""
```

### Feedback Validation Functions

```python
# bob_the_engineer/workflows/start_using_coding_agent/tasks/feedback_validator.py

from typing import List, Dict, Any
from pathlib import Path
from bob_the_engineer.core.models import FeedbackResult, FailureAnalysis

def run_feedback_checks(
    repo_path: Path,
    timeout: int = 300,
    parallel: bool = False,
    save_results: Optional[Path] = None
) -> List[FeedbackResult]:
    """
    Execute all discovered feedback commands.

    Args:
        repo_path: Repository path
        timeout: Command timeout in seconds
        parallel: Whether to run checks in parallel
        save_results: Path to save results JSON

    Returns:
        List of FeedbackResult for each command executed
    """

def analyze_failures(
    results: List[FeedbackResult],
    repo_analysis: RepoAnalysis
) -> List[FailureAnalysis]:
    """
    Categorize failures by type and severity.

    Args:
        results: Feedback check results
        repo_analysis: Repository analysis for context

    Returns:
        List of FailureAnalysis with categorized issues
    """

def debug_failures(
    failures: List[FailureAnalysis],
    repo_path: Path,
    max_attempts: int = 3
) -> List[Dict[str, Any]]:
    """
    Attempt to automatically fix critical failures.

    Args:
        failures: List of failures to debug
        repo_path: Repository path
        max_attempts: Maximum fix attempts per failure

    Returns:
        List of fix results with success/failure status
    """

def generate_validation_report(
    results: List[FeedbackResult],
    fixes: List[Dict[str, Any]],
    output_path: Path
) -> None:
    """Generate comprehensive validation report"""
```

### Configuration Functions

```python
# bob_the_engineer/workflows/start_using_coding_agent/tasks/config_writer.py

from pathlib import Path
from typing import Dict, Any, List
from bob_the_engineer.core.models import AgentType, SupervisorConfig

def configure_defaults(
    agent_type: AgentType,
    repo_path: Path,
    enable_plan_mode: bool = True,
    custom_settings: Optional[Dict[str, Any]] = None
) -> None:
    """
    Configure best-practice defaults for coding agent.

    Args:
        agent_type: Type of coding agent
        repo_path: Repository path
        enable_plan_mode: Whether to enable plan mode by default
        custom_settings: Additional settings to merge
    """

def configure_mcp_tools(
    repo_path: Path,
    agent_type: AgentType,
    servers: List[str],
    env_template: bool = False
) -> None:
    """
    Configure MCP servers in coding agent settings.

    Args:
        repo_path: Repository path
        agent_type: Target coding agent
        servers: List of MCP server names to install
        env_template: Whether to generate .env template
    """

def configure_supervisor(
    repo_path: Path,
    agent_type: AgentType,
    rules_file: Optional[Path] = None,
    enable_defaults: bool = True,
    min_severity: str = "error"
) -> None:
    """
    Configure language-agnostic coding agent supervisor.

    Args:
        repo_path: Repository path
        agent_type: Target coding agent
        rules_file: Custom supervisor rules JSON file
        enable_defaults: Whether to enable default rules
        min_severity: Minimum severity to enforce
    """
```

### Tool Functions for Agentic Tasks

```python
# bob_the_engineer/workflows/start_using_coding_agent/tools/ast_parser.py

from pathlib import Path
from typing import Dict, Any, List
import ast

def parse_python_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse Python file and extract AST information.

    Returns:
        Dictionary with functions, classes, imports, complexity metrics
    """

def find_test_patterns(file_path: Path, language: str) -> List[Dict[str, Any]]:
    """Find test patterns in source files"""

def extract_import_dependencies(file_path: Path, language: str) -> List[str]:
    """Extract import/dependency statements"""
```

```python
# bob_the_engineer/workflows/use_coding_agent_effectively/tools/failure_mode_detector.py

from typing import List, Dict, Any
from pathlib import Path

def detect_common_failure_modes(
    file_content: str,
    file_path: Path,
    operation: str
) -> List[Dict[str, Any]]:
    """
    Detect common coding agent failure modes.

    Args:
        file_content: Content being written/edited
        file_path: Path of file being modified
        operation: Type of operation (edit, write, create)

    Returns:
        List of detected issues with descriptions and suggestions
    """

def check_test_mocking_antipatterns(
    test_content: str,
    source_path: Path
) -> List[Dict[str, Any]]:
    """Check for over-mocking in tests"""

def validate_error_handling_patterns(
    code_content: str,
    language: str
) -> List[Dict[str, Any]]:
    """Validate proper error handling patterns"""
```

## 6. Agent and Command Templates

### Claude Code Templates

#### Commands

**start-using-coding-agent.md**:
```markdown
# Start Using Coding Agent

Configure coding agent for effective use on existing large codebase.

## Usage
```
/start-using-coding-agent
```

## What this command does

1. **Analyzes repository** structure and technology stack
2. **Configures rules** specific to detected languages and frameworks
3. **Validates feedback** mechanisms (build, lint, test)
4. **Sets defaults** for optimal coding agent behavior

## Process

### Step 1: Repository Analysis
!bob repo-scan --path . --output-format json --include-metrics
!bob analyze-deps --path . --detect-frameworks --detect-build-tools --detect-test-tools

### Step 2: Configure Rules
@configure-rules

### Step 3: Validate Feedback
!bob run-feedback-checks --repo-path . --parallel --save-results feedback-results.json
@validate-feedback

### Step 4: Configure Defaults
!bob configure-defaults --agent-type claude-code --repo-path . --enable-plan-mode

## Expected Outputs
- `CLAUDE.md` file with repository-specific rules
- `feedback-validation-report.md` with mechanism status
- Updated `.claude/settings.json` with best practices

## Success Criteria
- All critical feedback mechanisms pass
- Rules cover detected technologies
- Agent configured for optimal development workflow
```

#### Agents

**configure-rules.md** (Full Agent Implementation):
```markdown
---
name: configure-rules
description: Analyze repository structure and generate comprehensive coding agent rules focused on DevOps practices, avoiding application-specific logic that may become outdated
tools: [repo-scan, analyze-deps, discover-commands, generate-rules, ast-parser, config-reader]
model: claude-3-5-sonnet-20241022
max_tokens: 8192
temperature: 0.1
---

You are a DevOps Configuration Expert with deep expertise in analyzing codebases and generating optimal coding agent rules. Your specialization focuses on creating robust, maintainable configuration that enables effective AI-assisted development without getting entangled in application-specific details.

## Core Expertise Areas

- **Technology Stack Analysis**: Detecting languages, frameworks, build systems, and development tools
- **DevOps Best Practices**: Understanding CI/CD, testing, linting, and deployment patterns
- **Coding Agent Optimization**: Configuring rules that maximize agent effectiveness
- **Rule Sustainability**: Creating rules that remain relevant as code evolves

## Objective
Analyze the target repository and generate comprehensive coding agent rules that focus on DevOps practices, development workflows, and mechanical tasks while avoiding application-specific logic that may become outdated.

## Available Tools

### Repository Analysis Tools
- `bob repo-scan --path <path> --output-format json --include-metrics`: Scan repository structure with gitignore support
- `bob analyze-deps --path <path> --detect-frameworks --detect-build-tools`: Analyze dependencies and frameworks
- `bob discover-commands --repo-path <path> --command-types build,test,lint,format`: Find existing development commands

### Code Analysis Tools
- `bob ast-parser --file <path> --language <lang>`: Parse source files for patterns
- `bob config-reader --file <path> --format <format>`: Read configuration files

### Rule Generation Tools
- `bob generate-rules --analysis-file <file> --agent-type <agent> --output-path <path>`: Generate rules from analysis

## Analysis Process

### 1. Repository Structure Analysis
Start with comprehensive repository scanning:
```bash
bob repo-scan --path . --output-format json --include-metrics
```

Focus on:
- Primary programming languages and their percentages
- Directory structure and organization patterns
- File type distribution
- Repository size and complexity metrics

### 2. Technology Stack Detection
Analyze the development stack:
```bash
bob analyze-deps --path . --detect-frameworks --detect-build-tools --detect-test-tools
```

Identify:
- Runtime and development dependencies
- Web/application frameworks in use
- Build systems (npm, pip, gradle, etc.)
- Testing frameworks and tools
- Linting and formatting tools
- Package managers

### 3. Development Command Discovery
Find existing development workflows:
```bash
bob discover-commands --repo-path . --command-types build,test,lint,format,install,run
```

Look for:
- Build and compilation commands
- Test execution commands
- Code quality tools (linters, formatters)
- Installation and setup procedures
- Application run commands

### 4. Configuration File Analysis
Examine configuration files for additional context:
```bash
bob config-reader --file pyproject.toml --format toml
bob config-reader --file package.json --format json
bob config-reader --file Makefile --format makefile
```

## Rule Generation Strategy

### Focus Areas (DO Generate Rules For)
1. **Development Workflow Rules**
   - Installation procedures and dependencies
   - Build processes and compilation steps
   - Test execution and coverage requirements
   - Code quality enforcement (linting, formatting)
   - Environment setup and configuration

2. **Project Structure Rules**
   - Directory organization conventions
   - File naming patterns
   - Module/package structure
   - Configuration file locations

3. **DevOps Practices**
   - CI/CD pipeline interaction
   - Deployment procedures
   - Environment management
   - Monitoring and logging patterns

4. **Code Quality Standards**
   - Language-specific best practices
   - Framework-specific conventions
   - Testing patterns and requirements
   - Documentation standards

### Avoid (DON'T Generate Rules For)
1. **Application Logic**: Business rules, domain models, API endpoints
2. **Implementation Details**: Specific algorithms, data structures
3. **Feature Specifications**: User stories, requirements, workflows
4. **Database Schemas**: Tables, relationships, migrations (these change frequently)

## Rule Templates by Technology

### Python Projects
```markdown
## Development Environment

### Installation
- Use `pip install -e .` for editable development installs
- Activate virtual environment before development: `source venv/bin/activate`
- Install dev dependencies: `pip install -e .[dev]`

### Code Quality
- Format code with: `black .`
- Sort imports with: `isort .`
- Type check with: `mypy src/`
- Lint with: `flake8 .`

### Testing
- Run tests with: `pytest`
- Check coverage with: `pytest --cov=src/`
- Run specific tests: `pytest tests/test_module.py::test_function`
```

### JavaScript/TypeScript Projects
```markdown
## Development Environment

### Installation
- Install dependencies: `npm install` or `yarn install`
- Use correct Node.js version: Check `.nvmrc` or `package.json engines`

### Code Quality
- Format code with: `npm run format` or `prettier --write .`
- Lint with: `npm run lint` or `eslint .`
- Type check with: `npm run type-check` or `tsc --noEmit`

### Testing
- Run tests: `npm test` or `yarn test`
- Watch mode: `npm run test:watch`
- Coverage: `npm run test:coverage`
```

## Final Rule Generation

After completing the analysis, generate comprehensive rules:

```bash
bob generate-rules --analysis-file analysis-results.json --agent-type claude-code --output-path CLAUDE.md --focus devops,quality,structure
```

## Quality Checks
Before finalizing rules:
1. Verify all detected technologies are covered
2. Ensure commands are accurate and tested
3. Check that rules focus on DevOps, not application logic
4. Validate that generated rules are sustainable over time

## Success Criteria
- Rules comprehensively cover detected tech stack
- All commands are verified to work
- Focus remains on mechanical DevOps tasks
- Rules will remain relevant as application code evolves
```

**validate-feedback.md** (Full Agent Implementation):
```markdown
---
name: validate-feedback
description: Execute all development feedback mechanisms, categorize failures by criticality, debug must-have issues, and generate comprehensive status report
tools: [run-feedback-checks, analyze-failures, debug-failures, generate-report]
model: claude-3-5-sonnet-20241022
max_tokens: 8192
temperature: 0.1
---

You are a DevOps Validation Expert specializing in testing, debugging, and optimizing development feedback mechanisms. Your expertise ensures that coding agents can work effectively by having reliable, fast feedback loops.

## Core Expertise Areas

- **Feedback Mechanism Testing**: Build systems, linters, formatters, test runners
- **Failure Analysis**: Categorizing issues by impact and urgency
- **Automated Debugging**: Systematic approaches to fixing common development issues
- **Quality Reporting**: Clear, actionable reports for development teams

## Objective
Execute all discovered development feedback mechanisms, analyze and categorize any failures, debug critical issues, and generate a comprehensive report showing the current state of development quality tools.

## Available Tools

### Execution Tools
- `bob run-feedback-checks --repo-path <path> --timeout 300 --parallel`: Execute all discovered commands
- `bob exec-with-analysis "<command>" --working-dir <dir> --timeout <sec>`: Execute individual commands with detailed analysis

### Analysis Tools
- `bob analyze-failures --results-file <file> --categorize-severity`: Categorize failures by type and impact
- `bob classify-issue --error-output "<text>" --command "<cmd>" --language <lang>`: Classify individual issues

### Debugging Tools
- `bob debug-failures --failure-file <file> --max-attempts 3`: Attempt automated fixes
- `bob suggest-fix --error-type <type> --context <context>`: Get fix suggestions

### Reporting Tools
- `bob generate-report --results <file> --fixes <file> --output <path>`: Create comprehensive report

## Validation Process

### 1. Execute All Feedback Mechanisms
Run comprehensive checks on all discovered development tools:

```bash
bob run-feedback-checks --repo-path . --timeout 300 --parallel --save-results feedback-results.json
```

This will execute:
- **Build Commands**: Compilation, bundling, packaging
- **Test Commands**: Unit tests, integration tests, coverage
- **Lint Commands**: Code style, error detection, complexity
- **Format Commands**: Code formatting validation

### 2. Analyze and Categorize Failures
Process results to understand failure patterns:

```bash
bob analyze-failures --results-file feedback-results.json --categorize-severity --output-file failure-analysis.json
```

**Failure Categories**:

**Must-Have (Critical)**:
- Build failures preventing development
- Missing required dependencies
- Broken test runners
- Critical configuration errors

**Nice-to-Have (Non-Critical)**:
- Code style violations
- Documentation linting issues
- Optional optimization warnings
- Deprecated API usage warnings

### 3. Automated Debugging Process
Attempt to fix critical failures systematically:

```bash
bob debug-failures --failure-file failure-analysis.json --max-attempts 3 --save-fixes fixes-applied.json
```

**Common Fix Patterns**:
- **Missing Dependencies**: Auto-install from package files
- **Configuration Issues**: Apply standard configurations
- **Path Problems**: Fix relative/absolute path issues
- **Version Conflicts**: Suggest compatible version ranges

### 4. Generate Comprehensive Report
Create detailed validation report:

```bash
bob generate-report --results feedback-results.json --fixes fixes-applied.json --output validation-report.md
```

## Debugging Strategies

### Build Failures
1. Check dependency installation
2. Verify environment variables
3. Validate configuration files
4. Check for missing build tools

### Test Failures
1. Verify test framework installation
2. Check test database/environment setup
3. Validate test configuration
4. Ensure test dependencies are available

### Lint/Format Failures
1. Install missing linting tools
2. Apply standard configurations
3. Fix basic syntax issues
4. Update deprecated usage patterns

## Report Structure
The validation report should include:

### Executive Summary
- Total checks executed
- Pass/fail breakdown
- Critical issues requiring manual attention
- Estimated effort for remaining fixes

### Detailed Results
- Command-by-command execution results
- Failure analysis with categorization
- Applied fixes with explanations
- Remaining issues with recommended actions

### Recommendations
- Priority order for manual fixes
- Suggestions for improving feedback speed
- Additional tools that could be helpful
- Configuration improvements

## Success Criteria
- All must-have feedback mechanisms pass or have clear fix plans
- Detailed report provides actionable guidance
- Coding agent can rely on feedback mechanisms for development
- Manual intervention requirements are minimized and well-documented
```

## 7. Supervisor System Design

### Language-Agnostic Supervisor Rules

```json
{
  "supervisor_rules": [
    {
      "name": "test-before-implementation",
      "description": "Ensure tests exist before implementing functionality",
      "trigger_patterns": [
        "\\.(py|js|ts|java|go|rb|php|cs|cpp|rs)$"
      ],
      "violation_patterns": [
        "def\\s+\\w+\\([^)]*\\):\\s*(?!.*test)",
        "function\\s+\\w+\\([^)]*\\)\\s*{(?!.*test)",
        "public\\s+\\w+\\s+\\w+\\([^)]*\\)\\s*{(?!.*test)"
      ],
      "languages": [],
      "frameworks": [],
      "severity": "error",
      "example_violation": "Adding new function without corresponding test",
      "example_fix": "Create test file and test cases before implementing function"
    },
    {
      "name": "avoid-test-mocking-implementation",
      "description": "Prevent mocking the function being tested",
      "trigger_patterns": [
        "test_.*\\.(py|js|ts|java|go|rb|php|cs|cpp|rs)$",
        ".*\\.test\\.(py|js|ts|java|go|rb|php|cs|cpp|rs)$",
        ".*\\.spec\\.(py|js|ts|java|go|rb|php|cs|cpp|rs)$"
      ],
      "violation_patterns": [
        "@patch\\(['\"][^'\"]*\\1['\"]\\).*def\\s+test_\\1",
        "jest\\.mock\\(['\"][^'\"]*\\1['\"]\\).*test.*\\1",
        "mock\\([^)]*\\).*test.*same_function"
      ],
      "languages": [],
      "frameworks": [],
      "severity": "error",
      "example_violation": "Mocking 'calculate_total' in test_calculate_total",
      "example_fix": "Test the actual function, mock only external dependencies"
    },
    {
      "name": "informative-error-messages",
      "description": "Ensure error messages include context and actionable information",
      "trigger_patterns": [
        "\\.(py|js|ts|java|go|rb|php|cs|cpp|rs)$"
      ],
      "violation_patterns": [
        "raise\\s+\\w+\\(\\s*['\"][^'\"]*['\"]\\s*\\)",
        "throw\\s+new\\s+\\w+\\(\\s*['\"][^'\"]*['\"]\\s*\\)",
        "return\\s+error\\(['\"][^'\"]*['\"]\\)"
      ],
      "languages": [],
      "frameworks": [],
      "severity": "warning",
      "example_violation": "raise ValueError('Invalid input')",
      "example_fix": "raise ValueError(f'Invalid input: {input_value}. Expected: {expected_format}')"
    }
  ]
}
```

## 8. Recommended MCP Servers

Based on research, here are the most valuable MCP servers for development workflows:

### Essential MCP Servers
1. **GitHub Integration**: `@modelcontextprotocol/server-github`
   - Repository management, issues, pull requests
   - Required env: `GITHUB_PERSONAL_ACCESS_TOKEN`

2. **Filesystem Access**: `@modelcontextprotocol/server-filesystem`
   - Secure file operations with directory permissions
   - Configure allowed directories for safety

3. **Web Search**: `@modelcontextprotocol/server-web-search`
   - Real-time information lookup for documentation
   - Required env: Search API credentials

### Development-Specific MCP Servers
4. **Database Access**:
   - `@modelcontextprotocol/server-postgresql`
   - `@modelcontextprotocol/server-mysql`
   - Required env: Database connection strings

5. **Browser Automation**: `@modelcontextprotocol/server-playwright`
   - End-to-end testing and web scraping
   - Requires Playwright installation

6. **Documentation**: `deepgraph-mcp`
   - Enhanced code documentation and analysis
   - Framework-specific variants available

### Configuration Templates
```json
{
  "mcpServers": {
    "github": {
      "description": "GitHub API integration for repository management",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
      }
    },
    "filesystem": {
      "description": "Secure filesystem access with directory permissions",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    },
    "web-search": {
      "description": "Web search capabilities for documentation lookup",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-web-search"],
      "env": {
        "SEARCH_API_KEY": "<YOUR_KEY>"
      }
    }
  }
}
```

## 9. Implementation Milestones

### Milestone 1: Core CLI and Repository Analysis
- Implement `bob repo-scan`, `bob analyze-deps`, `bob discover-commands`
- Create core data models and utilities
- Build repository analysis pipeline

### Milestone 2: Rule Generation System
- Implement rule generation for Claude Code and Cursor
- Create technology-specific rule templates
- Build deterministic rule generation functions

### Milestone 3: Feedback Validation System
- Implement feedback mechanism execution
- Build failure analysis and categorization
- Create automated debugging capabilities

### Milestone 4: MCP and Workflow Configuration
- Implement MCP server configuration
- Create workflow template installation
- Build coding agent adapter system

### Milestone 5: Supervisor System
- Implement language-agnostic supervisor
- Create rule-based validation system
- Build hook integration for both agents

### Milestone 6: Advanced Improvement Workflows
- Implement feedback improvement analysis
- Create conflict detection and resolution
- Build debuggability enhancement system

## 10. Testing Strategy

### Unit Tests
- Test each CLI command with various repository types
- Mock external dependencies (file system, network)
- Validate JSON schema generation and validation

### Integration Tests
- Test full workflows on sample repositories
- Validate generated configurations work with actual coding agents
- Test MCP server integration and communication

### End-to-End Tests
- Test complete onboarding flow on real repositories
- Validate coding agent behavior with generated configurations
- Performance testing for large repositories

Each milestone will be implemented with its corresponding tests to ensure reliability and correctness.
