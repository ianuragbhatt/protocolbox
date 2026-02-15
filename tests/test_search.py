"""Tests for the pb_web_search tool — comprehensive edge-case coverage."""

from unittest.mock import MagicMock, patch

from protocolbox.tools.search import web_search


def _mock_ddgs_results(results: list[dict]) -> MagicMock:
    """Create a mock DDGS context manager that returns given results."""
    mock_ddgs = MagicMock()
    mock_ddgs.__enter__ = MagicMock(return_value=mock_ddgs)
    mock_ddgs.__exit__ = MagicMock(return_value=False)
    mock_ddgs.text = MagicMock(return_value=results)
    return mock_ddgs


class TestWebSearchBasic:
    """Basic happy-path search tests."""

    @patch("protocolbox.tools.search.DDGS")
    def test_returns_markdown_with_results(self, mock_ddgs_cls: MagicMock) -> None:
        """A successful search should return formatted Markdown."""
        mock_ddgs_cls.return_value = _mock_ddgs_results([
            {
                "title": "Example Page",
                "href": "https://example.com",
                "body": "An example result.",
            }
        ])
        result = web_search("test query")
        assert "## Search Results for: test query" in result
        assert "Example Page" in result
        assert "https://example.com" in result
        assert "An example result." in result

    @patch("protocolbox.tools.search.DDGS")
    def test_returns_multiple_results(self, mock_ddgs_cls: MagicMock) -> None:
        """Multiple results should be numbered correctly."""
        mock_ddgs_cls.return_value = _mock_ddgs_results([
            {"title": "First", "href": "https://a.com", "body": "Desc A"},
            {"title": "Second", "href": "https://b.com", "body": "Desc B"},
            {"title": "Third", "href": "https://c.com", "body": "Desc C"},
        ])
        result = web_search("multi query")
        assert "### 1. First" in result
        assert "### 2. Second" in result
        assert "### 3. Third" in result

    @patch("protocolbox.tools.search.DDGS")
    def test_respects_max_results(self, mock_ddgs_cls: MagicMock) -> None:
        """The max_results parameter should be passed to DDGS."""
        mock_ddgs_cls.return_value = _mock_ddgs_results([])
        web_search("query", max_results=5)
        ddgs_instance = mock_ddgs_cls.return_value.__enter__.return_value
        ddgs_instance.text.assert_called_once_with("query", max_results=5)

    @patch("protocolbox.tools.search.DDGS")
    def test_default_max_results_is_three(self, mock_ddgs_cls: MagicMock) -> None:
        """Default max_results should be 3."""
        mock_ddgs_cls.return_value = _mock_ddgs_results([])
        web_search("query")
        ddgs_instance = mock_ddgs_cls.return_value.__enter__.return_value
        ddgs_instance.text.assert_called_once_with("query", max_results=3)

    @patch("protocolbox.tools.search.DDGS")
    def test_return_type_is_string(self, mock_ddgs_cls: MagicMock) -> None:
        """Return type should always be str."""
        mock_ddgs_cls.return_value = _mock_ddgs_results([
            {"title": "T", "href": "h", "body": "b"}
        ])
        assert isinstance(web_search("test"), str)


class TestWebSearchNoResults:
    """Tests for when no results are found."""

    @patch("protocolbox.tools.search.DDGS")
    def test_no_results_message(self, mock_ddgs_cls: MagicMock) -> None:
        """An empty result list should return a no-results message."""
        mock_ddgs_cls.return_value = _mock_ddgs_results([])
        result = web_search("obscure query xyz")
        assert "No results found for: obscure query xyz" in result

    @patch("protocolbox.tools.search.DDGS")
    def test_no_results_is_still_string(self, mock_ddgs_cls: MagicMock) -> None:
        """No-results output should still be a string."""
        mock_ddgs_cls.return_value = _mock_ddgs_results([])
        assert isinstance(web_search("nothing"), str)


class TestWebSearchMissingFields:
    """Tests for results with missing fields."""

    @patch("protocolbox.tools.search.DDGS")
    def test_missing_title_uses_fallback(self, mock_ddgs_cls: MagicMock) -> None:
        """A result without 'title' should use fallback text."""
        mock_ddgs_cls.return_value = _mock_ddgs_results([
            {"href": "https://x.com", "body": "Some snippet"}
        ])
        result = web_search("query")
        assert "No title" in result

    @patch("protocolbox.tools.search.DDGS")
    def test_missing_body_uses_fallback(self, mock_ddgs_cls: MagicMock) -> None:
        """A result without 'body' should use fallback text."""
        mock_ddgs_cls.return_value = _mock_ddgs_results([
            {"title": "Title", "href": "https://x.com"}
        ])
        result = web_search("query")
        assert "No description available." in result

    @patch("protocolbox.tools.search.DDGS")
    def test_missing_href_uses_empty(self, mock_ddgs_cls: MagicMock) -> None:
        """A result without 'href' should not crash."""
        mock_ddgs_cls.return_value = _mock_ddgs_results([
            {"title": "Title", "body": "Description"}
        ])
        result = web_search("query")
        assert "Title" in result
        assert "**Link:**" in result

    @patch("protocolbox.tools.search.DDGS")
    def test_completely_empty_result_dict(self, mock_ddgs_cls: MagicMock) -> None:
        """An empty result dict should use all fallbacks."""
        mock_ddgs_cls.return_value = _mock_ddgs_results([{}])
        result = web_search("query")
        assert "No title" in result
        assert "No description available." in result


class TestWebSearchErrors:
    """Error handling tests."""

    @patch("protocolbox.tools.search.DDGS")
    def test_connection_error_returns_error_message(
        self, mock_ddgs_cls: MagicMock
    ) -> None:
        """Network errors should return a descriptive error string."""
        mock_ddgs = MagicMock()
        mock_ddgs.__enter__ = MagicMock(return_value=mock_ddgs)
        mock_ddgs.__exit__ = MagicMock(return_value=False)
        mock_ddgs.text.side_effect = ConnectionError("No internet")
        mock_ddgs_cls.return_value = mock_ddgs
        result = web_search("test")
        assert "Error" in result
        assert "ConnectionError" in result

    @patch("protocolbox.tools.search.DDGS")
    def test_timeout_error_returns_error_message(
        self, mock_ddgs_cls: MagicMock
    ) -> None:
        """Timeout should return a descriptive error string."""
        mock_ddgs = MagicMock()
        mock_ddgs.__enter__ = MagicMock(return_value=mock_ddgs)
        mock_ddgs.__exit__ = MagicMock(return_value=False)
        mock_ddgs.text.side_effect = TimeoutError("Timed out")
        mock_ddgs_cls.return_value = mock_ddgs
        result = web_search("test")
        assert "Error" in result

    @patch("protocolbox.tools.search.DDGS")
    def test_unexpected_exception_handled(self, mock_ddgs_cls: MagicMock) -> None:
        """Unexpected exception types should be caught gracefully."""
        mock_ddgs = MagicMock()
        mock_ddgs.__enter__ = MagicMock(return_value=mock_ddgs)
        mock_ddgs.__exit__ = MagicMock(return_value=False)
        mock_ddgs.text.side_effect = RuntimeError("Unexpected")
        mock_ddgs_cls.return_value = mock_ddgs
        result = web_search("test")
        assert "Error" in result
        assert "RuntimeError" in result

    @patch("protocolbox.tools.search.DDGS")
    def test_error_message_never_contains_html(
        self, mock_ddgs_cls: MagicMock
    ) -> None:
        """Error messages should be plain text."""
        mock_ddgs = MagicMock()
        mock_ddgs.__enter__ = MagicMock(return_value=mock_ddgs)
        mock_ddgs.__exit__ = MagicMock(return_value=False)
        mock_ddgs.text.side_effect = Exception("err")
        mock_ddgs_cls.return_value = mock_ddgs
        result = web_search("test")
        assert "<" not in result


class TestWebSearchEdgeCases:
    """Edge case inputs."""

    @patch("protocolbox.tools.search.DDGS")
    def test_unicode_query(self, mock_ddgs_cls: MagicMock) -> None:
        """Unicode characters in query should be handled."""
        mock_ddgs_cls.return_value = _mock_ddgs_results([
            {"title": "結果", "href": "https://x.com", "body": "日本語の結果"}
        ])
        result = web_search("日本語テスト")
        assert "日本語テスト" in result
        assert "結果" in result

    @patch("protocolbox.tools.search.DDGS")
    def test_emoji_in_query(self, mock_ddgs_cls: MagicMock) -> None:
        """Emoji in query should not crash."""
        mock_ddgs_cls.return_value = _mock_ddgs_results([])
        result = web_search("🚀 rocket")
        assert isinstance(result, str)

    @patch("protocolbox.tools.search.DDGS")
    def test_very_long_query(self, mock_ddgs_cls: MagicMock) -> None:
        """A very long query should not crash."""
        mock_ddgs_cls.return_value = _mock_ddgs_results([])
        long_query = "a " * 500
        result = web_search(long_query)
        assert isinstance(result, str)

    @patch("protocolbox.tools.search.DDGS")
    def test_special_characters_in_query(self, mock_ddgs_cls: MagicMock) -> None:
        """Special characters (quotes, ampersands) should not crash."""
        mock_ddgs_cls.return_value = _mock_ddgs_results([])
        result = web_search('python "best practices" & tips <2026>')
        assert isinstance(result, str)

    @patch("protocolbox.tools.search.DDGS")
    def test_max_results_one(self, mock_ddgs_cls: MagicMock) -> None:
        """max_results=1 should work correctly."""
        mock_ddgs_cls.return_value = _mock_ddgs_results([
            {"title": "Only", "href": "https://x.com", "body": "One result"}
        ])
        result = web_search("query", max_results=1)
        assert "### 1. Only" in result
        assert "### 2." not in result
