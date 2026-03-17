---
investor: thomas-reiner
date: 2026-01-16
source: Robonomics
type: substack
url: https://www.platformaeronaut.com/p/vibe-coding-an-ota-thoughts-on-ai
companies: [SOMNISEAT, AMS, ANTHROPIC, GOOGL, EXPE, BKNG, TCOM, MSFT, VERCEL, OPENAI, SABR, WMT, AMZN, TSLA, KR, UBER, MEWS, DIRECTBOOKER]
topics: [vibe-coding, ota, agentic-commerce, caching-strategies]
companies_detail:
  - ticker: SOMNISEAT
    focus: primary
  - ticker: AMS
    focus: secondary
  - ticker: ANTHROPIC
    focus: secondary
  - ticker: GOOGL
    focus: secondary
  - ticker: EXPE
    focus: mention
  - ticker: BKNG
    focus: mention
  - ticker: TCOM
    focus: mention
  - ticker: MSFT
    focus: mention
  - ticker: VERCEL
    focus: mention
  - ticker: OPENAI
    focus: mention
  - ticker: SABR
    focus: mention
  - ticker: WMT
    focus: mention
  - ticker: AMZN
    focus: mention
  - ticker: TSLA
    focus: mention
  - ticker: KR
    focus: mention
  - ticker: UBER
    focus: mention
  - ticker: MEWS
    focus: mention
  - ticker: DIRECTBOOKER
    focus: mention
topics_detail:
  - topic: vibe-coding
    focus: primary
  - topic: ota
    focus: secondary
  - topic: agentic-commerce
    focus: secondary
  - topic: caching-strategies
    focus: secondary
source_length: 1679
fetch_method: substack_api
fetch_id: vibe-coding-an-ota-thoughts-on-ai
---

# Robonomics — January 16, 2026

# Robonomics — January 16, 2026

We appear to have entered a new era for code generation. Since December I’ve frequently seen some impressive vibe coded solutions on twitter, so I wanted to take a crack at it myself. When traveling for work on long haul flights I try to find lie-flat seats, but despite Google Flights having an indicator for lie flat, you can’t actually search by it. So I decided to vibe code an OTA focused exclusively on lie flat seats: SomniSeat.

What surprised me wasn’t that I could build a lie-flat-only OTA in a day, it’s that nothing structurally prevented it from existing before. The constraints weren’t product vision or capital, they were developer time, integration friction, and iteration speed. Those constraints are collapsing fast.

[IMAGE: chart/figure]

SomniSeat.com

All of this took about one day’s work utilizing Claude Code, Github, Vercel, and the Amadeus self-service API for data. I have minimal coding experience beyond PHP back in the day and it spit out an impressively good copy of an OTA including some cool pages like Inspiration (pulling recently searched travel), AI Search (utilizing OpenAI API and facilitating search of the underlying data), and Lie-Flat Routes (pulling cached data from searches to demonstrate where and who flies lie-flat business class seats.

I will caveat that I haven’t hooked up the actual booking mechanism (either through Amadeus or sourcing a meta-esque solution through Kayak or direct with airlines) mostly because I don’t want to deal with the hurdle of contracts and legal setup since this is more playing around. Additionally, Amadeus is pretty ass-backwards from a technical perspective and the ability to move from limited test API data to production has been having technical issues for awhile and even the test API goes down sometimes so it’s a bit frustrating. Hence the actual flight results are limited right now, it’s probably 20% of actual flight availability and mostly close in with cached data but I’ll fix it as soon as Amadeus does.

Subscribe now

In terms of the learnings that are useful from an investor or industry observer perspective:

Data Integrity Varies Significantly

When I was looking at various APIs for flight specific data you get a huge range of data. Amadeus appears to have the most depth (they even have seat-tilt information by flight segment), while others like Skyscanner and Kayak are actually shockingly limited in the data they provide through API.

It’s no small wonder that Google doesn’t offer an external API for their travel data and closely protects it as I’m sure they’re doing a lot of data massaging. For the lie flat detector I was originally utilizing a call to a Seat Map API at Amadeus but that’s pretty rate limited and makes it difficult to limit when you get so many flight results back so I had to switch to a custom heuristic. I had to set a ton of rules utilizing data based on route, aircraft type, airline, segment duration, and more to properly try to predict lie flat seat availability.

Development Speed and Accessibility has 100x’ed

The fact that I was able to make this in a day and with a reasonable budget (maybe $50 including compute) means the ability for the average developer or consumer to develop a customized solution is more accessible than ever. You don’t like how Expedia displays or searches hotels or flights? Just make your own solution. That’s not going to be super impactful to Expedia’s business, but it’s interesting.

More important is what I believe to be the impact on the direct booking ecosystem. If the average hotel can now have a more robust home grown system, or it enables smaller companies like Mews or Directbooker to reach feature or speed parity with the OTAs on offerings, it could have an enormous impact on the speed that OTA disruption happens. 

The Importance of Caching

I got a bit of an inside look at the importance of caching and what that means for result and price integrity. The information received per search is like a firehose, and the more specifics you want the bigger the data pull and it can quickly get overwhelming. Then you have to make cache trade off decisions of how frequently, how to real-time update during searches, and how much data to store. The good news is none of this is really terribly complicated and with AI can be optimized even in the average developer’s hands. I’d guess if I set a budget of $1k I could easily have a more real-time but optimized cache solution for tens of thousands of daily searches.

A single broad transatlantic search can return tens of thousands of fare/segment permutations once you explode it by cabin, aircraft, and connection logic. Without aggressive caching, you’re either bankrupt or blind.

Enabling AI is Easier Than Ever

The fact that I could exposure AI to my Amadeus cached results and enable searching and results in a decently enough user friendly UX means the agentic world is even closer than previously thought. It’s easy to envision a world this year that every hotel or airline has an AI agent that can communicate rapidly with caching and surface the most relevant data to other agents and consumers.

[IMAGE: chart/figure]

In that world, the battle isn’t OTA vs direct, it’s whose agent is trusted as the system of record. Discovery, pricing, loyalty, and servicing collapse into a single conversational interface. OTAs don’t disappear, but their value migrates from traffic arbitrage to infrastructure, payments, and exception handling.

Vibe Coding Changes the Cost Curve, Not Just the UX

It’s not about prettier interfaces or faster prototyping, it’s about eliminating the translation friction between intent and software. When a single person can go from idea to production-grade product in a day, the constraint shifts from engineering capacity to imagination. That dynamic disproportionately benefits narrow, high-intent use cases that were never worth building before, and it’s exactly where incumbents’ scale and distribution moats are weakest. I spun up a real time lie-flat map organized by hub and airline with one prompt, 5k tokens, and 2 minutes:

[IMAGE: chart/figure]

Thanks for reading Platform Aeronaut! Subscribe for free to receive new posts.

Performance & Valuation Snapshot

As a reminder these snapshots below are interactive (filter/order/search). Unfortunately substack emails present them as a stale image that you need to click through to view them so I highly recommend clicking or viewing on Platform Aeronaut if you’re coming from email

What I Read This Week

Google’s new UCP lets AI agents handle checkout: Google teases agentic checkout for partners (incl. Expedia/Marriott), pushing AI from “search” to “transaction.”

KAYAK CEO tried to take company private: Booking’s metasearch unit explored a take-private; parent CEO Glenn Fogel vetoed.

Robotaxi outlook: Waymo, Zoox, Tesla on Bloomberg: Leaders debate timelines, economics, and regulatory risk for autonomous ride-hailing

Walmart × Wing expand drone delivery to 150 more stores: Drone drop-offs head to LA, Miami, Cincinnati, St. Louis; 270 locations targeted by 2027.

Kroger goes nationwide on Uber apps: Nearly 2,700 Kroger-family stores now on Uber Eats/Uber/Postmates with promo incentives.

Travel’s wallet-share is shrinking: New data: travel fell from 12% of consumer wallets (Jan ’24) to 8% (Dec ’25), raising stakes for conversion/upsell.

Sabre invests in BizTrip AI: Corporate-travel-focused LLM startup gets a strategic stake from Sabre.

UCP vs MCP: the race for an agentic commerce stack: PhocusWire breaks down how Google UCP and Anthropic’s MCP will coexist in travel workflows.

Recent Posts

Transcript Highlights (Exec Signals)

“We expect the transaction to be EPS accretive in the first full year post closing.”

“MSP will be a major strategic hub for the combined company.”

“Since the vast majority of our fleet is owned… the combined fleet will have significant embedded equity value.”

“The US economy remains on firm footing, and consumers continue to prioritize experiences with travel among the top spending categories,”

“We plan to grow capacity by 3% for the full year, with all new seat growth concentrated in premium cabins...”

“...this consistent and integrated strategy positions Delta with a sustained unit revenue premium of nearly 115% relative to the industry.”

Thanks for reading Platform Aeronaut! Subscribe for free to receive new posts.

The information presented in this newsletter is the opinion of the author and does not reflect the view of any other person or entity, including Altimeter Capital Management, LP (”Altimeter”). The information provided is believed to be from reliable sources but no liability is accepted for any inaccuracies. This is for informational purposes and should not be construed as investment advice or an investment recommendation. Past performance is no guarantee of future performance. Altimeter is an investment adviser registered with the U.S. Securities and Exchange Commission. Registration does not imply a certain level of skill or training. Altimeter and its clients trade in public securities and have made and/or may make investments in or investment decisions relating to the companies referenced herein. The views expressed herein are those of the author and not of Altimeter or its clients, which reserve the right to make investment decisions or engage in trading activity that would be (or could be construed as) consistent and/or inconsistent with the views expressed herein.

This post and the information presented are intended for informational purposes only. The views expressed herein are the author’s alone and do not constitute an offer to sell, or a recommendation to purchase, or a solicitation of an offer to buy, any security, nor a recommendation for any investment product or service. While certain information contained herein has been obtained from sources believed to be reliable, neither the author nor any of his employers or their affiliates have independently verified this information, and its accuracy and completeness cannot be guaranteed. Accordingly, no representation or warranty, express or implied, is made as to, and no reliance should be placed on, the fairness, accuracy, timeliness or completeness of this information. The author and all employers and their affiliated persons assume no liability for this information and no obligation to update the information or analysis contained herein in the future.
