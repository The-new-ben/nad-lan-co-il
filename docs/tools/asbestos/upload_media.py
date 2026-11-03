# -*- coding: utf-8 -*-
"""HAD-668 R11d: uploads the two asbestos page images (Nano Banana, benchmarked 3.11.2026) to the media library through the REST
API (the app password, decrypted in-process, never printed). Skips a file already in the library (by slug), sets the Hebrew alt
text and title, then downloads each public URL and compares its SHA-256 with the local file. Writes docs/tools/asbestos/media.json.
  python docs/tools/asbestos/upload_media.py"""
import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request

H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
SRC = os.path.join(REPO, "docs", "research", "2026-11-03-asbestos", "image")
FILES = {
    "asbestos-shikun-cutaway.webp": ("איפה יש אסבסט בבניין ישן: חתך של בניין שיכון, הדמיה להמחשה",
                                     "איפה יש אסבסט בבניין ישן בישראל: גגון מאסבסט-צמנט על הגג, ארובה, צינורות ניקוז וביוב בחזית, אדנית במרפסת ומחסן עם גג גלי בחצר"),
    "asbestos-roof-shed-tel-aviv.webp": ("גגון מאסבסט-צמנט על גג בתל אביב, הדמיה להמחשה",
                                         "גגון מלוחות אסבסט-צמנט גליים על גג בניין בתל אביב, ליד דודי שמש וצינור ישן"),
}
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "upload_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, AUTH, BASE = _ns["req"], _ns["AUTH"], _ns["BASE"]
out = {}
for n, (title, alt) in FILES.items():
    stem = os.path.splitext(n)[0]
    s, found, _ = req("GET", "/wp-json/wp/v2/media?slug=" + urllib.parse.quote(stem) + "&per_page=20&_fields=id,source_url,slug")
    hit = [m for m in (found or []) if isinstance(m, dict) and m.get("source_url", "").rsplit("/", 1)[-1] == n]
    if hit:
        out[n] = {"id": hit[0]["id"], "url": hit[0]["source_url"], "existing": True}
        continue
    data = open(os.path.join(SRC, n), "rb").read()
    r = urllib.request.Request(BASE + "/wp-json/wp/v2/media", data=data, method="POST")
    r.add_header("Authorization", AUTH)
    r.add_header("Content-Type", "image/webp")
    r.add_header("Content-Disposition", f'attachment; filename="{n}"')
    r.add_header("User-Agent", "Mozilla/5.0 NadLan-Asbestos/1.0")
    try:
        with urllib.request.urlopen(r, timeout=300) as resp:
            m = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"FATAL upload {n}: HTTP {e.code} {e.read()[:300]!r}")
    out[n] = {"id": m["id"], "url": m["source_url"], "bytes": len(data)}
    s2, _, _ = req("POST", f"/wp-json/wp/v2/media/{m['id']}", {"title": title, "alt_text": alt})
    out[n]["meta_http"] = s2
bad = 0
for n, v in out.items():
    local = open(os.path.join(SRC, n), "rb").read()
    rq = urllib.request.Request(v["url"] + "?nlb=" + str(len(local)), headers={"User-Agent": "Mozilla/5.0 NadLan-Asbestos/1.0"})
    with urllib.request.urlopen(rq, timeout=120) as resp:
        live = resp.read()
    ok = hashlib.sha256(live).hexdigest() == hashlib.sha256(local).hexdigest()
    v["byte_check"] = "OK" if ok else "MISMATCH"
    bad += 0 if ok else 1
    print(n, "|", v["id"], "|", v["url"], "|", "existing" if v.get("existing") else "uploaded", "|", v["byte_check"])
json.dump(out, open(os.path.join(H, "media.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
if bad:
    raise SystemExit(f"FATAL: {bad} file(s) differ after upload")
