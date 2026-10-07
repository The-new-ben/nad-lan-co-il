# live-truth: the code that runs on https://nad-lan.co.il (read 7.10.2026, plugin 1.72.432)

**Why this branch exists.** The CEO decision on HAD-443, 7.10.2026; Ben, 7.10: "consult with the CEO and start doing things".
The repo did not equal the live site. Releases patch the LIVE text of a file (the runner pattern), so main and the feature
branches drifted.

**How it was built (read-only).**
- `scripts/live_truth/live_truth.py` read every file of wp-content/plugins/nadlan-config, through one temporary admin bridge,
  with md5 checked. It also read every Code Snippet through the Code Snippets REST API.
- The bridge was deleted and its route answers 404. Nothing on the site changed.
- The branch starts from claude/apartment-experience-b1 (6c405489, the branch that released 1.72.429 to 1.72.432).
- The live files lie on top of it. The 735 rollback copies (*.bakNNN) were left out.

**The rules from here (CEO, HAD-443):**
- Every new PR targets `live-truth`.
- Old branches are not touched; aligning main is Ben's decision.
- No deploy without Ben (the loop releases under Ben's 5.10 "everything approved, publish and send links").

**Snippets:** live-truth/snippets/: 165 snippets (16 active), and their code is here.
- Exception: four snippets hold an embedded one-time token, and their code is kept out of git: 450 (x-einstein-flagship,
  active, it runs the Einstein page), and 457, 458, 459 (x-einstein-live-recovery-172207-*, active recovery routes from
  August).
- All four are gated by `current_user_can('update_plugins')` plus the token. They are logged as a finding: 457 to 459
  look obsolete, so deactivating them is the owner's call.
- About 570 temporary bridge snippets (x-tmp-*, tmp-*) are inactive leftovers and are not copied. Logged too.

## What was live and not in git, at the read

### Files whose live content differed from claude/apartment-experience-b1 (38, line endings ignored)
- assets/branding/favicon.svg
- assets/project-stage/ashira/stage.css
- assets/project-stage/ashira/stage.js
- assets/project-stage/bridge.js
- assets/project-stage/dimri/stage.css
- assets/project-stage/dimri/stage.js
- assets/project-stage/duo/stage.css
- assets/project-stage/duo/stage.js
- assets/project-stage/rainbow/stage.css
- assets/showroom-engine/buyflow.js
- assets/showroom-engine/i18n.js
- assets/showroom-engine/showroom.css
- assets/showroom-engine/studio.js
- assets/tours/designer-tour.html
- assets/urban/renewal-3d.js
- assets/urban/renewal-space.js
- i18n/stage-dict.json
- inc/auction.php
- inc/cards-render.php
- inc/directory.php
- inc/i18n.php
- inc/lead-e2e.php
- inc/matcher.php
- inc/professional-profile.php
- inc/project-experience.php
- inc/project-stage.php
- inc/rentals-manager.php
- inc/reviews.php
- inc/rfp.php
- inc/site-map.php
- inc/smart-404.php
- inc/smart-form.php
- inc/urban-hub.php
- inc/urban-map.php
- inc/urban-space.php
- inc/urban-tools.php
- inc/urban-wizard.php
- nadlan-config.php

### Files that exist only on the site (not in the branch before this commit)
- assets/rentals/guide/
- assets/rentals/help/
- assets/rentals/i18n/
- assets/rentals/rm-3d.js
- assets/rentals/rm-boot.js
- assets/rentals/rm-core.js
- assets/rentals/rm-demo.js
- assets/rentals/rm-drawers.js
- assets/rentals/rm-import.js
- assets/rentals/rm-lease.js
- assets/rentals/rm-portal.js
- assets/rentals/rm-views.js
- assets/rentals/rm.css
- inc/breadcrumbs.php.bak-had251
- inc/breadcrumbs.php.bakC1
- inc/breadcrumbs.php.bakT7
- inc/cards-render.php.bak-had251
- inc/catalog-meta.php.bak-had251
- inc/city-hubs.php.bakSEO2
- inc/claim-prompt.php.bak-had251
- inc/conversion-cta.php.bakT10
- inc/conversion-cta.php.bakT7
- inc/conversion-cta.php.bakV8
- inc/conversion-cta.php.bakV9
- inc/conversion-cta.php.bakV9B
- inc/directory-assets.php.bakT1
- inc/directory-assets.php.bakT7
- inc/directory.php.bak-had251
- inc/directory.php.bakC1
- inc/directory.php.bakDIR1
- inc/directory.php.bakSEO2
- inc/directory.php.bakT1
- inc/earth-experience.php.bakV6
- inc/feature-bar.php.bakT10
- inc/feature-bar.php.bakT9
- inc/feature-bar.php.bakV7
- inc/home-v2.php.bakT1
- inc/home-v2.php.bakV7
- inc/home-v2.php.bakV9
- inc/i18n.php.bakT7
- inc/i18n.php.bakV7
- inc/i18n.php.bakV8
- inc/legal-notice.php.bakNotice
- inc/listings-ux.php.bakT7
- inc/listings-ux.php.bakV7
- inc/mobile-nav-repair.php.bakV7
- inc/premium-ui.php.bakT7
- inc/premium-ui.php.bakV8
- inc/professional-profile.php.bak-had251
- inc/project-experience.php.bakT7
- inc/project-lang.php.bakSEO3
- inc/project-topbar.php.bakTOP1
- inc/rentals/
- inc/scheduler.php.bakT9
- inc/schema.php.bakT8
- inc/sdedov-teaser.php.bakV7
- inc/showroom-engine.php.bakT8
- inc/showroom-engine.php.bakT9
- inc/smart-404.php.bakC1
- inc/smart-404.php.bakC2
- inc/tour-routes.php.bakV5
- inc/wa-source.php.bakV8
- nadlan-config.php.bak-had251
- nadlan-config.php.bakC1
- nadlan-config.php.bakC2
- nadlan-config.php.bakNotice
- nadlan-config.php.bakSEO4
- nadlan-config.php.bakT1
- nadlan-config.php.bakT10
- nadlan-config.php.bakT7
- nadlan-config.php.bakT8
- nadlan-config.php.bakT9

### In the branch but not on the site: 6 files (kept; see the manifest)

The full listing with every md5 is in live-truth/LIVE-MANIFEST.json.
