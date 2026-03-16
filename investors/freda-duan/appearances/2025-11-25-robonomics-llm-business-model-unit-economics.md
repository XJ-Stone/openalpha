---
investor: freda-duan
date: 2025-11-25
source: Robonomics
type: substack
url: https://robonomics.substack.com/p/llm-unit-economics
companies: [OPENAI, ANTHROPIC, GOOGL, MSFT, AAPL, META, AMZN, NFLX, DIS]
sectors: [ai, ml-infrastructure, cloud-capex, streaming-media, search, digital-advertising, consumer-tech]
source_length: 1258
fetch_method: substack_api
fetch_id: llm-unit-economics
---

# Robonomics — November 25, 2025

I’ve been doing some deep thinking about the frontier-model business model. All of this is grounded in numbers leaked by The Information, NYT, etc.

1 - The Core: It’s a Compute-Burn Machine

At its heart, the model is brutally simple: almost all costs come from compute – inference, and especially training. Training follows something like a scaling law. Let’s assume costs rise ~5x every year; and ROI on training costs is 2x.

That creates a weird dynamic:

Year 1 training cost: 1

Year 2 revenue from that model: 2

But Year 2 training cost for the next model: 5

Net: +2 - 5 = -3

Run it forward and it gets worse:

Year 3 revenue: +10

Year 3 training cost: -25

Net: -15

Frontier models, as currently run, are negative-cash-flow snowballs. Every generation burns more cash than the one before.

For this to ever flip to positive cash flow, only two things can logically change:

A. Revenue grows much faster than 2x, or

B. Training cost growth slows from 5x a year to something like <2x

Anthropic’s CEO Dario Amodei has broken down scenario B (“training costs stop growing exponentially”) into two possible realities:

Source: time stamp ~17min

Physical/economic limits

You simply can’t train a model 5x bigger — not enough chips, not enough power, or the cost approaches world GDP.

Diminishing returns

You could train a bigger model, but the scaling curve flattens. Spending another 10x stops being worth it.

And here’s the key idea:

The moment you stop training a next 5x-bigger model, the P&L instantly looks amazing. Using our toy example: revenue +2, but no longer -5. Cash flow goes positive overnight.

2 - What OpenAI and Anthropic’s Numbers Reveal

Both companies’ leaked financial projections basically validate this framework.

OpenAI

OpenAI’s plan effectively assumes total compute capacity stops growing after 2028.

Translation: margins improve because training costs flatten. This is scenario B.

[IMAGE: chart/figure]

Anthropic

Anthropic’s model is different:

They assume the ROI per model increases each year. Spend 1, get back 5 instead of 2.

Their compute spend growth is also much more muted. From FY25 to FY28:

OpenAI: 8x

Anthropic: 3x

Using the framework above, they’re counting on both revenue ramp and slower cost growth.

[IMAGE: chart/figure]

[IMAGE: chart/figure]

Two companies. Two different ways to escape the negative-cash-flow treadmill.

3 - Is the Closest Analogy

In tech, capital-intensive models are rare, though not unprecedented. is a good analogy: for years it had deeply negative cash flow that worsened annually. They had to pour money into content upfront, and those assets depreciated over four years. In many ways it resembles data-center and model-training economics.

Peak cash burn in 2019: -3B

2020 cash flow: +2B

Why the sudden swing positive? COVID shut down production. Content spend stopped growing. Cash flow instantly flipped.

[IMAGE: chart/figure]

4 - The Endgame: Margins Arrive When Cost Growth Slows

 didn’t stop investing in content entirely – it just stopped *growing* that investment aggressively once it reached ~300M global subscribers. At that scale, stickiness is high, and they only need to maintain their position, not expand content spend 10x a year.

I don’t think OpenAI or Anthropic will ever stop training entirely. But they won’t need to grow training spend by multiples forever. At some point:

ROI per model goes up,

or scaling limits kick in,

or both.

And the moment annual training spend stops growing 5x a year, profit margins show up almost immediately.

That’s the strange thing about LLM economics:

It’s a burn machine…until suddenly it isn’t.

5 - Will AI end up looking more like streaming or more like search?

Streaming, search, and chatbots are all industries with low switching costs and no classic network effects. Yet streaming is fragmented while search became a near-monopoly. That contrast is the interesting part.

Streaming - fragmented by design

Content isn’t a commodity. It’s differentiated, non-exclusive, and lives on different platforms. So the market stays dispersed. YouTube, Netflix, Disney... each sits at single-digit share because each owns different shows.

Search - winner-take-almost-all

Google has ~90% share even though Bing isn’t that bad. Why?

Distribution/defaults are insanely powerful

Most people don’t choose a search engine. They accept what the device gives them. Google pays tens of billions per year to be the default.

Habit and brand

Google is a verb. Bing is not. The power of habit plus brand is wildly underrated (and I’m honestly a bit surprised by this).

Data flywheel (to some degree)

Better engine → more users → more data → better engine. I sometimes question how big this effect really is, but it definitely exists.

Ad ecosystem scale

Advertisers get more volume and better ROI on Google thanks to Search + YouTube + Maps + Android + Gmail. So they prioritize Google, which reinforces the lead.

Chatbots - closer to search than streaming?

Chatbots are more like search: outputs feel like commodities, and you want one assistant that remembers everything. Once you trust an agent, switching is rare - lock-in is even stronger than search. There will be regional/language pockets too (e.g., China).

At the user level: one core agent doing 70-90% of the work.

At the market level: 2-3 mega-assistants, not a single Google-style 90% winner.

Agents live across OS, messaging, productivity, and hardware - different companies will own different surfaces, so the world naturally splits into a few big poles. Apple, Google, Microsoft (maybe Meta/Amazon) will each push their own tightly integrated assistant. That almost guarantees at least two major cores (Apple vs. Windows/Android) plus a strong cross-platform player.

Compared to early : regulation is tighter, platforms are more fragmented; All of this makes a single monopoly far less likely.

Sources:

https://www.theinformation.com/articles/openai-spend-100-billion-backup-servers-ai-breakthroughs?rc=0cvbfp

https://www.theinformation.com/articles/openai-forecasts-revenue-topping-125-billion-2029-agents-new-products-gain?utm_source=chatgpt.com&rc=0cvbfp

https://www.theinformation.com/articles/anthropic-projects-70-billion-revenue-17-billion-cash-flow-2028?rc=0cvbfp

The information presented in this newsletter is the opinion of the author and does not necessarily reflect the view of any other person or entity, including Altimeter Capital Management, LP (”Altimeter”). The information provided is believed to be from reliable sources but no liability is accepted for any inaccuracies. This is for information purposes and should not be construed as an investment recommendation. Past performance is no guarantee of future performance. Altimeter is an investment adviser registered with the U.S. Securities and Exchange Commission. Registration does not imply a certain level of skill or training. Altimeter and its clients trade in public securities and have made and/or may make investments in or investment decisions relating to the companies referenced herein. The views expressed herein are those of the author and not of Altimeter or its clients, which reserve the right to make investment decisions or engage in trading activity that would be (or could be construed as) consistent and/or inconsistent with the views expressed herein.

This post and the information presented are intended for informational purposes only. The views expressed herein are the author’s alone and do not constitute an offer to sell, or a recommendation to purchase, or a solicitation of an offer to buy, any security, nor a recommendation for any investment product or service. While certain information contained herein has been obtained from sources believed to be reliable, neither the author nor any of his employers or their affiliates have independently verified this information, and its accuracy and completeness cannot be guaranteed. Accordingly, no representation or warranty, express or implied, is made as to, and no reliance should be placed on, the fairness, accuracy, timeliness or completeness of this information. The author and all employers and their affiliated persons assume no liability for this information and no obligation to update the information or analysis contained herein in the future.
