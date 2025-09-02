"""Template engine for generating agent-specific rule configurations."""

from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

from .factory import AdapterFactory


class TemplateEngine:
    """Engine for rendering agent-specific rule templates."""

    def __init__(self, templates_dir: Path):
        """Initialize template engine with templates directory.

        Args:
            templates_dir: Path to the templates directory
        """
        self.templates_dir = templates_dir
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def load_agent_config(self, agent_type: str) -> dict[str, Any]:
        """Load configuration for specified agent type.

        Args:
            agent_type: Type of coding agent (e.g., 'claude-code', 'cursor')

        Returns:
            Configuration dictionary for the agent

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid
        """
        config_path = (
            self.templates_dir.parent / "adapters" / "config" / f"{agent_type}.yaml"
        )

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)
            if not isinstance(config, dict):
                raise ValueError(f"Invalid configuration format in {config_path}")
            return config

    def render_configure_rules(
        self,
        agent_type: str,
        target_path: Path,
        additional_context: dict[str, Any] | None = None,
    ) -> str:
        """Render the configure_rules template for specified agent using two-pass rendering.

        Args:
            agent_type: Type of coding agent
            target_path: Path to target repository
            additional_context: Optional additional template context

        Returns:
            Rendered template content

        Raises:
            ValueError: If agent type is not supported
        """
        # Load agent configuration
        try:
            agent_config = self.load_agent_config(agent_type)
        except FileNotFoundError as e:
            raise ValueError(f"Unsupported agent type: {agent_type}") from e

        # Create adapter to get template variables
        adapter = AdapterFactory.create_adapter(agent_type, target_path, agent_config)

        # Combine configuration with adapter template variables
        template_context = {
            **agent_config,
            **adapter.get_template_variables(),
            **(additional_context or {}),
        }

        # TWO-PASS RENDERING:
        # Pass 1: Render Jinja2 template (including frontmatter)
        template = self.env.get_template("subagents/configure_rules.jinja2.md")
        rendered_content = template.render(**template_context)

        # Pass 2: Validate that frontmatter is valid YAML (optional)
        # This ensures the rendered frontmatter is proper YAML
        try:
            lines = rendered_content.split("\n")
            if lines[0] == "---":
                # Find end of frontmatter
                end_idx = None
                for i, line in enumerate(lines[1:], 1):
                    if line == "---":
                        end_idx = i
                        break

                if end_idx:
                    # Extract and validate frontmatter
                    frontmatter_content = "\n".join(lines[1:end_idx])
                    yaml.safe_load(frontmatter_content)  # Validate YAML

        except yaml.YAMLError as e:
            raise ValueError(
                f"Invalid YAML frontmatter after template rendering: {e}"
            ) from e

        return str(rendered_content)

    def generate_rules(
        self,
        agent_type: str,
        target_path: Path,
        additional_context: dict[str, Any] | None = None,
    ) -> list[Path]:
        """Generate and write rules for specified agent type.

        Args:
            agent_type: Type of coding agent
            target_path: Path to target repository
            additional_context: Optional additional template context

        Returns:
            List of output file paths where rules were written
        """
        # Render template
        rendered_content = self.render_configure_rules(
            agent_type, target_path, additional_context
        )

        # Create adapter and write rules
        adapter = AdapterFactory.create_adapter(agent_type, target_path)
        adapter.write_rules(rendered_content)

        return adapter.get_output_paths()
