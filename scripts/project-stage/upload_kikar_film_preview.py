# -*- coding: utf-8 -*-
"""The owner's order, 2.10.2026 night: "upload the video ... I watch it there ... then I can give you remarks". Uploads the Kikar
Hamedina film's private-review copies (HE 16x9 720p, HE 9x16 720x1280, poster) to the WordPress media library through the REST API
(the app password, decrypted in-process, never printed) and prints their public URLs. Nothing is placed on any page here.
Skips a file whose name is already in the library (no duplicates).   python scripts/project-stage/upload_kikar_film_preview.py <dir>"""
import json, os, sys, urllib.request, urllib.error, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SRC = sys.argv[1]
NAMES = ["kikar-hamedina-film-he-16x9-preview.mp4", "kikar-hamedina-film-he-9x16-preview.mp4", "kikar-hamedina-film-he-16x9-preview-poster.jpg", "kikar-hamedina-film-he-9x16-preview-poster.jpg",
         "kikar-hamedina-film-en-16x9-preview.mp4", "kikar-hamedina-film-en-9x16-preview.mp4", "kikar-hamedina-film-en-16x9-preview-poster.jpg", "kikar-hamedina-film-en-9x16-preview-poster.jpg"]
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "upload_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, AUTH, BASE = _ns["req"], _ns["AUTH"], _ns["BASE"]
out = {}
for n in NAMES:
    stem = os.path.splitext(n)[0]
    # by slug (the upload's file name), never by search: the title is set to Hebrew after upload, so a search misses it (2.10.2026:
    # that miss uploaded 8122-8124 twice; they are unused and left in place, a media delete is permanent and only the owner's)
    s, found, _ = req("GET", "/wp-json/wp/v2/media?slug=" + urllib.parse.quote(stem) + "&per_page=20&_fields=id,source_url,slug")
    hit = [m for m in (found or []) if isinstance(m, dict) and m.get("source_url", "").rsplit("/", 1)[-1] == n]
    if hit:
        out[n] = {"id": hit[0]["id"], "url": hit[0]["source_url"], "existing": True}
        continue
    data = open(os.path.join(SRC, n), "rb").read()
    ctype = "video/mp4" if n.endswith(".mp4") else "image/jpeg"
    r = urllib.request.Request(BASE + "/wp-json/wp/v2/media", data=data, method="POST")
    r.add_header("Authorization", AUTH)
    r.add_header("Content-Type", ctype)
    r.add_header("Content-Disposition", f'attachment; filename="{n}"')
    r.add_header("User-Agent", "Mozilla/5.0 NadLan-Film/1.0")
    try:
        with urllib.request.urlopen(r, timeout=600) as resp:
            m = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"FATAL upload {n}: HTTP {e.code} {e.read()[:300]!r}")
    out[n] = {"id": m["id"], "url": m["source_url"], "bytes": len(data)}
    # alt text / title: plain, honest
    req("POST", f"/wp-json/wp/v2/media/{m['id']}", {"title": "מגדלי כיכר המדינה: סרט, טיוטה לצפייה", "alt_text": "מגדלי כיכר המדינה, הדמיה להמחשה"})
for n, v in out.items():
    print(n, "|", v["id"], "|", v["url"], "| existing" if v.get("existing") else "| uploaded " + str(v.get("bytes")))
open(os.path.join(REPO, "docs", "qa", "v8-traffic", "film-preview-media.json"), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
