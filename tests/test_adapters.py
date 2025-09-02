"""Tests for the adapter template system."""


import pytest

from bob_the_engineer.adapters.claude.rules_manager import ClaudeRulesManager
from bob_the_engineer.adapters.cursor.rules_manager import CursorRulesManager
from bob_the_engineer.adapters.factory import AdapterFactory


class TestAdapterFactory:
    """Test adapter factory functionality."""

    def test_get_supported_agents(self):
        """Test that factory returns correct supported agents."""
        supported = AdapterFactory.get_supported_agents()
        assert "claude-code" in supported
        assert "cursor" in supported

    def test_create_claude_adapter(self, tmp_path):
        """Test creating Claude Code adapter."""
        adapter = AdapterFactory.create_adapter("claude-code", tmp_path)
        assert isinstance(adapter, ClaudeRulesManager)
        assert adapter.agent_name == "claude-code"
        assert adapter.output_format == "single_file"

    def test_create_cursor_adapter(self, tmp_path):
        """Test creating Cursor adapter."""
        adapter = AdapterFactory.create_adapter("cursor", tmp_path)
        assert isinstance(adapter, CursorRulesManager)
        assert adapter.agent_name == "cursor"
        assert adapter.output_format == "multiple_files"

    def test_unsupported_agent_type(self, tmp_path):
        """Test error handling for unsupported agent type."""
        with pytest.raises(ValueError, match="Unsupported agent type"):
            AdapterFactory.create_adapter("unknown-agent", tmp_path)


class TestClaudeRulesManager:
    """Test Claude Code rules manager."""

    def test_output_paths(self, tmp_path):
        """Test Claude adapter output paths."""
        adapter = ClaudeRulesManager(tmp_path)
        paths = adapter.get_output_paths()
        assert len(paths) == 1
        assert paths[0] == tmp_path / "CLAUDE.md"

    def test_template_variables(self, tmp_path):
        """Test Claude adapter template variables."""
        config = {"test_key": "test_value"}
        adapter = ClaudeRulesManager(tmp_path, config)
        variables = adapter.get_template_variables()
        assert variables["agent_type"] == "claude-code"
        assert variables["output_file"] == "CLAUDE.md"
        assert variables["test_key"] == "test_value"

    def test_write_rules(self, tmp_path):
        """Test writing rules to CLAUDE.md."""
        adapter = ClaudeRulesManager(tmp_path)
        test_content = "# Test Rules\nThis is a test."

        adapter.write_rules(test_content)

        output_file = tmp_path / "CLAUDE.md"
        assert output_file.exists()
        assert output_file.read_text() == test_content


class TestCursorRulesManager:
    """Test Cursor rules manager."""

    def test_output_paths(self, tmp_path):
        """Test Cursor adapter output paths."""
        adapter = CursorRulesManager(tmp_path)
        paths = adapter.get_output_paths()
        assert len(paths) == 4
        assert any("development-workflow.mdc" in str(p) for p in paths)

    def test_write_rules_creates_directory(self, tmp_path):
        """Test that writing rules creates .cursor/rules directory."""
        adapter = CursorRulesManager(tmp_path)
        test_content = "# Test Rules\nThis is a test."

        adapter.write_rules(test_content)

        cursor_rules_dir = tmp_path / ".cursor" / "rules"
        assert cursor_rules_dir.exists()
        assert (cursor_rules_dir / "coding-agent-rules.mdc").exists()
