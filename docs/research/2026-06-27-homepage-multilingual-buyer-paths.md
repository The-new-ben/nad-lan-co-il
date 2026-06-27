# Homepage Multilingual Buyer Paths - 2026-06-27

## Purpose

This note supports the homepage slice in PR #220. The public page must speak to buyers and investors, not to the build team. The homepage should help a visitor search, compare projects, understand a sample apartment, and find a language path without exposing internal implementation language.

## Sources Checked

- Google Search Central, localized versions: `https://developers.google.com/search/docs/specialty/international/localized-versions`
- Zillow homepage pattern: `https://www.zillow.com/`
- Rightmove homepage pattern: `https://www.rightmove.co.uk/`
- Madlan Israel property discovery pattern: `https://www.madlan.co.il/`

## Design Decision

1. Keep search and the project catalog high on the page.
   - Zillow and Rightmove both lead with property discovery and clear user paths.
   - The NadLan homepage therefore keeps a search-like opening and places project comparison above the first fold, but not as the first pixel of the page.

2. Put the interactive project showroom early, without making it the page top.
   - Desktop has room for the project comparison rail and the showroom in the first screen flow.
   - Tablet and mobile do not. The compact rule is now: opening promise first, language controls second, interactive showroom third, project cards after it.
   - This follows the same buyer logic visible on large property portals: search or compare first, then quickly reach an inspectable home or project experience.
   - The layout is intentionally different by viewport because a stacked mobile project card list delayed the actual apartment-selection experience too far down the page.

3. Add practical buyer paths below the showroom.
   - Buyers need to know what to check: availability, price estimate, surroundings, and documents.
   - These cards add content depth without turning the top of the page into a long article.

4. Treat multilingual as a route structure, not a cosmetic chip.
   - Google's localized-version guidance points toward separate language URLs and reciprocal language annotations when translated pages exist.
   - This PR adds visible language target sections so the current chips land somewhere real.
   - The project selector itself now has real language controls: project cards and the selected apartment panel can switch between Hebrew, English, French, Russian and Arabic.
   - It does not claim full multilingual SEO until separate English/French/Russian/Arabic pages are written, linked, and annotated.

5. Keep public language clean.
   - Visible text must not say SEO, CMS, engine, template, prototype, supplier, contractor, lead, funnel, monetization, or other internal words.
   - Public text speaks about apartments, projects, availability, price estimates, surroundings, documents, and contact with a representative.

## 2026-06-27 Placement Update

- Owner request: embed the multi-project experience above the fold, but not as the very top of the homepage, and make it multilingual.
- Implemented behavior:
  - Hero promise remains first.
  - A five-language control sits immediately under the hero and controls the project engine itself.
  - Desktop keeps project comparison before the showroom.
  - Tablet and mobile place the showroom before the card rail so the buyer reaches the model and apartment picker earlier.
  - The QA gate now fails if the interactive showroom starts too low in the homepage flow.

## 2026-06-27 Above-Fold Language Update

- The same five-language control now also changes the visible homepage opening promise, search labels, search value, aria labels and CTA buttons.
- The hero section receives the selected `lang` and `dir`, so English/French/Russian render LTR while Hebrew/Arabic render RTL.
- This is still a preview-layer language path, not a full international SEO launch. Full SEO launch still requires separate language URLs and reciprocal language annotations.
- The browser QA now fails if English/French/Russian/Arabic update only the project engine while leaving the above-fold promise in Hebrew.
- Research anchors:
  - Google recommends separate URLs and `hreflang` annotations for localized versions; this slice keeps language switching as a preview path and does not claim full multilingual SEO until the separate language pages are published.
  - Zillow and Rightmove both keep property discovery/search prominent on the homepage.
  - Homes.com presents 3D/Matterport and floor-plan experiences as part of the buyer decision path, which supports bringing the showroom into the early homepage experience rather than burying it below long text.

## Current Implementation Evidence

- Pattern: `patterns/nadlan-home-showroom.php`
- CSS: `assets/css/nadlan-home-showroom.css`
- Browser QA: `scripts/qa-home-showroom-preview.mjs`
- Pattern QA: `scripts/qa-home-showroom-pattern.mjs`
- Screenshot folder: `docs/qa/screenshots/home-showroom-preview-2026-06-27/`

## Not Yet Done

- Separate translated long-form pages for French, Russian, and Arabic.
- Reciprocal `hreflang` output.
- 3000-word project pages per language.
- Live WordPress render verification after the branch is installed.
