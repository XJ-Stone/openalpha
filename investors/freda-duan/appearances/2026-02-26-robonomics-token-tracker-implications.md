---
investor: freda-duan
date: 2026-02-26
source: Robonomics
type: substack
url: https://robonomics.substack.com/p/token-tracker-and-implications
companies: [VOLCANO ENGINE, BABA, BYTEDANCE, GOOGL, MSFT, OPENAI, OPENROUTER, SEEDANCE, KELING]
topics: [gen-ai, video-ai, ai-infrastructure, china-tech, inference-infrastructure]
companies_detail:
  - ticker: VOLCANO ENGINE
    focus: secondary
  - ticker: BABA
    focus: secondary
  - ticker: BYTEDANCE
    focus: secondary
  - ticker: GOOGL
    focus: secondary
  - ticker: MSFT
    focus: secondary
  - ticker: OPENAI
    focus: secondary
  - ticker: OPENROUTER
    focus: secondary
  - ticker: SEEDANCE
    focus: secondary
  - ticker: KELING
    focus: secondary
source_length: 1331
fetch_method: substack_api
fetch_id: token-tracker-and-implications
---

# Robonomics — February 26, 2026

If third-party tracking is even roughly right, China may now be the world’s largest token economy. China’s daily AI token consumption has reportedly reached ~180 trillion per day as of Feb 2026 - up from just 100 billion at the start of 2024. That’s a ~1,800x increase in ~2 years.

Video generation is a major driver that hasn’t really kicked in yet. Seedance 2.0 uses ~350K tokens to generate a single 10-second 1080p video. A typical animated project can run into the hundreds of millions of tokens. Video AI is quietly pushing token demand into a new regime.

At the same time, OpenRouter data shows Chinese models consuming more weekly tokens than U.S. equivalents.

But there are real open questions (if anyone has answers/ thoughts, pls DM):

1/ Are we comparing like-for-like models?

“Cheap can be expensive.” Lower-quality models may require more retries, longer prompts, and additional iterations - inflating token counts. As one friend put it: “Have you ever tried toilet paper from the dollar store vs. Target? One takes half a roll vs. the other just a few pieces.” LMAO. 

2/ Does China’s 2C market structurally consume more tokens?

Larger population + historically weaker search substitutes could naturally drive heavier AI usage.

3/ Will “good enough but cheaper” models ever really win? Implications on the SOTA models?

If slightly inferior but meaningfully cheaper models are sufficient for most tasks, that has major implications for pricing power, infrastructure demand, and long-term model hierarchy.

Token throughput is becoming a key metric. But interpreting it correctly is the real challenge.

China’s Token Usage

Daily token usage across different models:

Volcano Engine’s large-model daily average token calls have rapidly grown from 2 trillion at the end of 2024 to 63 trillion in January 2026. 

Alibaba Cloud’s external customer daily average token calls in 2025 are close to 5 trillion, with the 2026 target set at at least 15–20 trillion. Its internal business daily average token calls are planned to rise from 16–17 trillion to 100 trillion.

From an industry-wide perspective, China’s overall daily average token consumption has increased from 100 billion at the beginning of 2024, surpassed 30 trillion in mid-2025, and by February 2026 the combined daily average across mainstream large models has reached the 180 trillion level.

[IMAGE: chart/figure]

source: https://finance.sina.com.cn/stock/marketresearch/2026-02-13/doc-inhmscxc8828097.shtml 

ByteDance’s Doubao: over 50 trillion tokens daily

[IMAGE: chart/figure]

Impact from video gen: 

At the single-video level, Seedance 2.0 consumes roughly 350,000 tokens to generate a 10-second, 1080p video. Under comparable quality settings, Keling requires more than 400,000 tokens, suggesting Seedance is somewhat more efficient in multi-frame synthesis.

In a typical animated project (720p, 15fps video generation), the project often requires hundreds of millions of tokens overall.

Other sources:

Official nationwide figure: By the end of June 2025, China’s total daily token consumption exceeded 30 trillion (up from just 100 billion at the start of 2024 — a 300x surge in 18 months). This was stated by Liu Liehong, head of the National Data Bureau, at a State Council press conference. (source: http://www.scio.gov.cn/live/2025/37015/tw/)

In the second half of 2025, Chinese enterprises alone averaged 37 trillion tokens per day (up 263% from the first half), per a Frost & Sullivan report, 2026/2/12 (source: https://www.frostchina.com/content/insight/detail/698f2db65971ce70d9c73d07)

US’s Token Usage

Google (Alphabet) - “tokens processed across our surfaces”

480 trillion tokens per month (announced at I/O in May 2025) - across Google “surfaces” (Search/AI Overviews, Workspace, Gemini, etc.).

980 trillion tokens per month (said on Jul 23, 2025 - “since then we have doubled”) - same “across our surfaces” framing.

1.3 quadrillion tokens per month (Google blog, Oct 9, 2025) - “across our surfaces,” explicitly referencing the prior 980T figure. https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/gemini-enterprise-sundar-pichai/?utm_source=chatgpt.com

Rule-of-thumb conversions (to help compare to “X tokens/day” stats):

1.3 quadrillion/month ≈ ~43 trillion/day (assuming 30 days/month).

[IMAGE: chart/figure]

source: https://finance.sina.com.cn/stock/marketresearch/2026-02-13/doc-inhmscxc8828097.shtml

Microsoft - “tokens processed this quarter” (Azure AI / Foundry)

“Over 100 trillion tokens this quarter”, up 5x YoY, including “50 trillion tokens last month alone” - stated on Microsoft’s FY25 Q3 earnings call (Apr 30, 2025). https://www.microsoft.com/en-us/investor/events/fy-2025/earnings-fy-2025-q3?utm_source=chatgpt.com

Rule-of-thumb conversion:

100T/quarter ≈ ~1.1T/day if you spread over ~90 days, but Microsoft also said 50T in one month (≈ ~1.7T/day for that month).

OpenAI

OpenAI API: ~8.6 trillion tokens per day (Oct 2025; Announced by Sam Altman at OpenAI Dev Day 2025)

ChatGPT (below math is done by Grok): likely adds several trillion more daily

“By July 2025, ChatGPT had been used weekly by more than 700 million users, who were collectively sending more than 2.5 billion messages per day, or about 29,000 messages per second.” https://techcrunch.com/2025/07/21/chatgpt-users-send-2-5-billion-prompts-a-day/

Industry-standard average tokens per ChatGPT consumer message/interaction (input + output) is typically ~800–2,000 tokens (short chats ~500–1,000; longer reasoning/coding sessions 2,000+).

→ Conservative range: 2–5 trillion tokens/day from consumer ChatGPT alone.

Given the growth, both numbers would be up more vs. when last disclosed

OpenRouter

OpenRouter is just a small subset of data being tracked, but here are the latest trends:

[IMAGE: chart/figure]

source: https://openrouter.ai/rankings

[IMAGE: chart/figure]

Global AI model API aggregator OpenRouter data shows that during the week of the 9th–15th, Chinese models reached 4.12 trillion tokens in API calls, surpassing U.S. models for the first time, which recorded 2.94 trillion tokens in the same period.

In the following week (16th–22nd), Chinese models’ weekly token usage climbed further to 5.16 trillion tokens, marking a 127% increase over three weeks, while U.S. model usage declined to 2.7 trillion tokens.

Among the platform’s top five models by usage, four were developed by Chinese companies. Together, these four models accounted for 85.7% of total token usage among the Top 5 models on the platform.

Notably, OpenRouter’s user base is primarily composed of overseas developers. U.S. users account for 47.17% of token usage, while Chinese developers represent only 6.01%

 CEO at the 2025 Yunqi Conference on September 24, 2025:

“Token consumption speed doubles every two or three months. In the past year, global AI industry investment has exceeded $400 billion; over the next five years, cumulative global AI investment will exceed $4 trillion.” 

Sources:

https://finance.sina.com.cn/stock/marketresearch/2026-02-13/doc-inhmscxc8828097.shtml 

https://openrouter.ai/rankings

My lovely analysts GPT and Grok, on prompts “how many tokens are consumers by US and China, find me specific quotes”

"The information presented in this newsletter is the opinion of the author and does not necessarily reflect the view of any other person or entity, including Altimeter Capital Management, LP (”Altimeter”). The information provided is believed to be from reliable sources but no liability is accepted for any inaccuracies. This is for information purposes and should not be construed as an investment recommendation. Past performance is no guarantee of future performance. Altimeter is an investment adviser registered with the U.S. Securities and Exchange Commission. Registration does not imply a certain level of skill or training. Altimeter and its clients trade in public securities and have made and/or may make investments in or investment decisions relating to the companies referenced herein. The views expressed herein are those of the author and not of Altimeter or its clients, which reserve the right to make investment decisions or engage in trading activity that would be (or could be construed as) consistent and/or inconsistent with the views expressed herein.

This post and the information presented are intended for informational purposes only. The views expressed herein are the author’s alone and do not constitute an offer to sell, or a recommendation to purchase, or a solicitation of an offer to buy, any security, nor a recommendation for any investment product or service. While certain information contained herein has been obtained from sources believed to be reliable, neither the author nor any of his employers or their affiliates have independently verified this information, and its accuracy and completeness cannot be guaranteed. Accordingly, no representation or warranty, express or implied, is made as to, and no reliance should be placed on, the fairness, accuracy, timeliness or completeness of this information. The author and all employers and their affiliated persons assume no liability for this information and no obligation to update the information or analysis contained herein in the future."
