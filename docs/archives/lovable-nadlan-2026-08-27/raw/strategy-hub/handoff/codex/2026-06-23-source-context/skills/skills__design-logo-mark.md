# Logo & Brand Mark — wordmark, monogram, lockups

> **Notice to all agents:** The cartoon-house logo direction (generated 2026-05-28 via PIL, uploaded as `site_logo` media id 338) is **REJECTED**. The brand mark is the **serif wordmark + monogram in a gold double-circle seal** as specced by Lovable (`docs/design/lovable-output-2026-05-28.md` §B). This skill is the operational rules.

## The wordmark

- Text: **נדל״ן חכם**
- Family: **Frank Ruhl Libre**, weight **500**, tracking **−0.01em**, optical size **32–48px**.
- The **`״` (gershayim)** is preserved — **never** replaced with quote marks or hyphen.
- All letters baseline-aligned. No swashes, no italic, no shadow, no gradient, no 3D.
- Color: `--ink-900` on cream/paper; `--cream-50` on dark backgrounds.

## The monogram (the "seal")

- The Hebrew letter **נ** in Frank Ruhl Libre 500, color `--ink-900`.
- Enclosed in a **1px gold (`--gold-600`) circle** of diameter **1.6× cap-height**.
- Inside: a **second concentric circle** at **0.92× diameter** as a hairline frame — this "double rule" is borrowed from old auction houses (Sotheby's, Christie's).
- No fill behind the נ — the cream/paper shows through.
- The נ sits optically centered, **slightly raised (~3% of diameter)** to compensate for the letter's open base.

## Lockups (Lovable §B → Lockups)

### Horizontal (default — header use)
- **Monogram on the right** (RTL), 16px gap, wordmark to its left.
- Wordmark baseline aligned to monogram center.
- Optional tagline below wordmark: eyebrow style + 24px wide gold underline rule (1px) centered.

### Stacked (footer, social cards, occasional hero use)
- Monogram top, wordmark below, tagline below wordmark, centered.

### Favicon (browser tabs, PWA)
- **Monogram only**.
- 32×32 keeps the inner hairline circle.
- 16×16 **drops the inner hairline** (visual noise at that size).

### Dark-background variant
- Monogram and wordmark in `--cream-50`.
- Gold frame stays `--gold-600`.

## The tagline (eyebrow under wordmark)

- Text: **ידע. כלים. החלטות.** (Knowledge. Tools. Decisions.)
- Family: **Heebo 500**, size **12px**, tracking **0.22em**, color `--ink-500`.
- Optional — used when there's vertical room.

## What we will NEVER do (Lovable explicit + owner explicit)

- ❌ House icon, key, roof, graph, skyline, map pin (rejected by owner 2026-05-28).
- ❌ Abstract "n" mark (we use the Hebrew נ, not Latin).
- ❌ Gradient, 3D, shadow on the mark.
- ❌ Bright gold (#D89B3C from the deprecated palette) — use `--gold-600` (#9C7A3C).
- ❌ Bright corporate blue or any blue.
- ❌ Multi-color marks. The mark uses ink + gold + the underlying surface. That's it.
- ❌ Lockups with the wordmark on the right of the monogram in RTL contexts (it's monogram-right, wordmark-left).

## Implementation steps

1. **Replace the live `site_logo`** (currently media id 338, the rejected cartoon-house PNG) with the Lovable-specced lockup. Regenerate via:
   - The existing PIL pipeline at `assets/branding/` (Frank Ruhl Libre TTF is already at `/tmp/FRL.ttf`; bundled woff2 in repo at `assets/fonts/frank-ruhl-libre/`).
   - OR — preferable — hand it to a type designer to kern the gershayim and tune the gold circle weight (Lovable's honesty statement flags this as needing real designer review for the final lockup).
2. **Replace `site_icon`** (currently media id 340, the rejected favicon) with the new monogram-only 32×32 and 16×16 variants.
3. **Replace Yoast default OG** (currently media id 341, the rejected gold-band design) with an editorial OG following Lovable's `display-2` ink/cream/gold composition.
4. Set updated media ids via `POST /wp/v2/settings` with `site_logo` and `site_icon`.
5. Wire the dark-bg variant into the footer template-part once the footer is re-styled to the new tokens.

## Cleanup task (one bash call when ready)

```python
# Unset the rejected logo/favicon/OG to avoid them shipping accidentally
# until the new lockup is approved.
req('POST','/wp/v2/settings', {'site_logo': 0, 'site_icon': 0})
# Optional: delete media ids 338, 339, 340, 341 (rejected variants) once new ones live.
```

The owner approved unsetting these in chat 2026-05-28 (offered, awaiting say-the-word).

## Open TODOs

- [ ] Approve final monogram artwork (Lovable spec is strong; a human type designer can polish if owner wants).
- [ ] Generate new logo.png / logo-white.png / favicon-512.png / og-default.jpg to Lovable's spec.
- [ ] Upload + set `site_logo`, `site_icon`, Yoast default OG via REST.
- [ ] Unset the rejected media ids 338/340 from settings (one REST call).

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8). Source: docs/design/lovable-output-2026-05-28.md §B._

