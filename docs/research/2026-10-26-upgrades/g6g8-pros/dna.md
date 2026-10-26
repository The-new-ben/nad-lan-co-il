# G6 G7 G8: the professionals cluster (upgrade loop, Ben 26.10.2026)

Local round only. Nothing was deployed, posted, committed or requested for indexing. All research raw files are private in
`C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\` (serp\g6g8\, raw\g6g8\, raw\g6g8\official\).

| Gap | Owner page (kept, no new URL) | WP id | Head term | Volume / KD / CPC | GSC 90 days |
|---|---|---|---|---|---|
| G6 | https://nad-lan.co.il/home-inspection/ | 90 | בדק בית | 2,900 / 2 / $16.57 | 189 impressions, 0 clicks, head term absent |
| G7 | https://nad-lan.co.il/real-estate-appraiser/ | 86 | שמאי מקרקעין | 2,400 / 12 / $9.95 | 8 impressions, 0 clicks, head term absent |
| G8 | https://nad-lan.co.il/real-estate-lawyer/ | 11 | עורך דין מקרקעין | 1,600 / 24 / $12.98 | 549 impressions, 0 clicks, head term absent |

Zero clicks on all three means a title change risks nothing that exists today.

## 1. Intents and demand (DataForSEO Google Ads, Israel 2376, read 26.10.2026)

**G6 owns:** בדק בית 2,900 · בדק בית מחיר 390 · חברת בדק בית 210 · כמה עולה בדק בית 140 · דוח בדק בית 140 · בדק בית לפני קניה 110 ·
מהנדס בדק בית 90 · בדיקת דירה לפני קניה 90 · מחיר בדק בית 70 · בדק בית לדירה יד שניה 70 · תקופת בדק 70 · שנת בדק 50 · בדק בית לפני מסירה 50 ·
בדק בית לדירה חדשה 40 · אחריות קבלן 40 · בדק בית מקבלן 30 · אחריות קבלן על רטיבות 30. City variants (ראשון לציון 320, חיפה 110...) are local-pack
intent; the page does not chase them.
Neighbours owned elsewhere, linked not absorbed: חוק המכר דירות 3,600 and חוק המכר 1,900 (/real-estate-lawyer/sale-of-apartments-law/),
ליקויי בניה 320 (/real-estate-lawyer/construction-defects-lawsuit/), ת״י 466 (/glossary/תי-466/).

**G7 owns:** שמאי מקרקעין 2,400 · שמאות מקרקעין 2,400 · שמאי 2,400 · שמאי דירה 140 · דוח שמאי 110 · שמאי מקרקעין מחיר 90 · שמאי מקרקעין מומלץ 90 ·
חוק שמאי מקרקעין 50 · כמה עולה שמאי 40 · כמה עולה שמאי דירה 30 · פנקס שמאי מקרקעין 30 · חוות דעת שמאית 30 · שמאי משכנתא 20 · שמאי היטל השבחה 20 ·
תביעה לפי סעיף 197 10 · שמאי מייעץ 10.
Neighbours: שמאי מכריע 1,900 (/glossary/שמאי-מכריע/), ערר על היטל השבחה (/real-estate-tax-advisor/betterment-levy-appeal/), שמאי פינוי בינוי 50
(/glossary/shamai-pinui-binui/), הערכת שווי נכס 260 (/property-value-estimator/). היטל השבחה 3,600 has NO clear owner (the glossary URL
/glossary/היטל-השבחה/ is 404): a finding, not built here.

**G8 owns:** עורך דין מקרקעין 1,600 · עורך דין נדלן 590 (two spellings) · עורך דין מכירת דירה 390 · עורך דין קניית דירה 320 · עורך דין מקרקעין
מומלץ 210 · עורך דין רכישת דירה 90 · עורך דין לקניית דירה 90 · עורך דין חוזה מקרקעין 40 · כמה עולה עורך דין לקניית דירה 40 · שכר טרחה עורך דין
קניית דירה 30 · שכר טרחה עורך דין מכירת דירה 30 · עורך דין מקרקעין מחיר 20.
Neighbours: מס רכישה 6,600 (/purchase-tax-calculator/), הערת אזהרה 1,600 and נסח טאבו 49,500 (mentioned with facts, no page minted),
לשכת עורכי הדין 33,100 (navigational, not ours).

**English (IL / US):** lawyer israel 90 / 480 · israeli lawyer 90 / 480 · buying property in israel 30 / 50 · real estate lawyer israel 20 / 30 ·
israeli real estate lawyer 10 / 40 · bedek bayit 10 / 10. Everything else 0. Decision: one short English section per page, no English page.

## 2. Ownership and cannibalization

* `tools/seo/kw_guard.py` (Git Bash, `MSYS_NO_PATHCONV=1`) on every new title, H1, meta, tool title and anchor: all OK, one allowed WARN
  (the anchor "שמאי פינוי בינוי" carries the protected term פינוי בינוי, owner /urban-renewal/pinui-binui/; it is a qualified mention that
  links to the glossary). Full output: `kw-guard.txt`.
* No new URL is minted, so url_word_audit is not needed. No redirect anywhere.
* GSC overlap: the appraiser-fee queries ("כמה עולה שמאי דירה" and similar) land today on /property-value-estimator/. Not changed. The only
  suggestion (for Ben) is a link from that page to G7.

## 3. SERP, PAA and AI overview (DataForSEO live SERP, google.co.il Hebrew, 26.10.2026 11:32 to 11:33 UTC)

nad-lan.co.il is not in the top 20 for any of the queries below. Summaries: `serp/g6_summary.txt`, `g7_summary.txt`, `g8_summary.txt`.

| Query | Device | Top results | AI overview | PAA |
|---|---|---|---|---|
| בדק בית | desktop | midrag tip 981, doobie, hadas, hd-eng, local pack, zebedek, bhamim, bedek-mivnim, reporto glossary | present (wikipedia, midrag, hadas) | absent |
| בדק בית | mobile | civileng, agam, aradeng, zebedek, bhamim, 9222222, evenbedek | absent | absent |
| בדק בית מחיר | desktop | gaya, midrag price list, at-terminal, checkhouse, bedek-mivnim, laad, ha-bodkim | present (1,200 to 4,800 incl. VAT) | 8 questions |
| שמאי מקרקעין | desktop | landvalue (the association), j-cohen, teddy, shovi, midrag search, avrahams, mikied, mrea, d.co.il | present | absent |
| שמאי מקרקעין | mobile | same order | absent | absent |
| כמה עולה שמאי | desktop | w-b, tarya, afikil, d.co.il price list, calliber, re-ap, shovi | present (price ladder) | absent |
| עורך דין מקרקעין | desktop | lawfind, midrag, d.co.il x3, carish, cohenlawyers, ire-law, yonilevy | present | absent |
| עורך דין מקרקעין | mobile | same | present | 9 (mostly off-topic: insurance) |
| עורך דין קניית דירה | desktop | addalaw, lawreviews, doron-aharoni fees, otmazgin, ericyanai, amitvered, orilaw | present (0.5% + VAT; developer cap) | 8 questions |
| real estate lawyer israel | desktop | gornitzky, strn, aharoni, givati, directories | present | 3 questions |

**What Google wants (condensed from `competitors-dna-g6/7/8.md`):**
* G6: a commercial SERP of inspection companies; Midrag's sample prices win #1. Nobody ties a defect to the law's period, nobody dates
  prices or states VAT consistently, nobody shows the calendar from the handover day. Opening: the legal clock plus dated prices plus a
  "what is checked" table.
* G7: entities, not guides (the association #1, Tel Aviv offices). The AI overview carries the informational layer and the price ladder;
  the organic price pages are thin or old. Nobody covers the bank-appraisal rules, the levy and 45-day clock, section 197 or a register
  check. Opening: licence-first explainer plus dated price table plus the procedural gaps plus a live register search.
* G8: find-a-lawyer directories for the head term; long law-firm guides for "עורך דין קניית דירה". The AI overview already quotes the
  developer's-lawyer cap. Nobody puts the published fees next to the Bar's recommended tariff, the legal cap by price and the 2026 registry
  fees. Opening: a dated fee/cap/fees calculator, the steps with dates, and a neutral "how to choose and check" layer (no "our lawyer").

Competitors read in full (raw HTML in `raw\g6g8\`): G6 17 URLs, G7 17, G8 14 (lists in `competitors-g6/7/8.txt`).

## 4. Verified facts (official texts, dated; every number in the data files is checked by `tools/instruments/build_pros_data.py`, 125 checks)

| Fact | Source (read 26.10.2026) |
|---|---|
| Inspection periods by defect: 2 / 2 / 3 / 3 / 3 / 4 / 4 / 5 / 7 / 1 years; warranty 3 years after; structural 20 years; visible defect notice within 1 year; repair rule s.4ב; קונה משנה; spec, standard and regulations as non-conformity s.4(א)(1); maintenance instructions s.4(א)(6) | חוק המכר (דירות), התשל"ג-1973, ss.1, 4, 4א, 4ב and the schedule |
| Developer's lawyer: lower of 5,000 indexed (5,915 in 2026) and 0.5%, before VAT; not above 4,642,750; list fee 300; 2024 5,575.06; 2025 5,770.77 | Sale Law s.6ג; תקנות המכר (הגבלת גובה ההוצאות המשפטיות), התשע"ה-2014 and the 2026 notice; kolzchut 3.2.2026 |
| Bar recommended minimum tariff 2026 (non-binding): contract 2% to 95,004 (min 790), 1.5% to 377,607, 1.25% to 761,062, 1% to 2,283,281, 0.75% to 3,806,082, above by agreement (min 37,761); registration 1% to 633,967 then 0.75%; warning note 748 / 1,068; mortgage 0.5% (min 1,012) | כללי לשכת עורכי הדין (התעריף המינימלי המומלץ), 2026 amounts |
| One lawyer for both sides: limits | כללי האתיקה המקצועית, rule 14(ב), (ד) |
| Complaints on a lawyer: district ethics committees | חוק לשכת עורכי הדין ss.18ב, 63 |
| Land Registry fees 2026: sale 44, warning note 188, deletion 127, mortgage 188, electronic extract 18, certified copy 88, inheritance 188 | תקנות המקרקעין (אגרות), התשל"ה-1974, schedule |
| Declaration 30 days, purchase tax 60 days, 0.2% a week late; CGT advance 7.5% / 15% after more than 40% paid, reduction on request | חוק מיסוי מקרקעין s.15 (advance), s.73 (declaration) and the payment and late-payment sections (via ptax.json, Tax Authority buyer guide 2026) |
| Appraiser = registered; degree, exams, internship 1 year at 40 h or 2 years at 20 h, final exam; court filings; fee work only by registered, impersonation 1 year; conflict of interest; complaints, discipline committee, 30-day appeal | חוק שמאי מקרקעין, התשס"א-2001, ss.1, 7, 12, 13, 14, 17, 22, 23 |
| Exam pass mark 60 | תקנות שמאי מקרקעין (בחינות), התשס"ו-2006, reg. 7(ב) |
| Register 3,182 appraisers (376 with a city), updated 25.10.2026; exams file 93,728 rows (1.10.2026); final exam 2025: 674 sat, 322 passed (48%) | data.gov.il, dataset shamaim (Ministry of Justice), API read; licence "לא צויין", so searched live, not copied |
| Decisive appraiser fee: 3% / 2% / 1% / 0.5% brackets, min 2,000, max 100,000, half each side, a quarter upfront, plus VAT | תקנות התכנון והבניה (שכרו של שמאי מכריע ושמאי מייעץ), התשס"ט-2009 |
| Levy: half the betterment; 45 days to appeal or ask for a decisive appraiser; the chair names one in 15 days; up to 90,000 re-examination decided in 14 days; s.197 claim within 3 years | חוק התכנון והבניה, s.196א, Third Schedule ss.3, 14; s.197 |
| Bank appraisal: the bank's list and tariff, a copy for the payer, 90 days at another bank, no private appraisal, a second one on a significant gap | kolzchut (2.3.2025) citing Bank of Israel housing-loan rules ss.9-10 |
| Published prices (never offers): inspection, appraisal and lawyer fees with page date and VAT status | midrag, bedek-mivnim, ha-bodkim, ec-shamaut, d.co.il, doron-aharoni, addalaw, gelberg, bizportal (dates in `page-sources-g6/7/8.md`) |

## 5. Our pages today and their gaps (live REST read 26.10.2026; backups in `page-backup/`)

| Page | Live today | Gaps |
|---|---|---|
| G6 | 1,821 words, 1 table, 5 FAQ, 0 tools; H1 "בדק בית לפני קניית דירה: מה בודקים ואיך משתמשים בדוח" narrows the page to second-hand buyers (misses new apartments and the price intent); one unsourced price line ("1,200 עד 2,600") | no law clock, no dated prices, no calendar, no "what is checked" table, no English |
| G7 | 2,267 words, 1 table; FAQ under an h3 (no FAQPage); old gold/cream look; off-topic price blocks (Kfar Shmaryahu, Savyon, Rishpon, Herzliya Pituach) | no register check, no bank rules, no levy clock, no decisive fee, no exams data |
| G8 | 2,086 words, 1 table, 4 FAQ; three H2 "מדריך חדש" placeholders; hero image 404 (upload.wikimedia Tel_Aviv_skyline 960px); "כתוב ונבדק על-ידי עורך דין מקרקעין" (no such reviewer on record); same off-topic price blocks | no fee vs tariff vs cap, no registry fees, no steps with dates, the "who pays" FAQ misses the cap |

Professionals directory: /professionals/ holds only DEMO profiles with invented credentials (demo-david-peretz-appraiser,
demo-ronit-almog-lawyer, demo-uri-nahum-inspection, demo-avi-cohen-engineer) plus two empty profiles with the surname "שמאי". None is
linked from the new content. No person, rating or count is invented anywhere.

## 6. Build spec (rendered order: H1 → answer → CTAs → tool → facts → article)

All three: answer paragraph opens with the head term; three CTAs (the tool, the key table, WhatsApp) with `color:#fff!important`;
the tool right after; T1 facts table; new sections at exact anchors before named old headings; FAQ from PAA plus competitor questions
under an h2 "שאלות נפוצות…" so `nadlan_nli_faq()` builds FAQPage; English section; method line with the date. Look: ink #12202A, sea
#2F6F86, deep #1F4B5C, line #D3DCE2, red #C42550 only for a limit; IBM Plex Sans Hebrew + Mono. Old gold/cream is reformed only with `--style`.

**G6 /home-inspection/** · WP title = H1 "בדק בית: מה בודקים, כמה זה עולה ועד מתי הקבלן אחראי" · Yoast "בדק בית: מחירים 2026, מה בודקים ועד מתי
הקבלן אחראי" · tool `bedek` (defect against the law, inspection calendar, every published price; presets leak, cal, apt4, house, sub) ·
tables T1 to T7 (9 in the render) · drawings I1 periods, I2 prices, I3 calendar · FAQ 5 + 20 = 25 · honesty fix of the unsourced price line.

**G7 /real-estate-appraiser/** · H1 "שמאי מקרקעין: מתי צריך, כמה זה עולה ואיך בודקים שהוא מורשה" · Yoast "שמאי מקרקעין: מחירים 2026, סוגי שומה ובדיקת
רישיון" · tools `shamai` (8 purposes: who orders, who pays, the deadline from the reader's date, prices, decisive fee) and `shamaireg` (live
search in the official register) · tables T1 to T7 · drawings I1 purposes, I2 exams, I3 decisive fee · FAQ heading h3 → h2, 4 + 20 = 24.

**G8 /real-estate-lawyer/** · H1 "עורך דין מקרקעין: מה הוא בודק לפני החתימה, כמה זה עולה ואיך בוחרים" · Yoast "עורך דין מקרקעין: שכר טרחה 2026
ובדיקות לפני חתימה" · tool `orechdin` (published fees vs Bar tariff vs legal cap, registry fees, steps and tax dates; presets buy2, new, lux,
sell, steps) · legal line in the hero "המידע כללי ואינו ייעוץ משפטי. האתר אינו מייצג קונים, מוכרים או יזמים." · tables T1 to T8 · drawings I1 cap,
I2 fees, I3 steps · FAQ 4 + 24 = 28 · honesty fixes: the cap sentence in "who pays", the unbacked "reviewed by a lawyer" line removed.

## 7. Proof (depth_proof.py and fact_coverage.py, raw HTML, 26.10.2026 14:58 to 15:05)

| | Words | Tables | Cells | Tools | FAQ | Headings | Drawings | Facts (of 32) |
|---|---|---|---|---|---|---|---|---|
| G6 live | 1,821 | 1 | 24 | 0 | 5 | 18 | 0 | 12 |
| G6 local render | 5,584 | 9 | 373 | 1 | 25 | 52 | 3 | **32** (best competitor 15, Wikipedia) |
| G7 live | 2,267 | 1 | 18 | 0 | 11 | 26 | 1 | 7 |
| G7 local render | 5,209 | 8 | 303 | 2 | 31 | 57 | 4 | **32** (best 14, midrag price 8151) |
| G8 live | 2,086 | 1 | 18 | 0 | 4 | 23 | 1 | 10 |
| G8 local render | 5,190 | 10 | 253 | 1 | 28 | 60 | 4 | **32** (best 21, amitvered) |

**Predicted honest statements (to publish with the release report, after the live re-measure):**
* G6: "More facts than any page in the top 10 (32 of 32 against 15 at best), the only page with the law's clock per defect and dated
  prices with VAT status. Competitors carry more pictures (Midrag 71 images); ours are 3 drawings. We do not inspect and name no inspector."
* G7: "32 of 32 facts against 14 at best, the only page with a live search of the official register and the levy and 197 deadlines.
  afikil has more headings (63 against 57) and every office page has more images."
* G8: "32 of 32 facts against 21 at best; the only page with fees, the Bar tariff and the legal cap side by side. amitvered (17,749 words)
  and gelberg (7,453) are longer, lawreviews has two lead forms, directories show many more images. Not legal advice; we represent no side."

Image counts on competitor pages are mostly logos, icons and photos of staff; our count is real data drawings.

## 8. Needs Ben, findings, not verified

**Needs Ben:** the release (tools + data + registry + summaries, then the three writers); `--style` (reforming the old gold/cream look on
G7 and G8); removing the off-topic price blocks on G7 and G8; what to do with the DEMO profiles in /professionals/; an owner for היטל השבחה
(3,600/mo); a link from /property-value-estimator/ to G7.

**Findings (reported only):** G8 hero image 404; three "מדריך חדש" placeholder H2s on G8; demo profiles live since 2.7.2026; glossary
/glossary/היטל-השבחה/ 404.

**Not verified:** the Bar's lawyer search (israelbar.org.il 302 to israelbar.biz; deep links 404 or geo-blocked), so it is named without a
link; competitor prices are as published, not checked with the offices; the data.gov.il licence is "לא צויין", so the register is not copied;
the live render after release (only local previews at 390 and 1280 so far).
