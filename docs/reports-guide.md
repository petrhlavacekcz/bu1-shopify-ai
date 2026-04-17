# BU1 Reports Guide

All reports live in `reports/`. Every report is a single file.

---

## Naming convention

```
reports/YYYY-MM-DD-type-scope.md
```

| Segment | Values | Examples |
|---|---|---|
| `type` | `seo`, `data`, `translation`, `strategy` | `seo`, `data` |
| `scope` | Short descriptor of what it covers | `market-signals`, `monthly-review`, `translation-audit` |

---

## Frontmatter schema

Every report starts with YAML frontmatter:

```yaml
---
type: seo | data | translation | strategy
date: YYYY-MM-DD
scope: one-line description of what this report covers
trigger: what caused this report (monthly-loop | session | manual)
key_finding: the single most important finding — one sentence
action_required: true | false
actions_approved: []   # list approved actions, or [] if none yet
expires: YYYY-MM-DD    # when this data is no longer useful as a decision input
---
```

### `expires` conventions by type

| Type | Expires |
|---|---|
| `seo` (monthly review) | 35 days after date (next review supersedes it) |
| `data` (market signals, GSC snapshots) | 6 months after date (strategy input) |
| `translation` (audit) | Until the issues are fixed, then mark `action_required: false` |
| `strategy` (decisions, prioritization) | No expiry — permanent record |

---

## Report structure

Every report uses BLUF (Bottom Line Up Front): the key finding appears in the first 3 lines so the reader can decide in 10 seconds whether to read further.

```markdown
---
[frontmatter]
---

# [Report Title]

**TL;DR:** [One sentence. What happened / what was found / what needs to happen.]

**Kontext:** [Why this report exists — what question it answers or what triggered it.]

**K čemu slouží:** [Who or what should use this data. E.g.: "Použij pro prioritizaci obsahu v Cluster 2" or "Vstup pro měsíční monitoring loop".]

**Platnost dat:** [When the data was pulled. Expires: YYYY-MM-DD.]

---

[Report body]
```

---

## Living index

All reports are indexed in `reports/index.md`. Add a row for every new report. Remove rows when a report has expired AND has no unresolved `action_required`.

---

## Existing reports (pre-format)

Reports in `reports/` created before this guide (e.g., `FINAL_AUDIT_2026-04-10.md`) are valid reference documents. They do not need to be reformatted — just ensure they are indexed.
