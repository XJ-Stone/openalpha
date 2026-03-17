# Tracked Investors

This is the index of all investors currently tracked in the OpenAlpha knowledge base.

| Investor | Fund | Focus | Appearances | Primary Sources |
|---|---|---|---|---|
| Apoorv Agrawal | Altimeter Capital | ai-agents, ai-app-market-share, ai-education-advantage, ai-labs-profitability, ... | 7 | Apoorv's notes |
| Bill Gurley | Benchmark |  | 0 |  |
| Brad Gerstner | Altimeter Capital |  | 0 |  |
| Cathie Wood | ARK Invest |  | 0 |  |
| Chamath Palihapitiya | Social Capital |  | 0 |  |
| David Friedberg | The Production Board |  | 0 |  |
| David Sacks | Craft Ventures |  | 0 |  |
| Freda Duan | Altimeter Capital | 0dte-options, ads-vs-take-rate, agent-memory, agentic-checkout, ... | 49 | Robonomics |
| Howard Marks | Oaktree Capital Management | credit, value-investing, macro, market-cycles | 0 | Oaktree Memos, Bloomberg, CNBC, podcasts |
| Jamin Ball | Altimeter Capital | agent-front-door, agentic-commerce, ai-agents, ai-capex-roi, ... | 13 | Clouded Judgement |
| Jason Calacanis | Various (Angel Investor, LAUNCH Fund) |  | 0 |  |
| Stanley Druckenmiller | Duquesne Family Office |  | 0 |  |
| Thomas Reiner | Altimeter Capital | agent-latency-constraints, agentic-checkout, agentic-commerce, ai-agents, ... | 21 | Robonomics |

## Adding a New Investor

To add a new investor to the knowledge base:

### 1. Create the investor directory

```bash
mkdir -p investors/<slug>/appearances
```

The slug should be lowercase and hyphenated (e.g., `brad-gerstner`, `cathie-wood`).

### 2. Create a profile

Copy the profile template and fill it in:

```bash
cp templates/profile-template.md investors/<slug>/profile.md
```

Required frontmatter fields:

```yaml
---
name: Full Name
slug: lowercase-hyphenated
fund: Fund Name
role: Title
aum: "$XB+" or "N/A"
topics: [topic1, topic2]
companies: [TICK1, TICK2]
sources: [Source1, Source2]
last_updated: YYYY-MM-DD
---
```

Alternatively, once you have at least one appearance file, you can generate a profile automatically:

```bash
cd backend
python scripts/generate_profile.py --investor <slug>
```

### 3. Add appearances

Each appearance is a separate markdown file in the investor's directory. See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions on creating appearance files.

File naming convention: `YYYY-MM-DD-source-topic.md`

Example: `2025-01-14-bg2pod-ai-infrastructure.md`

### 4. Run post-ingest

After adding appearances, reconcile metadata:

```bash
cd backend
python scripts/post_ingest.py --all
```

This updates profile frontmatter and regenerates this index file.

### 5. Open a PR

See [CONTRIBUTING.md](CONTRIBUTING.md) for the PR process.

## Investor Selection Criteria

We prioritize investors who:

- **Have public track records** in technology and growth investing
- **Share detailed views** on specific companies (not just broad market commentary)
- **Appear regularly** in podcasts, interviews, conferences, or written memos
- **Are influential** in how the market thinks about technology companies

This is not a ranking of the "best" investors. It is a curated set of voices whose public commentary is worth tracking systematically.
