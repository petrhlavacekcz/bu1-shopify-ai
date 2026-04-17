# BU1 Shopify Data Model

This document is the working reference for the BU1 Shopify store data model.

Goal: keep it **KISS, lean, DRY, and operational**.

Everything below is either:
- **live-verified** against `bu1rebuild.myshopify.com` via Admin GraphQL on 2026-04-17, or
- clearly marked as **not verified with current auth**.

If a field or behavior is not listed here, do not assume it exists.

---

## 1. Store Overview

| Property | Value |
|---|---|
| Shopify store | `bu1rebuild.myshopify.com` |
| Primary domain | `https://bu1.cz` |
| International domain | `https://bu1sport.com` |
| Source locale | `cs` |
| Blog 1 | `gid://shopify/Blog/82163826771` → `magazin` |
| Blog 2 | `gid://shopify/Blog/83008618579` → `nasi-brankari` |

### Published locales

Live-verified via `shopLocales`:

`cs, sk, en, de, pl, fr, es, it, hu, ro, bg, hr`

### Current resource counts

| Resource | Count | Source |
|---|---|---|
| Products | `242` | live GraphQL `productsCount` |
| Collections | `48` | live GraphQL `collectionsCount` |
| Pages | `30` | live GraphQL `pagesCount` |
| Articles | `122` | live GraphQL `articles(first: 250)` |
| Blogs | `2` | live GraphQL `blogs(first: 20)` |

### Locale routing

| Locale | URL pattern |
|---|---|
| cs | `bu1.cz` |
| sk | `bu1.cz/sk` |
| en | `bu1sport.com` |
| de | `bu1sport.com/de` |
| pl | `bu1sport.com/pl` |
| fr | `bu1sport.com/fr` |
| es | `bu1sport.com/es` |
| it | `bu1sport.com/it` |
| hu | `bu1sport.com/hu` |
| ro | `bu1sport.com/ro` |
| bg | `bu1sport.com/bg` |
| hr | `bu1sport.com/hr` |

---

## 2. Resource Types and Translatable Fields

This section answers one practical question:

**What fields can be translated in Shopify today?**

### 2.1 Live translatable fields

Verified with `translatableResourcesByIds` on live Product, Collection, Page, and Article resources.

| Resource type | Live translatable keys |
|---|---|
| PRODUCT | `title`, `body_html`, `handle`, `product_type`, `meta_description` |
| COLLECTION | `title`, `body_html`, `handle`, `meta_title`, `meta_description` |
| PAGE | `title`, `body_html`, `handle`, `meta_description` |
| ARTICLE | `title`, `body_html`, `summary_html`, `handle`, `meta_title`, `meta_description` |
| BLOG | `title`, `handle` |

### 2.2 Important workflow distinction

There are two different things:

1. **What Shopify supports as translatable**
2. **What the current BU1 batch workflow actually exports and QC-checks**

These are not identical.

### 2.3 Current BU1 batch workflow coverage

Based on the current translation export batches in `BU1_translations/2026-04-10_shopify_email_export/`:

| Content type in current export/QC workflow | Covered |
|---|---|
| PRODUCT | Yes |
| PAGE | Yes |
| ARTICLE | Yes |
| BLOG | Yes |
| PRODUCT_OPTION | Yes |
| PRODUCT_OPTION_VALUE | Yes |
| SHOP_POLICY | Yes |
| COLLECTION | **No** |

**Meaning:** collections are translatable in Shopify, but are not currently part of the standard BU1 export/QC loop.

---

## 3. Metafield Definition Counts

Live-verified via `metafieldDefinitions`.

| Owner type | Count |
|---|---|
| PRODUCT | `40` |
| COLLECTION | `6` |
| PAGE | `1` |
| ARTICLE | `1` |
| BLOG | `1` |
| PRODUCTVARIANT | `3` |
| CUSTOMER | `0` |
| ORDER | `0` |

This is the current source of truth.

Any older note that claims Customer or Order metafield definitions exist is outdated.

---

## 4. Product Data Model

## 4.1 Product metafield definitions

Live-verified product metafield definitions:

| Namespace | Key | Type | Role |
|---|---|---|---|
| `custom` | `size_guide` | `mixed_reference` | Size guide content |
| `custom` | `strih_produktu` | `single_line_text_field` | Linking key for glove cut |
| `custom` | `barva` | `single_line_text_field` | Color label |
| `custom` | `pena` | `metaobject_reference` | Foam reference |
| `custom` | `grip` | `single_line_text_field` | Grip label |
| `custom` | `strih` | `metaobject_reference` | Cut reference |
| `custom` | `modelova_rada2` | `metaobject_reference` | Model line reference |
| `custom` | `zapinani` | `metaobject_reference` | Fastening reference |
| `custom` | `short_description` | `rich_text_field` | Short description |
| `custom` | `povrch` | `list.single_line_text_field` | Surface labels |
| `custom` | `modelova_rada_produktu` | `single_line_text_field` | Linking key for model line |
| `custom` | `product_info_img_1` | `file_reference` | Info block image 1 |
| `custom` | `product_info_heading_1` | `single_line_text_field` | Info block heading 1 |
| `custom` | `product_info_text_1` | `multi_line_text_field` | Info block text 1 |
| `custom` | `product_info_heading_2` | `single_line_text_field` | Info block heading 2 |
| `custom` | `product_info_text_2` | `multi_line_text_field` | Info block text 2 |
| `custom` | `product_info_img_2` | `file_reference` | Legacy/alternate info image field |
| `custom` | `product_info_img_video_2` | `file_reference` | Info block image/video 2 |
| `custom` | `product_info_heading_3` | `single_line_text_field` | Info block heading 3 |
| `custom` | `product_info_text_3` | `multi_line_text_field` | Info block text 3 |
| `custom` | `international_href` | `metaobject_reference` | International URL mapping |
| `custom` | `badges` | `list.single_line_text_field` | Product photo badges |
| `custom` | `en_product_images` | `list.file_reference` | EN-only image set |
| `shopify` | `size` | `list.metaobject_reference` | Shopify taxonomy |
| `shopify` | `color-pattern` | `list.metaobject_reference` | Shopify taxonomy |
| `shopify` | `fabric` | `list.metaobject_reference` | Shopify taxonomy |
| `shopify` | `activity` | `list.metaobject_reference` | Shopify taxonomy |
| `shopify` | `waist-rise` | `list.metaobject_reference` | Shopify taxonomy |
| `shopify` | `target-gender` | `list.metaobject_reference` | Shopify taxonomy |
| `shopify` | `pants-length-type` | `list.metaobject_reference` | Shopify taxonomy |
| `shopify` | `activewear-clothing-features` | `list.metaobject_reference` | Shopify taxonomy |
| `shopify` | `handwear-material` | `list.metaobject_reference` | Shopify taxonomy |
| `shopify` | `age-group` | `list.metaobject_reference` | Shopify taxonomy |
| `shopify--discovery--product_search_boost` | `queries` | `list.single_line_text_field` | Search boost |
| `shopify--discovery--product_recommendation` | `related_products` | `list.product_reference` | Related products |
| `shopify--discovery--product_recommendation` | `related_products_display` | `single_line_text_field` | Related display mode |
| `shopify--discovery--product_recommendation` | `complementary_products` | `list.product_reference` | Complementary products |
| `reviews` | `rating` | `rating` | Judge.me / reviews |
| `reviews` | `rating_count` | `number_integer` | Judge.me / reviews |
| `seo` | `hidden` | `number_integer` | Noindex flag |

## 4.2 Product instance fields observed live

Sample live product:
- `gid://shopify/Product/7206854688851`
- handle: `junior-bu1-light-hg`

Observed values:

| Field | Live value |
|---|---|
| `custom.barva` | `Černá` |
| `custom.povrch` | `["Na umělou trávu"]` |
| `custom.grip` | `HG grip` |
| `custom.strih_produktu` | `Junior` |
| `custom.modelova_rada_produktu` | `Light ` |
| `localesAI.translations` | `{}` |

This confirms:
- the product linking fields are really used
- `custom.grip` is real and active
- the trailing-space issue on `Light ` is real

## 4.3 Product instance-only keys observed live

On the sampled product, these keys exist as metafield instances even though they are not visible in the current `metafieldDefinitions` result set:

| Namespace | Key | Note |
|---|---|---|
| `custom` | `modelova_rada` | Legacy or protected definition visibility |
| `custom` | `travnata_hriste` | Legacy or protected definition visibility |
| `localesAI` | `translations` | Residual app data |
| `judgeme` | `badge` | Third-party app |
| `judgeme` | `widget` | Third-party app |

Treat these as real store data, even if the corresponding definition is not visible through current auth.

## 4.4 Product fields missing from current translation workflow

These are real product definitions, customer-visible, and currently outside the standard BU1 translation export/QC loop:

| Field group | Fields |
|---|---|
| Short description | `custom.short_description` |
| Info blocks | `custom.product_info_heading_1/2/3`, `custom.product_info_text_1/2/3` |
| Product labels | `custom.barva`, `custom.povrch`, `custom.grip`, `custom.badges` |

Operational meaning:
- if these fields appear on storefront templates, they are a localization gap
- they are not solved by `translationsRegister` on standard product fields alone

---

## 5. Product Variant Data Model

Live-verified variant metafield definitions:

| Namespace | Key | Type | Role |
|---|---|---|---|
| `custom` | `nejnizsi_cena_za_30_dni` | `number_integer` | Omnibus price history |
| `custom` | `voc_czk` | `money` | Cost-related field |
| `custom` | `svoc_czk` | `money` | Cost-related field |

Do not assume variants only carry the 30-day price field. There are currently three definitions.

---

## 6. Collection Data Model

## 6.1 Collection metafield definitions

Live-verified collection metafield definitions:

| Namespace | Key | Type | Role |
|---|---|---|---|
| `custom` | `parent_collection` | `collection_reference` | Collection hierarchy |
| `custom` | `international` | `metaobject_reference` | International routing |
| `custom` | `active_filters_bar_labels` | `single_line_text_field` | Preferred filter labels |
| `custom` | `collection_banner` | `file_reference` | Desktop banner |
| `custom` | `collection_banner_mobile` | `file_reference` | Mobile banner |
| `seo` | `hidden` | `number_integer` | Noindex flag |

## 6.2 Collection instance behavior observed live

Live-verified across all `48` collections:

- `custom.active_filters_bar_labels` is currently `null` on all collections
- `localesAI.translations` exists on `22 / 48` collections

This means:
- `active_filters_bar_labels` is a potential localization gap, not an active one today
- Locales.AI residue is not limited to products

## 6.3 Collection translation reality

Collections are live-translatable in Shopify:

`title`, `body_html`, `handle`, `meta_title`, `meta_description`

But collections are **not** currently part of the BU1 translation export/QC workflow.

---

## 7. Article, Blog, and Page Data Model

## 7.1 Definitions

Live-verified definitions:

| Owner type | Definition |
|---|---|
| PAGE | `custom.international_href` |
| ARTICLE | `custom.international_href` |
| BLOG | `custom.international_href` |

## 7.2 Live translation behavior

| Resource | Live translatable keys |
|---|---|
| PAGE | `title`, `body_html`, `handle`, `meta_description` |
| ARTICLE | `title`, `body_html`, `summary_html`, `handle`, `meta_title`, `meta_description` |
| BLOG | `title`, `handle` |

## 7.3 Blogs currently present

| Handle | Title | GID |
|---|---|---|
| `magazin` | `Magazín` | `gid://shopify/Blog/82163826771` |
| `nasi-brankari` | `Naši brankáři` | `gid://shopify/Blog/83008618579` |

---

## 8. Metaobject-Backed Fields

The following live-verified metafields are `metaobject_reference` and therefore depend on metaobject data behind them:

| Owner | Field |
|---|---|
| PRODUCT | `custom.pena` |
| PRODUCT | `custom.strih` |
| PRODUCT | `custom.modelova_rada2` |
| PRODUCT | `custom.zapinani` |
| PRODUCT | `custom.international_href` |
| COLLECTION | `custom.international` |
| PAGE | `custom.international_href` |
| ARTICLE | `custom.international_href` |
| BLOG | `custom.international_href` |

### Current limitation

`metaobjectDefinitions` returned an empty result with current store auth.

So:
- the existence of these references is **verified**
- the internal field structure of the referenced metaobjects is **not verified via current API auth**

Do not treat any older UI-derived metaobject field maps as authoritative unless they are re-verified.

---

## 9. SEO Layer

Use the resource's translatable SEO fields where available.

| Resource | Live translatable SEO keys |
|---|---|
| PRODUCT | `meta_description` |
| COLLECTION | `meta_title`, `meta_description` |
| PAGE | `meta_description` |
| ARTICLE | `meta_title`, `meta_description` |

### Important note

On live resources, Shopify also stores some SEO data in instance metafields like:
- `global.title_tag`
- `global.description_tag`

Operational rule:
- treat `translatableContent` keys such as `meta_title` and `meta_description` as the write interface for localization work
- do not manually write `global.*` metafields unless there is a specific reason and a verified workflow for it

### Noindex

`seo.hidden` exists on products and collections.

Operational rule:
- do not change it without explicit human approval

---

## 10. Translation System Implications

This is the practical summary for agents and scripts.

### 10.1 Safe write surfaces

| Data type | Write method |
|---|---|
| Standard translatable resource fields | `translationsRegister` |
| Non-translatable metafield content | `metafieldsSet` |
| Product/collection/page/article/blog content state | read first, then mutate only if explicitly asked |

### 10.2 What the current system does well

- product/page/article/blog translation flow is real and working
- resource digests can be read live and used safely with `translationsRegister`
- current docs around translation QC are directionally correct

### 10.3 What is currently outside the main loop

| Area | Why it matters |
|---|---|
| Collection translations | Shopify supports them, BU1 export/QC flow does not include them |
| Product content metafields | storefront-visible text lives outside standard translatable resource fields |
| Metaobject text | fields behind metaobject references are not verified with current auth |

---

## 11. Operational Rules

### Read before write

Always:
- read the current resource first
- read current `translatableContent` digests before `translationsRegister`
- read current metafield values before `metafieldsSet`

### Do write

- standard content translations via `translationsRegister`
- customer-visible text metafields only when you are explicitly updating those fields

### Do not write

- `custom.international_href`
- `custom.international`
- `seo.hidden` without approval
- Judge.me fields
- Shopify taxonomy fields unless explicitly instructed
- residual `localesAI.translations`

### Do not assume

- that current batch exports cover everything translatable
- that a visible metafield instance always has a visible definition in current auth
- that metaobject internals are known just because references exist

---

## 12. Known Issues and Cleanup

Only live-verified or workflow-verified items are listed here.

| Issue | Priority | Why |
|---|---|---|
| Product content metafields are outside main translation workflow | High | Customer-visible text can remain untranslated |
| Collections are translatable in Shopify but not in current BU1 export/QC loop | High | Real translation surface not covered by current operations |
| `custom.modelova_rada_produktu` contains `Light ` with trailing space | Medium | Confirms data quality inconsistency in linking keys |
| `localesAI.translations` exists on products and `22/48` collections | Medium | Residual app data should not remain part of active model |
| `custom.active_filters_bar_labels` is defined but unused | Low | Keep in model, but not an active translation gap today |
| Metaobject internals are not verified with current auth | High | Limits safe automation on referenced custom data |

---

## 13. Minimal Working Mental Model

If you only remember one thing, use this:

1. **Core content translation** lives on Product, Collection, Page, Article, Blog resources.
2. **Extra storefront text** also lives in `custom.*` metafields on products and collections.
3. **Routing/hreflang logic** lives in `custom.international_href` / `custom.international` references and should be treated as protected.
4. **Metaobject references exist**, but their internal schemas are not currently verified through API auth.
5. **Collections are first-class translatable resources**, even though the current BU1 workflow does not treat them that way yet.
