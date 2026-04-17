# BU1 Blog Articles

Brand rules: see [`docs/brand.md`](brand.md)
Translation workflow: see [`docs/translations.md`](translations.md)

## Blog Info

- **Blog**: Magazín (`gid://shopify/Blog/82163826771`)
- **Evergreen pages & internal links**: `config/article_generator.json` → `evergreen_pages` section
- **Topic clusters**: [`docs/topic-cluster-map.md`](topic-cluster-map.md)
- **Content brief template**: [`docs/content-brief-template.md`](content-brief-template.md)
- **Photography**: [`docs/blog-photography.md`](blog-photography.md)

## Article Creation Workflow

1. Read `config/article_generator.json` for brand voice, internal links, SEO rules
1b. **[Clusters 1–3 only] Run Gemini deep research** before creating the draft — see **Deep Research Protocol** below
2. Create a draft file in `drafts/blog/YYYY-MM-DD-<handle>.md` using the **Draft File Format** below (frontmatter = content brief + SEO + metadata, single source of truth)
3. Assign to a topic cluster from [`docs/topic-cluster-map.md`](topic-cluster-map.md) via `cluster` field
4. **Validate market keywords** for tier-1 and tier-2 locales (see **Market Keyword Localization** below). Add validated local search phrasing to `market_keywords` in frontmatter before writing the Czech article — translations depend on it.
5. Select 1-3 relevant internal links from `evergreen_pages` in config
6. Add `related_articles` — at least 1 link to another article from the same or adjacent cluster (see **Inter-Article Linking** below)
7. Write Czech article: H1 with keyword, 4-6× H2, min 1200 slov (pokud není zadáno jinak)
8. Apply brand voice from [`docs/brand.md`](brand.md)
9. Plan article visuals in `images` using [`docs/blog-photography.md`](blog-photography.md) and run `python3 scripts/validate_blog_images.py <draft>`
10. Save as draft via Shopify `articleCreate` mutation (`isPublished: false`)
11. Include SEO metafields (`global.title_tag`, `global.description_tag`)
12. Generate translations for all 11 locales (see [`docs/translations.md`](translations.md))
13. **Validate all links** in Czech article and every translation (see Link Validation below)
14. Validate against Translation Quality Checklist

## Draft File Format

Every draft lives in `drafts/blog/YYYY-MM-DD-<handle>.md`. **One file = one article = one source of truth.** Frontmatter replaces the old separate content brief.

```md
---
# Identity
title: Rozehrávka brankáře nohama
handle: rozehravka-brankare-nohama
locale: cs
status: draft            # draft | ready | published
author: Petr Hlavacek
date: 2026-04-10

# Shopify
blog_id: gid://shopify/Blog/82163826771
blog_handle: magazin
tags: [brankář, rozehrávka, hra nohama, trénink]

# Cluster & brief (replaces content-brief-template.md)
cluster: 3               # 1–5, see topic-cluster-map.md
primary_keyword: rozehrávka brankáře
secondary_keywords: [hra nohama, gólman rozehrávka, distribuce brankáře]
audience: dorost, trenéři, ambiciózní brankáři
search_intent: informational
business_goal: podpora autority v distribuci; soft link na rukavice

# Open questions — must be resolved before writing starts
# Remove this block once all questions are answered
open_questions: []        # example: ["Věková skupina: do 12 nebo 15?", "Zahrnout drily s brankářskými botami?"]

# SEO
seo_title: "Rozehrávka brankáře: 6 chyb, které odevzdávají míč"
seo_description: "Rozehrávka brankáře nohama u dětí a dorostu často rozhoduje pod tlakem. Podívejte se na 6 chyb, které zbytečně odevzdávají míč."

# Links
internal_links:
  - https://bu1.cz/pages/poradna-jak-spravne-vybrat-brankarske-rukavice
related_articles:        # handles from drafts/blog/ — minimum 1
  - jak-trenovat-postreh-brankare
  - brankarska-rozcvicka-pred-zapasem
evidence_sources:        # cite inline in body, NOT as a Zdroje section
  - FIFA Training Centre — build-up phase
  - Savelsbergh 2002 (Journal of Sports Sciences)

# Market keyword localization — validated local search phrasing per locale
# Only include locales where phrasing differs from a direct keyword translation.
# Translations use these as H1 + seo_title anchor. See docs/translations.md → Market Keyword Localization.
market_keywords:
  sk: rozhrávka brankára nohami
  hu: kapus labdakezelés lábbal
  de: Torwart Spielaufbau mit dem Fuß
  pl: rozgrywanie bramkarza nogą
  ro: mingea portarului cu piciorul

# Success criteria — defines what "working" means for this article
# Review date = 90 days after publish. Loop checks these automatically.
success_criteria:
  primary_goal: "rank top 3 for `rozehrávka brankáře` (CZ) within 90 days"
  target_position: 3
  target_ctr_percent: 5
  target_monthly_clicks: 60
  target_bounce_rate: 0.45
  internal_click_goal: "1 click to how_to_choose_gloves per 80 pageviews"
  review_date: 2026-07-10
  baseline_date: 2026-04-10

# Images — shortlist; full specs in blog-photography.md
images:
  - role: hero
    kind: photo
    size: 1600x900
    placement: top
    alt: Brankář při rozehrávce nohama otevírá tělo do volného prostoru
    prompt: "Realistic sports photo, goalkeeper distributing with feet, open body, 16:9"
  - role: first-touch-angle
    kind: infographic
    size: 1200x800
    placement: after_h2
    after_heading: "Chyba 1: Brankář si bere první dotek proti tlaku"
    alt: Otevřený první dotek vytváří bezpečný úhel pro další přihrávku.
    caption: Otevřený první dotek přidává čas. Zavřený první dotek zve pressing.
    prompt: "Clean football infographic showing goalkeeper receiving a back pass with open and closed body shape, simple arrows, no watermark, 3:2"
---

<h1>…</h1>
<p>…</p>
```

Rules:

- **No duplicate fields.** `title` is the single human title; `seo_title` is the `<title>` tag; `<h1>` is inside body. Never repeat values.
- **No `Zdroje` section in body.** Cite sources inline with author + year. `evidence_sources` in frontmatter is a checklist, not reader output.
- **No "SEO Rationale" prose.** If a title choice needs explaining, put it in the commit message.
- **Body starts right after frontmatter** — plain HTML, no ```html fence.
- **`market_keywords` is required for clusters 1–3.** Fill before writing — translations depend on it.
- **`images` stays only in the CS source draft.** Translation files do not duplicate image blocks.
- **Image roles must be unique.** Use machine-readable slugs (`hero`, `drink-comparison`, `penalty-biomechanics`), not repeated `supporting`.
- **Inline images need placement metadata.** Non-hero images require `placement: after_h2` and exact `after_heading`.
- **`open_questions` must be empty before writing starts.** If unresolvable, narrow article scope rather than writing a vague article.
- **`success_criteria` is required for all published articles.** Set targets before writing, not retroactively. Review date = 90 days after publish.
- **One search intent per article.** If H1 answers two different questions, split into two articles.

## Image Planning & Placement (mandatory)

Full image rules live in [`docs/blog-photography.md`](blog-photography.md). This section defines how image planning fits the article workflow.

### Why this exists

Long-form articles need visual breaks, but random images make content worse:
- Google image SEO works better when images sit near relevant text and use useful alt text
- Accessibility guidance requires images to convey meaning, not just decoration
- Public-sector content guidance warns that too many images reduce scanability and page speed

### BU1 heuristic

This is a **BU1 editorial rule**, not a universal web standard:

| Article length | Minimum image count | Default target |
|---|---|---|
| under 900 words | 1 | 1 |
| 900-1500 words | 2 | 2-3 |
| over 1500 words | 3 | 3-4 |

Rules:
- Every article has **exactly 1 hero image**
- If an article has only one image, it must be the hero at the top
- First inline image must be anchored after the **first or second H2**
- Longer articles must spread inline images across the piece, not cluster them in one section
- Maximum default ceiling is **5 images** unless the article genuinely needs more visual explanation

### What counts as a valid inline image

Use an inline image only if it does one of these:
- visualizes a drill setup that is hard to imagine from text alone
- clarifies a comparison, timeline, process, or biomechanical cue
- supports a section with a real match/training situation the reader should recognize

Do **not** use an inline image only to fill whitespace.

### Validation

Run:

```bash
python3 scripts/validate_blog_images.py
python3 scripts/validate_blog_images.py drafts/blog/YYYY-MM-DD-<handle>.md
```

`scripts/upload_blog_articles.mjs` now runs this validator automatically before any Shopify mutation.

## Market Keyword Localization

Czech is the source language. Translations must not mechanically translate the Czech primary keyword — they must use the phrase real users in that market actually search for.

### Why this matters

`jak trénovat postřeh brankáře` → mechanically translated to DE = `wie man die Reaktion des Torhüters trainiert`
But Germans search: `Torwart Reaktionstraining` or `Reflexübungen Torwart`

Using the wrong phrasing means: correct content, wrong keyword, no organic ranking.

### Locale tiers

| Tier | Locales | Action |
|---|---|---|
| **1 — always validate** | sk, hu, de | Research local phrasing before writing. Add to `market_keywords`. Translations use it in H1 + seo_title. |
| **2 — validate for goalkeeper content** | ro, hr, pl | Validate for clusters 1–3. Add to `market_keywords` if phrasing differs. |
| **3 — translate is sufficient** | en, fr, es, it, bg | Mechanical translation of primary keyword is acceptable. No `market_keywords` entry needed unless GSC shows a mismatch. |

### How to validate a market keyword

1. Check `config/article_generator.json` → `market_seo_tiers` for confirmed GSC signals per locale
2. Search the localized phrase on Google in that market — note what autocomplete and top results suggest
3. If the top-ranking competitor pages use a different phrase, use their phrase, not your translation
4. Record the validated phrase in `market_keywords` in the source draft frontmatter

### How translations use market_keywords

- If `market_keywords[locale]` is present: H1 and `seo_title` must contain that phrase (not the translated Czech keyword)
- The article body remains a localized translation of the Czech source — only H1, seo_title, and the first sentence are restructured around the local keyword
- `market_keywords` entries are informational for the translator, not published to Shopify

### Confirmed keyword signals from GSC (bu1sport.com, Jan–Apr 2026)

| Locale | Confirmed query | Impressions | CTR | Position |
|---|---|---|---|---|
| hu | `kapusedzés gyakorlatok` | 66 | 16.7% | 3.6 |
| hu | `bu1 kapuskesztyű` | 187 | 10.7% | 1.4 |
| de | `bu1 torwarthandschuhe` | 22 | 50% | 1.0 |
| pl | `korki dla bramkarza` | 309 | 2.3% | 5.3 |
| ro | goalkeeper training (translated) | 1 345 | 7.0% | 6.2 |
| hr | `nogometni trening za djecu` | 69 | 17.4% | 2.1 |

These confirm that goalkeeper content in HU, DE, HR converts at high CTR despite low BU1 brand awareness in those markets.

## Deep Research Protocol (Clusters 1–3)

For technique-heavy or science-backed goalkeeper articles, run a Gemini deep research session **before** creating the draft. This is the "Think Before Writing" phase — resolves `open_questions` and populates `evidence_sources`.

### When to use

- Cluster 1 (Fundamentals): any technique article — pádová technika, postřeh, postavení, jistota v rukou
- Cluster 2 (Match Situations): penalty science, 1v1, dead-ball situations
- Cluster 3 (Distribution): biomechanics, pressing reads, footwork
- Not needed for: Cluster 4 (Glove Education — product-based), Cluster 5 (Youth Dev — coaching practice-based)

### Research prompt template

```
Deep research for BU1 goalkeeper blog article:

Topic: [přesný název článku, např. "pádová technika brankáře"]
Target audience: [např. děti 10–14 let, rodiče, trenéři]
Primary keyword (CZ): [keyword]

Find:
1. What does the scientific/coaching literature say? (exercise physiology, biomechanics, UEFA/FIFA coaching docs, peer-reviewed studies)
2. What are the top 5 ranking articles on this topic covering that we might miss?
3. What are common misconceptions or mistakes coaches/players have about this topic?
4. What questions do goalkeepers, parents, and coaches actually ask? (forums, Reddit, coaching communities)
5. Any real player examples, club drills, or competition situations that illustrate the concept?

Output: summary of evidence + list of 3–5 citable sources (author, year, publication)
```

### How to use the output

- Sources → `evidence_sources` in frontmatter
- Open questions resolved → `open_questions: []` confirmed before writing
- Misconceptions → natural H2 angle ("Nejčastější chyba při pádové technice")
- Real examples → body storytelling (Karpathy: specific over vague)

**Do not paste Gemini output into the article.** Use it as a research brief — write the article in BU1 brand voice.

---

## Inter-Article Linking

Articles inside the same cluster (and adjacent clusters) must reference each other. This builds topical authority and reduces bounce.

Rules:

1. Every draft must list **at least 1** `related_articles` handle. Target 2.
2. Pick from the **same cluster first**; adjacent cluster only if the topical overlap is real.
3. Add **one inline `<a>`** per related article inside body_html, placed where the reader would naturally want more depth — not stuffed at the end.
4. Anchor text = natural Czech phrase matching the target article's primary keyword (e.g., `jak trénovat postřeh brankáře`), not "klikněte zde".
5. URL format: `https://bu1.cz/blogs/magazin/<handle>` for cs, `https://bu1.cz/sk/blogs/magazin/<handle>` for sk, `https://bu1sport.com/<locale>/blogs/magazin/<handle>` otherwise.
6. In translations, swap the handle for the localized one and the anchor text for the target language. If the target article is not yet translated into that locale, drop the link (better no link than broken).
7. Do not create reciprocal linking loops of 3+ articles where every one links to every other — feels spammy. Prefer 1–2 targeted links.

## SEO Requirements

- **Meta title**: max 60 chars, include primary keyword
- **Meta description**: 150-160 chars, active verbs, click-worthy
- **URL handle**: localized slug per language
- **H1**: one per article, contains primary keyword
- Each evergreen article needs: primary keyword, secondary keywords, target audience, search intent
- Avoid creating a new article if the topic is already covered — update existing asset instead
- If title or meta description is not provided, generate them based on actual article content

## Content Depth Rules

- **Concrete over vague**: "podle studie UEFA z roku 2023" instead of "mnoho expertů tvrdí"
- **Specific reasons**: explain concrete WHY, never just "je důležité"
- **Real sources**: FIFA, UEFA, scientific studies, official sports organizations — cite inline, naturally
- **No sources section**: do NOT add a "Zdroje" / "Sources" list at the end of articles
- **Storytelling**: based on real events, real players, real matches — never invented scenarios
- **Every paragraph must deliver value**: no filler sentences, no empty rhetoric
- **Specific names and data**: mention real players, coaches, clubs, tournaments, stats with years

## Content Rules

- Max 2-3 internal links per article, only when naturally relevant
- One CTA per section, product/action before atmosphere
- See [`docs/brand.md`](brand.md) for forbidden terms and tone

## Topic Cluster Rules

- Every article maps to exactly one primary cluster
- Prefer goalkeeper expertise, youth development, glove education, match situations
- Broad football culture topics are lower priority unless clear business reason
- See [`docs/topic-cluster-map.md`](topic-cluster-map.md) for full cluster definitions

## Internal Linking

### Source of truth

- **Evergreen pages**: `config/article_generator.json` → `evergreen_pages` (handles verified from sitemaps)
- **Sitemaps**: bu1.cz/sitemap.xml (cs, sk) | bu1sport.com/sitemap.xml (en + 9 locales)
- When in doubt, verify handle exists in the sitemap before linking

### URL construction per locale

| Locale | Base URL | Example |
|---|---|---|
| cs | bu1.cz | bu1.cz/pages/pece-o-rukavice |
| sk | bu1.cz/sk | bu1.cz/sk/pages/starostlivost-o-rukavice |
| en | bu1sport.com | bu1sport.com/pages/goalkeeper-gloves-care |
| de | bu1sport.com/de | bu1sport.com/de/pages/handschuhpflege |
| pl, fr, es, it, hu, ro, bg, hr | bu1sport.com/{locale} | bu1sport.com/pl/pages/opieka-o-rekawice |

Formula: `{store_base}/{type}/{localized_handle}`

### Rules

1. Max 2-3 internal links per article
2. Only when naturally relevant — never forced
3. Always use the **localized handle** for the target locale (lookup in `evergreen_pages`)
4. **Anchor text** always in the target language — never Czech anchor text in a foreign-language article
5. Never mix domains — no bu1.cz link in a DE article, no bu1sport.com link in a CS article
6. Never mix locale prefixes — no EN handle under `/de/` prefix
7. If the localized handle for a locale is unknown (null in config), do not link — better no link than a broken one
8. Prefer evergreen pages over collection/product links
9. Format: `<a href="FULL_URL">localized anchor text</a>`

### Priority evergreen pages

| Key | When to link |
|---|---|
| `how_to_choose_gloves` | Glove choice, beginner advice, first gloves, glove comparison |
| `glove_care` | Glove maintenance, cleaning, washing, lifespan, grip care |
| `custom_gloves` | Team orders, academy kits, personalization, custom design |
| `custom_shinguards` | Custom equipment, own design, personalized shinguards |

## Link Validation (mandatory QC step)

Before publishing an article or registering a translation, verify:

1. **Every internal link in body_html exists in the sitemap** for that locale
   - CS/SK: check bu1.cz/sitemap_pages_1.xml or bu1.cz/sk/sitemap_pages_1.xml
   - Others: check bu1sport.com/{locale}/sitemap_pages_1.xml
2. **Handle matches the localized handle** from `config/article_generator.json` → `evergreen_pages`
3. **No domain mixing** — bu1.cz links only in cs/sk articles, bu1sport.com links in all others
4. **No locale mixing** — the locale prefix in the URL matches the article's target locale
5. **If a handle for the target locale doesn't exist** in `evergreen_pages`, remove the link entirely — no broken links
6. **Product links** (`/products/`) — verify the product handle exists for the target locale in the products sitemap

## Translation File Format

Translation files live in `drafts/blog/translations/YYYY-MM-DD-<source-handle>-<locale>.md`.

They are **derived outputs** — not source of truth. Minimal frontmatter only:

```md
---
locale: en
source_handle: jak-trenovat-postreh-brankare
source_date: 2026-04-10
title: "How to Train Goalkeeper Reaction: 7 Drills for Training"
handle: how-to-train-goalkeeper-reaction
seo_title: "How to Train Goalkeeper Reaction: 7 Drills for Training"
seo_description: "How to train goalkeeper reaction? 7 drills, a weekly plan and the most common mistakes. A guide for youth goalkeepers, coaches and parents."
summary_html: "Reaction is not just about quick hands. Find 7 drills, a weekly plan and common mistakes that slow reflexes."
---

<h1>…</h1>
<p>…</p>
```

Rules:
- **No duplicate fields from source** — no cluster, tags, evidence_sources, images (those stay in the CS source file)
- **Localized internal links** — swap every internal link URL + anchor text for the target locale (see Internal Linking table in this doc)
- **Cross-article links** — use the localized handle defined in that translation file's own `handle` field; if the target article is not yet translated, drop the link
- **Formal register always** — Sie (DE), Pan/Pani (PL), Vy (SK), vous (FR), usted (ES), Lei (IT), Ön (HU), dumneavoastră (RO), Вие (BG), Vi (HR)
- **Blog handle** — `bu1.cz/blogs/magazin` for CS/SK; `bu1sport.com/blogs/magazine` for all others
- **BG handle: native Cyrillic only** — bu1sport.com/bg articles use Cyrillic text directly in the URL (e.g. `позициониране-на-вратаря-на-терена`). Never use Latin transliteration (e.g. `pozitsionirane-...`) or English for BG handles. Verify against `bu1sport.com/bg/sitemap_blogs_1.xml` when in doubt. Shopify accepts and stores Cyrillic slugs correctly; transliteration causes mismatch because Shopify's own auto-transliteration differs from any manual scheme.

## Shopify Upload Workflow

### Script

```bash
node scripts/upload_blog_articles.mjs                    # sync all files in drafts/blog/
node scripts/upload_blog_articles.mjs drafts/blog/YYYY-MM-DD-<handle>.md   # one file
python3 scripts/validate_blog_images.py                  # image strategy preflight
```

**Auth (run once per session):**
```bash
shopify store auth --store bu1rebuild.myshopify.com \
  --scopes write_content,write_translations,read_content,read_translations
```

**Preflight (runs automatically inside upload script):**
```bash
python3 scripts/validate_blog_images.py drafts/blog/YYYY-MM-DD-<handle>.md
```

### Publish rules — hardcoded in script, do not bypass

| Scenario | Behaviour |
|---|---|
| New article | `articleCreate` → `isPublished: false` (draft). Never auto-publishes. |
| Existing draft | `articleUpdate` → `isPublished` omitted → Shopify preserves `false` |
| Existing published | `articleUpdate` → `isPublished` omitted → Shopify preserves `true` (never unpublishes) |
| Translations | `translationsRegister` — overwrites existing entries for changed fields |

To manually publish a draft after review:
```bash
shopify store execute --store bu1rebuild.myshopify.com --allow-mutations \
  --query 'mutation { articleUpdate(id: "gid://shopify/Article/XXXXXX", article: { isPublished: true }) { article { id isPublished } userErrors { message } } }'
```

### Scenarios in detail

**1. New article (CS only, no translations yet)**
1. Create draft file `drafts/blog/YYYY-MM-DD-<handle>.md`
2. Run script → article created as draft on Shopify
3. Review in Shopify admin → publish manually when ready

**2. New article + all 11 translations**
1. Create draft file + 11 translation files in `drafts/blog/translations/`
2. Run script → article created as draft, 66 translation entries registered (11 locales × 6 fields)
3. Review → publish manually

**3. Add translations to existing article**
1. Create missing translation files in `drafts/blog/translations/`
   (filename: `YYYY-MM-DD-<source-handle>-<locale>.md`, `source_handle` must match CS draft handle)
2. Run script → article lookup finds existing GID, skips create/update, registers new translations
3. No change to publish status

**4. Update existing article content (CS + re-sync translations)**
1. Edit the CS draft file + any translation files that need updating
2. Run script → `articleUpdate` called with new content, preserves publish status, translations overwritten
3. Note: if only translating fields changed, `translationsRegister` alone would suffice (run script anyway — idempotent)

### Key API facts (lessons learned)

| Fact | Detail |
|---|---|
| `author` is required | `ArticleCreateInput.author` is non-null → always pass `{ name: "Petr Hlavacek" }` |
| CLI JSON format | `shopify store execute --json` returns data **directly** — no `{ "data": {} }` wrapper |
| Batch translations | Register all 11 locales in **one** `translationsRegister` call per article (array input) |
| Digest required | `translationsRegister` needs `translatableContentDigest` per field — fetch via `translatableResource` query first |
| Translatable keys | `title`, `body_html`, `summary_html`, `handle`, `meta_title`, `meta_description` |
| SEO storage | SEO title = metafield `global.title_tag` (type: `single_line_text_field`) · SEO desc = `global.description_tag` (type: `multi_line_text_field`) |
| Input field names | `body` (not `bodyHTML`), `summary` (not `summaryHTML`) in `ArticleCreateInput` / `ArticleUpdateInput` |
| Image preflight | Upload script aborts if `scripts/validate_blog_images.py` fails for the selected source draft(s) |
| Idempotent | Script is safe to re-run — existing articles are updated, existing translations overwritten |

### Article GIDs (as of 2026-04-10 upload)

| Handle | GID |
|---|---|
| `jak-trenovat-postreh-brankare` | `gid://shopify/Article/564468088915` |
| `brankarska-rozcvicka-pred-zapasem` | `gid://shopify/Article/564468351059` |
| `rozehravka-brankare-nohama` | `gid://shopify/Article/564468383827` |
| `postoj-brankare-v-poli` | `gid://shopify/Article/564725514323` |
