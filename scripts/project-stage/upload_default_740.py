# -*- coding: utf-8 -*-
"""HAD-740 stage 1 (Ben 14.11.2026): put the approved default card picture into the WordPress media library, then (with --set,
after 1.72.677 registered the setting) store its id in the option nadlan_pd_attachment through /wp/v2/settings.
The picture: docs/design/project-defaults-2026-11/fable/out/nadlan-new-projects-israel-choose-apartment-on-the-building-1600x1000.webp
Idempotent: a media item with the same slug is reused. Record: docs/qa/had-740/upload-<stamp>.json. Secrets are only read inside.
python scripts/project-stage/upload_default_740.py [--set]"""
import io, json, os, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(REPO, "docs", "design", "project-defaults-2026-11", "fable", "out", "nadlan-new-projects-israel-choose-apartment-on-the-building-1600x1000.webp")
OUT = os.path.join(REPO, "docs", "qa", "had-740")
TITLE = "נדל״ן: בחרו את הדירה שלכם על הבניין"
ALT = "נדל״ן: בחרו את הדירה שלכם על הבניין. מגדל מגורים עם קומה מסומנת, תוכנית הדירה ומפת הסביבה"
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "up740"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req, AUTH, BASE, UA = ns["req"], ns["AUTH"], ns["BASE"], ns["UA"]
name = os.path.splitext(os.path.basename(SRC))[0]
s, L, _ = req("GET", "/wp-json/wp/v2/media?slug=%s&per_page=20&_fields=id,slug,source_url,media_details" % ",".join([name, name + "-1", name + "-2"]))  # by slug: a title search misses (the title is Hebrew); 14.11 this slip made 8913 and 8914
have = [m for m in (L if isinstance(L, list) else []) if m.get("slug", "").startswith(name.lower())]
if have:
    m = have[0]; how = "reused"
else:
    data = open(SRC, "rb").read()
    r = urllib.request.Request(BASE + "/wp-json/wp/v2/media", data=data, method="POST")
    r.add_header("Authorization", AUTH); r.add_header("User-Agent", UA)
    r.add_header("Content-Type", "image/webp"); r.add_header("Content-Disposition", 'attachment; filename="%s"' % os.path.basename(SRC))
    with urllib.request.urlopen(r, timeout=180) as resp:
        m = json.loads(resp.read().decode())
    s2, _, _ = req("POST", "/wp-json/wp/v2/media/%d" % m["id"], {"alt_text": ALT, "title": TITLE})
    how = "uploaded (meta %s)" % s2
s, m, _ = req("GET", "/wp-json/wp/v2/media/%d?_fields=id,slug,source_url,alt_text,title,media_details" % m["id"])
sizes = {k: (v.get("width"), v.get("height"), v.get("source_url", "")[-60:]) for k, v in (m.get("media_details", {}).get("sizes", {}) or {}).items()}
print("[media]", m["id"], how, "|", m["source_url"], "|", m["media_details"].get("width"), "x", m["media_details"].get("height"))
print("[sizes]", json.dumps(sizes, ensure_ascii=False)[:600])
print("[alt]", m.get("alt_text") == ALT, "| title", (m.get("title") or {}).get("rendered"))
rec = {"at": time.strftime("%Y-%m-%d %H:%M:%S"), "id": m["id"], "url": m["source_url"], "sizes": sizes, "how": how}
if "--set" in sys.argv:
    s, cur, _ = req("GET", "/wp-json/wp/v2/settings")
    rec["option_before"] = cur.get("nadlan_pd_attachment") if isinstance(cur, dict) else None
    if not isinstance(cur, dict) or "nadlan_pd_attachment" not in cur:
        raise SystemExit("FATAL: the setting nadlan_pd_attachment is not registered yet (release 1.72.677 first): %s" % s)
    s, after, _ = req("POST", "/wp-json/wp/v2/settings", {"nadlan_pd_attachment": int(m["id"])})
    rec["option_after"] = after.get("nadlan_pd_attachment") if isinstance(after, dict) else None
    print("[option] nadlan_pd_attachment", rec["option_before"], "->", rec["option_after"], "| http", s)
    if rec["option_after"] != int(m["id"]):
        raise SystemExit("FATAL: the option did not take the id")
os.makedirs(OUT, exist_ok=True)
fp = os.path.join(OUT, "upload-%s.json" % time.strftime("%Y%m%dT%H%M%S"))
io.open(fp, "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
print("record:", os.path.relpath(fp, REPO))
