---
name: bu1-content-priority-orchestrator
description: "Use when combining BU1 translation QA with Shopify, GA4, GSC, Clarity, and Klaviyo signals to produce a ranked content backlog and recommended next actions."
---

# BU1 Content Priority Orchestrator

Use this skill when the goal is to decide what BU1 should fix next.

## When To Use

- building a ranked translation and content backlog
- combining defect reports with traffic, SEO, UX, and lifecycle data
- deciding which locale or page type deserves work first
- preparing weekly or operational prioritization reports

## Inputs

Use as many of these as available:

- translation QC output
- Shopify resource snapshots
- GA4 snapshots
- GSC snapshots
- Clarity snapshots
- Klaviyo snapshots

## Workflow

1. Normalize all records to a resource key: type, id, locale, canonical URL.
2. Remove known false positives and intentional exceptions.
3. Score quality severity.
4. Score business impact.
5. Score SEO and UX impact where available.
6. Produce a single ranked backlog with explicit reasoning.
7. Send execution items to `bu1-shopify-content-ops`.

## Priority Rules

- Revenue page with a hard content defect beats a low-traffic page with many cosmetic defects.
- High-impression low-CTR page beats a no-visibility page with the same metadata defect.
- Strong UX friction on a strategic page increases urgency.
- Intentional duplicate handles and model names should be downgraded or ignored.

## Guardrails

- Do not optimize for raw issue count.
- Do not rank pages before canonicalizing URLs and locales.
- Call out when a recommendation is based on incomplete source coverage.

## Expected Output

Return:

- ranked backlog
- why each item is high priority
- recommended owner or execution path
- data gaps that reduce confidence
