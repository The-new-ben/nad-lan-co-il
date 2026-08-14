# Browser and source verification record

Verification date: 2026-08-05, Asia/Jerusalem

Method: real user Chrome, direct source pages, Google Israel for discovery only. No publishing, form submission or page edits were performed.

## Search environment

- Browser: the user's connected Google Chrome.
- Google endpoint: `google.co.il`.
- Search parameters: Hebrew interface, Israel region (`hl=iw`, `gl=il`), personalization disabled in the query (`pws=0`).
- Google footer reported Tel Aviv-Yafo based on IP and "results are not personalized".
- Discovery query included: `שיכון ובינוי מגרש 109 שדה דב דיור להשכרה 324 היתר בנייה 2025` and a focused query for Shikun & Binui's 2025 reporting.
- Search snippets were not used as facts. Every accepted claim was checked on a direct source page or direct public document.

## Capture B1 - live Hebrew target page

URL: https://nad-lan.co.il/projects/shikun-binui-sde-dov/

Observed page title:

`שיכון ובינוי שדה דב - דיור להשכרה (מגרש 109) · תצוגת פרויקטים`

Head metadata captured:

- canonical: self-referencing target URL.
- `lang=he`, `dir=rtl`.
- meta description: `כל המידע על שיכון ובינוי שדה דב - דיור להשכרה (מגרש 109): פרטי הפרויקט, דירות ויצירת קשר עם נדלן - לפני שמתקדמים בעסקה.`
- OG title: `שיכון ובינוי שדה דב - דיור להשכרה (מגרש 109) - נדלן`.
- robots: index/follow.

Document/order capture:

- Exactly one H1 was present, but its top position was about 7,253 px into the rendered page.
- A project H2 appeared around 920 px, before the H1 and before the substantive article.
- The substantive article container was `.nadlan-project-article`.
- Article text measured about 23,555 characters and about 4,015 whitespace-delimited words.
- One visible empty H2 was detected.
- The article contained no external evidence links; links were internal anchors/site links plus email.

Generic experience content observed before the article:

- Status rail: `בהיתר בנייה`.
- Generic showroom: 38 floors and four apartments to choose.
- Demo cards: 2 rooms/floor 10/west/55 sqm; 3 rooms/floor 20/southwest/78 sqm; 4 rooms/floor 30/northwest/105 sqm; 4 rooms/floor 38/west/110 sqm.
- Inventory/selection language including `availability 4` and a selected-apartment lead flow.
- A model warning indicated that the generic model was not the project building.
- Generic interior/cinematic experience and purchase-oriented modules appeared on a rental project.
- Price module said project estimates were pending but displayed neighboring-project estimates.
- A 2035 district visualization appeared in the project experience.

Structured-data capture:

- One `ApartmentComplex` object named the project and declared 324 units.
- It emitted `מגרש 109, מתחם אשכול, רובע שדה דב, תל אביב-יפו` as `streetAddress`.
- It emitted latitude 32.113474 and longitude 34.781737; these coordinates were not independently verified in this research pass.
- Two `BreadcrumbList` objects were present.
- `FAQPage` contained three questions that did not match the nine visible article FAQs. One schema answer described an apartment-selection simulation/floor/unit flow that is unsupported for this project.

## Capture B2 - municipal licensing protocol

Direct URL opened in Chrome:

https://www.tel-aviv.gov.il/Transparency/DocLib3/%D7%A4%D7%A8%D7%95%D7%98%D7%95%D7%A7%D7%95%D7%9C%20%D7%94%D7%97%D7%9C%D7%98%D7%95%D7%AA%20%D7%A8%D7%A9%D7%95%D7%AA%20%D7%A8%D7%99%D7%A9%D7%95%D7%99%201-25-0069.pdf

Chrome reached the direct municipal PDF and displayed document title `לכבוד`, but the PDF viewer exposed no accessible document DOM. The identical public URL was then downloaded for local extraction. PDF page 4 (document page 3) was rendered to PNG and visually inspected at full resolution.

Verified from the rendered page and text extraction:

- Tel Aviv-Yafo municipality licensing authority, protocol dated 8 April 2025.
- Request 1109-24, building file 2436-014, information request 23-01607.
- Planning lot 109; application area 5,221 sqm.
- Applicant: `ריט ש.ב נדל"ן (נכסים) בע"מ`.
- Long-term rental for 20 years; 50% regulated rent for eligible tenants, 50% free market.
- Three buildings over four shared basement levels.
- Tower A: 40 floors including ground and technical, 229 homes.
- Building B: 9 floors including ground and roof, 44 homes.
- Building C: 9 floors including ground and roof, 51 homes.
- Total: 324 homes, with residential and commercial uses.

The direct municipal PDF is the authority for the dated licensing-program facts. It is not evidence of current rent, availability or a postal address.

## Capture B3 - current TASE/MAGNA disclosure

Direct URL:

https://mayafiles.tase.co.il/rhtm/1728001-1729000/H1728325.htm

Chrome DOM capture verified:

- Filing entity: `שיכון ובינוי בע"מ / SHIKUN & BINUI LTD`, company number 520036104.
- Filed 17 March 2026; reference 2026-01-023385.
- Main event concerned environmental requirements at Sde Dov B, lot 106.
- Separate exact paragraph for `פרויקט שדה דב א' (מגרש 109)` stated that work continued normally under statutory approvals, a full building permit existed, excavation and shoring were complete, and structural work had begun through a main contractor.

Guardrail: only that explicit lot-109 paragraph belongs to this project. Environmental findings and other details about lot 106 are excluded.

## Capture B4 - Muhlbauer Architects

Direct URL:

https://www.ome.co.il/project/%D7%A9%D7%93%D7%94-%D7%93%D7%91/

Chrome DOM capture verified:

- H1: `מתחם שדה דב 109, תל אביב-יפו`.
- Client: Shikun & Binui.
- Status: `בביצוע`.
- Rental complex with a 40-floor tower and two contextual buildings around an internal courtyard.
- Ground-level public area with commercial and community uses.
- 324 homes in varying sizes and resident shared spaces.
- Residents' club on floor 14.
- Plan area: 5 dunams; built area: 60,000 sqm.
- Architect/site identity: Muhlbauer Architects.

The page showed no publication/update date. Access date, not footer copyright, is used for current-page attribution.

## Capture B5 - Globes

Direct URL:

https://www.globes.co.il/news/article.aspx?did=1001528922

Chrome capture verified:

- H1: `היתר בנייה ראשון לפרויקט דיור להשכרה בשדה דב`.
- Published 11 December 2025 at 10:16; modified 11:33.
- Authors: Yuval Nisani and Halit Yanai-Levizon.
- Reported 324 long-term-rental homes, Muhlbauer Architects, a 38-floor tower and two 8-floor buildings, commercial frontage/resident spaces and a full first building permit after excavation/shoring authorization.
- Reported a company estimate from its Q3 report of September 2028 completion.
- Explicitly discussed a separate 511-home Shikun & Binui project; that project is excluded from lot 109.

The floor count and completion estimate are reported/datable claims, not current primary-source truth.

## Capture B6 - Nadlan Center

Direct URL:

https://www.nadlancenter.co.il/article/13451

Chrome DOM capture verified:

- H1: `מגדל בן 38 קומות: שיכון ובינוי קיבלה היתר מלא לבניית 324 יח"ד להשכרה בשדה דב`.
- Author: Dror Nir Kastel.
- Date: 11 December 2025.
- Corroborated the 324-unit rental identity, Muhlbauer Architects, full permit, 38/8 description and the reported September 2028 company estimate.
- Also mentioned the separate 511-unit project, which is excluded here.

## Inaccessible or limited sources

### Shikun & Binui report index

URL: https://shikunbinui.com/he/financial-reports/

The direct corporate page opened in Chrome, but its report list did not render into the accessible DOM after waiting. Only the investor-relations shell and navigation were visible.

### 2025 annual filing PDF

URL: https://mayafiles.tase.co.il/rpdf/1732001-1733000/P1732698-00.pdf

The direct PDF opened in Chrome but exposed an empty PDF shell to DOM inspection. A same-URL local extraction attempt did not yield reliable project text. Search snippets pointing to the PDF were therefore rejected as evidence.

## Evidence outcome

- Current construction source: B3, the March 2026 official exchange disclosure.
- Program/building-envelope source: B2, the April 2025 municipal protocol.
- Design/team/current project-page source: B4, the architect page.
- Dated press cross-check and estimate: B5-B6.
- Live target-page content is evidence of what the site currently displays, not an authority for project facts.
- Browser tabs were finalized after the last capture; no research tab was left as a deliverable or handoff.

