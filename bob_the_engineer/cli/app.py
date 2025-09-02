"""Main CLI application for bob-the-engineer."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from bob_the_engineer import __version__
from bob_the_engineer.adapters.factory import AdapterFactory
from bob_the_engineer.adapters.template_engine import TemplateEngine
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
def generate_rules(
    agent_type: str = typer.Option(
        "claude-code", help="Type of coding agent (claude-code, cursor)"
    ),
    target_path: str = typer.Option(".", help="Path to target repository"),
    output: str = typer.Option(None, help="Override output path (optional)"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Preview generated rules without writing files"
    ),
) -> None:
    """Generate coding agent rules for a repository."""
    logger = get_logger(__name__)

    logger.info(
        "Generate rules command invoked",
        agent_type=agent_type,
        target_path=target_path,
        dry_run=dry_run,
    )

    try:
        # Validate agent type
        supported_agents = AdapterFactory.get_supported_agents()
        if agent_type not in supported_agents:
            console.print(f"[red]Error:[/red] Unsupported agent type: {agent_type}")
            console.print(f"[dim]Supported types: {', '.join(supported_agents)}[/dim]")
            raise typer.Exit(1)

        # Validate target path
        target_path_obj = Path(target_path).resolve()
        if not target_path_obj.exists():
            console.print(
                f"[red]Error:[/red] Target path does not exist: {target_path}"
            )
            raise typer.Exit(1)

        # Initialize template engine
        templates_dir = Path(__file__).parent.parent / "templates"
        engine = TemplateEngine(templates_dir)

        console.print(f"[cyan]Generating rules for {agent_type}...[/cyan]")

        if dry_run:
            # Preview mode - just render and display
            rendered_content = engine.render_configure_rules(
                agent_type, target_path_obj
            )
            console.print("\n[yellow]Generated Rules Preview:[/yellow]")
            console.print("[dim]" + "=" * 50 + "[/dim]")
            # Create dedicated console for preview to avoid formatting issues
            preview = (
                rendered_content[:500] + "..."
                if len(rendered_content) > 500
                else rendered_content
            )
            preview_console = Console(width=120, height=50, markup=False)
            preview_console.print(preview)
            console.print("[dim]" + "=" * 50 + "[/dim]")
        else:
            # Generate and write rules
            output_paths = engine.generate_rules(agent_type, target_path_obj)

            console.print("[green]Rules generated successfully![/green]")
            console.print("[dim]Output files:[/dim]")
            for path in output_paths:
                console.print(f"  • {path}")

        logger.info("Generate rules command completed successfully")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        logger.error("Generate rules command failed", error=str(e))
        raise typer.Exit(1) from e
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        logger.error(
            "Generate rules command failed with unexpected error", error=str(e)
        )
        raise typer.Exit(1) from e


if __name__ == "__main__":
    app()
