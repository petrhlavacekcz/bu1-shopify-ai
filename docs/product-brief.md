# BU1 Shopify AI Ops — Product Brief

## Purpose

Define the real product goal of this workspace so the system does not drift into a narrow "CSV validator" or "single-agent prompt repo".

This workspace is an internal operations layer for BU1 over Shopify, brand rules, and performance data.

Its job is to help humans and AI agents do store content work safely, consistently, and with business context.

## Product Definition

**BU1 Shopify AI Ops** is an agent-agnostic operational workspace that connects Shopify, the BU1 Brand & Content System, and selected business data sources so agents can:

- write and publish blog content
- localize and review translations
- update products, pages, articles, SEO metadata, and structured content
- execute safe admin operations in Shopify
- prioritize work using traffic, SEO, lifecycle, and UX signals

The product is not tied to one model vendor or one assistant runtime.

## Agent-Agnostic Requirement

This system must work with multiple agent surfaces, including:

- Claude
- ChatGPT / Codex
- Gemini CLI
- GLM
- OpenRouter-backed agents
- Hugging Face-based agents and workflows

Therefore the workspace must prefer:

- portable documentation
- explicit workflows
- file-based source-of-truth documents
- standard interfaces such as MCP where useful
- direct APIs and snapshots where MCP is not available or not the best fit

The workspace must avoid assumptions that only one assistant can read one special file or use one proprietary integration path.

## Primary Goal

Enable high-quality BU1 store operations with AI assistance, where every output is aligned with:

- the live Shopify store state
- the BU1 brand and content rules
- the relevant locale and market
- the highest-priority business opportunities or defects

## Core Jobs To Be Done

### 1. Content Operations

Create, improve, and publish blog and page content that matches BU1 brand rules and SEO intent.

Examples:

- propose article topics
- draft blog articles
- save articles as Shopify drafts
- update SEO title and meta description
- add relevant internal links

### 2. Localization Operations

Review, improve, and validate translations for products, pages, articles, policies, and related content.

Examples:

- detect missing translation fields
- detect untranslated or duplicated text
- detect domain mistakes and Czech leakage
- prepare corrections for Shopify

### 3. Store Administration Operations

Execute safe Shopify-side changes with validation and traceability.

Examples:

- update product copy
- edit handles
- update metafields
- create or update blog articles
- inspect current store content before changing it

### 4. Prioritization Operations

Decide what to write, fix, translate, or refresh first based on real signals.

Examples:

- pages with high impressions and weak CTR
- pages with traffic and poor conversion
- lifecycle messages with revenue impact and stale copy
- high-friction pages in Clarity

## Non-Goals

This workspace is **not** meant to become:

- a master database of all Shopify content
- a custom CMS replacement for Shopify
- a file merger that tries to normalize every Shopify export into one canonical CSV
- a vendor-specific prompt pack for one model only
- a passive archive of exports with no operational workflows attached

## Source Of Truth Policy

The system must be explicit about what is canonical and what is derived.

### Canonical Sources

#### 1. Shopify

Canonical for:

- products
- pages
- blog articles
- blog handles
- SEO metafields
- publication state
- translation state as stored in Shopify

#### 2. BU1 Brand & Content System

Canonical for:

- tone of voice
- language rules
- communication channel rules
- brand language
- design principles
- tokenized design decisions
- AI/content operating principles

Source:

- [BU1 Brand & Content System](https://petrhlavacekcz.github.io/bu1-brand-design/)

#### 3. Analytics And Performance Sources

Canonical for their own domain:

- GA4 for traffic and engagement
- Google Search Console for search demand and CTR
- Klaviyo for lifecycle and email performance
- Clarity for UX friction and behavioral evidence

### Derived / Snapshot Inputs

Not canonical, but operationally useful:

- Shopify CSV exports from e-mail
- exported reports
- normalized local snapshots
- scored backlog outputs

These exist to support QA, reproducibility, and audits.
They must not be mistaken for the main source of truth.

## Data Source Policy

### Tier 1: Required

- Shopify Admin data and operations
- BU1 Brand & Content System

Without these two, the workspace cannot do correct content or admin work.

### Tier 2: Strongly Recommended

- Google Search Console
- GA4
- Klaviyo
- Clarity

These unlock prioritization and business context.

### Tier 3: Optional / Future

- Storefront MCP
- Customer Accounts MCP
- additional experimentation or merchandising data sources

These are valuable later, but not required for the core operating model.

## Workflow Model

Every meaningful workflow should follow this order:

1. Read the canonical rule layer.
2. Read the current Shopify or data-state layer.
3. Decide the target action.
4. Generate a proposed output or operation.
5. Validate it against rules and store context.
6. Execute only if the workflow allows execution.
7. Record the result in a stable artifact when useful.

This mirrors the brand system principle:

- first rule
- then context
- then output

## Portable Interface Strategy

To stay agent-agnostic, the workspace should split interfaces into three categories.

### 1. Human-Readable Rules

Examples:

- `CLAUDE.md`
- brand and content docs
- topic maps
- briefs
- workflow notes

These must remain readable without special tooling.

### 2. Agent Connectors

Examples:

- MCP servers
- Shopify Dev MCP
- future MCP bridges

Use these where they provide strong value for discovery, validation, or execution.

### 3. Direct APIs And Snapshots

Examples:

- Shopify Admin API
- GA4 Data API
- Search Console API
- Klaviyo APIs
- Clarity exports
- CSV export batches

These are the portability fallback and, in many cases, the more stable reporting layer.

## CSV Export Policy

Shopify e-mail exports can arrive as multiple CSV attachments for one export event.

Therefore:

- one export event may map to multiple CSV files
- the system must treat that set as one batch
- the system must not require manual merging into one master CSV
- the system must not split and reshape those files unless there is a very specific downstream need

CSV exports are an audit input, not the center of the product.

## Content System Requirement

The workspace must support a repeatable content production process:

1. topic discovery
2. intent definition
3. brand-aligned brief
4. article drafting
5. internal linking
6. Shopify draft creation
7. translation and localization
8. QA
9. performance review and refresh

This process must work regardless of which agent produced the first draft.

## Translation System Requirement

The workspace must support a repeatable localization QA process:

1. collect the current snapshot or store data
2. detect structural and linguistic issues
3. map issues to specific resources and locales
4. decide which issues matter most
5. prepare or execute Shopify-side fixes
6. re-check after changes

## Store Ops Requirement

The workspace must support safe Shopify execution:

- read before write
- narrow scope
- validated GraphQL or operation design
- explicit store target
- explicit publication state
- clear output artifacts for drafts and updates

## Architecture Direction

This workspace should evolve into four coordinated layers:

### 1. Rule Layer

- brand system
- content rules
- SEO rules
- localization rules
- workflow guardrails

### 2. Execution Layer

- Shopify Dev MCP
- Shopify Admin API / Admin execution
- draft and publish operations
- admin update workflows

### 3. Evidence Layer

- CSV export batches
- GA4
- GSC
- Klaviyo
- Clarity
- derived reports

### 4. Decision Layer

- prioritization logic
- ranked backlog
- recommended next action
- explanation of why a task matters

## Success Criteria

The product is working when an agent or human can reliably:

1. identify what should be worked on next
2. explain why it matters
3. trace the task to a specific source of truth
4. generate a valid content or admin action
5. execute it safely in Shopify when allowed
6. keep outputs aligned with BU1 brand and content rules

## Failure Modes To Prevent

The product has failed if:

- exports become the fake source of truth
- multiple documents redefine the same rule differently
- one agent runtime gets privileged treatment and others become second-class
- outputs are generated without reading the rule layer
- store operations happen without reading current state first
- analytics are present but not used to prioritize work

## One-Sentence Mission

Build a portable BU1 AI operations workspace that lets any capable agent work on Shopify content and admin tasks using shared rules, shared evidence, and shared execution guardrails.
