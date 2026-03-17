"""Shared fixtures for tests."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture()
def tmp_investors(tmp_path: Path) -> Path:
    """Create a minimal investors directory with one investor and appearances."""
    investor_dir = tmp_path / "investors" / "test-investor" / "appearances"
    investor_dir.mkdir(parents=True)

    # Profile
    profile = tmp_path / "investors" / "test-investor" / "profile.md"
    profile.write_text(
        "---\n"
        "name: Test Investor\n"
        "slug: test-investor\n"
        "fund: Test Capital\n"
        "role: Managing Partner\n"
        "topics: [ai-infrastructure, saas-metrics]\n"
        "companies: [NVDA, SNOW]\n"
        "sources: [TestPod]\n"
        "last_updated: 2025-06-01\n"
        "---\n\n"
        "# Test Investor\n\n## Background\nA test investor.\n"
    )

    # Appearance 1 — NVDA focused
    (investor_dir / "2025-06-01-testpod-nvidia-outlook.md").write_text(
        "---\n"
        "investor: test-investor\n"
        "date: 2025-06-01\n"
        "source: TestPod\n"
        "type: podcast\n"
        "url: https://example.com/ep1\n"
        "companies: [NVDA, MSFT]\n"
        "topics: [ai-infrastructure]\n"
        "companies_detail:\n"
        "  - ticker: NVDA\n"
        "    focus: primary\n"
        "  - ticker: MSFT\n"
        "    focus: secondary\n"
        "topics_detail:\n"
        "  - topic: ai-infrastructure\n"
        "    focus: primary\n"
        "---\n\n"
        "# TestPod — June 01, 2025\n\n"
        "## Company-Specific Views\n\n"
        "### NVDA (NVIDIA) — Bullish, HIGH, primary\n\n"
        "NVIDIA is the picks and shovels play for AI infrastructure.\n\n"
        "### MSFT (Microsoft) — Neutral, MEDIUM, secondary\n\n"
        "Microsoft benefits from Azure AI demand.\n\n"
        "## Broader Topics\n\n"
        "### ai-infrastructure (primary)\n\n"
        "The AI infrastructure buildout will continue through 2026.\n"
    )

    # Appearance 2 — SNOW focused
    (investor_dir / "2025-05-15-testpod-snowflake-deep-dive.md").write_text(
        "---\n"
        "investor: test-investor\n"
        "date: 2025-05-15\n"
        "source: TestPod\n"
        "type: podcast\n"
        "url: https://example.com/ep2\n"
        "companies: [SNOW]\n"
        "topics: [saas-metrics]\n"
        "companies_detail:\n"
        "  - ticker: SNOW\n"
        "    focus: primary\n"
        "topics_detail:\n"
        "  - topic: saas-metrics\n"
        "    focus: primary\n"
        "---\n\n"
        "# TestPod — May 15, 2025\n\n"
        "## Company-Specific Views\n\n"
        "### SNOW (Snowflake) — Bearish, MEDIUM, primary\n\n"
        "Snowflake's consumption model faces headwinds.\n\n"
        "## Broader Topics\n\n"
        "### saas-metrics (primary)\n\n"
        "NRR compression across enterprise SaaS.\n"
    )

    return tmp_path / "investors"
