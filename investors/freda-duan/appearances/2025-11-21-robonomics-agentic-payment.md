---
investor: freda-duan
date: 2025-11-21
source: Robonomics
type: substack
url: https://robonomics.substack.com/p/agentic-payment
companies: [OPENAI, STRIPE, SHOP, PYPL, AAPL, ADYEN, CHECKOUT, V, MA, AFRM, KLARNA, AMZN, PERPLEXITY, SKIMS, SQ]
topics: [agentic-commerce, payments, checkout, platform-economics]
companies_detail:
  - ticker: OPENAI
    focus: primary
  - ticker: STRIPE
    focus: primary
  - ticker: SHOP
    focus: primary
  - ticker: PYPL
    focus: mention
  - ticker: AAPL
    focus: mention
  - ticker: ADYEN
    focus: mention
  - ticker: CHECKOUT
    focus: mention
  - ticker: V
    focus: mention
  - ticker: MA
    focus: mention
  - ticker: AFRM
    focus: mention
  - ticker: KLARNA
    focus: mention
  - ticker: AMZN
    focus: mention
  - ticker: PERPLEXITY
    focus: mention
  - ticker: SKIMS
    focus: mention
  - ticker: SQ
    focus: mention
topics_detail:
  - topic: agentic-commerce
    focus: primary
  - topic: payments
    focus: secondary
  - topic: checkout
    focus: secondary
  - topic: platform-economics
    focus: secondary
source_length: 437
fetch_method: substack_api
fetch_id: agentic-payment
---

# Robonomics — November 21, 2025

Some thoughts (more open questions) on agentic payments:

1/ What’s the value prop of payment buttons in an agentic world?

Today, buttons like Shop Pay, Apple Pay, PayPal, etc. win on convenience. They store my card, billing, and shipping info. But in an agentic world, GPT becomes my wallet. It already knows all my details. And agents can type everything in instantly. So the convenience premium shrinks. That should reduce the pricing power of “button” payments.

Current pricing examples:

Standard online card rails (Stripe/Adyen): ~2.9% + $0.30

 Checkout: ~3.49% + $0.49

 is more expensive on both the % fee and fixed fee. In an agentic world, paying extra for “one-click” feels harder to justify.

2/ If agentic commerce succeeds, payment methods probably consolidate

A typical merchant now shows 4-6 checkout methods. If I add those use, you get: Visa/Mastercard, ACH, PayPal, Google Pay, Apple Pay, Klarna, Affirm, Afterpay, Venmo, Amazon Pay, Shop Pay, etc.

I don’t see GPT offering 10+ methods inside its agentic checkout UI. There simply isn’t enough space. This gives OpenAI leverage over which rails survive.

[IMAGE: chart/figure]

3/ If I choose Link inside GPT, which method does the merchant receive?

In Shopify’s case I’d assume the transaction routes through Shopify Payments. If true, all the other methods (Apple Pay, Klarna, etc.) that the merchant used to offer lose volume. This is a big shift: the agent chooses the path, not the user.

4/ Link is underrated. It might be event a threat to its own customers in the long-term

Link already has 200M+ saved shopper profiles. It’s embedded across hundreds of thousands of Stripe merchants (Stripe now markets this as “1M+ businesses”).

In Shopify’s setup today:

Link can pass the credentials to Shopify Payments.

Shopify Payments then processes the transaction.

Shop Pay is Shopify’s own “button,” but Link can sit upstream of it.

This raises a question: if my credentials live in Link, why would I also need to use Shopify Payments? At some point Link becomes “enough”?

Step 1 of agentic commerce: humans still choose the method.

Step 2: agents pick autonomously. That further weakens the value of branded payment buttons and pushes the ecosystem toward consolidation.

User experience on ChatGPT <> Shopify agentic commerce

Smooth flow. GPT can pick size and style (vs Perplexity Buy with Pro doesn’t offer any choices today).

No shopping bag yet. You can only buy one item at a time.

Recommendations feel clean. GPT didn’t push Skims when I asked for generic “comfy pajamas.”

Skims shows up on my credit card bill (vs. Perplexity Buy with Pro has Perplexity as the merchant of record)

[IMAGE: chart/figure]
