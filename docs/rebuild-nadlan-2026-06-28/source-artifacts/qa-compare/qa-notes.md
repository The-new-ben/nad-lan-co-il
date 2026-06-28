# NADLAN Visual QA — Live vs Claude Design Mock
Date: 2026-06-28

## Evidence Captured
- Chrome viewport evidence: chrome-live-home-viewport.png, chrome-live-ashira-viewport.png
- Full-page live/mock captures: live-home-desktop-full.png, mock-home-desktop-full.png, live-ashira-desktop-full.png, mock-ashira-desktop-full.png, and mobile equivalents.
- Side-by-side boards rebuilt directly from image files:
  - compare-home-desktop-live-vs-mock.png
  - compare-home-mobile-live-vs-mock.png
  - compare-ashira-desktop-live-vs-mock.png
  - compare-ashira-mobile-live-vs-mock.png

## Live Version
Healthcheck: nadlan-config 1.69.56.

## Anti-Stack Checks
Live Ashira desktop:
- #nl-root = 1
- .nlv2-showroom = 0
- .nlp3d = 0
- model-viewer = 1
- horizontal overflow = false

Live Ashira mobile:
- #nl-root = 1
- .nlv2-showroom = 0
- .nlp3d = 0
- model-viewer = 1
- horizontal overflow = false

Code scan:
- De-stack filter exists in plugins/nadlan-config/inc/showroom-engine.php at the_content, with DE-STACK comments.
- Old pattern files containing nlv2-showroom still exist under patterns/project-showroom-ashira-v2*.php.
- This means live target pages are not stacked, but legacy pattern sources still exist and must not be reinserted blindly.

## Homepage Differences
What live does well:
- Live homepage is visually richer than the mock. It has the large cinematic hero, search, metric cards, project cards, investor tools, professionals, CTA and footer.
- No horizontal overflow detected on desktop or mobile.
- One H1 detected.

Mismatch versus mock:
- Mock is a clean project-gallery landing page with the NADLAN mark and simple project cards. Live is a broader marketing hub.
- Live uses the existing WordPress/site header, not the mock header.
- Live has blue cursor/helper markers visible in screenshots, probably from QA/admin overlay, not the intended buyer surface.

## Ashira Project Differences
What live does well:
- Exactly one engine renders on Ashira.
- No duplicate old showroom in DOM.
- Model-viewer exists.
- No horizontal overflow detected in the screenshot metrics.

Mismatch versus mock:
- Live page is much longer than the mock: desktop body height ~17,795px vs mock ~5,223px; mobile ~25,364px vs mock ~5,808px.
- The SEO article still dominates the page after the showroom. The mock keeps the page tighter and more product-led.
- Live top showroom is less close to the clean mock composition: the building/selector area is present, but the card/map/content hierarchy is less calm.
- The article still reads as a long wall after the product experience instead of controlled sections.
- Mobile inherits the same length problem and therefore feels heavier than the mock.

## Honest Verdict
- Anti-stack gate: PASS for the live Ashira target page.
- Visual parity with Claude mock: PARTIAL, not pass.
- Homepage: strong and probably better as a live marketing page, but not identical to the mock.
- Ashira: technically cleaner than before, but not final. The biggest remaining issue is page hierarchy and article control, not duplicate rendering.

## Next Surgical Fix Recommendation
One release only:
1. Keep the single showroom engine as-is.
2. Do not add another renderer.
3. Add an article containment layer for Ashira: styled summary sections first, collapsible/deep article lower on the page.
4. Remove or hide QA cursor/helper artifacts from public buyer pages if they are not intentional.
5. Re-run the same anti-stack check: #nl-root=1, .nlv2-showroom=0, no horizontal overflow.
