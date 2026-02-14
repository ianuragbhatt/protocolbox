"""pb_scrape — Token-efficient web page scraper."""

import re

import html2text
import httpx

from protocolbox.server import mcp
from protocolbox.tools.utils import DEFAULT_TIMEOUT, DEFAULT_USER_AGENT


@mcp.tool()
def scrape(url: str) -> str:
    """Fetch a web page and return its content as clean Markdown.

    Strips scripts, styles, and footers for token-efficient reading.

    Args:
        url: The URL of the web page to scrape.

    Returns:
        The page content as Markdown, or an error message.
    """
    try:
        response = httpx.get(
            url,
            timeout=DEFAULT_TIMEOUT,
            headers={"User-Agent": DEFAULT_USER_AGENT},
            follow_redirects=True,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        return f"Error: Unable to access page. HTTP {e.response.status_code}."
    except httpx.RequestError as e:
        return f"Error: Unable to access page. {type(e).__name__}: {e}"

    html = response.text

    # Strip <script>, <style>, and <footer> tags and their contents.
    html = re.sub(
        r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE
    )
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(
        r"<footer[^>]*>.*?</footer>", "", html, flags=re.DOTALL | re.IGNORECASE
    )

    # Convert to Markdown.
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = True
    converter.body_width = 0  # No line wrapping

    markdown = converter.handle(html)

    # Clean up excessive blank lines.
    markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip()

    return markdown
