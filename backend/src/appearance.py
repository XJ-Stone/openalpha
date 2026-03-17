"""Shared Pydantic models, LLM summarization, and markdown rendering for appearances.

This module is source-agnostic — it takes raw text and metadata, and produces
structured summaries that render to appearance markdown files.
"""

from __future__ import annotations

from typing import Literal

import openai
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Pydantic models (used as OpenAI structured output schema)
# ---------------------------------------------------------------------------


class ChartReference(BaseModel):
    """A chart or image from the source that adds analytical value."""

    url: str = Field(description="Direct URL to the chart/image")
    description: str = Field(
        description=(
            "Detailed description of what the chart shows: axes, data series, "
            "key takeaways, and specific numbers visible in the chart."
        )
    )


class CompanyView(BaseModel):
    """A view on a specific company (public or private)."""

    ticker: str = Field(
        description=(
            "Standard ticker symbol for public companies (e.g. NVDA, MSFT, SNOW). "
            "For private companies, use the company name in uppercase (e.g. OPENAI, "
            "ANTHROPIC, STRIPE)."
        )
    )
    company_name: str = Field(description="Full company name, e.g. NVIDIA, Microsoft, OpenAI")
    focus: Literal["primary", "secondary", "mention"] = Field(
        description=(
            "primary = the report is substantially about this company (deep analysis, "
            "dedicated section, or central to the thesis); "
            "secondary = meaningful discussion but not the main focus; "
            "mention = referenced for comparison, context, or in passing"
        )
    )
    sentiment: Literal["Bullish", "Bearish", "Neutral", "Mixed"] = Field(
        description="Overall sentiment expressed toward this company"
    )
    conviction: Literal["HIGH", "MEDIUM", "MENTIONED"] = Field(
        description=(
            "HIGH = explicitly states position or strong recommendation; "
            "MEDIUM = clear opinion but no position confirmation; "
            "MENTIONED = referenced in passing or as supporting example"
        )
    )
    analysis: str = Field(
        description=(
            "Dense paragraph (3-8 sentences) distilling the investor's view: "
            "thesis, key evidence, specific numbers/metrics (exact — never round), "
            "one strong direct quote if memorable, catalysts, and risks. "
            "Cut filler, repetition, and setup — keep only what an analyst needs."
        )
    )
    charts: list[ChartReference] = Field(
        default_factory=list,
        description=(
            "Charts or images from the source that are directly relevant to this "
            "company view. Only include charts that add analytical value — data "
            "visualizations, financial comparisons, growth charts, etc."
        ),
    )


class TopicView(BaseModel):
    """A non-company-specific perspective: macro argument, thematic call, sector view,
    market observation, or any other insight not tied to a single ticker."""

    topic: str = Field(
        description="Concise topic label, 2-4 words, lowercase-hyphenated"
    )
    focus: Literal["primary", "secondary", "mention"] = Field(
        description=(
            "primary = central thesis of the piece; "
            "secondary = meaningfully discussed but not the core thesis; "
            "mention = referenced briefly for context"
        )
    )
    analysis: str = Field(
        description=(
            "Dense paragraph (3-8 sentences) distilling the investor's argument: "
            "core claim, supporting evidence, specific numbers/metrics (exact — "
            "never round), one direct quote if memorable, implications, and risks. "
            "Cut filler, repetition, and setup — keep only what an analyst needs."
        )
    )
    charts: list[ChartReference] = Field(
        default_factory=list,
        description=(
            "Charts or images from the source that are directly relevant to this "
            "topic. Only include charts that add analytical value — data "
            "visualizations, comparisons, trend charts, etc."
        ),
    )


class AppearanceSummary(BaseModel):
    """Structured extraction from a single investor appearance or publication."""

    companies: list[CompanyView] = Field(
        default_factory=list,
        description=(
            "Company-specific views. Include every company the investor analyzes, "
            "expresses an opinion on, or references for comparison — set the "
            "appropriate focus level (primary/secondary/mention) for each."
        ),
    )
    topics: list[TopicView] = Field(
        default_factory=list,
        description=(
            "Non-company-specific perspectives: macro arguments, thematic calls, "
            "sector views, market observations, geographic analyses, or any other "
            "viewpoint not tied to a single ticker. Each topic has a focus level."
        ),
    )


# ---------------------------------------------------------------------------
# Lightweight index model (for short sources kept verbatim)
# ---------------------------------------------------------------------------


class CompanyMention(BaseModel):
    """Lightweight company mention for indexing — no analysis text."""

    ticker: str = Field(
        description=(
            "Standard ticker symbol for public companies (e.g. NVDA, MSFT). "
            "For private companies, use uppercase name (e.g. OPENAI, STRIPE)."
        )
    )
    company_name: str = Field(description="Full company name")
    focus: Literal["primary", "secondary", "mention"] = Field(
        description=(
            "primary = the report is substantially about this company; "
            "secondary = meaningful discussion but not the main focus; "
            "mention = referenced for comparison or in passing"
        )
    )


class TopicMention(BaseModel):
    """Lightweight topic mention for indexing — no analysis text."""

    topic: str = Field(description="Concise topic label, 2-4 words, lowercase-hyphenated")
    focus: Literal["primary", "secondary", "mention"] = Field(
        description=(
            "primary = central thesis of the piece; "
            "secondary = meaningfully discussed but not the core thesis; "
            "mention = referenced briefly for context"
        )
    )


class AppearanceIndex(BaseModel):
    """Lightweight metadata extraction for short sources kept verbatim."""

    companies: list[CompanyMention] = Field(
        default_factory=list,
        description=(
            "Companies the investor analyzes, expresses an opinion on, or "
            "references for comparison. Set focus level for each."
        ),
    )
    topics: list[TopicMention] = Field(
        default_factory=list,
        description=(
            "Non-company-specific topics discussed: macro arguments, thematic "
            "calls, sector views, market observations. Each has a focus level."
        ),
    )


# ---------------------------------------------------------------------------
# System prompt for LLM extraction
# ---------------------------------------------------------------------------

EXTRACTION_SYSTEM_PROMPT = """\
You are an expert financial analyst assistant. Your job is to produce a STRUCTURED \
SUMMARY of investor opinions from a written publication or transcript.

## Compression target
Your total output must be 30-40% of the source text length. This is a DISTILLATION, \
not a rewrite. Sources range from short newsletters (~1,500 words) to long podcast \
transcripts (~10,000+ words). For short, already-dense sources the ratio may reach \
~50%; for verbose transcripts aim for ~25-30%.

Each analysis field should be a dense paragraph of 3-8 sentences. If you cannot say \
something in 3-8 sentences, you are not summarizing — you are copying.

## What to CUT
- Repetition (podcasts often say the same thing multiple ways)
- Setup and context the reader already knows ("as we all know, NVIDIA makes GPUs...")
- Interviewer questions, pleasantries, transitions
- Hedging language and filler ("I think it's really interesting that...")
- Meta-commentary about the article itself, disclaimers, boilerplate

## What to KEEP
- The investor's thesis and reasoning chain (compressed, not fragmented)
- ALL specific numbers: dollar figures, percentages, growth rates, multiples, \
user counts, margins, revenue, dates — use exact figures, never round
- One strong direct quote per view if the investor says something memorable
- Catalysts, risks, and conditions stated by the investor
- Image/chart references that add analytical value

## CompanyView
Include companies that are subjects of investment analysis, opinion, comparison, or \
used as examples to illustrate an investment thesis. For public companies use standard \
tickers (NVDA, MSFT, META). For private companies use a clean uppercase name (OPENAI, \
ANTHROPIC, STRIPE — no legal suffixes like Inc, LP, Ltd). \
For subsidiaries or divisions, use the parent company ticker (e.g. Volcano Engine → BYTEDANCE).

Do NOT include research firms, data providers, news outlets, consulting firms, \
investment funds, or hedge funds — these are sources, not subjects.

## TopicView
Use for perspectives not tied to a single company: macro arguments, thematic calls, \
sector views, market observations, geographic analyses, frameworks. \
Each topic gets a focus level. Do NOT repeat information already in a CompanyView. \
TopicViews add cross-cutting or non-company-specific insight only.

## Focus levels (applies to both companies and topics)
- primary: the piece deeply analyzes this subject (dedicated section, financials, core thesis)
- secondary: meaningful discussion but not the central subject
- mention: named as an example, comparison, or historical reference without analysis

## Images
When the source includes images (marked as [IMAGE: ...] with descriptions), attach \
them to the relevant CompanyView or TopicView if the image provides analytical value \
(charts, data visualizations, tables, diagrams). Skip decorative images.

## Topic rules
- 3-5 topics per piece, each 2-4 words, lowercase-hyphenated.
- Topics should help an analyst find this piece when researching an investment theme.
- Specific enough to distinguish from other investor commentary.
  Good: "agentic-commerce", "china-token-economy", "ride-hailing-competition"
  Bad: "ai", "gen-ai", "macro", "technology", "markets", "investing"
- Each topic must be semantically distinct — no overlapping or near-duplicate topics.
- When an existing topics list is provided, REUSE existing topics where semantically \
equivalent. Only create a new topic if nothing in the list fits.

## Rules
- Only extract views actually expressed — do not infer or editorialize
- Every claim must be traceable to the source text
- State each point ONCE across all CompanyViews and TopicViews — zero redundancy
"""


# ---------------------------------------------------------------------------
# Index-only prompt (for short sources — extract metadata, skip analysis)
# ---------------------------------------------------------------------------

INDEX_SYSTEM_PROMPT = """\
You are an expert financial analyst assistant. Your job is to extract STRUCTURED \
METADATA from a publication — companies discussed and topics.

You are NOT writing a summary. The full text will be kept verbatim. You are only \
extracting searchable index fields.

## CompanyMention
Include companies that are subjects of investment analysis, opinion, comparison, or \
used as examples to illustrate an investment thesis. For public companies use standard \
tickers (NVDA, MSFT, META). For private companies use a clean uppercase name (OPENAI, \
ANTHROPIC, STRIPE — no legal suffixes like Inc, LP, Ltd). \
For subsidiaries or divisions, use the parent company ticker (e.g. Volcano Engine → BYTEDANCE).

Do NOT include research firms, data providers, news outlets, consulting firms, \
investment funds, or hedge funds — these are sources, not subjects.

## TopicMention
Create one for each non-company-specific perspective: macro arguments, thematic calls, \
sector views, market observations, geographic analyses, frameworks. \
Each topic gets a focus level.

## Focus levels (applies to both companies and topics)
- primary: the piece deeply analyzes this subject (dedicated section, financials, core thesis)
- secondary: meaningful discussion but not the central subject
- mention: named as an example, comparison, or historical reference without analysis

## Topic rules
- 3-5 topics per piece, each 2-4 words, lowercase-hyphenated.
- Topics should help an analyst find this piece when researching an investment theme.
- Specific enough to distinguish from other investor commentary.
  Good: "agentic-commerce", "china-token-economy", "ride-hailing-competition"
  Bad: "ai", "gen-ai", "macro", "technology", "markets", "investing"
- Each topic must be semantically distinct — no overlapping or near-duplicate topics.
- When an existing topics list is provided, REUSE existing topics where semantically \
equivalent. Only create a new topic if nothing in the list fits.

## Rules
- Only extract views actually expressed — do not infer
"""

# Threshold: sources below this word count keep full text; above get compressed
COMPRESS_ABOVE_WORDS = 3000


# ---------------------------------------------------------------------------
# Ticker validation
# ---------------------------------------------------------------------------


class TickerCorrection(BaseModel):
    """A single ticker correction."""

    original: str = Field(description="The original ticker/name as extracted")
    corrected: str = Field(
        description=(
            "The corrected value. Standard ticker for public companies "
            "(e.g. SNOW, CRM, PLTR). Original value unchanged for private "
            "companies or if already correct."
        )
    )


class TickerValidationResult(BaseModel):
    """Result of validating a batch of extracted tickers."""

    corrections: list[TickerCorrection] = Field(
        description="One entry per input ticker. Return ALL tickers, not just changed ones."
    )


TICKER_VALIDATION_PROMPT = """\
You are a financial data quality assistant. You will receive a list of company \
identifiers extracted from an investor publication.

Your job: for each identifier, determine if it refers to a publicly traded company. \
If it does, return the standard stock ticker (e.g. SNOW for Snowflake, CRM for \
Salesforce, CRWD for CrowdStrike, PLTR for Palantir, UBER for Uber).

If the company is private (not publicly traded on any major exchange), return the \
identifier unchanged.

If the identifier is already a correct ticker, return it unchanged.

IMPORTANT: Do NOT guess. If you are unsure whether a company is public or what its \
ticker is, return the original value unchanged. It is much better to leave a wrong \
name than to introduce a wrong ticker.

Return one entry per input ticker, in the same order."""


def validate_tickers(
    tickers: list[str],
    *,
    api_key: str,
    model: str = "gpt-5-mini",
) -> dict[str, str]:
    """Validate extracted tickers and return a mapping of original → corrected.

    Only public companies with wrong identifiers get corrected.
    Private companies and already-correct tickers pass through unchanged.
    """
    if not tickers:
        return {}

    client = openai.OpenAI(api_key=api_key)

    user_prompt = (
        "Validate these company identifiers:\n\n"
        + "\n".join(f"- {t}" for t in tickers)
    )

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": TICKER_VALIDATION_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format=TickerValidationResult,
    )

    result = completion.choices[0].message.parsed
    if result is None:
        return {t: t for t in tickers}

    return {c.original: c.corrected for c in result.corrections}


def _apply_ticker_corrections(
    companies: list,
    corrections: dict[str, str],
) -> None:
    """Apply ticker corrections in-place to a list of CompanyView or CompanyMention."""
    for company in companies:
        original = company.ticker
        corrected = corrections.get(original, original)
        if corrected != original:
            company.ticker = corrected


# ---------------------------------------------------------------------------
# Image/chart description via vision model
# ---------------------------------------------------------------------------


def describe_images(
    image_urls: list[dict[str, str]],
    *,
    api_key: str,
    model: str = "gpt-5-mini",
) -> list[dict[str, str]]:
    """Send images to a vision-capable model and return text descriptions.

    Args:
        image_urls: List of dicts with 'url' and optionally 'alt' keys.
        api_key: OpenAI API key.
        model: Vision-capable model to use.

    Returns:
        List of dicts with 'url' and 'description' keys.
    """
    if not image_urls:
        return []

    client = openai.OpenAI(api_key=api_key)
    results: list[dict[str, str]] = []

    for img in image_urls:
        url = img["url"]
        alt = img.get("alt", "")

        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "Describe this image from a financial newsletter. "
                                    "If it's a chart/graph: describe the type, axes, data "
                                    "series, specific numbers/values, trends, and takeaway. "
                                    "If it's a table/comparison: describe rows, columns, "
                                    "and key data points. "
                                    "If it's a screenshot or diagram: describe what it shows "
                                    "and any relevant details. "
                                    "If it's purely decorative (logo, author photo, generic "
                                    "stock photo, newsletter banner), just say 'DECORATIVE'."
                                    + (f"\n\nAlt text hint: {alt}" if alt else "")
                                ),
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": url},
                            },
                        ],
                    }
                ],
                max_completion_tokens=2000,
            )

            description = resp.choices[0].message.content or ""
            if "DECORATIVE" not in description:
                results.append({"url": url, "description": description.strip()})

        except Exception:
            # Skip images that fail (broken URLs, access denied, etc.)
            continue

    return results


# ---------------------------------------------------------------------------
# LLM summarization
# ---------------------------------------------------------------------------


def summarize_text(
    text: str,
    investor: str,
    date: str,
    source: str,
    appearance_type: str,
    url: str,
    *,
    api_key: str,
    model: str = "gpt-5-mini",
    image_descriptions: list[dict[str, str]] | None = None,
    existing_topics: list[str] | None = None,
) -> AppearanceSummary:
    """Send raw text to OpenAI with structured output and return an AppearanceSummary.

    Args:
        image_descriptions: Optional list of dicts with 'url' and 'description' keys
            for charts/images found in the source.
    """
    client = openai.OpenAI(api_key=api_key)

    # Enrich text with chart descriptions
    enriched_text = text
    if image_descriptions:
        chart_section = "\n\n--- CHARTS/IMAGES FROM THIS PUBLICATION ---\n"
        for i, img in enumerate(image_descriptions, 1):
            chart_section += (
                f"\n[CHART {i}] URL: {img['url']}\n"
                f"Description: {img['description']}\n"
            )
        enriched_text = text + chart_section

    topics_hint = ""
    if existing_topics:
        topics_hint = (
            f"\n\nExisting topics (reuse when semantically equivalent):\n"
            f"{', '.join(existing_topics)}\n"
        )

    user_prompt = (
        f"Extract structured investor opinions from the following publication.\n\n"
        f"Metadata:\n"
        f"- Investor: {investor}\n"
        f"- Date: {date}\n"
        f"- Source: {source}\n"
        f"- Type: {appearance_type}\n"
        f"- URL: {url}\n"
        f"{topics_hint}\n"
        f"Publication text:\n---\n{enriched_text}\n---\n\n"
        f"Extract all company views and topic views now."
    )

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format=AppearanceSummary,
    )

    result = completion.choices[0].message.parsed
    if result is None:
        raise RuntimeError("LLM returned no parsed output")

    # Validate and correct tickers
    if result.companies:
        tickers = [c.ticker for c in result.companies]
        corrections = validate_tickers(tickers, api_key=api_key, model=model)
        _apply_ticker_corrections(result.companies, corrections)

    return result


def extract_index(
    text: str,
    investor: str,
    date: str,
    source: str,
    appearance_type: str,
    url: str,
    *,
    api_key: str,
    model: str = "gpt-5-mini",
    existing_topics: list[str] | None = None,
) -> AppearanceIndex:
    """Extract lightweight index metadata from short source text.

    Used when source is below COMPRESS_ABOVE_WORDS — full text is kept verbatim,
    so we only need tickers, topics, and focus levels for frontmatter.
    """
    client = openai.OpenAI(api_key=api_key)

    topics_hint = ""
    if existing_topics:
        topics_hint = (
            f"\n\nExisting topics (reuse when semantically equivalent):\n"
            f"{', '.join(existing_topics)}\n"
        )

    user_prompt = (
        f"Extract structured metadata from the following publication.\n\n"
        f"Metadata:\n"
        f"- Investor: {investor}\n"
        f"- Date: {date}\n"
        f"- Source: {source}\n"
        f"- Type: {appearance_type}\n"
        f"- URL: {url}\n"
        f"{topics_hint}\n"
        f"Publication text:\n---\n{text}\n---\n\n"
        f"Extract all company mentions and topic mentions now."
    )

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": INDEX_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format=AppearanceIndex,
    )

    result = completion.choices[0].message.parsed
    if result is None:
        raise RuntimeError("LLM returned no parsed output")

    # Validate and correct tickers
    if result.companies:
        tickers = [c.ticker for c in result.companies]
        corrections = validate_tickers(tickers, api_key=api_key, model=model)
        _apply_ticker_corrections(result.companies, corrections)

    return result


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def render_markdown(
    summary: AppearanceSummary,
    investor: str,
    date: str,
    source: str,
    appearance_type: str,
    url: str,
    source_length: int = 0,
    fetch_method: str = "",
    fetch_id: str = "",
) -> str:
    """Render an AppearanceSummary into the appearance markdown format."""
    from datetime import datetime

    dt = datetime.strptime(date, "%Y-%m-%d")
    heading_date = dt.strftime("%B %d, %Y")

    # Build flat lists for frontmatter (used by search grep)
    tickers_str = ", ".join(c.ticker for c in summary.companies) if summary.companies else ""
    topics_str = ", ".join(t.topic for t in summary.topics) if summary.topics else ""

    lines: list[str] = [
        "---",
        f"investor: {investor}",
        f"date: {date}",
        f"source: {source}",
        f"type: {appearance_type}",
        f"url: {url}",
        f"companies: [{tickers_str}]",
        f"topics: [{topics_str}]",
    ]
    if summary.companies:
        lines.append("companies_detail:")
        for c in summary.companies:
            lines.append(f"  - ticker: {c.ticker}")
            lines.append(f"    focus: {c.focus}")
    if summary.topics:
        lines.append("topics_detail:")
        for t in summary.topics:
            lines.append(f"  - topic: {t.topic}")
            lines.append(f"    focus: {t.focus}")
    if source_length:
        lines.append(f"source_length: {source_length}")
    if fetch_method:
        lines.append(f"fetch_method: {fetch_method}")
    if fetch_id:
        lines.append(f"fetch_id: {fetch_id}")
    lines += [
        "---",
        "",
        f"# {source} — {heading_date}",
        "",
    ]

    # Company-specific views
    lines.append("## Company-Specific Views")
    lines.append("")

    if summary.companies:
        for company in summary.companies:
            lines.append(
                f"### {company.ticker} ({company.company_name}) "
                f"— {company.sentiment}, {company.conviction}, {company.focus}"
            )
            lines.append("")
            lines.append(company.analysis)
            if company.charts:
                lines.append("")
                for chart in company.charts:
                    lines.append(f"![{chart.description}]({chart.url})")
            lines.append("")
    else:
        lines.append("No company-specific views expressed in this appearance.")
        lines.append("")

    # Topics
    lines.append("## Broader Topics")
    lines.append("")

    if summary.topics:
        for topic in summary.topics:
            lines.append(f"### {topic.topic} ({topic.focus})")
            lines.append("")
            lines.append(topic.analysis)
            if topic.charts:
                lines.append("")
                for chart in topic.charts:
                    lines.append(f"![{chart.description}]({chart.url})")
            lines.append("")
    else:
        lines.append("No broader topics discussed in this appearance.")
        lines.append("")

    # Inject summary_length into frontmatter (count words in body only)
    body_start = next(
        i for i, line in enumerate(lines) if line.startswith("# ")
    )
    body_words = sum(
        len(line.split()) for line in lines[body_start:]
        if not line.startswith("![")
    )
    # Insert summary_length right before the closing ---
    frontmatter_end = lines.index("---", 1)
    lines.insert(frontmatter_end, f"summary_length: {body_words}")

    return "\n".join(lines)


def render_markdown_full(
    index: AppearanceIndex,
    full_text: str,
    investor: str,
    date: str,
    source: str,
    appearance_type: str,
    url: str,
    source_length: int = 0,
    fetch_method: str = "",
    fetch_id: str = "",
) -> str:
    """Render frontmatter from index + full original text verbatim.

    Used for short sources below COMPRESS_ABOVE_WORDS.
    """
    from datetime import datetime

    dt = datetime.strptime(date, "%Y-%m-%d")
    heading_date = dt.strftime("%B %d, %Y")

    # Build flat lists for frontmatter (used by search grep)
    tickers_str = ", ".join(c.ticker for c in index.companies) if index.companies else ""
    topics_str = ", ".join(t.topic for t in index.topics) if index.topics else ""

    lines: list[str] = [
        "---",
        f"investor: {investor}",
        f"date: {date}",
        f"source: {source}",
        f"type: {appearance_type}",
        f"url: {url}",
        f"companies: [{tickers_str}]",
        f"topics: [{topics_str}]",
    ]
    if index.companies:
        lines.append("companies_detail:")
        for c in index.companies:
            lines.append(f"  - ticker: {c.ticker}")
            lines.append(f"    focus: {c.focus}")
    if index.topics:
        lines.append("topics_detail:")
        for t in index.topics:
            lines.append(f"  - topic: {t.topic}")
            lines.append(f"    focus: {t.focus}")
    if source_length:
        lines.append(f"source_length: {source_length}")
    if fetch_method:
        lines.append(f"fetch_method: {fetch_method}")
    if fetch_id:
        lines.append(f"fetch_id: {fetch_id}")

    lines += [
        "---",
        "",
        f"# {source} — {heading_date}",
        "",
        full_text,
    ]

    return "\n".join(lines)
