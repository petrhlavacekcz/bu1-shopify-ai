# BU1 System Capabilities & Ideas

Tento dokument mapuje, co vše lze se současnou architekturou BU1 (Shopify + GSC + GA4 + Klaviyo + AI) podniknout. Slouží jako zásobník pro prioritizaci dalších kroků.

---

## 1. Internal Link Intelligence (Conversion Optimizer)
**Cíl:** Proměnit blog z "čtečky" na "prodejce".
*   **Co:** Automatická identifikace chybějících prodejních odkazů v edukativním obsahu.
*   **Jak:** Agent porovná text článku se seznamem evergreen stránek a kolekcí v `config/article_generator.json`. Najde sémanticky vhodná místa, kde chybí odkaz na `brankarske-rukavice` nebo `pece-o-rukavice`.
*   **Data:** `config/article_generator.json`, lokální `.md` drafty, Shopify Product/Collection list.
*   **Dopad:** Zvýšení CTR z blogu do e-shopu (Goal 3 v `goals.md`).

## 2. International Growth Sniper (SEO Expansion)
**Cíl:** Dominovat na trzích s nízkou konkurencí (HU, RO, HR, PL).
*   **Co:** Chirurgické SEO opravy pro mezinárodní mutace na základě reálného výkonu.
*   **Jak:** Analýza GSC dat pro konkrétní locale. Identifikace dotazů na 5.–15. místě ("low hanging fruit"). Návrh na úpravu meta-titulků nebo přidání lokálně specifického odstavce (např. zmínka o oblíbeném lokálním brankáři).
*   **Data:** GSC API (skrz `mcp__gsc`), `reports/ga4_locale.json`.
*   **Dopad:** Rychlý nárůst organické návštěvnosti v HU/RO/HR (Goal 2 v `goals.md`).

## 3. Klaviyo Content Bridge (Lifecycle Engagement)
**Cíl:** Maximálně vytěžit nový obsah skrze e-mailing.
*   **Co:** Automatická transformace blogového článku do formátu e-mailové kampaně.
*   **Jak:** Agent vezme hotový `.md` článek a vytvoří: 1. Předmět a preview text, 2. Zkrácenou verzi ("teaser") pro e-mail, 3. Call-to-action linky. Vše v brand voice BU1.
*   **Data:** `drafts/blog/*.md`, `docs/brand.md`, Klaviyo segmenty.
*   **Dopad:** Vyšší open-rate a engagement u stávajících zákazníků, využití sezónních signálů (Spring prep).

## 4. Success Criteria Auditor (Performance Monitoring)
**Cíl:** Ověřit, zda se investice do obsahu vrací.
*   **Co:** Automatizovaný audit článků 90 dní po publikaci.
*   **Jak:** Skript projde frontmatter článků, vytáhne `success_criteria` a porovná je s realitou v GSC/GA4. Pokud článek neplní cíle, navrhne konkrétní "záchrannou" akci (např. změna H1, přidání interních odkazů).
*   **Data:** Markdown frontmatter (`target_position`, `target_monthly_clicks`), GSC, GA4.
*   **Dopad:** Udržování "živého" a výkonného obsahu (Goal 4 v `goals.md`).

## 5. Visual SEO & Alt-Text Localizer (Accessibility/Image SEO)
**Cíl:** Získat traffic z Google Images ve všech 12 jazycích.
*   **Co:** Automatická lokalizace Alt textů a popisků obrázků.
*   **Jak:** Na základě hlavního klíčového slova pro daný trh (např. `kapuskesztyű` pro HU) vygeneruje relevantní a SEO-optimalizované Alt texty pro všechny obrázky v článku.
*   **Data:** `docs/blog-photography.md`, `config/article_generator.json` (market_seo_tiers).
*   **Dopad:** Lepší indexace obrázků a přístupnost webu.

## 6. Topic Cluster Gap Analysis (Content Strategy)
**Cíl:** Najít, co brankáři hledají, ale my o tom ještě nepíšeme.
*   **Co:** Porovnání GSC dotazů, na které se web zobrazuje (ale nemá na ně článek), s mapou clusterů.
*   **Jak:** Analýza dotazů s vysokým počtem impresí a špatnou pozicí/CTR. Pokud dotaz nepatří do žádného existujícího článku, navrhne nový content brief.
*   **Data:** GSC Search Queries, `docs/topic-cluster-map.md`.
*   **Dopad:** Rozšiřování autority v CZ/SK (Goal 1 v `goals.md`).

## 7. Paid-to-Organic Search Term Miner (Ads -> Content)
**Cíl:** Psát o tom, co prokazatelně prodává.
*   **Co:** Extrakce vyhledávacích dotazů z Ads, které v minulosti vedly ke konverzi, a jejich porovnání s blogem.
*   **Jak:** Agent projde "Search Term Report" z Google Ads. Identifikuje dotazy s vysokým konverzním poměrem. Pokud na tento dotaz neexistuje hloubkový článek (Cluster 4), navrhne jeho vytvoření.
*   **Data:** Google Ads (`mcp__google-ads-mcp`), `docs/topic-cluster-map.md`.
*   **Dopad:** Obsah s vysokou pravděpodobností prodejního úspěchu.

## 8. Quality Score Content Booster (Ads Efficiency)
**Cíl:** Snížit cenu za proklik (CPC) u brandových kampaní.
*   **Co:** Optimalizace přistávacích stránek pro zvýšení "Ad Relevance" a "Landing Page Experience".
*   **Jak:** Analýza komponent Quality Score v Ads. Agent navrhne úpravu textu na stránce (meta tagy, nadpisy, hustota klíčových slov), aby lépe odpovídaly textům reklam.
*   **Data:** Google Ads Quality Score, Shopify Page/Product content.
*   **Dopad:** Nižší náklady na reklamu a lepší pozice v aukcích.

## 9. Market Demand Validator (Pre-SEO Testing)
**Cíl:** Neriskovat čas na překlady článků pro trhy, kde není zájem.
*   **Co:** Testování poptávky v nové lokalitě (např. BG, PL) pomocí mikro-kampaní před psaním obsahu.
*   **Jak:** Místo psaní 5 článků v polštině spustíme na týden levnou reklamu na hlavní klíčová slova. Agent vyhodnotí CTR a objem impresí. Pokud je zájem potvrzen, spustí se produkce obsahu.
*   **Data:** Google Ads Keyword Planner / Campaign performance.
*   **Dopad:** Efektivní alokace času na překlady a lokalizaci (Goal 2 v `goals.md`).

## 10. Audience Retargeting Bridge (GA4 -> Ads)
**Cíl:** Vrátit čtenáře blogu zpět k nákupu.
*   **Co:** Vytváření publik pro retargeting na základě hloubky dočtení článku.
*   **Jak:** Propojení GA4 eventů (např. `scroll_depth > 75%` u článku o výběru rukavic) s publiky v Google Ads. Těmto lidem pak Ads zobrazí reklamu na rukavice, o kterých četli.
*   **Data:** GA4 Eventy, Google Ads Audience Manager.
*   **Dopad:** Vyšší ROAS (návratnost investic do reklam).

## 11. Inventory-Driven Content Pulse (Ziskovost vs. Obsah)
**Cíl:** Neprodávat "všechno", ale to, co zrovna dává byznysový smysl.
*   **Co:** Automatické propojování blogu s reálným stavem skladu a marží.
*   **Jak:** Agent projde Shopify inventory. Najde produkty s vysokým stavem skladu. Vyhledá v blogu články, které s nimi sémanticky souvisejí, a navrhne posílení CTA na tyto modely.
*   **Data:** Shopify Inventory, Blog content.
*   **Dopad:** Aktivní pomoc při čištění skladu a podpora maržových produktů.

## 12. Weather-Reactive Goalkeeper Advice (Dynamická personalizace)
**Cíl:** Být "tady a teď" s brankářem v jeho lokalitě.
*   **Co:** Dynamická úprava doporučení produktů podle počasí u zákazníka.
*   **Jak:** Propojení Weather API s lokalitou zákazníka. V deštivých oblastech posílit v obsahu a mailingu modely "Aqua Grip" a produkty pro péči v mokru.
*   **Data:** Weather API, Klaviyo Locale, GSC seasonal queries.
*   **Dopad:** Výrazně vyšší relevance a konverzní poměr v konkrétním čase.

## 13. Skill-Level Behavioral Segmenter (Psychologie čtenáře)
**Cíl:** Segmentace na experty vs. začátečníky/rodiče.
*   **Co:** Profilování zákazníka podle hloubky a typu konzumovaného obsahu.
*   **Jak:** Analýza GA4 eventů. Čtenář "Základního postoje" = začátečník/rodič. Čtenář "Psychologie penalt" = aktivní brankář. Automatické tagování v Klaviyo.
*   **Data:** GA4 Content Engagement, Klaviyo Tags.
*   **Dopad:** Možnost posílat vysoce cílené newslettery (bezpečí pro rodiče vs. technické detaily pro profíky).

## 14. AI "Red Team" Competitor Logic Audit (Reverzní inženýrství)
**Cíl:** Pochopit UX a funkční výhody konkurence.
*   **Co:** Hloubková analýza logiky a prvků u top 3 konkurenčních článků.
*   **Jak:** Agent "přečte" konkurenční weby. Neřeší slova, ale strukturu: Mají interaktivní tabulky? FAQ schémata? Video ukázky? Navrhne funkční vylepšení našeho webu.
*   **Data:** DataForSEO SERP, Browser analysis.
*   **Dopad:** Uzavření "funkční mezery" mezi námi a velkými sportovními řetězci.

## 15. The "Goalkeeper's Slang" Localization QA (Kulturní integrita)
**Cíl:** Získat absolutní důvěru lokální brankářské komunity.
*   **Co:** Audit menu, produktů, stránek a blogu na "brankářskou hantýrku" v 12 jazycích.
*   **Jak:** Porovnání textů s databází lokálních idiomatických termínů (např. "vymést pavučinu" vs. lokální ekvivalent). Odhalení mechanických překladů, které působí neprofesionálně.
*   **Data:** Shopify Menu/Products/Pages, Blog translations, Local sports terminology database.
*   **Dopad:** Přechod z "přeloženého shopu" na "lokální brankářskou autoritu".

## 16. Product-Grounded Visual Merchandising Layer (Image Ops)
**Cíl:** Proměnit blogové obrázky z dekorace na obchodně užitečný asset.
*   **Co:** Generování a doplňování článkových obrázků, které jsou navázané na konkrétní sekce článku a podle potřeby i na reálné BU1 produkty.
*   **Jak:** Codex přečte draft, určí kde má obrázek přinést pochopení nebo rozbít dlouhý text, vybere produktové reference z `config/article_generator.json` a produktových sitemap, připraví prompt a metadata (`role`, `placement`, `after_heading`, `product_refs`, `alt`). Následně se obrázek vygeneruje, validuje a později nahraje do Shopify.
*   **Data:** `drafts/blog/*.md`, `docs/blog-photography.md`, `config/article_generator.json`, product sitemaps / Shopify product media.
*   **Dopad:** Lepší scanability článků, vyšší image SEO, silnější produktový kontext a připravený základ pro future featured-image automation.

## 17. Store-Grounded Creative Direction (AI Image Guardrails)
**Cíl:** Zabránit tomu, aby BU1 vizuály působily jako generické AI sporty bez vazby na reálný sortiment.
*   **Co:** Vrstva, která převádí BU1 produktový katalog do promptovacích pravidel pro obrázky.
*   **Jak:** Agent nepoužije jen sitemap URL jako seznam produktů, ale dohledá reálný model, PDP a vizuální cues. Sitemap slouží k objevování handle/URL; věrnost vzhledu se bere z produktové stránky nebo Shopify media. Pokud chybí grounding, obrázek zůstane nebrandovaný.
*   **Data:** `config/article_generator.json`, product URLs, Shopify PDP imagery, `docs/brand.md`.
*   **Dopad:** Produkt na obrázku odpovídá tomu, co BU1 skutečně prodává. Menší riziko vizuálního nesouladu a lepší návaznost blog → PDP.

---

## Jak s tímto dokumentem pracovat
*   Tento soubor popisuje **současné možnosti** systému. 
*   Pokud chceš něco z tohoto seznamu realizovat, vytvoř konkrétní úkol/skript.
*   Nápady na **nové funkce**, které vyžadují vývoj (např. nové integrace), patří do [docs/growth-backlog.md](growth-backlog.md).
