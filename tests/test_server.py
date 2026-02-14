"""Tests for the ProtocolBox MCP server."""

from protocolbox.server import mcp


class TestServerInit:
    """Test that the MCP server initializes correctly."""

    def test_server_instance_exists(self) -> None:
        """The MCP server instance should be created."""
        assert mcp is not None

    def test_server_name(self) -> None:
        """The server should be named 'ProtocolBox'."""
        assert mcp.name == "ProtocolBox"

    def test_tools_are_registered(self) -> None:
        """All three hero tools should be registered."""
        tool_names = [tool.name for tool in mcp._tool_manager.list_tools()]
        assert "scrape" in tool_names
        assert "heal_json" in tool_names
        assert "generate_invoice" in tool_names
