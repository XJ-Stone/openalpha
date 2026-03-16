---
investor: thomas-reiner
date: 2025-10-09
source: Robonomics
type: substack
url: https://www.platformaeronaut.com/p/openai-app-store-what-it-means-for
companies: [EXPE, BKNG, OPENAI, GOOGL, AAPL, META, RBLX, DASH, INSTACART, TIKTOK, TSLA, WAYMO, AMZN, GDS, HOTELS, MCP]
sectors: [ai, travel, travel-tech, platforms, marketplaces, payments, consumer-internet, digital-advertising, autonomous-vehicles, valuation]
source_length: 1368
fetch_method: substack_api
fetch_id: openai-app-store-what-it-means-for
---

# Robonomics — October 09, 2025

AI Travel’s First Inning: App Store Connectors, Clunky Handoffs, And Who Owns Discovery

It appears the first run at AI travel distribution is landing squarely in the “app store” model I previewed before: OTAs as enabled apps/connectors (MCP-style plugins) inside ChatGPT that you can query natively. That’s the right shape of the future, just not the feel yet

[IMAGE: Image]

What’s working

Supply pipes are finally reachable from the assistant. Being able to call Expedia and Booking from within ChatGPT is a meaningful step toward real-time pricing/availability without forcing users to context-switch. This is the connective tissue I expected as LLMs move from informational to agent.

Partnering buys time. In the short term, partnering with the incumbents prevents data shut-offs and accelerates coverage while the ecosystem sorts out standards (MCP, tool schemas, settlement).

What’s not (yet)

Latency kills conversion. In my testing, Expedia took ~2 minutes from ask → think → connect → show results. That’s a non-starter at checkout. Voice/agent UX wants sub-second first paint and progressive refinement. The GDS and many direct connects still live in 300–3000ms land per call. This is exactly why I’ve flagged latency as a first-order constraint for agents.

The flow isn’t end-to-end. You still click “Book on Expedia.” Every extra hop is drop-off. The magic trick of an agentic future is discovery → selection → payment → servicing in one continuous conversation, not a referral link with an off-ramp. I’ve argued the assistant needs to “own” the transaction loop or the value leaks.

Brand minimization is real. Search used to hand users to a branded surface (Expedia.com) where loyalty can compound via UX. In a connector world, ChatGPT owns the information layer and the UI. If OTAs are reduced to a “book” button, they’re functionally payment/servicing rails which is an expensive role for a 10–20% take rate. I’ve been clear: the OTA’s true value has always been discovery/information/comparison; if the assistant captures discovery, the OTA’s bargaining power erodes.

Thanks for reading Platform Aeronaut! Subscribe for free to receive new posts.

[IMAGE: Image]

ChatGPT App Design Guidelines

“But app stores and search had guidelines too…”

True the iOS App Store and Google search both constrained brand expression. The difference here is who owns the intermediary step. In mobile or web, OTAs still controlled room selection pages, image galleries, maps, and merchandising. With connectors, the OTA doesn’t even fully own that step; it’s increasingly just fulfillment. That’s a worse strategic position over time.

What consumers actually want

Not a referral click. They want the assistant to finish the job: select the suite, apply loyalty, pay, then be on the hook for changes, re-shops, and service disruptions. That requires:

Low-latency inventory and pricing (caching, prefetch, smarter fan-out).

Native payments and identity (cards, passports, loyalty IDs bound to the agent).

Integrated servicing (modify/cancel, IRROPS handling, on-stay messaging) without leaving the chat. All of this is consistent with where I’ve said voice/agents are heading—and why half-measures feel clunky today

So who wins if we keep marching down this path?

Near term (next 12 months):

OTAs benefit as the default pipes inside assistants. They’ll see incremental lead-gen without paying Google as much at the top of funnel. But economics will compress if agents intermediate discovery.

Google loses hotel/flight meta surface area if users start the journey in chat. “10 blue links” are structurally challenged for travel discovery in an LLM world.

Longer term (2–4 years):

UX owners win. The platform with the fastest, most trusted, end-to-end agent wins share of consumer (and therefore supplier) mind. That could be ChatGPT, iOS/Siri, or WhatsApp, whoever pairs latency + breadth + servicing with a delightful loop.

Direct suppliers regain leverage if they expose data right. Hotels that publish AI-readable inventory, policies, perks, and transact via open standards (think MCP as the “USB-C for agents”) can route around OTA dependency and let assistants book direct, with richer post-booking service. I’ve laid out this playbook for hoteliers explicitly.

The uncomfortable truth

This first inning feels like Custom GPTs with better branding: useful, but not the right answer yet. I don’t want a referral link; I just want it done. And when assistants actually own discovery and execution end-to-end, the rent paid to intermediaries that don’t control discovery will compress. 

Subscribe now

Performance & Valuation Snapshot

I’ve made a few adjustments to this. I’ve combined the two data sets into one, and I’ve also added a column “Chg in Multiple.” For this what I’ve done is calculated the average NTM EV / EBITDA consensus multiple that the business has traded at over the trailing 18 months and calculated the difference between that and the multiple it’s trading at today.

So taking Roblox for example, the stock up 116% YTD and is trading at 50x EV / EBITDA, but that’s only 18% higher than the average multiple it’s traded at in recent history.

Separately I’m experimenting with a chart below showing YTD price change vs the delta between today’s multiple and last 18mo average multiple. It’s kind of interesting how it shows both the implicit increase in fundamentals as well as multiple expansion (or contraction).

So DoorDash is up 67% for the year but the multiple is only 24% higher than the trailing 18mo average, implying considerable expansion in underlying fundamentals driving the majority of the stock performance this year.

What I Read This Week

ChatGPT adds “apps” via MCP: Wiring ChatGPT into travel tools using Model Context Protocol in a big step forward for agentic trip planning.

Instacart Partners with TikTok Retail Media: New integration tightens end-to-end ad-to-cart flow on TikTok

Tesla rolls out FSD v14.1: Adds robotaxi-style drop-offs for consumers where you can select where FSD should park: lot, street, driveway, etc

NHTSA Investigation into Tesla FSD Traffic Violations: They’re looking into incidents where FSD blew through red lights or traveled the wrong way.

DoorDash Ads Feature Expansion: Sponsored products, Ghost Ads, and category-level share reporting among the changes

Waymo Lobbyists Pushing for AVs in Minnesota: Due to state laws, big changes are required before AVs can function in the state.

Amazon Fresh Closing Stores in the US: Despite a push into fresh grocery delivery, Amazon Fresh is closing 5 of their US stores.

Poll of the Week

From My Recent Work

Transcript Highlights (Exec Signals)

Thanks for reading Platform Aeronaut! Subscribe for free to receive new posts.

The information presented in this newsletter is the opinion of the author and does not reflect the view of any other person or entity, including Altimeter Capital Management, LP (”Altimeter”). The information provided is believed to be from reliable sources but no liability is accepted for any inaccuracies. This is for informational purposes and should not be construed as investment advice or an investment recommendation. Past performance is no guarantee of future performance. Altimeter is an investment adviser registered with the U.S. Securities and Exchange Commission. Registration does not imply a certain level of skill or training. Altimeter and its clients trade in public securities and have made and/or may make investments in or investment decisions relating to the companies referenced herein. The views expressed herein are those of the author and not of Altimeter or its clients, which reserve the right to make investment decisions or engage in trading activity that would be (or could be construed as) consistent and/or inconsistent with the views expressed herein.

This post and the information presented are intended for informational purposes only. The views expressed herein are the author’s alone and do not constitute an offer to sell, or a recommendation to purchase, or a solicitation of an offer to buy, any security, nor a recommendation for any investment product or service. While certain information contained herein has been obtained from sources believed to be reliable, neither the author nor any of his employers or their affiliates have independently verified this information, and its accuracy and completeness cannot be guaranteed. Accordingly, no representation or warranty, express or implied, is made as to, and no reliance should be placed on, the fairness, accuracy, timeliness or completeness of this information. The author and all employers and their affiliated persons assume no liability for this information and no obligation to update the information or analysis contained herein in the future.
