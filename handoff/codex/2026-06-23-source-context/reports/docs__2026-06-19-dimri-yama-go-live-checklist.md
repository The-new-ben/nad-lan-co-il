# Dimri Yama Go-Live Checklist

Date: 2026-06-19
Target: Dimri Yama project showroom
Current branch: `codex/dimri-yama-showroom-factory`
PR: `https://github.com/The-new-ben/nad-lan-co-il/pull/190`

## Goal Of This Checklist

Take Dimri Yama from prepared theme/data work to a live WordPress draft, then only publish after
visual QA passes. This is intentionally theme-first and avoids another plugin ZIP unless the plugin
data contract needs a separate change.

## Current Evidence

- Live plugin healthcheck is reachable and reports `nadlan-config` version `1.67.2`.
- Dimri branch is not in `origin/main` yet.
- The branch contains:
  - theme block pattern,
  - scoped theme CSS/JS,
  - prototype poster/facade/model/data assets,
  - local desktop/tablet/mobile screenshots,
  - payload validator,
  - WordPress draft payload,
  - content/SERP brief,
  - buyer/contractor/monetization journey docs.

## Go-Live Order

### 1. Merge PR #190

Merge the branch to `main`.

Do not update the plugin for this slice. It is a theme/data slice.

### 2. Pull Git On UPress

Pull the live site Git copy so the server receives:

- `/wp-content/themes/nadlan-revenue/patterns/project-showroom-dimri-yama.php`
- `/wp-content/themes/nadlan-revenue/assets/css/nadlan-project-showroom.css`
- `/wp-content/themes/nadlan-revenue/assets/js/nadlan-project-showroom.js`
- `/wp-content/themes/nadlan-revenue/assets/projects/dimri-yama/`

### 3. Create A WordPress Draft

Use:

```powershell
node scripts/apply-wp-draft-payload.mjs --payload docs/wp-drafts/dimri-yama-project-draft.json --dry-run
```

Then, only when ready to create the draft:

```powershell
$env:WP_USER='<wordpress-user>'
$env:WP_APP_PASSWORD='<wordpress-application-password>'
node scripts/apply-wp-draft-payload.mjs --payload docs/wp-drafts/dimri-yama-project-draft.json --apply
```

The script refuses non-draft payloads.

### 4. Attach / Import Project Data

Use:

- `assets/projects/dimri-yama/showroom-payload.json`

Only import the payload after the real WordPress post ID exists.

### 5. QA The Draft In Chrome

Required viewports:

- desktop 1440 px
- tablet 768 px
- mobile 390 px
- Edge mobile user agent

Required checks:

- one visible H1;
- no raw `class=` or code leak;
- no horizontal overflow;
- model and facade remain close together;
- mobile facade does not cover the model;
- selected apartment card has a dismiss path;
- apartment cells are tappable and understandable;
- form submits with selected unit context;
- no internal public wording;
- no broken Hebrew/Russian/Arabic text;
- no console errors.

### 6. External QA

Before publishing:

- Lighthouse: performance/accessibility/SEO.
- WAVE or equivalent accessibility check.
- WordPress preview source: confirm HTML is not escaped.

### 7. Publish Or Hold

Publish only as an illustrative prototype unless these owner-only materials are supplied:

- official BIM/GLB;
- official facade/elevation;
- real inventory and availability;
- real price ranges or approved estimate wording;
- official floor plans;
- contractor phone/WhatsApp/email;
- approved sales video or interior tour;
- legal approval for public wording.

## What Not To Do

- Do not upload a plugin ZIP for this slice.
- Do not publish prototype prices as official.
- Do not copy official/paid media without permission.
- Do not call the page complete until Chrome screenshots prove desktop, tablet and mobile.
