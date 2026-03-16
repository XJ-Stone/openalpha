"""Frontmatter scanner and index for investor data."""

from __future__ import annotations

from pathlib import Path

import frontmatter

from .entity import ExtractedEntities


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


def _score_match_entities(item: dict, entities: ExtractedEntities) -> int:
    """Score an item against extracted entities.

    Scoring:
        - Ticker match in ``companies``    -> 100 per match
        - Sector match in ``sectors``      -> 50 per match
        - Investor name/slug match         -> 25
    """
    score = 0

    # Ticker matching — exact match on uppercase tickers
    item_companies = {c.upper() for c in (item.get("companies", []) or [])}
    for ticker in entities.tickers:
        if ticker in item_companies:
            score += 100

    # Topic matching — case-insensitive substring (reads both 'topics' and legacy 'sectors')
    item_topics = [t.lower() for t in (item.get("topics", []) or [])]
    item_topics += [s.lower() for s in (item.get("sectors", []) or [])]
    for topic in entities.topics:
        topic_lower = topic.lower()
        for item_topic in item_topics:
            if topic_lower in item_topic or item_topic in topic_lower:
                score += 50

    # Investor name matching — check against name, slug, fund
    if entities.investors:
        name = (item.get("name") or "").lower()
        slug = (item.get("slug") or item.get("investor_slug") or "").lower()
        fund = (item.get("fund") or "").lower()
        searchable = f"{name} {slug} {fund}"

        for investor in entities.investors:
            investor_lower = investor.lower()
            if investor_lower in searchable or any(
                part in searchable for part in investor_lower.split()
            ):
                score += 25

    return score


def search_by_entities(
    entities: ExtractedEntities,
    profiles: list[dict],
    appearances: list[dict],
) -> dict[str, list[dict]]:
    """Find matching investors and appearances using extracted entities.

    Results are sorted by relevance score then recency.
    """
    if entities.is_empty:
        # No entities extracted — return everything (broad query)
        return {"profiles": list(profiles), "appearances": list(appearances)}

    scored_profiles: list[tuple[int, dict]] = []
    for p in profiles:
        s = _score_match_entities(p, entities)
        if s > 0:
            scored_profiles.append((s, p))

    scored_appearances: list[tuple[int, dict]] = []
    for a in appearances:
        s = _score_match_entities(a, entities)
        if s > 0:
            scored_appearances.append((s, a))

    # If entity extraction returned investors but no ticker/sector matches,
    # also include all appearances for matched investor profiles
    if entities.investors and not scored_appearances and scored_profiles:
        matched_slugs = {p.get("slug") for _, p in scored_profiles}
        for a in appearances:
            a_slug = a.get("investor_slug") or a.get("investor", "")
            if a_slug in matched_slugs:
                scored_appearances.append((25, a))

    # Sort by score desc, then by date desc
    scored_profiles.sort(key=lambda p: (-p[0], str(p[1].get("date", "9999-99-99"))))
    scored_appearances.sort(key=lambda p: (-p[0], str(p[1].get("date", "9999-99-99"))))

    return {
        "profiles": [p for _, p in scored_profiles],
        "appearances": [a for _, a in scored_appearances],
    }


class InvestorIndex:
    """In-memory index over investor profiles and appearances.

    Scans the investors directory once (on first access) and caches the
    results for subsequent searches.  Also builds reverse mappings
    (sector → files, company → files) for fast lookup.
    """

    def __init__(self, investors_dir: Path) -> None:
        self._investors_dir = investors_dir
        self._profiles: list[dict] | None = None
        self._appearances: list[dict] | None = None
        # Reverse indexes: key → list of appearance dicts
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
        """Build topic→appearances and company→appearances mappings."""
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

    def search(self, entities: ExtractedEntities) -> dict[str, list[dict]]:
        """Search the index using extracted entities."""
        self._ensure_loaded()
        assert self._profiles is not None and self._appearances is not None
        return search_by_entities(entities, self._profiles, self._appearances)

    def reload(self) -> None:
        """Force a re-scan of the investors directory."""
        self._profiles = None
        self._appearances = None
        self._topic_index = None
        self._company_index = None
