"""Short content processor — extract metadata only, keep full text verbatim."""

from __future__ import annotations

from ingestion.models import ProcessedContent, RawContent
from src.appearance import extract_index


def process_short(
    raw: RawContent,
    investor: str,
    source_name: str,
    *,
    api_key: str,
    model: str = "gpt-5-mini",
    existing_topics: list[str] | None = None,
) -> ProcessedContent:
    """Extract index metadata from short content (≤3000 words).

    The full text is preserved verbatim — the LLM only extracts
    companies, topics, and focus levels for frontmatter.
    """
    index = extract_index(
        text=raw.text,
        investor=investor,
        date=raw.date,
        source=source_name,
        appearance_type=raw.source_type,
        url=raw.url,
        api_key=api_key,
        model=model,
        existing_topics=existing_topics,
    )

    return ProcessedContent(
        raw=raw,
        investor=investor,
        source_name=source_name,
        extraction=index,
        is_full_text=True,
    )
