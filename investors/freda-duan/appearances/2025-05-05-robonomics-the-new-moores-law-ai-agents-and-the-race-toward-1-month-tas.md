---
investor: freda-duan
date: 2025-05-05
source: Robonomics
type: substack
url: https://robonomics.substack.com/p/the-new-moores-law-ai-agents-and
companies: [OPENAI, MANUS, LMND, STATE FARM, ALL, META, YCOMBINATOR]
topics: [ai-agents, agents-building-agents, ai-rd-automation, model-training-strategies]
companies_detail:
  - ticker: OPENAI
    focus: secondary
  - ticker: MANUS
    focus: secondary
  - ticker: LMND
    focus: mention
  - ticker: STATE FARM
    focus: mention
  - ticker: ALL
    focus: mention
  - ticker: META
    focus: mention
  - ticker: YCOMBINATOR
    focus: mention
topics_detail:
  - topic: ai-agents
    focus: primary
  - topic: agents-building-agents
    focus: secondary
  - topic: ai-rd-automation
    focus: secondary
  - topic: model-training-strategies
    focus: secondary
source_length: 641
fetch_method: substack_api
fetch_id: the-new-moores-law-ai-agents-and
---

# Robonomics — May 05, 2025

Moore’s Law for AI Agents

Data from METR shows that the length of tasks AI agents can complete (measured in human hours) is doubling every 7 months. That lines up with what many users have already felt.

[IMAGE: Image]

In 2022, agents could do tasks that took a human ~30 seconds. Today, they’re tackling 1-hour tasks with ~50% autonomy.

And if the trend holds, they’ll handle month-long human tasks by 2029.

But here’s the kicker:

Since 2024, the pace has accelerated. Some agents now double task-length capability every 4 months.

At that rate, we reach 1-month agents by 2027.

This isn’t just better tooling — it reflects fundamental leaps in model capability.

And now the wild part:

Agents are starting to help build better agents.

→ Agents writing better code

→ That builds better models

→ That train even better agents

An accelerating flywheel.

AI Systems for AI R&D Automation ("ASARA") concept mentioned in this blogpost:

https://forethought.org/research/will-ai-r-and-d-automation-cause-a-software-intelligence-explosion?utm_source=chatgpt.com

We might be entering a super-exponential era.

Been very impressed with o3 lately — it’s the first model that truly behaves like an agent. I wouldn’t be surprised if many users have switched from 4o and Deep Research.

Core capabilities of an agent: tool use, instruction following, and long-context reasoning.

o3 marks a step-change in tool use — tool calls happen within the chain of thought; visualization and data analysis are now built-in.

There seem to be two main approaches to agents:

→ OpenAI’s path: more black-box, end-to-end. The model learns to reason and build tools internally. It doesn’t mimic human workflows — it solves tasks directly.

→ Manus-style agents: more white-box, VM-based. They mimic human software use — opening browsers, clicking buttons, coding in VS Code.

These differing philosophies have consequences:

OpenAI’s models internalize tool use via unified training — the environment is more constrained, but the integration is tighter and the reinforcement learning signal is stronger.

White-box agents rely on external orchestration and interfaces — offering more flexibility, but at the cost of higher latency and complexity.

It’s also impressive that o3 can reason about and manipulate images mid-thought — crop, rotate, enhance — all seamlessly embedded in inference.

This is the first time OpenAI has fused vision and reasoning this deeply. True multimodal CoT.

From the outside looking in, OpenAI also seems to take a different approach to reasoning models vs. pretraining models.

Instead of “big model → distill down,” they appear to be doing the reverse for reasoning models:

Start with a small, reasoning-capable model → then scale it up with long inference and full tool use.

My hunch is that RL trains better on smaller, more controllable models first — and only then do they scale once the behavior stabilizes.

A few examples comparing the two:

1/ Visit the official YC website and compile all enterprise information under the W25 B2B tag into a clear, well-structured table. Be sure to find all of it.

→ Manus: https://manus.im/share/tnQ4mpSxMB9T83haiJowJv?replay=1

→ o3: https://chatgpt.com/share/681906e8-ae44-8009-96df-0212c6e359ae

Observation: Manus mimics human behavior — it methodically scraped the YC site step by step. o3, on the other hand, opted for a shortcut via GitHub. In this case, the slower manual route may actually be preferable.

2/ Create an interactive middle-school lesson on the momentum theorem: 8-slide deck (HTML/JS), short voice-over script, and a quiz in Google-Forms format.

→ Manus: https://manus.im/share/7d92Ua6R93MOdTbqNnp62P?replay=1

→ o3: https://chatgpt.com/share/68190763-1988-8009-aa2e-be2fb7e6b3ae

Observation: o3 really impressed me here.

3/ Compare three U.S. renters-insurance policies (Lemonade, State Farm, Allstate). Output a ranked table (premiums, deductibles, coverage caps, claim-payout speed) and a one-page recommendation memo.

→ Manus: https://manus.im/share/g0o85dnaURbmzNxDqIdBcp?replay=1

→ o3: https://chatgpt.com/share/681907dc-03b4-8009-b013-0411e1c17a3f

Observation: Both are solid. Overall, I think o3 tends to deliver stronger research quality.

4/ Can you pull META's MAU and DAU (1Q21–3Q24) for me? I need both charts (in pptx) and the underlying data (in Excel).

→ Manus: https://manus.im/share/VYcdkayt2jQ4JTsHuauhbY?replay=1

→ o3: https://chatgpt.com/share/68190c2f-7768-8009-838e-cbefddae7967

Observation: Both are solid.
