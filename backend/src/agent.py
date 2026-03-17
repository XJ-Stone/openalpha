"""Agent orchestrator -- map-reduce query pipeline with async streaming."""

from __future__ import annotations

import asyncio
import json
import logging
import re
from dataclasses import dataclass
from typing import AsyncGenerator, Generator, Literal

from pydantic import BaseModel, Field

from .config import Settings, get_settings
from .entity import ExtractedEntities, extract_entities
from .llm import LLMProvider, get_provider
from .loader import load_system_prompt, load_skills
from .search import InvestorIndex

logger = logging.getLogger(__name__)

# Max files to feed directly without map phase
DIRECT_CONTEXT_LIMIT = 3

# Token budget caps per focus level (upper limits, not targets)
FOCUS_BUDGET = {"primary": 1000, "secondary": 400, "mention": 200}

# Target tokens per reduce batch — keep each LLM call's input manageable
REDUCE_BATCH_TARGET = 10_000

# ---------------------------------------------------------------------------
# Event types for streaming progress + content
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class StatusEvent:
    """Pipeline progress update (shown as collapsible status in UI)."""

    phase: str  # extract | search | map | reduce
    detail: str
    progress: str = ""  # e.g. "3/10" for map phase


@dataclass(frozen=True)
class ContentEvent:
    """A chunk of the final answer text."""

    token: str


@dataclass(frozen=True)
class SourcesEvent:
    """List of source references for citations in the answer."""

    sources: list[dict]  # [{index, investor, date, source, url}, ...]


@dataclass(frozen=True)
class ContentReplaceEvent:
    """Replaces the full accumulated answer text (used for citation renumbering)."""

    content: str


# Union type for the stream
StreamEvent = StatusEvent | ContentEvent | SourcesEvent | ContentReplaceEvent

# ---------------------------------------------------------------------------
# Structured output model for MAP phase
# ---------------------------------------------------------------------------


class MapExtract(BaseModel):
    """Structured output from the MAP phase for a single appearance."""

    relevance: Literal["RELEVANT", "NOT_RELEVANT"] = Field(
        description="Whether this appearance contains content relevant to the question"
    )
    key_excerpts: str = Field(
        default="",
        description=(
            "Verbatim quotes, numbers, and data points from the source that are "
            "relevant to the question. Preserve exact figures, dates, and direct "
            "quotes. Empty when NOT_RELEVANT."
        ),
    )
    analysis: str = Field(
        default="",
        description=(
            "Your analytical summary of how this appearance answers the question. "
            "Interpret the data: what is the investor's stance, how confident are "
            "they, what is their reasoning, and what catalysts or risks do they "
            "identify? Empty when NOT_RELEVANT."
        ),
    )


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

_MAP_PROMPT = """\
You are an investment research assistant. Given ONE investor appearance \
(article, newsletter, or transcript), analyze it in relation to the user's \
question.

If the appearance contains nothing relevant to the question, set relevance \
to NOT_RELEVANT and leave other fields empty.

If relevant:
1. In key_excerpts: extract verbatim quotes, specific numbers, metrics, \
   dates, and data points from the source. Preserve exact language. \
   This is the raw evidence.
2. In analysis: provide your analytical interpretation — what is the \
   investor's stance, conviction level, reasoning, key catalysts or risks \
   they identify, and how this relates to the user's question. Connect \
   the dots the investor may have left implicit.

## Extraction budget
The appearance metadata includes focus levels for companies and topics. \
Scale your extraction depth accordingly:
- primary (<1000 tokens): full thesis, evidence, key numbers, direct quotes
- secondary (<400 tokens): core opinion + one supporting data point
- mention (<200 tokens): one sentence with specific claim, or skip entirely
Focus your extraction on the companies/topics most relevant to the question."""

_REDUCE_PROMPT = """\
You are an expert investment research analyst. You have been given analyzed \
extracts from multiple investor appearances, each pre-filtered for relevance \
to the user's question. Each extract contains raw excerpts from the source \
and an analytical summary. Extracts are grouped by investor, newest first \
within each group.

Synthesize these into a clear, well-structured answer.

## Output structure
- **Start with "## Executive Summary"**: 2-3 sentences that directly answer \
  the question using the most recent data. A reader who stops here should \
  have the core answer with a date and citation.
- Then organize supporting detail in subsequent sections with markdown headers.
- **Recency order is mandatory**: within every section, start with the most \
  recent evidence and work backwards in time. Do NOT organize chronologically \
  from oldest to newest. The reader cares about the current view first.
- If positions evolved over time, note it briefly inline or add a short \
  "View Evolution" note at the end.
- Keep total response focused — depth over breadth.
- Write in flowing paragraphs within each section. Do NOT insert line \
  breaks mid-paragraph or between closely related sentences.

## Citation rules
- Use numbered citations like [1], [2] matching the extract numbers
- Preserve exact numbers, metrics, and direct quotes from the extracts
- Every factual claim must have a citation

## Handling multiple perspectives
- If investors disagree, present both sides prominently — disagreements \
  are among the most valuable signals
- When the SAME investor contradicts their own earlier view, call this \
  out explicitly with dates (e.g. "Duan reversed her SNOW stance between \
  Dec 2025 [3] and Feb 2026 [1]")
- If data is from a single investor, trace how their view evolved

## Recency
- The most recent opinion is the headline. Older views are supporting context.
- Always include the date when stating an investor's current position \
  (e.g. "As of March 2026, Duan is bullish on AMZN [1]" not just \
  "Duan is bullish on AMZN [1]"). The reader needs to see at a glance \
  how fresh the view is.
- Flag commentary older than 6 months as potentially stale.

## Boundaries
- If no relevant data was found, say so clearly
- Never infer positions the investor did not state
- Never make buy/sell/hold recommendations"""

_SECTOR_RESOLVE_PROMPT = """\
Given a user query about topics/themes in investment research, select the \
most relevant topic tags from the available list.

Available topics:
{sectors}

Return a JSON array of matching topic strings. Include topics that are \
directly mentioned OR semantically related to the query. Return [] if none match.
Return ONLY the JSON array, nothing else."""


_INTENT_PROMPT = """\
You are a router for an investor research agent. Given a conversation history \
and a new user message, classify the intent.

Return EXACTLY one word:
- RESEARCH — the user is asking a new research question, mentioning a new \
  company/ticker/sector/investor not already covered, or asking for data the \
  prior conversation does not contain.
- FOLLOW_UP — the user is asking to summarize, clarify, reformat, compare, \
  or dig deeper into information already present in the conversation. \
  Also includes meta-requests like "be more concise" or "give me bullet points"."""


# Max conversation turns to send for follow-ups (most recent N pairs)
MAX_HISTORY_TURNS = 6

# Max characters per assistant message in history to avoid context blowout
MAX_ASSISTANT_MSG_CHARS = 10000


class Agent:
    """Map-reduce orchestrator for investor research queries."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._index = InvestorIndex(self._settings.investors_dir)
        self._provider: LLMProvider = get_provider(self._settings)

    async def query_stream(
        self,
        question: str,
    ) -> AsyncGenerator[StreamEvent, None]:
        """Async generator yielding StatusEvents (progress) and ContentEvents (answer).

        Pipeline:
        1. Extract entities (tickers, investors, sectors) via LLM.
        2. Resolve fuzzy sector matches using the sector union index.
        3. Find matching appearances via reverse indexes.
        4. MAP: extract relevant content per-file in parallel.
        5. REDUCE: synthesize extracts into final answer (streamed).
        """
        # --- 1. Entity extraction ---------------------------------------------
        yield StatusEvent(phase="extract", detail="Analyzing question...")

        entities = await asyncio.to_thread(extract_entities, question, self._provider)

        entity_parts: list[str] = []
        if entities.tickers:
            entity_parts.append(", ".join(entities.tickers))
        if entities.investors:
            entity_parts.append(", ".join(entities.investors))
        if entities.topics:
            entity_parts.append(", ".join(entities.topics))
        entity_summary = "; ".join(entity_parts) if entity_parts else "broad query"
        yield StatusEvent(phase="extract", detail=entity_summary)

        logger.info(
            "Extracted entities: tickers=%s investors=%s topics=%s",
            entities.tickers,
            entities.investors,
            entities.topics,
        )

        # --- 2. Resolve topics against the full topic union -------------------
        resolved_sectors = await asyncio.to_thread(
            self._resolve_sectors, entities.topics
        )
        if resolved_sectors:
            logger.info("Resolved topics: %s", resolved_sectors)

        # --- 3. Find matching appearances -------------------------------------
        matched = self._find_appearances(entities, resolved_sectors)
        logger.info("Matched %d appearances", len(matched))

        if not matched:
            yield StatusEvent(phase="search", detail="No matching data found")
            async for event in self._stream_no_data(question):
                yield event
            return

        # Sort by date descending (most recent first)
        matched.sort(key=lambda a: a.get("date", ""), reverse=True)

        # Build search detail: investor names + appearance count
        investor_names = sorted(
            {a.get("investor", a.get("investor_slug", "unknown")) for a in matched}
        )
        n_investors = len(investor_names)
        n_appearances = len(matched)
        names_display = ", ".join(investor_names[:5])
        if n_investors > 5:
            names_display += f" (+{n_investors - 5} more)"
        yield StatusEvent(
            phase="search",
            detail=f"Found {n_appearances} appearances from {names_display}",
        )

        # --- 4 & 5: Direct or Map-Reduce depending on count ------------------
        if len(matched) <= DIRECT_CONTEXT_LIMIT:
            async for event in self._stream_direct(question, matched):
                yield event
        else:
            async for event in self._stream_map_reduce(question, matched):
                yield event

    # -----------------------------------------------------------------------
    # Follow-up: conversational continuation without re-running the pipeline
    # -----------------------------------------------------------------------

    async def follow_up_stream(
        self,
        question: str,
        history: list[dict[str, str]],
    ) -> AsyncGenerator[StreamEvent, None]:
        """Route a follow-up: either re-run the pipeline or continue the conversation.

        1. Classify intent (RESEARCH vs FOLLOW_UP) with a cheap LLM call.
        2. RESEARCH → run the full query_stream pipeline (new entity extraction, etc.)
        3. FOLLOW_UP → direct LLM call with truncated conversation history.
        """
        clean_history = self._sanitize_history(history)

        # --- Intent classification ---
        intent = await asyncio.to_thread(self._classify_intent, question, clean_history)
        logger.info("Follow-up intent: %s for question: %s", intent, question[:80])

        if intent == "RESEARCH":
            # New research question — run the full pipeline
            async for event in self.query_stream(question):
                yield event
            return

        # --- Conversational follow-up ---
        yield StatusEvent(phase="reduce", detail="Continuing conversation...")

        system_prompt = load_system_prompt(self._settings.prompts_dir)
        follow_up_system = (
            (
                f"{system_prompt}\n\n"
                "You are continuing a conversation about investor research. "
                "The previous messages contain your earlier analysis. "
                "Answer the user's follow-up using that context. "
                "Be concise and direct. If the user asks you to summarize, "
                "reformat, or dig deeper, work from your previous answer — "
                "do not re-explain the full pipeline."
            )
            if system_prompt
            else (
                "You are continuing a conversation about investor research. "
                "Answer the follow-up using the prior conversation context."
            )
        )

        messages: list[dict[str, str]] = [
            {"role": "system", "content": follow_up_system},
        ]
        messages.extend(clean_history)
        messages.append({"role": "user", "content": question})

        async for chunk in self._async_stream(messages):
            yield ContentEvent(token=chunk)

    def _classify_intent(
        self,
        question: str,
        history: list[dict[str, str]],
    ) -> str:
        """Classify whether a follow-up needs new research or is conversational."""
        # Build a compact summary of conversation for classification
        summary_parts: list[str] = []
        for msg in history[-4:]:  # Only last 2 turns for classification
            role = msg["role"].upper()
            content = msg["content"][:500]
            summary_parts.append(f"{role}: {content}")
        conversation_summary = "\n\n".join(summary_parts)

        raw = self._provider.chat(
            [
                {"role": "system", "content": _INTENT_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Conversation so far:\n{conversation_summary}\n\n"
                        f"New user message: {question}"
                    ),
                },
            ],
            stream=False,
        )
        assert isinstance(raw, str)
        result = raw.strip().upper()
        return "RESEARCH" if "RESEARCH" in result else "FOLLOW_UP"

    @staticmethod
    def _sanitize_history(history: list[dict[str, str]]) -> list[dict[str, str]]:
        """Truncate and clean conversation history for safe LLM consumption.

        - Removes empty messages
        - Truncates long assistant messages
        - Ensures alternating user/assistant roles
        - Caps to MAX_HISTORY_TURNS most recent turn pairs
        """
        # Filter empty messages
        clean: list[dict[str, str]] = []
        for msg in history:
            content = msg.get("content", "").strip()
            if not content or content == "(Stopped)":
                continue
            # Truncate long assistant messages
            if msg["role"] == "assistant" and len(content) > MAX_ASSISTANT_MSG_CHARS:
                content = content[:MAX_ASSISTANT_MSG_CHARS] + "\n\n[... truncated]"
            clean.append({"role": msg["role"], "content": content})

        # Ensure alternating roles (merge consecutive same-role messages)
        merged: list[dict[str, str]] = []
        for msg in clean:
            if merged and merged[-1]["role"] == msg["role"]:
                merged[-1]["content"] += "\n\n" + msg["content"]
            else:
                merged.append(dict(msg))

        # Ensure starts with user message
        while merged and merged[0]["role"] != "user":
            merged.pop(0)

        # Cap to recent turns (1 turn = user + assistant)
        if len(merged) > MAX_HISTORY_TURNS * 2:
            merged = merged[-(MAX_HISTORY_TURNS * 2) :]
            # Ensure still starts with user
            while merged and merged[0]["role"] != "user":
                merged.pop(0)

        return merged

    # -----------------------------------------------------------------------
    # Sync query (kept for CLI / non-streaming callers)
    # -----------------------------------------------------------------------

    def query(
        self,
        question: str,
        *,
        stream: bool = True,
    ) -> str | Generator[str, None, None]:
        """Synchronous query — returns string or generator. No status events."""
        entities = extract_entities(question, self._provider)
        resolved_sectors = self._resolve_sectors(entities.topics)
        matched = self._find_appearances(entities, resolved_sectors)

        if not matched:
            return self._answer_no_data(question, stream=stream)

        matched.sort(key=lambda a: a.get("date", ""), reverse=True)

        if len(matched) <= DIRECT_CONTEXT_LIMIT:
            return self._answer_direct(question, matched, stream=stream)
        else:
            return self._answer_map_reduce(question, matched, stream=stream)

    # -----------------------------------------------------------------------
    # Sector resolution
    # -----------------------------------------------------------------------

    def _resolve_sectors(self, query_sectors: list[str]) -> list[str]:
        """Use LLM to match query sector terms to actual sector tags."""
        if not query_sectors:
            return []

        all_sectors = self._index.all_sectors
        if not all_sectors:
            return []

        prompt = _SECTOR_RESOLVE_PROMPT.format(sectors=json.dumps(all_sectors))
        sector_query = ", ".join(query_sectors)

        raw = self._provider.chat(
            [
                {"role": "system", "content": prompt},
                {"role": "user", "content": sector_query},
            ],
            stream=False,
        )
        assert isinstance(raw, str)

        try:
            text = raw.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1] if "\n" in text else text[3:]
                if text.endswith("```"):
                    text = text[:-3]
                text = text.strip()
            return json.loads(text)
        except (json.JSONDecodeError, TypeError):
            logger.warning("Sector resolution failed, using raw sectors")
            return query_sectors

    # -----------------------------------------------------------------------
    # Appearance matching
    # -----------------------------------------------------------------------

    def _find_appearances(
        self,
        entities: ExtractedEntities,
        resolved_sectors: list[str],
    ) -> list[dict]:
        """Collect appearances matching extracted entities.

        When multiple entity dimensions are present (e.g. investor + ticker),
        uses AND logic — only appearances matching ALL specified dimensions are
        returned. When a single dimension is present, returns all matches for
        that dimension. Tickers and sectors are treated as a single "topic"
        dimension (OR'd together) since they're complementary ways to find
        topic-relevant appearances.
        """
        if entities.is_empty:
            return list(self._index.appearances)

        # --- Topic matches: tickers OR sectors (complementary filters) ---
        topic_paths: set[str] | None = None
        topic_apps: dict[str, dict] = {}

        if entities.tickers or resolved_sectors:
            topic_paths = set()
            if entities.tickers:
                for app in self._index.appearances_for_companies(entities.tickers):
                    path_key = str(app.get("_path", id(app)))
                    topic_paths.add(path_key)
                    topic_apps[path_key] = app
            if resolved_sectors:
                for app in self._index.appearances_for_sectors(resolved_sectors):
                    path_key = str(app.get("_path", id(app)))
                    topic_paths.add(path_key)
                    topic_apps[path_key] = app

        # --- Investor matches ---
        investor_paths: set[str] | None = None
        investor_apps: dict[str, dict] = {}

        if entities.investors:
            investor_paths = set()
            for app in self._index.appearances:
                slug = app.get("investor_slug", "") or app.get("investor", "")
                for inv in entities.investors:
                    inv_lower = inv.lower()
                    if inv_lower in slug.lower() or any(
                        part in slug.lower() for part in inv_lower.split()
                    ):
                        path_key = str(app.get("_path", id(app)))
                        investor_paths.add(path_key)
                        investor_apps[path_key] = app
                        break

        # --- Intersect dimensions (AND logic) ---
        dimension_sets = [s for s in (topic_paths, investor_paths) if s is not None]

        if not dimension_sets:
            return []

        if len(dimension_sets) == 1:
            # Single dimension — return all matches
            matched_paths = dimension_sets[0]
        else:
            # Multiple dimensions — AND (intersect)
            matched_paths = dimension_sets[0].intersection(*dimension_sets[1:])

        # Collect apps, preferring topic_apps for richer metadata
        all_apps = {**investor_apps, **topic_apps}
        return [all_apps[p] for p in matched_paths if p in all_apps]

    # -----------------------------------------------------------------------
    # Async streaming: Direct (≤ DIRECT_CONTEXT_LIMIT files)
    # -----------------------------------------------------------------------

    async def _stream_direct(
        self,
        question: str,
        appearances: list[dict],
    ) -> AsyncGenerator[StreamEvent, None]:
        """Stream answer directly with all matched files in context."""
        all_sources = self._build_sources_list(appearances)
        yield StatusEvent(phase="reduce", detail="Generating answer...")

        messages = self._build_direct_messages(question, appearances)
        accumulated = ""
        async for chunk in self._async_stream(messages):
            accumulated += chunk
            yield ContentEvent(token=chunk)

        rewritten, cited_sources = self._filter_cited_sources(accumulated, all_sources)
        if rewritten != accumulated:
            yield ContentReplaceEvent(content=rewritten)
        yield SourcesEvent(sources=cited_sources)

    # -----------------------------------------------------------------------
    # Async streaming: Map-Reduce (> DIRECT_CONTEXT_LIMIT files)
    # -----------------------------------------------------------------------

    async def _stream_map_reduce(
        self,
        question: str,
        appearances: list[dict],
    ) -> AsyncGenerator[StreamEvent, None]:
        """Map in parallel, then reduce with budget-aware batching."""
        total = len(appearances)
        yield StatusEvent(
            phase="map", detail=f"Reading {total} posts...", progress=f"0/{total}"
        )

        # MAP phase: run all in parallel via asyncio.to_thread
        async def _map_one(app: dict) -> MapExtract | None:
            return await asyncio.to_thread(self._extract_one, question, app)

        tasks = [_map_one(app) for app in appearances]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        extracts: list[MapExtract] = []
        relevant_appearances: list[dict] = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.warning("Map failed for appearance %d: %s", i, result)
            elif result is not None:
                extracts.append(result)
                relevant_appearances.append(appearances[i])

        relevant = len(extracts)
        skipped = total - relevant
        yield StatusEvent(
            phase="map",
            detail=f"{relevant} relevant, {skipped} skipped",
            progress=f"{total}/{total}",
        )

        if not extracts:
            yield StatusEvent(phase="search", detail="No relevant content found")
            async for event in self._stream_no_data(question):
                yield event
            return

        # Group by investor, sort by date ascending within each group
        grouped = self._group_by_investor(extracts, relevant_appearances)

        # Flatten back to ordered list (investor-contiguous, time-ascending)
        ordered_extracts: list[MapExtract] = []
        ordered_appearances: list[dict] = []
        for _slug, pairs in grouped:
            for ext, app in pairs:
                ordered_extracts.append(ext)
                ordered_appearances.append(app)

        all_sources = self._build_sources_list(ordered_appearances)

        # Batch into ~REDUCE_BATCH_TARGET token chunks
        batches = self._batch_extracts(
            ordered_extracts, ordered_appearances
        )

        if len(batches) == 1:
            # Single batch — direct reduce, stream the answer
            yield StatusEvent(phase="reduce", detail="Synthesizing answer...")
            b_extracts, b_apps = batches[0]
            messages = self._build_reduce_messages(
                question, b_extracts, appearances=b_apps
            )
            accumulated = ""
            async for chunk in self._async_stream(messages):
                accumulated += chunk
                yield ContentEvent(token=chunk)
        else:
            # Hierarchical reduce — reduce each batch, then final reduce
            yield StatusEvent(
                phase="reduce",
                detail=f"Synthesizing {len(batches)} batches...",
            )
            batch_summaries: list[MapExtract] = []
            batch_apps_flat: list[dict] = []
            for bi, (b_extracts, b_apps) in enumerate(batches):
                yield StatusEvent(
                    phase="reduce",
                    detail=f"Batch {bi + 1}/{len(batches)}",
                    progress=f"{bi + 1}/{len(batches)}",
                )
                messages = self._build_reduce_messages(
                    question, b_extracts, appearances=b_apps
                )
                raw = await asyncio.to_thread(
                    self._provider.chat, messages, stream=False
                )
                assert isinstance(raw, str)
                # Wrap batch summary as a MapExtract for the final reduce
                batch_summaries.append(
                    MapExtract(
                        relevance="RELEVANT",
                        key_excerpts="",
                        analysis=raw,
                    )
                )
                batch_apps_flat.extend(b_apps)

            # Final reduce across batch summaries — stream this one
            yield StatusEvent(phase="reduce", detail="Final synthesis...")
            messages = self._build_reduce_messages(
                question, batch_summaries, appearances=batch_apps_flat
            )
            accumulated = ""
            async for chunk in self._async_stream(messages):
                accumulated += chunk
                yield ContentEvent(token=chunk)

        # Filter to cited sources only and renumber sequentially
        rewritten, cited_sources = self._filter_cited_sources(accumulated, all_sources)
        if rewritten != accumulated:
            yield ContentReplaceEvent(content=rewritten)
        yield SourcesEvent(sources=cited_sources)

    # -----------------------------------------------------------------------
    # Async streaming: No data fallback
    # -----------------------------------------------------------------------

    async def _stream_no_data(
        self,
        question: str,
    ) -> AsyncGenerator[StreamEvent, None]:
        """Emit a static message when no matching data found, encouraging contribution."""
        yield StatusEvent(phase="reduce", detail="No coverage in knowledge base")
        answer = self._no_data_message(question)
        yield ContentEvent(token=answer)

    # -----------------------------------------------------------------------
    # Async streaming helper
    # -----------------------------------------------------------------------

    async def _async_stream(
        self, messages: list[dict[str, str]]
    ) -> AsyncGenerator[str, None]:
        """Wrap the sync provider generator so each chunk is read in a thread.

        Without this, iterating the sync generator on the event loop blocks it,
        which prevents FastAPI/Starlette from flushing SSE frames incrementally.
        """
        gen = await asyncio.to_thread(self._provider.chat, messages, stream=True)
        assert not isinstance(gen, str)

        _sentinel = object()
        loop = asyncio.get_running_loop()
        while True:
            chunk = await loop.run_in_executor(None, lambda: next(gen, _sentinel))
            if chunk is _sentinel:
                break
            yield chunk  # type: ignore[misc]

    # -----------------------------------------------------------------------
    # Investor profile context
    # -----------------------------------------------------------------------

    def _investor_context(self, appearances: list[dict]) -> str:
        """Build a short context block identifying which investors appear.

        Includes fund, role, and sectors from profile.md so the LLM doesn't
        confuse the publication source (e.g. Robonomics) with the fund name.
        """
        # Collect unique investor slugs from the appearances
        slugs = {
            a.get("investor_slug", "") or a.get("investor", "") for a in appearances
        }

        # Build a lookup from slug -> profile
        lines: list[str] = []
        for profile in self._index.profiles:
            slug = profile.get("slug", "")
            if slug in slugs:
                name = profile.get("name", slug)
                fund = profile.get("fund", "")
                role = profile.get("role", "")
                parts = [name]
                if role:
                    parts.append(role)
                if fund:
                    parts.append(fund)
                lines.append(" — ".join(parts))

        if not lines:
            return ""
        return "# Investor Profiles\n\n" + "\n".join(f"- {l}" for l in lines)

    # -----------------------------------------------------------------------
    # Message builders (shared by sync and async paths)
    # -----------------------------------------------------------------------

    def _build_direct_messages(
        self, question: str, appearances: list[dict]
    ) -> list[dict[str, str]]:
        system_prompt = load_system_prompt(self._settings.prompts_dir)
        skills = load_skills(self._settings.skills_dir, question)
        if skills:
            skills_block = "\n\n---\n\n".join(skills)
            system_prompt = (
                f"{system_prompt}\n\n# Analytical Skills\n\n{skills_block}"
                if system_prompt
                else f"# Analytical Skills\n\n{skills_block}"
            )

        context_parts: list[str] = []
        for app in appearances:
            investor = app.get("investor", app.get("investor_slug", "unknown"))
            date = app.get("date", "")
            source = app.get("source", "")
            content = app.get("_content", "")
            header = f"## {investor} — {source} ({date})"
            context_parts.append(f"{header}\n\n{content}")

        investor_context = "\n\n---\n\n".join(context_parts)
        profiles_block = self._investor_context(appearances)

        # Count unique investors so the LLM doesn't hallucinate the number
        unique_investors = sorted(
            {a.get("investor", a.get("investor_slug", "unknown")) for a in appearances}
        )
        investor_count_note = (
            f"**Data scope: {len(unique_investors)} tracked investor(s) "
            f"({', '.join(unique_investors)}) across {len(appearances)} appearance(s).**"
        )

        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        user_parts = []
        if profiles_block:
            user_parts.append(profiles_block)
        user_parts.append(investor_count_note)
        user_parts.append(f"# Investor Research Data\n\n{investor_context}")
        user_parts.append(f"# Question\n\n{question}")

        messages.append({"role": "user", "content": "\n\n".join(user_parts)})
        return messages

    def _build_reduce_messages(
        self,
        question: str,
        extracts: list[MapExtract],
        appearances: list[dict] | None = None,
    ) -> list[dict[str, str]]:
        system_prompt = load_system_prompt(self._settings.prompts_dir)
        skills = load_skills(self._settings.skills_dir, question)
        if skills:
            skills_block = "\n\n---\n\n".join(skills)
            system_prompt = (
                f"{system_prompt}\n\n# Analytical Skills\n\n{skills_block}"
                if system_prompt
                else f"# Analytical Skills\n\n{skills_block}"
            )

        reduce_system = (
            f"{system_prompt}\n\n{_REDUCE_PROMPT}" if system_prompt else _REDUCE_PROMPT
        )

        # Extracts arrive pre-ordered: grouped by investor, date-ascending within each
        extract_parts: list[str] = []
        for i, ext in enumerate(extracts):
            # Build a rich header with investor, source, and date
            if appearances and i < len(appearances):
                app = appearances[i]
                investor = app.get("investor", app.get("investor_slug", "unknown"))
                source = app.get("source", "")
                date = app.get("date", "")
                header = f"### Extract [{i+1}] — {investor}, {source} ({date})"
            else:
                header = f"### Extract [{i+1}]"

            body = f"**Key excerpts:**\n{ext.key_excerpts}\n\n**Analysis:**\n{ext.analysis}"
            extract_parts.append(f"{header}\n\n{body}")

        numbered_extracts = "\n\n---\n\n".join(extract_parts)
        profiles_block = self._investor_context(appearances or [])

        # Count unique investors so the LLM doesn't hallucinate the number
        unique_investors = sorted(
            {
                a.get("investor", a.get("investor_slug", "unknown"))
                for a in (appearances or [])
            }
        )
        investor_count_note = (
            f"**Data scope: {len(unique_investors)} tracked investor(s) "
            f"({', '.join(unique_investors)}) across {len(extracts)} appearance(s).**"
        )

        user_parts = []
        if profiles_block:
            user_parts.append(profiles_block)
        user_parts.append(investor_count_note)
        user_parts.append(
            f"# Extracts from Investor Appearances\n\n{numbered_extracts}"
        )
        user_parts.append(f"# Question\n\n{question}")

        return [
            {"role": "system", "content": reduce_system},
            {"role": "user", "content": "\n\n".join(user_parts)},
        ]

    @staticmethod
    def _no_data_message(question: str) -> str:
        """Return a static message when no data matches, encouraging contribution."""
        return (
            "## No Coverage Yet\n\n"
            f"None of the investors in our knowledge base have publicly commented "
            f"on this topic — so we don't have sourced opinions to show you.\n\n"
            "OpenAlpha only surfaces views that investors actually expressed in "
            "podcasts, newsletters, interviews, and conferences. We never guess "
            "or use AI-generated opinions.\n\n"
            "### Help us grow the knowledge base\n\n"
            "If you know of a reputable source (podcast episode, Substack post, "
            "interview transcript) where an investor discusses this topic, "
            "consider contributing it:\n\n"
            "1. **Easiest** — [open an issue](https://github.com/XJ-Stone/openalpha/issues/new) "
            "with the source link and we'll ingest it\n"
            "2. **Hands-on** — follow the [contribution guide](https://github.com/XJ-Stone/openalpha/blob/main/CONTRIBUTING.md) "
            "to add an appearance file and open a PR\n"
        )

    # -----------------------------------------------------------------------
    # Grouping and batching for reduce phase
    # -----------------------------------------------------------------------

    @staticmethod
    def _group_by_investor(
        extracts: list[MapExtract],
        appearances: list[dict],
    ) -> list[tuple[str, list[tuple[MapExtract, dict]]]]:
        """Group extract/appearance pairs by investor, sorted by date within each.

        Returns a list of (investor_slug, [(extract, appearance), ...]) tuples.
        Within each investor group, appearances are sorted date-descending (newest
        first) so the reduce step anchors on the most recent views.
        """
        from collections import OrderedDict

        groups: OrderedDict[str, list[tuple[MapExtract, dict]]] = OrderedDict()
        for ext, app in zip(extracts, appearances):
            slug = app.get("investor_slug", "") or app.get("investor", "unknown")
            groups.setdefault(slug, []).append((ext, app))

        # Sort each group by date descending (newest first)
        for slug in groups:
            groups[slug].sort(key=lambda p: p[1].get("date", ""), reverse=True)

        return list(groups.items())

    @staticmethod
    def _estimate_tokens(extract: MapExtract) -> int:
        """Rough token estimate for an extract (~4 chars per token)."""
        text = extract.key_excerpts + extract.analysis
        return max(len(text) // 4, 50)

    def _batch_extracts(
        self,
        extracts: list[MapExtract],
        appearances: list[dict],
    ) -> list[tuple[list[MapExtract], list[dict]]]:
        """Split extracts into batches of ~REDUCE_BATCH_TARGET tokens.

        Tries to keep each investor's extracts contiguous within a batch.
        """
        batches: list[tuple[list[MapExtract], list[dict]]] = []
        current_extracts: list[MapExtract] = []
        current_apps: list[dict] = []
        current_tokens = 0

        for ext, app in zip(extracts, appearances):
            est = self._estimate_tokens(ext)
            # Start new batch if adding this would exceed target,
            # unless current batch is empty
            if current_tokens + est > REDUCE_BATCH_TARGET and current_extracts:
                batches.append((current_extracts, current_apps))
                current_extracts = []
                current_apps = []
                current_tokens = 0
            current_extracts.append(ext)
            current_apps.append(app)
            current_tokens += est

        if current_extracts:
            batches.append((current_extracts, current_apps))

        return batches

    # -----------------------------------------------------------------------
    # Source list builder
    # -----------------------------------------------------------------------

    @staticmethod
    def _build_sources_list(appearances: list[dict]) -> list[dict]:
        """Build a list of source references from appearances for citation display."""
        sources: list[dict] = []
        for i, app in enumerate(appearances):
            sources.append(
                {
                    "index": i + 1,
                    "investor": app.get(
                        "investor", app.get("investor_slug", "unknown")
                    ),
                    "date": str(app.get("date", "")),
                    "source": app.get("source", ""),
                    "url": app.get("url", ""),
                    "title": app.get("title", ""),
                }
            )
        return sources

    @staticmethod
    def _filter_cited_sources(
        answer: str, sources: list[dict]
    ) -> tuple[str, list[dict]]:
        """Filter to cited sources only and renumber both answer and sources.

        Returns (rewritten_answer, renumbered_sources) where citations [N]
        in the answer and source indices are renumbered sequentially (1, 2, 3...).
        """
        cited_indices = sorted({int(m) for m in re.findall(r"\[(\d+)\]", answer)})
        # Build old_index -> new_index mapping
        index_map = {old: new for new, old in enumerate(cited_indices, 1)}

        # Rewrite citations in answer: replace [old] with [new]
        def _replace_citation(m: re.Match) -> str:
            old = int(m.group(1))
            return f"[{index_map.get(old, old)}]"

        rewritten = re.sub(r"\[(\d+)\]", _replace_citation, answer)

        # Filter and renumber sources
        cited = []
        for s in sources:
            if s["index"] in index_map:
                cited.append({**s, "index": index_map[s["index"]]})
        return rewritten, cited

    # -----------------------------------------------------------------------
    # Map helper (sync, called via asyncio.to_thread)
    # -----------------------------------------------------------------------

    def _extract_one(self, question: str, app: dict) -> MapExtract | None:
        """Extract relevant content from a single appearance. Returns None if irrelevant."""
        content = app.get("_content", "")
        if not content:
            return None

        investor = app.get("investor", app.get("investor_slug", "unknown"))
        date = app.get("date", "")
        source = app.get("source", "")

        file_context = (
            f"Investor: {investor}\n"
            f"Date: {date}\n"
            f"Source: {source}\n\n"
            f"{content}"
        )

        result = self._provider.chat_structured(
            [
                {"role": "system", "content": _MAP_PROMPT},
                {
                    "role": "user",
                    "content": (f"Question: {question}\n\n" f"---\n\n{file_context}"),
                },
            ],
            response_model=MapExtract,
        )

        if result.relevance == "NOT_RELEVANT":
            return None
        return result

    # -----------------------------------------------------------------------
    # Sync answer methods (for CLI)
    # -----------------------------------------------------------------------

    def _answer_direct(
        self, question: str, appearances: list[dict], *, stream: bool
    ) -> str | Generator[str, None, None]:
        messages = self._build_direct_messages(question, appearances)
        return self._provider.chat(messages, stream=stream)

    def _answer_map_reduce(
        self, question: str, appearances: list[dict], *, stream: bool
    ) -> str | Generator[str, None, None]:
        from concurrent.futures import ThreadPoolExecutor, as_completed

        extracts: list[MapExtract] = []
        relevant_appearances: list[dict] = []
        with ThreadPoolExecutor(max_workers=5) as pool:
            futures = {
                pool.submit(self._extract_one, question, app): app
                for app in appearances
            }
            for future in as_completed(futures):
                app = futures[future]
                try:
                    extract = future.result()
                    if extract:
                        extracts.append(extract)
                        relevant_appearances.append(app)
                except Exception as exc:
                    logger.warning(
                        "Map failed for %s: %s",
                        app.get("_path", "unknown"),
                        exc,
                    )

        if not extracts:
            return self._answer_no_data(question, stream=stream)

        # Group by investor, sort by date within each
        grouped = self._group_by_investor(extracts, relevant_appearances)
        ordered_extracts: list[MapExtract] = []
        ordered_apps: list[dict] = []
        for _slug, pairs in grouped:
            for ext, app in pairs:
                ordered_extracts.append(ext)
                ordered_apps.append(app)

        batches = self._batch_extracts(ordered_extracts, ordered_apps)

        if len(batches) == 1:
            b_extracts, b_apps = batches[0]
            messages = self._build_reduce_messages(
                question, b_extracts, appearances=b_apps
            )
            return self._provider.chat(messages, stream=stream)

        # Hierarchical reduce
        batch_summaries: list[MapExtract] = []
        all_apps: list[dict] = []
        for b_extracts, b_apps in batches:
            messages = self._build_reduce_messages(
                question, b_extracts, appearances=b_apps
            )
            raw = self._provider.chat(messages, stream=False)
            assert isinstance(raw, str)
            batch_summaries.append(
                MapExtract(relevance="RELEVANT", key_excerpts="", analysis=raw)
            )
            all_apps.extend(b_apps)

        messages = self._build_reduce_messages(
            question, batch_summaries, appearances=all_apps
        )
        return self._provider.chat(messages, stream=stream)

    def _answer_no_data(
        self, question: str, *, stream: bool
    ) -> str | Generator[str, None, None]:
        answer = self._no_data_message(question)
        if stream:
            return iter([answer])  # type: ignore[return-value]
        return answer

    def reload_index(self) -> None:
        """Force-reload the investor index from disk."""
        self._index.reload()
