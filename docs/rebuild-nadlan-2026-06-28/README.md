# NADLAN Rebuild 2026-06-28

This folder is the rebuild control room. It stores the uploaded design bundles, screenshots,
prompts, QA comparisons, repo knowledge map, and the rebuild plan before any new theme work starts.

The purpose is to stop stacking patches on the current site and move to a controlled rebuild:
preserve the current theme as a backup, build the next NADLAN theme/design system in a clean branch,
wire the existing real-estate data and showroom engine into it, and verify every public page with
browser screenshots before live activation.

## Source Folders

- `source-artifacts/downloads/` - bundles, mockups, screenshots, HTML prototypes and support files
  supplied from the local Downloads folder.
- `source-artifacts/attachments/` - pasted prompt/report files captured from the Codex attachment
  store.
- `source-artifacts/temp-screenshots/` - recent visual screenshots from the local temp folder.
- `source-artifacts/qa-compare/` - live-versus-mock screenshots and QA notes captured before this
  rebuild planning step.
- `source-artifacts/artifact-manifest.json` - generated file inventory.

## Control Documents

- `artifact-index.md` - what was preserved and why it matters.
- `repo-knowledge-map.md` - the repo-native reports, skills, specs, assets and code seams to use.
- `anti-stack-release-rules.md` - the release rules that prevent repeating the earlier failures.
- `rebuild-master-plan.md` - the practical rebuild plan, broken into controlled layers.

## Rebuild Principle

The new build is not a visual mockup exercise. NADLAN is a real-estate authority site first:
project pages, area pages, investor content, tools, professionals, and listings. The 3D showroom is
a premium module inside that system, not a replacement for the SEO and content platform.

The current production theme/code must remain recoverable until the new theme has passed visual,
SEO, language, and anti-stack QA.
