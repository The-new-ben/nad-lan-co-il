# -*- coding: utf-8 -*-
"""Write tools/tier3_ceo_section.md (the README section 'Tier 3: listing-site rents under the CEO rule (7.10.2026)', one line per edit, generated from the
22 JSON files that hold tier-3 edits) and put it into README.md before '## Files' (between the markers; re-running replaces it).
python gen_tier3_section.py [verified_utc]"""
import io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.dirname(HERE)
CBS = json.load(io.open(os.path.join(HERE, "cbs_rent_2026_q2.json"), encoding="utf-8"))
VERIFIED = sys.argv[1] if len(sys.argv) > 1 else "7.10.2026 20:22 UTC"
LIVE13 = ["tel-aviv", "jerusalem", "haifa", "herzliya", "netanya", "ramat-gan", "bat-yam", "hod-hasharon", "ashdod", "petah-tikva",
          "ashkelon", "eilat", "kiryat-ono"]
OTHER = ["beer-sheva", "bnei-brak", "givatayim", "holon", "kfar-saba", "modiin", "raanana", "ramat-hasharon", "rehovot", "rishon-lezion"]
ORDER = [s + "-apartment-prices" for s in LIVE13 + OTHER] + ["apartment-prices"]
START, END = "<!-- tier3-ceo:start -->", "<!-- tier3-ceo:end -->"
NO_CBS = {"eilat", "givatayim", "hod-hasharon", "kiryat-ono", "modiin", "raanana", "ramat-hasharon"}

lines, tot, per = [], {"replaced": 0, "removed": 0, "deleted": 0}, []
for slug in ORDER:
    J = json.load(io.open(os.path.join(D, slug + ".align-edits.json"), encoding="utf-8"))
    t3 = [e for e in J["edits"] if e.get("tier") == 3]
    if not t3:
        continue
    c = {"replaced": 0, "removed": 0, "deleted": 0}
    for e in t3:
        a = e["ceo_action"]
        tot[a] += 1
        c[a] += 1
        src = f" Source: {e['source_url']}" if e.get("source_url") else ""
        lines.append(f"- `{slug}`, n{e['n']} ({a}): {e['ceo_note']}.{src}")
    base = slug.replace("-apartment-prices", "")
    per.append(f"| [{slug}](https://nad-lan.co.il/{slug}/) | {J['page']['id']} | {'no (not in the CBS big-city list)' if base in NO_CBS else 'yes'} | {len(t3)} | {c['replaced']} | {c['removed']} | {c['deleted']} |")

n_all = sum(tot.values())
HYPO = {"ashdod": ["example rent 5,300"], "ashkelon": ["illustrative rents 4,700 and 3,200", "example rents 3,600"],
        "bat-yam": ["example rent 5,000", "example rent 5,200", "monthly gap 300-700"], "bnei-brak": ["example rents 4,700 and 5,950", "single-ad rents 6,500 and 2,500"],
        "holon": ["example rents 4,500-5,000"], "netanya": ["illustrative rent gap 700"],
        "raanana": ["illustrative rent range 7,500-8,500", "illustrative rent range 10,000-11,000"],
        "rishon-lezion": ["illustrative rents 8,000 and 4,500", "expected rent 5,600-6,300"], "haifa": ["illustrative rents 2,700 and 5,000"],
        "herzliya": ["illustrative rent 8,000"], "kiryat-ono": ["illustrative rent 7,500"], "eilat": ["illustrative rents 3,900 and 6,250"],
        "ramat-hasharon": ["illustrative rent 9,000"]}
exs = {}
for slug in ORDER:
    base = slug.replace("-apartment-prices", "")
    if base not in HYPO:
        continue
    J = json.load(io.open(os.path.join(D, slug + ".align-edits.json"), encoding="utf-8"))
    for e in J["edits"]:
        if e.get("tier") == 3 and any(k in e["ceo_note"] for k in HYPO[base]):
            exs.setdefault(base, []).append(e["n"])
miss = [(b, k) for b, ks in HYPO.items() for k in ks if not any(k in e["ceo_note"] for sl in ORDER if sl.startswith(b + "-apartment") for e in json.load(io.open(os.path.join(D, sl + ".align-edits.json"), encoding="utf-8"))["edits"] if e.get("tier") == 3)]
assert not miss, miss
EX = "; ".join(f"{sl} " + ", ".join(f"n{n}" for n in ns) for sl, ns in exs.items())
u = CBS["urls"]
md = f"""{START}
## Tier 3: listing-site rents under the CEO rule (7.10.2026)

DATA ONLY, like the rest of this folder: nothing was applied, no WordPress write, no commit, no push. After tier 1 and tier 2 (both live on the 24 pages) the
bodies of 22 pages still carried rent figures from listing and market sites, several of them contradicting the official CBS figures (Ramat Gan "about
6,411" against the CBS 5,894; Rishon LeZion 5,787-6,131 against 5,273). The {n_all} tier-3 edits (`"tier": 3`, n continuing the numbering after tier 2, same
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

**Counts: {tot['replaced']} replaced with the CBS value, {tot['removed']} number removed (sentence or cell kept), {tot['deleted']} sentence, row, column, table or paragraph deleted
({n_all} edits on 22 pages).**

| page | id | CBS row | tier-3 edits | replaced | removed | deleted |
|---|---|---|---|---|---|---|
""" + "\n".join(per) + f"""

**Official source used** (the same table as tier 2; every replacement line below carries its URL): CBS table 4.9, "Average monthly free-market rent (NIS) by
residential district, big city and size group (rooms)", Q2 2026 (April-June), Price Statistics Monthly No. 7/2026: {u['table_he_pdf']}. Figures are in
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
tier-3 edits, in order, to the live `content.rendered`: **{n_all} of {n_all} `old` strings match exactly once** (whole tables through their anchor), re-fetched {VERIFIED};
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
the affected edits are: {EX}.
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

""" + "\n".join(lines) + f"""
{END}
"""

io.open(os.path.join(HERE, "tier3_ceo_section.md"), "w", encoding="utf-8", newline="\n").write(md)
rp = os.path.join(D, "README.md")
rd = io.open(rp, encoding="utf-8", newline="").read()
if START in rd:
    a, b = rd.index(START), rd.index(END) + len(END)
    rd = rd[:a].rstrip("\n") + "\n\n" + md.rstrip("\n") + rd[b:]
else:
    k = rd.index("\n## Files")
    rd = rd[:k].rstrip("\n") + "\n\n" + md.rstrip("\n") + "\n" + rd[k:]
io.open(rp, "w", encoding="utf-8", newline="\n").write(rd)
print("section written;", n_all, "lines;", len(lines))
