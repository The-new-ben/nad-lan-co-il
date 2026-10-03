# Project page checklist (every agent, every project page, every release)

**Owner law, restated 27.9.2026:** we rank because Google finds the content, the keywords and the intent. People want the information up front too. So on every project page, on every screen width, phones first, the order is:

1. **the H1**: the project name in Hebrew and English;
2. **the answer paragraph**: 4-7 lines, keywords first;
3. **the buttons**;
4. **the stage** (the building, the showroom);
5. **the view and the map**, attached under the stage;
6. **the facts**;
7. **the rest of the tools**;
8. **the article**.

Technical things (a 3D stage, maps, code) never come before the answer paragraph, not in the source and not on the screen. The stage does not go down to the end either: it follows the paragraph at once.

**Why this file exists.** On 25.9.2026 (release 1.72.278, design system v33) the view and the map were moved right under the stage. On a phone that pushed the answer paragraph to 2,400px, below the stage, the view and the map. The source order was still right, and the only check looked at the source. Google indexes the phone version, so the rendered order is what counts. Fixed in 1.72.284 (design system v38).

## Before any change (the gates)

- **G1. Claude Design first.** Every visual or page change starts as a new version in the design system artifact (https://claude.ai/artifact/L9Nqz7Viv7K3MYeZrBc9s8): the README and the preview, published and looked at. Only then code.
- **G2. Read this file and the full recipe:** `docs/research/2026-09-24-rainbow-run/unit-layer-and-recipes.md`, section 3 (rules A1-A13, the page's 30 rows, the 67 selection checks).
- **G3. The iron laws** in `CLAUDE.md` (Claude) and `AGENTS.md` (every agent):
  - no invented facts;
  - marketing data as published, with its source;
  - illustrations labelled;
  - EcoCity never;
  - no noindex;
  - the URL word law.

## The content rules (the checks that failed once must never fail again)

| # | Rule | How it is checked |
|---|---|---|
| C1 | One H1, **visible**, first in the body, with the project name in Hebrew and English. The fleet's review-mode pages get it from `nadlan_pt_compose` (1.72.285) | the runner's `H1_EXACTLY_ONE` and ORDER; `tools/source_audit.py` |
| C2 | The answer paragraph (`.nl-lead`) is the first paragraph after the H1 **in the source**. It carries every name (he+en), the developer, the exact place, the status, the unit mix, a real price with its source and date, and what the page lets you do. No disclaimer comes before it | the runner's ORDER check (the source position) |
| C3 | **The answer paragraph comes before the stage on the screen, on every width**. On a 412px phone its top is above the stage's top and inside the first 1.2 screens; on desktop it is in the first screen | `python tools/content_first_check.py` (rendered, a mobile Googlebot user agent at 412×915 and desktop 1440×900); the runner needs the phone grid `"hero" "lead" "cta" "stage"` |
| C4 | The stage follows the paragraph and the buttons at once (on a phone its top is within the first 1.5 screens). It is never pushed to the end | `tools/content_first_check.py` |
| C5 | The view and the map are attached under the stage (the owner's standing order), after the paragraph, never before it | the same |
| C6 | The article (5,000+ words, written by the owner's ChatGPT) follows the tools, never replaced by them; its word count never drops | `tools/source_audit.py` (bytes and words), the release's page checks |
| C7 | The non-affiliation notice opens the article section, out of the snippet zone (the owner, 29.8.2026) | `tools/source_audit.py` (the notice light) |
| C8 | One map on the page; one `FAQPage`; one `BreadcrumbList` | the runner and the audit |

## After every release (the evidence)

- `python tools/source_audit.py`, before and after. An unexplained difference is a finding.
- `python tools/content_first_check.py`: every project page with a stage passes C3 and C4.
- The live click journey on desktop and phone, looked at. Screenshots go to the owner.

## Where this checklist lives

- **In the repository:** this file, for every agent. `AGENTS.md` and `CLAUDE.md` point here.
- **In the design system:** ProjectStage README, the content-first law at its top.
- **In WordPress:** the project edit screen shows this checklist in a box, so a person editing a project meets it too.
- **With Codex:** `docs/coordination/claude-codex.md`.

## C7: research before writing (owner law, 3.10.2026)
| # | Check | Evidence |
|---|---|---|
| C7 | Before the brief goes to ChatGPT or a writer: 1-5 owned intents and synonyms; a URL-ownership/cannibalization check; manual Google in the target language; the top 4-5 competitor pages read in full (URLs and times); the questions, suggestions and AI answers actually shown ("absent" if none) | an internal research file `docs/research/<date>-<slug>/serp-<lang>.md` |
