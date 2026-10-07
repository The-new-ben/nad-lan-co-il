# Alignment check: pages that put Rova 4 places in the Old North (7.10.2026)

Companion to align-edits.json. Nothing was published and the site was not touched. Facts: facts.md in this folder.

## 1. Method

- Raw content: `GET https://nad-lan.co.il/wp-json/wp/v2/pages/<id>?_fields=id,link,title,content,yoast_head_json`
  (content.rendered), retrieved 7.10.2026 about 08:10 UTC. Ids: 4884 /north-tel-aviv/old-north/, 4885 /north-tel-aviv/bavli/
  (via `?slug=bavli`), 4883 /north-tel-aviv/miriam-hahashmonait/ (via `?slug=miriam-hahashmonait`).
- Every "old" string was copied from content.rendered (tags included) and checked by script: it matches its field exactly
  once in the live text, and still exactly once when the edits are applied in order. 44 of 44 passed. No new text contains
  an em dash, an en dash or "!".
- Basis: Rova 3 = the Old North, west of Ibn Gabirol (R1, R11). Rova 4 = הצפון החדש, east of Ibn Gabirol, with Kikar
  HaMedina (R6), Bavli (R5) and Miriam HaHashmonait street, which the official street list puts in "הצפון החדש, החלק
  הצפוני" (R13).

## 2. Edits per page

| page | edits | link edits | what was wrong |
|---|---|---|---|
| 4884 /north-tel-aviv/old-north/ | 4 | 1 | the Old North's eastern edge given as "אבן גבירול וסביבת כיכר המדינה"; Miriam HaHashmonait presented as an Old North project (card + renewal paragraph) |
| 4885 /north-tel-aviv/bavli/ | 9 | 1 | eyebrow "שכונה · הצפון הישן"; "on the seam with the Old North"; "בצפון הוותיק" (twice); "the classic Old North"; "other parts of the Old North"; "belongs to the Old North"; the FAQ "is Bavli part of the Old North" answered as yes |
| 4883 /north-tel-aviv/miriam-hahashmonait/ | 31 | 1 | the whole page places the street in the Old North: title/H1, Yoast title, Yoast description, JSON-LD headline, eyebrow, opening, card, note, an H2 section, buyer/price/FAQ/investor lines, table cells, and the multilingual keyword table (Old North / старый север / القديم) |

Proposed title and H1 for the Miriam HaHashmonait page: **מרים החשמונאית: התחדשות עירונית בצפון החדש** (a colon instead of
the spaced dash, per the language law). Yoast title: the same + " | נדל״ן חכם". Search Console queries for this page are the
street name only, so the change is SEO-safe.

Link sentences (one per page, anchor "רובע 4", `https://nad-lan.co.il/north-tel-aviv/rova-4/`):
- Old North, end of the boundaries paragraph: "ממזרח לאבן גבירול מתחיל רובע 4, הצפון החדש, ובו כיכר המדינה."
- Bavli, end of the first "מיקום וגבולות" paragraph: "על הרובע כולו, הרחובות, התוכנית ומחירי הדירות: רובע 4."
- Miriam HaHashmonait, the further-reading list: a "רובע 4" item, with the Old North item kept as "the neighbouring quarter,
  west of Ibn Gabirol".
The new page returns 404 today, so apply the three link edits only after it is live.

## 3. Left as is, on purpose

- Mentions that only say "near" (near the Old North, near Kikar HaMedina), as instructed. Examples: Old North page "קרבתו
  ... לכיכר המדינה", "שכונת בבלי סמוכה למרחב הצפון הישן"; Miriam page "בשל הקרבה לפארק הירקון ולצפון הישן".
- Comparisons that keep the two areas apart: the Old North page's "אינו זהה לאזורים כמו בבלי ... כיכר המדינה"; the Bavli
  page's comparison table (הצפון הישן המערבי / המרכזי); the Miriam price-table row "דירה ישנה בצפון הישן".
- The Bavli H2 "השוואה לשכונות סמוכות בצפון הישן" (a comparison heading, not a location claim).
- The hero CTA buttons on the Bavli and Miriam pages that lead to /north-tel-aviv/old-north/. They are navigation, not a
  claim. Optional, the owner's call: point the Miriam button to the Rova 4 page once it is live.
- The Old North page's renewal table row "כמו במתחמים באזור מרים החשמונאית" (an example of a project type).

## 4. Found but not edited: no source to settle it

- Bavli page: "דרך ההלכה בדרום" as Bavli's southern boundary. Not a quarter error, and facts.md has no source for Bavli's
  southern line. Worth checking separately.
- Miriam page: claims about the street's own projects (Shikun Poalei HaNamal ~381 units, Acro / Ken HaTor ~104 units, Miriam
  HaHashmonait 32-34) were not reviewed. They are outside this task.

## 5. Other live pages: search for "הצפון הישן" (pages and posts)

`/wp-json/wp/v2/pages?search=הצפון הישן&per_page=100` returned 20 pages; `/posts?...` returned 1. I also searched pages and
posts for "כיכר המדינה", "צפון ישן", "רובע 4", "הצפון החדש", "old north", "Kikar", "בבלי" and "מרים החשמונאית" (116 unique
items), extracted the text, and flagged every sentence that puts Kikar HaMedina, Bavli or Miriam HaHashmonait inside the Old
North, or calls Kikar HaMedina "Old North" in any language. I also checked /projects/park-bavli/ (it is not a WP page).

**Result: apart from the three pages above, no live page calls Kikar HaMedina the Old North.** Close calls, none needing a
fix:

| page | sentence | verdict |
|---|---|---|
| /celebs-homes/ | "מגדלי כיכר המדינה, רובע שדה דב על קו החוף והצפון הישן"; "ובצפון הישן ובבבלי נקנו פנטהאוזים" | lists them separately: OK |
| /investment-apartment/tel-aviv-investment-neighborhoods/ | "לב העיר, הצפון הישן, חלקים מהצפון החדש, סביב כיכר המדינה" | separate items: OK |
| /property-value/luxury-apartments-tel-aviv/ | "כיכר המדינה מציעה ... קרבה לצפון הישן" | "near": OK |
| /tel-aviv-luxury-apartment-prices/ | a table row labelled "צפון ישן וכיכר המדינה" | groups the two areas in one row label; does not say Kikar is in the Old North. Optional: split the row |
| /new-projects/north-tel-aviv-new-projects/ | lists "הצפון הישן, הצפון החדש, בבלי ..." as separate markets | OK, and it already uses "הצפון החדש" |
| /projects/park-bavli/ | "סמוך ... לצפון הישן"; "הצפון הישן, אזור כיכר המדינה" as separate areas | "near" and separate items: OK |
| /north-tel-aviv/ (hub, 4866) | lists "רמת אביב, נווה אביבים, שכונת ל׳, הצפון הישן, בבלי ורובע שדה דב" | not wrong, but the hub never names הצפון החדש / רובע 4 or Kikar HaMedina; it should link down to the new page once it is live (content addition, not a correction) |

## 6. Apply notes

- Order matters only where two edits sit in the same paragraph (Bavli edits 7, 8 and 9, Old North edits 1 and 2); they do not
  overlap, and the sequential check passed.
- For the "title" field, also confirm that the Yoast title is not stored separately (if it is, apply the "yoast_title"
  edit too) and that the breadcrumb/JSON-LD in the content uses the new headline (edit 17).
- After applying: re-fetch each page, run `python tools/source_audit.py` on the three URLs (public-source law), and check
  that the H1 on /north-tel-aviv/miriam-hahashmonait/ reads "מרים החשמונאית: התחדשות עירונית בצפון החדש".
