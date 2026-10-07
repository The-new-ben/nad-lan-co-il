# /north-tel-aviv/ (page 4866): number audit and alignment edits (HAD-460 Stage A, 7.10.2026)

Companion to align-edits.json in this folder. Data only: nothing was applied, nothing published, nothing committed.
The hub had never been audited. Every number in its body was checked against the repo's facts and public sources.

## 1. Method

- Content: public `GET https://nad-lan.co.il/wp-json/wp/v2/pages/4866?_fields=id,link,title,content,yoast_head_json,modified_gmt`
  (content.rendered), retrieved 2026-10-07 10:39:51 UTC (page modified_gmt 2026-10-07 08:18:10, the guides paragraph added
  by another session). Saved: `source/hub-4866-rest.json`. Live H1 (theme, from the title): "צפון תל אביב - מדריך האזור,
  השכונות, הפרויקטים והמחירים"; 12 H2s.
- Every number token in the visible body was extracted by script (58 tokens before the edits), grouped into 13 distinct number
  claims, and each claim was checked against: the repo (sde-dov-prices.json sources, docs/research/2026-10-07-city-prices,
  docs/content/rova-4-2026-10/facts.md, the site's own Einstein dossier at /projects/einstein-tower/) and public sources opened
  today (section 3, with retrieval times).
- 22 edits. A script applied them in order to the saved content.rendered: each "old" matches exactly once and still once after
  the earlier edits; all 22 also match exactly once in the raw post content backed up by the 08:18 session
  (`docs/qa/had-460/align-backup/page-4866-20261007T111809.json`). No new text has an em dash, an en dash, "!" or an HTML
  entity. Result after the edits: `source/hub-4866-after-edits.html`.
- Not edited: the title, the H1, the URL, every H2 and H3 (none carries a number), the Yoast title and description.
- After the edits the translation gate (`check_translation.py --selftest`) finds **88 number tokens, 0 unmatched** on the hub
  (and 502 tokens, 0 unmatched, on Rova 4). Before the edits the same gate finds 17 tokens that no source supports (30, 40,
  13,500, 60,000, 95,000; listed in section 5).

## 2. Counts

| | distinct claims | occurrences |
|---|---:|---:|
| number claims in the body before the edits | 13 | 39 |
| CONSISTENT (kept; one gets its date, one gets its attribution fixed) | 5 | 15 |
| CONFLICT with a dated source | 4 | 16 |
| STALE (superseded or old date) | 3 | 6 |
| UNSOURCED | 1 | 2 |
| **unsourced numbers after the edits** | **0** | **0** |

Edits by verdict: 9 CONFLICT, 2 UNSOURCED, 1 STALE, 1 CONSISTENT+DATE, 2 DATE (footer, JSON-LD), 6 ADDED (optional: official
numbers in the prices table, which had none), plus 1 row label (the Einstein row now names the complex).

### The top conflicts

1. **EINSTEIN TOWER "כ-515 דירות"** (card, paragraph, table, FAQ). 515 apartments is Hagag's WHOLE Einstein complex: six
   residential buildings, 515 units, a shopping centre of about 11,400 m², a public building of about 3,950 m², 957 parking
   spaces, value about ₪4 billion (NC2601, 20.1.2026). EINSTEIN TOWER itself: 215 apartments in a 28-floor tower and two
   13-floor buildings over a commercial base (Hagag 2025 annual report and permit 20241734 of 9.7.2026, both in the site's own
   dossier). The site already fixed "515" to 215 on the project page on 14.8.2026; the hub still said 515.
2. **Neve Avivim "כ-40 פרויקטי תמ״א 38"** (5 places). The source of "about 40 projects" (12-13.1.2025) is about **Neot Afeka
   B**, not Neve Avivim. Replaced by a dated Neve Avivim plan: Yehuda HaNasi, approved 2023, 5 buildings / 80 apartments ->
   3 buildings of up to 14 floors / 195 apartments (NC2308).
3. **Ramat Aviv Gimel "בנייה חדשה כ-60,000 עד 95,000 ש״ח למ״ר"** ("הנתון שסופק"): no source. The published figures are about
   ₪51,000-53,000 per m² on average (2.8.2026) and older 1990s buildings at 40-43K (6.6.2026). Replaced by the official Q1
   2026 medians and three dated per-m² levels.
4. **"שני מגדלים בני 30 ו-28 קומות ושני בניינים בני 14 קומות"** mixes two projects and two dates (10.2024: 30 + 28 floors and
   FOUR buildings of 14; 3.2024: 30 and 33-floor towers, two of 13 and two of 14). The new text gives the complex without floor
   counts and EINSTEIN TOWER with the floors of its 2026 permit.
5. **13,500 m² of commerce** (4 places, 10.2024) is superseded by about 11,400 m² (1.2026).

## 3. Source keys

| key | source | date | read (UTC, 7.10.2026) | says |
|---|---|---|---|---|
| TLVSD | Tel Aviv-Yafo municipality, Sde Dov page https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx (via docs/content/ashira/00-source-ledger.md) | plan TA/4444 | read 5.8.2026 by the Ashira session, not re-read | about 16,000 planned homes, about 40,000 residents |
| NC2604 | https://www.nadlancenter.co.il/article/14303 (sde-dov-prices.json) | 15.4.2026 | 09:46 (Sde Dov session) | "about 1,280 sold out of about 16,000 planned" |
| NC2601 | https://www.nadlancenter.co.il/article/13735 | 20.1.2026 | about 10:47 | Hagag Einstein projects: six residential buildings, 515 units, shopping centre 11,400 m², public building about 3,950 m², 957 parking spaces, total value about ₪4 billion, bridge loans about ₪540M |
| NC2410 | https://www.nadlancenter.co.il/article/10799 | 15.10.2024 | about 10:46 | Einstein 33-35: a 30-floor and a 28-floor tower, 4 buildings of 14 floors, about 515 units, about 13,500 m² commerce, architect Moshe Tzur |
| NC2403 | https://www.nadlancenter.co.il/article/9639 | 27.3.2024 | about 10:46 | 215 units in a 30-floor tower + two 13-floor buildings, about 4,500 m² commerce; Einstein 35: 300 units in a 33-floor tower, two 14-floor buildings, 9,000 m² commerce |
| DOS | the site's dossier https://nad-lan.co.il/projects/einstein-tower/ (sources S001 Hagag project page 14.8.2026, S002 Hagag 2025 annual report, IVS008 permit 20241734 of 9.7.2026, S009 NTA Green Line) | 31.12.2025 / 9.7.2026 | 10:44 | EINSTEIN TOWER: 215 units, a 28-floor tower and two 13-floor buildings over a two-level commercial base; Moshe Tzur Architects; company completion estimate Q3 2030; Einstein and Levi Eshkol are future Green Line stations |
| NC2308 | https://www.nadlancenter.co.il/article/8139 | 2.8.2023 | about 10:48 | Neve Avivim, Yehuda HaNasi 14-22: plan approved; 5 buildings with 80 apartments -> 3 buildings of up to 14 floors, 195 apartments (80 to residents, 115 to the developers, 20 affordable) |
| NC2501 | https://www.nadlancenter.co.il/article/11343 | 12.1.2025 | about 10:48 | Neot Afeka B: over 20 permit requests in 2024, "half of the projects promoted in the neighbourhood, about 40" |
| ICE2501 | https://www.ice.co.il/realestate/news/article/1046703 | 13.1.2025 | about 10:47 | the same, Neot Afeka B (Neve Avivim only as a neighbour) |
| HEWNA | https://he.wikipedia.org/wiki/נווה_אביבים (last edited 7.10.2026 03:13) | live | about 10:49 | first houses mid-1960s, most of the neighbourhood in the 1970s, last houses mid-1990s; about 776 dunam |
| ICE2107 | https://www.ice.co.il/realestate/news/article/825174 | 8.7.2021 | about 10:50 | Ashdar Einstein: three 8-floor buildings, 45 apartments of 3-4 rooms plus penthouses; occupancy in about three years |
| GOVN | data.nadlan.gov.il neighbourhood and city files (Last-Modified 20.8.2026), via docs/research/2026-10-07-city-prices/neighbourhoods-all.csv | Q1 2026 (1-3.2026) | 08:49 (city-prices session) | 4-room medians: נווה אביבים וסביבתה 5,370,100; בבלי 6,549,400; תכנית ל 8,425,800; הצפון הישן, החלק הצפוני 6,542,100; Tel Aviv-Yafo 5,229,800 |
| ICE0606 | https://www.ice.co.il/realestate/news/article/1114418 | 6.6.2026 | about 10:49 (and 09:50 by the Sde Dov session) | Ramat Aviv recent deals average about 55K/m²; Ramat Aviv Gimel 1990s buildings 40-43K; a new apartment in a new Sde Dov project about 70-71K |
| BZ2608 | https://www.bizportal.co.il/realestates/news/article/20036053 | 2.8.2026 | about 10:49 | Ramat Aviv Gimel average about 51-53K/m², down about 10% in a year |
| ICE2105 | https://www.ice.co.il/realestate/news/article/1112481 (sde-dov-prices.json) | 21.5.2026 | 09:46 (Sde Dov session) | most Sde Dov projects around 70K/m² |
| THIS | this edit set | 7.10.2026 | | the page is updated by it |

## 4. Every number claim in the hub, with its verdict (audit ids A-1 to A-13; not the claims.json ids)

| # | claim (Hebrew as on the page) | where (occurrences) | verdict | source | edit |
|---|---|---|---|---|---|
| A-1 | רובע שדה דב מתוכנן לכ-16,000 דירות | opening, neighbourhoods, renewal table, prices table, comparison table, transport, FAQ (7) | CONSISTENT | TLVSD, NC2604 | none |
| A-2 | EINSTEIN TOWER כולל כ-515 דירות | card, paragraph, renewal table, FAQ (4) | CONFLICT (515 = the complex; the tower = 215) | NC2601, DOS | 1, 3, 6, 20 |
| A-3 | מגדלים עד 30 קומות / שני מגדלים בני 30 ו-28 קומות | card, paragraph, table, FAQ (4) | CONFLICT (sources disagree; the 2026 permit: one 28-floor tower) | DOS, NC2410, NC2403 | 1, 3, 6, 20 |
| A-4 | שני בניינים בני 14 קומות | paragraph, table, FAQ (3) | CONFLICT (complex: 4 of 14 in 2024; the tower: two of 13) | DOS, NC2410 | 3, 6, 20 |
| A-5 | 13,500 מ״ר מסחר | paragraph, table, legal, FAQ (4) | STALE (10.2024; 11,400 m² in 1.2026) | NC2601 | 3, 6, 18, 20 |
| A-6 | השווי המוערך של הפרויקט כ-4 מיליארד ש״ח | paragraph (1) | CONSISTENT, re-attributed to the complex | NC2601 | 3 |
| A-7 | אשדר איינשטיין: שלושה בניינים בני 8 קומות | paragraph, table (2) | CONSISTENT | ICE2107 | 4 (adds the year, 2021) |
| A-8 | אשדר איינשטיין: כ-45 דירות | paragraph, table (2) | CONSISTENT | ICE2107 | 4 |
| A-9 | נווה אביבים הוקמה בשנות ה-60 וה-70 | paragraph, prices table, FAQ (3) | CONSISTENT | HEWNA | none |
| A-10 | בנווה אביבים מקודמים כ-40 פרויקטי תמ״א 38 | paragraph, renewal table, prices table, comparison table, FAQ (5) | CONFLICT (the 40 is Neot Afeka B) | NC2501, ICE2501; replacement NC2308 | 2, 7, 10, 17, 19 |
| A-11 | בנייה חדשה ברמת אביב ג׳ כ-60,000 עד 95,000 ש״ח למ״ר | prices paragraph, prices table (2) | UNSOURCED | replacement GOVN, ICE0606, BZ2608, ICE2105 | 8, 9 |
| A-12 | עודכן יוני 2026 | footer (1) | STALE | THIS | 21 |
| A-13 | "dateModified":"2026-06-15" (JSON-LD, not visible) | head of the content (1) | STALE | THIS | 22 (optional) |

Numbers that are names, not claims: תמ״א 38, רובע 3 / רובע 4 (the guides paragraph), רמת אביב א/ב/ג (letters).
Non-number facts read on the way: the architect Moshe Tzur (CONSISTENT, DOS/NC2410); "the Green Line ... with an Einstein
station" (CONSISTENT as a future station, DOS S009).

## 5. Before and after (the translation gate on the Hebrew)

- Before the edits: 58 number tokens, 17 with no supporting claim: 30 (x4), 40 (x5), 13,500 (x4), 60,000 (x2), 95,000 (x2).
  The gate cannot see a wrong attribution (515 and 4 billion are true numbers of the complex): the audit above did.
- After the edits: 88 tokens, 0 unmatched; H1 1; banned 0; external links 0; heading duplicates 0 (compared live with
  /new-projects/, /guides/, /brokers/, /developer-deals/, /projects/hamedina/ and /north-tel-aviv/rova-4/).
- Soft style words left in the Hebrew (warnings, not edited, outside this task): "יחסית" and "כמעט" (6 on the hub).

## 6. Found but not edited (outside a number audit; for the owner or a later edit)

- The closing line "מקורות לעיון: עיריית תל אביב-יפו, רשות מקרקעי ישראל, נת״ע, פרסומי יזמים" names sources in the body, against
  the owner's 1.10.2026 rule for articles. The translations leave it out; the Hebrew could drop it.
- The hub still treats TAMA 38 as an active track ("פרויקטי תמ״א 38 נקודתיים"); TAMA 38 has ended in Tel Aviv and the quarter
  plans replaced it (the Rova 4 page explains this). Worth a wording pass.
- The hub never names the New North / Rova 4 or Kikar HaMedina in its own text (only in the guides line added today). A short
  paragraph linking to /north-tel-aviv/rova-4/ would give the new page an internal link from the hub's body (a content
  addition: the CEO's call).
- Language-law words in the Hebrew: "שכבה" (four times, "the layers of renewal"), "יחסית"/"יחסי". Not numbers; not edited.
- The H1 uses a spaced hyphen ("צפון תל אביב - מדריך האזור..."); the site's language law prefers a colon. Not edited (task rule).

## 7. Apply notes

- Order: 1 to 22. Edits 11-16 and 22 are optional and independent of the others.
- Re-fetch the page and re-check every "old" right before applying (another session edited this page today).
- After applying: re-fetch, run `python tools/source_audit.py` on /north-tel-aviv/ (public-source law), run
  `python docs/content/north-tel-aviv-2026-10/check_translation.py --selftest --live` (expect PASS), and confirm the H1 and the
  12 H2s are unchanged.
- The language versions must be built from the Hebrew AFTER these edits (the packets already are: build_packets.py applies
  align-edits.json in memory).
