# Q1 · /urban-renewal/map/ · page DNA and build spec

Research date: 25.10.2026 (Israel evening; SERPs pulled 19:21 to 19:23 UTC). Research only: nothing on the live site was changed, no Linear or Notion item was created.
Refreshes, does not redo: `docs/research/urban-renewal-2026-10/` (3.10.2026: competitors.md, demand-data.md, upgrade-plan.md, code-facts.md). The HAD-396 honesty fixes are taken as done.

Evidence classes used below: **SERP** (DataForSEO Google organic live advanced, Israel 2376, Hebrew, depth 20, raw JSON saved), **raw** (page HTML fetched as Google gets it, no scripts run, saved), **API** (official open data queried directly, saved), **GSC** (Search Console API, sc-domain:nad-lan.co.il, 25.7 to 23.10.2026), **prior** (verified in the 3.10.2026 research, with its source), **unverified** (kept out of the spec).

Raw evidence (private, not in the repo):
- SERP JSON: `C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\serp\q1_*.json` and readable digest `q1_summary.txt`
- Competitor HTML: `C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\raw\q1\` (gov.il pages via reader proxy, `*.reader.md`, because gov.il answers 403 to direct fetch)
- Official data pulls: `C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\data\` (`ur_datastore.json`, `ur_resource_show.json`, `arcgis_layer1_*.json`, `xplan_sample.json`, `our_renewal_map_data.json`, `gsc_query_page_90d.csv`, `ur_stats.py`)
- Baseline proof: `proof-before.md` in this folder.

---

## 1. Intents and keyword set

GSC, 90 days, this page: 1,919 impressions, 9 clicks, 76 queries.

| # | Intent (what the searcher wants) | Owned head term | Synonyms and long tail (GSC impressions@position) |
|---|---|---|---|
| 1 | See the official map of renewal complexes | מפת התחדשות עירונית (362@13.3) | התחדשות עירונית מפה 30@7 · מפת פינוי בינוי 29@11 · פינוי בינוי מפה 16@7 · מפת התחדשות 3@11 · הרשות להתחדשות עירונית מפה 3@7 |
| 2 | List of declared or approved complexes | מתחמי פינוי בינוי (164@18.9) | מתחמי התחדשות עירונית 102@17.8 · מתחם פינוי בינוי 75@38.8 · מתחמי פינוי בינוי מאושרים 61@26.5 · מתחמים מוכרזים לפינוי בינוי 10@9 · מתחמי פינוי בינוי מוכרזים 3@9 · אזורי פינוי בינוי 12@28 |
| 3 | Is a specific complex or building in renewal, what does "מתחם" mean | מתחם התחדשות עירונית (122@26.8) | פרויקט התחדשות עירונית 54@35 · תוכנית התחדשות עירונית 23@39 · איפה יש פינוי בינוי 15@54 · סטטוס פינוי בינוי 1@55 · מסלול רשויות פינוי בינוי 1@25 |
| 4 | Projects list (which projects exist, which are building) | פרויקטים בהתחדשות עירונית (208@66.9) | פרויקטים פינוי בינוי 133@58 · התחדשות עירונית פרויקטים 123@64 · פרויקט פינוי בינוי 32@61 · איזה פרויקטים של פינוי בינוי במרכז נמצאים כבר בשלבי בנייה? 7@5 · פרויקטים חדשים התחדשות עירונית 15@25 |
| 5 | The same, by city | מפת התחדשות עירונית + city | ראשון לציון 51+38+27 (three queries) · תל אביב 17+17 · ירושלים 16 · רמת גן 8+6 · חולון 4 · באר שבע 3 · נתניה 3 · בת ים 3+2 · חדרה 2 · פתח תקווה 10 |

Monthly Google volume (DataForSEO Google Ads, from the 3.10 research, prior): מפת התחדשות עירונית 260 · פרויקטים פינוי בינוי 210 · מתחמי פינוי בינוי 70 · מפת פינוי בינוי 40.

Where we stand in the live SERP today (SERP, desktop unless noted): not in the top 20 for "מפת התחדשות עירונית" (desktop and phone) although GSC averages 13.3 over 90 days (rank varies by day and person); #10 for "מתחם התחדשות עירונית"; #6 for "פרויקטים פינוי בינוי"; not in the top 20 for "מתחמי פינוי בינוי", "מתחמי התחדשות עירונית", "מתחמי פינוי בינוי מאושרים", "פרויקטים בהתחדשות עירונית".

### Cannibalization (GSC + `url_word_audit.py`)
- `--token map`: one owner, `/urban-renewal/map/`. Clean.
- `--token renewal`: 17 URLs, `--token pinui`: 6 URLs. None of them competes on the map or complex queries in GSC.
- The real split is with **`/projects/`** on the "projects" words: "פרויקט פינוי בינוי" 178@48.7 on /projects/ vs 32@61.2 on the map; "פרויקטים של פינוי בינוי" 31@45.9 vs 17@62.8; "פרויקטים בהתחדשות עירונית" 102@49.8 vs 208@66.9; "פרויקטים פינוי בינוי" 65@46.1 vs 133@58.3. Both URLs are weak (positions 46 to 67).
- Minor: `/urban-renewal/pinui-binui/` (197 impressions on pinui words, position 73) and the city project pages `/city/ראשון לציון/projects/` (44@39).
- **Ownership decision (no new URL, no redirect, no noindex):** the map page owns intents 1, 2, 3 and 5 (map, complexes, "מתחם", city maps). Intent 4 ("projects") stays shared: the map page answers it with the in-execution and approved lists (the complexes are the projects), and `/projects/` keeps the marketed new-build catalogue. Internal links: `/projects/` pinui filter and the city project pages link to the map with the anchor "מפת התחדשות עירונית"; the map links back to `/projects/?project_type=pinui_binui` with the anchor "פרויקטי פינוי בינוי בשיווק".

---

## 2. SERP snapshot (top 10 per query)

Union of what Google shows across the nine Q1 SERPs:
- **People also ask: absent in all nine SERPs** (desktop and phone). FAQ wording below therefore comes from related searches, "people also search", the AI overview sub-topics and our own GSC long tail.
- **AI overview: present in all nine.** It consistently answers with (a) the authority's map and complex list on gov.il, (b) XPLAN and mavat for plan status, (c) a definition of the complex types (declared, public body, developer, preferred housing complex, in execution), (d) national totals: "כ-970 מתחמי פינוי-בינוי ב-76 ערים... כ-592 מוכרזים רשמית... כ-150,000 דירות ישנות בכ-615,000 דירות חדשות", with a ranked city list (Jerusalem 213, Ramat Gan 78, Tel Aviv 55, Haifa 46, Netanya 41, Bat Yam 39, Petah Tikva 37). Its non-government source for those numbers is **dehaas.co.il/pinui-binui-by-city/**. For "מתחם התחדשות עירונית" it also cites municipal administrations (Kfar Saba, Yehud, Be'er Ya'akov, Ness Ziona) and getstatus for an address check.
- **What Google wants to show:** an official-feeling list by city with counts, status per complex, track (tax or authorities), and where to check the plan. It rewards the page that states the national totals and the city ranking in its first lines (dehaas, netunim), and it cites gov.il for "where is the map".
- Related and "people also search" union: מתחמי פינוי בינוי ירושלים · מתחמי פינוי בינוי תל אביב-יפו · מתחמי פינוי בינוי מאושרים ירושלים · בדיקת סטטוס פינוי בינוי (ירושלים, תל אביב, בת ים, פתח תקווה) · מכפיל פינוי בינוי · הכרזה על פינוי בינוי · ועדה מחוזית פינוי בינוי · חוק פינוי בינוי · מחשבון פינוי בינוי · תמל 2030 · מפת התחדשות עירונית פתח תקווה / ירושלים · התחדשות עירונית תל אביב מפה · מנהלת התחדשות עירונית · איתור תוכנית לפי גוש חלקה · תוכניות בניה לפי כתובת · איתור תכנית מנהל התכנון · דירוג יזמים פינוי בינוי.

### Top 10 per query (raw: serp/q1_*.json; long dashes in quoted titles normalised to ·)

#### "מפת התחדשות עירונית" (desktop), retrieved 2026-10-25 19:21 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | gov.il | https://gov.il/he/departments/government_authority... | https://gov.il/he/departments/government_authority_for_urban_renewal/govil-landing-page |
| 2 | meirim.org | חיפוש תוכניות בנייה | https://meirim.org/plans/ |
| 3 | cramim-pt.co.il | מסמך מדיניות להתחדשות עירונית , מרכז העיר פתח תקווה | https://cramim-pt.co.il/wp-content/uploads/2023/05/מצגת-דיון-וועדה-מקומית-17.11.22.pdf |
| 4 | www.gov.il | רשימת תכניות להתחדשות עירונית | https://www.gov.il/he/pages/plans_haifa |
| 5 | city-buildrs.com | בוני העיר: בית | https://city-buildrs.com/ |
| 6 | www.gov.il | מה מתוכנן באזורך - מערכת XPLAN לאיתור תכניות מקוונות | https://www.gov.il/he/service/searching-plans-submitted-planning-institutes-in-xplan-site |
| 7 | www.facebook.com | עירוניות מתחדשת בישראל | https://www.facebook.com/groups/Urbanism.il/?locale=he_IL |
| 8 | erets-ir.co.il | מדריך התחדשות עירונית 2024 - ייעוץ ראשוני חינם בחברת ''ארץ עיר'' | https://erets-ir.co.il/מדריך-התחדשות-עירונית-2024/ |
| 9 | www.madlan.co.il | בניין עיר - התחדשות עירונית · לוח יזמי נדל"ן של ... | https://www.madlan.co.il/developer/binyanir |
| 10 | newkey.co.il | התחדשות עירונית בישראל - באתר NewKey | https://newkey.co.il/urban-regeneration/ |

- nad-lan.co.il in this SERP: not in top 20
- People also ask: absent
- Related searches: הרשות להתחדשות עירונית בעלי תפקידים · הרשות להתחדשות עירונית טלפון · הרשות הממשלתית להתחדשות עירונית דרושים · איתור תוכנית דירה · חוק הרשות הממשלתית להתחדשות עירונית · איתור תוכנית לפי גוש חלקה · תוכנית דירה לפי גוש חלקה · תוכניות בניה לפי כתובת
- AI overview: present. Gist: ניתן לצפות במפת התחדשות עירונית ארצית ומפורטת דרך מפת התחדשות עירונית בישראל - Gov.il של הרשות הממשלתית להתחדשות עירונית. מערכת XPLAN / קווים כחולים · לאיתור תכניות בנייה ותכניות מתאר מקוונות ברחבי הארץ. אתר מידע תכנוני - מבא"ת · לחיפוש תכניות בנייה לפי גוש, חלקה, כתובת או מספר תכנית. רשימת מתחמים בהתחדשות עירונית · מאגר המציג מתחמי פינוי-בינוי וסטטוס הכרזה לפי יישובים. אם תרצה, תוכל לכתוב לי איזה עיר או כתובת מעניינ…
- AI overview sources: https://www.gov.il/he/departments/topics/mapa-renewal · https://mavat.iplan.gov.il/SV3 · https://www.gov.il/he/service/searching-plans-submitted-planning-institutes-in-xplan-site · https://mavat.iplan.gov.il/SV3?searchEntity=0&searchType=0&entityType=0&searchMethod=2 · https://www.gov.il/apps/moch/viewlist/renew-cf/mitchamim-rashut

#### "מפת התחדשות עירונית" (mobile), retrieved 2026-10-25 19:21 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | gov.il | https://gov.il/he/departments/government_authority... | https://gov.il/he/departments/government_authority_for_urban_renewal/govil-landing-page |
| 2 | meirim.org | חיפוש תוכניות בנייה | https://meirim.org/plans/ |
| 3 | cramim-pt.co.il | מסמך מדיניות להתחדשות עירונית , מרכז העיר פתח תקווה | https://cramim-pt.co.il/wp-content/uploads/2023/05/מצגת-דיון-וועדה-מקומית-17.11.22.pdf |
| 4 | www.gov.il | רשימת תכניות להתחדשות עירונית | https://www.gov.il/he/pages/plans_haifa |
| 5 | city-buildrs.com | בוני העיר: בית | https://city-buildrs.com/ |
| 6 | www.gov.il | מה מתוכנן באזורך - מערכת XPLAN לאיתור תכניות מקוונות · מינהל התכנון | https://www.gov.il/he/service/searching-plans-submitted-planning-institutes-in-xplan-site |
| 7 | www.facebook.com | עירוניות מתחדשת בישראל | https://www.facebook.com/groups/Urbanism.il/?locale=he_IL |
| 8 | erets-ir.co.il | מדריך התחדשות עירונית 2024 - ייעוץ ראשוני חינם בחברת ''ארץ עיר'' | https://erets-ir.co.il/מדריך-התחדשות-עירונית-2024/ |
| 9 | www.madlan.co.il | בניין עיר - התחדשות עירונית · לוח יזמי נדל"ן של ... | https://www.madlan.co.il/developer/binyanir |
| 10 | newkey.co.il | התחדשות עירונית בישראל - באתר NewKey | https://newkey.co.il/urban-regeneration/ |

- nad-lan.co.il in this SERP: not in top 20
- People also ask: absent
- Related searches: absent
- AI overview: present. Gist: ניתן לצפות במפה הרשמית של פרויקטים ומתחמים דרך מפת התחדשות עירונית בישראל של הרשות הממשלתית להתחדשות עירונית. מטרת המפה: הצגת מידע על חידוש, חיזוק ומיגון בנייני מגורים, פרויקטים של פינוי-בינוי, תוכניות מתאר ושלבי מתחמים ברחבי הארץ. מקור הנתונים: הרשות הממשלתית להתחדשות עירונית, בשיתוף יזמים ורשויות מקומיות (עם עדכונים שוטפים). סוגי מתחמים המוצגים: מוכרזים: מתחמים שהוכרזו לפינוי לשם בינוי (מזכים בקידום תכנוני והטבות מ…
- AI overview sources: https://www.gov.il/he/departments/topics/mapa-renewal · https://www.gov.il/he/pages/mitchamim · https://digital.ashdod.muni.il/page/gis-newironi

#### "מתחמי פינוי בינוי" (desktop), retrieved 2026-10-25 19:21 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | www.gov.il | שאלות ותשובות בנושאי התחדשות עירונית | https://www.gov.il/he/pages/renewal_faq |
| 2 | dehaas.co.il | מאגר יזמי התחדשות עירונית · 47 יזמי פינוי בינוי, מתחמים והיתרים | https://dehaas.co.il/pinui-binui-by-city/yazamim/ |
| 3 | www.city-people.co.il | אזורי התחדשות עירונית לפי תכנית המתאר | https://www.city-people.co.il/אזורי-התחדשות-עירונית-לפי-תכנית-המתאר/ |
| 4 | www.facebook.com | הרשות הממשלתית להתחדשות עירונית | https://www.facebook.com/hitchadshuteronit/photos/אתם-שואליםאנחנו-עוניםשומעים-לאחרונה-על-הכרזות… |
| 5 | www.amidor.co.il | מילון מושגים - התחדשות עירונית - עו"ד ... | https://www.amidor.co.il/dictionary-urban-renewal/ |
| 6 | www.rashuiot.co.il | 8163 דירות חדשות: הוכרזו 17 מתחמי פינוי-בינוי חדשים | https://www.rashuiot.co.il/html5/arcLookup.taf?_function=details&_ID=68518&did=1118&G=8640&SM= |
| 7 | mitar.co.il | מה זה מתחם מוכרז לפינוי בינוי · ולמה הכרזה היא לא הבטחה - מתאר | https://mitar.co.il/articles/declared-complex-not-a-promise |
| 8 | tidhar.co.il | התחדשות עירונית - פרויקטים על הנייר תכנון וניהול | https://tidhar.co.il/urban-renewal/ |
| 9 | www.kolzchut.org.il | התחדשות עירונית (תמ"א 38, פינוי-בינוי) | https://www.kolzchut.org.il/he/התחדשות_עירונית_(תמ"א_38,_פינוי-בינוי) |
| 10 | hl-jerusalem.co.il | החברה להתחדשות ירושלים - בעלי דירות מובילים להצלחה | https://hl-jerusalem.co.il/ |

- nad-lan.co.il in this SERP: not in top 20
- People also ask: absent
- Related searches: מתחמי פינוי בינוי ירושלים · מתחמי פינוי בינוי תל אביב-יפו · חוק פינוי בינוי · מכפיל פינוי בינוי · הכרזה על פינוי בינוי · ועדה מחוזית פינוי בינוי · פינוי בינוי מדריך · שמאות פינוי בינוי · פינוי בינוי כל זכות
- AI overview: present. Gist: בישראל פועלים כיום מאות מתחמי פינוי- בינוי המרוכזים דרך הרשות הממשלתית להתחדשות עירונית. היקף ארצי: קיימים כ-970 מתחמי פינוי-בינוי ב-76 ערים שונות ברחבי הארץ, כאשר מתוכם כ-592 מוכרזים רשמית. גידול ביחידות דיור: התוכניות המוצעות אמורות להחליף כ-150,000 דירות ישנות בכ-615,000 דירות חדשות (תוספת נטו של למעלה מ-464,000 יחידות דיור). ערים מובילות בהיקף מתחמים: ירושלים: כ-213 מתחמים רמת גן: כ-78 מתחמים תל אביב-יפו: כ-55 מת…
- AI overview sources: https://www.gov.il/he/pages/mitchamim · https://dehaas.co.il/pinui-binui-by-city/

#### "מתחמי פינוי בינוי" (mobile), retrieved 2026-10-25 19:22 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | www.dunietz-elad.co.il | מירושלים עד בת ים: הוכרזו 10 מתחמי פינוי בינוי | https://www.dunietz-elad.co.il/10-מתחמי-פינוי-בינוי-חדשים/ |
| 2 | minhelet.oryehuda.muni.il | מילון מונחים בהתחדשות עירונית | https://minhelet.oryehuda.muni.il/9/ |
| 3 | www.gov.il | הרשות הממשלתית להתחדשות עירונית · מתחמים בהתחדשות עירונית | https://www.gov.il/apps/moch/viewlist/renew/mitchamim-rashut |
| 4 | www.rashuiot.co.il | 8163 דירות חדשות: הוכרזו 17 מתחמי פינוי-בינוי חדשים | https://www.rashuiot.co.il/html5/arcLookup.taf?_function=details&_ID=68518&did=1118&G=8640&SM= |
| 5 | www.facebook.com | הרשות - אתם שואלים❓ אנחנו עונים✅ שומעים לאחרונה על הכרזות של מתחמים לפ | https://www.facebook.com/hitchadshuteronit/photos/אתם-שואליםאנחנו-עוניםשומעים-לאחרונה-על-הכרזות… |
| 6 | www.kolzchut.org.il | התחדשות עירונית (תמ"א 38, פינוי-בינוי) | https://www.kolzchut.org.il/he/התחדשות_עירונית_(תמ"א_38,_פינוי-בינוי) |
| 7 | mitar.co.il | מה זה מתחם מוכרז לפינוי בינוי · ולמה הכרזה היא לא הבטחה - מתאר | https://mitar.co.il/articles/declared-complex-not-a-promise |
| 8 | tidhar.co.il | התחדשות עירונית - פרויקטים על הנייר תכנון וניהול | https://tidhar.co.il/urban-renewal/ |
| 9 | www.engelinvest.co.il | פינוי בינוי - מדריך מקצועי לשנת 2024 , יתרונות וזמנים ומחיר | https://www.engelinvest.co.il/category/מה-זה-פינוי-בינוי |
| 10 | hl-jerusalem.co.il | החברה להתחדשות ירושלים - בעלי דירות מובילים להצלחה | https://hl-jerusalem.co.il/ |

- nad-lan.co.il in this SERP: not in top 20
- People also ask: absent
- Related searches: absent
- AI overview: present. Gist: בישראל פועלים כיום מאות מתחמי פינוי- בינוי המרוכזים דרך הרשות הממשלתית להתחדשות עירונית. היקף ארצי: קיימים כ-970 מתחמי פינוי-בינוי ב-76 ערים שונות ברחבי הארץ, כאשר מתוכם כ-592 מוכרזים רשמית. גידול ביחידות דיור: התוכניות המוצעות אמורות להחליף כ-150,000 דירות ישנות בכ-615,000 דירות חדשות (תוספת נטו של למעלה מ-464,000 יחידות דיור). ערים מובילות בהיקף מתחמים: ירושלים: כ-213 מתחמים רמת גן: כ-78 מתחמים תל אביב-יפו: כ-55 מת…
- AI overview sources: https://www.gov.il/he/pages/mitchamim · https://dehaas.co.il/pinui-binui-by-city/

#### "מתחם התחדשות עירונית" (desktop), retrieved 2026-10-25 19:22 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | azr.bartech-net.co.il | המינהלת להתחדשות עירונית - הוועדה המקומית לתכנון ובניה אזור | https://azr.bartech-net.co.il/המינהלת-להתחדשות-עירונית/ |
| 2 | minhelet.oryehuda.muni.il | מילון מונחים בהתחדשות עירונית | https://minhelet.oryehuda.muni.il/9/ |
| 3 | hl-jerusalem.co.il | החברה להתחדשות ירושלים - בעלי דירות מובילים להצלחה | https://hl-jerusalem.co.il/ |
| 4 | www.gov.il | התחדשות עירונית | https://www.gov.il/he/departments/topics/renewal_urbanism |
| 5 | he.wikipedia.org | התחדשות עירונית | https://he.wikipedia.org/wiki/התחדשות_עירונית |
| 6 | magdilim.co.il | מגדילים · חדשות הנדל"ן בישראל, התחדשות עירונית, בנייה ויזמות בישראל | https://magdilim.co.il/ |
| 7 | my-town.co.il | קבוצת MY-TOWN התחדשות עירונית: homepage | http://my-town.co.il/ |
| 8 | r-m-a.co.il | מה זה התחדשות עירונית - מדריך להתחדשות בניינית בישראל | https://r-m-a.co.il/about-urban-renewal/ |
| 9 | www.shelomi.org.il | נוהל התחדשות עירונית · שלומי | https://www.shelomi.org.il/נוהל-התחדשות-עירונית-שלומי/ |
| 10 | nad-lan.co.il | מפת התחדשות עירונית: פרויקטים ומתחמי פינוי בינוי לפי עיר · נדלן | https://nad-lan.co.il/urban-renewal/map/ |

- nad-lan.co.il in this SERP: #10
- People also ask: absent
- Related searches: מפת התחדשות עירונית ירושלים · התחדשות עירונית פינוי בינוי · מנהלת התחדשות עירונית ירושלים · החברה להתחדשות עירונית ירושלים · התחדשות עירונית נהריה · התחדשות עירונית יבנה · התחדשות עירונית אור יהודה · בדיקת סטטוס פינוי בינוי ירושלים · מדריך להתחדשות עירונית · מתחמי פינוי בינוי מאושרים ירושלים · התחדשות עירונית מינהל התכנון · תוכנית להתחדשות עירונית
- AI overview: present. Gist: ניתן לאתר ולעקוב אחר מתחמי התחדשות עירונית באמצעות הרשות הממשלתית להתחדשות עירונית או דרך מערכות מידע עירוניות ומקומיות. מוכרזים: מתחמים לפינוי לשם בינוי שהוכרזו על ידי מנהל הרשות או שר הבינוי והשיכון, המקבלים קידום במוסדות תכנון והטבות מס. מקודמים ע"י גוף ציבורי / יזמים: מתחמים שנמצאים בשלבי תכנון או עמדו בתנאי סף לקליטה במוסדות התכנון. מתחם מועדף לדיור: מתחמים שהוכרזו על ידי הממשלה ומקודמים במסלול מהיר. בביצוע: מתח…
- AI overview sources: https://www.gov.il/he/pages/mitchamim · https://www.gov.il/apps/moch/viewlist/renew-cf/mitchamim-rashut · https://ksaba-minhelet.complot.co.il/מתחמי-התחדשות-עירונית/ · https://yehud-monosson.muni.il/pcat/מתחמי-התחדשות-עירונית/ · https://www.b-y.org.il/duplicated-1702993078/ · https://www.nzc.org.il/רשימת-מתחמי-התחדשות-עירונית-נס-ציונה/ · https://search.getstatus.online/he/magazine/urban-renewal-project-my-address

#### "מתחמי התחדשות עירונית" (desktop), retrieved 2026-10-25 19:22 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | magdilim.co.il | התחדשות עירונית - החדשות העדכניות ביותר בישראל [2026] | https://magdilim.co.il/category/פינוי-בינוי/ |
| 2 | www.amidor.co.il | מילון מושגים - התחדשות עירונית - עו"ד ... | https://www.amidor.co.il/dictionary-urban-renewal/ |
| 3 | www.facebook.com | הרשות הממשלתית להתחדשות עירונית | https://www.facebook.com/hitchadshuteronit/posts/שבעה-מתחמים-חדשים-יוכרזו-כמתחמים-לפינוי-ובינוי… |
| 4 | pinuibinui.org.il | החברה להתחדשות עירונית · התחדשות עירונית · פינוי בינוי · התחדשות ... | https://pinuibinui.org.il/ |
| 5 | www.hon.co.il | מהי התחדשות עירונית - הון מדריכים פיננסים | https://www.hon.co.il/מהי-התחדשות-עירונית/ |
| 6 | www.kipa.co.il | דווקא עכשיו: 14 מתחמי פינוי בינוי חדשים ברחבי הארץ | https://www.kipa.co.il/חדשות/חדשות-נדלן/1169892-0/ |
| 7 | gov.il | https://gov.il/he/departments/government_authority... | https://gov.il/he/departments/government_authority_for_urban_renewal/govil-landing-page |
| 8 | www.facebook.com | הרשות הממשלתית להתחדשות עירונית‎ (@hitchadshuteronit) | https://www.facebook.com/hitchadshuteronit/?locale=el_GR |
| 9 | www.city-people.co.il | אזורי התחדשות עירונית לפי תכנית המתאר | https://www.city-people.co.il/אזורי-התחדשות-עירונית-לפי-תכנית-המתאר/ |
| 10 | www.facebook.com | הרשות הממשלתית להתחדשות עירונית | https://www.facebook.com/hitchadshuteronit/posts/שבעה-מתחמים-חדשים-יוכרזו-כמתחמים-לפינוי-ובינוי… |

- nad-lan.co.il in this SERP: not in top 20
- People also ask: absent
- Related searches: יזמים התחדשות עירונית · אתר התחדשות עירונית · רשימת התחדשות פתח תקווה · איפה יש פינוי בינוי בפתח תקווה · פינוי בינוי חדשות · דירוג יזמים פינוי בינוי · פינוי בינוי מגדל העמק · מגדילים הטובים ביותר · מפת התחדשות עירונית · כנס מגדילים 2026 · הרשות הממשלתית להתחדשות עירונית · מגדילים טלפון · מגדילים התחדשות עירונית · כנס מגדילים חוות רונית · התחדשות עירונית בארץ
- AI overview: present. Gist: ניתן לאתר ולעקוב אחר מתחמי התחדשות עירונית באמצעות הרשות הממשלתית להתחדשות עירונית או דרך מערכות מידע עירוניות ומקומיות. מוכרזים: מתחמים לפינוי לשם בינוי שהוכרזו על ידי מנהל הרשות או שר הבינוי והשיכון, המקבלים קידום במוסדות תכנון והטבות מס. מקודמים ע"י גוף ציבורי / יזמים: מתחמים שנמצאים בשלבי תכנון או עמדו בתנאי סף לקליטה במוסדות התכנון. מתחם מועדף לדיור: מתחמים שהוכרזו על ידי הממשלה ומקודמים במסלול מהיר. בביצוע: מתח…
- AI overview sources: https://www.gov.il/he/pages/mitchamim · https://www.gov.il/apps/moch/viewlist/renew-cf/mitchamim-rashut · https://ksaba-minhelet.complot.co.il/מתחמי-התחדשות-עירונית/ · https://yehud-monosson.muni.il/pcat/מתחמי-התחדשות-עירונית/ · https://www.b-y.org.il/duplicated-1702993078/ · https://www.nzc.org.il/רשימת-מתחמי-התחדשות-עירונית-נס-ציונה/ · https://search.getstatus.online/he/magazine/urban-renewal-project-my-address

#### "מתחמי פינוי בינוי מאושרים" (desktop), retrieved 2026-10-25 19:22 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | www.barlev-nadlan.co.il | מסלול רשויות מקומיות | https://www.barlev-nadlan.co.il/התחדשות-העירונית/פינוי-בינוי-מדריך/מסלול-רשויות-מקומיות/ |
| 2 | www.lustigman.co.il | התחדשות עירונית | https://www.lustigman.co.il/urban-renewal |
| 3 | www.rashuiot.co.il | הרשות הממשלתית הכריזה על 10 מתחמי פינוי-בינוי חדשים | https://www.rashuiot.co.il/html5/arclookup.taf?&_id=67109&did=1118&title=����� �������� ������ … |
| 4 | www.amidor.co.il | מילון מושגים - התחדשות עירונית - עו"ד ... | https://www.amidor.co.il/dictionary-urban-renewal/ |
| 5 | www.hakablan.co.il | הוכרזו 24 מתחמי פינוי-בינוי חדשים: 3448 דירות ישנות ייהרסו ... | https://www.hakablan.co.il/חדשות/הוכרזו-24-מתחמי-פינוי-בינוי-חדשים-3448-דירו/ |
| 6 | hadashim.co.il | בדיקת סטטוס פינוי בינוי: איפה בודקים ומה זה אומר · חדשים | https://hadashim.co.il/urban-renewal-status/ |
| 7 | www.rashuiot.co.il | כ־15 אלף דירות חדשות: אושרו 24 מתחמי התחדשות עירונית ברחבי ... | https://www.rashuiot.co.il/html5/arclookup.taf?&_id=75819&did=1118&g=8701&title=��15 ��� ����� … |
| 8 | law.tau.ac.il | תכנית הקורס | https://law.tau.ac.il/sites/law.tau.ac.il/files/media_server/law_heb/hagar/images/Tel Aviv-Jaff… |
| 9 | www.barlev-nadlan.co.il | התחדשות בניינית: החלופה המקומית לתמ"א 38 | https://www.barlev-nadlan.co.il/התחדשות-העירונית/התחדשות-בניינית/ |
| 10 | nadlan.walla.co.il | בעיר שלכם? הוכרזו 12 מתחמי פינוי-בינוי חדשים, רובם במרכז - נדל״ן | https://nadlan.walla.co.il/item/3675358 |

- nad-lan.co.il in this SERP: not in top 20
- People also ask: absent
- Related searches: absent
- AI overview: present. Gist: הרשות הממשלתית להתחדשות עירונית הכריזה לאחרונה על סדרה של 24 מתחמי פינוי- בינוי חדשים ברחבי הארץ, ובהם פרויקטים בולטים במסלולי רשויות ומיסוי. אשקלון: מתחם בן גוריון (הריסת 425 דירות ישנות ובניית 2,660 דירות חדשות). ראשון לציון: מתחם מטרו מרכז (בניית 2,816 דירות חדשות במקום 905 ישנות). רמלה: מתחם שער צפון (צפוי להוסיף כ-2,000 דירות חדשות לעיר). ירושלים: מתחמי ברגר על הפארק (שכונת פת), חיים חביב (קריית היובל) ומתחם שלו…
- AI overview sources: https://www.rashuiot.co.il/html5/arclookup.taf?&_id=75819&did=1118&g=8701&title=��15 ��� ����� �����: ����� 24 ����� ������� ������� ����� ���� · https://www.hakablan.co.il/חדשות/הוכרזו-24-מתחמי-פינוי-בינוי-חדשים-3448-דירו/ · https://www.rashuiot.co.il/html5/arclookup.taf?&_id=67109&did=1118&title=����� �������� ������ �� 10 ����� �����-����� ����� · https://hadashim.co.il/urban-renewal-status/

#### "פרויקטים בהתחדשות עירונית" (desktop), retrieved 2026-10-25 19:22 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | pinuibinui.org.il | מפת האתר · החברה להתחדשות עירונית | https://pinuibinui.org.il/מפת-האתר/ |
| 2 | www.hagag-group.co.il | התחדשות עירונית בתל אביב - איכות חיים משודרגת - קבוצת חג'ג' | https://www.hagag-group.co.il/התחדשות_עירונית_בתל_אביב |
| 3 | www.dunietz-elad.co.il | התחדשות עירונית: מדריכים, פרויקטים ומידע לדיירים | https://www.dunietz-elad.co.il/category/renewal/ |
| 4 | gabaygroup.com | פרויקטי התחדשות עירונית ופינוי בינוי בהרצליה | https://gabaygroup.com/התחדשות-עירונית-בהרצליה/ |
| 5 | climaxgrp.co.il | התחדשות עירונית בישראל · מפת אזורי השקעה | https://climaxgrp.co.il/urban-renewal-map-israel-hot-investment-areas/ |
| 6 | ophirbuilding.com | קבוצת אופיר: עמוד ראשי | https://ophirbuilding.com/ |
| 7 | www.barlev-nadlan.co.il | מהי התחדשות עירונית | https://www.barlev-nadlan.co.il/התחדשות-העירונית/מהי-התחדשות-עירונית/ |
| 8 | amisafgroup.co.il | קבוצת עמיסף: עמוד בית | https://amisafgroup.co.il/ |
| 9 | paz-berger.co.il | קבוצת פז ברגר התחדשות עירונית | https://paz-berger.co.il/ |
| 10 | bsh.co.il | עידן התחדשות עירונית- ביצוע פרויקטים למגורים והתחדשות עירונית | https://bsh.co.il/ |

- nad-lan.co.il in this SERP: not in top 20
- People also ask: absent
- Related searches: התחדשות עירונית תל אביב מפה · מפת התחדשות עירונית פתח תקווה · בדיקת סטטוס פינוי בינוי פתח תקווה · מנהלת התחדשות עירונית תל אביב · שיכון ובינוי התחדשות עירונית · רשימת התחדשות פתח תקווה · פתח תקווה התחדשות עירונית · תכנית התחדשות בניינית פתח תקווה
- AI overview: present. Gist: פרויקט התחדשות עירונית הוא תהליך לחידוש ושידרוג של אזורים בנויים ותיקים באמצעות חיזוק ומיגון מבנים, שיפוץ תשתיות או הריסה ובנייה מחדש ( הרשות הממשלתית להתחדשות עירונית ). החייאת רקמה ותיקה: שיפור פני השכונות ושיקום מרכזי הערים. מיגון וחיזוק: הוספת ממ"דים (מרחב מוגן דירתי) ועמידות בפני רעידות אדמה ואיומים ביטחוניים. הגדלת היצע הדיור: הוספת יחידות דיור חדשות למשק. שדרוג סביבתי: פיתוח שטחים ירוקים, מוסדות ציבור ופתרונות…
- AI overview sources: https://www.gov.il/he/pages/about_urban_renewal · https://www.kolzchut.org.il/he/מדריך_לתהליך_התחדשות_עירונית · https://he.wikipedia.org/wiki/התחדשות_עירונית · https://shakedgroup.co.il/urban-renewal/ · https://auraisrael.co.il/התחדשות-עירונית/ · https://www.gov.il/he/pages/mitchamim · https://www.shapir.co.il/projects/נדלן/התחדשות-עירונית/ · https://building.org.il/articles/איך-להתניע-פרויקט-התחדשות-עירונית-ה/

#### "פרויקטים פינוי בינוי" (desktop), retrieved 2026-10-25 19:22 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | pinuibinui.org.il | מפת האתר · החברה להתחדשות עירונית | https://pinuibinui.org.il/מפת-האתר/ |
| 2 | www.africa-ur.co.il | פינוי בינוי תל אביב: להתחדש ולהישאר בעיר | https://www.africa-ur.co.il/pinuy-binuy-tel-aviv |
| 3 | www.kan-binuy.co.il | כאן בינוי - חדשנות עירונית | https://www.kan-binuy.co.il/ |
| 4 | www.hon.co.il | פינוי בינוי · כל מה שצריך לדעת - הון מדריכים פיננסים | https://www.hon.co.il/פינוי-בינוי-כל-מה-שצריך-לדעת/ |
| 5 | galim-ltd.com | סוגי מסלולים התחדשות עירונית | https://galim-ltd.com/סוגי-מסלולים-התחדשות-עירונית/ |
| 6 | nad-lan.co.il | מפת התחדשות עירונית: פרויקטים ומתחמי פינוי בינוי לפי עיר · נדלן | https://nad-lan.co.il/urban-renewal/map/ |
| 7 | city-buildrs.com | בוני העיר: בית | https://city-buildrs.com/ |
| 8 | manosgroup.co.il | פינוי בינוי - מאמרים · התחדשות עירונית · ניהול פרויקטים בבניה | https://manosgroup.co.il/blog/pinui-binui-articles/ |
| 9 | city-buildrs.com | בוני העיר: בית | https://city-buildrs.com/ |
| 10 | bashgroup.co.il | התחדשות עירונית בשרון · פרויקטים מתקדמים עם ... | https://bashgroup.co.il/התחדשות-עירונית-באזור-השרון/ |

- nad-lan.co.il in this SERP: #6
- People also ask: absent
- Related searches: פרויקטים פינוי בינוי ירושלים · פרויקטים פינוי בינוי תל אביב-יפו · מפת פינוי בינוי תל אביב · פינוי בינוי תל אביב פרויקטים · בדיקת סטטוס פינוי בינוי תל אביב · בדיקת סטטוס פינוי בינוי בת ים · הפקדת תכנית פינוי בינוי · מכפיל פינוי בינוי · פינוי בינוי תל אביב מפה · פרוייקטים בשיווק · אפריקה ישראל פרויקטים בשיווק
- AI overview: present. Gist: פרויקט פינוי בינוי הוא תהליך של התחדשות עירונית מתחמי שבו הורסים בניינים ישנים ובונים במקומם בניינים חדשים וצפופים יותר, לצד שדרוג תשתיות ושטחים ציבוריים. מידע מפורט על התהליך זמין באתר כל-זכות ובמדריך של מגדילים. תנאי סף: נדרשים בדרך כלל לפחות 24 יחידות דיור במתחם והכרזה רשמית. דרישות הסכמה: נדרש רוב של שני שלישים מבעלי הדירות כדי להתחיל בתהליך, ולקראת ביצוע נדרשת הסכמה של 100% או אישור מבית משפט במקרה של סירוב לא ס…
- AI overview sources: https://he.wikipedia.org/wiki/פינוי_בינוי · https://magdilim.co.il/180120260947/ · https://www.kolzchut.org.il/he/פינוי-בינוי · https://www.nadlancenter.co.il/article/565 · https://www.nadlancenter.co.il/article/4744 · https://pinuibinui.reisdor.co.il/

---

## 3. Competitor DNA (pages read in full, raw HTML)

Head-term counts are in the visible main text (raw HTML, nav/footer removed). "מפת התחדשות עירונית" = exact phrase.

### 3.1 netunim.co.il · `/nadlan/pinuy-binuy` (the closest data competitor)
- Seen at #14 to #16 for "מתחם/מתחמי פינוי בינוי" and "מתחם התחדשות עירונית" (desktop and phone).
- **Placement:** title "פינוי-בינוי: 970 מתחמי התחדשות עירונית לפי יישוב | נתונים" (57 chars). H1 "פינוי-בינוי, מתחמי התחדשות עירונית לפי יישוב". The first paragraph carries every head number. Counts: מתחמי 34 · התחדשות עירונית 14 · פינוי-בינוי 3 (always hyphenated, "פינוי בינוי" 0) · מפת התחדשות עירונית 0.
- **Structure:** answer paragraph (970 complexes, 76 localities, 150,202 existing and 614,837 proposed units, 55 "בביצוע", last declaration 11.6.2026, file updated 15.8.2026) · 4 stat tiles · status table (5 statuses) · "by locality" with 7 district H3s, one table each (locality, complexes, existing, proposed, in execution, last declaration) · "how to read the data" · FAQ (4) · source line with date.
- **Size:** 1,378 words · 8 tables · 510 cells · 469 figures · 15 headings · 2 visuals.
- **Tools:** none on the page. 76 locality pages (`/nadlan/pinuy-binuy/<city>`) with a map of complex boundaries, status and plan link.
- **Data:** only the data.gov.il file of 15.8.2026, numbers shown "as in the source", explicitly "we do not estimate when a project starts".
- **Schema:** Dataset, FAQPage, WebApplication, BreadcrumbList. dateModified 15.8.2026. 77 internal links, outbound data.gov.il.
- **Why it ranks:** the most complete structured rendering of the official file in plain HTML, the exact plural "מתחמי התחדשות עירונית" in title and H1, Dataset schema, a 76-page locality hub, an explicit method and honesty paragraph, and a domain that only does public data. It does **not** rank for the map query: the word "מפת" never appears.

### 3.2 dehaas.co.il · `/pinui-binui-by-city/` (the AI overview's source)
- Cited by the AI overview for "מתחמי פינוי בינוי" (desktop and phone); its sibling `/pinui-binui-by-city/yazamim/` is #2 for the same query.
- **Placement:** title "מתחמי פינוי בינוי לפי עיר - 970 מתחמים | דה האס" (47). H1 "מתחמי פינוי בינוי לפי עיר". מתחמי 80 · פינוי בינוי 3 · התחדשות עירונית 2.
- **Structure:** one answer paragraph with the national totals ("970 מתחמים ב-76 ערים, מהם 592 מוכרזים רשמית... מ-150,261 יחידות דיור קיימות ל-615,027 מוצעות, תוספת של כ-464,766") · one line on the three tracks · 76 city links with counts · disclaimer · links to the firm's guides (שקד, היטל השבחה). Law-firm lead form.
- **Size:** 395 words · 0 tables · 82 figures. Schema Article, Place, BreadcrumbList. dateModified **23.10.2026**.
- **Why it ranks:** exact-match title and H1, one dense answer sentence with the national totals and city ranking that the AI overview lifts almost word for word, a fresh modified date, and a hub of 76 city pages inside a law firm's renewal cluster.

### 3.3 hadashim.co.il · `/urban-renewal-status/`
- #6 for "מתחמי פינוי בינוי מאושרים", and an AI overview source there.
- **Placement:** title "בדיקת סטטוס פינוי בינוי: איפה בודקים ומה זה אומר | חדשים" (56). מתחם 21 · התחדשות עירונית 22 · פינוי בינוי 11 · מפת התחדשות עירונית 2.
- **Structure:** "בקצרה" · four steps (declared? plan status? permit? municipal administration?) · table "איפה בודקים מה" (what you want, where, what the answer says, what it does not say) · what to do when sources disagree · FAQ (5) · sources (gov.il, State Comptroller).
- **Size:** 1,557 words · 1 table · 20 cells · 6 FAQ · 2 official sources. Published and modified 21.10.2026.
- **Why it ranks:** fresh, method-first, a clear "where to check" table and official outbound links. It answers the step the AI overview ends with ("בדיקת סטטוס פרטני").

### 3.4 climaxgrp.co.il · `/urban-renewal-map-israel-hot-investment-areas/`
- In four Q1 SERPs (#5 "פרויקטים בהתחדשות עירונית", #11 "מתחם התחדשות עירונית", #12 "מתחמי התחדשות עירונית").
- **Placement:** title "התחדשות עירונית בישראל · מפת אזורי השקעה" (40). H1 "מפת ההתחדשות העירונית בישראל: אזורים חמים להשקעה". התחדשות עירונית 10 · מתחם 2.
- **Structure:** three regions (Gush Dan, Jerusalem and north, south), each with activity, transport, land prices, planning maturity · pros and cons table · FAQ (3, FAQPage schema) · six lead forms.
- **Size:** 2,188 words · 2 tables (36 cells) · 23 headings · 13 visuals · 0 official sources. Published 9.6.2026.
- **Why it ranks:** "מפת ההתחדשות העירונית" in the H1 plus length. Its numbers (for example a land price of "~349,000 ₪") carry no source.

### 3.5 upside.co.il · city analysis hub
- #11 for "מפת התחדשות עירונית" (desktop and phone).
- **Placement:** title "ניתוח מתחמי התחדשות עירונית לפי ערים - אפסייד השקעות נדל״ן" (58), three H1s.
- **Structure:** city buttons · featured complex cards, each linking to a per-complex analysis page ("מתחם פינוי-בינוי דגל ראובן, פתח תקווה") · "how we analyse potential" · lead form.
- **Size:** 417 words · 47 images (card photos) · 0 tables. Modified 18.10.2026.
- **Why it ranks:** a city and complex hub with investor framing and fresh dates.

### 3.6 gov.il, the authority (the #1 and the AI overview's main source)
- `topics/mapa-renewal` "מפת התחדשות עירונית בישראל": about 200 words, two links to the ArcGIS map app, a how-to paragraph, "המפה מתעדכנת מדי יום", and a disclaimer that data comes from developers and local authorities "ולכן לעיתים אין נתונים מלאים וייתכנו אי-דיוקים". The #1 result itself is the authority landing page.
- `pages/mitchamim` "מתחמי התחדשות עירונית" (updated 6.9.2026): defines the five complex types (declared under section 14, public body, developer past threshold, preferred housing complex, in execution) and links to the list app.
- **Why it ranks:** it is the source and the authority. **Weak spots:** the map is an old ArcGIS viewer, the list is a JavaScript app, no city summary in text, no history of changes, no plan dates in one place.

### 3.7 Also on page one (short)
- **meirim.org/plans** (#2 for the map query): a JavaScript plan search, 0 words in raw HTML; its description promises "שירות התראות על הגשת תבעות חדשות". Ranks on brand and the plan-search intent. Alerts exist for plans in general, not for renewal complexes.
- **mitar.co.il** "מה זה מתחם מוכרז לפינוי בינוי, ולמה הכרזה היא לא הבטחה" (#7 for "מתחמי פינוי בינוי"): 584 words, a "certainty ladder", FAQ. Definitional intent.
- **getstatus** (AI overview source for "מתחם התחדשות עירונית"): an address-check guide of about 2,200 words with a 7-question FAQ and a commercial address search behind sign-up (read through WebFetch, not saved as raw HTML).

---

## 4. Union checklist (everything any competitor has, plus what none has)

| Item | Who has it | We have it today |
|---|---|---|
| National totals in the first paragraph (complexes, cities, existing and proposed units) | netunim, dehaas, AI overview | partly (947, stale) |
| Ranked city list with counts | dehaas (76), netunim (76 in tables) | 12 cities in HTML, 76 only inside the map script |
| Table by status with units | netunim | no |
| Per-city table: complexes, existing, proposed, in execution, last declaration | netunim | no |
| Grouping by district | netunim | no |
| Three tracks explained (tax, authorities, not declared) | dehaas, netunim, gov.il | counts per city only |
| Five complex types (gov.il definitions) | gov.il, AI overview | no |
| "Declared is not a promise", certainty ladder | mitar, hadashim | no |
| Where to check status, step by step, with a table | hadashim, getstatus | no (links to our check page only) |
| Links to XPLAN / mavat / authority list | hadashim, gov.il, AI overview | per-complex pages only |
| Map of complex boundaries | netunim (per city), gov.il | no (one circle per city) |
| Per-complex pages | netunim, upside, gov.il app | yes (947 project pages) |
| Investor framing (regions, land prices) | climax, upside | no (and not needed) |
| FAQ visible | netunim 4, hadashim 5, climax 3, mitar | no (3 in schema only) |
| Dataset schema | netunim | yes |
| Method and honesty paragraph | netunim, hadashim | short disclaimer |
| Fresh date shown | dehaas 23.10, hadashim 21.10, upside 18.10 | 13.7.2026 data |
| **History: what changed since the last official update** | **nobody** | no |
| **Plan dates from XPLAN (deposit, approval publication) next to each complex** | **nobody** | no |
| **The authority's measured time from approval to first permit, next to each approved complex** | **nobody** | no |
| **Units multiplier (proposed ÷ existing) per complex and city, "מכפיל פינוי בינוי" is a related search** | **nobody** | no |
| **Declarations per year (trend)** | **nobody** | no |
| **Freshness against the authority's live map (999 complexes on 20.10.2026), not the 15.8 file (970)** | **nobody** (all competitors show 970) | no (947) |

---

## 5. Verified facts (for the spec; every number with its source and date)

| # | Fact | Source | Date / how |
|---|---|---|---|
| F1 | Official open file "מתחמי התחדשות עירונית" (Ministry of Construction and Housing): **970 complexes, 76 localities**, 150,202 existing units, 459,877 additional, 614,896 proposed | data.gov.il resource f65a0daf-f737-49c5-9424-d378d52104f5 (`datastore_search`, all rows) | file last_modified 15.8.2026 22:00 UTC; pulled 25.10.2026 (API) |
| F2 | Status in that file: תכנית מאושרת לפני מימוש 344 · תכנון סטטוטורי 282 · תכנית מאושרת אחרי רישוי 177 · תכנון ראשוני 111 · תכנית מאושרת במימוש 55 · one malformed row ("2025") | same | same |
| F3 | Units by status (existing → proposed): ראשוני 30,379 → 115,588 · סטטוטורי 46,343 → 196,665 · מאושרת לפני מימוש 46,996 → 192,279 · במימוש 12,310 → 54,506 · אחרי רישוי 14,174 → 55,799 | same, our sum | same |
| F4 | Track field: מיסוי 363 · רשויות 232 · טרם הוכרז 73 · empty 302. "בביצוע" = כן in 55 | same | same |
| F5 | Permits recorded (SachHeterim): 76,806 units in 232 complexes. Plan number in 934 rows, mavat link in 900, GovMap link in 970 | same | same |
| F6 | Top localities: ירושלים 213 · רמת גן 78 · תל אביב יפו 55 · חיפה 46 · נתניה 41 · בת ים 39 · פתח תקוה 37 · חולון 26 · הרצליה 24 · גבעתים 23 · חדרה 20 · ראשון לציון 19 | same | same |
| F7 | Declarations per year (TaarichHachraza): 2017 23 · 2018 23 · 2019 42 · 2020 37 · 2021 29 · 2022 32 · 2023 46 · **2024 103 · 2025 119** · 2026 30 (latest 11.6.2026) | same, our count | same |
| F8 | Units multiplier (proposed ÷ existing), our calculation: Israel 4.09 · ירושלים 4.23 · רמת גן 3.29 · תל אביב יפו 3.07 · חיפה 4.28 · נתניה 3.88 · בת ים 3.48 · פתח תקוה 3.57 · חולון 3.20 · הרצליה 3.31 · גבעתים 2.60 · חדרה 6.56 · ראשון לציון 3.22 · אשדוד 4.84 · רמלה 4.08 | same, our calc (label it "חישוב שלנו") | same |
| F9 | The authority's live map layer "מתחמי פינוי בינוי מוכרזים": **999 complexes, 79 localities**, 153,319 existing → 618,325 proposed. Stage code: 1 תכנון ראשוני 107 · 2 תכנון סטטוטורי 303 · 3 מאושרת לפני מימוש 348 · 4 במימוש 53 · empty 188. Track: מיסוי 553 · רשויות 241 · טרם הוכרז 205 | services6.arcgis.com/I08Ekaykft5ELucH/.../GIS_UrbanRenewal/FeatureServer/1 (feeds the gov.il map) | dataLastEditDate **20.10.2026 22:23 UTC**; pulled 25.10.2026 (API). **Reuse licence: the item's licence field is empty (unverified).** Reporting counts is fact reporting; republishing polygons needs a licence check |
| F10 | Between the 15.8.2026 file and the 20.10.2026 map: **36 complexes added** (14,399 proposed units; 15 not yet declared, 14 tax track, 7 authorities track; Jerusalem 5, Haifa 4), 14 no longer listed, **17 moved a stage** (10 statutory → approved, 6 preliminary → statutory, 1 approved → in implementation, for example כפר שלם, תל אביב) | F1 vs F9 joined on complex number, our calc | 25.10.2026 |
| F11 | Our site shows 947 complexes from data pulled 13.7.2026 (`/wp-json/nadlan/v1/renewal-map-data` total 947) | our REST, raw | 25.10.2026 |
| F12 | XPLAN gives per plan the stage and dates. Example 507-0590687 (נווה עופר, מתחם דש"א): deposited 20.12.2021, approval published 10.3.2024, "התכנית אושרה" | ags.iplan.gov.il/arcgisiplan/rest/services/PlanningPublic/Xplan/MapServer/1 | 25.10.2026 (API) |
| F13 | gov.il map page: "המפה מתעדכנת מדי יום"; data from developers and local authorities, may be incomplete or inaccurate | gov.il/he/departments/topics/mapa-renewal | read 25.10.2026 via reader proxy |
| F14 | Five complex types shown in the authority's list (declared under section 14 of the authority law; public body; developer past the planning threshold; preferred housing complex; in execution, with permits counted against proposed units) | gov.il/he/pages/mitchamim (updated 6.9.2026) | read 25.10.2026 via reader proxy |
| F15 | Required majority in pinui binui: 66% of owners in the complex and at least 60% in each building | gov.il/he/departments/faq/renewal_faq | prior, 3.10.2026 |
| F16 | A pinui binui complex: at least 24 existing units; in the new state at least 70 units or double, whichever is higher | Authority 2025 report, Annex A (PDF) | prior, 3.10.2026 |
| F17 | 2025: 186 pinui binui plans approved with 75,925 units (34% of all units approved); permits for about 29,000 units; renewal is 28% of construction starts; "כל דירה חמישית שנמכרה בשוק בשנת 2025" was in a renewal project; 77 new tax-track complexes with 28,771 new units | gov.il/he/pages/urban_renewal_report_2025 and PDF p.68 | prior, 3.10.2026 |
| F18 | Average years from plan approval to the first building permit in pinui binui, by permit year (complexes): 2025 4.0 (28) · 2024 4.0 (43) · 2023 3.9 (28) · 2022 4.1 (33) · 2021 4.9 (23) · 2016 6.0 (7) | 2025 report PDF p.87 | prior, 3.10.2026 |
| F19 | 51 municipal renewal administrations operate | 2025 report | prior, 3.10.2026 |
| F20 | data.gov.il licence allows commercial use with attribution, not in a misleading way or as if the state endorses it | data.gov.il/he/terms-of-use | prior, 3.10.2026 |

**Unverified, kept out of the spec:** getstatus's statutory maximum timeframes (18 / 24 / 48 months), "592 officially declared" (dehaas; the file's empty track field makes the declared count ambiguous: tax + authorities = 595 in the file, 794 on the map), CitySquare and climax numbers, any "expected occupancy" year.

---

## 6. Our page as Google gets it (raw HTML, `?x=` cache-buster, 25.10.2026)

- **Title:** "מפת התחדשות עירונית: פרויקטים ומתחמי פינוי בינוי לפי עיר | נדלן" (63 chars, over 60).
- **H1:** "מפת ההתחדשות העירונית: כל פרויקטי פינוי בינוי בישראל" (the exact phrase "מפת התחדשות עירונית" is not in the H1 or anywhere in the body; 0 occurrences).
- **Answer paragraph:** "ריכוזי המתחמים המוכרזים לפי עיר, מתוך המאגר הרשמי של הרשות... הקישו על עיר לרשימת המתחמים שלה." Then: data "כפי שנמשך ב-13.7.2026" and "מיקום מדויק לכל מתחם יתווסף בהמשך" (a future promise; language DNA forbids promise copy).
- **Sections:** one H2 "מתחמי התחדשות עירונית בישראל לפי עיר", 12 city H3 cards (4 complexes each and "ועוד N"), links to the guide, the free building check, pinui binui, tama 38, the private project room, disclaimer.
- **Tools:** Mapbox map with one circle per city (76 cities, 947 complexes, from `renewal-map-data`), city click opens the list; the lookup `renewal-lookup` (city + street).
- **Numbers:** 947 complexes, 594 declared, per-city counts by track. **No table.**
- **FAQ:** 3 questions in FAQPage schema only, **not visible** on the page.
- **Schema:** WebPage, FAQPage, Dataset (license data.gov.il terms), ItemList (12 cities). dateModified 6.10.2026.
- **Size:** 618 words · 86 figures · 0 tables · 13 headings · 0 visuals in HTML · 0 official outbound links.

### Our gaps (ordered)
1. **Stale data**: 947 complexes from 13.7.2026, while every competitor shows 970 (15.8) and the authority map shows 999 (20.10). We are 52 complexes and 17 stage moves behind the source.
2. **Head term placement**: "מפת התחדשות עירונית" is in the title only; 0 in H1 and body. "מתחמי פינוי בינוי" is not in the H1.
3. **No tables** (netunim: 8 tables, 510 cells).
4. **FAQ hidden** (schema without visible questions; a mismatch Google can ignore or penalise).
5. **Thin text**: 618 words vs 1,378 to 2,188 for the text competitors.
6. **Only 12 of 76 cities in HTML**; the rest exist only inside the map script.
7. **Map at city level** with a future promise in the copy.
8. **No official outbound sources** (0; hadashim 2, netunim 1).
9. **No status, approved, or in-execution views**, although "מתחמי פינוי בינוי מאושרים" and "פרויקטים בשלבי בנייה" are live queries.
10. **Title 63 chars.**

---

## 7. BUILD SPEC

### 7.1 Keep (additive law: nothing removed)
Mapbox map and city click lists · the `renewal-lookup` search · the 12 city cards (become part of the full city table, cards stay as the visual for the top 12) · links to the guide, `/urban-renewal/check/`, pinui binui, tama 38 and alternatives, `/my-renewal/` · the disclaimer · Dataset, FAQPage and ItemList schema (ItemList grows to all cities) · the 947 project pages and their links.

### 7.2 Title (≤60)
`מפת התחדשות עירונית: 999 מתחמי פינוי בינוי לפי עיר | נדלן` (57 chars)
The number is filled at build time from the source used (999 = authority map 20.10.2026; if only the open file is used, 970). Fallback without a number: `מפת התחדשות עירונית: מתחמי ופרויקטי פינוי בינוי לפי עיר` (55).

### 7.3 H1
`מפת התחדשות עירונית: מתחמים ופרויקטים של פינוי בינוי בכל עיר` (60 chars)

### 7.4 Answer paragraph (53 words; first sentence holds the head term)
> מפת התחדשות עירונית של נדלן מציגה את כל 999 מתחמי הפינוי בינוי שהרשות הממשלתית להתחדשות עירונית מפרסמת ב-79 ערים, לפי שלב: תכנון ראשוני, תכנון סטטוטורי, תכנית מאושרת ובביצוע. לכל מתחם מספר התכנית, כמה דירות יש בו היום וכמה יהיו אחרי הבנייה, ומה השתנה בו מאז הבדיקה הקודמת. הנתונים נבדקו מול מפת הרשות ב-20.10.2026.

(Numbers and date are variables from the build data. Remove "מיקום מדויק לכל מתחם יתווסף בהמשך" once points are on the map; until then say what the map shows today, never what it will show.)

### 7.5 Section order (rendered order, phones first: H1 → answer → CTAs → stage → facts → article)
1. H1 + answer paragraph.
2. CTAs (two buttons): `חפשו את הבניין שלכם במאגר` (scrolls to the lookup) · `בדיקת בניין חינמית` (→ /urban-renewal/check/). Sitewide WhatsApp bar unchanged.
3. **The map** (kept), upgraded: one point per complex from the official coordinates (the 3.10 research found 872 unique points; complexes still on a city centre or 0,0 stay in the city circle and are labelled "מיקום לפי עיר"), colour by stage, filter chips for the four stages and "בביצוע".
4. **Four stat tiles**: מתחמים · ערים · דירות היום → אחרי הבנייה · מתחמים בביצוע (F1/F9 with date).
5. **The moat: "מה זז במאגר"** (7.8): the latest changes table plus the complex tracker search.
6. H2 `מתחמי פינוי בינוי לפי שלב`: status table T1 + funnel infographic I1.
7. H2 `מתחמי פינוי בינוי מאושרים`: table T3 (approved complexes, sortable, by city).
8. H2 `פרויקטי פינוי בינוי בביצוע`: table T4 (complexes marked in execution or with permits).
9. H2 `מפת התחדשות עירונית לפי עיר`: full city table T2 grouped by district (H3 per district), the 12 city cards above it.
10. H2 `מה זה מתחם התחדשות עירונית`: the five types (F14), tax vs authorities track, "הכרזה היא לא תכנית מאושרת" (certainty ladder in plain words).
11. H2 `כמה זמן עובר מאישור התכנית ועד היתר`: table T5 (F18) + the stage dictionary T6.
12. H2 `כמה מתחמים הוכרזו בכל שנה`: infographic I2 (F7).
13. H2 `איך בודקים סטטוס של מתחם`: four steps with official links (our lookup → authority list → XPLAN by plan number → municipal administration) and table T7 "איפה בודקים מה".
14. H2 per GSC city (H3 each, a mini table and a link to the city's project page): ראשון לציון · תל אביב יפו · ירושלים · רמת גן · פתח תקווה · חולון · בת ים · נתניה · חדרה · באר שבע.
15. H2 `שאלות נפוצות על מפת ההתחדשות העירונית`: visible FAQ (7.9), the same list in FAQPage schema.
16. H2 `איך נאסף המידע`: sources, dates, what the data does not say (no start or occupancy dates), disclaimer, the internal links block.

### 7.6 Tables (each with its real data source)
| ID | Table | Columns | Source |
|---|---|---|---|
| T1 | מתחמים לפי שלב | שלב · מתחמים · דירות היום · דירות אחרי הבנייה | F2/F3 (data.gov.il 15.8.2026) and the stage counts from the authority map (F9) with its date, side by side until the open file catches up |
| T2 | כל הערים (76 to 79 rows, grouped by district) | עיר · מתחמים · מאושרים · בביצוע · מסלול מיסוי · מסלול רשויות · טרם הוכרז · דירות היום · דירות אחרי הבנייה · מכפיל · הכרזה אחרונה | F1/F4/F7/F8 per city; district from the CBS localities list on data.gov.il (confirm the district field at build) |
| T3 | מתחמים מאושרים | מתחם · עיר · שלב · מספר תכנית (mavat link) · תאריך פרסום אישור (XPLAN) · דירות היום → אחרי | F1 status "תכנית מאושרת…" (576 complexes, 302,584 proposed units) + F12 |
| T4 | מתחמים בביצוע | מתחם · עיר · היתרים שניתנו (יח"ד) · מתוך יח"ד מוצעות | F1 Bebitzua + SachHeterim (55 marked, 232 with permits) |
| T5 | מאישור תכנית עד היתר ראשון | שנת ההיתר · שנים בממוצע · מתחמים | F18 (2025 report p.87) |
| T6 | מילון השלבים | שלב אצל הרשות · השלב ב-XPLAN · מה זה אומר · מה בדרך כלל הצעד הבא | F2, F12 stage vocabulary (prior competitors.md section א3) |
| T7 | איפה בודקים מה | מה רוצים לדעת · איפה · מה התשובה אומרת · מה היא לא אומרת | gov.il list, XPLAN, mavat, municipal administrations (F13, F14, F19) |
| T8 | מה זז במאגר | מתחם · עיר · מה השתנה (נוסף / עלה שלב / ירד מהרשימה) · משלב → לשלב · תאריך הבדיקה | F10, then every snapshot |

### 7.7 Infographics (2 to 3)
- **I1 Stage funnel**: five horizontal bars (complexes) with the proposed units printed on each bar; source line with date. Data F2/F3.
- **I2 Declarations per year**, 2000 to 2026: vertical bars, the 2024 (103) and 2025 (119) bars labelled; note that 2026 is partial (to 11.6.2026). Data F7.
- **I3 Top 15 cities, today vs after building**: paired horizontal bars (existing, proposed) with the multiplier at the end of each row ("× 4.23"). Data F1/F8.
Design note for the builder: palette from planning documents (plan-blue lines, approval green, deposit amber on a white sheet), Hebrew face chosen on purpose (for example Heebo or Assistant for data, a sturdier display face for H2), not the cream or brass default.

### 7.8 THE MOAT: "יומן המתחמים" (official stage tracker with history)
- **What it is:** for every complex, the official stage today **and what changed since the last official update**, with the plan's own dates. Nobody in the SERP stores history: gov.il shows only the current state, netunim and dehaas show the 15.8 file, meirim alerts on plans in general.
- **Inputs:** city, complex name or street (free text, with spelling normalisation: גבעתיים/גבעתים, פתח תקווה/פתח תקוה, the 3.10 research found the lookup missing these), or a plan number.
- **Output (one card per complex):** שלב אצל הרשות + מסלול · מספר תכנית + קישור ל-mavat · תאריך הפקדה ותאריך פרסום אישור (XPLAN) · "עברו X שנים מאישור התכנית; בממוצע עוברות 4.0 שנים עד היתר ראשון (הרשות, 2025)" (shown only for approved plans, worded as an average, never as a forecast) · דירות היום → אחרי הבנייה + מכפיל · היתרים שניתנו · "מופיע במאגר מאז" and the list of stage changes with dates. Page level: the "מה זז במאגר" table T8 and a count line ("מאז 15.8.2026 נוספו 36 מתחמים ו-17 עלו שלב").
- **Data:** data.gov.il file (F1, licence cleared) · the authority's map layer (F9, freshest; confirm reuse before republishing polygons, counts and stages are fact reporting) · XPLAN by plan number (F12) · snapshots stored by us: 13.7.2026 (site import), 15.8.2026 (file), 20.10.2026 (map), then weekly.
- **Why it compounds:** every week adds history nobody else kept; it feeds the 947 project pages (a "מה השתנה" line on each) and gives the private project room an alert trigger.
- **Honesty rules:** never an occupancy or start year; "תאריך הבדיקה" on every change; when two sources disagree, show both with dates.

### 7.9 FAQ (20 questions in searchers' words; PAA is absent, so wording comes from related searches, people also search, the AI overview sub-topics and GSC)
1. איפה רואים את מפת ההתחדשות העירונית הרשמית?
2. איך בודקים אם הבניין שלי נמצא במתחם פינוי בינוי?
3. מה זה מתחם התחדשות עירונית מוכרז?
4. מה ההבדל בין מסלול מיסוי למסלול רשויות?
5. מה ההבדל בין הכרזה על מתחם לבין תכנית מאושרת?
6. אילו מתחמי פינוי בינוי מאושרים יש בעיר שלי?
7. איזה פרויקטים של פינוי בינוי כבר בשלבי בנייה?
8. כמה זמן עובר מאישור התכנית ועד היתר בנייה?
9. מה אומר כל שלב: תכנון ראשוני, תכנון סטטוטורי, תכנית מאושרת?
10. מה זה מכפיל בפינוי בינוי?
11. כמה בעלי דירות צריכים להסכים לפינוי בינוי?
12. כמה דירות צריך כדי שבניין ייכנס למתחם פינוי בינוי?
13. למה המתחם שלי לא מופיע במפה?
14. האם פרויקטים של תמ"א 38 מופיעים במפה?
15. כל כמה זמן מתעדכנת מפת ההתחדשות העירונית?
16. איך מוצאים תכנית לפי גוש וחלקה או לפי כתובת?
17. מה זה מתחם מועדף לדיור (ותמ"ל) ובמה הוא שונה מפינוי בינוי?
18. מה זו מינהלת התחדשות עירונית ואיפה יש כזו?
19. כמה מתחמי פינוי בינוי יש בירושלים, בתל אביב ובראשון לציון?
20. כמה מתחמים חדשים הוכרזו בשנה האחרונה?
Answers: 2 to 4 sentences each, numbers only from section 5 with their date, an official link where one exists (authority list, XPLAN, mavat, renewal_faq). Q14: say plainly that the file lists complexes and tama 38 is not in it. Q17: only what F14 says.

### 7.10 Honesty target (from `proof-before.md`, raw HTML counts, 25.10.2026 21:32)
| Metric | Ours now | Best competitor (who) | All six competitors combined | Target after build |
|---|---|---|---|---|
| words | 618 | 2,188 (climax) | 6,519 | ≥ 2,500 (beat the best; combined is not a quality goal) |
| figures | 86 | 469 (netunim) | 697 | ≥ 800 (T2 alone gives about 800) |
| tables | 0 | 8 (netunim) | 11 | ≥ 12 (T1 to T8, T2 split into 7 district tables) |
| cells | 0 | 510 (netunim) | 566 | ≥ 900 |
| tools | 0 in raw count (map and lookup are scripts) | 0 | 0 | 2 counted (lookup form, tracker form) |
| faq | 3 (schema only) | 6 (hadashim) | 13 | 20 visible = 20 in schema |
| headings | 13 | 23 (climax) | 75 | ≥ 30 |
| visuals | 0 | 47 (upside, card photos) | 66 | ≥ 6 real charts and maps (we do not chase upside's photo count; the honesty statement names it) |
| official sources | 0 | 2 (hadashim) | 3 | ≥ 6 (data.gov.il, gov.il map, gov.il mitchamim, renewal_faq, XPLAN, the 2025 report) |
| freshness | data 13.7.2026 | 23.10.2026 (dehaas page date); data 15.8.2026 for all | | map data 20.10.2026 or newer, date on the page |

Honesty statement for the page bottom, once the targets are met (plain Hebrew, only true lines): which sources, which dates, what we do not know (start and occupancy dates), and the one metric where a competitor still leads (photos).
