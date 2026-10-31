# PriceNudge

A quiet price-list slip that rises from the bottom of a project page, late in the visit, and offers plans, a timeline and current prices on WhatsApp in one tap. It never covers the page, it leaves with a swipe of the finger, and it fades out by itself if it is ignored.

**Version 105.2 (31.10.2026, Ben's wording).** Built for Rainbow only first (release 1.72.538); every other project waits for Ben's look.

- **The line:** "מחירי הנדל״ן משתנים".
- **The small line:** "לחצו לקבלת עדכון מחיר, תוכניות וסטטוס הפרויקט, ישירות בוואטסאפ."
- **Three chips** ("עדכון מחיר", "תוכניות", "סטטוס הפרויקט"): each opens WhatsApp with its own ready message, so nobody has to type.
- **The button:** "לקבלת עדכון בוואטסאפ".
- **The delay is 25 seconds,** inside the 10 to 50 that the timing studies recommend, with 35% scroll.
- **Ben owns the wording.** The project box takes his own line.

**Version 105 (31.10.2026, Ben's order: catch the visitors who read Rainbow and leave).** Linear HAD-642.

## Why it looks like this

- The subject is the developer's price list (מחירון), so the sheet is a slip of paper: a perforated top edge, the project name and the word "מחירון" in the kicker, one serif line, one green WhatsApp button.
- It stays inside Skin A: `sa-surf` slip, `sa-line` perforation, `sa-sea` kicker and fade line, `wa-green` button (the only WhatsApp green on the site), Noto Serif Hebrew for the line and Assistant for the rest. No gold, cream or terracotta, no gradient, no emoji, no second accent colour.
- It is a banner by Google's own definition: on a phone it takes at most 30% of the screen height and the page above it stays readable and scrollable. It is not a modal: no dark backdrop, no focus trap, nothing is locked.

## When it appears (all thresholds are settings)

- **Never on arrival.** The first trigger is 25 seconds of the page being visible AND at least 35% of the page scrolled.
- **Leaving signals, desktop:** the pointer leaves through the top edge of the window after 15 seconds on the page.
- **Leaving signals, phone (there is no mouse):** a fast scroll back up (over 1,200 px per second) after the reader passed half the page; or the reader returns to the tab after leaving it for 20 seconds or more.
- **Never:** while a form field has focus, after the reader already tapped any WhatsApp button or opened the chat on this visit, on a page whose project is switched off, or inside the 3D stage's full-screen mode.
- **Not the back button.** Catching the back button (history trap) is a dark pattern that Google and browsers punish. It is not done.

## How it leaves

- **Swipe down** with a finger or the mouse: the slip follows the finger; past 35% of its height, or a flick faster than 0.5 px per ms, it drops away. Short of that it springs back.
- **"לא עכשיו"**, the ×, or Esc.
- **By itself:** a thin `sa-sea` line under the slip shrinks over 14 seconds; when it ends the slip fades away. Touching or hovering the slip pauses the line.
- After any of these, it does not return for 7 days on any project. After a WhatsApp tap, not for 30 days.

## Words (language-dna, honesty law)

- **Kicker:** the project's short name + " · מחירון".
- **Line:** "רוצים את המחירים העדכניים?"
- **Small line:** "תוכניות, לוח זמנים ומחירים מעודכנים, ישירות בוואטסאפ."
- **Date chip, only when it is true:** "המחירון באתר עודכן ב-14.10.2026" shows only when the project carries a dated price field updated in the last 60 days. Rainbow's prices are from the developer's reports up to 3.2026, so Rainbow gets no date chip. Ben's wording "המחירים התעדכנו" is not used as a blanket line, because on most project pages it would not be true.
- **Button:** "לקבלת תוכניות ומחירים בוואטסאפ" (the floating bar alone says "ייעוץ חינם").
- **The WhatsApp message:** "שלום, אשמח לקבל תוכניות, לוח זמנים ומחירים מעודכנים של <project>." plus the page, through wa-source.php.
- **On an urban renewal compound** (no prices exist): kicker "<compound> · התחדשות עירונית", line "רוצים לדעת מה קורה במתחם?", small line "עדכון על התכנון, החתימות וההיתר, בוואטסאפ.", button "לקבלת עדכונים בוואטסאפ".
- Five languages through `inc/i18n.php` (`nudge_*` keys).

## Control (Ben's checkbox)

- **Per project:** a box in the project's edit screen: "חלון עדכון מחירים: להציג בעמוד הזה" (on / off / follow the site default), and an optional own line. The same switch appears as a column in the projects list, so many projects can be turned on or off from one screen.
- **Site settings (Settings › NadLan › חלון עדכון):** on or off for the whole site, the default for new projects, the delay, the scroll depth, the leaving signals, the quiet days, and the share of visitors who do not see it (a 20% holdout, to measure what it really adds).
- **Off from day one:** Ashira (Ben, 31.10.2026), every broker and owner listing (they have their own contact bar), every page outside the project pages.

## One contact element per screen

- While the slip is up, the floating "ייעוץ חינם" bar steps aside (the slip has its own WhatsApp button), and the chat bubble's greeting is held back.
- The slip sits above the phone's home area: `bottom: env(safe-area-inset-bottom)`.

## Measurement

- Events to Google Analytics (gtag is on the site): `nudge_shown` (with the trigger: time, leave_desktop, scroll_up, tab_return), `nudge_close` (swipe, button, esc, fade), `nudge_wa` (the tap).
- The holdout group gets `nudge_holdout`, so WhatsApp taps per 100 visits can be compared with and without the slip, per project.
- Realistic expectation: the published median for lead popups in real estate is about 0.7% of displays (Popupsmart 2026). On Rainbow's current traffic that is a few extra conversations a month, not dozens. Traffic is the bigger lever.

## Accessibility

- `role="dialog"` with `aria-modal="false"` and `aria-labelledby`; focus is never moved into it; Esc closes it; the × has the label "סגירה".
- Every target is at least 44 px high. Under `prefers-reduced-motion` it appears and leaves without movement, and there is no fade line.

## Built from (when built)

- New: `inc/price-nudge.php` (meta box, list column, settings, render), `assets/nudge/nudge.js`, `assets/nudge/nudge.css`.
- Reads: the project's price-date field, `inc/i18n.php`, `inc/wa-source.php`, the `#nlcta` floating bar (to step it aside).
- Does not touch: the 3D stage and its engine, the area map's cone, any project's content.
