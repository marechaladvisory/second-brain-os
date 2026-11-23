#!/usr/bin/env python3
"""queue.py - capture queue in notes/inbox.md (stdlib only). See contracts.md §6.
  python3 queue.py add --source claude-code --session "<id>" --entities "a; b" \
      --facts "..." --decisions "what | why: ..." --open-loops "..." \
      --certainty fact|hypothesis --verbatim "exact user sentence"
  python3 queue.py list [--status new]
  python3 queue.py set <id> integrated|rejected "<result>"
  python3 queue.py has "<session key>"            # exit 0 + id if an entry has it, else exit 1
  python3 queue.py cursor get <connector>         # print the resume point (empty if none)
  python3 queue.py cursor set <connector> <ISO>   # never moves back; also stamps last_run
  python3 queue.py cursor status                  # one line per connector, with hours since last run
  python3 queue.py cursor stale <connector> <h>   # exit 0 if last_run is missing or older than h hours
Sync state lives in notes/sync-state.md (contracts §6). Never edit it by hand.
"""
import argparse, datetime as dt, re, sys
from pathlib import Path

INBOX = Path(__file__).resolve().parent / "notes" / "inbox.md"
STATE = Path(__file__).resolve().parent / "notes" / "sync-state.md"
SOURCES = ["claude-code", "claude.ai", "drive", "gmail", "granola", "other"]
CURSOR = re.compile(r"^- ([\w.-]+): (\S+) \| last_run: (\S+)\s*$", re.M)
HEAD = re.compile(r"^## (q-\d{8}-\d{4,6}) \| (\w+)\s*$", re.M)
FIELDS = ["date", "source", "session", "certainty", "entities", "facts", "decisions",
          "open_loops", "verbatim", "result"]


def read():
    return INBOX.read_text(encoding="utf-8") if INBOX.exists() else ""


def add(a):
    now = dt.datetime.now()
    taken = {qid for qid, _, _ in entries()}
    while now.strftime("q-%Y%m%d-%H%M%S") in taken:   # watch runs add several per second
        now += dt.timedelta(seconds=1)
    qid = now.strftime("q-%Y%m%d-%H%M%S")
    vals = {"date": now.date().isoformat(), "source": a.source, "session": a.session,
            "certainty": a.certainty, "entities": a.entities, "facts": a.facts,
            "decisions": a.decisions, "open_loops": a.open_loops,
            "verbatim": a.verbatim, "result": ""}
    block = f"\n## {qid} | new\n" + "".join(f"- {k}: {vals[k] or ''}\n" for k in FIELDS)
    INBOX.parent.mkdir(parents=True, exist_ok=True)
    with INBOX.open("a", encoding="utf-8") as f:
        f.write(block)
    print(qid)


def entries():
    text = read()
    heads = list(HEAD.finditer(text))
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        yield h.group(1), h.group(2), text[h.end():end].strip()


def list_(status):
    for qid, st, body in entries():
        if status in (None, st):
            print(f"## {qid} | {st}\n{body}\n")


def set_(qid, status, result):
    if status not in ("integrated", "rejected"):
        sys.exit("status must be integrated or rejected")
    text = read()
    pat = re.compile(rf"^## {re.escape(qid)} \| \w+\s*$(.*?)(?=^## q-|\Z)", re.M | re.S)
    m = pat.search(text)
    if not m:
        sys.exit(f"{qid} not found")
    body = re.sub(r"^- result:.*$", f"- result: {result}", m.group(1), count=1, flags=re.M)
    INBOX.write_text(text[:m.start()] + f"## {qid} | {status}" + body + text[m.end():],
                     encoding="utf-8")
    print(f"{qid} -> {status}")


def has(key):
    for qid, st, body in entries():
        if re.search(rf"^- session: {re.escape(key)}\s*$", body, re.M):
            print(f"{qid} | {st}")
            return 0
    return 1


def iso(value):
    """'2026-11-18', '2026-11-18T10:16:59.506Z' or with offset -> aware UTC datetime."""
    v = value.strip().replace("Z", "+00:00")
    d = dt.datetime.fromisoformat(v if "T" in v else v + "T00:00:00+00:00")
    return (d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)).astimezone(dt.timezone.utc)


def stamp(d):
    return d.strftime("%Y-%m-%dT%H:%M:%S.") + f"{d.microsecond // 1000:03d}Z"


def state():
    text = STATE.read_text(encoding="utf-8") if STATE.exists() else ""
    return text, {m.group(1): (m.group(2), m.group(3)) for m in CURSOR.finditer(text)}


def cursor(a):
    text, cur = state()
    now = dt.datetime.now(dt.timezone.utc)
    if a.action == "get":
        print(cur.get(a.connector, ("", ""))[0])
        return 0
    if a.action == "status":
        for k, (c, last) in cur.items():
            print(f"{k}: cursor {c} | last_run {last} | {(now - iso(last)).total_seconds() / 3600:.1f} h ago")
        return 0
    if a.action == "stale":
        last = cur.get(a.connector, ("", ""))[1]
        return 0 if not last or (now - iso(last)).total_seconds() > float(a.value) * 3600 else 1
    if a.action != "set" or not a.value:
        sys.exit("usage: cursor get|set|status|stale <connector> [value]")
    new = iso(a.value)
    old = cur.get(a.connector, ("", ""))[0]
    if old and iso(old) > new:
        new = iso(old)                       # a cursor never moves back (a run lost nothing)
    line = f"- {a.connector}: {stamp(new)} | last_run: {stamp(now)}"
    if not text:
        text = ("---\ntitle: Sync state\ntype: log\nstatus: active\n"
                f"created: {now.date()}\nupdated: {now.date()}\n"
                "summary: Resume point per connector for brain-watch. Written by queue.py cursor, never by hand.\n"
                "---\n# Sync state\nResume point = last source change already looked at. Written by `queue.py cursor set`.\n")
    if a.connector in cur:
        text = re.sub(rf"^- {re.escape(a.connector)}: .*$", line, text, count=1, flags=re.M)
    else:
        text = text.rstrip("\n") + "\n" + line + "\n"
    text = re.sub(r"^updated: .*$", f"updated: {now.date()}", text, count=1, flags=re.M)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(text, encoding="utf-8")
    print(line[2:])
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    ad = sub.add_parser("add")
    ad.add_argument("--source", choices=SOURCES, default="claude-code")
    for f in ["session", "entities", "facts", "decisions", "open-loops", "verbatim"]:
        ad.add_argument(f"--{f}", default="")
    ad.add_argument("--certainty", choices=["fact", "hypothesis"], default="fact")
    ls = sub.add_parser("list")
    ls.add_argument("--status")
    st = sub.add_parser("set")
    st.add_argument("id"); st.add_argument("status"); st.add_argument("result")
    hs = sub.add_parser("has")
    hs.add_argument("key")
    cu = sub.add_parser("cursor")
    cu.add_argument("action", choices=["get", "set", "status", "stale"])
    cu.add_argument("connector", nargs="?", default="")
    cu.add_argument("value", nargs="?", default="")
    a = p.parse_args()
    if a.cmd == "add":
        add(a)
    elif a.cmd == "list":
        list_(a.status)
    elif a.cmd == "has":
        sys.exit(has(a.key))
    elif a.cmd == "cursor":
        sys.exit(cursor(a))
    else:
        set_(a.id, a.status, a.result)
