# Designer plan files: notes, assumptions and size checks (HAD-701 / HAD-708)

11.11.2026. Local only, nothing here is live.

## Files

- Plans (nadlan-apartment v1, each with a `starter` furniture list): `plugins/nadlan-config/assets/designer/plans/ashira/E-4A.json`, `E-3B.json`, `E-5E.json`, `E-5F.json`, `example-3r.json`, `example-5r.json`, and `index.json`. `example-4r.json` is not touched by any of these tools.
- `build-plans.mjs`: the traced source of all six plans. It splits walls at every T-junction, merges shared corners, places every opening from its wall's a-end, and writes `plans-published.json` (every printed Ashira size and the dimension line we measure it on). Edit the specs there and run it again; never hand-edit the JSON.
- `check-plans.mjs`: the checker (no dependencies; imports the plugin's `core.js` and `catalog.js`). `node check-plans.mjs` must end with "7 of 7 plans pass".
- `plans-harness.html` + `shoot-plans.mjs`: open the designer module on any plan (`?plan=ashira/E-4A.json`) and save `plans-evidence/<id>.png` (the plan view) and `<id>-full.png` (plan and 3D).

## How the printed sizes are compared

A printed room size on an Israeli sales plan is a dimension line between two wall faces. So the check draws the same line on our redraw: from a point at the label's place, along the label's direction, both ways to the first wall face (a wall's thickness counts at the angle it is hit). Where the printed size runs across an open kitchen (the living room sizes), the line passes the divider; for kitchen runs it stops at it. Pass means within 4% either way.

The core's own "clear W×D" (the table the designer's spec sheet shows) is the axis-aligned bounding box of the space minus half the walls. It is printed for every room, but it is not the comparison: for an L-shaped room it gives the largest extent, and for E-3B's turned bedroom wing it is meaningless (see findings).

## Ashira, building E: what was traced and how

The four sales plans in `_private-research/2026-10-18-ashira-public-refs/` were looked at only. The sheets are not to scale in the same way: about 1.00 cm per sheet pixel for E-4A, 0.89 for E-3B, 1.08 for E-5E, and 1.46 across by 1.52 down for E-5F. Walls were traced in sheet pixels, scaled, then nudged so the printed sizes come out as clear sizes. Topology (who meets whom, where each door is and which way it opens) follows the drawing.

No plan of building E has a ממ"ד inside the apartment: every key plan shows the floor's shared protected space (ממ"ק) in the core. So there is no `mamad` wall kind and no safe-room room in the four Ashira files. That is the plan, not an omission.

### E-4A (4 rooms, north-west corner) · north_deg 11

| Room | Studio d | Printed | Ours | Deviation |
|---|---|---|---|---|
| Living and dining, width | 718×473 | 718 | 717.5 | -0.1% |
| Living and dining, depth (across the open kitchen) | | 473 | 472.5 | -0.1% |
| Master, upper width | 513×270 | 683 | 682.5 | -0.1% |
| Master, lower width beside the en-suite | | 513 | 507.5 | -1.1% |
| Master, depth | | 270 | 270.5 | +0.2% |
| Bedroom 1, width with the wardrobe niche | 348×288 | 348 | 348.0 | 0.0% |
| Bedroom 1, width below the niche | | 288 | 292.5 | +1.6% |
| Bedroom 2, width with the desk niche | 373×313 | 373 | 373.0 | 0.0% |
| Bedroom 2, width below the niche | | 313 | 308.5 | -1.4% |
| Bedroom 2, depth at the east wall (not in the studio list) | | 283 | 285.0 | +0.7% |

Largest deviation: 1.6% (bedroom 1, 288).

- The studio listed **683 under the kitchen**. On the plan, 683 is printed inside the master bedroom, just under the kitchen wall: it is the master's upper width (the master is L-shaped around the en-suite and the guest toilet). The kitchen has no printed size.
- **The two bedroom pairs (348/288, 373/313) are both widths**, at two heights of an L-shaped room: the top part takes a niche between the two bedrooms (a wardrobe niche for bedroom 1, a desk niche for bedroom 2), the lower part does not. The niches are drawn as one wall between the bedrooms down to the corridor's end.
- **Bedroom 1's vertical label 268 is not checked**: no wall-to-wall line near it measures 268 (the drawn depth is about 302 cm clear, because the bedroom's lower wall is drawn in line with the balcony glazing). Bedroom 2's vertical 283 does match a line (above the shaft notch) and is checked.
- Assumptions: the walls between rooms are partitions (10 cm) except the outline; the shaft notch in the corner of bedroom 2 is drawn as a structural jog and the small piece below it belongs to the bathroom; the right (east) outer wall is structural with no window (it is solid on the plan); the window and glazing widths are read off the plan to about 20 cm; the balcony curve is a 7-segment polyline.
- The entrance hall and the corridor between the bedrooms are separate spaces (a divider at the bathroom's lower wall) so each gets its own label.

### E-3B (3 rooms, south-east corner) · north_deg 296

| Room | Studio d | Printed | Ours | Deviation |
|---|---|---|---|---|
| Living, width (across the open kitchen) | 665×373 | 665 | 665.0 | 0.0% |
| Living, depth | | 373 | 373.0 | 0.0% |
| Kitchen run | 284 | 284 | 284.0 | 0.0% |
| Master, along the wing | 428×278 | 428 | 428.0 | 0.0% |
| Master, across the wing | | 278 | 278.0 | 0.0% |
| Bedroom, along the wing | 308×273 | 308 | 308.0 | 0.0% |
| Bedroom, across the wing | | 273 | 273.1 | 0.0% |

Largest deviation: under 0.1%.

- The bedroom wing is turned on the sheet. It is drawn as a true rectangle grid turned by 17.5 degrees (the drawing's own walls run between 16.4 and 18.2 degrees). The two bathrooms sit between the turned wing and the straight living part: their top and side walls follow the wing, their bottom wall is straight (it is the top of the living room, as drawn).
- The living space includes the open kitchen (284 is the run of cabinets from the south glazing) and is separated from the dining corner by dividers; "פינת אוכל" is the space by the entrance, as labelled on the plan.
- Assumptions: the washing-machine niche next to the en-suite is left out (it sits in the wall thickness of our trace); the entrance wall is traced at the wing's angle; the corridor (1.4 m²) is the short passage to the bedrooms, closed from the living room by a divider; window widths are approximate.

### E-5E (5 rooms, north-west, balcony with a jacuzzi) · north_deg 349

| Room | Studio d | Printed | Ours | Deviation |
|---|---|---|---|---|
| Living and dining, width | 573×493 | 493 | 493.3 | +0.1% |
| Living and dining, depth (across the open kitchen) | | 573 | 573.3 | +0.1% |
| Kitchen run, south wall | 333×273 | 333 | 333.1 | 0.0% |
| Kitchen run, west wall | | 273 | 273.7 | +0.3% |
| Bedroom 1, width | 313×288 | 288 | 288.1 | 0.0% |
| Bedroom 1, depth | | 313 | 313.0 | 0.0% |
| Master, width at the foot of the bed | 558×278 | 278 | 278.4 | +0.1% |
| Master suite, depth through the dressing area | | 558 | 565.7 | +1.4% |
| Bedroom 2, width | 313×283 | 313 | 313.0 | 0.0% |
| Bedroom 2, depth | | 283 | 292.4 | +3.3% |
| Bedroom 3, depth | 292×273 | 292 | 292.5 | +0.2% |
| Bedroom 3, width | | 273 | 273.0 | 0.0% |

Largest deviation: 3.3% (bedroom 2, 283).

- The master's 558 and bedroom 2's 283 share one wall (the line between the dressing area and bedroom 2). Satisfying 558 exactly would put bedroom 2 at 300 (+6%); satisfying 283 would put the suite at 573 (+2.8%). The wall sits between the two: +1.4% and +3.3%. Both inside 4%.
- The master is the room plus the dressing passage (one space, as drawn); the en-suite is its own room.
- Assumptions: the masonry pier between bedroom 1 and the master is drawn as a 22 cm jog in that wall (it is what makes 278 come out at the foot of the bed); the laundry niches along the corridor are left out; the bedroom 1 door is in its lower wall, opening off the corridor's top; the entrance hall and the corridor are separate spaces (dividers) so the labels land in the right place.

### E-5F (5-room penthouse, floor 16, wrap-around balcony) · north_deg 349

| Room | Studio d | Printed | Ours | Deviation |
|---|---|---|---|---|
| Living and dining, width | 583×858 | 583 | 580.9 | -0.4% |
| Living, dining and kitchen, depth | | 858 | 845.9 | -1.4% |
| Kitchen run | 373 | 373 | 373.0 | 0.0% |
| Bedroom 1, width | 388×268 | 388 | 394.2 | +1.6% |
| Bedroom 1, depth with the wardrobe row | | 268 | 271.2 | +1.2% |
| Bedroom 2, width | 388×278 | 388 | 394.2 | +1.6% |
| Bedroom 2, depth | | 278 | 278.8 | +0.3% |
| Bedroom 3, width | 333×408 | 333 | 335.8 | +0.8% |
| Bedroom 3, depth | | 408 | 405.0 | -0.7% |
| Master, width with the wardrobe wall | 478×288 | 478 | 464.3 | -2.9% |
| Master, depth at the label | | 288 | 297.1 | +3.2% |

Largest deviation: 3.2% (master, 288).

- **Read with care: the master's 288.** The master and bedroom 3 share the same south glazing and their top walls are drawn at nearly the same height, yet bedroom 3 is printed 408 deep and the master 288. The 288 is printed beside the master's door, under the wall at the end of the corridor, and from that wall to the glazing our redraw gives 297 cm (+3.2%). Measured at the bed, the master is about 345 cm deep. If 288 was meant as the full depth it cannot be met without redrawing the room against the plan's own geometry (it may be a misprint for 388, which would be -2.9% from what is drawn). The check uses the line at the label and passes; the doubt is listed here, not hidden.
- The plan's text is turned 90 degrees on the sheet; a turned number is a vertical dimension (confirmed on bedroom 3: 333 across, 408 down).
- The wrap-around balcony is one balcony; it is stored as two balcony spaces (north 53.1 m², west 39.0 m², both "מרפסת", split by a divider at the facade corner) because the plan view puts a label at the centre of a space's bounding box, which for the one U-shaped space fell inside the kitchen.
- Assumptions: the third and fourth wet rooms open from the corridor (as the door arcs show), so the master has no en-suite of its own; the closet column beside the guest toilet is left inside the living space; the entrance alcove is part of the living space; the facade corners are 3 to 4 straight facets each.

## Invented examples

Both are labelled "דירה לדוגמה" (source.kind example) and belong to no project.

- `example-3r`: 3 rooms, 72.2 m² net + 9.0 m² balcony. Living with dining, open kitchen with island, entrance, master bedroom, a ממ"ד used as the second bedroom (30 cm walls, door 80 cm, window), one bathroom.
- `example-5r`: 5 rooms, 134.4 m² net + 13.1 m² balcony. Living with dining, open kitchen with island, guest toilet, entrance and corridor, a parents' unit with its own shower room, two bedrooms, a family bathroom and a ממ"ד (9.8 m², 30 cm walls on all four sides).
- Both carry the same two placeholder rules as `example-4r` (to be verified against the Planning and Building Regulations before public use).

## Starter furniture

Only these catalogue pieces are used: sofa3, tv, rug, dining6, chair, kitchen (330×60 as catalogued), island, bedset, bed160, wardrobe2, plant, all `status: decor`. The checker requires each piece's centre to be in a room, every corner inside the apartment, and no overlap with any wall band except a divider (a rug or a kitchen run may cross the line of an open kitchen). E-4A has no island (the kitchen strip is 1.65 m deep and the plan shows none); the 3.30 m kitchen run is placed along the longest kitchen wall even where the printed run is shorter (E-3B, 2.84 m), crossing the open divider.

## Findings for the engine (not changed here; these files belong to other tasks)

1. `plan.js` puts a room label at the centre of the space's bounding box. For an L or U shape that point can be in another room (E-5F's balcony label sat in the kitchen). `core.js` already has `interior(f)`; the label should use it. Until then the plans avoid it with dividers.
2. `core.js` clear size (`clearW × clearD`) is the axis-aligned bounding box. For E-3B's turned wing the spec sheet will print 514×416 for a 428×278 master, and for L-shaped rooms it prints the largest extent. A turned or L-shaped room needs a measured size (the probe method above is one way).
3. `apartment.schema.json` (00:19) does not list `starter`, `points`, or the rule code `mamad.no_chasing`, which `designer.js`, `core.js` and the updated `example-4r.json` already use. The checker accepts them and prints a NOTE; the schema should add them.
4. The two "to be verified" rules apply to bedrooms only; the Ashira plans have bedrooms of 8.4 m² (E-3B, E-5E bedroom 3), just above the 8 m² placeholder.
