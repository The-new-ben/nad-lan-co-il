# RADIUS LOOP: the strongest project pages in north Tel Aviv and Herzliya (Ben, 1.11.2026)

## Ben's order
- **Where:** start with the radius: Sde Dov, Einstein (Ramat Aviv), Kochav HaTzafon, Shikun Lamed, then Herzliya.
- **Which projects:** every project now in marketing or construction, including the small streets (יהודה עמיחי, אייזק שטרן).
- **What each page gets:**
  - the right writing DNA;
  - all languages, written through ChatGPT, Gemini and Antigravity;
  - information, infographics, visualisation;
  - tools: calculators and the price list around the project.
- **The bar:** prove nobody beats us.
- **Kikar Hamedina is included.**
- **Later waves:** Petah Tikva, Kiryat Ono and the growing areas.

## The recipe (what makes Rainbow the page ChatGPT cites; evidence in `docs/research/2026-11-01-ai-referrals/`)
1. **The answer paragraph first:** location, developer, units, floors, stage, and price per sqm with its source and date.
2. **A line "עודכן ב<month year> · מקורות: …"** with the real sources.
3. **A facts table:**
   - developer, contractor, architect;
   - address, block and parcel;
   - units, floors, buildings;
   - stage, delivery;
   - price per sqm, each with its source.
4. **FAQ in schema:** 8-12 questions, written the way people ask ChatGPT.
5. **ApartmentComplex schema** with geo, sameAs to the developer's sites, and an AggregateOffer only with a sourced price.
6. **The price list around the project:** reported deals within about 500 m (data.nadlan.gov.il, allowed since 31.10), per sqm, by year and by rooms.
7. **The radius comparison:** the projects in the area side by side (stage, units, floors, price per sqm, distance to the sea).
8. **The project's tools:** the ProjectKit (total cost, mortgage, index linkage, affordability) prefilled with its numbers, plus what fits this particular project (sea distance, delivery-delay compensation, an Sde Dov soil check).
9. **Languages:** EN, FR, RU, AR through ChatGPT with the language DNA files (`docs/research/2026-10-25-projects-hub/lang-dna-*.md`).
10. **Honesty:** no number without a source. Unknown = omitted.

## Rules
- These laws still hold:
  - the additive law;
  - Ashira untouched;
  - the Einstein Tower Hebrew article is pinned, so additions go below it only;
  - the stage and the beam are frozen.
- Claude Design comes first for every new component (DS artifact L9Nqz7Viv7K3MYeZrBc9s8).
- **New pages:**
  - Run `url_word_audit.py` and `kw_guard.py` first.
  - Apply the research law: read the top 4-5 Google results in full, record the questions and the AI answer shown, then write.
  - Never a 301, never noindex, never "request indexing".
- **Pace:** waves of a few pages a day, with no sitewide mass change.
- **Releases:** the release chain and lock line as in `HAD-642-LOOP.md`. The runner runs in the background.
- **Report:** every report opens with the campaign line and sends Ben the links.

## Queue
- [x] **R0 Inventory** (1.11, 17:40). Output: `docs/research/2026-11-01-radius/projects.json` + `projects.md`.
  - **Counts:** 218 projects, 20 of them ours, 198 gaps. 75 of the gaps are for sale now; 35 rows carry a dated price with its source.
  - **Per zone:** Sde Dov 30, Kochav HaTzafon and Reading 6, Lamed and New Lamed 20, Einstein area 111, Herzliya 45.
  - **Top gaps:**
    - SEVEN SEAS (Electra and Dan, 437 units, about 80,000 per m²);
    - EINSTEIN 2.4.6.8 (Gindi and Shbiro, 380);
    - Einstein 15 (Gindi and Shbiro, 180, 30 floors);
    - Philharmonit, Agnon 28;
    - Sde Dov plot 105 (372 units and a hotel);
    - Brodetsky North (ICR, 166);
    - Yehuda Amichai 5 / Isaac Stern 18 (Eshkol Megurim, 62) and Isaac Stern 22 (23);
    - Reading 22 RAMATA and Reading 31-33;
    - Herzliya VILLE (Azorim, 1,843);
    - Herzliya Pituach seafront and the Ritz-Carlton Marina.
  - **Facts the sources contradict** (fix in R3-R5, each with its source):
    - Dimri Yama: 40 vs 38-39 floors;
    - Ashira: 8 vs 9 floors (do not touch Ashira, report only);
    - Einstein Tower: units, floors, corner;
    - Utopia: now under construction, since 10.2025;
    - Shikun & Binui: a second 511-unit rental building exists;
    - Vogue: floors;
    - Recanati: neighbourhood.
  - **Two EcoCity rows are marked do-not-publish** (the takedown order).
- [x] **R1 Design** (1.11, 16:45). Claude Design v105.5, DS artifact versions 256-257. Renders at 390 px are in `docs/research/2026-11-01-ai-referrals/design-105-5/`.
  - **RadiusPrices:**
    - deals within 500 m (median per m², by rooms, by year, the latest deals);
    - the official neighbourhood median with its quarter;
    - the projects around (the compare part lives here).
    - Preview: Einstein 19 with real numbers (62 deals, about 53,500 per m², 10.2023-9.2024; Ramat Aviv official median 4,931,600, Q1 2026).
  - **ProjectFacts:**
    - the "עודכן ב… · מקורות" line;
    - a sourced dl of facts;
    - buyers' questions;
    - one ApartmentComplex schema from the same rows (ends the 459/480 split).
    - Preview: Rainbow.
  - **Review fixes:** a cool sea tint instead of sand (Ben's 13.10 law); years run left to right; a unit sits outside the number span.
  - **Data findings:**
    - `tools/deals/build_radius_prices.py` places 70,866 Tel Aviv deals by block and parcel; output `tools/deals/radius-prices-v1.json`.
    - The per-deal file is old: in practice it ends at 8-9.2024, with a few 2025 rows. The period is always printed.
    - The official neighbourhood files run to Q1 2026 (`data.nadlan.gov.il/api/pages/neighborhood/buy/<id>.json`, file 20.8.2026; 16 radius neighbourhoods saved in `docs/research/2026-11-01-ai-referrals/gov-neighbourhoods/`).
    - "אזור שדה דב" has no official median yet, so the Sde Dov pages use the nearest named neighbourhoods (Kochav HaTzafon, Tochnit Lamed, Nofei Yam).
    - Herzliya is not in the Tel Aviv file. It needs the big-cities workbook or the official files (R6).
    - Fresher per-deal rows sit behind reCAPTCHA on api.nadlan.gov.il: never bypassed.
- [x] **R2a RadiusPrices live on the 3 pilot pages** (1.11, 17:15).
  - **Release 1.72.552:** new `inc/radius-prices.php` and `data/radius-prices.json`, module list + 'radius-prices'. Released and verified (deploy-result-552.json).
  - **Placement:** `rp_cms.py` put `[nadlan_radius_prices]` on Zohi 4747 and Einstein 19 4874 (before the kit) and on Hamedina 8113 (at the end). Backup: `rp-backup.json`.
  - **Rainbow fix:** num_units 480 → 459, the developer's figure that the page already quotes.
  - **Checked live at 390 px** (Chrome, `docs/qa/radius-552/*-390.png`): one H1, no sideways scroll, the block before the kit, 3 tiles, 5-6 projects around.
  - **Live numbers:**
    - Einstein 19: about 53,500 per m² (62 deals); Neve Avivim official 5,299,900 (Q1 2026).
    - Zohi: about 47,600 (18 deals); the neighbouring Tochnit Lamed 6,059,900.
    - Hamedina: about 68,200 (135 deals); 5,373,900.
- [x] **R2b** (1.11, 18:30). Release 1.72.553 ProjectFacts, plus "בצפון החדש" in the radius block.
  - **The first run rolled back.** A 552 check forbade nlrp on Einstein 19; the check was fixed and the rerun was released and verified.
  - **Placement:** `pfx_cms.py` opened Zohi and Einstein 19 with `[nadlan_project_facts]`.
    - Zohi: 11 sourced rows (Nadlan Center 30.1.2026, Calcalist 24.2.2026 marked as partner content, the Tel Aviv-Yafo plot 110 PDF).
    - Einstein 19: 8 rows (Nadlan Center 26.9.2023).
    - Every source is a link.
  - **Order at 390 px:** H1 154, lead 226, facts 2451, radius block 29861.
  - **Checks:** `content_first_check.py` failed 0. The Zohi radius box now shows Rainbow with 459 units. Stage pages (Hamedina) keep their own `.nlpf` and get no ProjectFacts.
  - **Design** v105.6 in DS artifact version 258.
- [ ] **R2c WAITS FOR Ben's look at the pilot.** Zohi, Einstein 19 and Hamedina. His word gates the clone waves R3-R6 (RadiusPrices + ProjectFacts on every radius page).
- [x] **R3a Fix the facts the sources contradict** (1.11, 19:00; meta only, `r3a_cms.py`, backup `r3a-backup.json`).
  - **Utopia** 4749: project_status permits → construction. Source: Nadlan Center 27.10.2025, "קבוצת נחמיאס החלה בעבודות הבניה", article 13109.
  - **Dimri Yama** 4745: num_floors 39 → 38. Source: the developer's page "8/38 קומות", 4 buildings, 458 units, read 1.11.2026.
    - The stage facts panel still says "מגדל של 40 קומות ... לפי תכנית". That is the approved plan, not the developer's design, so it is left as is: two figures, each with its own source.
  - **The neighbour boxes refresh** when their 12-hour cache ends.
  - **Left, with the reason:**
    - Einstein Tower: the sources disagree with each other (215/300/515 units, 28/30/33 floors), and the page is pinned. Report only.
    - Vogue: 8 vs 9 floors on the low building; minor, the source range is 9-44.
    - Recanati: the neighbourhood name. The radius block already uses the municipal polygon (Ramat Aviv Gimel).
    - Shikun & Binui: a second 511-unit rental building. It needs a content addition after Ben's look.
    - Ashira: report only.
- [x] **R7a Research for the gap pages** (1.11, 20:10). Output: `docs/research/2026-11-01-radius/briefs/`, 11 briefs plus `index.md` and `serp-log.md`. DataForSEO: 30 calls, $0.096.
  - **What Google shows:**
    - no People-Also-Ask in any of the 26 searches;
    - an AI Overview on 24 of 26, and it never cites us;
    - Philharmonit and Aviv BaReading show no AI answer on the name, so they are the easiest wins.
  - **Slugs that pass `url_word_audit`:** seven-seas, shbiro-2468, levi-55, philharmonit, landowners-105, brodetsky-33-39, amichai-stern, ramata, reading-31-33, ville, ritz-carlton.
    - "einstein" is already owned by 4 URLs, so no new "einstein-…" slug.
    - Each new street word (brodetsky, reading, amichai, stern) becomes that street's owner page.
  - **Corrections:**
    - Gindi's partner is **Shbiro** (Rami Shbiro), not "Shapir".
    - The Ritz-Carlton is resale of vacation flats in a hotel, not a new build.
- [x] **R2 Pilot on 3 pages (original item; superseded by R2a, R2b and R2c above):**
  - zohi-sde-dov: AI visits arrive, but the price data is thin;
  - einstein-19: the Einstein cluster has no AI visits;
  - hamedina: 8 AI visits, no date line, no tools.
  - Then Ben's look.
- [ ] **R3 Sde Dov wave:** dimri-yama, gindi-vogue, utopia, first, rainbow. Fix Rainbow's 459/480. Rainbow gets additions below only.
- [ ] **R4 Einstein wave:** ashdar-einstein, recanati-residence, einstein-tower (below the pinned article).
- [ ] **R5 Kochav and Park Tzameret:** akirov, yoo, park-bavli, duo, h-infinity.
- [ ] **R6 Herzliya:** marina-towers, plus the gaps there.
- [ ] **R7 Gap pages:** a new page for each real project we lack, small streets included, written through ChatGPT with the DNA.
- [ ] **R8 Languages:** the 8 radius pages without EN/FR/RU/AR, then the new pages.
- [ ] **R9 Measure:** GA4 AI landing pages every week (Rainbow baseline: 19 in 5 months). Record the ChatGPT answer for "<project> מחירים" before and after.
- [ ] **WAITS FOR BEN:**
  - IndexNow for Bing (ChatGPT search reads Bing; our Bing traffic is 49);
  - marking the WhatsApp click as a key event in GA4 (today 0).
