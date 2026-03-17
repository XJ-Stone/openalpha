"""Content processors — route raw content through short or long pipelines.

Short content (≤3000 words): keep full text, extract metadata only.
Long content (>3000 words): compress via LLM summarization.
"""

from __future__ import annotations

import sys

from ingestion.models import ProcessedContent, RawContent
from src.appearance import COMPRESS_ABOVE_WORDS

from .long import process_long
from .short import process_short


def process(
    raw: RawContent,
    investor: str,
    source_name: str,
    *,
    api_key: str,
    model: str = "gpt-5-mini",
    existing_topics: list[str] | None = None,
) -> ProcessedContent:
    """Route content to the appropriate processor based on word count."""
    word_count = len(raw.text.split())
    is_short = word_count <= COMPRESS_ABOVE_WORDS

    if is_short:
        print(
            f"  Processing (full-text, {word_count}w): {raw.title[:60]}",
            file=sys.stderr,
        )
        return process_short(
            raw, investor, source_name,
            api_key=api_key, model=model, existing_topics=existing_topics,
        )
    else:
        print(
            f"  Processing (summary, {word_count}w): {raw.title[:60]}",
            file=sys.stderr,
        )
        return process_long(
            raw, investor, source_name,
            api_key=api_key, model=model, existing_topics=existing_topics,
        )


__all__ = ["process", "process_short", "process_long"]
