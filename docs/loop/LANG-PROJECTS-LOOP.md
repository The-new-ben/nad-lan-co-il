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
| L6 | Release (hunk rules), create the WP pages under /en/ /ru/ /fr/, live checks, verify_live per language | 513 market data LIVE 25.10; 514 (code + en) dry-run running; ru+fr data next release |
| L7 | Links: /xx/ homes + /xx/new-projects/ guides -> /xx/projects/ (a few a day), /projects/ <-> language switcher | todo |
| L8 | Proof vs each language's competitors (depth + fact coverage), screenshots, links to Ben | todo |

## Follow-ups found
- ptax tool (ptax.json valid.extra/foreign + ptax.js strings) still says the foreign/additional tax order ends 31.12.2026: extend to 10.2.2027 in its own small release.
- English-speaker cities thin in our data (Beit Shemesh 1, Modiin 2, Efrat 0); French cities have no French project pages (Netanya, Ashdod, Jerusalem, Ra'anana).
- Prices: shekel is the price; the $/€ figure is labelled an approximate conversion (Consumer Protection s.17D). Legal reading for Ben.
