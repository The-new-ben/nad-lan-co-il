# -*- coding: utf-8 -*-
"""Split a page's content.rendered into text blocks (outside <script>, <style>, and <section id="nlpg">), keep raw offsets."""
import json, re, os, sys, html
HERE = os.path.dirname(os.path.abspath(__file__))

def strip_ranges(c):
    """return list of (start,end) ranges to ignore: script, style, nlpg section."""
    rng = []
    for m in re.finditer(r"<(script|style)\b.*?</\1>", c, re.S):
        rng.append((m.start(), m.end(), m.group(1)))
    i = c.find('<section id="nlpg"')
    if i < 0:
        m = re.search(r'<section[^>]*id="nlpg"', c)
        i = m.start() if m else -1
    if i >= 0:
        depth, j = 0, i
        for m in re.finditer(r"<(/?)section\b", c[i:]):
            if m.group(1) == "":
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    j = i + m.end() + c[i + m.end():].find(">") + 1
                    break
        rng.append((i, j, "nlpg"))
    return rng

BLOCK = re.compile(r"<(p|li|tr|h[1-6]|summary|figcaption|blockquote|caption)\b[^>]*>(.*?)</\1>", re.S)

def blocks(c):
    rng = strip_ranges(c)
    def ign(a):
        return any(s <= a < e for s, e, _ in rng)
    out = []
    for m in BLOCK.finditer(c):
        if ign(m.start()):
            continue
        inner = m.group(2)
        if m.group(1) == "tr":
            cells = re.findall(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", inner, re.S)
            txt = " | ".join(html.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in cells)
        else:
            txt = html.unescape(re.sub(r"<[^>]+>", "", inner)).strip()
        out.append({"tag": m.group(1), "start": m.start(), "end": m.end(), "text": re.sub(r"\s+", " ", txt)})
    # also text inside divs with no block (cards <b>...) : capture div.card
    for m in re.finditer(r'<div class="card"[^>]*>(.*?)</div>', c, re.S):
        if ign(m.start()):
            continue
        inner = m.group(1)
        if BLOCK.search(inner):
            continue
        out.append({"tag": "card", "start": m.start(), "end": m.end(), "text": re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", inner)).strip())})
    out.sort(key=lambda b: b["start"])
    return out, rng

if __name__ == "__main__":
    slug = sys.argv[1]
    p = json.load(open(os.path.join(HERE, "pages", slug + ".json"), encoding="utf-8"))
    c = p["content"]["rendered"]
    bl, rng = blocks(c)
    print(slug, p["id"], "ranges:", [(s, e, k) for s, e, k in rng])
    onlynum = "--all" not in sys.argv
    for k, b in enumerate(bl):
        if onlynum and not re.search(r"\d", b["text"]):
            if b["tag"].startswith("h"):
                print(f"## [{k}] {b['tag']}: {b['text']}")
            continue
        print(f"[{k}] {b['tag']}@{b['start']}: {b['text']}")
