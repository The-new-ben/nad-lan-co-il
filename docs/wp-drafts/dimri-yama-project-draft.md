# Dimri Yama WordPress Draft Payload

This folder contains a prepared REST payload for creating the first Dimri Yama showroom page as a WordPress draft.

## Files

- `dimri-yama-project-draft.json` - WordPress REST payload for a draft `nadlan_project` page.
- Source pattern: `patterns/project-showroom-dimri-yama.php`
- Source assets: `assets/projects/dimri-yama/`

## Safe Use

1. Merge and deploy the theme slice first, so the theme contains the showroom CSS, JavaScript, and assets.
2. Create the WordPress post as a draft only.
3. Do not publish the page until official project material is supplied or explicitly approved:
   - official BIM/GLB or approved massing model
   - official facade/elevation
   - real inventory and availability
   - real price ranges or approved estimate language
   - contractor contact details
   - approved floor plans and interior tour links
4. After the draft exists, import `assets/projects/dimri-yama/showroom-payload.json` into the project meta only when the real post ID is known.
5. Run Chrome QA at 1440, 768, and 390 px before publishing.

## Why This Exists

The goal is to make the next project repeatable without adding more plugin risk:

- the child theme owns the showroom presentation;
- the existing plugin keeps lead capture and project data contracts;
- each new project starts from a data file, assets, a draft page, and QA screenshots.

## Current Status

This is a prototype draft payload. It is not a live deploy and it has not been published.
