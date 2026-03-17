"""Source registry — maps URLs to investors and source metadata."""

from __future__ import annotations

from pathlib import Path

import yaml

_REGISTRY_PATH = Path(__file__).resolve().parent.parent / "data-ingestion" / "_registry.yaml"


def load_registry(path: Path | None = None) -> dict[str, dict]:
    """Load the registry YAML and return a dict keyed by normalized URL."""
    registry_path = path or _REGISTRY_PATH
    if not registry_path.exists():
        return {}
    data = yaml.safe_load(registry_path.read_text())
    result: dict[str, dict] = {}
    for entry in data.get("substacks", []):
        result[entry["url"].rstrip("/")] = entry
    return result


def resolve_from_registry(
    url: str, path: Path | None = None,
) -> tuple[str, str] | None:
    """Look up investor slug and source_name for a URL.

    Returns (investor, source_name) or None if not found.
    """
    registry = load_registry(path)
    entry = registry.get(url.rstrip("/"))
    if entry:
        return entry["investor"], entry["source_name"]
    return None
