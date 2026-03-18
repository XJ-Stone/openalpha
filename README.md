# OpenAlpha

**Real investor opinions. Real sources. No roleplay.**

OpenAlpha is an open-source research agent that searches a curated knowledge base of real investor opinions — sourced from podcasts, Substacks, and interviews. Ask about any company or sector and get back what investors have actually said, with dates, sources, and conviction levels.

**[Try the live demo](https://openalpha-eight.vercel.app/)**

## Why OpenAlpha?

Projects like [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) roleplay as famous investors using system prompts. OpenAlpha takes the opposite approach: investors are **data**, not code. Every opinion in the knowledge base traces to a real public statement with a date and source link.

| | ai-hedge-fund | OpenAlpha |
|---|---|---|
| Opinions | LLM roleplays as "Warren Buffett" | Real quotes with sources |
| Data | Simulated | Traceable to specific podcasts and memos |
| Extensibility | Add a persona in code | Add a markdown file |

## Quick Start

```bash
git clone https://github.com/XJ-Stone/openalpha.git
cd openalpha/backend
pip install poetry && poetry install
cp .env.example .env   # Add your Anthropic, OpenAI, or Ollama config
```

```bash
# CLI
poetry run python cli.py analyze "What do investors think about NVDA?"
poetry run python cli.py investors

# API server
poetry run python api.py
# http://localhost:8000 — docs at /docs
```

### Frontend

```bash
cd frontend
npm install && npm run dev
# http://localhost:3000
```

## Example Queries

```
"What do investors think about NVDA?"
"Who is bullish on autonomous vehicles and why?"
"What has Freda Duan written about agentic commerce?"
"Compare what Jamin Ball and Thomas Reiner say about AI infrastructure"
"Which tracked investors have commented on UBER?"
```

## Knowledge Base

The knowledge base currently has **90 appearances** across **11 tracked investors**. Coverage varies — some investors have deep Substack archives, others have profiles awaiting community contributions.

| Investor | Fund | Appearances | Primary Source |
|---|---|---|---|
| Freda Duan | Altimeter Capital | 49 | [Robonomics](https://robonomics.substack.com) |
| Thomas Reiner | Altimeter Capital | 21 | [Robonomics](https://robonomics.substack.com) |
| Jamin Ball | Altimeter Capital | 13 | [Clouded Judgement](https://cloudedjudgement.substack.com) |
| Apoorv Agrawal | Altimeter Capital | 7 | [Apoorv's notes](https://apoorvagrawal.substack.com) |
| Brad Gerstner | Altimeter Capital | 0 | — |
| Bill Gurley | Benchmark | 0 | — |
| Cathie Wood | ARK Invest | 0 | — |
| Chamath Palihapitiya | Social Capital | 0 | — |
| David Friedberg | The Production Board | 0 | — |
| David Sacks | Craft Ventures | 0 | — |
| Stanley Druckenmiller | Duquesne | 0 | — |

Investors with 0 appearances have profiles but need community contributions to populate their views. See [INVESTORS.md](INVESTORS.md) for the full index.

## Architecture

```
User query → search.py (scan frontmatter, score relevance)
           → loader.py (assemble context: system prompt + skills + investor data)
           → agent.py  (orchestrate messages)
           → llm.py    (Anthropic / OpenAI / Ollama, streaming)
           → CLI or API SSE response
```

The knowledge base is **just markdown files** with YAML frontmatter. No database, no embeddings, no vector store. Search scans frontmatter fields (`companies`, `topics`, investor names) and scores relevance. The LLM receives matched investor data as context and generates a sourced analysis.

```
investors/<slug>/profile.md                          # Stable investor identity
investors/<slug>/appearances/YYYY-MM-DD-source.md    # One file per public appearance
skills/<name>/SKILL.md                               # Analytical frameworks
prompts/system.md                                    # Base agent identity
```

## How to Contribute

You don't need to be an engineer. The highest-impact contribution is adding investor opinions.

1. **Add investor opinions** — Summarize a podcast or interview into an appearance markdown file
2. **Add analytical skills** — Create a `SKILL.md` that teaches the agent a new analytical framework
3. **Add a source extractor** — Build an ingestion pipeline for a new source type (RSS, earnings calls, etc.)
4. **Improve the engine** — Search, API, frontend, or LLM integration

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions.

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, Poetry
- **Frontend**: Next.js 15, React 19, Tailwind CSS 4
- **LLM**: Anthropic Claude, OpenAI, or Ollama (local)
- **Data**: Markdown + YAML frontmatter (no database)
- **Deployment**: Railway (backend), Vercel (frontend)

## License

MIT
