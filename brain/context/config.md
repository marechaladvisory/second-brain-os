---
title: Brain config
type: context
status: active
created: 2026-11-17
updated: 2026-11-23
summary: Settings every brain routine reads. Change values here, never in skills.
---
# Config
- timezone: Europe/Paris
- daily_time: "07:30"
- lint_day: friday
- lint_time: "16:00"
- connectors: [google-drive, gmail, granola]   # Drive: shared drive "Maréchal Advisory Team" (source of the setup, 2026-11-18); Gmail: mailbox of GM, initial pass 2026-11-23, then watched each morning by brain-daily (read-only, guard hook); Granola: meeting notes, account not created yet (connector refused on 2026-11-18, sign up then run the Granola pass). CRM Airtable not connected yet
- budget_reads: 80   # 60 → 80 on 2026-11-23: the morning watch now reads Drive (≤20) and Gmail (≤30) before integrating
- budget_writes: 25
- budget_fixes: 15
- proactivity: advisor    # observer | advisor (drafts, never sends) | assistant | partner
- capture_confirm: false  # true = /done shows the entry before queueing
- queue: inbox            # inbox (notes/inbox.md); airtable adapter later
## Watch (read by brain-watch; empty = connector not watched)
- watch_interval_hours: 12      # no separate watch task (quota, 2026-11-18): brain-daily runs the watch itself each morning, since the last run is then older than 18 h
- watch_budget_files: 20        # files read per run; the rest waits for the next run
- watch_drive_root: "0AJFAnfE8WNvjUk9PVA"            # shared drive "Maréchal Advisory Team"
- watch_drive_exclude: [10a4_E3DXcVAn6tCdKqni4jUuMfxyKoC2]   # "Wifi & Mdp" (passwords)
- watch_drive_skip_titles: ["CV "]                  # candidates' CVs are never read
- watch_drive_max_mb: 25
- watch_gmail_start: "2026-11-23"   # initial pass read the mailbox (from its start, 2026-10-26) up to 2026-11-23T08:51Z
- watch_gmail_query: "-category:promotions -category:social -category:forums -category:updates"
- watch_gmail_skip_senders: [noreply, no-reply, notification, mailer-daemon, airtable.com]   # automated senders, never read
- watch_gmail_budget_threads: 30
- watch_gmail_recruiting: summary   # Guillaume, 2026-11-23: campaign summary only, no candidate named from mail
- watch_gmail_recruiting_markers: ["candidature", "offre de stage", "stage", "internship", "entretien collectif"]
- watch_start: "2026-11-18"     # setup date; older Drive content was read by the setup
## Decay (read by brain.py; days; 0 = no decay)
- decay_half_life: project=30, entity=180, concept=365, source=365, log=7, inbox=3, context=0, decision=0
- decay_status_mult: active=1, draft=0.8, archived=0.3, superseded=0
- decay_weights: relevance=1, recency=1, importance=1   # raise relevance if old exact matches get buried
- review_days: context=90, concept=365, entity=180, project=30, inbox=7   # review_by = updated + this; read by skills
