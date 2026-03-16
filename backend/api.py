"""FastAPI backend for OpenAlpha — thin layer over the agent engine."""

from __future__ import annotations

import json
import logging
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from src.agent import Agent, ContentEvent, ContentReplaceEvent, SourcesEvent, StatusEvent
from src.config import get_settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class ChatMessage(BaseModel):
    """A single message in conversation history."""

    role: str  # "user" or "assistant"
    content: str


class AnalyzeRequest(BaseModel):
    """Request body for the /analyze endpoint."""

    question: str = Field(..., min_length=1, max_length=2000, description="Research question to analyze")
    history: list[ChatMessage] = Field(default_factory=list, description="Previous conversation messages for follow-ups")


class InvestorSummary(BaseModel):
    """Short summary returned in investor listings."""

    name: str
    slug: str
    fund: str
    role: str
    topics: list[str] = []
    companies: list[str] = []
    last_updated: str = ""


class AppearanceMeta(BaseModel):
    """Metadata for a single investor appearance (no full content)."""

    title: str = ""
    source: str = ""
    date: str = ""
    file: str = ""


class InvestorDetail(BaseModel):
    """Full profile data for a single investor."""

    name: str
    slug: str
    fund: str
    role: str
    topics: list[str] = []
    companies: list[str] = []
    last_updated: str = ""
    content: str = ""
    appearances: list[AppearanceMeta] = []


class EntityRanking(BaseModel):
    """A ranked entity (company ticker or sector) by mention count."""

    name: str
    kind: str  # "company" or "topic"
    count: int = 0  # number of appearances mentioning this entity
    investor_count: int = 0  # number of distinct investors mentioning it


class EntitiesResponse(BaseModel):
    """Ranked entities from recent appearances."""

    companies: list[EntityRanking] = []
    topics: list[EntityRanking] = []


class ErrorResponse(BaseModel):
    """Standard error envelope."""

    detail: str


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PROFILES_DIR = Path(__file__).resolve().parent.parent / "investors"


def _parse_profile_frontmatter(path: Path) -> dict | None:
    """Parse YAML frontmatter from a markdown profile file.

    Returns the frontmatter dict or None if the file cannot be parsed.
    """
    try:
        import frontmatter  # python-frontmatter

        post = frontmatter.load(str(path))
        meta: dict = dict(post.metadata)
        meta["_content"] = post.content
        return meta
    except Exception:
        logger.warning("Failed to parse profile: %s", path)
        return None


def _scan_profiles() -> list[dict]:
    """Return a list of parsed frontmatter dicts for every investor profile."""
    if not PROFILES_DIR.is_dir():
        return []
    profiles: list[dict] = []
    for md in sorted(PROFILES_DIR.glob("*/profile.md")):
        meta = _parse_profile_frontmatter(md)
        if meta:
            profiles.append(meta)
    return profiles


def _find_profile(slug: str) -> dict | None:
    """Find a single investor profile by slug."""
    profile_path = PROFILES_DIR / slug / "profile.md"
    if profile_path.is_file():
        return _parse_profile_frontmatter(profile_path)
    # Fallback: scan all profiles and match by slug field
    for meta in _scan_profiles():
        if meta.get("slug") == slug:
            return meta
    return None


def _find_appearances(slug: str) -> list[AppearanceMeta]:
    """Return metadata for all appearances filed under an investor slug."""
    appearances_dir = PROFILES_DIR / slug / "appearances"
    if not appearances_dir.is_dir():
        return []
    results: list[AppearanceMeta] = []
    for md in sorted(appearances_dir.glob("*.md")):
        meta = _parse_profile_frontmatter(md)
        if meta:
            results.append(
                AppearanceMeta(
                    title=meta.get("title", md.stem),
                    source=meta.get("source", ""),
                    date=str(meta.get("date", "")),
                    file=md.name,
                )
            )
    return results


def _meta_to_summary(meta: dict) -> InvestorSummary:
    """Convert raw frontmatter dict to an InvestorSummary."""
    return InvestorSummary(
        name=meta.get("name", ""),
        slug=meta.get("slug", ""),
        fund=meta.get("fund", ""),
        role=meta.get("role", ""),
        topics=meta.get("topics", []) or meta.get("sectors", []) or [],
        companies=meta.get("companies", []) or [],
        last_updated=str(meta.get("last_updated", "")),
    )


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title="OpenAlpha API",
    version="0.1.0",
    description="AI-powered investor research engine",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev — lock down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.post(
    "/analyze",
    summary="Analyze a research question",
    response_description="SSE stream of status updates and LLM tokens",
)
async def analyze(req: AnalyzeRequest) -> StreamingResponse:
    """Stream an LLM-powered analysis for *req.question*.

    The response is an SSE text/event-stream.  Each ``data:`` frame contains
    a JSON object.  Two event types:

    - ``{"type": "status", "phase": "...", "detail": "...", "progress": "..."}``
      — pipeline progress (collapsible in UI)
    - ``{"type": "token", "token": "..."}``
      — chunk of the final answer text

    The stream ends with a ``data: [DONE]`` sentinel.
    """

    async def _event_stream() -> AsyncGenerator[str, None]:
        try:
            agent = Agent()
            history = [{"role": m.role, "content": m.content} for m in req.history]
            stream = (
                agent.follow_up_stream(req.question, history)
                if history
                else agent.query_stream(req.question)
            )
            async for event in stream:
                if isinstance(event, StatusEvent):
                    payload = json.dumps({
                        "type": "status",
                        "phase": event.phase,
                        "detail": event.detail,
                        "progress": event.progress,
                    })
                elif isinstance(event, ContentEvent):
                    payload = json.dumps({
                        "type": "token",
                        "token": event.token,
                    })
                elif isinstance(event, ContentReplaceEvent):
                    payload = json.dumps({
                        "type": "content_replace",
                        "content": event.content,
                    })
                elif isinstance(event, SourcesEvent):
                    payload = json.dumps({
                        "type": "sources",
                        "sources": event.sources,
                    })
                else:
                    continue
                yield f"data: {payload}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as exc:
            logger.exception("Streaming error")
            error_payload = json.dumps({"type": "error", "detail": str(exc)})
            yield f"data: {error_payload}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        _event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get(
    "/investors",
    response_model=list[InvestorSummary],
    summary="List all tracked investors",
)
async def list_investors() -> list[InvestorSummary]:
    """Scan investor profile frontmatter and return a summary for each."""
    profiles = _scan_profiles()
    if not profiles:
        return []
    return [_meta_to_summary(p) for p in profiles]


@app.get(
    "/investors/{slug}",
    response_model=InvestorDetail,
    responses={404: {"model": ErrorResponse}},
    summary="Get a single investor profile",
)
async def get_investor(slug: str) -> InvestorDetail:
    """Return full profile data and appearance metadata for *slug*."""
    meta = _find_profile(slug)
    if meta is None:
        raise HTTPException(status_code=404, detail=f"Investor '{slug}' not found")

    appearances = _find_appearances(slug)

    return InvestorDetail(
        name=meta.get("name", ""),
        slug=meta.get("slug", slug),
        fund=meta.get("fund", ""),
        role=meta.get("role", ""),
        topics=meta.get("topics", []) or meta.get("sectors", []) or [],
        companies=meta.get("companies", []) or [],
        last_updated=str(meta.get("last_updated", "")),
        content=meta.get("_content", ""),
        appearances=appearances,
    )


@app.get(
    "/entities",
    response_model=EntitiesResponse,
    summary="Ranked entities from recent investor appearances",
)
async def get_entities(months: int = 6) -> EntitiesResponse:
    """Aggregate companies and topics from appearance frontmatter.

    Only appearances within the last *months* months are counted.
    Each appearance file counts as one mention regardless of how many
    times the entity appears in the content.
    """
    cutoff = date.today() - timedelta(days=months * 30)
    company_counts: Counter[str] = Counter()
    topic_counts: Counter[str] = Counter()
    # Track which investors mention each entity
    company_investors: dict[str, set[str]] = {}
    topic_investors: dict[str, set[str]] = {}

    if not PROFILES_DIR.is_dir():
        return EntitiesResponse()

    for md in PROFILES_DIR.glob("*/appearances/*.md"):
        meta = _parse_profile_frontmatter(md)
        if not meta:
            continue
        raw_date = meta.get("date")
        if not raw_date:
            continue
        try:
            appearance_date = date.fromisoformat(str(raw_date)[:10])
        except ValueError:
            continue
        if appearance_date < cutoff:
            continue

        investor_slug = meta.get("investor", md.parts[-3] if len(md.parts) >= 3 else "")

        for ticker in meta.get("companies", []) or []:
            key = ticker.upper()
            company_counts[key] += 1
            company_investors.setdefault(key, set()).add(investor_slug)
        # Read both 'topics' (new) and 'sectors' (legacy)
        all_tags = list(meta.get("topics", []) or []) + list(meta.get("sectors", []) or [])
        for tag in all_tags:
            key = tag.lower()
            topic_counts[key] += 1
            topic_investors.setdefault(key, set()).add(investor_slug)

    companies = [
        EntityRanking(
            name=name,
            kind="company",
            count=count,
            investor_count=len(company_investors.get(name, set())),
        )
        for name, count in company_counts.most_common(20)
    ]
    topics = [
        EntityRanking(
            name=name,
            kind="topic",
            count=count,
            investor_count=len(topic_investors.get(name, set())),
        )
        for name, count in topic_counts.most_common(20)
    ]

    return EntitiesResponse(companies=companies, topics=topics)


# ---------------------------------------------------------------------------
# Dev entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import os

    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True)
