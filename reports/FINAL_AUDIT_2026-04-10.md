# BU1 Translation Audit — Finální report 2026-04-10

## Doménová struktura
- **CZ**: bu1.cz (čeština, hlavní doména)
- **SK**: bu1.cz/sk (slovenština pod CZ doménou)
- **Ostatní**: bu1sport.com/{locale} (bg, de, en, es, fr, hr, hu, it, pl, ro)

## Analyzováno
- 242 produktů, 101 článků, 51 stránek
- 11 locale, 38,280 překladových záznamů
- Sitemap: 175 produktů, 31 stránek, 49 kolekcí

---

## KRITICKÉ (opravit ihned)

### 1. Broken WordPress obrázky — 5,751 výskytů
**35 článků** obsahuje `<img src="bu1.cz/wp-content/...">` — odkazy na starý WordPress, nefunkční.
- Všech 11 locale affected
- Příklad: `bu1.cz/wp-content/uploads/2016/11/bu1-roman-vales.jpg`
- **Akce**: Přesunout obrázky na Shopify CDN nebo smazat mrtvé reference

### 2. Meta description CTA → bu1.cz — 1,337 výskytů (non-SK)
Překladové meta popisy pro mezinárodní locale říkají "Order at www.bu1.cz >>" místo bu1sport.com.
- Dotčeno: ~130 produktů × 10 locale (vše kromě SK)
- SEO dopad: zákazník z Google klikne, CTA ho pošle na CZ doménu
- **Akce**: Hromadný replace `www.bu1.cz` → `www.bu1sport.com` v meta_description pro non-SK locale
- SK (193x) má bu1.cz bez /sk prefixu — zkontrolovat jestli root redirectuje

### 3. Broken staré WooCommerce linky — 143 výskytů
`bu1.cz/obchod/bu1-army-nc/` atd. — cesty z původního WooCommerce, 100% mrtvé.
- **Akce**: Nahradit `bu1.cz/obchod/{slug}` → `bu1sport.com/products/{new-handle}` nebo smazat

---

## VYSOKÁ PRIORITA

### 4. Chybějící překlady — 2,937 výskytů
Ale po přehodnocení:
- **Handle u modelových názvů (29 produktů)** — ZÁMĚRNÉ, model BU1 Gator = BU1 Gator ve všech jazycích. Toto NENÍ problém.
- **Skutečně chybějící** body_html/meta u:
  - `Currency rate` — všech 11 locale (body_html, meta_description)
  - `BU1 Camo Hybrid` a `BU1 Camo NC` — body_html + handle ve všech locale
  - `Testovací bundle` — body + meta ve všech locale
  - `Potisk` (custom print) — meta_description ve všech locale
  - `BU1 taška na rukavice` — meta_description ve všech locale
  - `Select FB Stratos` — body_html ve všech locale
- **Akce**: Doplnit překlady pro reálné produkty, ignorovat modelové handle

### 5. Czech leak v HR (chorvatština) — 120+ výskytů
Slovo "rukavice" se v chorvatštině skutečně používá pro rukavice obecně, ALE:
- V body_html/meta se vyskytuje v **českém kontextu**: "BU1 Gator rukavice s NC krojem" (česká větná stavba)
- 2 produkty (`Rukavice BU1 na přání`, `Junior BU1 Army 20`) mají "rukavice" leak ve VŠECH locale
- **Akce**: HR — zkontrolovat ručně, rozlišit legitimní HR "rukavice" od CZ leak. Ostatní locale — opravit

### 6. Kolekční/stránkové linky na bu1.cz — 186 + 80 výskytů
- `bu1.cz/collections/brankarske-rukavice` v body textech → `bu1sport.com/{locale}/collections/goalkeeper-gloves`
- `bu1.cz/jak-si-spravne-vybrat-rukavice/` → lokalizovaná verze stránky
- **Akce**: Přemapovat na bu1sport.com s lokalizovanými cestami

---

## STŘEDNÍ PRIORITA

### 7. "Soccer" místo "football" — 98 výskytů
- Většina v EN locale: product_type, body_html, meta_description
- Konkrétní produkty: tričko, batoh, ponožky, chrániče, FIT Pink NC, míč reflex
- **Akce**: Replace "soccer" → "football" v EN překladech

### 8. Body odkazy na bu1.cz — 350 výskytů
Články a produkty s textovými linky na bu1.cz (ne obrázky).
- Blog články, CZ stránky, produktové cross-linky
- **Akce**: Postupně přemapovat na bu1sport.com

### 9. Duplicate (identické s CZ) — 917 výskytů
- **Většina je OK**: modelové tituly (BU1 Gator = BU1 Gator)
- **Skutečný problém**: `BU1 Classic Roll Finger` má identický body_html s CZ ve všech locale
- **Akce**: Zkontrolovat body_html duplicity, tituly modelů ignorovat

---

## NÍZKÁ PRIORITA

### 10. Outdated překlady — 1,460 výskytů
Shopify je označil jako "outdated" — zdrojový CZ text se změnil, překlad ne.
- **Akce**: Postupný review při dalších aktualizacích obsahu

### 11. České handles v sitemap — 7 URL
- `/products/baleni-samponu-pro-tym` → `/products/glove-shampoo-5-pack-team`
- `/pages/us-zakony-shoda` → `/pages/us-compliance`
- `/pages/app-ochrana-soukromi` → `/pages/app-privacy`
- `/pages/tymovy-servis` → `/pages/team-service`
- `/collections/jiz-neni-v-nabidce` → `/collections/discontinued`
- `/collections/oblibene-produkty` → `/collections/popular-products`
- `/collections/vybaveni-a-doplnky` → `/collections/equipment-accessories`

---

## Pokrytí per locale (po přehodnocení)

| Locale | Skutečné problémy | Hlavní issue |
|--------|------------------:|---|
| **HR** | 920 | Nejvíce — CZ leak "rukavice" + domain issues |
| **EN** | 797 | Meta CTA bu1.cz, soccer term |
| **SK** | 771 | bu1.cz bez /sk prefix (info, ne kritické) |
| **HU** | 737 | Meta CTA bu1.cz |
| **FR** | 735 | Meta CTA bu1.cz |
| **ES** | 731 | Meta CTA bu1.cz |
| **IT** | 732 | Meta CTA bu1.cz |
| **RO** | 727 | Meta CTA bu1.cz |
| **BG** | 722 | Meta CTA bu1.cz |
| **DE** | 688 | Meta CTA bu1.cz + 1x CZ leak |
| **PL** | 598 | Nejlépe přeložený locale |
