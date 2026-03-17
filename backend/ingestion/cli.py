"""Unified CLI for the ingestion pipeline.

Usage:
    # Ingest from Substack (auto-resolves investor from registry):
    python -m ingestion substack --url https://robonomics.substack.com --months 6

    # Ingest from a local transcript:
    python -m ingestion manual --file transcript.txt --investor brad-gerstner \\
        --date 2025-03-01 --source "BG2Pod" --type podcast

    # YouTube transcript (requires youtube-transcript-api):
    python -m ingestion youtube --url "https://youtube.com/watch?v=..." \\
        --investor brad-gerstner --date 2025-03-01 --source "BG2Pod"

    # Dry run (list what would be fetched):
    python -m ingestion substack --url https://robonomics.substack.com --months 6 --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from textwrap import shorten

import frontmatter as fm

from ingestion.extractors import get_extractor
from ingestion.models import RawContent
from ingestion.processors import process
from ingestion.registry import resolve_from_registry
from ingestion.rendering import render

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def slugify(text: str) -> str:
    """Convert a title to a filename-safe slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")[:60]


def make_filename(date: str, title: str, source_name: str) -> str:
    """Generate appearance filename: YYYY-MM-DD-source-slug.md"""
    source_slug = slugify(source_name)
    title_slug = slugify(title)
    return f"{date}-{source_slug}-{title_slug}.md"


def collect_existing_topics(investors_dir: Path) -> list[str]:
    """Scan all appearance frontmatter and return the union of topic tags."""
    topics: set[str] = set()
    if not investors_dir.is_dir():
        return []
    for md_path in investors_dir.rglob("*.md"):
        if md_path.name == "profile.md":
            continue
        try:
            post = fm.load(str(md_path))
            for t in post.metadata.get("topics", []) or []:
                topics.add(t)
            for s in post.metadata.get("sectors", []) or []:
                topics.add(s)
        except Exception:
            continue
    return sorted(topics)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------


def run_ingest(
    source_type: str,
    url: str,
    investor: str,
    source_name: str,
    *,
    output_dir: Path | None = None,
    dry_run: bool = False,
    model: str = "gpt-5-mini",
    workers: int = 5,
    **extractor_kwargs,
) -> None:
    """Run the full ingestion pipeline: extract → process → render → write."""
    # --- Extract ---
    extractor = get_extractor(source_type)
    print(f"Fetching from {source_type}: {url}", file=sys.stderr)
    items = extractor.fetch(url, **extractor_kwargs)
    print(f"Found {len(items)} items.", file=sys.stderr)

    if not items:
        print("No content found.", file=sys.stderr)
        return

    # --- List items ---
    for i, item in enumerate(items, 1):
        preview = shorten(item.title, width=60, placeholder="...")
        print(f"  {i}. [{item.date}] {preview}", file=sys.stderr)

    if dry_run:
        print("\nDry run — no files generated.", file=sys.stderr)
        return

    # --- Resolve output directory ---
    if output_dir is None:
        output_dir = _PROJECT_ROOT / "investors" / investor / "appearances"
    output_dir.mkdir(parents=True, exist_ok=True)

    # --- Filter already-existing files ---
    to_process: list[tuple[int, RawContent]] = []
    for i, item in enumerate(items, 1):
        filename = make_filename(item.date, item.title, source_name)
        filepath = output_dir / filename
        if filepath.exists():
            print(f"  [{i}/{len(items)}] SKIP (exists): {filename}", file=sys.stderr)
        else:
            to_process.append((i, item))

    if not to_process:
        print("\nAll items already exist — nothing to do.", file=sys.stderr)
        return

    # --- Get API key ---
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src.config import get_settings

    settings = get_settings()
    api_key = settings.openai_api_key
    if not api_key:
        print("Error: OPENAI_API_KEY not set in .env", file=sys.stderr)
        sys.exit(1)

    # --- Collect existing topics ---
    existing_topics = collect_existing_topics(_PROJECT_ROOT / "investors")
    if existing_topics:
        print(f"Loaded {len(existing_topics)} existing topics for reuse.", file=sys.stderr)

    print(
        f"\nProcessing {len(to_process)} items with {model} ({workers} workers)...",
        file=sys.stderr,
    )

    # --- Process and render in parallel ---
    def _process_one(item: tuple[int, RawContent]) -> str:
        idx, raw = item
        filename = make_filename(raw.date, raw.title, source_name)
        filepath = output_dir / filename  # type: ignore[operator]

        try:
            processed = process(
                raw, investor, source_name,
                api_key=api_key, model=model,
                existing_topics=existing_topics,
            )
            md = render(processed)
            filepath.write_text(md + "\n", encoding="utf-8")
            mode = "full-text" if processed.is_full_text else "summary"
            word_count = len(raw.text.split())
            return f"  [{idx}/{len(items)}] OK ({mode}, {word_count}w): {filename}"
        except Exception as exc:
            return f"  [{idx}/{len(items)}] ERROR: {filename} — {exc}"

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_process_one, item): item for item in to_process}
        for future in as_completed(futures):
            print(future.result(), file=sys.stderr)

    print(f"\nDone. Output directory: {output_dir}", file=sys.stderr)
    print(
        f"\nNext: run post-ingest to update profile metadata:\n"
        f"  python scripts/post_ingest.py --investor {investor}\n",
        file=sys.stderr,
    )


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m ingestion",
        description="OpenAlpha ingestion pipeline — fetch, process, and render investor content.",
    )
    sub = parser.add_subparsers(dest="source_type", required=True)

    # --- Substack ---
    ss = sub.add_parser("substack", help="Ingest posts from a Substack newsletter")
    ss.add_argument("--url", required=True, help="Substack URL")
    ss.add_argument("--investor", default=None, help="Investor slug (auto-resolved from registry if omitted)")
    ss.add_argument("--source-name", default=None, help="Human-readable source name")
    ss.add_argument("--months", type=int, default=3, help="Months to look back (default: 3)")
    ss.add_argument("--model", default="gpt-5-mini", help="OpenAI model (default: gpt-5-mini)")
    ss.add_argument("--workers", type=int, default=5, help="Parallel workers (default: 5)")
    ss.add_argument("--dry-run", action="store_true", help="List posts without processing")
    ss.add_argument("--output-dir", default=None, help="Output directory")

    # --- YouTube ---
    yt = sub.add_parser("youtube", help="Extract transcript from a YouTube video")
    yt.add_argument("--url", required=True, help="YouTube video URL")
    yt.add_argument("--investor", required=True, help="Investor slug")
    yt.add_argument("--source-name", required=True, help="Source name (e.g. 'BG2Pod')")
    yt.add_argument("--date", required=True, help="Date in YYYY-MM-DD format")
    yt.add_argument("--title", default=None, help="Video title")
    yt.add_argument("--model", default="gpt-5-mini", help="OpenAI model")
    yt.add_argument("--dry-run", action="store_true", help="Fetch transcript without processing")
    yt.add_argument("--output-dir", default=None, help="Output directory")

    # --- Manual ---
    mn = sub.add_parser("manual", help="Ingest from a local file or stdin")
    mn.add_argument("--file", required=True, help="Path to text file, or '-' for stdin")
    mn.add_argument("--investor", required=True, help="Investor slug")
    mn.add_argument("--source-name", required=True, help="Source name")
    mn.add_argument("--date", required=True, help="Date in YYYY-MM-DD format")
    mn.add_argument("--type", dest="appearance_type", default="interview",
                     choices=["podcast", "substack", "interview", "conference", "tv", "twitter"],
                     help="Appearance type (default: interview)")
    mn.add_argument("--url", default="", help="Original source URL")
    mn.add_argument("--title", default=None, help="Content title")
    mn.add_argument("--model", default="gpt-5-mini", help="OpenAI model")
    mn.add_argument("--output-dir", default=None, help="Output directory")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.source_type == "substack":
        # Resolve investor from registry if not provided
        investor = args.investor
        source_name = args.source_name
        if not investor or not source_name:
            resolved = resolve_from_registry(args.url)
            if resolved:
                investor = investor or resolved[0]
                source_name = source_name or resolved[1]
            else:
                if not investor or not source_name:
                    print(
                        f"Error: '{args.url}' not found in registry.\n"
                        "Provide --investor and --source-name explicitly, or add it to\n"
                        "backend/data-ingestion/_registry.yaml",
                        file=sys.stderr,
                    )
                    sys.exit(1)

        run_ingest(
            source_type="substack",
            url=args.url,
            investor=investor,
            source_name=source_name,
            output_dir=Path(args.output_dir) if args.output_dir else None,
            dry_run=args.dry_run,
            model=args.model,
            workers=args.workers,
            months=args.months,
        )

    elif args.source_type == "youtube":
        run_ingest(
            source_type="youtube",
            url=args.url,
            investor=args.investor,
            source_name=args.source_name,
            output_dir=Path(args.output_dir) if args.output_dir else None,
            dry_run=args.dry_run,
            model=args.model,
            workers=1,
            date=args.date,
            title=args.title,
        )

    elif args.source_type == "manual":
        if args.date and not re.match(r"^\d{4}-\d{2}-\d{2}$", args.date):
            print(f"Error: Date must be YYYY-MM-DD, got: {args.date}", file=sys.stderr)
            sys.exit(1)

        run_ingest(
            source_type="manual",
            url=args.file,
            investor=args.investor,
            source_name=args.source_name,
            output_dir=Path(args.output_dir) if args.output_dir else None,
            dry_run=False,
            model=args.model,
            workers=1,
            date=args.date,
            title=args.title,
            source_url=args.url,
        )


if __name__ == "__main__":
    main()
