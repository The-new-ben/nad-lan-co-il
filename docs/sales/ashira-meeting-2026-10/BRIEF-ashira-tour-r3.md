# Ashira 360, round 3: plan-accurate apartments and developer-grade facilities. Same write scope/rules as BRIEF-ashira-tour.md. LOCAL ONLY.

Ben 18.10 night: "many levels above Rainbow", built from the project's PUBLIC images and the apartment plans.
Reference folder (READ ONLY, never copy any of these files into the repo or the site, never trace their pixels into a texture):
C:\Users\777\nad-lan\_private-research\2026-10-18-ashira-public-refs\
  apt-e-3b|4a|5e|5f-plan.png (the developer's published sale plans, building E), apt-e-*.jpg (their interior renders),
  pool.jpg spa-new.jpg gym.jpg cinema.jpg kids.jpg lounge1.jpg (their facility renders), complex-1-s.png, design-1-s.png.
Look at every image before modelling. Our scenes are our own Blender models INSPIRED by these (layout, proportion, palette,
mood), labelled "הדמיה להמחשה, לפי תוכנית הדירה שפורסמה באתר היזם".

## 1. Apartment E-4A (4 rooms) modelled from its plan, in centimetres (read apt-e-4a-plan.png yourself and confirm)
- Living room 718 x 473 on the west facade, full-height glazing along it; dining corner (round table, 5 chairs) east of it.
- Corner balcony (quarter-circle edge) at the north-west corner off the living room, with round table + 4 chairs + 2 planters.
- Kitchen along the west facade wall south of the living room (linear run: cooktop, sink, tall unit), open to the living room.
- Master bedroom 513 x 270 (south-west), en-suite shower room + guest WC; bedrooms 348 x 288 and 373 x 313 (north), family
  bathroom with bath; entry from the east corridor. Ceiling height 2.80 m. North arrow per the plan's note (relative to building).
- Scenes: living room 360 standing at the room centre looking west, and from the balcony; floors 10, 25, 34 (view changes by height),
  plus the master bedroom 360 on floor 25. Repeat the same treatment for E-3B, E-5E and E-5F living rooms at floor 25 (read their plans).
## 2. Interior style = the developer's own look (see apt-e-4a.jpg): warm minimal; light micro-cement or large pale stone floor,
  linen sheer curtains, black track lights, bouclé modular sofa, walnut shelving with black frame, round travertine dining table,
  leather lounge chair, textured rug, olive tree on the balcony, soft sunset light from the west. Real proportions, contact shadows.
## 3. Facilities modelled after the developer's renders:
- Pool hall (pool.jpg): long indoor half-Olympic pool, travertine/stone walls with wall-washers, the curved vaulted ceiling with
  linear lights, saunas along the left (DRY SAUNA signage), loungers right, glass end opening to a lounge with a green wall.
- Spa (spa-new.jpg): salt room glow, treatment area, warm wood. Gym (gym.jpg): overlooking the pool, equipment, mirrors.
- Cinema (cinema.jpg), Kids world (kids.jpg: jumbo play structure, climbing wall, Montessori wall, gaming zone),
  Lounge (lounge1.jpg: bar, work tables, sofas). Lobby: double height, stone, reception.
## 4. The view must carry decision information (like Rainbow's view panel): from each living-room 360 write, into
  ashira/tour/views.json, the true bearing of each window and the named places visible with straight-line distance, taken from
  ashira/places.json and city.json (sea/Reading beach, Yarkon mouth, Tel Aviv Port, the university, light-rail stop, schools,
  parks, shopping). Distances computed, not guessed. No labels baked into the images (the viewer draws them).
## 5. Quality: 4096x2048, 128 samples + OIDN, filmic/AgX, no blown windows; render a 1024 preview of each first and compare it
  side by side with the matching developer render (save compare-<scene>.jpg in docs/sales/ashira-meeting-2026-10/tour/).
## 6. Proof + honest REPORT.md (append a "Round 3" section): file list, sizes, times, what still differs from the developer look.
