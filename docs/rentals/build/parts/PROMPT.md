# The home-part pictures (HAD-795)

One studio picture per part kind, the same family for the opening card of /my-rentals/ and for every screen of the product.
Made one at a time in ChatGPT image generation (the owner's account), copied with "Copy image" and saved from the clipboard to
`D:\Media\nad-lan\rentals-pictures\raw\p-<kind>.png`; `python scripts/rentals/make_part_pics.py <kind> ...` writes the 192 px file
into `plugins/nadlan-config/assets/rentals/portfolio/img/`.

Prompt (only the subject changes):

> Create one square 1:1 image. Studio product photograph on a plain pale blue-grey background, soft even light, one soft shadow,
> the whole object centred and fully in frame with margin around it, no brand, no text, no logo, no labels, no display digits.
> Subject: <the object>, seen slightly from the side.

Subjects: boiler (white cylindrical electric water heater on a wall bracket, two copper pipes), ac (white split unit, indoor part),
panel (grey electricity panel, door open), water_meter (brass water meter with a valve), fridge, oven (free-standing cooker),
washer, dishwasher (stainless steel, door closed), heater (white oil-filled radiator on wheels), shutter (window with a white
electric roller shutter half lowered), gas (small grey domestic gas meter, shut-off valve with a yellow lever).
A new kind gets a picture before it is added to the list in `rm-plan2d.js` (`PIC`).
