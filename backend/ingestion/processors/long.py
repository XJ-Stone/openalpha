"""Long content processor — compress via LLM summarization."""

from __future__ import annotations

from ingestion.models import ProcessedContent, RawContent
from src.appearance import describe_images, summarize_text


def process_long(
    raw: RawContent,
    investor: str,
    source_name: str,
    *,
    api_key: str,
    model: str = "gpt-5-mini",
    existing_topics: list[str] | None = None,
) -> ProcessedContent:
    """Summarize long content (>3000 words) via LLM.

    Also describes images/charts if present in the source.
    """
    image_descriptions: list[dict[str, str]] = []
    if raw.images:
        image_descriptions = describe_images(
            raw.images, api_key=api_key, model=model,
        )

    summary = summarize_text(
        text=raw.text,
        investor=investor,
        date=raw.date,
        source=source_name,
        appearance_type=raw.source_type,
        url=raw.url,
        api_key=api_key,
        model=model,
        image_descriptions=image_descriptions,
        existing_topics=existing_topics,
    )

    return ProcessedContent(
        raw=raw,
        investor=investor,
        source_name=source_name,
        extraction=summary,
        is_full_text=False,
    )
