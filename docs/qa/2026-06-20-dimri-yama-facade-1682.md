# Dimri Yama Facade Release 1.68.2

## Goal

Replace the Dimri missing-facade state with a packaged, original concept facade bitmap while official developer/BIM material is still missing.

## Scope

- Dimri Yama only.
- No fake CSS/SVG square-grid facade revived.
- Official CMS-provided `project_3d_facade_images` always wins over the packaged concept.
- Concept is explicitly labeled as generated and not official developer material.

## Asset

- `plugins/nadlan-config/assets/projects/dimri-yama/dimri-yama-premium-facade-concept.jpg`
- `plugins/nadlan-config/assets/projects/dimri-yama/dimri-yama-premium-facade-concept.webp`

## Verification

- `php -l plugins/nadlan-config/inc/project-3d.php` clean.
- `php -l plugins/nadlan-config/inc/health.php` clean.
- `php -l plugins/nadlan-config/nadlan-config.php` clean.
- Inline `nadlan_p3d_inline_js` extracted and `node --check` clean.
- `node scripts/validate-project-showroom-payload.mjs --payload assets/projects/dimri-yama/showroom-payload.json` clean.
- `python scripts/build-plugin-zip.py 1.68.2` clean: 132 entries, zero backslash paths, rooted under `nadlan-config/`, CRC OK.
- `python scripts/verify-plugin-release.py 1.68.2` clean.
- ZIP contains both facade assets.

## Product References Checked

- Render Vision apartment viewer: building/future-environment view with apartment-level information in a few clicks. https://render-vision.com/apartment-selector/
- Homes.com Matterport: interior tour plus floor-plan experience. https://www.homes.com/solutions/matterport
- Zillow 3D Home: buyer-facing 3D tour capture and presentation pattern. https://www.zillow.com/3d-home/
- Image Map Pro real-estate tutorial: uploaded building image with interactive mapped areas. https://www.imagemappro.com/tutorials/real-estate

## Honest Limitation

This is a generated concept facade, not official Dimri/developer material. It exists to make the selector usable and honest while waiting for official elevation/BIM assets. The correct long-term path is still to replace this URL with contractor-supplied material through the CMS.
