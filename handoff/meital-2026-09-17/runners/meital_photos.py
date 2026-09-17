#!/usr/bin/env python3
"""Attach Cowork's uploaded photos to the 11 live listing pages: masthead photo, gallery section,
JSON-LD image[], featured image, photos_csv. Re-applies the collision-safe CSS. Owner order 17.9 ("complete the job").
Usage: python meital_photos.py [--only=L07] [--apply] [--verify]"""
import base64, ctypes, ctypes.wintypes as wt, json, os, re, sys, time, urllib.request, urllib.error, urllib.parse, html as htmlmod

SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
HERE = os.path.dirname(os.path.abspath(__file__))
PKG = r"C:/Users/777/nad-lan/nad-lan-co-il/handoff/meital-2026-09-17/package"
WP = "https://nad-lan.co.il"
ARGS = sys.argv[1:]
APPLY = "--apply" in ARGS
ONLY = [a.split("=", 1)[1] for a in ARGS if a.startswith("--only=")]
ONLY = set(ONLY[0].split(",")) if ONLY else set()

class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wt.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

def dpapi_unprotect(b64):
    raw = base64.b64decode(b64)
    blob_in = DATA_BLOB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    blob_out = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)):
        raise RuntimeError("DPAPI decrypt failed")
    try:
        return ctypes.string_at(blob_out.pbData, blob_out.cbData).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)

with open(SECRETS_PATH, encoding="utf-8-sig") as f:
    sec = json.load(f)
AUTH = "Basic " + base64.b64encode(f"{sec['username']}:{dpapi_unprotect(sec['password_dpapi'])}".encode()).decode()

def req(method, path, body=None, params=None):
    url = WP + "/wp-json" + path + ("?" + urllib.parse.urlencode(params) if params else "")
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={"Authorization": AUTH, "Content-Type": "application/json; charset=utf-8", "User-Agent": "nadlan-runner"})
    try:
        with urllib.request.urlopen(r, timeout=180) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode() or "null")
        except Exception:
            return e.code, None

def rd(p):
    return open(os.path.join(PKG, p), encoding="utf-8").read()

imap = json.load(open(os.path.join(PKG, "data", "import-map.json"), encoding="utf-8"))
idx = json.load(open(os.path.join(PKG, "data", "listings.json"), encoding="utf-8"))["listings"]
plan = json.load(open(os.path.join(HERE, "meital_photo_plan.json"), encoding="utf-8"))

EXTRA_LISTING = """
/* nad-lan: hide theme listing layers that the prestige block already covers */
.nlps-price,.nlps-facts,.nlps-chips,.nlps-trust,.nlps-hl,.nlps-3d,.nlps-facade,.nlps-costs,.nlps-map-sec,.nlcard,article.nlx~div.nlx{display:none!important}
.nlps{margin:0!important;padding:0!important}
.nlps-hero{margin:0!important;padding:0!important;min-height:0!important;border:0!important;background:none!important}
.nlps-title{position:absolute!important;width:1px!important;height:1px!important;overflow:hidden!important;clip:rect(0 0 0 0)!important;white-space:nowrap!important;margin:0!important}
/* nad-lan: the block masthead carries the photo; hide the theme's own featured image */
.single-nadlan_property .wp-block-post-featured-image{display:none!important}
/* nad-lan: the listing runs at its own width, not the theme's reading column */
.single-nadlan_property .entry-content.is-layout-constrained>*{max-width:none!important;margin-left:auto!important;margin-right:auto!important}
.nlx .nlx-wrap{max-width:1180px;margin-inline:auto;padding-inline:clamp(16px,3vw,28px)}
/* nad-lan: one breadcrumb, no site-wide pills on the broker's listing pages */
.single-nadlan_property .yoast-breadcrumbs,.single-nadlan_property .nlcta-start,.single-nadlan_property .nlcta-wa{display:none!important}
.single-nadlan_property .wp-block-post-featured-image{display:none!important}
/* nad-lan: the listing runs at its own width, not the theme's reading column */
.single-nadlan_property .entry-content.is-layout-constrained>*{max-width:none!important;margin-left:auto!important;margin-right:auto!important}
.nlx .nlx-wrap{max-width:1180px;margin-inline:auto;padding-inline:clamp(16px,3vw,28px)}
/* nad-lan: the masthead frame takes the photograph's own proportion, so nothing is cropped */
.nlx .nlx-plate--photo{background:var(--nlx-deep);aspect-ratio:var(--nlx-cover-ar,1.5);height:auto;max-height:78vh;position:relative;overflow:hidden}
.nlx .nlx-plate--photo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center;max-width:none}
/* nad-lan: photographs keep their own shape in a column gallery */
.nlx .nlx-gallery{columns:3;column-gap:12px;margin:0}
.nlx .nlx-gallery figure{break-inside:avoid;margin:0 0 12px;border-radius:var(--nlx-r,8px);overflow:hidden;background:var(--nlx-sand,#EEE9DD)}
.nlx .nlx-gallery img{width:100%;height:auto;display:block}
@media (max-width:900px){.nlx .nlx-gallery{columns:2}}
@media (max-width:520px){.nlx .nlx-gallery{columns:1}}
"""

def inline_css(content, css):
    marker = "<!-- wp:html -->"
    assert content.startswith(marker)
    return marker + "\n<style>\n" + css + "\n</style>\n" + content[len(marker):]

def esc(s):
    return htmlmod.escape(s or "", quote=True)

def build(it):
    L = it["id"]; p = plan[L]; cover = p["cover"]; gallery = p["gallery"]
    content = rd(f"listings/{L}/content-he.html")
    # 1. masthead: replace the illustration figure (first <figure class="nlx-plate" ...>...</figure>)
    m = re.search(r'<figure class="nlx-plate[^"]*"[^>]*>.*?</figure>', content, re.S)
    assert m, "plate figure not found"
    name_m = re.search(r'<span class="nlx-plate-name">(.*?)</span>', m.group(0), re.S)
    plate_name = name_m.group(1) if name_m else it["area"]["he"]
    ar = cover.get("r") or 1.5
    photo_fig = ('<figure class="nlx-plate nlx-plate--photo" style="--nlx-cover-ar:' + ("%.3f" % ar) + '"><img src="' + esc(cover["url"]) + '" alt="' + esc(cover["alt"]) +
                 '" width="' + str(cover.get("w") or 1600) + '" height="' + str(cover.get("h") or 1067) + '" loading="eager" decoding="async" fetchpriority="high"><span class="nlx-plate-name">' + plate_name + '</span></figure>')
    content = content[:m.start()] + photo_fig + content[m.end():]
    # 2. gallery section before the first content section inside .nlx-main
    if gallery:
        figs = "".join('<figure><img src="' + esc(g["url"]) + '" alt="' + esc(g["alt"]) + '" loading="lazy" decoding="async"></figure>' for g in gallery)
        sec = ('<section class="nlx-sec" id="photos-' + L + '-he"><div class="nlx-sec-head"><p class="nlx-eyebrow">תמונות</p><h2 class="nlx-h2">הנכס בתמונות</h2></div>'
               '<div class="nlx-gallery">' + figs + '</div><p class="nlx-facts-note">צילומים: מיטל קציר.</p></section>\n')
        anchor = re.search(r'<div class="nlx-main">\s*', content)
        assert anchor, "nlx-main not found"
        content = content[:anchor.end()] + sec + content[anchor.end():]
    # 3. JSON-LD image[]
    def add_image(mm):
        try:
            d = json.loads(mm.group(2))
        except Exception:
            return mm.group(0)
        imgs = [cover["url"]] + [g["url"] for g in gallery]
        nodes = d.get("@graph") if isinstance(d, dict) and "@graph" in d else [d]
        for n in nodes:
            if isinstance(n, dict) and n.get("@type") == "RealEstateListing":
                n["image"] = imgs
                if isinstance(n.get("about"), dict):
                    n["about"]["image"] = imgs[:1]
        return mm.group(1) + json.dumps(d, ensure_ascii=False) + mm.group(3)
    content, nsub = re.subn(r'(<script type="application/ld\+json">)(.*?)(</script>)', add_image, content, count=1, flags=re.S)
    content = inline_css(content, rd("assets/nlx-prestige.css") + EXTRA_LISTING)
    photos_csv = ",".join([cover["url"]] + [g["url"] for g in gallery])
    return content, photos_csv, int(cover["attachment_id"]), nsub

results = {}
for it in idx:
    L = it["id"]
    if ONLY and L not in ONLY:
        continue
    pid = imap[L + "-he"]
    content, photos_csv, fid, nsub = build(it)
    row = {"id": pid, "cover": fid, "gallery": len(plan[L]["gallery"]), "jsonld_patched": nsub, "chars": len(content)}
    if APPLY:
        st, r = req("POST", f"/wp/v2/nadlan_property/{pid}", {"content": content, "featured_media": fid, "meta": {"photos_csv": photos_csv}})
        raw = ((r or {}).get("content") or {}).get("raw", "")
        row.update({"http": st, "featured_saved": (r or {}).get("featured_media"), "saved_chars": len(raw), "photo_fig_saved": "nlx-plate--photo" in raw, "gallery_saved": "nlx-gallery" in raw, "link": (r or {}).get("link")})
        time.sleep(0.4)
    results[L] = row
    print(L, json.dumps(row, ensure_ascii=False))

if "--verify" in ARGS:
    for it in idx:
        L = it["id"]
        if ONLY and L not in ONLY:
            continue
        link = WP + "/properties/" + it["slug"]["he"] + "/"
        try:
            with urllib.request.urlopen(urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"}), timeout=90) as resp:
                s = resp.read().decode("utf-8", "replace"); code = resp.status
        except urllib.error.HTTPError as e:
            code = e.code; s = ""
        og = re.search(r'<meta property="og:image" content="([^"]+)"', s)
        print(L, code, "h1=" + str(len(re.findall(r"<h1[\s>]", s))), "photo-mast=" + str("nlx-plate--photo" in s), "gallery=" + str(s.count('class="nlx-gallery"')), "og:image=" + (og.group(1).split("/")[-1] if og else "-"), "illustration-caption=" + str("האיור אינו מתאר" in s))
json.dump(results, open(os.path.join(HERE, "meital_photos_result.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done apply=%s" % APPLY)
