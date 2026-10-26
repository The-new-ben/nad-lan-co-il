# -*- coding: utf-8 -*-
"""Redraw the featured chart of post 4960 /buy-property-israel-foreign-buyers/ (26.10.2026): the old picture had the Canada value sitting
on the brand footer and the retired cream and brass palette. Same facts as the post text: Israel Ministry of Finance, Chief Economist,
residential review for March 2026, published 13.5.2026: 487 foreign-resident purchases in Q1 2026 (413 in Q1 2025); United States 238,
France 130, United Kingdom 57, Canada 16, Australia 10; the rest (36) is 487 minus the listed countries.
NadLan Instruments identity: white chart paper, ink #12202A, deep #1F4B5C, sea #2F6F86, line #D3DCE2, IBM Plex Sans and Plex Mono.
   python foreign_buyers_chart.py            -> renders preview/foreign-purchases-israel-q1-2026-v2.png (look at it first)
   python foreign_buyers_chart.py --upload   -> uploads it and sets it as the featured picture of post 4960 (old media 5007 is kept)"""
import json, os, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "preview", "foreign-purchases-israel-q1-2026-v2.png")
TOTAL, PREV = 487, 413
ROWS = [("United States", 238), ("France", 130), ("United Kingdom", 57), ("Canada", 16), ("Australia", 10)]
ROWS.append(("All other passports", TOTAL - sum(v for _, v in ROWS)))
assert ROWS[-1][1] == 36
ALT = ("Bar chart of foreign-resident home purchases in Israel in Q1 2026 by passport country: United States 238, France 130, "
       "United Kingdom 57, Canada 16, Australia 10, all other passports 36; 487 in total, up from 413 in Q1 2025.")
INK, INK2, DEEP, SEA, LINE, MUTE = "#12202A", "#3E4C58", "#1F4B5C", "#2F6F86", "#D3DCE2", "#9FB3BF"
SANS = "font-family:'IBM Plex Sans',system-ui,sans-serif"; MONO = "font-family:'IBM Plex Mono',ui-monospace,monospace"


def t(x, y, s, size, weight=400, fill=INK, mono=False, anchor="start", ls=0):
    return '<text x="%s" y="%s" text-anchor="%s" style="%s;font-size:%spx;font-weight:%s;letter-spacing:%spx" fill="%s">%s</text>' % (
        x, y, anchor, MONO if mono else SANS, size, weight, ls, fill, s)


def svg():
    g = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">', '<rect width="1200" height="630" fill="#fff"/>']
    for x in range(0, 1201, 40):
        g.append('<line x1="%d" y1="0" x2="%d" y2="630" stroke="#F0F3F6" stroke-width="1"/>' % (x, x))
    for y in range(0, 631, 40):
        g.append('<line x1="0" y1="%d" x2="1200" y2="%d" stroke="#F0F3F6" stroke-width="1"/>' % (y, y))
    g.append('<rect x="64" y="40" width="56" height="5" fill="%s"/>' % SEA)
    g.append(t(64, 82, "NADLAN · FOREIGN BUYERS IN ISRAEL", 17, 500, SEA, mono=True, ls=1.5))
    g.append(t(64, 132, "Foreign-resident home purchases, Q1 2026", 42, 600))
    g.append(t(64, 172, "By passport country · %d purchases, up %d%% from %d in Q1 2025" % (TOTAL, round(100.0 * (TOTAL - PREV) / PREV), PREV), 22, 400, INK2))
    x0, maxw, y = 340, 640, 212
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.5"/>' % (x0, y - 8, x0, y + len(ROWS) * 58 - 14, LINE))
    for i, (name, v) in enumerate(ROWS):
        w = max(4, maxw * v / float(ROWS[0][1])); c = DEEP if i == 0 else (MUTE if name.startswith("All other") else SEA)
        g.append(t(x0 - 18, y + 27, name, 22, 600 if i == 0 else 500, INK, anchor="end"))
        g.append('<rect x="%d" y="%d" width="%.1f" height="36" fill="%s"/>' % (x0, y + 3, w, c))
        g.append(t(x0 + w + 14, y + 29, "%d" % v, 24, 600, INK, mono=True))
        g.append(t(x0 + w + 14 + 14.5 * len(str(v)) + 14, y + 29, "%.1f%%" % (100.0 * v / TOTAL), 19, 400, INK2, mono=True))
        y += 58
    g.append('<line x1="64" y1="566" x2="1136" y2="566" stroke="%s" stroke-width="1"/>' % LINE)
    g.append(t(64, 597, "Source: Israel Ministry of Finance, Chief Economist, residential review for March 2026, published May 13, 2026", 16, 400, "#5E6A75"))
    g.append(t(1136, 597, "nad-lan.co.il", 17, 500, SEA, mono=True, anchor="end"))
    g.append("</svg>")
    return "".join(g)


def render():
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    html = ('<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">'
            '<style>html,body{margin:0;background:#fff}</style></head><body>%s</body></html>' % svg())
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        pg = b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        pg.set_content(html); pg.wait_for_function("document.fonts.status === 'loaded'"); pg.wait_for_timeout(600)
        print("fonts:", pg.evaluate("[...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight).join(', ')"))
        pg.screenshot(path=OUT, clip={"x": 0, "y": 0, "width": 1200, "height": 630})
        b.close()
    print("written", OUT, os.path.getsize(OUT), "bytes")


def upload():
    REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
    src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "fbc"}
    exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
    req = ns["req"]
    s, post, _ = req("GET", "/wp-json/wp/v2/posts/4960?context=edit&_fields=featured_media,link")
    assert s == 200 and post["featured_media"] == 5007, (s, post.get("featured_media"))
    data = open(OUT, "rb").read()
    r = urllib.request.Request(ns["BASE"] + "/wp-json/wp/v2/media", data=data, method="POST")
    r.add_header("Authorization", ns["AUTH"]); r.add_header("User-Agent", ns["UA"]); r.add_header("Content-Type", "image/png")
    r.add_header("Content-Disposition", 'attachment; filename="foreign-purchases-israel-q1-2026-v2.png"')
    with urllib.request.urlopen(r, timeout=180) as resp:
        m = json.loads(resp.read().decode())
    mid = m["id"]; print("media", mid, m.get("source_url"))
    print("meta:", req("POST", "/wp-json/wp/v2/media/%d" % mid, {"alt_text": ALT, "title": "Foreign-resident home purchases in Israel, Q1 2026",
                                                                 "caption": "Source: Israel Ministry of Finance, Chief Economist, May 13, 2026"})[0])
    print("post:", req("POST", "/wp-json/wp/v2/posts/4960", {"featured_media": mid})[0])
    back = req("GET", "/wp-json/wp/v2/posts/4960?context=edit&_fields=featured_media")[1]["featured_media"]
    time.sleep(3)
    page = urllib.request.urlopen(urllib.request.Request(post["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
    print("read-back", back == mid, "| picture on page", "foreign-purchases-israel-q1-2026-v2" in page, "| og:image",
          'og:image" content="' in page and "q1-2026-v2" in page.split('og:image" content="')[1][:200], "| old media kept, id 5007")


if __name__ == "__main__":
    upload() if "--upload" in sys.argv else render()
