# /my-rentals/: how Israelis search for it (manual pass, 20.11.2026, HAD-795)

Who did what: every search below was typed by this session itself in the owner's Chrome ("gmktec", one signed-in desktop browser, google.co.il, hl=iw, gl=il), 20.11.2026 evening. Eleven phrases typed into the search box (no page load), five results pages loaded, no robot check. No agent, no API. Screenshots: `manual-2026-11-20/` (the suggestion lists were captured enlarged; the results pages at half zoom because the window is 361 px tall; number 12 is small, its titles are in the table). Not done yet: reading the top competitor pages in full (needed before the text is rewritten), English and other languages, search volumes.

Search Console (gsc_api.py, 20.8 to 18.11.2026, query by page): /my-rentals/ had 6 impressions in 90 days and no click. No page of the site holds the software phrases below.

## What Google suggests (as typed)
| Typed | Suggestions | Shot |
|---|---|---|
| ניהול השכרות | none of its own (only "השכרות רכב...") | 01 |
| ניהול דירות להשכרה | ניהול דירות להשכרה עלות · חברת ניהול דירות להשכרה · ניהול דירה להשכרה · ניהול השכרת דירות · ניהול דירות | 02 |
| ניהול נכסים | דרושים · פרטיים · תל אביב · מסחריים · בחיפה · קורס · מלונאים · בבאר שבע | 03 |
| ניהול שכירות | חברת ניהול שכירות · דמי ניהול שכירות · ניהול שכירויות · ניהול שוכרים · ניהול השכרת דירה · ניהול דירה שכורה | 04 |
| תוכנה לניהול נכסים | מניבים · תוכנה לניהול השכרת נכסים · תוכנה לניהול נכסים חינם · נכסי נדלן · תוכנה לניהול נדלן | 05 |
| מעקב שכר דירה | none of its own | 06 |
| חוזה שכירות | סטנדרטי · בלתי מוגנת להורדה חינם · עיריית תל אביב · קצר 2 דפים להורדה · להורדה word · עם ערבים להורדה | 07 |
| ניהול נכסים להשכרה | ניהול נכסים דירות להשכרה · ניהול נכס להשכרה · ניהול נכסים השכרת דירה · ניהול נכסים פרטיים | 08 |
| אפליקציה לניהול | first row is this browser's own history (clock icon), not counted; the rest are other fields | 09 |
| השכרת דירה ל | לטווח קצר · לטווח ארוך · לחברה · ללא תיווך ... (not this page's intent) | 10 |

## What the results pages show
| Search | Who is on page one | What it means |
|---|---|---|
| ניהול דירות להשכרה (11) | only management companies (bhomeisr, ys-property-management, property365, flamingo, housemanager, danya, doron...); an AI answer on what the SERVICE includes | people looking to HIRE a company. A software page does not belong in the title here; it can answer "alone or a company" lower down |
| ניהול שכירות (14) | the same companies; AI answer "מה כולל ניהול שכירות מקצועי" (איתור וסינון שוכרים, גבייה וחשבונות, תחזוקה ותקלות) | same intent |
| תוכנה לניהול נכסים (12) | Medatech, hoteltechreport "10 התוכנות הטובות ביותר לניהול נכסים להשכרה", nadlan2u "תוכנה לניהול נכסים, שכירויות ונדל״ן מניב", pickspace, almogerp, ziv, Google Play "אפליקציה לניהול השכרת דירות", kloyz, meshek. Related: תוכנה לניהול נכסים חינם · אפליקציה לניהול השכרת דירות | THIS is the page's search. Words of the winners: תוכנה / מערכת / אפליקציה לניהול נכסים, השכרת דירות, חוזים, חיובים, גבייה |
| אפליקציה לניהול שכירות לבעלי דירות (13) | Google Play, hoteltechreport, pickspace, EZGO "מערכת לניהול השכרת דירות לטווח קצר וארוך", Propel "אפליקציה לניהול השכרת דירות מהטלפון", nadlan2u, App Store "ניהול דירות להשכרה", Kloyz. AI answer names Propel (חוזים, תשלומים, הצמדה למדד, קריאות שירות), Kloyz (בעלי דירות פרטיים: גבייה, קבלות, חוזים), Nadlan2U, EZGO | the direct rivals and the feature words Google repeats |
| תוכנה לניהול נכסים חינם (15) | Google Play, hoteltechreport, excelwiz "אקסל לניהול נדלן והשכרה (הורדה חינם)", nadlan2u, pickspace, reddit. AI answer: an Excel file and the Renta app ("ניהול דירות מושכרות, מעקב תשלומי שכר דירה ותזכורות, ניהול מסמכים") | the free angle is open: no strong Israeli free product on page one |

## On the live page today (counted in the public HTML, the rentals block, about 2,960 words)
תוכנה לניהול 0 · מערכת לניהול 0 · אפליקציה 1 · ניהול דירות להשכרה 0 · ניהול השכרת דירות 0 · ניהול שכירות 0 · ניהול שוכרים 0 · ניהול נכסים 0 · ניהול השכרות 1 · חינם 4 · הצמדה למדד 2 · מעקב תשלומים 1 · שכר דירה 8 · חברת ניהול 2.
The page never names itself with the words people type. That, with the missing links to it, is why it is not shown.

## Ownership (kw_guard.py with the Search Console file, url_word_audit.py)
- "דירות" belongs to /properties/ and "נדלן" to the home page: allowed only inside a longer phrase (the guard warns, does not block).
- "דירות להשכרה" (27,100 searches a month) has no owner yet and is a listings search: keep it OUT of this page's title and h1; "ניהול דירות להשכרה" may appear once in a lower heading.
- "חוזה שכירות" belongs to /real-estate-lawyer/residential-lease-agreement/: this page does not target it, it links there.
- "ניהול נכסים מחיר / מסחריים" belong to /commercial-real-estate/commercial-property-management-fees/: this page says "תוכנה לניהול נכסים להשכרה", never the bare "ניהול נכסים מחיר".
- No new address is made; the address /my-rentals/ stays.

The five results-page screenshots (11 to 15) show the signed-in browser frame, so they are kept out of the public repository: `D:\Media
ad-lanentals-search-2026-11-20\` (and beside this file on this machine, untracked).

## Proposal (nothing of it is live; the exact title wording is Ben's to approve)
- Title: תוכנה לניהול השכרת דירות, חינם לבעלי דירות | השכרות נדל״ן
- h1: תוכנה חינמית לניהול השכרת דירות
- One sentence under it: כל הדירות שאתם משכירים במקום אחד: שוכרים, שכר דירה, חוזים ותיקונים.
- Opening paragraph (below the stage): השכרות נדל״ן היא תוכנה לניהול נכסים להשכרה לבעלי דירות פרטיים: ניהול שוכרים, מעקב תשלומי שכר דירה, הצמדה למדד, חוזים, מסמכים וקריאות תיקון, לדירה אחת או לכמה דירות, בחינם.
- Headings, in the words the search showed: מה כוללת התוכנה לניהול השכרת דירות · ניהול שוכרים · מעקב תשלומי שכר דירה ותזכורות · הצמדה למדד · ניהול חוזים ומסמכים · תחזוקה ותיקונים · תוכנה לניהול נכסים חינם: מה כלול בלי תשלום · ניהול דירה להשכרה לבד, או חברת ניהול דירות להשכרה. The existing guide heading and text stay in full.
- Kept out: "חוזה שכירות" as a target (the page links to /real-estate-lawyer/residential-lease-agreement/), "דירות להשכרה" in the title and h1, the bare "ניהול נכסים מחיר".
- Board: https://claude.ai/artifact/UnXWjYcZPJnARhMLhafL1C#page-b6 (frames 2 and 3 show the h1 and the sentence in place).
