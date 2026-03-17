# OpenAlpha

**Real investor opinions. Real sources. No roleplay.**

What have the smartest investors in tech publicly said about {stock}?

OpenAlpha is an open-source research agent that searches a community-curated knowledge base of real investor opinions sourced from podcasts, Substacks, interviews, and conferences. Ask a question about any company or sector and get back what elite investors have actually said -- with dates, sources, and conviction levels.

## How is this different from ai-hedge-fund?

| | ai-hedge-fund | OpenAlpha |
|---|---|---|
| Opinions | LLM roleplays as "Warren Buffett" | Real quotes from real investors with sources |
| Investors | Hard-coded personas in Python | Community-curated knowledge base of actual appearances |
| Data | Simulated | Traceable to specific podcasts, memos, and interviews |
| Extensibility | Add a new persona in code | Add a markdown file with a transcript summary |

**Real opinions, not roleplay. Investors are data, not code.**

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/XJ-Stone/openalpha.git
cd openalpha/backend
pip install poetry
poetry install
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your API key (Anthropic, OpenAI, or use Ollama locally)
```

### 3. Run the CLI

```bash
# Ask a research question
python cli.py analyze "What do investors think about NVDA?"

# List tracked investors
python cli.py investors

# View a specific investor
python cli.py investor brad-gerstner
```

### 4. Run the API server

```bash
python api.py
# Server starts at http://localhost:8000
# Docs at http://localhost:8000/docs
```

## Example Queries

```
"What do investors think about NVDA?"
"Who is bullish on Snowflake and why?"
"Compare what Gerstner and Cathie Wood say about AI infrastructure"
"What has Chamath said about fintech lately?"
"Which tracked investors have commented on MSFT?"
```

### Sample Output

```
Found 3 mentions of NVDA across 2 investors.

## Brad Gerstner (Altimeter Capital) — Bullish, HIGH conviction
"The most important company in the AI supply chain right now"
— BG2Pod, Jan 14, 2025

Gerstner views Nvidia as the primary beneficiary of the multi-year AI
infrastructure buildout. He emphasizes that enterprise GPU demand extends
through 2025-2026 and frames Nvidia as the core "picks and shovels" play.

## Cathie Wood (ARK Invest) — Mixed, MEDIUM conviction
...

### Consensus
Broadly positive on Nvidia's near-term positioning. Gerstner frames it as
infrastructure; Wood focuses on the innovation cycle. No tracked investor
is currently bearish on NVDA.

### Notable Gaps
Stanley Druckenmiller, Howard Marks, and Bill Gurley have not publicly
commented on Nvidia in our knowledge base.
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    User Query                        │
│          "What do investors think about NVDA?"       │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│                  CLI / API Layer                      │
│            cli.py  |  api.py (FastAPI)               │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│                  Search Engine                        │
│   src/search.py — scans frontmatter, scores matches  │
│   Ticker > Sector > Name matching with relevance     │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│                 Context Assembler                     │
│   src/loader.py — builds LLM context from results    │
│   System prompt + Investor data + Skills             │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│                   LLM Provider                       │
│   src/llm.py — Anthropic | OpenAI | Ollama           │
│   Streaming response back to user                    │
└──────────────────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
┌─────────────┐ ┌────────────┐ ┌────────────┐
│  investors/  │ │  skills/   │ │  prompts/  │
│  profiles +  │ │  analyze,  │ │  system    │
│  appearances │ │  compare,  │ │  prompt    │
│  (.md files) │ │  saas, ... │ │            │
└─────────────┘ └────────────┘ └────────────┘
```

The knowledge base is **just markdown files** with YAML frontmatter. No database, no embeddings, no vector store. Search works by scanning frontmatter fields (companies, sectors, investor names) and scoring relevance. The LLM receives matched investor data as context and generates a sourced analysis.

## How to Contribute

There are three ways to contribute, and you don't need to be an engineer for the first two:

1. **Add investor opinions** -- Summarize a podcast or interview into an `appearance.md` file
2. **Add analytical skills** -- Create a `SKILL.md` that teaches the agent a new framework
3. **Improve the engine** -- Work on search, the agent, the API, or the frontend

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions on each path.

## Tracked Investors

We currently track opinions from 10 investors. See [INVESTORS.md](INVESTORS.md) for the full index with funds, focus areas, and primary sources.

| Investor | Fund | Focus |
|---|---|---|
| Brad Gerstner | Altimeter Capital | Cloud, AI, Consumer Internet |
| Freda Duan | Altimeter Capital | Enterprise Software, AI |
| Chamath Palihapitiya | Social Capital | Fintech, Consumer, AI |
| David Sacks | Craft Ventures | Enterprise SaaS, AI |
| Jason Calacanis | Various | Early-stage, Marketplaces |
| Cathie Wood | ARK Invest | Disruptive Innovation |
| Stanley Druckenmiller | Duquesne | Macro, Tech |
| Howard Marks | Oaktree Capital | Credit, Market Cycles |
| Bill Gurley | Benchmark | Marketplaces, Internet |
| David Friedberg | The Production Board | Climate Tech, Biotech, AI |

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, pydantic
- **Frontend**: React / Next.js (TypeScript)
- **LLM**: Anthropic Claude, OpenAI GPT, or Ollama (local)
- **Data**: Markdown files with YAML frontmatter (no database required)
- **Search**: Frontmatter-based relevance scoring
- **CLI**: argparse + Rich

## Project Structure

```
openalpha/
├── backend/
│   ├── src/
│   │   ├── config.py      # Settings from .env
│   │   ├── search.py       # Frontmatter scanner and search index
│   │   ├── loader.py       # Context assembler for LLM
│   │   └── llm.py          # LLM provider abstraction
│   ├── scripts/
│   │   ├── generate_appearance.py  # Create appearance.md from transcript
│   │   └── generate_profile.py     # Synthesize profile.md from appearances
│   ├── api.py              # FastAPI server
│   ├── cli.py              # Terminal interface
│   └── pyproject.toml
├── investors/              # Knowledge base (one dir per investor)
│   └── brad-gerstner/
│       ├── profile.md
│       └── 2025-01-14-bg2pod-ai-infrastructure.md
├── skills/                 # Agent skills (analytical frameworks)
├── prompts/                # System prompts
├── templates/              # Templates for new content
├── frontend/               # Next.js web UI
├── CONTRIBUTING.md
├── INVESTORS.md
└── README.md
```

## License

MIT
