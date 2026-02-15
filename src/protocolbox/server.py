"""ProtocolBox MCP Server — the engine that exposes all tools."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ProtocolBox")

# Import tools so they register with the MCP server.
# Each tool module uses the `mcp` instance via import.
import protocolbox.tools.json_healer  # noqa: F401, E402
import protocolbox.tools.math_utils  # noqa: F401, E402
import protocolbox.tools.memory  # noqa: F401, E402
import protocolbox.tools.scraper  # noqa: F401, E402
import protocolbox.tools.search  # noqa: F401, E402
import protocolbox.tools.time_utils  # noqa: F401, E402
import protocolbox.tools.youtube  # noqa: F401, E402


def main() -> None:
    """Run the ProtocolBox MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
