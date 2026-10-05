# -*- coding: utf-8 -*-
"""The project films v1 (HAD-419 DUO, HAD-400 Rainbow, HAD-420 Dimri Yama; Ben 5.10.2026: "everything is approved, upload and then
send links"): upload the 720p web copies (he/en, 16x9/9x16) and their posters (frame at 2.5 s) to the media library through the
REST API (the app password, decrypted in-process, never printed). Skips a file already in the library (by slug, no duplicates),
then downloads every public URL and compares its SHA-256 with the local file. Nothing is placed on a page here.
The film audit (5.10, scratchpad film-audit): no draft label in any frame; the only badge is "הדמיה להמחשה"; the end card carries
the map-data credit (OpenStreetMap + Tel Aviv-Yafo GIS); no developer name and no price.
  python scripts/project-stage/upload_project_films.py docs/qa/film-v1-projects/stage"""
import hashlib, json, os, sys, urllib.request, urllib.error, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SRC = sys.argv[1]
PROJECTS = {
    "duo-tel-aviv": ("DUO תל אביב", "DUO תל אביב, סרטון הפרויקט: שני המגדלים במתחם סומייל, הדמיה להמחשה"),
    "rainbow-tel-aviv": ("Rainbow תל אביב", "Rainbow תל אביב, סרטון הפרויקט: המגדל ובנייני הבוטיק ברובע שדה דב, הדמיה להמחשה"),
    "dimri-yama-sde-dov": ("דמרי ימה שדה דב", "דמרי ימה שדה דב, סרטון הפרויקט: המגדל במתחם אשכול ברובע שדה דב, הדמיה להמחשה"),
}
NAMES = [f"{p}-film-v1-{l}-{f}{x}" for p in PROJECTS for l in ("he", "en") for f in ("16x9", "9x16") for x in (".mp4", "-poster.jpg")]
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "upload_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, AUTH, BASE = _ns["req"], _ns["AUTH"], _ns["BASE"]
out = {}
for n in NAMES:
    stem = os.path.splitext(n)[0]
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
    title, alt = PROJECTS[n.split("-film-v1-")[0]]
    req("POST", f"/wp-json/wp/v2/media/{m['id']}", {"title": title + ": סרטון הפרויקט, הדמיה להמחשה", "alt_text": alt})
for n, v in out.items():
    print(n, "|", v["id"], "|", v["url"], "| existing" if v.get("existing") else "| uploaded " + str(v.get("bytes")))
bad = 0
for n, v in out.items():
    local = open(os.path.join(SRC, n), "rb").read()
    rq = urllib.request.Request(v["url"] + "?nlb=" + str(len(local)), headers={"User-Agent": "Mozilla/5.0 NadLan-Film/1.0"})
    with urllib.request.urlopen(rq, timeout=300) as resp:
        live = resp.read()
    ok = hashlib.sha256(live).hexdigest() == hashlib.sha256(local).hexdigest()
    v["sha256"] = hashlib.sha256(live).hexdigest(); v["bytes_live"] = len(live); v["byte_check"] = "OK" if ok else "MISMATCH"
    bad += 0 if ok else 1
    print("[bytes]", n, len(live), v["sha256"][:16], v["byte_check"])
open(os.path.join(REPO, "docs", "qa", "film-v1-projects", "media.json"), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
if bad:
    raise SystemExit(f"FATAL: {bad} file(s) differ after upload")
print("all", len(out), "files byte-checked OK")
