"""Generate or regenerate a profile.md from existing appearance files.

Usage:
    # Generate a profile from appearances
    python scripts/generate_profile.py --investor brad-gerstner

    # Output to a specific file instead of the default location
    python scripts/generate_profile.py --investor brad-gerstner --output profile-draft.md

    # Print to stdout instead of writing to file
    python scripts/generate_profile.py --investor brad-gerstner --stdout
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

SYSTEM_PROMPT = """\
You are an expert financial analyst assistant. Your job is to synthesize an investor \
profile from their public appearances (podcasts, interviews, memos, etc.).

Given a set of appearance summaries for an investor, produce a markdown profile file \
in the following format:

1. YAML frontmatter with: name, slug, fund, role, aum (if inferrable, otherwise "N/A"), \
sectors (array), companies (array of tickers), sources (array of source names), \
last_updated (today's date or the most recent appearance date).

2. A heading: "# {Full Name}"

3. A "## Background" section: 2-3 sentences about who they are and career highlights. \
Derive this ONLY from what is stated or implied in the appearances. Do not fabricate \
biographical details.

4. A "## Investment Style" section: 3-5 bullet points distilled from their actual \
public statements across all appearances.

5. A "## Current Known Positions (from public statements)" section: Companies with \
sentiment and a one-line thesis. Only include positions that the investor has publicly \
stated or strongly implied. Use the format:
   - **TICKER (Company)**: Sentiment. One-line thesis.

6. A "## How to Read {First Name}" section: 1-2 paragraphs explaining what signals \
high conviction vs. casual mention, which sources contain their most considered views, \
and any patterns in how they communicate.

Rules:
- Use standard ticker symbols (NVDA not Nvidia, MSFT not Microsoft)
- The companies array in frontmatter should include ALL tickers mentioned across all \
appearances
- The sectors array should cover all sectors discussed
- Every claim in the profile must be traceable to at least one appearance
- Do not fabricate quotes, positions, or biographical details
- If you cannot determine something (e.g., AUM), use "N/A"
"""


def find_appearances(investor_slug: str) -> list[tuple[str, str]]:
    """Find all appearance files for the given investor.

    Returns a list of (filename, content) tuples.
    """
    settings = get_settings()
    investor_dir = settings.investors_dir / investor_slug

    if not investor_dir.is_dir():
        return []

    appearances: list[tuple[str, str]] = []
    # Check both top-level and appearances/ subdirectory
    search_dirs = [investor_dir]
    appearances_subdir = investor_dir / "appearances"
    if appearances_subdir.is_dir():
        search_dirs.append(appearances_subdir)
    for search_dir in search_dirs:
        for md_path in sorted(search_dir.glob("*.md")):
            # Skip the profile file itself
            if md_path.name == "profile.md":
                continue
            content = md_path.read_text(encoding="utf-8")
            appearances.append((md_path.name, content))

    return appearances


def generate_profile(investor_slug: str, appearances: list[tuple[str, str]]) -> str:
    """Send appearances to the LLM and return the generated profile markdown."""
    settings = get_settings()
    provider = get_provider(settings)

    # Build the appearances context
    appearances_text = ""
    for filename, content in appearances:
        appearances_text += f"\n\n--- Appearance: {filename} ---\n{content}"

    user_prompt = f"""\
Generate an investor profile for the investor with slug: {investor_slug}

The following are all of their recorded appearances in our knowledge base:

{appearances_text}

Generate the profile markdown file now. Output ONLY the markdown content \
(starting with the --- frontmatter delimiter). Do not wrap it in code fences."""

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
        prog="generate_profile",
        description=(
            "Generate or regenerate a profile.md for an investor by synthesizing "
            "their existing appearance files using an LLM."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  # Generate and write to the default location (investors/<slug>/profile.md)
  python scripts/generate_profile.py --investor brad-gerstner

  # Write to a custom location
  python scripts/generate_profile.py --investor brad-gerstner --output draft.md

  # Print to stdout for review
  python scripts/generate_profile.py --investor brad-gerstner --stdout
""",
    )

    parser.add_argument(
        "--investor",
        type=str,
        required=True,
        help="Investor slug (e.g., brad-gerstner). Must match a directory under investors/.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help=(
            "Output file path. Defaults to investors/<slug>/profile.md. "
            "Use --stdout to print to stdout instead."
        ),
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        default=False,
        help="Print the generated profile to stdout instead of writing to a file.",
    )

    return parser


def main() -> None:
    """Entry point."""
    parser = build_parser()
    args = parser.parse_args()

    investor_slug: str = args.investor

    # Find appearances
    print(f"Scanning appearances for {investor_slug}...", file=sys.stderr)
    appearances = find_appearances(investor_slug)

    if not appearances:
        print(
            f"Error: No appearance files found for investor '{investor_slug}'.\n"
            f"Expected files in: investors/{investor_slug}/*.md (excluding profile.md)\n\n"
            "Add at least one appearance before generating a profile.\n"
            "See: python scripts/generate_appearance.py --help",
            file=sys.stderr,
        )
        sys.exit(1)

    print(
        f"Found {len(appearances)} appearance(s). Generating profile...",
        file=sys.stderr,
    )

    try:
        result = generate_profile(investor_slug, appearances)
    except Exception as exc:
        print(f"Error generating profile: {exc}", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.stdout:
        print(result)
    else:
        if args.output:
            output_path = Path(args.output)
        else:
            settings = get_settings()
            output_path = settings.investors_dir / investor_slug / "profile.md"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result + "\n", encoding="utf-8")
        print(f"Profile written to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
