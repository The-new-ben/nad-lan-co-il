# Ashira Factory Run1 Engine Intake

Date: 2026-06-26

## Verdict

The `NadLan Ashira Factory Run1.zip` package can help, but only as a controlled engine and asset reference.
It is not a production WordPress import as-is.

What I accepted:

- `rainbow.glb`, `dimri.glb`, and their posters as lightweight prototype model assets.
- The multi-project idea: one compact selector that can appear on a homepage, project archive, or project page.
- The data shape idea: projects, models, units, status, price estimate, view note and CTA stay in data.

What I rejected:

- Generated `.dc.html` pages as production code.
- `support.js` as a direct runtime import.
- Any public language that speaks to us, the contractor, CMS, SEO, an engine, a template, or a lead system.

## Buyer-Language Correction

The public page must address only people considering apartments: families, Israeli buyers, investors, and foreign buyers.
They care about location, floor, view, rooms, sqm, price estimate, availability, plans, interior media, surroundings and the next inquiry step.

Forbidden public words include:

- SEO
- CMS
- CRM
- lead / leads
- engine / template / prototype
- funnel / monetization / paid placement
- פאנל / מנוע / תבנית / לידים
- project manager / supplier / contractor as internal audience labels

Allowed public words include:

- דירה
- קומה
- נוף
- מחיר
- אומדן לא מחייב
- זמינות
- תוכנית
- סיור
- דברו עם היזם
- בדיקת רכישה לא מחייבת

## Why This Direction Is Still Useful

The preview now supports a buyer-first archive/homepage pattern:

1. Compare Sde Dov projects visually.
2. Choose a project.
3. Rotate the model for spatial context.
4. Pick an apartment from obvious floor/unit choices.
5. See the selected apartment facts.
6. Send an inquiry with the chosen apartment attached.

This is suitable for a homepage or project-search teaser. The detailed project page still needs the full v2 contract:
official or generated poster, short buyer intro, rotating context GLB, adjacent facade picker, selected-apartment card,
media panel, surroundings, article content and multilingual SEO pages.

## Honest Technical Limit

Exact apartment clicking on the spinning GLB requires a model where apartments or floors are named/segmented meshes.
The Run1 GLBs are prototype massing files. They can rotate and show context, but they are not official BIM and do not
contain apartment geometry. Until a segmented GLB exists, the correct architecture is:

- GLB = context surface.
- Facade/elevation or clear floor/unit selector = apartment selection surface.

## Research Anchors Used

- Google Search Central helpful-content guidance: create people-first content and avoid search-engine-first pages.
  https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Nielsen Norman Group plain-language guidance: write in the user's words, not internal or expert jargon.
  https://www.nngroup.com/articles/plain-language-experts/
- model-viewer hotspots/annotations pattern: use model annotations when the 3D asset supports meaningful points.
  https://modelviewer.dev/examples/annotations/
- Matterport real-estate media pattern: interior tours and walkthroughs answer buyer confidence questions after a listing is chosen.
  https://matterport.com/industries/real-estate

## Next Step

Keep this preview as proof and port the pattern only after the Ashira v2 project page contract is stable.
Do not stack it onto Rainbow or Ashira CSS. Use a clean root and data-driven rendering.
