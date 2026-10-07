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
