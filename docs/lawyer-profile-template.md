# Lawyer profile / storefront — reusable template (DRAFT for owner approval)

> **Status:** template spec. The first instance is filled with the owner's verified facts (Ben Bettesh). Future lawyers reuse the same anatomy.
> **Design source:** merge of din.co.il (profile anatomy, answered-Q&A trust) + Fiverr (services-with-prices, reviews stamped with price-band + turnaround). Research §5b.
> **URL pattern:** `/lawyers/{slug}/` — e.g. `/lawyers/ben-betesh/`.
> **CPT:** reuse existing `professional` catalog CPT (registered in nadlan-config plugin).

---

## Section anatomy (top → bottom)

### A. Header card
- **Photo** (professional headshot, square).
- **Full name + title:** `בן בטש, עו"ד`
- **License / bar trust line:** `חבר לשכת עורכי הדין · רישיון מס' 29020` → link to israelbar.biz profile.
- **One-line specialty:** `עו"ד מקרקעין — חוזי מכר, שכירות ורכישה מקבלן`
- **City:** `תל אביב יפו`
- **★ rating + review count** (hide until real reviews exist).
- **"זמן תגובה ממוצע"** (Fiverr lever) — e.g. `תוך שעה`. (Populate from real data; omit if unknown — never fake.)
- **Languages (שפות):** עברית, אנגלית.
- **Primary CTA:** `הזמינו ביקורת חוזה` → `/contract-audit/` (with this lawyer pre-selected).

### B. About (`על עוה"ד`)
Short bio paragraph. Owner-supplied facts to weave in:
- בן בטש, עו"ד, בר 29020.
- Other site (sameAs / schema): https://jus-tice.co.il/
- Address: וולנברג ראול 18, תל אביב יפו.
- Contact (handoff/back-office only — NOT public on page unless owner wants): mobile 0525101555, info@nad-lan.co.il.

> **Owner: please supply 2–3 sentences of bio** (years of experience, areas, a human line). I'll draft a placeholder you can replace.
> **Draft placeholder bio:** `עו"ד בן בטש עוסק בדיני מקרקעין ומלווה רוכשים, מוכרים ושוכרים בעסקאות נדל"ן. הוא בודק חוזי דירה לעומק — מסמן סיכונים, מנסח הערות לתיקון ומסביר בשפה ברורה מה חשוב לפני החתימה.`

### C. Services (the storefront — Fiverr-style)
The 3 productized services WITH prices + `הזמינו` buttons, pulled from `/contract-audit/`:
- ביקורת חוזה — בסיסי · ₪390 + מע"מ · `הזמינו`
- ביקורת חוזה — מלא · ₪690 + מע"מ · `הזמינו`
- ביקורת חוזה — קבלן · ₪1,200 + מע"מ · `הזמינו`

### D. Sample work (`דוגמה לחוות דעת`)
A redacted sample opinion PDF/thumbnail (gallery). Builds confidence in the deliverable.
> **Owner: supply one redacted sample opinion** (or I draft a 1-page mock template marked "לדוגמה בלבד").

### E. Answered Q&A (`שאלות ותשובות`) — din's strongest trust move
Embed 3–5 real questions the lawyer has answered (מחיר למשתכן, הערת אזהרה, מה בודקים בחוזה שכירות…). Doubles as SEO. Bolt onto existing forum/Q&A content.

### F. Reviews
Each review stamped (Fiverr pattern): name · package bought · turnaround delivered · ★ · text · `לקוח חוזר` badge. Hide section until real reviews exist.

### G. Footer disclaimer
The approved disclaimer (lawyer = client's lawyer + חשבונית issuer; platform = intermediary) — from `contract-audit-tos-refund-disclaimer.md`.

---

## Schema (JSON-LD)
- `@type: Attorney` (or `LegalService`) — name, image, address, telephone (use **0525101555** — sole number; the landline 036916454 is retired), areaServed, sameAs `https://jus-tice.co.il/`, member of `לשכת עורכי הדין` (bar 29020).
- `makesOffer` → the 3 Service offers.
- Keep telephone consistent with the site's `tel:` / `wa.me` (already +972525101555).

---

## Owner inputs still needed (will use placeholders until provided)
1. Bio (2–3 sentences) — placeholder drafted above.
2. Headshot photo.
3. One redacted sample opinion (or approve a mock).
4. Real "average response time" value (else omit).
5. Confirm whether to show email/phone publicly on the profile, or keep them back-office only.
