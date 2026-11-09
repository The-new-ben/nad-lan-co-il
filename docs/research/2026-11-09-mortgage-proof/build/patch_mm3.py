# -*- coding: utf-8 -*-
"""Round R part 3: the font files Google serves differ by platform (Windows gets hinted files; Android, iPhone and Mac share one set).
Read them as a phone does and preload them only on phone widths (media="(max-width: 600px)"), so a desktop never downloads twice."""
import io, os
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
F = os.path.join(REPO, "plugins", "nadlan-config", "inc", "mortgage-market.php")
s = io.open(F, encoding="utf-8", newline="").read()
pairs = [
    ("'user-agent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36' ) );",
     "'user-agent' => 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Mobile Safari/537.36' ) );  // phones and Mac get these files; Windows gets hinted ones"),
    ('as="font" type="font/woff2" crossorigin>', 'as="font" type="font/woff2" media="(max-width: 600px)" crossorigin>'),
]
for a, b in pairs:
    assert s.count(a) == 1, (a[:60], s.count(a))
    s = s.replace(a, b)
assert s.count("nadlan_mm_font_preload_v1") == 2
s = s.replace("nadlan_mm_font_preload_v1", "nadlan_mm_font_preload_v2")
io.open(F, "w", encoding="utf-8", newline="").write(s)
print("ok")
