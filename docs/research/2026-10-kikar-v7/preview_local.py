# -*- coding: utf-8 -*-
"""V7: a local, read-only preview of a Kikar page with its NEW article, to look at before the release.

    python docs/research/2026-10-kikar-v7/preview_local.py he     -> preview/hamedina-he.html

The live page is fetched (GET only), and the post-content part the article owns (the sections inside the
div.nadlan-project-article wrapper, and the lead in div.nl-lead) is replaced by article-<lang>.html. Styles and scripts stay the
live page's (absolute URLs), so the reading column looks as it will. Nothing is written anywhere but preview/."""
import io, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = {"he": "hamedina", "en": "hamedina-en", "fr": "hamedina-fr", "ru": "hamedina-ru", "ar": "hamedina-ar"}
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128.0"}


def block(h, start_pat):
    m = re.search(start_pat, h)
    if not m:
        raise SystemExit("not found: " + start_pat)
    s = m.start()
    tag = re.match(r"<(\w+)", h[s:]).group(1)
    d = 0
    for t in re.finditer(r"<(/?)%s\b[^>]*>" % tag, h[s:]):
        d += -1 if t.group(1) else 1
        if d == 0:
            return s, s + t.end()


def main():
    lang = sys.argv[1]
    url = "https://nad-lan.co.il/projects/%s/" % SLUG[lang]
    h = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode("utf-8")
    art = io.open(os.path.join(HERE, "article-%s.html" % lang), encoding="utf-8").read().strip()
    lead = re.match(r"<p>(.*?)</p>", art, re.S).group(0)
    rest = art[len(lead):].replace('<div class="nadlan-project-article"></div>', "")
    a, b = block(h, r'<div class="nadlan-project-article nadlan-guide">')
    inner_open = re.match(r"<div[^>]*>", h[a:]).group(0)
    h = h[:a] + inner_open + rest + "</div>" + h[b:]
    a, b = block(h, r'<div class="nl-lead"[^>]*>')
    lead_open = re.match(r"<div[^>]*>", h[a:]).group(0)
    h = h[:a] + lead_open + lead + "</div>" + h[b:]
    h = h.replace("<head>", '<head><base href="https://nad-lan.co.il/">', 1)
    os.makedirs(os.path.join(HERE, "preview"), exist_ok=True)
    out = os.path.join(HERE, "preview", "hamedina-%s.html" % lang)
    io.open(out, "w", encoding="utf-8").write(h)
    print("wrote", out)


if __name__ == "__main__":
    main()
