# Bob the Engineer - Awesome DevOps Agents

A DevOps automation framework providing highly reliable subagents and workflows for Claude Code and Cursor, with a powerful companion CLI `bob-the-engineer`.

## Overview

Bob the Engineer transforms your AI coding assistant into a DevOps powerhouse by providing:
- **DevOps Workflows to make coding agent work on large existing codebases**
- **Production-ready Coding workflows for TDD, code review, and spec-driven development**
- **Specialized Subagents**: Expert agents for configuring environments, detecting issues, and improving code quality
- **Template Engine to support all coding agents**: Jinja2-based system for generating configurations for Claude Code and Cursor

## Key Features

### 🚀 Coding agent setup Workflows (`workflows/devops/`)

- **Start Using Coding Agent** (`start_using_coding_agent.jinja2.md`): Onboard AI agents to existing large codebases
- **Use Coding Agent Effectively** (`use_coding_agent_effectively.jinja2.md`): Configure advanced features like MCP and supervisor guards
- **Improve Code Repository** (`improve_code_repo.jinja2.md`): Detect and fix code quality issues systematically

#### Coding agent configuration subagents
- **`configure-rules`**: Generate agent-specific rule files (CLAUDE.md or .cursor/rules/)
- **`configure-defaults`**: Auto-detect repository characteristics and apply optimal coding agent settings like allowed and denied bash commands based on your organizational context
- **`configure-mcp`**: Set up necessary MCP servers and find servers relevant to your code
- **`configure-supervisor`**: Install guards using Claude Code hooks to agentically catch common mistakes coding agents make and give feedback to them in real-time, so that you are not repeating yourself again and again
- **`configure-coding-workflows`**: Install the coding workflows as first class commands

#### Subagents to make your code ready for coding agents
- **`build-test-run`**: Validate and resolve failures in feedback mechanisms (build, test, lint, run) to start using coding agents
- **`detect-conflicting-instructions`**: Find and resolve contradictory docs, configurations, code blocks that can confuse coding agents
- **`improve-code-quality-checks`**: Strengthen linting, formatting, code cov checks to provide quicker feedback to coding agents
- **`improve-debuggability`**: Improve logging, error handling, and debugging capabilities so that coding agents can debug issues and produce production-ready code



### 🤖 Coding Workflows (`workflows/coding/`)
- **TDD Workflow** (`tdd.jinja2.md`): Enforces test-first development with automatic test generation and validation
- **Code Review** (`code-review.jinja2.md`): Multi-aspect parallel review covering security, performance, and best practices
- **Spec-Driven Development** (`spec-driven.jinja2.md`): 6-phase iterative development from requirements to deployment


### 🔧 CLI

The `bob-the-engineer` CLI provides comprehensive commands for managing your DevOps environment:

```bash
# Core Commands
bob-the-engineer init              # Initialize agent environment with subagents and workflows
bob-the-engineer doctor            # Diagnose and repair installation issues
bob-the-engineer status            # Show project configuration status
```

The following commands are executed by the workflows/agents and don't need to invoked by you:
```bash
bob-the-engineer configure-defaults # Apply best-practice templates (solo/team/enterprise)
bob-the-engineer configure-workflows # Install development workflow templates
bob-the-engineer configure-mcp      # Configure Model Context Protocol servers
bob-the-engineer configure-supervisor # Set up supervisor guards (Claude Code only)
```

### 🏗 Architecture

```
bob_the_engineer/
├── adapters/           # Agent-specific implementations
│   ├── claude/        # Claude Code adapter
│   ├── cursor/        # Cursor adapter
│   └── factory.py     # Dynamic adapter creation
├── templates/         # Jinja2 templates
│   ├── subagents/    # Specialized agent prompts
│   └── workflows/    # DevOps workflow definitions
└── cli/              # Command-line interface
```

## Installation

### From Source
```bash
# Clone the repository
git clone https://github.com/yourusername/bob-the-engineer.git
cd bob-the-engineer

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .

# Verify installation
bob-the-engineer --help
```

### Quick Setup for Your Repository

```bash
# Initialize with all subagents and workflows
bob-the-engineer init --agent-type claude-code

# Or apply best-practice defaults based on team size
bob-the-engineer configure-defaults --agent-type claude-code --template-type development-team

# Available templates:
# - solo-developer: Fast iteration for individual developers
# - development-team: Balanced for 2-5 person teams with CI/CD
# - enterprise-security: High-security with audit trails
```

## Usage Examples

### Setting Up a New Project

```bash
# 1. Initialize the agent environment
bob-the-engineer init --agent-type cursor

# 2. Configure for your team size
bob-the-engineer configure-defaults --agent-type cursor --template-type development-team

# 3. Install specific workflows
bob-the-engineer configure-workflows --workflows tdd,code-review --agent-type cursor
```

### Configuring MCP Servers (Claude Code)

```bash
# Configure GitHub MCP server
bob-the-engineer configure-mcp --agent-type claude-code \
  --config '{"mcpServers": {"github": {"command": "npx", "args": ["@modelcontextprotocol/server-github"]}}}'
```

### Installing Supervisor Guards

```bash
# Install TDD and file protection guards
bob-the-engineer configure-supervisor --guards tdd-guard,file-guard
```

### Diagnosing Issues

```bash
# Check installation health
bob-the-engineer doctor

# Attempt automatic repairs
bob-the-engineer doctor --repair --agent-type claude-code
```

## Configuration Templates

The framework includes three pre-configured templates optimized for different team contexts:

### Solo Developer
- Fast code-first mode with minimal confirmations
- Auto-formatting and quick dependency installation
- Optimized for rapid prototyping

### Development Team
- Plan-first approach with code quality checks
- Git commit templates and test automation
- Balanced for team collaboration

### Enterprise Security
- Maximum security with audit logging
- Restricted permissions and compliance checks
- Approval workflows for sensitive operations

## Development

### Prerequisites
- Python 3.10+
- Poetry for dependency management
- Pre-commit for code quality

### Contributing

```bash
# Install development dependencies
poetry install

# Set up pre-commit hooks
pre-commit install

# Run tests
pytest

# Check code quality
ruff check .
mypy .
```

## Architecture Details

### Template Engine

The template engine uses Jinja2 to generate agent-specific configurations:

```python
from bob_the_engineer.adapters.template_engine import TemplateEngine

engine = TemplateEngine(templates_dir)
engine.generate_subagent_rules("configure-defaults", "claude-code", repo_path)
```

### Adapter Pattern

Each coding agent has a dedicated adapter implementing the base interface:

```python
from bob_the_engineer.adapters.factory import AdapterFactory

adapter = AdapterFactory.create_adapter("cursor", repo_path)
adapter.write_rules(content)
adapter.install_workflows(["tdd", "code-review"])
```

## Roadmap

- [ ] Support for additional AI coding assistants
- [ ] Advanced workflow orchestration
- [ ] Integration with CI/CD pipelines
- [ ] Custom workflow builder UI
- [ ] Performance metrics and analytics

## License

MIT License - see LICENSE file for details

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/bob-the-engineer/issues)
- **Documentation**: [Full Documentation](https://docs.bob-the-engineer.dev)
- **Community**: [Discord Server](https://discord.gg/bob-the-engineer)

## Acknowledgments

Built with ❤️ by the DevOps community for the DevOps community.

Special thanks to Anthropic (Claude) and Cursor teams for their excellent AI coding assistants.
