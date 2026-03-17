---
investor: freda-duan
date: 2025-05-29
source: Robonomics
type: substack
url: https://robonomics.substack.com/p/mid-year-fact-check-on-self-driving
companies: [GOOGL, BIDU, WERIDE, PONYAI, TSLA, UBER, LYFT]
topics: [robotaxis, fleet-management, international-expansion, autonomy]
companies_detail:
  - ticker: GOOGL
    focus: primary
  - ticker: BIDU
    focus: secondary
  - ticker: WERIDE
    focus: secondary
  - ticker: PONYAI
    focus: secondary
  - ticker: TSLA
    focus: secondary
  - ticker: UBER
    focus: mention
  - ticker: LYFT
    focus: mention
topics_detail:
  - topic: robotaxis
    focus: primary
  - topic: fleet-management
    focus: secondary
  - topic: international-expansion
    focus: secondary
  - topic: autonomy
    focus: secondary
source_length: 1220
fetch_method: substack_api
fetch_id: mid-year-fact-check-on-self-driving
---

# Robonomics — May 29, 2025

No major accidents (!)

Two main metrics to watch: number of new cities and fleet size. The pace of geographic expansion across global players truly surprised me on the upside. Honest self-reflection: I overestimated both the time and cost required for players using “HD map” stacks to expand to new cities.

We’re seeing a clear convergence around 1,000 vehicles as the industry's magic number—the threshold where self-driving shifts from 0 → 1. Waymo is already at 1,500; Baidu and Pony.ai are aiming for 1,000 by YE25; WeRide is at 1,200; and TSLA is now signaling 1,000 as the next milestone.

We’re slowly moving from early “enthusiasts” to the “early adopter” phase. Still very early, but the shift is starting to happen.

Waymo Update

Progress recap: The pace of expansion has been phenomenal. In just the past 12 months, Waymo has launched in San Francisco, the Peninsula, LA, Austin, Atlanta, and most recently, Silicon Valley (now open to early riders).

Coming soon: Miami and Washington D.C. are both announced for 2026.

Data collection underway in: Las Vegas, Dallas, San Antonio, Nashville, New Orleans, and several other metros.

[IMAGE: chart/figure]

Timing analysis:

San Francisco: ~5 years from initial mapping to commercial launch

Austin: ~2 years

Silicon Valley: Mapping vans spotted in Jan 2025, trusted tester program began March 11, 2025 — though this is more of an extension of an existing metro.

[IMAGE: chart/figure]

The Pattern:

A greenfield U.S. city now takes ~12–24 months from mapping vans to credit-card rides.

Lidar data capture: fast—often <30 days with 3–8 cars

Offline map build + QA (annotating curbs, syncing with sensor data, simulation): 1–3 months

Cost to map & refresh a ~100 sq mi service area = tens of millions

[IMAGE: chart/figure]

China Players Update

Baidu (Apollo):

Operating 400+ robotaxis in Wuhan alone

Plans to scale to 1,000 RT6 robotaxis in Wuhan by YE25

Fully driverless in 3 Chinese cities

Dubai expansion plan: 50 cars in 2025 → 1,000 by 2028

Cumulative rides hit 9M by Jan 2025, with 1.1M rides in 4Q24 alone

(For comparison: Waymo is now doing ~250K rides/week = 13M annualized)

WeRide:

Fleet hit 1,200+ vehicles in Q1 2025

Operating in at least five cities (Guangzhou, Beijing, Nanjing, Suzhou, Ordos)

Went live with Uber in Abu Dhabi (Dec 2024, with safety driver; aiming for full driverless by 2025)

May 2025 deal signed with Uber: plan to launch in 15 more cities globally over the next five years

Pony.ai:

Currently has >200 active robotaxis

Scaling to 1,000 Gen-7 mass-produced vehicles by YE25

Also targeting Dubai in their expansion roadmap

➡️ All three players—Baidu, WeRide, and Pony—are planning deployments in Dubai, which is becoming a serious international testing ground.

➡️ Most Chinese self-driving fleets still seem concentrated in suburban or low-density areas—except for Baidu in Wuhan. I’m curious whether their entire fleets are actually active. It doesn’t quite feel like China has ~3,000 robotaxis truly operating, especially when Waymo is only at 1,500.

[IMAGE: chart/figure]

TSLA

~10 Model Ys running “FSD Unsupervised” in select Austin zones (Source: Elon interview)

Elon: fleet should hit ~1,000 “in a few months” (Source: Elon interview)

 Vision for millions of autonomous Teslas in 2H 2026 (Source: April 2025 earnings call)

➡️ The 1,000-car milestone doesn’t seem far-fetched (obviously comes down to execution) when benchmarked against the rest of the industry.

Some Broader Reflections

If we define the robotaxi product as:

Tech = autonomy stack (e.g. end-to-end models, perception, planning)

Engineering = teleops, edge-case handling, redundancy

Then whether it’s an E2E neural net approach or a modular HD-map-based stack, both still need engineering support, at least today.

The lines between the two are blurring. Hopefully one day we’ll see a clean, scalable, tech-only E2E product—but for now, both approaches still require “patches,” ops support, and manual guardrails to reach commercial-grade performance.

Thinking About Robotaxi as a Product

To win market share, it needs to deliver on:

✅ Better experience – safety is table stakes; UX/entertainment features are hard to differentiate

✅ Faster – maybe, but unclear how much users care

✅ Cheaper – this is the biggest lever

➡️ Among the three, cheaper is by far the most important differentiator in the next phase—especially as the industry goes from 1 → 100.

Bonus Thought

How many robotaxis does it take to reach ~10% market share in each of the top 10 U.S. cities?

o3 (whose math is way better than mine)’s answer = 10,000 vehicles.

We’ll see.

[IMAGE: chart/figure]

Source: research conducted by ChatGPT o3, with below prompts:

Summarize Waymo's expansion: Which cities have they announced (and when)? Which cities are they operating in (and since when)? Do they operate solo or with partners (e.g. Uber)?

Based on your research: How long does it take Waymo to bring a new city online—from mapping to public launch? Roughly how much does that cost?

For self-driving companies excluding Waymo (e.g. Baidu, WeRide, Pony.ai): 

What’s their expansion trajectory? From how many cities/cars (and when) to how many now? Number of cars announced vs. actually operating? Cities announced vs. actually live? Use both English and Chinese sources.

What has Elon/Tesla said about their robotaxi expansion? How many cars and in how many cities? Where do they start, and with how many cars? By [when], what’s the target number of cities and vehicles?

Uber/Lyft market sizing: How many miles, rides, and how much revenue in the top 10 U.S. cities? To capture 10% of that market, how many robotaxis are needed?

The information presented in this newsletter is the opinion of the author and does not necessarily reflect the view of any other person or entity, including Altimeter Capital Management, LP ("Altimeter"). The information provided is believed to be from reliable sources but no liability is accepted for any inaccuracies. This is for information purposes and should not be construed as an investment recommendation. Past performance is no guarantee of future performance. Altimeter is an investment adviser registered with the U.S. Securities and Exchange Commission. Registration does not imply a certain level of skill or training. Altimeter and its clients trade in public securities and have made and/or may make investments in or investment decisions relating to the companies referenced herein. The views expressed herein are those of the author and not of Altimeter or its clients, which reserve the right to make investment decisions or engage in trading activity that would be (or could be construed as) consistent and/or inconsistent with the views expressed herein.

This post and the information presented are intended for informational purposes only. The views expressed herein are the author’s alone and do not constitute an offer to sell, or a recommendation to purchase, or a solicitation of an offer to buy, any security, nor a recommendation for any investment product or service. While certain information contained herein has been obtained from sources believed to be reliable, neither the author nor any of his employers or their affiliates have independently verified this information, and its accuracy and completeness cannot be guaranteed. Accordingly, no representation or warranty, express or implied, is made as to, and no reliance should be placed on, the fairness, accuracy, timeliness or completeness of this information. The author and all employers and their affiliated persons assume no liability for this information and no obligation to update the information or analysis contained herein in the future.
