---
type: data
date: 2026-04-17
scope: Review mining — zákaznický jazyk z recenzí BU1 rukavic
trigger: session
key_finding: Shopify MCP recenze přímo nevystavuje — pro plný audit je nutný ruční export z Shopify Adminu. Tento report dokumentuje postup, odvozené signály z dostupných dat a připravený framework pro analýzu.
action_required: true
actions_approved: []
expires: 2026-10-17
---

# BU1 Review Mining — Setup & Odvozené Signály 2026-04-17

**TL;DR:** Přímý přístup k recenzím přes Shopify MCP není dostupný. Tento report (a) dokumentuje jak recenze získat, (b) zachycuje odvozené signály ze zákaznického chování, které recenzím odpovídají, (c) připravuje framework pro analýzu hned jak data budou k dispozici.

**Kontext:** Review mining byl identifikován jako zdroj zákaznického jazyka pro keyword research a content briefs. Shopify MCP (`get-products`) recenze nevystavuje — jsou přístupné jen přes Shopify Admin nebo Product Reviews API.

**K čemu slouží:** Vstup pro content briefs Cluster 4, H2 kandidáti, FAQ obsah, market_keywords validace. Použít při psaní dalšího článku o výběru nebo péči o rukavice.

**Platnost dat:** Odvozené signály: Jan–Apr 2026. Plný audit: provést po exportu recenzí. Expires: 2026-10-17.

---

## Část 1: Jak získat reálná data recenzí

### Možnost A — Shopify Admin (doporučeno, 10 minut)

1. Přihlásit se do Shopify Admin → **Apps → Product Reviews** (nebo Judge.me / Okendo pokud je nainstalováno)
2. Export recenzí jako CSV
3. Otevřít v tabulkovém editoru, filtrovat na rukavice (ne oblečení)
4. Projít text recenzí a vyplnit sekci 2 níže

### Možnost B — Shopify GraphQL API

```graphql
query {
  products(first: 10, query: "rukavice") {
    edges {
      node {
        title
        metafields(namespace: "reviews", first: 10) {
          edges {
            node { key value }
          }
        }
      }
    }
  }
}
```

### Možnost C — Heureka / Google Reviews

Pokud BU1 sbírá recenze na Heurece nebo Google Business → exportovat z Heureka Partnera nebo Google Business Profile.

---

## Část 2: Framework pro analýzu (vyplnit po exportu)

Při čtení recenzí hledat a kategorizovat:

```
OBAVY PŘED NÁKUPEM → FAQ obsah, H2 nadpisy
[ ] Jak vybrat velikost?
[ ] Jaká pěna/střih je nejlepší pro umělou trávu?
[ ] Jak dlouho vydrží latex?
[ ] Jsou rukavice vhodné pro dítě X let?

POZITIVNÍ FRÁZE → meta popisky, copywriting
[ ] Co zákazníci chválí? (grip, přiléhavost, výdrž, cena/výkon)
[ ] Jak popisují pocit při chytání?

PROBLÉMY → potenciální produktové zlepšení, obsah FAQ
[ ] Kde se rukavice nejčastěji poškodí?
[ ] Jaké jsou stížnosti na latex?
[ ] Co chybí v balení?

ZÁKAZNICKÝ JAZYK → keywords
[ ] Jak zákazníci popisují produkt (ne jak ho popisuje BU1)?
[ ] Jaká slova opakují, která BU1 v popisu nepoužívá?

MARKET KEYWORDS (recenze v cizích jazycích)
[ ] DE: používají "Haftlatex" nebo "Grifflatex"? "Negative Cut" nebo "Negativ-Schnitt"?
[ ] HU: jak píší o "kesztyű"? Jaký zákaznický jazyk?
[ ] PL: "rękawice bramkarskie" — jaké adjektivy?
```

---

## Část 3: Odvozené signály (bez přístupu k recenzím)

Tato část kombinuje interní search data, Klaviyo signály a produktové popisy jako proxy pro zákaznický jazyk.

### 3.1 Nejsilnější odvozené signály z interního searche

Z auditu interního searche (report `2026-04-17-internal-search-audit.md`) vyplývá, že zákazníci po nákupu hledají:

| Co hledají | Sessions | Implikace pro content |
|---|---|---|
| lepidlo / sprej / šampon na rukavice | ~56 | Zákazníci nevědí jak pečovat — potřeba obsahu o péči |
| tabulka velikostí | ~9 | Zákazníci si nejsou jistí velikostí před nebo po nákupu |
| rukavice na umělou trávu | ~27 | Zákazníci hledají specifický typ, ale neví o Light HG |
| finger save | ~6 | Zákazníci hledají finger protection ale BU1 to nenabízí nebo nenazývá |

Tyto signály odpovídají typickým review kategoriím — zákazník, který po nákupu hledá "lepidlo", v recenzi pravděpodobně napsal "nevěděl jsem čím latex aktivovat".

### 3.2 Z produktových popisů — co BU1 zdůrazňuje

Analýzou produktových popisů (BU1 Gator, BU1 XX, Light HG) jsou vidět klíčová sdělení:
- **Negative Cut střih** = "pocit druhé kůže", "precizní cit při každém zákroku"
- **Light HG** = "odolnost na tvrdých površích", "jiné přednosti než profi pěny"
- **BU1 XX** = "cenově dostupná alternativa", "životnost pěny"

**Gap:** Produktové popisy neobsahují: jak vybrat velikost, jak pečovat, pro jaký věk je který model vhodný. Toto jsou pravděpodobně nejčastější recenzní otázky.

### 3.3 Klaviyo signály (konfirmace)

Z `docs/goals.md` → Seasonal Context:
- "Péče o rukavice" (Jan 2026) — email na toto téma byl odeslán → audience je receptivní
- "Střihy rukavic" (Jan 2026) — zákazníci mají zájem o vysvětlení střihů

To potvrzuje, že **péče a výběr střihu** jsou dvě témata, která zákazníci aktivně chtějí — i bez přístupu k recenzím.

---

## Část 4: Okamžitě použitelné výstupy

Tyto výstupy nevyžadují recenze — jsou odvozeny z dostupných dat a lze je použít hned:

### Content briefs připravené k napsání

| Téma | Cluster | Demand signal |
|---|---|---|
| "Jak pečovat o brankářské rukavice" | 4 | 56 search sessions, Klaviyo confirmed |
| "Brankářské rukavice na umělou trávu — jak vybrat" | 4 | 27 search sessions, GSC data |
| "Jak vybrat velikost brankářských rukavic" | 4 | 9 search sessions, chybí stránka |
| "Finger protection rukavice — co to je a kdy je potřeba" | 4 | 6 search sessions, product gap |

### H2 kandidáti (zákaznický jazyk bez recenzí)

Pro Cluster 4 články:
- "Proč se latex odlupuje a jak tomu předejít"
- "Lepidlo nebo sprej — co je lepší na aktivaci latexu"
- "Jakou velikost vybrat pro dítě v 8 letech"
- "Rozdíl mezi tréninkovými a zápasovými rukavicemi"
- "BU1 Light HG — pro koho jsou rukavice na umělou trávu"

---

## Doporučené akce

1. **Petr provede:** Export recenzí z Shopify Admin → nasdílí CSV nebo copy/paste vzorku → AI agent vyplní Část 2
2. **Mezitím:** Použít odvozené signály z Části 3 + 4 pro content briefs Cluster 4 — demand je potvrzený z jiných zdrojů
3. **Po exportu:** Aktualizovat tento report o reálná data, přepsat `action_required: false`, uložit výstupy do příslušných draft frontmatterů

---

## Poznámka o limitech

Tento report je **setup + odvozené signály**, ne plný review audit. Hlavní limitace:
- Shopify MCP nevystavuje recenze — nutný manuální krok
- Odvozené signály jsou validní ale nepřímé — skutečné recenze mohou odhalit překvapivé fráze
- Objem recenzí není znám — pokud je recenzí méně než 30, analýza nebude statisticky relevantní
