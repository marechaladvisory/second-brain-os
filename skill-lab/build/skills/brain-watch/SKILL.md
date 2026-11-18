---
name: brain-watch
description: Light connector watch for the second brain - list what changed in the watched sources (Google Drive now, Granola later) since the last resume point, read only the new or changed files, and queue one capture entry per file with new facts for brain-daily to integrate. Never edits notes. Use on its schedule (every few hours), when brain-daily finds the watch late, or when the user says "check the Drive", "watch for changes", "what changed in the Drive".
---

# brain-watch

Shared rules: `../_shared/contracts.md` (§6 queue and watch, §7 write discipline). Read it, the brain's `AGENTS.md` and the Watch section of `context/config.md` first.
Unattended: no questions. This skill only fills the queue (`notes/inbox.md`) and the resume points (`notes/sync-state.md`), both through `queue.py`. It never edits notes, hot.md or the daily note: brain-daily integrates.

**Automated-run marker**: first command `touch .claude/automated-run`; last command `rm -f .claude/automated-run`, also after a failure. On-demand runs skip it.

## 1. Which connectors
A connector is watched when it is in `connectors` and has its watch keys in config (Drive: `watch_drive_root`). Connectors with no section below are skipped and named in the report. `python3 queue.py cursor status` shows where each one stands.

## 2. Google Drive (connector name in sync-state: `google-drive`)
1. **Resume point**: `C = $(python3 queue.py cursor get google-drive)`; empty → C = `watch_start` from config, and `python3 queue.py cursor set google-drive <C>` now.
2. **List** (metadata only, does not count against the budget), every page, oldest first:
   `search_files` query `'<watch_drive_root>' in ancestors and trashed = false and (modifiedTime > '<C>' or createdTime > '<C>')`, `orderBy: "modifiedTime asc"`, `pageSize: 50`, `excludeContentSnippets: true`.
   For each id in `watch_drive_exclude`, run the same query with `'<excluded id>' in ancestors` and drop those files.
3. **Skip without reading** (count them per reason for the report):
   folders and shortcuts (`application/vnd.google-apps.folder|shortcut`); `image/*`, `video/*`, `audio/*`; titles starting with a `watch_drive_skip_titles` prefix; files over `watch_drive_max_mb` (list them by title); key `drive:<id>@<modifiedTime>` already queued (`python3 queue.py has "<key>"` exits 0).
4. **Read** the rest in order, at most `watch_budget_files` (`read_file_content`). For each file:
   - Find what the brain already knows: `python3 brain.py search "<title words or main entity>"`, open the best 1-2 notes. Facts from this file carry `(Drive: <title>` in notes.
   - Running documents (titles with ODJ, compte rendu, CR, Mails, Suivi, WhatsApp, or dated sections): keep only sections dated on or after the date of C. Other documents: keep only what the notes do not already say, or say differently.
   - Keep evergreen knowledge: decisions and their reason, amounts and fees, dates and deadlines, status changes, new organisations or people and their role, commitments, open questions. A tracking sheet gives an insight with its date ("12 exposants confirmés au 2026-11-18"), never its rows.
   - Never copy passwords, IDs, phone numbers, emails, postal addresses, passport or health data. Candidates: first name + initial only. [AGENTS.md]
   - New material → one entry per file:
     `python3 queue.py add --source drive --session "drive:<id>@<modifiedTime>" --certainty fact|hypothesis --entities "<existing slugs; ...>" --facts "<fact (Drive: <title>, <YYYY-MM-DD>); ...>" --decisions "<what | why: ...>" --open-loops "<...>"`
     Entities use the existing note names found by search. `hypothesis` when the document is a draft, a proposal not yet accepted, or the fact is unclear.
   - Nothing new → no entry.
   - Unreadable file → list it in the report and go on.
   - After each file, with or without an entry: `python3 queue.py cursor set google-drive <its modifiedTime>`. A crash then loses nothing and redoes nothing.
5. **End**: whole list handled → `python3 queue.py cursor set google-drive <latest modifiedTime or createdTime in the list>` (C again when the list was empty: this stamps `last_run`). Budget reached → the cursor stays on the last file read; the rest waits for the next run. (A file moved into the Drive keeps an old modifiedTime: createdTime catches it.)

## 3. Close the run
1. Something queued, budget reached, or a read failed → append to `log.md`: `## [date] watch | drive: <n> listed, <m> read, <k> queued, <s> skipped | touched: notes/inbox.md`. Nothing new → no log line (the run is visible in sync-state). [six runs a day would flood log.md]
2. Git repo → `git add notes/inbox.md notes/sync-state.md log.md && git commit -m "brain: watch <date>"`. The scheduled prompt pushes.

## 4. Report (only output)
Cursor before → after · Listed, read, queued (title → entities), skipped per reason · Too large or unreadable (titles) · Budget left or "rest next run" · Connectors not watched.
