# LANG-PROJECTS LOOP: /en|ru|fr/projects/ (Ben 25.10.2026)

Ben: "do it at the highest level ... they strengthen each other ... priority English, Russian, French (Arabic: not sure it is
needed) ... per language a small research on the nuances of what people search ... a moat nobody can copy: tools, infographics
... I want these pages first, first ... enter a small loop."

Approved by Ben 25.10.2026: /en/projects/, /ru/projects/, /fr/projects/ are the same page as /projects/ in another language (one
hreflang group with /projects/, x-default /projects/); the buyer guides /xx/new-projects/ stay their own group (guide intent),
cross-linked. Order: en, ru, fr; ar only if demand appears. Research basis: docs/research/2026-10-25-projects-hub/languages.md.

Laws in force: no redirect, no noindex, no indexing request, URL word law (a translation at the same path = same owner, Ben's
reading 25.10), no sitewide mass change in one day (links from the ~140 language pages spread over days), title of /projects/
unchanged, honesty (numbers dated, developer prices as published), language DNA per language (no tech words), release rule
from the 25.10 incident: PHP_RELS lists every hunked file; never make old code require a new file in the same release.

## Board
| # | Step | State |
|---|---|---|
| L1 | SERP per language in Ben's Chrome (en/ru/fr: head terms, AI overview, PAA, related) -> serp-lang.md | **done 25.10** (serp-lang.md: ru head term новостройки + МАМАД; fr programme neuf + prices in euros) |
| L2 | Competitor DNA per language (top pages read in full) + searcher nuances (GSC foreign queries, what foreign/oleh buyers need) -> lang-dna-{en,ru,fr}.md | **done 25.10** (lang-dna-en/ru/fr.md; found: foreign-buyer tax extended to 10.2.2027, Consumer Protection s.17D shekel-only prices, mamad 9 m² net, rooms/m² counting, Israel Lands Law 'foreigner') |
| L3 | Content per language: hub copy written natively (not a literal translation), language-specific sections (foreign buyer tax, olim, non-resident mortgage, FX, power of attorney, buying from abroad), FAQ from that language's PAA | en done (23 FAQ, research findings in); ru done (30 FAQ, новостройки, МАМАД/МАМАК); fr being written |
| L4 | Code: [nadlan_projects_hub lang=..] render (catalog cards in the language, market table labels, tools with en blocks, infographics), hreflang group /projects/ <-> /xx/projects/ (page-lang.php + projects-hub.php), sitemap | **written** (inc/projects-hub-lang.php, names.json, buyer calculator verified to the shekel; release 1.72.514 prepared, make_deploy514.py) |
| L5 | Design preview (phone + desktop) for en | done (preview/preview-en.html, phone checked) |
| L6 | Release (hunk rules), create the WP pages under /en/ /ru/ /fr/, live checks, verify_live per language | **done 25.10**: 513 market, 514 code+en, 515 ru+fr+decimal comma+ptax extension, 516 cards (short names h3, pictures, LTR heading, dateModified), 517 calculator form; pages /en/projects/ 8608, /ru/projects/ 8609, /fr/projects/ 8610 all checks OK; 518 language line, 519 homes: all live |
| L7 | Links: /xx/ homes + /xx/new-projects/ guides -> /xx/projects/ (a few a day), /projects/ <-> language switcher | **done 25.10**: guides en/ru/fr (link_guides.py), language line on all four catalogs (518), en/ru/fr homes link their catalog (519). Proposal only: the sitewide header language menu points to language homes, not the same page |
| L8 | Proof vs each language's competitors (depth + fact coverage), screenshots, links to Ben | **done 25.10**: en/ru/fr ahead on words, figures, tables, FAQ, sources, tools; behind only on pictures (image-card catalogs) and fr headings vs Evenis (46 vs 81); links sent to Ben |

## Follow-ups found
- ptax tool extension to 10.2.2027 rides 515; the Hebrew pages /purchase-tax-calculator/ (8 sentences + description) and /real-estate-tax-advisor/purchase-tax-investor/ (2) are corrected by fix_ptax_extension.py after 515.
- English-speaker cities thin in our data (Beit Shemesh 1, Modiin 2, Efrat 0); French cities have no French project pages (Netanya, Ashdod, Jerusalem, Ra'anana).
- Prices: shekel is the price; the $/€ figure is labelled an approximate conversion (Consumer Protection s.17D). Legal reading for Ben.

## Closed 25.10.2026
Every board step is done and live (1.72.513 to 1.72.519). The loop cron was deleted. Follow-ups are proposals for Ben (proposals-50.md, header language menu, $/€ legal reading).
