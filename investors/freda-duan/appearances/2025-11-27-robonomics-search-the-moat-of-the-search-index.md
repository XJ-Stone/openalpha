---
investor: freda-duan
date: 2025-11-27
source: Robonomics
type: substack
url: https://robonomics.substack.com/p/search-the-moat-of-the-search-index
companies: [GOOGL, MSFT, OPENAI, ANTHROPIC, BRAVE, PERPLEXITY]
topics: [search-index-moat, ai-agents, retrieval-synthesis, freshness-limitations]
companies_detail:
  - ticker: GOOGL
    focus: mention
  - ticker: MSFT
    focus: mention
  - ticker: OPENAI
    focus: mention
  - ticker: ANTHROPIC
    focus: mention
  - ticker: BRAVE
    focus: mention
  - ticker: PERPLEXITY
    focus: mention
topics_detail:
  - topic: search-index-moat
    focus: primary
  - topic: ai-agents
    focus: secondary
  - topic: retrieval-synthesis
    focus: secondary
  - topic: freshness-limitations
    focus: mention
source_length: 270
fetch_method: substack_api
fetch_id: search-the-moat-of-the-search-index
---

# Robonomics — November 27, 2025

A year or two ago, I was a bit nervous about whether GPT could handle fresh search well, given it can’t tap Google. If Google is the “better” search engine, why does ChatGPT – which is forced to use Bing – still return such high-quality results?

The key is the difference between Searching (what humans do) and Retrieving + Reading (what AI does). In many ways, the moat of the traditional search index is gone.

When you something, you normally type one query and look at the first or second result. If the top result is bad, you immediately think “Google failed.”

Google’s edge has always been in:

Ranking the single best link

Dealing with SEO spam, typos, long-tail queries

UI and instant answers, etc.

ChatGPT doesn’t operate like that. It has an “agent” advantage – it basically cheats by working harder (i.e. going through as many pages as needed). It uses multi-hop reasoning:

Ask Bing with query rewriting

Pull the top N results

Read them deeply and extract the relevant pieces

Synthesize an answer

Because it pulls from multiple sources, it naturally hides the failures of any single search result.

The gaps probably still show up in true edge cases: very long-tail or oddly phrased queries, ultra-fresh events (minutes or hours old), or heavily spammed / SEO-gamed topics.

I think this is an underappreciated point - for most queries, the moat of today’s search index is largely gone.

—

ChatGPT uses Bing.

Claude uses Brave Search (an independent, privacy-focused search engine).

Perplexity uses a combination of Bing, Google (via third parties), and its own index.

Gemini uses Google (obviously).
