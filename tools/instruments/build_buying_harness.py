# -*- coding: utf-8 -*-
"""HAD-683 (from build_prices_harness.py): the local preview of the new /buying-apartment/ (page 9) with its four tools.

    python tools/instruments/build_prices_harness.py            -> tools/instruments/harness_buying.html (live theme shell)
                                                                   tools/instruments/harness_buying_plain.html (no theme)
Steps: render docs/research/2026-11-07-prices-buying/page-9-new.html through the REAL shortcode (render_buying_page.php:
WordPress stubs + plugins/nadlan-config/inc/instruments.php), then put it in
  - the live page's own shell (a GET of https://nad-lan.co.il/buying-apartment/, every <script> removed, the old content
    swapped for the new one): the theme CSS, header, footer and content width exactly as on the site;
  - a plain shell (WordPress constrained layout: 760 px content, 1200 px wide), for offline work.
The tools load from the repo (core.css, core.js, prices-common.js, pmarket.js, pcity.js, panatomy.js, data/*.json).
Reads the live site only (GET); writes only the two harness files and the rendered parts next to them (_prices_*.html/json)."""
import io
import os
import re
import subprocess
import sys
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
PAGE = os.path.join(REPO, "docs", "research", "2026-11-07-prices-buying", "page-9-new.html")
BASE = "../../plugins/nadlan-config/"
FONTS = "https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap"
TOOLS = ["prices-common", "buying", "buying2", "buying3"]  # buying3 (HAD-686): the five Phase 3 tools and the reading layer


def render():
    out, ld = os.path.join(HERE, "_buying_content.html"), os.path.join(HERE, "_buying_ld.json")
    r = subprocess.run(["php", os.path.join(HERE, "render_buying_page.php"), PAGE, out, ld, BASE], capture_output=True, text=True, encoding="utf-8")
    print(r.stdout.strip(), r.stderr.strip())
    if r.returncode:
        raise SystemExit("render failed")
    return io.open(out, encoding="utf-8").read(), io.open(ld, encoding="utf-8").read()


def head_tags(ld):
    return ('<link rel="stylesheet" href="' + FONTS + '">\n<link rel="stylesheet" href="' + BASE + 'assets/instruments/core.css">\n<link rel="stylesheet" href="' + BASE + 'assets/instruments/tools/buying3.css">\n'
            '<script type="application/ld+json" id="nadlan-nli-ld">' + re.sub(r"\s+", " ", ld) + '</script>\n')


def tail_tags():
    s = '<script src="' + BASE + 'assets/instruments/core.js" defer></script>\n'
    for t in TOOLS:
        s += '<script src="' + BASE + 'assets/instruments/tools/' + t + '.js" defer></script>\n'
    return s


def plain(content, ld):
    return ('<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>קניית דירה: תצוגה מקומית</title>\n' + head_tags(ld) +
            '<style>body{margin:0;background:#fff;color:#12202A;font-family:system-ui}.entry-content{padding:0 16px}'
            '.entry-content>*{max-width:760px;margin-left:auto;margin-right:auto}.entry-content>.alignwide{max-width:1200px}</style></head>'
            '<body><main><div class="entry-content">' + content.replace("<!--nlpg-live-->", '<p style="border:1px dashed #999;padding:12px">[nadlan_price_guide key="apartment-prices"] renders here on the site</p>') + '</div></main>\n' + tail_tags() + '</body></html>')


def live(content, ld):
    req = urllib.request.Request("https://nad-lan.co.il/buying-apartment/", headers={"User-Agent": "Mozilla/5.0 NadLan-local-preview"})
    html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
    g = re.search(r'<style id="nlpg-css">.*?<script id="nlpg-js">.*?</script>', html, flags=re.S)  # the live [nadlan_price_guide] block, as rendered
    content = content.replace("<!--nlpg-live-->", g.group(0) if g else "<p>[nadlan_price_guide] (not found on the live page)</p>")
    html = re.sub(r"<script\b(?![^>]*nlpg-js)[^>]*>.*?</script>", "", html, flags=re.S | re.I)  # nothing of the live site runs here, but the guide's own block
    a = html.find('<div class="entry-content')
    a = html.find(">", a) + 1
    b = html.find("</main>", a)
    if a <= 0 or b < 0:
        raise SystemExit("the live shell changed: no entry-content / main")
    b = html.rfind("</div>", a, b)
    html = html[:a] + content + html[b:]
    html = html.replace("</head>", head_tags(ld) + "</head>", 1).replace("</body>", tail_tags() + "</body>", 1)
    return html


def main():
    content, ld = render()
    io.open(os.path.join(HERE, "harness_buying_plain.html"), "w", encoding="utf-8").write(plain(content, ld))
    print("wrote harness_buying_plain.html")
    try:
        io.open(os.path.join(HERE, "harness_buying.html"), "w", encoding="utf-8").write(live(content, ld))
        print("wrote harness_buying.html (live theme shell)")
    except Exception as e:  # noqa: BLE001
        print("live shell skipped:", e)


if __name__ == "__main__":
    main()
