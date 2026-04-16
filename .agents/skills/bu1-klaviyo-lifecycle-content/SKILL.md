---
name: bu1-klaviyo-lifecycle-content
description: "Use when evaluating BU1 email and lifecycle content through Klaviyo: flows, campaigns, segments, locale messaging, engagement, and attributed revenue."
---

# BU1 Klaviyo Lifecycle Content

Use this skill for BU1 lifecycle messaging analysis where email or CRM content needs prioritization.

## When To Use

- reviewing flow or campaign content by locale
- finding underperforming lifecycle messages with meaningful revenue impact
- checking whether untranslated or weak copy is hurting engagement
- mapping segment performance to content opportunities

## Preferred Inputs

Useful fields:

- flow or campaign name
- message id
- locale or segment
- sends
- opens
- clicks
- conversions
- attributed revenue

## Workflow

1. Identify the lifecycle surface: flow, campaign, or segment-driven message.
2. Rank by attributed revenue or strategic importance.
3. Compare copy quality and locale coverage against performance.
4. Distinguish audience-quality issues from message-quality issues.
5. Produce a prioritized message backlog.

## Guardrails

- Do not treat open rate as a standalone success metric.
- Do not assume a weak message is caused only by translation.
- Always prefer revenue-bearing or journey-critical messages first.

## Expected Output

Return:

- highest-priority lifecycle messages
- performance context
- likely content issue
- recommended fix order
