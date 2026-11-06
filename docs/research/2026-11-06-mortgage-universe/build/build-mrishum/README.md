# New tool for /mortgage-calculator/: "רישום משכנתה ואגרות" (id `mrishum`)

HAD-675, mortgage universe. Built 6.11.2026, **local only**: nothing deployed, nothing committed, no live write, no existing file
edited (`inc/instruments.php` untouched). Demand (manual SERP 6.11.2026): רישום משכנתא 880/mo, רישום משכנתא מקוון 590, בקשה לרישום
משכנתא 390, רישום משכנתא בטאבו 260, אגרת רישום משכנתא 210 + 210 + 90, טופס רישום משכנתא, תיקון משכנתה, ביטול משכנתא (בטאבו מקוון,
לאחר פטירה, התחייבות רמ"י), אגרת ביטול משכנתא.

## Files

| File | What |
|---|---|
| `plugins/nadlan-config/assets/instruments/tools/mrishum.js` | The tool, Hebrew only, RTL. Pure logic in `window.NLRS`; holds no amount, fee or deadline of its own (the test greps it). |
| `plugins/nadlan-config/assets/instruments/data/rishum.json` | Every amount (with its item number), condition, rule, document, contact fact and source (`src`: URL, title, publish / update / read dates); `"checked": "2026-11-06"`; `unverified` with the path filters that show each caveat. |
| `build-mrishum/registry.php.txt` | The exact PHP: the `nadlan_nli_tools()` entry and the `nadlan_nli_summary()` branch, plus the switcher chip and pane. `php -l` clean (PHP 8.3). |
| `build-mrishum/summary.render.html` | The server summary rendered against the real `rishum.json` with WordPress stubs (all 2026 fees in plain HTML). |
| `build-mrishum/test_mrishum.js` | Node test, 115 assertions. Last run: `test_mrishum.out.txt`. |
| `build-mrishum/preview.html` | Local mount exactly as the shortcode prints it, inside pane `#tool-rishum`, with the rendered summary inside the host. `?theme=1` adds the live theme stylesheets (read only). |
| `build-mrishum/verify.py` | Playwright (Chrome, headless): starts `http.server` on a free 127.0.0.1 port and stops it in `finally`. 292 checks. Last run: `verify.out.txt`, `verify.json`, `shots/`. |
| `build-mrishum/sources/` | What was read on 6.11.2026: the five Kol Zchut pages and the MoD page (HTML and extracted text), and the Wikisource raw text of the fees regulations, the land regulations and the Banking (Service to Customer) Law. |

Run from the repo root: `node docs/research/2026-11-06-mortgage-universe/build/build-mrishum/test_mrishum.js` and
`python docs/research/2026-11-06-mortgage-universe/build/build-mrishum/verify.py`.

## What the tool does

Three steps (tiles, phone first): (1) where the home is registered today: בטאבו / ברשות מקרקעי ישראל / בחברה משכנת / לא רשומה עדיין
(דירה מקבלן); (2) the action: רישום משכנתה / משכנתה נוספת או בדרגה שנייה / תיקון משכנתה (שינוי תנאים או הגדלה) / ביטול אחרי סילוק /
ביטול אחרי פטירה; (3) who files: עורך דין במקוון / ידנית בלשכה / הבנק, and on the ILA path בעל הזכויות / מייצג עם ייפוי כוח (both
online in "רמ"י שלי"; the options follow the path). Extras: the extract (online 18,
counter 88, none; for the pledge register: internet 12, counter 38), the pledge years, the amendment kind, the exemption.

The result: the headline "לשלם למדינה", what is registered where (with a verified / not fully verified badge), the 2026 fee ledger
(item number and source chip on every line, a total row; lines that are not part of the total say so), the exemption block
(conditions, how to claim, spouse and refund rules, and whether it lowers the fee on this path), the time and who pays, the steps in
order, "טופס רישום משכנתא: מה מגישים" (a checklist with checkboxes, copy and print, links to the official gov.il pages and the forms
page; no official form is hosted or recreated), the contact card, "מה לא אימתנו במסלול הזה", a copy-summary button, the source line
with the 2026 notice and its dates, and all sources with dates. The case lives in `#mrishum=reg.act.who.nesach.ex.years.amend`
(choices only, no personal data), written into the copied text; a shared link opens the pane and the case.

## Fee totals per path (2026, by hand; all in the node test; extract excluded unless said)

| Registered | Action | Who | לשלם למדינה |
|---|---|---|---|
| טאבו | רישום / משכנתה נוספת | עו"ד במקוון or ידנית | **188 ₪** (item 2(א)); with the default online extract **206 ₪**; counter extract 276 ₪ |
| טאבו | תיקון: שינוי תנאים / הגדלה | either | **188 ₪** (2(ב) / 2(א)) |
| טאבו | ביטול אחרי סילוק | הבנק | **0 ₪** (2(ג)(1): exempt when paid straight to the lender; the bank files within 30 days and pays, s.9A) |
| טאבו | ביטול אחרי סילוק | ידנית בלשכה (the bank refuses payment, reg. 72) | **188 ₪** (2(ג)(2)) |
| טאבו | ביטול אחרי פטירה | הבנק | **0 ₪**; inheritance registration 188 ₪ (3(א)) shown apart, not in the total |
| רמ"י | רישום / נוספת | בעל הזכויות or מייצג | headline "האגרה של רמ"י: לא מופיעה בדף השירות" (no number, no total row); a tabu warning note, if any, 188 ₪ shown apart (the ILA page does not mention one); later tabu registration 188 ₪ apart |
| רמ"י | תיקון | either | no number: "בודקים מול רמ"י", with *5575 (amendment is not on the service page) |
| רמ"י | ביטול / אחרי פטירה | הבנק | headline "הבנק מבטל את השעבוד"; discharge per procedure 90.02B, steps not on the page; warning-note deletion 127 ₪ apart |
| חברה משכנת | רישום / נוספת | either | **188 ₪** warning note (13(א)(1), an inference: no separate line); the company fee "לא ידוע", not in the total; later tabu registration 188 ₪ shown apart (unchanged, still unread) |
| חברה משכנת | תיקון | either | no number: "בודקים מול החברה המשכנת" |
| חברה משכנת | ביטול / אחרי פטירה | הבנק | headline "הבנק מבטל את השעבוד", 0 ₪ verified; warning-note deletion 127 ₪ (13(ב)) shown apart (payer not stated in s.9A) |
| לא רשומה (משכון) | רישום / נוספת | עו"ד במקוון | **38 ₪ × years up to 5: 190 ₪** for 5 years or more (3 years 114 ₪) |
| לא רשומה (משכון) | רישום / נוספת | ידנית (דלפק) | **45 ₪ × years up to 5: 225 ₪** for 5 years or more (3 years 135 ₪, 1 year 45 ₪); later tabu registration 188 ₪ apart |
| לא רשומה (משכון) | תיקון | online / counter | **38 ₪ / 45 ₪** (change of debtor, creditor, asset or owner); extension 38 / 45 a year shown apart; increase "לא ברשימה" |
| לא רשומה (משכון) | ביטול / אחרי פטירה | הבנק | **0 ₪** (pledge cancellation exempt) |

Exemption picked on a tabu registration or additional mortgage: 188 becomes **0 ₪** with the reason (with the online extract the
total is 18 ₪). Not applied (said on the page): to an amendment or increase (the regulation says "בעד רישום משכנתה"), to the ILA
commitment, to the company warning note, to the Registrar of Pledges.

## The exemption conditions (read 6.11.2026)

* **Regulation text**, תקנות המקרקעין (אגרות), התשל"ה-1974, consolidated text on Wikisource (version 18.2.2026),
  https://he.wikisource.org/wiki/תקנות_המקרקעין_(אגרות): reg. 12: a disabled person, an injured person and a family member of a
  soldier who fell are exempt from the fee for registering a mortgage and a lease, and so is the spouse; two singles, one entitled,
  who registered jointly and married within 12 months get back the fee the other paid. Reg. 1 definitions: "נכה" = entitled to
  compensation under the Invalids Law or the Nazi War Invalids Law; Nazi-persecution, work-injury, road-accident, paralysis or
  amputee disability of at least 50%; any other disability of 100%. "נפגע" = under the Border Injured or Terror Victims
  Compensation Law, including survivors entitled to an allowance. "בן משפחה של חייל שנספה" includes parents and widows not entitled
  for age or income, and an orphan up to age 30. Reg. 13: an oleh is exempt when the loan secured pays the price of real estate for
  whose purchase he got an exemption from "תוספת מס" under reg. 12 of the Land Betterment Tax (Tax Addition) Regulations 1974; the
  spouse too; the same 12-month refund. Reg. 11א: a fee deposited when a commitment to register a mortgage is made counts as paid.
* **Disabled**: Kol Zchut, updated 2.3.2025,
  https://www.kolzchut.org.il/he/פטור_מאגרת_רישום_משכנתא_ואגרת_רישום_שכירות_לאנשים_עם_נכות (the same groups; apply in person or in
  writing to the land registry office, show the disability confirmation and give block and parcel). IDF and security forces
  disabled: Kol Zchut, updated 2.3.2025, https://www.kolzchut.org.il/he/פטור_מאגרת_רישום_משכנתא_לנכי_צה%22ל_וכוחות_הביטחון (at least
  20%, or 10% before 1996; a special approval from the district welfare department, not the regular disability certificate).
* **Bereaved families, IDF and security forces**: Kol Zchut, updated 16.3.2026,
  https://www.kolzchut.org.il/he/פטור_מאגרת_רישום_משכנתא_ואגרת_רישום_שכירות_לבני_משפחה_של_חללי_צה%22ל_וכוחות_הביטחון (spouses at
  the time of death including common-law, bereaved parents, orphans under 30, orphans of two fallen parents at any age from 18, and
  the spouses of all these); MoD Families, Commemoration and Heritage Division, no update date on the page,
  https://mishpahot-hantzaha.mod.gov.il/discounts-and-exemptions/exemption-from-mortgage-registration-fee (approval requested in the
  personal area, given within 7 work days; the land registry decides; not for opening the bank file).
* **Bereaved families of terror victims**: Kol Zchut, updated 2.3.2025,
  https://www.kolzchut.org.il/he/פטור_מאגרות_על_רישום_משכנתא_ועל_רישום_שכירות_לבני_משפחה_של_חללי_פעולת_איבה (monthly-compensation
  recipients: widows and widowers, bereaved parents, orphans up to 21, orphans of two parents at any age from 18; spouses; NII branch
  approval).
* **Terror victims**: Kol Zchut, updated 10.11.2025,
  https://www.kolzchut.org.il/he/פטור_מתשלום_אגרת_רישום_משכנתא_לנפגע_פעולת_איבה (at least 20% permanent, or 10% with a monthly
  benefit before 1996; spouses; NII approval, block and parcel).
* "הגשת בקשה לרישום משכנתא" on Kol Zchut: not found (HTTP 404, no hit in the site search).

## The Israel Land Authority path (update, 6.11.2026 evening)

Source: https://www.gov.il/he/service/guide-mortgage ("התחייבות לרישום משכנתא | רשות מקרקעי ישראל"), read by hand in the owner's
browser on 6.11.2026 about 18:20 (scripts get 403; not bypassed). Facts in `rishum.json` → `ila` and `docs.ila_*`: online issue of a
"כתב התחייבות לרישום משכנתא" for ILA-managed homes not registered in tabu or in a housing or contractor company, in "רמ"י שלי" after
national identification; filed by the rights holder or a representative with a valid power of attorney, holding the lender's
referral letter; every rights holder signs in their own personal area; ILA undertakes not to register the rights in tabu unless the
mortgage is registered at the same time, and not to approve a transfer without the lender's consent; the e-signed digital file is
the original and a printed copy is not an official extract; conditions: procedure 90.02B "התחייבות לרישום משכנתא וסילוקה"; call
centre *5575 or 03-9533333, Sunday to Thursday 8:00 to 17:00; the page states no fee ("האגרה של רמ"י לא מופיעה בדף השירות"). The
official form "טופס בקשה למתן כתב התחייבות לרישום משכנתא והוראה בלתי חוזרת"
(https://www.gov.il/BlobFolder/policy/9002b-procedure/he/forms_wform351.pdf) is linked only. Changes: the ILA steps, documents
(referral letter; the power of attorney only when a representative files; all rights holders sign; the form link), contact card,
links and the server summary; step 3 on the ILA path is בעל הזכויות / מייצג עם ייפוי כוח; the warning note moved out of the ILA total
(the ILA page does not mention one); no "לא נקרא" or "לא ידוע" remains on the ILA path; the unread official forms show "קישור בלבד".
The old ILA caveat is gone; two narrower ones replace it: amendment and discharge are not on the page (procedure 90.02B not read),
and the page does not mention a tabu warning note. The housing-company path is unchanged.

## Other sources

* gov.il "בקשה לרישום משכנתה" and "fees-2026" (published 23.12.2025, updated 24.12.2025): read by hand by the owner on 6.11.2026; to
  scripts gov.il answers HTTP 403 (tried once on 6.11.2026, not bypassed), as does the forms page (linked only).
* Fees: הודעת המקרקעין (אגרות), התשפ"ו-2026, קובץ התקנות 12193; הודעת המשכון, קובץ התקנות 12123 (gov/gov.md section 1).
* Documents: Land Regulations 2011 regs 9 (request, deed, fee receipt, capacity, third-party consent), 10 (corporate party), 12
  and 14 (signing at the office or before a lawyer), 16 (ID), 21 and 22 (warning note), 71 and 72 (cancellation, deposit).
* Law: Banking (Service to Customer) Law s.9A (30 days from full payoff, the bank pays, one deadline for every banking corporation),
  s.7ח (second-degree consent), s.9ח2 (deferral up to 12 months after death).

## Still unverified (kept off the numbers or labelled on the page)

1. The housing-company process and fee; the ILA fee (not stated on the ILA service page) and the ILA amendment and discharge steps
   (procedure 90.02B, not read).
2. The 188 ₪ for a warning note of a commitment to register a mortgage is the general warning-note line (an inference).
3. Who pays for deleting the bank's warning note (s.9A(c) names mortgages and pledges only).
4. Whether reg. 12 and 13 cover an increase or an amendment (not applied).
5. Whether the reg. 2א online discount is in force in 2026 (full amounts shown).
6. How s.9A ("בעצמו ולא באמצעות ערב") applies when a life insurer repaid.
7. Whether the olim "תוספת מס" exemption is still granted; how to claim it today.
8. The Registrar of Pledges document list; a contractor's commitment and warning note for an unregistered flat.
9. Processing time at the registry office; equal-degree mortgages.
10. The longer deadline for mortgage banks that Google's AI answer claims was not found in the law and is not used anywhere.

## Results (6.11.2026)

* Node: **115 of 115** passed (after the ILA update; 101 before it) (every path total by hand, the five exemptions to 0, cancellation free when paid to the lender, the
  pledge 5-year totals 225 / 190, the hash, bad values, the ILA facts and documents, the words of all 396 combinations: no long dash, no banned word, no longer
  deadline, every shekel figure from the data file or the path total, the logic holds no amount).
* Browser: **292 of 292** (after the ILA update; 256 before it) at 390x844 (is_mobile) and 1280x900 plus a phone pass under the live theme: all 33 paths pressed at each
  width with the headline equal to `NLRS`, the extract, the five exemptions, the amendment kind, the pledge years (3, 5, 0, 25), the
  checklist ticks, both copy buttons read back from the clipboard, print, a shared link, and the ILA block (headline, facts, call
  centre, checklist with and without a representative, links, no "לא נקרא" or "לא ידוע"). No console error, no horizontal scroll,
  every visible control at least 44 px, every input labelled, every group named.
* Screenshots looked at (eyes): `page-default-390.png`, `page-default-1280.png`, `mrishum-ila-register-lawyer-390.png`,
  `mrishum-tabu-death-bank-390.png`, `mrishum-exempt-bereaved_idf-390.png`, `mrishum-none-register-search-390.png`,
  `mrishum-theme-register-390.png`. Fixed after looking: source chips and item references were in Plex Mono, which has no Hebrew (now
  Plex Sans Hebrew); the fifth action tile sat alone (now spans the row); the copy-summary button was at the very bottom (now under
  the steps); "שנים" wrapped inside the years box; a caveat showed "404" to readers. Fixed after the first browser run: an explicit
  extract choice carried into the pledge register, where the options mean something else (now reset when the option set changes).
  ILA update, after looking at `mrishum-ila-*-390.png` and measuring glyph positions in the DOM: phone numbers inside running text
  (*5575) now sit in `<bdi dir="ltr">` so the star stays on its side, and "03-9533333" no longer breaks at the hyphen.

## Release steps (not done)

1. Paste `registry.php.txt` parts (1) and (2) into `inc/instruments.php`; ship `tools/mrishum.js` and `data/rishum.json`.
2. Add the chip and pane to the /mortgage-calculator/ switcher (`tool-rishum`; markup in the snippet header). Where the chip goes
   and whether the tool also gets its own page are the owner's call (a new URL needs the URL word audit; "רישום" and "משכנתא" have
   owners to check).
3. After release: source audit of the raw HTML, content_first_check, the press-through in the owner's Chrome, and the summary seen
   in view-source.

## Design

Official-form paper: white surface (the instruments grid pattern is switched off), steel-blue ink (sea-deep #1F4B5C for pressed
tiles, step numbers and headings; sea #2F6F86 for links and chips), survey red #C42550 only for what is unverified or an error, open
green #4F9A5C only for exemptions and free lines. IBM Plex Sans Hebrew for every word, IBM Plex Mono for amounts. Square 2 px
corners, hairline rules, a 2 px ink rule above the result and the total, numbered step boxes like form fields. Why it is not the
default look: the subject is a land-registry filing, so the page reads as a ruled official form with item numbers and source stamps;
no cream, no gold, no gradient, no soft cards, no emoji. CSS id-scoped (`#nlrs`) with `!important` where the theme restyles headings,
buttons, inputs, lists and tables.
