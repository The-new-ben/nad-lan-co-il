# Ashira V2 Factory Readiness Gate

Date: 2026-06-27
Branch: `codex/ashira-showroom-v2-clean`

## Why This Gate Exists

The current failure mode is not only visual. A page can pass screenshots and still speak to the
wrong reader. Public project copy must address buyers and investors choosing an apartment, not our
internal build process, contractors, CMS setup, lead routing, SEO plan, or monetization.

The gate turns that rule into a repeatable check before any Ashira v2 WordPress import.

## Research Anchors

- Google Search Central: helpful content should be created for people first, with clear value for
  the intended audience.
- Nielsen Norman Group: web readers scan; pages need meaningful headings, objective language and
  scannable facts.
- Baymard Product Page UX research: product pages are decision surfaces; users need clear product
  information, availability, imagery and comparison signals.

Applied to NadLan project pages, buyer-facing copy must answer:

1. Which apartments can I compare?
2. What floor, rooms, sqm, view and direction does each apartment have?
3. What is the price context, and is it non-binding?
4. What plans, photos, video, interior tour or view can I open?
5. What is the next step if I want to check availability?

## Command

```powershell
npm run qa:ashira-factory-readiness
```

Direct command:

```powershell
node scripts\qa-ashira-factory-readiness.mjs --strict
```

## What It Checks

- Required Ashira v2 files exist.
- Asset sizes stay within prototype budgets.
- `showroom-payload.json` parses and has the required project showroom fields.
- Unit data includes id, title, label, floor, rooms, sqm, status, availability, estimate and facade
  coordinates.
- Every visible facade cell in the preview has a matching payload unit, and every payload unit is
  visible in the preview.
- Status values stay in the allowed inventory language.
- Public payload strings do not contain mojibake or internal wording.
- Preview/pattern/runtime copy does not contain visible internal wording.
- The latest screenshot report has four viewports, no failures, no horizontal overflow, one H1,
  model-viewer registration, 44px tap targets, and no visible mojibake/internal words.

## Result

Latest run:

```json
{
  "ok": true,
  "files": 9,
  "units": 5,
  "failures": []
}
```

Machine report:

`docs/qa/ashira-v2-factory-readiness-report.json`

## Honest Scope

This is a pre-import factory gate. It proves the Ashira v2 source package is ready for a controlled
WordPress import attempt. It does not prove a live WordPress page exists, that multilingual pages
were created, or that the public site changed.

After import, a separate live Chrome QA pass is still required.
