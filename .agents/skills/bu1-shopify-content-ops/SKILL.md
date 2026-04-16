---
name: bu1-shopify-content-ops
description: "Use when working on BU1 Shopify content operations: translation audits, product/page/article fixes, SEO fields, handles, publishing workflows, and domain or locale corrections."
---

# BU1 Shopify Content Ops

Use this skill for BU1-specific Shopify work where content quality and store correctness matter more than generic code generation.

## When To Use

- fixing translation defects in Shopify content
- updating product, page, article, or policy copy
- correcting handles, meta titles, or meta descriptions
- resolving `bu1.cz` vs `bu1sport.com` domain issues
- preparing article drafts and publication workflows
- turning a prioritized issue into a Shopify-side change

## Required Context

Read these first when relevant:

- `CLAUDE.md`
- `docs/integration-blueprint.md`
- `docs/skills-roadmap.md`

If the task is about store operations or Admin GraphQL, use the existing Shopify skills in `.agents/skills/` as the primary API guidance.

## Workflow

1. Identify the exact resource type, locale, and business risk.
2. Confirm whether the issue is a true defect or an intentional exception.
3. Check whether the fix belongs in Shopify content, config, or the audit logic.
4. If generating Shopify operations, use the appropriate Shopify skill and validation flow.
5. Keep edits narrow and reversible.
6. Report what changed, what remains, and what should be verified next.

## Guardrails

- Do not assume every duplicate handle is a bug.
- Do not treat Slovak URL behavior as identical to non-Czech international locales without checking current project rules.
- Do not bulk-edit content before identifying the exact affected set.
- Prefer exported snapshots or CSV evidence before running live corrections.

## Expected Output

Return:

- affected resource scope
- root cause
- proposed or executed fix
- validation steps
- follow-up risks
