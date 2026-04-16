---
name: bu1-clarity-friction-analysis
description: "Use when diagnosing BU1 page friction with Clarity data: rage clicks, dead clicks, quick backs, scroll behavior, and mismatch between user intent and content."
---

# BU1 Clarity Friction Analysis

Use this skill to interpret Clarity behavior signals for BU1 pages and locales.

## When To Use

- investigating why a page with traffic underperforms
- reviewing friction on translated product, page, or article URLs
- checking whether UX issues are actually content issues
- supporting decisions after GA4 or GSC identifies a problem page

## Preferred Inputs

Useful fields:

- URL
- locale
- rage clicks
- dead clicks
- quick backs
- scroll depth
- session counts
- referrer or campaign if available

## Workflow

1. Start from a specific URL or small URL set.
2. Check whether friction is localized to one locale or universal.
3. Look for mismatch between what the page promises and what it delivers.
4. Separate copy problems from layout, navigation, or technical problems.
5. Convert findings into corrective actions with confidence notes.

## Guardrails

- Clarity signals are diagnostic, not definitive.
- Do not attribute every rage click to translation quality.
- If evidence points to layout or functionality, say so explicitly.

## Expected Output

Return:

- friction signals observed
- most likely explanation
- content vs UX classification
- next recommended fix
