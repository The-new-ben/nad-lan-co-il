# Ashira Sde Dov Source Dossier

Date accessed: 2026-06-27
Status: preflight only. This is not public copy and must not be pasted into a live page as-is.

## Scope And Honesty

This dossier prepares the Ashira Sde Dov project page before any public build. It separates verified public facts from illustrative showroom assets and marks the missing owner/developer inputs that must be approved before a commercial launch.

The next Ashira page must be buyer and investor facing. Public wording should speak to people comparing apartments, views, location, price estimates, documents and contact options. It must not expose internal implementation terms or private workflow language.

## Source Map

### Official Project Source

- Ashira official project site: https://ashirabyavisror.com/
  - Safe facts from the official site:
    - Project brand: ASHIRA / Ashira Tel Aviv by Avisror.
    - Location signal: Sde Dov, Tel Aviv.
    - Nearby context shown by the project site includes Tel Baruch beach, Reading, Tel Aviv Port, Park Hayarkon, Ramat Aviv Mall, Tel Aviv University, light rail, University train station, Namir Road and Ibn Gabirol.
    - The project page presents a resident-focused lifestyle program: spa, pool, gym, cinema, kids world, lounge and commerce.
    - The site says the complex includes 2 to 5 room apartments in towers and boutique buildings, planned by Avner Yashar and designed by Dana Oberson.
  - Use limit: do not copy the developer text. Use it only as a fact/source signal and write original buyer copy.

### Municipal And Planning Source

- Tel Aviv municipality Sde Dov district page: https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx
  - Safe facts:
    - The former airport area is becoming a new district in north Tel Aviv.
    - The district is planned as mixed use: housing, business, leisure, offices, shops, hotels, public space, coastal park, urban squares and open space.
    - The municipality states around 16,000 apartments are planned in the district.
    - The master plan is TA/4444 and was approved in August 2020.
    - The district spans about 1,300 dunams.
    - The planned population is about 40,000 residents.
    - The Green Line light rail is planned to serve the district with stations along the continuation of Ibn Gabirol.
  - Use limit: city-level planning numbers can be cited. Do not imply every number belongs only to Ashira.

### Multilingual SEO Sources

- Google Search Central localized versions: https://developers.google.com/search/docs/specialty/international/localized-versions
  - Build rule: every translated version must link to all other variants and to itself with valid `hreflang`.
  - Use fully qualified URLs and valid ISO language or language-region codes.
  - Add `x-default` for the default selector or Hebrew page when relevant.
- Yoast hreflang guide: https://yoast.com/hreflang-ultimate-guide/
  - Practical rule: use hreflang when the same content exists in multiple languages or regions.
  - Return links and self-links are required.
  - Do not over-specify country targeting when language-only targeting is enough.
- Liquid Web WordPress hreflang guide: https://www.liquidweb.com/wordpress/seo/add-hreflang-tags/
  - WordPress options include translation plugins, Yoast with multilingual plugins, dedicated hreflang plugins, or manual theme output.
  - For this site, the safe first phase is separate crawlable pages per language plus a controlled theme-level hreflang map, not installing a broad translation plugin without a staging gate.

### JavaScript And Crawlability Source

- Google JavaScript SEO basics: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
  - Build rule: important content should be present in the HTML response or pre-rendered where possible.
  - The project page can use 3D and interaction for buyers, but core text, headings, project facts, links and contact paths must be crawlable without relying only on client-side rendering.

### 3D And BIM Sources

- model-viewer docs: https://modelviewer.dev/docs/
- model-viewer annotations example: https://modelviewer.dev/examples/annotations
  - Feasible now: GLB display, camera controls, auto rotate, basic hotspots attached to model positions.
  - Constraint: accurate apartment selection on a spinning model requires per-apartment geometry or reliable apartment coordinates in the model.
- xeokit BIM viewer: https://github.com/xeokit/xeokit-bim-viewer
  - Feasible for future premium BIM: browser BIM viewer, IFC support, object trees, storeys, model metadata and split model support.
  - License warning: xeokit SDK is AGPL unless a commercial license is used. Do not embed it into proprietary production code without license review.
- Google Photorealistic 3D Tiles: https://developers.google.com/maps/documentation/tile/3d-tiles
  - Feasible for future "view from apartment": Cesium or another 3D Tiles renderer can show photorealistic surroundings where coverage and billing allow.
  - Requires API key, billing, attribution and policy review.

## SERP And Intent Map

### Hebrew

Primary query cluster:

- דירות למכירה באשירה שדה דב
- אשירה שדה דב
- Ashira תל אביב
- אביסרור שדה דב
- דירות חדשות בשדה דב

Likely buyer intent:

- Find availability and apartment mix.
- Understand view, floor, direction and distance to sea.
- Compare Ashira with Rainbow, Dimri Yama and other Sde Dov projects.
- Check if the district plan supports long-term value.

Recommended visible page direction:

- Start with a tight buyer paragraph about Ashira, Sde Dov, apartment choice, view and non-binding estimate.
- The showroom should appear before the long article body.
- The article should then cover the project, the developer, the district plan, transport, beach access, amenities, legal checks, tax and foreign buyer considerations.

### English

Primary query cluster:

- Ashira Sde Dov apartments for sale
- Ashira Tel Aviv by Avisror
- Sde Dov new apartments Tel Aviv
- buy apartment Sde Dov Tel Aviv

Likely buyer intent:

- Foreign investors and relocation buyers need plain English, location confidence and process explanation.
- They need legal/tax reminders without legal advice.

Recommended direction:

- Create a separate crawlable English page, not only a language chip.
- Use an English title around "Ashira Sde Dov apartments for sale in Tel Aviv".
- Include non-binding price language, buyer checklist, tax/legal process, and contact path.

### French

Primary query cluster:

- appartement neuf Tel Aviv Sde Dov
- Ashira Tel Aviv appartement
- investir immobilier Tel Aviv Sde Dov

Likely buyer intent:

- French-speaking buyers often need neighborhood explanation, purchase process, legal representation, tax and currency clarity.

Recommended direction:

- Separate French page with a French H1, original French copy and reciprocal hreflang.
- Do not auto-translate Hebrew legal terms without checking meaning.

### Russian

Primary query cluster:

- квартиры в Тель Авиве Сде Дов
- Ashira Tel Aviv квартиры
- недвижимость Тель Авив новостройка

Likely buyer intent:

- Russian-speaking buyers need project basics, district context, availability, price estimate, documents and contact.

Recommended direction:

- Separate Russian page, original or carefully edited translation, with Hebrew legal terms explained simply.

### Arabic

Primary query cluster:

- شقق للبيع في تل أبيب سديه دوف
- مشروع أشيرا تل أبيب
- عقارات جديدة في تل أبيب

Likely buyer intent:

- Arabic-speaking buyers need location clarity, project status, unit choice, process, and contact options.

Recommended direction:

- Separate Arabic page with RTL Arabic, not mixed Hebrew.
- Do not ship Arabic labels until the actual Arabic page exists.

## Asset Truth Table

| Asset | Current State | Publish State Required |
| --- | --- | --- |
| Hero image | Generated concept in theme folder | Approved developer render or clearly labeled original editorial visual |
| Facade selector image | Generated concept | Official sale elevation or approved visual with manually traced apartment cells |
| GLB model | Temporary massing model | Official BIM/GLB, approved generated model, or clearly labeled illustrative model |
| Apartment geometry | Screen-space cells only | For spinning model selection, per-apartment meshes or precise GLB hotspot data |
| Prices | Empty or non-binding estimate text | Approved price range, source date and non-binding disclaimer |
| Inventory | Sample units only | Approved live unit status or explicit "availability must be verified" language |
| Floor plans | Empty URLs | Approved sale plans or no plan button |
| Interior tour/video | Empty URLs | Developer media, licensed generated tour, or no tour button |
| Surroundings | Illustrative environment and project list | Verified nearby POIs, transit, beach, schools and district facts |
| Translations | Language entry points only | Full crawlable pages with reciprocal hreflang |

## Technical Feasibility Notes

### What Is Feasible Now

- A premium project page with a rotating model for context.
- A side-by-side clickable facade where every apartment cell is a button.
- A selected-apartment card with unit facts, plan/view/tour/contact actions.
- A multilingual homepage project selector that shows Hebrew, English, French, Russian and Arabic entry points.
- Separate crawlable language pages when each language has real content.

### What Requires Better Assets

- Clicking exact apartments on a freely spinning GLB requires the model to contain separate apartment/floor meshes or reliable object metadata. Otherwise a facade plane is more honest and more usable.
- A BIM workflow can use xeokit or another BIM stack, but license, file size, conversion and metadata handling must be solved before production.
- Photorealistic view-from-apartment needs API billing and a 3D Tiles renderer with attribution.

## Build Readiness Checklist

- [ ] Official facts are separated from generated visuals.
- [ ] Page has one visible H1 and a strong first buyer paragraph.
- [ ] Project showroom is high on the page, but the first text explains why the buyer should interact.
- [ ] Long article body is structured below the product, with headings above paragraphs.
- [ ] All public copy avoids internal language.
- [ ] Apartment selector works on desktop, tablet and mobile screenshots.
- [ ] No horizontal overflow.
- [ ] Each language page exists before language chips claim full support.
- [ ] Hreflang map includes self, return links and x-default.
- [ ] Schema only includes visible facts.
- [ ] Assets have source notes and approval status.

## Next Slice Recommendation

Keep the homepage selector already embedded above the fold. Next, build Ashira from this source dossier in a clean V2 page structure:

1. Create the Hebrew Ashira draft page with verified facts and clear illustrative labels.
2. Keep the model and facade side-by-side on desktop, stacked cleanly on mobile.
3. Create language stubs only if they are noindex or clearly not final. For indexable pages, write full language content first.
4. Add a screenshot gate for the Ashira page before any live publication.
5. Only after Hebrew is visually green, repeat the same source-backed process for English, French, Russian and Arabic.
