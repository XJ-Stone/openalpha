---
investor: freda-duan
date: 2025-10-09
source: Robonomics
type: substack
url: https://robonomics.substack.com/p/agentic-commerce-deep-dive-i
companies: [OPENAI, PERPLEXITY, ETSY, SHOP, STRIPE, META, GOOG, WMT]
sectors: [ai, e-commerce, payments, marketplaces, advertising, fintech, consumer-internet]
source_length: 1004
fetch_method: substack_api
fetch_id: agentic-commerce-deep-dive-i
---

# Robonomics — October 09, 2025

Before We Talk About Agentic Commerce…

Everyone’s eager to talk about the impact of agentic commerce — but honestly, we can’t have that conversation until we get the basics right.

What kind of commerce are we even talking about?

Why did Meta and Google fail?

Which version of the 3P model is most likely to win?

Why are OpenAI and Perplexity doing it in completely different ways?

And what does all this mean for the broader internet?

Let’s unpack.

Commerce comes in a LOT of different categories

3P e-commerce comes in a LOT of different shapes

Perplexity “Buy with Pro” vs. ChatGPT Agentic Commerce

Why Google / Meta Failed at Commerce

THE IMPLICATIONS of Agentic Commerce - WINNERS vs. LOSERS

1/ Commerce Isn’t One Thing

Before we talk about agentic commerce - define what kind of commerce first. I think Alex Rampell’s framework is a very good starting point — Impulse Buys, Routine Essentials, and Life Purchases are totally different beasts.

For agentic commerce, Lifestyle and Functional Purchases look like the most promising categories: both require research, opinions, and trust. Over time, agents may even get good enough to handle Impulse Buys for us.

According to GPT, the online TAM for these three categories alone is roughly $3 trillion.

That’s why it’s smart for GPT to start with Etsy (5.4 M sellers) and Shopify (~3 M merchants) — they’re filled with the kind of “consultative” purchases that fit this mold perfectly.

[IMAGE: chart/figure]

Source: a16z — AI × Commerce

2/ 3P E-Commerce Exists on a Spectrum

Most people talk about “third-party commerce” as if it’s one thing. It’s a SPECTRUM! and are the two opposite ends, everything else sits in the middle:

 Platform is the merchant of record (“MoR”); platform handles refunds, chargebacks, unified payment, and tax. Merchants do NOT own any of the customer relationships. 

 Merchant is the MoR; everything is handled by the merchant — they choose their own PSP, manage fulfillment, and process returns independently. Merchants own 100% of the customer relationships.

Everything else falls somewhere in between:

 / : Platform is the MoR (centralized payment); but for returns, buyers first contact sellers — if no response within 2–3 days, the platform steps in.

Taobao / : Merchant is the MoR; but platforms are highly hands-on — they provide escrow / collect-and-pay services, and mediate disputes. 

Why this matters: agentic commerce is, by nature, 3P e-commerce. 

Where these systems sit on the spectrum determines:

1️⃣ how successful the business can be;

2️⃣ how much control merchants retain over traffic/data (real impact on merchants);

3️⃣ how much disruption hits the payment stack (👋 Stripe).

[IMAGE: chart/figure]

3/ Perplexity “Buy with Pro” vs. ChatGPT Agentic Commerce

Surprise! The two are very different — in Perplexity “Buy with Pro,” Perplexity is the MoR (it shows up on your credit card bill), whereas ChatGPT made it clear that merchants remain the MoR.

OpenAI <> Stripe Agentic Commerce Protocol (“ACP”)

ACP is agnostic to who the PSP is — it works with any PSP and any agent.

Most people don’t appreciate this, but it’s a big deal that Etsy isn’t using Stripe for payment processing, yet can still participate in ACP.

Flow: OpenAI packages the payment credential in a shared token → Etsy receives the token and passes it to their PSP → Etsy’s PSP unwraps the token, retrieves the credential, and processes the payment.

For merchants, they pay the same payment processing fees + a take rate to OpenAI. It’s unclear how much (if at all) Stripe monetizes from ACP — but as history shows, widely adopted open standards (think Android) usually win.

Perplexity “Buy with Pro”

Perplexity acts as the MoR, while Walmart (the merchant) is just the fulfiller. That means Perplexity takes on much more responsibility than OpenAI does.

Flow: funds first go through Perplexity; Stripe (via Link) processes your card for Perplexity’s checkout; then Perplexity places the order with Walmart using Walmart’s PSP.

For merchants, ACP is better if you care about owning payments, tax, refunds, fraud, CRM, and first-party data — while still getting agentic distribution. For platforms, ChatGPT’s approach is far easier to scale, since it carries little to no liability.

Long story short — OpenAI’s agentic commerce passes my first test. This is the right approach, IMHO. I’d be very concerned if OpenAI ever decided to become the MoR…

[IMAGE: chart/figure]

[IMAGE: chart/figure]

[IMAGE: chart/figure]

[IMAGE: chart/figure]

[IMAGE: chart/figure]

https://openai.com/index/buy-it-in-chatgpt/ 

Recommend read: Simon Taylor’s https://www.fintechbrainfood.com/p/agentic-checkout 

4/ Why Google / Meta Failed at Commerce

Neither nor wanted to be the MoR, so they both let merchants handle it. but not being the MoR isn’t the reason 3P ecomm didn’t work (as we summarized above).

It’s fair to say both realized that ads are a far easier (and more profitable) business model than ecommerce — so they leaned harder into ads instead.

 commerce never took off. Today it is purely display ads, and have some basic functions for people to compare prices on the same item. 

[IMAGE: chart/figure]

 struggled big time trying to make in-app checkout work (even made it mandatory for merchants in 2023). As of Sept 2025, Shops on FB/IG now default back to website checkout (link-out) - Meta Commerce is officially dead.

Payment UX on was… a mess: 8+ steps, forced logins, endless redirects.

Meta Pay (formerly Facebook Pay) never reached adoption, and integrations with PayPal, Shop Pay, or Amazon Pay didn’t fix the friction.

Why do these case studies? Because I need to fully understand why past 3P e-commerce attempts failed — agentic or not. From everything I’m seeing, it’s a big deal that OpenAI partnered with Stripe to build the Agentic Commerce Protocol (ACP). Honestly, if or had done something similar, their e-commerce efforts might have ended up in a very different place…

Btw if anyone can fully explain why ‘s checkout failed — drinks on me!

5/ THE IMPLICATIONS of Agentic Commerce - WINNERS vs. LOSERS

Yawn, so tired… see Part II of the deep dive. Thanks for reading this far. ;)

Simon Taylor’s https://www.fintechbrainfood.com/p/agentic-checkout
