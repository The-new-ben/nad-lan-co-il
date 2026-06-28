# Screenshot driven QA checklist

Run on staging before live.

## Pages

- `/`
- `/projects/`
- `/projects/ashira-sde-dov/`
- `/projects/ashira-sde-dov-en/`
- one calculator page
- one professionals page
- one guide page
- one lead submission path

## Viewports

- Desktop 1440
- Tablet 768
- Mobile 390

## Assertions

- One H1 per page.
- No horizontal overflow.
- Project page: `#nl-root` equals 1 when showroom engine is active.
- Project page: `.nlv2-showroom` equals 0 in visible render.
- No duplicate hreflang tags.
- EN and FR and RU pages are LTR.
- HE and AR pages are RTL.
- Language switch navigates to sibling URLs.
- Price is a range with a non-binding label.
- If comps are unavailable, the comps block collapses cleanly.
- Inquiry form carries selected apartment context.
- No public leak words: GLB, BIM, hotspot, mesh, token, Lovable, Codex, Featured, Sponsored.
- No em dash characters.
- Console has no page errors.
- All screenshots saved with page, language and viewport in the filename.

## Rollback proof

Before live, confirm:

- child theme can be deactivated back to `nadlan-revenue`
- orchestrator plugin can be deactivated without losing content
- `nadlan-config` remains active
- no post content is destructively rewritten
