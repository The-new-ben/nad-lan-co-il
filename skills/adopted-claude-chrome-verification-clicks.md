# Adopted: Chrome verification clicks under renderer stress (Claude, 2026-08-13)

> Physical clicks kept "missing" a button that JS could click fine. Three
> separate traps stacked on the same page (GLB + Mapbox + smooth scroll),
> and each one alone can silently kill a coordinate click.

## The traps

1. **Two coordinate spaces.** CDP screenshots are captured in screenshot
   pixels (e.g. 1568 wide) while `getBoundingClientRect()` returns CSS
   pixels (e.g. innerWidth 1475). Clicking JS-measured coordinates without
   scaling misses by ~6%. Convert: `shot_x = css_x * (shotW / innerWidth)`.
2. **Moving targets.** Deeplink smooth-scroll and late-loading sections keep
   shifting layout for seconds after "load". A coordinate measured even one
   action earlier can be stale. Any screenshot→click gap is a race.
3. **Stale compositor frames.** Under heavy load (satellite tiles, GLB,
   rAF camera loops) `Page.captureScreenshot` times out (30s) or returns
   blank cream frames after programmatic `scrollTo`. The DOM is fine — the
   compositor is behind.

## The laws

- **Deterministic activation:** `element.focus()` via JS, then a PHYSICAL
  Enter key. Fires the same click handler, immune to coordinates, and
  doubles as a keyboard-accessibility proof. This is the reliable way to
  press a specific control on a stressed/shifting page.
- After any programmatic scroll jump, force a repaint with two real scroll
  ticks (down 2, up 2) before screenshotting — cures the blank-frame lie.
- CDP screenshot timeout = wait 10s, retry once; it recovers.
- Verify outcomes via DOM state JS probe immediately after the interaction
  (dialog class, canvas presence), then confirm LOOK with the screenshot.
  JS probe alone is never "done" (visual proof loop law).

## Related

- skills/adopted-codex-visual-proof-loop.md
- skills/adopted-claude-hebrew-payload-verification.md
