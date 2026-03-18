"""Shared fixtures for tests."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture()
def tmp_investors(tmp_path: Path) -> Path:
    """Create a minimal investors directory with two investors and appearances."""
    investors_root = tmp_path / "investors"

    # --- Investor 1: test-investor ---
    inv1_dir = investors_root / "test-investor" / "appearances"
    inv1_dir.mkdir(parents=True)

    (investors_root / "test-investor" / "profile.md").write_text(
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

    # Appearance 1 — NVDA, recent
    (inv1_dir / "2026-02-01-testpod-nvidia-outlook.md").write_text(
        "---\n"
        "investor: test-investor\n"
        "date: 2026-02-01\n"
        "source: TestPod\n"
        "type: podcast\n"
        "url: https://example.com/ep1\n"
        "companies: [NVDA, MSFT]\n"
        "topics: [ai-infrastructure]\n"
        "---\n\n"
        "NVIDIA is the picks and shovels play for AI infrastructure.\n"
    )

    # Appearance 2 — SNOW, recent
    (inv1_dir / "2026-01-15-testpod-snowflake-deep-dive.md").write_text(
        "---\n"
        "investor: test-investor\n"
        "date: 2026-01-15\n"
        "source: TestPod\n"
        "type: podcast\n"
        "url: https://example.com/ep2\n"
        "companies: [SNOW]\n"
        "topics: [saas-metrics]\n"
        "---\n\n"
        "Snowflake's consumption model faces headwinds.\n"
    )

    # Appearance 3 — NVDA, old (over a year ago)
    (inv1_dir / "2024-06-01-testpod-nvidia-old.md").write_text(
        "---\n"
        "investor: test-investor\n"
        "date: 2024-06-01\n"
        "source: TestPod\n"
        "type: podcast\n"
        "url: https://example.com/ep3\n"
        "companies: [NVDA]\n"
        "topics: [ai-infrastructure]\n"
        "---\n\n"
        "Old take on NVIDIA from 2024.\n"
    )

    # --- Investor 2: other-investor ---
    inv2_dir = investors_root / "other-investor" / "appearances"
    inv2_dir.mkdir(parents=True)

    (investors_root / "other-investor" / "profile.md").write_text(
        "---\n"
        "name: Other Investor\n"
        "slug: other-investor\n"
        "fund: Other Capital\n"
        "role: Partner\n"
        "topics: [ai-infrastructure]\n"
        "companies: [NVDA, TSLA]\n"
        "sources: [OtherPod]\n"
        "last_updated: 2026-01-01\n"
        "---\n\n"
        "# Other Investor\n\n## Background\nAnother test investor.\n"
    )

    # Appearance — NVDA by other-investor
    (inv2_dir / "2026-01-20-otherpod-nvidia-take.md").write_text(
        "---\n"
        "investor: other-investor\n"
        "date: 2026-01-20\n"
        "source: OtherPod\n"
        "type: podcast\n"
        "url: https://example.com/ep4\n"
        "companies: [NVDA]\n"
        "topics: [ai-infrastructure]\n"
        "---\n\n"
        "Other investor's take on NVIDIA.\n"
    )

    return investors_root
