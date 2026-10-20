# -*- coding: utf-8 -*-
"""Upload a file to the WordPress media library (admin app password, in-process). python upload_media.py <file> [title]
Prints the attachment id and URL; records them in media.json beside this script."""
import io, json, os, sys, urllib.request
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "de"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
f = sys.argv[1]; name = os.path.basename(f); title = sys.argv[2] if len(sys.argv) > 2 else name
ct = {"mp4": "video/mp4", "jpg": "image/jpeg", "png": "image/png", "vtt": "text/vtt"}[name.rsplit(".", 1)[1]]
r = urllib.request.Request(ns["BASE"] + "/wp-json/wp/v2/media", data=open(f, "rb").read(), method="POST")
r.add_header("Authorization", ns["AUTH"]); r.add_header("User-Agent", ns["UA"]); r.add_header("Content-Type", ct)
r.add_header("Content-Disposition", 'attachment; filename="%s"' % name)
d = json.loads(urllib.request.urlopen(r, timeout=900).read())
s, d2, _ = ns["req"]("POST", "/wp-json/wp/v2/media/%d" % d["id"], {"title": title, "alt_text": title})
print(d["id"], d["source_url"])
M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media.json")
m = json.load(open(M)) if os.path.exists(M) else {}; m[name] = {"id": d["id"], "url": d["source_url"]}; json.dump(m, open(M, "w"), indent=1)
