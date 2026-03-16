"""Validate all investor markdown files for frontmatter consistency and quality.

Usage:
    python scripts/lint_investors.py                    # Lint all files
    python scripts/lint_investors.py --investor freda-duan  # Lint one investor
    python scripts/lint_investors.py --fix              # Auto-fix what's possible

Exit codes:
    0 = all good
    1 = errors found
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import frontmatter

INVESTORS_DIR = Path(__file__).resolve().parent.parent.parent / "investors"

VALID_TYPES = {"podcast", "substack", "interview", "conference", "tv", "twitter"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TICKER_RE = re.compile(r"^[A-Z]{1,5}$")
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]+$")

# Required frontmatter fields
PROFILE_REQUIRED = {"name", "slug", "fund", "role", "sectors", "companies", "sources", "last_updated"}
# Accept either 'topics' (new) or 'sectors' (legacy) — checked dynamically
APPEARANCE_REQUIRED = {"investor", "date", "source", "type", "companies"}


class LintError:
    def __init__(self, path: Path, message: str, fixable: bool = False):
        self.path = path
        self.message = message
        self.fixable = fixable

    def __str__(self) -> str:
        try:
            rel = self.path.relative_to(INVESTORS_DIR.parent)
        except ValueError:
            rel = self.path
        fix_tag = " [fixable]" if self.fixable else ""
        return f"  {rel}: {self.message}{fix_tag}"


def lint_profile(path: Path) -> list[LintError]:
    """Validate a profile.md file."""
    errors: list[LintError] = []

    try:
        post = frontmatter.load(str(path))
    except Exception as e:
        errors.append(LintError(path, f"Failed to parse frontmatter: {e}"))
        return errors

    meta = post.metadata

    # Check required fields
    missing = PROFILE_REQUIRED - set(meta.keys())
    if missing:
        errors.append(LintError(path, f"Missing required fields: {', '.join(sorted(missing))}"))

    # Validate slug matches directory name
    slug = meta.get("slug")
    dir_name = path.parent.name
    if slug and slug != dir_name:
        errors.append(LintError(path, f"slug '{slug}' doesn't match directory '{dir_name}'"))

    # Validate companies are uppercase tickers
    companies = meta.get("companies", [])
    if isinstance(companies, list):
        for ticker in companies:
            if not TICKER_RE.match(str(ticker)):
                errors.append(LintError(path, f"Invalid ticker format: '{ticker}' (expected uppercase, 1-5 chars)"))

    # Validate last_updated is a date
    last_updated = meta.get("last_updated")
    if last_updated and not DATE_RE.match(str(last_updated)):
        errors.append(LintError(path, f"Invalid last_updated format: '{last_updated}' (expected YYYY-MM-DD)"))

    # Validate sectors/topics is a list
    sectors = meta.get("sectors") or meta.get("topics")
    if sectors is not None and not isinstance(sectors, list):
        errors.append(LintError(path, "sectors/topics must be a list"))

    # Check content sections
    content = post.content
    expected_sections = ["## Background", "## Investment Style", "## Current Known Positions"]
    for section in expected_sections:
        if section not in content:
            errors.append(LintError(path, f"Missing section: {section}"))

    return errors


def lint_appearance(path: Path) -> list[LintError]:
    """Validate an appearance markdown file."""
    errors: list[LintError] = []

    try:
        post = frontmatter.load(str(path))
    except Exception as e:
        errors.append(LintError(path, f"Failed to parse frontmatter: {e}"))
        return errors

    meta = post.metadata

    # Check required fields
    missing = APPEARANCE_REQUIRED - set(meta.keys())
    if missing:
        errors.append(LintError(path, f"Missing required fields: {', '.join(sorted(missing))}"))

    # Validate investor slug matches directory
    investor = meta.get("investor")
    dir_name = path.parent.parent.name  # appearances/ is one level up from investor dir
    if investor and investor != dir_name:
        errors.append(LintError(path, f"investor '{investor}' doesn't match directory '{dir_name}'"))

    # Validate date
    date = meta.get("date")
    if date and not DATE_RE.match(str(date)):
        errors.append(LintError(path, f"Invalid date format: '{date}' (expected YYYY-MM-DD)"))

    # Validate date in filename matches frontmatter
    filename_match = re.match(r"^(\d{4}-\d{2}-\d{2})-", path.name)
    if filename_match and date:
        filename_date = filename_match.group(1)
        if str(date) != filename_date:
            errors.append(LintError(path, f"Date mismatch: frontmatter '{date}' vs filename '{filename_date}'"))

    # Validate type
    appearance_type = meta.get("type")
    if appearance_type and appearance_type not in VALID_TYPES:
        errors.append(LintError(path, f"Invalid type: '{appearance_type}' (valid: {', '.join(sorted(VALID_TYPES))})"))

    # Validate companies are uppercase tickers
    companies = meta.get("companies", [])
    if isinstance(companies, list):
        for ticker in companies:
            if not TICKER_RE.match(str(ticker)):
                errors.append(LintError(path, f"Invalid ticker format: '{ticker}' (expected uppercase, 1-5 chars)"))
    elif companies is not None:
        errors.append(LintError(path, "companies must be a list"))

    # Validate topics/sectors is a list (accept either)
    topics = meta.get("topics") or meta.get("sectors")
    if topics is not None and not isinstance(topics, list):
        errors.append(LintError(path, "topics/sectors must be a list"))
    if not meta.get("topics") and not meta.get("sectors"):
        errors.append(LintError(path, "Missing 'topics' (or legacy 'sectors') field"))

    # Check content sections
    content = post.content
    if "## Company-Specific Views" not in content and "## Broader Themes" not in content:
        errors.append(LintError(path, "Missing both '## Company-Specific Views' and '## Broader Themes' sections"))

    # Check for empty content
    if len(content.strip()) < 50:
        errors.append(LintError(path, "Content seems too short (< 50 chars)"))

    return errors


def lint_investor_dir(investor_dir: Path) -> list[LintError]:
    """Lint all files for a single investor."""
    errors: list[LintError] = []

    # Check profile exists
    profile = investor_dir / "profile.md"
    if not profile.exists():
        errors.append(LintError(investor_dir, "Missing profile.md"))
    else:
        errors.extend(lint_profile(profile))

    # Check appearances directory
    appearances_dir = investor_dir / "appearances"
    if appearances_dir.is_dir():
        appearance_files = sorted(appearances_dir.glob("*.md"))
        if not appearance_files:
            errors.append(LintError(appearances_dir, "appearances/ directory exists but has no .md files"))
        for f in appearance_files:
            errors.extend(lint_appearance(f))
    else:
        errors.append(LintError(investor_dir, "Missing appearances/ directory"))

    return errors


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Validate investor markdown files.")
    parser.add_argument("--investor", type=str, help="Lint only this investor (slug)")
    args = parser.parse_args()

    if not INVESTORS_DIR.is_dir():
        print(f"Error: investors directory not found at {INVESTORS_DIR}", file=sys.stderr)
        sys.exit(1)

    all_errors: list[LintError] = []

    if args.investor:
        investor_dir = INVESTORS_DIR / args.investor
        if not investor_dir.is_dir():
            print(f"Error: investor '{args.investor}' not found", file=sys.stderr)
            sys.exit(1)
        all_errors.extend(lint_investor_dir(investor_dir))
    else:
        # Lint all investors
        investor_dirs = sorted(
            d for d in INVESTORS_DIR.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        )

        for investor_dir in investor_dirs:
            all_errors.extend(lint_investor_dir(investor_dir))

    # Report results
    if all_errors:
        print(f"\n{len(all_errors)} error(s) found:\n")
        for error in all_errors:
            print(error)
        print()
        sys.exit(1)
    else:
        investor_label = args.investor or "all investors"
        print(f"All files valid for {investor_label}.")
        sys.exit(0)


if __name__ == "__main__":
    main()
