---
investor: jamin-ball
date: 2026-02-20
source: Clouded Judgement
type: substack
url: https://cloudedjudgement.substack.com/p/clouded-judgement-22026-the-ssd-memory
companies: [000660.KS, 005930.KS, KIOXIA, SANDISK, MU, WDC, HAMMERSPACE]
sectors: [ai, semiconductors, flash-memory, ssd-storage, storage, infrastructure, cloud, enterprise-storage, data-orchestration, saas]
source_length: 2879
fetch_method: substack_api
fetch_id: clouded-judgement-22026-the-ssd-memory
---

# Clouded Judgement — February 20, 2026

Every week I’ll provide updates on the latest trends in cloud software companies. Follow along to stay up to date!

Subscribe now

The SSD / Memory Reckoning

Memory stocks have taken over recently. If the early AI “trade” was compute, the current trade is memory! Over the last year:

SK Hynix is up >300%

Samsung is up >200%

Kioxia is up ~1,000%

Sandisk is up >1,200%

Micron is up >300%

Western Digital is up >400%

This is by no means an exhaustive list of memory related stocks, but it should give you a flavor of what’s happening in the stock market for memory related companies. So what’s happening? Why are memory stocks having a moment? I asked David Flynn, founder and CEO of Hammerspace to share his perspective. The below post was written together by David and myself. David is a repeat founder and long-time storage/memory architect who built Fusion-io, the company that put flash on the server fast path and helped change the industry’s performance playbook (later acquired by SanDisk). He also helped invent the architectural precursor to NVMe, so his perspective on why memory stocks are ripping is grounded in first-hand experience building the systems that made this era possible, and it’s only getting more critical as AI evolves and memory bandwidth, latency, and supply become the limiting factors for scaling compute.

Let’s dig in! 

Most of the conversation around AI infrastructure centered on GPUs over the last two years. That’s understandable; compute was the obvious driver of AI innovation and in a very short period of time has had a profound global economic effect. GPU supply has begun to normalize relative to two years ago (but still remains quite constrained!), however a new constraint has emerged that should have been foreseen and is potentially longer lasting: memory and storage due to global shortage in NAND flash memory supply. In many ways, memory and solid state storage now feels like GPUs did two years ago.

From Compute Bound to Data Bound

The memory and storage markets have exploded recently, but why? Early AI was training heavy. What does this mean? You loaded datasets, ran repeated passes, and optimized weights. It was compute bound and AI innovators were racing to deploy more GPUs, as fast as possible. Once the data was staged, GPUs did most of the work (and you hammered those GPUs with data…). Of course, over time, as training runs got larger, we added more and more data to the runs. However, inference is different. It’s more interactive / concurrent / session based. Models are pulling from large, diverse datasets, often stored in different locations, in real time. That makes the system increasingly data bound. It is not practical to colocate GPUs in every location data is generated and stored, the data needs to be “known to exist” and moveable to place it with a GPU when it is needed for a processing job. Results depend less on raw compute and more on how efficiently data can move to the model (from wherever it resides). Manual data identification, preparation, and management is too slow and cumbersome. And legacy storage systems are inefficient at this type of workload (and rely on overprovisioning both memory and solid state disk drives (SSDs)). Optimal AI architectures require all data to be able to be delivered at high performance to feed the GPUs for inference faster.

But there’s another accelerant: AI is now generating more data than it consumes. Inference is producing new artifacts continuously -synthetic training data, augmented datasets, embeddings and vector indexes for retrieval, logs/telemetry for evaluation and safety, and agent outputs that get stored, versioned, and re-used. Even when the underlying “source” data doesn’t change, AI pipelines create multiple derived representations (chunks, summaries, features, indexes) that have to be stored somewhere and be refreshed as models evolve. The result is a compounding data footprint: more reads and more writes, more metadata, more movement, and more capacity needing to be high performance.

Now add the KV cache (which is stored in memory). Every time a model processes a prompt, it stores intermediate attention state so it can generate the next tokens efficiently without recomputing prior context. What does this mean to an AI architect? Longer prompts? Bigger KV cache. More concurrent users? Bigger KV cache. Larger context windows? Bigger KV cache. Longer running agents & tasks? Bigger KV cache. All of these trends are pushing the limits of the KV cache (and creating incredible demand for memory). Unlike model weights, which are fixed, this memory footprint scales dynamically with usage. Memory demand rises meaningfully! That memory typically lives in GPU memory first, then spills into host DRAM and fast storage as systems scale. So inference does not just consume compute. It consumes memory across the entire hierarchy (from storage nodes to controller nodes to caching tiers to GPU nodes).

The more AI gets used, the more memory the system requires.

The Memory Crisis

The increased use of data that already exists, coupled with an increased amount of data generated and stored has created a global NAND shortage. NAND is used in memory and SSDs used for high-performance data storage. The NAND shortage isn’t just a typical quarterly fluctuation, it’s quickly becoming the underlying driver of a broader memory crisis. We’re coming off a massive downturn where manufacturers slashed production and returned to extreme capital discipline only to have AI demand explode at a rate that the market did not account for. Hyperscale clusters are now consuming exabytes of data annually. The multi-year supply agreements being signed today cover capacity that won’t even exist until 2027. That’s a structural shift, not a pricing cycle.

The “Flash Tax” on Innovation

The industry’s default response to AI scale has been overprovisioning capacity. When flash was abundantly available and relatively cheap, inefficiency was tolerated. Now that flash is in short supply and the price has skyrocketed, inefficiency painfully amplifies the problem.

The scarcity of flash changes the math for the entire infrastructure stack. AI clusters are tightly integrated systems including GPUs, storage, networking, and power integrated as a single unit. When flash costs spike and/or allocation is unpredictable, the “all-in” price per deployed GPU goes up forcing many customers to alter their deployment strategies, with profound implications.

Hyperscalers will just write a bigger check and pass the cost down to their tenants. But for Enterprises trying to stand up their next generation AI clusters, the “flash tax” is potentially a project killer. It forces harder, more conservative decisions about what customers can actually fund and how fast they can actually scale.

The Problem with “Enterprise-Grade” Storage

What can no longer be ignored is that most “enterprise-grade” storage architectures weren’t built for AI. They were built for traditional enterprise IT—transactional apps, VM farms, home directories, backup, and predictable throughput—not for feeding GPUs at line rate with high concurrency, low latency, and massive metadata activity… often with data stored in different data centers and clouds.

There are two main challenges historical storage architectures face in the Age of AI. These are what are creating such a crippling demand for memory as organizations look to fix it:

First, the tiering model breaks down. Historically, storage was broadly organized into three tiers: a performance tier for fast access (flash), a capacity tier for “cold” data you still need (HDDs), and an archive tier (often tape). In the Age of AI, data centers increasingly need performance across every tier—because AI pipelines don’t neatly separate “hot” vs “cold,” and retrieval/inference workflows routinely reach into long-tail datasets. But the capacity and archive tiers can’t deliver GPU-class performance because the physical media and architectures weren’t designed for it. What are we seeing? A shift toward all-flash (or flash-heavy) data centers and that pushes memory demand up because flash systems carry significant memory/metadata overhead to deliver performance and manage large namespaces at scale.

Second, the legacy NAS data path has too many hops—and too many copies. Traditional NAS architectures typically involve three roles: the storage node, a controller (or head), and the server/client. Each has CPUs, memory, NICs, and switches between them. If you trace the path from where data physically sits (let’s start at NVMe) to a GPU, the data is repeatedly staged, buffered, and copied: NVMe → CPU/memory → NIC (storage node) → switch → NIC → CPU/memory → NIC (controller) → switch → NIC → CPU/DRAM (client) → GPU (see image below). That’s easily 8–10 copies/hops depending on the design. When performance requirements were modest, this “hop tax” was tolerable. In the Age of AI—especially inference, where latency and concurrency dominate—it becomes a structural bottleneck. The common “fix” is to throw more memory at caching and buffering across the stack, which drives even more demand and cost.

[IMAGE: chart/figure]

The old-school response to this has been simple: overbuild. Throw more NVMe at it, make more copies, and hope the hardware masks the inefficiency. When flash was cheap and abundant, that waste was just noise. But in a constrained market, that inefficiency becomes a massive and debilitating liability (as well as a massive cost as prices rise!).

In an AI environment, you have unpredictable data reuse, massive and rapid scale, and since GPU servers have far greater gravity than data the orchestration of that data needs to be transparent and global in scale.

The GPU Utilization Trap

The demand for GPUs isn’t slowing down, but they don’t live in a vacuum. A 1000-GPU cluster might have hundreds of petabytes of SSD storage sitting behind it. If that SSD storage is delayed your GPUs spend their time idling.

The SSD crisis doesn’t eliminate GPU demand, but it can shift revenue timing, slow activation cycles, and introduce friction into the AI expansion curve. The GPU economy is now interdependent with SSD availability.

Solving for Efficiency, Not Just Supply

The global NAND issues are not easily fixable, but we can stop being so wasteful with the silicon we already have. At Hammerspace, we look at this as a data orchestration problem. Some of the benefits of the Hammerspace data platform:

Leverage GPU Server Storage: GPU servers typically ship with local NVMe. Hammerspace enables you to use it as strategic Tier-0 shared storage with Enterprise-class reliability. This enables you to leverage an asset you have already invested in, immediately move forward with your AI projects and since the data is exactly where the compute lives, you will get the highest levels of performance. In the “legacy” graphic shared above data takes 8-10 hops. With Tier-0 (graphic below) it takes only 1.

[IMAGE: chart/figure]

Consider HDD Storage: Not all data is “hot.” Orchestrating “cold” sets to high-capacity HDD systems saves the fast flash for the work that actually needs it.

Recover Stranded Capacity: Most enterprises have petabytes of storage locked in legacy silos. We federate those assets into one logical system so you can stop buying new SSDs to create yet another storage silo for AI and instead continue using what you already own.

Hybrid Cloud: The public cloud has supply of both GPUs and SSD storage, and we provide a single logical system that enables a hybrid cloud approach that many of our customers are already using. You can leverage GPUs both on premises and in cloud and orchestrate data seamlessly to where you GPUs are without copying data.

Intelligent Tiering: We orchestrate data between all of these different tiers live and transparently leveraging policies that eliminates any impact to your operations.

Geo-Deduplication: You shouldn’t have to replicate a dataset three times just to access it in three regions. Our global namespace lets you access one instance of the data from anywhere, instantly reducing your flash footprint.

In Summary

We’re moving into a phase where AI success won’t only be defined by who has the biggest purchase orders for GPUs. It will also be determined by those who manages their data most intelligently regardless of physical constraints. Flash isn’t infinite and that has become glaringly apparent. It’s time we started building architectures that not only reflect that reality but thrive in spite of it.

Quarterly Reports Summary

[IMAGE: chart/figure]

Top 10 EV / NTM Revenue Multiples

[IMAGE: chart/figure]

Top 10 Weekly Share Price Movement

[IMAGE: chart/figure]

Update on Multiples

SaaS businesses are generally valued on a multiple of their revenue - in most cases the projected revenue for the next 12 months. Revenue multiples are a shorthand valuation framework. Given most software companies are not profitable, or not generating meaningful FCF, it’s the only metric to compare the entire industry against. Even a DCF is riddled with long term assumptions. The promise of SaaS is that growth in the early years leads to profits in the mature years. Multiples shown below are calculated by taking the Enterprise Value (market cap + debt - cash) / NTM revenue. 

Overall Stats:

Overall Median: 3.2x

Top 5 Median: 18.4x

10Y: 4.1%

[IMAGE: chart/figure]

[IMAGE: chart/figure]

Bucketed by Growth. In the buckets below I consider high growth >22% projected NTM growth, mid growth 15%-22% and low growth <15%. I had to adjusted the cut off for “high growth.” If 22% feels a bit arbitrary, it’s because it is…I just picked a cutoff where there were ~10 companies that fit into the high growth bucket so the sample size was more statistically significant

High Growth Median: 10.7x

Mid Growth Median: 7.0x

Low Growth Median: 2.7x

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
