"""Claude Code rules manager adapter."""

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

    def validate_environment(self) -> bool:
        """Validate that the target environment is suitable for Claude Code.

        Returns:
            True if environment is valid, False otherwise
        """
        if not super().validate_environment():
            return False

        # Check for Claude Code specific requirements
        return True  # Claude Code doesn't require pre-existing .claude directory
