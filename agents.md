# BU1 Agent Workflows

This file maps tasks to the right documentation. Read the linked doc before starting any workflow.

## Project Overview

BU1 is a Czech goalkeeping equipment brand. This project manages content and translations for the Shopify store across 12 locales (cs = source + 11 translations).

- **Czech store**: bu1.cz
- **International store**: bu1sport.com
- **Shopify CLI store**: bu1rebuild.myshopify.com

## Workflow Index

| Task | Primary Doc | Also Read |
|---|---|---|
| Write blog article | [`docs/blog-articles.md`](docs/blog-articles.md) | [`docs/brand.md`](docs/brand.md), `config/article_generator.json` |
| Translate content | [`docs/translations.md`](docs/translations.md) | [`docs/brand.md`](docs/brand.md) |
| QC translation batch | [`docs/translations.md`](docs/translations.md) | — |
| Upload / sync articles to Shopify | [`docs/blog-articles.md`](docs/blog-articles.md) § Shopify Upload Workflow | `scripts/upload_blog_articles.mjs` |
| Create content brief | [`docs/content-brief-template.md`](docs/content-brief-template.md) | [`docs/topic-cluster-map.md`](docs/topic-cluster-map.md) |
| Generate blog images | [`docs/blog-photography.md`](docs/blog-photography.md) | [`docs/brand.md`](docs/brand.md) |
| Social media post | [`docs/brand.md`](docs/brand.md) | — |

## Shared Resources

| Resource | Path | What It Contains |
|---|---|---|
| Brand design system | https://petrhlavacekcz.github.io/bu1-brand-design/ | **Source of truth** for brand voice, colors, typography |
| Brand config | `config/article_generator.json` | Colors, typography, tone, sitemaps, internal links, evergreen pages |
| Brand docs | [`docs/brand.md`](docs/brand.md) | Brand voice, forbidden terms, audiences (derived from brand design system) |
| Topic clusters | [`docs/topic-cluster-map.md`](docs/topic-cluster-map.md) | Blog topic clusters and editorial rules |
| Content brief template | [`docs/content-brief-template.md`](docs/content-brief-template.md) | Template for content briefs |
| QC validation script | `scripts/validate_translations.py` | Offline CSV validation for translation batches |
| Article upload script | `scripts/upload_blog_articles.mjs` | Create / update articles + register translations via Shopify CLI |
| Translation exports | `BU1_translations/` | Dated Shopify e-mail export batches |

## Sitemaps

| Scope | URL |
|---|---|
| CZ + SK | https://bu1.cz/sitemap.xml |
| EN + 9 locales | https://bu1sport.com/sitemap.xml |

## Shopify Store

- **Store ID**: `bu1rebuild.myshopify.com`
- **Blog**: Magazín (`gid://shopify/Blog/82163826771`)
- **Locales**: cs (source), sk, en, de, pl, fr, es, it, hu, ro, bg, hr
- **Priority locales** (100% coverage): EN, DE, PL, SK
- **CLI auth**: `shopify store auth --store bu1rebuild.myshopify.com --scopes <needed_scopes>`
- **Execute**: `shopify store execute --store bu1rebuild.myshopify.com --allow-mutations --query '...' --variables '...'`
- **QC script**: `python3 scripts/validate_translations.py --input BU1_translations/<batch-dir>`
