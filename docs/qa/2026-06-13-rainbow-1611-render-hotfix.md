# Rainbow v1.61.1 Render Hotfix QA

## Live Defect Reproduced

Target: https://nad-lan.co.il/projects/rainbow-tel-aviv/

Live healthcheck before the fix reported `version=1.61.0`. After the owner hard-refreshed with Ctrl+Shift+R, the defect persisted, so this was not a browser-cache issue.

Desktop 1440px live DOM proof:

- `.nlp3d`: present at `x=23 y=772 w=1380 h=3511`.
- `.nlpf`: missing from the DOM as an element.
- Visible text node on the page: `class="nlpf" dir="rtl" style="--pc:#334236;--ps:#F1F4EE">`.
- Article H1 pushed down to roughly `y=4530`.
- Drag technically changed the scene angle, but the malformed markup and giant console made the user experience feel jammed.

Mobile 390px live DOM proof:

- `.nlp3d`: present at `x=26 y=564 w=374 h=5787`.
- `.nlpf`: missing from the DOM as an element.
- Same visible `class="nlpf"...` text node.
- Article H1 pushed to roughly `y=6762`.

Screenshots captured from the live v1.61.0 page are in:

- `docs/qa/screenshots-2026-06-13-rainbow-live/desktop-1440-top.png`
- `docs/qa/screenshots-2026-06-13-rainbow-live/desktop-1440-post-refresh.png`
- `docs/qa/screenshots-2026-06-13-rainbow-live/desktop-1440-stage-view-click.png`
- `docs/qa/screenshots-2026-06-13-rainbow-live/desktop-1440-after-interactions.png`

## Root Cause

`nadlan_p3d_insert_after_project_header()` searched for the substring `class="nlpf"` and inserted the 3D module at that offset. Because the directory project profile header is prepended as an HTML string before the 3D content filter runs, this split the opening `<div class="nlpf"...>` tag after `<div `. The browser then rendered the remaining attributes as visible text and the original profile card was not parsed as `.nlpf`.

## Fix

1. Insert before the full `<div class="nlpf"...>` opening tag using a regex with `PREG_OFFSET_CAPTURE`, instead of splitting at the `class` attribute.
2. Contain the 3D buyer console height at desktop, tablet, and mobile breakpoints so the module cannot push the article headline thousands of pixels down before the project content.
3. Hide the stage selected-unit card until a buyer actually selects a unit, dock it to the side when shown, prevent it from stealing facade clicks, and exclude it from model-drag pointer handling.
4. Keep the release surgical: no schema changes, no content changes, no new routes.

## Post-Deploy Gate

After v1.61.1 is installed live:

1. Healthcheck returns `version=1.61.1`.
2. On `/projects/rainbow-tel-aviv/`, no visible text contains `class="nlpf"`.
3. `document.querySelector('.nlpf')` exists.
4. `.nlp3d` appears before `.nlpf`, but not inside its opening tag.
5. At 1440px, `.nlp3d-console` height is bounded to the stage height and does not create a multi-thousand-pixel blank/console column before the H1.
6. At 390px, no horizontal document overflow and the article title is reachable shortly after the module.
7. Building drag still changes `--angle`.
8. Stage view button still opens the Mapbox view when a token is configured.
9. The stage card is hidden on initial load, appears after selecting a floor/unit, and does not block facade hotspot clicks.

## Local Checks

- JavaScript extraction passed `node --check`.
- `git diff --check` passed with Windows CRLF warnings only.
- ZIP rebuilt as `plugin-dist/nadlan-config-1.61.1.zip`.
- ZIP has 130 entries, rootless `nadlan-config/` prefix, zero backslash paths, and includes `nadlan-config/inc/project-3d.php`.
- Packaged markers confirm the `.nlpf` full-opening-tag regex, bounded console CSS, and `Version: 1.61.1`.
- Header, healthcheck, manifest, and ZIP filename align at `1.61.1`.
- PHP lint remains a deploy-gate item because this Windows shell has no PHP binary.
