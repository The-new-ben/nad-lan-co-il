# Writing brief: the chapters of the buying guide (page 9, HAD-686)

You write original Hebrew chapters for https://nad-lan.co.il/buying-apartment/ (the owner of "קניית דירה"). Ben's order: every piece of information that any top Israeli guide has must be on this page, written better, with official sources. The integrator (another session) assembles your fragments into the page; you only write fragments and a coverage report.

## Inputs (read them)
- What is missing: `amit-vered-gaps.md` and `amit-vered-map.md` (365 units of Amit Vered; YES / PARTIAL / NO against our live page), `other-competitors-gaps.md` and `other-competitors-map.md` (Elkayam, Yoni Levy, ygoldlaw, prlaw, gov.il, Kol Zchut and others; units new versus Amit Vered), `competitor-metrics.md` (terms used by 3 or more competitors and absent from our page: use the ones that belong to your chapters, naturally).
- What is already on the page: `page-9-live-2026-11-09.html` (raw content; read the sections your chapters wrap so you do not repeat them) and `page-9-internal-links.txt` (internal links and their anchors).
- Facts: `sources-ledger-gov.md` and `sources-ledger-law.md`. A number or a legal rule enters the page ONLY if it is CONFIRMED there, or already stated on the live page with its source (the who-pays table, the deadlines table, the 13 programmes). If what you need is NOT CONFIRMED, write the idea without the number ("אגרה לפי תעריף רשות המקרקעין") and list it in your report under "missing facts".
- Search DNA: `serp-family-top5.md` (titles, people-also-ask, related searches). H3s are real questions and phrasings people type; never invent marketing headings.
- Design: the BuyingGuide component (design system v109), summarised in the class contract below.

## The chapters (the deal in order) and who writes what
| # | Chapter (H2) | Wraps existing live sections | Writer | New words (target) |
|---|---|---|---|---|
| 1 | לפני שמחפשים: מטרה, תקציב ומחיר נוח (existing H2) | that section, עלות כוללת, קניית דירה לפני מכירה (bsell), סיוע ברכישת דירה ראשונה, ההטבות לקונה (bhelp) | W1 | 600 |
| 2 | קודם המימון, אחר כך הדירה (existing H2) | that section | W1 | 700 |
| 3 | בחירת עיר ושכונה (existing H2) | that section, איך משווים מחיר דירה בצורה זהירה? | W1 | 300 |
| 4 | ביקור בדירה ובדיקה פיזית (new H2) | שאלות לשאול כשרואים דירה (bvisit), בדיקת מצב הדירה והבניין | W1 | 900 |
| 5 | בדיקת זכויות ומסמכים (existing H2) | that section and its H3 on a flat not registered in the land registry | W2 | 1,100 |
| 6 | new: the seller and who lives in the flat | none | W2 | 900 |
| 7 | new: the condominium file and the planning check | the existing H3 on building deviations moves here | W2 | 1,200 |
| 8 | new: the taxes in the deal, from the buyer's seat | מי משלם מה בעסקת דירה יד שנייה (bwho) | W3 | 1,300 |
| 9 | new: the memorandum and the negotiation | none (tool bmemo goes here) | W3 | 1,000 |
| 10 | new: the contract, its protections and the lawyer | תפקיד עורך הדין בקניית דירה | W4 | 1,600 |
| 11 | new: the payment schedule | none (tool bpay) | W4 | 600 |
| 12 | new: signing day | none (tool bsign) | W4 | 600 |
| 13 | new: the warning note | none | W5 | 900 |
| 14 | new: after signing: reports, mortgages and certificates | קניית דירה: המועדים אחרי החתימה, לוח זמנים לקניית דירה (bdates); tool breg goes here | W5 | 1,600 |
| 15 | new: handover | none (tool bkeys) | W5 | 600 |
| 16 | new: registration in your name | none | W5 | 600 |
| 17 | buying from a developer (new H2) | יד שנייה, מקבלן או להשקעה and its H3 on buying from a developer | W6 | 2,600 (Elkayam alone has 167 missing units) |
| 18 | new: special cases | none (the existing FAQ on a receiver stays in the FAQ; link to it) | W7 | 1,300 |
| + | FAQ additions (new questions only, from people-also-ask, related searches and competitors' FAQs) | the existing 19 questions stay | W7 | 1,400 |
| + | glossary: about 60 terms, one or two sentences each, each linked to its chapter | none | W7 | 1,500 |

Where sources disagree, `LEDGER-DECISIONS.md` decides.

For a NEW chapter you write the whole chapter (head and body). For an existing chapter you write ADDITIONS only: new H3 subsections, notes and tables that hold the missing units, plus one answer sentence and the "מה עושים בשלב הזה" box for the chapter head. Never rewrite or delete live text.

## Voice
- Hebrew of an Israeli real-estate portal: plain, warm, exact. Second person plural ("בודקים", "שימו לב", "אתם"). Short sentences. A reader at the kitchen table, not a law student.
- Concrete: who does it, where, when, what it costs, what proves it is done. Practical moments ("מהשטח") are welcome when they are general practice and stated as such; never invented stories, never named people or companies in negative topics.
- Not legal advice, but no hedging in every sentence: say it once where it matters ("עורך הדין שלכם בודק את זה").
- Forbidden: the word "אטלס" or "Atlas"; slogan lines ("אפס X"); tech or UI talk about the site ("הכלי שלנו מחשב באמצעות"); long dashes (U+2013, U+2014) anywhere; "דוגמה" labels on real rules; superlatives about ourselves; the word "פראייר" outside the existing FAQ.
- Do not open a chapter or a paragraph with the exact phrase "קניית דירה". Use variants: רכישת דירה, עסקת הדירה, הקונים, הדירה שבחרתם.

## Keyword guard
- Never START an H2 or H3 with a protected head phrase owned by another page: משכנתא / מחשבון משכנתא (/mortgage-calculator/), מס רכישה / מחשבון מס רכישה (/purchase-tax-calculator/), בדק בית (/home-inspection/), שמאי מקרקעין (/real-estate-appraiser/), עורך דין מקרקעין (/real-estate-lawyer/), דירות מקבלן, דירות חדשות, דירות על הנייר, פרויקטים חדשים (/projects/), דירה בהנחה / מחיר למשתכן (/dira-behanacha/), הערכת שווי דירה / שווי דירה (/property-value-estimator/), דירה להשקעה (/investment/), מחירי דירות (/apartment-prices/), עלויות קניית דירה / מחשבון קניית דירה (/apartment-purchase-cost-calculator/). In body text these words are fine.
- Link to a child page once per chapter where it helps, with the anchor that already appears in `page-9-internal-links.txt` for that URL (or the child's own H1). Do not add links to other sites except the official sources.

## HTML contract (exactly these classes; plain HTML, no inline styles, no scripts)
```html
<section class="nlbg-ch" id="nlbg-c13" data-ch="c13">
  <p class="nlbg-kick">שלב 13 מתוך 18 · אחרי החתימה</p>
  <h2>...</h2>
  <p class="nlbg-ans">One answer sentence, under 40 words, quotable as is.</p>
  <div class="nlbg-who"><span>רשם המקרקעין (טאבו)</span><span>עורך הדין</span></div>
  <div class="nlbg-todo"><p class="nlbg-todo__t">מה עושים בשלב הזה</p><ol><li>verb first</li></ol></div>
  <h3>A question people ask</h3>
  <p>...</p>
  <div class="nlbg-note nlbg-note--fig"><p class="nlbg-note__lab">מספר רשמי</p><p>אגרת ...: <b>188 ₪</b></p><p class="nlbg-src">מקור: <a href="OFFICIAL URL">name of the page</a> · נבדק 9.11.2026</p></div>
  <div class="nlbg-note nlbg-note--stop"><p class="nlbg-note__lab">עצרו</p><p>...</p></div>
  <div class="nlbg-note nlbg-note--field"><p class="nlbg-note__lab">מהשטח</p><p>...</p></div>
  <div class="nlbg-tw"><table class="nlbg-tbl"><thead><tr><th>..</th></tr></thead><tbody><tr><td data-l="same as th">..</td></tr></tbody></table></div>
  <p class="nlbg-back"><a href="#nlbg-map">חזרה למפת המדריך</a></p>
</section>
```
- Phase names for the kicker: לפני שקונים (1 to 4) · לפני החתימה (5 to 8) · החתימה (9 to 12) · אחרי החתימה עד המפתח (13 to 16) · מסלולים נוספים (17, 18).
- Tools are placed by the integrator with `[nadlan_tool id="..." h="3"]`; mark where yours goes with an HTML comment `<!-- TOOL bpay -->`.
- Every official figure: a `nlbg-note--fig` or a `nlbg-src` line right after the sentence. The reading date is the ledger's date.
- For additions to an existing chapter, deliver `<div class="nlbg-add" data-ch="c5">` blocks with the head parts (`nlbg-ans`, `nlbg-who`, `nlbg-todo`) and your H3 subsections; the integrator places them.
- The glossary: `<dl class="nlbg-gloss" id="nlbg-gloss"><dt>term</dt><dd>definition <a href="#nlbg-c5">שלב 5</a></dd>...</dl>`.
- FAQ additions: `<h3>question</h3><p>answer</p>` pairs (the integrator merges them into the existing FAQ and its FAQPage schema).

## Copyright and honesty
- Write every sentence yourself. Read competitors only to understand a fact; never copy a sentence or a list order. No run of 6 or more words may match a competitor page (the integrator checks this by script and sends back any fragment that fails).
- No invented numbers, cases, quotes, people or statistics.

## Output
- Fragments: `docs/research/2026-11-08-buying-guide-re/chapters/c<N>.html` (one file per chapter; additions in the same file as `nlbg-add` blocks), `faq-add.html`, `glossary.html`.
- A report per writer: `chapters/W<k>-report.md`: words written per chapter (Hebrew words), the unit ids covered (amit-vered-map #, other-competitors-map refs), the facts used with their ledger ids, missing facts, and anything you chose to leave out and why.
- Self-check before you finish: zero long dashes, zero forbidden words, every `<td>` has `data-l`, every number has a source, HTML well formed (python html.parser parses it without errors).
