"""pb_web_search — Privacy-focused web search via DuckDuckGo."""

from duckduckgo_search import DDGS

from protocolbox.server import mcp


@mcp.tool()
def web_search(query: str, max_results: int = 3) -> str:
    """Search the web using DuckDuckGo and return formatted results.

    Allows an Agent to query the live web for up-to-date information
    without tracking or ads.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return (default 3).

    Returns:
        A Markdown-formatted string of search results, or an error message.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return f"No results found for: {query}"

        lines: list[str] = [f"## Search Results for: {query}\n"]
        for i, r in enumerate(results, 1):
            title = r.get("title", "No title")
            link = r.get("href", "")
            snippet = r.get("body", "No description available.")
            lines.append(f"### {i}. {title}")
            lines.append(f"**Link:** {link}")
            lines.append(f"{snippet}\n")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: Web search failed. {type(e).__name__}: {e}"
