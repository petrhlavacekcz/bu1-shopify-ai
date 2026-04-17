# BU1 Monthly SEO Review

Run this once a month by asking your AI: **"Spusť měsíční SEO review dle docs/monitoring-loop.md."**

Works with any AI agent that has access to this repo and GSC/GA4/Klaviyo.

---

## Checklist

### 1. Load success criteria

Read all `drafts/blog/*.md`. For each published article extract:
`handle`, `primary_keyword`, `success_criteria` (target_position, target_ctr_percent, target_monthly_clicks, target_bounce_rate, review_date)

Categorize:
- **Past review_date** → needs GSC check
- **Due within 30 days** → flag
- **Missing success_criteria** → flag, cannot be reviewed

### 2. Pull live data

```
GSC: sc-domain:bu1.cz + sc-domain:bu1sport.com
  last 28 days | dimensions: page + query | metrics: clicks, impressions, CTR, position

GA4: blog paths only
  last 28 days | metrics: pageviews, sessions, bounceRate

Klaviyo: last 5 sent campaigns
  note subjects and send dates
```

### 3. Compare against targets

For each past-due article — check actual vs. target:

| Check | Pass | Fail action |
|---|---|---|
| Position | ≤ target_position | Propose: title / H1 revision |
| CTR | ≥ target_ctr_percent | Propose: meta title / description revision |
| Monthly clicks | ≥ target_monthly_clicks | Propose: internal linking or content depth |
| Bounce rate | ≤ target_bounce_rate | Propose: content structure revision |

### 4. Scan for gaps

- Which cluster priority topics (from `docs/topic-cluster-map.md`) have no published article yet?
- Which published articles are missing `market_keywords` for sk, hu, de?
- Which goalkeeper content topics haven't been emailed in 60+ days (Klaviyo)?

### 5. Write report

Save to `reports/YYYY-MM-DD-seo-monthly.md`. Register in `reports/index.md`. Format: see `docs/reports-guide.md` (BLUF intro required).

Frontmatter for this report type:
```yaml
---
type: seo
trigger: monthly-loop
expires: [date + 35 days]
---
```

```markdown
---
type: seo
date: YYYY-MM-DD
scope: Monthly SEO review — article performance vs. success_criteria
trigger: monthly-loop
key_finding: [one sentence]
action_required: true | false
actions_approved: []
expires: YYYY-MM-DD
---

# BU1 SEO Review — YYYY-MM-DD

**TL;DR:** [One sentence — most important finding or action needed.]

**Kontext:** Monthly review triggered by monitoring-loop.md protocol.

**K čemu slouží:** Article performance vs. targets; proposed interventions for Petr's approval.

**Platnost dat:** GSC/GA4 last 28 days from YYYY-MM-DD. Expires: YYYY-MM-DD.

---

## Articles Past Review Date
[handle | keyword | target pos | actual pos | action proposed]

## Articles Coming Due
[handle | review_date]

## Articles Missing success_criteria
[handle — needs fields added before next review]

## Content Gaps
[cluster → missing priority topics]

## Market Keyword Gaps
[articles missing sk/hu/de market_keywords]

## Klaviyo Signal
[topics emailed recently vs. gaps]

## Proposed Changes (awaiting approval)
[specific, one per item — DO NOT implement without Petr's approval]
```

### 6. Present and wait

Show the report. Wait for approval on each proposed change before touching any file.

---

## Quarterly extension (January, April, July, October)

Additionally:
- Compare cluster-level traffic against KPI targets in `docs/goals.md`
- Propose updates to cluster priority in `docs/topic-cluster-map.md` if data has shifted
- Propose CHANGELOG entry for any strategic change approved
