# Rainbow SEO, Investor And Multilingual Readiness Audit

Date: 2026-06-15  
Live URL: `https://nad-lan.co.il/projects/rainbow-tel-aviv/`  
Live plugin version during audit: `1.66.2`  
Purpose: verify what is actually live before Rainbow becomes the template for the next Sde Dov
project.

## Live Structural QA

Command:

```bash
node scripts/qa-project-showroom-live.mjs --site https://nad-lan.co.il --slug rainbow-tel-aviv --post-id 4464 --strict
```

Result: `23 passed / 0 failed`.

Important passing signals:

- live plugin version is new enough: `1.66.2 >= 1.65.2`;
- payload API marker exists: `project_3d.showroom_payload_api_v1652`;
- exactly one visible H1 according to the QA script;
- showroom section exists;
- `<model-viewer>` exists;
- model-viewer script renders as `type="module"`;
- model-viewer uses `reveal="auto"` and `loading="auto"`;
- 6 hotspot slots exist;
- selected-apartment action card exists;
- buyer inquiry / non-binding purchase form exists;
- contractor project request form exists;
- transaction-led SEO title and meta description are present;
- no obvious PHP, code/class or mojibake leak.

This is a structural/render contract pass. It does not replace the visual/mobile gate. PR #187 still
needs live deployment and visual QA for the 390px containment issue.

## Template Gate Result

Command:

```bash
node scripts/qa-project-template-gate.mjs --site https://nad-lan.co.il --slug rainbow-tel-aviv --post-id 4464 --out docs/qa/rainbow-template-gate-live-1662.json
```

Result against current live `1.66.2`: `20 passed / 5 failed`, `template_ready: false`.

The failures are real and expected at this stage:

- live plugin is below the v1.66.3 template gate;
- `project_page_assembly.rainbow_public_copy_v1663` is not live yet;
- `og:image` uses HTTP on current production; PR #187 now contains the same-site HTTPS normalizer;
- old public text still contains internal lead wording;
- the visual Chrome gate was not run in that command.

This is the correct state before PR #187 is deployed. Do not mark Rainbow clone-ready until this
template gate passes with `--visual --strict` after the live update.

## Live SEO Extraction

Rendered page extraction from public HTML:

| Element | Current value / status | Readiness |
| --- | --- | --- |
| Title | `דירות למכירה ב-Rainbow תל אביב | מחירים, תוכניות ובחירת דירה בשדה דב | נדלן חכם` | Strong buyer intent. Long at 79 chars, but acceptable for a flagship page if SERP testing shows it displays well. |
| Meta description | `Rainbow Tel Aviv - ריינבו תל אביב בשדה דב: מחירים מדווחים ואומדן לא מחייב, בחירת דירה בתלת ממד, תוכניות, מבט מהדירה וליווי בדיקה לפני פנייה ליזם.` | Good. 145 chars, includes price, estimate, 3D selection, plans and developer contact. |
| Canonical | `https://nad-lan.co.il/projects/rainbow-tel-aviv/` | Good. |
| Robots | `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1` | Good. |
| H1 | `Rainbow Tel Aviv – ריינבו תל אביב` | Good, one visible H1 per QA script. |
| H2 count | 20 | Strong depth, but monitor readability and headline alignment visually. |
| OG image | `http://nad-lan.co.il/wp-content/uploads/2026/06/rainbow-tel-aviv-hero.jpg` on live 1.66.2 | Pending PR #187; expected to normalize same-site images to HTTPS after deploy. |
| JSON-LD count | 4 | Good. |
| Schema types | WebPage, ImageObject, BreadcrumbList, WebSite, Organization, FAQPage, ApartmentComplex | Strong. |
| Hreflang | none | Not multilingual-ready yet. |

First H2s visible in extraction:

1. `דירות למכירה ב- Rainbow Tel Aviv בשדה דב: מחירים, זמינות ובחירת דירה`
2. `דירות למכירה ב-Rainbow Tel Aviv – ריינבו תל אביב: בחירת דירה בתלת ממד`
3. `דירות למכירה ב-Rainbow Tel Aviv: מחיר, זמינות ובדיקת עסקה`
4. `למה המודל התלת ממדי חשוב לרוכשים וליזמים`
5. `שאלות נפוצות על Rainbow Tel Aviv`

## SERP Landscape Checked

Fresh web search on 2026-06-15 for:

- `ריינבו תל אביב שדה דב Rainbow Tel Aviv ישראל קנדה`
- `Rainbow Tel Aviv Sde Dov Israel Canada`
- `ריינבו תל אביב מחיר דירות למכירה שדה דב`

Observed competitor/source set:

| Source | URL | What it owns |
| --- | --- | --- |
| Official Rainbow site | `https://rainbowtlv.com/` | Brand, premium imagery, official concept language. |
| Israel Canada Hebrew page | `https://www.israel-canada.co.il/projects/tel-aviv/rainbow` | Developer authority, Sde Dov/Eshkol context, project positioning. |
| Israel Canada English page | `https://www.israel-canada.co.il/en/projects/tel-aviv/rainbow` | English foreign-buyer/luxury signal. |
| Madlan project page | `https://www.madlan.co.il/projects/חלקה_15_שדה_דב_תל_אביב` | Project listing data and buyer lead intent. |
| SdeDov.co.il Rainbow page | `https://sdedov.co.il/project/rainbow/` | District/project discovery, amenities language. |
| Calcalist | `https://www.calcalist.co.il/market/article/bj411jfga1g` | Reported sales volume and average apartment value. |
| Bizportal | `https://www.bizportal.co.il/realestates/news/article/816625` | Price per sqm and early price framing. |
| Globes / Globes English | `https://www.globes.co.il/` and `https://en.globes.co.il/` Rainbow/Sde Dov coverage | Investor and notable-sale context. |
| Ynet English | `https://www.ynetnews.com/business/article/bk5abetlje` | English notable purchase and amenity details. |

## SEO Positioning Decision

The official and developer pages are better at brand authority. NadLan should not try to beat them
by sounding more official than the developer.

NadLan can win the missing buyer/investor layer:

- price and reported-price context, clearly non-binding;
- apartment selection and availability checks;
- floor plans, drawings and view-from-apartment workflow;
- Sde Dov surroundings and neighboring projects;
- FAQ and due-diligence language;
- foreign-buyer / remote-buyer guidance once translated pages are approved.

This is why the current title/meta direction is right: `דירות למכירה`, `מחירים`, `תוכניות`,
`בחירת דירה`, `שדה דב`.

## Investor Signals: Done vs Missing

| Signal | Current evidence | Status |
| --- | --- | --- |
| Buyer/price title | Live title starts with `דירות למכירה` and includes `מחירים`. | Done |
| Non-binding price disclaimer | Meta includes `אומדן לא מחייב`; page schema price meta exists. | Done |
| Apartment selector | Live healthcheck reports model-viewer, dual showroom, unit picker, stage card and payload API. | Done structurally |
| FAQ schema | `FAQPage` in JSON-LD and `faq_meta: true`. | Done |
| ApartmentComplex schema | `ApartmentComplex` in JSON-LD and `price_meta: true`. | Done |
| Social image | OG image present, dimensions present; live URL is currently HTTP. | Pending PR #187 HTTPS normalizer |
| Foreign-buyer signals | English competitor pages exist; no hreflang or translated NadLan page exists. | Missing |
| Real inventory | Unit picker exists, but official inventory/availability source is not proven. | Missing owner/developer input |
| Real prices | Estimate framing exists; official current price list is not proven. | Missing owner/developer input |
| Ranking proof | IndexNow recent pings exist, but no rank tracking proof is stored. | Missing |
| Visual mobile proof | Structural QA passes; visual QA has a known pending v1.66.3 fix. | Pending PR #187 |

## Multilingual Readiness

Current live page has no `hreflang`. That is correct until real translated URLs exist.

Recommended staged path:

1. Finish Hebrew template visual QA first.
2. Create English page only after the Hebrew page is stable.
3. Use an owner-approved route pattern such as `/en/projects/rainbow-tel-aviv/`.
4. Translate the page from the same project payload and source notes.
5. Add `hreflang` only after both Hebrew and English URLs are live and equivalent.
6. Repeat for French/Russian only after English passes.

Do not generate language shells just to show a selector. A foreign buyer page must preserve source
labels, tax/legal disclaimers, non-binding price wording and developer-contact path.

## High-Priority Next Actions

1. Merge/deploy PR #187, then run the visual QA harness and the template gate again.
2. Confirm rendered `og:image` changed to HTTPS after PR #187 is live.
3. Add a small rank-tracking note for target queries:
   - `ריינבו תל אביב`
   - `Rainbow Tel Aviv`
   - `ריינבו שדה דב`
   - `דירות למכירה Rainbow תל אביב`
   - `מחיר ריינבו תל אביב`
4. Get owner/developer approval for real inventory and price wording.
5. Start English pilot only after the Hebrew template is green.

## Template Decision

Rainbow is **SEO structurally ready** as a Hebrew project page, but not fully **template ready** until
the visual mobile gate and public-copy cleanup from v1.66.3 are live-green.

The next project should reuse the data/payload/schema/showroom contract, not copied page markup.
