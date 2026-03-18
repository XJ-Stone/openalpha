"""Frontmatter scanner and index for investor data."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import frontmatter

from .entity import ExtractedEntities

MAX_APPEARANCES = 50


def scan_profiles(investors_dir: Path) -> list[dict]:
    """Read all profile.md files under investors_dir and return frontmatter metadata.

    Each returned dict contains the parsed frontmatter fields plus a ``_path``
    key pointing to the source file.
    """
    profiles: list[dict] = []
    if not investors_dir.is_dir():
        return profiles

    for profile_path in sorted(investors_dir.rglob("profile.md")):
        try:
            post = frontmatter.load(str(profile_path))
            meta = dict(post.metadata)
            meta["_path"] = profile_path
            meta["_content"] = post.content
            # Derive slug from parent directory name
            meta.setdefault("slug", profile_path.parent.name)
            profiles.append(meta)
        except Exception:
            # Skip malformed files silently
            continue

    return profiles


def scan_appearances(investors_dir: Path) -> list[dict]:
    """Read all appearance .md files (anything that is not profile.md) and return metadata.

    Each returned dict contains frontmatter fields plus ``_path`` and ``_content``.
    """
    appearances: list[dict] = []
    if not investors_dir.is_dir():
        return appearances

    for md_path in sorted(investors_dir.rglob("*.md")):
        if md_path.name == "profile.md":
            continue
        try:
            post = frontmatter.load(str(md_path))
            meta = dict(post.metadata)
            meta["_path"] = md_path
            meta["_content"] = post.content
            # Derive investor slug from grandparent or parent directory
            meta.setdefault("investor_slug", md_path.parent.parent.name)
            appearances.append(meta)
        except Exception:
            continue

    return appearances


# ---------------------------------------------------------------------------
# Matching helpers
# ---------------------------------------------------------------------------


def _matches_investor(app: dict, investors: list[str]) -> bool:
    """Check if an appearance belongs to any of the given investors."""
    slug = (app.get("investor_slug", "") or app.get("investor", "")).lower()
    for inv in investors:
        inv_lower = inv.lower()
        if inv_lower in slug or any(part in slug for part in inv_lower.split()):
            return True
    return False


def _matches_companies(app: dict, tickers: list[str]) -> bool:
    """Check if an appearance mentions any of the given tickers."""
    app_companies = {c.upper() for c in (app.get("companies", []) or [])}
    return bool(app_companies & {t.upper() for t in tickers})


def _matches_topics(app: dict, topics: list[str]) -> bool:
    """Check if an appearance covers any of the given topics (substring match)."""
    app_topics = [t.lower() for t in (app.get("topics", []) or [])]
    app_topics += [s.lower() for s in (app.get("sectors", []) or [])]
    for topic in topics:
        topic_lower = topic.lower()
        for app_topic in app_topics:
            if topic_lower in app_topic or app_topic in topic_lower:
                return True
    return False


def _parse_date(d: str | date | None) -> date | None:
    """Parse a date field from frontmatter (may be str or date object)."""
    if isinstance(d, date):
        return d
    if isinstance(d, str):
        try:
            parts = d.split("-")
            return date(int(parts[0]), int(parts[1]), int(parts[2]))
        except (ValueError, IndexError):
            return None
    return None


def _within_time_range(app: dict, months: int) -> bool:
    """Check if an appearance's date falls within the last N months."""
    d = _parse_date(app.get("date"))
    if d is None:
        return False
    cutoff = date.today() - timedelta(days=months * 30)
    return d >= cutoff


# ---------------------------------------------------------------------------
# Core search: AND across categories, OR within categories
# ---------------------------------------------------------------------------


def search_by_entities(
    entities: ExtractedEntities,
    appearances: list[dict],
    profiles: list[dict],
    resolved_topics: list[str] | None = None,
    *,
    max_appearances: int = MAX_APPEARANCES,
) -> dict[str, list[dict]]:
    """Filter appearances using AND-across-categories, OR-within-categories logic.

    Dimensions:
    - investor: match if appearance belongs to ANY listed investor
    - company:  match if appearance mentions ANY listed ticker
    - topic:    match if appearance covers ANY listed topic (includes resolved_topics)
    - time:     match if appearance date is within time_months

    An appearance must satisfy ALL specified dimensions to be included.
    Profiles are matched by investor name/slug only (never by ticker/topic).
    """
    if entities.is_empty:
        return {"profiles": [], "appearances": []}

    # Merge raw topics with resolved topics
    all_topics = list(entities.topics or [])
    if resolved_topics:
        all_topics.extend(resolved_topics)

    # --- Filter appearances: AND across dimensions ---
    matched: list[dict] = []
    for app in appearances:
        # Each dimension is a gate — if specified, must match
        if entities.investors and not _matches_investor(app, entities.investors):
            continue
        if entities.tickers and not _matches_companies(app, entities.tickers):
            continue
        if all_topics and not _matches_topics(app, all_topics):
            continue
        if entities.time_months and not _within_time_range(app, entities.time_months):
            continue
        matched.append(app)

    # Sort by date descending (newest first)
    matched.sort(key=lambda a: str(a.get("date", "")), reverse=True)

    # Cap results
    matched = matched[:max_appearances]

    # --- Match profiles by investor only ---
    matched_slugs = {
        a.get("investor_slug", "") or a.get("investor", "") for a in matched
    }
    matched_profiles: list[dict] = []
    for p in profiles:
        slug = p.get("slug", "")
        # Include if investor slug appears in matched appearances
        if slug in matched_slugs:
            matched_profiles.append(p)
            continue
        # Or if profile directly matches an investor name query
        if entities.investors:
            name = (p.get("name") or "").lower()
            p_slug = slug.lower()
            fund = (p.get("fund") or "").lower()
            searchable = f"{name} {p_slug} {fund}"
            for inv in entities.investors:
                inv_lower = inv.lower()
                if inv_lower in searchable or any(
                    part in searchable for part in inv_lower.split()
                ):
                    matched_profiles.append(p)
                    break

    return {"profiles": matched_profiles, "appearances": matched}


class InvestorIndex:
    """In-memory index over investor profiles and appearances.

    Scans the investors directory once (on first access) and caches the
    results for subsequent searches.
    """

    def __init__(self, investors_dir: Path) -> None:
        self._investors_dir = investors_dir
        self._profiles: list[dict] | None = None
        self._appearances: list[dict] | None = None
        # Reverse indexes: key -> list of appearance dicts
        self._topic_index: dict[str, list[dict]] | None = None
        self._company_index: dict[str, list[dict]] | None = None

    def _ensure_loaded(self) -> None:
        """Lazily scan the filesystem and populate caches."""
        if self._profiles is None:
            self._profiles = scan_profiles(self._investors_dir)
        if self._appearances is None:
            self._appearances = scan_appearances(self._investors_dir)
            self._build_reverse_indexes()

    def _build_reverse_indexes(self) -> None:
        """Build topic->appearances and company->appearances mappings."""
        assert self._appearances is not None
        self._topic_index = {}
        self._company_index = {}
        for app in self._appearances:
            # Read both 'topics' (new) and 'sectors' (legacy) into the same index
            all_tags = list(app.get("topics", []) or []) + list(app.get("sectors", []) or [])
            for tag in all_tags:
                key = tag.lower()
                self._topic_index.setdefault(key, []).append(app)
            for company in app.get("companies", []) or []:
                key = company.upper()
                self._company_index.setdefault(key, []).append(app)

    @property
    def profiles(self) -> list[dict]:
        """Return cached profile list."""
        self._ensure_loaded()
        assert self._profiles is not None
        return self._profiles

    @property
    def appearances(self) -> list[dict]:
        """Return cached appearance list."""
        self._ensure_loaded()
        assert self._appearances is not None
        return self._appearances

    @property
    def all_sectors(self) -> list[str]:
        """Return the union of all topic/sector tags across appearances."""
        self._ensure_loaded()
        assert self._topic_index is not None
        return sorted(self._topic_index.keys())

    @property
    def all_companies(self) -> list[str]:
        """Return the union of all company tickers across appearances."""
        self._ensure_loaded()
        assert self._company_index is not None
        return sorted(self._company_index.keys())

    def appearances_for_sectors(self, sectors: list[str]) -> list[dict]:
        """Return appearances matching any of the given topic/sector keys."""
        self._ensure_loaded()
        assert self._topic_index is not None
        seen_paths: set[str] = set()
        results: list[dict] = []
        for sector in sectors:
            for app in self._topic_index.get(sector.lower(), []):
                path_key = str(app.get("_path", id(app)))
                if path_key not in seen_paths:
                    seen_paths.add(path_key)
                    results.append(app)
        return results

    def appearances_for_companies(self, tickers: list[str]) -> list[dict]:
        """Return appearances matching any of the given company tickers."""
        self._ensure_loaded()
        assert self._company_index is not None
        seen_paths: set[str] = set()
        results: list[dict] = []
        for ticker in tickers:
            for app in self._company_index.get(ticker.upper(), []):
                path_key = str(app.get("_path", id(app)))
                if path_key not in seen_paths:
                    seen_paths.add(path_key)
                    results.append(app)
        return results

    def search(
        self,
        entities: ExtractedEntities,
        resolved_topics: list[str] | None = None,
        *,
        max_appearances: int = MAX_APPEARANCES,
    ) -> dict[str, list[dict]]:
        """Search the index using extracted entities with AND logic."""
        self._ensure_loaded()
        assert self._profiles is not None and self._appearances is not None
        return search_by_entities(
            entities,
            self._appearances,
            self._profiles,
            resolved_topics,
            max_appearances=max_appearances,
        )

    def reload(self) -> None:
        """Force a re-scan of the investors directory."""
        self._profiles = None
        self._appearances = None
        self._topic_index = None
        self._company_index = None
