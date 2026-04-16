# BU1 Data Integration Blueprint

## Purpose

Turn this workspace from a translation QA project into a content operations system that:

- pulls business and behavioral signals from Shopify, Klaviyo, GA4, Clarity, and Google Search Console
- prioritizes translation and content fixes by impact, not only by linguistic defects
- supports agent workflows through MCP where MCP is the right interface
- keeps reproducible local snapshots for reporting and automation

This document is the target architecture for the next implementation phase.

As of 2026-04-10:

- `shopify-dev-mcp` is already enabled in the local Codex environment
- no local MCP integration for Klaviyo, GA4, Clarity, or Search Console is configured in this workspace
- the current repo is a content and QA workspace, not an application repo

## Principles

1. Shopify remains the operational source of truth for catalog, translations, handles, pages, blogs, and publication state.
2. MCP is used for interactive agent work, schema discovery, and guided execution.
3. Repeatable reporting must run on local snapshots, not only on live MCP or API calls.
4. Every content issue should be traceable to both a resource and an impact score.
5. Priority should be decided by business value and user friction, not by raw issue count.

## Recommended Tooling Split

### 1. Shopify Dev MCP

Use for:

- latest Shopify docs and schema-aware exploration
- Admin GraphQL query design and validation
- Storefront MCP and Customer Accounts MCP design work
- Polaris, Liquid, Functions, and extension generation support

Why:

- Shopify positions the Dev MCP server as the current interface for development resources and schema access.
- The server runs locally and does not require store authentication for docs/schema tasks.

Use in this project for:

- translation audit query generation
- article publishing workflows
- future AI shopping agent work
- validation of generated Shopify operations before execution

### 2. Shopify Admin API / Admin Execution

Use for:

- exporting translatable resources
- reading product, page, blog, and policy metadata
- fixing bad handles, bad domains, and broken content references
- publishing drafts and writing SEO metafields

Why:

- this is the system of record for actual store content
- it should power all correction workflows, even if issue discovery comes from other systems

### 3. Storefront MCP and Customer Accounts MCP

Use for:

- future BU1 shopping assistant
- storefront product discovery, cart, and policy QA
- customer order and account workflows where the app eventually needs them

Recommendation:

- do not make this phase 1
- treat it as phase 4, after data prioritization and translation QA are stable

### 4. Klaviyo API

Use for:

- campaign and flow performance by locale and market
- revenue-bearing events and metric aggregates
- segment and profile-driven content prioritization

Use in this project for:

- identify high-value locale segments with weak content
- identify flows using stale or untranslated copy
- compare email revenue contribution against on-site content quality

### 5. GA4 Data API

Use for:

- landing page traffic and engagement
- ecommerce revenue by page, locale, device, and channel
- measuring whether translation defects affect engagement and conversion

Use in this project for:

- prioritize product/page/article translation fixes by sessions, engagement, and revenue
- detect locale pages with high entrances and weak conversion

### 6. Google Search Console API

Use for:

- impressions, clicks, CTR, and average position by page, query, country, and device
- identifying SEO-impacting translation problems

Use in this project for:

- prioritize fixes on pages with high impressions and weak CTR
- identify locale pages where title/meta/handle defects likely reduce organic performance

### 7. Microsoft Clarity

Use for:

- behavioral friction diagnosis
- rage clicks, quick backs, dead clicks, scroll issues, and top problem URLs
- custom tagging for locale, content type, and experiment grouping

Use in this project for:

- explain why a page underperforms after translation
- validate whether copy and UX mismatch are driving exits

## Architecture

### Layer A: Connectors

Interactive:

- Shopify Dev MCP
- optional future MCP bridges for non-Shopify systems

Scheduled/API:

- Shopify Admin API
- Klaviyo REST APIs
- GA4 Data API
- Google Search Console API
- Clarity Data Export API

### Layer B: Local Snapshots

Create a local data folder:

```text
data/
  snapshots/
    shopify/
    klaviyo/
    ga4/
    gsc/
    clarity/
  normalized/
  scores/
```

Purpose:

- keep raw extracts versionable outside of source control if needed
- normalize all systems into a common resource model
- allow reproducible daily or weekly scoring runs

### Layer C: Normalized Resource Model

Every record should map to a canonical resource key:

```text
resource_type: PRODUCT | PAGE | ARTICLE | BLOG | COLLECTION | POLICY | FLOW_MESSAGE
resource_id: native platform id if available
locale: cs | sk | en | de | ...
canonical_url: absolute public URL
handle: localized handle if relevant
title: current localized title
owner_system: shopify | klaviyo | ga4 | gsc | clarity
```

This is the bridge between language QA and performance data.

### Layer D: Scoring

Each resource gets:

- `quality_score`
- `impact_score`
- `priority_score`
- `recommended_action`

Example:

```text
priority_score =
  issue_severity_weight
  * business_impact_weight
  * traffic_weight
  * seo_weight
  * ux_friction_weight
```

## Proposed Scoring Inputs

### Quality inputs

From current scripts:

- missing required translation fields
- wrong domain
- forbidden Czech leakage
- duplicate untranslated copy
- outdated status
- broken image references
- broken legacy links

### Business inputs

From Shopify:

- product status
- inventory availability
- collection membership
- product age / launch recency

From Klaviyo:

- attributed revenue
- flow revenue
- campaign revenue
- engagement by locale segment

From GA4:

- sessions
- engaged sessions
- ecommerce revenue
- add-to-cart rate
- conversion rate

From Search Console:

- impressions
- clicks
- CTR
- average position

From Clarity:

- rage clicks
- dead clicks
- quick backs
- low scroll depth on key pages

## Priority Heuristics

Use these default rules:

1. Revenue page with wrong domain or missing content: highest priority.
2. High-impression page with weak title/meta and low CTR: very high priority.
3. High-traffic page with Clarity friction and duplicated translation: very high priority.
4. Low-traffic outdated translation with no revenue and no SEO visibility: low priority.
5. Model-name duplicates and intentionally shared handles: ignore or downgrade.

## Files To Add Next

Create these files in the next implementation pass:

```text
scripts/fetch_shopify_snapshot.py
scripts/fetch_klaviyo_snapshot.py
scripts/fetch_ga4_snapshot.py
scripts/fetch_gsc_snapshot.py
scripts/fetch_clarity_snapshot.py
scripts/normalize_snapshots.py
scripts/score_content_priority.py
scripts/export_priority_report.py
config/data_sources.example.json
config/scoring_weights.json
docs/data-contracts.md
```

## Suggested Config

Add a checked-in example config only, never secrets:

```json
{
  "shopify": {
    "store_domain": "bu1rebuild.myshopify.com"
  },
  "ga4": {
    "property_id": "123456789"
  },
  "gsc": {
    "site_urls": [
      "https://bu1.cz/",
      "https://bu1sport.com/"
    ]
  },
  "clarity": {
    "project_id": "clarity-project-id"
  },
  "klaviyo": {
    "revision": "2025-10-15"
  }
}
```

Secrets should live in local environment variables or a non-committed env file.

## Data Contract Per Source

### Shopify snapshot

Minimum outputs:

- products with ids, handles, titles, status, collections
- pages and articles with ids, handles, titles, published status
- translation fields and outdated status
- SEO metafields where used

### GA4 snapshot

Minimum outputs:

- page path
- landing page
- locale or country dimension if available
- sessions
- engaged sessions
- ecommerce purchases
- item revenue or purchase revenue

### Search Console snapshot

Minimum outputs:

- page
- query
- country
- device
- clicks
- impressions
- CTR
- position

### Clarity snapshot

Minimum outputs:

- URL
- source / medium / campaign where available
- traffic
- engagement time
- rage click count
- dead click count
- quick back count
- scroll depth

### Klaviyo snapshot

Minimum outputs:

- metric id and metric name
- event aggregate counts
- attributed revenue where available
- campaign / flow message metadata
- locale or audience segment mapping

## Recommended Phase Order

### Phase 1: Stabilize current QA

Scope:

- fix rule drift in current docs and validators
- remove secrets from docs
- make current reports reproducible

Deliverables:

- aligned domain rules
- corrected validator exit behavior
- updated audit workflow docs

### Phase 2: Add data snapshot layer

Scope:

- implement Shopify, GA4, GSC, and Clarity fetchers
- define normalized resource keys
- store daily snapshots locally

Reason:

- these four sources provide the fastest value for content prioritization

### Phase 3: Add scoring and reporting

Scope:

- combine QC issues with traffic, SEO, and UX signals
- generate a ranked backlog

Deliverables:

- `priority_report.csv`
- `priority_report.md`
- top issues by locale, page type, and business impact

### Phase 4: Add Klaviyo

Scope:

- connect campaign and flow performance to content resources
- score email copy and locale performance

Reason:

- valuable, but the mapping model is slightly more custom than GA4/GSC/Clarity

### Phase 5: Add storefront agent capabilities

Scope:

- evaluate Storefront MCP and Customer Accounts MCP for BU1 assistant use cases
- separate customer-facing agent work from internal content ops workflows

## What I Would Build First

If we want the highest leverage with the lowest implementation risk, build this first:

1. `fetch_shopify_snapshot.py`
2. `fetch_ga4_snapshot.py`
3. `fetch_gsc_snapshot.py`
4. `fetch_clarity_snapshot.py`
5. `normalize_snapshots.py`
6. `score_content_priority.py`

That gives BU1 a single ranked list like:

- fix EN product meta descriptions that still point to `bu1.cz`
- fix HR product pages with Czech leakage and high exits
- fix DE articles with high impressions, low CTR, and broken image references
- fix SK landing pages with wrong domain or missing localized handles

## MCP Strategy

Recommended MCP usage in this repo:

- keep using `shopify-dev-mcp` for Shopify docs, schema discovery, and code validation
- do not block implementation on finding official MCP servers for every external system
- for Klaviyo, GA4, Clarity, and Search Console, use direct APIs first unless a reliable MCP integration is already supported in your local environment

Reason:

- MCP is excellent for interactive agent workflows
- scheduled reporting is usually cleaner and more deterministic through direct API clients

This is an intentional split, not a fallback.

## External Documentation Notes

These points informed the design above:

- Shopify Dev MCP is the current official entry point for assistant-driven Shopify development workflows.
- Shopify Storefront MCP and Customer Accounts MCP are positioned for customer-facing AI shopping experiences, not as replacements for internal reporting pipelines.
- GA4 Data API supports report-based extraction of dimensions and metrics for ecommerce and traffic analysis.
- Search Console API supports search analytics queries by page, query, country, and device, with documented quotas and partial-row behavior.
- Clarity exposes both a client API for tagging and a Data Export API with strict limits.
- Klaviyo exposes metrics and segments APIs suitable for campaign and event aggregation, but project-specific modeling will be needed to align email data to BU1 resource keys.

## Risks

- inconsistent locale mapping across systems
- weak URL canonicalization between `bu1.cz`, `bu1.cz/sk`, and `bu1sport.com/{locale}`
- false positives if intentional shared handles are not explicitly whitelisted
- snapshot freshness issues if all systems are queried at different times
- privacy and consent issues if Clarity or customer-linked data is joined carelessly

## Non-Negotiables

- remove API keys from committed docs
- add explicit locale URL mapping in config, not only in prose
- whitelist intentional duplicate handles and model names
- make every report reproducible from saved snapshots
- keep source-level and normalized data separate

## Immediate Next Step

Implement phase 1 before adding more integrations:

1. align domain rules in `CLAUDE.md` and validators
2. fix validator filtering and exit-code behavior
3. add a committed integration config example
4. remove committed secrets from documentation

After that, build the snapshot layer in phase 2.
