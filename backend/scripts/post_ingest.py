"""Post-ingestion reconciliation: update profile metadata and INVESTORS.md.

Run this after adding new appearances (manually or via data-ingestion scripts).
It does NOT use an LLM — it only aggregates frontmatter from appearance files.

Usage:
    # Reconcile a single investor
    python scripts/post_ingest.py --investor freda-duan

    # Reconcile all investors
    python scripts/post_ingest.py --all

    # Dry run — show what would change without writing
    python scripts/post_ingest.py --all --dry-run
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import frontmatter

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
INVESTORS_DIR = PROJECT_ROOT / "investors"
INVESTORS_MD = PROJECT_ROOT / "INVESTORS.md"
STATS_JSON = PROJECT_ROOT / "investors" / "_stats.json"


# ---------------------------------------------------------------------------
# Profile reconciliation
# ---------------------------------------------------------------------------


def reconcile_profile(investor_dir: Path, dry_run: bool = False) -> dict:
    """Aggregate companies/sectors from appearances and update profile.md.

    Returns a summary dict with investor metadata for INVESTORS.md.
    """
    slug = investor_dir.name
    profile_path = investor_dir / "profile.md"
    appearances_dir = investor_dir / "appearances"

    if not profile_path.exists():
        print(f"  WARN: {slug} has no profile.md — skipping", file=sys.stderr)
        return {}

    # Load profile
    profile = frontmatter.load(str(profile_path))
    meta = profile.metadata

    # Scan all appearances
    all_companies: set[str] = set()
    all_topics: set[str] = set()
    all_sources: set[str] = set()
    appearance_count = 0
    latest_date = ""

    if appearances_dir.is_dir():
        for md_path in sorted(appearances_dir.glob("*.md")):
            try:
                app = frontmatter.load(str(md_path))
            except Exception:
                continue

            appearance_count += 1
            app_meta = app.metadata

            for ticker in app_meta.get("companies", []):
                if isinstance(ticker, str):
                    all_companies.add(ticker.upper())

            # Read both 'topics' (new) and 'sectors' (legacy)
            for topic in app_meta.get("topics", []) or []:
                if isinstance(topic, str):
                    all_topics.add(topic.lower())
            for sector in app_meta.get("sectors", []) or []:
                if isinstance(sector, str):
                    all_topics.add(sector.lower())

            source = app_meta.get("source", "")
            if source:
                all_sources.add(source)

            app_date = str(app_meta.get("date", ""))
            if app_date > latest_date:
                latest_date = app_date

    # Determine what changed in profile
    old_companies = set(meta.get("companies", []))
    old_topics = set(meta.get("topics", []) or meta.get("sectors", []) or [])
    old_sources = set(meta.get("sources", []))

    companies_changed = all_companies != old_companies
    topics_changed = all_topics != old_topics
    sources_changed = all_sources != old_sources

    changes: list[str] = []
    if companies_changed:
        added = all_companies - old_companies
        removed = old_companies - all_companies
        if added:
            changes.append(f"companies +{sorted(added)}")
        if removed:
            changes.append(f"companies -{sorted(removed)}")
    if topics_changed:
        added = all_topics - old_topics
        if added:
            changes.append(f"topics +{sorted(added)}")
    if sources_changed:
        added = all_sources - old_sources
        if added:
            changes.append(f"sources +{sorted(added)}")

    if changes:
        print(f"  {slug}: {'; '.join(changes)}", file=sys.stderr)
    else:
        print(f"  {slug}: up to date", file=sys.stderr)

    if not dry_run and changes:
        meta["companies"] = sorted(all_companies)
        meta["topics"] = sorted(all_topics)
        # Remove legacy 'sectors' key if present
        meta.pop("sectors", None)
        meta["sources"] = sorted(all_sources)
        meta["last_updated"] = str(date.today())

        profile.metadata = meta
        profile_path.write_text(frontmatter.dumps(profile) + "\n", encoding="utf-8")

    return {
        "name": meta.get("name", slug),
        "slug": slug,
        "fund": meta.get("fund", ""),
        "topics": sorted(all_topics) if all_topics else meta.get("topics", meta.get("sectors", [])),
        "appearances": appearance_count,
        "sources": sorted(all_sources) if all_sources else meta.get("sources", []),
    }


# ---------------------------------------------------------------------------
# INVESTORS.md generation
# ---------------------------------------------------------------------------

_INVESTORS_HEADER = """\
# Tracked Investors

This is the index of all investors currently tracked in the OpenAlpha knowledge base.

| Investor | Fund | Focus | Appearances | Primary Sources |
|---|---|---|---|---|
"""

_INVESTORS_FOOTER = """
## Adding a New Investor

To add a new investor to the knowledge base:

### 1. Create the investor directory

```bash
mkdir -p investors/<slug>/appearances
```

The slug should be lowercase and hyphenated (e.g., `brad-gerstner`, `cathie-wood`).

### 2. Create a profile

Copy the profile template and fill it in:

```bash
cp templates/profile-template.md investors/<slug>/profile.md
```

Required frontmatter fields:

```yaml
---
name: Full Name
slug: lowercase-hyphenated
fund: Fund Name
role: Title
aum: "$XB+" or "N/A"
topics: [topic1, topic2]
companies: [TICK1, TICK2]
sources: [Source1, Source2]
last_updated: YYYY-MM-DD
---
```

Alternatively, once you have at least one appearance file, you can generate a profile automatically:

```bash
cd backend
python scripts/generate_profile.py --investor <slug>
```

### 3. Add appearances

Each appearance is a separate markdown file in the investor's directory. See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions on creating appearance files.

File naming convention: `YYYY-MM-DD-source-topic.md`

Example: `2025-01-14-bg2pod-ai-infrastructure.md`

### 4. Run post-ingest

After adding appearances, reconcile metadata:

```bash
cd backend
python scripts/post_ingest.py --all
```

This updates profile frontmatter and regenerates this index file.

### 5. Open a PR

See [CONTRIBUTING.md](CONTRIBUTING.md) for the PR process.

## Investor Selection Criteria

We prioritize investors who:

- **Have public track records** in technology and growth investing
- **Share detailed views** on specific companies (not just broad market commentary)
- **Appear regularly** in podcasts, interviews, conferences, or written memos
- **Are influential** in how the market thinks about technology companies

This is not a ranking of the "best" investors. It is a curated set of voices whose public commentary is worth tracking systematically.
"""


def generate_stats(dry_run: bool = False) -> None:
    """Scan all appearances and write investors/_stats.json.

    Produces ranked lists of companies and sectors with counts and
    per-investor breakdowns so the frontend can render without an API call.
    """
    company_counts: Counter[str] = Counter()
    topic_counts: Counter[str] = Counter()
    company_investors: dict[str, set[str]] = {}
    topic_investors: dict[str, set[str]] = {}
    total_appearances = 0

    for md in sorted(INVESTORS_DIR.glob("*/appearances/*.md")):
        try:
            post = frontmatter.load(str(md))
        except Exception:
            continue

        meta = post.metadata
        total_appearances += 1
        investor_slug = meta.get("investor", md.parts[-3] if len(md.parts) >= 3 else "")

        for ticker in meta.get("companies", []) or []:
            if isinstance(ticker, str):
                key = ticker.upper()
                company_counts[key] += 1
                company_investors.setdefault(key, set()).add(investor_slug)

        # Read both 'topics' (new) and 'sectors' (legacy)
        all_tags = list(meta.get("topics", []) or []) + list(meta.get("sectors", []) or [])
        for tag in all_tags:
            if isinstance(tag, str):
                key = tag.lower()
                topic_counts[key] += 1
                topic_investors.setdefault(key, set()).add(investor_slug)

    stats = {
        "generated": str(date.today()),
        "total_appearances": total_appearances,
        "companies": [
            {
                "name": name,
                "count": count,
                "investor_count": len(company_investors.get(name, set())),
                "investors": sorted(company_investors.get(name, set())),
            }
            for name, count in company_counts.most_common()
        ],
        "topics": [
            {
                "name": name,
                "count": count,
                "investor_count": len(topic_investors.get(name, set())),
                "investors": sorted(topic_investors.get(name, set())),
            }
            for name, count in topic_counts.most_common()
        ],
    }

    if dry_run:
        print(
            f"\n  _stats.json would have {len(stats['companies'])} companies, "
            f"{len(stats['topics'])} topics",
            file=sys.stderr,
        )
    else:
        STATS_JSON.write_text(
            json.dumps(stats, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(
            f"  _stats.json updated ({len(stats['companies'])} companies, "
            f"{len(stats['topics'])} topics, {total_appearances} appearances)",
            file=sys.stderr,
        )


def regenerate_investors_md(
    summaries: list[dict], dry_run: bool = False
) -> None:
    """Regenerate INVESTORS.md from aggregated investor summaries."""
    # Sort by name
    summaries.sort(key=lambda s: s.get("name", ""))

    rows: list[str] = []
    for s in summaries:
        name = s["name"]
        fund = s.get("fund", "")
        focus = ", ".join(s.get("topics", s.get("sectors", []))[:4])
        if len(s.get("topics", s.get("sectors", []))) > 4:
            focus += ", ..."
        appearances = s.get("appearances", 0)
        sources = ", ".join(s.get("sources", []))
        rows.append(f"| {name} | {fund} | {focus} | {appearances} | {sources} |")

    content = _INVESTORS_HEADER + "\n".join(rows) + "\n" + _INVESTORS_FOOTER

    if dry_run:
        print(f"\n  INVESTORS.md would list {len(summaries)} investors", file=sys.stderr)
    else:
        INVESTORS_MD.write_text(content, encoding="utf-8")
        print(f"\n  INVESTORS.md updated ({len(summaries)} investors)", file=sys.stderr)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Post-ingestion: reconcile profile metadata and INVESTORS.md.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--investor", type=str, help="Reconcile a single investor")
    group.add_argument("--all", action="store_true", help="Reconcile all investors")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show changes without writing"
    )
    args = parser.parse_args()

    if not INVESTORS_DIR.is_dir():
        print(f"Error: investors directory not found at {INVESTORS_DIR}", file=sys.stderr)
        sys.exit(1)

    print("Reconciling profiles...", file=sys.stderr)

    summaries: list[dict] = []

    if args.investor:
        investor_dir = INVESTORS_DIR / args.investor
        if not investor_dir.is_dir():
            print(f"Error: investor '{args.investor}' not found", file=sys.stderr)
            sys.exit(1)
        summary = reconcile_profile(investor_dir, dry_run=args.dry_run)
        if summary:
            summaries.append(summary)
        # Still regenerate INVESTORS.md with all investors
        for d in sorted(INVESTORS_DIR.iterdir()):
            if d.is_dir() and not d.name.startswith(".") and d.name != args.investor:
                s = reconcile_profile(d, dry_run=True)  # read-only for others
                if s:
                    summaries.append(s)
    else:
        for d in sorted(INVESTORS_DIR.iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                summary = reconcile_profile(d, dry_run=args.dry_run)
                if summary:
                    summaries.append(summary)

    # Regenerate INVESTORS.md
    if summaries:
        regenerate_investors_md(summaries, dry_run=args.dry_run)

    # Generate _stats.json (company/sector counts for UI)
    generate_stats(dry_run=args.dry_run)

    # Run lint
    print("\nRunning lint...", file=sys.stderr)
    import subprocess

    lint_cmd = [sys.executable, str(Path(__file__).parent / "lint_investors.py")]
    if args.investor:
        lint_cmd += ["--investor", args.investor]
    result = subprocess.run(lint_cmd, capture_output=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
