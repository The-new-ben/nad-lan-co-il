# Buyer gaze and thumb rules for the apartment cockpit

Research date: 10.11.2026. Scope: the panel that opens when a buyer taps an apartment in the 3D tower
(plan, view from the window, price and deals, monthly cost and taxes, the area, the shops below, video
call, 360 inside). Hebrew first (right to left), plus English, French, Russian and Arabic.

Viewports used for every "how it applies" line:
- Phone: 375 x 812 CSS px (iPhone X class). On this class 1 mm is about 6 CSS px
  (1125 device px / 458 ppi = 62.4 mm wide, divided by 375 CSS px = 0.166 mm per px).
- Desktop: 1440 px wide, about 800 to 900 px of usable height.

## How to read the evidence grades

| Grade | Meaning |
|---|---|
| A | Controlled experiment at scale, field experiment, or meta-analysis. |
| B | Large observational data, or a usability or eye-tracking finding replicated across studies and years. |
| C | Single lab or usability study, expert guideline built from usability testing, or a platform standard (normative, not empirical). |
| D | Vendor claim, industry survey, anecdote, or inference from adjacent evidence. |

"Verified" below means the figure was read on the primary page or abstract on 10.11.2026. "Secondary"
means the primary page was unreachable or paywalled and the figure comes from a summary that quotes it.
Every rule is a prior, not a law: rule R36 says how to test it on our own traffic.

## The cockpit in one picture

- Phone: a sheet over the live tower with three heights. Peek (about 140 px): apartment identity and
  all-in price. Half (about 55% of the screen): the apartment's own visual, key facts, one primary
  action. Full: the complete apartment page with its own address (URL), Back support, vertical
  sections and a slim action bar at the bottom.
- Desktop: a docked panel on the reading-start side (right in Hebrew and Arabic, left in English,
  French and Russian), about 440 to 520 px wide, with the tower still live beside it.

---

## A. First screen and attention

### R1. Lead with the apartment's own visual, never with decoration
**Rule:** The first large element in the panel is information-carrying imagery of this exact apartment
(floor plan, real view from its windows, real or clearly labelled interior), not a lifestyle or stock image.

**Evidence:**
- Seiler, Madhavan and Liechty 2012, Journal of Real Estate Research 34(2), eye tracking of home buyers
  on listing pages: the photo is viewed first, then the quantitative facts, "distantly followed" by agent
  remarks; dwell time on the photo predicts the buyer's opinion of the home and its value. Verified (abstract).
  A press summary of Seiler's follow-up (45 participants) gives roughly 60% of viewing time on photos,
  20% on the description, 20% on agent remarks. Secondary.
- Baymard Institute product-page testing: 56% of users' first action on a product page is to inspect
  the images. Verified on Baymard's site; platform (desktop or mobile) not stated.
- Nielsen Norman Group (NN/g) 2010, "Photos as web content": users look at information-carrying images
  (products, real people) and ignore decorative and stock images. Verified (summary).
- Zhang, Lee, Singh and Srinivasan 2022, Management Science 68(8): Airbnb units that received
  professional "verified" photos earned about 8.9% more demand (working-paper figure; about 41% of the
  effect attributed to image quality). Secondary for the exact number.

**Strength:** B. Convergent across eye tracking, usability and field data; the real-estate eye-tracking
samples are small (tens of people) and from 2011 to 2013.

**Phone 375x812:** In the half state the visual takes roughly 35 to 55% of the visible sheet; default to
the floor plan for new-build projects (the buyer cannot visit) and to the real view when the floor is high.

**Desktop 1440:** The visual is the first block under the identity line, full panel width (about 480 px),
4:3 or 1:1, with a one-click switch between plan, view and interior.

**RTL:** Visual order of the switcher (plan, view, 360) starts at the right edge in Hebrew and Arabic.

### R2. The first screen answers "which, how big, how much" and offers one next step
**Rule:** Without scrolling, the panel shows the apartment identity (building, floor, rooms, m2,
orientation), the all-in price, the visual, and one primary action.

**Evidence:**
- NN/g 2018, "Scrolling and attention": 120 participants, more than 130,000 fixations on a 1920x1080
  screen. 57% of viewing time was above the fold and 74% within the first two screenfuls; in 2010 the
  share above the fold was 80%. Verified. Desktop only; no mobile data in that study.
- Counterpoint: Chartbeat 2014 (Haile, TIME): on media article pages about 66% of engaged time happens
  below the fold. People scroll when the first screen promises more. Secondary.

**Strength:** B for desktop; mobile is inferred (no comparable mobile eye-tracking figure was found).

**Phone 375x812:** Peek state = identity + all-in price. Half state = visual + identity + price +
3 to 4 key facts + one primary action, all inside the first 812 px with the sheet at about 450 px.

**Desktop 1440:** Identity, price and primary action sit in a sticky panel header (about 120 px tall);
the visual follows directly below.

**RTL:** Identity and price align to the right edge in Hebrew and Arabic.

### R3. Front-load every line and heading; the start is the right edge in Hebrew and Arabic
**Rule:** Put the information-carrying word or number at the start of each line, label and heading,
because scanning eyes fixate on line starts and drop off along the line.

**Evidence:**
- NN/g F-pattern (first reported 2006, re-checked 2017): users fixate the top lines and the start of
  lines; "alive and well" on desktop and mobile; the pattern is mirrored for Arabic ("reversed F").
  Heatmaps aggregate 45 to 47 users per page. Verified.
- NN/g 2019, "Text scanning patterns": F, spotted, layer-cake and commitment patterns; in right-to-left
  languages the F is mirrored with more attention on the right side. Verified.
- Pollatsek, Bolozky, Well and Rayner 1981, Brain and Language: the perceptual span of Israeli readers
  extends in the direction of reading (to the left in Hebrew, to the right in English), so attention
  follows script direction. Classic lab study; old but foundational.
- NN/g horizontal-attention article 2010 states that usability studies in right-to-left countries showed
  attention to line beginnings on the right, but those Israeli studies did not use eye tracking. Verified.

**Strength:** B for left-to-right; C for Hebrew web pages (Arabic observed by NN/g, Hebrew web scanning
not eye-tracked in any source found).

**Phone 375x812:** "4 rooms, 112 m2, floor 18, south-west" beats "This spacious apartment offers...".
Labels start with the noun: "Monthly cost", "Purchase tax", "Delivery".

**Desktop 1440:** Same; lines in the panel stay under about 60 characters so the scan path is short.

**RTL:** In Hebrew and Arabic the first word sits at the right edge. A mixed line such as a project's
English name must not push the key Hebrew word away from the right start.

### R4. Headings carry the answer (the layer-cake reader)
**Rule:** Each section heading includes the key figure or verdict, so a reader who scans only headings
gets the summary ("Monthly cost about 9,800 NIS", "Shops below: supermarket, pharmacy").

**Evidence:**
- NN/g 2019 layer-cake pattern: users fixate mostly on headings and subheadings and read the body only
  under the heading that matches their need. Verified (illustrated with single-user examples).
- Baymard on vertical collapsed sections: each header on its own line gives more "information scent".
  Verified.

**Strength:** C (pattern well documented, sample sizes for this pattern not published).

**Phone 375x812:** Collapsed section headers show the number in the header row, so closed sections
still inform.

**Desktop 1440:** Same headers; sections may open by default on desktop where there is room.

**RTL:** The number appears after the Hebrew label in reading order; isolate it (see R33).

### R5. Serve the committed reader: full facts inside, legible
**Rule:** Do not cut tax details, delivery date, specification, legal status or fees "for a clean look";
keep them in the panel one tap deep, set in readable type (running text at least 16 CSS px on phones,
contrast at least 4.5:1).

**Evidence:**
- NN/g 2019 commitment pattern: highly motivated readers read nearly everything. Verified.
- Liechty and Madhavan 2011 (NASA NTRS conference paper, simulated real-estate site): experienced home
  buyers showed a more direct, refined visual search than novices; stated likes did not match gaze. Secondary.
- NN/g 2016 (Moran): comprehension on phones matched desktop for simple text, but people slow down on
  difficult text on mobile. Secondary (study summary).
- WCAG 2.x SC 1.4.3 contrast minimum 4.5:1 (standard). Apple's default body text is 17 pt and Material's
  body-large is 16 sp (platform guidance).

**Strength:** C.

**Phone 375x812:** Long items (purchase-tax brackets, payment schedule) live in collapsed sections of the
full state, not on a separate site.

**Desktop 1440:** Same content; tables may show inline.

**RTL:** Hebrew and Arabic glyphs look smaller than Latin at the same px size; choose faces on purpose
and test at 16 px.

### R6. Never make real information look like an advertisement
**Rule:** No banners, animated promos, boxed "special offer" strips or ad-shaped cards around facts or
actions in the panel.

**Evidence:** NN/g banner blindness: documented 1997, replicated 2007 and 2018 (Pernice, "Banner blindness
revisited", desktop and mobile). Users also skip legitimate content that looks ad-like; on mobile, large
stand-out graphics are sometimes mistaken for ads. Verified via summaries.

**Strength:** B (replicated over three decades).

**Phone 375x812:** Deals and incentives appear as plain rows in the price section with terms and date.

**Desktop 1440:** No right-rail or side "promo" box; on desktop RTL the left rail is the classic ad slot.

**RTL:** Same.

---

## B. Layout on each device

### R7. Phone: a non-modal sheet that grows into a real page
**Rule:** Open the cockpit as a non-modal bottom sheet over the live tower at peek and half heights; at
full height it becomes the apartment page (own URL, Back closes it, visible close button, swipe-down),
never a long transient overlay.

**Evidence:** NN/g 2023 (Laubheimer), "Bottom sheets": suited when users need the background context
(Google Maps place sheet is the non-modal example); support Back for dismissal; provide a visible close
button because swipe-to-dismiss is easy to miss; do not stack sheets; sheets are for short interactions
and "should not replace page-to-page flows, such as product-detail pages"; the claim that sheets improve
reachability is "largely incorrect". Verified. Apple HIG sheets support medium and large heights (detents).

**Strength:** C (expert guidance from NN/g usability studies; sample sizes not published).

**Phone 375x812:** Peek about 140 px, half about 450 px, full = 812 px minus the status bar. Tower
interactions stay live at peek and half; the full state pushes a history entry.

**Desktop 1440:** Not applicable (see R8).

**RTL:** Mirror the sheet header: the back arrow sits at the start corner (top-right in Hebrew and Arabic,
pointing right) and the close X at the opposite corner. Keep one convention in all five languages,
mirrored only by direction. Both corners are hard to reach (R12), so Back and swipe-down must also work.

### R8. Desktop: a docked side panel on the reading-start side, tower still live
**Rule:** On wide screens show the cockpit as a docked, non-modal side panel on the reading-start side,
leaving the 3D tower interactive beside it.

**Evidence:**
- NN/g 2010, "Horizontal attention leans left": 69% of viewing time on the left half, 30% on the right
  half, 1% beyond 1024 px (1024x768 monitor, left-to-right sites). A later NN/g video gives 80/20. The
  article says right-to-left users attend to line starts on the right, but layouts there are not always
  mirrored (it cites Haaretz with right-aligned text and a left navigation bar). Verified.
- Afsari, Ossandón and König 2016, Journal of Vision: image exploration starts with a bias toward the
  reading-start side; native right-to-left readers' bias shifts with what they just read, so bilingual
  Israeli users may flip between sessions. Secondary for the details.
- NN/g 2023: non-modal panels preserve context (Google Maps pattern). Verified.

**Strength:** B for left-to-right; C/D for the right-to-left mirror (inferred, plus one lab study).

**Phone 375x812:** Not applicable.

**Desktop 1440:** Panel 440 to 520 px on the right in Hebrew and Arabic, on the left in English, French
and Russian; tower canvas keeps the remaining 920 to 1000 px; clicking another apartment swaps panel
content without closing it.

**RTL:** This is the mirrored rule itself. Do not leave the panel on the right in the English version
just because the Hebrew one is there.

### R9. One vertical scroll with collapsible sections, not horizontal tabs
**Rule:** Put plan, view, price and deals, monthly cost, area, shops, video call and 360 as vertical,
collapsible sections in one scroll, with a section index, instead of horizontal tabs.

**Evidence:** Baymard Institute product-page testing: 27% of users overlooked content behind horizontal
tabs versus 8% for vertical collapsed sections; per-site overlook rates 18% (Sephora), 21% (Crutchfield),
43% (REI). On mobile, narrow screens hide some tabs entirely. Verified (summary page).

**Strength:** B (large qualitative testing program plus benchmark of hundreds of sites).

**Phone 375x812:** Full state is one scroll; each section header 48 to 56 px tall; first two sections
open by default (plan or view, then price).

**Desktop 1440:** Same order; more sections open by default because height allows.

**RTL:** Expand/collapse chevrons mirror; section order is identical in all languages.

### R10. Keep the section index visible, not behind a "more" button
**Rule:** Show the sections as a visible, horizontally scrollable index of chips under the panel header,
with at most 4 to 5 fully visible at once; never hide core sections in a hamburger or kebab menu.

**Evidence:**
- NN/g 2016 hidden-navigation study: 179 participants, 6 live sites, desktop and phone. Hidden navigation
  cut discoverability by more than 20%; on desktop hidden menus were used in 27% of cases versus 48%
  (visible) and 50% (combo); task time at least 39% slower on desktop and 15% slower on phones versus
  combo; difficulty 2.6 versus 2.1 on a 1 to 7 scale. Recommendation: show up to 4 top-level links
  visibly on mobile. Verified.
- Tab-bar versus hamburger reports (Facebook iOS; Redbooth +70% session time and +65% daily users;
  zeebox +8.7% daily frequency): anecdotes from companies, not peer reviewed. Grade D.

**Strength:** B (NN/g quantitative study); D for the company anecdotes.

**Phone 375x812:** Chips row 44 to 48 px tall, sticky under the header in the full state; the active chip
follows scroll position.

**Desktop 1440:** All 8 chips can fit in 480 px only as two rows or short labels; prefer a vertical
index on the panel's outer edge if labels are long in French or Russian.

**RTL:** Chip row starts at the right edge and scrolls leftward in Hebrew and Arabic.

### R11. One layer at a time; heavy media opens as a full-screen mode with a clear exit
**Rule:** 360 inside, video call, full-screen plan and the view simulator open as a full-screen mode with
a visible exit and Back support, never as a sheet stacked on the cockpit sheet.

**Evidence:** NN/g 2023: stacked sheets make users track their position and confuse "close this" with
"close all". Verified.

**Strength:** C.

**Phone 375x812:** Exit button at least 48 px in the top start corner plus Back gesture.

**Desktop 1440:** Modes open inside the tower area (the panel stays), Escape exits.

**RTL:** Exit arrow points to the start side (right in Hebrew and Arabic).

---

## C. Thumb and touch

### R12. Actions live in the middle-to-lower band, not in corners
**Rule:** Place frequent actions in the middle and lower part of the screen; reserve corners and the top
strip for rare, forgiving actions, and make anything you must put there bigger.

**Evidence:**
- Hoober 2013 (UXmatters): 1,333 street observations; of people touching the screen, 49% one-handed,
  36% cradled, 15% two-handed; grips change constantly. Not claimed as scientific. Secondary
  (UXmatters returned HTTP 522 on 10.11.2026; figures via Roselli 2013 and Osmani 2020).
- Hoober 2017, "Design for fingers, touch, and people": people prefer to look at and touch the center;
  touch accuracy about 7 mm at the center, 9 mm at edges, 12 mm in corners. Secondary.
- NN/g 2023: "the middle of the screen represents the most easily tappable area" across grips. Verified.
- Eardley, Roudaut, Gill and Thompson, CHI 2017: on larger phones, reaching distant targets forces grip
  shifts, tilting and rotating the phone. Verified (abstract). Le, Mayer, Bader and Henze, CHI 2018: the
  grip moves toward the top edge as phone size grows. Verified (abstract).
- Bergstrom-Lehtovirta and Oulasvirta, CHI 2014: the reachable thumb area depends on screen size, hand
  size and grip; model fitted to 20 participants. Verified (abstract).

**Strength:** B (observation plus lab studies agree on "center good, corners bad"; the classic
thumb-zone heat map is a simplification Hoober himself later called wrong).

**Phone 375x812:** Primary action centered in the lower third (or a full-width bar at the bottom of the
full state); the tower's floor picker and apartment taps happen in the middle band.

**Desktop 1440:** Not a thumb problem; use Fitts's law instead: the primary action sits in the panel
header, close to where the eye already is.

**RTL:** See R13.

### R13. Mirror the reading, not the hand
**Rule:** Right-to-left changes reading direction, not handedness: keep primary actions reachable for a
right thumb and a left thumb alike (centered or full-width), in every language.

**Evidence:**
- Hoober 2013: of one-handed users, 67% used the right thumb and 33% the left. Secondary.
- Papadatou-Pastou and colleagues 2020, Psychological Bulletin meta-analysis (about 2.4 million people):
  left-handedness about 10.6% by the most common definition (9.3% to 18.1% depending on definition).

**Strength:** B.

**Phone 375x812:** Do not move the primary button to the right edge in Hebrew "because it is the start";
center it or make it full-width. Secondary actions may sit at the start side.

**Desktop 1440:** Not applicable.

**RTL:** This is the rule. A mirrored layout with a right-edge primary button disadvantages the
one-third of one-handed users who use the left thumb.

### R14. Targets at least 44 x 44 CSS px, never under 24, bigger at edges and corners
**Rule:** Every tappable element has a hit area of at least 44 x 44 CSS px (48 preferred); nothing is
under 24 x 24; edge and corner targets are 55 to 72 px (9 to 12 mm).

**Evidence:**
- WCAG 2.2 SC 2.5.8 (AA): at least 24 x 24 CSS px or 24 px spacing; inline links exempt. SC 2.5.5 (AAA):
  44 x 44. Apple HIG: 44 x 44 pt. Material: 48 x 48 dp. Standards.
- Parhi, Karlson and Bederson, MobileHCI 2006: one-handed thumb targets of 9.2 mm (single taps) and
  9.6 mm (sequences) were sufficient; smaller raised errors. Verified (abstract).
- Hoober 2017 accuracy by region (7 / 9 / 12 mm). Secondary.

**Strength:** A/C (standards plus repeated lab findings that converge on about 9 to 10 mm).

**Phone 375x812:** 44 px = about 7.3 mm; 55 px = 9.2 mm; 72 px = 12 mm. Floor and apartment hit areas in
the tower need invisible enlarged hit zones (at least 44 px) even when the drawn window is smaller.

**Desktop 1440:** Mouse targets may be smaller, but keep 32 px minimum and 44 px for touch laptops.

**RTL:** No difference.

### R15. Space adjacent targets; isolate actions that cannot be undone
**Rule:** Keep at least 8 px between adjacent targets, and keep sending, booking or deleting away from
other controls.

**Evidence:** WCAG 2.5.8 spacing exception (24 px circles must not overlap). Hoober 2017 advises keeping
risky controls such as "send" away from neighbours because some people still miss at these accuracies.
Secondary.

**Strength:** C.

**Phone 375x812:** "Book a visit" and "Video call" never touch; a lead form submit button stands alone.

**Desktop 1440:** Same.

**RTL:** No difference.

### R16. No gesture traps inside the sheet
**Rule:** A 3D view, 360 view or map embedded in the scrolling panel must not capture a vertical swipe;
the user enters an explicit "explore" mode, or the embed needs two fingers.

**Evidence:** Google Maps JavaScript API "cooperative" gesture handling exists for this reason (one-finger
swipes scroll the page, two fingers pan the map). Platform guidance; no controlled study was found.

**Strength:** D (practice and platform documentation only).

**Phone 375x812:** Embedded previews are static images or inert canvases with "Explore 360" and "Open
view" buttons; touch-action: pan-y until the mode is entered.

**Desktop 1440:** Mouse wheel over an embed scrolls the panel unless the user clicked into the embed.

**RTL:** No difference.

---

## D. Choices and structure

### R17. Show four or five top-level choices at a time; disclose the rest progressively
**Rule:** The first screen offers at most 4 to 5 top-level choices (sections or modes); further options
appear only after the user opens a section.

**Evidence:**
- Hick 1952 and Hyman 1953: choice reaction time grows with the logarithm of the number of equally
  likely alternatives. Robust for simple choices. In menus, novices search linearly and only experts
  approach the Hick-Hyman curve (Cockburn, Gutwin and Greenberg, CHI 2007).
- Cowan 2001, Behavioral and Brain Sciences: working memory holds about 4 chunks (not Miller's 7).
- NN/g 2006, progressive disclosure (expert guidance) and NN/g 2016 "up to 4 visible links" on mobile.

**Strength:** B for the laws themselves; C for the exact UI threshold, which is an inference.

**Phone 375x812:** Half state: plan or view switch (2 to 3 options), one primary action, one secondary,
the chip index. Not 8 equal buttons.

**Desktop 1440:** Same limit for buttons; the chip index can show more because it is navigation, not
decision.

**RTL:** No difference.

### R18. Curate comparisons: two or three similar apartments, not the whole tower
**Rule:** Inside the cockpit, compare the apartment with two or three similar ones (same rooms, nearby
floors or lines), not with a list of every unit.

**Evidence:**
- Iyengar and Lepper 2000 (24 versus 6 jams, 3% versus 30% bought) started the field.
- Scheibehenne, Greifeneder and Todd 2010, Journal of Consumer Research meta-analysis: 50 experiments,
  N = 5,036, mean effect "virtually zero" with large variance. Verified (abstract).
- Chernev, Böckenholt and Goodman 2015, Journal of Consumer Psychology meta-analysis: 99 observations,
  N = 7,202; overload appears when the set is complex, the task is difficult, preferences are uncertain
  and the person wants to minimise effort. McShane and Böckenholt 2018 re-analysis: the effect can
  reverse when those moderators are low. Verified (abstracts).

**Strength:** B but contested. An apartment purchase hits all four amplifiers, so curation is the safer
prior here.

**Phone 375x812:** A "Similar in this building" row of 2 to 3 cards with one differing fact highlighted
(floor, view, price per m2).

**Desktop 1440:** Same, side by side; a full unit table belongs to the project page, not the cockpit.

**RTL:** Card order starts at the right edge.

### R19. One primary action, at most one secondary; the video call is secondary until tested
**Rule:** Each state shows one primary action and at most one secondary; on the phone's full state they
live in a slim bottom bar that appears once the in-flow buttons leave the screen.

**Evidence:**
- Hick-Hyman and Cowan (see R17).
- Sticky call-to-action tests are vendor reports: Conversion Rate Experts (long mobile page for a
  high-priced product, +8% minimum and +25% best variant); Cleancommit (AFTCO, +6.2% mobile conversion,
  -2.5% order value; a persistent bar helped mobile but hurt desktop). Grade D.
- NN/g on sticky headers: partially persistent headers on mobile "work moderately well"; oversized sticky
  bars eat the screen. Murano and Kongshaug 2024 (24 participants, 13-inch laptop): persistent headers
  improved performance and satisfaction; phones out of scope. Secondary.
- Live video calls for property sales: no controlled evidence found.

**Strength:** C/D.

**Phone 375x812:** Bar height at most about 88 px including the safe area (about 11% of 812); primary
button full-width or two equal halves; it never covers a focused input.

**Desktop 1440:** Primary action in the sticky panel header; no floating bar.

**RTL:** In a two-button bar the primary sits on the start side (right) in Hebrew and Arabic, and both
halves are equal width so the left thumb is not penalised (R13).

### R20. Calculator defaults are decisions; make them real and visible
**Rule:** Start the monthly-cost and mortgage calculator from values that are legal and typical today
(for example the Bank of Israel caps: financing up to 75% for a single home, 70% for upgraders, 50% for
investors; repayment up to 50% of income), show every assumption, and let the buyer change it.

**Evidence:** Jachimowicz, Duncan, Weber and Johnson 2019, Behavioural Public Policy meta-analysis:
58 studies, N = 73,675, average default effect d = 0.68 (95% CI 0.53 to 0.83), stronger in consumer
domains, very heterogeneous. Verified (abstract). Bank of Israel caps as used by nad-lan's own mortgage
pages (docs/research/2026-11-09-mortgage-proof); re-check before each release.

**Strength:** A for the default effect; the specific values are regulatory facts that change.

**Phone 375x812:** Defaults shown as editable chips ("25% equity", "25 years", "prime + mix") above the
result, numeric keyboard on edit.

**Desktop 1440:** Same, with sliders allowed (slider thumbs at least 44 px).

**RTL:** Slider direction: decide once whether "more" goes left or right in Hebrew and keep it across the
site; label both ends with numbers.

---

## E. Price, cost and honest persuasion

### R21. All-in price on first view; no late surprises
**Rule:** Show the total price including VAT and every mandatory charge on first view; the one-time costs
(purchase tax, lawyer, fees) and the monthly cost are one glance away in the same section, never revealed
later in a flow.

**Evidence:**
- Israeli Consumer Protection Law sections 17A to 17B (Amendment 11, 2002): the "total price" a dealer
  displays includes VAT and all mandatory payments. The Consumer Protection and Fair Trade Authority acted
  against Booking.com, which agreed to show VAT-inclusive prices from 1 July 2023. Secondary (Knesset
  amendment text and press). VAT is 18% since January 2025.
- Blake, Moshary, Sweeney and Tadelis 2021, Marketing Science 40(4): StubHub randomised half of US users
  to back-end (late) fees; hidden fees raised spending (about 21% revenue in a summary) by obscuring the
  price. This is evidence that drip pricing works through deception, not that it is acceptable. Secondary
  for the exact percentage.
- US FTC rule on unfair or deceptive fees (effective 12 May 2025) and Airbnb's switch to total-price
  display worldwide (April 2025, after about 17 million guests had used its total-price toggle).
- Brown, Imai, Vieider and Camerer 2024, Journal of Economic Literature meta-analysis of loss aversion:
  607 estimates, mean coefficient 1.955 (95% interval 1.82 to 2.10). Costs that appear late are felt as
  losses about twice as strongly as equal gains. Verified (abstract).

**Strength:** A (law plus a large field experiment plus a meta-analysis).

**Phone 375x812:** Peek and half states show the total price incl. VAT; the price section shows three
lines: total price, one-time costs (sum with a breakdown link), monthly cost (sum with assumptions).

**Desktop 1440:** Same three lines in the panel header area or first section.

**RTL:** Currency sign position follows the locale formatter (Hebrew usually "3,450,000 ₪"); the number
is isolated (R33).

### R22. Anchors must be real: show dated deals next to the asking price
**Rule:** The first price figure anchors the buyer's sense of value, so place the asking price beside real
reference points (closed deals nearby with date and source, price per m2, the building's own price list
history), and never invent a "was" price.

**Evidence:**
- Northcraft and Neale 1987, Organizational Behavior and Human Decision Processes: estate agents and
  students valued the same house differently depending on the list price shown; agents denied using it.
- Bucchianeri and Minson 2013, Journal of Economic Behavior and Organization: more than 14,000
  transactions; higher list prices go with higher sale prices; the abstract states that 10 to 20%
  over-pricing goes with a sale price increase of "$117 to $163" for the average home, a small effect.
  Verified (abstract).
- Klein and colleagues 2014 (Many Labs 1): anchoring replicated robustly across labs.
- Thomas, Simon and Kadiyali 2010, Marketing Science: buyers judge precise prices as smaller than round
  ones; precise list prices went with higher sale prices in two housing markets. Verified (abstract).
- Israeli Consumer Protection Law section 2(a): misleading about the "ordinary or normal price or the
  price charged in the past" is prohibited. Verified (WIPO Lex English text).

**Strength:** A for anchoring in the lab; B for real-estate field data, where the effect is small.

**Phone 375x812:** Under the price: "Price per m2 X; 3 deals within 300 m in the last 12 months: A, B, C
(source: Tax Authority, date)". Tap opens the deals list.

**Desktop 1440:** Same plus a small dated dot chart of deals.

**RTL:** Charts keep time left to right in Hebrew, as nad-lan's mortgage charts and the Bank of Israel do;
see R33 for the conflict with platform guidance.

### R23. Show the monthly figure beside the total, with assumptions, never alone
**Rule:** Present the monthly cost (mortgage payment, arnona, building committee fee, insurance) next to
the total price, with the rate, term and date it assumes; never advertise only a small monthly number.

**Evidence:**
- Gourville 1998, Journal of Consumer Research ("pennies-a-day"): reframing a cost as a small per-period
  amount makes it feel smaller and raises acceptance.
- Morwitz, Greenleaf and Johnson 1998, Journal of Marketing Research: partitioned prices lower the total
  that buyers recall and can raise demand.
- Israeli section 2 (material matters include credit terms and interest). Verified (WIPO Lex).

**Strength:** B (lab and field replications in pricing research); legal duty is clear.

**Phone 375x812:** One line: "About 9,800 NIS a month (mortgage 7,900 + arnona 650 + committee 450 +
insurance 800), assumes 25% equity, 25 years, rates of [month]".

**Desktop 1440:** Same, with an editable breakdown.

**RTL:** The plus signs and numbers are one isolated LTR run.

### R24. Scarcity and social proof only when true, specific, dated and sourced
**Rule:** Show "sold" and "remaining" counts, deadlines or demand only when they are live facts with a
source and timestamp; no countdown timers, no "people are viewing now", no "last apartment" unless it is.

**Evidence:**
- Barton, Zlatevska and Oppewal 2022, Journal of Retailing meta-analysis: 416 effect sizes from 131
  studies; scarcity cues raise purchase intentions; time-based scarcity works best for high-involvement
  products. Verified (abstract). The cue is effective, which is exactly why it is regulated.
- Mathur and colleagues 2019 (CSCW), crawl of about 53,000 product pages on about 11,000 shopping sites:
  1,818 dark-pattern instances on 1,254 sites, including fake countdowns and activity messages; 234
  outright deceptive instances on 183 sites. Verified (abstract).
- UK Competition and Markets Authority 2019: Booking.com, Expedia, Agoda, Hotels.com, ebookers and trivago
  committed to stop false or misleading popularity and availability messages; a Which? audit then found
  "1 room left" while 34 rooms were available. Verified (press).
- EU Unfair Commercial Practices Directive, Annex I point 7: falsely stating that a product is available
  only for a very limited time is banned outright.
- Israel: Consumer Protection Law section 2 (misleading), section 3 (exploiting inexperience, undue
  influence), section 7 (misleading advertisements; the Commissioner may demand substantiation, and
  failure is prima facie misleading). Amendment 39 added administrative fines; the Authority announced an
  intended fine of about 1.9 million NIS against Gindi Holdings over a project advertising campaign.
  Secondary (press).
- Social proof is weaker than its reputation: the hotel-towel norm study (Goldstein and colleagues 2008)
  failed a direct replication (Bohner and Schlüter 2014); a Bayesian synthesis of 7 studies (Scheibehenne,
  Jamil and Wagenmakers 2016) supported a small effect, and a re-analysis found only weak evidence.

**Strength:** A for legal risk; B for the size of the persuasion effect.

**Phone 375x812:** "31 of 120 apartments sold, updated 10.11.2026" as plain text in the project block,
not a red badge. No timers anywhere.

**Desktop 1440:** Same.

**RTL:** Same rule in all five languages; a pressure line translated into Russian or Arabic is still the
same legal exposure in Israel.

### R25. Label every render, staging and AI image; show the real view when it exists
**Rule:** Every visual that is not a photograph of this apartment as it is (renders, virtual staging,
AI-generated interiors, simulated views) carries a visible label; where the floor exists or a drone shot
at that height exists, show the real view.

**Evidence:**
- Israeli Consumer Protection Law sections 2 and 7 (misleading by act, omission or advertisement). Legal
  inference; no Israeli ruling on render labels was found in this research.
- View is a material price driver: Benson, Hansen, Schwartz and Smersh 1998, Journal of Real Estate
  Finance and Economics: high-quality ocean views added almost 60% to otherwise comparable single-family
  homes, low-quality views about 8%. Verified (abstract). A wrong view is therefore a misrepresentation
  of something buyers pay for.

**Strength:** C (legal inference plus hedonic-price evidence).

**Phone 375x812:** A small persistent label inside the image corner ("Render" / "הדמיה"), not only in
alt text; view images state floor and direction.

**Desktop 1440:** Same.

**RTL:** Label at the image's start-top corner.

---

## F. Media inside the cockpit

### R26. The floor plan is never more than one tap away
**Rule:** The floor plan is in the first screen or one tap from it, zoomable, with room dimensions,
north arrow and the apartment's position in the floor.

**Evidence:**
- Rightmove buyer survey (UK, about 10,000 respondents, date not given): 37% less likely to enquire
  without a floor plan, about 1 in 5 would ignore the listing, 1 in 10 would never book a viewing
  without one. Grade D (survey by a portal that sells floor plans).
- Strike (UK agent) 2021 eye-tracking: buyers sought floor plans quickly after arriving. Grade D.
- Zillow (vendor data): listings with an interactive floor plan received 49% more saves than similar
  nearby listings. Observational, selection-biased. Grade D.

**Strength:** D individually, consistent in direction. For off-plan sales the plan is the product, so the
prior is strong even though the studies are weak.

**Phone 375x812:** Plan is the default visual for apartments not yet built; pinch-zoom inside a
full-screen plan mode (R11).

**Desktop 1440:** Plan fills the panel visual slot; hover shows room sizes.

**RTL:** Do not mirror the plan; it is a map of the real world. Mirror only the UI around it.

### R27. 3D, 360 and video are screening tools: offer them, never autoplay, never block the first view
**Rule:** Offer the 360 tour, video and video call as explicit choices loaded on demand; do not autoplay
them or load them before the apartment's first view is on screen.

**Evidence (mixed on price, positive on screening speed):**
- Troncoso and Zhang (Harvard Business School, reported December 2023): 75,178 Los Angeles home sales,
  March 2019 to March 2021, about 22% with 3D tours; after controlling for photo and description quality
  the price effect was not significant (about 1.1% without controls); tours may lengthen time on market;
  they helped while in-person viewing was restricted. Verified (summary).
- Meng and colleagues 2025, Information Systems Research: about 43,000 listings on China's largest
  platform; VR tours cut average days on market from 34 to 19 with no effect on price; larger and newer
  homes benefited most. Verified (university release).
- Yu, Ma, Pant and Hu 2021 (Orange County): virtual tours went with at least 2% higher price and 6% longer
  time on market. Secondary.
- Zillow 3D Home data: 10% to 14% faster sales and 32% to 55% more saves (different periods), observational
  and vendor-published. Grade D.

**Strength:** B (several large observational studies; causality limited by which sellers choose tours).

**Phone 375x812:** "Explore 360" and "Video call" buttons in their own sections; tapping opens a
full-screen mode; nothing streams on the cockpit's first paint.

**Desktop 1440:** 360 opens in the tower area beside the panel.

**RTL:** Media playback controls are not mirrored (Material bidirectionality guidance).

### R28. Galleries: swipe with a visible count on phones, thumbnails on desktop
**Rule:** On phones, a swipeable full-width gallery with a "3 / 12" counter; on desktop, visible
thumbnails. Dots alone are not enough.

**Evidence:** Baymard benchmark: 100% of desktop sites use thumbnails but only 24% of mobile sites; mobile
users almost always swipe and use dots only as a fallback; dots are too small to tap reliably. Verified.

**Strength:** B.

**Phone 375x812:** Counter at the image's bottom start corner; swipe area at least the full image.

**Desktop 1440:** Thumbnail strip under the main visual, each thumbnail at least 56 px.

**RTL:** In Hebrew and Arabic the next image comes from the left (the user swipes toward the right);
verify the carousel library honours dir="rtl".

---

## G. Speed

### R29. Show the apartment within 2.5 seconds on a mid-range phone; the 3D model comes after
**Rule:** The tower page and the cockpit's first view render a static poster and the apartment's visual
first (Largest Contentful Paint at or under 2.5 s at the 75th percentile), then stream the 3D model.

**Evidence:**
- Bing controlled slowdown (Kohavi and colleagues; 10% of users slowed by 100 ms and 10% by 250 ms for two
  weeks): each 100 ms cost about 0.6% revenue. Grade A. Secondary for the exact wording.
- Booking.com, Bernardi, Mavridis and Estevez, KDD 2019 ("150 successful machine learning models"):
  a controlled experiment adding synthetic latency; about 30% more latency cost more than 0.5% conversion.
  Grade A. Secondary (summary of the paper).
- Google/SOASTA 2017: as mobile load time goes from 1 s to 3 s, the probability of bounce rises 32%.
  Model-based, Google-published. Verified.
- Deloitte for Google 2020 ("Milliseconds make millions"): 37 brands, 4 weeks; a 0.1 s mobile speed gain
  across the journey went with +8.4% retail and +10.1% travel conversions. Correlational. Verified.
- Core Web Vitals "good" thresholds at the 75th percentile: LCP 2.5 s, INP 200 ms, CLS 0.1 (web.dev).

**Strength:** A.

**Phone 375x812:** First paint = tower poster image (compressed WebP/AVIF) and the cockpit text; glTF
geometry, textures and 360 panoramas load after first interaction or idle time.

**Desktop 1440:** Same budget; desktops forgive more bytes, not more blocking.

**RTL:** Hebrew and Arabic web fonts are large; subset them and use font-display: swap.

### R30. A tap answers within 100 ms and finishes within 200 ms
**Rule:** Tapping an apartment gives visible feedback within 100 ms (highlight, sheet starts moving) and
the cockpit's first view is complete within 200 ms (INP "good").

**Evidence:** Response-time limits 0.1 s (feels instant), 1 s (keeps flow), 10 s (keeps attention):
Miller 1968, Card, Robertson and Mackinlay 1991, Nielsen 1993. INP "good" at 200 ms (web.dev standard).

**Strength:** B (classic and stable human-factors thresholds) plus standard.

**Phone 375x812:** Pre-load the apartment's text data with the tower; images for that unit start loading
on tap-down, not on tap-up.

**Desktop 1440:** Prefetch on hover.

**RTL:** No difference.

### R31. Nothing jumps
**Rule:** Reserve space for every image, price and badge so the panel never shifts under the thumb
(Cumulative Layout Shift at or under 0.1).

**Evidence:** Core Web Vitals CLS threshold 0.1 (web.dev). Mis-taps after shifts follow directly from the
accuracy limits in R12 and R14. Standard plus inference.

**Strength:** C.

**Phone 375x812:** Fixed aspect-ratio boxes for visuals; price line has a reserved height before data
arrives.

**Desktop 1440:** Same.

**RTL:** Late-loading web fonts can re-flow Hebrew lines; match fallback metrics (size-adjust).

### R32. Loading states: real content first; skeletons are optional, progress for long waits
**Rule:** Show real content progressively; use a skeleton only for waits under about 1 s if a local test
favours it; show progress for anything over 1 s and a percentage or steps for anything near 10 s (the 3D
model, the 360 panorama).

**Evidence:** Evidence on skeleton screens conflicts: Viget 2017 (136 mobile participants) found skeleton
screens worst on perceived wait (2.82 s versus 2.41 s spinner and 2.29 s blank); Mejtoft, Långström and
Söderström 2018 (ECCE) found skeletons better on perceived speed. Secondary. Response-time limits as in R30.

**Strength:** C (mixed).

**Phone 375x812:** "Loading the view from floor 18, 60%" beats a spinning logo.

**Desktop 1440:** Same.

**RTL:** Progress bars fill from the start side (right in Hebrew and Arabic).

---

## H. Languages and direction

### R33. Numbers are islands of left-to-right; isolate them
**Rule:** Wrap every price, area, floor, room count, date range, phone number and percentage in an
isolated left-to-right run (bdi, dir="ltr" or unicode-bidi: isolate) and format with the locale's
Intl.NumberFormat; in Hebrew charts keep time running left to right.

**Evidence:** Unicode Bidirectional Algorithm (UAX 9) and W3C internationalisation guidance on inline
bidirectional text (standards): without isolation, ranges such as "3-4", signed numbers and phone numbers
reorder visually. Material and Wikimedia Codex: do not mirror numbers or phone numbers. Material says
linear time is mirrored in right-to-left, but Israeli financial charts (Bank of Israel, nad-lan's own
mortgage block) run time left to right; local convention wins for Hebrew, and Arabic needs its own test.

**Strength:** C (standards plus convention); the chart direction is a known conflict.

**Phone 375x812:** "3,450,000 ₪", "112 m2", "4.5 rooms", "054-1234567" each in their own isolate.

**Desktop 1440:** Same.

**RTL:** For Arabic, decide Western or Arabic-Indic digits once (Israeli Arabic sites mostly use Western
digits) and set numberingSystem explicitly.

### R34. Design for longer text and five scripts
**Rule:** Leave room for French and Russian labels to run much longer than Hebrew (short labels can double
or triple; long text grows about 30%), never fix button widths, and test every state in all five languages.

**Evidence:** W3C internationalisation article "Text size in translation", quoting IBM averages for
English into European languages: strings up to 10 characters reach 200% to 300% of the source length,
strings over 70 characters about 130%. Verified. Hebrew source text is usually shorter than English, so
expansion from Hebrew is likely larger (inference).

**Strength:** C.

**Phone 375x812:** Chip labels and button text wrap to two lines rather than truncate; the bottom bar
height is computed, not fixed.

**Desktop 1440:** Panel width chosen for the longest language (usually Russian or French).

**RTL:** Arabic needs taller line height than Hebrew for diacritics and ascenders.

### R35. Mirror the interface, not the world
**Rule:** In Hebrew and Arabic mirror direction-bearing interface elements (back arrows, gallery order,
progress, chip rows, steppers), but never mirror the world: floor plans, compass, the 3D tower's
orientation, maps, clocks and media playback.

**Evidence:** Material Design bidirectionality guidance (mirror back and forward and linear progress; do
not mirror circular time or media playback), Apple HIG right-to-left guidance, Wikimedia Codex (numbers
and phone numbers stay). Afsari and colleagues 2016: bilingual readers' visual scan direction adapts to
what they just read, so mixed-language sessions need consistent cues. Standards plus one lab study.

**Strength:** C.

**Phone 375x812:** The sheet's back arrow points right in Hebrew; the tower's north stays north.

**Desktop 1440:** Panel side flips (R8); the tower view does not.

**RTL:** This rule is RTL.

---

## I. Method

### R36. Every rule here is a prior; test it on our own traffic
**Rule:** Ship changes behind an experiment or a before-and-after with a pre-declared metric (leads per
cockpit open, plan opens, time to first meaningful action), and expect most ideas not to win.

**Evidence:** Kohavi and colleagues 2009 ("Online experimentation at Microsoft"): only about one third of
ideas improved the metric they were designed to improve; Kohavi, Tang and Xu 2020, "Trustworthy online
controlled experiments" (Cambridge University Press). Thomke 2020 (Harvard Business Review, "Experimentation
works"): Booking.com runs about 25,000 tests a year, about 1,000 at once.

**Strength:** A (as a method).

**Phone 375x812:** Measure phone and desktop separately; Cleancommit's sticky-bar test (R19) helped one
and hurt the other.

**Desktop 1440:** Same.

**RTL:** Segment results by language; Hebrew and Arabic users may react differently from English users
to the same mirrored layout.

---

## Where the evidence is thin (read before you cite)

- **Hebrew web eye tracking:** no eye-tracking study of Hebrew web pages was found. Mirroring rests on NN/g's
  Arabic observations, Hebrew reading research (Pollatsek 1981) and one image-scanning lab study (Afsari 2016).
- **Mobile attention above the fold:** NN/g's 57% and 74% figures are desktop (1920x1080). No mobile
  equivalent with numbers was found.
- **Thumb zones:** Hoober's 2013 and 2017 figures are observational and were read through secondary summaries
  (UXmatters was down). The popular thumb-zone heat map is a simplification its sources now reject.
- **Bottom sheets for detail pages:** NN/g advises against using a sheet as a product-detail page; R7
  reconciles this by turning the full state into a real page.
- **Sticky action bars, video calls, floor plans and virtual staging:** vendor tests, portal surveys or
  nothing. No peer-reviewed study of live video calls in property sales was found.
- **3D and VR tours:** large observational studies disagree on price; they agree that tours help screening.
- **Choice overload:** two meta-analyses disagree; the rule relies on the moderators.
- **Israeli law:** the provisions cited are real, but no ruling was found on render labels or on urgency
  messages in real estate; confirm with counsel before publishing persuasion copy.
- **Old studies:** Hick (1952), Northcraft and Neale (1987), Benson (1998), the NN/g horizontal attention
  study (2010) and the real-estate eye-tracking work (2011 to 2013) predate current phones.

## Sources (opened or searched on 10.11.2026)

- NN/g, Scrolling and attention (2018): https://www.nngroup.com/articles/scrolling-and-attention/
- NN/g, F-shaped pattern (2017): https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/
- NN/g, Text scanning patterns (2019): https://www.nngroup.com/articles/text-scanning-patterns-eyetracking/
- NN/g, Horizontal attention leans left (2010): https://www.nngroup.com/articles/horizontal-attention-original-research/
- NN/g, Hamburger menus and hidden navigation (2016): https://www.nngroup.com/articles/hamburger-menus/
- NN/g, Bottom sheets (2023): https://www.nngroup.com/articles/bottom-sheet/
- NN/g, Photos as web content (2010): https://www.nngroup.com/articles/photos-as-web-content/
- NN/g, Sticky headers: https://www.nngroup.com/articles/sticky-headers/
- NN/g, Mobile content comprehension (2016): https://www.nngroup.com/articles/mobile-content/
- Seiler, Madhavan, Liechty 2012, JRER: https://econpapers.repec.org/RePEc:jre:issued:v:34:n:2:2012:p:211-242
- Liechty, Madhavan 2011: https://ntrs.nasa.gov/citations/20110012067
- Baymard, horizontal tabs: https://baymard.com/blog/avoid-horizontal-tabs
- Baymard, thumbnails: https://baymard.com/blog/always-use-thumbnails-additional-images
- Baymard, UX statistics: https://baymard.com/learn/UX-statistics
- Zhang et al. 2022, Airbnb images: https://pubsonline.informs.org/doi/10.1287/mnsc.2021.4175
- Hoober 2013: https://www.uxmatters.com/mt/archives/2013/02/how-do-users-really-hold-mobile-devices.php
- Hoober 2017: https://www.uxmatters.com/mt/archives/2017/07/design-for-fingers-touch-and-people-part-3.php
- Osmani, touch-friendly design: https://addyosmani.com/blog/touch-friendly-design/
- Eardley et al. CHI 2017: https://core.ac.uk/download/145642744.pdf
- Le et al. CHI 2018: https://www.medien.informatik.uni-muenchen.de/pubdb/publications/pub/le2018fingersrange/le2018fingersrange.pdf
- Bergstrom-Lehtovirta, Oulasvirta CHI 2014: https://researchr.org/publication/Bergstrom-LehtovirtaO14
- Parhi, Karlson, Bederson 2006: https://www.microsoft.com/en-us/research/?p=155150
- WCAG 2.2 target size: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- Scheibehenne et al. 2010: https://ideas.repec.org/a/oup/jconrs/v37y2010i3p409-425.html
- Chernev et al. 2015: https://www.kellogg.northwestern.edu/faculty/research/detail/2015/when-product-assortment-leads-to-choice-overload-a-conceptual/
- Jachimowicz et al. 2019: https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html
- Bucchianeri, Minson 2013: https://www.hks.harvard.edu/publications/homeowners-dilemma-anchoring-residential-real-estate-transactions
- Thomas, Simon, Kadiyali 2010: https://econpapers.repec.org/RePEc:inm:ormksc:v:29:y:2010:i:1:p:175-190
- Blake et al. 2021, StubHub: https://www.nber.org/papers/w25186.pdf
- Brown et al. 2024, loss aversion: https://www.aeaweb.org/doi/10.1257/jel.20221698
- Barton et al. 2022, scarcity: https://research.monash.edu/en/publications/scarcity-tactics-in-marketing-a-meta-analysis-of-product-scarcity/
- Mathur et al. 2019: https://arxiv.org/abs/1907.07032
- CMA 2019 hotel booking commitments: https://www.gov.uk/government/news/hotel-booking-sites-to-make-major-changes-after-cma-probe
- Which? 2019 follow-up: https://www.which.co.uk/news/2019/09/booking-com-still-misleading-holidaymakers-with-1-room-left-claims/
- Israeli Consumer Protection Law (English, WIPO Lex): https://www.wipo.int/wipolex/en/text/128083
- Amendment 11 (total price, 2002): https://fs.knesset.gov.il/15/law/15_lsr_300479.pdf
- Gindi intended fine (Walla): https://finance.walla.co.il/item/2847463
- Authority summary of OECD dark patterns (2023): https://www.gov.il/BlobFolder/dynamiccollectorresultitem/cfta_darkpatternsreaserch/he/OECD%20-%20%D7%93%D7%A4%D7%95%D7%A1%D7%99%D7%9D%20%D7%90%D7%A4%D7%9C%D7%99%D7%9D.pdf
- Airbnb total price 2025: https://skift.com/2025/04/21/airbnb-makes-total-price-display-standard-on-listings-worldwide/
- Scheibehenne, Jamil, Wagenmakers 2016 and critique: https://www.frontiersin.org/articles/10.3389/fams.2017.00012/full
- Benson et al. 1998, value of a view: https://ideas.repec.org/a/kap/jrefec/v16y1998i1p55-73.html
- Rightmove floor plans: https://www.rightmove.co.uk/news/articles/property-news/maximise-chances-finding-buyer-floorplan/
- Strike eye tracking 2021: https://www.realhomes.com/news/eyetracking-study-reveals-home-features-buyers-want
- Zillow 3D Home: https://www.zillow.com/learn/virtual-tours-home-sell-faster
- Troncoso, Zhang (HBS WK 2023): https://www.library.hbs.edu/working-knowledge/are-virtual-tours-still-worth-it-in-real-estate-evidence-from-75000-home-sales
- Meng et al. 2025 (UT Dallas release): https://news.utdallas.edu/business-management/virtual-reality-tours-real-estate-2025
- Yu et al. 2021: https://ideas.repec.org/a/taf/rjelxx/v28y2021i2p133-149.html
- Bernardi et al. 2019 (summary): https://blog.acolyer.org/2019/10/07/150-successful-machine-learning-models/
- Bing slowdown (Kohavi rules of thumb): https://blog.acolyer.org/2017/09/26/seven-rules-of-thumb-for-web-site-experimenters/
- Google/SOASTA 2017: https://www.thinkwithgoogle.com/data/page-load-time-statistics/
- Deloitte 2020: https://web.dev/case-studies/milliseconds-make-millions
- Core Web Vitals thresholds: https://web.dev/articles/defining-core-web-vitals-thresholds
- Viget skeleton test 2017: https://www.viget.com/articles/a-bone-to-pick-with-skeleton-screens/
- NN/g skeleton screens (cites Mejtoft 2018): https://www.nngroup.com/articles/skeleton-screens/
- Conversion Rate Experts sticky CTA: https://conversion-rate-experts.com/sticky-cta-win-report/
- Cleancommit sticky tests: https://cleancommit.io/ab-tests/sticky-mobile-add-to-cart-button/
- Material bidirectionality: https://m2.material.io/go/design-bidirectionality
- W3C text size in translation: https://www.w3.org/International/articles/article-text-size
- Afsari et al. 2016: https://doi.org/10.1167/16.11.8
- Thomke 2020, Booking.com: https://hbswk.hbs.edu/item/at-booking-com-innovation-means-constant-failure
