"""Generate appearance.md files from a Substack newsletter.

Fetches posts from a Substack archive, extracts content, and uses an LLM
with structured output to produce appearance markdown files.

Usage:
    # Auto-resolve investor from registry:
    python data-ingestion/substack.py --url https://robonomics.substack.com --months 6

    # Explicit investor (skips registry lookup):
    python data-ingestion/substack.py --url https://robonomics.substack.com \\
        --investor freda-duan --source-name Robonomics --months 3

    # Dry run — list posts without calling the LLM:
    python data-ingestion/substack.py --url https://robonomics.substack.com --months 3 --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timedelta
from html.parser import HTMLParser
from pathlib import Path
from textwrap import shorten

import httpx
import yaml

# Ensure the backend package is importable when running as a script
_BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BACKEND_DIR))

from src.appearance import (
    COMPRESS_ABOVE_WORDS,
    AppearanceIndex,
    AppearanceSummary,
    describe_images,
    extract_index,
    render_markdown,
    render_markdown_full,
    summarize_text,
)
from src.config import get_settings

_REGISTRY_PATH = Path(__file__).resolve().parent / "_registry.yaml"


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


def load_registry() -> dict[str, dict]:
    """Load _registry.yaml and return a dict keyed by normalized URL."""
    if not _REGISTRY_PATH.exists():
        return {}
    data = yaml.safe_load(_REGISTRY_PATH.read_text())
    return {
        entry["url"].rstrip("/"): entry
        for entry in data.get("substacks", [])
    }


def resolve_from_registry(
    url: str,
) -> tuple[str, str] | None:
    """Look up investor slug and source_name for a Substack URL.

    Returns (investor, source_name) or None if not found.
    """
    registry = load_registry()
    entry = registry.get(url.rstrip("/"))
    if entry:
        return entry["investor"], entry["source_name"]
    return None


# ---------------------------------------------------------------------------
# HTML → plain text converter (stdlib-only, no BeautifulSoup needed)
# ---------------------------------------------------------------------------


class _HTMLToText(HTMLParser):
    """HTML→text converter that preserves paragraph structure and extracts images."""

    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._images: list[dict[str, str]] = []
        self._skip = False
        self._block_tags = {"p", "div", "h1", "h2", "h3", "h4", "li", "br", "tr", "blockquote"}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style", "noscript"):
            self._skip = True
        if tag in self._block_tags:
            self._chunks.append("\n")
        if tag == "br":
            self._chunks.append("\n")
        if tag == "img":
            attr_dict = dict(attrs)
            src = attr_dict.get("src", "")
            alt = attr_dict.get("alt", "")

            # Prefer the original S3 URL from data-attrs (Substack CDN URLs
            # contain tokens that may not be accessible to the vision API)
            data_attrs_str = attr_dict.get("data-attrs", "")
            if data_attrs_str:
                try:
                    data_attrs = json.loads(data_attrs_str)
                    original_src = data_attrs.get("src", "")
                    if original_src:
                        src = original_src
                except (json.JSONDecodeError, TypeError):
                    pass

            if src:
                self._images.append({"url": src, "alt": alt or ""})
                # Leave a placeholder so the summarizer knows an image was here
                self._chunks.append(f"\n[IMAGE: {alt or 'chart/figure'}]\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "noscript"):
            self._skip = False
        if tag in self._block_tags:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip:
            self._chunks.append(data)

    def get_text(self) -> str:
        raw = "".join(self._chunks)
        # Collapse excessive whitespace while preserving paragraph breaks
        raw = re.sub(r"[ \t]+", " ", raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return raw.strip()

    def get_images(self) -> list[dict[str, str]]:
        return self._images


def html_to_text_and_images(html: str) -> tuple[str, list[dict[str, str]]]:
    """Convert HTML to readable plain text and extract image URLs.

    Returns:
        Tuple of (text, images) where images is a list of dicts with 'url' and 'alt'.
    """
    parser = _HTMLToText()
    parser.feed(html)
    return parser.get_text(), parser.get_images()


# ---------------------------------------------------------------------------
# Substack data fetching
# ---------------------------------------------------------------------------


def fetch_substack_posts(
    substack_url: str,
    months: int = 3,
) -> list[dict]:
    """Fetch posts from a Substack using its API endpoint.

    Returns a list of dicts with keys: title, date, url, body_text, images.
    """
    base_url = substack_url.rstrip("/")
    cutoff = datetime.now() - timedelta(days=months * 30)
    posts: list[dict] = []
    offset = 0
    limit = 25

    with httpx.Client(timeout=30, follow_redirects=True) as client:
        while True:
            api_url = f"{base_url}/api/v1/posts?limit={limit}&offset={offset}"
            print(f"  Fetching {api_url} ...", file=sys.stderr)
            resp = client.get(api_url)
            resp.raise_for_status()
            items = resp.json()

            if not items:
                break

            for item in items:
                post_date_str = item.get("post_date", "")
                if not post_date_str:
                    continue

                # Parse ISO date (e.g. "2026-03-12T16:02:30.000Z")
                post_date = datetime.fromisoformat(
                    post_date_str.replace("Z", "+00:00")
                )
                post_date_naive = post_date.replace(tzinfo=None)

                if post_date_naive < cutoff:
                    # Posts are in reverse chronological order — we're done
                    return posts

                # Extract body text and images from HTML
                body_html = item.get("body_html", "")
                if body_html:
                    body_text, images = html_to_text_and_images(body_html)
                else:
                    body_text, images = "", []

                if not body_text.strip():
                    print(
                        f"  Skipping '{item.get('title', '?')}' — no body text",
                        file=sys.stderr,
                    )
                    continue

                slug = item.get("slug", "")
                post_url = f"{base_url}/p/{slug}" if slug else ""

                posts.append(
                    {
                        "title": item.get("title", "Untitled"),
                        "date": post_date_naive.strftime("%Y-%m-%d"),
                        "url": post_url,
                        "slug": slug,
                        "body_text": body_text,
                        "images": images,
                    }
                )

            offset += limit
            time.sleep(0.5)  # Be polite to the API

    return posts


# ---------------------------------------------------------------------------
# Filename generation
# ---------------------------------------------------------------------------


def slugify(text: str) -> str:
    """Convert a title to a filename-safe slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)  # Remove non-alphanumeric
    text = re.sub(r"[\s_]+", "-", text)  # Spaces/underscores → hyphens
    text = re.sub(r"-+", "-", text)  # Collapse multiple hyphens
    return text.strip("-")[:60]


def make_filename(date: str, title: str, source_name: str) -> str:
    """Generate appearance filename: YYYY-MM-DD-source-slug.md"""
    source_slug = slugify(source_name)
    title_slug = slugify(title)
    return f"{date}-{source_slug}-{title_slug}.md"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate appearance files from a Substack newsletter.",
    )
    parser.add_argument(
        "--url",
        required=True,
        help="Substack URL, e.g. https://robonomics.substack.com",
    )
    parser.add_argument(
        "--investor",
        default=None,
        help="Investor slug (auto-resolved from registry if omitted)",
    )
    parser.add_argument(
        "--source-name",
        default=None,
        help="Human-readable source name (auto-resolved from registry if omitted)",
    )
    parser.add_argument(
        "--months",
        type=int,
        default=3,
        help="Number of months to look back (default: 3)",
    )
    parser.add_argument(
        "--model",
        default="gpt-5-mini",
        help="OpenAI model to use (default: gpt-5-mini)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List posts that would be processed without calling the LLM",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory. Defaults to investors/<slug>/appearances/",
    )
    args = parser.parse_args()

    # Resolve investor and source_name
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
                    f"Error: '{args.url}' not found in registry ({_REGISTRY_PATH}).\n"
                    f"\n"
                    f"Either add it to {_REGISTRY_PATH.name}:\n"
                    f"\n"
                    f"  - url: {args.url}\n"
                    f"    investor: <investor-slug>\n"
                    f"    source_name: <Newsletter Name>\n"
                    f"\n"
                    f"Or provide --investor and --source-name explicitly.",
                    file=sys.stderr,
                )
                sys.exit(1)

    # Resolve output directory
    project_root = Path(__file__).resolve().parent.parent.parent
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = project_root / "investors" / investor / "appearances"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Fetch posts
    print(f"Fetching posts from {args.url} (last {args.months} months)...", file=sys.stderr)
    posts = fetch_substack_posts(args.url, months=args.months)
    print(f"Found {len(posts)} posts.", file=sys.stderr)

    if not posts:
        print("No posts found in the specified date range.", file=sys.stderr)
        sys.exit(0)

    # List posts
    for i, post in enumerate(posts, 1):
        preview = shorten(post["title"], width=60, placeholder="...")
        print(f"  {i}. [{post['date']}] {preview}", file=sys.stderr)

    if args.dry_run:
        print("\nDry run — no files generated.", file=sys.stderr)
        sys.exit(0)

    # Get API key
    settings = get_settings()
    api_key = settings.openai_api_key
    if not api_key:
        print("Error: OPENAI_API_KEY not set in .env", file=sys.stderr)
        sys.exit(1)

    # Process each post
    print(f"\nGenerating appearances with {args.model}...", file=sys.stderr)
    for i, post in enumerate(posts, 1):
        filename = make_filename(post["date"], post["title"], source_name)
        filepath = output_dir / filename

        if filepath.exists():
            print(f"  [{i}/{len(posts)}] SKIP (exists): {filename}", file=sys.stderr)
            continue

        print(
            f"  [{i}/{len(posts)}] Processing: {post['title']} ({post['date']})...",
            file=sys.stderr,
        )

        try:
            source_length = len(post["body_text"].split())
            fetch_method = "substack_api"
            fetch_id = post.get("slug", "")

            if source_length <= COMPRESS_ABOVE_WORDS:
                # Short source: extract index only, keep full text
                print(
                    f"           Mode: full-text ({source_length} words < {COMPRESS_ABOVE_WORDS})",
                    file=sys.stderr,
                )
                index: AppearanceIndex = extract_index(
                    text=post["body_text"],
                    investor=investor,
                    date=post["date"],
                    source=source_name,
                    appearance_type="substack",
                    url=post["url"],
                    api_key=api_key,
                    model=args.model,
                )

                md = render_markdown_full(
                    index=index,
                    full_text=post["body_text"],
                    investor=investor,
                    date=post["date"],
                    source=source_name,
                    appearance_type="substack",
                    url=post["url"],
                    source_length=source_length,
                    fetch_method=fetch_method,
                    fetch_id=fetch_id,
                )
            else:
                # Long source: describe images + full structured summary
                print(
                    f"           Mode: summary ({source_length} words > {COMPRESS_ABOVE_WORDS})",
                    file=sys.stderr,
                )
                image_descriptions: list[dict[str, str]] = []
                if post.get("images"):
                    print(
                        f"           Describing {len(post['images'])} image(s)...",
                        file=sys.stderr,
                    )
                    image_descriptions = describe_images(
                        post["images"],
                        api_key=api_key,
                        model=args.model,
                    )
                    print(
                        f"           {len(image_descriptions)} chart(s) identified.",
                        file=sys.stderr,
                    )

                summary: AppearanceSummary = summarize_text(
                    text=post["body_text"],
                    investor=investor,
                    date=post["date"],
                    source=source_name,
                    appearance_type="substack",
                    url=post["url"],
                    api_key=api_key,
                    model=args.model,
                    image_descriptions=image_descriptions,
                )

                md = render_markdown(
                    summary=summary,
                    investor=investor,
                    date=post["date"],
                    source=source_name,
                    appearance_type="substack",
                    url=post["url"],
                    source_length=source_length,
                    fetch_method=fetch_method,
                    fetch_id=fetch_id,
                )

            filepath.write_text(md + "\n", encoding="utf-8")
            print(f"           Written: {filename}", file=sys.stderr)

            # Brief pause between API calls
            time.sleep(1)

        except Exception as exc:
            print(f"           ERROR: {exc}", file=sys.stderr)
            continue

    print(f"\nDone. Output directory: {output_dir}", file=sys.stderr)
    print(
        f"\nNext: run post-ingest to update profile metadata and INVESTORS.md:\n"
        f"  python scripts/post_ingest.py --investor {investor}\n",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
