# -*- coding: utf-8 -*-
"""HAD-695 (10.11.2026): put the finished pilot pictures (docs/design/project-images-2026-11/) on the site.
- Uploads each picture's card crop (960x600, the drawing only) to the media library, for the immediate-occupancy cards on /projects/.
- For the two pilot projects that have their own page (Recanati Residence 4877, Einstein Ramat Aviv = ashdar-einstein 4875) it also
  uploads the full 4:3 picture (with the drawn strip of facts) and makes it the featured image: the project page and the share image
  use it, and the catalog card shows its top (8:5) through the 1.72.638 card. The previous featured ids are recorded first.
- Held back on purpose (drawn facts rest on conflicting sources): hasollelim (33 vs 35 floors), gindi-towers (tower count drawn
  for illustration). Jaffa Courtyard has no row or page on the site.
Idempotent: a file already in the library (same slug name) is reused. Writes docs/qa/had-695/upload-<stamp>.json.
python scripts/project-stage/upload_pilot_695.py [--dry | --rollback <record.json>]"""
import io, json, os, sys, time, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
PILOT = os.path.join(REPO, "docs", "design", "project-images-2026-11")
OUT = os.path.join(REPO, "docs", "qa", "had-695")
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "up695"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req, AUTH, BASE, UA = ns["req"], ns["AUTH"], ns["BASE"], ns["UA"]
# slug in the pilot -> WordPress project id (or None: the picture serves the immediate-occupancy card only)
PICS = {"moma-tel-aviv": None, "port-tlv-residence-tel-aviv": None, "recanati-residence-tel-aviv": 4877, "remez-36-tel-aviv": None,
        "zichron-weizman-tel-aviv": None, "bloch-22-tel-aviv": None, "einstein-ramat-aviv-tel-aviv": 4875}
man = {p["slug"]: p for p in json.load(io.open(os.path.join(PILOT, "manifest.json"), encoding="utf-8"))["projects"]}


def find_media(name):
    s, L, _ = req("GET", "/wp-json/wp/v2/media?search=%s&per_page=20&_fields=id,source_url,slug" % urllib.request.quote(name))
    if s == 200 and isinstance(L, list):
        for m in L:
            if m.get("slug", "").startswith(name.lower()):
                return m
    return None


def upload(path, alt, title):
    name = os.path.splitext(os.path.basename(path))[0]
    have = find_media(name)
    if have:
        return have["id"], have["source_url"], "reused"
    data = open(path, "rb").read()
    r = urllib.request.Request(BASE + "/wp-json/wp/v2/media", data=data, method="POST")
    r.add_header("Authorization", AUTH); r.add_header("User-Agent", UA)
    r.add_header("Content-Type", "image/webp"); r.add_header("Content-Disposition", 'attachment; filename="%s"' % os.path.basename(path))
    with urllib.request.urlopen(r, timeout=180) as resp:
        m = json.loads(resp.read().decode())
    s, _, _ = req("POST", "/wp-json/wp/v2/media/%d" % m["id"], {"alt_text": alt, "title": title})
    return m["id"], m["source_url"], "uploaded (meta %s)" % s


if "--rollback" in sys.argv:
    rec = json.load(io.open(sys.argv[sys.argv.index("--rollback") + 1], encoding="utf-8"))
    for pid, old in rec.get("featured_before", {}).items():
        s, _, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%s" % pid, {"featured_media": int(old)})
        print("[rollback] project", pid, "featured ->", old, s)
    raise SystemExit(0)

rec = {"at": time.strftime("%Y-%m-%d %H:%M:%S"), "pics": {}, "featured_before": {}, "featured_after": {}}
for slug, pid in PICS.items():
    p = man[slug]
    files = p["files"]
    card = os.path.join(PILOT, files["card_960x600"]["file"] if "card_960x600" in files else "web/%s-card-960x600.webp" % slug)
    full = os.path.join(PILOT, files["full_1440x1080"]["file"])
    alt = p.get("alt") or p.get("name")
    print("[pic]", slug, "| card", os.path.exists(card), "| full", os.path.exists(full), "| project", pid)
    if "--dry" in sys.argv:
        continue
    cid, curl, how = upload(card, alt, p["name"])
    rec["pics"][slug] = {"name": p["name"], "card_id": cid, "card_url": curl, "how": how}
    print("   card", cid, curl, how)
    if pid:
        s, cur, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,featured_media,slug" % pid)
        if s != 200:
            raise SystemExit("FATAL read project %d: %s" % (pid, s))
        rec["featured_before"][str(pid)] = int(cur.get("featured_media") or 0)
        fid, furl, how2 = upload(full, alt, p["name"])
        s2, after, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % pid, {"featured_media": fid})
        ok = s2 == 200 and int(after.get("featured_media") or 0) == fid
        rec["featured_after"][str(pid)] = fid
        rec["pics"][slug].update({"full_id": fid, "full_url": furl, "project": pid, "slug": cur.get("slug")})
        print("   full", fid, furl, how2, "| featured", cur.get("featured_media"), "->", fid, "OK" if ok else "FAILED %s" % s2)
        if not ok:
            raise SystemExit("FATAL featured on %d" % pid)
if "--dry" not in sys.argv:
    os.makedirs(OUT, exist_ok=True)
    fp = os.path.join(OUT, "upload-%s.json" % time.strftime("%Y%m%dT%H%M%S"))
    io.open(fp, "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
    print("record:", os.path.relpath(fp, REPO))
