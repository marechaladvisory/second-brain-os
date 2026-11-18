#!/usr/bin/env python3
"""Merge Drive metadata pages into all.tsv, tree.md, stats.md (metadata only)."""
import glob, json, os, sys
from collections import defaultdict, Counter
from datetime import date, timedelta

S = sys.argv[1]
TEAM = "0AJFAnfE8WNvjUk9PVA"
MYDRIVE = "0AA_OO0X7ardYUk9PVA"
TODAY = date(2026, 11, 17)
CUTOFF = (TODAY - timedelta(days=90)).isoformat()
FOLDER = "application/vnd.google-apps.folder"

def load(pattern):
    out = []
    for p in sorted(glob.glob(os.path.join(S, pattern))):
        with open(p) as fh:
            out.extend(json.load(fh).get("files", []))
    return out

# folders
folders = {}
for f in load("folders-*.json") + load("foldersA-*.json") + load("foldersB-*.json"):
    folders[f["id"]] = {"title": f["title"], "parentId": f.get("parentId"),
                        "modifiedTime": f.get("modifiedTime", "")}
tsv = os.path.join(S, "folders-x1.tsv")
if os.path.exists(tsv):
    for line in open(tsv, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line:
            continue
        fid, par, mod, title = line.split("\t", 3)
        folders.setdefault(fid, {"title": title, "parentId": par, "modifiedTime": mod})

# files
files = {}
raw_file_rows = 0
for f in load("files-*.json") + load("filesA-*.json") + load("shared-*.json"):
    raw_file_rows += 1
    if f.get("mimeType") == FOLDER:
        folders.setdefault(f["id"], {"title": f["title"], "parentId": f.get("parentId"),
                                     "modifiedTime": f.get("modifiedTime", "")})
        continue
    files[f["id"]] = f

path_cache = {}
orphans = set()
def fpath(fid, depth=0):
    """Path of folder fid, ending with '/'."""
    if fid == TEAM:
        return "TEAM/"
    if fid == MYDRIVE:
        return "MYDRIVE/"
    if fid is None or fid not in folders or depth > 50:
        if fid is not None:
            orphans.add(fid)
        return "?/"
    if fid in path_cache:
        return path_cache[fid]
    f = folders[fid]
    p = fpath(f["parentId"], depth + 1) + f["title"].replace("/", "∕").strip() + "/"
    path_cache[fid] = p
    return p

def clean(s):
    return (s or "").replace("\t", " ").replace("\n", " ")

# all.tsv
rows = []
for fid, f in files.items():
    par = f.get("parentId")
    rows.append([fid, clean(f.get("title")), f.get("mimeType", ""), par or "",
                 fpath(par) + clean(f.get("title")), (f.get("modifiedTime") or "")[:10],
                 f.get("owner") or ("team-drive" if f.get("sharedDriveId") == TEAM else ""),
                 f.get("fileSize", ""), clean(f.get("lastModifyingUserName"))])
rows.sort(key=lambda r: r[4].lower())
with open(os.path.join(S, "all.tsv"), "w", encoding="utf-8") as out:
    out.write("id\ttitle\tmimeType\tparentId\tpath\tmodifiedTime\towner\tfileSize\tlastModifyingUser\n")
    for r in rows:
        out.write("\t".join(str(x) for x in r) + "\n")

# tree
children = defaultdict(list)
for fid, f in folders.items():
    children[f["parentId"]].append(fid)
direct = Counter()
latest_direct = {}
for f in files.values():
    p = f.get("parentId")
    direct[p] += 1
    m = (f.get("modifiedTime") or "")[:10]
    if m > latest_direct.get(p, ""):
        latest_direct[p] = m

sub_count, sub_latest = {}, {}
def agg(fid, depth=0):
    if fid in sub_count:
        return sub_count[fid], sub_latest[fid]
    c = direct.get(fid, 0)
    l = latest_direct.get(fid, "")
    if depth < 60:
        for ch in children.get(fid, []):
            cc, ll = agg(ch, depth + 1)
            c += cc
            l = max(l, ll)
    sub_count[fid], sub_latest[fid] = c, l
    return c, l

roots = [("TEAM", TEAM), ("MYDRIVE", MYDRIVE)]
lines = ["# Drive folder tree", "",
         "Format: `name` (direct files / subtree files, latest modified in subtree)", ""]
def walk(fid, depth):
    for ch in sorted(children.get(fid, []), key=lambda x: folders[x]["title"].lower()):
        c, l = agg(ch)
        lines.append("  " * depth + f"- {folders[ch]['title'].strip()} ({direct.get(ch,0)} / {c}, {l or '-'})")
        walk(ch, depth + 1)
for name, rid in roots:
    c, l = agg(rid)
    lines.append(f"## {name}/ ({direct.get(rid,0)} direct / {c} subtree, latest {l or '-'})")
    lines.append("")
    walk(rid, 0)
    lines.append("")
nulls = direct.get(None, 0)
lines.append(f"## ?/ (no parent, shared with me): {nulls} files")
orph_folders = [fid for fid, f in folders.items()
                if f["parentId"] not in folders and f["parentId"] not in (TEAM, MYDRIVE)]
if orph_folders:
    lines.append("")
    lines.append("## Orphan folders (parent not in folder set)")
    for fid in orph_folders:
        lines.append(f"- {folders[fid]['title']} ({fid}) parent={folders[fid]['parentId']}")
with open(os.path.join(S, "tree.md"), "w", encoding="utf-8") as out:
    out.write("\n".join(lines) + "\n")

# stats
by_mime = Counter(f.get("mimeType", "") for f in files.values())
by_top = Counter()
by_top_recent = Counter()
for r in rows:
    parts = r[4].split("/")
    key = "/".join(parts[:3]) if len(parts) > 3 else "/".join(parts[:2])
    by_top[key] += 1
    if r[5] >= CUTOFF:
        by_top_recent[key] += 1
recent = sum(1 for r in rows if r[5] >= CUTOFF)
st = ["# Drive inventory stats", "",
      f"- Folders: {len(folders)}", f"- Files (deduped): {len(files)} (raw rows: {raw_file_rows})",
      f"- Files modified in last 90 days (>= {CUTOFF}): {recent}",
      f"- Orphan parent ids: {len(orphans)}", "",
      "## By mimeType", "", "| mimeType | count |", "|---|---|"]
for k, v in by_mime.most_common():
    st.append(f"| {k} | {v} |")
st += ["", "## By top-level folder (first 2 path levels)", "",
       "| path | files | modified last 90d |", "|---|---|---|"]
for k, v in sorted(by_top.items(), key=lambda kv: kv[0].lower()):
    st.append(f"| {k} | {v} | {by_top_recent.get(k,0)} |")
with open(os.path.join(S, "stats.md"), "w", encoding="utf-8") as out:
    out.write("\n".join(st) + "\n")

print(f"folders={len(folders)} files={len(files)} raw={raw_file_rows} recent90={recent} "
      f"orphans={len(orphans)} orphan_folders={len(orph_folders)}")
