"""Entity extraction — resolves natural language queries into structured entities."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field

from .llm import LLMProvider

logger = logging.getLogger(__name__)

_EXTRACTION_PROMPT = """\
Extract structured entities from the user's investment research question.
Return a JSON object with these fields:

- "tickers": list of stock ticker symbols (uppercase, e.g. "SNOW", "TSLA", "PLTR").
  Convert company names to tickers: "Snowflake" → "SNOW", "Tesla" → "TSLA",
  "Palantir" → "PLTR", "Meta" → "META", etc.
  If the company is private or you don't know the ticker, use the company name in uppercase.
- "investors": list of investor name strings as mentioned (e.g. "Brad Gerstner", "Cathie Wood").
  Include partial names, nicknames, or fund names: "Druck" → "Druckenmiller",
  "ARK" → "Cathie Wood", "Chamath" → "Chamath Palihapitiya".
- "sectors": list of sector/theme strings (e.g. "AI-infrastructure", "fintech", "cloud").
  Normalize to lowercase-hyphenated.

Rules:
- Only extract entities actually mentioned or clearly implied in the question.
- If the question is broad (e.g. "what's hot right now?"), return empty lists.
- Always return valid JSON, nothing else. No markdown, no explanation.

Example:
  Input: "What does Cathie Wood think about Tesla?"
  Output: {"tickers": ["TSLA"], "investors": ["Cathie Wood"], "sectors": []}

Example:
  Input: "Who's bullish on AI infrastructure?"
  Output: {"tickers": [], "investors": [], "sectors": ["AI-infrastructure"]}

Example:
  Input: "How do Gerstner and Druckenmiller differ on Snowflake?"
  Output: {"tickers": ["SNOW"], "investors": ["Gerstner", "Druckenmiller"], "sectors": []}
"""


@dataclass
class ExtractedEntities:
    """Structured entities extracted from a user query."""

    tickers: list[str] = field(default_factory=list)
    investors: list[str] = field(default_factory=list)
    sectors: list[str] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not self.tickers and not self.investors and not self.sectors


def extract_entities(query: str, provider: LLMProvider) -> ExtractedEntities:
    """Use a fast LLM call to extract structured entities from a natural language query."""
    messages = [
        {"role": "system", "content": _EXTRACTION_PROMPT},
        {"role": "user", "content": query},
    ]

    try:
        raw = provider.chat(messages, stream=False)
        assert isinstance(raw, str)

        # Strip markdown fences if the model wraps its response
        text = raw.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

        parsed = json.loads(text)
        return ExtractedEntities(
            tickers=[t.upper() for t in parsed.get("tickers", [])],
            investors=parsed.get("investors", []),
            sectors=parsed.get("sectors", []),
        )
    except (json.JSONDecodeError, KeyError, AssertionError) as exc:
        logger.warning("Entity extraction failed, falling back to raw query: %s", exc)
        return ExtractedEntities()
