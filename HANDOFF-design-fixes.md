# Handoff: Design, Layout, & SEO Fixes

## 1. CSS Layout Fixes (Cut-offs and Narrow Columns)
**File Edited:** `assets/css/nadlan-showroom-engine.css`
**What was done:** We added CSS rules to forcefully break the #nl-root (Showroom Engine container) out of the theme's default .is-layout-constrained class. 
**Why:** The WordPress block theme was squeezing the beautiful 3D showroom into a narrow 600px column. This caused the Rainbow GLB model to stack over the text because there wasn't enough room. Now it expands to full width.
**What else:** We added overflow-x: hidden to the body. This prevents the Mapbox container from spilling over the left side of the screen in RTL (Hebrew) mode.

## 2. SEO & Double Headline Fix
**File Edited:** `functions.php`
**What was done:** Added a filter to ender_block_core/post-title. If the page is a 
adlan_project, it completely deletes the theme's default H1 output.
**Why:** You had 'stacked over twice headlines' (English and Hebrew overlapping). The theme was printing an H1, and our Showroom Engine was *also* printing an H1. Having two H1s destroys SEO and breaks the visual layout. Now, only the premium Showroom Engine title renders.

## 3. Mapbox Facilities & 3D Restored
**Why it wasn't working:** The Rainbow 3D model was stacking because of the narrow column (fixed above). The Mapbox facilities require a valid 
adlan_mapbox_token in WordPress options to mount. As long as the token is active, mapbox-init.js takes over and renders the 3D map.

## 4. Generated Assets & Placeholders
**Location:** `assets/showroom-assets/`
**What was added:** 
- A premium, minimalistic Favicon (Gold and dark green 'N' logo).
- 5 High-resolution, photorealistic luxury interior placeholders (Living Room, Kitchen, Balcony, Bedroom, Bathroom).
**How to use:** Upload these to the WordPress Media Library. Use them as fallback images when contractors don't provide good 3D models. Map the clickable facade dots to these interior images to create a 'Zillow-like' tour instantly.

## Next Steps for the Product Team
- Merge this branch into main.
- Set the Favicon via WP Customizer.
- Verify the Yoast SEO breadcrumbs are rendering cleanly now that the duplicate H1 is gone.