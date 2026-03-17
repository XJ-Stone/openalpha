"""Extractor registry — each source type has one extractor.

To add a new source, create a file in this package with a class that inherits
from BaseExtractor and implements the `fetch` method. Then register it in
EXTRACTOR_REGISTRY below.
"""

from __future__ import annotations

from .base import BaseExtractor
from .manual import ManualExtractor
from .substack import SubstackExtractor
from .youtube import YouTubeExtractor

# Map source type string → extractor class.
# To add a new source, add an entry here.
EXTRACTOR_REGISTRY: dict[str, type[BaseExtractor]] = {
    "substack": SubstackExtractor,
    "youtube": YouTubeExtractor,
    "manual": ManualExtractor,
}


def get_extractor(source_type: str) -> BaseExtractor:
    """Return an extractor instance for the given source type."""
    cls = EXTRACTOR_REGISTRY.get(source_type)
    if cls is None:
        available = ", ".join(sorted(EXTRACTOR_REGISTRY.keys()))
        raise ValueError(
            f"Unknown source type: {source_type!r}. Available: {available}"
        )
    return cls()


__all__ = [
    "BaseExtractor",
    "EXTRACTOR_REGISTRY",
    "get_extractor",
    "ManualExtractor",
    "SubstackExtractor",
    "YouTubeExtractor",
]
