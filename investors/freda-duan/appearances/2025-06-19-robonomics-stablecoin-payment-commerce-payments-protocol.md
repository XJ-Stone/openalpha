---
investor: freda-duan
date: 2025-06-19
source: Robonomics
type: substack
url: https://robonomics.substack.com/p/commerce-payments-protocol
companies: [COIN, SHOP, STRIPE, V, MA, PYPL, AMZN, WMT, EXPE, MOONPAY, CIRCLE]
topics: [payments, stablecoin-rails, merchant-incentives, cross-border-payments]
companies_detail:
  - ticker: COIN
    focus: primary
  - ticker: SHOP
    focus: secondary
  - ticker: STRIPE
    focus: secondary
  - ticker: V
    focus: secondary
  - ticker: MA
    focus: secondary
  - ticker: PYPL
    focus: mention
  - ticker: AMZN
    focus: mention
  - ticker: WMT
    focus: mention
  - ticker: EXPE
    focus: mention
  - ticker: MOONPAY
    focus: mention
  - ticker: CIRCLE
    focus: mention
topics_detail:
  - topic: payments
    focus: primary
  - topic: stablecoin-rails
    focus: secondary
  - topic: merchant-incentives
    focus: secondary
  - topic: cross-border-payments
    focus: secondary
source_length: 1609
fetch_method: substack_api
fetch_id: commerce-payments-protocol
---

# Robonomics — June 19, 2025

We’re watching crypto and fintech collide—there are lots of debates around whether stablecoins can truly dent the dominance of card networks.

Fintech camp says: no chance.

Credit cards are sticky. Perks are too good for consumers to switch.

Merchants always flirt with cheaper rails. Debit, ACH, RTP—they’ve all existed. None replaced credit.

Crypto rails have existed via Stripe, Shopify, etc. for years—yet traction is near zero.

For most C2B retail payments in developed markets, stablecoins are a “solution looking for a problem.”

Any traction will take years, and likely be limited to cross-border or unstable-currency markets.

Crypto camp says: LFG

Cheaper. Faster. Programmable.

V/MA are dead. Take rates compress. Everyone wins—except the incumbents.

Meanwhile, in the real world:

WSJ reports Amazon, Walmart, Expedia, and airlines are exploring issuing their own stablecoins

Stripe x Shopify just launched stablecoin payments

Visa, Mastercard, PayPal are making moves too

All while stablecoin legislation inches forward in Congress

First principles: what does a retail payment rail need to work?

Instant “yes/no” authorization — so the merchant knows immediately whether to ship. 

Irrevocable or network-guaranteed funds — once approved, the payment is either final or the network guarantees it. Even if the shopper later disputes the charge, the network resolves it internally; the merchant doesn’t risk a clawback.

A liability-shift framework — to protect the shopper. Under Reg Z and Visa/MC rules, the issuer refunds the cardholder first and only then seeks repayment from the merchant if needed. 

Ubiquitous tooling and a strong economic loop — one-button integration, seamless APIs, and enough margin to keep banks, PSPs, and merchants engaged.

[IMAGE: chart/figure]

Why didn’t other payment rails break through?

ACH was never an option:

❌ No instant authorization (fails #1)

❌ No guaranteed funds (fails #2) – Credits can be recalled; debits can be reversed up to 60 days if marked “unauthorized.” Merchants who already shipped can lose the money.

RTP had promise but never took off:

❌ No liability shift (fails #3) - No fraud protection – Get tricked? The loss is yours. Banks may “try to help,” but they’re not liable.

❌ Poor UX/tooling (fails #4) – Consumers are used to cards that autofill. RTP’s “push” model (scan a QR, approve) feels clunky.

But i think the real issue was No economics. A few cents per payment won’t fund rewards or fraud ops. So banks bury RTP deep inside bill pay.

Now comes stablecoin. On paper, it’s no better than RTP—it lacks 2/, 3/, 4/. So why might it win?

One word: incentives.

Every $100 of stablecoins issued can earn ~$5/year in yield (via T-bills). That’s new economic fuel.

Issuers can share that yield with PSPs, merchants, and even fund buyer protection.

That’s a real engine.

The missed revenue under card rails is enormous:

Total U.S. card volume: ~$12T annually

$5T debit (avg. 0.8%)

$7T credit (avg. 2.3%)

Gross fees: ~$200B

Rewards back to consumers: ~$50–100B (points, cashback, miles). 

Likely, much of it goes unused

To calculate the total $ of yields stablecoins enjoy, one needs to consider the amount of time (4x for card economy on avg.) money flows through the system (bc stablecoins yield are only based on $ issued). → but even with that discount, we are talking about tens of billions of incentives to share with the ecosystem.

The rest of crypto’s appeal is real, but secondary:

Global by default

Programmable payments

Composability + wallet-native UX

Missing features? All of those can be fixed / layered on:

Push vs. pull? Push is native, but "pull" can be mimicked via wallet allowances

Fraud & liability? Not native, but buildable—via escrow, insurance pools, dispute layers

“I want card rewards” → What if the item is 3% cheaper instead?

Consumer wallets? Merchant tools? Yes—still friction points. But solvable.

So why is this time different?

🔴 Clear incentives + 🔴 Regulatory clarity

The technical readiness has always been there.

Sometimes disruption needs a breakthrough technology.

Other times, all it takes is decent tech—plus the right incentives and regulatory greenlight.

Imagine a world where you can either:

Get 1–2% cashback

or

Just pay 2–3% less

Both are frictionless. Which do you choose?

It’s kind of wild how far we’ve come: Base’s Commerce Payments Protocol addresses nearly every major pain point that’s kept crypto out of mainstream commerce. This isn’t theory—it’s live, open-source, and real money is flowing.

Let’s break it down.

[IMAGE: chart/figure]

1/ Instant “yes/no” authorization

Merchants need to know: should I ship this item?

On-chain, that’s trivial. The protocol gives an immediate Authorized response by calling authorize(), which either succeeds or reverts. No polling. No ambiguity.

2/ Irrevocable or network-guaranteed funds

This is where the protocol shines most clearly compared to card networks. With traditional cards, “authorization” simply places a hold on credit—it’s a promise, not a payment. But in Base’s USDC rail, the authorize() call immediately moves the full transaction amount into an escrow smart contract. These funds are held securely and can only be released through a capture, refund, or void path defined by the protocol itself.

This replaces the concept of a “credit hold” with something more akin to a “debit hold”—the buyer’s balance is reduced instantly, yet the funds remain locked until the merchant captures them.

If a buyer lacks sufficient funds, the transferWithAuthorization call will revert with a standard ERC-20 error (transfer amount exceeds balance), causing the entire transaction to fail upfront. It’s equivalent to card error code 51: insufficient funds or credit limit.

[IMAGE: chart/figure]

3/ Shopper protection, restructured

Unlike cards—where issuers bear statutory obligations to protect buyers—crypto-native payments shift consumer protections to the PSP or wallet layer.

The Base Commerce Protocol supports refunds via refund() calls, which can be executed using either the merchant’s wallet balance or, when that’s unavailable, the PSP’s own risk reserves.

The result is a system where consumer protection still exists, but it is no longer a matter of regulation—it becomes contractual and reputation-driven.

For example:

On day 0, the buyer pays, and funds move into merchant escrow.

By day 10, if the product fails to arrive, the buyer disputes. The PSP calls refund() and retrieves the funds from the merchant’s balance—dispute closed.

By day 65, if the merchant has disappeared and their balance is empty, the PSP may use its own risk fund.

By day 91, if the refund window has expired, on-chain refund is no longer possible. The PSP might offer an ex gratia credit, or the buyer may need to pursue resolution through Circle or legal avenues.

This model can’t replicate the statutory guarantees of traditional cards, but it provides meaningful recourse backed by smart contracts and financial incentives.

[IMAGE: chart/figure]

4/ Ubiquitous tooling and robust economic incentives

The final pillar of any successful payment rail is ecosystem maturity.

Base’s protocol supports modern, developer-friendly APIs and low-friction onboarding for merchants. The economics are sustainable: the rails are lean, yet they leave enough room for PSPs, wallets, and service providers to participate profitably.

One critical challenge remains: frictionless funding.

Today, stablecoin payments still require the buyer to source USDC, hold it in a wallet, and have ETH for gas. This user experience is far from optimal—but solvable.

A well-designed abstraction layer (whether built by Coinbase, Shopify, or an emerging fintech like MoonPay with its new stablecoin card) can bridge that final gap—bringing crypto rails to parity with cards not just on cost and finality, but also on ease of use.

[IMAGE: chart/figure]

What the ecosystem is building to remove those bumps

[IMAGE: chart/figure]

Unit economics + impact on various players - Shopify × Stripe × Coinbase USDC:

[IMAGE: chart/figure]

Status quo take rate source: Timothy Chiodo (UBS)’s excellent report on 

Gross take rate = same, with (up to) 0.5% cashback to merchants

Processing partner fees (i.e. Stripe) = assume same as card

Coinbase fee = 1%, but assume Shopify gets 50% discount

(https://www.coinbase.com/commerce)

Consumer rewards = 1% (per Tobi interview) — not considered “yield sharing” under the GENIUS Act

Cross-border (14% of SHOP merchants):

“All USDC payments convert to local currency, no FX or multi-currency fees”

(https://www.shopify.com/enterprise/blog/shopify-usdc-checkout)

If I’m understanding card rails correctly, cross-border merchants do pay extra for FX:

Example: U.S. card → USD checkout → Asian merchant paid in local currency. 

Network converts USD → SGD at wholesale rate + 1bp spread, which adds ≈1.25% in FX + assessment fees. Two business days later (T+2 for Visa, T+1 for Mastercard) the acquirer deposits, for example, SGD 135.20 into the merchant’s bank account, less its processing + FX fees. The cardholder’s statement still shows USD 100.00 because no currency changed on their side.

→ So stablecoin rails give real savings to cross-border merchants.

Net take rate / margin ends up similar for now - but over time, no reason gross take rate or fees wouldn’t compress?

I’m also surprised Stripe hasn’t pushed its own stablecoin rails post-Bridge.

For large merchants, issuing their own stablecoins/ switching to stablecoin rails feels like a no-brainer. 

With net margins often in the low single digits, cutting 1–2% in payment fees could boost profits by 50% or more.

[IMAGE: chart/figure]

[IMAGE: chart/figure]

This has challenged many of my prior assumptions about how payment rails work. I’m genuinely impressed by the ecosystem that’s come together—much of it built in just the past few months, following (or anticipating) regulatory clarity.

The Base Commerce Protocol offers a compelling preview of a new kind of payment architecture: transparent, programmable, and structurally more efficient than the legacy systems we’ve grown used to.

As wallet UX, credit overlays, and fiat onramps continue to improve, crypto for commerce may arrive much sooner than expected.

Never underestimate what an open-source, programmable system can unlock.

https://github.com/base/commerce-payments/blob/main/docs/Fees.md 

https://github.com/base/commerce-payments/blob/main/docs/README.md 

https://blog.base.dev/commerce-payments-protocol 

Coinbase <> SHOP interview:
