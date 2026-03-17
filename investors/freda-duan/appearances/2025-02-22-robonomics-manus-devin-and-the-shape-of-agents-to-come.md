---
investor: freda-duan
date: 2025-02-22
source: Robonomics
type: substack
url: https://robonomics.substack.com/p/manus-devin-and-the-shape-of-agents
companies: [MANUS, DEVIN, ANTHROPIC, OPENAI, META, BKNG, GOOGL, DEEPSEEK, DEEPSEARCH]
topics: [ai-agents, computer-using-agents, agentic-commerce, agent-memory]
companies_detail:
  - ticker: MANUS
    focus: primary
  - ticker: DEVIN
    focus: secondary
  - ticker: ANTHROPIC
    focus: secondary
  - ticker: OPENAI
    focus: secondary
  - ticker: META
    focus: mention
  - ticker: BKNG
    focus: mention
  - ticker: GOOGL
    focus: mention
  - ticker: DEEPSEEK
    focus: mention
  - ticker: DEEPSEARCH
    focus: mention
topics_detail:
  - topic: ai-agents
    focus: primary
  - topic: computer-using-agents
    focus: secondary
  - topic: agentic-commerce
    focus: secondary
  - topic: agent-memory
    focus: secondary
source_length: 898
fetch_method: substack_api
fetch_id: manus-devin-and-the-shape-of-agents
---

# Robonomics — February 22, 2025

[IMAGE: Image]

Another Step Forward for AI Agents

Been testing @ManusAI_HQ over the past few days—here are some quick thoughts:

Workflow Transparency

$Manus stands out for its ability to visually track agent workflows step-by-step and share replayable links (examples below). This closely mirrors the appeal of DeepSeek's “DeepThink” and highlights how much users value transparency in agents' thought processes.

Memory

Memory updates happen in real-time (upon user confirmation), which I see as a key requirement for broad agent adoption.

Comparison with $Devin

Both $Manus and $Devin operate full virtual machines—planners, IDEs, browsers, terminals, and MCP—with room for further performance via RL optimization.

Interestingly, both are built on Claude Sonnet, which seems well-suited for agent systems thanks to its strength in instruction-following and agentic behaviors.

$Manus is more user- and customer-facing, while $Devin is geared toward developers. In general, Manus tends to deliver more comprehensive results and faster turnaround.

OpenAI vs. Anthropic

@AnthropicAI increasingly looks like an OS or Android-style platform supporting a full ecosystem of agents.

@OpenAI leans more Apple-like—fully integrated from infrastructure to interface.

Comparison with GPT Operator (Beta)

It’s a bit unfair to compare $Manus with $OpenAI Operator today since Operator is still in beta. Operator currently lacks IDE/terminal integration and Office-suite functions.

Operator (and DeepSearch) also tend to start with multiple clarifying questions, whereas Manus jumps right into task execution. It’ll be interesting to see how Operator evolves into a fuller product.

Limitations

$Manus currently avoids directly making bookings. It prompts me to handle them manually rather than input credentials into the VM.

Interesting Manus Examples:

Tariff Trajectories & Investment Implications:

https://manus.im/share/ispmaS1CQ68z8KlVVW8K1B?replay=1

Robotaxi Launch Marketing (~20 docs):

https://manus.im/share/QrR8KEP6BoLPMlyA9RrSwR?replay=1

Brad Gerstner Deck Compilation:

https://manus.im/share/USVrjj7kzXP0pJ3h9rZdlP?replay=1

Interactive Game Design:

https://manus.im/share/cAkrqELWwTNZ40FxwcAzII?replay=1

META DAU/MAU Pull:

https://manus.im/share/VYcdkayt2jQ4JTsHuauhbY?replay=1

US Fiscal Deficit Analysis:

https://manus.im/share/RRj2qUegBZ5sSEIWGDIwsN?replay=1

Quick Thoughts on Agents — Opportunities & Open Questions

▶️ Tasks like “book a hotel” or “pull historical financials” are mostly solved!

Agents can already parse earnings reports and navigate Booking.com. Complex flows still trip them up, but it’s increasingly a solved (or solvable) problem.

▶️ Accuracy & Speed should be the north stars.

▶️ Lower Build & Migration Costs

It took me two minutes to spin up this website: 

https://dog-breed-quiz-app-pban7z74.devinapps.com

Consumers win—lower switching costs, more choices. Competition will shift toward product quality.

▶️ Agents ≠ Automation Tools?

The more I think about it, the more most “agents” today are just automation tools—like how most “robots” are really just machines 🤖

❓A Few Key Questions — Would Love Your Thoughts

1. Remote Servers & Logins

If agents need to log into Booking.com or Gmail to act on our behalf, how will those services respond?

Some may block remote logins for security. Is there a technical workaround?

2. Generalization vs. Fine-Tuning

Do agents need to be trained per environment (e.g., Booking.com)? Or can they generalize?

Feels like an RL / post-training question.

3. Frontend vs. Backend Agent Execution

Anthropic’s “Computer Use” seems to run on the frontend—remotely controlling your actual desktop (ref: Rowan’s post).

This might boost accuracy, but it’s not practical. Devin’s backend-style “background agent” seems more useful—but how much accuracy does it sacrifice?

A Few $Devin Test Cases That Stood Out

1. Pulling $META MAU/DAU (1Q21–3Q24)

Devin took 11 minutes, delivered perfect Excel data.

It didn’t hallucinate numbers post-4Q23 (Meta stopped reporting)—it simply omitted them.

It navigated Meta’s IR site and parsed the reports like a diligent intern.

→ This proves $Devin (and similar agents) can “read” real screens.

2. Booking a Hotel

Devin booked the InterContinental NYC on Booking.com in 5 minutes.

It filled the right fields, recovered from errors, and got the job done.

Unclear whether it was trained on Booking.com or figured it out on the fly.

3. Canceling a Booking

This was trickier—cancellation required a login, so Devin accessed my Booking.com via Gmail.

It succeeded—but Google blocked Devin from directly logging into Gmail when I tried that separately.

4. Booking from Hotel Websites

Tried InterContinental NYC and Four Seasons Boston via their official sites.

It struggled with selecting check-in/check-out dates—some progress, some blockers.

Takeaways from Scott Wu (Invest Like the Best)

1/ Self-Driving Cars = the First True Agents

Driving requires 99.999% accuracy. Agents like $Devin are still in their 2014-era—saving 90% of the effort but still imperfect.

2/ Impact on Collaboration Platforms

Agents will reshape how tools like Slack and GitLab are used—likely becoming co-workers alongside humans.

▶️ Agent Technologies: API-Based vs. Computer-Using Agents

API-Based Agents:

There was a wave of hype last year around API-based approaches (e.g., Baby AGI, API stores). But two key limitations stand out:

Compounding accuracy loss — a 90% accurate agent drops to just 60% after 5 sequential steps (90%^5).

Third-party dependency — execution hinges on external API availability and stability, which introduces fragility and scaling bottlenecks.

Computer-Using Agents:

More scalable by design. These agents interact with software through the interface itself—no custom APIs needed. In the AI arms race, the first to scale this method and generate network effects will take the lead.

It’s a bit like web scraping—but far more reliable and accurate, likely because they’re trained on real human-computer interaction data.

▶️ Computer-Using Agents vs. RPA

Unlike traditional RPA (Robotic Process Automation), which requires manual scripting, AI agents can handle complex, unstructured tasks with minimal user input. They apply human-like reasoning and adapt on the fly.

We may be on the verge of a true shift in Human-Computer Interaction—where agents don’t just automate, they collaborate.
