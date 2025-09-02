# Subagent Templating Transformation Plan

## Overview
This document outlines the complete process for converting a single subagent prompt file into a flexible template system that can generate agent-specific versions for different coding agents (Claude Code, Cursor, etc.).

## Prerequisites
- Existing subagent prompt file (e.g., `configure_rules.md`)
- Understanding of agent-specific differences
- Knowledge of tools available to each agent type

## Phase 1: Prepare the Source Prompt

### Step 1.1: Remove CLI Dependencies
**Goal**: Make the subagent completely agentic using only reasoning

**Actions**:
1. Identify all CLI command references in the prompt file
2. Replace CLI commands with reasoning-based approaches:
   - `bob repo-scan --path <path>` → "Use directory listing and file reading to understand repository organization"
   - `bob analyze-deps --path <path>` → "Read and parse dependency files (package.json, pyproject.toml, etc.)"
   - `bob discover-commands --repo-path <path>` → "Examine package.json scripts, Makefile targets, and other automation"
3. Update tool references from CLI tools to analysis capabilities:
   - Replace command-based analysis with file reading and semantic search
   - Replace validation commands with reasoning-based quality assurance

### Step 1.2: Clean Up Markdown Structure
**Goal**: Remove redundant formatting within markdown files

**Actions**:
1. Search for `````markdown` blocks within the .md file
2. Remove the markdown code block markers while preserving content
3. Ensure consistent heading structure

### Step 1.3: Identify Agent-Specific Content
**Goal**: Find content that varies between agents

**Actions**:
1. Identify sections that mention specific agent features
2. Note differences in output formats (single file vs multiple files)
3. Document tool differences between agents
4. Identify integration-specific content

## Phase 2: Create Template System Infrastructure - already done

### Step 2.1: Update Dependencies
**File**: `pyproject.toml`

**Actions**:
```python
dependencies = [
    # ... existing dependencies ...
    "jinja2>=3.1.0",      # Template engine for rule generation
    "pyyaml>=6.0",        # YAML configuration parsing
]
```

### Step 2.2: Create Directory Structure
**Goal**: Set up the template system architecture

**Actions**:
1. Create directories:
   ```bash
   mkdir -p bob_the_engineer/adapters/config
   mkdir -p bob_the_engineer/adapters/claude
   mkdir -p bob_the_engineer/adapters/cursor
   mkdir -p bob_the_engineer/templates/subagents
   ```

### Step 2.3: Create Base Adapter Interface
**File**: `bob_the_engineer/adapters/base.py`

**Content**:
```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

class BaseAdapter(ABC):
    def __init__(self, target_path: Path, config: Optional[Dict[str, Any]] = None):
        self.target_path = target_path
        self.config = config or {}

    @property
    @abstractmethod
    def agent_name(self) -> str:
        pass

    @property
    @abstractmethod
    def output_format(self) -> str:
        pass

    @abstractmethod
    def get_template_variables(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def write_rules(self, rendered_content: str) -> None:
        pass

    @abstractmethod
    def get_output_paths(self) -> list[Path]:
        pass
```

### Step 2.4: Create Adapter Factory
**File**: `bob_the_engineer/adapters/factory.py`

**Content**:
```python
from .claude.rules_manager import ClaudeRulesManager
from .cursor.rules_manager import CursorRulesManager

class AdapterFactory:
    _adapters = {
        "claude-code": ClaudeRulesManager,
        "cursor": CursorRulesManager,
    }

    @classmethod
    def create_adapter(cls, agent_type: str, target_path: Path, config = None):
        if agent_type not in cls._adapters:
            raise ValueError(f"Unsupported agent type: {agent_type}")
        return cls._adapters[agent_type](target_path, config)
```

## Phase 3: Create Agent-Specific Adapters

### Step 3.1: Research Agent-Specific Tools
**Goal**: Identify correct tool names for each agent

**Claude Code Tools**: `[Read, Write, Edit, Bash, Task]`
**Cursor Tools**: `[read_file, list_dir, grep, codebase_search, glob_file_search]`

**Research Methods**:
1. Check design documents and specifications
2. Look at existing subagent configurations
3. Search claude code or cusrsor docs for tool references

### Step 3.2: Create Claude Code Adapter
**File**: `bob_the_engineer/adapters/claude/rules_manager.py`

**Key Features**:
- Single file output (`CLAUDE.md`)
- Integration with Claude Code hooks and commands
- Bash tool integration

### Step 3.3: Create Cursor Adapter
**File**: `bob_the_engineer/adapters/cursor/rules_manager.py`

**Key Features**:
- Multiple file output (`.cursor/rules/*.mdc`)
- Category-focused rule files
- Cursor-specific features

### Step 3.4: Create Configuration Files
**Files**:
- `bob_the_engineer/adapters/config/claude-code.yaml`
- `bob_the_engineer/adapters/config/cursor.yaml`

**Content Structure**:
```yaml
agent_name: "agent-name"
output_format: "single_file" | "multiple_files"

file_organization:
  type: "single_file" | "multiple_files"
  location: "repository_root" | ".cursor/rules/"
  filename: "CLAUDE.md" # for single file
  files: [...] # for multiple files

features:
  # Agent-specific capabilities

tool_references:
  # Agent-specific tool preferences

configuration_approach:
  # Agent-specific configuration style
```

## Phase 4: Create Template Engine

### Step 4.1: Create Template Engine Class
**File**: `bob_the_engineer/adapters/template_engine.py`

**Key Features**:
- Jinja2 environment setup
- Agent configuration loading
- Two-pass rendering for frontmatter templating
- YAML validation

**Critical Implementation Detail - Two-Pass Rendering**:
```python
# Pass 1: Render Jinja2 template (including frontmatter)
template = self.env.get_template("subagents/configure_rules.jinja2.md")
rendered_content = template.render(**template_context)

# Pass 2: Validate YAML frontmatter (optional)
yaml.safe_load(frontmatter_content)
```

### Step 4.2: Handle Frontmatter Templating
**Challenge**: YAML parsers process frontmatter before Jinja2

**Solution**: Use Jinja2 conditionals in frontmatter with two-pass rendering:
```yaml
---
name: subagent-name
{% if agent_type == "claude-code" -%}
tools: [Read, Write, Edit, Bash, Task]
{% elif agent_type == "cursor" -%}
tools: [read_file, list_dir, grep, codebase_search, glob_file_search]
{% endif %}
model: claude-3-5-sonnet-20241022
---
```

## Phase 5: Convert Prompt to Template

### Step 5.1: Create Jinja2 Template
**File**: `bob_the_engineer/templates/subagents/{subagent_name}.jinja2.md`

**Actions**:
1. Copy the cleaned prompt content
2. Add agent-specific conditionals for:
   - Tools in frontmatter
   - Objective statements
   - Rule generation approaches
   - Integration sections

### Step 5.2: Add Agent-Specific Conditionals
**Pattern**:
```jinja2
{% if agent_type == "claude-code" -%}
Claude-specific content here
{% elif agent_type == "cursor" -%}
Cursor-specific content here
{% endif %}
```

**Apply to**:
- Objective statements
- Rule generation processes
- Integration guidelines
- Output format descriptions

## Phase 6: CLI Integration

### Step 6.1: Add CLI Command
**File**: `bob_the_engineer/cli/app.py`

**Add Command**:
```python
@app.command()
def generate_rules(
    agent_type: str = typer.Option("claude-code", help="Type of coding agent (claude-code, cursor)"),
    target_path: str = typer.Option(".", help="Path to target repository"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without writing"),
) -> None:
    """Generate coding agent rules for a repository."""
    # Implementation with TemplateEngine
```

### Step 6.2: Handle Display Issues
**Challenge**: Rich Console truncates long lines

**Solution**: Use dedicated console with optimal settings:
```python
preview_console = Console(width=120, height=50, markup=False)
preview_console.print(content)
```

## Phase 7: Testing and Validation

### Step 7.1: Create Tests
**File**: `tests/test_adapters.py`

**Test Coverage**:
- Adapter factory functionality
- Agent-specific adapter behavior
- Template variable generation
- File writing operations

### Step 7.2: Validate Tool Names
**Actions**:
1. Research official documentation for each agent
2. Verify tool names in existing project configurations
3. Test generated templates with actual agents

### Step 7.3: End-to-End Testing
**Commands**:
```bash
# Test preview mode
bob-the-engineer generate-rules --dry-run --agent-type claude-code
bob-the-engineer generate-rules --dry-run --agent-type cursor

# Test actual generation
bob-the-engineer generate-rules --agent-type claude-code
bob-the-engineer generate-rules --agent-type cursor

# Run tests
pytest tests/test_adapters.py -v
```

## Phase 8: Documentation and Cleanup

### Step 8.1: Update __init__.py Files
**Create proper module imports for**:
- `adapters/__init__.py`
- `adapters/claude/__init__.py`
- `adapters/cursor/__init__.py`
- `templates/__init__.py`

### Step 8.2: IDE Configuration
**File**: `.vscode/settings.json`

**Add**:
```json
"files.associations": {
  "*.md.jinja2": "markdown",
  "*.jinja2.md": "markdown"
}
```

### Step 8.3: Clean Up
**Actions**:
1. Remove temporary debug files
2. Update any references to the old prompt file

## Replication Checklist for Other Subagents

### For Each New Subagent:

1. **☐ Analyze Source Prompt**
   - Identify CLI dependencies
   - Find agent-specific content
   - Note tool requirements

2. **☐ Clean Source Prompt**
   - Remove CLI commands → reasoning approaches
   - Remove markdown code blocks
   - Identify conditional content

3. **☐ Update Agent Configs**
   - Add subagent-specific settings to `claude-code.yaml`
   - Add subagent-specific settings to `cursor.yaml`

4. **☐ Create Template**
   - Copy cleaned prompt to `templates/subagents/{name}.jinja2.md`
   - Add agent-specific conditionals
   - Test tool specifications

5. **☐ Update Template Engine**
   - Add new template rendering method if needed
   - Update CLI to support new subagent

6. **☐ Test and Validate**
   - Test with both agent types
   - Verify tool lists are correct
   - Run adapter tests

## Common Patterns for Different Subagents

### Analysis-Focused Subagents
- **Tools**: File reading, semantic search, pattern matching
- **Output**: Analysis reports, recommendations
- **Variations**: Claude uses Bash tool, Cursor uses native tools

### Generation-Focused Subagents
- **Tools**: File writing, editing, creation
- **Output**: Generated files, configurations
- **Variations**: Claude writes via Write tool, Cursor via edit tools

### Validation-Focused Subagents
- **Tools**: Testing, checking, validation
- **Output**: Reports, pass/fail status
- **Variations**: Claude can execute commands, Cursor focuses on analysis

## Technical Gotchas

### Jinja2 in YAML Frontmatter
- **Issue**: YAML parsers conflict with Jinja2 syntax
- **Solution**: Two-pass rendering (Jinja2 first, then YAML validation)

### Rich Console Line Truncation
- **Issue**: Long tool lists get truncated in Rich Console
- **Solution**: Dedicated console with `Console(width=120, height=50, markup=False)`

### Tool Name Variations
- **Issue**: Different agents use different tool naming conventions
- **Solution**: Agent-specific conditionals in frontmatter

### Template vs Preview Files
- **Issue**: Need markdown preview for Jinja2 templates
- **Solution**: File associations in VS Code + `.jinja2.md` extension

## Success Criteria
- ✅ Template generates valid frontmatter for both agents
- ✅ Agent-specific tools are correctly specified
- ✅ CLI commands work for both dry-run and actual generation
- ✅ Generated prompts are completely agentic (no CLI dependencies)
- ✅ All tests pass
- ✅ Markdown preview works for template files

## Files Created in This Process

### Core Infrastructure:
- `bob_the_engineer/adapters/__init__.py`
- `bob_the_engineer/adapters/base.py`
- `bob_the_engineer/adapters/factory.py`
- `bob_the_engineer/adapters/template_engine.py`

### Agent Adapters:
- `bob_the_engineer/adapters/claude/__init__.py`
- `bob_the_engineer/adapters/claude/rules_manager.py`
- `bob_the_engineer/adapters/cursor/__init__.py`
- `bob_the_engineer/adapters/cursor/rules_manager.py`

### Configuration:
- `bob_the_engineer/adapters/config/claude-code.yaml`
- `bob_the_engineer/adapters/config/cursor.yaml`

### Templates:
- `bob_the_engineer/templates/__init__.py`
- `bob_the_engineer/templates/subagents/configure_rules.jinja2.md`

### Testing:
- `tests/test_adapters.py`

### Configuration:
- Updated `pyproject.toml` (added jinja2, pyyaml dependencies)
- Updated `bob_the_engineer/cli/app.py` (added generate-rules command)
- Updated `.vscode/settings.json` (added file associations)

## Command Reference

### Generate Rules:
```bash
# Preview Claude Code rules
bob-the-engineer generate-rules --dry-run --agent-type claude-code

# Preview Cursor rules
bob-the-engineer generate-rules --dry-run --agent-type cursor

# Generate actual files
bob-the-engineer generate-rules --agent-type claude-code
bob-the-engineer generate-rules --agent-type cursor

# Target different repository
bob-the-engineer generate-rules --target-path /path/to/repo --agent-type cursor
```

### Testing:
```bash
# Run adapter tests
pytest tests/test_adapters.py -v

# Install with new dependencies
pip install -e .[dev]
```
