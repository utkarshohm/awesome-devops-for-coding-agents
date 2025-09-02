"""Factory for creating coding agent adapters."""

from pathlib import Path
from typing import Any, ClassVar

from .base import BaseAdapter
from .claude.rules_manager import ClaudeRulesManager
from .cursor.rules_manager import CursorRulesManager


class AdapterFactory:
    """Factory for creating appropriate adapters based on coding agent type."""

    _adapters: ClassVar[dict[str, type[BaseAdapter]]] = {
        "claude-code": ClaudeRulesManager,
        "cursor": CursorRulesManager,
    }

    @classmethod
    def create_adapter(
        self,
        agent_type: str,
        target_path: Path,
        config: dict[str, Any] | None = None,
    ) -> BaseAdapter:
        """Create an adapter for the specified coding agent.

        Args:
            agent_type: Type of coding agent ('claude-code' or 'cursor')
            target_path: Path to the target repository
            config: Optional configuration for the adapter

        Returns:
            Appropriate adapter instance

        Raises:
            ValueError: If agent_type is not supported
        """
        if agent_type not in self._adapters:
            supported = list(self._adapters.keys())
            raise ValueError(
                f"Unsupported agent type: {agent_type}. Supported: {supported}"
            )

        adapter_class = self._adapters[agent_type]
        return adapter_class(target_path, config)

    @classmethod
    def get_supported_agents(self) -> list[str]:
        """Return list of supported coding agent types.

        Returns:
            List of supported agent type strings
        """
        return list(self._adapters.keys())
