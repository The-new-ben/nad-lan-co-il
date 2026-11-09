# The NadLan mail system: what was proven, counted (HAD-687, 9.11.2026)

Ben, 9.11.2026: "תוכיח לי מדעית שזה התצורת מייל הכי מקצועית שיש בעולם ... תעשה השוואות גם עם מתחרים בארץ".

**Method.** Two research passes, sources read 9.11.2026:
- **`research.md`**, 26 requirements (E1 to E26) on design, reading, accessibility, delivery and the law. Its sources:
  - NN/g;
  - Litmus;
  - the Email Markup Consortium 2026 report (376,348 emails);
  - caniemail;
  - Google's bulk-sender rules;
  - Brevo;
  - the Israeli Communications Law, section 30A.
- **`../2026-11-09-nadlan-b2b-outreach/research.md`**, 22 requirements (L1 to L22) on reaching businesses. Its sources:
  - section 30A(ג) and the case law;
  - Gong, Belkins, Backlinko and Woodpecker (vendor data, marked as such);
  - caniemail on video.

Every row below was checked against the built system, and every claim is backed by one of these:
- the automated tests `tools/ownermail/test_mail_studio.php` and `test_owner_mail.php`;
- the release checks;
- a real message received in Gmail on 9.11.2026.

## Design and delivery (E)
| # | Requirement | Status | Evidence |
|---|---|---|---|
| E1 | A subject that says what is inside | ✓ field + guidance | studio field; content is the writer's |
| E2 | A preheader carries the key fact | ✓ | Gmail showed "Rainbow ו־DUO, עם כל הפרטים שיש באתר" as the preview line |
| E3 | One primary button | ✓ | one teal button; card links weaker by design |
| E4 | One column, 600 px, readable at 375 | ✓ | rendered at 390 and 640 |
| E5 | Body text at least 16 px | ✓ 17 px / 28 px | test |
| E7 | lang="he" dir="rtl" | ✓ | test asserts it on every look |
| E8 | role="presentation" on layout tables | ✓ | every table |
| E9 | One H1 and a real title | ✓ | test asserts exactly one H1 |
| E10 | Alt text, nothing image-only | ✓ | the wordmark is text; card and film images carry alt |
| E11 | Contrast at least 4.5:1 | ✓ | white on teal 5.6, mute on white 5.4, white on abyss 16 |
| E12 | Descriptive links | ½ | "לכל הפרטים" sits under each card's title; not self-describing alone |
| E13 | A Hebrew-safe font stack | ✓ | Assistant, then Segoe UI and Arial |
| E14 | Under 102 KB | ✓ | 8 to 16 KB (a live listings mail was 8,093 bytes) |
| E15 | Dark mode | ½ | the color-scheme meta and Apple dark CSS; Gmail dark untested |
| E16 | Success measured by clicks | ½ | the Brevo log shows clicks once the key works; the screen does not |
| E17 | A stable sender | ✓ | the settings name, Reply-To to Ben |
| E18 | SPF, DKIM and DMARC | ½ | **live Gmail headers: SPF pass, DMARC pass**; DKIM comes with Brevo once a valid key is saved |
| E19 | One-click unsubscribe plus a visible link | ✓ | List-Unsubscribe + List-Unsubscribe-Post seen in the received message; the confirm page; immediate |
| E20 | Spam-rate monitoring | ✗ | Google Postmaster Tools is not set up yet |
| E21 | Israeli advertisement rules | ✓ | "פרסומת:" forced first in every distribution subject, a tag in the body, the sender line, refusal |
| E22 | Service mail kept apart from promotion | ✓ | a personal mail never carries the ad label or a pitch list |
| E23 | A notice at sign-up and double opt-in | ½ | the price window has the full section 11 notice; it is single opt-in with an explicit box |
| E24 | One HTML source for templates | ✓ | one renderer, three looks plus the invitation |
| E25 | One-to-one plus segmented lists | ✓ | segments: clients, developers, brokers, professionals |
| E26 | A release gate with screenshots | ½ | Edge at 390 and 640, Gmail delivery and headers; no Outlook or Apple Mail screenshots |

## Reaching businesses (L)
| # | Requirement | Status | Evidence |
|---|---|---|---|
| L1 | Counsel opinion on 30A for B2B | ✗ open | Ben's decision; flagged |
| L2 | A recorded legal basis per address | ✓ | the contacts table: consent, wording, time, source, kind |
| L3 | The first invitation carries no pitch and no film | ✓ enforced | an invitation strips listings, film and button (test) |
| L4 | One invitation only | ✓ enforced | invited_at is set at send; a second send is skipped (code path tested) |
| L5 | Sender and refusal in the invitation | ✓ | a footer with the sender line and "להסרה" |
| L6 | Refusal honoured at once | ✓ | "לא" and the refusal link set unsub_at immediately |
| L7 | Proof for existing customers | ½ | price-window consents imported with their wording; brokers have no ad consent yet |
| L8 | A named person, an authenticated domain | ½ | signature and Reply-To to Ben; DKIM after the Brevo key |
| L9 | 50 to 100 words in the first touch | ✓ | the recommended invitation is about 55 words |
| L10 | A short subject | ✓ | "שאלה קצרה מנדל״ן" |
| L11 | Real personalisation | ✓ | {שם} and {חברה} per recipient |
| L12 | One value-framed ask | ✓ | one question, two buttons |
| L13 | Follow-ups only with consent | ✓ | none without "כן" |
| L14 | The film as a poster linking to a page | ✓ | the developer-film-v3 poster, plus a button to /marketing/#film |
| L15 | The film only after consent | ✓ enforced | an invitation can't carry it |
| L18 | Replies within a business day | ½ | Ben gets a mail on every "כן"; the reply time is his |
| L19 | Measure replies and meetings, not opens | ½ | yes and no are counted in the list; meetings are Ben's |
| L20 | 50-send pilots with a control | ✗ | the daily cap is there; the pilot discipline is a choice |

## Score
| | Met in full | Partly | Open |
|---|---|---|---|
| Design and delivery (24 rows) | 17 | 6 | 1 |
| Reaching businesses (18 rows) | 12 | 4 | 2 |

**Compared with others:**
- **Israeli competitors** (Madlan, Yad2, Homeless, OnMap, the developers): none of their mails could be seen. Their sites answered 403, and nothing is public. A fair counted comparison needs a test inbox signed up to their alerts, and that is Ben's decision.
- **World examples** (Zillow, Redfin, Airbnb, Stripe, Apple): the public archives show only images, so their rows are "not seen", not "missing".
- **What can be said honestly:**
  - The EMC 2026 report found a serious or critical accessibility problem in 99.88% of emails. Its top failures are missing lang/dir, tables without a role, low contrast and missing alt.
  - The NadLan mails pass all four by test.
  - Not one of the 48 requirements is claimed without its test or its live evidence.
