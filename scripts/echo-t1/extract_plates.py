# -*- coding: utf-8 -*-
"""Extract base64-embedded plate images from echo-city-redesign.html."""
import base64, io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
SRC = r"C:\Users\777\Downloads\echo-city-redesign.html"
OUT = os.path.dirname(os.path.abspath(__file__))
html = open(SRC, encoding="utf-8", errors="replace").read()
print("html chars:", len(html))
imgs = list(re.finditer(r'data:image/(jpeg|png|webp);base64,([A-Za-z0-9+/=]+)', html))
print("embedded images:", len(imgs))
for i, m in enumerate(imgs):
    kind = m.group(1)
    data = base64.b64decode(m.group(2))
    ctx = html[max(0, m.start()-700):m.start()]
    label = "unknown"
    low = ctx.lower()
    if "stricker" in low or "שטריקר" in low or "ברנדיס" in low:
        label = "stricker"
    elif "bnei" in low or "בני דן" in low:
        label = "bnei-dan"
    path = os.path.join(OUT, f"plate-{i}-{label}.{ 'jpg' if kind=='jpeg' else kind }")
    with open(path, "wb") as f:
        f.write(data)
    print(f"#{i} {label} {kind} {len(data):,}b -> {os.path.basename(path)}")
    alts = re.findall(r'alt="([^"]{0,120})"', html[m.start():m.start()+3000])
    if alts:
        print("   nearest alt:", alts[0])
# title / h1 / headings overview of the file
title = re.search(r"<title>(.*?)</title>", html, re.S)
print("file title:", title.group(1) if title else "none")
h1s = [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S)]
print("h1:", h1s)
h2s = [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.S)]
print(f"h2 ({len(h2s)}):")
for h in h2s[:20]:
    print("  -", h[:90])
print("has form:", "<form" in html, "| lead endpoint ref:", "nadlan/v1/lead" in html)
print("em-dash count:", html.count("—"), "| en-dash:", html.count("–"))
