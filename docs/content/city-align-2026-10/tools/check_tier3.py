# -*- coding: utf-8 -*-
"""Check the TIER-3 edits (listing-site rents, CEO rule of 7.10.2026) of docs/content/city-align-2026-10/<slug>.align-edits.json against the LIVE page.

Tier 1 and tier 2 are already live, so only the tier-3 edits are applied, in the listed order, on the current content.rendered.
Checks: every old matches exactly once (whole tables through their anchor); fields present; no em/en dash, "!", HTML entity, newspaper name in new; every number
in new is in old, in kept_numbers, an official city-file number or a CBS table 4.9 figure (rounded half up or one decimal); source_keys resolve; ceo_action /
source_url consistent (replaced = cbs.gov.il source_url, nothing else has one); typography of the touched text (double spaces, space before punctuation,
unbalanced brackets, empty paragraphs and cells); tag balance of the result; tier-1 and tier-2 'new' texts still present unless a tier-3 edit overlaps them;
RESIDUAL SCAN: every block of the result with a rent word and a 1,000-20,000 figure is listed unless all its figures are CBS table 4.9 figures.

python check_tier3.py [slug ...] [--live-dir DIR] [--quiet]
"""
import html, io, json, os, re, sys, time, urllib.request
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check as C  # official_numbers, resolve_key, numbers_in, NEWSPAPERS, apply_edit
from blocks import strip_ranges, blocks

OUTDIR = C.OUTDIR
CBS = json.load(io.open(os.path.join(HERE, "cbs_rent_2026_q2.json"), encoding="utf-8"))
ARGS = sys.argv[1:]
LIVE_DIR = ARGS[ARGS.index("--live-dir") + 1] if "--live-dir" in ARGS else None
QUIET = "--quiet" in ARGS
CITY_HE = {"ashdod": "אשדוד", "ashkelon": "אשקלון", "beer-sheva": "באר שבע", "bnei-brak": "בני ברק", "bat-yam": "בת ים", "herzliya": "הרצליה", "holon": "חולון",
           "haifa": "חיפה", "jerusalem": "ירושלים", "kfar-saba": "כפר סבא", "netanya": "נתניה", "petah-tikva": "פתח תקוה", "rishon-lezion": "ראשון לציון",
           "rehovot": "רחובות", "ramat-gan": "רמת גן", "tel-aviv": "תל אביב"}
RENT_WORDS = re.compile(r"שכירות|שכר דיר|שכ\"ד|שוכר|מושכר|להשכיר|השכר|תשואה|שכירו")
# a rent figure = a 1,000-20,000 number (or the first of a range) that carries a currency marker
FIG = re.compile(r"(?<![\d,.])(\d{1,2},\d{3})(?![\d,])(?=(?:\s*(?:-|–|עד|ל-)\s*\d{1,2},\d{3})?\s*(?:₪|ש\"ח|ש״ח|שקל))")


def cbs_numbers():
    vals = set()

    def add(v):
        if v is None:
            return
        vals.add(f"{int(Decimal(str(v)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)):,}")
        vals.add(f"{v:,.1f}")
    for r in CBS["rows"].values():
        add(r["total"])
        for g in r["groups"].values():
            add(g)
    vals.add(str(CBS["dwellings_share"]["tel_aviv_district_pct"]))
    return vals


def resolve_cbs(key):
    m = re.fullmatch(r"cbs_rent\[(.+?)\]\.(total|1-2|2\.5-3|3\.5-4|4\.5\+)\.q2_2026", key)
    if m:
        row = CBS["rows"].get(m.group(1))
        if not row:
            return False
        return (row["total"] if m.group(2) == "total" else row["groups"].get(m.group(2))) is not None
    return key == "cbs_dwellings[מחוז תל אביב].share_2025"


def live_page(slug, pid):
    if LIVE_DIR:
        return json.load(io.open(os.path.join(LIVE_DIR, slug + ".json"), encoding="utf-8"))
    u = "https://nad-lan.co.il/wp-json/wp/v2/pages/%d?_fields=id,link,modified,content&nlca=%d" % (pid, time.time())
    p = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 NadLan-cityalign"}), timeout=90).read().decode("utf-8"))
    p["retrieved_utc"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    return p


def tag_balance(h):
    """open/close counts of the structural tags outside script, style and the price list"""
    for s, e, kind in sorted(strip_ranges(h), reverse=True):
        h = h[:s] + " " + h[e:]
    res = {}
    for t in ("p", "table", "thead", "tbody", "tr", "td", "th", "div", "h2", "h3", "li", "ul", "ol", "details", "summary"):
        o = len(re.findall(r"<%s(?:\s[^>]*)?>" % t, h))
        c = len(re.findall(r"</%s>" % t, h))
        res[t] = (o, c)
    return res


def typo_issues(new):
    out = []
    plain = re.sub(r"<[^>]+>", "", new)
    for pat, name in ((r"(?<=\S) {2,}(?=\S)", "double space"), (r" [,.;:]", "space before punctuation"), (r",,|\.\.|,\.|\.,", "doubled punctuation"),
                      (r'ש"ח ש"ח|₪ ₪|ש״ח ש״ח', "doubled currency"), (r"\(\s|\s\)", "space inside bracket"), (r"-\s*-", "doubled hyphen")):
        if re.search(pat, plain):
            out.append(name)
    if plain.count("(") != plain.count(")"):
        out.append("unbalanced brackets")
    if re.search(r"<p[^>]*>\s*</p>|<td[^>]*>\s*</td>|<li[^>]*>\s*</li>", new):
        out.append("empty element")
    return out


def check(slug):
    J = json.load(io.open(os.path.join(OUTDIR, slug + ".align-edits.json"), encoding="utf-8"))
    d = json.load(io.open(os.path.join(C.CITIES, slug + ".json"), encoding="utf-8"))
    t3 = [e for e in J["edits"] if e.get("tier") == 3]
    if not t3:
        return None
    page = live_page(slug, J["page"]["id"])
    live = page["content"]["rendered"]
    text = live
    offs = C.official_numbers(d) | cbs_numbers()
    cbsn = cbs_numbers()
    errs, warns, left = [], [], []
    for tier in (1, 2):
        keep = [e for e in J["edits"] if e.get("tier", 1) == tier]
        n_in = sum(1 for e in keep if e["new"] in live)
        if n_in != len(keep):
            errs.append(f"tier {tier} not fully live: {n_in} of {len(keep)} 'new' texts found")
    ns = [e["n"] for e in J["edits"]]
    if ns != list(range(1, len(ns) + 1)):
        errs.append(f"edit numbers not 1..N: {ns[:5]}...")
    counts = {"replaced": 0, "removed": 0, "deleted": 0}
    bal0 = tag_balance(live)
    city_cbs = set()
    row = CBS["rows"].get(CITY_HE.get(slug.replace("-apartment-prices", ""), ""))
    if row:
        for v in [row["total"]] + list(row["groups"].values()):
            if v is not None:
                city_cbs.add(f"{int(Decimal(str(v)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)):,}")
    for e in t3:
        n = e["n"]
        for f in ("page_id", "field", "old", "new", "source_keys", "verdict", "audit_verdict", "why", "tier", "raw_risk", "ceo_action", "ceo_note", "matches_in_live"):
            if f not in e:
                errs.append(f"#{n} missing {f}")
        if e.get("page_id") != page["id"]:
            errs.append(f"#{n} page_id")
        # the edit must not touch the price list (<section id="nlpg">), a script or a style
        probe = e.get("anchor") if e.get("spans_tags") else e["old"]
        rng_now = strip_ranges(text)
        for m0 in re.finditer(re.escape(probe), text):
            for s0, e0, kind in rng_now:
                if s0 <= m0.start() < e0:
                    errs.append(f"#{n} {'anchor' if e.get('spans_tags') else 'old'} sits inside {kind}")
        text2, cnt, note = C.apply_edit(text, e)
        if cnt == -1 or (note and not e.get("spans_tags")):
            errs.append(f"#{n} {note}: {e['old'][:70]!r}")
        elif e.get("spans_tags") and e["old"] not in text:
            errs.append(f"#{n} whole table: old string does not match the live table exactly")
        text = text2
        new, old = e["new"], e["old"]
        for bad in ("—", "–", "!", "&#", "&quot;", "&amp;", "&nbsp;"):
            if bad in new and bad not in old:
                errs.append(f"#{n} new contains {bad!r}")
        low = re.sub(r"(בכל|ברחבי|רחבי|כל) הארץ", " ", new.lower())
        for w in C.NEWSPAPERS:
            if w.lower() in low and w.lower() not in old.lower():
                errs.append(f"#{n} new names a newspaper/site: {w}")
        oldnums = set(C.numbers_in(old)) | set(x.replace(",", "") for x in C.numbers_in(old))
        kept = set(str(x) for x in e.get("kept_numbers", []))
        for x in C.numbers_in(re.sub(r"<[^>]+>", " ", new)):
            xs = x.replace(",", "")
            if x in oldnums or xs in oldnums or x in kept or x in offs or xs in offs:
                continue
            if re.fullmatch(r"20[12]\d", xs) or (xs.isdigit() and int(xs) <= 12) or x in ("2.5", "3.5", "4.5"):
                continue
            errs.append(f"#{n} number {x} in new is not in old, not official, not kept")
        for k in e.get("source_keys", []):
            if not (C.resolve_key(d, k) or resolve_cbs(k)):
                errs.append(f"#{n} source_key does not resolve: {k}")
        act = e.get("ceo_action")
        if act not in counts:
            errs.append(f"#{n} ceo_action {act!r}")
        else:
            counts[act] += 1
        if act == "replaced":
            if not e.get("source_url", "").startswith("https://www.cbs.gov.il/"):
                errs.append(f"#{n} replaced without a cbs.gov.il source_url")
            if not any(x in cbsn for x in C.numbers_in(re.sub(r"<[^>]+>", " ", new))):
                errs.append(f"#{n} replaced but no CBS figure appears in new")
            if not re.search(r"הלשכה המרכזית לסטטיסטיקה|הלמ.ס", new):
                errs.append(f"#{n} replaced but the CBS is not named in new")
            if "רבעון" not in new and "אפריל עד יוני" not in new:
                warns.append(f"#{n} replaced without the quarter in this text (check the header or the neighbouring sentence)")
        if act != "replaced" and e.get("source_url"):
            errs.append(f"#{n} source_url on a non-replaced edit")
        if act == "deleted" and new.strip() and not e.get("spans_tags") and len(new) > 0.8 * len(old):
            warns.append(f"#{n} 'deleted' but new is almost as long as old")
        if e.get("tier") != 3:
            errs.append(f"#{n} tier")
        t = typo_issues(new)
        if t:
            errs.append(f"#{n} typography in new: {', '.join(t)}")
        if e.get("spans_tags") and new.strip():
            sig = lambda h: set(re.findall(r"<(?:table|thead|tbody|tr|th|td)[^>]*>", h))
            extra = sig(new) - sig(old)
            if extra:
                errs.append(f"#{n} rebuilt table uses tags/attributes the old table did not: {sorted(extra)[:3]}")
        # numbers that left this edit must be listing-site rents, never an official figure
        for x in set(C.numbers_in(old)) - set(C.numbers_in(new)):
            if x in city_cbs and x not in C.numbers_in(new):
                warns.append(f"#{n} removed {x}, which equals a CBS figure (check that it was not already the CBS value)")
    # tier 1 / tier 2 texts survive
    for e in J["edits"]:
        if e.get("tier", 1) in (1, 2) and not e.get("spans_tags") and e["new"] not in text and e["new"] in live:
            warns.append(f"tier {e.get('tier', 1)} #{e['n']} 'new' text is changed by a tier-3 edit (overlap)")
    # typography across the edit boundaries: the visible text must not gain a space before punctuation, a doubled space or doubled punctuation
    def vis_text(h):
        for s0, e0, kind in sorted(strip_ranges(h), reverse=True):
            h = h[:s0] + " " + h[e0:]
        h = re.sub(r"</t[dh]>|</tr>|</p>|</li>|</h\d>|<br\s*/?>", "\n", h)
        return html.unescape(re.sub(r"<[^>]+>", "", h))
    v0, v1 = vis_text(live), vis_text(text)
    for pat, name in ((r"[^\S\n]+[,.;:](?=\s|$)", "space before punctuation"), (r"[^\S\n]{2,}", "double space"), (r",,|\.\.|,\.|\.,", "doubled punctuation"),
                      (r"\(\s|\s\)", "space inside bracket")):
        a, b = len(re.findall(pat, v0)), len(re.findall(pat, v1))
        if b > a:
            ctx = [v1[max(0, m.start() - 40):m.end() + 40].replace("\n", "/") for m in re.finditer(pat, v1)][:3]
            errs.append(f"{name}: {a} -> {b} in the visible text after tier 3, e.g. {ctx}")
    # tag balance
    bal1 = tag_balance(text)
    for t in bal1:
        if bal1[t][0] != bal1[t][1]:
            errs.append(f"unbalanced <{t}> after tier 3: open {bal1[t][0]} close {bal1[t][1]}")
    # residual scan: sentence by sentence (table rows are one sentence), so a rent word and a figure must sit in the same sentence
    bl, _ = blocks(text)
    for k, b in enumerate(bl):
        sents = [b["text"]] if b["tag"] == "tr" else re.split(r"(?<=[.!?])\s+", b["text"])
        for tx in sents:
            if not RENT_WORDS.search(tx):
                continue
            nums = []
            for m in FIG.finditer(tx):
                x = m.group(1)
                tail = tx[m.end():m.end() + 40]
                if re.match(r"(?:\s*(?:-|\u2013|עד|ל-)\s*[\d,]+)?\s*(?:₪|ש\"ח|ש\u05f4ח|שקל)\s*(?:למ\"ר|למ\u05f4ר)", tail):
                    continue  # a price per m2, not a rent
                if 1000 <= int(x.replace(",", "")) <= 20000 and x not in cbsn:
                    nums.append(x)
            if nums:
                left.append((k, nums, tx[:200]))
    # tables whose header names a rent: every figure in their rows counts (rows of a rent table need no rent word of their own)
    rng_final = strip_ranges(text)
    for tm in re.finditer(r"<table\b.*?</table>", text, re.S):
        if any(s0 <= tm.start() < e0 for s0, e0, kind in rng_final):
            continue
        rows = re.findall(r"<tr\b.*?</tr>", tm.group(0), re.S)
        cells = [[html.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", r, re.S)] for r in rows]
        if not cells or not RENT_WORDS.search(" ".join(cells[0])):
            continue
        for r in cells[1:]:
            tx = " | ".join(r)
            nums = []
            for m in FIG.finditer(tx):
                x = m.group(1)
                tail = tx[m.end():m.end() + 40]
                if re.match(r"(?:\s*(?:-|–|עד|ל-)\s*[\d,]+)?\s*(?:₪|ש\"ח|ש״ח|שקל)\s*(?:למ\"ר|למ״ר)", tail):
                    continue
                if 1000 <= int(x.replace(",", "")) <= 20000 and x not in cbsn:
                    nums.append(x)
            if nums and not any(nums == l[1] and tx[:60] == l[2][:60] for l in left):
                left.append(("table", nums, tx[:200]))
    # references to a table / list that may have been deleted
    return {"slug": slug, "errs": errs, "warns": warns, "left": left, "counts": counts, "n": len(t3), "retrieved": page.get("retrieved_utc"),
            "modified": page.get("modified"), "chars_before": len(live), "chars_after": len(text), "text": text}


if __name__ == "__main__":
    slugs = [a for a in ARGS if not a.startswith("--") and a != LIVE_DIR]
    if not slugs:
        slugs = sorted(f[:-len(".align-edits.json")] for f in os.listdir(OUTDIR) if f.endswith(".align-edits.json"))
    tot = {"replaced": 0, "removed": 0, "deleted": 0}
    bad = nleft = pages = 0
    for s in slugs:
        r = check(s)
        if not r:
            continue
        pages += 1
        for k in tot:
            tot[k] += r["counts"][k]
        bad += len(r["errs"])
        nleft += len(r["left"])
        print(f"[{s}] tier-3 edits {r['n']} | replaced {r['counts']['replaced']} removed {r['counts']['removed']} deleted {r['counts']['deleted']} | "
              f"errors {len(r['errs'])} | warnings {len(r['warns'])} | rent figures still in the body {len(r['left'])} | live {r['retrieved']} UTC, modified {r['modified']}")
        for x in r["errs"]:
            print("  ERR", x)
        if not QUIET:
            for x in r["warns"]:
                print("  warn", x)
        for k, nums, tx in r["left"]:
            print(f"  LEFT [{k}] {nums}: {tx}")
    print("TOTAL pages", pages, tot, "errors", bad, "rent figures left", nleft)
