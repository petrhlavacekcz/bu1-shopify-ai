# BU1 Integrations Catalog

## Purpose

This document defines which external systems belong in the BU1 Shopify AI Ops workspace, how they should be connected, and which interface type should be preferred:

- MCP
- direct API
- CLI
- local snapshots

The catalog is agent-agnostic.

It is written for a multi-agent environment that may include Claude, ChatGPT/Codex, Gemini CLI, GLM, OpenRouter-based agents, and Hugging Face workflows.

## Operating Rule

If an official MCP server exists and is stable, use it for interactive agent work.

If MCP is not available, not accessible, or not mature enough, use the official API directly.

If neither MCP nor API is the right runtime interface for day-to-day reporting, use scheduled snapshots derived from the official API.

## Priority Tiers

### Tier 1: Core Integrations

Required for the system to be operational:

- Shopify
- BU1 Brand & Content System

### Tier 2: Business Intelligence Integrations

Strongly recommended because they drive prioritization:

- Google Analytics 4
- Google Search Console
- Klaviyo
- Google Merchant Center / Merchant API
- Microsoft Clarity

### Tier 3: Paid Media Integrations

Recommended once the core workflows are stable:

- Google Ads
- Meta / Facebook Ads
- Sklik

### Tier 4: Optional Future Integrations

Add only if they map to a real BU1 workflow:

- review platforms
- support/helpdesk tools
- ERP or warehouse systems
- experimentation platforms

## Integration Matrix

| System | Why it matters | Preferred interface | Fallback | Read/Write | Status |
|---|---|---|---|---|---|
| Shopify Dev docs and schemas | authoritative Shopify development context | official MCP | skills + docs | read | adopt |
| Shopify store operations | actual store changes | Admin API + CLI execution | direct GraphQL | read/write | adopt |
| BU1 Brand & Content System | canonical brand and content rules | external URL reference | cached summary notes | read | adopt |
| Klaviyo | lifecycle content and revenue context | official MCP | API | read first, selective write | adopt |
| GA4 | traffic, ecommerce, landing page impact | official MCP for exploration | Data API | read | adopt |
| Search Console | impressions, CTR, query demand | API | local snapshots | read | adopt |
| Merchant Center | product visibility on Google | API + Merchant docs MCP | local reports | read first, selective write | adopt |
| Clarity | friction and behavior evidence | API / export | local snapshots | read | adopt |
| Google Ads | paid search performance and campaign diagnostics | official MCP for exploration | Ads API | read first, selective write later | phase 2 |
| Meta Ads | paid social diagnostics | API | snapshots | read first | phase 2 |
| Sklik | Czech paid search context | API | snapshots | read first | phase 2 |

## Canonical External References

### BU1 Brand & Content System

Keep this as a live external reference because it is expected to change over time.

- Canonical URL: [BU1 Brand & Content System](https://petrhlavacekcz.github.io/bu1-brand-design/)

Local docs in this workspace may summarize or operationalize those rules, but they must not silently redefine them.

## Core Integrations

### 1. Shopify

#### Role

Primary operational system for:

- products
- pages
- blog articles
- SEO fields
- publication state
- translations stored in Shopify

#### Interfaces

- Official MCP: Shopify Dev MCP
- Official toolkit: Shopify AI Toolkit plugin and skills
- Official execution path: Shopify CLI `shopify store execute`
- Official store API: Shopify Admin GraphQL API

#### Why this is core

Shopify explicitly supports multiple AI tools through the Shopify AI Toolkit, including Claude Code, Codex CLI, Cursor, Gemini CLI, and VS Code.

Sources:

- [Shopify AI Toolkit](https://shopify.dev/docs/apps/build/ai-toolkit)
- [Shopify AI Toolkit changelog](https://shopify.dev/changelog/shopify-ai-toolkit-connect-your-ai-tools-to-the-shopify-platform)
- [Storefront MCP](https://shopify.dev/docs/apps/build/storefront-mcp)

#### Recommended usage

- use Dev MCP for docs, schemas, and validation
- use Admin API and CLI for real store changes
- use local workflow skills to standardize how agents operate on top

### 2. BU1 Brand & Content System

#### Role

Canonical rule layer for:

- tone of voice
- language rules
- channel rules
- design principles
- AI operating principles

#### Interface

- Primary interface: external URL reference
- Local support: concise operational summaries and pointers

#### Recommended usage

- always link to the live URL
- do not fork the brand system into competing local copies
- store only minimal local operational notes when needed

Source:

- [BU1 Brand & Content System](https://petrhlavacekcz.github.io/bu1-brand-design/)

## Business Intelligence Integrations

### 3. Klaviyo

#### Role

Lifecycle and CRM source for:

- campaign performance
- flow performance
- email and SMS content
- attributed revenue
- segment and profile context

#### Interfaces

- Official MCP: yes
- Official API: yes

#### Recommended usage

- use MCP for interactive exploration and account-connected workflows
- default to read-only mode first when possible
- use API or exports for batch reporting and reproducible snapshots

Sources:

- [Klaviyo MCP server](https://developers.klaviyo.com/en/docs/klaviyo_mcp_server)
- [Klaviyo API docs](https://developers.klaviyo.com/)

### 4. Google Analytics 4

#### Role

Traffic and commerce source for:

- landing pages
- engagement
- ecommerce signals
- page-level prioritization

#### Interfaces

- Official MCP: yes
- Official API: yes, Data API

#### Recommended usage

- use MCP for interactive analysis
- use Data API for repeatable reporting
- keep GA4 read-only

Sources:

- [Google Analytics MCP](https://developers.google.com/analytics/devguides/MCP)
- [Google Analytics Data API overview](https://developers.google.com/analytics/devguides/reporting/)

### 5. Google Search Console

#### Role

Search performance source for:

- impressions
- clicks
- CTR
- average position
- page and query opportunity discovery

#### Interfaces

- Official MCP: none validated for this workspace
- Official API: yes

#### Recommended usage

- use the official API directly
- materialize snapshots for reporting and prioritization
- treat GSC as read-only

Sources:

- [Search Console API overview](https://developers.google.com/webmaster-tools/about)
- [Search Console API home](https://developers.google.com/webmaster-tools)

### 6. Google Merchant Center / Merchant API

#### Role

Critical commerce visibility source for:

- product appearance on Google
- inventory and product issues
- Merchant Center-side diagnostics
- product and feed operations

#### Interfaces

- Official MCP: docs-focused MCP for Merchant API guidance
- Official API: yes, Merchant API

#### Recommended usage

- add this integration early
- use Merchant API for real account and product operations
- use the Merchant docs MCP for development help and migration guidance

Sources:

- [Merchant API overview](https://developers.google.com/merchant/api/overview)
- [Merchant API docs MCP](https://developers.google.com/merchant/api/guides/devdocs-mcp)

### 7. Microsoft Clarity

#### Role

Behavioral evidence source for:

- rage clicks
- dead clicks
- quick backs
- page friction
- URL-level diagnostics

#### Interfaces

- Official MCP: none validated for this workspace
- Official API: yes, Data Export API

#### Recommended usage

- use Clarity Data Export API for structured reporting
- use client API only if custom instrumentation becomes necessary
- keep Clarity read-only on the reporting side

Sources:

- [Clarity Data Export API](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api)
- [Clarity client API](https://learn.microsoft.com/clarity/setup-and-installation/clarity-api)

## Paid Media Integrations

### 8. Google Ads

#### Role

Paid search source for:

- campaign performance
- search term diagnostics
- ad and asset analysis
- spend-aware content prioritization

#### Interfaces

- Official MCP: yes, experimental
- Official API: yes

#### Recommended usage

- start with read-heavy diagnostics
- use the official Ads API for stable automation
- treat MCP as helpful interactive tooling, not the only integration path

Sources:

- [Google Ads MCP repo](https://github.com/googleads/google-ads-mcp)
- [Google Ads developer token docs](https://developers.google.com/google-ads/api/docs/get-started/dev-token)
- [Google Ads OAuth docs](https://developers.google.com/google-ads/api/docs/oauth/overview)

### 9. Meta / Facebook Ads

#### Role

Paid social source for:

- campaign performance
- creative diagnostics
- audience and funnel signals

#### Interfaces

- Official MCP: none validated for this workspace
- Official API: yes, Marketing API

#### Recommended usage

- use official API first
- avoid relying on unofficial MCP wrappers unless there is a strong reason and a security review
- begin with read-only reporting and diagnostics

Reference entry points:

- [Meta Marketing API docs root](https://developers.facebook.com/docs/marketing-apis)
- [Meta Business SDK repo example](https://github.com/facebook/facebook-java-business-sdk)

### 10. Sklik

#### Role

Czech paid search source for:

- campaign and ad performance
- local market paid demand
- Czech-language search context

#### Interfaces

- Official MCP: none validated for this workspace
- Official API: yes

#### Recommended usage

- use the Sklik API directly
- snapshot results for scoring and reporting
- read-only first

Source:

- [Sklik API docs](https://api.sklik.cz/)

## If MCP Is Not Available

Yes, the system can still work correctly through APIs.

MCP is useful, but it is not mandatory.

If MCP is unavailable or inappropriate, use this order:

1. official API
2. CLI, if the vendor offers one and it helps execution
3. scheduled snapshots generated from the official API

This is especially appropriate for:

- Search Console
- Merchant Center
- Clarity
- Meta Ads
- Sklik

## Skills And Local Workflow Layer

External integrations are not enough on their own.

The workspace also needs local workflow skills that tell agents how to reason and what outputs to produce.

Current BU1-local skills:

- `bu1-shopify-content-ops`
- `bu1-content-priority-orchestrator`
- `bu1-ga4-content-impact`
- `bu1-gsc-seo-priority`
- `bu1-clarity-friction-analysis`
- `bu1-klaviyo-lifecycle-content`

Current Shopify toolkit skills:

- `shopify-admin`
- `shopify-admin-execution`
- `shopify-dev`
- `shopify-custom-data`
- `shopify-storefront-graphql`
- and related Shopify API skills in `.agents/skills/`

These skills should remain vendor-agnostic in behavior even if they call vendor-specific APIs.

## CLI And Runtime Requirements

### Required now

- Shopify CLI
- Node.js for Shopify Dev MCP and related tooling

### Likely needed as integrations expand

- Python runtime for some MCP or API tooling
- OAuth-capable credential storage
- snapshot jobs or scripts for recurring data pulls

## Read / Write Policy

Default to the narrowest safe access.

### Read-only by default

- GA4
- Search Console
- Clarity
- Merchant reporting
- Google Ads diagnostics
- Meta Ads diagnostics
- Sklik diagnostics

### Selective write access

- Shopify
- Klaviyo
- Merchant Center only when a clear operational need exists

## Recommended Next Additions

If the goal is to improve BU1 content, localization, and store ops, the next additions after Shopify should be:

1. Klaviyo MCP
2. GA4
3. Google Search Console
4. Merchant API
5. Clarity
6. Google Ads
7. Meta Ads
8. Sklik

## Notes On Trust

Prefer official vendor MCP servers and official vendor APIs.

If only a third-party MCP exists, treat it as optional and higher risk.

For business-critical systems, the absence of MCP is not a blocker as long as an official API exists.
