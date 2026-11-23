---
title: Brain config
type: context
status: active
created: 2026-11-10
updated: 2026-11-10
summary: Settings every brain routine reads. Change values here, never in skills.
---
# Config
- timezone: Europe/Paris
- daily_time: "07:30"
- lint_day: friday
- lint_time: "16:00"
- connectors: [google-drive, gmail]   # simulated in evals: evals/fixtures/drive/, evals/fixtures/gmail/
- budget_reads: 60
- budget_writes: 25
- budget_fixes: 15
- proactivity: advisor    # observer | advisor (drafts, never sends) | assistant | partner
- capture_confirm: false  # true = /done shows the entry before queueing
- queue: inbox            # inbox (notes/inbox.md); airtable adapter later
## Watch (read by brain-watch; empty = connector not watched)
- watch_interval_hours: 4
- watch_budget_files: 20
- watch_drive_root: "SANDBOX-DRIVE"
- watch_drive_exclude: [EXCL-PASSWORDS]
- watch_drive_skip_titles: ["CV "]
- watch_drive_max_mb: 25
- watch_start: "2026-11-10"
- watch_gmail_start: "2026-11-10"
- watch_gmail_query: "-category:promotions -category:social -category:forums"
- watch_gmail_skip_senders: [noreply, no-reply, notification, mailer-daemon]
- watch_gmail_budget_threads: 30
- watch_gmail_recruiting: summary
- watch_gmail_recruiting_markers: ["candidature", "offre de stage"]
## Decay (read by brain.py; days; 0 = no decay)
- decay_half_life: project=30, entity=180, concept=365, source=365, log=7, inbox=3, context=0, decision=0
- decay_status_mult: active=1, draft=0.8, archived=0.3, superseded=0
- decay_weights: relevance=1, recency=1, importance=1   # raise relevance if old exact matches get buried
- review_days: context=90, concept=365, entity=180, project=30, inbox=7   # review_by = updated + this; read by skills
