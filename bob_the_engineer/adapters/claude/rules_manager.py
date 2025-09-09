"""Claude Code rules manager adapter."""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from rich.console import Console

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

    @staticmethod
    def load_settings_template(template_name: str) -> dict[str, Any]:
        """Load a Claude Code settings template from the templates directory."""
        template_file = (
            Path(__file__).parent.parent.parent
            / "templates"
            / "settings"
            / f"claude_{template_name}.json"
        )

        if not template_file.exists():
            available = ClaudeRulesManager.list_available_templates()
            available_names = [t.stem.replace("claude_", "") for t in available]
            raise FileNotFoundError(
                f"Template '{template_name}' not found. Available: {', '.join(available_names)}"
            )

        with template_file.open() as f:
            return cast(dict[str, Any], json.load(f))

    @staticmethod
    def list_available_templates() -> list[Path]:
        """List all available Claude Code settings templates."""
        templates_dir = Path(__file__).parent.parent.parent / "templates" / "settings"
        if not templates_dir.exists():
            return []
        return list(templates_dir.glob("claude_*.json"))

    def apply_settings_template(
        self, template: dict[str, Any], dry_run: bool = False
    ) -> None:
        """Apply a Claude Code settings template to the project.

        Args:
            template: The template configuration dictionary
            dry_run: If True, preview changes without applying them
        """
        console = Console()

        template_info = template.get("_template_info", {})
        template_name = template_info.get("name", "unknown")

        if dry_run:
            console.print(
                f"\n[bold yellow]Dry Run - {template_name} template for Claude Code[/bold yellow]"
            )
            console.print(
                f"[dim]Description: {template_info.get('description', 'N/A')}[/dim]"
            )
            console.print(
                f"[dim]Best for: {template_info.get('best_for', 'N/A')}[/dim]"
            )

            settings_file = self.target_path / ".claude" / "settings.json"
            console.print(f"[dim]Would update: {settings_file}[/dim]")

            # Show permissions summary
            permissions_summary = template_info.get("permissions_summary", {})
            if permissions_summary:
                console.print("\n[bold]Configuration Summary:[/bold]")
                for perm_type, descriptions in permissions_summary.items():
                    if perm_type == "allow":
                        console.print("[green]✓ ALLOWED Operations:[/green]")
                    elif perm_type == "deny":
                        console.print("[red]✗ DENIED Operations:[/red]")
                    elif perm_type == "ask":
                        console.print("[yellow]? ASK Operations:[/yellow]")

                    for i, desc in enumerate(descriptions, 1):
                        console.print(f"  {i}. {desc}")
                    console.print()

            console.print(
                "[yellow]This is a preview. Remove --dry-run to apply changes.[/yellow]"
            )
            return

        # Apply the configuration
        console.print(
            f"\n[bold green]Applying {template_name} template for Claude Code[/bold green]"
        )

        # Create backup if settings exist
        settings_file = self.target_path / ".claude" / "settings.json"
        if settings_file.exists():
            backup_file = settings_file.with_suffix(
                f".json.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            )
            backup_file.write_text(settings_file.read_text())
            console.print(f"[dim]✓ Created backup: {backup_file.name}[/dim]")

        # Remove template metadata and apply settings
        settings_data = {k: v for k, v in template.items() if not k.startswith("_")}
        self.configure_settings(settings_data)

        # Show summary
        template_info = template.get("_template_info", {})
        console.print(f"\n[bold cyan]Applied Template: {template_name}[/bold cyan]")
        console.print(
            f"[dim]Description: {template_info.get('description', 'N/A')}[/dim]"
        )

        # Show key permissions summary
        if "permissions" in settings_data:
            perms = settings_data["permissions"]
            if "allow" in perms:
                console.print(
                    f"[green]✓[/green] {len(perms['allow'])} allowed operations"
                )
            if "deny" in perms:
                console.print(f"[red]✗[/red] {len(perms['deny'])} denied operations")
            if "ask" in perms:
                console.print(
                    f"[yellow]?[/yellow] {len(perms['ask'])} operations require approval"
                )

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
model: claude-sonnet-4-20250514
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
model: claude-sonnet-4-20250514
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
