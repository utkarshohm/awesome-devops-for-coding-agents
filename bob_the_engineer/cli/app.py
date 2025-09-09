"""Main CLI application for bob-the-engineer."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from bob_the_engineer import __version__
from bob_the_engineer.adapters.claude.rules_manager import ClaudeRulesManager
from bob_the_engineer.adapters.cursor.rules_manager import CursorRulesManager
from bob_the_engineer.adapters.factory import AdapterFactory
from bob_the_engineer.adapters.template_engine import TemplateEngine
from bob_the_engineer.cli.logging_config import get_logger, setup_cli_logging

# Create the main Typer app
app = typer.Typer(
    name="bob-the-engineer",
    help="Agentic DevOps OSS CLI",
    add_completion=False,
)

console = Console()


@app.callback()
def main_callback(
    verbose: int = typer.Option(
        0,
        "-v",
        "--verbose",
        count=True,
        help="Increase verbosity (use -v, -vv, or -vvv)",
    ),
    log_file: str | None = typer.Option(
        None,
        "--log-file",
        help="Write logs to file",
    ),
) -> None:
    """Bob the Engineer - Agentic DevOps OSS CLI."""
    # Set up logging based on verbosity
    setup_cli_logging(verbose=verbose, log_file=log_file)


@app.command()
def version() -> None:
    """Show version information."""
    logger = get_logger(__name__)
    logger.info("Version command invoked")

    table = Table(title="Bob the Engineer")
    table.add_column("Component", style="cyan")
    table.add_column("Version", style="magenta")

    table.add_row("bob-the-engineer", __version__)
    table.add_row("Python", "3.10+")

    console.print(table)


@app.command()
def hello(
    name: str = typer.Option("World", help="Name to greet"),
) -> None:
    """Say hello with structured logging example."""
    logger = get_logger(__name__)

    logger.info("Hello command invoked", name=name)

    console.print(f"[bold green]Hello {name}![/bold green]")

    logger.debug("Hello command completed successfully", name=name)


@app.command()
def status() -> None:
    """Show project status and configuration."""
    logger = get_logger(__name__)

    logger.info("Status command invoked")

    # Check if we're in a git repository
    git_dir = Path(".git")

    table = Table(title="Project Status")
    table.add_column("Check", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="dim")

    # Git repository check
    if git_dir.exists():
        table.add_row("Git Repository", "✓ Found", str(git_dir.absolute()))
        logger.info("Git repository detected")
    else:
        table.add_row("Git Repository", "✗ Not found", "Not in a git repository")
        logger.warning("No git repository found")

    # Configuration files check
    config_files = [
        ("pyproject.toml", "Python project config"),
        (".pre-commit-config.yaml", "Pre-commit hooks"),
        ("package.json", "Node.js project config"),
        ("Dockerfile", "Container configuration"),
    ]

    for filename, description in config_files:
        filepath = Path(filename)
        if filepath.exists():
            table.add_row(description, "✓ Found", str(filepath.absolute()))
            logger.info("Configuration file found", file=filename)
        else:
            table.add_row(description, "✗ Not found", f"No {filename}")
            logger.warning("Configuration file missing", file=filename)

    console.print(table)
    logger.info("Status command completed")


@app.command()
def configure_defaults(
    agent_type: str = typer.Option(
        None, help="Type of coding agent (claude-code, cursor)"
    ),
    repo_path: str = typer.Option(".", help="Path to target repository"),
    template_type: str = typer.Option(
        None,
        help="Configuration template to use (vibe_coder, software_engineer)",
    ),
    auto_detect: bool = typer.Option(
        False,
        "--auto-detect",
        help="Auto-detect best template based on repository analysis",
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Preview configuration without applying changes"
    ),
    list_templates: bool = typer.Option(
        False, "--list", help="List all available configuration templates"
    ),
) -> None:
    """Configure coding agent default settings with best-practice templates.

    This command applies optimal configuration settings for your coding agent
    based on proven templates for different development scenarios.

    Available Templates:

    • vibe_coder: Fast iteration for solo developers and rapid prototyping
    • software_engineer: Production-focused with security and team collaboration

    Examples:

    # List all available templates with details
    bob configure-defaults --list

    # Apply specific template
    bob configure-defaults --agent-type claude-code --template-type vibe_coder
    bob configure-defaults --agent-type cursor --template-type software_engineer

    # Preview configuration without applying
    bob configure-defaults --agent-type cursor --template-type vibe_coder --dry-run
    """
    logger = get_logger(__name__)

    logger.info(
        "Configure defaults command invoked",
        agent_type=agent_type,
        repo_path=repo_path,
        template_type=template_type,
        dry_run=dry_run,
    )

    try:
        # List templates if requested
        if list_templates:
            _display_available_templates()
            return

        # Validate required parameters
        if not agent_type:
            console.print("[red]Error:[/red] --agent-type is required")
            console.print("[dim]Supported types: claude-code, cursor[/dim]")
            raise typer.Exit(1)

        if not template_type:
            console.print("[red]Error:[/red] --template-type is required")
            console.print(
                "[dim]Available templates: vibe_coder, software_engineer[/dim]"
            )
            console.print("[dim]Use --list to see detailed descriptions[/dim]")
            raise typer.Exit(1)

        # Validate agent type
        supported_agents = ["claude-code", "cursor"]
        if agent_type not in supported_agents:
            console.print(f"[red]Error:[/red] Unsupported agent type: {agent_type}")
            console.print(f"[dim]Supported types: {', '.join(supported_agents)}[/dim]")
            raise typer.Exit(1)

        # Validate template type
        available_templates = ["vibe_coder", "software_engineer"]
        if template_type not in available_templates:
            console.print(
                f"[red]Error:[/red] Unsupported template type: {template_type}"
            )
            console.print(
                f"[dim]Available templates: {', '.join(available_templates)}[/dim]"
            )
            raise typer.Exit(1)

        # Validate repository path
        repo_path_obj = Path(repo_path).resolve()
        if not repo_path_obj.exists():
            console.print(
                f"[red]Error:[/red] Repository path does not exist: {repo_path}"
            )
            raise typer.Exit(1)

        console.print(
            f"[cyan]Configuring {agent_type} with {template_type} template...[/cyan]"
        )

        # Apply configuration based on agent type
        if agent_type == "claude-code":
            _configure_claude_code(repo_path_obj, template_type, dry_run)
        elif agent_type == "cursor":
            _configure_cursor(repo_path_obj, template_type, dry_run)

        logger.info("Configure defaults command completed successfully")

    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        logger.error(
            "Configure defaults command failed with unexpected error", error=str(e)
        )
        raise typer.Exit(1) from e


def _display_available_templates() -> None:
    """Display information about available configuration templates."""
    templates = ClaudeRulesManager.list_available_templates()

    if not templates:
        console.print("[yellow]No configuration templates found.[/yellow]")
        return

    console.print("\n[bold cyan]Available Configuration Templates[/bold cyan]")

    table = Table()
    table.add_column("Template", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Best For", style="dim")

    for template_file in templates:
        template_name = template_file.stem.replace("settings_", "")
        try:
            template_data = ClaudeRulesManager.load_settings_template(template_name)
            info = template_data.get("_template_info", {})

            table.add_row(
                template_name,
                info.get("description", "No description"),
                info.get("best_for", "General use"),
            )
        except Exception as e:
            table.add_row(
                template_name, f"[red]Error loading template: {e}[/red]", "N/A"
            )

    console.print(table)
    console.print(
        "\n[dim]Use --agent-type and --template-type to apply a template.[/dim]"
    )


def _configure_claude_code(repo_path: Path, template_name: str, dry_run: bool) -> None:
    """Configure Claude Code with the specified template."""
    try:
        # Load template
        console.print(f"[cyan]Loading {template_name} template...[/cyan]")
        template = ClaudeRulesManager.load_settings_template(template_name)

        # Get adapter and apply configuration
        adapter = AdapterFactory.create_adapter("claude-code", target_path=repo_path)
        # Cast to ClaudeRulesManager since apply_settings_template is specific to Claude Code
        if isinstance(adapter, ClaudeRulesManager):
            adapter.apply_settings_template(template, dry_run=dry_run)
        else:
            raise TypeError("Expected ClaudeRulesManager adapter")

        if not dry_run:
            console.print("[green]✓ Claude Code configuration completed![/green]")

    except Exception as e:
        console.print(f"[red]Error configuring Claude Code:[/red] {e}")
        raise


def _configure_cursor(repo_path: Path, template_name: str, dry_run: bool) -> None:
    """Configure Cursor with the specified template."""
    try:
        # Load template info
        console.print(f"[cyan]Loading {template_name} template...[/cyan]")
        template = ClaudeRulesManager.load_settings_template(template_name)
        template_info = template.get("_template_info", {})

        # Get adapter
        adapter = AdapterFactory.create_adapter("cursor", target_path=repo_path)

        # Handle template-specific behavior for Cursor
        if template_name == "vibe_coder":
            if dry_run:
                console.print(
                    f"\n[bold yellow]Dry Run - {template_name} template for Cursor[/bold yellow]"
                )
                console.print(
                    f"[dim]Description: {template_info.get('description', 'N/A')}[/dim]"
                )
                console.print(
                    "\n[yellow]This template requires no additional Cursor rules.[/yellow]"
                )
                console.print(
                    "[dim]The vibe_coder template is designed for minimal restrictions.[/dim]"
                )
                console.print(
                    "[dim]Since Cursor doesn't enforce command-level permissions,[/dim]"
                )
                console.print(
                    "[dim]no additional configuration files are needed.[/dim]"
                )
            else:
                console.print(
                    f"\n[bold green]Applying {template_name} template for Cursor[/bold green]"
                )
                console.print(
                    "[yellow]✓ No additional Cursor rules needed for this template.[/yellow]"
                )
                console.print(
                    "[dim]The vibe_coder template is designed for minimal restrictions.[/dim]"
                )
                console.print(
                    "[dim]Your Cursor environment is ready for fast iteration![/dim]"
                )

        elif template_name == "software_engineer":
            if dry_run:
                console.print(
                    f"\n[bold yellow]Dry Run - {template_name} template for Cursor[/bold yellow]"
                )
                console.print(
                    f"[dim]Description: {template_info.get('description', 'N/A')}[/dim]"
                )
                console.print("\n[yellow]Would install security protections:[/yellow]")
                console.print(
                    "  • AI safety guidelines (.cursor/rules/bash_deny_list.mdc)"
                )
                console.print("  • Shell command protection (bash_protection.sh)")
                console.print("  • Safe AI commands (ai-commands.json)")
            else:
                # Apply security protections using existing rules manager
                console.print(
                    f"\n[bold green]Applying {template_name} template for Cursor[/bold green]"
                )
                # Cast to CursorRulesManager since configure_full_protection is specific to Cursor
                if isinstance(adapter, CursorRulesManager):
                    results = adapter.configure_full_protection()
                else:
                    raise TypeError("Expected CursorRulesManager adapter")

                console.print(
                    "\n[bold cyan]Security Configuration Applied:[/bold cyan]"
                )
                if results.get("ai_rules"):
                    console.print("  ✅ AI safety guidelines installed")
                if results.get("ai_commands"):
                    console.print("  ✅ Safe AI commands configured")
                if results.get("shell_protection", {}).get("protection_installed"):
                    console.print("  ✅ Shell protection enabled")

        if not dry_run:
            console.print("[green]✓ Cursor configuration completed![/green]")

    except Exception as e:
        console.print(f"[red]Error configuring Cursor:[/red] {e}")
        raise


def _display_analysis_results(analysis: Any) -> None:
    """Display repository analysis results."""
    console.print("\n[bold cyan]Repository Analysis Results[/bold cyan]")
    console.print("=" * 40)

    # Tech stack
    if hasattr(analysis, "tech_stack") and analysis.tech_stack:
        tech_list = ", ".join(analysis.tech_stack)
        console.print(f"[bold]Tech Stack:[/bold] {tech_list}")

    # Team size
    if hasattr(analysis, "team_size"):
        console.print(f"[bold]Estimated Team Size:[/bold] {analysis.team_size}")

    # Repository characteristics
    if hasattr(analysis, "repo_size"):
        console.print(f"[bold]Repository Size:[/bold] ~{analysis.repo_size} files")

    if hasattr(analysis, "security_level"):
        console.print(f"[bold]Security Level:[/bold] {analysis.security_level}")

    # Features detected
    features = []
    if hasattr(analysis, "has_ci_cd") and analysis.has_ci_cd:
        features.append("CI/CD")
    if hasattr(analysis, "has_containers") and analysis.has_containers:
        features.append("Containers")
    if hasattr(analysis, "has_microservices") and analysis.has_microservices:
        features.append("Microservices")

    if features:
        console.print(f"[bold]Features Detected:[/bold] {', '.join(features)}")

    # Display package managers and frameworks
    if analysis.package_managers:
        console.print(
            f"\n[bold]Package Managers:[/bold] {', '.join(analysis.package_managers)}"
        )
    if analysis.frameworks:
        console.print(f"[bold]Frameworks:[/bold] {', '.join(analysis.frameworks)}")


def _display_config_preview(
    template: Any, agent_type: str, config_content: str, analysis: Any
) -> None:
    """Display configuration preview without applying changes."""
    console.print(
        f"\n[bold yellow]Configuration Preview - {template.name}[/bold yellow]"
    )
    console.print("=" * 60)

    # Show template info
    console.print(f"[bold]Template:[/bold] {template.name}")
    console.print(f"[bold]Agent Type:[/bold] {agent_type}")
    console.print(f"[bold]Description:[/bold] {template.description}")

    if agent_type == "claude-code":
        files_to_modify = [".claude-code-config.json"]
    else:
        files_to_modify = [".cursorrules"]

    console.print("\n[bold]Files to be created/modified:[/bold]")
    for file in files_to_modify:
        console.print(f"  • {file}")

    console.print("\n[bold]Configuration Content Preview:[/bold]")

    # Show first few lines of config
    lines = config_content.split("\n")
    preview_lines = lines[:15] if len(lines) > 15 else lines

    for line in preview_lines:
        console.print(f"  {line}")

    if len(lines) > 15:
        console.print(f"  ... ({len(lines) - 15} more lines)")

    # Show recommendation confidence
    console.print(
        f"\n[dim]Template recommendation confidence: {analysis.confidence:.1%}[/dim]"
    )
    console.print(
        "\n[yellow]This is a preview. Use --no-dry-run to apply the configuration.[/yellow]"
    )


def _apply_configuration(
    template: Any, agent_type: str, config_content: str, repo_path: Path, analysis: Any
) -> None:
    """Apply the configuration to the repository."""
    console.print(
        f"\n[bold green]Applying {template.name} configuration...[/bold green]"
    )

    try:
        if agent_type == "claude-code":
            config_file = repo_path / ".claude-code-config.json"
            config_file.write_text(config_content)
            console.print(f"[green]✓[/green] Created {config_file}")

        elif agent_type == "cursor":
            config_file = repo_path / ".cursorrules"
            config_file.write_text(config_content)
            console.print(f"[green]✓[/green] Created {config_file}")

        # Generate documentation
        doc_content = f"""# Coding Agent Configuration Applied

**Template:** {template.name}
**Agent Type:** {agent_type}
**Applied:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Template Description
{template.description}

## Best For
{template.best_for}

## Configuration Details
- Confidence Score: {analysis.confidence:.1%}
- Repository Analysis: Completed
- Tech Stack: {", ".join(analysis.tech_stack) if hasattr(analysis, "tech_stack") else "Unknown"}

## Usage Notes
Refer to the {agent_type} documentation for how to use these configuration settings.

## Next Steps
1. Test the configuration with a simple coding task
2. Adjust settings based on your team's feedback
3. Consider running `bob configure-defaults --list` to explore other templates

Generated by bob-the-engineer configure-defaults
"""
        doc_file = repo_path / f"AGENT_CONFIG_{agent_type.upper()}.md"
        doc_file.write_text(doc_content)
        console.print(f"[green]✓[/green] Created documentation: {doc_file}")

        console.print("\n[bold green]Configuration successfully applied![/bold green]")
        console.print(
            f"[dim]Template: {template.name} (confidence: {analysis.confidence:.1%})[/dim]"
        )
        console.print(f"[dim]Files created: {config_file.name}, {doc_file.name}[/dim]")

    except Exception as e:
        console.print(f"[red]Error applying configuration:[/red] {e}")
        raise


@app.command()
def configure_workflows(
    workflows: str = typer.Option(
        ...,
        help="Workflows to configure (comma-separated: spec-driven,tdd,code-review,research,triage)",
    ),
    agent_type: str = typer.Option(
        ..., help="Type of coding agent (claude-code, cursor)"
    ),
    repo_path: str = typer.Option(".", help="Path to target repository"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Preview installation without applying changes"
    ),
) -> None:
    """Configure development workflow templates as coding agent commands.

    This command configures proven development workflows tailored to your coding agent.
    Each workflow is installed as a specialized command that guides development practices.

    Available workflows: spec-driven, tdd, code-review, research, triage

    Examples:
    bob configure-workflows --workflows spec-driven,tdd --agent-type claude-code
    bob configure-workflows --workflows code-review --agent-type cursor --dry-run
    """
    logger = get_logger(__name__)

    logger.info(
        "Configure workflows command invoked",
        workflows=workflows,
        agent_type=agent_type,
        repo_path=repo_path,
        dry_run=dry_run,
    )

    try:
        # Validate agent type
        supported_agents = ["claude-code", "cursor"]
        if agent_type not in supported_agents:
            console.print(f"[red]Error:[/red] Unsupported agent type: {agent_type}")
            console.print(f"[dim]Supported types: {', '.join(supported_agents)}[/dim]")
            raise typer.Exit(1)

        # Validate repository path
        repo_path_obj = Path(repo_path).resolve()
        if not repo_path_obj.exists():
            console.print(
                f"[red]Error:[/red] Repository path does not exist: {repo_path}"
            )
            raise typer.Exit(1)

        # Parse workflows
        workflow_list = [w.strip() for w in workflows.split(",")]
        available_workflows = [
            "spec-driven",
            "tdd",
            "code-review",
            "research",
            "triage",
        ]

        # Validate workflows
        invalid_workflows = [w for w in workflow_list if w not in available_workflows]
        if invalid_workflows:
            console.print(
                f"[red]Error:[/red] Invalid workflows: {', '.join(invalid_workflows)}"
            )
            console.print(
                f"[dim]Available workflows: {', '.join(available_workflows)}[/dim]"
            )
            raise typer.Exit(1)

        console.print(f"[cyan]Configuring workflows for {agent_type}...[/cyan]")

        # Create adapter and configure workflows
        adapter = AdapterFactory.create_adapter(agent_type, target_path=repo_path_obj)

        if dry_run:
            console.print(
                "[yellow]Dry-run mode: Preview of workflow configuration[/yellow]"
            )
            console.print(f"[dim]Target agent: {agent_type}[/dim]")
            console.print(f"[dim]Repository: {repo_path_obj}[/dim]")
            console.print(
                f"[dim]Workflows to configure: {', '.join(workflow_list)}[/dim]"
            )

            if agent_type == "claude-code":
                console.print("[dim]Would create commands in .claude/commands/[/dim]")
                for workflow in workflow_list:
                    console.print(f"  • {workflow}.md")
            else:
                console.print("[dim]Would create commands in .cursor/commands/[/dim]")
                for workflow in workflow_list:
                    console.print(f"  • {workflow}.md")

        else:
            # Configure workflows (need to implement this in adapter)
            try:
                output_paths = adapter.install_workflows(workflow_list)
                console.print("[green]Workflows configured successfully![/green]")
                console.print("[dim]Configured files:[/dim]")
                for path in output_paths:
                    console.print(f"  • {path}")
            except AttributeError as e:
                console.print(
                    f"[red]Error:[/red] Workflow configuration not yet implemented for {agent_type}"
                )
                console.print(
                    "[yellow]Please use the configure-defaults command for now[/yellow]"
                )
                raise typer.Exit(1) from e

        logger.info("Configure workflows command completed successfully")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        logger.error("Configure workflows command failed", error=str(e))
        raise typer.Exit(1) from e
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        logger.error(
            "Configure workflows command failed with unexpected error", error=str(e)
        )
        raise typer.Exit(1) from e


@app.command()
def configure_mcp(
    agent_type: str = typer.Option(
        ..., help="Type of coding agent (claude-code, cursor)"
    ),
    config: str = typer.Option(..., help="MCP configuration as JSON string"),
    repo_path: str = typer.Option(".", help="Path to target repository"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Preview configuration without applying changes"
    ),
) -> None:
    """Configure Model Context Protocol servers for enhanced capabilities.

    This command sets up MCP servers by writing JSON configuration to the appropriate file:
    - Claude Code: Updates .claude/settings.json
    - Cursor: Creates .cursor/mcp.json

    Examples:
    # Configure GitHub MCP server for Claude Code
    bob configure-mcp --agent-type claude-code --config '{"mcpServers": {"github": {"command": "npx", "args": ["@modelcontextprotocol/server-github"]}}}'

    # Configure multiple servers for Cursor
    bob configure-mcp --agent-type cursor --config '{"servers": {"github": {"url": "https://api.github.com"}}}'

    # Preview configuration with valid JSON
    bob configure-mcp --agent-type claude-code --config '{"mcpServers": {"postgres": {"command": "npx", "args": ["@modelcontextprotocol/server-postgres"]}}}' --dry-run
    """
    logger = get_logger(__name__)

    logger.info(
        "Configure MCP command invoked",
        agent_type=agent_type,
        config_length=len(config),
        repo_path=repo_path,
        dry_run=dry_run,
    )

    try:
        # Validate agent type
        supported_agents = ["claude-code", "cursor"]
        if agent_type not in supported_agents:
            console.print(f"[red]Error:[/red] Unsupported agent type: {agent_type}")
            console.print(f"[dim]Supported types: {', '.join(supported_agents)}[/dim]")
            raise typer.Exit(1)

        # Validate repository path
        repo_path_obj = Path(repo_path).resolve()
        if not repo_path_obj.exists():
            console.print(
                f"[red]Error:[/red] Repository path does not exist: {repo_path}"
            )
            raise typer.Exit(1)

        # Parse and validate JSON configuration
        try:
            mcp_config = json.loads(config)
        except json.JSONDecodeError as e:
            console.print(f"[red]Error:[/red] Invalid JSON configuration: {e}")
            console.print(
                "[dim]Note: Use proper JSON syntax, not {...} placeholders[/dim]"
            )
            console.print("[dim]Example valid JSON:[/dim]")
            if agent_type == "claude-code":
                console.print(
                    '[dim]  \'{"mcpServers": {"postgres": {"command": "npx", "args": ["@modelcontextprotocol/server-postgres"]}}}\'[/dim]'
                )
            else:
                console.print(
                    '[dim]  \'{"servers": {"postgres": {"url": "postgresql://localhost"}}}\'[/dim]'
                )
            raise typer.Exit(1) from e

        console.print(f"[cyan]Configuring MCP servers for {agent_type}...[/cyan]")

        # Determine configuration approach based on agent
        if agent_type == "claude-code":
            config_description = ".claude/settings.json (merged with existing settings)"
        else:  # cursor
            config_description = ".cursor/mcp.json"

        if dry_run:
            console.print("[yellow]Dry-run mode: Preview of MCP configuration[/yellow]")
            console.print(f"[dim]Target agent: {agent_type}[/dim]")
            console.print(f"[dim]Repository: {repo_path_obj}[/dim]")
            console.print(f"[dim]Configuration file: {config_description}[/dim]")

            console.print("\n[bold]Configuration to apply:[/bold]")
            formatted_config = json.dumps(mcp_config, indent=2)
            console.print(
                Panel(
                    formatted_config,
                    title="[bold]MCP Configuration[/bold]",
                    border_style="blue",
                )
            )

            console.print(
                "\n[yellow]This is a preview. Use --no-dry-run to apply the configuration.[/yellow]"
            )
        else:
            # Apply configuration
            if agent_type == "claude-code":
                # For Claude Code, merge with existing settings
                settings_file = repo_path_obj / ".claude" / "settings.json"

                # Load existing settings
                if settings_file.exists():
                    with open(settings_file) as f:
                        existing_settings = json.load(f)
                else:
                    existing_settings = {}
                    # Ensure directory exists
                    settings_file.parent.mkdir(parents=True, exist_ok=True)

                # Merge MCP configuration into existing settings
                existing_settings.update(mcp_config)

                # Write updated settings
                with open(settings_file, "w") as f:
                    json.dump(existing_settings, f, indent=2)

            else:  # cursor
                # Write MCP config to dedicated file
                cursor_dir = repo_path_obj / ".cursor"
                cursor_dir.mkdir(parents=True, exist_ok=True)
                mcp_file = cursor_dir / "mcp.json"

                with open(mcp_file, "w") as f:
                    json.dump(mcp_config, f, indent=2)

            console.print("✓ MCP configuration applied successfully!")

            # Show what was configured
            console.print("\n[bold cyan]Configuration Applied:[/bold cyan]")
            if "mcpServers" in mcp_config:
                servers = list(mcp_config["mcpServers"].keys())
                console.print(f"  • Configured MCP servers: {', '.join(servers)}")
            elif "servers" in mcp_config:
                servers = list(mcp_config["servers"].keys())
                console.print(f"  • Configured MCP servers: {', '.join(servers)}")
            else:
                console.print("  • Custom MCP configuration applied")

        logger.info("Configure MCP command completed successfully")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        logger.error("Configure MCP command failed", error=str(e))
        raise typer.Exit(1) from e
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        logger.error("Configure MCP command failed with unexpected error", error=str(e))
        raise typer.Exit(1) from e


@app.command()
def doctor(
    repair: bool = typer.Option(
        False, "--repair", help="Attempt to repair issues found"
    ),
    repo_path: str = typer.Option(".", help="Path to target repository"),
    agent_type: str = typer.Option(
        None, help="Focus diagnostics on specific agent type (claude-code, cursor)"
    ),
) -> None:
    """Diagnose and optionally repair installation issues.

    This command checks for common configuration problems and can attempt
    automatic repairs where possible.

    Examples:
    bob doctor
    bob doctor --agent-type claude-code --repair
    """
    logger = get_logger(__name__)
    logger.info("Doctor command invoked", repair=repair, agent_type=agent_type)

    try:
        # Validate repository path
        repo_path_obj = Path(repo_path).resolve()
        if not repo_path_obj.exists():
            console.print(
                f"[red]Error:[/red] Repository path does not exist: {repo_path}"
            )
            raise typer.Exit(1)

        # Validate agent type if provided
        if agent_type:
            supported_agents = ["claude-code", "cursor"]
            if agent_type not in supported_agents:
                console.print(f"[red]Error:[/red] Unsupported agent type: {agent_type}")
                console.print(
                    f"[dim]Supported types: {', '.join(supported_agents)}[/dim]"
                )
                raise typer.Exit(1)

        console.print(f"[cyan]Running diagnostics on {repo_path_obj}...[/cyan]")

        issues_found = []
        repairs_made = []

        # Check agent-specific issues
        agents_to_check = [agent_type] if agent_type else ["claude-code", "cursor"]

        for agent in agents_to_check:
            console.print(
                f"\n[bold yellow]Checking {agent} configuration...[/bold yellow]"
            )

            if agent == "claude-code":
                claude_settings = repo_path_obj / ".claude" / "settings.json"
                claude_commands_dir = repo_path_obj / ".claude" / "commands"

                if claude_settings.exists():
                    console.print("  ✓ .claude/settings.json found")
                else:
                    console.print("  ⚠ .claude/settings.json missing")
                    issues_found.append("claude_settings_missing")

                if claude_commands_dir.exists():
                    commands = list(claude_commands_dir.glob("*.md"))
                    console.print(
                        f"  ✓ .claude/commands/ directory found ({len(commands)} commands)"
                    )
                else:
                    console.print("  - .claude/commands/ directory not found")

            else:  # cursor
                cursor_rules_file = repo_path_obj / ".cursorrules"
                cursor_rules_dir = repo_path_obj / ".cursor" / "rules"
                cursor_commands_dir = repo_path_obj / ".cursor" / "commands"

                if cursor_rules_file.exists():
                    console.print("  ✓ .cursorrules file found")
                else:
                    console.print("  ⚠ .cursorrules file missing")
                    issues_found.append("cursor_rules_missing")

                if cursor_rules_dir.exists():
                    rules = list(cursor_rules_dir.glob("*.mdc"))
                    console.print(
                        f"  ✓ .cursor/rules/ directory found ({len(rules)} rule files)"
                    )
                else:
                    console.print("  ⚠ .cursor/rules/ directory missing")

                if cursor_commands_dir.exists():
                    commands = list(cursor_commands_dir.glob("*.md"))
                    console.print(
                        f"  ✓ .cursor/commands/ directory found ({len(commands)} commands)"
                    )
                else:
                    console.print("  - .cursor/commands/ directory not found")

        # Attempt repairs if requested
        if repair and issues_found:
            console.print(
                f"\n[bold green]Attempting to repair {len(issues_found)} issues...[/bold green]"
            )

            for issue in issues_found:
                if issue == "claude_settings_missing":
                    console.print("  Suggested fix:")
                    console.print(
                        "    Suggested fix: Run 'bob configure-defaults --agent-type claude-code --template-type development-team'"
                    )
                    console.print(
                        "    Or choose from: solo-developer, development-team, enterprise-security"
                    )
                    repairs_made.append("claude_rules_suggestion")

                elif issue == "cursor_rules_missing":
                    console.print("  Suggested fix:")
                    console.print(
                        "    Suggested fix: Run 'bob configure-defaults --agent-type cursor --template-type development-team'"
                    )
                    console.print(
                        "    Or choose from: solo-developer, development-team, enterprise-security"
                    )
                    repairs_made.append("cursor_rules_suggestion")

        # Summary
        if not issues_found:
            console.print(
                "\n[bold green]✓ No issues found! Your setup looks good.[/bold green]"
            )
        else:
            console.print(
                f"\n[bold yellow]Found {len(issues_found)} issues[/bold yellow]"
            )
            if repair:
                console.print(
                    f"[dim]Suggested {len(repairs_made)} repair actions[/dim]"
                )
            else:
                console.print("[dim]Run with --repair to see suggested fixes[/dim]")

        logger.info("Doctor command completed successfully")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        logger.error("Doctor command failed", error=str(e))
        raise typer.Exit(1) from e


@app.command()
def init(
    agent_type: str = typer.Option(
        "claude-code", help="Type of coding agent (claude-code, cursor)"
    ),
    target_path: str = typer.Option(".", help="Path to target repository"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without writing"),
    subagents_only: bool = typer.Option(
        False, "--subagents-only", help="Install only subagents"
    ),
    workflows_only: bool = typer.Option(
        False, "--workflows-only", help="Install only workflows"
    ),
    subagent: str | None = typer.Option(None, help="Install specific subagent only"),
    workflow: str | None = typer.Option(None, help="Install specific workflow only"),
) -> None:
    """Initialize bob-the-engineer in your repository.

    This command sets up the necessary files and configurations for your
    chosen coding agent, installing subagents and workflows as specified.

    Examples:
    bob init                                    # Full setup with Claude Code
    bob init --agent-type cursor               # Full setup with Cursor
    bob init --subagents-only                  # Install all subagents only
    bob init --subagent configure-defaults     # Install specific subagent
    bob init --workflows-only --agent-type cursor  # Install workflows for Cursor
    """
    logger = get_logger(__name__)
    logger.info("Init command invoked", agent_type=agent_type, target_path=target_path)

    try:
        # Validate agent type
        supported_agents = ["claude-code", "cursor"]
        if agent_type not in supported_agents:
            console.print(f"[red]Error:[/red] Unsupported agent type: {agent_type}")
            console.print(f"[dim]Supported types: {', '.join(supported_agents)}[/dim]")
            raise typer.Exit(1)

        # Validate repository path
        repo_path_obj = Path(target_path).resolve()
        if not repo_path_obj.exists():
            console.print(
                f"[red]Error:[/red] Repository path does not exist: {target_path}"
            )
            raise typer.Exit(1)

        # Determine what to install
        install_subagents = not workflows_only or subagents_only or subagent
        install_workflows = not subagents_only or workflows_only or workflow

        # Get available items
        templates_dir = Path(__file__).parent.parent / "templates"
        template_engine = TemplateEngine(templates_dir)
        available_subagents = template_engine.list_available_subagents()
        available_workflows = template_engine.list_available_workflows()

        # Filter to specific items if requested
        subagents_to_install = (
            [subagent] if subagent else available_subagents if install_subagents else []
        )
        workflows_to_install = (
            [workflow] if workflow else available_workflows if install_workflows else []
        )

        if dry_run:
            console.print(f"[yellow]Dry run for {agent_type} initialization[/yellow]")
            console.print(f"[dim]Target directory: {repo_path_obj}[/dim]")

            if subagents_to_install:
                console.print(
                    f"[green]Subagents to install ({len(subagents_to_install)}):[/green]"
                )
                for sub in subagents_to_install:
                    console.print(f"  [dim]→[/dim] {sub}")

            if workflows_to_install:
                console.print(
                    f"[green]Workflows to install ({len(workflows_to_install)}):[/green]"
                )
                for wf in workflows_to_install:
                    console.print(f"  [dim]→[/dim] {wf}")

            console.print("[dim]" + "=" * 80 + "[/dim]")
            console.print(
                "[yellow]Dry run complete. Use without --dry-run to initialize.[/yellow]"
            )
        else:
            # Initialize the coding agent environment
            console.print(f"[cyan]Initializing {agent_type} environment...[/cyan]")

            all_output_paths = []

            # Install subagents
            if subagents_to_install:
                console.print(
                    f"[cyan]Installing {len(subagents_to_install)} subagents for {agent_type}...[/cyan]"
                )
                for subagent_name in subagents_to_install:
                    try:
                        output_paths = template_engine.generate_subagent_rules(
                            subagent_name, agent_type, repo_path_obj
                        )
                        all_output_paths.extend(output_paths)
                        console.print(f"  [green]✓[/green] {subagent_name}")
                    except Exception as e:
                        console.print(f"  [red]✗[/red] {subagent_name}: {e}")

            # Install workflows
            if workflows_to_install:
                console.print(
                    f"[cyan]Installing {len(workflows_to_install)} workflows for {agent_type}...[/cyan]"
                )
                for workflow_name in workflows_to_install:
                    try:
                        output_paths = template_engine.install_coding_workflows(
                            [workflow_name], agent_type, repo_path_obj
                        )
                        all_output_paths.extend(output_paths)
                        console.print(f"  [green]✓[/green] {workflow_name}")
                    except Exception as e:
                        console.print(f"  [red]✗[/red] {workflow_name}: {e}")

            # Success summary
            if all_output_paths:
                console.print(
                    f"\n[green]✓ Successfully initialized {agent_type} environment![/green]"
                )
                console.print(f"[dim]Created {len(all_output_paths)} files:[/dim]")
                for path in all_output_paths:
                    rel_path = (
                        path.relative_to(repo_path_obj)
                        if path.is_relative_to(repo_path_obj)
                        else path
                    )
                    console.print(f"  [dim]→[/dim] {rel_path}")
            else:
                console.print("[yellow]No files were created.[/yellow]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        logger.error("Init command failed", error=str(e))
        raise typer.Exit(1) from e


if __name__ == "__main__":
    app()
