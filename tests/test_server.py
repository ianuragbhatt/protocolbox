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
        return [
            tool.name
            for tool in mcp._tool_manager.list_tools()
        ]

    def test_scrape_registered(self) -> None:
        assert "scrape" in self._tool_names()

    def test_heal_json_registered(self) -> None:
        assert "heal_json" in self._tool_names()

    def test_generate_invoice_registered(self) -> None:
        assert "generate_invoice" in self._tool_names()

    def test_exactly_three_tools(self) -> None:
        """There should be exactly 3 registered tools."""
        assert len(self._tool_names()) == 3

    def test_no_duplicate_tools(self) -> None:
        """No tool name should appear more than once."""
        names = self._tool_names()
        assert len(names) == len(set(names))


class TestToolDescriptions:
    """Verify tools have non-empty descriptions."""

    def _tools_by_name(self) -> dict:
        return {
            tool.name: tool
            for tool in mcp._tool_manager.list_tools()
        }

    def test_scrape_has_description(self) -> None:
        tools = self._tools_by_name()
        assert tools["scrape"].description
        assert len(tools["scrape"].description) > 10

    def test_heal_json_has_description(self) -> None:
        tools = self._tools_by_name()
        assert tools["heal_json"].description
        assert len(tools["heal_json"].description) > 10

    def test_generate_invoice_has_description(self) -> None:
        tools = self._tools_by_name()
        assert tools["generate_invoice"].description
        assert len(tools["generate_invoice"].description) > 10


class TestPackageImports:
    """Verify package-level imports work correctly."""

    def test_version_available(self) -> None:
        from protocolbox import __version__

        assert __version__ == "0.1.0"

    def test_tools_importable_from_package(self) -> None:
        from protocolbox.tools import (
            generate_invoice,
            heal_json,
            scrape,
        )

        assert callable(scrape)
        assert callable(heal_json)
        assert callable(generate_invoice)

    def test_server_importable(self) -> None:
        from protocolbox.server import main

        assert callable(main)
