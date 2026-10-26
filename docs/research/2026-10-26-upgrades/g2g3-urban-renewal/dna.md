# G2 + G3 · /urban-renewal/pinui-binui/ and /urban-renewal/ · page DNA, facts and build spec

Research date 26.10.2026 (SERPs pulled 10:06 to 10:07 UTC). Local only: nothing on the live site changed, no REST write, no runner,
nothing committed, no Linear or Notion item created by this agent. Builds on, does not redo: `docs/research/urban-renewal-2026-10/`
(3.10.2026) and `../q1-renewal-map/dna.md` (facts F1 to F20).

Evidence classes: **SERP** (DataForSEO Google organic live advanced, Israel 2376, Hebrew, depth 20, AI overview loaded, PAA click
depth 2; raw JSON kept), **raw** (page HTML as served, no scripts), **reader** (r.jina.ai text for pages that block scripts or render
in JS), **PDF** (the authority's 2025 report, 144 pages, downloaded 26.10.2026, text extracted and key pages checked as images),
**law** (the open law book on Wikisource, as amended to תשפ"ג; the binding text is in Reshumot), **GSC** (Search Console API,
sc-domain:nad-lan.co.il, 90 days to 24.10.2026), **unverified** (kept off the pages).

Raw evidence (private, not in the repo): `C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\serp\g2_pb_{d,m}.json`,
`g3_ur_{d,m}.json`, `g2g3_summary.txt`, `g2g3_kw_*_out.json`; competitor HTML and text in `...\raw\g2g3\` (`g2-*.html/.txt`,
`g3-*.html/.txt`, `*.reader.md`); official sources in `...\raw\g2g3\official\` (`report2025.pdf`, `report2025.txt`, page images
`p25.png p71.png p72.png p114-116.png`, `law-pb.txt`, `law-tama.txt`, `gov-*.reader.md`).

---

## 1. Intents, demand and the split between the two pages

### 1.1 Demand (DataForSEO Google Ads, Israel, monthly, pulled 26.10.2026)
| Term | Searches | CPC $ | Goes to |
|---|---|---|---|
| פינוי בינוי | 12,100 | 4.67 | **G2 owner** |
| התחדשות עירונית | 8,100 | 5.16 | **G3 owner** |
| תמא 38 | 1,000 | 1.80 | /urban-renewal/tama-38/ (owner, not touched; linked) |
| **חוק פינוי בינוי** | **880** | 1.36 | **G2** (new secondary intent: the law) |
| חלופת שקד | 480 | 0.03 | /urban-renewal/tama-38-alternatives/ (linked from G3) |
| התחדשות עירונית חיפה | 480 | 4.35 | G3 (city section) |
| הרשות להתחדשות עירונית | 390 | 2.27 | G3 (authority section) |
| תקן 21 | 320 | n/a | G2 (who pays) + FAQ on both |
| תמא 38 2 · פינוי בינוי חיפה · פינוי בינוי באר שבע | 260 each | | G2 FAQ (elderly 38/2), G3 cities |
| עורך דין פינוי בינוי | 210 (CPC 24.4) | | G2 FAQ |
| התחדשות עירונית באר שבע / ירושלים / תל אביב / רמת גן | 210 / 170 / 170 / 170 | | G3 city H3s |
| מנהלת התחדשות עירונית · חברות התחדשות עירונית | 140 each | | G3 |
| מה זה פינוי בינוי · כמה זמן לוקח פינוי בינוי · דייר סרבן · הכרזה על מתחם | 110 / 70 / 70 / 70 | | G2 FAQ |
| מה זה התחדשות עירונית · התחדשות בניינית | 70 each | | G3 FAQ |
| שלבי פינוי בינוי · שמאי פינוי בינוי · תהליך פינוי בינוי · מתחמי פינוי בינוי | 50 each | | G2 (stages exist), map page owns מתחמים |
| קבלת 2 דירות · הסכם פינוי בינוי | 40 each | | G2 FAQ |
| **English** (Israel): tama 38 140 · urban renewal 50 · pinui binui 30 · tama 38 israel / pinui binui israel / pinui binui jerusalem 10 each; (US): pinui binui 20 (CPC $46), tama 38 40; "urban renewal" 14,800 in the US is generic, not Israel | | | a short English section on each page, linking to the English owner /urban-renewal/english-guide/ (no new URL) |

### 1.2 The split (one owner per intent, no rival URL, no redirect)
- **G2 /urban-renewal/pinui-binui/ = the program**: what it is by law, the majority building by building, refusal and the elderly, the
  developer's clock (1ד), what is tax free and up to what ceiling, who pays (standard 21, the government calculator), the official
  time numbers, special cases, the law ("חוק פינוי בינוי").
- **G3 /urban-renewal/ = the umbrella**: the three tracks side by side (pinui binui, TAMA 38, fast licensing / Shaked), the tax vs the
  authorities track, TAMA 38 and its replacement plan in each city, building renewal numbers, urban renewal by city, the authority and
  the administrations, the national numbers.
- The map page /urban-renewal/map/ keeps "מפת התחדשות עירונית" and "מתחמי פינוי בינוי"; both pages link to it with that anchor.

### 1.3 Search Console (90 days, query × page)
- /urban-renewal/pinui-binui/: 190 impressions, 0 clicks, average position 72.5; queries: פינוי בינוי אחוז הסכמה 25@84, תהליך פינוי
  בינוי 23@81, יזם פינוי בינוי 21@75, קבלת 2 דירות 20@72, יזמי 16@82, שלבי 13@71, מה מקבלים 12@89, מנהלת דיירים 11@73, שלבים 10@18,
  שלבים בפינוי בינוי 7@5.9. **No impressions for "פינוי בינוי" or "חוק פינוי בינוי".**
- /urban-renewal/: 104 impressions, 0 clicks, position 61.7; התחדשות עירונית פינוי בינוי 24@78, יחס דירות פינוי בינוי 16@51, מה זה נון
  שופ 13@68, יזם פינוי בינוי 11@76, פינוי בינוי אחוז הסכמה 10@69. **No impressions for "התחדשות עירונית".**
- **Overlap (real, small):** "פינוי בינוי אחוז הסכמה" (25 on G2, 10 on G3) and "יזם פינוי בינוי" (21 / 11). Fix by re-targeting:
  G3's new title drops "פינוי בינוי", G2 gets the full majority section and the tool, G3 links to G2 for the calculation.
- Map page (for context): 1,948 impressions, 9 clicks, the only page of the cluster with clicks.

### 1.4 Keyword guard (python tools/seo/kw_guard.py, 26.10.2026, GSC CSV above)
| Page | Kind | Text | Result |
|---|---|---|---|
| G2 | title | פינוי בינוי: החוק, הרוב הנדרש, השלבים ומה מקבלים \| נדלן (55) | OK for "פינוי בינוי" (owner); WARN only for the sitewide brand "נדלן" |
| G2 | h1 | פינוי בינוי: המסלול המלא לפי החוק, מהחתימה ועד המפתח | OK |
| G2 | meta | פינוי בינוי לפי החוק היום: שני שלישים ... ומחשבון לבניין שלכם. (149) | OK |
| G2 | tool name | הבניין שלכם בפינוי בינוי: הרוב לפי החוק, מה מגיע לכם וכמה זמן | OK |
| G3 | title | התחדשות עירונית: המסלולים, המספרים והמתחמים בכל עיר \| נדלן (58) | OK (owner); brand WARN only |
| G3 | h1 | התחדשות עירונית: המסלולים, המספרים בכל עיר ומה בודקים לפני שחותמים | OK |
| G3 | title **today** | התחדשות עירונית: המדריך המלא לבעלי דירות \| תמ״א 38 ופינוי בינוי \| נדלן (71) | WARN ×4: "פינוי בינוי" (G2's), "תמא 38" (tama-38's), "דירות" (/properties/), brand; over 60 chars. Replaced. |
| G3 | meta / tool name | ... פינוי בינוי, תמ"א 38 ... / ... ותמ"א 38 | WARN: qualified mentions after the page's own topic (allowed; GSC shows no competing URL on those words for G3) |
| **Findings (not changed, Ben):** | | | |
| /glossary/pinui-binui/ and /glossary/pinui-binui-term/ | title + h1 | "פינוי בינוי - נדלן" / "פינוי בינוי" (two glossary pages, same term) | **BLOCK** (lead with G2's term). Re-target text tested: "מילון הנדל״ן: פינוי בינוי, ההגדרה בקצרה" → WARN (allowed). Two duplicates: one should be retired or re-targeted on Ben's word. |
| /urban-renewal/pinui-binui-tenant-guide/ | title + h1 | "פינוי בינוי 2026: זכויות הדייר..." / "פינוי בינוי: המדריך המלא לדייר 2026" (old brand "נדל\"ן חכם" in the title) | **BLOCK**. Re-target tested: "זכויות הדייר בפינוי בינוי: ערבויות, שכירות ולוח זמנים" → WARN. |
| /urban-renewal/pinui-binui-tel-aviv/ | title | "פינוי בינוי בתל אביב: ..." | **BLOCK** by the rule (city long tail; Ben's call). |
| ~9 complex project pages | title | official names starting "התחדשות עירונית ..." / "פינוי בינוי ..." | rule says BLOCK; official names, low priority, listed for Ben. |

---

## 2. What Google shows (SERP, 26.10.2026 10:06-10:07 UTC; nad-lan in the top 20: **no**, all four)

### "פינוי בינוי", desktop
1 mako.co.il (N12, sponsored law-firm article) הסכם פינוי בינוי: איך שוכר אחד מעכב פרויקט שלם? · 2 land-registration.lawx.co.il התחדשות עירונית בישראל: המדריך המשפטי המלא · 3 barlev-nadlan.co.il פינוי בינוי | מדריך · 4 hiborim4u.co.il כל מה שצריך לדעת על תהליך פינוי בינוי · 5 hon.co.il מהי התחדשות עירונית · 6 digagroup.co.il מילון מונחים בפינוי בינוי · 7 b7net.co.il (tag) · 8 baithadash.com (tenant management) · 9 pinuibinui.org.il מאמרים · 10 mishpati.co.il · then mitar, facebook, igindi tag, myrishon, ynet tag, laws-nadlan.
- **AI overview: present.** Definition from Wikipedia; principles: 24 units threshold (kolzchut), **"רוב מיוחס של 66% (שני שליש)"** (nadlancenter 3988), compensation (shovalbinui, magdilim), refusers with protection "for 75+" (israelhayom, nadlancenter), tax exemptions (kolzchut), **"7 עד 12 שנים"** (shovalbinui, a developer's claim). Sources: he.wikipedia, kolzchut, nadlancenter/3988, shovalbinui, magdilim, israelhayom.
- People also ask: absent. Related: פינוי בינוי ירושלים · פינוי בינוי תל אביב-יפו. Video pack (YouTube, Instagram reels), knowledge graph, images.
### "פינוי בינוי", mobile
1 hb-adv.co.il (video page) · 2 minhelet.oryehuda.muni.il מילון מונחים · 3 saf.co.il (directory) · 4 hiborim4u · local pack (3 tenant-management firms) · 5 bizportal tag · 6 b-g.org.il תהליך התחדשות עירונית · 7 igindi tag · 8 lawx · 9 instagram · 10 baithadash.
- **People also ask: present (9)**: איך למצוא פינוי בינוי? · מהן הזכויות של קשישים בתמ"א 38/2? · מי מאשר פינוי בינוי? · מהי ההגדרה של קשיש לפי חוק פינוי בינוי? · מהן זכויות הדייר בפרויקט פינוי-בינוי? · מהן הזכויות של קשישים בפרויקט פינוי-בינוי בשנת 2026? · מהן הזכויות של בני 70 ומעלה במסגרת פינוי בינוי? · האם תמ"א 38 היא חוק חדש? · האם ניתן לקבל שתי דירות בפינוי בינוי? (no expanded answers returned). **All 9 are answered in G2's FAQ.**
- People also search: פינוי בינוי ירושלים · תל אביב-יפו · מתחמי פינוי בינוי · אור יהודה · מדיניות תמורות התחדשות עירונית.
### "התחדשות עירונית", desktop
1 zfbuilding.co.il (developer) · 2 engelinvest.co.il (category) · 3 minhelet-j.org.il (Jerusalem administration) · local pack · 4 ura.co.il (tenants' association) · 5 dunietz-elad.co.il (category) · 6 hagag-group.co.il (Tel Aviv) · 7 b-g.org.il (category) · 8 shoob.co.il (law firm) · 9 facebook · 10 engelinvest post; then ml-engineering, enav, adatolaw, rashuiot, alev-law, ynet, shlvm, pinuibinui.org.il.
- **AI overview: present.** Definition (gov.il about_urban_renewal, Wikipedia); tracks: pinui binui (threshold "12-24 units"), TAMA 38, upgrade; consent "2/3 ... or 60% in each building"; independent professionals paid by the developer; the authority. Sources: gov.il about_urban_renewal, he.wikipedia, gov.il authority page.
- PAA absent. Related: מפת התחדשות עירונית ירושלים · מנהלת התחדשות עירונית (ירושלים, תל אביב, אשקלון, רמת גן, חיפה) · מדיניות התחדשות עירונית ירושלים · התחדשות עירונית תל אביב מפה.
### "התחדשות עירונית", mobile
1 engelinvest · 2 ura · local pack · 3 dunietz-elad · 4 hagag · 5 rotshtein-holding · 6 amidor (glossary) · 7 africa-ur · 8 b-g · 9 ynet · 10 enav. AI overview: absent on mobile. PAA absent. People also search: התחדשות עירונית תל אביב מפה · מנהלת ... תל אביב · בדיקת סטטוס פינוי בינוי תל אביב · פרויקטים של פינוי בינוי.

**What Google wants:** for "פינוי בינוי" a plain-language legal and process guide (majority, rights, tax, refusers, elderly, time),
answered by law and news brands; for "התחדשות עירונית" a definition and the tracks, filled mostly by companies' service pages with
thin text, plus the municipal administration and the authority in the AI overview. Neither SERP has a page with official data,
tables or a tool. Both are winnable on content (KD 23 and 28); brand strength is the gap.

---

## 3. Competitor DNA (read in full: raw HTML text, reader text where blocked)

### G2 "פינוי בינוי"
| # | Page | Size and form | Keyword placement | Why it ranks | Weak spots |
|---|---|---|---|---|---|
| 1 | mako.co.il (sponsored, Halpert law firm), 21.7.2026 | ~690 words (reader), no table | title and H1 "הסכם פינוי בינוי" | N12 brand, fresh, exact phrase | one topic (a tenant who will not leave), no data |
| 2 | lawx (Golan law firm), 26.1.2026 | ~1,400 words (reader), one comparison table, 4 FAQ, JS-rendered | "פינוי בינוי" in H2s | length, legal framing, internal links | **wrong majority: "80%"** for pinui binui and TAMA 38/2; no numbers, no sources |
| 3 | barlev-nadlan.co.il, 16.5.2025 | ~4,300 visible words, old/new majority table | title "פינוי בינוי \| מדריך" | the most complete legal guide: new majority (66/60), s.4 30% rule, 1ד cancellation grounds, abusive signing, elderly 70/75, nursing 5-6 | dated (2025), names an old ombudsman, no data, no tool, no official links |
| 4 | hiborim4u.co.il, 2023 | 398 words, 12 images | title phrase | tenant-management brand | thin, old |
| 5 | hon.co.il, 2019 | 1,236 words | "מהי התחדשות עירונית" | age, financial-guides brand | 2019, no current law |
| AIO | nadlancenter/3988 (10.5.2026) | ~2,100 words, 13 H2 | "חוק פינוי בינוי" ×N | AIO's source for "66%"; history, arnona discount, elderly | still states 80%/75% as the definition, then the 2021 change; no tables |
| AIO | shovalbinui (20.9.2026) | 1,856 words, 3 tables, 7 FAQ | "שלבי תהליך פינוי בינוי" | fresh; the "7 to 12 years" timeline table the AIO lifts | timeline unsourced (developer's estimate); "80% ומעלה" majority |
| AIO | kolzchut | not read (Cloudflare challenge on direct and reader fetch) | | | |

### G3 "התחדשות עירונית"
| # | Page | Size and form | Why it ranks | Weak spots |
|---|---|---|---|---|
| 1 | zfbuilding.co.il | ~400 words (reader), icons, video, form | developer brand, exact H1 | no information beyond benefits icons |
| 2 | engelinvest.co.il | 811 words, category | tenant-org brand, local pack | no data, 2025 in title |
| 3 | minhelet-j.org.il | 2,171 words, 83 images | the Jerusalem administration (official), fresh 19.10.2026 | one city |
| 4 | ura.co.il | 962 words, 115 images | association brand | promotional |
| 5 | dunietz-elad.co.il | 1,269 words, 30 H2 (article list), 67 images | law firm category hub | a list of links |
| 6 | hagag-group.co.il | 1,338 words | developer, Tel Aviv | one city, promotional |
| AIO | gov.il about_urban_renewal | ~200 words | the authority | definition only |

### Union checklist (what any competitor has, plus what none has)
| Item | Who has it | G2 after | G3 after |
|---|---|---|---|
| Definition, tracks, process steps | all | ✓ | ✓ |
| Majority with the current law (66% + 60% + common property), small buildings | barlev (table), AIO | ✓ + calculator | ✓ (link + FAQ) |
| s.4 owner over 30%, offender exclusion | barlev | ✓ | |
| 1ד cancellation clocks | barlev | ✓ + tool + I2 | |
| Abusive signing, ombudsman | barlev, lawx | ✓ with 2025 numbers | ✓ |
| Elderly 70 / 75, nursing, terminally ill | barlev, nadlancenter | ✓ + T6 | FAQ |
| Tax exemptions with the ceiling (120 m² / 150% / 200 m²) | none states the ceiling | ✓ + T8 computed | ✓ in T2 |
| Betterment levy by track | none | ✓ T9 | ✓ T2 |
| Standard 21 and the government calculator's assumptions | none | ✓ T10 | FAQ |
| Official time numbers (4.0 years, series) | none (shoval has an unsourced 7-12) | ✓ I3 + T11 | ✓ FAQ |
| Plans approved per year, by district | none | ✓ I4 + T12 + T13 | |
| Complexes on the authority map, stage, multiplier, per city | none | ✓ (tool) | ✓ tool + T8 + city H3s |
| TAMA 38 replacement plan per city, extension, Tel Aviv | none | | ✓ T5 |
| Building renewal: permits split, request-to-permit per city | none | | ✓ I3 + T6 + T7 |
| Tax vs authorities track with yearly declarations | none | short | ✓ I2 + T3 + T4 |
| A tool | none | ✓ pinui | ✓ urcity |
| English section | none | ✓ | ✓ |
| Photos and icons | hiborim 12, minhelet-j 83, ura 115, dunietz 67 | 4 SVG | 4 SVG (3 new + 1 old) |

---

## 4. Verified facts used on the pages (every number with its source and date)
| # | Fact | Source |
|---|---|---|
| G1 | Special majority: owners of ≥ 2/3 of the apartments in the cluster; ≥ 3/5 in every building (4-5 apartments: ≥ 3 apartments and > 2 owners); > 1/2 of the common property in every building | LAW s.1 (read 26.10.2026); gov.il renewal_faq ("66% ... 60%") |
| G2 | "בית משותף" = at least 4 apartments; "קשיש" = 70 at the first deal and 2 years in the apartment | LAW s.1 |
| G3 | Appraiser for economic feasibility: more than 2/5 of apartments and common property in every building; director names within 15 days; free; 40% per the service page | LAW s.1, 2א; gov.il service bakasha-leminuy-shamay-renewal |
| G4 | Convention + offer document ≥ 2 weeks before the first deal; notice; signed without them → majority may cancel while < 40% signed | LAW ss.1א-1ג |
| G5 | 1ד: ½ within 2 years, ⅗ within 4 years, detailed plan within 4 years 6 months (not for s.14(a)(1) complexes); +1 year at ≥ 120 units; public housing ≤ 40% excluded; payment per the 2025 regulations | LAW s.1ד |
| G6 | Refusal grounds (7), elderly options (5; 3 out-of-project for 75+, terminally ill, nursing 5/6) | LAW s.2(ב)(1)-(7) |
| G7 | Offender exclusion with > ½ owners in the building; court may reduce damages; owner > 30% in 6+ apartments counts 30% + ⅓ of excess; abusive signing (4 grounds); disclosure duty | LAW ss.2(א1), 3, 4, 5ב, 6 |
| G8 | What a deal must hold (4 items + power of attorney) | LAW s.1 "עסקת פינוי ובינוי"; gov.il renewal_faq |
| G9 | TAMA 38: expansion 60%; new apartments 2/3 + 2/3 common property via the superintendent; demolition 2/3 + 2/3 (≥ 4 apts, > 2 owners); elderly 75 in strengthening; deal clocks 18 months / 3 years / 3.5 years | LTAMA ss.4, 5, 5א, 5ג |
| G10 | Complex: ≥ 24 existing units; new ≥ 70 or double; tracks comparison rows | R25 annex A p.114 (checked on the page image) |
| G11 | Pinui binui tax: shevach exempt (ch.5 4), purchase tax exempt, VAT 0 (31א), no unit limit, downsizing 1 apartment; ceiling: max(120 m², 150% of value minus rights, +50% to 200 m²) + rent; betterment 25%, from May 2022 25/50/exempt to May 2027; ILA exempt | R25 pp.115-116 (images) |
| G12 | TAMA/fast: shevach ch.5 5 to end of 2033; demolition 2 apartments; +25 m² / ₪1,777,600; betterment rules | R25 pp.115-116 |
| G13 | 2025: 186 plans / 75,925 units (55,074 additional), 34% of approved units; permits 28,902 (13,066 in 38 PB complexes + 15,836 in 568 building projects); 86 complexes started (65,461); 5 building plans (14,084 add.); 21 replacement plans (+~286,500, in planning); 51 administrations | R25 p.22; report page (published 26.5.2026, updated 16.6.2026): 35% of approved, 28% of starts, one in five sold |
| G14 | Approval to first permit, by permit year: 2015 5.6 (4) · 2016 6.0 (7) · 2017 4.2 (9) · 2018 3.1 (10) · 2019 2.7 (10) · 2020 3.1 (5) · 2021 4.9 (23) · 2022 4.1 (33) · 2023 3.9 (28) · 2024 4.0 (43) · 2025 4.0 (28) | R25 p.87 |
| G15 | Plans approved per year 2010-2025 (8/1,909 ... 186/75,925); by district cumulative (TA 246/96,081, Center 174/112,068, Jerusalem 211/54,349, Haifa 97/44,553, North 12/4,939, South 50/29,789, J&S 1/600) | R25 pp.25 (image), 26 |
| G16 | Tax track: declaration conditions (plan deposited/approved, 66% per cluster, 60% per building); 77 new complexes / 28,771 units in 2025; per year 2015-2025; preliminary decisions 627 / 67,294 / 275,262 by district | R25 pp.68, 70 |
| G17 | **Report inconsistency**: p.71 district rows sum to 336 / 33,341 / 132,294 under a printed total of 337 / 33,488 / 133,321; the p.72 locality chart sums to 337 / 133,044 | R25 pp.71-72 (images); stated on G3 |
| G18 | TAMA 38 expired Oct 2023; extended to May 2026 or the city plan's approval (earlier) where a replacement plan is advanced; not in Bnei Brak, Bat Yam; Tel Aviv no extension; 21 replacement plans with status (Ramla, Yavne, Raanana 2024; Kfar Saba, Petah Tikva, Be'er Sheva, Lod 2025; ...), Jerusalem early check, Givatayim approved 2025, 7 cities with a plan in force before | R25 pp.90-93 |
| G19 | Fast licensing (s.145א1, amendment 139): 400% / 500% (3+ plots) / 200%; mobility 300% / 100%; 450/500/550% by order; permit request at deposit | R25 p.94 |
| G20 | Building renewal 2025: requests 430 / 10,678 (−60% vs 25,617), permits 568 / 15,836 (8,161 added; 2024: 15,574), occupied 260 / 7,419, by track | R25 p.96 |
| G21 | Permits split 2013-2025 (rebuild 28% → 65%); requests split (rebuild 71% in 2025). p.102 prints 52% strengthening for 2016, p.34 prints 58% (kept p.34; sums to 100) | R25 pp.34, 102 |
| G22 | Request to permit by city (31 cities; Ramat Gan 6.2 ... Kiryat Motzkin 1.7; Tel Aviv 4.1 with 180 permits; Jerusalem 3.4) | R25 pp.109-110 |
| G23 | Apartments sold in renewal projects 2025 by city (Tel Aviv 1,292, Petah Tikva 817, Jerusalem 769 ...) | R25 p.41 |
| G24 | Ombudsman: ~135 filed, 73 closed, ~185 decided in 2025; budget ₪366m (2025); ₪94.1m to planning | R25 pp.18, 42 |
| G25 | Developers pay all project costs; arnona discount on the added area, limited and gradual; elderly on income support: 5 years of the maintenance difference | gov.il renewal_faq (reader, 26.10.2026) |
| G26 | Standard 21 updated 13.6.2022: no fixed profit/compensation; sensitivity table; before ~25 m² customary and ~20% profit; the government appraiser sets minimum profit by area | gov.il policies/standard_21 |
| G27 | Government calculator assumptions: 36 months evacuation, 12 m² safe room, ~90 m² land per unit, tenant costs ~5%, maintenance fund 10 years ₪350 for 65%, developer purchase tax 5%, 20% profit | gov.il pages/model_dinami |
| G28 | Authority map 25.10.2026: 993 complexes, 79 localities; stages 105 / 302 / 345 / 53 / 188 none; tracks 551 / 240 / 202; units 152,722 → 615,036; multiplier 4.01 (our calc on pairs) | renewal-track.json + renewal-stats.json (Q1 pipeline) |

**Unverified, kept off the pages:** the government appraiser's regional minimum profit rates (14-17%, only in press coverage), the
arnona discount percentages by year (press only), what each city decided after May 2026, "7 to 12 years" for a whole project
(developer's estimate), "2/3 per building" variants in old articles, kolzchut's text (not readable), any start or occupancy year.

---

## 5. Our pages today (raw HTML, 26.10.2026) and the gaps
**G2 today:** title "פינוי בינוי: שלבים, רוב נדרש ומה מקבלים בעלי הדירות | נדלן"; H1 "פינוי בינוי: המסלול המלא מהחתמה ועד מפתח"; 1,530
words, 0 tables, 10 figures, 0 tools, 4 FAQ (no FAQPage), 1 official link, modified 12.7.2026.
Honesty errors found in the live text (fixed by the writer, R_FIX): "מאז חוק ההסדרים של 2023 די בהסכמת 66%" and "מ-2024, הסכמה של 67% ...
(ירידה מ-80%)" contradict the law today (67% is the old appraiser majority, not the refuser rule); single building "80% / 75%" is the old
TAMA rule (today 2/3 + 2/3); "a national average close to a decade" has no source; "many apartments of one owner" is not a pinui binui
tax exception (annex: no limit).
**G3 today:** title 71 chars with four protected terms of other pages; H1 "התחדשות עירונית: מה בודקים לפני שחותמים"; 3,885 words (3,986 by
depth_proof), 1 table, 54 figures, 2 tools (lookup, consent calculator), 7 FAQ (no FAQPage), 1 official link, modified 3.10.2026.
Language and design findings: "בקרוב נשיק כאן חדר פרויקט..." (a promise of something that is live at /my-renewal/), "מערכת", "מודל",
and the start band, links and Tel Aviv box in the banned cream/brown/terracotta palette (fixed by style-only edits); **the lookup and
consent-calculator shortcodes still print that palette from plugin code (inc/urban-hub.php, inc/urban-tools.php), the lookup says "כפי
שנמשך ב-13.7.2026"; urban-hub.php is another agent's file now, so not touched**; the old infographic SVG keeps its palette inside.
Both pages: no FAQPage schema today; it appears once a [nadlan_tool] is on the page (inc/instruments.php builds it from the FAQ section).

---

## 6. BUILD SPEC (implemented in the writers; rendered order H1 → answer → CTAs → tool → numbers → article)

### 6.1 G2 /urban-renewal/pinui-binui/ (page 5446)
- **Title** `פינוי בינוי: החוק, הרוב הנדרש, השלבים ומה מקבלים | נדלן` (55) · **meta** (149) · **H1** `פינוי בינוי: המסלול המלא לפי החוק, מהחתימה ועד המפתח`.
- **Answer** (first sentence = the definition with the head term; then the law's majority; then 186 / 75,925 / 4.0 years with the source).
- **CTAs**: בדקו את הרוב בבניין שלכם (#pinui-tool) · לקבלת פרטים נוספים בוואטסאפ · בדיקת בניין חינמית.
- **Moat, tool `pinui`**: maj (the special majority building by building, the gap in red, the appraiser line, the 40% line, the complex
  at the authority), mine (tax-free ceiling for my size, multiplier, what the law fixes vs the negotiation, 70/75 options), time (the 1ד
  dates from my first deal, years since approval vs the 4.0-year average worded as an average). Nobody in the SERP has a tool; nobody
  states the current majority with the per-building trap or the 1ד clock with dates.
- **Sections added** (anchors): פינוי בינוי לפי החוק (T2) · הרוב הנדרש (I1, T3, T4) · דייר סרבן וקשישים (T5, T6) · השעון של היזם (I2,
  T7) · tax ceiling and taxes (T8, T9) · who pays and standard 21 (T10) · official time numbers (I3, T11, I4, T12, T13) · special cases ·
  25 new FAQ (all 9 PAA + GSC long tail + volume terms) · English section · method line "עודכן 26.10.2026".
- **Infographics**: I1 three buildings, one majority · I2 the 1ד clock · I3 approval to permit by year · I4 plans approved per year.

### 6.2 G3 /urban-renewal/ (page 73)
- **Title** `התחדשות עירונית: המסלולים, המספרים והמתחמים בכל עיר | נדלן` (58) · **meta** (144) · **H1** `התחדשות עירונית: המסלולים, המספרים בכל עיר ומה בודקים לפני שחותמים`.
- **Answer**: definition with the head term; the three tracks named; 35% / 28% (2025) and 993 complexes in 79 cities (25.10.2026).
- **CTAs**: התחדשות עירונית בעיר שלכם (#urcity-tool) · לקבלת פרטים נוספים בוואטסאפ · בדיקת בניין חינמית.
- **Moat, tool `urcity`**: city (complexes by stage and track, units and multiplier, what moved since the file, the report's TAMA 38 line,
  request-to-permit years, sales, tax declarations; table of every complex), track (which of the three tracks stays open for my building
  and the majority in apartments), rank (all cities). Tied to the tracker: same data file, links to the map and the tracker.
- **Sections added**: three tracks side by side (I1, T2 with 11 rows) · tax vs authorities track (I2, T3, T4, the report inconsistency
  note) · TAMA 38 in every city (T5, T6, T7, I3 in the tracks section) · urban renewal by city (T8, 10 city H3s: Jerusalem, Haifa, Tel
  Aviv, Ramat Gan, Be'er Sheva, Petah Tikva, Netanya, Bat Yam, Holon, Rishon) · the authority and administrations · 18 new FAQ ·
  English section · method line.

### 6.3 Design (Claude Design components PinuiBinuiPage and UrbanRenewalHub, not published)
Palette ink #12202A, sea #2F6F86 (in process), deep #1F4B5C (approved / holds), line #D3DCE2, survey red #C42550 only for a gap;
IBM Plex Sans Hebrew + Plex Mono; tool titles in Karantina (engine). **Why not the default AI look:** a planning sheet and a rights table,
not a card deck: no cream, brass, terracotta or gradient, no acid accent on black, every colour states a status.

---

## 7. Proof plan and the predicted honesty statement
Competitors: `competitors-g2.txt` (mako, lawx, barlev, hiborim, hon, nadlancenter/3988, shoval, laws-nadlan, digagroup) and
`competitors-g3.txt` (zf, engel, minhelet-j, ura, dunietz, hagag, b-g, shoob, mitar, africa-ur). Facts: `coverage-facts-g2.json` (35),
`coverage-facts-g3.json` (32). After the release: `python tools/depth_proof.py --ours <live url> --them $(cat competitors-g*.txt)` and
`python tools/fact_coverage.py --facts coverage-facts-g*.json --urls <live url> $(cat competitors-g*.txt)`.

| Metric (depth_proof, raw HTML) | G2 now | G2 predicted (local render) | best G2 competitor | G3 now | G3 predicted | best G3 competitor |
|---|---|---|---|---|---|---|
| words | 1,535 | 6,200 | 1,797 shoval (barlev ~4,300 visible incl. menus; lawx 1,407 by reader) | 3,986 | 8,548 | 2,171 minhelet-j |
| figures | 10 | 661 | 33 shoval | 73 | 962 | 106 minhelet-j |
| tables / cells | 0 / 0 | 13 / 410 | 3 / 48 shoval | 1 / 12 | 9 / 655 | 0 / 0 |
| tools | 0 | 1 | 0 | 1 | 1 (+ the 2 old ones) | 0 |
| FAQ | 4 | 29 | 7 shoval | 11 | 29 (25 in schema) | 1 ura |
| headings | 20 | 57 | 22 shoval | 35 | 71 | 30 dunietz |
| facts covered (fact_coverage) | 4 / 35 | 35 / 35 | 15 barlev | 5 / 32 | 32 / 32 | 4 minhelet-j |
| visuals | 0 | 4 | **12 hiborim** (9 nadlancenter) | 1 | 4 | **115 ura** (83 minhelet-j, 67 dunietz) |
| official sources | 1 | 2 domains (8 links) | 1 shoval | 1 | 2 domains (6 links) | 0 |

**Predicted honest statement (to be confirmed by the after-release run, never printed before it):** "בעמוד הזה יותר מידע מכל אחד
מהעמודים שמופיעים ראשונים בגוגל על 'פינוי בינוי', ומכולם יחד: יותר מילים, מספרים, טבלאות, שאלות ותשובות ועובדות שנבדקו, ומחשבון
שאין לאף אחד מהם. מקורות: החוק בנוסחו היום ודוח הרשות לשנת 2025. איפה אחרים מובילים: בתמונות (12 אצל hiborim4u מול 4 איורים כאן)."
Same for G3 with "התחדשות עירונית" and the pictures line (115 at ura.co.il, mostly logos and photos, vs 4 drawings).
Not measurable by script and named as such: mako (blocks scripts), lawx and zf (render in JS); their reader text was measured by hand
(689 / 1,407 / 403 words, 1 / 3 / 0 facts).

---

## 8. What needs Ben, findings, what could not be verified
**Ben's word:** (1) the release (tools + data + registry + summaries) and running the two writers; (2) the G3 title change (it removes
"פינוי בינוי" and "תמ״א 38" from the hub's title to stop the overlap; the hub gets 0 clicks, so the risk is low); (3) the family BLOCKs:
two glossary pages titled "פינוי בינוי" (duplicates of each other) and the tenant guide titled "פינוי בינוי 2026" (old brand in the
title): re-target text tested, or retire on his word; (4) the style-only reform of the old G3 start band.
**Findings:** /city/<name>/projects/ answers **410** for every city tested while Search Console still shows impressions on those URLs
(e.g. "פינוי בינוי באר שבע" 61@29 on /projects/?city=באר שבע; /city/חיפה/projects/ 27@66); the lookup on /urban-renewal/ still says
"כפי שנמשך ב-13.7.2026" and prints the old palette (inc/urban-hub.php, another agent's file today); the consent calculator and the old
G3 infographic keep the old palette; the report's own cumulative tax-track tables do not add up (G17); gov.il answers 403 to scripts
(official links checked by reader, not by status code).
**Could not verify:** kolzchut (Cloudflare), the regional minimum profit of the government appraiser, the arnona discount schedule, what
happened to TAMA 38 in each city after May 2026, the official 2025 list of the 51 administrations by city (gov.il app is JS-only).
