---
name: buyer-gaze-ux
description: Evidence-based rules and browser checks for where a property buyer's eyes and thumb go on a phone (first) and a desktop (second), in Hebrew right-to-left and in English, French, Russian and Arabic. Use when designing, reviewing or auditing an apartment or project page, the "apartment cockpit" panel that opens from a 3D tower, a listing card, a price, deals or monthly-cost block, a gallery, plan, view or 360 module, or a lead button on nad-lan, houseindex or the owner's other real-estate sites; and when asked "where should this go on mobile", "is this button reachable", "is this urgency line allowed", "audit the gaze / thumb UX", or "make the cockpit evidence-based".
---

# buyer-gaze-ux

Rules for the first screen, the thumb and the buyer's decision on property pages, each backed by a cited
study, standard or law, with measurable browser checks. Built 10.11.2026 for the Kikar showcase apartment
cockpit (tap an apartment in the 3D tower, one panel shows plan, view, price and deals, monthly cost and
taxes, the area, shops below, video call and 360 inside).

Full evidence: `references/rules.md` (36 rules R1 to R36, sources, strength grades A to D).
Full checks and the console script: `references/checks.md` (K0 to K32) and `scripts/bgu-audit.js`.
Research copy: `nad-lan-co-il/docs/research/2026-11-10-kikar-showcase/ux/`.

## When to use

- Designing or reviewing any real-estate page state on a phone or desktop, before code and before release.
- Auditing a competitor page the same way (the script is read-only).
- Writing persuasion copy around price, scarcity, deals or "sold" counts.
- Choosing where a button, sheet, gallery, plan or 3D view goes, in any of the five languages.

Not for: palette, typefaces and visual identity (the owner's design law decides those), SEO structure,
or indexing decisions.

## Inputs to collect first

1. The page URL or build, and the states to audit: phone peek, half and full sheet; desktop panel.
2. The languages available (Hebrew is mandatory; add at least one left-to-right language).
3. Which elements are the primary actions (ask the developer to mark them `data-cta`) and which lines
   are sourced facts (`data-source` and `data-asof`).
4. Real-user Core Web Vitals if they exist (Search Console, CrUX), otherwise lab only and say so.

## Procedure

1. Set the viewport to 375 x 812 with touch and a mobile user agent. Open the page, tap one apartment.
2. Paste `scripts/bgu-audit.js` into the console (set `window.BGU = { panel: '<cockpit selector>' }`
   first). Run it at peek, half, full, and after scrolling each full-state screen.
3. Repeat at 1440 x 900 on the desktop panel.
4. Repeat steps 1 to 3 in the second language; check that the desktop panel moved sides (R8).
5. Do the manual checks (K2, K11, K12, K15, K17, K18, K21, K22, K24, K25, K27, K29 to K31), about 30
   minutes in total; the order is in `references/checks.md`.
6. Score every failure against the rule list below, highest tier first, and write the report.
7. Never fix a live site from this skill alone; hand fixes to the normal branch, PR and release flow.

## Rules in priority order

Grades: A controlled experiment, field experiment or meta-analysis; B large observational or replicated
usability evidence; C single study, expert guideline or standard; D vendor, survey or inference.

### Tier 1: trust and law (a failure here blocks release)

1. **R21 All-in price first (A).** Total including VAT and mandatory charges on first view; one-time costs
   and monthly cost in the same section. Israeli CPL 17A-17B; StubHub field experiment; loss aversion 1.96.
2. **R24 True scarcity only (A).** Sold, remaining, deadlines and demand only when live, sourced and
   dated; no countdowns, no "people viewing now". CPL 2, 3, 7; UCPD Annex I(7); CMA 2019.
3. **R22 Real anchors (A).** Asking price beside dated nearby deals and price per m2; no invented "was"
   prices. Anchoring (Many Labs); CPL 2(a).
4. **R25 Label renders (C).** Every render, staging, AI image and simulated view is labelled inside the
   image; show the real view when it exists. View is a priced attribute (Benson 1998).
5. **R33 Isolate numbers (C).** Prices, areas, ranges, phones and dates are isolated LTR runs; locale
   formatting via Intl.

### Tier 2: speed and reach

6. **R29 Apartment visible in 2.5 s (A).** Poster and visual first, 3D streams after. Bing, Booking.com
   latency experiments; Core Web Vitals.
7. **R30 Tap answers in 100 ms, done in 200 ms (B).** INP at most 200 ms.
8. **R31 Nothing jumps (C).** CLS at most 0.1.
9. **R14 Targets 44 px, never under 24, corners bigger (A/C).** WCAG 2.5.8, Apple, Material, Parhi 2006.
10. **R12 Actions in the middle-to-lower band (B).** Hoober; NN/g 2023; Eardley 2017.
11. **R13 Mirror the reading, not the hand (B).** Primary action centred or full-width in every language.
12. **R2 First screen answers which, how big, how much (B).** Identity, all-in price, visual, one action.

### Tier 3: structure

13. **R1 Lead with this apartment's own visual (B).** Plan for off-plan, real view for high floors.
14. **R7 Phone: non-modal sheet that becomes a real page (C).** Peek, half, full; full has a URL, Back,
    close button and swipe-down. NN/g warns against sheets as detail pages, so the full state is a page.
15. **R8 Desktop: docked panel on the reading-start side (B/C).** Right in Hebrew and Arabic, left in
    English, French and Russian; tower stays live.
16. **R9 One vertical scroll, collapsible sections, no horizontal tabs (B).** Baymard 27% versus 8%.
17. **R10 Visible section index, no hidden menus (B).** NN/g hidden navigation study, 179 people.
18. **R17 Four or five top-level choices at once (B/C).** Hick-Hyman, Cowan.
19. **R19 One primary, at most one secondary action (C/D).** Slim bottom bar on phone full state.
20. **R27 3D, 360 and video on demand only (B).** Tours speed screening; price effect unproven.
21. **R26 Floor plan within one tap (D, strong prior).**
22. **R11 One layer at a time (C).** Heavy media opens full-screen with a visible exit.
23. **R16 No gesture traps (D).** Embeds do not steal vertical scroll.

### Tier 4: craft

24. **R3 Front-load lines; start is the right edge in RTL (B/C).**
25. **R4 Headings carry the figure (C).**
26. **R5 Full facts inside, legible: 16 px text, 4.5:1 contrast (C).**
27. **R6 Nothing looks like an ad (B).**
28. **R15 Space targets; isolate irreversible actions (C).**
29. **R18 Compare two or three similar apartments, not all (B, contested).**
30. **R20 Calculator defaults are real, visible, editable (A).** Bank of Israel caps, date-stamped.
31. **R23 Monthly figure beside the total, with assumptions (B).**
32. **R28 Gallery counter on phone, thumbnails on desktop (B).**
33. **R32 Real content first; progress for waits over 1 s (C, mixed).**
34. **R34 Room for longer French and Russian text (C).**
35. **R35 Mirror the interface, never the world (C).** Plans, compass, tower, clocks, media stay.

### Always

36. **R36 Every rule is a prior (A as method).** Ship with a declared metric; split results by device
    and language.

## Checks at a glance

| Check | Pass | Rule |
|---|---|---|
| K0 mobile viewport | layout width = screen width | R14 |
| K1 visual share of panel screen | 0.30 to 0.60 | R1, R2 |
| K2 identity + all-in price + one action visible | all three | R2 |
| K3 words above first visual | at most 20 | R1, R3 |
| K4 headings with a figure | at least 50% auto, 80% on review | R4 |
| K5 targets under 24 / under 44 / small in corners | 0 / at most 10% / 0 | R14, R12 |
| K6 crowded small targets | 0 | R15 |
| K7 primary actions outside 35-98% height band (phone) | 0 | R12, R13 |
| K8 visible interactive elements / primary actions | at most 8 / 1 to 2 | R17, R19 |
| K9 horizontal tabs on core content | 0 | R9 |
| K10 core sections only in hidden menus | 0 | R10 |
| K11 sheet: Back, close, swipe, Esc, URL, no stacking | all | R7, R11 |
| K12 vertical swipe on embed scrolls the panel | yes | R16 |
| K13 LCP p75 | at most 2.5 s | R29 |
| K14 3D assets before LCP | 0 | R27, R29 |
| K15 INP for tapping an apartment | at most 200 ms | R30 |
| K16 CLS | at most 0.1 | R31 |
| K17 progress for waits over 1 s | yes | R32 |
| K18 all-in price, one-time and monthly costs, assumptions | all | R21, R23 |
| K19 unsourced urgency lines / ticking countdowns | 0 / 0 | R24 |
| K20 struck-through prices without a dated record | 0 | R22 |
| K21 renders labelled | 100% | R25 |
| K22 plan within one tap, zoom, dimensions | all | R26 |
| K23 unisolated number runs in RTL | 0 | R33 |
| K24 pseudo-localised labels clip | 0 | R34 |
| K25 lang/dir match; UI mirrored, world not | all | R35 |
| K26 bottom bar height | at most 11% of viewport | R19 |
| K27 ad-like treatment | 0 | R6 |
| K28 inputs under 16 px / running text at 16 px | 0 / at least 80% | R5, R20 |
| K29 gallery counter or thumbnails | yes | R28 |
| K30 comparison set | 2 or 3 | R18 |
| K31 calculator defaults visible and current | all | R20 |
| K32 change has metric and test | yes | R36 |

## Right-to-left quick sheet

- Start side = right in Hebrew and Arabic: identity, price and section index start there.
- Desktop panel sits on the right in Hebrew and Arabic, on the left in the other three languages.
- The thumb is not mirrored: keep primary actions centred or full-width in every language.
- Numbers, prices, ranges, phones and dates are isolated LTR runs; Hebrew charts keep time left to right
  (Israeli finance convention), which conflicts with Material guidance; test Arabic separately.
- Mirror arrows, gallery order, progress and chip rows; never mirror plans, compass, the tower, clocks or
  media playback controls.
- Arabic digits: choose Western or Arabic-Indic once and set numberingSystem explicitly.

## Report format

Write the report in the language of the person who asked (Hebrew for the owner, plain words, no rule
numbers in the opening lines). Structure:

1. One paragraph: what was audited (URL, states, sizes, languages), the date, and the verdict.
2. Blocking failures (Tier 1 and Tier 2), each with: what is wrong, where (state and screenshot), the fix
   in one line, the rule ID and its evidence grade.
3. Other failures (Tier 3 and 4), same format, shorter.
4. Passes worth keeping.
5. Not tested and why (devices, languages, states, field data missing), and which thresholds are derived.
6. Proposed experiments for any change whose evidence is grade C or D (R36).

Attach the console table output for each state. Keep claims to what was measured; when the evidence for
a rule is thin, say so in the line that uses it.

## Guardrails

- Never write or suggest fake urgency, invented "was" prices, unlabeled renders or hidden fees, even for
  a test; these are Israeli consumer-law exposures, not style choices.
- Do not cite a vendor figure (Zillow, Matterport, sticky-bar tests, portal surveys) as proof; label it D.
- The NN/g above-the-fold figures are desktop; do not quote them as phone measurements.
- Visual identity is out of scope; follow the owner's design law for palette and type.
- This skill measures and recommends; it never edits a live site, Linear or Notion by itself.

## Evidence gaps to keep in mind

No eye tracking of Hebrew web pages exists in the sources; mobile above-the-fold attention has no
numbers; Hoober's thumb data is observational; sticky bars, video calls, floor plans and virtual staging
rest on vendor tests and surveys; 3D tours help screening but their price effect is mixed; choice
overload is contested; Israeli law has no ruling yet on render labels or real-estate urgency lines.
