# -*- coding: utf-8 -*-
"""Kikar Hamedina film v2r1, the captions (design v104.41, the Kikar loop turn 26): upload the narrated film's two caption files
(he/en WebVTT, the narration script timed to the voice) to the media library through the REST API (the app password, decrypted
in-process, never printed). Skips a file already in the library (by slug, no duplicates), then downloads every public URL and
compares its SHA-256 with the local file (bytes per the table). Nothing is placed on a page here.
  python scripts/project-stage/upload_kikar_facilities.py docs/qa/film-facilities/stage"""
import hashlib, json, os, sys, urllib.request, urllib.error, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SRC = sys.argv[1]
NAMES = [f"kikar-hamedina-film-v2-{l}.vtt" for l in ("he", "en")]
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
    ctype = "text/vtt"
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
    req("POST", f"/wp-json/wp/v2/media/{m['id']}", {"title": "מגדלי כיכר המדינה: כתוביות הסרט"})
for n, v in out.items():
    print(n, "|", v["id"], "|", v["url"], "| existing" if v.get("existing") else "| uploaded " + str(v.get("bytes")))
bad = 0
for n, v in out.items():
    local = open(os.path.join(SRC, n), "rb").read()
    rq = urllib.request.Request(v["url"] + "?nlb=" + str(len(local)), headers={"User-Agent": "Mozilla/5.0 NadLan-Film/1.0"})
    with urllib.request.urlopen(rq, timeout=300) as resp:
        live = resp.read(); v["served_type"] = resp.headers.get("Content-Type")
    ok = hashlib.sha256(live).hexdigest() == hashlib.sha256(local).hexdigest()
    v["sha256"] = hashlib.sha256(live).hexdigest(); v["bytes_live"] = len(live); v["byte_check"] = "OK" if ok else "MISMATCH"
    bad += 0 if ok else 1
    print("[bytes]", n, len(live), v["sha256"][:16], v["byte_check"])
os.makedirs(os.path.join(REPO, "docs", "qa", "film-v2r1"), exist_ok=True)
open(os.path.join(REPO, "docs", "qa", "film-v2r1", "media-vtt.json"), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
if bad:
    raise SystemExit(f"FATAL: {bad} file(s) differ after upload")
