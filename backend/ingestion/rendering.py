"""Markdown renderer — turns ProcessedContent into appearance .md files."""

from __future__ import annotations

from ingestion.models import ProcessedContent
from src.appearance import (
    AppearanceIndex,
    render_markdown,
    render_markdown_full,
)


def render(processed: ProcessedContent) -> str:
    """Render a ProcessedContent to the appearance markdown format.

    Routes to full-text or summary rendering based on ``is_full_text``.
    """
    source_length = len(processed.raw.text.split())
    fetch_method = processed.raw.source_type
    fetch_id = processed.raw.metadata.get("slug", "")

    if processed.is_full_text:
        assert isinstance(processed.extraction, AppearanceIndex)
        return render_markdown_full(
            index=processed.extraction,
            full_text=processed.raw.text,
            investor=processed.investor,
            date=processed.raw.date,
            source=processed.source_name,
            appearance_type=processed.raw.source_type,
            url=processed.raw.url,
            source_length=source_length,
            fetch_method=fetch_method,
            fetch_id=fetch_id,
        )
    else:
        return render_markdown(
            summary=processed.extraction,
            investor=processed.investor,
            date=processed.raw.date,
            source=processed.source_name,
            appearance_type=processed.raw.source_type,
            url=processed.raw.url,
            source_length=source_length,
            fetch_method=fetch_method,
            fetch_id=fetch_id,
        )
