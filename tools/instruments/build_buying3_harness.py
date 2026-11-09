# -*- coding: utf-8 -*-
"""HAD-686: the local preview of the guide's reading layer and the five Phase 3 tools of /buying-apartment/ (page 9).

    python tools/instruments/build_buying3_harness.py   -> tools/instruments/harness_buying3.html (the live theme shell, offline)
                                                           tools/instruments/harness_buying3_plain.html (no theme)
    python tools/instruments/build_buying3_harness.py <content.html> <tag>   -> harness_<tag>.html and harness_<tag>_plain.html
      (any page content, for example docs/research/2026-11-08-buying-guide-re/page-9-v3.html with the tag v3)
Steps: tools/instruments/harness_buying3_src.html (the guide map, five chapters, the glossary and the shortcodes bpay, bsign,
breg and bmemo with h="3" inside chapters and bkeys outside) gets the page's own CSS block (the <style id="nlbp-css"> of
docs/research/2026-11-07-prices-buying/page-9-new.html), then goes through the REAL shortcode (render_buying_page.php: WordPress
stubs + inc/instruments.php + inc/buying-hub.php, so the server summaries and the h3 option run as on the site).
The theme shell is the copy of the live page that build_buying_harness.py saved (harness_buying.html): its theme CSS, header,
footer and content width, with the old content and the old tool tags taken out. No network: nothing is fetched here.
Writes only the harness files and the rendered parts next to them (_buying3_*.html/json)."""
import io
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "harness_buying3_src.html")
TAG = sys.argv[2] if len(sys.argv) > 2 else "buying3"
PAGE9 = os.path.join(REPO, "docs", "research", "2026-11-07-prices-buying", "page-9-new.html")
SHELL = os.path.join(HERE, "harness_buying.html")
BASE = "../../plugins/nadlan-config/"
FONTS = "https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap"
TOOLS = ["prices-common", "buying", "buying2", "buying3"]


def render():
    src = io.open(SRC, encoding="utf-8").read()
    css = re.search(r'<style id="nlbp-css">.*?</style>', io.open(PAGE9, encoding="utf-8").read(), flags=re.S)
    src = src.replace("<!--nlbp-css-->", css.group(0) if css else "")
    tmp = os.path.join(HERE, "_" + TAG + "_src_full.html")
    io.open(tmp, "w", encoding="utf-8", newline="\n").write(src)
    out, ld = os.path.join(HERE, "_" + TAG + "_content.html"), os.path.join(HERE, "_" + TAG + "_ld.json")
    r = subprocess.run(["php", os.path.join(HERE, "render_buying_page.php"), tmp, out, ld, BASE], capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL)
    print(r.stdout.strip(), r.stderr.strip())
    if r.returncode:
        raise SystemExit("render failed")
    return io.open(out, encoding="utf-8").read(), io.open(ld, encoding="utf-8").read()


def head_tags(ld):
    return ('<link rel="stylesheet" href="' + FONTS + '">\n<link rel="stylesheet" href="' + BASE + 'assets/instruments/core.css">\n'
            '<link rel="stylesheet" href="' + BASE + 'assets/instruments/tools/buying3.css">\n'
            '<script type="application/ld+json" id="nadlan-nli-ld">' + re.sub(r"\s+", " ", ld) + '</script>\n')


def tail_tags():
    s = '<script src="' + BASE + 'assets/instruments/core.js" defer></script>\n'
    for t in TOOLS:
        s += '<script src="' + BASE + 'assets/instruments/tools/' + t + '.js" defer></script>\n'
    return s


def plain(content, ld):
    return ('<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>קניית דירה: שכבת הקריאה והכלים החדשים (תצוגה מקומית)</title>\n' + head_tags(ld) +
            '<style>body{margin:0;background:#fff;color:#12202A;font-family:system-ui}.entry-content{padding:0 16px}'
            '.entry-content>*{max-width:760px;margin-left:auto;margin-right:auto}.entry-content>.alignwide{max-width:1200px}</style></head>'
            '<body><main><div class="entry-content">' + content + '</div></main>\n' + tail_tags() + '</body></html>')


def themed(content, ld):
    html = io.open(SHELL, encoding="utf-8").read()
    html = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?family=Karantina[^"]*">\n?', "", html)
    html = re.sub(r'<link rel="stylesheet" href="\.\./\.\./plugins/nadlan-config/assets/instruments/[^"]*">\n?', "", html)
    html = re.sub(r'<script type="application/ld\+json" id="nadlan-nli-ld">.*?</script>\n?', "", html, flags=re.S)
    html = re.sub(r'<script src="\.\./\.\./plugins/nadlan-config/[^"]*"[^>]*></script>\n?', "", html)
    a = html.find('<div class="entry-content')
    a = html.find(">", a) + 1
    b = html.find("</main>", a)
    if a <= 0 or b < 0:
        raise SystemExit("the saved shell changed: no entry-content / main")
    b = html.rfind("</div>", a, b)
    html = html[:a] + content + html[b:]
    html = html.replace("</head>", head_tags(ld) + "</head>", 1).replace("</body>", tail_tags() + "</body>", 1)
    return html.replace("\u2014", "-").replace("\u2013", "-")  # two long dashes sit in the theme's own CSS comments; this local copy stays dash-free


def main():
    content, ld = render()
    io.open(os.path.join(HERE, "harness_" + TAG + "_plain.html"), "w", encoding="utf-8", newline="\n").write(plain(content, ld))
    print("wrote harness_" + TAG + "_plain.html")
    if os.path.exists(SHELL):
        io.open(os.path.join(HERE, "harness_" + TAG + ".html"), "w", encoding="utf-8", newline="\n").write(themed(content, ld))
        print("wrote harness_" + TAG + ".html (the saved live theme shell)")
    else:
        print("no saved shell (run build_buying_harness.py once); only the plain harness was written")


if __name__ == "__main__":
    main()
