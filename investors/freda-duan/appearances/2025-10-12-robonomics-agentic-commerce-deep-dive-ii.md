---
investor: freda-duan
date: 2025-10-12
source: Robonomics
type: substack
url: https://robonomics.substack.com/p/agentic-commerce-deep-dive-ii
companies: [SHOP, STRIPE, OPENAI, PERPLEXITY, GOOGL, AAPL, PDD, BABA]
topics: [agentic-commerce, ads-vs-take-rate, platform-economics, payments, digital-advertising]
companies_detail:
  - ticker: SHOP
    focus: secondary
  - ticker: STRIPE
    focus: secondary
  - ticker: OPENAI
    focus: secondary
  - ticker: PERPLEXITY
    focus: mention
  - ticker: GOOGL
    focus: secondary
  - ticker: AAPL
    focus: mention
  - ticker: PDD
    focus: mention
  - ticker: BABA
    focus: mention
topics_detail:
  - topic: agentic-commerce
    focus: primary
  - topic: ads-vs-take-rate
    focus: secondary
  - topic: platform-economics
    focus: secondary
  - topic: payments
    focus: secondary
  - topic: digital-advertising
    focus: secondary
source_length: 1141
fetch_method: substack_api
fetch_id: agentic-commerce-deep-dive-ii
---

# Robonomics — October 12, 2025

In Part I, I analyzed whether agentic commerce can actually work. 

This second piece assumes it does — and examines the ripple effects across the internet economy.

We’ll look at:

How agentic commerce reshapes ads revenue vs. take-rate economics

What it means for merchants and platforms (both near-term and long-term)

The diverging impact on pure infra players like vs. traffic-owning platforms like etc. 

How it could re-wire the payments stack (Stripe)

Impact on ads platforms 

1/ What does history tell us - Googl vs. OTAs?

We can’t really discuss agentic commerce’s impact without first understanding how — the OG “top of the funnel” — reshaped OTAs and other consumer internet platforms.

 / 

Roughly half of their bookings and traffic are direct, and the other half indirect (mostly through Google).

For the indirect portion, the companies basically just break even, given the high CPCs they pay Google.

Unit economics-wise: assume a $300/night hotel, a 15% take rate, CPC of $1–3, and a click-to-book conversion rate of 3–4%. That implies ~$50 in marketing expense per completed booking — essentially breakeven on indirect traffic.

Direct traffic, by contrast, is gold. It’s profitable and monetizable via paid placements (ads account for ~10% of revenue, ~5% for ; about 25% of EBIT).

 is similar. Marketing runs ~30% of revenue — implying the indirect portion is barely profitable.

The lesson: indirect traffic is an expensive squeeze. extracted more total profit from travel than all the OTAs combined - let that sink in.

[IMAGE: chart/figure]

[IMAGE: chart/figure]

Recommend reading on OTAs: Substack Platform Aeronaut 

2/ The New Digital Tax: Ads Expense ≈ Take Rate

Unit Economics under agentic commerce — ads expense and take rate as interchangeable digital tax

This is a really interesting mental framework in consumer internet: ads expense and take rate are interchangeable forms of digital tax. Every networked economy can be viewed as charging a “take rate.”

YouTube’s “tax” is 45% on creators.

 captures ~99% of creator economics via ads.

 App Store: 15–30%.

In the OTA example above, the effective take rate on indirect traffic is 0–5%, even though the headline rate is 15% for both direct and indirect. That means if ChatGPT were to charge a 10–15% take rate, they’d essentially breakeven compared with getting traffic from .

This convergence of ads (ads expense) & e-commerce (take rate) business models has already happened in China. PDD, BABA, among other platforms, have all blurred the lines between ads vs. take rate when they charge merchants. It is indeed just a digital tax!

How this could play out: ChatGPT starts at a low take rate (say 2%), then gradually raises toward equilibrium (10–15%). Whether it’s called “take rate” or “ad spend” is semantics — top-of-funnel networks always get their digital tax!

3/ Impact on Merchants / Platforms

The impact on merchants comes from several different angles:

Direct vs. indirect traffic mix

For the direct traffic portion, ads rev

For the indirect traffic portion, unit economics — the “effective take rate” concept discussed above

For the indirect traffic portion, conversion rate

For the indirect traffic portion, market share

Industry online penetration — I’ve seen a lot of sell-side calling for higher online penetration driven by agentic commerce adoption. I don’t quite get that logic, but let’s see.

Like Dr Strange seeing 14 million futures — most paths don’t look great for merchants / platforms — given the squeeze on direct traffic mix %. The squeeze could be harsher than Apple’s 30% or Google’s CPC toll. 

Merchants traditionally depend on shoppers exploring their sites to lift order values through upsells and cross-sells. Agentic commerce changes that: purchases happen off-site, with no visit, pixel, or browsing data. You might still get the buyer’s email, but you lose visibility and retargeting power. The question is whether a 6× higher conversion rate offsets that loss. For smaller merchants, probably yes. For big retailers built around AOV optimization, I don’t think so...

[IMAGE: chart/figure]

[IMAGE: chart/figure]

In the above table:

Marketing expenses: goes to “top of the funnel”, whether that’s in the form of ads spend or take rate

Ads rev (this is only from direct traffic): where would this go (if agentic commerce further shifts traffic away from direct)??

4/ Shopify - the Infra Winner

 may be the cleanest structural fit for ChatGPT’s agentic world.

 was never the Merchant of Record (“MoR”) and doesn’t “curate” merchants the way a marketplace does. So the direct vs. indirect traffic issue won’t really apply. For years, has been criticized for not becoming a true consumer marketplace — but in this new world, that might actually turn out to be a blessing.

Impact:

GMV tilts toward quality SMBs. Many of ~3 M merchants sell unique, high-quality products but can’t afford the ad-spend arms race. Agents could level the field.

Higher penetration. SMBs that struggle to build data/catalog pipelines for agents may migrate to standardized stack.

Marketing becomes more efficient. itself spends ~$1.4B (16% of revenue) on marketing, while its merchants collectively spend an estimated $20–50B (based on ~$300B GMV and typical 7–15% marketing-to-sales ratios). That duplicated “digital tax” could be streamlined in an agentic world.

[IMAGE: chart/figure]

5/ Impact on Payments: Stripe’s Quiet Leverage

Both OpenAI’s Agentic Commerce Protocol and Perplexity’s approach let merchants keep existing PSPs — and Stripe powers both.

As agentic checkout spreads, Stripe’s role as the neutral connective tissue likely strengthens.

[IMAGE: chart/figure]

See a separate Stripe Deep Dive.

6/ Impact on Google / Ads

I get the bull case on — it has a near-perfect “T-shaped” value proposition:

Vertically integrated across the full stack, from applications to cloud to chips; and

Horizontally well-positioned across a wide range of products — productivity (Google Suite), entertainment (YouTube), and utilities (Google Home, etc.). In the end, the best model tends to win.

I also understand that, so far, ’s search ads revenue hasn’t been meaningfully affected by GPT. could theoretically lose 95% of its search volume and still grow revenue — as long as it retains the valuable queries, which are largely commerce-related.

But whether ’s ads model survives the agentic era intact — still TBD.

7/ The Road Ahead

In Patrick Collison’s chat with Tobi Lütke, he mused that someone should build a universal catalog of consumer products — not just for Shopify merchants, but for everything. That’s the dream state for agentic commerce: standardized product data powering AI agents to shop intelligently.

Today, “find me women’s running shoes” is still too high-level. Tomorrow, agents may parse “a black-and-white mohair sweater with a big letter G.” That will require product-specific models and richer metadata

A feedback-driven review layer is also needed to close the loop.

Source/ reference/ recommended readings:

[IMAGE: chart/figure]
Platform Aeronaut
Data-driven deep dives on travel, delivery, marketplaces, and enterprise software from unit economics to dilution. Plus how agentic AI reshapes distribution, loyalty, and advertising moats.

By Thomas Reiner
