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


class ThemeView(BaseModel):
    """A non-company-specific perspective: sector view, macro argument, thematic call,
    market observation, or any other insight not tied to a single ticker."""

    theme: str = Field(
        description=(
            "Concise theme label, e.g. 'Agentic Commerce', 'AI ROI Measurement', "
            "'Neo Cloud Adoption', 'China AI Infrastructure'"
        )
    )
    companies_referenced: list[str] = Field(
        default_factory=list,
        description=(
            "Tickers or company names mentioned in the context of this theme but "
            "not discussed deeply enough to warrant a separate CompanyView. "
            "Use ticker symbols for public companies, uppercase names for private."
        ),
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
            "theme. Only include charts that add analytical value — data "
            "visualizations, comparisons, trend charts, etc."
        ),
    )


class AppearanceSummary(BaseModel):
    """Structured extraction from a single investor appearance or publication."""

    companies: list[CompanyView] = Field(
        default_factory=list,
        description=(
            "Company-specific views. Only include companies the investor "
            "actually analyzed or expressed an opinion on — not every company "
            "mentioned in passing. Those belong in ThemeView.companies_referenced."
        ),
    )
    themes: list[ThemeView] = Field(
        default_factory=list,
        description=(
            "Non-company-specific perspectives: sector views, macro arguments, "
            "thematic calls, market observations, geographic analyses, "
            "organizational insights, or any other viewpoint not tied to a "
            "single ticker."
        ),
    )
    topics: list[str] = Field(
        default_factory=list,
        description=(
            "3-5 topic tags capturing what this appearance is about. Topics are "
            "broader than sectors — they capture narratives, themes, and conversations "
            "(e.g. 'AI investment bubble', 'agentic commerce', 'China token economy', "
            "'ride-hailing competition', 'Fed rate cuts impact on growth'). "
            "Lowercase hyphenated. Reuse existing topics from the provided list when "
            "semantically equivalent; only create new ones if nothing fits."
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


class ThemeMention(BaseModel):
    """Lightweight theme mention for indexing — no analysis text."""

    theme: str = Field(description="Concise theme label")
    companies_referenced: list[str] = Field(
        default_factory=list,
        description="Tickers or company names mentioned in this theme's context.",
    )


class AppearanceIndex(BaseModel):
    """Lightweight metadata extraction for short sources kept verbatim."""

    companies: list[CompanyMention] = Field(
        default_factory=list,
        description="Companies the investor analyzed or expressed an opinion on.",
    )
    themes: list[ThemeMention] = Field(
        default_factory=list,
        description="Non-company-specific themes discussed.",
    )
    topics: list[str] = Field(
        default_factory=list,
        description=(
            "3-5 topic tags capturing what this appearance is about. Reuse "
            "existing topics from the provided list when semantically equivalent; "
            "only create new ones if nothing fits."
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
Use when the investor analyzes or expresses a clear opinion on a specific company. \
For public companies use standard tickers (NVDA, MSFT, META). For private companies \
use uppercase name (OPENAI, ANTHROPIC, STRIPE).

Do NOT create a CompanyView for companies merely mentioned in passing — those belong \
in ThemeView.companies_referenced.

## ThemeView
Use for perspectives not tied to a single company: sector views, macro arguments, \
market observations, geographic analyses, frameworks.

Do NOT repeat information already in a CompanyView. ThemeViews add cross-cutting or \
non-company-specific insight only. Skip meta-commentary, disclaimers, and themes \
that merely reword a CompanyView.

## Images
When the source includes images (marked as [IMAGE: ...] with descriptions), attach \
them to the relevant CompanyView or ThemeView if the image provides analytical value \
(charts, data visualizations, tables, diagrams). Skip decorative images.

## Company focus levels
- primary: the report is substantially about this company (deep analysis, dedicated section)
- secondary: meaningful discussion but not the main focus
- mention: referenced for comparison, context, or in passing

## Topics
Extract 3-5 topic tags that capture what this appearance is about. Topics are broader \
than financial sectors — they capture narratives, themes, and market conversations \
(e.g. 'agentic commerce', 'AI investment bubble', 'China token economy'). \
When an existing topics list is provided, REUSE existing topics where semantically \
equivalent. Only create a new topic if nothing in the list fits.

## Rules
- Only extract views actually expressed — do not infer or editorialize
- Every claim must be traceable to the source text
- State each point ONCE across all CompanyViews and ThemeViews — zero redundancy
"""


# ---------------------------------------------------------------------------
# Index-only prompt (for short sources — extract metadata, skip analysis)
# ---------------------------------------------------------------------------

INDEX_SYSTEM_PROMPT = """\
You are an expert financial analyst assistant. Your job is to extract STRUCTURED \
METADATA from a publication — companies discussed, themes, and topics.

You are NOT writing a summary. The full text will be kept verbatim. You are only \
extracting searchable index fields.

## CompanyMention
Create one for each company the investor analyzes or expresses an opinion on. \
For public companies use standard tickers (NVDA, MSFT, META). For private companies \
use uppercase name (OPENAI, ANTHROPIC, STRIPE). Set the focus level: primary if the \
report is substantially about this company, secondary for meaningful but non-central \
discussion, mention for passing references.

Do NOT create a CompanyMention for companies merely mentioned in passing — those \
belong in ThemeMention.companies_referenced.

## ThemeMention
Create one for each non-company-specific perspective: sector views, macro arguments, \
market observations, geographic analyses, frameworks.

## Topics
Extract 3-5 topic tags that capture what this appearance is about. Topics are broader \
than financial sectors — they capture narratives, themes, and market conversations \
(e.g. 'agentic commerce', 'AI investment bubble', 'China token economy'). \
When an existing topics list is provided, REUSE existing topics where semantically \
equivalent. Only create a new topic if nothing in the list fits.

## Rules
- Only extract views actually expressed — do not infer
"""

# Threshold: sources below this word count keep full text; above get compressed
COMPRESS_ABOVE_WORDS = 3000


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
        f"Extract all company-specific views and thematic perspectives now."
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
    so we only need tickers, sentiment, themes, and sectors for frontmatter.
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
        f"Extract all company mentions, themes, and topic tags now."
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
    # Collect all tickers for frontmatter
    all_tickers: list[str] = [c.ticker for c in summary.companies]
    for theme in summary.themes:
        for t in theme.companies_referenced:
            if t not in all_tickers:
                all_tickers.append(t)

    # Format date for heading
    from datetime import datetime

    dt = datetime.strptime(date, "%Y-%m-%d")
    heading_date = dt.strftime("%B %d, %Y")

    # Build frontmatter
    tickers_str = ", ".join(all_tickers) if all_tickers else ""
    topics_str = ", ".join(summary.topics) if summary.topics else ""

    # Build companies_detail with focus levels
    companies_detail: list[dict[str, str]] = []
    for c in summary.companies:
        companies_detail.append({"ticker": c.ticker, "focus": c.focus})

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
    if companies_detail:
        lines.append("companies_detail:")
        for cd in companies_detail:
            lines.append(f"  - ticker: {cd['ticker']}")
            lines.append(f"    focus: {cd['focus']}")
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

    # Themes
    lines.append("## Broader Themes")
    lines.append("")

    if summary.themes:
        for theme in summary.themes:
            lines.append(f"### {theme.theme}")
            lines.append("")
            lines.append(theme.analysis)
            if theme.companies_referenced:
                refs = ", ".join(theme.companies_referenced)
                lines.append("")
                lines.append(f"**Companies referenced:** {refs}")
            if theme.charts:
                lines.append("")
                for chart in theme.charts:
                    lines.append(f"![{chart.description}]({chart.url})")
            lines.append("")
    else:
        lines.append("No broader themes discussed in this appearance.")
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

    # Collect all tickers for frontmatter
    all_tickers: list[str] = [c.ticker for c in index.companies]
    for theme in index.themes:
        for t in theme.companies_referenced:
            if t not in all_tickers:
                all_tickers.append(t)

    # Build companies_detail with focus levels
    companies_detail: list[dict[str, str]] = []
    for c in index.companies:
        companies_detail.append({"ticker": c.ticker, "focus": c.focus})

    dt = datetime.strptime(date, "%Y-%m-%d")
    heading_date = dt.strftime("%B %d, %Y")

    tickers_str = ", ".join(all_tickers) if all_tickers else ""
    topics_str = ", ".join(index.topics) if index.topics else ""

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
    if companies_detail:
        lines.append("companies_detail:")
        for cd in companies_detail:
            lines.append(f"  - ticker: {cd['ticker']}")
            lines.append(f"    focus: {cd['focus']}")
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
