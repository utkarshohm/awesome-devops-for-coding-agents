"""Logging configuration for bob-the-engineer CLI."""

import logging
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import structlog

if TYPE_CHECKING:
    pass


def configure_logging(
    log_level: str = "INFO",
    log_file: Path | None = None,
    enable_json: bool = False,
) -> None:
    """Configure structured logging for the CLI application.

    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to
        enable_json: Whether to output JSON structured logs
    """

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, log_level.upper()),
        handlers=[],
    )

    # Configure structlog
    processors: list[Any] = [
        # Add timestamp
        structlog.processors.TimeStamper(fmt="ISO"),
        # Add log level
        structlog.stdlib.add_log_level,
        # Add function name and line number in debug mode
        structlog.processors.CallsiteParameterAdder(
            parameters=[structlog.processors.CallsiteParameter.FUNC_NAME]
            if log_level.upper() == "DEBUG"
            else []
        ),
    ]

    if enable_json:
        # JSON output for structured logging
        processors.append(structlog.processors.JSONRenderer())
    else:
        # Human-readable output for CLI
        processors.extend(
            [
                structlog.processors.StackInfoRenderer(),
                structlog.dev.set_exc_info,
                structlog.dev.ConsoleRenderer(
                    colors=sys.stderr.isatty(),  # Only use colors in interactive terminals
                    exception_formatter=structlog.dev.rich_traceback,
                ),
            ]
        )

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper())
        ),
        logger_factory=structlog.stdlib.LoggerFactory(),
        context_class=structlog.threadlocal.wrap_dict(dict),
        cache_logger_on_first_use=True,
    )

    # Set up file logging if requested
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logging.getLogger().addHandler(file_handler)


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a configured logger for the given name."""
    return cast(structlog.BoundLogger, structlog.get_logger(name))


# CLI logging utilities
def setup_cli_logging(verbose: int = 0, log_file: str | None = None) -> None:
    """Set up logging for CLI based on verbosity level.

    Args:
        verbose: Verbosity level (0=WARNING, 1=INFO, 2=DEBUG)
        log_file: Optional log file path
    """
    log_levels = ["WARNING", "INFO", "DEBUG"]
    log_level = log_levels[min(verbose, len(log_levels) - 1)]

    file_path = Path(log_file) if log_file else None

    configure_logging(
        log_level=log_level,
        log_file=file_path,
        enable_json=False,  # CLI prefers human-readable logs
    )
