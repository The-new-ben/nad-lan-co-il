# -*- coding: utf-8 -*-
"""Write tools/tier2_ceo_section.md (the README section 'Tier 2 under the CEO rule (7.10.2026)', one line per edit, generated from the
14 JSON files) and put it into README.md before '## Files' (between the markers; re-running replaces it).
python gen_tier2_section.py [verified_utc]"""
import io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.dirname(HERE)
CBS = json.load(io.open(os.path.join(HERE, "cbs_rent_2026_q2.json"), encoding="utf-8"))
VERIFIED = sys.argv[1] if len(sys.argv) > 1 else "7.10.2026 12:04 UTC"
LIVE13 = ["tel-aviv", "jerusalem", "haifa", "herzliya", "netanya", "ramat-gan", "bat-yam", "hod-hasharon", "ashdod", "petah-tikva",
          "ashkelon", "eilat", "kiryat-ono"]
OTHER = ["beer-sheva", "bnei-brak", "givatayim", "holon", "kfar-saba", "modiin", "raanana", "ramat-hasharon", "rehovot", "rishon-lezion"]
ORDER = [s + "-apartment-prices" for s in LIVE13 + OTHER] + ["apartment-prices"]
START, END = "<!-- tier2-ceo:start -->", "<!-- tier2-ceo:end -->"

lines, tot, per_slug = [], {"replaced": 0, "removed": 0, "deleted": 0}, {}
for slug in ORDER:
    fn = os.path.join(D, slug + ".align-edits.json")
    J = json.load(io.open(fn, encoding="utf-8"))
    for e in J["edits"]:
        if e.get("tier") != 2:
            continue
        a = e["ceo_action"]
        tot[a] += 1
        per_slug.setdefault(slug, {"replaced": 0, "removed": 0, "deleted": 0})[a] += 1
        src = f" Source: {e['source_url']}" if e.get("source_url") else ""
        lines.append(f"- `{slug}`, n{e['n']} ({a}): {e['ceo_note']}.{src}")

rep = [(s, [e["n"] for e in json.load(io.open(os.path.join(D, s + ".align-edits.json"), encoding="utf-8"))["edits"]
            if e.get("tier") == 2 and e["ceo_action"] == "replaced"]) for s in per_slug]
rep = [(s.replace("-apartment-prices", ""), n) for s, n in rep if n]
dele = [(s.replace("-apartment-prices", ""), [e["n"] for e in json.load(io.open(os.path.join(D, s + ".align-edits.json"), encoding="utf-8"))["edits"]
                                           if e.get("tier") == 2 and e["ceo_action"] == "deleted"]) for s in per_slug]
dele = [(s, n) for s, n in dele if n]
fmt = lambda xs: "; ".join(f"{s} " + ", ".join(map(str, n)) for s, n in xs)
u = CBS["urls"]
md = f"""{START}
## Tier 2 under the CEO rule (7.10.2026)

DATA ONLY, like the rest of this folder: nothing was applied, no WordPress write, no commit, no push. The 52 tier-2 edits (rent, percentage and
renovation-cost figures with no dated source) were rebuilt under the CEO's rule of 7.10.2026. The 312 tier-1 edits are untouched; tier 1 is live
(every tier-1 `new` text is on the 14 live pages), so the tier-2 `old` strings were re-checked against the live content, not the audited copy.

**The rule.** (1) If an official, dated value exists for the same thing, the number is replaced by it, with its period: rents from the Central
Bureau of Statistics (CBS) average-rent table, sale prices from the city files (Tax Authority, data.nadlan.gov.il). (2) If none exists the number is
removed. The sentence or cell stays only as advice or a hedged statement that makes no price-level claim ("a renovation may be needed", "check against
similar deals"); a statement of level ("rent here is above the city average", "usually lower than new") needs an official figure, and without one it is
deleted, with the row or column that had no value without the number. (3) No number invented, no newspaper named, titles, H1s and headings untouched.

**Counts: {tot['replaced']} replaced with an official value, {tot['removed']} number removed (sentence or cell kept), {tot['deleted']} sentence, row or column deleted.**
Replaced: {fmt(rep)}. Deleted: {fmt(dele)}.

**Official sources used** (the only new ones; every replacement line below carries its URL):
- CBS table 4.9, "Average monthly free-market rent (NIS) by residential district, big city and size group (rooms)", latest quarter IV-VI 2026
  (Q2 2026, April-June), Price Statistics Monthly No. 7/2026: {u['table_he_pdf']} (Hebrew; English version `a4_9_e.pdf` in the same folder). Issue 8/2026
  (`price08a`) holds the identical table; `price09a` answered 404 on 7.10.2026, so Q2 2026 is the latest published quarter. The table is in
  `tools/cbs_rent_2026_q2.json` (Israel, 6 districts, 18 big cities; the Hebrew and English PDFs hold the same 1,107 price figures). The size groups are
  the CBS groups (1-2, 2.5-3, 3.5-4 and 4.5+ rooms; a 3-room flat sits in 2.5-3, a 4-room flat in 3.5-4, a 5-room flat in 4.5+) and the text rounds the
  published one-decimal average to whole shekels, half up (Herzliya 6,774.5 becomes 6,775). Since Q1 2026 the top group is "4.5+" (all larger sizes).
- CBS press release 021/2026 of 19.1.2026, "דירות ומבנים בישראל, 2025" (dwelling register, July 2025): the Tel Aviv district holds 19.5% of Israel's
  dwellings: {CBS['dwellings_share']['url']}
- Sale prices: the city files only (Herzliya edit 12 keeps the 3-room median 2,793,600, 1-3.2026).

**Where there is no official figure.** The CBS big-city list has no Eilat, Givatayim, Hod HaSharon, Kiryat Ono, Raanana, Ramat HaSharon or Modiin row, and its
rent table has no neighbourhood rents and no rent medians. For yields, renovation costs, per-m2 prices, new-vs-second-hand premiums and negotiation gaps no
official dated figure was found (the city files hold deal medians by rooms only), so those numbers are removed. Herzliya and Haifa lose their rent median
and every neighbourhood rent; the CBS publishes city averages only.

**Verification.** `python tools/check_tier2.py` fetches each page and applies only the tier-2 edits, in the listed order, to the live
`content.rendered`: **52 of 52 `old` strings match exactly once** (whole tables through their anchor), checked on copies fetched 7.10.2026 11:42 UTC and
again {VERIFIED}; no page changed in between (modified stamps unchanged). Every number in a new text is in the old text, a city file or the CBS table;
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

{chr(10).join(lines)}

**Outside the 52 edits, not touched.** A scan of the pages as they will stand after tier 1 and tier 2 (`python tools/scan_rent_left.py`, output
`tools/rent_lines_left_after_tier2.json`) still finds rent figures between 1,000 and 20,000 in the body: lenient keeps from named, dated, non-official
samples (listing pages checked 5-6.6.2026), explicit "if" examples, and the CBS lines added here. For cities with a CBS row several differ from the CBS
average (for example Ramat Gan "average about 6,411" against 5,894 in Q2 2026, Rishon LeZion averages 5,787-6,131 against 5,273); a follow-up pass could replace them under the same rule.
{END}
"""
io.open(os.path.join(HERE, "tier2_ceo_section.md"), "w", encoding="utf-8", newline="\n").write(md)

fn = os.path.join(D, "README.md")
R = io.open(fn, encoding="utf-8", newline="").read().replace("\r\n", "\n")
R = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n\n?", "", R, flags=re.S)
i = R.index("## Files")
R = R[:i] + md + "\n" + R[i:]
# pointer in the older tier-2 bullet
ptr = ' Superseded by the section "Tier 2 under the CEO rule (7.10.2026)" below: an official figure replaces the number wherever one exists.'
if ptr.strip() not in R:
    R = R.replace("remove renovation costs, new-flat premiums and negotiation percentages.", "remove renovation costs, new-flat premiums and negotiation percentages." + ptr, 1)
files_old = "`check.py` (dry run and number trace), `gen_readme.py` (summary tables)."
files_new = ("`check.py` (dry run and number trace), `gen_readme.py` (summary tables). Tier 2 under the CEO rule: `cbs_rent_2026_q2.json` (CBS table 4.9), "
             "`b_tier2_ceo.py` (rebuilds the tier-2 edits), `check_tier2.py` (applies them to the live pages), `gen_tier2_section.py` and `tier2_ceo_section.md` "
             "(this README section), `scan_rent_left.py` (rent figures still in the body).")
if "cbs_rent_2026_q2.json" not in R.split("## Files")[1]:
    R = R.replace(files_old, files_new, 1)
io.open(fn, "w", encoding="utf-8", newline="\n").write(R)
print("section", len(md), "chars; README", len(R), "chars; lines", len(lines), tot)
