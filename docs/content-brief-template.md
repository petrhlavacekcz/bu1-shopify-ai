# Content Brief

**The brief lives in the draft file's YAML frontmatter.** One article = one file in `drafts/blog/`.

See `docs/blog-articles.md` → **Draft File Format** for the canonical schema.

---

## Required frontmatter fields

- `title`
- `primary_keyword` — validate against `docs/topic-cluster-map.md` → Data signals before choosing
- `secondary_keywords`
- `audience`
- `search_intent`
- `cluster` (1–5, see `docs/topic-cluster-map.md`)
- `business_goal`
- `internal_links` (1–3 from `evergreen_pages` in `config/article_generator.json`)
- `related_articles` (≥1, see `docs/blog-articles.md` → Inter-Article Linking)
- `evidence_sources` (≥2 — cite inline, never as a Zdroje section)
- `open_questions` — must be empty `[]` before writing starts
- `market_keywords` — required for clusters 1–3; see `docs/blog-articles.md` → Market Keyword Localization
- `success_criteria` — required before publishing; see `docs/goals.md` → Success Criteria Framework

---

## Editorial rules

- Goalkeeper, goalkeeper training, youth development, glove choice/care, match situations — these first.
- Solve a real problem for player, parent, or coach.
- Avoid broad football culture unless there is a clear business reason.
- Link to evergreen pages before product collections.
- One search intent per article. Two questions = two articles.

---

## Before choosing a keyword

Check `docs/topic-cluster-map.md` → Data signals for the relevant cluster. The data signals show which queries have impressions but low CTR — those are the highest-leverage targets. Do not duplicate this data here.
