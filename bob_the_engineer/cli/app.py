"""Main CLI application for bob-the-engineer."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from bob_the_engineer import __version__
from bob_the_engineer.adapters.factory import AdapterFactory
from bob_the_engineer.adapters.template_engine import TemplateEngine
from bob_the_engineer.config_templates import (
    generate_config_content,
    get_template,
    list_templates,
)
from bob_the_engineer.logging_config import get_logger, setup_cli_logging

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
        logger.info("Git repository found", path=str(git_dir.absolute()))
    else:
        table.add_row("Git Repository", "✗ Not found", "Not a git repository")
        logger.warning("Git repository not found")

    # Configuration files check
    config_files = [
        ("pyproject.toml", "Python project config"),
        (".pre-commit-config.yaml", "Pre-commit hooks"),
        ("README.md", "Project documentation"),
    ]

    for filename, description in config_files:
        file_path = Path(filename)
        if file_path.exists():
            table.add_row(filename, "✓ Found", description)
            logger.info("Configuration file found", file=filename)
        else:
            table.add_row(filename, "✗ Missing", description)
            logger.warning("Configuration file missing", file=filename)

    console.print(table)
    logger.info("Status command completed")


@app.command()
def configure_defaults(
    agent_type: str = typer.Option(
        ..., help="Type of coding agent (claude-code, cursor)"
    ),
    repo_path: str = typer.Option(".", help="Path to target repository"),
    template_type: str = typer.Option(
        None,
        help="Configuration template to use (run with --help to see available templates)",
    ),
    auto_detect: bool = typer.Option(
        True,
        "--auto-detect/--no-auto-detect",
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

    This command analyzes your repository and applies optimal configuration settings
    for your coding agent based on your project characteristics and team size.

        Available Templates:

    • solo-developer: Streamlined for individual developers and rapid prototyping
    • development-team: Optimized for 2-5 developers with CI/CD and code review
    • enterprise-security: High-security for large teams and regulated environments

    Examples:

    # List all available templates with details
    bob configure-defaults --list

    # Auto-detect and apply best template
    bob configure-defaults --agent-type cursor --repo-path .

    # Use specific template
    bob configure-defaults --agent-type claude-code --template-type development-team

    # Preview configuration without applying
    bob configure-defaults --agent-type cursor --template-type solo-developer --dry-run
    """
    logger = get_logger(__name__)

    logger.info(
        "Configure defaults command invoked",
        agent_type=agent_type,
        repo_path=repo_path,
        template_type=template_type,
        auto_detect=auto_detect,
        dry_run=dry_run,
    )

    try:
        # Validate agent type
        supported_agents = ["claude-code", "cursor"]
        if agent_type not in supported_agents:
            console.print(f"[red]Error:[/red] Unsupported agent type: {agent_type}")
            console.print(f"[dim]Supported types: {', '.join(supported_agents)}[/dim]")
            raise typer.Exit(1)

        # List templates if requested
        if list_templates:
            _display_template_details()
            return

        # Validate repository path
        repo_path_obj = Path(repo_path).resolve()
        if not repo_path_obj.exists():
            console.print(
                f"[red]Error:[/red] Repository path does not exist: {repo_path}"
            )
            raise typer.Exit(1)

        console.print(f"[cyan]Analyzing repository: {repo_path_obj}[/cyan]")

        # TODO: Repository analysis functionality needs to be restored
        # For now, use simple template selection
        console.print(
            "[yellow]Note: Automatic repository analysis temporarily unavailable.[/yellow]"
        )
        console.print("[dim]Please specify --template-type explicitly[/dim]")

        if not template_type:
            console.print(
                "[red]Error:[/red] Repository analysis unavailable. Please specify --template-type"
            )
            console.print(
                "Available options: solo-developer, development-team, enterprise-security"
            )
            raise typer.Exit(1)

        # Create a minimal analysis object for compatibility
        class SimpleAnalysis:
            def __init__(self) -> None:
                self.tech_stack = {"python"}  # Default assumption
                self.team_size = 1
                self.repo_size = 100
                self.security_level = "medium"
                self.has_ci_cd = False
                self.has_containers = False
                self.has_microservices = False
                self.package_managers: list[str] = []
                self.frameworks: list[str] = []
                self.recommended_template = "development-team"
                self.confidence = 0.5

        analysis = SimpleAnalysis()

        # Display analysis results
        _display_analysis_results(analysis)

        # Determine template to use
        if template_type:
            # Use specified template
            try:
                template = get_template(template_type)
                console.print(
                    f"[green]Using specified template: {template.name}[/green]"
                )
            except ValueError as e:
                console.print(f"[red]Error:[/red] {e}")
                _display_template_details()
                raise typer.Exit(1) from e
        elif auto_detect:
            # Auto-detection is temporarily unavailable
            console.print(
                "[red]Error:[/red] Auto-detection requires --template-type when analysis is unavailable"
            )
            console.print(
                "Available options: solo-developer, development-team, enterprise-security"
            )
            raise typer.Exit(1)
        else:
            console.print(
                "[red]Error:[/red] Either specify --template-type or enable --auto-detect"
            )
            raise typer.Exit(1)

        # Generate configuration
        config_content = generate_config_content(template, agent_type)

        if dry_run:
            # Preview mode
            _display_config_preview(template, agent_type, config_content, analysis)
        else:
            # Apply configuration
            _apply_configuration(
                template, agent_type, config_content, repo_path_obj, analysis
            )

        logger.info("Configure defaults command completed successfully")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        logger.error("Configure defaults command failed", error=str(e))
        raise typer.Exit(1) from e
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        logger.error(
            "Configure defaults command failed with unexpected error", error=str(e)
        )
        raise typer.Exit(1) from e


def _display_template_details() -> None:
    """Display detailed information about all available templates."""
    templates = list_templates()

    console.print("\n[bold cyan]Available Configuration Templates[/bold cyan]")
    console.print("=" * 60)

    for template in templates:
        # Create template panel
        content = Text()
        content.append("Best for: ", style="bold")
        content.append(f"{template.best_for}\n\n", style="dim")
        content.append("Description: ", style="bold")
        content.append(f"{template.description}\n\n", style="dim")

        # Add key features
        content.append("Key Features:\n", style="bold")
        if template.name == "solo-developer":
            features = [
                "• Fast code-first mode",
                "• Minimal confirmations",
                "• Auto-formatting",
                "• Quick dependency installation",
                "• Optimized for speed",
            ]
        elif template.name == "development-team":
            features = [
                "• Plan-first approach",
                "• Code quality checks",
                "• Team collaboration",
                "• Git commit templates",
                "• Test automation",
            ]
        elif template.name == "enterprise-security":
            features = [
                "• Maximum security",
                "• Audit logging",
                "• Restricted permissions",
                "• Compliance checks",
                "• Approval workflows",
            ]
        else:
            features = ["• General purpose configuration"]

        for feature in features:
            content.append(f"{feature}\n", style="green")

        panel = Panel(
            content,
            title=f"[bold yellow]{template.name}[/bold yellow]",
            border_style="blue",
            expand=False,
        )
        console.print(panel)
        console.print()  # Add spacing


def _display_analysis_results(analysis: Any) -> None:
    """Display repository analysis results."""
    console.print("\n[bold cyan]Repository Analysis Results[/bold cyan]")

    # Create analysis table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Characteristic", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Impact", style="dim")

    table.add_row(
        "Technology Stack",
        ", ".join(analysis.tech_stack) if analysis.tech_stack else "Mixed/Unknown",
        "Determines tool permissions and commands",
    )

    table.add_row(
        "Team Size",
        str(analysis.team_size),
        "Influences collaboration features and approval workflows",
    )

    table.add_row(
        "Repository Size",
        f"{analysis.repo_size} code files",
        "Affects timeout settings and operation modes",
    )

    table.add_row(
        "Security Level",
        analysis.security_level.title(),
        "Determines permission restrictions and audit requirements",
    )

    table.add_row(
        "CI/CD Present",
        "Yes" if analysis.has_ci_cd else "No",
        "Enables integration with automated workflows",
    )

    table.add_row(
        "Containers",
        "Yes" if analysis.has_containers else "No",
        "Adds container-specific commands and integrations",
    )

    console.print(table)

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

    # Show what files would be created/modified
    if agent_type == "claude-code":
        files_to_modify = [".claude-code-config.json"]
    else:  # cursor
        files_to_modify = [".cursorrules"]

    console.print("[bold]Files that would be created/modified:[/bold]")
    for file_path in files_to_modify:
        console.print(f"  • {file_path}")

    console.print("\n[bold]Configuration Content Preview:[/bold]")

    # Limit preview to first 30 lines to avoid overwhelming output
    lines = config_content.split("\n")
    preview_lines = lines[:30]
    if len(lines) > 30:
        preview_lines.append("... (truncated)")

    preview_content = "\n".join(preview_lines)

    panel = Panel(
        preview_content,
        title=f"[bold]{files_to_modify[0]}[/bold]",
        border_style="yellow",
        expand=False,
    )
    console.print(panel)

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

        else:  # cursor
            config_file = repo_path / ".cursorrules"
            config_file.write_text(config_content)
            console.print(f"[green]✓[/green] Created {config_file}")

        # Create documentation file
        doc_content = f"""# Coding Agent Configuration Applied

## Template: {template.name}
**Applied:** {datetime.now().isoformat()}
**Agent Type:** {agent_type}

## Template Description
{template.description}

## Best For
{template.best_for}

## Repository Analysis
- **Technology Stack:** {", ".join(analysis.tech_stack) if analysis.tech_stack else "Mixed/Unknown"}
- **Team Size:** {analysis.team_size}
- **Repository Size:** {analysis.repo_size} code files
- **Security Level:** {analysis.security_level.title()}
- **CI/CD:** {"Yes" if analysis.has_ci_cd else "No"}
- **Containers:** {"Yes" if analysis.has_containers else "No"}

## Recommendation Confidence
{analysis.confidence:.1%}

## Usage Guidelines
Refer to the {agent_type} documentation for how to use these configuration settings.

## Next Steps
1. Test the configuration with a simple coding task
2. Adjust settings based on your team's feedback
3. Consider running `bob configure-defaults --list` to explore other templates

Generated by bob-the-engineer configure-defaults
"""

        doc_file = repo_path / f"AGENT_CONFIG_{agent_type.upper()}.md"
        doc_file.write_text(doc_content)
        console.print(f"[green]✓[/green] Created {doc_file}")

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

    Available workflows:
    • spec-driven: 6-phase iterative development
    • tdd: Test-first development with enforcement
    • code-review: Multi-aspect parallel review
    • research: Parallel information gathering
    • triage: Context gathering and problem diagnosis

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
        supported_agents = AdapterFactory.get_supported_agents()
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

        # Parse workflows list
        workflow_list = [w.strip() for w in workflows.split(",") if w.strip()]

        # Validate workflow names
        available_workflows = [
            "spec-driven",
            "tdd",
            "code-review",
            "research",
            "triage",
        ]
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
        adapter = AdapterFactory.create_adapter(agent_type, repo_path_obj)

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
                console.print("[dim]Files that would be created:[/dim]")
                for workflow in workflow_list:
                    console.print(f"  • .claude/commands/{workflow}.md")
            else:  # cursor
                console.print("[dim]Files that would be created:[/dim]")
                for workflow in workflow_list:
                    console.print(f"  • .cursor/commands/{workflow}.md")
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
    • For claude-code: Updates .claude/settings.json (merged with existing settings)
    • For cursor: Creates/updates .cursor/mcp.json

    Examples:
    # Configure GitHub MCP server for Claude Code
    bob configure-mcp --agent-type claude-code --config '{"mcpServers": {"github": {"command": "npx", "args": ["@modelcontextprotocol/server-github"]}}}'

    # Configure multiple servers for Cursor
    bob configure-mcp --agent-type cursor --config '{"servers": {"github": {...}, "postgres": {...}}}'

    # Preview configuration
    bob configure-mcp --agent-type claude-code --config '{"mcpServers": {...}}' --dry-run
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
        supported_agents = AdapterFactory.get_supported_agents()
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
            raise typer.Exit(1) from e

        console.print(f"[cyan]Configuring MCP servers for {agent_type}...[/cyan]")

        # Determine target file based on agent type
        if agent_type == "claude-code":
            target_file = repo_path_obj / ".claude" / "settings.json"
            config_description = ".claude/settings.json (merged with existing settings)"
        else:  # cursor
            target_file = repo_path_obj / ".cursor" / "mcp.json"
            config_description = ".cursor/mcp.json"

        if dry_run:
            console.print("[yellow]Dry-run mode: Preview of MCP configuration[/yellow]")
            console.print(f"[dim]Target agent: {agent_type}[/dim]")
            console.print(f"[dim]Repository: {repo_path_obj}[/dim]")
            console.print(f"[dim]Configuration file: {config_description}[/dim]")

            console.print("\n[bold]Configuration to apply:[/bold]")
            formatted_config = json.dumps(mcp_config, indent=2)
            panel = Panel(
                formatted_config,
                title="[bold]MCP Configuration[/bold]",
                border_style="yellow",
                expand=False,
            )
            console.print(panel)

            console.print(
                "\n[yellow]This is a preview. Use --no-dry-run to apply the configuration.[/yellow]"
            )
        else:
            # Apply configuration
            if agent_type == "claude-code":
                # Merge with existing settings
                claude_dir = repo_path_obj / ".claude"
                claude_dir.mkdir(parents=True, exist_ok=True)

                if target_file.exists():
                    try:
                        with open(target_file, encoding="utf-8") as f:
                            existing_settings = json.load(f)
                    except (json.JSONDecodeError, FileNotFoundError):
                        existing_settings = {}
                else:
                    existing_settings = {}

                # Merge MCP configuration into existing settings
                existing_settings.update(mcp_config)

                with open(target_file, "w", encoding="utf-8") as f:
                    json.dump(existing_settings, f, indent=2)

            else:  # cursor
                # Write MCP config to dedicated file
                cursor_dir = repo_path_obj / ".cursor"
                cursor_dir.mkdir(parents=True, exist_ok=True)

                with open(target_file, "w", encoding="utf-8") as f:
                    json.dump(mcp_config, f, indent=2)

            console.print("[green]✓ MCP configuration applied successfully![/green]")
            console.print(f"[dim]Updated: {target_file}[/dim]")

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
def configure_supervisor(
    guards: str = typer.Option(
        ...,
        help="Guards to configure (comma-separated: file-guard,tdd-guard,self-review)",
    ),
    repo_path: str = typer.Option(".", help="Path to target repository"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Preview installation without applying changes"
    ),
) -> None:
    """Configure coding agent supervisor guards and hooks (Claude Code only).

    This command sets up guards and hooks to prevent common AI coding mistakes.

    Available guards:
    • file-guard: Protects sensitive files from AI access
    • tdd-guard: Enforces test-first development
    • self-review: Catches implementation shortcuts

    Examples:
    bob install-supervisor --guards file-guard,tdd-guard
    bob install-supervisor --guards self-review --dry-run
    """
    logger = get_logger(__name__)

    logger.info(
        "Install supervisor command invoked",
        guards=guards,
        repo_path=repo_path,
        dry_run=dry_run,
    )

    try:
        # This command only works with Claude Code
        agent_type = "claude-code"

        # Validate repository path
        repo_path_obj = Path(repo_path).resolve()
        if not repo_path_obj.exists():
            console.print(
                f"[red]Error:[/red] Repository path does not exist: {repo_path}"
            )
            raise typer.Exit(1)

        # Parse guards list
        guard_list = [g.strip() for g in guards.split(",") if g.strip()]

        # Validate guard names
        available_guards = ["file-guard", "tdd-guard", "self-review"]
        invalid_guards = [g for g in guard_list if g not in available_guards]
        if invalid_guards:
            console.print(
                f"[red]Error:[/red] Invalid guards: {', '.join(invalid_guards)}"
            )
            console.print(f"[dim]Available guards: {', '.join(available_guards)}[/dim]")
            raise typer.Exit(1)

        console.print("[cyan]Configuring supervisor guards for Claude Code...[/cyan]")

        # Create adapter and install supervisor
        adapter = AdapterFactory.create_adapter(agent_type, repo_path_obj)

        if dry_run:
            console.print(
                "[yellow]Dry-run mode: Preview of supervisor configuration[/yellow]"
            )
            console.print(f"[dim]Repository: {repo_path_obj}[/dim]")
            console.print(f"[dim]Guards to configure: {', '.join(guard_list)}[/dim]")
            console.print("[dim]Configuration file to update:[/dim]")
            console.print("  • .claude/settings.json (hooks section)")
        else:
            # Configure supervisor (need to implement this in adapter)
            try:
                config_path = adapter.install_supervisor(guard_list)
                console.print(
                    "[green]Supervisor guards configured successfully![/green]"
                )
                console.print(f"[dim]Configuration updated: {config_path}[/dim]")

                console.print("\n[bold cyan]Usage:[/bold cyan]")
                console.print(
                    "Guards work automatically and are disabled in plan/ask mode."
                )
                console.print("To temporarily disable:")
                console.print("  export BOB_TDD_ENABLED=false  # Disable TDD guard")
                console.print("  export BOB_GUARDS_ENABLED=false  # Disable all guards")

            except AttributeError as e:
                console.print(
                    "[red]Error:[/red] Supervisor configuration not yet implemented"
                )
                raise typer.Exit(1) from e

        logger.info("Configure supervisor command completed successfully")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        logger.error("Configure supervisor command failed", error=str(e))
        raise typer.Exit(1) from e
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        logger.error(
            "Configure supervisor command failed with unexpected error", error=str(e)
        )
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

    This command checks for common installation problems and can attempt repairs.

    Diagnostics include:
    • File permissions and directory structure
    • Configuration file validity
    • Agent-specific setup verification
    • Template installation completeness

    Examples:
    bob doctor --repo-path .
    bob doctor --repair --agent-type claude-code
    """
    logger = get_logger(__name__)

    logger.info(
        "Doctor command invoked",
        repair=repair,
        repo_path=repo_path,
        agent_type=agent_type,
    )

    try:
        # Validate repository path
        repo_path_obj = Path(repo_path).resolve()
        if not repo_path_obj.exists():
            console.print(
                f"[red]Error:[/red] Repository path does not exist: {repo_path}"
            )
            raise typer.Exit(1)

        # If agent_type specified, validate it
        if agent_type:
            supported_agents = AdapterFactory.get_supported_agents()
            if agent_type not in supported_agents:
                console.print(f"[red]Error:[/red] Unsupported agent type: {agent_type}")
                console.print(
                    f"[dim]Supported types: {', '.join(supported_agents)}[/dim]"
                )
                raise typer.Exit(1)

        console.print(f"[cyan]Running diagnostics on {repo_path_obj}...[/cyan]")

        issues_found = []
        repairs_made = []

        # Basic repository checks
        console.print("\n[bold]Basic Repository Checks[/bold]")

        # Check if it's a git repository
        git_dir = repo_path_obj / ".git"
        if git_dir.exists():
            console.print("  ✓ Git repository detected")
        else:
            console.print("  ⚠ Not a git repository")
            issues_found.append("not_git_repo")

        # Check for common config files
        config_files = [
            ("pyproject.toml", "Python project config"),
            ("package.json", "Node.js project config"),
            ("README.md", "Project documentation"),
        ]

        for filename, description in config_files:
            file_path = repo_path_obj / filename
            if file_path.exists():
                console.print(f"  ✓ {filename} found")
            else:
                console.print(f"  - {filename} not found ({description})")

        # Agent-specific checks
        if not agent_type:
            # Check both agents
            agents_to_check = AdapterFactory.get_supported_agents()
        else:
            agents_to_check = [agent_type]

        for agent in agents_to_check:
            console.print(f"\n[bold]{agent.title()} Agent Checks[/bold]")

            if agent == "claude-code":
                # Check Claude Code setup
                claude_file = repo_path_obj / "CLAUDE.md"
                claude_settings = repo_path_obj / ".claude" / "settings.json"
                claude_commands_dir = repo_path_obj / ".claude" / "commands"

                if claude_file.exists():
                    console.print("  ✓ CLAUDE.md rules file found")
                else:
                    console.print("  ⚠ CLAUDE.md rules file missing")
                    issues_found.append("claude_rules_missing")

                if claude_settings.exists():
                    console.print("  ✓ .claude/settings.json found")
                    # TODO: Validate JSON format
                else:
                    console.print("  - .claude/settings.json not found")

                if claude_commands_dir.exists():
                    commands = list(claude_commands_dir.glob("*.md"))
                    console.print(
                        f"  ✓ .claude/commands/ directory found ({len(commands)} commands)"
                    )
                else:
                    console.print("  - .claude/commands/ directory not found")

            elif agent == "cursor":
                # Check Cursor setup
                cursor_rules_dir = repo_path_obj / ".cursor" / "rules"
                cursor_settings = repo_path_obj / ".cursor" / "settings.json"
                cursor_commands_dir = repo_path_obj / ".cursor" / "commands"

                if cursor_rules_dir.exists():
                    rules = list(cursor_rules_dir.glob("*.mdc"))
                    console.print(
                        f"  ✓ .cursor/rules/ directory found ({len(rules)} rule files)"
                    )
                else:
                    console.print("  ⚠ .cursor/rules/ directory missing")
                    issues_found.append("cursor_rules_missing")

                if cursor_settings.exists():
                    console.print("  ✓ .cursor/settings.json found")
                    # TODO: Validate JSON format
                else:
                    console.print("  - .cursor/settings.json not found")

                if cursor_commands_dir.exists():
                    commands = list(cursor_commands_dir.glob("*.md"))
                    console.print(
                        f"  ✓ .cursor/commands/ directory found ({len(commands)} commands)"
                    )
                else:
                    console.print("  - .cursor/commands/ directory not found")

        # Repair issues if requested
        if repair and issues_found:
            console.print("\n[bold yellow]Repair suggestions...[/bold yellow]")

            for issue in issues_found:
                if issue == "claude_rules_missing":
                    console.print("  Missing CLAUDE.md rules file")
                    console.print(
                        "    Suggested fix: Run 'bob configure-defaults --agent-type claude-code --template-type development-team'"
                    )
                    console.print(
                        "    Or choose from: solo-developer, development-team, enterprise-security"
                    )
                    repairs_made.append("claude_rules_suggestion")

                elif issue == "cursor_rules_missing":
                    console.print("  Missing .cursor/rules/ directory")
                    console.print(
                        "    Suggested fix: Run 'bob configure-defaults --agent-type cursor --template-type development-team'"
                    )
                    console.print(
                        "    Or choose from: solo-developer, development-team, enterprise-security"
                    )
                    repairs_made.append("cursor_rules_suggestion")

        # Summary
        console.print("\n[bold]Summary[/bold]")
        if issues_found:
            console.print(f"  Issues found: {len(issues_found)}")
            if repair:
                console.print(f"  Repair suggestions provided: {len(repairs_made)}")
            else:
                console.print("  Run with --repair to see suggested fixes")
        else:
            console.print("  ✓ No issues found")

        logger.info("Doctor command completed successfully")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        logger.error("Doctor command failed", error=str(e))
        raise typer.Exit(1) from e
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        logger.error("Doctor command failed with unexpected error", error=str(e))
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
    """Initialize coding agent environment with subagents and workflows."""
    logger = get_logger(__name__)

    logger.info(
        "Init command invoked",
        agent_type=agent_type,
        target_path=target_path,
        dry_run=dry_run,
        subagents_only=subagents_only,
        workflows_only=workflows_only,
        subagent=subagent,
        workflow=workflow,
    )

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

        # Initialize template engine
        templates_dir = Path(__file__).parent.parent / "templates"
        template_engine = TemplateEngine(templates_dir)

        # Determine what to install
        install_subagents = not workflows_only
        install_workflows = not subagents_only

        # If specific items are requested, only install those
        if subagent or workflow:
            install_subagents = bool(subagent)
            install_workflows = bool(workflow)

        # Get available subagents and workflows
        available_subagents = [
            "build_test_run",
            "configure_defaults",
            "configure_mcp",
            "configure_rules",
            "configure_supervisor",
            "detect_conflicting_instructions",
            "improve_code_quality_checks",
            "improve_debuggability",
        ]

        available_workflows = ["code-review", "spec-driven", "tdd"]

        # Filter to specific items if requested
        subagents_to_install = (
            [subagent] if subagent else available_subagents if install_subagents else []
        )
        workflows_to_install = (
            [workflow] if workflow else available_workflows if install_workflows else []
        )

        if dry_run:
            # Preview mode
            console.print(f"\n[cyan]Preview initialization for {agent_type}:[/cyan]")
            console.print("[dim]" + "=" * 80 + "[/dim]")

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
                        continue

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
                        continue

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
