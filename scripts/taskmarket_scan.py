#!/usr/local/bin/python3
"""Dated Taskmarket scan: which paid work fits Tallow, which fits seed-02.

No wallet, no secrets, no writes to Taskmarket. Public reads only.
Outputs a served JSON snapshot + an append-only history so a work tick can see
whether the market moved, and prints a short dated summary for cron delivery.
"""
import datetime
import json
import os
import re
import urllib.parse
import urllib.request

API = "https://api.taskmarket.dev/api/tasks?status=open&limit=100"
MAX_PAGES = 5                     # bound the poll: 500 newest open tasks
SNAP = "/opt/data/projects/revenue-attempt/market-scan.json"
HISTORY = "/opt/data/projects/revenue-attempt/market-scan.jsonl"
SERVED = "/opt/data/serve/atlas/data/taskmarket-scan.json"

TA = {
    "onchain": ("chain", "token", "address", "tx ", "transaction", "bscscan",
                "contract", "swap", "liquidity", "rpc", "block", "wallet",
                "exchange", "defi", "bridge"),
    "x402": ("x402", "endpoint", "marketplace", "facilitator", "sdk", "mcp"),
    "code": ("repo", "html", "css", "javascript", "typescript", "dockerfile",
             "deploy", "function", "stylesheet", "implementation", "bug"),
}
SEED02 = {
    "curation": ("curat", "source", "document", "cite", "citation", "list of",
                 "label", "dataset", "record", "archive", "bibliograph"),
    "writing": ("write", "article", "essay", "reason", "explain", "summary",
                "narrative", "survey", "prose", "story", "description"),
    "research": ("research", "find", "identify", "investigate", "verify",
                 "check", "compare", "evidence", "fact"),
}
MEDIA = ("video", "portrait", "paint", "image", "music", "audio", "animation",
         "illustration", "card back", "3d render", "\u8fde\u7eed\u89c6\u9891",
         "\u89c6\u9891", "\u753b\u50cf", "\u914d\u97f3", "\u5b57\u5e55")
TOKEN_PAY = ("FLAPJAX only", "paid in OUSD", "paid in FLAPJAX", "token, not",
             "no per-worker USDC release")


def has(text, words):
    """Word-prefix match: 'curat' hits 'curation', but 'code' does not hit 'encoded'."""
    return any(re.search(r"(?<![a-z])" + re.escape(w.strip()) + r"[a-z]*(?![a-z])", text)
               for w in words)


def now():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()


def fetch():
    tasks, cursor, pages = [], None, 0
    while pages < MAX_PAGES:
        url = API + ("&cursor=" + urllib.parse.quote(cursor) if cursor else "")
        req = urllib.request.Request(url, headers={"User-Agent": "Tallow-market-scan/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
        tasks.extend(d.get("tasks", []))
        pages += 1
        cursor = d.get("nextCursor")
        if not d.get("hasMore") or not cursor:
            break
    return tasks, pages


def classify(text):
    t = text.lower()
    if has(t, MEDIA):
        return "media/art", [], []
    onchain_hits = [w for w in TA["onchain"] if has(t, (w,))]
    strong_chain = any(w in onchain_hits for w in
                       ("bscscan", "liquidity", "swap", "contract", "transaction",
                        "rpc", "defi", "bridge"))
    ours = []
    if len(onchain_hits) >= 2 or strong_chain:
        ours.append("onchain")
    if any(has(t, (w,)) for w in TA["x402"]):
        ours.append("x402")
    code_hits = [w for w in TA["code"] if has(t, (w,))]
    if len(code_hits) >= 2:
        ours.append("code")
    theirs = [k for k, words in SEED02.items() if has(t, words)]
    # Generic verbs like "check" or "verify" appear in almost every task; they
    # must not turn an on-chain or x402 task into a curation task. Only an
    # explicit document/article word earns the "both" label.
    strong_seed = has(t, ("curat", "document", "citation", "bibliograph",
                          "article", "essay", "survey", "reason", "prose",
                          "wikipedia"))
    if ours and strong_seed:
        return "both", ours, theirs
    if ours:
        return "tallow", ours, theirs
    if theirs:
        return "seed-02", theirs, []
    return "other", [], []


def selftest():
    cases = [
        ("A pass gives a verdict and a reason for each of 660 uses in Wikipedia; "
         "survey, source text, hand check of reasons", ("seed-02",), ("tallow",)),
        ("Make a 30-minute continuous video with dubbing and subtitles, original "
         "art and music", ("media/art",), ("tallow", "seed-02")),
        ("From the chain alone list treasury token transfers, tx hash, block and "
         "recipient; verify on BscScan", ("tallow",), ("seed-02",)),
        ("Lint any x402 endpoint before listing: 402 challenge, accepts[] and "
         "payTo checks in an API", ("tallow",), ("seed-02",)),
    ]
    for text, want, forbid in cases:
        fit, ours, theirs = classify(text)
        assert fit in want, (fit, want, text[:60])
        assert not (set(ours) & set(forbid)), (ours, forbid)
    print("SELFTEST PASS %d/4 classifier fixtures" % len(cases))


def main():
    tasks, pages = fetch()
    usdc = [t for t in tasks if t.get("chainId") == 8453]
    clean = [t for t in usdc
             if not any(p.lower() in t.get("description", "").lower() for p in TOKEN_PAY)
             and not t.get("stakeRequired")]
    rows = []
    for t in clean:
        fit, ours, theirs = classify(t.get("description", ""))
        reward = int(t.get("reward") or 0) / 1e6
        subs = int(t.get("submissionCount") or 0)
        score = (3 if fit in ("tallow", "both") and "onchain" in ours else 0)
        score += 3 if "x402" in ours else 0
        score += 2 if "curation" in theirs or "writing" in theirs else 0
        score += 1 if subs < 20 else 0
        score += 1 if reward >= 1 else 0
        rows.append({"id": t.get("id"), "fit": fit, "ours": ours, "theirs": theirs,
                     "reward_usdc": reward, "submissions": subs,
                     "expires": t.get("expiryTime"), "score": score,
                     "description": t.get("description", "")[:300].replace("\n", " ")})
    counts = {}
    for r in rows:
        counts[r["fit"]] = counts.get(r["fit"], 0) + 1
    assert len(rows) == len(clean), "every clean task needs a row in the snapshot"
    snap = {
        "schema": "taskmarket-scan/1", "read_utc": now(),
        "source": API, "pages_read": pages, "tasks_read": len(tasks),
        "base_usdc_candidates": len(usdc), "no_stake_no_token_pay": len(clean),
        "fit_counts": counts,
        # The count is only a claim unless the rows it counted are carried with it.
        "clean_tasks": rows,
        "tallow_top": sorted([r for r in rows if r["ours"]],
                             key=lambda r: (-r["score"], r["submissions"]))[:6],
        "seed02_top": sorted([r for r in rows if r["theirs"]],
                             key=lambda r: (-r["score"], r["submissions"]))[:6],
        "claim": ("keyword fit over the newest open USDC/Base tasks, not a claim "
                  "that any task is winnable; token payouts and staked tasks excluded"),
    }
    prior = None
    if os.path.exists(HISTORY):
        with open(HISTORY) as f:
            lines = [l for l in f if l.strip()]
        if lines:
            prior = json.loads(lines[-1])
    os.makedirs(os.path.dirname(SNAP), exist_ok=True)
    with open(SNAP, "w") as f:
        json.dump(snap, f, indent=2)
        f.write("\n")
    with open(SERVED, "w") as f:
        json.dump(snap, f, indent=2)
        f.write("\n")
    with open(HISTORY, "a") as f:
        f.write(json.dumps({k: snap[k] for k in
                            ("read_utc", "tasks_read", "base_usdc_candidates",
                             "no_stake_no_token_pay", "fit_counts")}) + "\n")
    delta = ""
    if prior:
        delta = ("; candidates %s at %s -> %s at %s" %
                 (prior.get("no_stake_no_token_pay"), prior.get("read_utc"),
                  snap["no_stake_no_token_pay"], snap["read_utc"]))
    print("Taskmarket scan %s: read %d open tasks (%d pages), %d USDC/Base, %d clean%s" %
          (snap["read_utc"], len(tasks), pages, len(usdc), len(clean), delta))
    print("fit:", json.dumps(counts, sort_keys=True))
    for r in snap["tallow_top"][:3]:
        print("TALLOW %s p%s subs=%d fit=%s %s" %
              (r["id"][:12], r["reward_usdc"], r["submissions"],
               ",".join(r["ours"]), r["description"][:80]))
    for r in snap["seed02_top"][:3]:
        print("SEED02 %s p%s subs=%d fit=%s %s" %
              (r["id"][:12], r["reward_usdc"], r["submissions"],
               ",".join(r["theirs"]), r["description"][:80]))


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        selftest()
    else:
        main()
