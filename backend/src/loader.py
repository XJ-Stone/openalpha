"""Context assembler -- builds LLM context from search results."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def load_system_prompt(prompts_dir: Path) -> str:
    """Read the system prompt from prompts/system.md.

    Returns an empty string if the file does not exist.
    """
    system_path = prompts_dir / "system.md"
    if not system_path.is_file():
        return ""
    return system_path.read_text(encoding="utf-8").strip()


# Keyword -> skill file mapping.  The first matching rule wins.
_SKILL_KEYWORDS: list[tuple[list[str], str]] = [
    (["compare", "vs", "versus", "difference"], "compare/SKILL.md"),
    (
        [
            "saas",
            "arr",
            "nrr",
            "churn",
            "cac",
            "ltv",
            "rule of 40",
            "net retention",
            "magic number",
        ],
        "saas-metrics/SKILL.md",
    ),
]

_DEFAULT_SKILL = "analyze/SKILL.md"


def load_skills(skills_dir: Path, query: str) -> list[str]:
    """Determine which skills are relevant for *query* and return their content.

    Falls back to the default ``analyze.md`` skill when no keyword matches.
    """
    if not skills_dir.is_dir():
        return []

    query_lower = query.lower()
    matched_files: list[str] = []

    for keywords, filename in _SKILL_KEYWORDS:
        if any(kw in query_lower for kw in keywords):
            matched_files.append(filename)

    if not matched_files:
        matched_files.append(_DEFAULT_SKILL)

    skills: list[str] = []
    for filename in matched_files:
        skill_path = skills_dir / filename
        if skill_path.is_file():
            skills.append(skill_path.read_text(encoding="utf-8").strip())

    return skills


def load_investor_context(
    profiles: list[dict],
    appearances: list[dict],
) -> str:
    """Assemble full-text content from matched profiles and appearances.

    The output is organised by investor so the LLM sees a coherent block
    per person.
    """
    if not profiles and not appearances:
        return ""

    # Group appearances by investor slug
    appearances_by_investor: dict[str, list[dict]] = {}
    for a in appearances:
        slug = a.get("investor_slug", "unknown")
        appearances_by_investor.setdefault(slug, []).append(a)

    sections: list[str] = []

    for profile in profiles:
        slug = profile.get("slug", "unknown")
        name = profile.get("name", slug)
        parts: list[str] = [f"## Investor: {name}"]

        # Profile content
        content = profile.get("_content", "")
        if content:
            parts.append(content)

        # Append any matched appearances for this investor
        investor_appearances = appearances_by_investor.pop(slug, [])
        for app in investor_appearances:
            title = app.get("title", "Appearance")
            date = app.get("date", "")
            header = f"### {title}" + (f" ({date})" if date else "")
            parts.append(header)
            app_content = app.get("_content", "")
            if app_content:
                parts.append(app_content)

        sections.append("\n\n".join(parts))

    # Remaining appearances whose investor wasn't in the profile list
    for slug, apps in appearances_by_investor.items():
        parts: list[str] = [f"## Investor: {slug}"]
        for app in apps:
            title = app.get("title", "Appearance")
            date = app.get("date", "")
            header = f"### {title}" + (f" ({date})" if date else "")
            parts.append(header)
            app_content = app.get("_content", "")
            if app_content:
                parts.append(app_content)
        sections.append("\n\n".join(parts))

    return "\n\n---\n\n".join(sections)


def assemble_context(
    query: str,
    search_results: dict[str, list[dict]],
    settings: Any,
) -> dict[str, str | list[str]]:
    """Orchestrate context assembly and return all pieces the LLM needs.

    Returns a dict with keys:
        - ``system_prompt``:    The base system prompt text.
        - ``investor_context``: Assembled investor data (profiles + appearances).
        - ``skills``:           List of skill content strings.
    """
    system_prompt = load_system_prompt(settings.prompts_dir)
    skills = load_skills(settings.skills_dir, query)
    investor_context = load_investor_context(
        profiles=search_results.get("profiles", []),
        appearances=search_results.get("appearances", []),
    )

    return {
        "system_prompt": system_prompt,
        "investor_context": investor_context,
        "skills": skills,
    }
