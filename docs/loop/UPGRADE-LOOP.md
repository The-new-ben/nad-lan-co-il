# UPGRADE LOOP: quick fixes + mortgage calculator + investment + English mortgage (Ben 25.10.2026)

Ben, 25.10.2026 (evening): "start with the small fixes and really do them, and the upgrades: the mortgage calculator, the investment
page, an English mortgage page. If a competitor, or all of them together, would be close to me or above me, better not to do it. I
need to give an honesty statement, you must commit. Richness: infographics, tables, prices, tools; every page gets a moat, something
practical that is really needed and tied to the keyword and the intent; many details, data, numbers, arranged in an interesting way,
visualisation; work with Claude Design; a very deep loop; competitor research in everything: how they place the keyword, why they
rank, what people search, what Google wants to show, and give it a thousand times more. Absorb everyone's DNA, sophisticated tools
with UX and design, every page a masterpiece. The cities later (HAD-602), not enough usage now."

## Gates for every page (none skipped)
1. Intents + keyword set from Search Console (docs/research/2026-10-25-projects-hub/upgrade-targets-gsc.json), ownership check
   (tools/gsc/url_word_audit.py + GSC overlaps): one owner page per intent, no new rival URL, no redirect, no noindex.
2. Google by hand (Ben's Chrome) or DataForSEO SERP: top results, People also ask, AI overview (or "absent"), retrieval time.
3. Top 4-5 competitors read in full: keyword placement (title, H1, first paragraph, headings), depth, tools, data, freshness,
   schema, why they rank. Raw HTML kept in _private-research.
4. Build spec: title / H1 / answer paragraph (language DNA), sections, tables with real data, infographics, the moat, FAQ from PAA.
5. Claude Design first: the NadLan Instruments identity (tools/guides/nlag.py: chart paper, ink, sea, survey red; Karantina,
   IBM Plex Sans Hebrew, IBM Plex Mono). Not the default AI look.
6. Build + preview + release by the hunk rules; live checks; raw-source audit.
7. Honesty statement: tools/depth_proof.py + tools/fact_coverage.py vs the same competitors. We ship only when we are above each
   competitor AND their union on words, figures, tables, tools, FAQ, sources, facts; any metric where a competitor leads is named.
8. Link to Ben, Linear + Notion.

## Board
| # | Page | Main queries (90 days, impressions @ position) | State |
|---|---|---|---|
| Q1 | /urban-renewal/map/ | מפת התחדשות עירונית 362@13 · מתחמי פינוי בינוי 164@19 · מתחם התחדשות עירונית 122@27 | **1.72.520 releasing**: data layer inc/urban-map-data.php + data/renewal-stats.json (tools/urban/build_renewal_stats.py: data.gov.il 970 complexes/76 cities 15.8.2026 + authority map counts 999/79 20.10.2026): tiles, stage table+funnel, tracks, approved by district, execution, 7 district tables, top-15, declarations per year, stage dictionary, approval-to-permit, where to check, 20 visible FAQ = FAQPage, sources; promise copy removed; live base used (repo copy not live: memory nadlan-repo-not-live-files). Next: page H1/title/answer via REST, proof, then stage B (complex tracker with history = moat) |
| Q2 | /property-value-estimator/ | הערכת שווי דירה 461@21 · הערכת שווי נכס 450@20 · כמה שווה הדירה שלי 172@24 · בדיקת שווי נכס 167@20 | research DONE. **Stage 1 LIVE 25.10**: title 'הערכת שווי דירה בחינם: מחשבון שווי נכס לפי עסקאות אמת', H1, answer, breadcrumb, seller section (247 impr), FAQ 5 -> 22 (schema 22). Proof after stage 1: words 3,316 vs 1,997, figures 97 vs 39, FAQ 22 vs 5, headings 46 vs 24; BEHIND on visuals 1 vs 19 (wecheck). Stage 2: tables T1-T5, 5-year sparkline per city (data.nadlan.gov.il), CBS district index chart, the three-anchors moat in pval; honesty statement only after stage 2 |
| Q3 | /glossary/מחירון-דקל-לבנייה-ותשתיות/ | מחירון דקל 251@18 · מחירון דקל 2026 67@16 · מחירון דקל בניה 61@12 | research DONE: live errors (yearly update, invented 500 ₪ concrete). Rewrite ready (write_q3.py, 1,430 words, 3 tables, 15 FAQ), goes live after 520; tool (chooser + quote check) in a later release |
| Q4 | /glossary/דקל-תוכנה/ | דקל תוכנה 206@9 | research DONE (company name = דקל תוכנה (ד.ב.י) בע"מ; 'דקל בענן' ~5,400/month missing). Rewrite next |
| Q5 | /glossary/תי-466/ | ת"י 466 147@9 · תקן ישראלי 466 86@12 · תקן 466 חלק 2 77@21 | research DONE: live errors (413/118 'international', production = 118, wrong arithmetic). Rewrite ready (write_q5.py, 1,653 words, 4 tables incl. the 466-and-my-apartment table, 15 FAQ), goes live after 520 |
| Q6 | /glossary/לוח-גבס-אדום/ | גבס אדום 133@9 · לוח גבס כתום 80@28 · לוח גבס אדום 70@12 | **LIVE 25.10** rewrite (write_q6.py): ת"י 1142 error fixed (Google AI was quoting it), pink synonym, 5 tables, 16 FAQ, 1,777 words; FAQPage now = real questions (520 term-faq-schema); title needs the 520 REST meta (rerun meta after 520); wall calculator later |
| Q7 | Sde Dov: /sde-dov/ vs /sde-dov/prices/ | דירות למכירה בשדה דב: 181@34 on /sde-dov/ and 96@17 on /sde-dov/prices/ (two of our pages on one query) | finding; owner decision after research |
| Q8 | /projects/rainbow-tel-aviv/ | ריינבו קנדה ישראל 100@14 · rainbow תל אביב 96@13 · פרויקט ריינבו 94@15 | later (fleet page laws) |
| U1 | /mortgage-calculator/ | מחשבון משכנתא 573@45 · מחשבון משכנתא הפוכה 434@54 · חישוב משכנתא 338@44 · כמה משכנתא אפשר לקחת 310@64 (8,215 impressions) | research DONE; quick fixes LIVE (19 dead links, BoI defaults, banned words, interest-rates meta). **Builder agent running** (local only): data/boi-mortgage.json + tools/mortgage.js (Mortgage 2.0 + the 'your offer vs the Bank of Israel' moat) + math cross-check + preview. Then: page sections T1-T9, V1-V4, 30 FAQ, design board, release, proof |
| U2 | /investment/ | נדלן להשקעה 345@36 · השקעות נדלן 333@75 · מימון נדלן 273@83 · דירות להשקעה 231@55 (7,026) | research DONE (u2-investment/dna.md; 65-city yield data built). **Quick fixes LIVE 25.10** (false 'no government yield' claim, 8% tax end date 10.2.2027, ten 'טעון אימות' hedges, banned brand, stale footer, schema author name). **Builder agent running** (local only): data/invest.json + tools/invest.js (yield and cash-flow map, 'כמה מהדירה שכר הדירה קונה') + cross-check + preview |
| U3 | English mortgage | israel mortgage for foreigners 179@63 · hipoteca en israel para extranjeros 83@77 | research DONE (u3-en-mortgage/dna.md). **Finding: /israel-mortgage-non-residents/ (post 4962) is ENGLISH content tagged he-IL**; an /en/ copy would make two English pages. Recommendation: /en/ page + rewrite the root in real Hebrew (40+30+30/mo Hebrew demand), hreflang pair, x-default = English. **Ben's decision**. Meanwhile LIVE 25.10: its stale rates fixed (3.25% / 4.75% / 1.6% / 23.11.2026 / August averages, 'resident' -> 'citizen'). Same language issue on /israel-purchase-tax-foreign-residents/, /buy-property-israel-foreign-buyers/, /buying-real-estate-israel-foreign-investor/ (recorded only) |
| C | Cities (HAD-602) | later, Ben's word | parked |

## Findings for Ben (no action without his word)
- U3: English content at the Hebrew root (4 pages) and the /en/ plan above.
- U2: /buy-or-rent/ and /buy-vs-rent/ are two live calculators for one intent; /investment-apartment/ and /investment/apartments-for-investment/ overlap the hub (suggest re-targeting each, no merge or removal); 'מס על שכר דירה' (260/mo) has no owner and /rental-income-tax/ answers 404; 'מימון נדלן' is developer finance (no owner).
- Foreign Latin-language demand (Italian 345, Portuguese 257, Spanish 178 impressions in 90 days on /investment/).
