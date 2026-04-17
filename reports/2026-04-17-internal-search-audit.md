---
type: data
date: 2026-04-17
scope: Shopify interní search — co zákazníci hledají přímo v bu1.cz (Jan–Apr 2026)
trigger: session
key_finding: Zákazníci hledají produkty péče o rukavice (lepidlo, sprej, šampon) v 60+ sessions — BU1 je neprodává. Tabulka velikostí chybí jako stránka (5 sessions). Kategorie "umělá tráva" má 22+ sessions ale Light HG není dohledatelný.
action_required: true
actions_approved: []
expires: 2026-10-17
---

# BU1 Interní Search Audit — 2026-04-17

**TL;DR:** GA4 zachytil 641 unikátních search termínů (Jan–Apr 2026). Tři okamžité příležitosti: (1) zákazníci aktivně hledají péčová příslušenství k rukavicím, která BU1 neprodává, (2) chybí size chart stránka, (3) kategorie "umělá tráva" není v navigaci dohledatelná.

**Kontext:** Data z GA4 `view_search_results` eventu, bu1.cz, leden–duben 2026. Celkem 641 unikátních dotazů. Tento report zobrazuje termíny s ≥2 sessions.

**K čemu slouží:** Vstup pro (a) produktový development/sourcing, (b) nové contenthové stránky, (c) navigaci a search optimalizaci v obchodě. Před každým novým content briefem Cluster 4 zkontrolovat tento report.

**Platnost dat:** GA4 Jan–Apr 2026. Expires: 2026-10-17 (obnovit s dalším auditem).

---

## 1. Péče o rukavice — produktová mezera (nejvyšší revenue potenciál)

Zákazníci hledají doplňkové produkty péče, které BU1 aktuálně neprodává. Kombinovaný objem je největší signál v celém datasetu.

| Termín | Sessions | Poznámka |
|---|---|---|
| lepidlo | 15 | aktivátor/lepidlo na latex |
| sprej na rukavice | 13 | rehydratační sprej |
| sprej | 11 | (totéž) |
| šanpón / šampon / šampón na rukavice | ~9 | glove wash |
| lepidlo (variace) | 2+2 | totéž jiným zápisem |
| spreje na rukavice | 2 | |
| glue | 2 | EN varianta |
| **Celkem péčové produkty** | **~56 sessions** | |

**Interpretace:** Zákazník, který koupí BU1 rukavice, za 2–4 týdny přijde hledat jak je udržovat. BU1 tuto poptávku aktuálně posílá ke konkurenci. Tři možné akce:
- **A) Sourcing:** přidat glove wash + latex spray do katalogu jako cross-sell k rukavicím
- **B) Obsah:** rozšířit `/pages/pece-o-rukavice` o konkrétní doporučení produktů třetích stran s affiliate nebo přímým odkazem
- **C) Blog:** Cluster 4 článek "Jak pečovat o brankářské rukavice" (přímý demand signal)

---

## 2. Tabulka velikostí — chybějící stránka

| Termín | Sessions |
|---|---|
| tabulka velikostí | 3+2 = **5** |
| jak vybrat velikost rukavic | 2 |
| velikosti | 2 |
| **Celkem** | **~9 sessions** |

**Interpretace:** Zákazníci aktivně hledají size chart a nenacházejí ho — nebo ho hledají znovu, protože není snadno dostupný. Dedicated `/pages/tabulka-velikosti-brankarske-rukavice` stránka by vyřešila both interní search i GSC organic dotazy. Tato stránka zároveň přirozeně interně odkazuje na kolekci rukavic.

**Okamžitá akce:** Zkontrolovat, zda size chart existuje v produktových popisech nebo jako stránka. Pokud ne → vytvořit jako evergreen page + přidat do navigace.

---

## 3. Umělá tráva — kategorie existuje, ale není dohledatelná

| Termín | Sessions |
|---|---|
| umělá tráva | 8+6+3 = **17** |
| rukavice na umělou trávu | 3+2 = **5** |
| BU1 Light HG 2.0 | 3 |
| do haly | 2 |
| **Celkem** | **~27 sessions** |

**Interpretace:** BU1 Light HG (pro umělou trávu) existuje a zákazníci ho hledají — ale hledají ho přes interní search, ne přes navigaci nebo kategorii. To znamená, že buď není v menu dostatečně viditelný, nebo SEO handle/popis neobsahuje klíčová slova "umělá tráva".

**Akce:**
- Přidat filtr nebo kategorii "Umělá tráva" do kolekce rukavic
- Přidat "umělá tráva" + "HG" do product tagů
- Blog článek: "Brankářské rukavice na umělou trávu — co vybrat" (Cluster 4, přímý demand)

---

## 4. Chrániče — produktová mezera

| Termín | Sessions |
|---|---|
| chranice / chrániče | 6+5 = **11** |
| brankárske chraniče kolen | 3 |
| **Celkem** | **~14 sessions** |

**Interpretace:** Zákazníci hledají brankářské chrániče kolen/loktů — produkty, které BU1 aktuálně neprodává. Třetí největší produktová mezera po péčových produktech.

**Akce:** Zvážit sourcing nebo partnerství. Případně blog obsah "Jaké chrániče potřebuje brankář" s odkazem na doporučení externího produktu.

---

## 5. Navigační a findability problémy

| Termín | Sessions | Problém |
|---|---|---|
| brankářské rukavice pro děti | 3 | Junior kolekce existuje, ale není surfovaná |
| junior / dětské | 3+2 = 5 | Totéž |
| finger save / fingersave | 4+2 = **6** | Model s finger save hledán, název musí být v tagu/filtru |
| voucher | 3 | Gift card — Shopify má nativní funkcionalitu, BU1 ji nemá aktivní |
| pece o rukavice | 2 | Evergreen stránka existuje, ale vyhledávání ji nevrací |
| vraceni zbozi | 2 | Returns stránka není snadno dohledatelná |
| do haly | 2 | Halové rukavice — samostatná kategorie nebo filtr chybí |
| Reakčna doska (SK) | 3 | Tréninkové vybavení — mimo katalog |
| batoh | 5 | Batoh — mimo katalog |
| taska na rukavice | 3 | Glove bag — mimo katalog |

---

## 6. Produktové dotazy s nulovým výsledkem (pravděpodobně)

Tyto termíny naznačují poptávku po produktech mimo aktuální katalog. Slouží jako vstup pro **produktový development Q3/Q4 2026**:

| Produkt | Sessions | Priorita |
|---|---|---|
| Péčové produkty (lepidlo, sprej, šampon) | ~56 | **Vysoká** — cross-sell k existujícímu katalogu |
| Tabulka velikostí (stránka) | ~9 | **Vysoká** — 0 effort, vysoký dopad |
| Chrániče kolen/loktů | ~14 | Střední — sourcing/partnerství |
| Voucher / dárkový poukaz | 3 | Střední — Shopify nativní, snadná aktivace |
| Batoh / taška na míče | 5+3 = 8 | Nízká — mimo core |
| Zimní rukavice (tréninkové) | 3 | Nízká — sezónní |

---

## Doporučené akce (čekají na schválení Petra)

1. **Okamžitě (0 effort):** Přidat "umělá tráva" tag na Light HG produkty + přidat do navigace jako filtr
2. **Tento týden:** Vytvořit `/pages/tabulka-velikosti-brankarske-rukavice` — size chart pro všechny modely
3. **Tento měsíc:** Rozšířit `/pages/pece-o-rukavice` o sekci doporučených péčových produktů (even bez přímého prodeje)
4. **Content brief:** Cluster 4 článek "Brankářské rukavice na umělou trávu" — demand je potvrzený
5. **Zvážit (Q3 2026):** Aktivovat Shopify gift cards, sourcing péčových produktů jako bundle k rukavicím

---

## Metodologie

- Zdroj: GA4 `view_search_results` event, sc-domain bu1.cz
- Období: 2026-01-17 – 2026-04-17 (90 dní)
- Celkem unikátních termínů: 641
- Tento report zobrazuje termíny s ≥2 sessions (threshold: eliminuje překlepy a jednorázové dotazy)
- Termíny s mezerami/překlepy sloučeny (např. "sprej" + "sprej na rukavice" + "spreje na rukavice")
