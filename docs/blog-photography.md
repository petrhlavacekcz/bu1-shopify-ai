# BU1 Blog Photography

Brand rules: see [`docs/brand.md`](brand.md)

## Purpose

Guidelines for planning, generating, and placing images for BU1 blog articles.

This workflow combines:
- **Google Search Central** image SEO guidance: images should use standard HTML, sit near relevant text, and have useful alt text
- **W3C / web.dev** accessibility guidance: alt text should describe the image's meaning, not just its appearance
- **GOV.UK / public-sector content guidance**: every blog post needs a strong top image, but too many images hurt scanability

**Important:** those sources do **not** prescribe a universal "1 image per X words" formula. The count and placement rules below are a **BU1 editorial heuristic** derived from those sources and tuned for long-form goalkeeper content.

## Image Roles

| Role | Purpose | Placement |
|---|---|---|
| `hero` | Main article visual / featured image | Top of article only |
| Inline photo | Shows a drill, posture, match situation, or environment referenced in the text | After a relevant H2 |
| Inline infographic | Clarifies a comparison, process, timeline, or biomechanical cue | After a relevant H2 |

## Count Heuristic

Use the **minimum** number of images that improves understanding.

| Article length | Minimum | Default target | Hard ceiling |
|---|---|---|---|
| under 900 words | 1 image | 1 | 2 |
| 900-1500 words | 2 images | 2-3 | 4 |
| over 1500 words | 3 images | 3-4 | 5 |

Rules:
- Every article needs **exactly 1 `hero` image**.
- If you only have one image, it must be the hero at the top.
- Inline images must **teach, clarify, or visualize** something the section is discussing.
- Do **not** add images only to "make the page look less empty".

## Placement Rules

1. `hero` image goes at the top of the article and should represent the main promise of the piece.
2. First inline image must appear **after the first or second H2**.
3. For longer articles, spread inline images across the piece. Do not cluster them under one section.
4. Every inline image must be anchored to a real H2 via `after_heading` in frontmatter.
5. Do not attach multiple inline images to the same H2 unless the section genuinely needs a photo + diagram pair.
6. Do not use back-to-back decorative visuals with no new information.

## Dimensions & Format

- **Hero target**: 1600 × 900 px minimum, 16:9
- **Inline target**: 1200 px wide minimum, landscape
- **Format**: WebP preferred, JPEG fallback
- **Max file size**: 500 KB target for inline images, 1 MB ceiling for hero

## Source Draft Schema

Use the `images` block in the Czech source draft. `role` values must be unique machine-readable slugs.

```md
images:
  - role: hero
    kind: photo
    size: 1600x900
    placement: top
    alt: Brankář při rozehrávce nohama otevírá tělo do volného prostoru.
    prompt: "Realistic sports photo, goalkeeper distributing with feet, open body, 16:9"
  - role: body-shape-scan
    kind: infographic
    size: 1200x800
    placement: after_h2
    after_heading: "Chyba 1: Brankář si bere první dotek proti tlaku"
    alt: Otevřené tělo brankáře vytváří bezpečný úhel pro další přihrávku.
    caption: Otevřený první dotek nevytváří efekt. Vytváří čas na další rozhodnutí.
    product_refs:
      - https://bu1sport.com/products/bu1-triangle-nc
    prompt: "Clean football infographic, goalkeeper opening body shape to receive a back pass..."
```

Rules:
- `kind`: `photo` | `infographic` | `diagram` | `chart` | `timeline`
- `placement`: `top` or `after_h2`
- `after_heading` is required for every non-hero image
- `caption` is required for `infographic`, `diagram`, `chart`, and `timeline`
- `product_refs` is optional, but recommended whenever a person in the image should wear real BU1 gear from the store

## BU1 Product-Grounded Visuals

If a generated image shows a person wearing BU1 gear, the visual must be grounded in **real store products**, not invented BU1 styling.

### What source to use

Use sources in this order:

1. `config/article_generator.json` → `internal_links` / `glove_models`
2. product URLs discovered from BU1 product sitemaps
3. real PDP imagery or Shopify product data

### Important distinction

- **Sitemap is good for discovery**: it gives handles, URLs, and coverage across locales
- **Sitemap is not enough for fidelity**: it does not tell you the glove color blocking, cut details, jersey pattern, or exact visual appearance

If the goal is "goalkeeper in BU1 Triangle gloves", the workflow should:
1. resolve the real product URL from config or sitemap
2. inspect the live product page or Shopify product media
3. use those details as grounding notes in the prompt

### Codex / CLI role

Yes, Codex can orchestrate this layer, but not in the simplistic sense of "CLI generates the picture".

- **Codex / Codex CLI** is the orchestrator: choose article sections, map product references, generate prompts, run validators, and update draft metadata
- **Image model** is the renderer: generate the actual raster asset
- **Shopify workflow** is the publisher: later upload the asset and attach it to the article

That means the right mental model is:

`Codex planning + product grounding + validation` → `image generation` → `Shopify upload`

### When branded product visuals are allowed

Allowed:
- real BU1 glove model from store is explicitly referenced
- article has commercial relevance to the product being shown
- prompt uses real product cues gathered from store data

Not allowed:
- random pink/black gloves labeled as "BU1 style"
- invented model details that do not map to any real product
- generic apparel branded as BU1 without a real store reference

## Alt Text Rules

- Alt text describes the **meaning of the image in context**, not a robotic literal description.
- Keep alt text **specific and concise**. Cap at **150 characters**.
- Do not start with "Obrázek", "Foto", "Image of", or "Photo of".
- Do not keyword-stuff.
- If the visual contains essential information beyond what fits in alt text, restate the takeaway in the caption or surrounding copy.

Good:

```md
alt: Brankář po prvním zákroku okamžitě znovu otevírá postoj pro dorážku.
```

Weak:

```md
alt: Obrázek brankáře při tréninku.
```

## AI Image Generation Guidelines

- Prompt language: always English
- Style: hyper-realistic sports photography, magazine quality
- No text overlays, logos, or watermarks in generated images
- No invented BU1 product placement in AI images
- Specific, not generic: prompt must reference actual article content
- Use diagrams/infographics only when the section is genuinely easier to understand visually

If BU1 products appear in the image:
- resolve them from real product URLs first
- use `product_refs` in draft metadata
- prefer a faithful representation over an aggressively branded fantasy shot

## Prompt Structure

Each prompt should include:

1. **Subject**: specific person/action/scene from the article
2. **Technical**: camera model, lens, aperture, ISO when useful
3. **Composition**: angle, framing, depth of field
4. **Lighting**: natural / stadium / cinematic setup
5. **Environment**: pitch, weather, training setup, match context
6. **Quality**: "hyper-realistic", "professional sports photography", "magazine quality"
7. **Dimensions**: append the required output size and aspect ratio

## What To Avoid

- Generic stock-photo style images
- Images that repeat the paragraph without adding understanding
- Multiple inline images attached to the same idea just for decoration
- Text-heavy images used instead of readable HTML copy
- BU1 branding in AI-generated photos unless the article explicitly discusses a real BU1 product visual grounded in store data

## Validation

Run the image validator before upload:

```bash
python3 scripts/validate_blog_images.py
python3 scripts/validate_blog_images.py drafts/blog/YYYY-MM-DD-handle.md
```

`scripts/upload_blog_articles.mjs` now runs this validation automatically and aborts if the image plan is weak or incomplete.

## Example Prompt

```text
Young goalkeeper (14-15 years old) in full goalkeeper kit diving to catch a high cross ball
during training session on a grass pitch. Dynamic mid-air action shot. Shot with Canon EOS R5,
70-200mm f/2.8 lens, 1/2000s shutter speed, ISO 800. Low-angle composition, shallow depth
of field with blurred stadium background. Golden hour side lighting creating dramatic shadows.
Green grass field with training cones visible. Hyper-realistic, 8K UHD, professional sports
photography, magazine quality. Dimensions: 2560x1440 pixels, 16:9 aspect ratio.
```
