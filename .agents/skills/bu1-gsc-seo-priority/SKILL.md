---
name: bu1-gsc-seo-priority
description: "Use when analyzing BU1 SEO opportunities or risks with Google Search Console data: impressions, CTR, queries, positions, locale URLs, titles, and metadata issues."
---

# BU1 GSC SEO Priority

Use this skill to turn Search Console data into a concrete BU1 SEO backlog.

## When To Use

- ranking locale pages by impressions and low CTR
- finding metadata or title problems on high-visibility pages
- checking whether translation issues affect search performance
- deciding which article or product pages deserve SEO-focused fixes first

## Preferred Inputs

Prefer normalized or snapshot data over manual exports.

Useful fields:

- page
- query
- country
- device
- clicks
- impressions
- CTR
- average position

## Workflow

1. Group by page first, then inspect queries.
2. Prioritize high-impression pages before low-volume anomalies.
3. Look for mismatch between query intent and current page title/meta/copy.
4. Distinguish indexing problems from snippet problems from content problems.
5. Convert analysis into a page-level action list.

## Guardrails

- Do not overreact to low-volume query noise.
- Do not claim ranking loss causes without comparing against page quality and CTR context.
- Canonicalize locale URLs before aggregation.

## Expected Output

Return:

- top SEO-priority URLs
- reason for prioritization
- likely metadata/content fix
- confidence level where inference is involved
