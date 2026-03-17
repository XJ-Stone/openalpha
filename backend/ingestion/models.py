"""Shared data models for the ingestion pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RawContent:
    """Output of an extractor — one unit of fetched content, source-agnostic.

    Every extractor must produce this. The processor and renderer never need
    to know which source it came from.
    """

    text: str
    title: str
    date: str  # YYYY-MM-DD
    url: str
    source_type: str  # "substack", "youtube", "podcast", etc.
    images: list[dict[str, str]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ProcessedContent:
    """Output of a processor — structured extraction ready for rendering."""

    raw: RawContent
    investor: str
    source_name: str
    # Either AppearanceSummary (long/compressed) or AppearanceIndex (short/verbatim)
    extraction: Any  # AppearanceSummary | AppearanceIndex
    is_full_text: bool  # True = short content kept verbatim
