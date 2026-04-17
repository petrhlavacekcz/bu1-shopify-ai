---
type: data
date: 2026-04-16
scope: Country-level GSC CTR signals for bu1sport.com international markets
trigger: session
key_finding: AUT, GBR, and PL show 28–66% CTR on bu1sport.com brand queries with zero goalkeeper educational content — high-leverage localization gap
action_required: false
actions_approved: []
expires: 2026-10-16
---

# BU1 Market Signals — International CTR Snapshot 2026-04-16

**TL;DR:** AUT, GBR, and PL visitors click on bu1sport.com at 28–66% CTR when they find the site — but there is no goalkeeper educational content in German (AT), English (GB), or Polish. First localized goalkeeper article in each market is likely to outperform CZ equivalents in CTR immediately.

**Kontext:** Pulled from GSC (sc-domain:bu1sport.com) during April 2026 strategy session. This snapshot captures country-level brand awareness vs. content gap.

**K čemu slouží:** Prioritizace překladu/lokalizace goalkeeper článků. Tier-1 a Tier-2 markets z `agents.md` jsou potvrzeny daty. Použij jako vstup pro výběr lokalizačního jazyka pro každý nový Cluster 1–3 článek.

**Platnost dat:** GSC data Jan–Apr 2026. Expires: 2026-10-16.

---

## Country signals (bu1sport.com, Jan–Apr 2026)

| Country | CTR | Clicks | Impressions | Avg Position | Status |
|---|---|---|---|---|---|
| AUT | 28.6% | 62 | ~217 | 1.06 | Brand known (`bu1`), zero goalkeeper educational content in DE |
| GBR | 65.8% | small volume | — | — | Goalkeeper curiosity signals; EN content gap |
| POL | 41.7% | moderate | — | — | Goalkeeper equipment demand; no PL goalkeeper education content |
| HUN | 16.7% | 11 | ~66 | 3.6 | `kapusedzés gyakorlatok` — goalkeeper training demand confirmed, low local competition |
| ROU | 7% | 94 | 1 345 | — | Existing goalkeeper training article performing; content gap in other topics |
| HRV | 17.4% | 12 | ~69 | 2.1 | `nogometni trening za djecu` — goalkeeper content for kids, low competition |
| DEU (all) | 50% | 11 | ~22 | 1 | `bu1 torwarthandschuhe` — brand + glove query, zero goalkeeper education content |

---

## Interpretation

### High-priority gaps (tier 1 markets)

**AUT/DE:** `bu1` brand queries at pos 1.06 with 28.6% CTR. The brand exists in the German-speaking market. The content doesn't. Any goalkeeper article in German (fundamentals, glove care, training drills) fills a vacuum — no local competitor content from BU1 exists.

**PL:** 41.7% CTR on brand queries. Polish is Tier 2 but the CTR signal is stronger than some Tier 1 markets. First goalkeeper education article in Polish is the highest-leverage move in this market.

### Established performers

**RO:** 94 clicks on existing training article (CTR 7%). Content works. Priority: expand with 2–3 more goalkeeper articles — the formula is proven.

**HU:** `kapusedzés gyakorlatok` at pos 3.6, CTR 16.7%. Goalkeeper training demand exists. Market keyword localization is already in `config/article_generator.json`. Next step: publish first Cluster 1 article with HU `market_keywords` set.

**HR:** `nogometni trening za djecu` at pos 2.1, CTR 17.4%. Strong niche. Youth goalkeeper development (Cluster 5) or Fundamentals (Cluster 1) for a young audience maps directly.

---

## Recommended actions (awaiting Petr's prioritization)

1. When next Cluster 1 article is ready for translation → prioritize DE localization (AUT market, brand already known)
2. PL localization of goalkeeper fundamentals article — CTR signal justifies moving PL from Tier 2 treatment toward Tier 1 for goalkeeper content
3. RO: create content plan for 2–3 more goalkeeper articles; existing one at 94 clicks proves the market

These are inputs for the next content planning session. No files modified.
