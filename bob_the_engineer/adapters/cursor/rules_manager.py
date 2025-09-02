"""Cursor rules manager adapter."""

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

        # For now, write all content to a single comprehensive file
        # TODO: Split content into categorized files based on sections
        main_file = cursor_rules_dir / "coding-agent-rules.mdc"
        main_file.write_text(rendered_content, encoding="utf-8")

    def validate_environment(self) -> bool:
        """Validate that the target environment is suitable for Cursor.

        Returns:
            True if environment is valid, False otherwise
        """
        if not super().validate_environment():
            return False

        # Cursor doesn't have specific requirements beyond basic directory structure
        return True
