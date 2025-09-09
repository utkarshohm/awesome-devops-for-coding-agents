"""Cursor rules manager adapter."""

import json
import os
import shutil
from pathlib import Path
from typing import Any

from ..base import BaseAdapter


class CursorRulesManager(BaseAdapter):
    """Adapter for generating Cursor rules configuration."""

    @property
    def agent_name(self) -> str:
        """Return the name of the coding agent this adapter supports."""
        return "cursor"

    @property
    def output_format(self) -> str:
        """Return the expected output format."""
        return "multiple_files"

    def get_template_variables(self) -> dict[str, Any]:
        """Return Cursor specific template variables."""
        # Merge default config with any provided config
        default_vars = {
            "agent_type": "cursor",
            "output_file": ".cursor/rules/",
        }

        # If config was provided, merge it in
        if self.config:
            default_vars.update(self.config)

        return default_vars

    def get_output_paths(self) -> list[Path]:
        """Return list of output paths where rules will be written."""
        cursor_rules_dir = self.target_path / ".cursor" / "rules"
        return [
            cursor_rules_dir / "development-workflow.mdc",
            cursor_rules_dir / "code-standards.mdc",
            cursor_rules_dir / "project-structure.mdc",
            cursor_rules_dir / "devops-practices.mdc",
        ]

    def write_rules(self, rendered_content: str) -> None:
        """Write the rendered rules to multiple .mdc files.

        Args:
            rendered_content: The rendered template content
        """
        cursor_rules_dir = self.target_path / ".cursor" / "rules"
        cursor_rules_dir.mkdir(parents=True, exist_ok=True)

        # Write main rules file
        main_file = cursor_rules_dir / "coding-agent-rules.mdc"
        main_file.write_text(rendered_content, encoding="utf-8")

        # Setup deny list rule for AI guidance
        self._setup_deny_list_rule(cursor_rules_dir)

    def install_workflows(self, workflows: list[str]) -> list[Path]:
        """Install workflow templates as Cursor commands.

        Args:
            workflows: List of workflow names to install

        Returns:
            List of output file paths where workflows were installed
        """
        cursor_commands_dir = self.target_path / ".cursor" / "commands"
        cursor_commands_dir.mkdir(parents=True, exist_ok=True)

        output_paths = []

        for workflow in workflows:
            # Create workflow command file for Cursor
            command_file = cursor_commands_dir / f"{workflow}.md"

            # Generate workflow command template for Cursor
            workflow_content = self._generate_workflow_command(workflow)

            command_file.write_text(workflow_content, encoding="utf-8")
            output_paths.append(command_file)

        return output_paths

    def install_subagents(self, subagents: list[str]) -> list[Path]:
        """Install subagent templates as Cursor commands (Cursor doesn't have separate subagents).

        Args:
            subagents: List of subagent names to install

        Returns:
            List of output file paths where subagents were installed as commands
        """
        cursor_commands_dir = self.target_path / ".cursor" / "commands"
        cursor_commands_dir.mkdir(parents=True, exist_ok=True)

        output_paths = []

        # Get the path to subagent templates
        templates_dir = Path(__file__).parent.parent.parent / "templates" / "subagents"

        for subagent in subagents:
            # Look for the template file
            template_file = templates_dir / f"{subagent}.jinja2.md"
            if template_file.exists():
                # Copy template to commands directory (Cursor uses commands not subagents)
                command_file = cursor_commands_dir / f"{subagent}.md"
                shutil.copy2(template_file, command_file)
                output_paths.append(command_file)
            else:
                # Generate a basic command template
                command_file = cursor_commands_dir / f"{subagent}.md"
                command_content = self._generate_command_template(subagent)
                command_file.write_text(command_content, encoding="utf-8")
                output_paths.append(command_file)

        return output_paths

    def configure_full_protection(
        self, auto_install_shell: bool = False
    ) -> dict[str, Any]:
        """Configure complete Cursor protection (AI + Shell).

        Args:
            auto_install_shell: If True, automatically install shell protection

        Returns:
            Dictionary with configuration results
        """
        results: dict[str, Any] = {
            "ai_commands": None,
            "ai_rules": None,
            "shell_protection": None,
            "vscode_settings": None,
        }

        # 1. Install AI commands
        results["ai_commands"] = self.install_ai_commands()

        # 2. Setup deny list rule (AI guidance)
        cursor_rules_dir = self.target_path / ".cursor" / "rules"
        cursor_rules_dir.mkdir(parents=True, exist_ok=True)
        self._setup_deny_list_rule(cursor_rules_dir)
        results["ai_rules"] = cursor_rules_dir / "bash_deny_list.mdc"

        # 3. Setup bash protection (shell enforcement)
        results["shell_protection"] = self.setup_bash_protection(auto_install_shell)

        # 4. Configure VS Code settings for Cursor
        vscode_settings = {
            "cursor.chat.model": "claude-3-5-sonnet",
            "cursor.chat.model.temperature": 0.3,
            "cursor.chat.model.maxTokens": 4096,
            "files.autoSave": "afterDelay",
            "editor.formatOnSave": True,
        }
        results["vscode_settings"] = self.configure_settings(vscode_settings)

        # Print summary
        print("\n🛡️  Cursor Protection Configuration Complete:")
        print(f"  ✅ AI Commands: {results['ai_commands']}")
        print(f"  ✅ AI Rules: {results['ai_rules']}")
        print(f"  ✅ VS Code Settings: {results['vscode_settings']}")

        if results["shell_protection"]["protection_installed"]:
            print("  ✅ Shell Protection: Installed")
        else:
            print("  ⚠️  Shell Protection: Manual setup required")
            for instruction in results["shell_protection"]["instructions"]:
                print(f"     {instruction}")

        return results

    def configure_settings(self, settings: dict[str, Any]) -> Path:
        """Update Cursor settings configuration.

        Args:
            settings: Dictionary of settings to update

        Returns:
            Path to the updated settings file
        """
        cursor_dir = self.target_path / ".cursor"
        cursor_dir.mkdir(parents=True, exist_ok=True)

        settings_file = cursor_dir / "settings.json"

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

    def _generate_workflow_command(self, workflow_name: str) -> str:
        """Generate a basic workflow command template for Cursor.

        Args:
            workflow_name: Name of the workflow

        Returns:
            Generated command content
        """
        return f"""# {workflow_name.replace("-", " ").title()} Workflow

## Overview
This is the {workflow_name} development workflow for Cursor.

## Usage
Use this workflow to guide your {workflow_name} development process.

## Instructions
1. Analyze requirements carefully
2. Plan your implementation approach
3. Execute development in phases
4. Validate results at each step

## Key Principles
- Follow best practices for {workflow_name}
- Maintain code quality throughout
- Document decisions and changes
- Test thoroughly before completion

*Note: This is a generated template. Customize according to your specific needs.*
"""

    def _generate_command_template(self, command_name: str) -> str:
        """Generate a basic command template for Cursor.

        Args:
            command_name: Name of the command

        Returns:
            Generated command content
        """
        return f"""# {command_name.replace("-", " ").title()} Command

## Purpose
This command handles {command_name.replace("-", " ")} tasks in Cursor.

## Usage
This command will help you with {command_name.replace("-", " ")} operations.

## Instructions
1. Analyze the current situation
2. Determine the best approach
3. Execute the necessary actions
4. Verify the results

## Capabilities
- Process and analyze requirements
- Execute specialized tasks
- Generate reports and recommendations
- Provide guidance and best practices

*Note: This is a generated template. Customize as needed for your specific use case.*
"""

    def validate_environment(self) -> bool:
        """Validate that the target environment is suitable for Cursor.

        Returns:
            True if environment is valid, False otherwise
        """
        if not super().validate_environment():
            return False

        # Cursor doesn't have specific requirements beyond basic directory structure
        return True

    def _setup_deny_list_rule(self, rules_dir: Path) -> None:
        """Setup the bash deny list rule for AI guidance.

        Args:
            rules_dir: Directory to install deny list to
        """
        # Copy bash_deny_list.mdc to rules directory
        source_file = (
            Path(__file__).parent.parent.parent
            / "templates"
            / "cursor-only"
            / "bash_deny_list.mdc"
        )
        if source_file.exists():
            dest_file = rules_dir / "bash_deny_list.mdc"
            shutil.copy2(source_file, dest_file)
            print(f"✅ Installed AI safety guidelines: {dest_file}")

    def setup_bash_protection(self, auto_install: bool = False) -> dict[str, Any]:
        """Setup bash-level protection for dangerous commands.

        Args:
            auto_install: If True, automatically install to shell config

        Returns:
            Dictionary with setup status and instructions
        """
        result: dict[str, Any] = {
            "shell_type": None,
            "rc_file": None,
            "protection_installed": False,
            "ai_rules_installed": False,
            "instructions": [],
        }

        # Detect shell type
        shell = os.environ.get("SHELL", "")
        home = Path.home()

        if "zsh" in shell:
            result["shell_type"] = "zsh"
            result["rc_file"] = home / ".zshrc"
        elif "bash" in shell:
            result["shell_type"] = "bash"
            result["rc_file"] = home / ".bashrc"
        else:
            result["instructions"].append("⚠️  Could not detect shell type")
            return result

        # Setup deny list rule (always do this)
        cursor_rules_dir = self.target_path / ".cursor" / "rules"
        cursor_rules_dir.mkdir(parents=True, exist_ok=True)
        self._setup_deny_list_rule(cursor_rules_dir)
        result["ai_rules_installed"] = True

        # Setup bash protection file
        protection_file = (
            Path(__file__).parent.parent.parent
            / "templates"
            / "cursor-only"
            / "bash_protection.sh"
        )

        if not protection_file.exists():
            result["instructions"].append(
                f"❌ Protection file not found: {protection_file}"
            )
            return result

        # Check if already installed
        if result["rc_file"].exists():
            rc_content = result["rc_file"].read_text()
            if (
                "bash_protection.sh" in rc_content
                or "Cursor AI Safety Shell Protection" in rc_content
            ):
                result["protection_installed"] = True
                result["instructions"].append("✅ Shell protection already installed")
                return result

        if auto_install:
            # Add source line to shell config
            source_line = f"\n# Cursor AI Safety Protection\nsource {protection_file}\n"

            with open(result["rc_file"], "a") as f:
                f.write(source_line)

            result["protection_installed"] = True
            result["instructions"].append(
                f"✅ Shell protection installed to {result['rc_file']}"
            )
            result["instructions"].append("🔄 Restart terminal or run: source ~/.zshrc")
        else:
            # Provide manual instructions
            result["instructions"].extend(
                [
                    "📋 To install shell protection manually:",
                    f"1. Add to {result['rc_file']}:",
                    f"   source {protection_file}",
                    "2. Restart terminal or run:",
                    f"   source {result['rc_file']}",
                    "3. Verify with: cursor_protection_status",
                ]
            )

        return result

    def install_ai_commands(self) -> Path:
        """Install AI commands with safety guidelines.

        Returns:
            Path to the AI commands file
        """
        # Create ai-commands.json with safety-focused commands
        ai_commands = [
            {
                "name": "safe-commit",
                "prompt": "Stage and commit changes. NEVER use 'git add .' or 'git add -A'. Always add specific files by name. Show me what files you're adding before committing. Check .cursor/rules/bash_deny_list.mdc for safety guidelines.",
                "description": "Safely commit changes with specific file additions",
            },
            {
                "name": "install-deps",
                "prompt": "Install project dependencies. First, show me what will be installed. Never use sudo. Prefer virtual environments for Python. Check .cursor/rules/bash_deny_list.mdc for safety guidelines.",
                "description": "Safely install dependencies with review",
            },
            {
                "name": "run-tests",
                "prompt": "Run the test suite. If tests fail, analyze the errors and suggest fixes without making destructive changes. Never use rm -rf or force operations.",
                "description": "Run tests and analyze results safely",
            },
            {
                "name": "code-review",
                "prompt": "Review the current changes for potential issues. Check for: accidental commits of sensitive files, unsafe commands, proper error handling. Reference .cursor/rules/bash_deny_list.mdc.",
                "description": "Review code changes for safety and quality",
            },
            {
                "name": "safe-cleanup",
                "prompt": "Clean up temporary files and build artifacts. Never use 'rm -rf' without showing what will be deleted first. Use interactive mode when possible.",
                "description": "Safely clean up project files",
            },
        ]

        commands_file = self.target_path / "ai-commands.json"

        # Merge with existing commands if file exists
        if commands_file.exists():
            with open(commands_file) as f:
                existing = json.load(f)
                if isinstance(existing, list):
                    # Don't duplicate commands
                    existing_names = {
                        cmd.get("name") for cmd in existing if isinstance(cmd, dict)
                    }
                    for cmd in ai_commands:
                        if cmd["name"] not in existing_names:
                            existing.append(cmd)
                    ai_commands = existing

        with open(commands_file, "w") as f:
            json.dump(ai_commands, f, indent=2)

        print(f"✅ Installed AI commands: {commands_file}")
        return commands_file
