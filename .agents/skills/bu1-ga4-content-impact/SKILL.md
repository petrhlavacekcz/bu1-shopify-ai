---
name: bu1-ga4-content-impact
description: "Use when analyzing BU1 content performance through GA4: landing pages, engagement, ecommerce impact, locale performance, and traffic-based prioritization."
---

# BU1 GA4 Content Impact

Use this skill to interpret GA4 data for BU1 content and translation decisions.

## When To Use

- ranking pages by sessions, engagement, or revenue
- comparing locale landing-page performance
- checking whether a translation defect likely affects business outcomes
- identifying high-traffic pages that deserve immediate content fixes

## Preferred Inputs

Prefer normalized or snapshot data over ad hoc live queries.

Useful fields:

- page path or landing page
- locale or country
- sessions
- engaged sessions
- purchases
- revenue
- device category
- channel grouping

## Workflow

1. Identify the page set and time window.
2. Segment by locale, page type, and channel where possible.
3. Separate traffic problems from content problems.
4. Compare performance against similar BU1 pages, not against arbitrary site averages.
5. Feed the result into a ranked recommendation, not only a descriptive summary.

## Guardrails

- Do not infer copy quality from traffic alone.
- Do not mix URL variants without canonicalization.
- Flag when locale inference is weak or missing.

## Expected Output

Return:

- top affected URLs
- impact summary
- probable content implication
- recommended next action
