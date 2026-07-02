# COWORK MEGA PROMPT v2 - The Image Factory (honest plates at scale)
Paste this whole file as the session prompt. Mission: give every project,
listing and professional surface on nad-lan.co.il a beautiful sketch-plate
image in one shared DNA, WITHOUT ever drawing a fake world. This runs at
scale: hundreds of subjects, not three.

## 0. THE PRIME LAW: sharp subject, honest environment
A buyer must never absorb a wrong impression from our art. Therefore every
plate follows the AUTHENTICITY LADDER:

- **Tier A - verified surroundings** (rare): we possess checked ground truth
  for the immediate context - an urban plan, Google Maps 3D imagery the
  operator personally inspected, or the developer's site plan. Only then may
  neighboring buildings, streets and landmarks be drawn as specific shapes,
  and each one must match the source.
- **Tier B - THE DEFAULT for every subject**: the building itself is drawn
  sharp and accurate (floors, massing, facade rhythm from our data), and the
  ENTIRE environment is deliberately abstracted: it dissolves into pale,
  out-of-focus wash strokes and blank cream paper, like an architect who
  drew the subject and let the world fade. NO identifiable neighboring
  buildings, NO landmarks, NO invented streets. The only environmental facts
  allowed are MACRO-TRUE ones stated in the fact sheet: the sea as a soft
  horizon band on the correct side at the correct visual distance, open sky,
  a hill line where the city truly has one (Jerusalem, Haifa). If a macro
  fact is not verified, it is omitted, not guessed.
- **Never Tier C.** There is no "plausible neighborhood" option. Blur beats
  fake, always. A beautiful lie is a defect.

## 1. THE FACT SHEET (before any prompt - minimal but mandatory)
For each subject pull from OUR OWN catalog (REST: `/wp-json/wp/v2/<type>?slug=`
or the live page):
1. Type + form: floors, massing (tower/midrise/garden/penthouse), facade
   character if known. Never draw the wrong height (+-1 floor max).
2. City + true sea relationship. Distance to shoreline (Tel Aviv coast ~lng
   34.7752): `d_m = (lng - 34.7752) * 111320 * cos(lat)`. Verified: Rainbow
   ~870m, Ashira ~1,170m - NOT beachfront. Rule: <250m = shoreline may meet
   the frame edge; 250-1500m = sea only as a soft distant horizon band;
   >1500m or unknown = no sea at all.
3. One-line terrain truth if it exists and is verified (e.g. "Jerusalem:
   stone city on hills", "Haifa: slope down to a bay"). Nothing finer.
4. Interior facts for the cutaway: rooms, sqm, balcony, exposure - from the
   listing/unit meta only.
Optionally, ChatGPT can be asked to browse-verify a macro fact ("is X within
300m of the sea?") before drawing - allow it to research, but whatever is not
POSITIVELY verified stays abstract. When in doubt: abstract.

## 2. TEMPLATE A - PROJECT / LISTING PLATE (the workhorse, Tier B)
```
Architectural presentation plate, hand-drawn fine-line ink and pencil sketch on
warm cream paper, in the style of a master architect's illustrated poster.
Subject: a real {FLOORS}-floor {TYPE} in {CITY}. Draw ONLY the building itself
in sharp, accurate detail: {MASSING_NOTES}, {ROOMS_RANGE} apartments,
continuous balconies. The building stands alone as the hero.
CRITICAL - the environment is deliberately abstract and unfocused: everything
around the building dissolves into pale, loose, out-of-focus pencil wash
strokes and untouched cream paper, like an unfinished master drawing. Do NOT
draw any identifiable neighboring buildings, streets, cars or landmarks. Only
these true elements may appear, softly: {MACRO_TRUTHS - e.g. "a muted teal sea
band far on the horizon behind soft haze, clearly about {D} away" / "a pale
hill line" / "open sky"}. If unsure about any surrounding detail, leave it as
blank paper.
One apartment on floor {N} facing {DIRECTION} is highlighted with a thin gold
outline, with fine leader lines to a floating 3D cutaway of that apartment
beside the building: open living room, kitchen island, {ROOMS} rooms, balcony
with two sketched chairs, furniture in the same ink style.
Margin elements: a small data card titled "{UNIT_LABEL}" listing floor {N},
{ROOMS} rooms, {SQM} sqm, balcony, exposure {DIRECTION}; a small floor plan
top-right; a compass; an elegant serif title "{NAME_LATIN} - {CITY_LATIN}"
top-left.
Color: monochrome ink with restrained watercolor washes only - muted teal for
distant water, warm sand, soft amber horizon, single muted gold accents for
the highlighted apartment and rules. No saturated color, no photorealism, no
people, no invented city skyline. Square 1:1, extremely detailed linework on
the building, everything else soft and faded.
```
For LISTINGS (existing apartments, not new projects): same template, but the
cutaway matches the listing's real rooms/sqm, the data card carries the real
price line only if published, and the title is the street + city. Demo
listings keep the honesty of their pages ("לדוגמה" stays on-site).

## 3. TEMPLATE B - PROFESSIONAL VIGNETTE (no faces, ever)
Professionals keep their monogram avatars. Their PAGES and category cards get
a profession vignette in the same DNA:
```
Small architectural still-life vignette, fine-line ink sketch with restrained
watercolor washes on warm cream paper. Subject: the working world of a
{PROFESSION_EN} in real estate - {PROFESSION_PROPS}. Objects only, arranged
like an elegant desk-and-tools study; soft edges fading into blank paper.
Single muted gold accent. No people, no faces, no text, no logos. 4:3.
```
PROFESSION_PROPS examples: lawyer = fountain pen, contract with a wax seal,
brass scales; appraiser = folded plans, laser measure, magnifier over a floor
plan; mortgage advisor = calculator, amortization curve on graph paper, house
key; inspector = hard hat, level, checklist board; interior designer = fabric
swatches, color washes, a sketched sofa; contractor = crane silhouette study,
blueprints, theodolite.

## 4. TEMPLATE C - CITY / AREA TILE (macro truth only)
```
Wide sketch vignette of {CITY}, fine-line ink with light washes on cream
paper: only its VERIFIED macro character - {e.g. "Mediterranean shoreline and
white city blocks fading into haze" / "golden stone buildings on hills" /
"a slope of houses descending to a curved bay"}. Loose, atmospheric, half the
frame dissolves into paper. No specific identifiable buildings unless
world-famous and verified. No text, no people. 4:3.
```

## 5. THE RUN PLAN (this is a factory, not three images)
Work queue, in order, logging every plate:
1. Flagships: Ashira, Rainbow, Dimri Yama - hero + og:image (1:1 + 1200x630).
2. ALL 7 demo listings (IDs 4951-4957) - replace the flat SVG art (4:3).
3. Homepage flag card (16:11) + /en/ hero (16:9) + /advertise/ header (16:9).
4. Area tiles for the top cities in the areas grid (Template C).
5. Professional category vignettes (Template B) for: lawyer, shamai,
   mashkanta, bedek_bait, interior_designer, kablan, architect, inspector.
6. THEN the long tail: work through additional published projects from
   /projects/ in catalog order, batch of 10 per session, Template A Tier B
   for every one (their fact sheets come from their own pages). This is how
   hundreds of pages get populated without a single fake view.
Per image: generate 2-3 candidates -> QA gate -> upload -> place -> verify ->
log in docs/content/2026-07-02-publish-log.md (subject, fact sheet, media ID,
placement).

## 6. QA GATE (reject if ANY fails)
- No invented identifiable surroundings (the core check - compare against the
  fact sheet; anything specific that is not in it = reject).
- Sea/hills on the correct side at the correct visual distance, or absent.
- Floor count within +-1; massing recognizable.
- Palette = cream/ink/muted washes/single gold; zero AI-gloss; no people.
- Text in the plate is clean or absent (garbled text = regenerate).
- Side-by-side with the approved Ashira/Rainbow plates: same artist's hand.

## 7. PLACEMENT (after QA)
Upload: `POST /wp-json/wp/v2/media` (slugged filename, Hebrew alt text of the
REAL subject + "הדמיה להמחשה"). Place per slot: project hero = featured image
+ project_model_poster meta; listing = featured image; og:image comes free
from the featured image. Verify on the live page RENDERED BODY. The on-page
disclaimer stays; the plate itself must already be honest.

## 8. LAWS
No em-dash in user-facing text. Site name "נדלן"/NadLan only. No faces. No
fake geography - blur beats fake, always. Log everything.
