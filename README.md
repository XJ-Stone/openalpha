# OpenAlpha

**Real investor opinions. Real sources. No roleplay.**

OpenAlpha is a research agent that searches a knowledge base of real investor opinions — sourced from podcasts, Substacks, and interviews. Ask about any company or sector and get back what investors have actually said, with dates, sources, and conviction levels.

**[Try the live demo](https://openalpha-eight.vercel.app/)**

Most AI investment tools simulate investor behavior — predefined analysis pipelines that assume how an investor would think, with LLMs roleplaying as specific personas. OpenAlpha skips the simulation. Investors are **data**, not personas — every opinion traces to a real public statement with a date and source link.

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

## How It Works

The knowledge base is markdown files with YAML frontmatter — no database, no embeddings. Search scans frontmatter fields (`companies`, `topics`, investor names), scores relevance, and passes matched investor data to the LLM as context.

```
User query → search.py  (scan frontmatter, score relevance)
           → loader.py  (assemble context: system prompt + skills + investor data)
           → agent.py   (orchestrate messages)
           → llm.py     (Anthropic / OpenAI / Ollama, streaming)
           → CLI or API response
```

```
investors/<slug>/profile.md                        # Investor identity
investors/<slug>/appearances/YYYY-MM-DD-source.md  # One file per public appearance
skills/<name>/SKILL.md                             # Analytical frameworks
prompts/system.md                                  # Base agent identity
```

### Ingestion

New appearances can be ingested from Substacks, YouTube transcripts, or local files:

```bash
cd backend
poetry run python -m ingestion substack --url https://robonomics.substack.com --months 6
poetry run python -m ingestion youtube --url "https://youtube.com/watch?v=..." --investor brad-gerstner --date 2025-03-01 --source-name "BG2Pod"
```

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, Poetry
- **Frontend**: Next.js 15, React 19, Tailwind CSS 4
- **LLM**: Anthropic Claude, OpenAI, or Ollama (local)
- **Data**: Markdown + YAML frontmatter
- **Deployment**: Railway (backend), Vercel (frontend)

## License

MIT
