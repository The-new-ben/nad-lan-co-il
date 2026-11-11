# -*- coding: utf-8 -*-
"""HAD-712 (Ben 11.11.2026: "Calculator and images"). The Hebrew Kikar article (/projects/hamedina/, post 8113) had no picture in its
body (3 images on a page of 58 phone screens). It gains 7 figures, 18 pictures, each beside the text it shows. Every picture is a render
from our own scene of the square (Blender; the same pictures the showroom and the apartment screen use), copied under descriptive
names into assets/project-stage/hamedina/gallery/ (release 1.72.648), and every figure says "הדמיה להמחשה" in its caption: none is a
photograph or an official specification. Styles: .nlws-fig (inc/project-stage.php, 1.72.648; the Claude Design board "C2").
Small anchored insertions on the LIVE post text; the live md5 is pinned; each anchor must appear exactly once. Backup before, read-back
after (restored if it differs); dry by default.   python scripts/kikar/had712_images.py [--go] [--dump out.json]"""
import hashlib, io, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
PID, SLUG, PIN = 8113, "hamedina", "fca74aa6882cf21f3b7e229dc29be405"  # modified 2026-11-11T17:37:59 (the content round)
G = "https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/project-stage/hamedina/gallery/"
P = "במגדלי כיכר המדינה"


def img(f, alt, w, h):
    return '<img src="%s%s" alt="%s" width="%d" height="%d" loading="lazy" decoding="async">' % (G, f, alt, w, h)


def cell(f, alt, w, h, label):
    return '<span class="nlws-fig__i">' + img(f, alt, w, h) + "<b>" + label + "</b></span>"


def fig(inner, cap):
    return '<figure class="nlws-fig">' + inner + "<figcaption>" + cap + "</figcaption></figure>"


def grid(n, cells):
    return '<div class="nlws-fig__g nlws-fig__g--%d">' % n + "".join(cells) + "</div>"


L = "<b>הדמיה להמחשה.</b> "
F_AERIAL = fig(img("kikar-hamedina-towers-aerial.webp", "שלושת מגדלי כיכר המדינה בתוך הכיכר בתל אביב, מבט מהאוויר", 1600, 1000),
               L + "שלושת מגדלי כיכר המדינה בתוך הכיכר, מבט מהאוויר לכיוון הים.")
F_TOWERS = fig(grid(3, [cell("kikar-hamedina-tower-a.webp", "מגדל A " + P + ", 40 קומות", 756, 1080, "מגדל A"),
                        cell("kikar-hamedina-tower-b.webp", "מגדל B " + P + ", 37 קומות", 756, 1080, "מגדל B"),
                        cell("kikar-hamedina-tower-c.webp", "מגדל C " + P + ", 40 קומות", 756, 1080, "מגדל C")]),
               L + "כל מגדל לבדו: A ו-C בני 40 קומות, B בן 37 קומות.")
F_BALCONY = fig(img("kikar-hamedina-balcony.webp", "מבט ממרפסת בקומה 30 במגדל C " + P + ", לכיוון מערב", 1200, 675),
                L + "מבט ממרפסת בקומה 30 במגדל C, לכיוון מערב, לקראת שקיעה.")
F_DIRS = fig(grid(2, [cell("kikar-hamedina-floor-30-north.webp", "המבט צפונה מקומה 30 " + P, 640, 360, "צפון"),
                      cell("kikar-hamedina-floor-30-east.webp", "המבט מזרחה מקומה 30 " + P, 640, 360, "מזרח"),
                      cell("kikar-hamedina-floor-30-south.webp", "המבט דרומה מקומה 30 " + P, 640, 360, "דרום"),
                      cell("kikar-hamedina-floor-30-west.webp", "המבט מערבה מקומה 30 " + P, 640, 360, "מערב")]),
             L + "המבט מקומה 30 במגדל C לארבעה כיוונים. הנוף מדירה מסוימת תלוי במגדל, בקומה ובכיוון.")
F_FLOORS = fig(grid(3, [cell("kikar-hamedina-view-floor-20.webp", "הנוף מערבה מקומה 20 " + P, 1200, 675, "קומה 20"),
                        cell("kikar-hamedina-view-floor-30.webp", "הנוף מערבה מקומה 30 " + P, 1200, 675, "קומה 30"),
                        cell("kikar-hamedina-view-floor-38.webp", "הנוף מערבה מקומה 38 " + P, 1200, 675, "קומה 38")]),
               L + "אותו כיוון, מערב, משלוש קומות במגדל C.")
F_HOME = fig(grid(2, [cell("kikar-hamedina-living-room.webp", "סלון בדירה לדוגמה בקומה 30 " + P, 1200, 675, "סלון"),
                      cell("kikar-hamedina-bedroom.webp", "חדר שינה בדירה לדוגמה בקומה 30 " + P, 1200, 675, "חדר שינה")]),
             L + "סלון וחדר שינה בדירה לדוגמה בקומה 30; לא צילום ולא מפרט רשמי.")
F_FAC = fig(grid(2, [cell("kikar-hamedina-pool.jpg", "בריכת השחייה " + P, 1200, 675, "בריכה"),
                     cell("kikar-hamedina-gym.jpg", "חדר הכושר " + P, 1200, 675, "חדר כושר"),
                     cell("kikar-hamedina-spa.jpg", "הספא " + P, 1200, 675, "ספא"),
                     cell("kikar-hamedina-lobby.jpg", "הלובי " + P, 1200, 675, "לובי")]),
            "<b>הדמיית מתקנים להמחשה:</b> לא צילום ולא מפרט רשמי.")

A1 = "של המוכר.</p><table><tbody><tr><th>שם ומיקום</th>"
A2 = "<td>כ-160 מטר</td></tr></tbody></table><h3>מה הסיבוב עושה למרפסות ולמבט החוצה?</h3>"
A3 = "<h3>מה נמצא בכל כיוון?</h3>"
A4 = "<h3>איך הקומה נכנסת למחיר?</h3>"
A5 = "שאינה עונה על מה שחיפשתם.</p></section><section class=\"nlws\" id=\"nlws-homes\">"
A6 = "<h3>השטח שמשרת את החיים שלכם</h3>"
A7 = "<h3>מהלובי ועד הדירה</h3>"
SWAPS = [
    (A1, "של המוכר.</p>" + F_AERIAL + "<table><tbody><tr><th>שם ומיקום</th>"),
    (A2, "<td>כ-160 מטר</td></tr></tbody></table>" + F_TOWERS + "<h3>מה הסיבוב עושה למרפסות ולמבט החוצה?</h3>"),
    (A3, F_BALCONY + A3),
    (A4, F_DIRS + A4),
    (A5, "שאינה עונה על מה שחיפשתם.</p>" + F_FLOORS + "</section><section class=\"nlws\" id=\"nlws-homes\">"),
    (A6, F_HOME + A6),
    (A7, F_FAC + A7),
]
if "--dump" in sys.argv:
    json.dump({"figs": [F_AERIAL, F_TOWERS, F_BALCONY, F_DIRS, F_FLOORS, F_HOME, F_FAC]}, open(sys.argv[sys.argv.index("--dump") + 1], "w", encoding="utf-8"), ensure_ascii=False)
    sys.exit(0)
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "h712i"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
GO = "--go" in sys.argv
GAL = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "hamedina", "gallery")
for a, b in SWAPS:
    for f in [x.split('"')[0] for x in b.split(G)[1:]]:
        assert os.path.isfile(os.path.join(GAL, f)), "no gallery file " + f
s, g, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,slug,modified,content" % PID)
assert s == 200 and g["slug"] == SLUG, (s, g.get("slug"))
raw = g["content"]["raw"]
now = hashlib.md5(raw.encode("utf-8")).hexdigest()
if now != PIN:
    raise SystemExit("the live post changed since it was read (%s, modified %s): read it again before replacing anything" % (now[:10], g["modified"]))
new = raw
for old, rep in SWAPS:
    c = new.count(old)
    if c != 1:
        raise SystemExit("anchor x%d: %s" % (c, old[:90]))
    new = new.replace(old, rep)
assert new.count("<figure") == 7 and new.count("</figure>") == 7 and new.count("<img ") == 18 and new.count("<h3>") == raw.count("<h3>")
print("[plan] post %d: 7 figures, 18 pictures; %d -> %d chars" % (PID, len(raw), len(new)))
if not GO:
    sys.exit(0)
if GO:  # the pictures and the styles must be live first (release 1.72.648)
    import urllib.request
    for _f in ("kikar-hamedina-lobby.jpg", "kikar-hamedina-towers-aerial.webp", "kikar-hamedina-tower-b.webp"):
        _rq = urllib.request.Request(G + _f, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(_rq, timeout=30) as _rs:
            assert _rs.status == 200 and _rs.headers.get("Content-Type", "").startswith("image/"), "the gallery is not live yet: release 1.72.648 first (" + _f + ")"
bk = os.path.join(REPO, "docs", "qa", "had-712"); os.makedirs(bk, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
io.open(os.path.join(bk, "backup-%d-%s.html" % (PID, stamp)), "w", encoding="utf-8", newline="").write(raw)
s1, r1, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new})
assert s1 in (200, 201), (s1, str(r1)[:300])
s, r, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=content,modified" % PID)
ok = r["content"]["raw"] == new
res = {"post": PID, "before_md5": now, "after_md5": hashlib.md5(r["content"]["raw"].encode("utf-8")).hexdigest(), "read_back_equal": ok, "modified": r.get("modified"), "figures": 7, "pictures": 18}
json.dump({"stamp": stamp, "result": res}, open(os.path.join(bk, "result-images-%s.json" % stamp), "w", encoding="utf-8"), indent=1)
if not ok:  # put the old text back and stop
    sb, _, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": raw})
    raise SystemExit("read-back differs: restored the backup (http %s)" % sb)
print("[done] post %d written and read back; backup and result in docs/qa/had-712/ (%s)" % (PID, stamp))
