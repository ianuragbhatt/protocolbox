"""Tests for the pb_scrape tool — comprehensive edge-case coverage."""

from unittest.mock import MagicMock, patch

import httpx

from protocolbox.tools.scraper import scrape


def _mock_response(
    text: str, status_code: int = 200
) -> MagicMock:
    """Helper to build a mock httpx response."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = text
    resp.raise_for_status = MagicMock()
    return resp


class TestScrapeBasic:
    """Basic happy-path scraping tests."""

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_returns_markdown(self, mock_get: MagicMock) -> None:
        """Valid HTML should return clean Markdown."""
        mock_get.return_value = _mock_response(
            "<html><body><h1>Hello</h1>"
            "<p>This is a <strong>test</strong>.</p></body></html>"
        )
        result = scrape("https://example.com")
        assert "Hello" in result
        assert "test" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_preserves_links(self, mock_get: MagicMock) -> None:
        """Links should be preserved in Markdown output."""
        mock_get.return_value = _mock_response(
            '<html><body><a href="https://x.com">Link</a>'
            "</body></html>"
        )
        result = scrape("https://example.com")
        assert "Link" in result
        assert "https://x.com" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_preserves_headings_hierarchy(
        self, mock_get: MagicMock
    ) -> None:
        """Multiple heading levels should be preserved."""
        mock_get.return_value = _mock_response(
            "<html><body>"
            "<h1>Title</h1><h2>Subtitle</h2><h3>Section</h3>"
            "</body></html>"
        )
        result = scrape("https://example.com")
        assert "Title" in result
        assert "Subtitle" in result
        assert "Section" in result


class TestScrapeStripping:
    """Verify that script, style, and footer tags are removed."""

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_strips_scripts(self, mock_get: MagicMock) -> None:
        mock_get.return_value = _mock_response(
            "<html><body><p>OK</p>"
            "<script>alert('xss')</script></body></html>"
        )
        assert "alert" not in scrape("https://x.com")

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_strips_inline_script_attrs(
        self, mock_get: MagicMock
    ) -> None:
        """Script tags with attributes should still be stripped."""
        mock_get.return_value = _mock_response(
            '<html><body><p>Safe</p>'
            '<script type="module" src="app.js"></script>'
            "</body></html>"
        )
        result = scrape("https://x.com")
        assert "Safe" in result
        assert "app.js" not in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_strips_multiline_script(
        self, mock_get: MagicMock
    ) -> None:
        """Multi-line script blocks should be fully removed."""
        html = (
            "<html><body><p>Content</p>"
            "<script>\n"
            "  const x = 1;\n"
            "  console.log(x);\n"
            "</script></body></html>"
        )
        mock_get.return_value = _mock_response(html)
        result = scrape("https://x.com")
        assert "console" not in result
        assert "Content" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_strips_styles(self, mock_get: MagicMock) -> None:
        mock_get.return_value = _mock_response(
            "<html><body>"
            "<style>.x{display:none}</style>"
            "<p>Visible</p></body></html>"
        )
        result = scrape("https://x.com")
        assert "display" not in result
        assert "Visible" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_strips_footer(self, mock_get: MagicMock) -> None:
        mock_get.return_value = _mock_response(
            "<html><body><p>Main</p>"
            "<footer>© 2026</footer></body></html>"
        )
        result = scrape("https://x.com")
        assert "2026" not in result
        assert "Main" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_strips_nested_footer(
        self, mock_get: MagicMock
    ) -> None:
        """Footers containing nested elements should be stripped."""
        mock_get.return_value = _mock_response(
            "<html><body><p>Body</p>"
            "<footer><div><a href='/'>Home</a>"
            "<span>Legal</span></div></footer></body></html>"
        )
        result = scrape("https://x.com")
        assert "Legal" not in result
        assert "Body" in result


class TestScrapeEdgeCases:
    """Edge cases and unusual inputs."""

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_empty_body(self, mock_get: MagicMock) -> None:
        """An empty HTML body should return empty/whitespace."""
        mock_get.return_value = _mock_response(
            "<html><body></body></html>"
        )
        result = scrape("https://x.com")
        assert result.strip() == "" or len(result.strip()) < 10

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_unicode_content(self, mock_get: MagicMock) -> None:
        """Unicode characters should be preserved."""
        mock_get.return_value = _mock_response(
            "<html><body>"
            "<p>日本語テスト 🚀 café résumé</p>"
            "</body></html>"
        )
        result = scrape("https://x.com")
        assert "日本語テスト" in result
        assert "🚀" in result
        assert "café" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_special_html_entities(
        self, mock_get: MagicMock
    ) -> None:
        """HTML entities like &amp; should be decoded."""
        mock_get.return_value = _mock_response(
            "<html><body>"
            "<p>Tom &amp; Jerry &lt;3</p>"
            "</body></html>"
        )
        result = scrape("https://x.com")
        assert "Tom & Jerry" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_only_scripts_no_content(
        self, mock_get: MagicMock
    ) -> None:
        """A page with only scripts should return empty."""
        mock_get.return_value = _mock_response(
            "<html><body>"
            "<script>var x = 1;</script>"
            "<script>var y = 2;</script>"
            "</body></html>"
        )
        result = scrape("https://x.com")
        assert "var x" not in result
        assert "var y" not in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_multiple_blank_lines_collapsed(
        self, mock_get: MagicMock
    ) -> None:
        """Excessive blank lines should be collapsed."""
        mock_get.return_value = _mock_response(
            "<html><body>"
            "<p>A</p><br><br><br><br><br><p>B</p>"
            "</body></html>"
        )
        result = scrape("https://x.com")
        assert "\n\n\n" not in result
        assert "A" in result
        assert "B" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_table_content_preserved(
        self, mock_get: MagicMock
    ) -> None:
        """Table data should be present in output."""
        mock_get.return_value = _mock_response(
            "<html><body><table>"
            "<tr><th>Name</th><th>Age</th></tr>"
            "<tr><td>Alice</td><td>30</td></tr>"
            "</table></body></html>"
        )
        result = scrape("https://x.com")
        assert "Alice" in result
        assert "30" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_large_html_page(self, mock_get: MagicMock) -> None:
        """A large HTML page should not crash."""
        paragraphs = "".join(
            f"<p>Paragraph {i} content here.</p>" for i in range(500)
        )
        mock_get.return_value = _mock_response(
            f"<html><body>{paragraphs}</body></html>"
        )
        result = scrape("https://x.com")
        assert "Paragraph 0" in result
        assert "Paragraph 499" in result
        assert isinstance(result, str)

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_malformed_html(self, mock_get: MagicMock) -> None:
        """Malformed HTML should not crash."""
        mock_get.return_value = _mock_response(
            "<html><body><p>Unclosed paragraph"
            "<div>Nested <span>mess</div></span>"
        )
        result = scrape("https://x.com")
        assert isinstance(result, str)

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_return_type_is_always_string(
        self, mock_get: MagicMock
    ) -> None:
        """Return type should always be str."""
        mock_get.return_value = _mock_response(
            "<html><body><p>Test</p></body></html>"
        )
        assert isinstance(scrape("https://x.com"), str)


class TestScrapeErrors:
    """HTTP error and network failure handling."""

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_handles_404(self, mock_get: MagicMock) -> None:
        resp = MagicMock()
        resp.status_code = 404
        resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found", request=MagicMock(), response=resp
        )
        mock_get.return_value = resp
        result = scrape("https://x.com/404")
        assert "Error" in result
        assert "404" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_handles_500(self, mock_get: MagicMock) -> None:
        resp = MagicMock()
        resp.status_code = 500
        resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server Error", request=MagicMock(), response=resp
        )
        mock_get.return_value = resp
        result = scrape("https://x.com/500")
        assert "Error" in result
        assert "500" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_handles_403(self, mock_get: MagicMock) -> None:
        """Forbidden response should return clear error."""
        resp = MagicMock()
        resp.status_code = 403
        resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Forbidden", request=MagicMock(), response=resp
        )
        mock_get.return_value = resp
        result = scrape("https://x.com/403")
        assert "Error" in result
        assert "403" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_handles_connection_error(
        self, mock_get: MagicMock
    ) -> None:
        mock_get.side_effect = httpx.ConnectError(
            "Connection refused"
        )
        assert "Error" in scrape("https://unreachable.com")

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_handles_timeout_error(
        self, mock_get: MagicMock
    ) -> None:
        """Timeout should return an error message."""
        mock_get.side_effect = httpx.ReadTimeout(
            "Read timed out"
        )
        result = scrape("https://slow.com")
        assert "Error" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_handles_dns_error(
        self, mock_get: MagicMock
    ) -> None:
        """DNS resolution failure should return error."""
        mock_get.side_effect = httpx.ConnectError(
            "Name resolution failed"
        )
        result = scrape("https://nonexistent.invalid")
        assert "Error" in result

    @patch("protocolbox.tools.scraper.httpx.get")
    def test_error_message_never_contains_html(
        self, mock_get: MagicMock
    ) -> None:
        """Error messages should be plain text."""
        resp = MagicMock()
        resp.status_code = 500
        resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Error", request=MagicMock(), response=resp
        )
        mock_get.return_value = resp
        result = scrape("https://x.com")
        assert "<" not in result
