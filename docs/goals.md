# BU1 Content & SEO Goals

This document answers three questions for every person or agent working in this project:
**Why does this work exist? What does success look like? How do we know we got there?**

## Why This Project Exists

BU1 is a Czech goalkeeper equipment brand with 9 years of history and a strong domestic brand (position 2.05 for "bu1" in CZ). The business depends almost entirely on organic and direct traffic — all non-brand Google Ads campaigns are paused as of April 2026. The blog is the only active non-brand acquisition channel.

The core tension: BU1 has deep goalkeeper expertise and product trust, but the blog historically spent too much surface area on broad football culture (transfers, history, lifestyle). That content gets impressions but does not convert to glove sales or brand authority.

This project redirects the content operation toward goalkeeper education and equipment decisions — the topics where BU1 has authority AND commercial relevance.

## Primary Goals

### Goal 1: Build goalkeeper content authority in CZ + SK

Rank in the top 3 for the most searched goalkeeper training and equipment queries in Czech and Slovak. These feed the `/collections/brankarske-rukavice` funnel directly.

**Why now:** Non-brand CZ queries like `brankářské rukavice` (4 772 imp, pos 8.2) and `brankářské rukavice dětské` (1 159 imp, pos 10.3) are stuck on page 1 bottom. Supporting educational content can lift the collection page into top 5.

### Goal 2: Expand organically to HU, AT/DE, RO, HR, PL

Brand is already known in these markets (HU: `bu1 kapuskesztyű` pos 1.4; AT: `bu1` pos 1.06; RO: `bu1` pos 1, 74.5% CTR). Goalkeeper content in local language converts at high CTR (HU: 16.7%, HR: 17.4%, RO: 7%) because local competition is low.

**Why now:** CZ/SK SEO is strong but incrementally harder. These markets have confirmed brand awareness + content gaps + lower competition. A well-localized article can rank top 3 in HU or HR where it would rank 8 in CZ.

### Goal 3: Make the blog a conversion asset, not just a traffic asset

Every goalkeeper article should move a reader one step closer to a glove purchase or a glove care page visit. Internal linking to evergreen pages (`/pages/pece-o-rukavice`, `/pages/poradna-jak-spravne-vybrat-brankarske-rukavice`) is the primary mechanism.

**Why now:** The collection page has 29 518 organic impressions and 1.65% CTR. Even a modest CTR improvement from blog-driven authority is worth more than publishing 5 more broad football articles.

### Goal 4: Keep the system self-improving

The content strategy should update itself as data arrives. GSC, GA4, and Klaviyo are connected. A monthly monitoring loop flags gaps and proposes updates — but always waits for human approval before changing anything.

---

## KPIs and Baselines (as of 2026-04-16)

### Blog organic performance (bu1.cz, CZ)

| Metric | Baseline (Jan–Apr 2026) | 6-month target (Oct 2026) |
|---|---|---|
| Total blog GSC clicks (CZ) | ~800 | 2 500 |
| Top blog article clicks | 170 (children training) | 400 |
| Goalkeeper-specific blog clicks | 140 (training drills) | 800 |
| Avg position, non-brand goalkeeper queries | 8–11 | ≤ 5 |

### Collection funnel

| Metric | Baseline | Target |
|---|---|---|
| `/collections/brankarske-rukavice` impressions | 29 518 | — (organic) |
| `/collections/brankarske-rukavice` CTR | 1.65% | 3.0% |
| `brankářské rukavice` query position | 8.2 | ≤ 5 |
| `brankářské rukavice dětské` query position | 10.3 | ≤ 6 |

### International markets (bu1sport.com)

| Market | Baseline signal | 6-month target |
|---|---|---|
| HU goalkeeper content clicks | 11 (`kapusedzés gyakorlatok`) | 80 |
| DE goalkeeper content clicks | 11 (`torwarthandschuhe`) | 60 |
| RO goalkeeper content clicks | 94 (training article) | 250 |
| HR goalkeeper content clicks | 12 (`trening za djecu`) | 60 |

### Email / Klaviyo

| Metric | Baseline | Target |
|---|---|---|
| Content-driven campaigns per quarter | 1 (jarní příprava, Feb 2026) | 3 |
| List growth tied to content | not tracked | establish tracking |

---

## Success Criteria Framework (per article)

Every new goalkeeper article must define success before it is written. These fields live in the draft frontmatter under `success_criteria`.

### Required fields

```yaml
success_criteria:
  primary_goal: "rank top X for [keyword] in [locale] within [timeframe]"
  target_position: 3          # GSC average position
  target_ctr_percent: 5       # GSC CTR for primary keyword
  target_monthly_clicks: 50   # GSC clicks/month after 90 days
  target_bounce_rate: 0.45    # GA4 bounce rate
  internal_click_goal: "1 click to evergreen page per 80 pageviews"
  review_date: YYYY-MM-DD     # 90 days after publish
  baseline_date: YYYY-MM-DD   # publish date
```

### How to set targets

- **Position target**: If the keyword has > 1 000 monthly impressions → target ≤ 3. If 200–1 000 → target ≤ 5. If < 200 → target ≤ 8.
- **CTR target**: Position 1–3 in Czech goalkeeper space historically yields 6–15% CTR. Use 5% as conservative minimum.
- **Monthly clicks**: Position × CTR × estimated monthly impressions. Sanity-check against existing top articles.
- **Review date**: Always 90 days after publish. If target not met → article gets a structured update pass.

### Review protocol (monthly loop)

Once a month, the GSC monitoring loop:
1. Pulls position + CTR + clicks for every published article
2. Compares against `success_criteria` in frontmatter
3. Flags articles where `review_date` has passed AND targets are not met
4. Proposes specific interventions (title change, H2 restructure, internal link addition)
5. **Waits for Petr's approval before making any change**

See `docs/monitoring-loop.md` for setup and schedule.

---

## Seasonal Content Signals

Klaviyo campaign history confirms two recurring content windows when audience engagement peaks:

| Window | Period | Signal |
|---|---|---|
| Equipment season | January–February | "Péče o rukavice" (Jan 2026) + "Střihy rukavic" (Jan 2026) sent — equipment education topics have active audience in this period |
| Spring prep | February–March | "Tréninkové tipy pro jarní přípravu" (Feb 2026) confirmed engagement — goalkeeper training content resonates with list ahead of spring season start |

**Planning use:** Schedule Klaviyo campaigns tied to goalkeeper blog articles in these windows. Content published Oct–Nov has 90 days to build GSC traction before January equipment season.

---

## Review Cadence

| Review type | Frequency | What gets updated |
|---|---|---|
| Article performance vs. success_criteria | Monthly (automated loop) | Article content, meta title, internal links |
| Topic cluster priority | Quarterly | `docs/topic-cluster-map.md` |
| KPI baselines | Quarterly | This file (`docs/goals.md`) |
| agents.md accuracy | After every major workflow change | `agents.md` |
| CHANGELOG | After every strategic decision | `CHANGELOG.md` |

---

## What We Deliberately Don't Optimize For

- **Broad football culture traffic** — transfers, history, lifestyle. Gets impressions, doesn't convert, dilutes topical authority.
- **Volume over depth** — 1 well-localized goalkeeper article > 5 translated broad football pieces.
- **Short-term email open rates** — at the cost of list health or content integrity.
- **Rankings at any cost** — no keyword stuffing, no thin content. Every article must genuinely help a goalkeeper, parent, or coach.
