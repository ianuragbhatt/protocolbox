"""Tests for the pb_get_transcript tool — comprehensive edge-case coverage."""

from unittest.mock import MagicMock, patch

from protocolbox.tools.youtube import _extract_video_id, get_transcript


class TestExtractVideoIdStandard:
    """Test video ID extraction from standard YouTube URLs."""

    def test_standard_url(self) -> None:
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert _extract_video_id(url) == "dQw4w9WgXcQ"

    def test_standard_url_without_www(self) -> None:
        url = "https://youtube.com/watch?v=dQw4w9WgXcQ"
        assert _extract_video_id(url) == "dQw4w9WgXcQ"

    def test_http_url(self) -> None:
        url = "http://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert _extract_video_id(url) == "dQw4w9WgXcQ"

    def test_url_with_extra_params(self) -> None:
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=120&list=PLtest"
        assert _extract_video_id(url) == "dQw4w9WgXcQ"

    def test_url_with_feature_param(self) -> None:
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=shared"
        assert _extract_video_id(url) == "dQw4w9WgXcQ"


class TestExtractVideoIdShort:
    """Test video ID extraction from short youtu.be URLs."""

    def test_short_url(self) -> None:
        url = "https://youtu.be/dQw4w9WgXcQ"
        assert _extract_video_id(url) == "dQw4w9WgXcQ"

    def test_short_url_with_timestamp(self) -> None:
        url = "https://youtu.be/dQw4w9WgXcQ?t=60"
        assert _extract_video_id(url) == "dQw4w9WgXcQ"

    def test_short_url_http(self) -> None:
        url = "http://youtu.be/dQw4w9WgXcQ"
        assert _extract_video_id(url) == "dQw4w9WgXcQ"


class TestExtractVideoIdEmbed:
    """Test video ID extraction from embed URLs."""

    def test_embed_url(self) -> None:
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        assert _extract_video_id(url) == "dQw4w9WgXcQ"

    def test_embed_url_with_params(self) -> None:
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1"
        assert _extract_video_id(url) == "dQw4w9WgXcQ"


class TestExtractVideoIdInvalid:
    """Test invalid URLs that should fail extraction."""

    def test_empty_string(self) -> None:
        assert _extract_video_id("") is None

    def test_random_url(self) -> None:
        assert _extract_video_id("https://example.com") is None

    def test_youtube_homepage(self) -> None:
        assert _extract_video_id("https://www.youtube.com") is None

    def test_youtube_channel(self) -> None:
        assert _extract_video_id("https://www.youtube.com/@username") is None

    def test_youtube_playlist(self) -> None:
        url = "https://www.youtube.com/playlist?list=PLtest123"
        assert _extract_video_id(url) is None

    def test_malformed_url(self) -> None:
        assert _extract_video_id("not a url at all") is None

    def test_partial_video_id(self) -> None:
        """Video ID must be exactly 11 characters."""
        url = "https://www.youtube.com/watch?v=short"
        assert _extract_video_id(url) is None

    def test_none_like_input(self) -> None:
        """A URL with no recognizable pattern."""
        assert _extract_video_id("youtube.com") is None


class TestExtractVideoIdEdgeCases:
    """Edge cases for video ID extraction."""

    def test_id_with_hyphens(self) -> None:
        url = "https://youtu.be/abc-def_123"
        assert _extract_video_id(url) == "abc-def_123"

    def test_id_with_underscores(self) -> None:
        url = "https://youtu.be/___________"
        assert _extract_video_id(url) == "___________"

    def test_id_all_numbers(self) -> None:
        url = "https://youtu.be/12345678901"
        assert _extract_video_id(url) == "12345678901"


def _make_mock_transcript(segments: list[dict]) -> MagicMock:
    """Create a mock FetchedTranscript that is iterable over snippet objects."""
    snippets = []
    for seg in segments:
        snippet = MagicMock()
        snippet.text = seg["text"]
        snippets.append(snippet)
    mock_transcript = MagicMock()
    mock_transcript.__iter__ = MagicMock(return_value=iter(snippets))
    return mock_transcript


class TestGetTranscriptBasic:
    """Basic happy-path transcript tests."""

    @patch("protocolbox.tools.youtube.YouTubeTranscriptApi")
    def test_returns_joined_text(self, mock_api_cls: MagicMock) -> None:
        """Transcript segments should be joined into a single string."""
        mock_api = mock_api_cls.return_value
        mock_api.fetch.return_value = _make_mock_transcript(
            [
                {"text": "Hello world."},
                {"text": "This is a test."},
                {"text": "Thank you."},
            ]
        )
        result = get_transcript("https://youtu.be/dQw4w9WgXcQ")
        assert "Hello world." in result
        assert "This is a test." in result
        assert "Thank you." in result

    @patch("protocolbox.tools.youtube.YouTubeTranscriptApi")
    def test_segments_separated_by_spaces(self, mock_api_cls: MagicMock) -> None:
        """Segments should be joined with spaces."""
        mock_api = mock_api_cls.return_value
        mock_api.fetch.return_value = _make_mock_transcript(
            [
                {"text": "Word1"},
                {"text": "Word2"},
            ]
        )
        result = get_transcript("https://youtu.be/dQw4w9WgXcQ")
        assert "Word1 Word2" in result

    @patch("protocolbox.tools.youtube.YouTubeTranscriptApi")
    def test_return_type_is_string(self, mock_api_cls: MagicMock) -> None:
        mock_api = mock_api_cls.return_value
        mock_api.fetch.return_value = _make_mock_transcript([{"text": "Test"}])
        assert isinstance(get_transcript("https://youtu.be/dQw4w9WgXcQ"), str)

    @patch("protocolbox.tools.youtube.YouTubeTranscriptApi")
    def test_requests_english_language(self, mock_api_cls: MagicMock) -> None:
        """The API should be called with languages=['en']."""
        mock_api = mock_api_cls.return_value
        mock_api.fetch.return_value = _make_mock_transcript([{"text": "T"}])
        get_transcript("https://youtu.be/dQw4w9WgXcQ")
        mock_api.fetch.assert_called_once_with("dQw4w9WgXcQ", languages=["en"])

    @patch("protocolbox.tools.youtube.YouTubeTranscriptApi")
    def test_strips_leading_trailing_whitespace(self, mock_api_cls: MagicMock) -> None:
        """Output should be stripped."""
        mock_api = mock_api_cls.return_value
        mock_api.fetch.return_value = _make_mock_transcript([{"text": "  Hello  "}])
        result = get_transcript("https://youtu.be/dQw4w9WgXcQ")
        assert result == "Hello"


class TestGetTranscriptErrors:
    """Error handling tests."""

    def test_invalid_url_returns_error(self) -> None:
        result = get_transcript("https://example.com/not-youtube")
        assert "Error" in result
        assert "Could not extract video ID" in result

    def test_empty_url_returns_error(self) -> None:
        result = get_transcript("")
        assert "Error" in result

    @patch("protocolbox.tools.youtube.YouTubeTranscriptApi")
    def test_api_exception_returns_error(self, mock_api_cls: MagicMock) -> None:
        """API exceptions should be caught and returned as error strings."""
        mock_api = mock_api_cls.return_value
        mock_api.fetch.side_effect = Exception("Transcript not available")
        result = get_transcript("https://youtu.be/dQw4w9WgXcQ")
        assert "Error" in result
        assert "dQw4w9WgXcQ" in result

    @patch("protocolbox.tools.youtube.YouTubeTranscriptApi")
    def test_no_transcript_available(self, mock_api_cls: MagicMock) -> None:
        """When no transcript exists, should return error."""
        mock_api = mock_api_cls.return_value
        mock_api.fetch.side_effect = Exception("No transcripts available")
        result = get_transcript("https://youtu.be/dQw4w9WgXcQ")
        assert "Error" in result

    @patch("protocolbox.tools.youtube.YouTubeTranscriptApi")
    def test_network_error_returns_error(self, mock_api_cls: MagicMock) -> None:
        """Network errors should be caught."""
        mock_api = mock_api_cls.return_value
        mock_api.fetch.side_effect = ConnectionError("No internet")
        result = get_transcript("https://youtu.be/dQw4w9WgXcQ")
        assert "Error" in result

    def test_error_includes_url_on_bad_input(self) -> None:
        """Error message should include the invalid URL."""
        bad_url = "https://notyoutube.com/video"
        result = get_transcript(bad_url)
        assert bad_url in result

    @patch("protocolbox.tools.youtube.YouTubeTranscriptApi")
    def test_error_return_type_is_string(self, mock_api_cls: MagicMock) -> None:
        mock_api = mock_api_cls.return_value
        mock_api.fetch.side_effect = Exception("fail")
        assert isinstance(get_transcript("https://youtu.be/dQw4w9WgXcQ"), str)


class TestGetTranscriptEdgeCases:
    """Edge cases and unusual inputs."""

    @patch("protocolbox.tools.youtube.YouTubeTranscriptApi")
    def test_empty_transcript(self, mock_api_cls: MagicMock) -> None:
        """An empty transcript list should return an empty string."""
        mock_api = mock_api_cls.return_value
        mock_api.fetch.return_value = _make_mock_transcript([])
        result = get_transcript("https://youtu.be/dQw4w9WgXcQ")
        assert result == ""

    @patch("protocolbox.tools.youtube.YouTubeTranscriptApi")
    def test_single_segment(self, mock_api_cls: MagicMock) -> None:
        """A single segment should work correctly."""
        mock_api = mock_api_cls.return_value
        mock_api.fetch.return_value = _make_mock_transcript([{"text": "Only segment"}])
        result = get_transcript("https://youtu.be/dQw4w9WgXcQ")
        assert result == "Only segment"

    @patch("protocolbox.tools.youtube.YouTubeTranscriptApi")
    def test_unicode_transcript(self, mock_api_cls: MagicMock) -> None:
        """Unicode characters should be preserved."""
        mock_api = mock_api_cls.return_value
        mock_api.fetch.return_value = _make_mock_transcript(
            [
                {"text": "日本語テスト"},
                {"text": "🚀 emoji"},
            ]
        )
        result = get_transcript("https://youtu.be/dQw4w9WgXcQ")
        assert "日本語テスト" in result
        assert "🚀" in result

    @patch("protocolbox.tools.youtube.YouTubeTranscriptApi")
    def test_very_long_transcript(self, mock_api_cls: MagicMock) -> None:
        """A very long transcript should not crash."""
        mock_api = mock_api_cls.return_value
        segments = [{"text": f"Segment {i}"} for i in range(1000)]
        mock_api.fetch.return_value = _make_mock_transcript(segments)
        result = get_transcript("https://youtu.be/dQw4w9WgXcQ")
        assert "Segment 0" in result
        assert "Segment 999" in result
        assert isinstance(result, str)

    @patch("protocolbox.tools.youtube.YouTubeTranscriptApi")
    def test_segments_with_special_characters(self, mock_api_cls: MagicMock) -> None:
        """Special characters (HTML entities, etc.) should pass through."""
        mock_api = mock_api_cls.return_value
        mock_api.fetch.return_value = _make_mock_transcript(
            [
                {"text": "Tom & Jerry"},
                {"text": "Price: $5 < $10"},
            ]
        )
        result = get_transcript("https://youtu.be/dQw4w9WgXcQ")
        assert "Tom & Jerry" in result
        assert "$5" in result
