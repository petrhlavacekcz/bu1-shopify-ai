# BU1 Growth Backlog

Living document. Add ideas here — remove them only when implemented (→ CHANGELOG) or explicitly abandoned (→ mark as `dropped` with reason).

**Difference from other docs:**
- `CHANGELOG.md` — decisions already made
- `docs/integrations-catalog.md` — technical integration specs
- `docs/skills-roadmap.md` — AI agent skills
- This file — ideas under evaluation, not yet decided

---

## How to read this file

Each item has:
- **What** — one sentence
- **Why it matters for BU1** — concrete business case
- **Effort** — Low / Medium / High
- **Dependencies** — what needs to exist first
- **Status** — `idea` | `evaluating` | `approved` | `dropped`

---

## Theme 1: Data & Intelligence Gaps

### 1.1 Microsoft Clarity MCP
**What:** Connect Clarity MCP server (`npx @microsoft/clarity-mcp-server`) to get scroll depth, heatmaps, and session data per article.

**Why it matters for BU1:** GA4 tells us bounce rate. Clarity tells us *where* readers drop off. If 60% of readers on `brankarska-rozcvicka-pred-zapasem` stop at the second H2, the fix is structure — not keyword. Without this data we're guessing. The 4 articles published April 2026 have no scroll data yet.

**Effort:** Low — npm install + API token from Clarity dashboard.

**Dependencies:** Clarity account must be tracking bu1.cz and bu1sport.com. Limit: 10 API req/day, 3 days of data per query.

**Status:** `approved` — implement at next session. Add to monthly monitoring loop after setup.

---

### 1.2 DataForSEO MCP
**What:** Pay-per-use SEO API (~0.1–2 USD/request) with keyword volume, SERP data, and competitor rankings across all markets.

**Why it matters for BU1:** GSC only shows queries where BU1 already exists. DataForSEO shows the full keyword landscape — what our CZ/HU/DE/PL competitors rank for, true search volumes, and keyword difficulty. Enables genuine gap analysis, not just "our low-CTR queries". Especially valuable for HU, DE, PL markets where we have no GSC baseline yet.

**Concrete use case:** Before writing a new Cluster 4 article, check: what does `sportisimo.cz` rank for in `brankářské rukavice` space that BU1 doesn't?

**Effort:** Low — MCP server available, pay-per-use.

**Dependencies:** DataForSEO account. [Setup guide](https://nextgrowth.ai/dataforseo-mcp-server-setup/).

**Status:** `evaluating` — test with one keyword research session before committing.

---

### 1.3 LLM Brand Monitoring (manual, monthly)
**What:** Monthly check — ask ChatGPT, Perplexity, and Google AI Mode: "Doporuč brankářské rukavice pro dítě" and "goalkeeper gloves recommendation" → record whether BU1 is cited.

**Why it matters for BU1:** LLM-referred traffic converts 4.4× better than organic search. Google AI Overviews now appear on 14% of shopping queries (5.6× increase in 4 months). If BU1 is not being cited by LLMs, we have a structural content problem — probably missing FAQ schema, thin evidence sourcing, or weak entity signals.

**Effort:** Low — 10 minutes/month, manual. Add to `docs/monitoring-loop.md` as step 7.

**Dependencies:** None.

**Status:** `approved` — add to monitoring loop at next session.

---

### 1.4 Review Mining — Customer Language as Content & Copy Input
**What:** Systematicky číst produktové recenze BU1 rukavic a vytěžit z nich zákaznický jazyk pro keyword research, FAQ obsah a copywriting.

**Why it matters for BU1:** Zákazníci v recenzích píšou přesně ta slova, která pak píšou do Googlu — ale přirozeněji než keywordy navrhované SEO nástroji. Konkrétně: recenze odhalí, jak rodiče popisují problém s výběrem rukavic pro dítě ("nevím jakou velikost", "rukavice se rozlepily po prvním dešti") → to jsou H2 nadpisy pro Cluster 4 články. Druhá hodnota: zjistíme, jaké obavy rozhodují nákup → informuje copywriting produktových stránek a meta popisků. Třetí hodnota: recenze v němčině nebo maďarštině potvrdí nebo zpochybní naše market_keywords.

**Jak:** Exportovat recenze ze Shopify (Shopify MCP nebo admin export) → seskupit podle tématu → identifikovat opakující se fráze, otázky a obavy → přidat do `open_questions` pro relevantní draft nebo jako input pro nový brief.

**Effort:** Low — jednorázový audit ~2 hodiny, pak čtvrtletní update.

**Dependencies:** Recenze musí existovat v Shopify. Pokud jsou recenze na externích platformách (Heureka, Google Reviews), přidat jako zdroj.

**Status:** `approved` — plná analýza v `reports/2026-04-17-review-mining-analysis.md`. Zdroj: Judge.me CSV export, 1478 recenzí. Příští export: 2027-04-17 nebo po 500+ nových recenzích. Ukládáme jako `reports/bu1rebuild-all-published-reviews-in-judgeme-format-YYYY-MM-DD-*.csv`.

---

### 1.5 Shopify Internal Search Analytics
**What:** Aktivovat a číst data z interního vyhledávání v bu1.cz — co zákazníci hledají přímo v obchodě.

**Why it matters for BU1:** Interní search je čistý purchase intent: zákazník už je na webu a aktivně hledá produkt nebo informaci. Pokud 80 zákazníků za měsíc hledá "rukavice pro 8 let" a žádná stránka jim to neodpoví, je to zároveň obsahová mezera i produktová příležitost. Kvalitnější signal než GSC — GSC ukazuje co lidé hledají, než přijdou; internal search ukazuje co jim chybí poté, co přišli.

**Jak:** Shopify Admin → Analytics → Search analytics (pokud je Shopify Search & Discovery app aktivní). Alternativně přes GA4 site_search event. Export top 50 dotazů → porovnat s existujícím obsahem a produktovým katalogem → identifikovat mezery.

**Effort:** Low — data jsou dostupná v Shopify Admin, žádná integrace nutná.

**Dependencies:** Shopify Search & Discovery app musí být nainstalovaná (většinou default). Pokud není, GA4 site_search event jako fallback.

**Status:** `evaluating` — reálná data stažena a analyzována v `reports/2026-04-17-internal-search-audit.md`. 3 okamžité akce identifikovány (size chart, Light HG tag, péče content). Čeká na schválení Petrem.

---

### 1.6 Ahrefs MCP
**What:** Backlink analysis, Domain Rating competitors, keyword difficulty, organic traffic estimates.

**Why it matters for BU1:** Backlink gaps show where BU1 is losing authority vs. larger sporting goods retailers. Useful for understanding why `brankářské rukavice` is stuck at pos 8.2.

**Effort:** Medium — requires paid Ahrefs plan.

**Dependencies:** DataForSEO covers 80% of the same use cases for less. Evaluate 1.2 first.

**Status:** `idea` — revisit if DataForSEO proves insufficient.

---

## Theme 2: Content Production Improvements

### 2.1 Gemini Deep Research Before Technical Articles
**What:** Before writing any technique-heavy or science-backed goalkeeper article (Clusters 1–3), run a Gemini deep research session to gather scientific evidence, common misconceptions, and competitor content coverage.

**Why it matters for BU1:** BU1's authority advantage over generic sporting goods blogs is goalkeeper expertise. That advantage only holds if articles cite real evidence (exercise physiology, coaching science) — not just "practice these 5 drills". Gemini Deep Research surfaces:
- Peer-reviewed evidence (journals, UEFA/FIFA coaching docs)
- What the top 10 ranking articles cover that we might miss
- Common goalkeeper training misconceptions to correct
- Reddit/forum questions the audience actually has

This directly improves `evidence_sources` in frontmatter and helps resolve `open_questions`. It's the "Think Before Writing" principle extended to subject matter, not just keyword/audience.

**Effort:** Low — prompt template, 15–30 min per article pre-write.

**How to use:** See `docs/blog-articles.md` → Article Creation Workflow, step 1b.

**Dependencies:** Gemini access (already listed in `integrations-catalog.md` as supported agent).

**Status:** `approved` — workflow already updated in `docs/blog-articles.md`.

---

### 2.2 GEO / Structured Data Layer
**What:** Add `FAQPage`, `HowTo`, and `Article` JSON-LD schema to goalkeeper blog articles via Shopify metafield or body_html injection.

**Why it matters for BU1:** Structured data is the primary mechanism for LLM citation and Google rich snippets. A `FAQPage` block on "Jak vybrat brankářské rukavice" increases the chance of appearing in:
- Google AI Overviews for equipment queries
- ChatGPT answers to "goalkeeper glove sizing"
- Perplexity recommendations for parents buying first gloves

The 4 articles published April 2026 have zero structured data. The collection page has 29k impressions and 1.65% CTR — a rich snippet from a linked blog article can move that number.

**Schema targets per cluster:**
- Cluster 1 (Fundamentals): `HowTo` (step-by-step technique), `FAQPage`
- Cluster 2 (Match Situations): `FAQPage`, `Article`
- Cluster 3 (Distribution): `HowTo`, `FAQPage`
- Cluster 4 (Glove Education): `FAQPage` (sizing, care), `Product` (link to collection)
- Cluster 5 (Youth Dev): `FAQPage`, `Article`

**Effort:** Medium — script to generate and inject JSON-LD via Shopify MCP.

**Dependencies:** Article content must be published. Start with 4 existing articles.

**Status:** `approved` — high leverage, implement before next monitoring loop.

---

### 2.3 YouTube → Blog Pipeline
**What:** If BU1 has goalkeeper training videos, transcribe them → structure into blog article format → embed video in article.

**Why it matters for BU1:** YouTube mentions have the strongest correlation with AI visibility (ChatGPT, AI Mode, AI Overviews). Embedding video in article increases average engagement time → GA4 bounce rate drops → positive ranking signal. Video content also builds a library of `evidence_sources`.

**Effort:** Medium — depends on whether video content exists. Transcription via Whisper API or YouTube auto-captions.

**Dependencies:** BU1 YouTube channel audit needed first.

**Status:** `idea` — validate whether video content exists.

---

### 2.4 PDF Lead Magnet + Email Funnel
**What:** Create "Průvodce výběrem první brankářské rukavice" as a downloadable PDF, gate it with email opt-in, trigger a 5-email Klaviyo welcome sequence.

**Why it matters for BU1:** Cluster 4 (Glove Education) serves parents buying first gloves — exactly the audience that needs hand-holding. A PDF guide builds the email list from the highest-commercial-intent audience. Once Klaviyo write access is available, the email sequence can link to `brankářské rukavice` collection at the right moment.

**Funnel:**
1. Blog article (how to choose gloves for children)
2. CTA: "Stáhněte si průvodce zdarma"
3. Email → 5-email sequence → soft product recommendation at email 4

**Effort:** High — requires content creation (PDF), Shopify form, Klaviyo flow build.

**Dependencies:** Klaviyo write MCP access (currently read-only beta). Start building content while waiting.

**Status:** `idea` — plan content once Cluster 4 articles are published.

---

### 2.5 Product-Grounded Blog Image Pipeline
**What:** Build an end-to-end workflow that plans, generates, and later uploads blog images grounded in the actual BU1 product catalog.

**Why it matters for BU1:** Dnes už máme image planning rules a validátor, ale chybí obchodní vrstva nad tím: obrázek nemá být jen "brankář ve tmě", ale může nést konkrétní produktový signál. Pokud článek o penaltách ukazuje brankáře v reálně existujících rukavicích BU1 Triangle nebo článek o rozcvičce používá reálné BU1 apparel cues, blog přestává být čistě edukační asset a začíná fungovat i jako soft merchandising. Zároveň to zvyšuje důvěru: čtenář vidí to, co může opravdu koupit.

**Important constraint:** sitemap sama o sobě nestačí pro věrný vizuál. Je výborná pro discovery (handle, URL, coverage napříč locales), ale neobsahuje dost detailů pro faithful rendering. Pro branded visuals je nutné sahat i na reálnou PDP media nebo Shopify product data.

**Proposed workflow:**
1. Draft article → identify which H2 sections deserve an image
2. Resolve `product_refs` from `config/article_generator.json` and product sitemaps
3. Read real product page imagery / Shopify media for visual grounding
4. Generate prompt and alt text in draft metadata
5. Render with image model
6. Upload to Shopify and attach to article once image upload pipeline exists

**Codex role:**
- yes for orchestration, validation, prompt building, product resolution, and metadata updates
- no as the core renderer; the actual image should come from an image model/tool

**Effort:** Medium

**Dependencies:** existing image planning validator, product URL discovery, future product-media fetch step, future Shopify image upload step.

**Status:** `approved` — strategy is clear, implementation should continue in two phases: (1) product grounding and asset generation, (2) Shopify upload + localized alt management.

---

## Theme 3: New Acquisition Channels

### 3.1 Competitor SERP Monitoring (agent-browser.dev)
**What:** CLI browser automation tool for AI agents. Use to screenshot and parse SERP for target goalkeeper keywords across Google.cz, Google.hu, Google.de, Google.pl weekly.

**Why it matters for BU1:** We currently have no visibility into whether a Czech or Slovak competitor has published a goalkeeper article that could push BU1 out of top 5. Early detection = early response.

**Concrete use case:**
- Weekly: check top 5 results for `brankářská rozcvička` (CZ), `kapusedzés` (HU)
- Monthly: screenshot top 10 for all target keywords → compare vs. previous month

**Effort:** Medium — install via Homebrew, build automation script.

**Dependencies:** agent-browser.dev installed. [GitHub](https://github.com/agent-browser/agent-browser).

**Status:** `idea` — implement after core content gaps are filled (Q3 2026).

---

### 3.2 Programmatic SEO — Size & Care Guide Pages
**What:** Generate structured pages like "Brankářské rukavice velikost 7 — jak vybrat" or "Torwarthandschuhe Größentabelle Kinder" from product catalog data.

**Why it matters for BU1:** Size and care queries have high commercial intent and low competition. DataForSEO would confirm volumes. Templates can be generated in all 12 locales from a single size-guide data model.

**Warning:** Programmatic SEO produces thin content at scale — directly contradicts BU1's authority positioning. Only viable for strictly factual pages (size charts, washing instructions) — not for goalkeeper technique.

**Effort:** Medium — template design + Shopify page creation via MCP.

**Dependencies:** DataForSEO validation of keyword volumes first. Quality review gate before any publish.

**Status:** `idea` — validate keyword volumes before committing.

---

## Theme 4: Conversion & Retention

### 4.1 AI Shopping Assistant (Goalkeeper Glove Advisor)
**What:** Use Shopify Storefront MCP to power a conversational glove advisor: "Which goalkeeper gloves for my 8-year-old son who plays on artificial turf?"

**Why it matters for BU1:** The collection page has 29k impressions and 1.65% CTR. A conversational sizing assistant on the collection page would directly address the parents who don't know what to buy. BU1 would be the first goalkeeper brand on the Czech market with this capability.

**Shopify Storefront MCP tools available:** product catalog, cart, policies, order tracking. Conversational product discovery is live as of Winter '26 Edition.

**Effort:** High — requires theme integration, conversational script design, localization.

**Dependencies:** Cluster 4 (Glove Education) content must exist first — the assistant needs to link to educational articles, not just products.

**Status:** `idea` — revisit Q4 2026 after Cluster 4 content is published.

---

### 4.2 Article-to-Email Automation
**What:** Klaviyo flow triggered by blog reading behavior: 3+ goalkeeper articles read → enter nurture sequence → glove recommendation at email 4.

**Why it matters for BU1:** Current email is campaign-based (one-off sends). Behavioral triggers turn reading intent into purchase intent automatically. Estimated conversion improvement: 15–30% on nurtured list vs. cold campaign send.

**Effort:** Medium — Klaviyo flow build + web tracking setup.

**Dependencies:** Klaviyo write MCP access (currently read-only beta).

**Status:** `idea` — revisit when Klaviyo write access becomes available.

---

## Theme 5: Research Methods

### 5.1 Meta Title A/B Testing via GSC
**What:** Systematicky testovat varianty meta title u top 5 brankářských článků a měřit změnu CTR přes GSC.

**Why it matters for BU1:** CTR brankářských článků se pohybuje mezi 5–16%. Rozdíl mezi "Brankářská rozcvička: 8 cviků před zápasem" a "Jak správně rozcvičit brankáře před zápasem" může být 3–5 procentních bodů CTR — při 1 000 impressích měsíčně to je 30–50 kliků navíc bez jediné nové stránky. GSC tato data přímo měří (impressions × CTR → clicks). Je to nejrychlejší lever na organický traffic po publikaci.

**Jak:**
1. Vybrat 5 článků s nejvyššími impressemi a CTR pod 8%
2. Navrhnout alternativní meta title — otestovat: otázka vs. benefit vs. číslo ("8 cviků" vs. "Jak..." vs. "Proč brankáři...")
3. Změnit přes Shopify MCP (`seo_title` metafield)
4. Po 4 týdnech porovnat CTR v GSC (stejné období, year-over-year nebo vs. baseline)
5. Vítěze ponechat, poraženého vrátit nebo zkusit třetí variantu

**Effort:** Low — 30 minut příprava, 4 týdny čekání, 15 minut vyhodnocení.

**Dependencies:** GSC přístup (máme). Shopify MCP pro změnu meta title (máme). Stačí min. ~500 impressí/měsíc na článek aby byl test statisticky smysluplný.

**Cadence:** Čtvrtletně — 1 test = 1 článek × 4 týdny. Paralelně max 2–3 testy najednou aby nedošlo k záměně signálů.

**Status:** `approved` — zařadit do quarterly review v monitoring-loop.md.

---

### 5.2 Monthly LLM Visibility Check Protocol
**What:** Standardized set of 5 prompts to run in ChatGPT, Perplexity, and Google AI Mode monthly — check if BU1 is cited.

**Prompts:**
1. "Doporuč brankářské rukavice pro 10leté dítě"
2. "Jak pečovat o brankářské rukavice"
3. "goalkeeper gloves recommendation for children"
4. "Torwarthandschuhe für Kinder empfehlen"
5. "kapus kesztyű gyerekeknek ajánlás"

**Record:** whether BU1 is mentioned, in what context, which article/page is cited. Save to `reports/YYYY-MM-DD-llm-visibility.md`.

**Effort:** Low — 15 min/month.

**Status:** `approved` — add to monitoring-loop.md.

---

## Dropped Ideas

*(None yet — add here with reason when an idea is abandoned)*

---

## Backlog Review Cadence

| When | What to review |
|---|---|
| Monthly (with SEO loop) | Status updates — any `evaluating` items ready to approve? |
| Quarterly | Full sweep — remove stale ideas, add new ones from data |
| After any major market data update | Theme 1 and Theme 3 |
