"""Template engine for generating agent-specific rule configurations."""

import logging
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

    def list_coding_workflows(self) -> list[dict[str, str]]:
        """List available coding workflow templates.

        Returns:
            List of workflow dictionaries with name, description, and purpose
        """
        workflows_dir = self.templates_dir / "workflows" / "coding"
        workflows: list[dict[str, str]] = []

        if not workflows_dir.exists():
            return workflows

        for template_file in workflows_dir.glob("*.jinja2.md"):
            try:
                template = self.env.get_template(
                    f"workflows/coding/{template_file.name}"
                )
                # Render with dummy agent_type to extract frontmatter
                content = template.render(agent_type="cursor")

                # Parse frontmatter to get metadata
                lines = content.split("\n")
                if lines[0] == "---":
                    end_idx = None
                    for i, line in enumerate(lines[1:], 1):
                        if line == "---":
                            end_idx = i
                            break

                    if end_idx:
                        frontmatter_content = "\n".join(lines[1:end_idx])
                        metadata = yaml.safe_load(frontmatter_content)

                        workflow_name = template_file.stem.replace(".jinja2", "")
                        workflows.append(
                            {
                                "name": workflow_name,
                                "title": metadata.get("name", workflow_name),
                                "description": metadata.get(
                                    "description", "No description available"
                                ),
                            }
                        )
            except Exception as e:
                # Skip templates that can't be parsed
                # Log the error but continue processing other templates
                logger = logging.getLogger(__name__)
                logger.debug(
                    "Skipping template %s due to parsing error: %s",
                    template_file.name,
                    e,
                )
                continue

        return workflows

    def render_coding_workflow(
        self,
        workflow_name: str,
        agent_type: str,
        additional_context: dict[str, Any] | None = None,
    ) -> str:
        """Render a coding workflow template for specified agent.

        Args:
            workflow_name: Name of the workflow template
            agent_type: Type of coding agent
            additional_context: Optional additional template context

        Returns:
            Rendered workflow content

        Raises:
            ValueError: If workflow template doesn't exist or agent type is unsupported
        """
        template_path = f"workflows/coding/{workflow_name}.jinja2.md"

        try:
            template = self.env.get_template(template_path)
        except Exception as e:
            raise ValueError(f"Workflow template '{workflow_name}' not found") from e

        # Validate agent type
        supported_agents = ["claude-code", "cursor"]
        if agent_type not in supported_agents:
            raise ValueError(f"Unsupported agent type: {agent_type}")

        # Create template context
        template_context = {
            "agent_type": agent_type,
            **(additional_context or {}),
        }

        return str(template.render(**template_context))

    def install_coding_workflows(
        self,
        workflow_names: list[str],
        agent_type: str,
        target_path: Path,
        additional_context: dict[str, Any] | None = None,
    ) -> list[Path]:
        """Install coding workflow templates to the appropriate directory.

        Args:
            workflow_names: List of workflow names to install
            agent_type: Type of coding agent
            target_path: Path to target repository
            additional_context: Optional additional template context

        Returns:
            List of output file paths where workflows were installed

        Raises:
            ValueError: If workflow or agent type is invalid
        """
        output_paths = []

        # Determine target directory based on agent type
        if agent_type == "claude-code":
            commands_dir = target_path / ".claude" / "commands"
        elif agent_type == "cursor":
            commands_dir = target_path / ".cursor" / "commands"
        else:
            raise ValueError(f"Unsupported agent type: {agent_type}")

        # Create directory if it doesn't exist
        commands_dir.mkdir(parents=True, exist_ok=True)

        # Install each workflow
        for workflow_name in workflow_names:
            rendered_content = self.render_coding_workflow(
                workflow_name, agent_type, additional_context
            )

            output_file = commands_dir / f"{workflow_name}.md"
            output_file.write_text(rendered_content, encoding="utf-8")
            output_paths.append(output_file)

        return output_paths

    def render_subagent_template(
        self,
        subagent_name: str,
        agent_type: str,
        target_path: Path,
        additional_context: dict[str, Any] | None = None,
    ) -> str:
        """Render a subagent template for specified agent using two-pass rendering.

        Args:
            subagent_name: Name of the subagent template (e.g., 'detect_conflicting_instructions')
            agent_type: Type of coding agent
            target_path: Path to target repository
            additional_context: Optional additional template context

        Returns:
            Rendered template content

        Raises:
            ValueError: If agent type or subagent is not supported
        """
        # Validate agent type
        supported_agents = ["claude-code", "cursor"]
        if agent_type not in supported_agents:
            raise ValueError(f"Unsupported agent type: {agent_type}")

        # Check if template exists
        template_path = f"subagents/{subagent_name}.jinja2.md"
        try:
            template = self.env.get_template(template_path)
        except Exception as e:
            raise ValueError(f"Subagent template '{subagent_name}' not found") from e

        # Create template context
        template_context = {
            "agent_type": agent_type,
            "target_path": target_path,
            **(additional_context or {}),
        }

        # TWO-PASS RENDERING:
        # Pass 1: Render Jinja2 template (including frontmatter)
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

    def generate_subagent_rules(
        self,
        subagent_name: str,
        agent_type: str,
        target_path: Path,
        additional_context: dict[str, Any] | None = None,
    ) -> list[Path]:
        """Generate and write subagent rules for specified agent type.

        Args:
            subagent_name: Name of the subagent template
            agent_type: Type of coding agent
            target_path: Path to target repository
            additional_context: Optional additional template context

        Returns:
            List of output file paths where rules were written
        """
        # Render template
        rendered_content = self.render_subagent_template(
            subagent_name, agent_type, target_path, additional_context
        )

        # Determine output path based on agent type
        if agent_type == "claude-code":
            # For Claude Code, create a command file
            commands_dir = target_path / ".claude" / "commands"
            commands_dir.mkdir(parents=True, exist_ok=True)
            output_file = commands_dir / f"{subagent_name}.md"
        elif agent_type == "cursor":
            # For Cursor, create a command file
            commands_dir = target_path / ".cursor" / "commands"
            commands_dir.mkdir(parents=True, exist_ok=True)
            output_file = commands_dir / f"{subagent_name}.md"
        else:
            raise ValueError(f"Unsupported agent type: {agent_type}")

        # Write the rendered content
        output_file.write_text(rendered_content, encoding="utf-8")

        return [output_file]
