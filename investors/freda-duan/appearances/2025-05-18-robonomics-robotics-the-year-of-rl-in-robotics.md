---
investor: freda-duan
date: 2025-05-18
source: Robonomics
type: substack
url: https://robonomics.substack.com/p/robotics-framework
companies: [TSLA, NVDA, UNITREE]
topics: [robotics-rl, sim-to-real, manipulation-learning, robotics-reshoring]
companies_detail:
  - ticker: TSLA
    focus: secondary
  - ticker: NVDA
    focus: secondary
  - ticker: UNITREE
    focus: mention
topics_detail:
  - topic: robotics-rl
    focus: primary
  - topic: sim-to-real
    focus: secondary
  - topic: manipulation-learning
    focus: secondary
  - topic: robotics-reshoring
    focus: mention
source_length: 512
fetch_method: substack_api
fetch_id: robotics-framework
---

# Robonomics — May 18, 2025

2025 is the year of agents in the LLM world—and the year of RL in robotics.

Robots today are roughly where $TSLA’s Autopilot was in 2019–2020.

Optimus walking or dancing? Probably comparable to Tesla’s early lane-following.

Reinforcement Learning (RL) is one of the few learning algorithms that can operate across both:

🧠 The world of bits

🤖 And the world of atoms

But there’s still a lot of jargon and confusion in this space. Here’s one way to frame the core approaches—using a simple 2×2 matrix:

[IMAGE: Image]

🧭 A Simple Framework for Robotics Learning

Use CaseData TypeLearning TypeExample / CommentFSDReal-worldSupervised (+RL)$TSLA Autopilot, lane followingLocomotionSimulationRLUnitree, Optimus – trained in sim, deployed in real worldManipulationEvolvingHybridVaries – mix of supervised + RL, often using real data

✅ Locomotion = Sim Data × RL

Locomotion is largely solved with RL.

Robots are trained entirely in simulation

Then transferred directly to the real world

The sim-to-real gap is no longer a major blocker

RL has improved too—it’s no longer limited to one-off tasks.

Today’s RL can generalize across a broader set of useful behaviors.

🔍 Open question: How general can this get?

So far, even similar actions (e.g., hiking, running, dancing) still require separate models.

🧩 Manipulation = Still Evolving

Manipulation is a much harder problem.

In theory, we want it to be sim data × RL too—but:

The reward functions are harder to define

Walking = “don’t fall”

Opening a door = ???

Real-world tasks are highly variable

Most models today rely on real-world data × supervised learning

With the rise of VLA (Vision-Language-Action) models, we’re starting to see hybrid approaches:

sim + real data × supervised learning

→ and slowly, RL is entering the mix

🔍 First Principles: The Real Bottleneck Is Data

Zooming out, the real bottleneck becomes clear:

Data.

Imitation learning doesn’t scale.

Most teams are still paying $50–$100/hour for manual data collection.

Want 100 million hours of interaction?

You’re looking at billions of dollars, before even testing your scaling law.

This leaves two paths forward:

Path 1: Breakthroughs in simulation

$NVDA’s role becomes critical

Need to "sim everything"

Must model real-world physics, materials, edge cases

Path 2: Real-world agents, born digital

Start with agents that master software, screens, and interfaces

From 2D → 3D: expand from the digital world into the physical

Let AI adapt to hardware, not the other way around

📈 Why Robotics Really Matters

Productivity growth is the only thing that moves GDP long term.

And robotics may be the biggest unlock in decades.

McKinsey estimates that AI + robotics could raise U.S. productivity from ~1.8% → 3–4% annually.

That’s trillions in added GDP

Enough to offset demographic drag from aging populations

🏭 A National Strategy

But this isn’t just about economic growth.

In a fractured, post-globalization world, robotics should be a national strategy.

It’s the only way the U.S. and its allies can reshore manufacturing without giving up cost competitiveness.

Robots flatten the global labor curve—on both cost and quality.

Thanks for reading Driven by Duan! Subscribe for free to receive new posts and support my work.
