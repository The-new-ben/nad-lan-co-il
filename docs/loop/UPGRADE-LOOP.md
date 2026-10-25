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
| Q1 | /urban-renewal/map/ | מפת התחדשות עירונית 362@13 · מתחמי פינוי בינוי 164@19 · מתחם התחדשות עירונית 122@27 | research (agent A; builds on docs/research/urban-renewal-2026-10/) |
| Q2 | /property-value-estimator/ | הערכת שווי דירה 461@21 · הערכת שווי נכס 450@20 · כמה שווה הדירה שלי 172@24 · בדיקת שווי נכס 167@20 | research (agent A) |
| Q3 | /glossary/מחירון-דקל-לבנייה-ותשתיות/ | מחירון דקל 251@18 · מחירון דקל 2026 67@16 · מחירון דקל בניה 61@12 | research (agent B) |
| Q4 | /glossary/דקל-תוכנה/ | דקל תוכנה 206@9 | research (agent B) |
| Q5 | /glossary/תי-466/ | ת"י 466 147@9 · תקן ישראלי 466 86@12 · תקן 466 חלק 2 77@21 | research (agent B) |
| Q6 | /glossary/לוח-גבס-אדום/ | גבס אדום 133@9 · לוח גבס כתום 80@28 · לוח גבס אדום 70@12 | research (agent B) |
| Q7 | Sde Dov: /sde-dov/ vs /sde-dov/prices/ | דירות למכירה בשדה דב: 181@34 on /sde-dov/ and 96@17 on /sde-dov/prices/ (two of our pages on one query) | finding; owner decision after research |
| Q8 | /projects/rainbow-tel-aviv/ | ריינבו קנדה ישראל 100@14 · rainbow תל אביב 96@13 · פרויקט ריינבו 94@15 | later (fleet page laws) |
| U1 | /mortgage-calculator/ | מחשבון משכנתא 573@45 · מחשבון משכנתא הפוכה 434@54 · חישוב משכנתא 338@44 · כמה משכנתא אפשר לקחת 310@64 · לפי החזר חודשי 298@38 (8,215 impressions) | research DONE (u1-mortgage-calculator/dna.md). Quick fixes LIVE 25.10: 19 dead links in 5 cluster pages fixed, calculator defaults = BoI averages (4.62 / 4.75 / 3.19, dated), banned words out, interest-rates meta updated; calculator pressed: 6,625 ₪ for the default mix = hand calc. Next: data file data/boi-mortgage.json (SDMX + BoI xls), Mortgage 2.0 tool, design, page sections T1-T9 + V1-V4 + 30 FAQ + moat |
| U2 | /investment/ | נדלן להשקעה 345@36 · השקעות נדלן 333@75 · מימון נדלן 273@83 · דירות להשקעה 231@55 (7,026) | next |
| U3 | /en/israel-mortgage-non-residents/ (English version of the Hebrew page) | israel mortgage for foreigners 179@63 on the Hebrew page · hipoteca en israel para extranjeros 83@77 | next |
| C | Cities (HAD-602) | later, Ben's word | parked |
