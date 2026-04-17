# BU1 Project Changelog

This is a **decision log**, not a code diff log.

Every entry answers: **What changed? Why? What data drove it? What's the expected impact?**

Format: newest first. Each entry links to affected files.

---

## 2026-04-17 — Product-Grounded Blog Image Layer

**Why:**
The previous image workflow solved editorial structure (how many images, where, basic metadata), but not the next business question: can blog imagery become a merchandising layer instead of generic decoration? For BU1, the answer is yes, but only if branded visuals are grounded in real store products instead of invented "BU1-like" styling.

**What changed:**
- `docs/blog-photography.md` — updated: product-grounded branded visuals are now defined; `product_refs` added to the draft schema; sitemap vs. PDP-media distinction documented.
- `docs/system-capabilities.md` — updated: new capability entries for product-grounded image ops and store-grounded creative direction.
- `docs/growth-backlog.md` — updated: approved roadmap item for a product-grounded blog image pipeline.

**Key decision:**
- Sitemap is a discovery source, not a fidelity source.
- Use sitemap/config to find product URLs and coverage.
- Use real product page imagery or Shopify media to ground any BU1-branded generated visual.
- If product grounding is missing, keep the image unbranded instead of inventing BU1 gear.

**Codex role:**
Codex can orchestrate the workflow: read drafts, resolve product references, write prompts, validate image plans, and later drive upload scripts. The actual raster image should still come from an image-generation model/tool, not from shell scripting alone.

**Expected impact:**
- Blog visuals can start supporting soft product merchandising without breaking brand trust.
- Future upload automation has a cleaner metadata model (`product_refs`) to work from.

**Status:** Implemented at strategy/workflow level. Upload and locale-specific image translation are still pending implementation.

---

## 2026-04-17 — Blog Image Strategy Workflow

**Why:**
The blog workflow already captured image prompts, but it did not answer three practical questions that matter for long-form content: how many images an article should have, where they should appear, and how to keep image planning enforceable instead of optional. External guidance from Google Search Central, W3C/web.dev, GOV.UK, and public-sector accessibility teams converges on the same principle: use meaningful images near relevant text, write useful alt text, and avoid flooding the page with decorative visuals.

**What changed:**
- `docs/blog-photography.md` — rewritten: BU1 image strategy now defines count heuristics, placement rules, alt-text constraints, image metadata schema, and validator usage.
- `docs/blog-articles.md` — updated: article workflow now includes image planning + validation before upload; draft schema expanded with `kind`, `placement`, `after_heading`, and `caption`.
- `scripts/validate_blog_images.py` — created: validates hero image presence, minimum image count by article length, inline image placement against real H2 headings, and alt-text metadata.
- `scripts/upload_blog_articles.mjs` — updated: runs blog image validation automatically before any Shopify mutation.
- `agents.md` — updated: image validator added to current workflow resources.

**Design decision:**
There is no universal "one image per X words" standard in the source guidance. BU1 therefore uses a house heuristic:
- under 900 words = 1 image minimum
- 900-1500 words = 2 images minimum
- over 1500 words = 3 images minimum

This keeps the workflow practical while preventing decorative overload.

**Expected impact:**
- Long articles stop shipping as unbroken walls of text
- Image planning becomes machine-checkable before Shopify upload
- Future image upload automation has stable anchors (`role`, `placement`, `after_heading`) to build on

**Status:** Implemented

---

## 2026-04-16 — Goalkeeper Slang & Technical Glossary

**Why:**
Cultural integrity audit (Capability 15) revealed that machine translations often fail on goalkeeper-specific terminology (e.g., using "Schaum" instead of "Haftschaum" in DE, or "Pullover" instead of "Hoodie"). To maintain professional authority across 12 locales, a standardized glossary was needed.

**What changed:**
- `config/goalkeeper_glossary.json` — created: standardized terms (latex, cuts, warm-up, saves) for all 12 locales + forbidden terms list.
- `agents.md` — updated: glossary added to Shared Resources.
- `docs/translations.md` — updated: glossary made mandatory for all translation workflows.

**Status:** Implemented

---

## 2026-04-16 — System Capabilities Map (Capability Map)

**Why:**
The workspace has many data sources (GSC, GA4, Klaviyo, Shopify) and scripts, but it was hard to quickly see "what can I actually DO with this right now?". We needed a bridge between raw data and business execution.

**What changed:**
- `docs/system-capabilities.md` — created: a catalog of 6 high-impact workflows possible with the *current* system (e.g., Internal Link Intelligence, International Growth Sniper).
- `agents.md` — updated: system-capabilities.md added to shared resources.
- Distinction established: `system-capabilities.md` (what we can do now) vs. `growth-backlog.md` (what we need to build).

**Status:** Implemented

---

## 2026-04-16 — Growth Backlog + Gemini Deep Research Protocol

**Why:**
After external research (DataForSEO, Microsoft Clarity MCP, agent-browser, Shopify Storefront MCP, GEO/LLM optimization trends), it became clear that the codebase can serve more business layers than content + translation. A living strategic backlog was missing — ideas had nowhere to live between "brainstorm" and "CHANGELOG decision".

Separately: goalkeeper articles in Clusters 1–3 are science-backed but the current workflow had no step for gathering evidence before writing. Gemini deep research fills the "Think Before Writing" gap.

**What changed:**
- `docs/growth-backlog.md` — created: living strategic backlog with 10 evaluated ideas across 5 themes (data gaps, content production, acquisition, conversion, research methods)
- `docs/blog-articles.md` — step 1b added: Gemini deep research for Clusters 1–3; "Deep Research Protocol" section added with prompt template and usage rules
- `docs/integrations-catalog.md` — Tier 5 (growth tools) added; Clarity entry updated to reflect new MCP server
- `agents.md` — growth-backlog.md added to workflow index

**Approved items in backlog (ready to implement next):**
- Clarity MCP setup (1.1)
- LLM brand monitoring monthly check (1.3)
- GEO / structured data layer — JSON-LD schema on existing articles (2.2)
- LLM visibility check protocol (5.1)

**Status:** Implemented

---

## 2026-04-16 — Reports System + Lost Data Recovery

**Why:**
Three data points were lost during DRY cleanup: seasonal Klaviyo signals, confirmed content format performance (drill vs. age-specific), and country-level GSC CTR signals. Recovered and placed in canonical locations. Reports system added to give all future data snapshots a home with BLUF structure, expires dates, and a living index.

**What changed:**
- `docs/goals.md` — "Seasonal Content Signals" subsection added (Jan–Feb equipment window, Feb–Mar spring prep — confirmed by Klaviyo)
- `docs/topic-cluster-map.md` — Cluster 1: format signal added (drill format = 16% bounce vs. age-specific = ~25% bounce); Cluster 2: country-level GSC CTR signals added (AUT 28.6%, GBR 65.8%, PL 41.7%)
- `docs/reports-guide.md` — created: naming convention, frontmatter schema, BLUF intro template, `expires` conventions per type
- `reports/index.md` — created: living registry of all reports
- `reports/2026-04-16-market-signals.md` — created: first report in new format, capturing today's country-level market signals
- `docs/monitoring-loop.md` — updated: SEO review reports now use `reports/YYYY-MM-DD-seo-monthly.md` + BLUF frontmatter
- `agents.md` — reports/ directory and reports-guide.md added to workflow index and shared resources

**Design decisions:**
- One file per report (snapshot + review combined, not separate files)
- Different `expires` dates per type (seo: 35 days; data: 6 months; translation: until fixed; strategy: permanent)
- Existing pre-format reports (`FINAL_AUDIT_2026-04-10.md`) left as-is, indexed but not reformatted

**Status:** Implemented

---

## 2026-04-16 — Monthly SEO Monitoring Loop

**Why:**
Without a structured monthly review, articles drift past their `review_date` unnoticed. The loop creates a fixed protocol any agent can run on demand.

**What changed:**
- `docs/monitoring-loop.md` — created: lean checklist-based review protocol (agent-agnostic, no vendor infrastructure)

**Design decision:** Remote cloud trigger was created and immediately disabled. Reason: vendor lock-in, unnecessary complexity for a task that runs once a month with human in the loop. Lean alternative: ask any AI "spusť měsíční SEO review dle docs/monitoring-loop.md" — same outcome, zero infrastructure.

**Status:** Active — run manually on the 1st of each month

---

## 2026-04-16 — Success Criteria Framework + Goal-Driven Content System

**Why:**
Content was being produced without measurable targets. "Write an article" is a task; "rank top 3 for X within 90 days, CTR ≥ 5%" is a verifiable goal. Without success criteria, there's no signal to loop on — no way to know if an article needs updating or is working fine.

Inspired by Andrej Karpathy's principle: *"LLMs are exceptionally good at looping until they meet specific goals. Don't tell it what to do, give it success criteria and watch it go."*

**What changed:**
- `docs/goals.md` — created: WHY this project exists, business goals, KPI baselines, success criteria framework per article
- `docs/blog-articles.md` — `success_criteria` added to frontmatter schema; `open_questions` checkpoint added before writing
- `docs/content-brief-template.md` — `open_questions` and `success_criteria` added to minimum fields
- `CHANGELOG.md` — this file created
- `docs/monitoring-loop.md` — monthly GSC review loop documented

**Data that drove it:**
- No article in the blog had defined a target position or review date
- 4 new articles published 2026-04-10 with no mechanism to verify if they're working
- Karpathy principles review confirmed: task-based instruction produces bloated, unverifiable work

**Expected impact:**
- Every future article has a 90-day review date; underperformers get a structured update pass instead of being forgotten
- Monthly loop surfaces problems before they become invisible

**Status:** Implemented

---

## 2026-04-16 — International SEO Strategy: Market Keyword Localization

**Why:**
CZ brand SEO is strong (pos 2.05 for "bu1", 1553 clicks). Non-brand CZ goalkeeper queries are positions 8–11 — harder to improve incrementally. Meanwhile, BU1 brand is already known in HU, AT, RO with high CTR but no goalkeeper educational content exists in those languages. Local competition is lower; a quality localized article ranks top 3 where it would rank 8 in CZ.

Critical insight: translating the Czech keyword is not the same as using the local search phrase. German users search `Torwart Reaktionstraining`, not `wie man die Reaktion des Torhüters trainiert`.

**What changed:**
- `docs/blog-articles.md` — `market_keywords` field added to frontmatter schema; full "Market Keyword Localization" section with tier system and GSC-confirmed signals
- `docs/translations.md` — "Market Keyword Localization" section added before Translation Depth Rules; tier 1/2/3 locale classification; rule: if market_keywords[locale] exists, H1 + seo_title use it, not the translated Czech keyword
- `docs/content-brief-template.md` — `market_keywords` added to minimum fields for clusters 1–3
- `config/article_generator.json` — `market_seo_tier` added to every locale; `market_seo_tiers` section with rationale and GSC signals

**Data that drove it:**
- GSC bu1sport.com (Jan–Apr 2026): HU `kapusedzés gyakorlatok` pos 3.6, CTR 16.7% — goalkeeper training content works in HU with low competition
- DE `bu1 torwarthandschuhe` pos 1, CTR 50% — brand known, content gap
- RO goalkeeper training article: 94 clicks, 1 345 imp, CTR 7%
- HR `nogometni trening za djecu`: pos 2.1, CTR 17.4%
- AT `bu1`: 62 clicks, pos 1.06, CTR 28.6% — strong brand, zero goalkeeper educational content

**Expected impact:**
- HU/DE/RO/HR translations rank significantly higher because H1/seo_title match actual local search phrasing
- Tier 1 markets (SK, HU, DE) produce compounding organic traffic from goalkeeper content within 6 months

**Status:** Implemented

---

## 2026-04-16 — Data-Driven Topic Cluster Priority Revision

**Why:**
Previous priority sequence (1→2→3→4→5) was editorial intuition. GSC + GA4 data now allows evidence-based ordering. Cluster 4 (Glove Education) was ranked #4 but has the strongest commercial case: the collection page has 29 518 impressions and 1.65% CTR — educational blog content is the highest-leverage way to improve that CTR.

**What changed:**
- `docs/topic-cluster-map.md` — full rewrite: "Data signals" section added to every cluster with concrete GSC/GA4 numbers; priority sequence revised to 1→4→2→3→5 with rationale; "Data Sources and Refresh Schedule" table added

**Previous priority:**
1. Goalkeeper Fundamentals
2. Match Situations
3. Goalkeeper Distribution
4. Glove Education ← was here
5. Youth Development

**New priority:**
1. Goalkeeper Fundamentals (confirmed: #2 blog article by clicks, 16% bounce)
2. **Glove Education** ← moved up: 29k impressions on collection, 1.65% CTR
3. Match Situations (EN international demand confirmed: 20k imp on penalty article)
4. Goalkeeper Distribution (brand-building, lower immediate SEO return)
5. Youth Development (email-confirmed audience, lower search-capture potential)

**Data that drove it:**
- `/collections/brankarske-rukavice`: 29 518 GSC impressions, 487 clicks, CTR 1.65%
- `brankářské rukavice` query: 4 772 imp, pos 8.2 — bottom of page 1
- `brankářské rukavice dětské`: 1 159 imp, pos 10.3 — no blog content for this
- EN `top-10-most-famous-penalties`: 20 927 imp on bu1sport.com

**Status:** Implemented

---

## 2026-04-16 — Karpathy Principles Adapted for BU1 Content Ops

**Why:**
Reviewed Andrej Karpathy's observations about LLM coding pitfalls (via forrestchang/andrej-karpathy-skills). Four principles map directly to content operations, with modifications for this domain.

**What was adopted and where:**

| Karpathy principle | BU1 adaptation | Implemented in |
|---|---|---|
| Think Before Coding | `open_questions` checkpoint: all ambiguities resolved before writing | frontmatter, content-brief-template.md |
| Simplicity First | "One search intent per article" editorial rule | blog-articles.md |
| Surgical Changes | Surgical translation updates: only changed sections get re-translated | translations.md |
| Goal-Driven Execution | `success_criteria` in frontmatter + monthly monitoring loop | blog-articles.md, goals.md, monitoring-loop.md |

**What was NOT adopted:**
- Test-first for content (overengineering — content is not code)
- Code-level surgical changes (translations follow different rules than code diffs)

**Status:** Implemented

---

## 2026-04-10 — First Goalkeeper Cluster Articles Published

**Why:**
Keyword gap analysis (2026-04-10) identified goalkeeper training queries as entirely missing from the blog despite being core to BU1's authority. Decision to fill the highest-value gaps first.

**What changed:**
- 4 articles published as Shopify drafts:
  - `jak-trenovat-postreh-brankare` (GID: 564468088915)
  - `brankarska-rozcvicka-pred-zapasem` (GID: 564468351059)
  - `rozehravka-brankare-nohama` (GID: 564468383827)
  - `postoj-brankare-v-poli` (GID: 564725514323)

**Note:** Articles published before success_criteria framework existed. Baseline data to be set retroactively in next session.

**Status:** Published (draft → needs success_criteria backfill)

---

## 2026-04-10 — Keyword Gap Analysis (Without GSC)

**Why:**
No formal content backlog existed. Analysis done from title-clustering of 122 existing articles + public search signal research.

**Limitation noted at time of writing:**
> "This is not a first-party keyword analysis from Google Search Console or GA4. When those data sources are connected, the backlog should be re-ranked."

**Status:** Superseded — GSC and GA4 now connected (2026-04-16). See `docs/topic-cluster-map.md` for data-confirmed priority.

---

## Pre-2026 — Translation System Established

**Why:**
BU1 operates 12 locales (cs source + 11 translations). Manual translation at scale was unsustainable.

**What exists:**
- Translation workflow, QC script (`scripts/validate_translations.py`), upload script (`scripts/upload_blog_articles.mjs`)
- Coverage targets: 100% for EN/DE/PL/SK; 95%+ for others
- 12-locale Shopify store architecture across bu1.cz and bu1sport.com

**Status:** Active system, iteratively improved.
