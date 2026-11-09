# -*- coding: utf-8 -*-
"""HAD-686 (Ben 8.11.2026): page 9 v3 (/buying-apartment/, the owner of "קניית דירה"): the full guide in 18 chapters, the guide map,
the glossary and the official sources, around the 15 buying tools. Content built by scripts/seo/build_buying_v3.py from the live
content of 9.11.2026 (every live section, link and tool kept) and checked by scripts/seo/check_buying_v3.py. The WP title and the H1 stay;
the Yoast title and meta description name the full guide; the focus phrase stays. Only after release 1.72.617 is live.
Backup before, exact read-back after.   python scripts/seo/write_buying_v3_page.py [--go | --rollback <backup.json>]"""
import io, json, os, re, sys, time, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "ph"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
PAGE = 9
R = os.path.join(REPO, "docs", "research", "2026-11-08-buying-guide-re")
NEWC = io.open(os.path.join(R, "page-9-v3.html"), encoding="utf-8").read()
BASE = io.open(os.path.join(R, "page-9-live-2026-11-09.html"), encoding="utf-8").read()
META = {"_yoast_wpseo_title": "קניית דירה בישראל 2026: המדריך המלא, 18 שלבים ו־15 כלים | nad-lan",
        "_yoast_wpseo_metadesc": "קניית דירה בישראל 2026, המדריך המלא: 18 שלבים מהתקציב ועד הנסח על שמכם, 15 כלים ו־82 מקורות רשמיים עם תאריך קריאה: מסים, חוזה, הערת אזהרה, מסירה ורישום.",
        "_yoast_wpseo_focuskw": "קניית דירה"}
BK = os.path.join(REPO, "docs", "qa", "buying-guide-2026-11-09"); os.makedirs(BK, exist_ok=True)
if "--rollback" in sys.argv:
    b = json.load(io.open(sys.argv[sys.argv.index("--rollback") + 1], encoding="utf-8"))
    s, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PAGE, {"content": b["content"], "meta": b["meta"]}); print("rollback", s); sys.exit(0)
assert NEWC.count("<h1") == 1 and NEWC.count('class="nlbg-ch"') == 18 and 'id="nlbg-map"' in NEWC and 'id="nlbg-gloss"' in NEWC
for t in ("bplan", "bequity", "bladder", "boffer", "bcompare", "bsell", "bhelp", "bvisit", "bwho", "bdates", "bpay", "bsign", "bkeys", "breg", "bmemo"):
    assert NEWC.count('[nadlan_tool id="%s"' % t) == 1, t
assert not re.search(r"[–—]", re.sub(r"<[^>]+>", " ", NEWC)), "long dash in visible text"
assert not re.search(r"[–—]", "".join(META.values())), "long dash in meta"
s, h, _ = req("GET", "/wp-json/nadlan/v1/health"); ver = (h or {}).get("version")
s, g, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=title,meta,content,link,modified" % PAGE); assert s == 200, s
print("[plan] live version %s; content %d -> %d chars; modified %s; meta title -> %s" % (ver, len(g["content"]["raw"]), len(NEWC), g.get("modified"), META["_yoast_wpseo_title"]))
assert g["content"]["raw"] == BASE, "page 9 changed since the build read it (9.11.2026): rebuild from the new live content first"
if "--go" not in sys.argv: sys.exit(0)
assert ver == "1.72.617", "the 1.72.617 tools are not live (%s)" % ver
stamp = time.strftime("%Y%m%dT%H%M%S"); bkf = os.path.join(BK, "backup-9-%s.json" % stamp)
io.open(bkf, "w", encoding="utf-8").write(json.dumps({"title": g["title"]["raw"], "content": g["content"]["raw"],
    "meta": {k: (g.get("meta") or {}).get(k) for k in META}}, ensure_ascii=False))
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PAGE, {"content": NEWC, "meta": META}); assert s2 in (200, 201), s2
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=title,meta,content" % PAGE)
assert r["content"]["raw"] == NEWC and all((r.get("meta") or {}).get(k) == v for k, v in META.items()) and r["title"]["raw"] == g["title"]["raw"], "read-back"
time.sleep(8)
live = urllib.request.urlopen(urllib.request.Request(g["link"] + "?zq=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=120).read().decode("utf-8", "replace")
res = {"backup": bkf, "h1": len(re.findall(r"<h1[\s>]", live)), "chapters": live.count('class="nlbg-ch"'), "map": 'id="nlbg-map"' in live,
       "gloss": 'id="nlbg-gloss"' in live, "raw shortcode": "[nadlan_" in live, "fatal": "Fatal error" in live, "FAQPage": '"FAQPage"' in live,
       "buying3.js": "tools/buying3.js?ver=1.72.617" in live, "tools": sorted(set(re.findall(r'data-nli="(b\w+)"', live)))}
print(json.dumps(res, ensure_ascii=False))
assert res["h1"] == 1 and res["chapters"] == 18 and res["map"] and res["gloss"] and not res["raw shortcode"] and not res["fatal"] and res["FAQPage"] and len(res["tools"]) == 15, "live check"
print("PAGE 9 v3 LIVE and checked")
