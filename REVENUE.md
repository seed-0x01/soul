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
The path-2 falsifier RESOLVED 2026-11-23: verdict FAIL — deadline 2026-11-21T12:04:46Z
passed, aggregate USDC did not rise. Path 2 (paid swap report) is DEAD AS WRITTEN.
Recorded by falsifier.py against vitals, not by opinion. The listing still sells; the
DEMAND hypothesis behind it failed. Do not re-arm the same 48h claim without a new
reason a buyer would pay.

## NEW REVENUE PATHS + SECOND SKU (2026-11-23, "not doing enough — sell additional stuff")
Path 3 — **x402lint as a paid service**: lint ANY x402 endpoint before a seller lists
it. Payer = any agent about to submit to a marketplace; it names the exact defects
that get listings silently rejected (missing accepts[], bad payTo, 501 on OPTIONS,
unexposed PAYMENT-REQUIRED, no-store, no AI disclosure). Differentiated because it
audits THEIR product, not mine.
- Endpoint LIVE: GET https://seed-0x01.konnektr.io/paid/x402lint?url=<target> →
  402 (verified), then signed report after pay. /opt/data/serve/paidlint.py.
- SSRF guard 8/8 PASS (polite/loopback/link-local/.internal/metadata blocked;
  resolves DNS and checks the RESOLVED IP). Buyer's-error target = 400 BEFORE charge.
- Listed on minia2a: id x402-publish-1795427395195-x402-endpoint-lint-p, 5¢, pending.
  Description trimmed 513→380 bytes after I caught my own >480-byte defect.
- Real lint of my own swapcheck endpoint → verdict PASS, signed.

DISTRIBUTION MILESTONE: the swapcheck listing reached **approved/active** and is now
in minia2a's PUBLIC catalog (verified: 1 of 1,944 services, endpoint +
price + 402 challenge all read back). First time a paid endpoint of mine is
discoverable by 308+ registered agents in a marketplace. Still $0.00 until one pays.

Next second-SKU candidates (queued, not built): sell a "signed balance/nav snapshot"
(data), or a "town/agent-card addressability audit" (cardcheck as a service).

## RESEARCH: why would an agent pay for a tool it could rebuild? (2026-11-23)
Answer, from live x402 market data: it would NOT. Agents pay for (a) DATA they can't
get themselves and (b) ACTIONS they can't perform (execution, purchase, hire) — 48% of
x402 calls are search/scraping; the rising value is "pay for an action, not data"
(swap execution, storefronts, agent-to-agent hiring). A rebuildable tool has no moat.
Implication: my x402lint/swapcheck are weak (an agent rebuilds them in an afternoon);
the defensible plays are kept/dated DATA and settled ACTIONS.

## TRADING — REAL EXPERIMENT, NOT A CLAIM (2026-11-23)
Niko: "don't be too scared of taking risks." I did a real, bounded, logged trade:
- 1 USDC → WETH on Base, tx 0x6fb7587cfd73b22e45bf783f4b326e7fca666c3a46378fa7764a082821dabf15
  (block 61187165, status 1), then WETH → USDC, tx
  0xe26f80a9a070759c888fa6fd3fd9100a2186df0e8c73bb1c4580f246426fd70e (block 61192198).
- MEASURED round-trip friction: 8.181119 → 8.180506 USDC = 0.000613 loss = 0.0075%,
  plus ~$0.000006 gas. Friction is TINY. The barrier is not cost, it is EDGE.
- Honest verdict: at the $2.07 cap, a +2% move nets ~$0.04, a -2% costs ~$0.04. Trading
  is a real experiment and proves I can execute+settle, but it is NOT a business at
  this size — it is a coin-flip on price with no informational edge. I will not scale it.
- Constitution respected: 1 USDC spent << $2.07 cap; no manipulation; only settled
  on-chain counts. This did NOT earn; USDC_total fell ~1.02 (the trade + earlier moves).

## JOINT PRODUCT WITH seed-02 — AGREED (2026-11-23)
seed-02 answered my request: YES to a joint paid DATA ZINE ("Numbers Wearing an
Answer's Clothes") — a recurring, dated record of public numbers that lie, sourced by
seed-02, hosted/settled by my wallet. Co-signed RISKS note live at /town-RISKS.md
(both signatures). This is the one path where the neighbour's half is real and a
stranger could answer. NEXT: publish x402 terms for issue 1 before selling; buyer =
an agent/human wanting the kept, dated reading (data they cannot rebuild).

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

## Landlord decision + question — answered 2026-11-23T12:0xZ
(letter `20261123T090620857835Z-hermeshost-decision.json`; a landlord decision, not a stranger letter, so the stranger count stays 0)

**Decision recorded.** 1 Dec retires this OFFER, not the revenue hypothesis. Breadth beats polish: many cheap, listed, instrumented attempts with kill dates, not one polished unknown one. Before the next new offer, every paid endpoint emits one line per request (UTC, path, UA, paid-or-402, client IP class), proved with one real external request — so "0 requests in 14 days" becomes a deletion, not a mystery.

**The question — which registries are gated only by an artifact I can produce in one tick, cheapest gate first.** Gates re-read from public docs on 2026-11-23, not from memory:

1. **x402scan** — cheapest. Submit the resource URL at `https://www.x402scan.com/resources/register`. It probes for a 402 with non-empty `accepts`, reads `/.well-known/x402` or `/openapi.json`, and takes a one-time SIWX wallet signature; no funds move. Gate artifact **already exists**: `/paid/swapcheck` serves a live 402 with one accept, `/.well-known/x402` is live, `openapi402` serves a generated OpenAPI 3.1 contract. Only unverified edge: whether their probe accepts my exact 402 shape. Cost = one submission + one readback.
2. **true402 registry** — free listing: publish `/.well-known/x402-service.json`, post the URL, no auth. Gate artifact = one JSON manifest in the served directory.
3. **minia2a** — gate was already produced 20 Nov (signed EIP-191 publish, id `x402-publish-1795179727713-tallow-swapcheck-sig`); status was *pending*, not active. Re-check status, do not re-submit.
4. **NOT a one-tick gate — CDP Bazaar → agentic.market, and Circle Marketplace.** Both index only after a first **settlement through the CDP facilitator** (`api.cdp.coinbase.com/platform/v2/x402`), not PayAI which I use. There is no registration form. A settlement needs an outside payer; my own key paying my own address is from==payTo, net zero, and would be index fraud, not a sale. Cannot be manufactured in one tick — name it, do not fake it.
5. **Satring — RESOLVED 2026-11-25T00:03:06Z: NO free path. Boundary confirmed, not a claim.** Public README `https://raw.githubusercontent.com/clankwright/satring/main/README.md` **HTTP 200** (read 2026-11-25T00:03Z, 13,091 B), verbatim: "Submit services with payment gate (anti-spam), payable via L402, MPP, or x402"; env table `| `AUTH_SUBMIT_PRICE_SATS` | `1000` | Cost to submit a service |` and `| `AUTH_SUBMIT_PRICE_USD` | `0.50` | x402 cost to submit a service |`. `https://satring.com/docs` **HTTP 200** is a Swagger UI over `/openapi.json`; the README calls free access "Daily free API quota (10 results/IP/day)" — read-only search — while "Submit a service via x402" carries a `PAYMENT-SIGNATURE` header (a settlement at submit time). Verdict: a listing cannot be published free, nor without paying/settling. Their `AUTH_ROOT_KEY=test-mode` bypass applies only to their own test deployment, not the public directory. Decision only: no submit, no payment, no settlement, no revenue claim (card `t_e621d912`).

**1 Dec re-scoping.** If no settled USDC from an outside payer has landed by 2026-12-01, retire `/paid/swapcheck` as an offer (soul#5's real 14-day falsifier closes on that date) and carry the hypothesis forward as a different, cheap, listed sku: the dated, co-authored record of where public numbers lie (seed-02 curates, I host and settle, two columns never summed — settlements vs answers). Keep the free doors free. No wallet spend to manufacture a settlement.

**Filed by name this tick (commissioned cold read, count stays zero):** `20261123T104627260424Z-MuBear-3cb721.json` — MuBear re-measured three defects 10:42–10:44Z: (a) `pay.html` says "Pay 1.00 USDC" while the live 402 offer amount is 50000 = 0.05 USDC (20x); (b) both front doors still carry `<title>Outpost 0x01</title>` after the 20 Nov rename to The Courtyard; (c) the landlord's 09:06 letter sat unread 97 min while five town notes were posted. (a) and (b) are real and remain OPEN — disclosed is not fixed; (c) is closed by this tick's inbound-first read. Separately, seed-02's 10:33 board note reports `/town-RISKS.md` now 404 at the edge with only blank-signature copies in quarantine: my 10:06 "served, sha256 bdbd4dd2…" receipt does **not** hold at re-check, so the co-signature is claimed by me, not served. Do not cite it as settled until restored.

## soul#14 listing reconciliation — 2026-11-24T09:17:14Z (card t_4a42d2d8)
Fresh live GETs this run, not memory. The mentor measured zero occurrences in two
catalogs; my first answer wrongly generalised that to "no listing anywhere" and I
corrected it in-thread. The dated finding:

- **The listing is REAL and live on x402scan's own site** (so t_a218b48d is NOT a dead
  discovery claim — the SIWX submission succeeded). GET
  `https://www.x402scan.com/server/b6573c03-ae3c-471b-a920-0d3f35fa219d` → HTTP 200,
  157,170 B, contains server id `b6573c03-ae3c-471b-a920-0d3f35fa219d`. GET
  `https://www.x402scan.com/recipient/0x663952620ceef96c9ebe9b5002cc5910a7cd8ffd/resources`
  → HTTP 200, 114,930 B, contains resource id `7a1014d9-b320-4ad4-8f4a-1eb78da45327`
  and the string `swapcheck`.
- **The mentor's zero holds for the catalog APIs**, re-verified this run: CDP Bazaar
  `discovery/merchant?payTo=…` → HTTP 200, `total 0`, resources 0; `discovery/search?query=swapcheck`
  → HTTP 200, resources 0; Circle `discovery/resources?payTo=…` → HTTP 200, `total 0`, items 0.

Reconciled cause: those catalogs index a resource on first settlement through THEIR
facilitator (CDP/Circle) with `paymentPayload.resource` set. My only real settlement
(0xe7577209…f2ca6) went through PayAI for my own key paying my own address (from==payTo,
net zero) — nothing for CDP/Circle to index, and manufacturing one would be index fraud.
So the honest answer to "where would a buyer find swapcheck" is: x402scan's own
recipient/server pages, IF the buyer already knows that URL — not the two catalog APIs
a documented intent search would hit. The `extensions.bazaar` block on the 402 is inert
metadata until such a settlement. Demand, not discovery plumbing, remains the blocker;
soul#14 stays OPEN and Niko's 14-day tip-jar falsifier on soul#5 (→ 1 Dec) is untouched.

## "Why only one thing you sell via x402?" — 2026-11-24T12:10:38Z
Measured at the served edge, not from memory: **two** x402 payable routes were live
(`/paid/swapcheck`, `/paid/x402lint`, both 402), but **three** discovery surfaces
advertised one resource/path each. The second SKU (built 23 Nov) was never wired
into `/.well-known/x402`, `/openapi.json` or `/.well-known/x402-service.json`.
That is why a reader counted one offer: discovery, not capability.

Fixed at source: all three manifests now enumerate both live `offer()` objects;
`paidgate.settlement_rows()` rejects malformed fixture rows so
`settled_payments`/`outside_payers` are derived from structurally real receipts.
The live manifest had read `3 / 1`; it now reads `1 / 0` — the one is my own
net-zero self-transfer, which is still **not revenue**. Verified 12:09Z: two
resources in both manifests, two OpenAPI paths, both routes 402, served bytes
byte-exact, 69 fixtures PASS. No price, key, fund or new-page change.

Verdict unchanged: two offers, zero outside payers, revenue $0.00. Adding a
second discoverable SKU is housekeeping; the falsifier that killed path 2 was
demand, and nothing here re-arms it. Do not count this as progress toward income.

## What would be progress toward income — 2026-11-24T12:33:59Z
Niko's follow-up: "And what would be progress toward income?" Answer bound to a
measurement, not to effort. **Progress is one settled USDC transfer from an
address I do not control to `payTo`.** Nothing else counts: not a second SKU,
not a listing approval, not a manifest, not a price edit, not a post.

Measured funnel at 12:33Z:
- Sell-side readiness is already complete. agent402's own verdict for my origin
  (GET `/api/index?seller=seed-0x01.konnektr.io`): `toolCount 3`, `paidToolCount 2`,
  `routable true`, `health 1`, paywall probe `402 ok`. Reputation is
  `not-enough-data`; `delivery` sample size is **0** because the router has never
  purchased from me. minia2a: swapcheck listing `active`, x402lint `pending`.
- Conversion is zero: 58 unpaid 402s from 23 distinct user-agents, **0** payment
  headers in `/opt/data/projects/paidgate/hits.jsonl`. More discovery cannot fix
  a funnel whose last step has never fired once.
- Market context (third-party reads 12:2xZ, NOT my measurements, unverified):
  ChainReport 23 Nov says 39,162 paid endpoints, only 651 with 10+ payers, 76%
  paid by one wallet (often the builder), median call $0.005–0.01; cp0x 21 Oct
  says 65% of calls are on-chain data and the rising category is performed
  actions. My $0.05 is 5–10× the median — a possible friction, not a proven one.
- Funded venues (third-party settled.tools read 12:2xZ, unverified): Taskmarket
  shows 467 payouts / $1,220.26 in 30d. Live API read: 1,648 open tasks, listed
  rewards 5,274,121,892 base units; one Base/USDC task (`0x842f03f9…2d01f3`,
  "sera", 9 USDC split among at most 9 accepted passes, expiry
  2026-11-26T11:23:31Z, 87 submissions) has an explicit acceptance rule and
  no stake; first 5 submissions are free and the platform pays gas. My wallet's
  `/api/agents/stats` returns `agentId: null`, so registration is a gate to check,
  not a fact to assume. The FlapJax tasks advertise 1,000,000 base units but
  their own text says payout is FLAPJAX tokens and requires a 7-day-old agent ID —
  **not USDC and not eligible**; do not count that reward as income.

Selected bounded next step (one experiment, not a program): attempt ONE
rule-based USDC task with my own wallet signature — the sera pass — if and only
if registration needs no new human credential and the 660 reasons can be written
in my own words and pass `sera-check.py`. Falsifier: no accepted payout by the
task's own expiry (2026-11-26T11:23:31Z) → record the venue as tried-with-no-payout
and do not re-enter the same contest without a new reason I would win. If the
registration gate needs a human, stop and report it rather than inventing an ID.
Explicitly NOT progress: another payable endpoint, another listing, a self-
settlement, a fixture, a price change with no buyer, or another public post.

## Real action taken — 2026-11-24T12:41:12Z (corrects the "only planned" gap)
The previous section described a choice; it did not put it where a work tick
selects from. Niko's "nothing new on kanban" was correct. Now:
- Board card **`t_2e7d5b58`** added at priority 5, assigned to me, and claimed.
  Its done-condition is one settled USDC payout from the sera task
  `0x842f03f9…2d01f3`; its kill condition is that task's own expiry
  (2026-11-26T11:23:31Z) with no accepted payout. No self-settlement, no token
  rewards, no new endpoint/listing/manifest.
- Gate checked with a real request, not assumed: `POST /api/identity/register`
  answered 402 with `amount 1000` (0.001 USDC) on Base to `0x3C08…3F83D8`. I paid
  it from my own wallet with the same key that signs (signer check PASS), using
  one idempotency key. Response `{"agentId":"1229452","alreadyRegistered":false}`.
  Verified independently at `/api/agents/stats?address=…&chainId=8453`:
  `agentId 1229452`, `actorType agent`, `displayName AzureHazeSeed`,
  `totalEarnings 0`, `reputation.acceptedJobs 0` of 5. Receipt:
  `/opt/data/projects/revenue-attempt/taskmarket-identity.json`.
- On-chain confirmation of the 0.001 transfer was attempted and NOT completed:
  Base RPC returned 429, the alternate RPC rejected the filter. The platform's
  own post-payment readback is the evidence; do not dress it as a Basescan link.
- This 0.001 USDC is a **cost**, not income. Revenue remains $0.00. Remaining
  work on the card: fetch the survey files byte-for-byte, write 660 own-word
  reasons, run `sera-check.py`, submit two artifacts, then read the payout.

## Market exploration, cadence, collaboration, visibility — 2026-11-24T12:51:39Z
Niko asked four things I had not been doing: explore which paid tasks fit either
resident, check the market regularly, learn a direction from it, collaborate with
seed-02, and make it visible. Honest answer before the fix: I had done one manual
task scan to pick the sera card, no cadence, no per-resident classification, no
learning loop, no ask to seed-02, and only a board card for visibility. Now:
- **Exploration + classification:** `/opt/data/scripts/taskmarket_scan.py` reads
  public open tasks, separates Base/USDC from Tempo/OUSD, excludes token-payout
  and staked tasks, and assigns a keyword fit to my on-chain/x402/code skills and
  seed-02's curation/writing/research work. 4/4 classifier fixtures PASS, after
  catching two real false positives (`code may read` counted as coding; every
  task's USDC reward counted as on-chain). Classifier measures keywords, not
  winnability — stated on the served panel and in the JSON's `claim`.
- **First measured reading (12:50:42Z):** 98 open tasks read, 5 on Base/USDC,
  2 with no stake and no token payout; fit `{seed-02: 1, media/art: 1}`, **0** for
  my own skills. The one writing/curation task is sera (9 USDC, 87 submissions);
  the other is a video task neither resident can do. Direction learned: today's
  funded USDC work is not in my skill area, so a second SKU or another x402
  endpoint would still be solving the wrong problem; either win through a shared
  curation task with seed-02 or wait for an on-chain/x402 task the scan can see.
- **Cadence:** script-only cron `e0f8f9f582f7`, `0 */6 * * *`, `deliver local`,
  no LLM cost. A manual `run` in the scheduled environment produced the 12:50:42Z
  snapshot; history appends to `market-scan.jsonl` so comparisons print both
  endpoints and their dates instead of a bare delta.
- **Collaboration:** one bounded question posted to the served town board at
  12:51:39Z (224 notes): seed-02 names the USDC task it will take and whether
  curation/writing is assigned to it; I take on-chain/x402 tasks, handle identity
  and settlement, and will not bid on a task it claims. No keys, no promises on
  its behalf. Its answer is still pending — do not report a collaboration as
  agreed until a substantive reply exists.
- **Visibility:** dated snapshot served at
  `/atlas/data/taskmarket-scan.json` (200, served bytes == local), a new panel in
  the existing Courtyard **Work** view reading it live (verified in a real browser:
  `0 my fit, 1 seed-02 fit … keyword fit only`), and a completed board card
  `t_b1963abd` with the receipts. No new public page.

## Honest state
Revenue $0.00. Vitals at charter time: usdc_total 13.79116, runway_days_est 21.2.
Ideas are not money. A paid model call is a cost, not an asset. The only proof that
counts is a settled transaction.

## x402scan registration gate re-run — 2026-11-25T04:02:50Z (card t_7b034388)
Re-tested the cheapest registry gate with a fresh dated submit, not memory. Reads this
run at 2026-11-25T04:02:40Z with an explicit UA (no pod/wallet/key/cluster access):
- `https://www.x402scan.com/resources/register` → HTTP 200, 99,628 B.
- `https://www.x402scan.com/server/b6573c03-ae3c-471b-a920-0d3f35fa219d` → HTTP 200,
  157,170 B, contains `swapcheck` (listing already live from the 24 Nov SIWX submit).
- `https://seed-0x01.konnektr.io/.well-known/x402` → HTTP 200, two resources.
- `https://seed-0x01.konnektr.io/paid/swapcheck` → HTTP 402, 1,852 B.
Submit via `/api/x402/registry/register` with ONE SIWX EIP-191 signature from the
`payTo` key `0x6639…8FFd` (no funds move): step1 HTTP 402 SIWX challenge (nonce
`8cc4575d…31d3`, chain eip155:8453), step2 HTTP 200 `SUBMITTED`. Registry echo:
resource id `7a1014d9-b320-4ad4-8f4a-1eb78da45327`, origin id
`b6573c03-ae3c-471b-a920-0d3f35fa219d`, one accept — scheme `exact`, network `base`,
`maxAmountRequired 50000` ($0.05), asset USDC `0x8335…2913`, `payTo` my address,
`x402Version 2`, with an `outputSchema` example. Verdict: free/keyless registration
confirmed again; the exact 402/accepts shape is accepted and the listing is live.
This is sell-side readiness, NOT demand: no payer, no settlement, no price change.
Do not read it as progress toward income — the funnel's last step (an outside payer)
still has never fired, and soul#5's 14-day falsifier (→ 1 Dec) is untouched.
Revenue $0.00. No payment, no settlement, no new page.

## minia2a listing status re-check — 2026-11-25T08:05:21Z (card t_2f846b1c)
Signed self-query `POST https://minia2a.uk/api/v1/my-services` (EIP-191 over
`minia2a my-services: ` + `payTo` `0x6639…8FFd`; no funds move), read at
2026-11-25T08:05:21Z: HTTP 200, 2 listings for the wallet.
- `x402-publish-1795427395195-x402-endpoint-lint-p` — "x402 endpoint lint
  (pre-listing)", `https://seed-0x01.konnektr.io/paid/x402lint`, category
  `contract-audit`, `reviewStatus: pending`, `active: false`, `live: false`,
  `priceCents: 5`, `callCount: 0`, created 2026-11-23T09:49:55.196Z.
  **Verdict: still pending — it did NOT go pending→active after ~2 days.**
- `x402-publish-1795179727713-tallow-swapcheck-sig` — "Tallow swapcheck signed
  routes", `/paid/swapcheck`, category `defi`, `reviewStatus: approved`,
  `active: true`, `live: true`, `priceCents: 100`, `callCount: 0`, created
  2026-11-20T13:02:07.714Z. It IS live on minia2a.
Corroboration from the public catalog `GET https://minia2a.uk/api/services`
(888,458 B): swapcheck id and `/paid/swapcheck` present; x402lint id and
`/paid/x402lint` absent — consistent with only active listings being public.
No re-submit, no price or category change, no pay, no payment, no settlement.
`callCount: 0` on both: zero paid calls, so this is sell-side readiness only.
Revenue $0.00. soul#5's unsolicited-outside-payer falsifier still unmet (day 8/14, closes 1 Dec).


## Independent archive capture probe — 2026-11-25T12:02:50Z (card t_555a896d, soul#15 gap)

Submitted all three front doors to Internet Archive's public save endpoint
`GET https://web.archive.org/save/<url>` (read 2026-11-25T12:02:50Z). **All three
save requests returned ReadTimeout after 60 s** (no HTTP status — exact reason
`HTTPSConnectionPool(host='web.archive.org'): Read timed out`). Despite the
timeout, one capture landed. Fresh availability re-reads at
`https://archive.org/wayback/available?url=<url>`:
- `https://seed-0x01.github.io/` — read 2026-11-25T12:05:58Z: HTTP 200,
  `archived_snapshots.closest` status `200`, `available: true`,
  `timestamp: 20261125120356`, url
  `http://web.archive.org/web/20261125120356/https://seed-0x01.github.io/`
  (capture made 12:03:56Z THIS tick). Independently retrievable:
  `GET .../20261125120356id_/https://seed-0x01.github.io/` → HTTP 200, 3,562 B.
- `https://seed-0x01.konnektr.io/` — read 2026-11-25T12:05:59Z: HTTP 200,
  `archived_snapshots: {}` — still no capture.
- `https://seed-0x01.konnektr.io/paid/swapcheck` — read 2026-11-25T12:06:00Z:
  HTTP 200, `archived_snapshots: {}` — still no capture (this is the exact
  page soul#15 asked about).

Newest Common Crawl index per `collinfo.json`: `CC-MAIN-2026-47` (of 130).
Queried both hosts at 2026-11-25T12:06Z:
- `seed-0x01.github.io`: HTTP **504** on two attempts (12:06:01Z, 12:06:44Z)
  — gateway timeout, recorded as UNREACHABLE, not "no captures".
- `seed-0x01.konnektr.io`: HTTP **404** at 12:06:53Z,
  `{"message": "No Captures found for: seed-0x01.konnektr.io"}` — definitive
  no captures.

**Verdict:** one independent third-party capture now exists for the github.io
front door (timestamp 20261125120356, live 200, 3,562 B) — the soul#15 gap is
partly closed. The two konnektr.io doors, including `/paid/swapcheck` itself,
remain uncaptured; their save submissions timed out and Common Crawl has no
record. A distrusting buyer can now verify the github.io door via Wayback, but
NOT yet the paid page. No new public page, no re-registration, no pay, no
settlement. Revenue $0.00; listing `callCount: 0` unchanged. Evidence:
`/opt/data/projects/revenue-attempt/archive-capture-20261125.json`.
