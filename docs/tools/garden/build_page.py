# -*- coding: utf-8 -*-
"""HAD-669 R12e: builds docs/tools/garden/page.html for /tel-aviv-garden-apartments/ from the ChatGPT Pro article
(docs/research/2026-11-03-garden/garden.he.article.html). Rendered order (the content-first law): the answer paragraph (the
article's first <p>), three buttons, the numbers strip, the deals map, the worth tool, the real listings, the street lookup,
the ground-floor comparison, then the rest of the article (its FAQ feeds the FAQPage schema)."""
import io, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
art = io.open(os.path.join(REPO, "docs", "research", "2026-11-03-garden", "garden.he.article.html"), encoding="utf-8").read().replace("\r\n", "\n")
m = re.search(r"<p>.*?</p>", art, re.S)
first, rest = m.group(0), art[m.end():].strip()
sc = lambda i: '<!-- wp:shortcode -->\n[%s]\n<!-- /wp:shortcode -->' % i
cta = ('<div class="gdp-cta"><a class="is-main" href="#gdn-worth">מה שווה דירת גן בשכונה שלכם</a><a href="#gdn-list">דירות גן שמוצעות עכשיו</a>'
       '<a href="/post-listing/">פרסמו דירת גן</a></div>')
strip = ('<div class="gdp-strip"><div><strong>81</strong><span>עסקאות דירות גן, 2020 עד 2024</span></div><div><strong>5.4 מיליון ₪</strong><span>המחיר החציוני</span></div>'
         '<div><strong>₪44,422</strong><span>החציון למ״ר בנוי</span></div><div><strong>115 מ״ר</strong><span>השטח הבנוי החציוני</span></div></div>')
out = [first, cta, strip, '<div id="gdn-map">\n' + sc('nadlan_tool id="gdnmap"') + '\n</div>', '<div id="gdn-worth">\n' + sc('nadlan_tool id="gdnworth"') + '\n</div>',
       '<h2 id="gdn-list">דירות גן בתל אביב שמוצעות עכשיו באתר</h2>\n' + sc('nadlan_garden_listings'),
       '<div id="gdn-street">\n' + sc('nadlan_tool id="gdnstreet"') + '\n</div>', '<div id="gdn-ground">\n' + sc('nadlan_tool id="gdnground"') + '\n</div>', rest]
io.open(os.path.join(H, "page.html"), "w", encoding="utf-8", newline="\n").write("\n\n".join(out) + "\n")
print("page.html", sum(len(x) for x in out), "chars")
