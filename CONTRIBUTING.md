# Contributing to OpenAlpha

There are three ways to contribute to OpenAlpha. Pick whichever matches your background -- you don't need to be an engineer to add valuable data.

---

## Path 1: Add Investor Opinions (for finance people)

This is the highest-impact contribution. Every appearance you add makes the knowledge base more useful for everyone.

### What is an appearance?

An appearance is a markdown file summarizing what an investor said in a specific podcast episode, Substack post, interview, conference talk, or TV appearance. Each appearance file lives in the investor's directory and follows a standard template.

### Steps to add an appearance

#### Option A: Use the generation script (recommended)

If you have a transcript or source text, the `generate_appearance.py` script will extract structured opinions using an LLM:

```bash
cd backend

# From a transcript file
python scripts/generate_appearance.py \
  --transcript path/to/transcript.txt \
  --investor brad-gerstner \
  --date 2025-03-01 \
  --source "BG2Pod" \
  --type podcast \
  --url "https://youtube.com/watch?v=..."

# From pasted text (reads from stdin if no --transcript file)
python scripts/generate_appearance.py \
  --investor brad-gerstner \
  --date 2025-03-01 \
  --source "BG2Pod" \
  --type podcast \
  --url "https://youtube.com/watch?v=..." \
  < transcript.txt
```

The script outputs a formatted appearance file. Review it for accuracy before committing.

#### Option B: Ingest from Substack (easiest for newsletters)

If the investor publishes on Substack, you can ingest all their posts in one command:

```bash
cd backend

# If the Substack is already in the registry — just URL + time range:
python data-ingestion/substack.py --url https://robonomics.substack.com --months 6

# Dry run first to see what will be fetched:
python data-ingestion/substack.py --url https://robonomics.substack.com --months 6 --dry-run
```

The script auto-resolves the investor slug and source name from `backend/data-ingestion/_registry.yaml`. It skips posts that already have appearance files, so it's safe to re-run.

**Adding a new Substack to the registry:**

Edit `backend/data-ingestion/_registry.yaml` and add a 3-line entry:

```yaml
  - url: https://somenewsletter.substack.com
    investor: investor-slug
    source_name: Newsletter Name
```

Then create the investor directory and profile (see "Adding a new investor" below).

**One-off ingestion without editing the registry:**

```bash
python data-ingestion/substack.py \
  --url https://somenewsletter.substack.com \
  --investor investor-slug \
  --source-name "Newsletter Name" \
  --months 3
```

#### Option C: Write it manually

1. Copy the template from `templates/appearance-template.md`
2. Fill in the frontmatter (see requirements below)
3. Write up company-specific views and broader themes
4. Save as `investors/<slug>/YYYY-MM-DD-source-topic.md`

### Frontmatter requirements

Every appearance file **must** include this frontmatter:

```yaml
---
investor: brad-gerstner          # Slug matching the investor directory name
date: 2025-01-14                 # ISO date of the appearance
source: BG2Pod                   # Source name (podcast, publication, etc.)
type: podcast                    # One of: podcast, substack, interview, conference, tv, twitter
url: https://...                 # Link to the original source
companies: [NVDA, MSFT, SNOW]   # Tickers mentioned (THIS IS THE SEARCH INDEX)
sectors: [AI-infrastructure]     # Sectors discussed
---
```

**The `companies` array is the search index.** If a user asks "What do investors think about NVDA?" the search engine finds appearances where `NVDA` appears in the `companies` frontmatter. If you forget a ticker, that opinion won't surface in search results.

### Content guidelines

- **Source everything.** Every claim traces to a specific moment in the source material.
- **Date everything.** Opinions change. The date is essential context.
- **No fabricated quotes.** Use direct quotes when the investor said something memorable. Otherwise, paraphrase clearly (e.g., "Gerstner argued that..." not "Gerstner said '...'").
- **Include sentiment and conviction.** For each company view, note whether the investor is Bullish/Bearish/Neutral/Mixed and estimate conviction (high, medium, mentioned-in-passing).
- **Capture broader themes.** Market-level or sector-level views that aren't tied to a single company go in the "Broader Themes" section.

### Adding a new investor

Before adding appearances, the investor needs a directory and profile:

1. Create the directory: `investors/<slug>/appearances/`
2. Create `investors/<slug>/profile.md` following the format of existing profiles (see `investors/freda-duan/profile.md` for reference)
3. If they publish on Substack, add their URL to `backend/data-ingestion/_registry.yaml`
4. Run the ingestion script or generate a profile with:

```bash
cd backend
python scripts/generate_profile.py --investor <slug>
```

### After adding appearances: run post-ingest

After adding new appearances (manually or via scripts), run the reconciliation script:

```bash
cd backend

# Reconcile a single investor (updates profile metadata + INVESTORS.md)
python scripts/post_ingest.py --investor freda-duan

# Or reconcile all investors at once
python scripts/post_ingest.py --all

# Dry run to preview changes
python scripts/post_ingest.py --all --dry-run
```

This does three things (no LLM needed):
1. **Updates `profile.md` frontmatter** — aggregates `companies`, `sectors`, and `sources` from all appearances
2. **Regenerates `INVESTORS.md`** — the top-level index table with accurate appearance counts
3. **Runs lint** — catches frontmatter issues (missing fields, invalid tickers, etc.)

### PR process for appearances

1. Fork the repo
2. Create a branch: `git checkout -b add/brad-gerstner-2025-03-01-bg2pod`
3. Add your appearance file(s)
4. Run `python scripts/post_ingest.py --all` to reconcile metadata
5. Open a PR with:
   - Source link
   - Brief description of what's covered
   - Confirmation that you reviewed the output for accuracy
6. A maintainer will review for frontmatter consistency and source quality

---

## Path 2: Add Skills (for analysts)

Skills teach the agent analytical frameworks. When a user's query matches certain keywords, the relevant skill is loaded into the LLM's context.

### What is a skill?

A skill is a markdown file (`SKILL.md`) that contains instructions for how the agent should approach a specific type of analysis. Skills live in `skills/<skill-name>/SKILL.md`.

### When skills activate

The loader (`src/loader.py`) maps keywords in the user's query to skill files:

- "compare", "vs", "versus" -> `compare.md`
- "saas", "arr", "nrr", "churn" -> `saas-metrics.md`
- "dcf", "valuation" -> `valuation.md`
- "macro", "fed", "interest rate" -> `macro.md`
- Default (no keyword match) -> `analyze.md`

### Creating a new skill

1. Copy `templates/skill-template.md`
2. Create a directory: `skills/<skill-name>/SKILL.md`
3. Write concise instructions (the LLM reads this as context, so shorter is better)
4. Add keyword mappings to `src/loader.py` in the `_SKILL_KEYWORDS` list

### Skill template

```yaml
---
name: your-skill-name
description: >
  1-3 sentences: what this skill does and when it should activate.
---

# Skill Name

[Concise instructions for the agent. What framework to apply,
what to look for, how to structure the output.]
```

### Guidelines

- Keep skills focused. One analytical lens per skill.
- Write for the LLM, not for humans. Be direct and specific about what to do.
- Start minimal. Real usage will reveal what instructions actually help.
- Test your skill by running queries that should trigger it.

---

## Path 3: Improve the Engine (for engineers)

### Architecture overview

```
cli.py / api.py          Entry points (CLI and FastAPI)
    │
    ▼
src/search.py             Scans investor markdown, builds in-memory index,
                          scores query matches (ticker > sector > name)
    │
    ▼
src/loader.py             Assembles LLM context: system prompt + matched
                          investor data + relevant skills
    │
    ▼
src/llm.py                Provider abstraction (Anthropic, OpenAI, Ollama)
                          Supports both streaming and batch responses
```

### Key modules

- **`src/config.py`** -- Settings loaded from `.env` via pydantic-settings. All configuration is centralized here.
- **`src/search.py`** -- `InvestorIndex` class scans `investors/` for profile and appearance files, parses frontmatter, and provides a `search(query)` method with relevance scoring.
- **`src/loader.py`** -- Reads system prompts, loads skills based on query keywords, and assembles investor context organized by person.
- **`src/llm.py`** -- `LLMProvider` ABC with implementations for Anthropic, OpenAI, and Ollama. Factory function `get_provider(settings)` returns the configured provider.
- **`api.py`** -- FastAPI app with `/analyze` (SSE streaming), `/investors`, and `/investors/{slug}` endpoints.
- **`cli.py`** -- Terminal interface using Rich for formatted output with streaming support.

### Code standards

- Python 3.11+ with type annotations
- Use `from __future__ import annotations` for PEP 604 style
- Format with `black`, lint with `ruff`
- Tests go in `tests/` using pytest
- Keep dependencies minimal -- check `pyproject.toml` before adding new ones

### Testing

```bash
cd backend
poetry run pytest
```

When adding new functionality:
- Unit test search scoring logic in `tests/test_search.py`
- Unit test loader assembly in `tests/test_loader.py`
- Test LLM integration with mocks (don't call real APIs in CI)

### Areas for contribution

- **Search improvements**: Better relevance scoring, fuzzy matching, synonym handling
- **New LLM providers**: Gemini, Mistral, local models
- **Frontend**: The Next.js frontend in `frontend/` needs work
- **Caching**: Cache LLM responses for identical queries
- **Tools**: Give the agent the ability to fetch live price data, SEC filings, etc.
- **Testing**: More test coverage across all modules

---

## Quality Standards (all paths)

These apply to every contribution:

1. **Source everything.** No unsourced claims in the knowledge base.
2. **Date everything.** Opinions without dates are nearly useless.
3. **No fabricated quotes.** If you're not sure of the exact words, paraphrase.
4. **Frontmatter consistency.** The `companies` array is the search index. Missing tickers mean missing search results.
5. **Use standard tickers.** `NVDA` not `Nvidia`, `MSFT` not `Microsoft`, `META` not `Facebook`.
6. **Keep appearance files focused.** One source per file. If an investor appeared on two podcasts the same day, those are two files.
7. **Review LLM-generated content.** The generation scripts are helpful but not infallible. Always verify against the source.
