"""Base class for all content extractors.

To add a new source (RSS, Twitter/X, earnings calls, etc.):

1. Create a new file in this directory (e.g., ``rss.py``)
2. Subclass ``BaseExtractor``
3. Implement ``fetch()`` — return a list of ``RawContent``
4. Register it in ``__init__.py``'s ``EXTRACTOR_REGISTRY``

That's it. The processing and rendering layers handle everything else.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ingestion.models import RawContent


class BaseExtractor(ABC):
    """Abstract base for content extractors.

    Each extractor knows how to fetch content from one source type
    and normalize it into ``RawContent`` objects.
    """

    @property
    @abstractmethod
    def source_type(self) -> str:
        """Short identifier for this source (e.g. 'substack', 'youtube')."""
        ...

    @abstractmethod
    def fetch(self, url: str, **kwargs) -> list[RawContent]:
        """Fetch content from the source.

        Args:
            url: The source URL (Substack base URL, YouTube video URL, etc.)
            **kwargs: Source-specific options (e.g. ``months=6`` for Substack)

        Returns:
            A list of RawContent items, one per article/episode/post.
        """
        ...
