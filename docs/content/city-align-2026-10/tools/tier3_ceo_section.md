<!-- tier3-ceo:start -->
## Tier 3: listing-site rents under the CEO rule (7.10.2026)

DATA ONLY, like the rest of this folder: nothing was applied, no WordPress write, no commit, no push. After tier 1 and tier 2 (both live on the 24 pages) the
bodies of 22 pages still carried rent figures from listing and market sites, several of them contradicting the official CBS figures (Ramat Gan "about
6,411" against the CBS 5,894; Rishon LeZion 5,787-6,131 against 5,273). The 139 tier-3 edits (`"tier": 3`, n continuing the numbering after tier 2, same
schema, `ceo_action`, `ceo_note`, `source_url` on replacements) apply the CEO's rule to every one of them. Tel Aviv and the national hub `/apartment-prices/`
have no rent figure left and get no edit. This is the follow-up pass that the last paragraph of the tier-2 section proposed; tier 1 and tier 2 are untouched.

**The rule as applied.** (1) Where the CBS publishes the same thing (city and size group, table 4.9, Q2 2026, April-June 2026) the listing figure is replaced by
the CBS value with its quarter, in the page's own wording (first mention "לפי הלשכה המרכזית לסטטיסטיקה, שכר הדירה החודשי הממוצע ב<city> ברבעון השני של 2026
(אפריל עד יוני) היה ..."). Rooms map to the CBS groups as in tier 2: 1-2 rooms (a "2 rooms" figure), 2.5-3 (3 rooms), 3.5-4 (4 rooms), 4.5+ (5 rooms and larger,
also 6 rooms). Tables that keep exact room labels because the neighbouring column is the Tax Authority median by room count (Ashdod, Bat Yam, Holon, Kfar Saba,
Ramat Gan) name the CBS group inside each rent cell; the other rent tables are regrouped to the four CBS groups and the usage notes of merged rows are joined.
A listing city median has no CBS counterpart (the CBS publishes averages, no medians): it is replaced by the CBS city average, as tier 2 did for Haifa. National
comparisons use the CBS Israel row (5,086; 2.5-3 rooms 4,466). (2) Where the CBS publishes nothing (neighbourhood and area rents in every city; Eilat, Givatayim,
Hod HaSharon, Kiryat Ono, Raanana, Ramat HaSharon and Modiin, which are not in the CBS big-city list; houses; Kfar Saba 1-2 rooms, a dash in the CBS table) the
number is removed. The sentence or cell stays only if it is still true and useful without the number and makes no rent-level claim; otherwise the sentence, row,
column, table or paragraph is deleted. (3) No number invented, no new arithmetic, no newspaper named, titles, H1s and headings untouched.

**Counts: 64 replaced with the CBS value, 43 number removed (sentence or cell kept), 32 sentence, row, column, table or paragraph deleted
(139 edits on 22 pages).**

| page | id | CBS row | tier-3 edits | replaced | removed | deleted |
|---|---|---|---|---|---|---|
| [jerusalem-apartment-prices](https://nad-lan.co.il/jerusalem-apartment-prices/) | 4575 | yes | 5 | 4 | 0 | 1 |
| [haifa-apartment-prices](https://nad-lan.co.il/haifa-apartment-prices/) | 4579 | yes | 1 | 0 | 1 | 0 |
| [herzliya-apartment-prices](https://nad-lan.co.il/herzliya-apartment-prices/) | 154 | yes | 1 | 0 | 1 | 0 |
| [netanya-apartment-prices](https://nad-lan.co.il/netanya-apartment-prices/) | 4577 | yes | 6 | 5 | 1 | 0 |
| [ramat-gan-apartment-prices](https://nad-lan.co.il/ramat-gan-apartment-prices/) | 4570 | yes | 10 | 7 | 2 | 1 |
| [bat-yam-apartment-prices](https://nad-lan.co.il/bat-yam-apartment-prices/) | 4583 | yes | 7 | 6 | 1 | 0 |
| [hod-hasharon-apartment-prices](https://nad-lan.co.il/hod-hasharon-apartment-prices/) | 4558 | no (not in the CBS big-city list) | 4 | 0 | 2 | 2 |
| [ashdod-apartment-prices](https://nad-lan.co.il/ashdod-apartment-prices/) | 4587 | yes | 8 | 6 | 2 | 0 |
| [petah-tikva-apartment-prices](https://nad-lan.co.il/petah-tikva-apartment-prices/) | 4573 | yes | 6 | 3 | 1 | 2 |
| [ashkelon-apartment-prices](https://nad-lan.co.il/ashkelon-apartment-prices/) | 4593 | yes | 12 | 6 | 3 | 3 |
| [eilat-apartment-prices](https://nad-lan.co.il/eilat-apartment-prices/) | 4597 | no (not in the CBS big-city list) | 10 | 0 | 5 | 5 |
| [kiryat-ono-apartment-prices](https://nad-lan.co.il/kiryat-ono-apartment-prices/) | 4560 | no (not in the CBS big-city list) | 7 | 0 | 3 | 4 |
| [beer-sheva-apartment-prices](https://nad-lan.co.il/beer-sheva-apartment-prices/) | 4589 | yes | 6 | 4 | 1 | 1 |
| [bnei-brak-apartment-prices](https://nad-lan.co.il/bnei-brak-apartment-prices/) | 4595 | yes | 10 | 6 | 2 | 2 |
| [givatayim-apartment-prices](https://nad-lan.co.il/givatayim-apartment-prices/) | 4571 | no (not in the CBS big-city list) | 7 | 0 | 3 | 4 |
| [holon-apartment-prices](https://nad-lan.co.il/holon-apartment-prices/) | 4585 | yes | 5 | 4 | 0 | 1 |
| [kfar-saba-apartment-prices](https://nad-lan.co.il/kfar-saba-apartment-prices/) | 4562 | yes | 5 | 5 | 0 | 0 |
| [modiin-apartment-prices](https://nad-lan.co.il/modiin-apartment-prices/) | 4555 | no (not in the CBS big-city list) | 8 | 0 | 5 | 3 |
| [raanana-apartment-prices](https://nad-lan.co.il/raanana-apartment-prices/) | 167 | no (not in the CBS big-city list) | 7 | 0 | 6 | 1 |
| [ramat-hasharon-apartment-prices](https://nad-lan.co.il/ramat-hasharon-apartment-prices/) | 160 | no (not in the CBS big-city list) | 4 | 0 | 3 | 1 |
| [rehovot-apartment-prices](https://nad-lan.co.il/rehovot-apartment-prices/) | 4591 | yes | 4 | 4 | 0 | 0 |
| [rishon-lezion-apartment-prices](https://nad-lan.co.il/rishon-lezion-apartment-prices/) | 4581 | yes | 6 | 4 | 1 | 1 |

**Official source used** (the same table as tier 2; every replacement line below carries its URL): CBS table 4.9, "Average monthly free-market rent (NIS) by
residential district, big city and size group (rooms)", Q2 2026 (April-June), Price Statistics Monthly No. 7/2026: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf. Figures are in
`tools/cbs_rent_2026_q2.json`, rounded half up to whole shekels in the text (Bnei Brak 4,482.5 becomes 4,483; Ramat Gan 6,826.5 becomes 6,827). Nothing else official was added.

**What replaced what, by kind of line.**
- Lead sentences and FAQ answers with rents by rooms, a city median or a city average: the CBS city average and/or the four size groups of the city.
- Rent tables (rent column or whole table): rebuilt on the CBS size groups; columns that only held a second private source, a "working range", an ad count or a
  yield derived from the private rent are deleted.
- Worked examples that used a listing-site rent (Ashdod, Ashkelon, Bat Yam, Bnei Brak, Holon): the rent becomes the CBS group average and the
  figures computed from the old rent (annual rent, gross yield %) are dropped rather than recomputed; the formula stays in words. Where the city has no CBS row the
  example rent is replaced by words ("a high rent", "a lower rent than expected").
- Neighbourhood and area rents (Ashkelon, Beer Sheva, Bnei Brak, Eilat, Jerusalem, Petah Tikva, Ramat Gan, Rishon LeZion, Raanana, Modiin...): the rent column or
  paragraph is deleted. In the neighbourhood tables that kept their "what to check" column, eight cells that read a rent level into the area or pointed at a rent sample
  ("premium", "relatively cheap rent", "lower rent reflects demand", "do not conclude from one rent") were reworded as checks or lost the claim (Jerusalem Old Katamon, Petah Tikva four,
  Ramat Gan Shikun Vatikim, Rishon LeZion two); rows whose only content was the rent sample were deleted (Jerusalem Romema, Givatayim City).
- Yields from listing-site rents (Bnei Brak 3.6%, Eilat 6.1%, Holon 2.2%-3.7%, Modiin 2.9%): removed with the rent they rested on.

**Verification.** `python tools/b_tier3_ceo.py` rebuilds the 22 files from the live pages (public GET `wp/v2/pages/<id>`); `python tools/check_tier3.py` applies only the
tier-3 edits, in order, to the live `content.rendered`: **139 of 139 `old` strings match exactly once** (whole tables through their anchor), re-fetched 7.10.2026 20:28 UTC;
the `modified` stamps of the 22 pages were unchanged between the first fetch and the last. Also checked: the `new` texts hold no dash, "!", entity or newspaper name and
no double space or space before punctuation (also across the edit boundaries); every number in a `new` text is in its `old`, in a city file or a CBS table 4.9 figure;
every `source_keys` entry resolves; replacements name the CBS and carry a cbs.gov.il `source_url` and (in their own text or the header beside it) the quarter; rebuilt
tables use only the tags and attributes of the table they replace and the tag counts of the page stay balanced; the tier-1 and tier-2 `new` texts are all still live.
**Residual scan after the edits: 0 rent figures between 1,000 and 20,000 outside the CBS figures** (sentence by sentence, and in every table whose header names a rent). Two
figures near rent words are not rents and stay: Bat Yam "2,675 homes for sale" and Jerusalem "3,150 rent ads" (a supply count, kept in the Jerusalem snapshot table).
Raw versus rendered: as in tiers 1 and 2, every `old` outside whole tables sits inside one element; the deleted paragraphs carry their `<p dir="rtl">` tags in `old`
(raw_risk "contains tags"); the rebuilt and deleted tables are applied through their `anchor` (the page's own table markup is kept: the tables of Ramat Gan are
indented, the rebuilt ones are flat, which does not change the rendering).

**Judgement calls for the CEO to confirm.**
(a) *Hypothetical rents in worked examples* ("if a flat is rented at 5,300...") were treated as rent figures, because most of them copy the listing-site level shown
elsewhere on the same page. With a CBS row they now use the CBS group average; the derived yield or annual rent is dropped. If round pedagogical examples may stay,
the affected edits are: haifa n26; herzliya n17; netanya n18; bat-yam n17, n18, n19; ashdod n21, n24; ashkelon n17, n21; eilat n35; kiryat-ono n22; bnei-brak n15, n17; holon n22; raanana n8, n9; ramat-hasharon n19; rishon-lezion n13, n14.
(b) *Neighbourhood tables*: the rent column goes everywhere; where the remaining columns only restated the rent level (Ashkelon "price signal", Rishon "what the number
may hint") they go too; where they hold genuine advice (Jerusalem, Petah Tikva, Ramat Gan, Rishon) the advice column stays. Whole rent tables with no advice of their own were deleted (Eilat two, Hod HaSharon, Kiryat Ono, Modiin, Raanana,
Ramat HaSharon, Givatayim, Bnei Brak areas).
(c) *Kfar Saba 1-2 rooms and houses*: the CBS table has a dash for Kfar Saba 1-2 rooms and no house category, so those cells read "לא פורסם", the wording the tables already use
for a missing sale median.
(d) *Cities without a CBS row* get no number at all, not even a district figure. The CBS does publish district averages for all flats (Tel Aviv District 6,412; Center District 5,474; South
District 3,703; Haifa District 3,719; Jerusalem District 5,302; North District 3,271), but a district is not the city; adding one as context is a one-line option per page if wanted (which district
each city belongs to would be checked first).
(e) *Counts of rent ads* (Netanya 226, Petah Tikva 184-233, Ramat Gan 520, Beer Sheva 628, Bnei Brak 37, Eilat 188 ...) were deleted wherever they only qualified a removed rent sample.
(f) *Sentences about private rent sources* that give general caution ("rent ads are not signed contracts", "sources differ") stay: they contain no figure.

**Found on the way, not touched (not rent figures).** Renovation costs still stand on about a dozen pages (Ashdod 150,000-300,000 in two places, Bat Yam 100,000-300,000 / 120,000-180,000,
Eilat 120,000, Haifa 250,000, Herzliya 150-300 thousand / 250,000, Kfar Saba 80,000-300,000 / 250,000, Raanana 200,000-300,000 in four places, Ramat HaSharon 300,000, Rishon LeZion 80,000 and 180,000):
the same rule as tier 2 would apply. Listing-site per-m2 prices and sale-price examples are also unchanged (tier 1 left them).

**One line per edit.**

- `jerusalem-apartment-prices`, n18 (replaced): replaced the listing-site family-flat rent range 5,500-8,500 (and "more in luxury, large or new flats") with the CBS Jerusalem averages for 3.5-4 and 4.5+ rooms, Q2 2026: 6,180 / 7,748 ש"ח. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `jerusalem-apartment-prices`, n19 (replaced): replaced the asking-rent average 7,100 with the CBS Jerusalem average 5,347 ש"ח (Q2 2026); "gaps of thousands between neighbourhoods" became "rent varies between neighbourhoods". Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `jerusalem-apartment-prices`, n20 (replaced): in the market-snapshot table replaced the asking-rent average 7,100 with the CBS Jerusalem average 5,347 ש"ח (Q2 2026) and deleted the ad-site median row 6,200 (361 ads); the other rows are untouched. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `jerusalem-apartment-prices`, n21 (replaced): replaced the ad-site median 6,200 (361 ads, May 2026) and the average 7,100 with the CBS Jerusalem averages for all flats and by size group, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `jerusalem-apartment-prices`, n22 (deleted): deleted the neighbourhood rent column (12 values 5,684-12,714 ש"ח) and the Romema row, whose note was only about the rent sample; the Old Katamon note "higher rent can reflect..." became a check; the other notes stay.
- `haifa-apartment-prices`, n26 (removed): removed the two illustrative rents 2,700 and 5,000 from the example (the CBS averages 3,405 and 3,119 stay in the same paragraph); the two cases are stated in words.
- `herzliya-apartment-prices`, n17 (removed): removed the illustrative rent 8,000 (it matches neither the CBS city average 6,775 nor any CBS size group); the sentence says it in words.
- `netanya-apartment-prices`, n13 (replaced): replaced the family-flat rent range 5,000-8,000 with the CBS Netanya averages for 3.5-4 and 4.5+ rooms, Q2 2026: 5,273 / 6,695 ש"ח; "sharp gaps" became "rent varies". Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `netanya-apartment-prices`, n14 (replaced): replaced the family-flat rent range 5,000-8,000 with the CBS Netanya averages for 3.5-4 and 4.5+ rooms (5,273 / 6,695 ש"ח, Q2 2026). Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `netanya-apartment-prices`, n15 (replaced): in the quick-facts table replaced the family-flat rent range 5,000-8,000 with the CBS Netanya averages for 3.5-4 and 4.5+ rooms (5,273 / 6,695 ש"ח, Q2 2026); the other rows are untouched. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `netanya-apartment-prices`, n16 (replaced): replaced the ad counts (hundreds; 226 ads on 16.4.2026) and the market-page average 6,265 and median 5,300 with the CBS Netanya averages for all flats and by size group, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `netanya-apartment-prices`, n17 (replaced): rebuilt the rent-check table on the CBS Netanya averages (all flats 4,816; 1-2: 3,084; 2.5-3: 4,116; 3.5-4: 5,273; 4.5+: 6,695 ש"ח, Q2 2026); the ad-count row, the market-page median row, the "working range" column (3,200-9,500) and the unsourced sea-view premium range were deleted; the sea-view row now reads "לא פורסם". Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `netanya-apartment-prices`, n18 (removed): removed the illustrative rent gap 700 ש"ח a month.
- `ramat-gan-apartment-prices`, n13 (replaced): replaced the median 6,000, the average 6,411 (the "about 6,411" the CEO flagged) and the per-room rents (2: 4,896; 3: 6,486; 4: 7,736) with the CBS Ramat Gan averages for all flats and by size group, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `ramat-gan-apartment-prices`, n14 (replaced): replaced the rent 6,000-6,500 (median or average) with the CBS Ramat Gan average 5,894 ש"ח (Q2 2026). Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `ramat-gan-apartment-prices`, n15 (replaced): in the fact table replaced the average rent 6,411 with the CBS Ramat Gan average 5,894 ש"ח (Q2 2026) and deleted the median row 6,000 and the "520 active rent ads checked" row; the other rows are untouched. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `ramat-gan-apartment-prices`, n16 (replaced): replaced the listing-site rents by rooms (1: 3,368; 2: 4,896; 3: 6,486; 4: 7,736; 5: 10,209; 6+: 12,279) with the CBS Ramat Gan averages by size group, Q2 2026: 4,168 / 5,469 / 6,827 / 8,255 ש"ח; each cell names its group. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `ramat-gan-apartment-prices`, n17 (deleted): deleted the area rent column (14 values 4,350-11,890 ש"ח); in the Shikun Vatikim row "quiet market and relatively low rent" lost its rent clause; the other notes stay.
- `ramat-gan-apartment-prices`, n18 (replaced): replaced the median 6,000, average 6,411, the 520-ad sample and the national median 4,400 with the CBS Ramat Gan average 5,894 and the CBS national average 5,086 ש"ח, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `ramat-gan-apartment-prices`, n19 (replaced): rebuilt the rent-by-rooms table on the CBS Ramat Gan size groups (4,168 / 5,469 / 6,827 / 8,255 ש"ח, Q2 2026); six rows (1-6 rooms, 3,368-12,279) regrouped to four. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `ramat-gan-apartment-prices`, n20 (removed): removed the area rents (Ramat Chen 9,090; Ramat Efal 10,775; Kiryat Krinitzi 11,890) from the FAQ answer.
- `ramat-gan-apartment-prices`, n21 (removed): removed the Bursa-area rent 6,793 from the FAQ answer.
- `ramat-gan-apartment-prices`, n22 (replaced): replaced the city rent 6,000-6,411 with the CBS Ramat Gan average 5,894 ש"ח (Q2 2026) in the FAQ answer. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `bat-yam-apartment-prices`, n14 (replaced): replaced the private average rents (asking average 5,500; second source 5,760) and the remark that 3-room flats are popular with the CBS Bat Yam average 4,407 ₪, Q2 2026; the count of sale listings stays. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `bat-yam-apartment-prices`, n15 (replaced): replaced the ad-site examples (2 rooms 4,200; 3 rooms 4,600; 4 rooms 6,600; 5 rooms 8,950) and the second source average 5,760 with the CBS Bat Yam averages for all flats and by size group, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `bat-yam-apartment-prices`, n16 (replaced): replaced the rent ranges (2 rooms 3,800-4,800; 3 rooms 4,300-5,600; 4 rooms 5,800-7,200; 5 rooms 7,200-9,500) with the CBS Bat Yam averages by size group, Q2 2026; each cell names its group because the sale-median column beside it is by exact room count. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `bat-yam-apartment-prices`, n17 (replaced): replaced the example rent 5,000 with the CBS 2.5-3 rooms average for Bat Yam (4,107 ₪, Q2 2026); dropped the annual rent 60,000 and the yield 3.0% that depended on it (no new arithmetic). Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `bat-yam-apartment-prices`, n18 (replaced): replaced the example rent 5,200 with the CBS 2.5-3 rooms average for Bat Yam (4,107 ₪, Q2 2026); dropped the yield 2.4% that depended on it. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `bat-yam-apartment-prices`, n19 (removed): removed the unsourced monthly gap 300-700 and its annual 3,600-8,400; the sentence says it in words.
- `bat-yam-apartment-prices`, n20 (replaced): replaced the FAQ asking averages (5,500 and 5,760) with the CBS Bat Yam averages for all flats and by size group, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `hod-hasharon-apartment-prices`, n21 (removed): removed the market-page average rent 7,500-9,100 for 4-5 rooms; the paragraph under the heading now says only that rent varies by size, building age and location.
- `hod-hasharon-apartment-prices`, n22 (deleted): deleted the row "average observed rent about 7,900-8,500" from the fact table; the other rows are untouched.
- `hod-hasharon-apartment-prices`, n23 (removed): removed the market-page average 8,500 and the ranges by rooms (3: 4,500-5,900; 4: 7,537-8,400; 5: 8,905-9,850); the sentence now lists what rent depends on.
- `hod-hasharon-apartment-prices`, n24 (deleted): deleted the rent-by-rooms table (1-2 rooms 4,094-6,000; 3: 4,500-5,900; 4: 7,537-8,400; 5: 8,905-9,850; 6: 10,373; 6+: 12,125) with its notes: private market pages, no official counterpart.
- `ashdod-apartment-prices`, n17 (replaced): replaced the listing-site rents by rooms (2: 3,500; 3: 4,474-4,500; 4: 5,300; 5: 7,650) with the CBS average rent in Ashdod by size group, Q2 2026: 3,119 / 3,906 / 4,855 / 6,239 ש"ח. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `ashdod-apartment-prices`, n18 (removed): removed the district rent 4,000-4,200 (listing pages; the CBS publishes no district rent); the sentence now ends on the official sale medians.
- `ashdod-apartment-prices`, n19 (replaced): replaced the rent column (2 rooms 3,500; 3 rooms 4,474-4,500; 4 rooms 5,300; 5 rooms 7,650) with the CBS Ashdod averages by size group, Q2 2026; each cell names its group because the sale-median column beside it is by exact room count. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `ashdod-apartment-prices`, n20 (replaced): replaced the private rent median 3,925 (250 listings), 3-room 4,474 and national 4,400 with the CBS Ashdod average 4,455 and the CBS national average 5,086 ש"ח, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `ashdod-apartment-prices`, n21 (replaced): replaced the example rent 5,300 with the CBS average for 3.5-4 rooms in Ashdod (4,855, Q2 2026) and dropped the computed yield 2.9% (no new arithmetic); the formula stays. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `ashdod-apartment-prices`, n22 (removed): removed the sentence with the district rent 4,000-4,200 (listing pages; no official district rent).
- `ashdod-apartment-prices`, n23 (replaced): replaced the FAQ rents by rooms (3,500 / 4,474-4,500 / 5,300 / 7,650) and the city median 3,925 with the CBS Ashdod averages by size group and for all flats, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `ashdod-apartment-prices`, n24 (replaced): replaced the example rent 5,300 with the CBS 3.5-4 rooms average for Ashdod (4,855, Q2 2026); dropped the annual rent 63,600 and the yield 2.9% that depended on it (no new arithmetic). Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `petah-tikva-apartment-prices`, n14 (replaced): replaced the rent range 5,000-8,000 "in most neighbourhoods" with the CBS Petah Tikva average 5,138 ש"ח (Q2 2026). Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `petah-tikva-apartment-prices`, n15 (replaced): replaced the five neighbourhood example rents (Amishav 4,383; centre 5,098; Kfar Ganim A 6,681; Em HaMoshavot 8,209; Neve Gan 9,875) with the CBS Petah Tikva averages for all flats and by size group, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `petah-tikva-apartment-prices`, n16 (replaced): in the quick-facts table replaced the family-flat rent range 5,500-8,700 with the CBS Petah Tikva averages for 3.5-4 and 4.5+ rooms (5,311 / 7,099 ש"ח, Q2 2026); the other rows are untouched. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `petah-tikva-apartment-prices`, n17 (deleted): deleted the sentence on the 184-233 active rent ads in the samples (the neighbourhood rents it qualified are gone).
- `petah-tikva-apartment-prices`, n18 (deleted): deleted the neighbourhood rent column (15 values 4,383-9,875 ש"ח); four notes that read a rent level into the area ("premium", "relatively high rent", "lower rent reflects demand", "more accessible price") became checks; the other eleven notes stay.
- `petah-tikva-apartment-prices`, n19 (removed): removed the Em HaMoshavot example rent 8,209; the advice to compare with similar flats in the same area stays.
- `ashkelon-apartment-prices`, n12 (replaced): replaced the listing-site city rent midpoint 3,500 with the CBS Ashkelon averages by size group, Q2 2026: 2,740 / 3,261 / 4,031 / 4,906 ש"ח. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `ashkelon-apartment-prices`, n13 (replaced): replaced the private rent figures (average 3,500, median 3,500 from 279 ads, average 4,130) and the median-vs-average remark with the CBS Ashkelon average 3,698 ש"ח, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `ashkelon-apartment-prices`, n14 (deleted): deleted the paragraph with 9 neighbourhood rent medians (Barnea 3,209, Afridar 4,233, Agamim 4,980, Marina 5,053, Ir HaYayin 5,287, S.Y. Agnon 2,300, Ben Gurion 2,731, Jabotinsky 2,858, Neve Yam 2,918): the CBS publishes no neighbourhood rent.
- `ashkelon-apartment-prices`, n15 (deleted): deleted the two sentences with neighbourhood rent medians (Ir HaYayin 5,287, Marina 5,053, Agamim 4,980) and the demand reading drawn from them; the sentence on what enters a sale value stays.
- `ashkelon-apartment-prices`, n16 (deleted): deleted the neighbourhood rent column (9 values 2,731-5,500) and the price-signal column that restated the rent level; area and what-to-check columns stay.
- `ashkelon-apartment-prices`, n17 (removed): removed the two illustrative rents 4,700 and 3,200; the comparison stays in words.
- `ashkelon-apartment-prices`, n18 (replaced): replaced the 279-ad sample (median 3,500, average 4,130, 3 rooms 3,629, national median 4,400) with the CBS averages: Ashkelon 3,698 / 3,261 (2.5-3 rooms) against 5,086 / 4,466 nationally, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `ashkelon-apartment-prices`, n19 (removed): removed the second listing source (293 ads, average 4,108, median 3,500, 4.6.2026); the general remark on listing sources stays.
- `ashkelon-apartment-prices`, n20 (replaced): rebuilt the rent-by-rooms table on the CBS Ashkelon size groups (2,740 / 3,261 / 4,031 / 4,906 ש"ח, Q2 2026) with the national CBS average for each group; ad counts, the second-source column and the one-ad 6-room row (18,000) deleted. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `ashkelon-apartment-prices`, n21 (replaced): replaced the example rents 3,600 / 4,700 / 5,500 / 7,100 with the CBS Ashkelon averages for 2.5-3, 3.5-4 and 4.5+ rooms (3,261 / 4,031 / 4,906 ש"ח, Q2 2026); the hypothetical sale prices stay. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `ashkelon-apartment-prices`, n22 (removed): removed the neighbourhood rents (Ir HaYayin 5,287, Agamim 4,980); the advice to check the supply still to come stays.
- `ashkelon-apartment-prices`, n23 (replaced): replaced the FAQ rents (city median 3,500, averages 4,108-4,130, by rooms 2,963 / 3,629 / 4,709 / 7,127) with the CBS Ashkelon averages for all flats and by size group, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `eilat-apartment-prices`, n28 (removed): removed the asking rents 3,100 (2 rooms) to 8,850 (5 rooms) from the lead.
- `eilat-apartment-prices`, n29 (removed): removed all rent figures from the paragraph (188 ads, average 4,486, median 3,585, minimum 530; second source average 3,500, yield 6.1%, 3,100 / 3,900 / 6,250 / 8,850); the remark that rent differs by property type, location, furnishing and season stays in general form.
- `eilat-apartment-prices`, n30 (removed): removed the average 4,486 and the median 3,585 from the caution paragraph.
- `eilat-apartment-prices`, n31 (deleted): deleted the paragraph with the Eilat average 4,486, median 3,585, minimum 530 and 14 area averages (Shahamon 7,087 ... the hotels 6,500) from a private ad source.
- `eilat-apartment-prices`, n32 (deleted): deleted the table of the Eilat average and 12 area averages with ad counts (4,486 / 3,585; Shahamon 7,087 ... the hotels 6,500): private ad data, no official counterpart.
- `eilat-apartment-prices`, n33 (deleted): deleted the sentence with the second-source rents by rooms (3,100 / 3,900 / 6,250 / 8,850); the advice on reconciling different rent sources stays.
- `eilat-apartment-prices`, n34 (deleted): deleted the table of rent by rooms (2 rooms 3,100; 3 rooms 3,900; 4 rooms 6,250; 5 rooms 8,850) with its messages to the buyer: private source, no official counterpart.
- `eilat-apartment-prices`, n35 (removed): removed the two illustrative rents 3,900 and 6,250.
- `eilat-apartment-prices`, n36 (removed): removed the private-source yield 6.1% (built on private rents).
- `eilat-apartment-prices`, n37 (deleted): deleted the FAQ sentence with the average 4,486, the median 3,585 and the rents by rooms (3,100 / 3,900 / 6,250 / 8,850).
- `kiryat-ono-apartment-prices`, n20 (removed): removed the rent range 5,800-8,200 for 3-5 rooms and the 11,900-14,000 for a house or very large flat; the paragraph under the heading keeps the contrast between an old flat without parking and a newer one with a safe room, lift and parking.
- `kiryat-ono-apartment-prices`, n21 (deleted): deleted the row "general average rent 7,600-7,900" from the fact table; the other rows are untouched.
- `kiryat-ono-apartment-prices`, n22 (removed): removed the illustrative rent 7,500.
- `kiryat-ono-apartment-prices`, n23 (removed): removed "alongside the common monthly rent from a visible market check" from the sentence that introduces the sale-median table (the rent column is deleted in the next edit).
- `kiryat-ono-apartment-prices`, n24 (deleted): deleted the "common monthly rent" column (3 rooms 5,800-6,600; 4 rooms 7,300-7,500; 5 rooms 7,900-8,200) from the sale-median table; median, yearly change and check note stay.
- `kiryat-ono-apartment-prices`, n25 (deleted): deleted the rent-by-rooms table (1-2 rooms 3,700-4,300; 3: 5,800-6,600; 4: 7,300-7,500; 5: 7,900-8,200; 6: 8,700+; house 11,900-14,000) with its "relation to the sale price" column: private market pages, no official counterpart.
- `kiryat-ono-apartment-prices`, n26 (deleted): deleted the FAQ sentence with the common rent 5,800-6,600 for such 3-room flats.
- `beer-sheva-apartment-prices`, n15 (replaced): replaced the asking rents by rooms (2: 2,300; 3: 2,600-2,760; 4: 3,170-3,640; 5: 4,750-5,740) with the CBS Beer Sheva averages by size group, Q2 2026: 2,321 / 2,788 / 3,501 / 4,908 ₪. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `beer-sheva-apartment-prices`, n16 (replaced): replaced the ad-site median 2,600, average 3,003, the 628-ad count and the 3-room asking rent 2,759 with the CBS Beer Sheva average 3,183 ₪ and the 2.5-3 rooms average 2,788 ₪, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `beer-sheva-apartment-prices`, n17 (replaced): rebuilt the rent table on the CBS Beer Sheva size groups (2,321 / 2,788 / 3,501 / 4,908 ₪, Q2 2026); the three private-source rent columns (asking, median, working range) deleted; rows regrouped to the CBS groups. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `beer-sheva-apartment-prices`, n18 (deleted): deleted the paragraph with 11 neighbourhood rent medians (Gimel 2,672, Dalet 2,479, Ramot 3,971, Ramot B 5,244, Park HaNahal 5,313, Neve Zeev 5,377 and others): the CBS publishes no neighbourhood rent.
- `beer-sheva-apartment-prices`, n19 (removed): removed the neighbourhood rents (Park HaNahal 5,313, Neve Zeev 5,377, Gimel 2,672); the caution to normalise rooms, size and target group stays.
- `beer-sheva-apartment-prices`, n20 (replaced): replaced the FAQ rents (median 2,600, average 3,003, by rooms 2,200-5,738) with the CBS Beer Sheva averages for all flats and by size group, Q2 2026; deleted the unsourced remark that rent is higher in Neve Zeev, Park HaNahal and Ramot B. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `bnei-brak-apartment-prices`, n10 (replaced): replaced the asking rents 4,000 (2 rooms) to 7,900 (5 rooms) with the CBS Bnei Brak range by size group, Q2 2026: 3,443 (1-2 rooms) to 6,272 (4.5+ rooms) ש"ח. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `bnei-brak-apartment-prices`, n11 (replaced): replaced the private asking rent 5,700 with the CBS Bnei Brak average 4,483 ש"ח (Q2 2026); removed the private yield 3.6%. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `bnei-brak-apartment-prices`, n12 (deleted): deleted the paragraph with 5 area rents (Pardes Katz 4,900; Tel Giborim 4,100; Givat Rokach 5,350; Nahalat Shimon 4,313; industrial zone 6,100): the CBS publishes no area rent.
- `bnei-brak-apartment-prices`, n13 (replaced): replaced the two private rent sources (asking average 5,700; 37 ads: average 4,888, median 4,600, cheapest 2,500) and the remark built on their gap with the CBS Bnei Brak averages for all flats and by size group, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `bnei-brak-apartment-prices`, n14 (replaced): rebuilt the rent table on the CBS Bnei Brak averages (size groups 3,443 / 4,236 / 5,030 / 6,272 and all flats 4,483 ש"ח, Q2 2026); the private average 5,700, the second source 4,888 and the median 4,600 rows deleted. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `bnei-brak-apartment-prices`, n15 (replaced): replaced the example rents 4,700 and 5,950 with the CBS Bnei Brak averages for 2.5-3 and 3.5-4 rooms (4,236 / 5,030 ש"ח, Q2 2026); dropped the annual rents 56,400 and 71,400 (no new arithmetic). Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `bnei-brak-apartment-prices`, n16 (deleted): deleted the table of 9 area rents (Pardes Katz 4,900 ... Shikun HaHistadrut 2,500) with their ad counts and notes: the CBS publishes no area rent.
- `bnei-brak-apartment-prices`, n17 (removed): removed the two single-ad rents 6,500 and 2,500 (they came from the deleted area table); the caution stays in words.
- `bnei-brak-apartment-prices`, n18 (removed): removed the Pardes Katz area rent 4,900 (11 ads) from the FAQ answer; the answer ends on the advice to check similar deals.
- `bnei-brak-apartment-prices`, n19 (replaced): replaced the FAQ rents by rooms (4,000 / 4,700 / 5,950 / 7,900) and the second source (average 4,888, median 4,600, 37 ads) with the CBS Bnei Brak averages for all flats and by size group, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `givatayim-apartment-prices`, n17 (removed): removed the listing median rent 6,000 from the lead.
- `givatayim-apartment-prices`, n18 (removed): removed the median rent 6,000 and the 3-room rent 6,391 from the control points; the price per m2 (not a rent) stays.
- `givatayim-apartment-prices`, n19 (deleted): deleted the row "median rent about 6,000" from the fact table; the four sale rows are untouched.
- `givatayim-apartment-prices`, n20 (deleted): deleted the "City" row ("expensive rent around 10,450 in an expensive area") from the area table; the other twelve rows are untouched.
- `givatayim-apartment-prices`, n21 (deleted): deleted the two sentences with the city median 6,000 (293 ads), the 3-room average 6,391 and the indications 5,580 / 6,150 / 7,500 / 10,350.
- `givatayim-apartment-prices`, n22 (deleted): deleted the rent table (city median 6,000; 293 ads; 2-5 rooms 5,580-10,350; Shenkin 5,393; City 10,450): private ad data, no official counterpart.
- `givatayim-apartment-prices`, n23 (removed): removed the Shenkin area rent 5,393 ("relatively cheap rent") from the FAQ answer; the advice to check flat type and comparable deals stays.
- `holon-apartment-prices`, n21 (replaced): replaced the private asking rent 5,150 and the examples by rooms (4,100 / 4,500 / 5,800 / 8,200) with the CBS Holon averages for all flats and by size group, Q2 2026; the count of sale listings stays. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `holon-apartment-prices`, n22 (replaced): replaced the example rents 4,500-5,000 and 4,700 with the CBS 2.5-3 rooms average for Holon (4,321 ₪, Q2 2026); dropped the computed yield 2.8%-3.1% (no new arithmetic). Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `holon-apartment-prices`, n23 (deleted): deleted the paragraph that set three private rent sources against each other (5,150; 5,721 and median 5,200; 5,563).
- `holon-apartment-prices`, n24 (replaced): replaced the private asking rent (4,500 / 5,800 / 8,200) with the CBS Holon averages by size group, Q2 2026 (4,321 / 5,434 / 6,981 ₪); deleted the private rent-range column (4,200-8,800) and the gross-yield column (2.2%-3.7%) built on it; the purchase-price column stays. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `holon-apartment-prices`, n25 (replaced): replaced the FAQ private average 5,150-5,721 and median 5,200 with the CBS Holon average 4,945 ₪ (Q2 2026); deleted the unsourced "moderate gross yield" claim against 2,000,000-2,700,000. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `kfar-saba-apartment-prices`, n17 (replaced): replaced the market-source average rent 7,200-7,350 with the CBS Kfar Saba average 6,146 ש"ח (Q2 2026). Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `kfar-saba-apartment-prices`, n18 (replaced): replaced the average rent 7,200-7,350 with the CBS Kfar Saba average 6,146 ש"ח (Q2 2026). Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `kfar-saba-apartment-prices`, n19 (replaced): replaced the family-flat rents (4 rooms 6,750-6,800; 5 rooms 8,100-9,100) with the CBS Kfar Saba averages for 3.5-4 and 4.5+ rooms, Q2 2026: 6,042 / 7,796 ש"ח. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `kfar-saba-apartment-prices`, n20 (replaced): replaced the market rents (2 rooms 4,000-4,500; 3 rooms 5,550-5,800; 4 rooms 6,750-6,800; 5 rooms 8,100-9,100; private house 13,500) with the CBS Kfar Saba averages (4,771 / 6,042 / 7,796 ש"ח, Q2 2026); the 2-room and private-house cells say "לא פורסם" (the CBS has no such figure). Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `kfar-saba-apartment-prices`, n21 (replaced): replaced the FAQ rents (average 7,200-7,350; by rooms 4,000-9,100) with the CBS Kfar Saba averages for all flats and by size group, Q2 2026; states that no 1-2 rooms average was published. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `modiin-apartment-prices`, n16 (deleted): deleted three rows from the quick-index table: average rent 7,600, asking rent 7,200 and average city yield 2.9% (listing sites, read 5.6.2026); the sale median, price per m2 and listing-count rows are untouched.
- `modiin-apartment-prices`, n17 (removed): removed the rents by rooms (3: 6,200; 4: 6,950; 5: 8,500) from the sentence; the 6-room sale prices that follow stay.
- `modiin-apartment-prices`, n18 (deleted): deleted the two sentences with the average rent 7,600, the asking rent 7,200 and the average city yield 2.9% (read 5.6.2026).
- `modiin-apartment-prices`, n19 (removed): removed the sentence with the rents by rooms (3: 6,200; 4: 6,950; 5: 8,500); "the meaning is that a regular family flat" became "a regular family flat".
- `modiin-apartment-prices`, n20 (deleted): deleted the rent-by-rooms table (monthly rent 6,200 / 6,950 / 8,500, annual rent 74,400 / 83,400 / 102,000, asking average 7,200 and 86,400): listing-site rents and the annual figures derived from them.
- `modiin-apartment-prices`, n21 (removed): removed the 4-room rent 6,950 from the FAQ answer; the asking price per m2 and the advice stay.
- `modiin-apartment-prices`, n22 (removed): removed the FAQ rents (average 7,600; asking 7,200; by rooms 6,200 / 6,950 / 8,500); the answer says that rent varies by rooms, neighbourhood and condition and points to ads and rental deals of similar flats.
- `modiin-apartment-prices`, n23 (removed): removed the listing-site yield 2.9% from the investor row of the users table; the advice to build a net calculation stays.
- `raanana-apartment-prices`, n5 (removed): removed the Merkaz Darom rent 9,600 and "these numbers indicate strong demand"; the average purchase price and the caution that it does not price every flat stay.
- `raanana-apartment-prices`, n6 (removed): removed the rent 9,600 from the Merkaz Darom row of the area table; the average purchase price in the same cell stays.
- `raanana-apartment-prices`, n7 (removed): removed the median 8,000 (52 ads), the levels 7,257 / 8,559 / 10,959 and the Merkaz Darom rent 9,600; the paragraph keeps its first sentence and says that rent varies by flat type and area.
- `raanana-apartment-prices`, n8 (removed): removed the illustrative rent range 7,500-8,500 for a 4-room flat offered at 3,700,000.
- `raanana-apartment-prices`, n9 (removed): removed the illustrative rent range 10,000-11,000 for a 5-room flat.
- `raanana-apartment-prices`, n10 (deleted): deleted the table of rent levels (median 8,000 on 52 ads; 7,257 / 8,559 / 10,959 market reports; Merkaz Darom 9,600) with its readings: private data, no official counterpart.
- `raanana-apartment-prices`, n11 (removed): removed the FAQ rents (median 8,000; 7,257 / 8,559 / 10,959; Merkaz Darom 9,600); the answer keeps "rent gives context for demand" and the caution that follows.
- `ramat-hasharon-apartment-prices`, n17 (removed): removed the public-market average rent 9,500; "another source presented" became "public market data presented" so the average price that follows still has its source.
- `ramat-hasharon-apartment-prices`, n18 (deleted): deleted the rent table (2 rooms 4,850-6,200; 3: 6,700-8,050; 4: 8,400-9,400; 5: 11,500-11,880; duplex, penthouse or garden flat 11,000-13,250; house 13,500) with its readings and warnings: private data, no official counterpart.
- `ramat-hasharon-apartment-prices`, n19 (removed): removed the illustrative rent 9,000 a month from the seller example; the asking price 4.6 million stays.
- `ramat-hasharon-apartment-prices`, n20 (removed): removed the FAQ rents (average 9,500; asking 11,750; by rooms 4,850-9,400); the answer says that rent varies by rooms, property type and condition and points to ads and rental deals of similar properties.
- `rehovot-apartment-prices`, n20 (replaced): replaced the asking rents by rooms (2: 3,300; 3: 4,900; 4: 5,700; 5: 7,950) and the ad median 4,500 / average 4,987 with the CBS Rehovot averages by size group, Q2 2026: 3,281 / 4,171 / 5,102 / 6,555 ₪. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `rehovot-apartment-prices`, n21 (replaced): rebuilt the rent table on the CBS Rehovot averages (size groups 3,281 / 4,171 / 5,102 / 6,555 and all flats 4,943 ₪, Q2 2026); removed the ad figures (3,300-7,950, 5,425, median 4,500, average 4,987, 3-room median 4,814). Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `rehovot-apartment-prices`, n22 (replaced): replaced the 97-ad sample (median 4,500, average 4,987, 3-room median 4,814, national median 4,400, extreme ads 1,920 and 10,200) with the CBS Rehovot average 4,943 and the CBS national average 5,086 ₪, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `rehovot-apartment-prices`, n23 (replaced): replaced the FAQ asking rents (3,300 / 4,900 / 5,700 / 7,950; median 4,500, average 4,987) with the CBS Rehovot averages for all flats and by size group, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `rishon-lezion-apartment-prices`, n10 (replaced): replaced the lead rents (median 5,000; averages 5,787-6,131 the CEO flagged; higher in western neighbourhoods) with the CBS Rishon LeZion averages for all flats (5,273) and by size group, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `rishon-lezion-apartment-prices`, n11 (replaced): replaced the median 5,000, the averages 5,787-6,131 and the remark on large/western/new flats with the CBS Rishon LeZion averages 5,273 (all flats) and 7,498 (4.5+ rooms), Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `rishon-lezion-apartment-prices`, n12 (deleted): deleted the neighbourhood rent column (16 values 3,900-8,950 ש"ח) and the "what the number may hint" column (premium, moderate, relatively high...); the caution column stays, two cautions that pointed at a rent sample were reworded.
- `rishon-lezion-apartment-prices`, n13 (removed): removed the two illustrative rents 8,000 and 4,500; the two cases are stated in words.
- `rishon-lezion-apartment-prices`, n14 (replaced): in the worked-example table replaced the expected rent 5,600-6,300 for the 4-room flat with the CBS Rishon LeZion average for 3.5-4 rooms (5,555 ש"ח, Q2 2026); the other steps are untouched. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
- `rishon-lezion-apartment-prices`, n15 (replaced): replaced the FAQ rents (median 5,000; averages 5,787-6,131; 7,000-9,000 in western or large flats) with the CBS Rishon LeZion averages for all flats and by size group, Q2 2026. Source: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price07a/a4_9_h.pdf
<!-- tier3-ceo:end -->
