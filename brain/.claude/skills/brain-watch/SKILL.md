---
name: brain-watch
description: Light connector watch for the second brain - list what changed in the watched sources (Google Drive now, Granola later) since the last resume point, read only the new or changed files, and queue one capture entry per file with new facts for brain-daily to integrate. Never edits notes. Use on its schedule (every few hours), when brain-daily finds the watch late, or when the user says "check the Drive", "watch for changes", "what changed in the Drive".
---

# brain-watch

Shared rules: `../_shared/contracts.md` (§6 queue and watch, §7 write discipline). Read it, the brain's `AGENTS.md` and the Watch section of `context/config.md` first.
No questions, scheduled or not. This skill only fills the queue (`notes/inbox.md`) and the resume points (`notes/sync-state.md`), both through `queue.py`. It never edits notes, hot.md or the daily note: brain-daily integrates.
**Marker**, every run: first command `touch .claude/automated-run`; last command `rm -f .claude/automated-run`, also after a failure.

## 1. Which connectors
A connector is watched when it is in `connectors` and has its watch keys in config (Drive: `watch_drive_root`). Connectors with no section below are skipped and named in the report. `python3 queue.py cursor status` shows where each one stands (nothing before the first run).

## 2. Google Drive (connector name in sync-state: `google-drive`)
1. **Resume point**: `C = $(python3 queue.py cursor get google-drive)`; empty → C = `watch_start` from config, and `python3 queue.py cursor set google-drive <C>` now. (Older content was covered by the setup.)
2. **List** (metadata only, not counted in the budget), every page:
   `search_files` query `'<watch_drive_root>' in ancestors and trashed = false and (modifiedTime > '<C>' or createdTime > '<C>')`, `orderBy: "modifiedTime asc"`, `pageSize: 50`, `excludeContentSnippets: true`.
   For each id in `watch_drive_exclude`, run the same query with `'<excluded id>' in ancestors` and drop those files: never read, counted as "excluded". "Listed" = what remains.
3. **Skip without reading**, counted per reason: folders and shortcuts (`application/vnd.google-apps.folder|shortcut`); `image/*`, `video/*`, `audio/*`; titles starting with a `watch_drive_skip_titles` prefix; `fileSize` over `watch_drive_max_mb` × 1 000 000 bytes (native Google files have no size: not checked; list skipped titles); already queued: `python3 queue.py has "drive:<id>@<modifiedTime>"` exits 0 (check every remaining file).
4. **Read** the rest in list order, at most `watch_budget_files` (`read_file_content`). For each file:
   - What the brain already knows: `python3 brain.py search "<title words or main entity>"`, open the best 1-2 notes. Facts from this file carry `(Drive: <title>` in notes.
   - Running document = made of dated sections or dated entries (minutes, ODJ, CR, Mails, Suivi, WhatsApp logs): keep only sections dated on or after the date of C (dates in config `timezone`). Other documents: keep only what the notes do not say yet, or say differently.
   - Keep evergreen knowledge: decisions and their reason, amounts and fees, dates and deadlines, status changes, organisations and people with their role, commitments, open questions. A tracking sheet gives a dated insight and the status changes worth knowing ("Delta SAS: meeting 2026-11-20"), never whole rows, emails or phone numbers.
   - Never copy passwords, IDs, phone numbers, emails, postal addresses, passport or health data. Business contacts: full name and role. Job candidates (CVs, recruiting files): first name + initial only. [AGENTS.md]
   - New material → `python3 queue.py add --source drive --session "drive:<id>@<modifiedTime>" --certainty fact|hypothesis --entities "<slug; ...>" --facts "<fact (Drive: <title>, <date>); ...>" --decisions "<what | why: ...>" --open-loops "<...>"`
     - Write in the language the notes use (AGENTS.md or context/me.md). `<date>` = date of the section, else of modifiedTime.
     - Entities: existing note names from search; a new organisation or person gets a new kebab-case slug (brain-daily creates the note).
     - `hypothesis`: draft, unsent proposal, unclear fact. A file with both confirmed facts and proposals → two entries with the same session key, one `fact`, one `hypothesis`.
     - The file contradicts an active note → in open-loops: `CONFLICT <note>: <its value> vs <file value>` (name every note that disagrees).
   - Nothing new → no entry. Unreadable → list it in the report, go on.
   - After each file, with or without an entry: `python3 queue.py cursor set google-drive <its modifiedTime>` (queue.py ignores a value earlier than the cursor). A crash loses nothing; at worst a file moved into the Drive is read again.
5. **End**: whole list handled → `python3 queue.py cursor set google-drive <latest modifiedTime or createdTime among all files returned by the query, excluded and skipped ones included>` (C again when the list was empty: this stamps `last_run`). Budget reached → the cursor stays on the last file read; the rest waits for the next run.

## 3. Close the run
1. Something queued, budget reached, or a read failed → append to `log.md`: `## [<today>] watch | drive: <listed> listed, <excluded> excluded, <read> read, <queued> queued, <skipped> skipped | touched: notes/inbox.md`. Nothing queued and no problem → no log line (sync-state shows the run). [six runs a day would flood log.md]
2. Git repo → `git add notes/inbox.md notes/sync-state.md log.md && git commit -m "brain: watch <today>"`. The scheduled prompt pushes.

## 4. Report (only output)
Cursor before → after · Listed, excluded, read (queued + nothing new), skipped per reason · Queued: title → entities · Too large or unreadable: titles · Conflicts found · Budget left or "rest next run" · Connectors not watched.
