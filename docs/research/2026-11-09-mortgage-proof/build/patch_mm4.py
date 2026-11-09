# -*- coding: utf-8 -*-
"""Round R part 4: drop the Stripe/PMS defer filter from the speed block (the rewrite test did not bring the WhatsApp bar forward,
and Ben's rule of 6.11 keeps those scripts as they are). The font preload stays."""
import io, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
F = os.path.join(REPO, "plugins", "nadlan-config", "inc", "mortgage-market.php")
b = io.open(F, encoding="utf-8", newline="").read()
s = b.replace(chr(13) + chr(10), chr(10))
i = s.index("\tadd_filter( 'script_loader_tag', function ( $tag, $handle, $src ) {")
j = s.index("\t}, 20, 3 );\n", i) + len("\t}, 20, 3 );\n")
s = s[:i] + s[j:]
s = s.replace("/* 1.72.615 (HAD-675): phone speed on the pages that hold the market section. Fonts first, blocking payment scripts deferred. */",
              "/* 1.72.615 (HAD-675): phone speed on the pages that hold the market section: the H1 and text fonts are fetched first, so the\n"
              "   first paint already has the final line breaks (CLS 0.179 -> 0.07 on a slow phone, scratchpad probe 9.11.2026). */", 1)
assert "script_loader_tag" not in s and "nadlan_mm_font_preload" in s
io.open(F, "w", encoding="utf-8", newline="").write(s.replace(chr(10), chr(13) + chr(10)))
print("ok")
