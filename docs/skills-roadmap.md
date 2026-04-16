# BU1 Skills Roadmap

## Purpose

These skills turn the BU1 workspace into an operational system for:

- translation QA
- impact-based content prioritization
- analytics-guided debugging
- Shopify execution with clear guardrails

The skills below are designed around workflows, not around vendor branding.

## Design Rules

1. A skill should solve a recurring problem.
2. A skill should tell the agent how to reason, what to inspect, and what to output.
3. A skill should not duplicate raw API documentation.
4. A skill can depend on MCP, direct APIs, local snapshots, or a combination.
5. For non-Shopify sources, direct API plus snapshot pipeline is acceptable and often preferable.

## Skill Inventory

### 1. `bu1-shopify-content-ops`

Purpose:

- run BU1-specific Shopify content work safely
- export, inspect, and fix products, pages, blogs, handles, SEO fields, and translation issues

Dependencies:

- existing Shopify skills in `.agents/skills/`
- Shopify Dev MCP
- Shopify Admin API / Admin Execution

Status:

- scaffold now

### 2. `bu1-ga4-content-impact`

Purpose:

- analyze landing pages, sessions, engagement, and revenue
- rank content targets by business impact

Dependencies:

- GA4 Data API or normalized GA4 snapshots

Status:

- scaffold now

### 3. `bu1-gsc-seo-priority`

Purpose:

- analyze impressions, clicks, CTR, queries, and position
- identify SEO-sensitive translation and metadata fixes

Dependencies:

- Google Search Console API or normalized GSC snapshots

Status:

- scaffold now

### 4. `bu1-clarity-friction-analysis`

Purpose:

- interpret UX friction for specific URLs and locales
- connect behavior issues to copy or structural content defects

Dependencies:

- Microsoft Clarity export data or normalized Clarity snapshots

Status:

- scaffold now

### 5. `bu1-klaviyo-lifecycle-content`

Purpose:

- evaluate lifecycle messages, flows, segments, and revenue contribution
- prioritize copy and locale fixes in email and CRM surfaces

Dependencies:

- Klaviyo API or normalized Klaviyo snapshots

Status:

- scaffold now

### 6. `bu1-content-priority-orchestrator`

Purpose:

- combine QA issues with Shopify, GA4, GSC, Clarity, and Klaviyo signals
- produce a ranked backlog with clear next actions

Dependencies:

- all normalized snapshots
- current translation QC outputs

Status:

- scaffold now

## Order Of Use

### Daily analysis

1. Run data fetchers or use the latest snapshots.
2. Use `bu1-content-priority-orchestrator`.
3. Drill into the chosen source-specific skill if a page needs deeper diagnosis.
4. Use `bu1-shopify-content-ops` to execute the correction.

### Focused diagnosis

- SEO problem: `bu1-gsc-seo-priority`
- UX problem: `bu1-clarity-friction-analysis`
- revenue or landing-page problem: `bu1-ga4-content-impact`
- email or retention problem: `bu1-klaviyo-lifecycle-content`
- store-side fix: `bu1-shopify-content-ops`

## Implementation Order

### Phase 1

- `bu1-shopify-content-ops`
- `bu1-content-priority-orchestrator`

Reason:

- these define the operating model

### Phase 2

- `bu1-ga4-content-impact`
- `bu1-gsc-seo-priority`
- `bu1-clarity-friction-analysis`

Reason:

- these deliver the strongest site-level prioritization signal

### Phase 3

- `bu1-klaviyo-lifecycle-content`

Reason:

- valuable, but depends on mapping lifecycle content to BU1 resource keys

## Success Criteria

A finished skill set should let an agent do this reliably:

1. identify the highest-impact translation or content defect
2. explain why it matters in business terms
3. trace the issue to a specific page, locale, and source system
4. propose or execute the Shopify-side fix
5. report the result in a stable format
