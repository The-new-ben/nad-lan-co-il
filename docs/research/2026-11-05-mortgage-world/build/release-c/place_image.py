# -*- coding: utf-8 -*-
"""The page's original image (HAD-675). Uploads img/mortgage-calculator-israel.jpg to the media library (alt, caption: illustration),
places one <figure> after the tools switcher on page 121 (additive), and asks Yoast to use it as the share image. Runs after
write_page_b.py. python place_image.py [--dry]"""
import io, json, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", "..", ".."))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 121
IMG = os.path.join(H, "img", "mortgage-calculator-israel.jpg")
ALT = "זוג בודק אישור עקרוני למשכנתא ומחשבון החזר בטלפון, במטבח של דירה חדשה עם נוף לעיר ולים"
CAP = "תמונה להמחשה"
ANCHOR = '<details class="nlmx-fold"><summary><span>המחשבון הקלאסי לפי שלושה מסלולים'

src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "mw_img"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req, AUTH, BASE, UA = ns["req"], ns["AUTH"], ns["BASE"], ns["UA"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link,meta" % PID)
assert s == 200, s
raw = r["content"]["raw"]
assert 'class="nlmx-sw"' in raw, "release B content is not on the page yet"
assert 'class="nlmx-hero"' not in raw, "already placed"
assert raw.count(ANCHOR) == 1, raw.count(ANCHOR)
if DRY:
    print("[dry] anchor found once; image", os.path.getsize(IMG), "bytes"); sys.exit(0)

# 1. upload
data = open(IMG, "rb").read()
rq = urllib.request.Request(BASE + "/wp-json/wp/v2/media", data=data, method="POST", headers={
    "Authorization": AUTH, "User-Agent": UA, "Content-Type": "image/jpeg", "Content-Disposition": 'attachment; filename="mortgage-calculator-israel.jpg"'})
m = json.load(urllib.request.urlopen(rq, timeout=180))
mid, url = m["id"], m["source_url"]
s3, _, _ = req("POST", "/wp-json/wp/v2/media/%d" % mid, {"alt_text": ALT, "caption": CAP, "title": "מחשבון משכנתא: אישור עקרוני ומחשבון החזר"})
print("[media]", mid, url, "meta", s3)
sizes = (m.get("media_details") or {}).get("sizes") or {}
mid_url = (sizes.get("large") or sizes.get("medium_large") or {}).get("source_url", url)
FIG = ('<figure class="nlmx-hero" style="margin:8px 0 22px"><img src="%s" alt="%s" width="1536" height="1024" loading="lazy" decoding="async" '
       'style="width:100%%;height:auto;border-radius:6px;display:block" srcset="%s 1536w%s" sizes="(max-width: 860px) 100vw, 820px">'
       '<figcaption style="font:400 12px/18px \'IBM Plex Mono\',ui-monospace,monospace;color:#5E6A75;margin-top:6px">%s</figcaption></figure>\n'
       % (url, ALT, url, (", %s %dw" % (mid_url, (sizes.get("large") or sizes.get("medium_large") or {}).get("width", 1024))) if mid_url != url else "", CAP))
new = raw.replace(ANCHOR, FIG + ANCHOR)
for line in raw.split("\n"):
    if line.strip():
        assert line in new, ("an original line is missing", line[:80])
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new,  # no featured_media: the theme could print it above the H1
                                                         "meta": {"_yoast_wpseo_opengraph-image": url, "_yoast_wpseo_opengraph-image-id": str(mid), "_yoast_wpseo_twitter-image": url}})
print("[page] POST", s2)
time.sleep(4)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
ok = {"figure": 'class="nlmx-hero"' in page, "alt": ALT in page, "og:image": re.search(r'property="og:image" content="[^"]*mortgage-calculator-israel', page) is not None, "one h1": page[page.find("<body"):].count("<h1") == 1}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
