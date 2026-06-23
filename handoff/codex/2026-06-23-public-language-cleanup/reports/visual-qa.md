# Nadlan3D Public Language Cleanup Visual QA

Date: 2026-06-23

Scope:

- Clean visible language in the prototype so public pages do not expose build terms, internal ranking labels, model file formats, font names, or prompt-style wording.
- Verify Hebrew and English pages on desktop and 390px mobile.
- Save screenshots and a rendered text scan under this handoff folder.

## What changed

- Hebrew CTA changed to `סיור בפרויקט`.
- Hebrew headline changed from `שלוש דקות בפנים, החלטה ללא שיווץ` to `שלוש דקות בפנים, החלטה בלי ניחושים`.
- Public card labels no longer show model file terms or internal placement names.
- Paid placement remains transparent using buyer-facing words such as `מודעה`, `מקודם`, and `Ad`.
- The project viewer now stops claiming a model is live when the model file is missing. It shows `המודל ממתין להעלאה` instead.
- Metadata and error states were cleaned so social/search previews do not use internal language.
- Mobile apartment drawer labels were localized in Hebrew.

## Verification

Command results:

- Build: passed with `npm run build`.
- Rendered text scan: 18 screenshots, zero banned public-language hits.
- Overflow scan: zero measured horizontal overflow failures.

Generated evidence:

- `screenshots/` contains 18 full-page screenshots.
- `data/rendered-text-and-overflow-scan.json` contains the rendered text and overflow scan.
- `exports/public-language-cleanup-visual-qa.html` is the owner-readable gallery.

Screenshots covered:

- Home, listings, project tour, and Tel Aviv city page.
- Hebrew and English.
- Desktop 1440px and mobile 390px.
- Hebrew mobile menu open.
- Hebrew project-tour unit drawer open.

## Visual readout

Passed:

- Public pages no longer show model file jargon, exposed font names, internal ranking words, or prompt-like phrasing.
- Mobile 390px screens do not horizontally overflow in the captured states.
- The Hebrew homepage CTA now uses the Hebrew project name.
- The project-tour missing-model state is now honest and no longer says the model is live.
- The apartment drawer is usable on mobile and the action buttons stay inside the viewport.

Not contractor-ready yet:

- Project images are still generic demo imagery and must be replaced with real project images, renders, or approved visual assets before showing this as a serious contractor sales surface.
- The project-tour fallback facade is clean but simple. It is evidence of state handling, not a premium 3D experience.
- The real model file for Rainbow is not present in this prototype, so the viewer correctly shows a pending model state.
- The brand mark and visual identity still need a stronger premium pass before becoming the final public design system.

Decision:

This pass is acceptable as a language and QA discipline cleanup. It is not yet acceptable as the final showroom redesign.
