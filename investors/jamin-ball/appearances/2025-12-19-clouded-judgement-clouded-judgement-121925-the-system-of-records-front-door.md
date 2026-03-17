---
investor: jamin-ball
date: 2025-12-19
source: Clouded Judgement
type: substack
url: https://cloudedjudgement.substack.com/p/clouded-judgement-121925-the-front
companies: [SABR, AMS.MC, GALILEO, WORLDSPAN, TRAVELPORT, BKNG, EXPE, PRICELINE, TRAVELOCITY, CRM, WDAY, NOW]
topics: [agent-front-door, system-of-records-evolution, saas-valuation, travel-gds-analogy]
companies_detail:
  - ticker: SABR
    focus: secondary
  - ticker: AMS.MC
    focus: secondary
  - ticker: GALILEO
    focus: mention
  - ticker: WORLDSPAN
    focus: mention
  - ticker: TRAVELPORT
    focus: mention
  - ticker: BKNG
    focus: secondary
  - ticker: EXPE
    focus: secondary
  - ticker: PRICELINE
    focus: mention
  - ticker: TRAVELOCITY
    focus: mention
  - ticker: CRM
    focus: secondary
  - ticker: WDAY
    focus: secondary
  - ticker: NOW
    focus: secondary
topics_detail:
  - topic: agent-front-door
    focus: primary
  - topic: system-of-records-evolution
    focus: secondary
  - topic: saas-valuation
    focus: secondary
  - topic: travel-gds-analogy
    focus: mention
source_length: 1903
fetch_method: substack_api
fetch_id: clouded-judgement-121925-the-front
---

# Clouded Judgement — December 19, 2025

# Clouded Judgement — December 19, 2025

Every week I’ll provide updates on the latest trends in cloud software companies. Follow along to stay up to date!

Subscribe now

The System of Record’s “Front Door”

Last week I wrote a post about the evolving role systems of record will play in the era of agents. The core argument was that while interfaces, workflows, and agents are changing rapidly, enterprises still need something far more boring and far more important underneath it all: a reliable source of truth. As workflows become more automated and more agent driven, the real failure mode is not model quality, but whether the agent pulled the right definition from the right system at the right moment.

A lot of people interpreted that post as a kind of safety blanket for legacy SaaS systems of record. They’re too important to be disrupted. They hold the data. They define the truth. They’re safe. This post is meant as a follow up, not so much to counter that conclusion, but to reframe it. Systems of record are not disappearing. But they are evolving in ways that materially change where value accrues.

The analogy that keeps coming to mind is the travel industry at the dawn of the internet. I’m not a travel industry expert, but the shape of the transition feels similar.

Before the internet, travel was booked through Global Distribution Systems, or GDSs. These were centralized networks where airlines, hotels, and car rental companies published inventory, pricing, and availability. Instead of travel agents querying dozens of individual airline systems, there was one place to look. When a seat was sold or a fare changed, the GDS was where that state was updated and propagated. Systems like Sabre and Amadeus were not necessarily consumer products, but infrastructure. They quietly sat in the middle of the ecosystem, normalizing data, enforcing rules, and handling transactions on behalf of downstream users.

The major GDS platforms, Sabre, Amadeus, Galileo, and Worldspan, were founded decades before the consumer internet. Sabre dates back to the 1960s, with the others emerging in the late 1980s and early 1990s. These systems were the systems of record for travel inventory. They also owned the front door - the experience layer. Travel agents interacted directly with the GDS, and consumers rarely booked travel themselves. You went through an intermediary. The system of record aggregated the data, defined the workflow, and captured the value (because they owned the front door).

Then came the internet, and with it Online Travel Agencies. Expedia, Priceline, Travelocity, and Booking.com were all founded in the mid 1990s. Importantly, these companies still needed a reliable source of truth. That source of truth remained the GDS. But the internet introduced a new front door, and a new end user (direct consumers).

Once OTAs sat on top of the GDS, two things happened. First, a new end user emerged. Consumers could now book travel directly without going through a human travel agent. Second, while GDS platforms still served as the front door for travel agents, a much larger front door appeared for consumers, one the GDS providers did not control.

With the benefit of hindsight, we know how this industry played out. The original systems of record (GDSs) survived, but their value capture changed dramatically. Amadeus is still public today, with a market cap around $30 billion. Sabre was taken private for roughly $5 billion in 2007, later re IPOed, and now trades at under $1 billion. Galileo and Worldspan were consolidated under Travelport, which was taken private in 2023 for about $4 billion. Meanwhile, Booking is worth roughly $175 billion, and Expedia around $35 billion.

The system of record did not disappear. But it lost control of the front door, and with it, a large share of the economic upside. I asked ChatGPT to create a graphic for this, and it did a pretty good job! I coulnd’t get it to reverse the arrows from Airlines / hotels / car rentals going to the GDS (instead of the GDS pointing to them). On the left, the GDS captured the main front door. On the right, the OTAs captured the front door, with the GDS capturing the smaller “side” door for travel agents. 

[IMAGE: chart/figure]

I think something very similar is playing out in enterprise software today. Legacy SaaS systems of record like Salesforce, Workday, and ServiceNow have historically owned both the source of truth and the primary interface for humans and admins (ie the front door). AI changes that equation. A new end user is emerging in the form of agents, and with that comes a new front door to the system of record.

The question is not whether these systems remain important. They will. The question is whether they capture this new front door, or whether someone else does. And that distinction matters enormously for where value accrues.

The optimistic read is that Amadeus is still a $30 billion company. The less optimistic read is that Booking and Expedia together are worth well over $200 billion. Capturing the new front door can dwarf the value of owning the underlying system of record. Is this what Satya mean when he compared legacy SaaS apps to a “dumb DRUD database”? Humans will still interact with enterprise systems, but far less frequently, and at far smaller scale, than agents will.

This is, I think, at the core of the recurring “is software dead” debate. The answer is not binary. Software is not going away. But the balance of power and profit may shift. The open question is whether legacy SaaS systems of record evolve to own the agent front door, or whether they become thinner, lower margin layers underneath a new generation of platforms that capture the majority of the incremental value from here.

An idea for a follow up post - what will be the offensive / defensive reactions these “legacy” systems of record take. 

Offensive - innovating themselves, and building the new front door

Defensive - locking down the data, and adopting the “egress fees” that the hyperscalers have (ie charging people to access the data or move it out of their own system of record)

I think we’ll see a lot of the latter!

Top 10 EV / NTM Revenue Multiples

[IMAGE: chart/figure]

Top 10 Weekly Share Price Movement

[IMAGE: chart/figure]

Update on Multiples

SaaS businesses are generally valued on a multiple of their revenue - in most cases the projected revenue for the next 12 months. Revenue multiples are a shorthand valuation framework. Given most software companies are not profitable, or not generating meaningful FCF, it’s the only metric to compare the entire industry against. Even a DCF is riddled with long term assumptions. The promise of SaaS is that growth in the early years leads to profits in the mature years. Multiples shown below are calculated by taking the Enterprise Value (market cap + debt - cash) / NTM revenue. 

Overall Stats:

Overall Median: 4.6x

Top 5 Median: 20.9x

10Y: 4.1%

[IMAGE: chart/figure]

[IMAGE: chart/figure]

Bucketed by Growth. In the buckets below I consider high growth >22% projected NTM growth, mid growth 15%-22% and low growth <15%. I had to adjusted the cut off for “high growth.” If 22% feels a bit arbitrary, it’s because it is…I just picked a cutoff where there were ~10 companies that fit into the high growth bucket so the sample size was more statistically significant

High Growth Median: 13.8x

Mid Growth Median: 7..6x

Low Growth Median: 3.7x

[IMAGE: chart/figure]

[IMAGE: chart/figure]

EV / NTM Rev / NTM Growth

The below chart shows the EV / NTM revenue multiple divided by NTM consensus growth expectations. So a company trading at 20x NTM revenue that is projected to grow 100% would be trading at 0.2x. The goal of this graph is to show how relatively cheap / expensive each stock is relative to its growth expectations.

[IMAGE: chart/figure]

[IMAGE: chart/figure]

EV / NTM FCF

The line chart shows the median of all companies with a FCF multiple >0x and <100x. I created this subset to show companies where FCF is a relevant valuation metric. 

[IMAGE: chart/figure]

Companies with negative NTM FCF are not listed on the chart

[IMAGE: chart/figure]

Scatter Plot of EV / NTM Rev Multiple vs NTM Rev Growth

How correlated is growth to valuation multiple?

[IMAGE: chart/figure]

Operating Metrics

Median NTM growth rate: 12%

Median LTM growth rate: 13%

Median Gross Margin: 76%

Median Operating Margin (1%)

Median FCF Margin: 19%

Median Net Retention: 108%

Median CAC Payback: 36 months

Median S&M % Revenue: 37%

Median R&D % Revenue: 23%

Median G&A % Revenue: 15%

Comps Output

Rule of 40 shows rev growth + FCF margin (both LTM and NTM for growth + margins). FCF calculated as Cash Flow from Operations - Capital Expenditures 

GM Adjusted Payback is calculated as: (Previous Q S&M) / (Net New ARR in Q x Gross Margin) x 12. It shows the number of months it takes for a SaaS business to pay back its fully burdened CAC on a gross profit basis. Most public companies don’t report net new ARR, so I’m taking an implied ARR metric (quarterly subscription revenue x 4). Net new ARR is simply the ARR of the current quarter, minus the ARR of the previous quarter. Companies that do not disclose subscription rev have been left out of the analysis and are listed as NA. 

[IMAGE: chart/figure]

[IMAGE: chart/figure]

Sources used in this post include Bloomberg, Pitchbook and company filings

The information presented in this newsletter is the opinion of the author and does not necessarily reflect the view of any other person or entity, including Altimeter Capital Management, LP (”Altimeter”). The information provided is believed to be from reliable sources but no liability is accepted for any inaccuracies. This is for information purposes and should not be construed as an investment recommendation. Past performance is no guarantee of future performance. Altimeter is an investment adviser registered with the U.S. Securities and Exchange Commission. Registration does not imply a certain level of skill or training. Altimeter and its clients trade in public securities and have made and/or may make investments in or investment decisions relating to the companies referenced herein. The views expressed herein are those of the author and not of Altimeter or its clients, which reserve the right to make investment decisions or engage in trading activity that would be (or could be construed as) consistent and/or inconsistent with the views expressed herein.

This post and the information presented are intended for informational purposes only. The views expressed herein are the author’s alone and do not constitute an offer to sell, or a recommendation to purchase, or a solicitation of an offer to buy, any security, nor a recommendation for any investment product or service. While certain information contained herein has been obtained from sources believed to be reliable, neither the author nor any of his employers or their affiliates have independently verified this information, and its accuracy and completeness cannot be guaranteed. Accordingly, no representation or warranty, express or implied, is made as to, and no reliance should be placed on, the fairness, accuracy, timeliness or completeness of this information. The author and all employers and their affiliated persons assume no liability for this information and no obligation to update the information or analysis contained herein in the future.

Subscribe now

Share Clouded Judgement

Leave a comment
