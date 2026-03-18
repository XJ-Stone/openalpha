"""Tests for the search engine (AND-across-categories, OR-within-categories)."""

from __future__ import annotations

from pathlib import Path

from src.entity import ExtractedEntities
from src.search import InvestorIndex


class TestANDLogic:
    """Investor + ticker/topic should AND — only appearances matching both."""

    def test_investor_and_ticker(self, tmp_investors: Path):
        """'What does Test Investor think about NVDA?' — only Test's NVDA appearances."""
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(tickers=["NVDA"], investors=["test-investor"])
        result = index.search(entities)
        assert len(result["appearances"]) == 2  # 2026-02-01 + 2024-06-01
        for app in result["appearances"]:
            assert app["investor"] == "test-investor"
            assert "NVDA" in app["companies"]

    def test_investor_and_ticker_excludes_other_investor(self, tmp_investors: Path):
        """Other investor's NVDA appearance should NOT appear."""
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(tickers=["NVDA"], investors=["test-investor"])
        result = index.search(entities)
        slugs = {a["investor"] for a in result["appearances"]}
        assert "other-investor" not in slugs

    def test_investor_and_ticker_excludes_other_ticker(self, tmp_investors: Path):
        """Test investor's SNOW appearance should NOT appear when asking about NVDA."""
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(tickers=["NVDA"], investors=["test-investor"])
        result = index.search(entities)
        for app in result["appearances"]:
            assert "NVDA" in app["companies"]


class TestORWithinCategory:
    """Multiple investors or tickers should OR within their category."""

    def test_multiple_investors(self, tmp_investors: Path):
        """'What do Test and Other think about NVDA?' — NVDA from both."""
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(
            tickers=["NVDA"], investors=["test-investor", "other-investor"]
        )
        result = index.search(entities)
        slugs = {a["investor"] for a in result["appearances"]}
        assert "test-investor" in slugs
        assert "other-investor" in slugs

    def test_multiple_tickers(self, tmp_investors: Path):
        """'What does Test think about NVDA and SNOW?' — both tickers from Test."""
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(
            tickers=["NVDA", "SNOW"], investors=["test-investor"]
        )
        result = index.search(entities)
        tickers_seen = set()
        for app in result["appearances"]:
            tickers_seen.update(app["companies"])
        assert "NVDA" in tickers_seen
        assert "SNOW" in tickers_seen


class TestSingleDimension:
    """When only one dimension is specified, filter by that dimension alone."""

    def test_ticker_only(self, tmp_investors: Path):
        """'Who's talking about NVDA?' — all NVDA appearances, any investor."""
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(tickers=["NVDA"])
        result = index.search(entities)
        assert len(result["appearances"]) == 3  # 2 from test + 1 from other
        for app in result["appearances"]:
            assert "NVDA" in app["companies"]

    def test_investor_only(self, tmp_investors: Path):
        """'What has Test Investor said?' — all of Test's appearances."""
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(investors=["test-investor"])
        result = index.search(entities)
        assert len(result["appearances"]) == 3  # all 3 test-investor appearances
        for app in result["appearances"]:
            assert app["investor"] == "test-investor"

    def test_topic_only(self, tmp_investors: Path):
        """'What are investors saying about AI infrastructure?'"""
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(topics=["ai-infrastructure"])
        result = index.search(entities)
        assert len(result["appearances"]) >= 3
        for app in result["appearances"]:
            topics = (app.get("topics") or []) + (app.get("sectors") or [])
            assert any("ai-infrastructure" in t.lower() for t in topics)


class TestEmptyEntities:
    """Empty entities should return nothing, not everything."""

    def test_empty_returns_nothing(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities()
        result = index.search(entities)
        assert result["profiles"] == []
        assert result["appearances"] == []


class TestTimeRange:
    """Time filtering should exclude old appearances."""

    def test_recent_only(self, tmp_investors: Path):
        """With time_months=6, the 2024 appearance should be excluded."""
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(tickers=["NVDA"], time_months=6)
        result = index.search(entities)
        for app in result["appearances"]:
            assert app["date"].year >= 2025 or (
                isinstance(app["date"], str) and app["date"] >= "2025"
            )

    def test_no_time_filter_includes_old(self, tmp_investors: Path):
        """Without time_months, old appearances are included."""
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(tickers=["NVDA"])
        result = index.search(entities)
        dates = [str(a["date"]) for a in result["appearances"]]
        assert any("2024" in d for d in dates)


class TestProfileMatching:
    """Profiles should match by investor only, never by ticker/topic."""

    def test_ticker_only_profiles_from_appearances(self, tmp_investors: Path):
        """Ticker-only search: profiles come from matched appearances' investors."""
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(tickers=["SNOW"])
        result = index.search(entities)
        # SNOW only appears in test-investor's appearances
        profile_slugs = {p["slug"] for p in result["profiles"]}
        assert "test-investor" in profile_slugs
        assert "other-investor" not in profile_slugs

    def test_investor_query_includes_profile(self, tmp_investors: Path):
        """Investor name query should include that investor's profile."""
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(investors=["other-investor"])
        result = index.search(entities)
        profile_slugs = {p["slug"] for p in result["profiles"]}
        assert "other-investor" in profile_slugs


class TestResultLimit:
    """Results should be capped at max_appearances."""

    def test_limit(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(tickers=["NVDA"])
        result = index.search(entities, max_appearances=1)
        assert len(result["appearances"]) == 1

    def test_sorted_newest_first(self, tmp_investors: Path):
        """Results should be sorted newest first."""
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(tickers=["NVDA"])
        result = index.search(entities)
        dates = [str(a["date"]) for a in result["appearances"]]
        assert dates == sorted(dates, reverse=True)


class TestInvestorIndex:
    """Basic index functionality tests."""

    def test_loads_profiles(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        assert len(index.profiles) == 2

    def test_loads_appearances(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        assert len(index.appearances) == 4

    def test_all_companies(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        companies = index.all_companies
        assert "NVDA" in companies
        assert "SNOW" in companies

    def test_all_sectors(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        sectors = index.all_sectors
        assert "ai-infrastructure" in sectors
        assert "saas-metrics" in sectors

    def test_reload_clears_cache(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        _ = index.profiles
        index.reload()
        assert index._profiles is None
        assert index._appearances is None
