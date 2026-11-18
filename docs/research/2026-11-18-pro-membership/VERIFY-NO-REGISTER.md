# Verifying a professional who is in no government register (Israel)

18.11.2026. For interior designers, home stylists, kitchen planners, handymen, renovation project managers, mortgage advisers and anyone else with no open licence register. The forum today shows a verified mark only from the three open registers (brokers 25,375, appraisers 3,198, contractors 24,742 rows; see `../2026-11-12-pro-forum/israel-law-business.md`).

Rule for every method below: the mark says exactly **what** was checked and **when** ("זהות ומספר עוסק נבדקו ב-11.2026"), never a vague "מאומת". Thumbtack's model (licence shown only if searchable in a public database, removed on expiry) and Checkatrade's (each check named) are the reference. https://help.thumbtack.com/article/manage-my-license ; https://www.checkatrade.com/twelve-checks

"Our cost" = staff minutes or money per check. Minutes are our planning assumptions, not measured; money is from a published price or marked "not published".

---

## The methods

| # | Method | What it proves | What it does NOT prove | Our cost per check | Abuse it leaves open | Who uses it (source) |
|---|---|---|---|---|---|---|
| 1 | Mail code (we have it) | Control of a mailbox | Name, trade, skill | Zero staff time; mail cost per message on Brevo not read today (pricing page did not render) | Throwaway mailboxes; one person, many accounts | Our forum (live since 1.72.676) |
| 2 | Phone code (SMS or voice) | Control of an Israeli phone number | Name, trade | Zero staff time; SMS about 0.04 ₪ each (1,000 for 40 ₪ at sms4free, price read 12.11.2026, `../2026-11-12-pro-forum/DECISION-PACK-HE.md`) | Virtual or borrowed numbers | easy claims by SMS or voice code https://support.easy.co.il/hc/he/articles/360015899911 ; B144 reviewers by phone code https://www.b144.co.il/MarketingReviews/ |
| 3 | Company number (ח"פ) lookup | The company exists, its name, status (active, violating, in liquidation), city | That the member is that company's owner or works there | Automatic: data.gov.il dataset `ica_companies` "מאגר חברות - רשם החברות", Ministry of Justice, CSV resource `f004176c-b85f-4542-8901-7b3176f9a054`, about 733,887 rows (estimate), fields include מספר חברה, שם חברה, סטטוס חברה, מפרה, שם עיר; updated 18.11.2026. https://data.gov.il/api/3/action/datastore_search?resource_id=f004176c-b85f-4542-8901-7b3176f9a054&limit=1 | Typing another firm's number; the dataset has no phone or person to match | Nextdoor asks for business documents with an exact name match https://help.nextdoor.com/s/article/Verify-your-business ; Checkatrade checks company history https://www.checkatrade.com/twelve-checks |
| 4 | עוסק מורשה or פטור number | The number is registered for VAT, with a name and address | Ownership by the member, skill | gov.il has a free online service "בקשה לקבלת פרטי עוסק מורשה במס ערך מוסף באופן מקוון" that returns name, address and VAT status by number (**unverified**: page returned 403 to the tool; seen in a search summary). https://www.gov.il/he/service/vat-apply-online . If it requires a form or a robot check, this is a manual check of about 2 minutes | Same as 3; most sole traders have no company number, so this is the main business proof for designers | המקצוענים asks for a registered business number https://www.pro.co.il/advertise |
| 5 | Invoice match | A real tax invoice from the member to a client carries the same business number and name | Quality of the work | Manual, about 3 minutes; the member blacks out the client's details before upload | Forged PDF; one invoice is weak, so ask for 2 from different months | Midrag asks for invoices of recent customers https://biz.midrag.co.il/Content/Article/14450 ; המקצוענים asks for 5+ consecutive invoices https://www.pro.co.il/advertise |
| 6 | Association membership | The association admitted the person under its criteria | Current quality | Manual, about 2 minutes: name in the public member directory of אגודת מעצבי הפנים https://www.i-arc.co.il/חברי-האגודה/ plus the member's card number | Same name as a real member; mitigate by asking for the numbered member card | אגודת מעצבי הפנים criteria: B.Design 4 years, B.Arch, registered הנדסאי, or committee route with 5+ years, portfolio and interview https://www.i-arc.co.il/תנאי-קבלה/ ; IIPDO criteria behind login (unverified) https://www.iipdo.org/about ; architects' union associate membership for interior designers 150 ₪ https://u-architects.activetrail.biz/registerisra-arch2024 |
| 7 | Diploma or הנדסאי registration certificate | Formal training in the field | Current work, honesty of the copy | Manual, about 3 minutes; certificate shown in a short video call, not stored | Forged or borrowed images if uploaded; video lowers this | Registers exist by law: הנדסאים under חוק ההנדסאים והטכנאים המוסמכים, התשע"ג-2012 (unit page https://www.gov.il/he/departments/Units/practical-engineers-unit ); engineers and architects under חוק המהנדסים והאדריכלים, התשי"ח-1958 (unit page https://www.gov.il/he/departments/units/engineers-and-architects-unit ). **Whether either register has a public name search today is unverified**: gov.il returned 403 and data.labor.gov.il/EngineersAndArchitects.aspx returned an error page on 18.11.2026; data.gov.il has no dataset for either (searches "מהנדסים" and "הנדסאים" returned 0) |
| 8 | Live identity check by video | The face matches an ID card, live, today | Trade or skill | Manual, about 5 minutes of staff time plus LiveKit minutes (about 10 participant minutes, under 1 cent at 0.0005 USD per minute, see COST-PER-MEMBER.md); we see the ID and do not keep a copy | Staff time; a determined fraud with a borrowed ID | Reddit r/AskDocs: photo of credentials with the handwritten username, "We do not accept digital forms of identification" https://reddifier.com/free-subreddit-analysis-tool/r/AskDocs ; Bark: photo ID plus face recognition (paid plan only) https://help.bark.com/hc/en-gb/articles/17035153606044-Are-professionals-verified-on-Bark |
| 9 | LinkedIn verified identity | LinkedIn checked a passport chip (Persona; Israel is listed) | Trade, unless the workplace is verified too | Zero money; about 1 minute: the member puts a one-time code from us in his LinkedIn "About" for a day | Linking someone else's profile (the code step closes it) | https://www.linkedin.com/help/linkedin/answer/a1631613 |
| 10 | Own website or domain mail | Control of the business's site or mail domain | Skill | Automatic: code in a page or a TXT record, or mail code to an address on the business domain | Domains are cheap; weak alone | Doximity: "use your professional medical domain email to expedite" https://support.doximity.com/hc/en-us/articles/55386210147475-How-to-Register-on-Doximity |
| 11 | Portfolio with proof | Real finished work, photographed | That the member did it alone | Manual, about 3 minutes; reverse image search on 3 photos | Stolen photos from other designers (reverse search closes most); tagging closes the rest | Houzz minimum profile of 4 photos https://pro.houzz.com.au/pro-help/r/minimum-standards-for-houzz-pro |
| 12 | Client confirmations from closed requests | A client identified by code says the job was done | Size or price of the job | Automatic: our requests board closes with "מצאתי" and a client who entered by code can confirm and give a פרגון | Friends posing as clients (one confirmation per request, code-verified client, and a pattern check) | Houzz "Verified Hires": projects paid through the platform, shown from 3 https://pro.houzz.com.au/pro-help/r/verified-hires ; MyBuilder reviews only after a confirmed hire or invoice https://support.mybuilder.com/s/article/How-do-you-make-sure-reviews-are-from-genuine-customers |
| 13 | Calling past clients | Several clients say they were served well | Licence | Manual and slow: Midrag calls 5 to 15 random customers per pro and charges about 390 ₪ plus VAT once https://biz.midrag.co.il/Content/Article/14483 | Pro chooses which invoices to send | Midrag; המקצוענים call centre https://www.pro.co.il/our-liability |
| 14 | Peer vouching ("עבדנו יחד") | A verified member worked with him | Skill in general | Zero (we have skill confirmations live) | Rings of friends; count only vouches from members verified at level 2+ | LinkedIn recommendations; Avvo peer endorsements https://www.avvo.com/support/articles/913946-attorneys-what-is-the-avvo-rating |
| 15 | Professional-liability insurance certificate | A policy exists today | Skill | Manual, about 2 minutes; expiry date stored, mark drops on expiry | Cancelled policy after upload; recheck at expiry | IIPDO offers such insurance to members https://www.iipdo.org/about ; Checkatrade and Angi record insurance https://intercom.help/angi/en/articles/11366580-how-to-update-your-licensing-and-insurance-details |
| 16 | Skills test | Knows basic trade facts | Taste, honesty | Building and keeping a fair test in Hebrew: large; not recommended for designers | Answers shared online | MyBuilder online skills test for unregulated trades https://www.mybuilder.com/quality-check |
| 17 | Criminal background check | No record (in the US) | Skill | Not available to a private site in Israel in the same way; not proposed | n/a | Thumbtack, Angi (US) https://help.thumbtack.com/article/background-checks |

---

## Recommendation for interior designers (and every no-register trade)

Three levels, each shown with its date and what was checked. A level is never sold; paying never changes a level.

| Level | Name on the card | What it takes | Time for us |
|---|---|---|---|
| 1 | חבר בפורום | Mail code (method 1) | 0 |
| 2 | זהות ועסק נבדקו | Phone code (2) **and** a business number that matches the name, ח"פ from `ica_companies` (3) or עוסק number (4), **and** one invoice with the client blacked out that carries that number (5), since neither lookup links the number to the person | 3 to 5 minutes |
| 3 | מקצוע נבדק | Level 2 **and any one** of: association membership (6), diploma or הנדסאי certificate shown on video (7), or 3 client confirmations from closed requests on our board (12) | 2 to 5 minutes, or zero for route 12 |

Extra marks that sit beside the level (each earned, each dated): insurance valid to date (15), works shown with photos (11), "עונה תוך יום" (LinkedIn rule: shown only when earned, https://www.linkedin.com/help/linkedin/answer/a550345 ).

Why this mix: the business number plus phone gives the "real business" proof every Israeli directory relies on, at almost no cost; the third step gives three honest routes so a self-taught designer with happy clients is not shut out (JustAnswer accepts "several years of experience" for the same reason, https://www.justanswer.co.uk/info/expert-quality-process ); and route 12 grows from our own requests board, so the best proof is one that only our site can give.

Recheck: yearly for levels 2 and 3 (Thumbtack rechecks yearly); insurance on its expiry date; a level is removed at once after a confirmed fraud report.

## Israeli specifics found

- Company register on data.gov.il: `ica_companies`, free API, daily update (link above). Related: `ica-deletion` (companies marked for deletion), `pr2018` (official receiver). https://data.gov.il/api/3/action/package_search?q=חברות&rows=10
- VAT dealer lookup on gov.il: exists by name in a search summary; page blocked to the tool (unverified).
- Engineers and architects register (1958 law) and הנדסאים register (2012 law): units exist; public search unverified today.
- Interior design has no statutory licensing in Israel (Hebrew Wikipedia, read by the sub-agent, not reopened: unverified).
- אגודת מעצבי הפנים: public member directory and stated entry criteria (links above). IIPDO: criteria and fees behind login.
- LinkedIn identity check works for Israeli NFC passports (link above).

## What could not be checked

gov.il pages (403); data.labor.gov.il register search (error page); IIPDO membership rules (login); Brevo mail price (page did not render); whether reading the VAT service by script is allowed (needs a lawyer and the page itself).
