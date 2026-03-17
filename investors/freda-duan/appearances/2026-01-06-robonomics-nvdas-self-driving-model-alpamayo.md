---
investor: freda-duan
date: 2026-01-06
source: Robonomics
type: substack
url: https://robonomics.substack.com/p/nvdas-self-driving-model-alpamayo
companies: [NVDA, TSLA, MBG, UBER, LYFT, LCID, TTM]
topics: [autonomous-vehicles, ai-infrastructure, platform-economics, multi-modal-ai]
companies_detail:
  - ticker: NVDA
    focus: primary
  - ticker: TSLA
    focus: secondary
  - ticker: MBG
    focus: secondary
  - ticker: UBER
    focus: secondary
  - ticker: LYFT
    focus: secondary
  - ticker: LCID
    focus: mention
  - ticker: TTM
    focus: mention
topics_detail:
  - topic: autonomous-vehicles
    focus: primary
  - topic: ai-infrastructure
    focus: secondary
  - topic: platform-economics
    focus: secondary
  - topic: multi-modal-ai
    focus: secondary
source_length: 625
fetch_method: substack_api
fetch_id: nvdas-self-driving-model-alpamayo
---

# Robonomics — January 06, 2026

Implications - if successful:

If successful, this could be the “Android” of self-driving.

OEM accessibility improves materially. Many automakers could ship credible self-driving systems without spending billions on model development. For reference, TSLA’s self-driving training spend is estimated at $3–4B in FY24, with ~$5B per year likely required to sustain its edge.

The constraint shifts to time and hardware readiness - most cars on the road today only have 1-2 cameras - but that’s just a matter of time (and Chinese OEMs don’t have that constraint).

Platform economics improve for Uber / Lyft–style networks. 

Setup

Why this one might work:

This approach is directionally very similar to Tesla’s, both in hardware philosophy and end-to-end learning.

NVDA is not just selling tools anymore (as they’ve been doing before; with limited success) - it is now offering a complete model. 

Questions:

Track record: has been investing in autonomous driving for years, with mixed, publicly visible outcomes. This is the first time it is offering the full “brain” - not just the picks-and-shovels stack. Whether the model performs at production-grade levels, across real-world edge cases, remains an open question until it is road-tested at scale.

OEM adoption

Whether this model can get enough data

NVDA: trained on 80,000 hours of multi-camera driving video (>1B images), with disclosed real-world data spanning 25 countries, 2,500+ cities, and 1,727 hours.

TSLA: reports ~7B cumulative miles driven with FSD engaged. At 30 mph average speed → ~238M hours.

Bottom line:

You can read the paper 100x, but the real answer only comes from on-road performance. In this case, the first meaningful signal will be the Mercedes-Benz CLA deployments, expected in 2026. Until then, most conclusions are educated guesswork, and Tesla will likely continue to trade with a higher, sentiment-driven discount rate.

Self-driving remains frontier tech. There is still no consensus on:

Long-term market penetration, or

Sustainable market share for any single player

As a result, any new information that meaningfully shifts expectations on either dimension is likely to amplify volatility.

Approach - 

Before: Mostly “Picks and Shovels”

NVIDIA sold the platform:

In-car compute (DRIVE)

Software stack

Reference architectures

Simulation and training tooling

The driving policy itself - end-to-end model design and trained weights - was owned by OEMs, Tier-1s, or AV developers.

After: Offering the “Brain”

NVIDIA now provides a 10B-parameter VLA (Vision-Language-Action) model.

Training Stack

Training Chips

Trained on NVIDIA H100 (Hopper) clusters

Next-generation versions are being trained on Blackwell (B200)

Training Data

Total volume:

80,000 hours of multi-camera driving video

>1 billion images

Real-world data:

Collected across 25 countries and 2,500+ cities

1,727 hours explicitly referenced in the paper

Includes 360° camera coverage, plus LiDAR and radar for physical grounding

Data collection platform:

Vehicles instrumented to Hyperion 8 / 8.1 (NVIDIA’s AV reference platform)

Open dataset details:

7 cameras + 1 top-mounted 360° LiDAR for all clips

Radar available for a subset (163,850 clips)

Source: Hugging Face dataset

https://huggingface.co/datasets/nvidia/PhysicalAI-Autonomous-Vehicles

Does the model use LiDAR?

Logging includes LiDAR (per open dataset)

https://huggingface.co/datasets/nvidia/PhysicalAI-Autonomous-Vehicles

Alpamayo-R1 model inputs (per paper):

Multi-camera video

Calibration

Ego-motion

LiDAR is not explicitly listed as a direct model input

Paper: https://d1qx31qr3h6wln.cloudfront.net/publications/Alpamayo-R1_1.pdf

Versus Tesla

Tesla reports ~7B cumulative miles driven with FSD engaged.

Converting miles to “hours” requires assumptions and is only a rough proxy:

At 30 mph average speed → ~238M hours

Critically:

“Miles driven with FSD engaged” ≠ actual training set

The number is directional, not directly comparable

Customers and Early Partners

Confirmed Production Program

Mercedes-Benz CLA (2026 MY)

Next-generation, EV-first CLA

First U.S. Mercedes running fully on MB.OS

Sensor suite:

10 cameras

5 radar

12 ultrasonic sensors

“Showing Interest” (Important Wording)

Per NVIDIA’s press release - not confirmed production contracts:

Lucid

Jaguar Land Rover (JLR)

Uber

Berkeley DeepDrive

Source (NVIDIA Newsroom):

https://nvidianews.nvidia.com/news/alpamayo-autonomous-vehicle-development?utm_source=chatgpt.com

Hardware

[IMAGE: chart/figure]

https://arxiv.org/abs/2511.00088

https://research.nvidia.com/publication/2025-10_alpamayo-r1
