# Premium Catalog Redesign Spec

Date: 2026-06-04
Status: Draft implementation target for Claude review.
Scope: catalog and profile visual system only. No URL changes. No plugin code in this PR.

## Objective

Move the Nadlan catalog system from â€œWordPress directory with colorful pillsâ€ to a first-class real-estate product experience. The target is not decoration. The target is trust, desirability, scan speed, and advertiser value.

This spec covers:

- `/projects/`
- `/professionals/`
- single `nadlan_project` pages
- single `nadlan_professional` pages
- sponsored/available premium slots
- generated fallback assets for listings without photos

## Design Position

The current system says: â€œHere is a database row.â€
The new system should say: â€œThis is a verified real-estate opportunity worth attention.â€

The direction is closer to Zillow Showcase, Compass, The Modern House, Sothebyâ€™s International Realty, LoopNet, Madlan developer pages, Houzz professional profiles, Realtor.com, realestate.com.au, and Idealista:

- image-first
- restrained typography
- serious trust signals
- quiet controls
- no emoji identity
- premium state visible through layout, not a small badge only

## Typography Scale

Use a split system:

- Serif display for editorial project/professional names and premium hero moments.
- Sans-serif UI for filters, facts, buttons, chips, metadata, forms, and dense scan surfaces.

Recommended scale:

| Use | Desktop | Mobile | Notes |
| --- | ---: | ---: | --- |
| Single profile H1 | 44-56px | 30-36px | Serif, line-height 1.05-1.15. Avoid oversized text inside compact panels. |
| Catalog page H1 | 38-48px | 30-34px | Serif or refined sans. Keep category pages useful, not landing-page theatrical. |
| Card title | 20-24px | 18-20px | Strong, two lines max, no negative letter spacing. |
| Card price/key fact | 18-22px | 17-19px | If price exists, it outranks category. For projects, use units/status/developer. |
| Body / description | 16-18px | 16px | Minimum mobile content text 16px. |
| Metadata | 13.5-15px | 14px | Never below 14px on mobile for meaningful text. |
| Labels / badges | 11-12px | 11-12px | Use sparingly, uppercase only for English. Hebrew labels should remain readable. |
| Button text | 14.5-16px | 15-16px | Tap targets minimum 44px high. |

## Color Palette

Move away from the current bright cyber pills and childish icon colors.

Base neutrals:

- Ink: `#11110F`
- Charcoal: `#2B2924`
- Warm gray: `#6D665C`
- Hairline: `#DDD6C8`
- Surface: `#FAF8F3`
- Card: `#FFFFFF`
- Soft band: `#F3EFE7`

Premium accents:

- Old gold: `#9C7A3C`
- Champagne: `#D7C39A`
- Deep olive: `#334236`
- Deep sea: `#183C3C`
- Clay: `#9F6F54`

Rules:

- Do not use emoji as visual identity.
- Do not use hot pink/bright blue category pills as the dominant catalog language.
- Accent color should mark interaction or premium state, not flood every card.
- Sponsored/premier state may use old gold, but should still be mostly neutral and image-led.

## Catalog Card Anatomy

### Project Card

Priority order:

1. Image or generated architectural fallback.
2. Project name.
3. City/neighborhood.
4. One strongest fact row: units, towers/floors, status, developer.
5. Status/verification chips.
6. CTA or affordance.

Recommended layout:

- Image ratio: 4:3 for compact grid, 16:10 for featured cards.
- Card radius: 6-8px maximum.
- Gutters: 16px mobile, 20-24px tablet, 28px desktop.
- Title area: 2-line clamp.
- Fact row: max 2 lines before card grows.
- Footer: one trust mark plus one action, not three tiny facts.

Premium project card:

- Larger image ratio or two-column card at `900px+`.
- Quiet `Premier` or `Showcase` label in image corner.
- Extra proof line: developer, verification date, or â€œeditorial showcaseâ€.
- No separate cheap badge as the only premium sign.

### Professional Card

Priority order:

1. Logo/headshot/work image or generated monogram.
2. Professional/company name.
3. Specialty and city/service area.
4. Credential/registry/license proof.
5. Review/response proof if available.
6. CTA.

Rules:

- Hide empty review copy on cards unless it is specifically useful.
- Replace repeated â€œbe first to rateâ€ states with proof-first content.
- If no real media exists, use a generated neutral monogram or category illustration.
- Registry proof should be a designed trust chip, not a tiny footer.

## State Design

Hover:

- Lift no more than 2px.
- Add subtle image zoom or tonal overlay.
- Do not use flashy gradients.

Focus:

- Visible 2px outline with strong contrast.
- Preserve RTL focus order.
- Focus ring must not be clipped by card overflow.

Loading:

- Use skeleton rectangles matching final image/title/fact geometry.
- Avoid spinner-only loading.
- Keep dimensions stable so layout does not jump.

Empty:

- Empty directories should show a calm editorial empty state with one clear next action.
- Empty professional reviews should not dominate public cards.
- Empty photos should generate a tasteful fallback asset, not an icon.

Sponsored:

- `.nldc-sponsored-spot` should look like a premium ad slot, not an unfilled print box.
- It should communicate the value sold: location, expected exposure, package, and CTA.
- Sponsored cards need the same image-first quality as organic cards.
- â€œAvailable sponsored spotâ€ should feel desirable, not cheap.

## Filter Bar Treatment

Replace the current glassy `.nldir-pill` pattern with a quiet, real-estate control surface.

Desktop:

- Search input first.
- City/neighborhood field.
- Category/status segmented control.
- Advanced filter button.
- Sort control.
- Count/result summary in text, not a giant decorative number.

Mobile:

- Top row: search field and filter button.
- Filters open in a bottom sheet.
- Active filters appear as compact removable chips under search.
- Tap targets minimum 44px.
- Avoid sticky controls covering content.

Filter design:

- White or warm surface with hairline borders.
- Active state can use ink text with gold underline or soft neutral background.
- No emoji in filters.
- No full hero gradient needed for utility catalog pages.

## Single Profile Hero

### Project Hero

Desktop:

- Full-width media hero or large left media with right fact panel.
- H1, city/neighborhood, developer, status, and verified source above fold.
- Fact strip: units, towers/floors, status, developer, address, last verified.
- CTA cluster: â€œ×§×‘×œ×ª ×ž×™×“×¢â€, â€œ×©×™×—×” ×¢× × ×¦×™×’â€, â€œ×©×ž×™×¨×ª ×¤×¨×•×™×§×˜â€ if supported.
- Gallery visible early.

Mobile:

- Image first.
- H1 directly below image.
- Fact chips in horizontal scroll or two-column grid.
- Primary CTA sticky only if it does not cover content and respects safe area.

### Professional Hero

Desktop:

- Logo/headshot/work image.
- Name, specialty, city/service area.
- Credential/registry proof.
- Review summary only if real.
- Primary CTA plus secondary call.
- Portfolio/recent work before claim/admin prompts.

Mobile:

- Identity block first.
- CTA stack full width.
- Hide claim form behind a secondary link unless profile owner intent is detected.

## Generated Asset Plan

For advertisers or cards without photos:

Project fallback:

- Use generated architectural render-like abstract image.
- Keep it clearly illustrative if not a real render.
- Ratio: 16:10 source, crop-safe to 4:3 and 1:1.
- Palette: warm stone, Tel Aviv light, deep green, charcoal, muted gold.
- No fake logos, no misleading real building photos.

Professional fallback:

- Monogram/logo card using initials and profession category.
- Optional subtle texture: concrete, blueprint line, stone, glass.
- No emoji.
- Works at 50px avatar and 16:10 card image.

Category illustration:

- SVG is acceptable for small abstract category art.
- Use a restrained line style.
- No cartoon houses.
- Use only when real or generated photographic media is not available.

Caption and legality:

- Generated assets should be marked internally as generated/illustrative.
- Public captions should say â€œ×”×“×ž×™×” ×œ×”×ž×—×©×”â€ only when the image could be mistaken for a project render.
- Never copy Madlan, Yad2, developer, or brokerage photos without license.

## Mobile Breakpoints

Use exact implementation targets:

| Breakpoint | Target behavior |
| ---: | --- |
| 390px | Single-column cards. Image ratio 4:3. Search plus filter button only. No horizontal overflow. Tap targets 44px. Body text minimum 16px. |
| 600px | Two-column compact grid only if card width remains at least 270px. Otherwise stay one column. Bottom-sheet filters may become inline chips. |
| 900px | Two or three-column catalog grid. Featured cards can span two columns. Profile hero can move to media plus facts. |
| 1240px | Full desktop density. Catalog content max width around 1160-1240px. Filters/sidebar allowed if they do not reduce card media below premium size. |

Do not scale font size with viewport width. Use fixed tokens per breakpoint.

## Accessibility And Interaction Requirements

- Minimum text size: 14px for metadata, 16px for body.
- Minimum tap target: 44px by 44px.
- Keyboard focus visible on every card, filter, CTA, and gallery control.
- Image alt text must identify the project/professional or say generated/illustrative.
- Color contrast must pass WCAG AA for text.
- RTL spacing must be explicit. Do not rely on LTR defaults for icons/arrows.
- Do not mirror icons that have semantic direction unless verified for RTL.

## What I Actually Looked At

| Source | URL | Specific design lesson |
| --- | --- | --- |
| Zillow Showcase | https://www.zillowgroup.com/news/zillow-showcase-brings-listings-to-life/ | Premium listing is a media product, not a badge. Zillow frames Showcase around virtual staging, interactive 3D floor plans, and SkyTour. Nadlan should make premier cards visibly richer through media and interaction, not only `.nldc-sponsor`. |
| Zillow SkyTour design | https://www.zillow.com/news/designing-an-immersive-3d-experience-for-home-exteriors-skytour/ | Surrounding context matters. A project profile should help users understand exterior, neighborhood, parks, transport, and setting. Nadlan currently shows an empty `.nlpf-banner`. |
| Compass search and listing pages | https://www.compass.com/ and https://www.compass.com/homes-for-sale/north-carolina/ | Compass cards lead with real property imagery, price, beds/baths/square feet, address, and status like Coming Soon/Open House. Nadlan cards lead with emoji avatars and category pills. |
| The Modern House | https://themodernhouse.com/ | The page reads editorial and curated: large image moments, restrained copy, order controls, and architecture-first positioning. Nadlan needs this calm authority for flagship projects, especially Rainbow. |
| Sothebyâ€™s International Realty | https://www.sothebysrealty.com/ | Luxury real-estate presentation is built around global inventory, lifestyle, and the brand promise of â€œhome and livingâ€. Nadlanâ€™s current catalog language is too operational and icon-heavy. |
| Sothebyâ€™s property editorial | https://www.sothebys.com/en/articles/stunning-properties-from-sothebys-international-realty | Property storytelling highlights distinctive amenities, scale, setting, and lifestyle. Nadlan should surface amenities and project story visually, not bury everything under the generic profile shell. |
| LoopNet | https://www.loopnet.com/ | Commercial listings are serious and data-rich: lease/sale/auction intent, active listing counts, market trust, and business tools. Nadlan professional/project filters should feel like decision tools, not decorative chips. |
| Madlan project page | https://www.madlan.co.il/projects/%D7%A9%D7%93%D7%A8%D7%95%D7%AA_%D7%9B%D7%A8%D7%9E%D7%99_%D7%92%D7%AA_2_%D7%A7%D7%A8%D7%99%D7%AA_%D7%92%D7%AA | Madlan project pages foreground concrete project facts such as price, buildings, floors, units, developer, architect, stage, and benefits. Nadlan has some facts, but not in a premium fact architecture. |
| Madlan developer index | https://www.madlan.co.il/developers | Developer profiles use project counts and company context. Nadlan professional profiles should similarly turn registry/proof into a real identity system. |
| Houzz professionals | https://www.houzz.com/professionals | Houzz pro cards foreground reviews, verified license, hires, awards, and service proof. Nadlanâ€™s repeated empty review state should be replaced by proof-first hierarchy. |
| Realtor.com search | https://www.realtor.com/realestateandhomes-search/Sacramento_CA/ | Search pages combine listing facts with SEO-discoverable area pages. Nadlan category pages can be premium and SEO-rich without turning into a marketing landing page. |
| realestate.com.au search help | https://help.realestate.com.au/hc/en-us/articles/33736178677017-How-to-search-on-www-realestate-com-au | The search model is simple: buy/rent/sold, location, filters, list/map, save search. Nadlan should make catalog controls practical and predictable. |
| Idealista | https://www.idealista.com/en/venta-viviendas/ | Idealista makes transaction, property type, location, valuation, owner tools, and professional tools part of one ecosystem. Nadlan needs the same product-system mindset for advertisers and users. |

## What I Could Not Do And Why

- I could not use the main Sothebyâ€™s search result as a deep UI inspection source through text fetch because some search/listing content is sparse in the crawler output. I used Sothebyâ€™s official homepage and official Sothebyâ€™s property editorial pages as accessible substitutes.
- I did not create visual mockups or screenshots because this PR is audit/spec only.
- I did not edit plugin modules, routes, or live pages.

## Implementation Guardrails For Claude

- Keep one concept per URL. Do not create a new public advertising/catalog route while implementing this visual system.
- Replace visual identity first: media/fallbacks before decorative badges.
- Make `paid_tier=premier` visible through card anatomy and priority, not only through text.
- Preserve existing data contracts unless Claude approves new fields.
- If a needed field is missing, stop and map the gap rather than faking it in copy.
