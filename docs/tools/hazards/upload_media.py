# -*- coding: utf-8 -*-
"""HAD-670 R13c: uploads the three hazards page images (Nano Banana, 3.11.2026) to the media library through the REST API (the app
password, decrypted in-process, never printed). Skips a file already in the library (by slug), sets the Hebrew alt text and title,
then downloads each public URL and compares its SHA-256 with the local file. Writes docs/tools/hazards/media.json.
  python docs/tools/hazards/upload_media.py"""
import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request

H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
SRC = os.path.join(REPO, "docs", "research", "2026-11-03-hazards", "image")
FILES = {
    "environmental-hazards-neighbourhood-aerial.webp": ("מפגעים סביבתיים בשכונה: קו מתח עליון, תחנת משנה, תחנת דלק ואזור תעשייה, הדמיה להמחשה",
        "מבט מהאוויר על שכונת מגורים בישראל: קו מתח עליון עם עמודים, תחנת משנה מגודרת, תחנת דלק בפינת הרחוב ואזור תעשייה ברקע"),
    "cellular-antenna-rooftop-israel.webp": ("אנטנה סלולרית על גג בניין מגורים, הדמיה להמחשה",
        "אנטנה סלולרית עם שלושה לוחות על גג בניין מגורים בישראל, ליד דודי שמש"),
    "radiation-survey-apartment.webp": ("מדידת קרינה בדירה, הדמיה להמחשה",
        "מודד קרינה בודק בדירה עם מכשיר מדידה ליד החלון ומד על חצובה בסלון"),
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
    r.add_header("User-Agent", "Mozilla/5.0 NadLan-Hazards/1.0")
    try:
        with urllib.request.urlopen(r, timeout=300) as resp:
            m = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"FATAL upload {n}: HTTP {e.code} {e.read()[:300]!r}")
    out[n] = {"id": m["id"], "url": m["source_url"], "bytes": len(data)}
    out[n]["meta_http"] = req("POST", f"/wp-json/wp/v2/media/{m['id']}", {"title": title, "alt_text": alt})[0]
bad = 0
for n, v in out.items():
    local = open(os.path.join(SRC, n), "rb").read()
    with urllib.request.urlopen(urllib.request.Request(v["url"] + "?nlb=" + str(len(local)), headers={"User-Agent": "Mozilla/5.0 NadLan-Hazards/1.0"}), timeout=120) as resp:
        live = resp.read()
    v["byte_check"] = "OK" if hashlib.sha256(live).hexdigest() == hashlib.sha256(local).hexdigest() else "MISMATCH"
    bad += v["byte_check"] != "OK"
    print(n, "|", v["id"], "|", v["url"], "|", "existing" if v.get("existing") else "uploaded", "|", v["byte_check"])
json.dump(out, open(os.path.join(H, "media.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
if bad:
    raise SystemExit(f"FATAL: {bad} file(s) differ after upload")
