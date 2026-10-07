# City price pages: body text aligned with the official price list (7.10.2026)

DATA ONLY. Nothing here was applied: no WordPress write, no commit, no push. Each `<slug>.align-edits.json` holds the audit
(claims inventory) and the proposed edits for one page, in the schema of `docs/content/sde-dov-prices-2026-10/align-edits.json`.

## Why

Every Hebrew city price page now shows an official price list (`<section id="nlpg">`, shortcode `[nadlan_price_guide]`), built from
the Tax Authority deal medians on data.nadlan.gov.il and stored in `scripts/project-stage/price_guide/cities/<slug>.json`. The older
article text on the same page carried its own prices (asking-price "working ranges", portal averages, 2023 neighbourhood averages,
street averages), so a reader saw two different prices for the same flat. The edits replace or remove every body figure that
contradicts the list or has no dated source, and keep the rest.

## What was audited

- 24 pages: the 23 city pages of `price_guide/cities/` and the national hub `/apartment-prices/`.
- Source: public `GET /wp-json/wp/v2/pages?slug=<slug>&_fields=id,link,title,content,modified` (content.rendered), retrieved
  7.10.2026 10:34 UTC. The price list section, `<script>` and `<style>` are outside the audit; the byline, H1 and titles were not edited.
- Facts: the city JSON files (official settlement and neighbourhood files, version 20.8.2026; data quarter 1-3.2026, the national
  file 4-6.2026). `source_keys` in every edit are JSON paths in that file (`rooms.4.latest`, `rooms.3.quarters[10-12.2025]`,
  `neighbourhoods[אפרידר].rooms.4`, `cities[<slug>].rooms.3.latest`); `page` marks a figure kept from the page itself.
- While the audit ran, the price list was added to the other 11 pages and to the hub (modified 7.10.2026 13:46-13:47 site time,
  10:46-10:47 UTC). Re-fetched at 11:17-11:20 UTC: the text outside the list is identical to the audited copy (only blank lines around
  the inserted list), so the audit stands. Each JSON records this under `live_recheck`.

## Rules used

A claim is one statement (a sentence or a table row) with one or more figures of one kind; `figures` counts the numbers in it.

- **CONSISTENT**: the official figure for the same rooms (and the same period, if the claim names one) lies inside the stated range
  (official within low x 0.99 to high x 1.01); a point figure ("כ-X", "סביב X", "ממוצע X") within 5%; a floor ("מ-X") at or below the
  official figure; a ceiling ("עד X") at or above it. A city average of all flats is compared with the all-rooms median.
- **CONFLICT**: the same measure, outside that tolerance. Every city-level sale figure for a 3, 4 or 5-room flat was compared with the
  official median whatever its label (asking price, working range, anchor, second-hand, new, a portal figure with a date).
- **STALE**: an older period presented as the current level (2023 neighbourhood deals, multi-year averages, 2025 deals called recent).
- **UNSOURCED**: a figure the official data cannot support (2-room and 6+-room prices, per m2, rent, yield, street averages, all-rooms
  neighbourhood averages, renovation costs, rules of thumb). Kept only when the page tells the reader both the kind of source and its
  date (in the sentence, row or section, or the page's own visible check date such as "עודכן ונבדק: 2026-06-06"). Otherwise
  rephrased without the number or replaced with an official city or neighbourhood figure.
- Not claims: explicit hypotheticals ("אם דירת 4 חדרים מוצעת ב-3.45 מיליון...") that do not assert the market level; they are listed
  in each JSON's `notes`.
- **tier 1** = alignment of sale prices with the list (conflicts, stale and unsourced sale figures). **tier 2** = rent, percent and
  cost figures with no dated source (removed under the strict reading of the rule). Tier 1 can be applied alone; the checker verified
  that the tier-1 edits still match when tier 2 is skipped.
- New text: natural Hebrew in each page's tone; official figures exactly as published, with their quarter ("לפי נתוני רשות המסים
  לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 4 חדרים ... היה ..."); the quarter is named when a room count's latest median is older
  (for example "הנתון האחרון שפורסם לדירות 3 חדרים"); no new portal or newspaper names; no em or en dash, no "!", no HTML entity;
  every number is either official or already on the page (machine-checked).

## Totals

| pages | CONSISTENT | CONFLICT | STALE | UNSOURCED kept / edited | edits (tier 1 / tier 2) |
|---|---|---|---|---|---|
| 13 pages that already had the list | 127 | 69 | 11 | 142 / 178 | 209 (171 / 38) |
| 10 other cities + the national hub | 133 | 80 | 17 | 141 / 105 | 155 (141 / 14) |
| **all 24 pages** | 260 | 149 | 28 | 283 / 283 | 364 (312 / 52) |

177 claims in conflict or stale hold 365 figures. 60 edits replace a whole table.

## Per page (13 live pages first)

| page | id | list on page | CONSISTENT | CONFLICT | STALE | UNSOURCED kept / edited | edits (tier 1 / 2) | whole tables | olds with risky characters | dry run |
|---|---|---|---|---|---|---|---|---|---|---|
| [tel-aviv-apartment-prices](https://nad-lan.co.il/tel-aviv-apartment-prices/) | 135 | yes | 0 | 0 | 0 | 0 / 5 | 8 (8 / 0) | 0 | 6 | pass |
| [jerusalem-apartment-prices](https://nad-lan.co.il/jerusalem-apartment-prices/) | 4575 | yes | 6 | 3 | 0 | 16 / 10 | 17 (14 / 3) | 2 | 11 | pass |
| [haifa-apartment-prices](https://nad-lan.co.il/haifa-apartment-prices/) | 4579 | yes | 6 | 12 | 0 | 2 / 29 | 25 (19 / 6) | 8 | 21 | pass |
| [herzliya-apartment-prices](https://nad-lan.co.il/herzliya-apartment-prices/) | 154 | yes | 21 | 3 | 0 | 1 / 16 | 16 (8 / 8) | 4 | 13 | pass |
| [netanya-apartment-prices](https://nad-lan.co.il/netanya-apartment-prices/) | 4577 | yes | 10 | 2 | 0 | 14 / 7 | 12 (11 / 1) | 1 | 8 | pass |
| [ramat-gan-apartment-prices](https://nad-lan.co.il/ramat-gan-apartment-prices/) | 4570 | yes | 10 | 0 | 0 | 20 / 11 | 12 (5 / 7) | 0 | 9 | pass |
| [bat-yam-apartment-prices](https://nad-lan.co.il/bat-yam-apartment-prices/) | 4583 | yes | 10 | 6 | 0 | 11 / 11 | 13 (13 / 0) | 4 | 4 | pass |
| [hod-hasharon-apartment-prices](https://nad-lan.co.il/hod-hasharon-apartment-prices/) | 4558 | yes | 15 | 2 | 5 | 8 / 7 | 20 (17 / 3) | 3 | 15 | pass |
| [ashdod-apartment-prices](https://nad-lan.co.il/ashdod-apartment-prices/) | 4587 | yes | 13 | 5 | 0 | 10 / 18 | 16 (16 / 0) | 3 | 14 | pass |
| [petah-tikva-apartment-prices](https://nad-lan.co.il/petah-tikva-apartment-prices/) | 4573 | yes | 10 | 3 | 0 | 16 / 19 | 13 (8 / 5) | 3 | 6 | pass |
| [ashkelon-apartment-prices](https://nad-lan.co.il/ashkelon-apartment-prices/) | 4593 | yes | 2 | 11 | 0 | 12 / 11 | 11 (11 / 0) | 2 | 10 | pass |
| [eilat-apartment-prices](https://nad-lan.co.il/eilat-apartment-prices/) | 4597 | yes | 8 | 14 | 6 | 18 / 23 | 27 (25 / 2) | 5 | 13 | pass |
| [kiryat-ono-apartment-prices](https://nad-lan.co.il/kiryat-ono-apartment-prices/) | 4560 | yes | 16 | 8 | 0 | 14 / 11 | 19 (16 / 3) | 1 | 14 | pass |
| [beer-sheva-apartment-prices](https://nad-lan.co.il/beer-sheva-apartment-prices/) | 4589 | added during the audit | 10 | 3 | 2 | 7 / 18 | 14 (14 / 0) | 2 | 3 | pass |
| [bnei-brak-apartment-prices](https://nad-lan.co.il/bnei-brak-apartment-prices/) | 4595 | added during the audit | 16 | 0 | 0 | 26 / 4 | 9 (9 / 0) | 2 | 6 | pass |
| [givatayim-apartment-prices](https://nad-lan.co.il/givatayim-apartment-prices/) | 4571 | added during the audit | 10 | 13 | 0 | 28 / 6 | 16 (15 / 1) | 2 | 14 | pass |
| [holon-apartment-prices](https://nad-lan.co.il/holon-apartment-prices/) | 4585 | added during the audit | 17 | 4 | 1 | 14 / 16 | 20 (13 / 7) | 3 | 3 | pass |
| [kfar-saba-apartment-prices](https://nad-lan.co.il/kfar-saba-apartment-prices/) | 4562 | added during the audit | 11 | 11 | 2 | 12 / 11 | 16 (16 / 0) | 3 | 14 | pass |
| [modiin-apartment-prices](https://nad-lan.co.il/modiin-apartment-prices/) | 4555 | added during the audit | 8 | 21 | 3 | 17 / 14 | 15 (15 / 0) | 4 | 10 | pass |
| [raanana-apartment-prices](https://nad-lan.co.il/raanana-apartment-prices/) | 167 | added during the audit | 24 | 0 | 0 | 13 / 4 | 4 (2 / 2) | 1 | 2 | pass |
| [ramat-hasharon-apartment-prices](https://nad-lan.co.il/ramat-hasharon-apartment-prices/) | 160 | added during the audit | 17 | 11 | 1 | 9 / 9 | 16 (14 / 2) | 2 | 2 | pass |
| [rehovot-apartment-prices](https://nad-lan.co.il/rehovot-apartment-prices/) | 4591 | added during the audit | 5 | 13 | 8 | 11 / 12 | 19 (19 / 0) | 3 | 4 | pass |
| [rishon-lezion-apartment-prices](https://nad-lan.co.il/rishon-lezion-apartment-prices/) | 4581 | added during the audit | 6 | 0 | 0 | 4 / 10 | 9 (7 / 2) | 2 | 8 | pass |
| [apartment-prices](https://nad-lan.co.il/apartment-prices/) | 7151 | added during the audit | 9 | 4 | 0 | 0 / 1 | 17 (17 / 0) | 0 | 13 | pass |

## Worst conflicts

Live pages:
- **Modiin** (not yet live at audit time, the owner's example): 3 rooms "2.4-2.7 מיליון" and the portal asking 2,650,000 vs the
  official 2,039,500 (10-12.2025, the latest published for 3 rooms); 4 rooms "2.8-3.2 מיליון" / 3,190,000 vs 2,559,800; city averages
  2,701,971 and 3,350,000 vs the all-rooms median 2,512,500. 21 conflicts, the most of any page.
- **Ashkelon**: lead directly above the list, 3 rooms "1.0-1.35 מיליון" vs 918,100; 4 rooms "1.45-1.85 מיליון" vs 1,405,800; asking
  anchors 1.2M / 1.69M / 2.2M in the rooms table and FAQ.
- **Eilat**: 3 rooms "1,100,000-1,450,000" vs 1,516,100 (the page was too LOW); an all-years average of 1.12M vs 1,624,100; 2023 street
  averages and 2021-2025 yearly averages presented as current.
- **Haifa**: 3 rooms 1,250,000 and 4 rooms 1,750,000-1,830,000 asking averages vs 1,135,100 and 1,597,500; city average 1,560,586 vs
  1,406,400; neighbourhood "averages" such as Hadar 549,379 vs the official Hadar 3-room median 1,066,400.
- **Bat Yam**: a private-site city average of 2,450,000 (lead, deals section, table, FAQ) vs the all-rooms median 1,901,500.
- **Kiryat Ono**: 5 rooms 3.76-4.10M second-hand and 3.6-4.7M new vs 3,533,500; city average 3.38-3.41M vs 3,175,100.
- **Herzliya**: "purchase averages around 4.0-4.24M" vs the all-deals median 3,202,200; new 4 rooms 3.49-3.55M vs 3,272,800.
- **Netanya**: a market-page city average of 1,582,219 vs the all-rooms median 2,629,800.
- **Jerusalem**: city average "about 2.9M" three times vs 2,717,100; neighbourhood averages far below the official medians (Gila
  1,215,394 vs 1,929,200 for 3 rooms).
- **Hod Hasharon**: city average 3,520,000-3,657,246 vs 3,149,300; 2023 neighbourhood averages (stale).
- **Petah Tikva**: Mahane Yehuda 3 rooms "1.5-1.9M" (table, deals table, FAQ) vs the official neighbourhood median 1,951,200.
- **Ashdod**: 3 rooms "1.66-1.68M" vs 1,603,300; new 5-room range 2.1-2.6M vs 2,784,800.
- **Ramat Gan, Tel Aviv**: no conflicts. Ramat Gan loses nine undated street averages; Tel Aviv's only figures (a per-m2 table with no
  source or date) become official neighbourhood medians.

Other pages:
- **Givatayim**: every 4-room figure too low ("3.1-3.6M", "3,096,234-3,600,000", a 3.32M example) vs 4,158,900; city averages 2,847,355
  and 4,350,000 vs 3,635,300; FAQ 5 rooms 4,290,568 vs 4,960,000.
- **Rehovot**: a multi-year private database average of 1,549,879 vs the all-rooms median 2,421,900; new-flat averages 3,110,000 (4
  rooms) and 2,380,000 (3 rooms) vs 2,345,500 and 1,921,100; historic neighbourhood averages (stale).
- **Ramat HaSharon**: new 5 rooms 5.4-6.7M vs 4,663,600; new 4 rooms 4.01-5.0M vs 3,809,600; second-hand 3 rooms 2.75-3.49M vs 3,544,800.
- **Kfar Saba** (the owner's example): 3 rooms "2-3M" / "2.1-3.0M" vs 1,941,300 (10-12.2025); city average about 2.8M vs 2,415,900.
- **Beer Sheva**: 5 rooms 1.86-1.89M vs 1,766,500 (7-9.2025, the latest published for 5 rooms); 2023 street averages (stale).
- **Holon**: a portal city average of 2,400,000 (four places) vs 2,219,400; every 3/4/5-room figure was consistent.
- **Bnei Brak, Raanana, Rishon LeZion**: no conflicts; undated street, deal or column figures were replaced or removed.
- **National hub**: the city cards for Modiin ("3 חד' ~2.65 מיליון"), Ashkelon ("מ-1.0 מיליון"), Kfar Saba ("2-3 מיליון") and Kiryat Ono
  ("ממוצע ~3.4 מיליון") contradict the official medians. All 14 cards are restated as the official 3-room median so they share one
  measure; the notice above the cards says which quarter (Kfar Saba, Netanya and Modiin: 10-12.2025).

## Dry-run match test

- Method (`tools/check.py`): every edit is applied in order to content.rendered; each `old` must match exactly once at its turn
  (`replace_all` entries exactly `expect_matches` times), never inside the price list, a script or a style; the tier-1-only run must
  also match; every number in `new` must be official or already in `old`; `source_keys` must resolve; CONFLICT and STALE claims must
  point at an edit. Result on the audited copy (10:34 UTC) and again on the live content (11:17-11:20 UTC): **24 of 24 pages pass,
  364 of 364 edits match**.
- Raw vs rendered: the raw content cannot be read without authentication. Evidence that the two agree inside a paragraph: the 24
  rendered pages hold no curly quotation mark (U+201C / U+201D) while hundreds of straight quotes survive inside ש"ח, מ"ר and
  ממ"ד, so wptexturize does not run on these pages; paragraphs are explicit `<p>` elements with no `<br>`. Every old string except the whole-table edits
  sits inside one element. Still, each edit carries `raw_risk`: 223 of 364 olds contain a character that wptexturize could change if it
  were on (206 straight double quotes, 24 apostrophes as in "חד'", 3 en dashes on the hub cards), 6 contain tags (the Tel Aviv table
  cells, single-line), and 60 are whole tables.
- Whole tables (`spans_tags`: true, 60 edits, 47 of them with line breaks between tags): `old` is the rendered table; if it does not
  match the raw content exactly, locate the single `<table>` element that contains `anchor` (a header cell unique on the page) and
  replace that element with `new`.
- Applying: generalise `scripts/project-stage/apply_align_sdedov.py` (page id from each file, `anchor` per table edit, optional tier
  filter, all or nothing, backup, read-back, rendered check). Re-fetch first; the live re-check above is from 7.10.2026 11:20 UTC.

## Found on the way

1. **The city files keep only 8 neighbourhoods.** 15 of the 23 files hold exactly 8; the official files hold far more (Haifa 57,
   Rehovot 33, Beer Sheva 23) and several of the missing ones DO have 1-3.2026 medians (checked 7.10.2026: Haifa Bat Galim 4 rooms
   2,854,300 and Givat Zemer 5 rooms 3,450,500; Rehovot Ahuzat HaNasi 4 rooms 2,905,000 and Rehovot HaMada 5 rooms 3,443,800; Beer
   Sheva Neve Menachem 4 rooms 1,228,000, Shchuna Tet 843,700 / 1,168,400). The new text therefore never says "לא פורסם" for a
   neighbourhood missing from a capped file; it says "לא מוצג במחירון" (not shown in the page's list). For the cities under the cap
   (Herzliya, Kfar Saba, Modiin, Hod Hasharon) every official neighbourhood was checked: none of the missing ones has a 1-3.2026
   median, so "לא פורסם" is true there. Adding more neighbourhoods to the city files would let those rows show official figures.
2. **Official medians that move sharply** (worth a look before the text leans on them): Ashkelon 3 rooms 1,142,100 to 918,100 in one
   quarter (-20.6% on the year; the FAQ shows both quarters); Kfar Saba 3 rooms -21.3% on the year, below the page's own May 2026 deals
   and below the city-centre 3-room median 2,106,700; Modiin all flats -18.5% and 4 rooms -15.9% on the year; Ramat HaSharon 3 rooms
   +16.4% with only 4 of 8 quarters published; Bat Yam 5 rooms +13% with 3 missing quarters; Ashdod all flats +12.7% while each room
   count moved -5.8% to +6.2% (deal mix); Haifa all flats +10.1% with flat room counts; Rehovot has no 3-room median for 1-3.2025.
3. Rishon LeZion: the wording on cheap and dear neighbourhoods disagrees with the official medians (Ramat Eliyahu called "נמוך עד
   בינוני" has a higher 4-room median than Remez, Rambam and Abramovitz; Nahalat Yehuda is the highest). Wording only, not edited.
4. Ashdod: the three deals in the deals table carry 15.3.2026, the same date as the CBS release the page cites; it may be the date they
   were read. Kept; the FAQ names the street without the date.
5. Tool notes for a future run: the checker's newspaper filter must ignore "בכל הארץ"; the room pattern must not read "3.5 חדרים" as 5
   rooms (both fixed in `tools/check.py`).

## Edits to decide on before applying

- **Consistent figures restated as the median** (optional, for one figure per room count): Ashkelon 5 rooms, Jerusalem rooms table
  (its 2-room, 6-room and luxury rows had no source), Bnei Brak lead / table / FAQ, Raanana rooms-table column, Herzliya 3 rooms, the
  9 consistent hub cards.
- **Tier 2, strict reading (52 edits)**: Herzliya shows no check date anywhere, so all its rent figures, the rent table and every
  34,000-38,000 per-m2 mention lose their numbers (8 edits); Haifa labels rents only "estimated", so the rent columns leave two tables
  (6); Ramat Gan, Holon (7 each), Petah Tikva (5) and others remove renovation costs, new-flat premiums and negotiation percentages. Superseded by the section "Tier 2 under the CEO rule (7.10.2026)" below: an official figure replaces the number wherever one exists.
- **Lenient keeps** that become tier-2 edits under a stricter reading: Kiryat Ono (rent, per m2, 2-room and 6+ rooms on "בדיקת נתוני
  שוק גלויים מ-5 ביוני 2026"), Rishon LeZion (a 16-row rent table labelled only "מדגם"), Petah Tikva per-m2 by area, Raanana street
  deals (page check date only), Ashkelon rent sample.
- **Near the tolerance edge**: Rehovot database average 2.55M (+5.3%), Ramat HaSharon averages 3,969,719 and 3.97-4.15M (about -6%),
  Kiryat Ono new 5 rooms (1.8% outside), Raanana 4 rooms 3.3-3.5M (inside by 1%), Herzliya 3 rooms 2.52-2.78M (median 2,793,600 just
  above).
- **Name mappings**: Kfar Saba "כפר סבא הירוקה" = official "הירוקה כ"ס 80"; Holon "קריית שרת" shown with the official "קרית שרת
  מערב" (part of it, the cell says so); Netanya "מרכז העיר" = official "מרכז העיר" (not "מע"ר"); Petah Tikva "אם המושבות החדשה" NOT
  mapped to "הדר המושבות החדשה"; Bnei Brak official "אהרונוביץ- סוקולוב" written "אהרונוביץ וסוקולוב", not treated as the page's
  "גבעת סוקולוב"; Tel Aviv uses natural names for the truncated official ones.
- **New table shapes**: Jerusalem rooms table keeps a size column (6 columns, check phone width); Haifa street table becomes the
  last five quarters of city medians and the category table becomes Haifa vs national; Eilat 2023 street table becomes the last five
  quarters; Bat Yam and Herzliya area tables lose their price column (official figures move to the paragraph above).
- **Removed rather than recomputed**: Modiin and Ashdod yield columns (their purchase prices conflicted; no new arithmetic was
  allowed). Holon keeps its 3-5-room yields (built from a named rent source and ranges that contain the medians).
- **Examples left as they are**: 90 remaining SUSPECT lines in the checker are individual dated deals or explicit "if" examples. Some
  examples still sit far from the median (Ashkelon "a 3-room flat offered at 1.32M", 44% above 918,100); they are illustrations, not
  claims, but could be softened.

<!-- tier2-ceo:start -->
## Tier 2 under the CEO rule (7.10.2026)

DATA ONLY, like the rest of this folder: nothing was applied, no WordPress write, no commit, no push. The 52 tier-2 edits (rent, percentage and
renovation-cost figures with no dated source) were rebuilt under the CEO's rule of 7.10.2026. The 312 tier-1 edits are untouched; tier 1 is live
(every tier-1 `new` text is on the 14 live pages), so the tier-2 `old` strings were re-checked against the live content, not the audited copy.

**The rule.** (1) If an official, dated value exists for the same thing, the number is replaced by it, with its period: rents from the Central
Bureau of Statistics (CBS) average-rent table, sale prices from the city files (Tax Authority, data.nadlan.gov.il). (2) If none exists the number is
removed. The sentence or cell stays only as advice or a hedged statement that makes no price-level claim ("a renovation may be needed", "check against
similar deals"); a statement of level ("rent here is above the city average", "usually lower than new") needs an official figure, and without one it is
deleted, with the row or column that had no value without the number. (3) No number invented, no newspaper named, titles, H1s and headings untouched.

**Counts: 8 replaced with an official value, 40 number removed (sentence or cell kept), 4 sentence, row or column deleted.**
Replaced: haifa 10, 11, 24; herzliya 10, 11, 12, 16; ramat-gan 1. Deleted: haifa 12; hod-hasharon 20; eilat 14, 15.

**Official sources used** (the only new ones; every replacement line below carries its URL):
- CBS table 4.9, "Average monthly free-market rent (NIS) by residential district, big city and size group (rooms)", latest quarter IV-VI 2026
  (Q2 2026, April-June), Price Statistics Monthly No. 7/2026: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf (Hebrew; English version `a4_9_e.pdf` in the same folder). Issue 8/2026
  (`price08a`) holds the identical table; `price09a` answered 404 on 7.10.2026, so Q2 2026 is the latest published quarter. The table is in
  `tools/cbs_rent_2026_q2.json` (Israel, 6 districts, 18 big cities; the Hebrew and English PDFs hold the same 1,107 price figures). The size groups are
  the CBS groups (1-2, 2.5-3, 3.5-4 and 4.5+ rooms; a 3-room flat sits in 2.5-3, a 4-room flat in 3.5-4, a 5-room flat in 4.5+) and the text rounds the
  published one-decimal average to whole shekels, half up (Herzliya 6,774.5 becomes 6,775). Since Q1 2026 the top group is "4.5+" (all larger sizes).
- CBS press release 021/2026 of 19.1.2026, "דירות ומבנים בישראל, 2025" (dwelling register, July 2025): the Tel Aviv district holds 19.5% of Israel's
  dwellings: https://www.cbs.gov.il/he/mediarelease/DocLib/2026/021/04_26_021b.pdf
- Sale prices: the city files only (Herzliya edit 12 keeps the 3-room median 2,793,600, 1-3.2026).

**Where there is no official figure.** The CBS big-city list has no Eilat, Givatayim, Hod HaSharon, Kiryat Ono, Raanana, Ramat HaSharon or Modiin row, and its
rent table has no neighbourhood rents and no rent medians. For yields, renovation costs, per-m2 prices, new-vs-second-hand premiums and negotiation gaps no
official dated figure was found (the city files hold deal medians by rooms only), so those numbers are removed. Herzliya and Haifa lose their rent median
and every neighbourhood rent; the CBS publishes city averages only.

**Verification.** `python tools/check_tier2.py` fetches each page and applies only the tier-2 edits, in the listed order, to the live
`content.rendered`: **52 of 52 `old` strings match exactly once** (whole tables through their anchor), checked on copies fetched 7.10.2026 11:42 UTC and
again 7.10.2026 12:04 UTC; no page changed in between (modified stamps unchanged). Every number in a new text is in the old text, a city file or the CBS table;
no dash, "!", entity or newspaper name; every `source_keys` resolves; every replacement carries a cbs.gov.il `source_url`. Two `old` strings were
widened to stand alone (Haifa 11 takes the next sentence, whose example rent 3,820 was the removed table figure; Eilat 14 takes the sentence that
pointed at "such gaps"); the other 50 `old` strings are unchanged. New fields on tier-2 edits: `ceo_action` (replaced, removed, deleted), `ceo_note`,
`source_url` (replacements only); each file with tier-2 edits also has `tier2_ceo_recheck`. `python tools/b_tier2_ceo.py` rebuilds the 14 files from the
live pages; `tools/check.py` accepts the CBS keys and figures.

**Judgement calls for the CEO to confirm.** (a) Hedged advice survives without its number ("a renovation may be needed"); a level claim does not: where a
cell would only have said "usually lower than new" or "premium market" it became a check ("compare with closed deals of similar second-hand flats"),
or the row went. (b) Herzliya's rent table keeps the CBS city average and size groups; its median row and six neighbourhood rows are deleted. (c) Table
rows regroup to the CBS size groups (Haifa and Herzliya: 1 and 2 rooms become "1 עד 2 חדרים", 5 and 6 rooms become "4.5 חדרים ומעלה"). (d) Per-m2
cells on Ramat Gan, a private-site per-m2 range on Holon and the city per-m2 on Herzliya had no official counterpart in the city files and are removed.

**One line per edit.**

- `jerusalem-apartment-prices`, n11 (removed): removed the 10%-25% new-flat per-m2 premium (no official source); cell kept hedged.
- `jerusalem-apartment-prices`, n12 (removed): removed the renovation cost 150,000-600,000 (no official source); cell kept.
- `jerusalem-apartment-prices`, n13 (removed): removed the renovation cost 150,000-600,000 (no official source); 'common mistake' cell kept.
- `haifa-apartment-prices`, n10 (replaced): replaced the 6-row rent column with the CBS average rent for Haifa by size group (1-2, 2.5-3, 3.5-4, 4.5+ rooms), Q2 2026: 2,478 / 3,119 / 4,061 / 5,420 ש"ח; rows regrouped to the CBS groups, usage notes kept. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `haifa-apartment-prices`, n11 (replaced): replaced rent 'median 3,400 / average 3,867' with the CBS average 3,405 ש"ח (Haifa, Q2 2026); the example sentence's 3,820 rent became the CBS 2.5-3 rooms average 3,119. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `haifa-apartment-prices`, n12 (deleted): deleted the neighbourhood rent column (no official neighbourhood rent exists); the 'what to check' notes stay.
- `haifa-apartment-prices`, n17 (removed): removed the renovation cost range 150,000-400,000 (no official source); caution sentence kept.
- `haifa-apartment-prices`, n24 (replaced): replaced rent 'median 3,400 / average 3,867' with the CBS average 3,405 ש"ח (Haifa, Q2 2026). Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `haifa-apartment-prices`, n25 (removed): removed the renovation cost range 150,000-400,000 (no official source); caution sentence kept.
- `herzliya-apartment-prices`, n1 (removed): removed 'hundreds of thousands, even over a million' (no official source); the sentence now only says that same-size flats sell at different prices by area.
- `herzliya-apartment-prices`, n4 (removed): removed the city per-m2 figure 34,000-38,000 (no official source); the advice stays.
- `herzliya-apartment-prices`, n10 (replaced): replaced rents 6,500-6,800 (3 rooms) and 7,500-8,500 (4 rooms) with the CBS average rent for Herzliya, Q2 2026: 6,775 ש"ח. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `herzliya-apartment-prices`, n11 (replaced): replaced the unsourced rent median / average / per-room list with the CBS size-group range for Herzliya, Q2 2026: 4,444 (1-2 rooms) to 9,461 (4.5+ rooms); median dropped (the CBS publishes none). Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `herzliya-apartment-prices`, n12 (replaced): rebuilt the rent table on the CBS Herzliya figures (city 6,775; 1-2: 4,444; 2.5-3: 5,606; 3.5-4: 7,041; 4.5+: 9,461 ש"ח, Q2 2026); median row and 6 neighbourhood rows deleted (no official source). Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `herzliya-apartment-prices`, n13 (removed): removed the city per-m2 figure 34,000-38,000 (no official source); the advice stays.
- `herzliya-apartment-prices`, n15 (removed): removed the city per-m2 range 34,000-38,000 (no official source); the answer now says no single city figure fits.
- `herzliya-apartment-prices`, n16 (replaced): replaced the undated per-room rent list with the CBS Herzliya size-group averages, Q2 2026: 4,444 / 5,606 / 7,041 / 9,461 ש"ח. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `netanya-apartment-prices`, n5 (removed): removed the 10%-30% garden / roof premium (no official source); cell now says what to compare against.
- `ramat-gan-apartment-prices`, n1 (replaced): kept 19.5% and added its official source and period: CBS dwelling register, July 2025 (press release 021/2026, 19.1.2026). Source: https://www.cbs.gov.il/he/mediarelease/DocLib/2026/021/04_26_021b.pdf
- `ramat-gan-apartment-prices`, n6 (removed): removed the renovation cost 150,000-500,000 (no official source); advice to price it from quotes kept.
- `ramat-gan-apartment-prices`, n7 (removed): removed the 5%-20% second-hand discount (no official source); cell kept as a hedged 'sometimes lower'.
- `ramat-gan-apartment-prices`, n8 (removed): removed the second-hand per-m2 range 30,000-38,000 (no official source); cell now says what to compare against.
- `ramat-gan-apartment-prices`, n9 (removed): removed the new-flat per-m2 range 40,000-55,000 (no official source); cell now says what to compare against.
- `ramat-gan-apartment-prices`, n10 (removed): removed the renovation cost 150,000-500,000 (no official source); cell kept as 'may need a renovation'.
- `ramat-gan-apartment-prices`, n12 (removed): removed the 3%-8% asking-price gap (no official source); sentence kept.
- `hod-hasharon-apartment-prices`, n10 (removed): removed the renovation cost 150,000-400,000 (no official source); sentence kept.
- `hod-hasharon-apartment-prices`, n12 (removed): removed the renovation cost 150,000-400,000 (no official source); cell kept.
- `hod-hasharon-apartment-prices`, n20 (deleted): deleted the two undated single-address price rows (אסירי ציון 19, שדרות הנשיאים 42); the three dated May 2026 deals stay.
- `petah-tikva-apartment-prices`, n1 (removed): removed the 8%-22% new-vs-second-hand premium (no official source); cell says it varies by project.
- `petah-tikva-apartment-prices`, n7 (removed): removed the 5%-12% renovation premium (no official source); cell kept hedged.
- `petah-tikva-apartment-prices`, n8 (removed): removed the 8%-18% new-flat premium (no official source); cell kept hedged.
- `petah-tikva-apartment-prices`, n9 (removed): removed the 10%-22% off-plan premium (no official source); cell says it varies by project.
- `petah-tikva-apartment-prices`, n13 (removed): removed the 2%-4% and 8%-12% asking-to-deal gaps (no official source); sentence kept.
- `eilat-apartment-prices`, n14 (deleted): deleted the sentence with the old-source rents 1,341-3,096 and yields 3.4%-5.1% (undated, no official counterpart: the CBS has no Eilat figure); the next sentence made self-standing.
- `eilat-apartment-prices`, n15 (deleted): deleted the old-source rent and yield column (undated, no official counterpart); the note that pointed at the gap between sources reworded.
- `kiryat-ono-apartment-prices`, n14 (removed): removed the renovation cost 100,000-300,000 (no official source); cell kept as 'quotes set the cost'.
- `kiryat-ono-apartment-prices`, n15 (removed): removed same-street gaps 300,000 / 500,000 (no official source); sentence kept.
- `kiryat-ono-apartment-prices`, n16 (removed): removed the 2-8 percent asking-to-closing gap (no official source); cell kept.
- `givatayim-apartment-prices`, n11 (removed): removed the renovation cost 150,000-500,000 (no official source); cell kept.
- `holon-apartment-prices`, n3 (removed): removed 250,000-350,000 and the per-m2 range 25,000-29,000 (no official source); the 10 m2 example and the advice stay.
- `holon-apartment-prices`, n4 (removed): removed the 5%-12% floor / balcony gap (no official source); hedged sentence kept.
- `holon-apartment-prices`, n12 (removed): removed the 8%-20% new-flat premium (no official source); hedged sentence kept.
- `holon-apartment-prices`, n14 (removed): removed the renovation cost 80,000-300,000 (no official source); cell kept as 'a renovation may be needed'.
- `holon-apartment-prices`, n15 (removed): removed the 50,000-250,000 effect on the offer (no official source); cell kept.
- `holon-apartment-prices`, n16 (removed): removed the renovation cost 80,000-300,000 (no official source); cell kept as advice.
- `holon-apartment-prices`, n20 (removed): removed the 8%-20% new-flat premium (no official source); hedged sentence kept.
- `raanana-apartment-prices`, n3 (removed): removed the renovation cost 150,000-400,000 (no official source); sentence kept.
- `raanana-apartment-prices`, n4 (removed): removed the renovation cost 150,000-500,000 (no official source); cell kept.
- `ramat-hasharon-apartment-prices`, n8 (removed): removed the renovation cost 250,000-600,000 (no official source); sentence kept.
- `ramat-hasharon-apartment-prices`, n10 (removed): removed the renovation cost gap 200,000-700,000 (no official source); sentence kept.
- `rishon-lezion-apartment-prices`, n3 (removed): removed the renovation cost 100,000-250,000 (no official source); sentence kept.
- `rishon-lezion-apartment-prices`, n6 (removed): removed the renovation cost 80,000-300,000 (no official source); cell kept.

**Outside the 52 edits, not touched.** A scan of the pages as they will stand after tier 1 and tier 2 (`python tools/scan_rent_left.py`, output
`tools/rent_lines_left_after_tier2.json`) still finds rent figures between 1,000 and 20,000 in the body: lenient keeps from named, dated, non-official
samples (listing pages checked 5-6.6.2026), explicit "if" examples, and the CBS lines added here. For cities with a CBS row several differ from the CBS
average (for example Ramat Gan "average about 6,411" against 5,894 in Q2 2026, Rishon LeZion averages 5,787-6,131 against 5,273); a follow-up pass could replace them under the same rule.
<!-- tier2-ceo:end -->

## Files

- `<slug>.align-edits.json` (24): `page`, `source`, `facts`, `apply_rules`, `claims_summary`, `notes`, `claims` (the full inventory with
  where / quote / measure / rooms / figures / official / verdict / action), `edits` (n, page_id, url, field, old, new, source_keys,
  audit_verdict, why, matches_in_live, tier, raw_risk, and when used replace_all + expect_matches, spans_tags + anchor,
  kept_numbers), `live_recheck`.
- `tools/`: the scripts that produced and checked the files: `fetch.py` (public GET into `tools/pages/`), `blocks.py` (article blocks
  outside the list), `facts.py` (official fact sheet), `mk.py` (builder helpers), `b_<page>.py` (one builder per page; Ashkelon was the
  worked example), `check.py` (dry run and number trace), `gen_readme.py` (summary tables). Tier 2 under the CEO rule: `cbs_rent_2026_q2.json` (CBS table 4.9), `b_tier2_ceo.py` (rebuilds the tier-2 edits), `check_tier2.py` (applies them to the live pages), `gen_tier2_section.py` and `tier2_ceo_section.md` (this README section), `scan_rent_left.py` (rent figures still in the body). They read the pages from `tools/pages/`, so
  run `python tools/fetch.py` first.
