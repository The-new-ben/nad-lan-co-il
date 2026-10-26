# -*- coding: utf-8 -*-
"""G5 preview only: what [nadlan_rent_listings] prints, rebuilt from the LIVE /properties/?listing_type=rent HTML read on 26.10.2026
(a public GET; the cards are the archive's own nadlan_plist_card() markup). The real page never carries this snapshot: the shortcode
renders the live count and cards from the database (instruments-snippet.md, block 3). Demo listings are dropped, as the shortcode does.
  python build_listings_snapshot.py <saved archive html>"""
import collections, io, os, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
src = io.open(sys.argv[1], encoding="utf-8").read()
cards = [m.group(0) for m in re.finditer(r'<a class="nlpl-card[^"]*" href="[^"]+".*?</a>', src, re.S) if "nlpl-card--demo" not in m.group(0)]
cities = collections.Counter(re.sub(r"<[^>]+>", "", re.search(r'nlpl-kicker">(.*?)</span>', c).group(1)).split(",")[-1].split("·")[-1].strip() for c in cards)
CSS = io.open(os.path.join(H, "listings.css"), encoding="utf-8").read()
parts = " ו־".join(["%d ב%s" % (n, c) if n > 1 else "אחת ב%s" % c for c, n in cities.most_common()])
html = ('<style id="nlrh-list-css">%s</style><div class="nlrh-list"><p class="nlrh-count"><b>%d</b> מודעות להשכרה באתר: %s.</p><div class="nlpl-grid">%s</div>'
        '<p class="nlrh-more"><a href="https://nad-lan.co.il/properties/?listing_type=rent">לכל המודעות באתר, עם סינון לפי עיר, חדרים ומחיר</a></p></div>' % (CSS, len(cards), parts, "".join(cards)))
io.open(os.path.join(H, "preview", "listings-snapshot.html"), "w", encoding="utf-8").write(html)
print("snapshot: %d real listings (%s)" % (len(cards), dict(cities)))
