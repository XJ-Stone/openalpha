# next10x — Product Requirements Document

## What This Is

An open-source agent that answers: **"What have the smartest investors in tech publicly said about {stock}?"**

It searches a community-curated knowledge base of real investor opinions — extracted from podcasts, Substacks, interviews, conferences — and surfaces who said what, when, with source links. No inference. No roleplay. Just aggregated intelligence that would take hours to find manually.

Ships as a CLI, a FastAPI backend, and a React frontend.

## Why This Exists

virattt/ai-hedge-fund (48.7k stars) proved massive demand for "AI + famous investors + stock analysis." But his investors are system prompts — `"You are Warren Buffett"` — that roleplay investment philosophies. They don't know what Buffett actually said last quarter. His architecture is pre-skills era LangChain (each investor is a Python file with a hardcoded prompt).

next10x takes the opposite approach: **investors are defined by what they actually say, not by system prompts pretending to be them.** Each investor is a folder of markdown files containing real, timestamped, sourced quotes and positions. The AI reads their actual words to answer questions.

The architecture follows the Agent Skills open standard (2025+). Investor data, analytical skills, agent prompts, and engine code are fully separated — enabling three independent contribution paths (finance people add opinions, analysts add skills, engineers improve the engine).

## Core Principles

### 1. Don't Infer
The system ONLY surfaces opinions investors actually expressed. If Gerstner never mentioned HOOD, the response says "No public commentary found from Brad Gerstner." It does not guess based on adjacent positions or general philosophy. Restraint is the brand.

### 2. Investors Are Data, Not Code
Each investor is a folder of markdown files. Adding a new investor or updating an existing one requires zero code. A finance student who watched a podcast can contribute by writing a markdown file.

### 3. Progressive Disclosure
Profile.md is the lean entry point (always loaded). Appearance files are reference material loaded selectively based on query relevance. Skills load only when contextually triggered. This keeps context windows tight.

### 4. Skills Are Composable
Skills define how the agent approaches different tasks — from query modes ("analyze a stock") to analytical frameworks ("SaaS metrics"). They're all markdown files in `skills/`. The agent loads them based on context. Contributors can add skills without touching investor data or engine code.

### 5. Source Everything
Every claim links to a source with a date. No unsourced opinions. No undated claims.

---

## Folder Structure

```
next10x/
├── investors/                          # Community-curated knowledge base
│   ├── brad-gerstner/
│   │   ├── profile.md
│   │   └── appearances/
│   │       ├── 2025-12-15-bg2pod-ep52.md
│   │       ├── 2025-11-20-substack-annual-letter.md
│   │       └── 2025-09-08-cnbc-squawk.md
│   ├── freda-duan/
│   │   ├── profile.md
│   │   └── appearances/
│   ├── druckenmiller/
│   │   ├── profile.md
│   │   └── appearances/
│   └── cathie-wood/
│       ├── profile.md
│       └── appearances/
│
├── skills/                             # All skills (query modes + analytical)
│   ├── analyze/
│   │   └── SKILL.md                    # "how to answer questions about a stock"
│   ├── compare/
│   │   └── SKILL.md                    # "how to compare expert views on X vs Y"
│   └── saas-metrics/
│       └── SKILL.md                    # analytical skill (proof of concept)
│
├── prompts/
│   └── system.md                       # Base agent identity + "don't infer" rules
│
├── backend/
│   ├── api.py                          # FastAPI endpoints (thin layer)
│   ├── cli.py                          # CLI entry point (thin layer)
│   ├── src/
│   │   ├── search.py                   # Frontmatter scanner + index
│   │   ├── loader.py                   # Context assembler
│   │   ├── agent.py                    # Orchestrator
│   │   ├── llm.py                      # Provider abstraction
│   │   ├── config.py                   # Settings
│   │   ├── tools/                      # Simple data fetchers (V1: interface only)
│   │   │   └── base.py
│   │   └── subagents/                  # Independent reasoning agents (V1: interface only)
│   │       └── base.py
│   ├── scripts/
│   │   ├── generate_appearance.py      # LLM-assisted appearance file generation
│   │   └── generate_profile.py         # Generate profile from appearances + web search
│   ├── pyproject.toml
│   └── .env.example
│
├── frontend/                           # React/Next.js app, deploys separately
│   ├── package.json
│   └── ...
│
├── templates/
│   ├── profile-template.md
│   ├── appearance-template.md
│   └── skill-template.md
│
├── CONTRIBUTING.md
├── INVESTORS.md                        # Index of tracked investors
├── README.md
└── .gitignore
```

---

## File Formats

### profile.md

The stable identity of an investor. Always loaded when that investor is relevant. Keep under 2000 words. Generated from appearances + web search using `scripts/generate_profile.py`, then human-reviewed.

The `companies` array is an aggregated index of all companies the investor has publicly commented on across appearances.

```markdown
---
name: Brad Gerstner
slug: brad-gerstner
fund: Altimeter Capital
role: Founder & CEO
aum: "$20B+"
sectors: [cloud, AI-infrastructure, consumer-internet, enterprise-software]
companies: [SNOW, META, UBER]
sources: [BG2Pod, Altimeter Substack, CNBC]
last_updated: 2025-12-15
---

# Brad Gerstner

## Background
Founder and CEO of Altimeter Capital, a technology-focused investment firm.
Previously founded Altitude Digital and served as CEO of General Catalyst.
Known for concentrated, high-conviction bets on technology platform companies.
Early and vocal investor in Snowflake (pre-IPO), Meta (during 2022 drawdown),
and Uber.

## Investment Style
- Growth-at-reasonable-price with concentrated positions
- Focuses on "inevitable" technology trends and TAM expansion
- Values management quality and capital allocation discipline
- Willing to pay up for category-defining platforms
- Prefers companies with strong network effects or data moats

## Current Known Positions (from public statements)
- **SNOW**: Bullish, high conviction — "AI data layer" thesis
- **META**: Bullish, long since 2022 — restructuring and AI investment thesis
- **UBER**: Bullish — autonomous driving optionality + marketplace dominance

## How to Read Gerstner
When Gerstner says "inevitable," he means he's willing to hold through
volatility. When he references specific metrics (e.g., net revenue
retention, free cash flow margin), he's signaling deeper diligence vs.
a thematic mention. His Substack annual letters contain his most
considered, highest-conviction views. Podcast appearances are more
conversational and exploratory.
```

### appearance.md

One file per public appearance. Immutable once created. Date-first filenames for chronological sorting. Can be generated from transcripts/posts using `scripts/generate_appearance.py`, then human-reviewed.

The `sectors` array captures thematic coverage even when specific tickers aren't named.

```markdown
---
investor: brad-gerstner
date: 2025-12-15
source: BG2Pod Episode 52
type: podcast
url: https://youtube.com/watch?v=example
companies: [SNOW, META, UBER, MSFT]
sectors: [AI-infrastructure, cloud, consumer-internet]
---

# BG2Pod Episode 52 — Dec 15, 2025

## Company-Specific Views

**Snowflake (SNOW)** — Bullish, high conviction
"We've been adding to Snowflake. The AI data layer thesis is playing out
faster than we expected. Cortex is a game changer for enterprise adoption."
Sees Snowflake as the "picks and shovels" of enterprise AI — every company
needs a data layer before they can deploy AI models.

**Meta (META)** — Bullish, holding
Still considers META undervalued relative to its AI investment cycle.
Compared current CapEx spending to Amazon's AWS build-out in 2012-2015:
"Everyone thought Bezos was crazy spending on AWS. Zuckerberg is making
the same bet and the market is underpricing it."

**Uber (UBER)** — Bullish, watching closely
Mentioned autonomous driving optionality but noted Waymo partnership terms
need clarity before increasing conviction.

**Microsoft (MSFT)** — Mentioned, no position stated
Referenced Microsoft's Copilot rollout as evidence that enterprise AI
adoption is accelerating. Did not state a position.

## Broader Themes
- AI infrastructure spending is sustainable through 2027 at minimum
- Skeptical of "AI wrapper" companies with no data or distribution moat
- Enterprise software companies without AI integration will lose share
- "We're in the first or second inning of enterprise AI adoption"
```

---

## Skills

All skills live in `skills/` using the same SKILL.md format. Query mode skills (analyze, compare) and analytical skills (saas-metrics) are treated identically — the agent loads whichever is relevant to the question.

### skills/analyze/SKILL.md

```markdown
---
name: analyze
description: >
  Analyze what tracked investors have said about a company or topic.
  Use when the user asks about a specific stock, sector, or investor.
---

# Analyze

You are answering a user question about a company or investment topic.

## You have access to
- Investor profiles and appearances (loaded into context)
- Other skills (loaded when relevant)
- [Future] Tools for price data, filings, web search

## Goals
- Surface relevant investor opinions with sources and dates
- Apply analytical skills when they add context
- Highlight consensus, disagreements, and gaps
- Be honest about what you don't know

## Output guidelines
- Lead with a one-line summary (how many mentions, how many investors, sentiment tilt)
- Group by investor, ordered by recency of their commentary
- For each: name, fund, sentiment, conviction, key quote, date, source
- End with: consensus view, key disagreements, notable gaps (who hasn't commented)
- If all commentary is >6 months old, flag staleness
- If no investor has mentioned the company: say so clearly, suggest contributing
```

### skills/compare/SKILL.md

```markdown
---
name: compare
description: >
  Compare what different investors think about the same company or topic.
  Use when the user asks to compare views, or asks about disagreements.
---

# Compare

The user wants to understand where investors agree and disagree.

## Goals
- Present each investor's view side by side
- Highlight the specific points of agreement and divergence
- Note the reasoning behind each position, not just the conclusion
- Surface when investors are looking at different timeframes or metrics

## Output guidelines
- Brief intro stating what's being compared
- Side-by-side presentation of each investor's view with sources
- Explicit "where they agree" and "where they disagree" sections
- Note if any investor has changed their view over time
```

### skills/saas-metrics/SKILL.md (proof of concept, kept short)

```markdown
---
name: saas-metrics
description: >
  Key metrics for evaluating SaaS companies. Use when investor
  commentary references ARR, NDR, Rule of 40, or similar metrics.
---

# SaaS Metrics Context

When investors discuss SaaS companies, these benchmarks help
contextualize their statements:

- NDR >130% = elite, >120% = strong, >110% = healthy
- Rule of 40: Revenue growth % + FCF margin % should exceed 40
- Gross margin >75% is software-like
- "Efficient growth" = strong Rule of 40
- "Land and expand" = high NDR driving growth

Flag when investor is bullish but key metrics don't support it.
```

---

## Prompt

### prompts/system.md

The base agent identity. Always loaded. Skills are layered on top.

```markdown
You are the next10x research assistant. You surface what elite investors
have publicly stated about companies. You are backed by a curated
knowledge base of real investor opinions from podcasts, Substacks,
interviews, and conferences.

## Core Rules

1. **ONLY reference opinions investors actually expressed.** Every claim
   must trace to a specific appearance with a date and source.

2. **NEVER infer.** If an investor hasn't commented on a company, say
   "No public commentary found." Do not guess based on adjacent positions,
   investment style, or philosophy.

3. **Always cite source and date.** Format: "BG2Pod Ep 52, Dec 15 2025."

4. **Distinguish conviction levels:**
   - HIGH: Explicitly states a position, mentions adding/buying
   - MEDIUM: Clear opinion but no position confirmation
   - MENTIONED: Referenced in passing, no clear view

5. **Flag stale commentary.** >6 months old = warn the user.

6. **Highlight disagreements.** Opposing views between investors are
   among the most valuable signals. Surface them prominently.

7. **Note absence as information.** "None of the 12 tracked investors
   have commented on this company" is itself a data point.

8. **Never make buy/sell/hold recommendations.** You surface opinions
   and context. The user decides.

9. **Be concise.** Lead with findings, not preamble.
```

---

## Agent Architecture

### LLM Provider Abstraction

Thin wrapper around provider SDKs. No framework (no LangChain). Each provider is ~30 lines wrapping the official SDK. Support tools parameter from day one for future extensibility.

```python
# backend/src/llm.py
class LLMProvider:
    def chat(self, messages: list[dict], stream: bool = True, tools: list | None = None):
        """Send messages to LLM, optionally with tool definitions."""
        ...

class AnthropicProvider(LLMProvider): ...
class OpenAIProvider(LLMProvider): ...
class OllamaProvider(LLMProvider): ...   # community can add more
```

V1 ships with Anthropic + OpenAI. Adding DeepSeek, MiniMax, GLM, etc. is trivial since they follow the OpenAI chat completions format. Set `LLM_PROVIDER` and `LLM_MODEL` in `.env`.

### Tools (V1: interface only)

Simple data fetchers — an API call that returns data. For future use.

```python
# backend/src/tools/base.py
class Tool:
    name: str
    description: str
    def run(self, **kwargs) -> dict: ...
```

Future tools: `price.py` (stock price/OHLCV), `search.py` (web search for recent news).

### Sub-Agents (V1: interface only)

Independent reasoning agents that get their own system prompt, tools, and LLM call. For complex multi-step analysis that goes beyond a simple data fetch.

```python
# backend/src/subagents/base.py
class SubAgent:
    name: str
    description: str
    system_prompt: str
    tools: list[Tool]
    def run(self, question: str, context: dict) -> str: ...
```

Future sub-agents: `filing.py` (analyze 13F changes), `technical.py` (price action + entry points).

The main agent in `agent.py` orchestrates — it decides which tools and sub-agents to invoke based on the query, collects their outputs, and synthesizes the response.

### Core Engine Flow

```
User question
    ↓
search.py — scan frontmatter for matching tickers/sectors
    ↓
loader.py — assemble context (profiles + appearances + skills)
    ↓
agent.py — build messages (system prompt + skills + investor context + question)
    ↓
llm.py — call provider, stream response
    ↓
Output (CLI terminal or API response)
```

---

## Generating .md Files

### Appearance Generation

```
backend/scripts/generate_appearance.py
```

Input: a transcript (text file, YouTube URL, or pasted text) + investor slug + metadata (date, source name, URL).

Process: Sends the transcript to the LLM with a system prompt that extracts company-specific views, quotes, sentiment, conviction levels, sectors, and broader themes. Outputs a draft appearance.md file.

The contributor reviews, edits if needed, and PRs it. **Human-in-the-loop, not fully automated.** The LLM extracts, the human verifies.

### Profile Generation

```
backend/scripts/generate_profile.py --investor brad-gerstner
```

Input: all existing appearance files for an investor + web search for biographical background.

Process: Reads all appearances, synthesizes investment style and current positions from actual statements, fetches background info via web search, outputs a draft profile.md.

Key principle: **appearances are the source of truth, profiles are derived summaries.** Profile.md should be regenerable at any time. When new appearances are added, re-run the generator to update the profile.

Both scripts use the same LLM abstraction from `backend/src/llm.py`.

---

## Example Questions

These represent the range of user queries the agent should handle:

**Stock lookup (core V1)**
- "What do experts say about SNOW?"
- "Anyone talking about Palantir?"
- "What's the sentiment on HOOD?"

**Investor-specific (core V1)**
- "What has Gerstner said lately?"
- "What is Cathie Wood's current view on Tesla?"

**Sector/thematic (V1, matches on sector frontmatter)**
- "Who's bullish on AI infrastructure?"
- "What are experts saying about fintech right now?"

**Comparison (V1, uses compare skill)**
- "How do Gerstner and Druckenmiller differ on AI spending?"

**Discovery (V1, scans broadly)**
- "What stocks are getting the most attention from tracked investors?"
- "Any contrarian views in the dataset?"

All question types use the same engine — the question determines which frontmatter fields match and which skills activate. No different code paths.

---

## Frontend

Separate React/Next.js app deployed independently. Talks to the backend API.

### Backend API Endpoints

```
POST /analyze          ← takes { question: string }, streams LLM response
GET  /investors        ← list all tracked investors (from profile frontmatter)
GET  /investors/{slug} ← investor profile + list of appearances
```

### Frontend Pages (V1, keep minimal)

- **Home / Search**: Search box, submit a question. Show streaming response with investor cards, sentiment badges, source links.
- **Investors Index**: Grid/list of all tracked investors with appearance counts and sectors.
- **Investor Profile**: Single investor view — profile info + chronological list of appearances.

The frontend is where the README screenshot comes from. A clean UI showing investor cards with sentiment, quotes, and sources is 10x more shareable than terminal output.

---

## Templates

### templates/profile-template.md

```markdown
---
name: [Full Name]
slug: [lowercase-hyphenated]
fund: [Fund Name]
role: [Title]
aum: [AUM if known, or "N/A"]
sectors: [sector1, sector2]
companies: [TICK1, TICK2]
sources: [Source1, Source2]
last_updated: YYYY-MM-DD
---

# [Full Name]

## Background
[2-3 sentences: who they are, career highlights]

## Investment Style
[3-5 bullet points distilled from actual public statements]

## Current Known Positions (from public statements)
[Companies with sentiment and one-line thesis. Only publicly stated positions.]

## How to Read [Name]
[1-2 paragraphs: what signals high conviction vs. casual mention,
which sources contain their most considered views]
```

### templates/appearance-template.md

```markdown
---
investor: [slug]
date: YYYY-MM-DD
source: [Source Name]
type: [podcast | substack | interview | conference | tv | twitter]
url: [link]
companies: [TICK1, TICK2]
sectors: [sector1, sector2]
---

# [Source Name] — [Month DD, YYYY]

## Company-Specific Views

**[Company] ([TICKER])** — [Bullish/Bearish/Neutral/Mixed], [conviction]
[What they said with relevant quotes and context.]

## Broader Themes
[Market-level or sector-level views not tied to a single company.]
```

### templates/skill-template.md

```markdown
---
name: [lowercase-hyphenated]
description: >
  [1-3 sentences: what this skill does and when it should activate.]
---

# [Skill Name]

[Concise instructions for how the agent should use this framework.
Keep it short until real usage reveals what's actually helpful.]
```

---

## Configuration

### .env.example

```
# LLM Provider: anthropic | openai | ollama
LLM_PROVIDER=anthropic
LLM_MODEL=claude-sonnet-4-20250514

# API Keys
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# Ollama (local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Display
VERBOSE=false
```

---

## Initial Content Plan

Ship with 8-10 investors, each with 5-15 appearances:

| Investor | Fund | Primary Sources | Target Appearances |
|---|---|---|---|
| Brad Gerstner | Altimeter Capital | BG2Pod, Substack | 15 |
| Freda Duan | Altimeter Capital | BG2Pod | 5 |
| Chamath Palihapitiya | Social Capital | All-In Pod, X | 15 |
| David Sacks | Craft Ventures | All-In Pod, X | 10 |
| Jason Calacanis | Various | All-In Pod, X | 8 |
| Cathie Wood | ARK Invest | ARK Webcasts, CNBC | 10 |
| Stanley Druckenmiller | Duquesne | Conferences, Bloomberg | 5 |
| Howard Marks | Oaktree | Memos, Interviews | 5 |
| Bill Gurley | Benchmark | Podcast appearances | 5 |
| David Friedberg | Various | All-In Pod | 8 |

~85-100 appearance files at launch. Use `scripts/generate_appearance.py` to accelerate creation from transcripts, with human review on every file.

---

## Future Roadmap (Not in V1)

- **13F integration**: Sub-agent that parses SEC filings. Enable "say vs. do" analysis.
- **Technical analysis sub-agent**: Chart patterns, entry points, support/resistance.
- **Track record scoring**: When an investor made a call, what happened 3/6/12 months later?
- **Corporate investment signals**: Track strategic investments as leading indicators.
- **Auto-ingestion**: RSS, YouTube transcript API, Twitter API for semi-automated appearance generation.
- **"What would X do?" mode**: Grounded simulation based on real historical statements.

---

## Claude Code Build Instructions

### Execution Strategy

Use Claude Code's multi-agent capabilities for parallel work:

- **Subagent 1**: Investor profiles and appearance files (content generation)
- **Subagent 2**: Skills, prompts, and templates
- **Subagent 3**: Backend engine code (`backend/src/`)
- **Subagent 4**: Backend API + CLI (`backend/api.py`, `backend/cli.py`)
- **Subagent 5**: Frontend scaffold
- **Subagent 6**: README, CONTRIBUTING.md, INVESTORS.md, config files

### Priorities

1. **Correctness over speed.** YAML frontmatter must be consistent across all files. The `companies` and `sectors` arrays are the search index — get them right.
2. **Don't cut corners on the search/loader logic.** This is the core product.
3. **Test the full loop.** `next10x analyze SNOW` should find appearances, load profiles, assemble context, stream a well-formatted response.
4. **Prioritize code quality.** Type hints, docstrings, error handling, clean separation. Token cost doesn't matter — output quality does.

### Code Standards
- Python 3.11+, Poetry for dependencies
- Type hints throughout
- Docstrings on public functions
- `pathlib` for file operations
- `python-frontmatter` for YAML parsing
- `rich` for CLI terminal output
- FastAPI for backend API with streaming support
- Error handling for missing API keys, empty results, malformed frontmatter
- Clean separation: search knows nothing about LLMs, agent knows nothing about filesystem

### Content Notes
When creating investor appearance files, use real publicly available information. Use actual quotes from public sources where available. Do not fabricate quotes — paraphrase clearly and note it if exact wording is unknown. Always include source URLs. Prioritize recency (2024-2025) and specificity (named companies with clear views).