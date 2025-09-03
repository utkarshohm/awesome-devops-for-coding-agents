"""Claude Code rules manager adapter."""

import json
import shutil
from pathlib import Path
from typing import Any

from ..base import BaseAdapter


class ClaudeRulesManager(BaseAdapter):
    """Adapter for generating Claude Code rules configuration."""

    @property
    def agent_name(self) -> str:
        """Return the name of the coding agent this adapter supports."""
        return "claude-code"

    @property
    def output_format(self) -> str:
        """Return the expected output format."""
        return "single_file"

    def get_template_variables(self) -> dict[str, Any]:
        """Return Claude Code specific template variables."""
        # Merge default config with any provided config
        default_vars = {
            "agent_type": "claude-code",
            "output_file": "CLAUDE.md",
        }

        # If config was provided, merge it in
        if self.config:
            default_vars.update(self.config)

        return default_vars

    def get_output_paths(self) -> list[Path]:
        """Return list of output paths where rules will be written."""
        return [self.target_path / "CLAUDE.md"]

    def write_rules(self, rendered_content: str) -> None:
        """Write the rendered rules to CLAUDE.md file.

        Args:
            rendered_content: The rendered template content
        """
        output_path = self.target_path / "CLAUDE.md"
        output_path.write_text(rendered_content, encoding="utf-8")

    def install_workflows(self, workflows: list[str]) -> list[Path]:
        """Install workflow templates as Claude Code commands.

        Args:
            workflows: List of workflow names to install

        Returns:
            List of output file paths where workflows were installed
        """
        claude_commands_dir = self.target_path / ".claude" / "commands"
        claude_commands_dir.mkdir(parents=True, exist_ok=True)

        output_paths = []

        # Mapping of workflow names to template directories
        workflow_mapping = {
            "spec-driven": "spec_driven_development",
            "tdd": "test_driven_development",
            "code-review": "code_review",
            "research": "research",
            "triage": "triage",
        }

        for workflow in workflows:
            # Create workflow command file for Claude Code
            command_file = claude_commands_dir / f"{workflow}.md"

            # For now, create a basic workflow command template
            # TODO: Use actual templates when they're available
            workflow_content = self._generate_workflow_command(
                workflow, workflow_mapping.get(workflow, workflow)
            )

            command_file.write_text(workflow_content, encoding="utf-8")
            output_paths.append(command_file)

        return output_paths

    def install_subagents(self, subagents: list[str]) -> list[Path]:
        """Install subagent templates as Claude Code agents.

        Args:
            subagents: List of subagent names to install

        Returns:
            List of output file paths where subagents were installed
        """
        claude_agents_dir = self.target_path / ".claude" / "agents"
        claude_agents_dir.mkdir(parents=True, exist_ok=True)

        output_paths = []

        # Get the path to subagent templates
        templates_dir = Path(__file__).parent.parent.parent / "templates" / "subagents"

        for subagent in subagents:
            # Look for the template file
            template_file = templates_dir / f"{subagent}.jinja2.md"
            if template_file.exists():
                # Copy template to agents directory
                agent_file = claude_agents_dir / f"{subagent}.md"
                shutil.copy2(template_file, agent_file)
                output_paths.append(agent_file)
            else:
                # Generate a basic subagent template
                agent_file = claude_agents_dir / f"{subagent}.md"
                agent_content = self._generate_subagent_template(subagent)
                agent_file.write_text(agent_content, encoding="utf-8")
                output_paths.append(agent_file)

        return output_paths

    def configure_settings(self, settings: dict[str, Any]) -> Path:
        """Update Claude Code settings configuration.

        Args:
            settings: Dictionary of settings to update

        Returns:
            Path to the updated settings file
        """
        claude_dir = self.target_path / ".claude"
        claude_dir.mkdir(parents=True, exist_ok=True)

        settings_file = claude_dir / "settings.json"

        # Load existing settings or create new ones
        if settings_file.exists():
            with open(settings_file, encoding="utf-8") as f:
                existing_settings = json.load(f)
        else:
            existing_settings = {}

        # Merge new settings
        existing_settings.update(settings)

        # Write updated settings
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(existing_settings, f, indent=2)

        return settings_file

    def install_supervisor(self, guards: list[str]) -> Path:
        """Install supervisor guards and hooks for Claude Code.

        Args:
            guards: List of guard names to install

        Returns:
            Path to the updated configuration file
        """
        # Supervisor configuration for Claude Code
        hooks_config: dict[str, Any] = {"hooks": {"preToolUse": []}}

        for guard in guards:
            if guard == "file-guard":
                hooks_config["hooks"]["preToolUse"].append(
                    {
                        "name": "file-guard",
                        "script": "bob-the-engineer guard-file-access",
                        "condition": "${CLAUDE_MODE} != 'plan'",
                    }
                )
            elif guard == "tdd-guard":
                hooks_config["hooks"]["preToolUse"].append(
                    {
                        "name": "tdd-guard",
                        "script": "bob-the-engineer guard-tdd",
                        "condition": "${BOB_TDD_ENABLED} != 'false'",
                    }
                )
            elif guard == "self-review":
                hooks_config["hooks"]["postResponse"] = [
                    {
                        "name": "self-review",
                        "script": "bob-the-engineer guard-self-review",
                        "condition": "Math.random() < 0.1",  # 10% chance
                    }
                ]

        return self.configure_settings(hooks_config)

    def _generate_workflow_command(self, workflow_name: str, template_name: str) -> str:
        """Generate a basic workflow command template.

        Args:
            workflow_name: Name of the workflow
            template_name: Name of the template directory

        Returns:
            Generated command content
        """
        return f"""---
name: {workflow_name}
description: {workflow_name.replace("-", " ").title()} workflow for development
tools: [Read, Write, Edit, Bash, Task]
model: claude-3-5-sonnet-20241022
max_tokens: 8192
temperature: 0.3
---

# {workflow_name.replace("-", " ").title()} Workflow

## Overview
This is the {workflow_name} development workflow template.

## Usage
This workflow will guide you through the {workflow_name} development process.

## Steps
1. Analyze requirements
2. Plan implementation
3. Execute development
4. Validate results

*Note: This is a generated template. Customize as needed.*
"""

    def _generate_subagent_template(self, subagent_name: str) -> str:
        """Generate a basic subagent template.

        Args:
            subagent_name: Name of the subagent

        Returns:
            Generated subagent content
        """
        return f"""---
name: {subagent_name}
description: {subagent_name.replace("-", " ").title()} subagent
tools: [Read, Write, Edit, Bash]
model: claude-3-5-sonnet-20241022
max_tokens: 4096
temperature: 0.3
---

# {subagent_name.replace("-", " ").title()} Agent

## Purpose
This agent handles {subagent_name.replace("-", " ")} tasks.

## Capabilities
- Analyze and process requirements
- Execute specialized tasks
- Generate reports and recommendations

*Note: This is a generated template. Customize as needed.*
"""

    def validate_environment(self) -> bool:
        """Validate that the target environment is suitable for Claude Code.

        Returns:
            True if environment is valid, False otherwise
        """
        if not super().validate_environment():
            return False

        # Check for Claude Code specific requirements
        return True  # Claude Code doesn't require pre-existing .claude directory
