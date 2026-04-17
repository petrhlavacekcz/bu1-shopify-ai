# BU1 Agent Workflows

This file maps tasks to the right documentation. Read the linked doc before starting any workflow.

## Project Overview

BU1 is a Czech goalkeeping equipment brand. This project manages content and translations for the Shopify store across 12 locales (cs = source + 11 translations).

- **Czech store**: bu1.cz
- **International store**: bu1sport.com
- **Shopify CLI store**: bu1rebuild.myshopify.com

**Why read this first:** Google Ads běží — brand i non-brand search (CZ + SK brankářské rukavice bez brandu, obecná kw), PMax Shopping, display remarketing. Blog je klíčový organický kanál, ale placená akvizice je aktivní. Každé obsahové a překladové rozhodnutí má přímý komerční dopad.

See [`docs/goals.md`](docs/goals.md) for full business context, KPIs, and success criteria.

---

## Workflow Index

| Task | Primary Doc | Also Read |
|---|---|---|
| Write blog article | [`docs/blog-articles.md`](docs/blog-articles.md) | [`docs/brand.md`](docs/brand.md), `config/article_generator.json`, [`docs/goals.md`](docs/goals.md) |
| Translate content | [`docs/translations.md`](docs/translations.md) | [`docs/brand.md`](docs/brand.md), [`docs/shopify-data-model.md`](docs/shopify-data-model.md) |
| QC translation batch | [`docs/translations.md`](docs/translations.md) | [`docs/shopify-data-model.md`](docs/shopify-data-model.md) |
| Inspect or update Shopify data model | [`docs/shopify-data-model.md`](docs/shopify-data-model.md) | — |
| Upload / sync articles to Shopify | [`docs/blog-articles.md`](docs/blog-articles.md) § Shopify Upload Workflow | `scripts/upload_blog_articles.mjs`, `scripts/validate_blog_images.py` |
| Create content brief | [`docs/content-brief-template.md`](docs/content-brief-template.md) | [`docs/topic-cluster-map.md`](docs/topic-cluster-map.md), [`docs/goals.md`](docs/goals.md) |
| Generate blog images | [`docs/blog-photography.md`](docs/blog-photography.md) | [`docs/brand.md`](docs/brand.md) |
| Social media post | [`docs/brand.md`](docs/brand.md) | — |
| SEO keyword analysis | [`docs/keyword-gap-analysis-2026-04-10.md`](docs/keyword-gap-analysis-2026-04-10.md) | [`docs/topic-cluster-map.md`](docs/topic-cluster-map.md) — note: GSC now live, re-rank from data |
| Monthly SEO review | [`docs/monitoring-loop.md`](docs/monitoring-loop.md) | [`docs/goals.md`](docs/goals.md) |
| Automate billing / iDoklad invoicing | [`docs/skills-roadmap.md`](docs/skills-roadmap.md) | [`docs/integrations-catalog.md`](docs/integrations-catalog.md) |
| Review strategic decisions | [`CHANGELOG.md`](CHANGELOG.md) | [`docs/goals.md`](docs/goals.md) |
| Plan new integrations | [`docs/integrations-catalog.md`](docs/integrations-catalog.md) | [`docs/integration-blueprint.md`](docs/integration-blueprint.md) |
| Plan new skills | [`docs/skills-roadmap.md`](docs/skills-roadmap.md) | — |
| Explore growth ideas / new tools | [`docs/growth-backlog.md`](docs/growth-backlog.md) | [`docs/integrations-catalog.md`](docs/integrations-catalog.md) |
| Product content brief | [`docs/product-brief.md`](docs/product-brief.md) | [`docs/brand.md`](docs/brand.md) |
| Read or write a report | [`reports/index.md`](reports/index.md) | [`docs/reports-guide.md`](docs/reports-guide.md) |

---

## Shared Resources

| Resource | Path | What It Contains |
|---|---|---|
| Brand design system | https://petrhlavacekcz.github.io/bu1-brand-design/ | **Source of truth** for brand voice, colors, typography |
| Goalkeeper Glossary | [`config/goalkeeper_glossary.json`](config/goalkeeper_glossary.json) | Standardized goalkeeper slang & technical terms for all 12 locales |
| Brand config | `config/article_generator.json` | Colors, typography, tone, sitemaps, internal links, evergreen pages, market SEO tiers |
| Brand docs | [`docs/brand.md`](docs/brand.md) | Brand voice, forbidden terms, audiences (derived from brand design system) |
| Goals & KPIs | [`docs/goals.md`](docs/goals.md) | WHY this project exists, business goals, KPI baselines, success criteria framework |
| System Capabilities | [`docs/system-capabilities.md`](docs/system-capabilities.md) | What the current system CAN do (Capability Map), ideas for immediate use |
| Topic clusters | [`docs/topic-cluster-map.md`](docs/topic-cluster-map.md) | Blog topic clusters, editorial rules, data-confirmed priority (updated 2026-04-16) |
| Content brief template | [`docs/content-brief-template.md`](docs/content-brief-template.md) | Template for content briefs including market_keywords and success_criteria |
| Decision log | [`CHANGELOG.md`](CHANGELOG.md) | What changed, why, what data drove it, expected impact |
| Monitoring loop | [`docs/monitoring-loop.md`](docs/monitoring-loop.md) | Monthly GSC/GA4 review protocol and quarterly strategy drift detection |
| iDoklad API docs | https://api.idoklad.cz/Help/v3/cs/ | Official auth, contacts, invoices, payments, webhook, and filtering reference |
| QC validation script | `scripts/validate_translations.py` | Offline CSV validation for translation batches |
| Blog image validator | `scripts/validate_blog_images.py` | Checks article image count, placement, alt text metadata, and hero/inline structure before upload |
| Article upload script | `scripts/upload_blog_articles.mjs` | Create / update articles + register translations via Shopify CLI |
| Translation exports | `BU1_translations/` | Dated Shopify e-mail export batches |
| Reports | [`reports/index.md`](reports/index.md) | All data, SEO, translation, and strategy reports. Format: `docs/reports-guide.md` |

---

## Data Integrations

All integrations are live as of 2026-04-16. Use them before making content or strategy decisions.

| Source | What it answers | MCP available | Last used |
|---|---|---|---|
| Google Search Console (bu1.cz + bu1sport.com) | Which queries get impressions but not clicks? Where is the organic gap? | Yes (`mcp__gsc__*`) | 2026-04-16 |
| Google Analytics 4 | Which pages get traffic? What's the bounce rate? | Yes (`mcp__google-analytics-mcp__*`) | 2026-04-16 |
| Klaviyo | Which email topics resonate? What flows are live? | Yes (`mcp__claude_ai_Klaviyo__*`) | 2026-04-16 |
| Google Ads | Which campaigns are active? What's the paid demand signal? | Yes (`mcp__google-ads-mcp__*`) | 2026-04-16 |

**Key signal as of April 2026:** Google Ads aktivní — brand (CZ + SK), non-brand search (brankářské rukavice bez brandu CZ + SK, obecná kw), PMax Shopping, display remarketing (DRTG 0-3, 13-30 dní). Blog = klíčový organický kanál vedle placené akvizice.

---

## Sitemaps

| Scope | URL |
|---|---|
| CZ + SK | https://bu1.cz/sitemap.xml |
| EN + 9 locales | https://bu1sport.com/sitemap.xml |

---

## Shopify Store

- **Store ID**: `bu1rebuild.myshopify.com`
- **Blog**: Magazín (`gid://shopify/Blog/82163826771`)
- **Locales**: cs (source), sk, en, de, pl, fr, es, it, hu, ro, bg, hr
- **Priority locales** (100% coverage): EN, DE, PL, SK
- **CLI auth**: `shopify store auth --store bu1rebuild.myshopify.com --scopes <needed_scopes>`
- **Execute**: `shopify store execute --store bu1rebuild.myshopify.com --allow-mutations --query '...' --variables '...'`
- **QC script**: `python3 scripts/validate_translations.py --input BU1_translations/<batch-dir>`

---

## Market SEO Tiers

Goalkeeper content must be localized (not just translated) for tier-1 and tier-2 markets. See `config/article_generator.json` → `market_seo_tiers` and `docs/blog-articles.md` → Market Keyword Localization.

| Tier | Locales | Rule |
|---|---|---|
| 1 — always validate | sk, hu, de | Validate primary keyword before writing. Fill `market_keywords` in frontmatter. |
| 2 — validate for goalkeeper content | ro, hr, pl | Validate for clusters 1–3. |
| 3 — translate is sufficient | en, fr, es, it, bg | Translate keyword. No pre-validation required. |

---

## Staying Current

**Monthly:** Ask your AI — *"Spusť měsíční SEO review dle docs/monitoring-loop.md."* Works with any agent. Produces a report in `reports/`, proposes changes, waits for approval.

**Quarterly:** Same command, extended — includes cluster priority and KPI baseline review.

**After any strategic change:** Add a CHANGELOG entry. If it's not in `CHANGELOG.md`, future sessions won't know why something was done.

**Rule:** `agents.md` must reflect current reality. If a doc, workflow, or integration is added and `agents.md` doesn't mention it, it doesn't exist for future sessions.
