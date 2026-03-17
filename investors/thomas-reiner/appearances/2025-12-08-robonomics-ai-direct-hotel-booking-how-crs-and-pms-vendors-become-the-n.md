---
investor: thomas-reiner
date: 2025-12-08
source: Robonomics
type: substack
url: https://www.platformaeronaut.com/p/ai-direct-hotel-booking-how-crs-and
companies: [SABR, AMS.MC, CENDYN, SHR, MIRAI, AVVIO, MEWS, CLOUDBEDS, ORCL, MYMA, CANARY]
topics: [crs-native-bookings, agentic-commerce, travel-distribution, pms-servicing]
companies_detail:
  - ticker: SABR
    focus: secondary
  - ticker: AMS.MC
    focus: secondary
  - ticker: CENDYN
    focus: secondary
  - ticker: SHR
    focus: secondary
  - ticker: MIRAI
    focus: secondary
  - ticker: AVVIO
    focus: secondary
  - ticker: MEWS
    focus: secondary
  - ticker: CLOUDBEDS
    focus: secondary
  - ticker: ORCL
    focus: secondary
  - ticker: MYMA
    focus: mention
  - ticker: CANARY
    focus: mention
topics_detail:
  - topic: crs-native-bookings
    focus: primary
  - topic: agentic-commerce
    focus: secondary
  - topic: travel-distribution
    focus: secondary
  - topic: pms-servicing
    focus: mention
source_length: 2006
fetch_method: substack_api
fetch_id: ai-direct-hotel-booking-how-crs-and
---

# Robonomics — December 08, 2025

# Robonomics — December 08, 2025

We’re approaching the first real rewrite of hotel distribution since the OTA boom of the 2000s. AI agents don’t browse websites, they transact. And the systems best positioned to serve them are the ones long ignored because they lived below the funnel.

I’ve written in the past about how hotels can thrive in an agentic AI world as we move from SEO to MCP, as well as the challenges the OTAs will likely face but I wanted to spend some time doing an overview of what technological and product changes the CRS, PMS, and Booking Engine vendors themselves are doing to enable the hotels themselves to take control.

At a super high level there’s a few definitions I’d like to provide first:

Property Management System (PMS): the hotel’s system of record for on-property operations. Manages guests once they exist as a reservation and responsible for everything that happens between booking and checkout. In an AI-first world it enables reservation modifications, amenities, inventory checks, and actions.

Central Reservation System (CRS): the hotel’s commerce and distribution system that manages rates, availability, and booking rules. It’s the revenue operating system. The CRS creates the booking and pushes it to the PMS for fulfillment.

Booking Engine (BE): the hotel’s direct-to-consumer storefront and transaction UI.

It sits on top of the CRS and converts real-time rates & availability into guest-facing offers. The BE orchestrates pricing display, room selection, upsells, payment capture, and confirmation.

MCP (Model Context Protocol): is the emerging standard that enables AI agents to call tools, query APIs, and execute transactions. Effectively giving booking agents direct programmatic access into a hotel’s systems.”

CRS = Where AI Agents “shop, compare, select, and book”

PMS = Where AI Agents “service, modify, fulfill requests, and manage”

BE = Where AI Agents “display, package, upsell, and transact”

MCP = Where AI Agents “access, understand, and digest”

Subscribe now

With that said I’ve put together a hotel tech stack graphic for distribution with the general flow from guest to hotel so we can identify where the best positioned players are for an AI Agentic future. 

[IMAGE: chart/figure]

When you zoom out at the full distribution flow, the misalignment becomes obvious: the top of the funnel is built for human browsing, not agentic transactions.

Who is Best Positioned to Enable MCP Style AI Bookings?

If you look at the above diagram the further down the tech stack you get the richer, more accurate, and most up to date data you get, and those are the players who are best positioned to enable MCP style AI Bookings direct.

The CRS / Booking Engine / PMS is where the hotel controls rate, availability, inventory, policies, room categories, content, LOS rules, restrictions, and real-time booking workflows. This is exactly the data an MCP needs to:

Query availability

Reason about room types

Price compare across dates

Evaluate cancellation policies

Transact the booking

See customized offers/packages

You don’t get the full fidelity from OTAs, TMCs, metasearch, or GDS. Top of the funnel intermediaries are structurally misaligned with MCP-native booking execution. They worked in a pre-AI age of the internet because of disaggregated supply and tech-challenged hoteliers who didn’t know how to best display their data.

OTAs don’t own the ARI, they use cached availability, weren’t built for reasoning-based agents, sit outside the canonical data path, and pricing logic is opaque.

#1 CRS (Central Reservation System)

This is the canonical source of truth for ARI (rates, availability, inventory). They already power Brand.com, mobile apps, GDS feeds, OTA extranets, wholesales, TMC links and call centers. This means one CRS integration gives an MCP agent the ability to book at any hotel distribution endpoint. Additionally the CRS already has the transactional logic to perform the actual reservation commit + confirmation and CRS vendors already expose APIs ready-made for MCP adapters. 

An MCP powered by the CRS gives AI Agents full life-cycle visibility:

Availability → Booking → Modify → Cancel → Loyalty → Upsell

SynXis CRS: Hospitality Solutions (Sabre sold this to TPG at the worst time) has rolled out SynXis Concierge.AI and an AI “Booking Agent” embedded in the SynXis Booking Engine, a gen-AI chatbot that recommends rooms, answers questions in 50+ languages, and completes bookings on top of SynXis APIs.

[IMAGE: Sabre Hospitality extends AI to booking engine | PhocusWire]

Amadeus iHotelier / CRS: Amadeus positions iHotelier as a highly personalized, data-driven CRS + booking engine and has publicly said it wants to be the real-time pricing and content provider to AI platforms rather than compete with them, ie they’re building the pipes MCP agents would hit for live rates/availability.

Cendyn (Pegasus CRS + CRM): Cendyn combines Pegasus CRS with an AI-enhanced CRM/CDP that uses AI-powered insights for personalization and has explicitly said it’s investing in APIs and MCPs to feed “AI helpers,” making it the only one today name-checking MCP directly.

SHR Windsurfer: Markets an “AI-driven booking engine” and CRS with an AI assistant that auto-generates content/translations and optimizes UX, so they’re already using AI inside the CRS/IBE and would be relatively straightforward to front with an MCP agent.

Conclusion: CRS vendors are the new gatekeepers of AI travel because they own the canonical ARI dataset, the pricing logic, and the transactional rail, which are the three ingredients AI agents require to book autonomously.

CRS vendors have the right economic incentive: unlike OTAs, they’re paid by the hotel and are not built on arbitrage or consumer acquisition spend.

#2 BE (Direct Booking Engines)

Booking engines (TravelClick, Mirai, Avvio, Mews BE, Cloudbeds BE are the closest to the guest-facing UX but still depend on the CRS or PMS for availability, pricing, and rules. They are well positioned to expose AI-native storefront UIs but they’re not the source of ARI truth.

CRS = the source of truth

BE = the source of UX

In an AI-mediated flow, the guest never sees the booking engine, an MCP agent may call its endpoints directly. AI is compressing the gap between CRS and BE. Many booking engines may evolve into API layers rather than UI layers, with MCP servers orchestrating the commerce flow instead of a traditional web interface.

SynXis Booking Engine: SynXis BE now includes gen-AI Booking Agent / Concierge.AI, so the booking engine itself exposes a conversational UI that can handle search, recommendations, and checkout which is an agentic booking flow you could either embed or call from MCP.

Mirai Booking Engine: Mirai has launched Sarai, an AI agent that chats with guests, routes them into the Mirai booking engine with trackable links, and is experimenting with a 3D-native booking UI. So they’re actively treating BE as an AI-first storefront, not just a form.

[IMAGE: Mirai launches Sarai, the new generation of AI agents for hotels]

Cloudbeds Booking Stack (BE + Platform): Cloudbeds’ unified platform includes a direct booking engine and is now wrapped with “Signals,” a causal AI / gen-AI layer plus AI messaging and voice concierge that can answer questions and complete bookings, making it a natural candidate for MCP-style agents to sit on top of.

Conclusion: BEs are where the MCP conversation experience can be surfaced, but the CRS is where it is best executed.

#3 PMS (Property Management System)

PMS is not the best place to run MCP-driven OTA bypass because it’s operationally focused and often syncs ARI from the CRS or RMS systems and doesn’t handle multi-channel distribution. PMS should receive the reservation but not handle the AI booking logic.

But while PMS is the wrong place to book, it’s the right place for an MCP server to look for servicing. Whether it’s modifications, extensions, mid-stay requests, loyalty benefits, room moves, upsells, or in-stay commerce, this can all be managed through the PMS and so it stands to see a bit of a renaissance as well. In an AI-first stay, most guest interactions (extensions, upgrades, chat-based requests) flow through the PMS, not the CRS.

Mews PMS: Mews is leaning hard into AI with “AI Smart Tips” and AI-powered guest insights (summaries of reviews, stay history, lifetime value) plus a broader “agentic AI for hotels” narrative, so their PMS is already exposing AI-enhanced servicing and is philosophically aligned with MCP-style agents.

[IMAGE: chart/figure]

Cloudbeds PMS: Cloudbeds bills itself as an “AI-powered hospitality platform” and uses its Signals model plus gen-AI for forecasting, revenue intelligence, and AI messaging / voice concierge that can take calls, answer questions, and handle bookings, so PMS + distribution + guest comms are all being instrumented for agentic workflows.

Oracle OPERA Cloud: OPERA Cloud has a built-in Digital Assistant chatbot for natural-language operations tasks and offers a robust Integration Platform (OHIP) that third-party AI tools like Myma.ai and Canary already use for automated guest messaging and personalization, making it more of an “API fabric” that MCP agents could plug into than a branded AI agent itself.

Conclusion: Hybrid/vertically integrated players like Mews and Cloudbeds could attempt this given more robust RMS and CRS offerings natively integrated, but traditional PMS vendors like Oracle are not structurally aligned with distribution innovation.

The big shift underway is that AI collapses the layers of hotel distribution

OTAs won the web era because guests needed aggregation, comparison, and UX.

But AI agents don’t browse, they transact. They go directly to the systems with the richest, most accurate, most up-to-date data. And that’s the CRS.

The vendors who sit closest to the canonical source of truth for rates and availability are the ones best positioned to power MCP-native bookings. Over the next five years, the influence of CRS vendors will grow dramatically, booking engines will evolve from interfaces to APIs, and PMS platforms will become the operational brain for AI-managed stays.

Implications for OTAs:

OTAs don’t disappear, but their role shifts from primary booking originators to marketing surfaces. Their margin structure becomes pressure-tested as hotels regain control of direct programmatic access.

If OTAs were the UI layer of the last generation, CRS will be the API layer of the next. Hotels that understand this shift early will own their distribution economics again, maybe for the first time in 20 years.

Thanks for reading Platform Aeronaut! Subscribe for free to receive new posts.

The information presented in this newsletter is the opinion of the author and does not reflect the view of any other person or entity, including Altimeter Capital Management, LP (”Altimeter”). The information provided is believed to be from reliable sources but no liability is accepted for any inaccuracies. This is for informational purposes and should not be construed as investment advice or an investment recommendation. Past performance is no guarantee of future performance. Altimeter is an investment adviser registered with the U.S. Securities and Exchange Commission. Registration does not imply a certain level of skill or training. Altimeter and its clients trade in public securities and have made and/or may make investments in or investment decisions relating to the companies referenced herein. The views expressed herein are those of the author and not of Altimeter or its clients, which reserve the right to make investment decisions or engage in trading activity that would be (or could be construed as) consistent and/or inconsistent with the views expressed herein.

This post and the information presented are intended for informational purposes only. The views expressed herein are the author’s alone and do not constitute an offer to sell, or a recommendation to purchase, or a solicitation of an offer to buy, any security, nor a recommendation for any investment product or service. While certain information contained herein has been obtained from sources believed to be reliable, neither the author nor any of his employers or their affiliates have independently verified this information, and its accuracy and completeness cannot be guaranteed. Accordingly, no representation or warranty, express or implied, is made as to, and no reliance should be placed on, the fairness, accuracy, timeliness or completeness of this information. The author and all employers and their affiliated persons assume no liability for this information and no obligation to update the information or analysis contained herein in the future.
