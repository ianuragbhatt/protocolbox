"""Tests for the pb_scrape tool."""

from unittest.mock import MagicMock, patch

import httpx

from protocolbox.tools.scraper import scrape


class TestScrape:
    """Test the scrape tool."""

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_scrape_returns_markdown(self, mock_get: MagicMock) -> None:
        """Scraping valid HTML should return clean Markdown."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
        <head><title>Test</title></head>
        <body>
            <h1>Hello World</h1>
            <p>This is a <strong>test</strong> page.</p>
        </body>
        </html>
        """
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = scrape("https://example.com")

        assert "Hello World" in result
        assert "test" in result
        assert "<script>" not in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_scrape_strips_scripts(self, mock_get: MagicMock) -> None:
        """Script tags should be stripped from output."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
        <body>
            <p>Content</p>
            <script>alert('xss')</script>
        </body>
        </html>
        """
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = scrape("https://example.com")

        assert "alert" not in result
        assert "Content" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_scrape_strips_styles(self, mock_get: MagicMock) -> None:
        """Style tags should be stripped from output."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
        <body>
            <style>.hidden { display: none; }</style>
            <p>Visible</p>
        </body>
        </html>
        """
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = scrape("https://example.com")

        assert "display: none" not in result
        assert "Visible" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_scrape_strips_footer(self, mock_get: MagicMock) -> None:
        """Footer tags should be stripped from output."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
        <body>
            <p>Main content</p>
            <footer>Copyright 2026</footer>
        </body>
        </html>
        """
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = scrape("https://example.com")

        assert "Copyright 2026" not in result
        assert "Main content" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_scrape_handles_404(self, mock_get: MagicMock) -> None:
        """A 404 response should return an error message."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found",
            request=MagicMock(),
            response=mock_response,
        )
        mock_get.return_value = mock_response

        result = scrape("https://example.com/404")

        assert "Error" in result
        assert "404" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_scrape_handles_500(self, mock_get: MagicMock) -> None:
        """A 500 response should return an error message."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server Error",
            request=MagicMock(),
            response=mock_response,
        )
        mock_get.return_value = mock_response

        result = scrape("https://example.com/500")

        assert "Error" in result
        assert "500" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_scrape_handles_connection_error(self, mock_get: MagicMock) -> None:
        """A connection error should return an error message."""
        mock_get.side_effect = httpx.ConnectError("Connection refused")

        result = scrape("https://unreachable.example.com")

        assert "Error" in result
