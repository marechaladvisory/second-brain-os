---
title: Brain config
type: context
status: active
created: {{TODAY}}
updated: {{TODAY}}
summary: Settings every brain routine reads. Change values here, never in skills.
---
# Config
- timezone: Europe/Paris
- daily_time: "07:30"
- lint_day: friday
- lint_time: "16:00"
- connectors: []          # e.g. [calendar, gmail, fireflies, crm]
- budget_reads: 60
- budget_writes: 25
- budget_fixes: 15
- proactivity: advisor    # observer | advisor (drafts, never sends) | assistant | partner
- capture_confirm: false  # true = /done shows the entry before queueing
- queue: inbox            # inbox (notes/inbox.md); airtable adapter later
## Watch (read by brain-watch; empty = connector not watched)
- watch_interval_hours: 4       # schedule of brain-watch; brain-daily catches up if the last run is older than 1.5x this
- watch_budget_files: 20        # files read per run; the rest waits for the next run (cursor stays on the last one read)
- watch_drive_root: ""          # Drive folder or shared drive id to watch, e.g. 0AJF...
- watch_drive_exclude: []       # folder ids never read (passwords, personal)
- watch_drive_skip_titles: []   # title prefixes never read, e.g. ["CV "]
- watch_drive_max_mb: 25        # larger files are listed in the report, not read
- watch_start: ""               # first resume point (ISO date) when sync-state has none
- watch_gmail_start: ""         # Gmail watched when set: first resume point (ISO date); older mail = initial pass or ignored
- watch_gmail_query: "-category:promotions -category:social -category:forums"   # added to after:<cursor>
- watch_gmail_skip_senders: [noreply, no-reply, notification, mailer-daemon]   # automated senders, never read
- watch_gmail_budget_threads: 30   # threads read per run
- watch_gmail_recruiting: summary  # summary (one entry per run, no candidate named) | candidates (first name + initial) | skip
- watch_gmail_recruiting_markers: ["candidature", "offre de stage"]   # subject words that mark a recruiting thread
## Decay (read by brain.py; days; 0 = no decay)
- decay_half_life: project=30, entity=180, concept=365, source=365, log=7, inbox=3, context=0, decision=0
- decay_status_mult: active=1, draft=0.8, archived=0.3, superseded=0
- decay_weights: relevance=1, recency=1, importance=1   # raise relevance if old exact matches get buried
- review_days: context=90, concept=365, entity=180, project=30, inbox=7   # review_by = updated + this; read by skills
