# HAD-256 · computed contrast and the floating bar, every screen (generated)

From `test_layout.py` on real WordPress + Chrome: every text node under the journey, its computed colour on the effective background (alpha-blended up the ancestors), 4.5:1 (3:1 for 24px+ or 18.66px+ bold), placeholders included; every focusable control focused and checked with `document.elementFromPoint` against the site's real floating bar `#nlcta`.

| Width, language | Screens | Text nodes | Under the ratio | Exempt (disabled controls, WCAG 1.4.3) | Controls focused | Covered or off screen | JS errors |
|---|---|---|---|---|---|---|---|
| 320-he | 13 | 361 | 0 | 2 | 161 | 0 | 0 |
| 360-he | 13 | 361 | 0 | 2 | 161 | 0 | 0 |
| 390-he | 13 | 361 | 0 | 2 | 161 | 0 | 0 |
| 412-he | 13 | 361 | 0 | 2 | 161 | 0 | 0 |
| 1440-he | 13 | 467 | 0 | 2 | 161 | 0 | 0 |
| 320-en | 13 | 362 | 0 | 2 | 161 | 0 | 0 |
| 360-en | 13 | 362 | 0 | 2 | 161 | 0 | 0 |
| 390-en | 13 | 362 | 0 | 2 | 161 | 0 | 0 |
| 412-en | 13 | 362 | 0 | 2 | 161 | 0 | 0 |
| 1440-en | 13 | 469 | 0 | 2 | 161 | 0 | 0 |

Exempt items (disabled controls; drawn solid and readable anyway):

- 320-he, promotion-off: "רשימת הנכסים" 4.13:1 (disabled control)
- 320-he, promotion-off: "לא זמין כרגע" 4.28:1 (disabled control)
- 320-en, promotion-off: "Property list" 4.13:1 (disabled control)
- 320-en, promotion-off: "Not available yet" 4.28:1 (disabled control)
