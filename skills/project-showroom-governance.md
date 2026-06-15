# Project Showroom Governance

Use this skill before changing Rainbow Tel Aviv or cloning the showroom pattern to another
`nadlan_project`. It exists to prevent the plugin from becoming the whole website and to keep
future project pages field-driven, safe to release, and easy to replicate.

## North Star

The product is a buyer-facing apartment selector:

- The buyer sees a premium project page, not a WordPress admin artifact.
- The buyer clicks apartment cells or polygons on the building/facade, not abstract dots.
- The selected apartment shows status, floor, rooms, sqm, view, non-binding price context and a
  clear next action.
- The contractor can update model URLs, poster, unit inventory, prices, drawings, video, tours and
  contact fields without a new plugin rewrite.

## Ownership Boundaries

Keep each concern in the smallest durable layer:

| Layer | Owns | Does not own |
|---|---|---|
| Plugin | CPT fields, REST payload route, sanitizers, schema emitters, showroom renderer, lead payload, feature healthcheck | Long-form article copy, every page layout, global typography, one-off marketing text |
| WordPress content | Opening paragraph, article body, FAQ text, Yoast title/meta, internal links | Renderer bugs, field registration, release packaging |
| Project asset folder | GLB, poster, facade/elevation image, unit-map JSON, drawings, surroundings, source notes | Runtime business logic |
| Theme/block template | Global header, breadcrumbs, article column width, H2/H3 typography, footer, page chrome | Project data contracts |
| QA docs | Screenshots, live gate output, known gaps, source/license notes | Runtime fixes |

Default decision: try fields/assets/content first. Touch plugin code only when the data contract or
renderer is missing or broken.

## When To Touch The Plugin

Touch the plugin only for these reasons:

- a required project field is missing from the CMS/REST contract;
- saved data is not sanitized or cannot be exported/imported by the project payload route;
- the public renderer is broken, inaccessible, overflowing, or leaking code/internal copy;
- a lead/WhatsApp/contact action does not carry the selected project/unit context;
- schema/healthcheck/release surfaces are missing or wrong;
- a bug cannot be fixed safely in content, assets, theme, or project data.

If the work is only copy, SEO title/meta, official source data, images, drawings, unit availability
or price notes, do not open plugin code first.

## Cautious Release Rule

After the 1.66.x package incident, no plugin update is allowed without this sequence:

1. One small release purpose. Do not bundle unrelated visual, data, billing and SEO changes.
2. Build only with `python scripts/build-plugin-zip.py <version>`.
3. Verify only with `python scripts/verify-plugin-release.py <version>`.
4. Confirm the header, main healthcheck, `inc/health.php`, manifest version, download URL and ZIP
   filename all match.
5. Confirm zero backslash paths and CRC OK in the ZIP.
6. Do not tell the owner to update until the preflight is green.
7. After live update, verify `/wp-json/nadlan/v1/healthcheck` and the public page in Chrome.
8. If the live site is damaged, stop feature work and restore a known clean plugin folder before
   continuing.

## Visual And Typography Gate

Project pages fail the premium gate if headings and paragraphs do not live in the same readable
column.

Required checks:

- H2/H3 headings sit directly above their paragraph content.
- No heading is visually thrown to the far right while the text is centered or left in a different
  column.
- Article body uses the `nadlan-guide` pattern or an equivalent framed content pattern, not bare
  black heading/text blocks.
- The 3D/showroom block does not force the article into a narrow vertical strip.
- Check at 1440, 768 and 390 px. A desktop screenshot taken narrow by the theme is still a bug.

If the cause is the theme content column or block template, fix it in theme/block/page assembly, not
by adding more plugin CSS overrides.

## Image, Poster And Search Result Gate

Every project needs a stable visual identity:

- Use an HTTPS poster or featured image that loads publicly.
- Use a project-specific OG image or poster; do not let search/social previews fall back to a blank
  or missing image.
- If the image is generated or illustrative, label it as a simulation/illustration in the page
  copy.
- Do not copy paid-source photos or subscription data into public assets without owner approval.
- For a "3D model available" visual claim, the public page must actually render the model or an
  honest interactive facade selector.

## Clone-Ready Project Factory

Do not clone Rainbow by copying rendered HTML. Clone the data contract:

1. Create the project folder with `node scripts/init-project-showroom.mjs <slug> --post-id <id>`.
2. Fill `source-notes.md`, `unit-map.json`, `drawings.json`, `environment.json`,
   `view-layer-config.json`, model/poster/facade URLs and `qa.md`.
3. Build and validate `showroom-payload.json`.
4. Import through the authenticated showroom payload route only after live healthcheck proves the
   route is available.
5. Run the live showroom gate and the stricter template gate.
6. Save the gate output in `docs/qa/`.

If any of these are red, the project is a prototype, not a factory source.

## Multilingual Rule

English, French, Russian or other language versions are separate buyer pages, not automatic shells.

Before adding `hreflang`:

- decide the URL structure;
- translate the visible copy, legal disclaimers, price notes and FAQ accurately;
- keep the same source facts and schema intent;
- do not invent prices, availability, financing or tax rules in translation.

## Revision Log

- 2026-06-15 - Added after the Rainbow 1.66.x stabilization work to capture plugin-boundary,
  release-safety, typography, image, translation and clone-readiness rules for future project pages.
