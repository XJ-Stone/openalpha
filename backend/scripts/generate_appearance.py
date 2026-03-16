"""Generate an appearance.md file from a transcript using an LLM.

Usage:
    # From a transcript file
    python scripts/generate_appearance.py \\
        --transcript path/to/transcript.txt \\
        --investor brad-gerstner \\
        --date 2025-03-01 \\
        --source "BG2Pod" \\
        --type podcast \\
        --url "https://youtube.com/watch?v=..."

    # From stdin
    echo "transcript text" | python scripts/generate_appearance.py \\
        --investor brad-gerstner \\
        --date 2025-03-01 \\
        --source "BG2Pod" \\
        --type podcast

    # Output to a file instead of stdout
    python scripts/generate_appearance.py \\
        --transcript transcript.txt \\
        --investor brad-gerstner \\
        --date 2025-03-01 \\
        --source "BG2Pod" \\
        --type podcast \\
        --output investors/brad-gerstner/2025-03-01-bg2pod-topic.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure the backend package is importable when running as a script
_BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BACKEND_DIR))

from src.config import get_settings
from src.llm import get_provider

VALID_TYPES = ("podcast", "substack", "interview", "conference", "tv", "twitter")

SYSTEM_PROMPT = """\
You are an expert financial analyst assistant. Your job is to extract structured \
investor opinions from a transcript or source text.

Given a transcript and metadata about the investor and source, produce a markdown \
file in the following format:

1. YAML frontmatter with: investor, date, source, type, url, companies (array of \
tickers mentioned), sectors (array of sectors discussed).

2. A heading: "# {Source} — {Month DD, YYYY}"

3. A "## Company-Specific Views" section. For each company discussed:
   - Use the format: **Company Name (TICKER)** — Sentiment, Conviction
   - Sentiment is one of: Bullish, Bearish, Neutral, Mixed
   - Conviction is one of: HIGH (explicitly states position/buying), MEDIUM (clear \
opinion but no position confirmation), MENTIONED (referenced in passing)
   - Summarize what the investor said. Use direct quotes when the investor made a \
memorable or specific statement. Otherwise, paraphrase clearly.

4. A "## Broader Themes" section with bullet points for market-level or sector-level \
views not tied to a single company.

Rules:
- Use standard ticker symbols (NVDA not Nvidia, MSFT not Microsoft, META not Facebook)
- Only include companies the investor actually discussed -- do not infer
- Every claim must be traceable to the source material
- Keep it concise but thorough
- If the investor did not discuss any specific companies, the Company-Specific Views \
section should say "No company-specific views expressed in this appearance."
"""


def build_user_prompt(
    transcript: str,
    investor: str,
    date: str,
    source: str,
    appearance_type: str,
    url: str,
) -> str:
    """Build the user message for the LLM."""
    return f"""\
Extract structured investor opinions from the following transcript.

Metadata:
- Investor slug: {investor}
- Date: {date}
- Source: {source}
- Type: {appearance_type}
- URL: {url or "N/A"}

Transcript:
---
{transcript}
---

Generate the appearance markdown file now. Output ONLY the markdown content \
(starting with the --- frontmatter delimiter). Do not wrap it in code fences."""


def read_transcript(args: argparse.Namespace) -> str:
    """Read transcript from file, argument, or stdin."""
    if args.transcript:
        path = Path(args.transcript)
        if path.is_file():
            return path.read_text(encoding="utf-8")
        # Treat as inline text if not a valid file path
        return args.transcript

    # Read from stdin
    if not sys.stdin.isatty():
        return sys.stdin.read()

    print(
        "Error: No transcript provided. Use --transcript <file_or_text> "
        "or pipe text via stdin.",
        file=sys.stderr,
    )
    sys.exit(1)


def generate_appearance(
    transcript: str,
    investor: str,
    date: str,
    source: str,
    appearance_type: str,
    url: str,
) -> str:
    """Send the transcript to the LLM and return the generated appearance markdown."""
    settings = get_settings()
    provider = get_provider(settings)

    user_prompt = build_user_prompt(
        transcript=transcript,
        investor=investor,
        date=date,
        source=source,
        appearance_type=appearance_type,
        url=url,
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    result = provider.chat(messages, stream=False)

    if not isinstance(result, str):
        # If streaming generator was returned despite stream=False, collect it
        result = "".join(result)

    return result.strip()


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="generate_appearance",
        description=(
            "Generate an appearance.md file from a transcript using an LLM. "
            "The script extracts company-specific views, sectors, and broader themes."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python scripts/generate_appearance.py \\
      --transcript transcript.txt \\
      --investor brad-gerstner \\
      --date 2025-03-01 \\
      --source "BG2Pod" \\
      --type podcast \\
      --url "https://youtube.com/watch?v=abc"

  cat transcript.txt | python scripts/generate_appearance.py \\
      --investor chamath-palihapitiya \\
      --date 2025-02-15 \\
      --source "All-In Podcast" \\
      --type podcast
""",
    )

    parser.add_argument(
        "--transcript",
        type=str,
        default=None,
        help="Path to a transcript file, or inline text. Reads from stdin if omitted.",
    )
    parser.add_argument(
        "--investor",
        type=str,
        required=True,
        help="Investor slug (e.g., brad-gerstner, cathie-wood).",
    )
    parser.add_argument(
        "--date",
        type=str,
        required=True,
        help="Date of the appearance in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help='Name of the source (e.g., "BG2Pod", "All-In Podcast", "CNBC").',
    )
    parser.add_argument(
        "--type",
        type=str,
        required=True,
        choices=VALID_TYPES,
        dest="appearance_type",
        help="Type of appearance.",
    )
    parser.add_argument(
        "--url",
        type=str,
        default="",
        help="URL link to the original source.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output file path. Prints to stdout if omitted.",
    )

    return parser


def main() -> None:
    """Entry point."""
    parser = build_parser()
    args = parser.parse_args()

    # Validate date format
    import re

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", args.date):
        print(
            f"Error: Date must be in YYYY-MM-DD format, got: {args.date}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Read transcript
    transcript = read_transcript(args)
    if not transcript.strip():
        print("Error: Transcript is empty.", file=sys.stderr)
        sys.exit(1)

    print(f"Generating appearance for {args.investor} ({args.date})...", file=sys.stderr)

    try:
        result = generate_appearance(
            transcript=transcript,
            investor=args.investor,
            date=args.date,
            source=args.source,
            appearance_type=args.appearance_type,
            url=args.url,
        )
    except Exception as exc:
        print(f"Error generating appearance: {exc}", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result + "\n", encoding="utf-8")
        print(f"Written to {output_path}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
