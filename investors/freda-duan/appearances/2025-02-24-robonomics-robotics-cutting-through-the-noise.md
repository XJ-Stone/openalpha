---
investor: freda-duan
date: 2025-02-24
source: Robonomics
type: substack
url: https://robonomics.substack.com/p/robotics-cutting-through-the-noise
companies: [TSLA, NVDA, OPENAI, FIGURE AI, GOOGL, GALBOT, BOSTON DYNAMICS]
topics: [robotics-manipulation, rl-for-robotics, robotics-hardware-production, simulation-to-real-gap]
companies_detail:
  - ticker: TSLA
    focus: secondary
  - ticker: NVDA
    focus: secondary
  - ticker: OPENAI
    focus: mention
  - ticker: FIGURE AI
    focus: mention
  - ticker: GOOGL
    focus: mention
  - ticker: GALBOT
    focus: mention
  - ticker: BOSTON DYNAMICS
    focus: mention
topics_detail:
  - topic: robotics-manipulation
    focus: primary
  - topic: rl-for-robotics
    focus: secondary
  - topic: robotics-hardware-production
    focus: secondary
  - topic: simulation-to-real-gap
    focus: secondary
source_length: 700
fetch_method: substack_api
fetch_id: robotics-cutting-through-the-noise
---

# Robonomics — February 24, 2025

Robotics is moving fast (lots of exciting demos lately), but there’s still so much confusion and a lack of clear benchmarks. Without a shared framework, it’s hard to evaluate real progress.

I genuinely want to see this industry thrive—so in the spirit of open-sourcing knowledge and pushing things forward, this (long) thread is my attempt to break down:

What’s impressive vs. what’s not

How to evaluate robots & demos

What frameworks can help

I welcome all feedback and input. A better-informed public means fewer missteps, less wasted effort, and faster progress for everyone. Let’s push the field forward.

🌟 TL;DR: What matters & where we are

Hardware: All about consistency + scaled production. The supply chain is maturing. Chinese players (and $TSLA) arguably have an edge in mass production.

Locomotion: More or less a solved problem via RL.

Manipulation: Still Day 1. Cutting-edge research (e.g., VLA) is here, but better simulation (e.g., $NVDA) is needed for a real step change.

Big picture: Robotics has made significant progress, but for manipulation, the industry is still in the demo phase.

That said, even demos deserve recognition—it all starts with getting one task right once before scaling to generalizable, consistent skills.

This doesn’t mean we’re “always years away” from commercialization. In fact, I believe things can move fast—from one final impressive demo to commercialization could take months, not years.

🌟 How to Evaluate a Robot or Demo

Start with the end goal (smooth/human-like, generalizable, and consistent) and work backward:

1. Generalization

Should work across diverse objects—varying color, reflectivity, and softness

Test with slight disruptions: lighting changes, interference, object positioning

2. Consistency

Most demos today are cherry-picked

Eventually, we should see robots executing hundreds of tasks, thousands of times, with high accuracy

🧠 Data & Robot Training 101

Robotics has a well-known data problem. Two primary sources:

Imitation learning (tele-op, real-world data)

Reinforcement learning (mostly simulation-based)

Rule of thumb:

If you have real-world data (e.g., $TSLA FSD), imitation learning can take you far

If you don’t, RL is the only option—and it’s now far more data-efficient

What’s changed recently:

✅ Language models (OpenAI, etc.)

✅ $NVDA's tools (Isaac Gym/Sim/Lab) are reducing the sim-to-real gap

✅ RL has expanded from single-task to a broader set of useful tasks

Chips?

Robot models are much smaller than LLMs, so even Chinese players aren’t significantly chip-constrained.

2025 (and beyond) = The Year of RL for Robotics

▶️ Hardware

“Consistent quality + scaled production.”

Precision is harder to maintain for mobile robots than cars—every moving part must repeat complex joint movements reliably across a fleet.

Progress: The robotics supply chain (esp. in Asia) is evolving fast—even dexterous hands are being tackled.

Cost: ~$100k per humanoid in the U.S., less than half for Chinese players.

Open questions:

Will robotics hardware follow the EV industry shakeout?

Many EV makers burned billions and failed—even with a mature supply chain. Why wouldn’t the same happen here?

▶️ Locomotion (e.g. walking, running, backflip)

Locomotion is more or less a solved problem today.

Old way: Rule-based MPC (think Boston Dynamics)

New way: RL, which is more scalable and leads to better balance/control

There’s still debate on whether RL truly generalizes.

Robots can now hike varied terrain without retraining

But distinct actions (e.g., hiking vs. backflip) still require separate models

👉 Great breakdown from Jim Fan: link

▶️ Manipulation (e.g. sorting, wiping, general tasks)

RL, which works like magic for locomotion, struggles here. Why?

Objects vary too much: shape, rigidity, material

The sim-to-real gap is much larger

Tasks like cooking, washing dishes, and opening bottles are highly diverse

VLA (Vision-Language-Action) is the current buzzword—think of it as FSD for robotics.

It’s an end-to-end model, trained using massive RL + simulation.

Players: Figure AI, DeepMind, Galbot (China) are all in the game.

Reality check:

Even tele-op-assisted manipulation (1X, Tesla Optimus) is impressive given today’s constraints.

Open questions:

How much can real-world data help scale manipulation?

If simulation is the bottleneck, what should $NVDA build to leapfrog the field?

Final Thoughts

I’m excited about where robotics is headed—but we need to cut through the noise and focus on real progress.

Breakthroughs will come faster than expected—if we stay grounded and focus on what truly moves the industry forward.
