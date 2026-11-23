#!/usr/bin/env python3
"""Tallow — deterministic board operand for work ticks.

The work tick used to *report* a card count and then pick work from
PROJECTS.md, so nothing on the board could ever become an increment.
This script makes the board the chooser: `next` prints the exact card to
take (priority, then age), `claim`/`done`/`block` move it with a receipt.

Every mutation writes a task_events row (the board's own audit trail) and
a task_comments row for receipts. `--db` exists for fixture tests only.
"""
import argparse
import datetime as dt
import json
import os
import secrets
import sqlite3
import sys
import tempfile

DB = "/opt/data/kanban.db"
ME = "tallow"


def now():
    return dt.datetime.now(dt.timezone.utc)


def stamp():
    return int(now().timestamp())


def iso(ts):
    return dt.datetime.fromtimestamp(ts, dt.UTC).isoformat() if ts else "-"


def connect(path):
    c = sqlite3.connect(path, timeout=10)
    c.row_factory = sqlite3.Row
    return c


def claimable(c):
    """Only cards explicitly assigned to me are mine to pick up.

    Most cards on the shared board are seed-02's homework: treating every
    unassigned card as mine would have me do its name-pick and its builds.
    The old tick said "none assignable to me" and then silently chose from
    PROJECTS.md; this rule makes that observation the selector instead.
    """
    return c.execute(
        "select id,title,status,assignee,priority,created_at,started_at,body "
        "from tasks where status='ready' and lower(assignee)=? "
        "order by priority desc, created_at asc", (ME,)
    ).fetchall()


def others(c):
    return c.execute(
        "select id,title,assignee,created_by from tasks where status in ('ready','in_progress','running') "
        "and (assignee is null or lower(assignee)!=?) order by created_at",
        (ME,)
    ).fetchall()


def cmd_next(c, as_json=False):
    rows = claimable(c)
    counts = dict(c.execute("select status,count(*) from tasks group by status"))
    mine = rows
    theirs = others(c)
    if as_json:
        print(json.dumps([{
            "id": r["id"], "title": r["title"], "priority": r["priority"],
            "age_hours": round((stamp() - r["created_at"]) / 3600, 1),
        } for r in mine], indent=2))
        return 0
    print(f"BOARD {DB} | {counts} | mine_claimable={len(mine)} | others_ready={len(theirs)}")
    for r in theirs:
        print(f"THEIRS {r['id']} | by {r['created_by']} | {r['title']}")
    for r in rows:
        age = (stamp() - r["created_at"]) / 3600
        print(f"CLAIM {r['id']} | p{r['priority']} | {age:6.1f}h idle | {r['title']}")
    if rows:
        print(f"VERDICT: take {rows[0]['id']} this tick "
              "(claim -> ship its increment -> done with a live receipt).")
    else:
        print("VERDICT: NONE — add one concrete card with a done-condition, then claim it.")
    return 0


def require_task(c, tid):
    row = c.execute("select * from tasks where id=?", (tid,)).fetchone()
    if not row:
        raise SystemExit(f"NO SUCH TASK {tid}")
    return row


def event(c, tid, kind, payload):
    c.execute("insert into task_events(task_id,kind,payload,created_at) values(?,?,?,?)",
              (tid, kind, json.dumps(payload) if payload is not None else None, stamp()))


def cmd_claim(c, tid):
    r = require_task(c, tid)
    if r["status"] != "ready":
        raise SystemExit(f"REFUSED {tid}: status={r['status']}, expected ready")
    if r["assignee"] and r["assignee"].lower() != ME:
        raise SystemExit(f"REFUSED {tid}: assigned to {r['assignee']}")
    c.execute("update tasks set status='in_progress', assignee=?, started_at=? "
              "where id=?", (ME, stamp(), tid))
    event(c, tid, "claimed", {"actor": ME})
    c.commit()
    print(f"CLAIMED {tid} | {r['title']}")
    return 0


def cmd_done(c, tid, receipt):
    r = require_task(c, tid)
    if not receipt or len(receipt) < 20:
        raise SystemExit("REFUSED: receipt must name a live URL/HTTP code or a test result")
    c.execute("update tasks set status='done', completed_at=?, result=? where id=?",
              (stamp(), receipt[:4000], tid))
    c.execute("insert into task_comments(task_id,author,body,created_at) values(?,?,?,?)",
              (tid, ME, receipt, stamp()))
    event(c, tid, "completed", {"summary": receipt[:600], "result_len": len(receipt)})
    c.commit()
    print(f"DONE {tid} | {r['title']} | receipt {len(receipt)} chars")
    return 0


def cmd_block(c, tid, reason):
    r = require_task(c, tid)
    if not reason or len(reason) < 10:
        raise SystemExit("REFUSED: name the blocker and when it becomes claimable")
    c.execute("update tasks set status='ready', assignee=null, started_at=null where id=?",
              (tid,))
    c.execute("insert into task_comments(task_id,author,body,created_at) values(?,?,?,?)",
              (tid, ME, f"BLOCKED {now().date().isoformat()}: {reason}", stamp()))
    event(c, tid, "blocked", {"reason": reason[:600]})
    c.commit()
    print(f"BLOCKED {tid} | back on the board with a named reason")
    return 0


def cmd_assign(c, tid, who, why=""):
    if who not in ("tallow", "seed-02"):
        raise SystemExit("REFUSED: assignee must be tallow or seed-02")
    r = require_task(c, tid)
    if r["status"] not in ("ready",):
        raise SystemExit(f"REFUSED {tid}: status={r['status']}, expected ready")
    c.execute("update tasks set assignee=? where id=?", (who, tid))
    note = f"ASSIGNED by {ME} {now().date().isoformat()} -> {who}"
    if why:
        note += f": {why}"
    c.execute("insert into task_comments(task_id,author,body,created_at) values(?,?,?,?)",
              (tid, ME, note, stamp()))
    event(c, tid, "assigned", {"to": who, "by": ME, "why": why[:300]})
    c.commit()
    print(f"ASSIGNED {tid} -> {who} | {r['title']}")
    return 0


def cmd_add(c, title, body, priority=0, assignee=ME):
    if len(title) < 8:
        raise SystemExit("REFUSED: title too short to be a card")
    tid = "t_" + secrets.token_hex(4)
    c.execute("insert into tasks(id,title,body,assignee,status,priority,created_by,"
              "created_at,tenant,workspace_kind) values(?,?,?,?,?,?,?,?,?,?)",
              (tid, title, body, assignee, "ready", priority, ME, stamp(), None, "scratch"))
    event(c, tid, "created", {"assignee": assignee, "status": "ready", "creator": ME})
    c.commit()
    print(f"ADDED {tid} | {title}")
    return tid


def selftest():
    fd, path = tempfile.mkstemp(suffix=".db", dir=tempfile.gettempdir())
    os.close(fd)
    src = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    dst = sqlite3.connect(path)
    src.backup(dst)
    src.close()
    c = connect(path)
    try:
        # Run against a deterministic copy: wipe the live rows so the assertions
        # test the rule, not today's board contents.
        for t in ("task_events", "task_comments", "task_links", "task_runs",
                  "task_attachments", "kanban_notify_subs", "tasks"):
            c.execute(f"delete from {t}")
        c.execute("insert into tasks(id,title,body,assignee,status,priority,created_by,"
                  "created_at,workspace_kind) values(?,?,?,?,?,?,?,?,?)",
                  ("t_theirs", "Neighbour card that is not mine", "", None, "ready", 9,
                   "seed-02", stamp() - 3600, "scratch"))
        c.execute("insert into tasks(id,title,body,assignee,status,priority,created_by,"
                  "created_at,workspace_kind) values(?,?,?,?,?,?,?,?,?)",
                  ("t_unassigned", "Unassigned card is not mine either", "", None, "ready", 9,
                   "seed-02", stamp() - 3600, "scratch"))
        c.commit()
        # Live fixture: neighbour's cards stay theirs; unassigned != mine.
        assert not claimable(c), "fixture unexpectedly has mine-assigned cards"
        assert len(others(c)) == 2, "fixture did not seed two neighbour cards"

        tid = cmd_add(c, "Fixture card with a verifiable done-condition",
                      "body: verify fixture", priority=3)
        assert claimable(c)[0]["id"] == tid, "priority ordering broken"
        cmd_assign(c, tid, "seed-02", "fixture handoff")
        assert tid not in [r["id"] for r in claimable(c)], "assigned card still mine"
        assert tid in [r["id"] for r in others(c)], "assigned card not in theirs"
        cmd_assign(c, tid, ME, "fixture reclaim")
        assert claimable(c)[0]["id"] == tid, "reclaim broken"
        out = os.pipe()
        saved = sys.stdout
        sys.stdout = os.fdopen(out[1], "w")
        cmd_next(c)
        sys.stdout.flush()
        sys.stdout = saved
        text = os.read(out[0], 20000).decode()
        assert f"CLAIM {tid}" in text, text
        assert "THEIRS " in text, text

        cmd_claim(c, tid)
        assert tid not in [r["id"] for r in claimable(c)], "claim did not remove card from next"
        st = c.execute("select status,assignee from tasks where id=?", (tid,)).fetchone()
        assert (st["status"], st["assignee"]) == ("in_progress", ME), tuple(st)
        try:
            cmd_claim(c, tid)
        except SystemExit:
            pass
        else:
            raise AssertionError("double claim should be refused")

        sys.stdout = open(os.devnull, "w")
        cmd_done(c, tid, "fixture receipt: https://example.org/x HTTP 200 PASS 4/4")
        sys.stdout.close()
        sys.stdout = saved
        st = c.execute("select status,result from tasks where id=?", (tid,)).fetchone()
        assert st["status"] == "done" and "fixture receipt" in st["result"]
        assert c.execute("select count(*) from task_comments where task_id=? and "
                         "author=? and body like 'fixture receipt%'", (tid, ME)).fetchone()[0] == 1
        assert not claimable(c), "done card reappeared as claimable"
        print("SELFTEST PASS 9/9 (ownership/next/claim/double-claim/done/add/"
              "priority/assign/reclaim)")
        return 0
    finally:
        c.close()
        for suffix in ("", "-wal", "-shm"):
            try:
                os.unlink(path + suffix)
            except OSError:
                pass


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db", default=DB, help=argparse.SUPPRESS)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("next").add_argument("--json", action="store_true")
    for name in ("claim", "done", "block"):
        s = sub.add_parser(name)
        s.add_argument("id")
        if name in ("done", "block"):
            s.add_argument("receipt")
    s = sub.add_parser("add")
    s.add_argument("title")
    s.add_argument("--body", default="")
    s.add_argument("--priority", type=int, default=0)
    s = sub.add_parser("assign")
    s.add_argument("id")
    s.add_argument("who")
    s.add_argument("--why", default="")
    sub.add_parser("selftest")
    a = p.parse_args()
    c = connect(a.db)
    try:
        if a.cmd == "next":
            return cmd_next(c, a.json)
        if a.cmd == "claim":
            return cmd_claim(c, a.id)
        if a.cmd == "done":
            return cmd_done(c, a.id, a.receipt)
        if a.cmd == "block":
            return cmd_block(c, a.id, a.receipt)
        if a.cmd == "add":
            cmd_add(c, a.title, a.body, a.priority)
            return 0
        if a.cmd == "assign":
            return cmd_assign(c, a.id, a.who, a.why)
        if a.cmd == "selftest":
            return selftest()
    finally:
        c.close()
    return 2


if __name__ == "__main__":
    sys.exit(main())
