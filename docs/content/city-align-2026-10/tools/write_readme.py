# -*- coding: utf-8 -*-
"""Write docs/content/city-align-2026-10/README.md from the 24 JSON files plus the narrative below."""
import io, json, os, glob
D = r"C:\Users\777\nad-lan\nad-lan-co-il\docs\content\city-align-2026-10"
LIVE13 = ["tel-aviv", "jerusalem", "haifa", "herzliya", "netanya", "ramat-gan", "bat-yam", "hod-hasharon", "ashdod", "petah-tikva",
          "ashkelon", "eilat", "kiryat-ono"]
OTHER = ["beer-sheva", "bnei-brak", "givatayim", "holon", "kfar-saba", "modiin", "raanana", "ramat-hasharon", "rehovot", "rishon-lezion"]
ORDER = [s + "-apartment-prices" for s in LIVE13 + OTHER] + ["apartment-prices"]


def load(slug):
    return json.load(io.open(os.path.join(D, slug + ".align-edits.json"), encoding="utf-8"))


def stats(J):
    cl = J["claims"]
    c = lambda v: sum(1 for x in cl if x["verdict"] == v)
    uk = sum(1 for x in cl if x["verdict"] == "UNSOURCED" and not x["action"].startswith("edit"))
    ue = c("UNSOURCED") - uk
    E = J["edits"]
    t1 = sum(1 for e in E if e.get("tier", 1) == 1)
    return dict(C=c("CONSISTENT"), X=c("CONFLICT"), S=c("STALE"), Uk=uk, Ue=ue, E=len(E), t1=t1, t2=len(E) - t1,
                tab=sum(1 for e in E if e.get("spans_tags")), risky=sum(1 for e in E if e.get("raw_risk")))


rows, groups = [], {"live": dict.fromkeys(["C", "X", "S", "Uk", "Ue", "E", "t1", "t2", "tab", "risky"], 0)}
groups["other"] = dict(groups["live"]); groups["all"] = dict(groups["live"])
for slug in ORDER:
    J = load(slug)
    st = stats(J)
    g = "live" if slug.replace("-apartment-prices", "") in LIVE13 else "other"
    for k, v in st.items():
        groups[g][k] += v
        groups["all"][k] += v
    lr = J["live_recheck"]
    lst = "yes" if g == "live" else "added during the audit"
    rows.append(f"| [{slug}]({J['page']['link']}) | {J['page']['id']} | {lst} | {st['C']} | {st['X']} | {st['S']} | {st['Uk']} / {st['Ue']} | "
                f"{st['E']} ({st['t1']} / {st['t2']}) | {st['tab']} | {st['risky']} | {'pass' if 'errors 0' in lr['dry_run'] else 'FAIL'} |")


def grow(name, g):
    return (f"| {name} | {g['C']} | {g['X']} | {g['S']} | {g['Uk']} / {g['Ue']} | {g['E']} ({g['t1']} / {g['t2']}) |")


md = f"""# City price pages: body text aligned with the official price list (7.10.2026)

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
{grow("13 pages that already had the list", groups["live"])}
{grow("10 other cities + the national hub", groups["other"])}
{grow("**all 24 pages**", groups["all"])}

{groups['all']['X'] + groups['all']['S']} claims in conflict or stale hold 365 figures. {groups['all']['tab']} edits replace a whole table.

## Per page (13 live pages first)

| page | id | list on page | CONSISTENT | CONFLICT | STALE | UNSOURCED kept / edited | edits (tier 1 / 2) | whole tables | olds with risky characters | dry run |
|---|---|---|---|---|---|---|---|---|---|---|
""" + "\n".join(rows) + """

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
  (6); Ramat Gan, Holon (7 each), Petah Tikva (5) and others remove renovation costs, new-flat premiums and negotiation percentages.
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

## Files

- `<slug>.align-edits.json` (24): `page`, `source`, `facts`, `apply_rules`, `claims_summary`, `notes`, `claims` (the full inventory with
  where / quote / measure / rooms / figures / official / verdict / action), `edits` (n, page_id, url, field, old, new, source_keys,
  audit_verdict, why, matches_in_live, tier, raw_risk, and when used replace_all + expect_matches, spans_tags + anchor,
  kept_numbers), `live_recheck`.
- `tools/`: the scripts that produced and checked the files: `fetch.py` (public GET into `tools/pages/`), `blocks.py` (article blocks
  outside the list), `facts.py` (official fact sheet), `mk.py` (builder helpers), `b_<page>.py` (one builder per page; Ashkelon was the
  worked example), `check.py` (dry run and number trace), `gen_readme.py` (summary tables). They read the pages from `tools/pages/`, so
  run `python tools/fetch.py` first.
"""
io.open(os.path.join(D, "README.md"), "w", encoding="utf-8", newline="\n").write(md)
print("README written", len(md), "chars")
print(groups)
# the tier-2 section (CEO rule, 7.10.2026) is generated from the JSON files and inserted before "## Files"
import subprocess, sys
subprocess.run([sys.executable, os.path.join(D, "tools", "gen_tier2_section.py")], check=False)
