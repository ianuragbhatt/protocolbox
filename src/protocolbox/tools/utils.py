"""Shared utilities for ProtocolBox tools."""

import httpx

# Standard timeout for HTTP requests (seconds).
DEFAULT_TIMEOUT = 10.0

# Generic User-Agent to avoid bot detection.
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (compatible; ProtocolBox/0.1; +https://protocolbox.in)"
)


def get_http_client(**kwargs: object) -> httpx.Client:
    """Create a pre-configured httpx Client.

    Uses standard timeout and User-Agent defaults.
    Additional kwargs are passed through to httpx.Client.
    """
    headers = {"User-Agent": DEFAULT_USER_AGENT}
    return httpx.Client(
        timeout=DEFAULT_TIMEOUT,
        headers=headers,
        follow_redirects=True,
        **kwargs,  # type: ignore[arg-type]
    )
