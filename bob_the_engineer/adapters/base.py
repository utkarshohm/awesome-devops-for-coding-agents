"""Base adapter interface for coding agents."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseAdapter(ABC):
    """Base adapter for coding agent integrations."""

    def __init__(self, target_path: Path, config: dict[str, Any] | None = None):
        """Initialize adapter with target repository path and optional configuration.

        Args:
            target_path: Path to the target repository
            config: Optional configuration dict for the adapter
        """
        self.target_path = target_path
        self.config = config or {}

    @property
    @abstractmethod
    def agent_name(self) -> str:
        """Return the name of the coding agent this adapter supports."""
        pass

    @property
    @abstractmethod
    def output_format(self) -> str:
        """Return the expected output format (e.g., 'single_file', 'multiple_files')."""
        pass

    @abstractmethod
    def get_template_variables(self) -> dict[str, Any]:
        """Return variables to be used in template rendering.

        Returns:
            Dictionary of template variables specific to this adapter
        """
        pass

    @abstractmethod
    def write_rules(self, rendered_content: str) -> None:
        """Write the rendered rules to appropriate location(s).

        Args:
            rendered_content: The rendered template content
        """
        pass

    @abstractmethod
    def get_output_paths(self) -> list[Path]:
        """Return list of output paths where rules will be written.

        Returns:
            List of Path objects for output files
        """
        pass

    @abstractmethod
    def install_workflows(self, workflows: list[str]) -> list[Path]:
        """Install workflow templates as agent commands.

        Args:
            workflows: List of workflow names to install

        Returns:
            List of output file paths where workflows were installed
        """
        pass

    @abstractmethod
    def install_subagents(self, subagents: list[str]) -> list[Path]:
        """Install subagent templates as agent subagents.

        Args:
            subagents: List of subagent names to install

        Returns:
            List of output file paths where subagents were installed
        """
        pass

    @abstractmethod
    def configure_settings(self, settings: dict[str, Any]) -> Path:
        """Update agent settings configuration.

        Args:
            settings: Dictionary of settings to update

        Returns:
            Path to the updated settings file
        """
        pass

    def validate_environment(self) -> bool:
        """Validate that the target environment is suitable for this adapter.

        Returns:
            True if environment is valid, False otherwise
        """
        return self.target_path.exists() and self.target_path.is_dir()
