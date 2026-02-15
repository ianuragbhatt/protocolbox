"""pb_get_transcript — YouTube video transcript fetcher."""

import re

from youtube_transcript_api import YouTubeTranscriptApi

from protocolbox.server import mcp

# Regex to extract Video ID from various YouTube URL formats.
_VIDEO_ID_PATTERN = re.compile(
    r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)"
    r"([a-zA-Z0-9_-]{11})"
)


def _extract_video_id(url: str) -> str | None:
    """Extract the 11-character video ID from a YouTube URL.

    Supports:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/embed/VIDEO_ID

    Args:
        url: A YouTube video URL.

    Returns:
        The video ID string, or None if extraction fails.
    """
    match = _VIDEO_ID_PATTERN.search(url)
    return match.group(1) if match else None


@mcp.tool()
def get_transcript(video_url: str) -> str:
    """Fetch the English transcript of a YouTube video.

    Extracts the video ID from the URL, fetches the transcript,
    and returns it as a single clean block of text.

    Args:
        video_url: A YouTube video URL
                   (e.g. "https://www.youtube.com/watch?v=dQw4w9WgXcQ").

    Returns:
        The transcript text, or an error message if fetching fails.
    """
    video_id = _extract_video_id(video_url)
    if not video_id:
        return (
            f"Error: Could not extract video ID from '{video_url}'. "
            "Please provide a valid YouTube URL."
        )

    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=["en"])
        text = " ".join(snippet.text for snippet in transcript)
        return text.strip()
    except Exception as e:
        return (
            f"Error: Could not fetch transcript for video '{video_id}'. "
            f"{type(e).__name__}: {e}"
        )
