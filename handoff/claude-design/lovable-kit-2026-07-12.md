# LOVABLE MEGA-PROMPT KIT for nad-lan.co.il (2026-07-12)

How to use (10 minutes of setup, then build):
1. Create a new Lovable project (Pro recommended: free tier = 5 credits/day AND
   public projects; a full design set costs ~15-25 credits).
2. Open Project Settings -> Knowledge and paste PART 1 whole (this is the
   design system - Lovable re-reads it before EVERY generation; it is the
   only thing that keeps a multi-page build consistent).
3. Send PART 2 as the first chat message (scaffold only - no content yet).
4. Send the PART 3 prompts ONE AT A TIME, in order, reviewing each result
   before the next (Lovable's own docs: "a full-page prompt gets you noise,
   a section-based prompt gets you signal").
5. When a section drifts off-style, reply exactly: "Re-read the Knowledge
   file and fix this section to match the design tokens. Change nothing else."
6. Connect GitHub (two-way sync) so we can pull any code we like into the
   real plugin.

---

## PART 1 - PROJECT KNOWLEDGE (paste into Lovable "Knowledge", verbatim)

# Project: NadLan - premium Hebrew real-estate platform (nad-lan.co.il)

## Product context
NadLan is Israel's "choose your apartment from inside the building" platform:
every new-construction project is a living 3D model (floors, apartments, sun,
view from the window). Around that core: property listings, a professionals
directory, an urban-renewal product (a private "project room" where a
building tracks consent on a 3D model), a rentals manager for private
landlords (portfolio map -> building 3D -> apartment file), calculators, and
a real-estate encyclopedia. Audience: Hebrew-speaking apartment buyers and
owners first; English for olim and foreign investors. Positioning: premium,
editorial, trustworthy - a boutique institution, not a classifieds board.

## Language and direction (NON-NEGOTIABLE, verify on every page)
- All UI text in HEBREW. lang="he" and dir="rtl" on <html>.
- Tailwind LOGICAL utilities ONLY: ms-/me-/ps-/pe-/text-start/text-end.
  NEVER ml-/mr-/pl-/pr-/left-/right-/text-left/text-right.
- Wrap the app in Radix DirectionProvider dir="rtl".
- Add rtl:space-x-reverse wherever space-x-* is used.
- Mirror ALL directional icons (chevrons, arrows, back buttons) for RTL.
- Numbers, prices and phone numbers sit in <span dir="ltr"> (₪ prices,
  +972 phones, dates). English brand names too.
- Every page also gets an /en/ sibling in ENGLISH with dir="ltr" - same
  components, translated copy, mirrored layout.

## Design tokens (exact - never substitute)
- --paper: #FAF7F1 (page ground)  --ink: #1B1A17 (text)
- --gold: #9C7A3C (structure accents, links, kickers)
- --terracotta: #C2563A (money CTAs ONLY - one per viewport)
- --hairline: #E2DCD0 (borders)  --band: #F3EEE3 (alternate band ground)
- --theater: #14130F (reserved: ONE dark stage for the 3D showcase and the
  international band - never stack dark sections)
- Semantic: success #517048, warning #9C7A3C, danger #C2563A, muted #A79E8D
- Radius: cards 16px, stages 22px, chips 999px. Shadows: soft, warm,
  0 24px 60px -28px rgba(27,26,23,.35) for elevated stages only.

## Typography (Google Fonts - load both)
- Headlines: "Frank Ruhl Libre" (serif), weights 500-800.
- Body + UI: "Heebo", weights 400-700.
- Scale: h1 clamp(1.7rem,4vw,2.5rem)/1.25; h2 ~1.5rem; body 14.5-15.5px/1.7;
  captions 12px. Hebrew line-height never below 1.5. Uppercase kickers:
  Heebo 700 12.5px letter-spacing .06em in gold.

## Composition laws
- ONE of everything per page: one search, one map, one contact bar.
- Premium is restraint: gold is an accent, never a surface. At most ONE dark
  band per page (the 3D theater). Everything else cream/white/band.
- Generous whitespace; hero is a thesis, not a collage.
- Every estimate or illustration carries an honest label ("הדמיה",
  "נתוני דוגמה", "אומדן בלבד").
- No lorem ipsum EVER - real Hebrew copy is provided per section prompt.
- Images must depict the section's actual content (a Tel Aviv building for a
  Tel Aviv project card, a landlord dashboard for the rentals band) - never
  decorative stock. Style for generated images: architectural ink-and-wash
  sketch on cream paper, restrained color washes, single gold accent - or
  clean photoreal aerial/architectural photography. Never purple gradients,
  never generic 3D blobs, never smiling-stock-people.

## Component rules
- Buttons: primary = terracotta fill, white text, 12px radius, subtle warm
  shadow; secondary = 1.5px gold border on white; both with hover
  brightness(1.06). Focus rings visible (gold).
- Cards: white, 1px hairline border, 16px radius, hover translateY(-2px) +
  gold border.
- Chips: band ground, hairline border, 999px radius, Heebo 600 12px.
- Forms: inputs on paper ground, hairline border, 10px radius, 11px padding.
- Status is shown as color + label, never color alone.

## Pages to build (React Router routes)
/ (homepage), /projects, /project/:slug, /listings, /listing/:id,
/professionals, /urban-renewal, /my-renewal (product landing),
/my-rentals (product landing), /calculators, /glossary, /en (English home).

## Never do
- No LTR layouts, no physical direction classes.
- No default shadcn look, no purple/blue gradients, no emoji as icons.
- No more than one dark band per page. No fake statistics or fake teams.
- No placeholder text or placeholder images.

---

## PART 2 - FOUNDING PROMPT (first chat message)

# Context
Premium Hebrew RTL real-estate platform "NadLan". The complete design system,
language mandate and page list are in the project Knowledge - follow them
exactly. Before doing anything, review the Knowledge and confirm your
understanding of: the token palette, the RTL rules, and the one-dark-band law.

## Task
Scaffold ONLY the application shell:
1. index.css + tailwind config carrying the exact tokens from Knowledge.
2. Google Fonts: Frank Ruhl Libre + Heebo.
3. <html lang="he" dir="rtl">, Radix DirectionProvider dir="rtl".
4. React Router with all routes from Knowledge (empty pages, each showing
   only its Hebrew page title in the correct type scale).
5. Header: logo "נדלן" (Frank Ruhl Libre 800), nav: פרויקטים חדשים, דירות,
   אנשי מקצוע, התחדשות עירונית, ניהול השכרות, מדריכים; language toggle HE/EN.
6. Footer: 4 columns of real links (use the nav items + מחשבונים, מילון
   מונחים, אודות, צור קשר), one dark band (--theater) - this is the page's
   only dark section.

### Guidelines
Editorial, calm, premium. Reference feel: a luxury broadsheet, not a SaaS
dashboard.

#### Constraints
NO page content yet. NO images yet. Verify the rendered shell is RTL
(nav flows right-to-left, logical classes only) before finishing.

---

## PART 3 - SECTION PROMPTS (send one at a time, in order)

S1 HERO (homepage): Full-bleed aerial photograph of the Tel Aviv shoreline
(generate: photoreal aerial, oblique angle, beach + marina + city receding,
late-afternoon warm light). Overlay: dark glass card (right side), H1
"מוצאים דירה, בודקים מחיר, מכירים את הסביבה - לפני שחותמים", sub
"כל פרויקט באתר הוא מודל תלת-ממדי חי: קומות, דירות, שמש ונוף מהחלון.",
search tabs [קנייה] [השכרה] [פרויקטים] [אנשי מקצוע] + one input + terracotta
button "חיפוש". Trust row: "197 פרויקטים · 938 מתחמי התחדשות · 5 מחשבונים".

S2 FLAGSHIP 3D THEATER: the page's ONE dark band (--theater). Title
"בחרו דירה מתוך הבניין, בתלת ממד". Left: large stage placeholder for a 3D
model (dark, radial glow) with chip "הדגם התלת ממדי האמיתי של הפרויקט".
Right: 4 selector cards (real projects: "קשת חולון · 118 דירות",
"DUO רמת גן · 2 מגדלים", "רינבו באר יעקב · 240 דירות", "שדה דב ת״א").
Honest line: "פרויקטים אמיתיים שהפכנו למודלים חיים כהדגמת יכולת - היזמים
המוצגים אינם לקוחות שלנו." + gold link "יזמים: רוצים את הבניין שלכם על הבמה?"

S3 LIVE MAP BAND (light): cream-styled map illustration with named city
chips ("תל אביב · 43", "ירושלים · 28", "חיפה · 19") and terracotta pins;
kicker "LIVE", title "מפת הפרויקטים החיה", sub "התקרבו לעיר ובחרו פרויקט".

S4 RENTALS BAND (white card, gold frame): kicker "ניהול השכרות · חינם",
title "כל הדירות המושכרות שלכם: על המפה ובתוך הבניין", 3 numbered step chips
(מוסיפים נכס / מסמנים דירות על המודל / רואים הכל בצבע אחד), terracotta CTA
"מתחילים לנהל, חינם", note "מעקב ותזכורות, לא סליקה". Generate image: the
landlord dashboard concept - a 3D building with green/gold/terracotta
apartment dots, map above it, ink-sketch style on cream.

S5 URBAN RENEWAL BAND (band ground): kicker "התחדשות עירונית", title
"חדר הפרויקט של הבניין שלכם", 3 steps (בודקים את הבניין / פותחים חדר /
מזמינים את השכנים), CTAs "בדיקת כדאיות חינם" + "הדגמה חיה".

S6 LISTINGS GRID: 4 cards with real copy ("דירת 3 חדרים משופצת, לב תל אביב
· ₪3,690,000 · 78 מ״ר · קומה 2"...). Images: ink-sketch building plates,
NEVER cropped (object-fit contain on band ground).

S7 TOOLS ROW: 5 light tool cards (מחשבון משכנתא, מס רכישה, שווי נכס,
קנייה מול שכירות, בדיקת התחדשות) - lead card on band ground w/ gold border.

S8 MAGAZINE/GUIDES: editorial 3-card row with kicker/serif titles from real
guides ("מה במקום תמ״א 38?", "מדריך קניית דירה", "פינוי בינוי: המדריך המלא").

S9 PROJECT PAGE (/project/:slug): hero = 3D stage (dark) + facts rail;
tabs for apartments/floors; sun + view chips; offer CTA. Use "קשת חולון".

S10 /my-rentals LANDING: hero + 3 steps + live demo frame (the dashboard
from S4 as a big embedded card: map, building, apartment panel with ledger
grid, health cards row חוזה/שכ״ד/בטוחות/תיקונים/מס/חידוש).

S11 /my-renewal LANDING: mirror of S10 for the renewal room (3D consent
colors, 10-stage stepper, documents rollup).

S12 ENGLISH HOME (/en): same components dir="ltr", translated copy
("Find an apartment, check the price, know the area - before you sign").

FINAL AUDIT PROMPT (Plan/Chat mode, costs no build credits):
"List every element still using physical direction classes, any English text
on Hebrew pages, any lorem ipsum, any image not matching its section's
content, and any second dark band. Do not change code - just list."
