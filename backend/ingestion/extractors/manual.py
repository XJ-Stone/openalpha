"""Manual extractor — reads content from a local file or stdin.

Used when a contributor has a transcript, blog post, or interview text
they want to ingest directly.
"""

from __future__ import annotations

import sys
from pathlib import Path

from ingestion.models import RawContent

from .base import BaseExtractor


class ManualExtractor(BaseExtractor):
    """Read content from a file path or stdin."""

    @property
    def source_type(self) -> str:
        return "manual"

    def fetch(self, url: str, **kwargs) -> list[RawContent]:
        """Read content from a file or stdin.

        Args:
            url: Path to a text file, or "-" to read from stdin.

        Kwargs:
            date: Publication date in YYYY-MM-DD format (required).
            title: Title for the content (optional).
            source_url: Original URL of the content (optional).
        """
        date = kwargs.get("date")
        if not date:
            raise ValueError("Manual extractor requires --date YYYY-MM-DD")

        if url == "-":
            if sys.stdin.isatty():
                raise ValueError("No input on stdin. Pipe text or use a file path.")
            text = sys.stdin.read()
        else:
            path = Path(url)
            if not path.is_file():
                raise ValueError(f"File not found: {url}")
            text = path.read_text(encoding="utf-8")

        if not text.strip():
            raise ValueError("Input text is empty")

        title = kwargs.get("title", Path(url).stem if url != "-" else "manual-input")
        source_url = kwargs.get("source_url", "")

        return [
            RawContent(
                text=text,
                title=title,
                date=date,
                url=source_url,
                source_type="manual",
            )
        ]
