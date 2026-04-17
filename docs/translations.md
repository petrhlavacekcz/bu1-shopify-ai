# BU1 Translations

Brand rules and terminology: see [`docs/brand.md`](brand.md)

## Store Domains

| Locale | Store URL |
|---|---|
| cs | bu1.cz |
| sk | bu1.cz/sk |
| en | bu1sport.com |
| de, pl, fr, es, it, hu, ro, bg, hr | bu1sport.com/{locale} |

Sitemaps: bu1sport.com/sitemap.xml (EN + 9 locales) | bu1.cz/sitemap.xml (CZ + SK)

## Translation Data

- **Source**: Shopify e-mail export batches in `BU1_translations/`
- **Content types**: ARTICLE, BLOG, PAGE, PRODUCT, PRODUCT_OPTION, PRODUCT_OPTION_VALUE, SHOP_POLICY
- **Fields**: title, body_html, handle, meta_description, meta_title, summary_html, name, product_type, body
- **Locales**: bg, de, en, es, fr, hr, hu, it, pl, ro, sk

## Quality Checklist

When creating or reviewing translations, verify:

1. **Correct domain in links** — bu1sport.com for all non-Czech locales (never bu1.cz)
2. **Formal register** — formal "you" in all languages (Sie/Pan/Vy, never du/ty/tu)
3. **Goalkeeper Slang per glossary** — ALWAYS use [`config/goalkeeper_glossary.json`](../config/goalkeeper_glossary.json) for technical terms (latex, cuts, saves, etc.)
4. **Terminology consistency** — consistent terms (football, not soccer; goalkeeper, not goalie)
5. **No forbidden terms** — no Czech words leaking into translations (fotbal, brankářské, rukavice, brankář) and no forbidden terms from the glossary (e.g., no "Schaumstoff" in DE)
5. **Meta description matches correct product** — no copy-paste errors from other products
6. **No duplicate text** — translation must differ from Czech default (flag identical content)
7. **Localized, not literal** — adapt for target market while keeping brand voice

## Localization vs. Translation Rules

### Translate (adapt, not literally):
- Product descriptions, meta descriptions, UI texts
- Blog articles and page content
- CTA phrases appropriate for each market

### Localize (change for target market):
- URL handles (localized slugs)
- Currency references
- Contact details and store information
- CTA phrases (culturally appropriate)

### Do NOT translate:
See `docs/brand.md` → "Do NOT Translate" section

## Required Fields Per Content Type

| Content Type | Required Fields |
|---|---|
| PRODUCT | title, body_html, meta_description, handle |
| PAGE | title, body_html, meta_description, handle |
| ARTICLE | title, body_html, summary_html, handle |
| BLOG | title, handle |
| PRODUCT_OPTION | name |
| PRODUCT_OPTION_VALUE | name |
| SHOP_POLICY | body |

## Coverage Targets

- **100%** for priority locales: EN, DE, PL, SK
- **95%+** for other locales: BG, ES, FR, HR, HU, IT, RO

## QC Scripts

```bash
# Full check for one export batch
python3 scripts/validate_translations.py --input BU1_translations/<batch-dir>

# Filter by locale or content type
python3 scripts/validate_translations.py --input BU1_translations/<batch-dir> --locale de --type PRODUCT --verbose

# Coverage summary only
python3 scripts/validate_translations.py --input BU1_translations/<batch-dir> --summary

# Export report
python3 scripts/validate_translations.py --input BU1_translations/<batch-dir> --report reports/qc_$(date +%Y%m%d).csv
```

## Market Keyword Localization

See `docs/blog-articles.md` → **Market Keyword Localization** for the full rules, tier system, and GSC signals.

**Short rule:** if `market_keywords[locale]` exists in source frontmatter → H1, seo_title, and opening sentence use that phrase, not a translated version of the Czech keyword.

## Surgical Translation Updates

When a published Czech article is updated, **do not regenerate all translations**. Only update what changed.

### Protocol

1. Identify what changed in the Czech source: which section(s), which fields (body, H2, meta title)?
2. For each translation: update only the corresponding section(s) in that locale
3. If only `seo_title` changed in Czech → update only `seo_title` in each translation (9 words, not 1200)
4. If a new H2 section was added → translate only that section and insert in the correct position
5. Re-run link validation only for the changed section

### Why this matters

Regenerating a full translation risks introducing regressions — a validated localized keyword in H1 may get overwritten, or a carefully placed internal link may move. Surgical updates preserve the work already done.

### When to regenerate fully

- Article is restructured (H2 order changed, major sections added/removed)
- Primary keyword changed
- More than 40% of body content changed

## Translation Depth Rules

When translating articles or content:

- **Preserve ALL facts** — numbers, statistics, player names, club names, sources stay unchanged
- **URLs in links stay unchanged** — translate the anchor text, never modify the href URL
- **Localize internal links** — replace Czech internal links with the correct localized URL for the target locale (see `docs/blog-articles.md` → Internal Linking)
- **Cultural adaptation** — adapt idioms, metaphors, and culturally specific references for the target market where appropriate
- **No mechanical translation** — the result must read naturally to a native speaker
- **Formal register always** — Sie (DE), Pan/Pani (PL), Vy (SK), vous (FR), usted (ES), Lei (IT), Ön (HU), dumneavoastră (RO), Вие (BG), Vi (HR)

## Link Validation in Translations (mandatory QC step)

Before registering a translation via `translationsRegister`, verify:

1. **Every internal link in the translated body_html** uses the correct localized URL for that locale
2. **Handle matches** the localized handle from `config/article_generator.json` → `evergreen_pages`
3. **Domain is correct** — bu1sport.com/{locale} for all non-Czech locales (never bu1.cz)
4. **No leftover Czech links** — no bu1.cz URLs in non-Czech/Slovak translations
5. **If a localized handle doesn't exist** for the target locale, remove the link — better no link than a 404

## Shopify API Workflow

- Store: `bu1rebuild.myshopify.com`
- Auth: `shopify store auth --store bu1rebuild.myshopify.com --scopes write_translations`
- Register translations: `translationsRegister` mutation via `shopify store execute`
- Query translatable resources: `translatableResourcesByIds` query to get digest values
