---
investor: freda-duan
date: 2026-02-08
source: Robonomics
type: substack
url: https://robonomics.substack.com/p/org-design-and-reorgs
companies: [META, HOOD, REVOLUT, TOSS, SHOP, AAPL, SQ, COIN, UBER, DASH, ABNB, PG, UL, SPACEX, XAI, TSLA]
topics: [org-design, reorg-investment-opportunity, gm-vs-centralized, ai-org-centralization]
companies_detail:
  - ticker: META
    focus: primary
  - ticker: HOOD
    focus: primary
  - ticker: REVOLUT
    focus: primary
  - ticker: TOSS
    focus: primary
  - ticker: SHOP
    focus: primary
  - ticker: AAPL
    focus: primary
  - ticker: SQ
    focus: secondary
  - ticker: COIN
    focus: mention
  - ticker: UBER
    focus: mention
  - ticker: DASH
    focus: mention
  - ticker: ABNB
    focus: mention
  - ticker: PG
    focus: mention
  - ticker: UL
    focus: mention
  - ticker: SPACEX
    focus: mention
  - ticker: XAI
    focus: mention
  - ticker: TSLA
    focus: mention
topics_detail:
  - topic: org-design
    focus: primary
  - topic: reorg-investment-opportunity
    focus: primary
  - topic: gm-vs-centralized
    focus: secondary
  - topic: ai-org-centralization
    focus: secondary
source_length: 1403
fetch_method: substack_api
fetch_id: org-design-and-reorgs
---

# Robonomics — February 08, 2026

I’ve always been fascinated by two things: 1/ how different companies design their org structures, and 2/ what it signals when a company goes through a major reorg or restructuring.

1/ Org structure: no one-size-fits-all

Broadly, companies sit on a spectrum from centralized to single-GM.

Centralized: decision-making, product strategy, and core engineering are tightly controlled at the center. This works best when coherence matters more than speed - a single system, brand, or architecture where fragmentation creates tech debt or UX inconsistency.

Single GM: businesses are run as semi-autonomous units with clear P&L ownership. This works when speed, local optimization, and accountability matter more than perfect cohesion.

A. Common patterns

Centralized

High premium on end-to-end quality, architectural integrity, and brand consistency. Typical in “one-system” products

Examples: Apple, Airbnb

Single GM

Optimized for portfolios of distinct businesses, categories, or geographies. 

Speed and ownership beat strict coordination

Examples: Common in CPG (P&G, Unilever) and multi-country, regulated businesses (often country GMs, e.g., Revolut)

Hybrid

GM / vertical / geo owners paired with shared platform teams (core eng, data, infra, risk, compliance, brand). This only works if leadership is psychologically comfortable giving up control and pushing decisions down to BU leaders

Examples: Marketplaces and multi-line fintechs (Uber, DoorDash, Robinhood, Coinbase, Revolut)

B. 180-degree org reversals can happen

Robinhood

Centralized → GM-led (2022)

Arguably a major contributor to the sharp acceleration in product velocity that followed

Square

GM-led → centralized after Dorsey returned

A classic response when coordination costs explode, architecture degrades, or brand/system coherence becomes the bottleneck after rapid expansion

[IMAGE: chart/figure]

2/ Restructuring as an investment opportunity

Major restructurings often create windows to own good companies while sentiment is messy and execution risk is over-discounted.

A few that just/ are going through major restructurings:

Meta

Shopify

Apple

SpaceX / xAI / Tesla (potentially)

Meta

Old setup (early Llama era): federated AI

Llama lived closer to FAIR, not as a universal platform

Ads, Instagram, Integrity, Reality Labs often made local decisions on models, training, and priorities

New setup (MSL era): centralized AI platform

AI reorganized into Meta Superintelligence Labs (MSL)

Clear lanes across frontier models, applied research, infrastructure, and FAIR

Goal: one pipeline from frontier training → productization → deployment

Operating model shift

Core teams own base models, training recipes, evals, tooling

Product teams adapt via fine-tuning, distillation, routing, RAG, on-device variants - not full end-to-end foundation training

Compute elevated

Creation of Meta Compute centralizes capacity planning and infra

Reinforces the “shared platform serving many products” model

Org signal

Fewer layers, tighter mandate, faster decision velocity

Headcount trimmed in legacy areas while hiring continues in frontier-focused teams

Shopify

Leadership shake-up (mid–late 2025)

~8 senior leaders exited across ops, revenue, partnerships, design, marketing, and Shop/Shop Pay

COO role redefined

General Counsel elevated to COO

Signals heavier AI, partner, and compliance complexity vs. classic ops execution

Commercial org rework

Push upmarket / enterprise

Sales coverage shifted from geo-based to vertical-based

Shop Pay positioned as an enterprise wedge

AI + product leadership changes

Product leadership reshuffled around merchant data, Catalog, and OpenAI checkout

Clear focus on agent-ready commerce primitives

Flattening

Targeted cuts framed as removing management layers

Partnerships org reworked again in early 2026, consistent with tighter AI strategy

Apple

AI pulled into Software Engineering

Siri leadership moved under Craig Federighi’s software org

AI leadership now reports through the team that ships iOS/macOS, not a standalone research pillar

Implication: AI is execution-first, not exploratory

Design re-anchored under Hardware

New “executive sponsor” model with Hardware Engineering leadership

Tighter coupling of design + engineering

Also reads as succession grooming, not just org cleanup

A few interesting case studies in org structure

Robinhood (HOOD)

Shift to a GM model (mid-2022): Moved from a functionally matrixed setup to clear General Manager ownership, where each GM runs an individual business end-to-end (P&L, roadmap, execution). The explicit goals were cost discipline and clear accountability.

Primary objective: unlock product velocity. Management framed the reorg as a way to reduce coordination overhead and speed up shipping.

Operating model change: Centralized CPO + centralized engineering pools → decentralized business units.

Engineering now reports into the three business leaders

Design remains centralized

Infra stays shared as a platform layer

2×2 as organizing logic: Accountability structured around Retail vs. Institutional × US vs. International, applied consistently across product lines.

Three clear BUs: Broker, Crypto, and Money - each with explicit retail and institutional mandates.

Flattening the org: The GM model was explicitly positioned as a way to reduce layers, cut handoffs, and eliminate redundant roles - fewer approvals, lower coordination tax.

2022 layoffs as part of the reset:

Apr 26, 2022: ~9% reduction

Aug 2–4, 2022: ~23% reduction

After that, product velocity inflected meaningfully.

[IMAGE: chart/figure]

Revolut

Two-layer structure: A regulated multi-entity group (holding company + licensed banking, securities, insurance entities) sitting underneath a fast-moving operating layer.

Heavy governance by design: Committee-based oversight with a traditional financial-services control spine (board, exec committees, risk committees).

Three Lines of Defence is explicit:

1LoD: business owns risk

2LoD: independent risk & compliance

3LoD: internal audit

Risk managers increasingly embedded into the first line as the company scales.

Execution model: “pods” with local CEO ownership: Cross-functional teams with strong product-owner accountability for outcomes, not just roadmaps.

Centralized standards, decentralized execution: Teams move fast, but quality bars and “what good looks like” are tightly enforced (often described as founder-grade review).

Explicit high-performance culture: Framed internally as “startup mode,” “Dream Team,” and radical honesty (sports-team metaphor).

Operationalized performance management: Publicly described, metrics-driven reviews across delivery, skills, and cultural contribution.

Incentives extend into control behavior: Use of points-style systems (e.g., “Karma”) tied to risk and compliance behavior, with compensation implications - making expectations measurable, not aspirational.

Toss

Core idea: internal adaptability. Toss optimizes for the ability to detect org failure modes early and redesign structure and norms without killing velocity.

Why it matters: In a regulated super-app, the main scaling risk isn’t product - it’s org and compliance debt compounding faster than execution.

Mission-based org: Toss is organized around product/service domains (e.g., banking, payments, commerce, ads), not classic functional silos.

End-to-end ownership: Domain teams own outcomes; functions (eng, design, data, risk, compliance) embed into teams rather than sit as gatekeepers.

Three-layer operating model:

Domain Leaders = mini-CEOs with P&L-like accountability and real decision rights

Chapter Heads maintain functional quality bars and talent density across domains

Super ICs drive cross-domain initiatives without becoming people managers

Alignment overlay: A small set of roles exists to prevent local optimization from overwhelming global strategy - powerful if disciplined, bureaucratic if not.

Source: public information

WCM’s case study on Toss:

https://www.wcminvest.com/insight/toss-how-to-keep-your-edge-while-growing

"The information presented in this newsletter is the opinion of the author and does not necessarily reflect the view of any other person or entity, including Altimeter Capital Management, LP (”Altimeter”). The information provided is believed to be from reliable sources but no liability is accepted for any inaccuracies. This is for information purposes and should not be construed as an investment recommendation. Past performance is no guarantee of future performance. Altimeter is an investment adviser registered with the U.S. Securities and Exchange Commission. Registration does not imply a certain level of skill or training. Altimeter and its clients trade in public securities and have made and/or may make investments in or investment decisions relating to the companies referenced herein. The views expressed herein are those of the author and not of Altimeter or its clients, which reserve the right to make investment decisions or engage in trading activity that would be (or could be construed as) consistent and/or inconsistent with the views expressed herein.

This post and the information presented are intended for informational purposes only. The views expressed herein are the author’s alone and do not constitute an offer to sell, or a recommendation to purchase, or a solicitation of an offer to buy, any security, nor a recommendation for any investment product or service. While certain information contained herein has been obtained from sources believed to be reliable, neither the author nor any of his employers or their affiliates have independently verified this information, and its accuracy and completeness cannot be guaranteed. Accordingly, no representation or warranty, express or implied, is made as to, and no reliance should be placed on, the fairness, accuracy, timeliness or completeness of this information. The author and all employers and their affiliated persons assume no liability for this information and no obligation to update the information or analysis contained herein in the future."
