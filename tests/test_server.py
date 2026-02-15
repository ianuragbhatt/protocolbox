"""Tests for the ProtocolBox MCP server — comprehensive coverage."""

from protocolbox.server import mcp


class TestServerInit:
    """Test that the MCP server initializes correctly."""

    def test_server_instance_exists(self) -> None:
        """The MCP server instance should be created."""
        assert mcp is not None

    def test_server_name(self) -> None:
        """The server should be named 'ProtocolBox'."""
        assert mcp.name == "ProtocolBox"


class TestToolRegistration:
    """Verify all tools are properly registered."""

    def _tool_names(self) -> list[str]:
        return [tool.name for tool in mcp._tool_manager.list_tools()]

    def test_scrape_registered(self) -> None:
        assert "scrape" in self._tool_names()

    def test_heal_json_registered(self) -> None:
        assert "heal_json" in self._tool_names()

    def test_web_search_registered(self) -> None:
        assert "web_search" in self._tool_names()

    def test_safe_math_registered(self) -> None:
        assert "safe_math" in self._tool_names()

    def test_get_time_registered(self) -> None:
        assert "get_time" in self._tool_names()

    def test_get_transcript_registered(self) -> None:
        assert "get_transcript" in self._tool_names()

    def test_remember_registered(self) -> None:
        assert "remember" in self._tool_names()

    def test_recall_registered(self) -> None:
        assert "recall" in self._tool_names()

    def test_exactly_eight_tools(self) -> None:
        """There should be exactly 8 registered tools."""
        assert len(self._tool_names()) == 8

    def test_no_duplicate_tools(self) -> None:
        """No tool name should appear more than once."""
        names = self._tool_names()
        assert len(names) == len(set(names))


class TestToolDescriptions:
    """Verify tools have non-empty descriptions."""

    def _tools_by_name(self) -> dict:
        return {tool.name: tool for tool in mcp._tool_manager.list_tools()}

    def test_scrape_has_description(self) -> None:
        tools = self._tools_by_name()
        assert tools["scrape"].description
        assert len(tools["scrape"].description) > 10

    def test_heal_json_has_description(self) -> None:
        tools = self._tools_by_name()
        assert tools["heal_json"].description
        assert len(tools["heal_json"].description) > 10

    def test_web_search_has_description(self) -> None:
        tools = self._tools_by_name()
        assert tools["web_search"].description
        assert len(tools["web_search"].description) > 10

    def test_safe_math_has_description(self) -> None:
        tools = self._tools_by_name()
        assert tools["safe_math"].description
        assert len(tools["safe_math"].description) > 10

    def test_get_time_has_description(self) -> None:
        tools = self._tools_by_name()
        assert tools["get_time"].description
        assert len(tools["get_time"].description) > 10

    def test_get_transcript_has_description(self) -> None:
        tools = self._tools_by_name()
        assert tools["get_transcript"].description
        assert len(tools["get_transcript"].description) > 10

    def test_remember_has_description(self) -> None:
        tools = self._tools_by_name()
        assert tools["remember"].description
        assert len(tools["remember"].description) > 10

    def test_recall_has_description(self) -> None:
        tools = self._tools_by_name()
        assert tools["recall"].description
        assert len(tools["recall"].description) > 10


class TestPackageImports:
    """Verify package-level imports work correctly."""

    def test_version_available(self) -> None:
        from protocolbox import __version__

        assert __version__ == "0.1.4"

    def test_tools_importable_from_package(self) -> None:
        from protocolbox.tools import (
            get_time,
            get_transcript,
            heal_json,
            recall,
            remember,
            safe_math,
            scrape,
            web_search,
        )

        assert callable(scrape)
        assert callable(heal_json)
        assert callable(web_search)
        assert callable(safe_math)
        assert callable(get_time)
        assert callable(get_transcript)
        assert callable(remember)
        assert callable(recall)

    def test_server_importable(self) -> None:
        from protocolbox.server import main

        assert callable(main)
