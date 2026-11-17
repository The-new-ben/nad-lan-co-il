# -*- coding: utf-8 -*-
"""HAD-768: uploads the state's form files (forms-inventory.json, downloaded byte-for-byte from gov.il) to the nad-lan.co.il Media
Library through the REST API (the app password, decrypted in-process, never printed). The original file name is sent as is; WordPress
may normalise it (a space becomes "-", a taken name gets "-1"), and the final URL is recorded. Each public URL is downloaded back and
its SHA-256 compared with the gov.il file. Resumable: a file already in media.json with byte_check OK is skipped.
  python docs/research/2026-11-17-gov-forms/upload_forms_media.py [--dry]"""
import hashlib, json, os, sys, time, urllib.error, urllib.parse, urllib.request

H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "upload_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, AUTH, BASE = _ns["req"], _ns["AUTH"], _ns["BASE"]
MIME = {"pdf": "application/pdf", "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "doc": "application/msword"}
inv = json.load(open(os.path.join(H, "forms-inventory.json"), encoding="utf-8"))
OUT = os.path.join(H, "media.json")
done = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
todo = []
for e in inv:
    files = []
    if e.get("local_path"):
        files.append((e["local_path"], e.get("original_filename"), e.get("direct_file_url"), e.get("sha256")))
    for a in e.get("additional_files") or []:
        if a.get("local_path"):
            files.append((a["local_path"], a.get("original_filename") or os.path.basename(a["local_path"]), a.get("direct_file_url") or a.get("url"), a.get("sha256")))
    for lp, fn, src, sha in files:
        key = lp.replace("\\", "/")
        if key in done and done[key].get("byte_check") == "OK":
            continue
        if any(t[0] == key for t in todo):
            continue
        todo.append((key, fn or os.path.basename(lp), src, sha, e.get("official_name_he", ""), e.get("form_number", "")))
print(f"[plan] {len(todo)} files to upload, {len(done)} already done")
if "--dry" in sys.argv:
    for t in todo[:10]:
        print(" ", t[0], "->", t[1])
    raise SystemExit(0)
bad = 0
for key, fn, src, sha, name, num in todo:
    path = os.path.join(H, *key.split("/"))
    data = open(path, "rb").read()
    if sha and hashlib.sha256(data).hexdigest() != sha:
        raise SystemExit("FATAL: the local file is not the inventory file: " + key)
    ext = fn.rsplit(".", 1)[-1].lower()
    r = urllib.request.Request(BASE + "/wp-json/wp/v2/media", data=data, method="POST")
    r.add_header("Authorization", AUTH)
    r.add_header("Content-Type", MIME.get(ext, "application/octet-stream"))
    r.add_header("Content-Disposition", 'attachment; filename="' + fn.replace('"', '').encode("utf-8").decode("latin-1") + '"')
    r.add_header("User-Agent", "Mozilla/5.0 NadLan-Forms/1.0")
    try:
        with urllib.request.urlopen(r, timeout=300) as resp:
            m = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"FAIL upload {key}: HTTP {e.code} {e.read()[:200]!r}")
        bad += 1
        continue
    title = ((f"טופס {num}: " if num and num not in name else "") + name + " (העותק הרשמי מ-gov.il)").strip()
    req("POST", f"/wp-json/wp/v2/media/{m['id']}", {"title": title, "alt_text": name})
    rec = {"id": m["id"], "url": m["source_url"], "bytes": len(data), "orig_name": fn, "gov_url": src, "same_name": m["source_url"].rsplit("/", 1)[-1] == urllib.parse.quote(fn) or urllib.parse.unquote(m["source_url"].rsplit("/", 1)[-1]) == fn}
    try:
        rq = urllib.request.Request(m["source_url"] + "?nlf=" + str(len(data)), headers={"User-Agent": "Mozilla/5.0 NadLan-Forms/1.0"})
        with urllib.request.urlopen(rq, timeout=120) as resp:
            live = resp.read()
        rec["byte_check"] = "OK" if hashlib.sha256(live).hexdigest() == hashlib.sha256(data).hexdigest() else "MISMATCH"
    except Exception as ex:  # noqa: BLE001
        rec["byte_check"] = "READ-FAIL " + str(ex)[:80]
    if rec["byte_check"] != "OK":
        bad += 1
    done[key] = rec
    json.dump(done, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(key, "|", m["id"], "|", rec["url"].rsplit("/", 1)[-1], "|", rec["byte_check"], "| same name" if rec["same_name"] else "| RENAMED")
    time.sleep(0.4)
print(f"[done] {len(done)} in media.json, {bad} problem(s)")
