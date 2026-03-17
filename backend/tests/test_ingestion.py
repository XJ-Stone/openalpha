"""Tests for the ingestion pipeline (extractors, models, rendering, registry)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ingestion.extractors import get_extractor, EXTRACTOR_REGISTRY
from ingestion.extractors.substack import html_to_text_and_images, _HTMLToText
from ingestion.extractors.youtube import _extract_video_id
from ingestion.cli import slugify, make_filename, collect_existing_topics
from ingestion.models import RawContent, ProcessedContent
from ingestion.registry import load_registry, resolve_from_registry
from ingestion.rendering import render
from src.appearance import AppearanceIndex, CompanyMention, TopicMention


class TestExtractorRegistry:
    def test_known_extractors(self):
        assert "substack" in EXTRACTOR_REGISTRY
        assert "youtube" in EXTRACTOR_REGISTRY
        assert "manual" in EXTRACTOR_REGISTRY

    def test_get_extractor_returns_instance(self):
        ext = get_extractor("substack")
        assert ext.source_type == "substack"

    def test_get_extractor_unknown_raises(self):
        with pytest.raises(ValueError, match="Unknown source type"):
            get_extractor("tiktok")


class TestHTMLParser:
    def test_basic_html(self):
        text, images = html_to_text_and_images("<p>Hello <b>world</b></p>")
        assert "Hello world" in text
        assert images == []

    def test_extracts_images(self):
        html = '<p>Before</p><img src="https://example.com/chart.png" alt="Revenue chart"/><p>After</p>'
        text, images = html_to_text_and_images(html)
        assert len(images) == 1
        assert images[0]["url"] == "https://example.com/chart.png"
        assert "[IMAGE: Revenue chart]" in text

    def test_strips_script_tags(self):
        html = "<p>Hello</p><script>evil()</script><p>World</p>"
        text, _ = html_to_text_and_images(html)
        assert "evil" not in text
        assert "Hello" in text
        assert "World" in text

    def test_preserves_paragraph_breaks(self):
        html = "<p>Paragraph one</p><p>Paragraph two</p>"
        text, _ = html_to_text_and_images(html)
        assert "Paragraph one" in text
        assert "Paragraph two" in text

    def test_data_attrs_image_src(self):
        html = '<img src="cdn.substack.com/img.png" data-attrs=\'{"src":"s3.amazonaws.com/original.png"}\' />'
        _, images = html_to_text_and_images(html)
        assert images[0]["url"] == "s3.amazonaws.com/original.png"


class TestYouTubeVideoID:
    def test_standard_url(self):
        assert _extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_short_url(self):
        assert _extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_embed_url(self):
        assert _extract_video_id("https://youtube.com/embed/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_bare_id(self):
        assert _extract_video_id("dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_invalid_url(self):
        assert _extract_video_id("https://example.com") is None


class TestSlugify:
    def test_basic(self):
        assert slugify("Hello World") == "hello-world"

    def test_special_chars(self):
        assert slugify("NVIDIA's Q4 Results!") == "nvidias-q4-results"

    def test_truncation(self):
        result = slugify("a" * 100)
        assert len(result) <= 60

    def test_collapses_hyphens(self):
        assert slugify("foo---bar") == "foo-bar"


class TestMakeFilename:
    def test_format(self):
        result = make_filename("2025-06-01", "AI Chip Market", "Robonomics")
        assert result == "2025-06-01-robonomics-ai-chip-market.md"


class TestRegistry:
    def test_load_registry(self):
        registry = load_registry()
        assert len(registry) > 0
        # Check a known entry
        entry = registry.get("https://robonomics.substack.com")
        assert entry is not None
        assert entry["investor"] == "freda-duan"

    def test_resolve_known_url(self):
        result = resolve_from_registry("https://robonomics.substack.com")
        assert result == ("freda-duan", "Robonomics")

    def test_resolve_unknown_url(self):
        result = resolve_from_registry("https://unknown.substack.com")
        assert result is None

    def test_resolve_trailing_slash(self):
        result = resolve_from_registry("https://robonomics.substack.com/")
        assert result == ("freda-duan", "Robonomics")


class TestCollectExistingTopics:
    def test_collects_from_fixtures(self, tmp_investors: Path):
        topics = collect_existing_topics(tmp_investors)
        assert "ai-infrastructure" in topics
        assert "saas-metrics" in topics

    def test_empty_dir(self, tmp_path: Path):
        topics = collect_existing_topics(tmp_path / "nonexistent")
        assert topics == []


class TestRendering:
    def test_render_full_text(self):
        raw = RawContent(
            text="This is the full text of a short article.",
            title="Short Article",
            date="2025-06-01",
            url="https://example.com/article",
            source_type="substack",
            metadata={"slug": "short-article"},
        )
        index = AppearanceIndex(
            companies=[
                CompanyMention(ticker="NVDA", company_name="NVIDIA", focus="primary"),
            ],
            topics=[
                TopicMention(topic="ai-chips", focus="primary"),
            ],
        )
        processed = ProcessedContent(
            raw=raw,
            investor="test-investor",
            source_name="Test Source",
            extraction=index,
            is_full_text=True,
        )

        md = render(processed)
        assert "---" in md
        assert "investor: test-investor" in md
        assert "date: 2025-06-01" in md
        assert "companies: [NVDA]" in md
        assert "topics: [ai-chips]" in md
        assert "This is the full text" in md
        assert "# Test Source — June 01, 2025" in md
