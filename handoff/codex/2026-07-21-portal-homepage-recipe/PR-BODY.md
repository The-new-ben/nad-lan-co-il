## Summary

- add a dated competitor corpus covering 39 Israeli, global, off-plan and luxury benchmarks
- define one canonical image-rich NadLan portal recipe
- specify homepage, project card, project page, WordPress content governance, freshness, asset rights, foreign-buyer and 3D contracts
- add a formal Hebrew developer marketing plan and presentation-readiness gate
- add five static review views plus desktop/mobile screenshot evidence

## Important boundary

Documentation and review artifacts only. This PR does **not** change the WordPress theme, plugin, templates, REST data, users, application passwords or live content. It is not a deployable homepage implementation.

All project-like media in the previews is existing repository concept/prototype material and is visibly labelled illustrative. Official developer-approved media is still required before external presentation.

## QA

- 10 full-page Chromium captures: five pages at 1440px and 390px
- no missing images or browser errors
- no page-level horizontal overflow after fixing the Studio review page at 390px
- HE pages render RTL with Heebo/Frank Ruhl Libre; foreign-buyer page renders LTR

See `handoff/codex/2026-07-21-portal-homepage-recipe/screenshots/QA.md`.

## Review order

1. `README.md`
2. `START-HERE.html`
3. `spec/portal-recipe.md`
4. five files under `preview/`
5. `spec/presentation-readiness.md`

## After approval

Select a launch cohort, obtain rights-cleared assets and verified facts, then open a separate implementation branch. No merge or deployment is requested from this draft PR.
