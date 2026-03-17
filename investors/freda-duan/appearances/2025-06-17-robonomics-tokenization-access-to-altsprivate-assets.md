---
investor: freda-duan
date: 2025-06-17
source: Robonomics
type: substack
url: https://robonomics.substack.com/p/tokenization-alts
companies: [HOOD, SCHW, OPENAI, SPACEX, NVDA, BLK, HLNE, SECURITIZE, ANCHORAGE]
topics: [retail-alts-access, tokenized-alternative-assets, tokenized-private-shares, tokenization-regulation]
companies_detail:
  - ticker: HOOD
    focus: secondary
  - ticker: SCHW
    focus: secondary
  - ticker: OPENAI
    focus: mention
  - ticker: SPACEX
    focus: mention
  - ticker: NVDA
    focus: mention
  - ticker: BLK
    focus: secondary
  - ticker: HLNE
    focus: secondary
  - ticker: SECURITIZE
    focus: secondary
  - ticker: ANCHORAGE
    focus: secondary
topics_detail:
  - topic: retail-alts-access
    focus: primary
  - topic: tokenized-alternative-assets
    focus: secondary
  - topic: tokenized-private-shares
    focus: secondary
  - topic: tokenization-regulation
    focus: secondary
source_length: 1718
fetch_method: substack_api
fetch_id: tokenization-alts
---

# Robonomics — June 17, 2025

Been thinking about the real play of tokenization. I see it as giving retail access to alts— and thus a threat to legacy wealth platforms.

In the U.S.:

Public equity = ~$50T

  • 60%+ of adults say they own stocks

  • 40% of total U.S. equity market cap is held directly by households

Alts = ~$11T

  • Alts are just 5% of advisor-client portfolios (vs. 25% for institutions)

[IMAGE: chart/figure]

Public markets have shrunk. In 1996, there were 7,300 public companies. Today? 4,300. Meanwhile, PE-backed companies have grown 5x in 20 years.

From July 2020 to June 2021: Private offerings raised $3.3T vs. IPOs raised just $317B.

Nearly 90% of U.S. companies with >$100M revenue are private. Companies are also staying private longer — median IPO age went from 6 years (1980) to 11 (2021).

Despite this growth, private markets remain off-limits to most retail — largely due to the “accredited investor” rule: Net worth >$1M (excluding home) or Income >$200K/yr for 2 years. Only ~18.5% of U.S. households qualify.

To me, it’s inevitable that the 5% alts penetration will go up. The only question is how fast, when, and how.

Traditional (off-chain) players are inching forward. launched SAIS (Schwab Alternative Investments Select) in April 2025 — a curated shelf of PE, credit, hedge funds, and RE. For the first time, Schwab lets retail access illiquid alts directly. But only if you have >$5M in Schwab assets.

Many have asked: Why bother with tokenize? What can tokenization do that traditional platforms can’t? Esp. if SEC “loosens” their rules a little bit.

On paper, tokenization throws out all the buzzwords: Liquidity. Efficiency. Transparency. Fractionalization. Financial inclusion. 24/7 trading. Global reach.

But let’s be clear — tokenization doesn’t create a new asset class.

The same regulators still govern the underlying assets. The on-chain wrapper changes how we access them, not what they are.

So what’s the big deal?

Yes, it’s fair to ask:

– Is 24/7 trading really that important?

– Couldn’t the SEC just modernize traditional rails instead?

The reality is: 

Alts have been off-limits to retail for so long — gated behind accredited or QP status — that most people just stopped asking/ looking for it. It simply feels remote & only for the elites

The subs onboarding is tedious af (weeks + documents) - almost impossible to be complete without a human advisor (again, only for the rich). The buying process is painful. 

Alts lacks a real catalyst to really take off in the “real world”.

Tokenization changes that. Not by rewriting the laws. But by packaging alts in a way that finally makes sense to retail:

Fast onboarding

Lower minimums

Digital-native flows

Sometimes, all it takes to unlock demand is a selling point/ story & a better user experience.

If (still a big if) tokenization really takes off, here’s what my case study / investment documentation might look like a few years from now:

Industry tailwind: Rode the inevitable shift — alts penetration climbed from 5% to [_]% as access widened and demand finally met supply.

PMF via user experience: Nothing magical about tokenized assets themselves. But the experience? Night and day. What used to take a week of forms and wires got compressed into minutes inside a browser wallet. “Tokenized” sounded cool — and that was enough. Retail adoption ramped quickly [two years after 2025].

Smaller checks = wider reach: Tokenization cut back-office friction and cost. That brought minimum check sizes down — from millions to tens of thousands. Traditional wealth management is still bound by 3(c)(7) rules: max 2,000 qualified purchasers per fund. Keeping the ticket big helps avoid hitting that limit. But it also caps reach.

Off-chain: every new LP means forms, wires, statements, blue-sky filings.

On-chain: just a wallet + an API call.

[IMAGE: chart/figure]

(Bonus) Expanded eligibility under a friendlier administration: The SEC finally moved beyond wealth as a proxy for sophistication. “Accredited investor” got redefined to include anyone advised by a registered RIA or broker under Reg BI, or anyone who passed a standardized knowledge test.

Knowledge ≠ wealth. The rulebook caught up.

Adoption path:

Started with tokenized public equities (as a demo rail) → moved to alts.

Europe moved first → U.S. followed with regulatory clarity.

Everything snowballed from there.

Crazy? Maybe. But my case study’s already written lol.

Now just waiting for the disruptors to execute. :)

HOOD: How Tokenized Private Shares Work

What is it:

Robinhood’s new “stock tokens” are over-the-counter (OTC) derivative contracts issued on the Arbitrum blockchain. Each token is backed 1:1—Robinhood either holds or delta-hedges one real share for every token issued (source).

Key mechanics:

Holders get price exposure and dividends, but no voting rights (source).

Tokens cannot be withdrawn to external wallets. Robinhood is the sole counterparty for buys/sells.

The tokens cannot be redeemed for the underlying shares (source).

Pricing:

Reference prices come from the latest verified secondary-market valuations:

OpenAI: ≈ $469/share (Forge Global, June 30, 2025) → Robinhood acquired 2,309 tokens (source).

SpaceX: ≈ $225/share (Forge Global, June 30, 2025).

Token prices update only when Robinhood’s oracle ingests new secondary trades, tender offers, or funding rounds. Even with heavy demand, token prices remain static until new reference pricing emerges.

Regulatory structure:

The private companies (OpenAI, SpaceX) do not need to file a prospectus. Since Robinhood is the issuer—not the companies—no S-1 or prospectus is required unless the company itself is offering shares.

The issuer is Robinhood Europe. The product complies with EU rules under KID + MiFID.

Can This Work in the U.S.? EU vs. U.S.—What Tokenization Unlocks

Traditionally, buying private shares—whether in the EU or the U.S.—requires investors to qualify as a Qualified Purchaser (QP) or equivalent. Everyday retail investors are excluded unless they meet high income/net-worth thresholds (e.g. ~$8M for secondaries).

Tokenization changes that—at least in the EU.

EU:

Tokenized private shares (like OpenAI or SpaceX) can be offered directly to everyday investors. Thanks to PRIIPs and MiFID, Robinhood can issue 1:1 share-backed derivatives with a KID in place—no wealth or income barrier.

→ Tokenization = massive access unlock for EU retail.

U.S.:

Even with tokenization, access remains restricted. While private companies still don’t need to file an S-1, the tokens cannot be sold to retail investors. Until infrastructure exists to route trades through an SEC-registered exchange or SBS facility, only Eligible Contract Participants (ultra-HNWIs and institutions) can be offered the OTC product.

[IMAGE: chart/figure]

[IMAGE: chart/figure]

APPENDIX — Regulatory Framework — Digital Asset CLARITY Act; Market-Structure bill

Just like the GENIUS and STABLE Acts laid the foundation for stablecoins, it’s encouraging to see tokenization efforts progress with the Market Structure Bill and the CLARITY Act.

Think of CLARITY as the operator’s manual, and the Market Structure Bill as the political guardrails.

Clarity Act:

Replaces today’s regulation-by-enforcement with a dual-registration model: SEC for capital raises, CFTC for spot markets.

Sec. 201 clarifies that tokens sold under an investment contract are not securities once the underlying blockchain is “functional & mature.”

Paves a two-step path: raise under SEC rules → graduate to CFTC oversight. Provides safe harbor for open-source developers and self-custody.

Market Structure Bill:

Enshrines a split-regulator regime, self-custody rights, and DeFi carveouts.

Would bring clarity to token classification, give legal certainty to exchanges, and likely re-rate U.S. token liquidity.

[IMAGE: chart/figure]

But here’s the key nuance:

Tokenized equities or funds remain securities. Putting NVDA, SpaceX, or a hedge fund on-chain doesn’t change their legal nature. Issuance and secondary trading still follow SEC rules—disclosure, lockups, liability remain intact. The benefit is modernized plumbing: on-chain records, SEC digital ATS rules.

Only native/network tokens can “flip” to digital commodities. After an SEC-registered raise and successful maturity certification, oversight shifts to the CFTC. These tokens can then trade freely on crypto exchanges or DeFi pools without triggering “unregistered security” concerns.

Bottom line:

Tokenized NVDA / SpaceX / hedge funds → stay under SEC jurisdiction (primary + secondary, ATS-based).

Native/network tokens post-CLARITY → graduate to CFTC regime (spot trading, DeFi, centralized crypto exchanges).

[IMAGE: chart/figure]

Europe doesn’t look too different vs. the US on this regulatory framework

The SEC analogue in Europe is a two-tier system: ESMA writes the technical rules and coordinates, but your day-to-day licence comes from the relevant NCA.

There is no CFTC-style, pan-EU commodities watchdog; commodity derivatives sit inside the same MiFID venue framework, and physical-spot markets remain largely outside financial regulation.

Whether in the U.S. or the EU, a tokenised hedge-fund interest, NVDA share or SpaceX private share stays a security—the wrapper doesn’t change its legal nature. All the usual prospectus, custody and market-abuse rules apply; the only “crypto-specific” twist in the EU is that you can test on-chain settlement under the DLT-Pilot sandbox, while in the U.S. you list on an SEC-regulated ATS.

APPENDIX — A snapshot of tokenized alts in the U.S. today

1/ Same eligibility, smaller checks.

Tokenization doesn’t lower the regulatory bar — you still need to be accredited or a qualified purchaser for most PE/credit funds.

But it does meaningfully shrink the minimum investment: from millions down to tens of thousands.

Eligibility is a legal issue, not a tech one.

 Sponsors choose an exemption (e.g., 3(c)(1) or 3(c)(7)), and the law sets the wealth bar — tokenization doesn’t change that.

Minimums are dropping fast.

 Example: Securitize cut a Hamilton Lane private-credit fund minimum from $2M to $10K, with fully digital onboarding and KYC.

No shortcuts on compliance.

 Tokenization doesn’t weaken legal tests — it just automates them. Platforms like Securitize and Anchorage handle KYC/AML and wallet whitelisting at sign-up, making the process instant and API-driven.

2/ Process is night-and-day.

What used to be a week of back-and-forth — subscription docs, wire transfers, email confirmations — now takes minutes inside a browser wallet.

Redemptions settle to the same wallet in stablecoins or new fund tokens.

3/ Operational alpha is real.

Managers like Hamilton Lane and BlackRock aren’t just chasing buzz — they see real savings and broader reach.

Smart contracts replace 3–4 legacy vendors

Capital flows go from multi-week to same-day

Administrative costs drop by ~50%

This is why large PE firms are already launching tokenized evergreen feeders — even before any regulatory changes to investor eligibility. As SEC custody rules evolve and custodians support wallet infrastructure, expect this momentum to accelerate.

[IMAGE: chart/figure]

APPENDIX — Main Street vs. the Qualified Purchasers (“QP”)

[IMAGE: chart/figure]
