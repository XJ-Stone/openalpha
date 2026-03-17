"""Tests for the search engine (InvestorIndex + scoring)."""

from __future__ import annotations

from pathlib import Path

from src.entity import ExtractedEntities
from src.search import InvestorIndex, _score_match_entities


class TestScoring:
    """Unit tests for _score_match_entities."""

    def test_ticker_match_scores_100(self):
        item = {"companies": ["NVDA", "MSFT"]}
        entities = ExtractedEntities(tickers=["NVDA"], investors=[], topics=[])
        assert _score_match_entities(item, entities) == 100

    def test_multiple_ticker_matches(self):
        item = {"companies": ["NVDA", "MSFT"]}
        entities = ExtractedEntities(tickers=["NVDA", "MSFT"], investors=[], topics=[])
        assert _score_match_entities(item, entities) == 200

    def test_topic_match_scores_50(self):
        item = {"topics": ["ai-infrastructure"]}
        entities = ExtractedEntities(tickers=[], investors=[], topics=["ai-infrastructure"])
        assert _score_match_entities(item, entities) == 50

    def test_legacy_sectors_field(self):
        item = {"sectors": ["ai-infrastructure"]}
        entities = ExtractedEntities(tickers=[], investors=[], topics=["ai-infrastructure"])
        assert _score_match_entities(item, entities) == 50

    def test_investor_match_scores_25(self):
        item = {"name": "Brad Gerstner", "slug": "brad-gerstner", "fund": "Altimeter"}
        entities = ExtractedEntities(tickers=[], investors=["Gerstner"], topics=[])
        assert _score_match_entities(item, entities) == 25

    def test_no_match_scores_zero(self):
        item = {"companies": ["AAPL"], "topics": ["fintech"]}
        entities = ExtractedEntities(tickers=["NVDA"], investors=[], topics=["ai"])
        assert _score_match_entities(item, entities) == 0

    def test_empty_entities_scores_zero(self):
        item = {"companies": ["NVDA"]}
        entities = ExtractedEntities(tickers=[], investors=[], topics=[])
        assert _score_match_entities(item, entities) == 0

    def test_combined_scoring(self):
        item = {
            "companies": ["NVDA"],
            "topics": ["ai-infrastructure"],
            "name": "Test",
            "slug": "test-investor",
            "fund": "Test Fund",
        }
        entities = ExtractedEntities(
            tickers=["NVDA"], investors=["test-investor"], topics=["ai-infrastructure"],
        )
        # 100 (ticker) + 50 (topic) + 25 (investor) = 175
        assert _score_match_entities(item, entities) == 175

    def test_case_insensitive_ticker(self):
        item = {"companies": ["nvda"]}
        entities = ExtractedEntities(tickers=["NVDA"], investors=[], topics=[])
        assert _score_match_entities(item, entities) == 100

    def test_substring_topic_match(self):
        item = {"topics": ["ai-infrastructure-buildout"]}
        entities = ExtractedEntities(tickers=[], investors=[], topics=["ai-infrastructure"])
        assert _score_match_entities(item, entities) == 50


class TestInvestorIndex:
    """Integration tests for InvestorIndex against fixture data."""

    def test_loads_profiles(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        assert len(index.profiles) == 1
        assert index.profiles[0]["slug"] == "test-investor"

    def test_loads_appearances(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        assert len(index.appearances) == 2

    def test_all_companies(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        companies = index.all_companies
        assert "NVDA" in companies
        assert "SNOW" in companies
        assert "MSFT" in companies

    def test_all_sectors(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        sectors = index.all_sectors
        assert "ai-infrastructure" in sectors
        assert "saas-metrics" in sectors

    def test_appearances_for_companies(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        results = index.appearances_for_companies(["NVDA"])
        assert len(results) == 1
        assert results[0]["companies"] == ["NVDA", "MSFT"]

    def test_appearances_for_sectors(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        results = index.appearances_for_sectors(["saas-metrics"])
        assert len(results) == 1
        assert "SNOW" in results[0]["companies"]

    def test_search_by_ticker(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(tickers=["SNOW"], investors=[], topics=[])
        result = index.search(entities)
        assert len(result["profiles"]) == 1
        assert len(result["appearances"]) == 1

    def test_search_empty_entities_returns_all(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(tickers=[], investors=[], topics=[])
        result = index.search(entities)
        assert len(result["profiles"]) == 1
        assert len(result["appearances"]) == 2

    def test_search_no_match(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        entities = ExtractedEntities(tickers=["AAPL"], investors=[], topics=[])
        result = index.search(entities)
        assert len(result["profiles"]) == 0
        assert len(result["appearances"]) == 0

    def test_reload_clears_cache(self, tmp_investors: Path):
        index = InvestorIndex(tmp_investors)
        _ = index.profiles  # trigger load
        index.reload()
        assert index._profiles is None
        assert index._appearances is None
