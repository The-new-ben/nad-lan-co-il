# DIMRI YAMA Sde Dov - existing live page audit

Audit date: 2026-08-04

Scope: read-only review of the live Hebrew project page and its EN, FR, RU and AR sibling URLs. No page, post, repository, code, media or WordPress field was changed. The ASHIRA package was inspected only as a format and QA reference. No ASHIRA prose was reused.

## Executive verdict

All four foreign-language slugs exist and render indexable project pages. That does not mean they are ready for publication at the Utopia standard.

- The Hebrew page has one H1 and a substantial article, but the H1 is the fourteenth non-empty heading in document order. Seven showroom H2 headings, two H3 headings and three internal showroom-footer H5 headings appear before it.
- The page is a stack of several products rather than one clean buyer journey: shared site chrome, an independent-site notice, a project showroom, demo apartment inventory, map and price modules, an embedded showroom footer, the long article, more injected comparison and financing modules, a visit-request form and the global footer.
- The article wrapper contains about 3,298 whitespace tokens, including its navigation and labels. It is below the new 5,000-word content standard.
- The live showroom exposes four illustrative apartments and two apparent availability labels. These are not a verified current inventory and must not be carried into new content.
- The NIS 3.75 million figure is a dated December 2025 launch price for a two-room apartment of about 56.5 sqm. The current article presents it repeatedly without the publication date, which makes it read like a current price.
- The statement that almost half of the apartments sold were bought by the controlling shareholder omits its essential time frame. The report concerned four of nine contracts in the first quarter of 2026, not almost half of all project sales.
- The page names sources but supplies no clickable public source URLs in the article. The only off-domain links found on the rendered page were WhatsApp and email links.
- EN and FR contain substantial translated articles, but their showroom shells leak Hebrew and English. RU and AR are materially broken: both expose Hebrew H1s and Hebrew openings, both report `lang="iw"`, and the Russian page is LTR while the Arabic page is RTL.
- Every tested page emits the same six-member hreflang cluster twice, for 12 alternate tags. Canonicals are self-referencing, but the duplicate hreflang emitter should be investigated before any multilingual publication work.

## Live URLs and existence

| Language | Live URL | Rendered status evidence | Canonical and robots | HTML language and direction | Approx. article-wrapper tokens | Audit verdict |
| --- | --- | --- | --- | --- | ---: | --- |
| Hebrew | https://nad-lan.co.il/projects/dimri-yama-sde-dov/ | Project template rendered, post ID present, one H1 | Self-canonical, index/follow | `he`, RTL | 3,298 | Exists, article and showroom need factual cleanup |
| English | https://nad-lan.co.il/projects/dimri-yama-sde-dov-en/ | Project template rendered, post ID 5061, one H1 | Self-canonical, index/follow | `en`, LTR | 3,274 | Exists, under length target, Hebrew shell leakage and stale delivery claim |
| French | https://nad-lan.co.il/projects/dimri-yama-sde-dov-fr/ | Project template rendered, post ID 5075, one H1 | Self-canonical, index/follow | `fr`, LTR | 5,134 | Exists and long, but shell is mixed-language and title lacks native accents |
| Russian | https://nad-lan.co.il/projects/dimri-yama-sde-dov-ru/ | Project template rendered, post ID 5076, one H1 | Self-canonical, index/follow | `iw`, LTR | 3,641 | Exists but not a valid Russian product |
| Arabic | https://nad-lan.co.il/projects/dimri-yama-sde-dov-ar/ | Project template rendered, post ID 5077, one H1 | Self-canonical, index/follow | `iw`, RTL | 3,447 | Exists but not a valid Arabic product |

Token counts are a reproducible comparison of visible text inside `.nadlan-project-article`; they include labels and navigation and therefore slightly overstate article prose.

## Hebrew title, H1 and opening

### Head metadata

- Browser title: `DIMRI YAMA שדה דב - י.ח דמרי · תצוגת פרויקטים`
- Meta description: `כל המידע על DIMRI YAMA שדה דב - י.ח דמרי: פרטי הפרויקט, דירות ויצירת קשר עם נדלן - לפני שמתקדמים בעסקה.`
- Canonical: `https://nad-lan.co.il/projects/dimri-yama-sde-dov/`
- Robots: `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1`
- OG title: `DIMRI YAMA שדה דב - י.ח דמרי - נדלן`
- OG description is an automatically clipped version of the long-form opening and ends in an ellipsis.

### Visible H1

`DIMRI YAMA שדה דב - י.ח דמרי`

There is exactly one H1, but a showroom H2 with exactly the same text appears near the top of the document. The H1 itself appears only after the complete interactive showroom and its internal footer. In heading order it is index 13, after the following visible headings:

1. `DIMRI YAMA שדה דב - י.ח דמרי` as H2
2. `בוחרים דירה מתוך הבניין`
3. `הכל על מפה אחת: מחירים, סביבה, תוכניות עתידיות`
4. `מחיר ואומדן באזור`
5. `עסקאות שנמכרו באזור`
6. `כל מה שמסביב`
7. `פרויקטים סמוכים`
8. `קונים מחו״ל`
9. `מעוניינים בדירה? נחזור אליכם`
10. Three H5 headings in the embedded showroom footer: projects, areas and languages

This is a structural relevance problem. A crawler and a reader encounter demo inventory, estimates, generic tool labels and an internal mini-footer before reaching the page's semantic H1 and substantive opening.

### First substantive article heading

`DIMRI YAMA שדה דב - תמצית הפרויקט ושורה תחתונה`

### First substantive paragraph

> DIMRI YAMA הוא אחד הפרויקטים הבולטים ברובע שדה דב בתל אביב, הן בגלל המיקום בקו ראשון לחוף הים והן בגלל מבנה העסקה שממנה הגיע הפרויקט לידי היזם הנוכחי. הפרויקט משווק על ידי י.ח דמרי, באמצעות החברה י.ח דמרי בשדה דב בע"מ, והוא ממוקם במתחם אשכול, ברחוב אבן גבירול 220, בין חוף הים, פארק הירקון והמרחב העירוני החדש של צפון תל אביב.

The opening is direct and data-led, but it hardens two claims that need qualification: `קו ראשון לחוף` is developer marketing language, and `אבן גבירול 220` is used in commercial listings but has not been established here as a final municipal postal assignment for lot 107. The project profile immediately above the article simultaneously says `מיקום משוער עד לאישור היזם`, creating an internal contradiction.

## Visible content composition

The live DOM order is materially different from the simple article outline.

1. Global NadLan header and primary navigation.
2. Independent-site notice.
3. Stage tracker showing `בשיווק`.
4. Action menu for model, apartment selection, window view, design studio, district tour and plans. Four of these crawlable links use only `href="#"`.
5. A second, showroom-specific brand header and language controls.
6. Showroom hero with an H2 project title, CTAs and headline numbers.
7. 3D building viewer, facade control, demo apartments, sun simulation and design-studio control.
8. Map layers and an area-price estimate.
9. Demo inventory, price block, environment, media, foreign-buyer CTA and enquiry form.
10. A showroom-specific footer with project, area and language links.
11. The real H1, project fact card, breadcrumb and long-form table of contents.
12. Thirteen long-form chapters.
13. Injected price comparison, mortgage, district-tour, professional and tool modules.
14. Visit-request form.
15. Global site footer and independent-site legal note.

The embedded showroom header and footer make the page feel like one complete page followed by a second complete page. The long-form article is not the first semantic content block even though it contains the sole H1.

## Hebrew long-form outline

The long article contains these H2 chapters, in this order:

1. `DIMRI YAMA שדה דב - תמצית הפרויקט ושורה תחתונה`
2. `הנתונים: דירות, קומות ובניינים`
3. `מיקום: קו ראשון לחוף, מתחם אשכול ואבן גבירול 220`
4. `אדריכלות ועיצוב: רני זיס ו-Kelly Hoppen`
5. `תמהיל הדירות והמרפסות`
6. `מתקנים ושירותים: בריכות, ספא, יוגה, גן פנימי`
7. `מחירים: החל מ-3.75 מיליון והשוואה לאזור`
8. `שלב הפרויקט וסיפור הרכישה מחנן מור בהסדר חוב`
9. `היזם: י.ח דמרי`
10. `נקודות תשומת לב צרכניות: מעבר יזם בהסדר חוב ומה זה אומר לרוכש, רכישת דירות על ידי בעל השליטה ועסקאות בעלי עניין`
11. `בדיקות משפטיות לפני רכישה על הנייר: חוק המכר, בטוחות, חוזה, מפרט, מועד מסירה, דמי ניהול ומיסוי`
12. `שאלות נפוצות`
13. `שורת סיום והפניות`

The visible FAQ contains nine H3 questions. The JSON-LD FAQPage contains only four different questions, including a price-per-sqm question that is not one of the nine visible article FAQs. The structured-data FAQ therefore does not mirror the visible FAQ set.

## Current factual spine supported by public evidence

The following is the safest factual baseline as of the audit date. It is not a replacement for a dedicated source ledger.

| Topic | Evidence-backed position | Safe editorial treatment |
| --- | --- | --- |
| Project | DIMRI YAMA or YAMA TLV is Y.H. Dimri's project in the Eshkol section of Sde Dov, Tel Aviv | Keep brand capitalization consistent and identify the project company only where sourced |
| Legal/project company | Public materials identify `י.ח דמרי בשדה דב בע"מ` | State that this is the project company; the binding seller must still be checked in the contract |
| Planning parcel | Public acquisition reporting identifies lot 107 in Eshkol | Prefer `מגרש 107, מתחם אשכול` over an unqualified final street address |
| Residential scale | 458 planned homes | Supported by the developer's June 2026 investor presentation and multiple public reports |
| Buildings | Four buildings, commonly reported as towers of 39 and 16 storeys plus two buildings of 8 and 9 storeys | Attribute the convention because the developer's own project graphic also shows 38, 15, 8 and 8; confirm against the approved permit before freezing floor counts |
| Mixed use | About 1,500 sqm of commerce and a 70-room business hotel are part of the wider project plan | These are major components missing from the current buyer summary and should not be silently omitted |
| Architecture | Rani Ziss Architects | Supported by the developer and public planning coverage |
| Interior concept | Kelly Hoppen is presented by the developer as designing public spaces and apartments | Attribute to the developer; do not imply every delivered apartment receives a bespoke Kelly Hoppen interior unless the sale specification says so |
| Amenities | Developer marketing presents a rooftop infinity pool, indoor semi-Olympic pool, spa, dry and wet sauna, chef kitchen and bar, gym, workspace/library, yoga/Pilates studio, lounge, children's room, music room and wine cellar | Describe as planned or developer-presented amenities; operations, access, fees and delivery are not verified |
| Acquisition | In July 2024 Dimri acquired the rights from a Hanan Mor group company through the debt arrangement for NIS 1.1 billion plus VAT | Use the full transaction context and lot 107; do not imply the current project itself was in distress after the transfer |
| Status | The June 1, 2026 investor presentation labels the project `ביצוע` | Date the status. `Execution` does not by itself establish a full permit, contractual delivery date or current construction milestone |
| Sales | The June 1, 2026 investor presentation reported 41 homes sold and four purchase requests at that reporting point | Historical corporate reporting only. It is not a live availability feed |
| Launch price | On December 22, 2025, public launch reporting presented two-room homes of about 56.5 sqm from NIS 3.75 million | Historical launch example only. No current complete official price list or inventory was found in this audit |
| Delivery | No verified current contractual handover date was established | State `not publicly verified`; do not reuse the English page's 2028 target |

## Conflicting, unsupported or stale claims

### Release blockers for any reused content

#### 1. Illustrative units look like inventory

The showroom displays four unit records:

- 3 rooms, floor 12, west, 92 sqm, labelled illustrative
- 4 rooms, floor 24, southwest, 132 sqm, labelled priority
- 5 rooms, floor 36, northwest, 178 sqm, labelled illustrative
- 6 rooms, floor 39, west, 250 sqm, labelled priority

The interface also says `4 דירות לבחירה`, `זמינות 2` and `4 דירות`. A later disclaimer says the model and apartments are preliminary illustration and not an approved inventory, but the earlier controls still resemble live stock. None of these four records should be reused as a real apartment, plan, size, direction, floor, availability or price fact.

#### 2. Price estimates lack a dated factual basis

The live page presents:

- `₪66,000 - ₪84,000 למ״ר`
- `ממוצע מבוקש ₪75,000 למ״ר`
- an injected comparison card of about `₪75,000 למ״ר`
- FAQ schema answering that the estimate is about `₪75,000 למ״ר`

No source date, comparable set, VAT basis or calculation method is visible beside those numbers. Calcalist reported in May 2026 that the average for apartments sold in the project had been NIS 67,000 per sqm excluding VAT and that the company forecast NIS 62,000 excluding VAT on subsequent deals. Those figures are not directly interchangeable with consumer asking prices including VAT, but they demonstrate why a free-floating NIS 75,000 estimate should not be presented as a current project fact.

#### 3. NIS 3.75 million is shown as current

The long article, FAQ and summary repeat `החל מ-3.75 מיליון שקל` without its December 22, 2025 date or the associated two-room, approximately 56.5 sqm launch example. By August 2026 this must be labelled as historical launch marketing, not a live starting price or availability statement.

#### 4. Related-party sales are stripped of their denominator and period

The page says that almost half of the apartments Dimri sold were bought by the controlling shareholder. The supporting May 28, 2026 report said four of nine contracts in the first quarter of 2026 were signed by Yigal Dimri and relatives. The company's June 2026 presentation reported 41 homes sold in total at that reporting point. Safe wording must preserve `four of nine in Q1 2026`; otherwise readers can wrongly understand that almost half of all project sales were related-party transactions.

#### 5. Russian and Arabic pages are not genuine language pages

The RU page renders with `lang="iw"`, LTR direction, a Hebrew H1, a Hebrew first H2 and a Hebrew opening paragraph. The main project area contained roughly 4,248 Hebrew letters during the Chrome audit. Later sections contain Russian, but the page's most prominent and earliest content is not Russian.

The AR page renders with `lang="iw"`, RTL direction, a Hebrew H1, a Hebrew first H2 and a Hebrew opening paragraph. The main project area contained roughly 5,313 Hebrew letters versus about 13,703 Arabic letters. The top shell also contains malformed Hebrew filler such as `בבקשה אל תדאג בקשר לזה` rather than native Arabic buyer copy.

Both pages fail the language, opening, H1 and cultural-quality gates despite being indexable and present in hreflang.

### High-priority factual conflicts

#### Address conflict

The article states `אבן גבירול 220` as the address. Yad2 uses that address, while transaction and planning coverage identify lot 107. The project's own fact card on NadLan says the Sde Dov location is approximate pending developer confirmation. The exact address should therefore be described as a marketing/listing address until an official project-specific municipal assignment is verified.

#### Floor-count conflict

The article uses 39, 16 and two 8-to-9-storey buildings. The developer's narrative says four buildings ranging from 9 to 39 floors, but the same developer page's building graphic shows 38, 15, 8 and 8. This may be a convention difference between residential floors and total floors, but it cannot be silently resolved without the approved plan or permit.

#### Status conflict

The top stage tracker emphasizes `בשיווק`, while the article says construction began and the June 2026 investor presentation labels the project `ביצוע`. Sales status and construction status should be separate dated fields. A single `בשיווק` status is incomplete.

#### Missing hotel and commerce

The current article repeatedly describes a four-building residential complex but does not explain that the wider approved/project plan includes about 1,500 sqm of commerce and a 70-room hotel. Those uses can affect access, activity, management and the character of the site and belong in a buyer-facing description.

#### Sea and view language

The developer markets the project on the coastal line and describes sea-facing facilities and western-facade views. The current article goes further by treating first-line location as a value and future-liquidity fact. A project's coastal position does not verify a permanent or unobstructed sea view for every apartment. Unit-specific view claims require the exact building, floor, orientation, approved surroundings and verified visual study.

#### Delivery target in English

The English opening says delivery is targeted around 2028. No source found in this audit supports a current 2028 handover target. The developer's own later marketing article speaks more generally about residents entering within six years, which is itself forward-looking and not a contractual date. The English 2028 statement should be treated as stale or unsupported.

### Medium-priority content and trust issues

- The developer amenity list is presented as an existing project feature set rather than consistently as planned/developer-presented. Contract, access, management and fees are still unknown.
- Facility chips assert pool, gym, children's areas, parking and safe room. Pool, gym and children's space have developer support; parking allocation, storage and unit-level rights still require the sale specification. A generic facility chip is not proof of an entitlement.
- The article claims proximity affects demand, prices and future liquidity. These are market expectations, not verified project facts or guarantees.
- The current source notation is name-only. Readers cannot inspect the exact publication, date or supporting paragraph.
- Two freshness statements coexist: `עודכן יוני 2026` in the article and `עודכן 06/07/2026` in a later module. The latter is also locale-ambiguous.
- The project fact card displays `מאגר התחדשות עירונית · data.gov.il` beside `בנייה חדשה`. That template label is unrelated to a new-build lot and can confuse readers about the source and project type.
- The Hebrew article does not publish a current room mix, current inventory, contractual handover, full permit milestone, parking/storage rights, maintenance estimate or financing terms. It should say these were not publicly verified rather than let the showroom simulation fill the gaps.

## Language-page quality findings

### English

- Title: `Dimri Yama Sde Dov | Kelly Hoppen Living on the Tel Aviv Coast · Project showroom`
- H1: `Dimri Yama Sde Dov | Kelly Hoppen Living on the Tel Aviv Coast`
- First H2: `Dimri Yama: the bottom line before you choose an apartment`
- Opening is English and project-specific, but includes the unsupported 2028 target.
- The main project area contained roughly 1,149 Hebrew letters. The top status value, action menu and parts of the showroom remain Hebrew.
- About 3,274 wrapper tokens, below the 5,000-word standard.

### French

- Title: `Dimri Yama Sde Dov | Residences signees Kelly Hoppen · Vitrine des projets`
- H1: `Dimri Yama Sde Dov | Residences signees Kelly Hoppen`
- First H2: `DIMRI YAMA Sde Dov - synthèse du projet et conclusion`
- Long article is French and exceeds 5,000 wrapper tokens, but the title drops the accents from `Résidences signées` and does not lead with a tested buyer search phrase.
- The main project area contained roughly 1,246 Hebrew letters. The status tracker and action menu are primarily Hebrew, while several feature headings remain English.

### Russian

- Direct rendered H1: `דימרי ימה שדה דב | מגורים קלי הופן`
- Direct rendered first H2: `דמרי יאמה שדה דב - תיאור קצר של הפרויקט והתוצאה`
- Opening paragraph is Hebrew.
- `lang="iw"` and `dir="ltr"`.
- Later chapters are Russian, but the page is only about 3,641 wrapper tokens and the top of the page fails Russian intent and native-language quality.
- During the same Chrome session, an earlier navigation exposed a Russian browser title while a later direct suffix navigation hydrated a Hebrew title. The visible H1 and opening remained Hebrew. This indicates inconsistent client-side language hydration and should be reproduced in a clean acceptance test.

### Arabic

- Direct rendered H1: `דימרי יאמה שדה דב | קלי הופן דיזיין רזידנס`
- Direct rendered first H2: `דמרי יאמה שדה דב - סיכום הפרויקט ושורה אחרונה`
- Opening paragraph is Hebrew.
- `lang="iw"` with RTL direction.
- Later chapters contain Arabic, but the page is only about 3,447 wrapper tokens and the most prominent content is Hebrew.
- The shell includes nonsensical Hebrew fallback copy instead of native Arabic labels.

### Multilingual wiring

Positive findings:

- All five pages are live.
- Each tested suffix page has a self-canonical.
- Each page is index/follow.
- The footer language switcher links to all five sibling URLs.
- Each page advertises he, en, fr, ru, ar and x-default alternates.

Problems:

- The complete six-link alternate cluster is emitted twice on every tested page, producing 12 hreflang tags.
- RU and AR declare Hebrew `iw` rather than `ru` and `ar` in the rendered HTML.
- RU is LTR despite being a Russian target page only because its actual top content is Hebrew; AR is RTL but remains mixed Hebrew/Arabic.
- Page-shell dictionaries are incomplete across EN, FR, RU and AR.
- The language URLs are technically linked, but content equivalence and visible language are not trustworthy enough for search engines or buyers.

## Internal links

### Links inside the long-form article wrapper

The substantive article itself links to:

- Sde Dov guide: https://nad-lan.co.il/sde-dov/
- Real-estate lawyer guide: https://nad-lan.co.il/real-estate-lawyer/
- Purchase-tax calculator: https://nad-lan.co.il/purchase-tax-calculator/
- Home and project archive through the breadcrumb
- A Hebrew city-project route: `https://nad-lan.co.il/city/%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91-%D7%99%D7%A4%D7%95/projects/`
- Article chapter anchors

### Links supplied by surrounding modules

The page also exposes:

- Mortgage calculator: https://nad-lan.co.il/mortgage-calculator/
- Buying guide: https://nad-lan.co.il/buying-apartment/
- Glossary: https://nad-lan.co.il/glossary/
- Professionals search and Tel Aviv professionals filter
- 3D district tour and project-focused tour
- Premium facility filters
- Nearby projects: Rainbow, ASHIRA, Gindi Vogue, ZOHI and FIRST
- All five language siblings

### Gaps for the future content product

- The mortgage calculator is not linked naturally from the article prose; it appears in a later injected commercial module.
- The required contractor/new-project guide URL `https://nad-lan.co.il/new-projects/` is absent. A different `/buying-apartment/` guide is present.
- The required Tel Aviv city page `https://nad-lan.co.il/cities/%d7%aa%d7%9c-%d7%90%d7%91%d7%99%d7%91-%d7%99%d7%a4%d7%95/` is absent. The breadcrumb uses a different singular `/city/.../projects/` route with percent-encoded Hebrew.
- Model, apartment, window-view and plan items in the top action menu expose `href="#"`, so they do not provide crawlable destinations even if JavaScript controls elsewhere on the page work.

## Visible source list

The article names these sources in prose:

- Dimri website
- Sde Dov district website
- Madlan
- Yad2
- Economic reporting on the acquisition from Hanan Mor
- Economic reporting on related-party apartment purchases

A later module says: `המקור: דמרי, מדלן, יד2, גלובס, כלכליסט, רובע שדה דב · עודכן 06/07/2026`.

None of those names is a clickable external source link in the long article. The source section is therefore not auditable by a public reader and does not meet the Utopia/ASHIRA evidence standard.

## Public evidence used for this audit

1. Official Dimri Hebrew project page: https://www.dimri.co.il/dimriyama-2/
2. Official Dimri English project page: https://www.dimri.co.il/en/dimriyama/
3. Y.H. Dimri investor presentation dated June 1, 2026: https://ir.dimri.co.il/wp-content/uploads/2026/06/P1746208-00.pdf
4. Public report on the July 2024 lot-107 acquisition: https://www.nadlancenter.co.il/article/10309
5. Calcalist, May 28, 2026, on four of nine Q1 contracts and project sales context: https://www.calcalist.co.il/market/article/rkc1lyrggl
6. Dated December 22, 2025 launch-price report: https://sdedov.co.il/%D7%94%D7%97%D7%9C-%D7%9E-3-75-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C%D7%99%D7%9D-%D7%93%D7%9E%D7%A8%D7%99-%D7%9E%D7%AA%D7%97%D7%99%D7%9C%D7%94-%D7%A9%D7%99%D7%95%D7%95%D7%A7-%D7%91/
7. Yad2 project listing using Ibn Gvirol 220: https://www.yad2.co.il/yad1/project/18245
8. Globes planning background from August 4, 2024: https://www.globes.co.il/news/article.aspx?did=1001485854

## Safe carry-forward rules for the later content phase

- Do not reuse any of the four showroom apartment records or their status labels.
- Do not state a current price, current price per sqm, current availability or live sales count without a dated primary source.
- Describe NIS 3.75 million only as the December 2025 launch example for a two-room home of about 56.5 sqm.
- Preserve the exact related-party context: four of nine Q1 2026 contracts, not nearly half of all project sales.
- Treat 41 sold and four purchase requests as June 1, 2026 corporate-reporting history, not live inventory.
- Do not publish 2028 or another handover year without a current contractual or primary-source basis.
- Use lot 107 and Eshkol as the planning location; qualify Ibn Gvirol 220 until an official project postal address is verified.
- Freeze the building floor convention only after checking the approved plan or permit because current public materials conflict.
- Attribute amenities, Kelly Hoppen involvement and view language to the developer's plans.
- Separate project coastal location from the view of any specific apartment.
- Include the planned commerce and 70-room hotel because they materially affect the buyer's understanding of the complex.
- Build a real source chapter with exact public URLs and dates.
- Rebuild each foreign language from its own search and cultural-intent research. Existing EN/FR/RU/AR prose is evidence to audit, not text to recycle.
- Keep the ASHIRA package method: one frozen fact ledger, an explicit conflict table, prohibited claims, a shared public source list and a language-by-language acceptance report. Reuse the method only, never its prose.

## Isolation record

The audit used read-only Chrome inspection, public web research and read-only access to the ASHIRA package's README and source-ledger format. The only file created is this audit file. No live page, WordPress record, repository file, code, media or ASHIRA deliverable was edited.
