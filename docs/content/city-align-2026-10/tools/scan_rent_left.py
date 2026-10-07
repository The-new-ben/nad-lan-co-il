# -*- coding: utf-8 -*-
"""List the rent figures (1,000-20,000 near the words rent / שכירות / שכר דירה) that still stand in the body of the 24 pages after tier 1 (live) and the
tier-2 edits of docs/content/city-align-2026-10 are applied. Fetches the live pages, applies the tier-2 edits in order, scans the visible text outside the
price list, scripts and styles. Writes tools/rent_lines_left_after_tier2.json (data only, nothing is applied anywhere).
python scan_rent_left.py"""
import io, json, os, re, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from blocks import strip_ranges
D = os.path.dirname(HERE)
CBS = json.load(io.open(os.path.join(HERE, "cbs_rent_2026_q2.json"), encoding="utf-8"))
CITY = {"ashdod": "אשדוד", "ashkelon": "אשקלון", "beer-sheva": "באר שבע", "bnei-brak": "בני ברק", "bat-yam": "בת ים", "herzliya": "הרצליה", "holon": "חולון",
        "haifa": "חיפה", "jerusalem": "ירושלים", "kfar-saba": "כפר סבא", "netanya": "נתניה", "petah-tikva": "פתח תקוה", "rishon-lezion": "ראשון לציון",
        "rehovot": "רחובות", "ramat-gan": "רמת גן", "tel-aviv": "תל אביב"}


def visible(h):
    for s, e, k in sorted(strip_ranges(h), reverse=True):
        h = h[:s] + " " + h[e:]
    h = re.sub(r"</t[dh]>", " | ", h)
    h = re.sub(r"</tr>", " // ", h)
    h = re.sub(r"</p>|</li>|</h\d>", "\n", h)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"[ \t]+", " ", h)


out, total = {}, 0
for fn in sorted(os.listdir(D)):
    if not fn.endswith(".align-edits.json"):
        continue
    slug = fn[:-len(".align-edits.json")]
    J = json.load(io.open(os.path.join(D, fn), encoding="utf-8"))
    u = "https://nad-lan.co.il/wp-json/wp/v2/pages/%d?_fields=id,content&nlca=%d" % (J["page"]["id"], time.time())
    t = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 NadLan-cityalign"}), timeout=90).read().decode("utf-8"))["content"]["rendered"]
    for e in J["edits"]:
        if e.get("tier") != 2:
            continue
        if e.get("spans_tags"):
            i = t.find(e["anchor"])
            a, z = t.rfind("<table", 0, i), t.find("</table>", i) + 8
            t = t[:a] + e["new"] + t[z:]
        else:
            t = t.replace(e["old"], e["new"])
    lines = []
    for line in re.split(r"\n|\s//\s", visible(t)):
        if re.search(r"שכירות|שכר דיר|דמי שכירות|מושכר", line):
            nums = [x for x in re.findall(r"(?<![\d,.])\d{1,2},\d{3}(?![\d,])", line) if 1000 <= int(x.replace(",", "")) <= 20000]
            if nums:
                lines.append({"numbers": nums, "text": line.strip()[:220]})
    base = slug.replace("-apartment-prices", "")
    row = CBS["rows"].get(CITY.get(base, ""))
    out[slug] = {"lines": lines, "cbs_city_row": bool(row), "cbs_city_average_q2_2026": row["total"] if row else None}
    total += len(lines)
    print(f"{base:16s} lines {len(lines):3d}  CBS city row {'yes' if row else 'no '}  CBS average {row['total'] if row else '-'}")
io.open(os.path.join(HERE, "rent_lines_left_after_tier2.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(
    {"what": "rent figures (1,000-20,000) still in the body after tier 1 (live) and tier 2 (CEO rule) are applied; lines include the CBS figures added by tier 2",
     "pages": out}, ensure_ascii=False, indent=1) + "\n")
print("total lines", total)
