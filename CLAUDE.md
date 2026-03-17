# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

OpenAlpha is an open-source research agent that surfaces real, sourced investor opinions about stocks. Unlike ai-hedge-fund (which roleplays as investors via system prompts), OpenAlpha treats investors as **data** — markdown files with YAML frontmatter containing actual quotes, dates, and sources from podcasts, Substacks, and interviews. No inference, no roleplay.

## Build & Run Commands

### Backend (Python 3.11+, Poetry)
```bash
cd backend
poetry install                          # Install dependencies
poetry run python api.py                # Start FastAPI server (localhost:8000)
poetry run python cli.py analyze "..."  # CLI query
poetry run pytest                       # Run all tests
poetry run pytest tests/test_search.py  # Single test file
```

### Frontend (Next.js 15, React 19, Tailwind 4)
```bash
cd frontend
npm install
npm run dev     # Dev server
npm run build   # Production build
npm run lint    # ESLint
```

### Data Ingestion
```bash
cd backend
python data-ingestion/substack.py --url <substack-url> --months 6   # Ingest Substack posts
python scripts/generate_appearance.py --transcript <file> --investor <slug> --date YYYY-MM-DD --source "Name" --type podcast --url "..."
python scripts/generate_profile.py --investor <slug>                 # Generate profile from appearances
python scripts/post_ingest.py --all                                  # Reconcile metadata after adding appearances
python scripts/lint_investors.py                                     # Lint frontmatter
```

### Deployment
Backend deploys via Railway (`railway.toml` uses `backend/Dockerfile`). Frontend deploys separately (Next.js).

## Architecture

### Core Engine Flow
```
User query → search.py (frontmatter scan + relevance scoring)
           → loader.py (assemble context: system prompt + skills + investor data)
           → agent.py (orchestrate, build messages)
           → llm.py (Anthropic/OpenAI/Ollama, streaming)
           → CLI terminal or API SSE response
```

### Key Design Decisions
- **No database, no embeddings.** The entire knowledge base is markdown files with YAML frontmatter. Search works by scanning frontmatter fields (`companies`, `sectors`, investor names) and scoring relevance.
- **No LangChain.** LLM provider abstraction is a thin wrapper (~30 lines per provider) around official SDKs.
- **Progressive context loading.** `profile.md` always loads for matched investors; appearance files load selectively by relevance. Skills load only when query keywords match.
- **Clean separation.** Search knows nothing about LLMs; the agent knows nothing about the filesystem.

### Backend Modules (`backend/src/`)
- `config.py` — pydantic-settings, loads from `.env` (LLM_PROVIDER, API keys)
- `search.py` — `InvestorIndex` scans `investors/` frontmatter, provides `search(query)` with scoring (ticker > sector > name)
- `loader.py` — Assembles LLM context; maps query keywords to skills via `_SKILL_KEYWORDS`
- `llm.py` — `LLMProvider` ABC with Anthropic/OpenAI/Ollama implementations; factory `get_provider(settings)`
- `agent.py` — Orchestrator that builds messages and calls LLM
- `entity.py` / `appearance.py` — Data models

### API Endpoints (`backend/api.py`)
- `POST /analyze` — SSE streaming LLM response for a question
- `GET /investors` — List all tracked investors
- `GET /investors/{slug}` — Investor profile + appearances

### Frontend (`frontend/src/`)
- Next.js App Router in `app/`
- Main page (`page.tsx`) — search/chat interface with streaming responses
- `components/` — ChatMessage, EntityChips, EntityDrawer, InvestorCard, ResponseStream, SearchBar, SentimentBadge, ThinkingSteps
- `lib/api.ts` — Backend API client

### Content Structure
- `investors/<slug>/profile.md` — Stable investor identity (always loaded when relevant)
- `investors/<slug>/YYYY-MM-DD-source-topic.md` — Immutable appearance files (one per public appearance)
- `skills/<name>/SKILL.md` — Analytical frameworks loaded by query context
- `prompts/system.md` — Base agent identity and "don't infer" rules
- `templates/` — Templates for new profiles, appearances, and skills

## Core Principles

1. **Don't infer.** Only surface opinions investors actually expressed. If no data exists, say so.
2. **Source everything.** Every claim needs a date and source link.
3. **Frontmatter is the search index.** The `companies` array in appearance frontmatter is how search finds content. Missing tickers = missing results.
4. **Use standard tickers.** `NVDA` not `Nvidia`, `META` not `Facebook`.

## Code Standards

- Python: 3.11+, type hints, `pathlib` for file ops, `python-frontmatter` for YAML
- Frontend: TypeScript, Tailwind CSS
- Config via `.env` — set `LLM_PROVIDER` (anthropic/openai/ollama) and `LLM_MODEL`
