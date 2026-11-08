# PriceAlert

A price-alert window for every Hebrew project page and listing. It carries an attention mark, the line "המחירים באזור זה במגמת שינוי" and a down arrow that blinks three times. One tap says what the visitor cares about, then the phone and the email (both required) sign them up for price updates. It replaces PriceNudge (105.x).

**Version 106 (8.11.2026, Ben, Linear HAD-684).** Ben: "I don't see it pop up at all. Make it very smart: an attention mark, prices in this area are changing, a blinking down arrow, without writing that prices are falling; sign up for price updates; phone and email required. On all the projects, not Meital Katzir, not the professionals."

## Why nobody saw PriceNudge
- **Triggers:** it waited 25 s AND 35% of the page (or 2.5 screens).
- **Holdout:** 20% of browsers were held out for good, because the bucket never expired.
- **Quiet:** any close started 7 days of quiet across the whole site, and the automatic 14 s fade counted as a close.
- **Session:** it showed once per session.
- **106 resets all of it** with new storage keys, so earlier closes do not block it.

## Why it looks like this (the anti-default line)
- **The subject is a market price board.** So the window opens with a dark board strip: `nlb-abyss` #10262f with `nl-champagne` #cfe3ea for the kicker.
  - It holds one signal red, `tick-down` #ff5a4f (5.1:1 on the board), for the down-tick and the attention triangle.
  - The sheet below is `sa-surf`. The action is `sa-sea` (hover `sa-seah`). Errors use `j-bad`; the success check uses `j-ok`. WhatsApp keeps `wa-green`.
- **Type: Assistant only, the site's Hebrew UI face.** The line is in 800, so it reads as a market alert, not an editorial serif. No new font is loaded.
- **What it avoids:**
  - no cream, gold, terracotta or brass;
  - no gradient and no emoji;
  - no Inter;
  - no "editorial" serif-on-paper look;
  - it is not near-black with a single acid pop: the red only means a price going down, as on any trading screen.

## Words (Ben's line, honest by data)
- **Kicker:** a live dot, "נדל״ן · nad-lan.co.il", and a chip with the city from the page.
  - It never shows a project or listing name (Ben 1.11, the Brokers Law exemption).
- **Attention:** a red triangle with "!", plus "שימו לב".
- **The line:**
  - "המחירים באזור זה במגמת שינוי", with the blinking down-tick beside it.
  - **Honesty rule:** the arrow stands beside the line only where the CBS dwelling price index is down over 12 months, for the page's district (or the national index when the city is not mapped).
  - **The data** (`data/prices-hub.json`, 07.2026): national -1.8%, Tel Aviv -1.9%, Center -2.7%, Jerusalem -0.2%, Haifa -1.4%, North -0.8%, South -1.5%.
  - **Elsewhere,** the line reads "המחירים באזור זה משתנים", and the arrow moves down to point at the question:
    - a rent listing reads "מחירי השכירות באזור זה משתנים";
    - a project abroad has no Israeli series;
    - the same applies to any district whose index turns up.
  - The window never shows a figure and never says "יורדים".
- **Sub line (honest loss framing):** "בשוק שזז, מחיר של לפני כמה חודשים כבר לא המחיר. הירשמו לעדכוני מחירים ב{עיר}, ותדעו על כל שינוי לפני שאתם מחליטים."
- **Step 1:** "על מה לעדכן אתכם?" with three tap chips: "קנייה באזור", "יש לי נכס באזור", "השקעה". The decline, "לא עכשיו", sits on the same row as the independence line.
- **Step 2:**
  - **Phone:** "טלפון נייד", with the hint "לעדכון מהיר בוואטסאפ כשיש שינוי. המספר לא עובר לאף אחד." Below it, the "אימייל" field.
  - **Consent:** one unticked box: "אני רוצה לקבל מנדל״ן עדכוני מחירים ופרסומים בנושא נדל״ן, במייל, בטלפון ובוואטסאפ. אפשר להסיר בכל רגע."
  - **Button:** "כן, עדכנו אותי".
- **Notice at the form, all five section 11 parts:**
  - the details are voluntary, and without them no updates can be sent;
  - the purpose;
  - who holds the details: נדל״ן (nad-lan.co.il), info@nad-lan.co.il;
  - who receives them: no developer, broker or anyone else without separate consent;
  - the rights to see, correct and delete, plus a link to the privacy policy.
- **Step 3:** "נרשמתם לעדכוני המחירים", then "נעדכן אתכם כשהמחירים ב{עיר} זזים. רוצים תשובה כבר עכשיו?", a "דברו איתנו בוואטסאפ" button and "סגירה". "ייעוץ חינם" stays on the floating bar only.
- **Independence line:** "אתר מידע עצמאי, לא מטעם יזם או מתווך."

## When it appears: the behaviour model (106.2, 1.72.611)
Ben, 8.11.2026: "Too fast, too aggressive. Wait at least 10-15 s, let them search and look, then pop it. Smart, by behaviour. Prove the method."

A clock alone is not a reason. A founder showed a fixed 20 s popup to all 80,000 visitors and got 0.1%; the same box inside the page got 0.5% (IndieHackers, 2022). So the window waits for four things. All thresholds are settings.

1. **A floor: 15 s of the page being visible.** It never opens earlier, whatever happens.
2. **Active time: 25 s on the first project or listing page of a visit, 15 s from the second page on.**
   - A second counts only while the tab is visible AND the reader scrolled, touched, moved or typed in the last 15 s. A tab left open does not count.
   - Evidence:
     - Klaviyo and Shopify practitioners: "delay until 30 seconds or the second page view".
     - Wisepops' best delay bucket is 11 to 15 s, and it reports a page-2 trigger at +39%.
     - Kivetz et al. 2006 (goal gradient): motivation grows with progress, so ask deep in the visit.
3. **Evidence of looking: 2 signals out of 5.**
   - The five signals:
     - **read:** 1.5 screens or 30% of the page;
     - **price:** a ₪ figure on screen for 2 s;
     - **explore:** a tap on the page's own tools (a tab, the gallery, the map, the 3D stage, the plans);
     - **pause:** a 6 s stop to read after a screen;
     - **return:** the 2nd project or listing page of the visit.
   - Evidence:
     - Freedman and Fraser 1966: a small earlier action raised agreement to the big one from 17% to 76% (foot in the door; consistency).
     - Organic Aromas: a popup "after three clicks" or on exit brought subscribers who bought more often (14.1% and 19.03%).
     - Real-estate tools ask after 1 to 2 listing views (BoomTown at the 2nd, IDX Broker "request after the 1st or 2nd").
4. **A natural break.** Even when ready, it waits until:
   - scrolling stopped for 1.5 s;
   - no finger or button is down;
   - no text is selected, no field is focused, no video is playing.
   - Evidence:
     - Adamczyk and Bailey (CHI 2004): the best moment brought 56% less annoyance than the worst and 43% less than a random timer.
     - Bailey and Konstan 2006: mid-task interruption gave 31% to 106% more annoyance and twice the errors.
     - Iqbal and Bailey 2008: frustration was 2.6 at a breakpoint against 5.5 mid-action.
     - Edwards, Li and Lee 2002 (pop-up ads, about 373 people): show them "only at breaks in content".
     - Yahoo! JAPAN 2017 (687,840 users): waiting for a break cut response time 49.7% and raised clicks.

**Leaving signals are the last chance.** They need the floor and one signal: the pointer out through the top (desktop), a fast run back to the top after 2 screens (phone), a return to the tab after 15 s away.

**A visitor who never engages never sees it.**

**Never:**
- while a field has focus;
- in full screen;
- while another dialog is open;
- after a WhatsApp tap on this visit;
- on a page that is not Hebrew.

**Measured, not assumed:**
- `pa_shown` carries the trigger, the active seconds, the page seconds, the signals and the page number.
- Every sign-up stores the same, and Ben's mail says it in words, for example "לפני ההרשמה: 31 שניות פעילות מתוך 44, עמוד 2 בביקור; ראה מחירים, עצר לקרוא".
- The 10% holdout shows the lift.

**Checking links:**
- `?nudge=show`: only a look at the design, after 2 s.
- `?nudge=fresh`: the real timing as a new visitor, with a small live meter at the top: seconds, active time, signals, and "מחכה לרגע שקט" until the window opens.

**Tested before release** (the real markup, CSS and JS on a long page; phone 375):
- idle for 41 s: never opened;
- skimming continuously for 27 s: active 26 of 25, but one signal (read), so it did not open;
- the same reader then stopped to read: it opened at 31 s active with read and pause (`pa_trigger: engaged`).
- **How often:**
  - once a session, and at most twice in 30 days;
  - 3 days of quiet after a close, 1 day if it was ignored (30 s untouched on a phone);
  - never again for a year after a sign-up;
  - a 10% holdout, re-drawn every 30 days, so nobody is excluded for good.
- **Checking link:** `?nudge=show` shows it after 2 s.

## Format
- **Phone:** a bottom sheet with no backdrop. The page keeps scrolling. Swipe the board down, ×, "לא עכשיו" or Esc closes it.
  - Step 2 hides the sub line, so the form fits.
  - The sheet rides above the keyboard (visualViewport).
- **Desktop:** a centred 440 px modal over a 55% scrim. Focus moves in, Tab is trapped, and Esc, the scrim or × close it. Focus returns to where it was.
- **Indexing:** the markup waits in a `<template>`, so the indexed page carries no repeated text and no extra heading.

## Where
- **Shown on:**
  - every published Hebrew `nadlan_project`, except Ashira (blocked by slug, Ben 31.10) and any project whose box says off (Rainbow, Ben 1.11);
  - every Hebrew `nadlan_property` with no `nl_broker_id`;
  - Hebrew `nadlan_intl` projects.
- **Never on:**
  - Meital Katzir's listings or any broker's;
  - professionals and broker pages, articles and city pages.
- **Admin:**
  - the project box and the list column stay;
  - Settings › חלון עדכוני מחירים has the three scope switches, the timings, the holdout, a count of sign-ups and the current national figure.

## The sign-up
- **Endpoint:** `POST /nadlan/v1/price-alert` creates a private `nadlan_lead` with:
  - goal "עדכוני מחירים", utm_source `price_alert`;
  - the page, the city, the interest, the trigger and the trend;
  - the consent text, its version (`pa1-2026-11-08`) and its time.
- **Owner alert:** Ben gets the rich lead mail 2 minutes later, with tap-to-call and WhatsApp links.
- **Never routed:** no developer, broker or card owner gets it (no `lead_card_id`). No drip and no AI call run on it.
- **Checks:**
  - Israeli phone numbers only;
  - a honeypot;
  - 6 sign-ups an hour per device, 4 a day per email;
  - one sign-up per email and page a day.

## Proof: a counted comparison (research read 8.11.2026)
Research files: `docs/research/2026-11-08-price-alert-had684/`.

✓ = has it, ½ = partly, ✗ = no, ? = could not verify.

| What the visitor gets | NadLan 106 | Zillow | Redfin | Rightmove | Zoopla | Idealista | Domain | Bayut | Property Finder | Yad2 | Madlan | Dimri | Tidhar | Azorim |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A price alert for an area or a project (not only a saved listing or search) | ✓ | ✗ | ✗ | ✗ | ½ (own home) | ✗ | ½ (home alerts) | ✗ | ✗ | ✗ | ? | ✗ | ✗ | ✗ |
| No account needed | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ? | ✓ (WhatsApp) | ✗ | ? | ✓ | ✓ | ✓ |
| Offered by itself at the moment of interest | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ? | ✗ | ✗ | ✗ |
| An official-data guard on the message | ✓ | ✗ | ✗ | ½ (2% rule) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ? | ✗ | ✗ | ✗ |
| One-tap interest (buy / own / invest) | ✓ | ✗ | ✗ | ½ (New Homes, signed in) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ? | ✗ | ½ (topic) | ½ (project) |
| WhatsApp as a channel | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ½ (contact) | ✗ | ? | ½ (consent) | ✗ | ✗ |
| The full section 11 notice at the form | ✓ | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | ? | ? | ½ | ½ | ½ |
| The phone field explained | ✓ | n/a | n/a | n/a | n/a | n/a | n/a | ? | n/a | n/a | ? | ✗ | ✗ | ? |
| **Score (✓ = 1, ½ = 0.5)** | **8** | 0 | 0 | 1 | 0.5 | 0 | 0.5 | 0 | 1.5 | 0 | ? | 2 | 2 | 1.5 |

The highest competitor score is 2 of 8. No site checked offers an area or project price alert without an account, at the moment of interest, guarded by official data.

## Proof: the evidence checklist (16 of 16)
1. **Not on arrival; 12 s plus one screen.** NN/g says "never show a popup before users can glean value". Wisepops' best delay bucket is 11 to 15 s.
2. **A bottom sheet on phones, the page scrollable, easy to dismiss.** This is Google's listed exception ("banners that use a reasonable amount of screen space and are easily dismissible").
3. **The close button is never delayed.** Delaying it would break "easily dismissible".
4. **Two contact fields only.** Popupsmart: 2 fields 0.94% against 0.56% for 3.
5. **The phone field is explained inline.** Baymard: an unexplained required phone field brings fake numbers or abandonment.
6. **A small first step.** Freedman and Fraser 1966: 76% against 17%. Vendor data on two-step forms is mixed, so this is measured, not assumed.
7. **A first-person button.** "My" against "your": +24% (Wiebe) and +90% (ContentVerve).
8. **A neutral decline, no guilt line.** NN/g's article on shaming users.
9. **Blinking under 5 s, none under reduced motion.** WCAG 2.2.2.
10. **At most two showings.** Popupsmart's fatigue curve: 1.33%, then 1.22%, then down to 0.41% by the sixth.
11. **A 10% holdout** for the real lift.
12. **The success state names the next step,** with no dead end (gov form patterns).
13. **The consent is an unticked, separate box,** and the wording, version and time are kept (Privacy Protection Authority, 25.2.2026).
14. **The section 11 notice has all five parts** (amendment 13).
15. **No repeated text in the indexed page** (the template).
16. **The area comes from the page, not from IP.** Wisepops: geo targeting converted 3.48% against 5.29% without it.

## What is still unknown
- **The real rate here.** The published median for real-estate lead popups is 0.69% of displays, and the top 10% reach 3.87% (Popupsmart 2026). The holdout and the GA4 events `pa_shown`, `pa_step2`, `pa_submit`, `pa_done`, `pa_close`, `pa_error`, `pa_holdout` and `generate_lead` will show where NadLan lands.
- **Lost sign-ups.** A required phone field costs sign-ups: one 2014 case lost 52%. Ben chose both fields.
- **The one-step version** (fields on the first screen) is the next test.
- **Sending is manual for now.** The sign-ups reach Ben. The automatic alert engine (`inc/near-alerts.php`) is dormant until he turns it on.

## 106.3 and 106.4 (8.11.2026, 1.72.612 and 1.72.613): automatic updates, a direct line and the owner's lead mail
Ben, 8.11.2026: "Turn the automatic updates on; what matters is that we keep their details and it sends them to us. Let a person also just contact us through the window. Send me the details in an orderly way, like a lead. Make it possible to act from the mail."

- **Automatic updates.**
  - A sign-up also asks the site's alert engine (inc/near-alerts.php), which was switched on 8.11.
  - **Double opt-in:** one confirmation mail first; step 3 says it was sent.
  - **On a project**, a change in its price per m², stage or units, and new listings within 1.5 km.
  - **On a listing**, its price drop and new listings around it.
  - The privacy policy carries the matching sentence.
- **A direct line.**
  - Step 1 adds a row under the three choices: "או ישר: [שיחזרו אליי] [וואטסאפ]".
  - "שיחזרו אליי" opens the form in call mode ("לאן לחזור אליכם?"), with an optional question.
  - The form also has "אשמח גם שיחזרו אליי לשיחה קצרה על האזור".
  - The WhatsApp message is Ben's approved 105.7 wording.
  - A repeat sign-up from the same person that asks for a call is never lost: it updates the first lead and mails again.
- **The owner's lead mail.** One HTML mail per sign-up replaces the plain-text alert for these leads.
  - **The top:** a dark strip with the city, then "ליד חדש" or "ליד חם: ביקש/ה שיחה". The phone in 34 px, tap to call, then the email.
  - **Three buttons:** התקשר, וואטסאפ, מייל.
  - **The facts:** what interests them, the request, their question, area, page, behaviour before signing up, the updates status, time.
  - **Two signed actions** that work from the mail with no login: "חזרתי אליו" and "לא רלוונטי". The link opens one confirm button, so a mail scanner changes nothing; the click marks the lead's status and the audit log.
  - **Links:** the lead in the admin, and the Excel of all sign-ups.
- **The Excel export:** Settings › חלון עדכוני מחירים, "הורדת כל הנרשמים (Excel)".

## Pressed live (8.11.2026, Chrome, 1.72.609 and 1.72.610)
- **Desktop 1366:** the modal opens over a 55% scrim. Focus moves in and the floating bar steps aside.
  - Step 1, then step 2, then the empty-form errors (three, in Hebrew).
  - The typo suggestion "התכוונתם ל־dana@gmail.com?" accepts on one click. Then the consent box, then step 3.
  - The payload holds the cleaned phone, the corrected email, the interest, the consent and the notice version.
  - The GA events arrive in order.
- **Phone 390:** the sheet sits under the H1 and the lead paragraph, the accessibility button rises above it, and a swipe on the board closes it (`pa_close: swipe`).
- **The theme writes every input with `!important`:** a cream #fffdf8 field, a 0.14 hairline border, a brass focus ring, and pill buttons without the shadow.
  - 1.72.610 adds an `html body #nlnu` layer that wins.
  - Any new form inside the site needs the same layer.

## Accessibility
- **Roles and labels:**
  - `role="dialog"`: `aria-modal` is true on desktop and false on the phone sheet;
  - it is labelled by the line and described by the sub line;
  - every field has a visible label.
- **Errors** are spoken (`aria-live`) and mark the field `aria-invalid`.
- **Targets** are at least 44 px; inputs use 17 px text, so iOS does not zoom.
- **Contrast:**
  - white and champagne on the board: 15.6:1 and 11.8:1;
  - the red on the board: 5.1:1;
  - `sa-ink2` on white: 9.5:1;
  - fine print `nlb-mute`: 5.46:1.
- **Focus** rings are visible everywhere.
