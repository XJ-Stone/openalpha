"""YouTube transcript extractor — fetches transcripts from YouTube videos.

This is a placeholder implementation. To use it, install the
``youtube-transcript-api`` package:

    pip install youtube-transcript-api

Contributions welcome — see CONTRIBUTING.md for how to improve extractors.
"""

from __future__ import annotations

import re

from ingestion.models import RawContent

from .base import BaseExtractor


class YouTubeExtractor(BaseExtractor):
    """Extract transcripts from YouTube videos.

    Supports single video URLs. Playlist/channel support is a future goal.
    """

    @property
    def source_type(self) -> str:
        return "youtube"

    def fetch(self, url: str, **kwargs) -> list[RawContent]:
        """Fetch transcript for a YouTube video.

        Kwargs:
            date: Publication date in YYYY-MM-DD format (required — YouTube
                  metadata extraction is not yet implemented).
            title: Video title (optional, defaults to video ID).
        """
        video_id = _extract_video_id(url)
        if not video_id:
            raise ValueError(f"Could not extract video ID from URL: {url}")

        date = kwargs.get("date")
        if not date:
            raise ValueError(
                "YouTube extractor requires --date YYYY-MM-DD "
                "(automatic date extraction not yet implemented)"
            )

        title = kwargs.get("title", f"YouTube video {video_id}")

        try:
            from youtube_transcript_api import YouTubeTranscriptApi
        except ImportError:
            raise ImportError(
                "youtube-transcript-api is required for YouTube extraction.\n"
                "Install it with: pip install youtube-transcript-api"
            )

        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join(entry["text"] for entry in transcript_list)

        return [
            RawContent(
                text=full_text,
                title=title,
                date=date,
                url=url,
                source_type="youtube",
                metadata={"video_id": video_id},
            )
        ]


def _extract_video_id(url: str) -> str | None:
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"(?:embed/)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    # Maybe it's just a video ID
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url):
        return url
    return None
