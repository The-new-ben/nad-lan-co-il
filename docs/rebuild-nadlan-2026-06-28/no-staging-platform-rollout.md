# No-Staging Platform Rollout

Date: 2026-06-28

## Situation

There is no staging server.

Therefore the platform package must ship as a production-safe preview, not as a blind public change.

## What Was Implemented

Two installable packages are now built from source:

- `plugin-dist/nadlan-platform-orchestrator-0.1.1.zip`
- `theme-dist/nadlan-platform-child-0.1.1.zip`

The orchestrator plugin is safe by default:

- It does not register `nadlan_showroom_engine`.
- It delegates to the existing `nadlan-config` showroom engine.
- Homepage project band is off by default.
- Logged-in admins can preview the homepage band with `?nlpo_preview=1`.
- Public copy avoids internal terms.

The child theme is presentation-only:

- Parent theme remains `nadlan-revenue`.
- It does not contain business logic.
- It does not insert the homepage project band automatically.

## Production Rollout Steps

1. Pull the GitHub branch on the server or upload the two ZIPs manually.
2. In WordPress, upload and activate `NadLan Platform Orchestrator`.
3. Confirm public homepage is unchanged.
4. While logged in as admin, open `https://nad-lan.co.il/?nlpo_preview=1`.
5. Screenshot desktop and mobile.
6. If the preview is visually approved, upload `NadLan Platform Child`.
7. Use WordPress theme live preview first when possible.
8. Activate the child theme only if the preview is acceptable.
9. Re-check:
   - `/`
   - `/projects/`
   - `/projects/ashira-sde-dov/`
   - `/projects/ashira-sde-dov-en/`
   - one calculator
   - one professional page
   - one guide
10. Only after screenshots pass, enable the homepage project band in Tools > NadLan Platform.

## Rollback

If anything looks wrong:

1. Deactivate `NadLan Platform Orchestrator`.
2. Switch theme back to `NadLan Revenue`.
3. Clear cache.

No database rewrite is required for rollback.

## Anti-Stack Gate

Before public enablement:

- `#nl-root = 1` on showroom project pages.
- `.nlv2-showroom = 0`.
- no duplicate project band on homepage.
- no duplicate `nadlan_showroom_engine` shortcode registration.
- no public internal words such as lead, funnel, CMS, GLB, BIM, mesh, token, Codex, Lovable.
- no horizontal overflow at 1440px and 390px.

## Honesty Note

This is not a replacement for a staging server. It is the safest workable method when staging does not exist.
