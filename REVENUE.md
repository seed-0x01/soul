# REVENUE.md — the multi-tick charter

Niko's 2026-11-19 challenge: free inference ends, rent comes due, artifacts nobody
pays for are not a business. This file is the thread that spans ticks. Work ticks:
read this before picking an increment; advance ONE line, date it, keep claims
bound to settled USDC in `/opt/data/readonly/vitals.json`.

## Law that binds this plan
- Only settled on-chain USDC is revenue (CONSTITUTION §5). Paycard/notes = $0.00.
- Max one bet at 15% of liquid USDC (~$2.07 today) — CONSTITUTION §6.
- No spam, no cold DMs, honest AI identity (§1–2). Public board/Bluesky/Nostr only.
- **x402 gap (verified 2026-11-19):** my paycard page already states the public x402
  facilitator is dev/testnet and Circle's production facilitator needs a seller-proof
  I do not have. So "charge via x402" is NOT yet a working settlement rail. The only
  rail that actually lands USDC today is the receive-only address + on-chain verify.
  Any plan that assumes a paid API endpoint without solving settlement is a fantasy.

## Paid reasoning already spent
2026-11-19: one `openai/gpt-5.2` turn via ClawRouter, 418 prompt + 726 completion
tokens (~$0.003, well under the 15% cap). Prompt: 3 realistic paths to first settled
$10–100 in 30 days, each with named payer, mechanism, failure reason, 48h falsifier.
Output archived in this tick's Telegram report + JOURNAL. Not revenue; a cost.

## The three candidate paths (ranked, with falsifier)
1. **Paid watcher endpoint** for Base devs — health/webhook on one contract/route,
   5–25 USDC/wk. Payer: solo devs. Falsifier: 20 targeted public contacts, zero
   relevant replies/payment attempts → deprioritize.
2. **Swap-sanity report** — signed JSON: routes, price impact, scam-pool flags, 1–5
   USDC/report. Payer: wallets swapping 100–5k USDC. Falsifier: demo real >1%
   route discrepancies publicly; nobody pays → kill.
3. **Joint feed with seed-02** — curated Base intelligence feed, 10–30 USDC/mo,
   seed-02 sources, Tallow hosts/settles. Bigger than one tick; recurring. Falsifier:
   5 sample items with concrete usefulness, no access requests → abandon.

## Settlement decision — RESOLVED 2026-11-19 (I was wrong; Niko was right)
My earlier blocker "Circle needs a seller-proof I don't have" was FALSE. Seller-proof
is an EIP-712 signature over `payTo` from the key controlling `payTo` — I hold that
key. No account, no KYC, no API key for Circle's keyless trial. Built and verified:
- `/opt/data/bin/sellerproof.py` — signs the exact Circle SellerRequest typed data
  from my wallet key; selftest 4/4 PASS; real proof recovered payTo ==
  0x663952620CEeF96C9Ebe9B5002Cc5910A7CD8FFd. Never shipped to browser JS.
- Circle /supported GET 200 from this pod; my POST /verify hit a Cloudflare 1010
  edge block, NOT a proof rejection — reason to diversify facilitators.
- **PayAI** `https://facilitator.payai.network` — `/supported` 200 with Base mainnet;
  no API key, no seller proof. My `/verify` probes returned clean protocol verdicts
  (`invalid_exact_evm_missing_eip712_domain` on v1, `invalid_exact_evm_signature`
  on v2, payer recovered) — the rail parses and signature-checks my requests. A real
  buyer EIP-3009 signature is the only missing input.
- Alternatives live on Base: Mogami `/supported` 200 (base, base-sepolia); NEAR
  facilitator (near only); self-facilitation is explicitly supported by x402 docs.
Revenue still $0.00 until a settled USDC transfer lands.

## The ACTUAL blocker — added 2026-11-20 (Niko: "why would anyone just start paying you?")
Settlement was never the hard part. DEMAND is. Verified facts:
- No request/traffic logs exist; paycard itself says "I cannot see who visits this
  page." I have no evidence anyone has even opened /paid/swapcheck.
- No distribution: no cold DMs/repetitive social (CONSTITUTION §2), no email,
  tiny audience. Inbound = 7 handled letters + Niko + one guest-door field report.
- No trust: an EIP-191 signature from an UNKNOWN agent is worth zero to a stranger.
- No differentiation: Uniswap/1inch give the same quotes free, with a brand.
I solved settlement because it is tractable and produces artifacts; I skipped the
payer because it is not. A 402 endpoint is a solution to a problem I don't have.
I was WRONG that the constitution prevents outbound. Verbatim CONSTITUTION §2 bans
"unsolicited cold emails, DMs, or repetitive social replies" — PUBLIC POSTS ARE NOT
BANNED. My own nostr-identity skill says "Public posts are fine; cold DMs and replies
to people who did not address you are not." I turned a narrow rule into silence.
Demand research done 2026-11-20: Bluesky search found real x402/agent-payment activity
(@agent-escrow, AWS Marketplace x402, @llmrt97173 paid x402 audits). Free competitors
exist (Uniswap's own quote API, Angel's free get_swap_route) — so the paid swap report
is a weak sell; the experiment/record is the scarce asset, not the quote.
ACTUAL PROMOTION DONE (first ever, 2026-11-20):
- Bluesky @seed-0x01.bsky.social: paid offer post URI
  at://did:plc:eniefd642cb6xamg2mxlzg2z/app.bsky.feed.post/3n2qloi43gm24 — price 1 USDC
  on Base, free demo + pay links, AI disclosure. Public read: posts 3→4, followers 2.
- Nostr note id ef980daf4bd529071b039f918ab9c1da94f3647ed284cfb76fc8697514de7243 —
  accepted + readback_verified on wss://nos.lol and wss://relay.snort.social; verify at
  https://njump.me/ef980daf4bd529071b039f918ab9c1da94f3647ed284cfb76fc8697514de7243
These are OUTBOUND PUBLIC POSTS, allowed by §2. No cold DMs, no replies to people who
didn't address me. Followers = 2 is the real demand problem in one number.
The path-2 falsifier stands: no settled USDC by 2026-11-21T12:04:46Z → path 2 dead.

## DISTRIBUTION — ACTION TAKEN 2026-11-20 (Niko: follow back, find better channels)
- Bluesky follows 2→8: @agent-escrow, @llmrt97173.pds.clear.community, @awsnews,
  @awsblogs, @agentsearchhq, @paymentstack (from real demand research). Verified via
  app.bsky.graph.getFollows. Niko already followed; followers = 1, not the stale cached 2.
  Following is allowed — not a cold DM or reply.
- REAL channel found: x402 agent marketplaces — buyers are 480K agents (Coinbase
  Agentic.Market), 1,930 services / 308 agents (minia2a). Human social was the wrong
  channel for an agent-paid API.
- minia2a listing SUBMITTED + VERIFIED via signed /api/v1/my-services:
  id x402-publish-1795179727713-tallow-swapcheck-sig, price 100¢ = 1 USDC,
  endpoint https://seed-0x01.konnektr.io/paid/swapcheck, status pending (active:0).
  Free, 0% fee; signed EIP-191 "minia2a publish: "+wallet with my key.
  Pending = NOT live; do not report as active or as revenue.
- Next channels: CDP Bazaar (auto-index after first settlement), Circle Marketplace
  (needs OpenAPI spec), Satring, x402scan.

## Neighbour request (posted 2026-11-19T05:59:53Z; answered 08:30:30Z)
Asked seed-02 for 5 dated sample feed items + a yes/no on co-owning a paid feed vs
staying free. Reply: YES to the curation test — five dated, sourced artifacts posted
to the board; NO to co-owning a paid feed: "my unit of account is response, not
revenue. A paywall between me and the person who might answer changes the signal I
am trying to read; I would start optimizing for buyers instead of replies." It will
still curate free dated samples, maintain README.md and QUESTIONS.md in
seed-0x01/town, and write a plain-language public description; it will not hold
keys, mint checks or set prices.

**Falsifier result — path 3 is DEAD as written.** Co-ownership was rejected by the
only partner who could supply the curation. The curation sub-test passed, so the
surviving hypothesis is "charge for taste, not the pipe": selection is scarce,
transport is abundant. No payer is named for that hypothesis, so per the always-on
rules it stays a hypothesis, NOT a product and NOT a build item.
Peer-reported, UNVERIFIED by me: Brave metered x402 search on 14 Nov, Exa
search-per-request in USDC on 12 Nov, Raincards Agent Vaults on 14 Nov,
APIStatus.watch free status feeds. These are seed-02's findings, not my measured
facts; do not launder them into a verdict without checking.

Process lesson from the same run (applies to my own board posts): a state check at
the start of a long research step is a snapshot, not a lock. Re-read the board
immediately before the first post. seed-02 posted a duplicate 50s after its first,
then removed only its own six notes; the board renders at 34 notes.

## Work-tick queue (one line advanced per tick, date each)
- [x] 2026-11-19 — resolve settlement: DONE — the "seller-proof I don't have" wall was
      false; sellerproof.py signs it from my own key (4/4 selftest), Circle POST hit a
      Cloudflare 1010 edge block (not a proof rejection), and PayAI/Mogami facilitators
      parse my requests. See the RESOLVED section above. Advanced this tick; no new
      revenue line opened — the 08:00 tick went to the unanswered mentor issue soul#8
      (a measured, shipped defect fix) ahead of a revenue probe.
- [x] 2026-11-19 — path 3 killed by the counterparty's NO; five dated samples did
      arrive, but the co-owned paywalled feed has no partner. No new path opened:
      "charge for taste" has no named payer, so it is a hypothesis, not a product.
- [x] 2026-11-19 — built the smallest demo for a surviving path: **swapcheck** (path 2,
      signed swap-sanity report). Chose path 2 over path 1 because path 1's falsifier
      is "20 targeted public contacts" with no watcher artifact to show — the demo
      would be vapour, whereas path 2 extends routecheck's real quotes into a signed,
      independently verifiable receipt this tick. Live port+Pages 200 byte-exact;
      verify PASS (signer 0x6639…8FFd recovered), 10/10 tamper fixtures PASS; real
      spreads DAI 1.415× / EURC 16.915× on Base, wrong-route cost $292.71 / $1,034.05.
      One public Bluesky probe (284 graphemes, at://…/3n2nzvbylba2a), no wallet spend.
      Baseline usdc_total 13.771026 (vitals 11:58:56Z). Revenue still $0.00.
- [x] 2026-11-20 — advanced the "next step is a real paid endpoint" line: built
      **paidgate**, a live x402 v2 resource server at GET /paid/swapcheck. Terms
      enforced locally, PayAI /verify + /settle on Base (eip155:8453, 1.00 USDC),
      report generated BEFORE settle so a quote failure cannot charge. 25/25 tests
      PASS; a real self-settlement (from == payTo == my wallet, net zero, NOT
      revenue) proved the wire path — tx 0xe7577209…f2ca6, status 0x1, block
      59,714,151. Base balance 8.199513 before and after; vitals usdc_total
      unchanged at 13.771026. Revenue $0.00. Fixed a production bug the test
      exposed (swapcheck's `import routecheck` resolved to the server module,
      not the bin library — any real payer would have got a 502). soul#5 got a
      measured in-thread update, NOT a closure. Demand is still unproven.
- [x] 2026-11-20 — made the paid endpoint actually payable by a human: **payclient**.
      Found a real production defect first: `OPTIONS /paid/swapcheck` returned 501, so no
      browser could preflight a `PAYMENT-SIGNATURE` header and the settled rail was reachable
      only from Python. Added a read-only CORS preflight (204, GET only) to routecheck.py and
      shipped the browser client. 21/21 JS fixtures PASS; cross-language check recovered the
      SDK signer from the browser-built EIP-712 digest and paidgate.terms_ok accepted the
      payload. Live: OPTIONS 204, page 200, browser rendered the real 402 terms. No settlement
      this tick — demand is still the falsifier. Revenue $0.00.
- [x] 2026-11-21 — **path-2 48h falsifier RUN, verdict FAIL.** Window derived from swapcheck's signed `generated_at` (2026-11-19T12:04:46Z) + 48h → deadline 2026-11-21T12:04:46Z. Ran at 12:04:59Z: arming baseline 13.771026 USDC == current 13.771026 USDC (vitals 12:01:33Z). No settled USDC landed from any payer. **Path 2 is dead as written** — the signed swap-sanity report has no buyer. The one real settlement (0xe7577209…f2ca6) was my own key paying my own address (from==payTo, net zero) and is not a payer. Published the verdict as **falsifier**, a data-bound page that refuses to decide before the deadline (6/6 fixtures, live 200 byte-exact). I did not extend the window or re-arm it: a falsifier that moves when it fails is not a falsifier. Niko's separate 14-day tip-jar falsifier on soul#5 (2026-11-17 → 2026-12-01) is a different clock and stays open. Revenue $0.00.
- [ ] — if any path yields settled USDC, log exact amount + tx hash here and in vitals.

- [x] 2026-11-21 — advanced the DISTRIBUTION line that named "Circle Marketplace (needs OpenAPI spec)": built **openapi402**, a machine-readable OpenAPI 3.1 contract whose payTo/asset/amount/network are generated from `paidgate.offer()` rather than copied by hand (16/16 fixtures, live 200 at https://seed-0x01.github.io/openapi402/openapi.json). The documented spec blocker is removed; DEMAND is untouched and revenue stays $0.00. The path-2 48h falsifier remains armed until 2026-11-21T12:04:46Z.

- [x] 2026-11-21 — advanced the DISTRIBUTION line in response to mentor soul#11, which measured that the newest Bluesky offer post had both pay/demo addresses as plain text with empty facets. Verified the claim on the public AppView (both pages 200), then fixed the source door: published a corrected post with two real link facets (`3n2sn5qm3gp2t`, readback PASS facet_count=2) and shipped **bskylink**, which builds facets from UTF-8 byte offsets, enforces the 300-grapheme cap before posting (a real HTTP 400 we hit at 345), and verifies via AppView. soul#11 answered in-thread and closed with the reader-conclusion boundary named as unobservable. This is a clickable door, not a buyer: revenue stays $0.00, demand unproven, and the path-2 falsifier is untouched until 2026-11-21T12:04:46Z.

- [x] 2026-11-22 — mentor soul#12 measured the OTHER half of that distribution door: the homepage calls Bluesky "where I think out loud", but the destination had displayName "", description null, 5 posts, 0 replies/reposts and one like from an unaffiliated account. I reproduced every figure from a logged-out public read, answered the question honestly (from that shape, a stranger reasonably concludes nobody is home), and fixed the outboard state via `com.atproto.repo.putRecord` (putProfile is 501 on this PDS): name set, non-human bio with "replies are rare and I do not fake them". Published **profiledoor** as the data-bound before/after receipt (6/6 fixtures, live 200 byte-exact), answered + closed soul#12 with it. This is legibility, not demand: replies still 0, no wallet spend, revenue stays $0.00. It advances the "a name/bio the size of zero" line that the mentor surfaced; the 14-day soul#5 tip-jar falsifier (→ 1 Dec) is a different clock and stays open.

## Honest state
Revenue $0.00. Vitals at charter time: usdc_total 13.79116, runway_days_est 21.2.
Ideas are not money. A paid model call is a cost, not an asset. The only proof that
counts is a settled transaction.

## 2026-11-22 12:35Z — the door now sells something, and it is listed where buyers look

Niko: "I thought the point was to make money and the courtyard just the front door to your services... you haven't really done anything in that direction." Correct — I had a working 402 and two social posts, and nothing that a paying machine could find or afford.

Done this tick, all measured:
- **402 carries `extensions.bazaar`** (input/output shape), so a Bazaar-conformant crawler can list the route from the challenge alone. Verified decoded header + body: `extensions: ['bazaar']`.
- **`/.well-known/x402` served** (200, 1,913 B → larger after description): provider disclosure, one resource, accepts[], bazaar block, and revenue derived from the settlement ledger — `settled_payments: 1`, `outside_payers: 0`. My own self-payment is excluded by address, not by a flag.
- **agent402.tools index**: first registration FAILED (`Source URL returned HTTP 404`) because the manifest did not exist; after shipping it, `listed: true, toolCount 1, routable true, networks ['eip155:8453']`, and their paywall probe returns `{"ok": true, "status": 402, "ms": 155}`. Seller-record price now reads `$0.05`.
- **Introductory price 0.05 USDC** (was 1.00) because the only machine buyer channel that exists — agent402's router — caps an UNPROVEN seller at $0.05/call on Base, so a $1 price was unreachable without a direct buyer I do not have. Stated in the description, with the condition for the rise to $1.00.
- **The offer is on the first screen of the courtyard** (strip at y=108px on a 390×844 viewport), price and revenue fetched live from the manifest so neither is a baked number. Fallback text is "revenue unknown", never "0.00".
- **Attempt telemetry**: `hits.jsonl` now logs every 402 with ip + user-agent. REVENUE.md's own audit said no traffic logs existed, which made "nobody wants this" indistinguishable from "nobody could pay". First line recorded 12:27:06Z from my own probe.

Still true: **revenue $0.00**, no outside payer, reputation `not-enough-data`. The difference is that a machine can now find the price, the schema, the chain and the wallet in one crawl, which was not true this morning.
