"""Substack extractor — fetches posts from a Substack newsletter via its API."""

from __future__ import annotations

import json
import re
import time
from datetime import datetime, timedelta
from html.parser import HTMLParser

import httpx

from ingestion.models import RawContent

from .base import BaseExtractor


class SubstackExtractor(BaseExtractor):
    """Fetch posts from a Substack newsletter."""

    @property
    def source_type(self) -> str:
        return "substack"

    def fetch(self, url: str, **kwargs) -> list[RawContent]:
        """Fetch posts from the Substack API.

        Kwargs:
            months: Number of months to look back (default: 3).
        """
        months = kwargs.get("months", 3)
        return fetch_substack_posts(url, months=months)


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
        self._block_tags = {
            "p", "div", "h1", "h2", "h3", "h4", "li", "br", "tr", "blockquote",
        }

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
        raw = re.sub(r"[ \t]+", " ", raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return raw.strip()

    def get_images(self) -> list[dict[str, str]]:
        return self._images


def html_to_text_and_images(html: str) -> tuple[str, list[dict[str, str]]]:
    """Convert HTML to readable plain text and extract image URLs."""
    parser = _HTMLToText()
    parser.feed(html)
    return parser.get_text(), parser.get_images()


# ---------------------------------------------------------------------------
# Substack API fetching
# ---------------------------------------------------------------------------


def fetch_substack_posts(substack_url: str, months: int = 3) -> list[RawContent]:
    """Fetch posts from a Substack using its API endpoint.

    Returns a list of RawContent items, one per post.
    """
    import sys

    base_url = substack_url.rstrip("/")
    cutoff = datetime.now() - timedelta(days=months * 30)
    posts: list[RawContent] = []
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

                post_date = datetime.fromisoformat(
                    post_date_str.replace("Z", "+00:00")
                )
                post_date_naive = post_date.replace(tzinfo=None)

                if post_date_naive < cutoff:
                    return posts

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
                    RawContent(
                        text=body_text,
                        title=item.get("title", "Untitled"),
                        date=post_date_naive.strftime("%Y-%m-%d"),
                        url=post_url,
                        source_type="substack",
                        images=images,
                        metadata={"slug": slug},
                    )
                )

            offset += limit
            time.sleep(0.5)  # Be polite to the API

    return posts
