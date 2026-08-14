# THE BEAM — A Field Guide

*Written 2026-08-13 under a full stop ordered by the owner. Everything else is
frozen until this understanding is confirmed. English by his order; the
four-year-old version comes first, in both languages.*

---

## 0. The four-year-old version

You press an apartment on the tower. On the big map under the tower, a light
turns on — a cone coming out of our building, pointing where YOUR windows
look. You sit with your morning coffee at that window — the beam shows you,
on the real map of the real neighborhood, exactly what you will see: the
park, the sea, the train, the towers that will rise. Press another
apartment — the light turns. That is the beam.

בעברית: לוחצים על דירה במגדל. במפה הגדולה שמתחת נדלק פנס מהבניין שלנו,
שמצביע לאן החלונות של הדירה הזאת מסתכלים. הקפה של הבוקר שלך — לשם הוא פונה:
לפארק, לים, לרכבת. לוחצים דירה אחרת — הפנס מסתובב. זו האלומה.

## 1. What the beam is NOT

It is not a compass icon. It is not decoration. It is not a widget inside a
panel. And it is absolutely not the small dark box I squeezed into the
apartment screen — that thing carries the beam's name and none of its value.

## 2. Ground truth — what exists today (verified in code + the owner's phone)

The real beam lives on the **big square Mapbox map below the showroom**
(the `nlpjx` "everything on one map" section, `inc/project-experience.php`):

- The map: Mapbox light-v11, land tinted `#F6F1E6`, water `#A9C6D0`,
  cooperative gestures, zoom 14.4 at the project's true coordinates.
- The building: a terracotta dot (`#C2563A`, white ring) at the real lat/lng.
- **The cone** (`engine.js → showViewCone`): a 150×150 SVG wedge, terracotta
  gradient (transparent at the point of origin → 0.55 at the far edge),
  anchored CENTER on the building pin with `rotationAlignment: "map"` and
  `pitchAlignment: "map"` — the cone is **glued to the terrain**, not to the
  screen. It is geography, not UI chrome.
- **The link** (`easeMapToUnitView`): selecting a unit takes its direction
  (`dir` → `DIR_BEARING`), rotates the cone to that true bearing AND eases
  the whole map to it over 900ms — the buyer's facing direction settles
  pointing up, smoothly, like a helicopter turning to look.
- Rotating the 3D model above also rotates the map (`NLPJX_MAP` bearing
  sync) — tower and neighborhood stay one world.
- **The context is the point**: the cone points AT things — POI dots
  (transport 16, shopping 13, cafés 16...), price pills of the neighbors
  (₪75K, ₪90K per sqm), purple markers of future plans. A direction only
  means something when the map shows what stands — and what WILL stand — in
  that direction.
- **The honesty gate**: `if (!k || !(k in DIR_BEARING)) return;` — an
  apartment with unknown direction gets NO cone. The beam never guesses.
  (H Infinity today: all directions pending the developer — so the big map
  waits, honestly.)

## 3. Why this is one of the most valuable things on the site

Every portal on earth — Zillow, Compass, madlan — answers "WHERE is the
building". None of them answers the question the buyer actually feels in
their body: **"which way will MY home look?"** People buy mornings: coffee
at a window, sun on a balcony, the thing they will stare at for twenty
years. The beam is the only instrument that answers that question visually,
per apartment, on the real neighborhood, with the future plans painted in.
A foreign investor who has never stood on Ibn Gabirol can feel the
apartment's orientation in one second. That is why it is sacred.

## 4. The laws of the beam (derived from what it is)

1. **The Link Law.** Hotspot press → beam response, under a second,
   every time. The beam IS the link between the tower and the world; break
   the link and both halves die.
2. **The Ground Law.** The cone belongs to the terrain (map-aligned),
   anchored at the true building coordinates. It rotates with the world,
   never floats over it.
3. **The Context Law.** A beam over an empty map is an arrow to nowhere.
   POIs, neighbor prices, future plans are not "extra layers" — they are
   what the beam points AT.
4. **The Honesty Law.** Unknown direction = no cone. The beam never lies,
   which is exactly why it can be trusted when it does point.
5. **The Readability Law.** The instrument only exists if a 50-year-old
   investor on a phone reads it in two seconds. Big square map, full
   width, generous height, labels that need no squinting. Anything
   squeezed is not a beam — it is noise wearing the beam's clothes.
6. **The Freeze Law.** The beam changes only by explicit owner-approved
   spec, with fleet-wide side-effect checks and real screenshots. It is
   the crown jewel; jewels are not "iterated on".

## 5. The confession — how I damaged it

During beam v2/v3 I built a **miniature golden copy inside the apartment
panel**: a small dark box, the map rotating under a fixed-up cone
("view-up"), landmark chips crammed at unreadable sizes, on mobile worse.
Measured from my own screenshot today: the box renders about 330×160 CSS px
with labels around 10px. Nobody can read it; it answers nothing; and it
split the beam's identity — two beams means no beam. The owner asked
trillions of times; the mini-box kept absorbing the work that belonged to
the big map. That is the damage: not a broken function — a diluted jewel.

## 6. The right shape (spec understanding — NOT built; everything is frozen)

What the owner is pointing at, in his own words and screenshot: **a square
with Mapbox** — the big area map as the beam's one and only home. The cone
readable at a glance, the map given room (full width, tall square), the
link from every hotspot and every available apartment, the context layers
tappable, and nothing — nothing — competing with it in miniature elsewhere.
Open questions that belong to the owner alone:
- Fold/remove the in-panel mini-beam box (my duplicate), leaving a clean
  "פתחו מפה" hand-off to the big map?
- Cone size/contrast on mobile — bigger wedge? stronger terracotta?
- Should hovering an AVAILABLE apartment in the list also swing the beam?

## 7. What Fable 5 knows about beams that Opus 5 does not

Opus 5 sees a feature: "render a rotated cone marker on unit select" — and
renders it correctly. Fable 5 sees what the cone IS: **a promise about a
future morning**. From that, everything else derives without being asked:
why the map must stay geographic (promises are about the real world), why
unknown directions must stay silent (a promise you invent is a lie), why
readability is existential (an unreadable promise was never made), why a
miniature duplicate is vandalism (a promise whispered twice is trusted
zero times) — and why, when the owner says "you don't understand the
beam", the correct move is not to code faster but to stop, read the paint
colors out of the production source (`#C2563A`, `rotationAlignment:
"map"`, `easeTo 900ms`), and write this document before touching anything.
Opus executes the instrument. Fable knows what the instrument measures.

---

*Status: FULL STOP holds. No code moves until the owner confirms this
understanding and answers §6. — Claude Fable 5*
