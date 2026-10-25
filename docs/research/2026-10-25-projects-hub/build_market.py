# -*- coding: utf-8 -*-
"""market.json (research, 566 projects in marketing as published, 25.10.2026) -> plugins/nadlan-config/data/projects-market.json,
the data the /projects/ hub reads. Keeps only the fields the page shows (no source URLs on the page: the evidence stays in
_private-research); links a project to its own page on nad-lan.co.il when we have one (matched by a distinctive name and the
city, printed for review). Unknown stays empty.
  python docs/research/2026-10-25-projects-hub/build_market.py"""
import io, json, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
OUT = os.path.join(REPO, "plugins", "nadlan-config", "data", "projects-market.json")
src = json.load(io.open(os.path.join(H, "market.json"), encoding="utf-8"))

# our page -> (patterns that must match the market name, city must contain)
OURS = [
    ("/projects/rainbow-tel-aviv/", [r"rainbow", r"ריינבו"], "תל אביב"),
    ("/projects/duo-tel-aviv/", [r"\bduo\b", r"דואו"], "תל אביב"),
    ("/projects/ashira-sde-dov/", [r"ashira", r"אשירה"], "תל אביב"),
    ("/projects/dimri-yama-sde-dov/", [r"yama\s*tlv", r"dimri\s*yama", r"ימה\s*תל", r"YAMA TLV"], "תל אביב"),
    ("/projects/h-infinity-somail-tel-aviv/", [r"infinity", r"אינפיניטי"], "תל אביב"),
    ("/projects/six-8-herbert-samuel-tel-aviv/", [r"six-?8", r"הרברט סמואל"], "תל אביב"),
    ("/projects/yoo-tel-aviv/", [r"\byoo\b"], "תל אביב"),
    ("/projects/gindi-vogue-sde-dov/", [r"vogue", r"ווג"], "תל אביב"),
    ("/projects/zohi-sde-dov/", [r"zohi", r"זוהי"], "תל אביב"),
    ("/projects/first-sde-dov/", [r"\bfirst\b"], "תל אביב"),
    ("/projects/utopia-sde-dov/", [r"utopia", r"אוטופיה"], "תל אביב"),
    ("/projects/einstein-tower/", [r"einstein\s*tower", r"מגדל איינשטיין"], "תל אביב"),
    ("/projects/recanati-residence/", [r"recanati", r"רקנאטי"], "תל אביב"),
    ("/projects/aurelia/", [r"aurelia", r"אורליה"], "תל אביב"),
    ("/projects/meier-on-rothschild/", [r"מאייר", r"meier"], "תל אביב"),
    ("/projects/park-bavli/", [r"פארק בבלי"], "תל אביב"),
    ("/projects/akirov-towers/", [r"אקירוב"], "תל אביב"),
    ("/projects/marina-towers-herzliya/", [r"מגדלי המרינה"], "הרצליה"),
    ("/projects/hamedina/", [r"מגדלי כיכר המדינה"], "תל אביב"),
]
ST = {"presale", "marketing", "construction", "near_occupancy", "immediate"}


def clean(s):
    """one space between words; the long dashes of published names become a plain hyphen (no long dash on the site)"""
    return re.sub(r"\s+", " ", str(s).replace("–", "-").replace("—", "-")).strip() if s not in (None, "") else ""


def note(s):
    """The price note keeps only what describes the price (rooms, presale, last units); where it was read stays in the evidence file."""
    s = clean(s)
    s = re.sub(r"\((?:[^()]*?)(?:יד2|ice|מרכז הנדל|כתבה)[^()]*\)", "", s)
    s = re.sub(r"\b(?:יד2|ice)\b", "", s)
    s = re.sub(r",?\s*כתבה[^,]*", "", s)
    s = re.sub(r"^החל מ[,\s]*", "", s).strip(" ,;")
    if s.startswith("פרויקט") or len(s) > 40 or ";" in s:
        return ""
    return s


rows, matched = [], []
for p in src:
    name = clean(p.get("name")); city = clean(p.get("city"))
    if not name or not city:
        continue
    url = ""
    hay = (name + " " + clean(p.get("name_en"))).lower()
    for path, pats, c in OURS:
        if c in city and any(re.search(x, hay, re.I) for x in pats):
            url = path; matched.append((name, city, path)); break
    pr = p.get("price_from"); ps = p.get("price_psqm")
    row = {
        "name": name, "city": city, "neighbourhood": clean(p.get("neighbourhood")), "developer": clean(p.get("developer")),
        "rooms": clean(p.get("rooms")), "price_from": int(pr) if isinstance(pr, (int, float)) and pr > 100000 else None,
        "price_note": note(p.get("price_note")), "price_psqm": int(ps) if isinstance(ps, (int, float)) and ps > 1000 else None,
        "deal": clean(p.get("deal")), "status": p.get("status") if p.get("status") in ST else "", "delivery": clean(p.get("delivery")),
        "renewal": clean(p.get("renewal")), "src": clean(p.get("source_type")),
    }
    if url:
        row["url"] = url
    rows.append({k: v for k, v in row.items() if v not in ("", None)})
data = {"read": "2026-10-25", "note": "projects in marketing as their developers publish them (developer sites and the developers' marketing listings); built by build_market.py", "projects": rows}
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
print("written", OUT, len(rows), "projects", os.path.getsize(OUT), "bytes")
print("priced:", sum(1 for r in rows if r.get("price_from")), "| Tel Aviv:", sum(1 for r in rows if "תל אביב" in r["city"]), "| linked to our pages:", len(matched))
for m in matched:
    print("  link:", m[0], "|", m[1], "->", m[2])
