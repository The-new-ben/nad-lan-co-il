# YOO Tel Aviv - browser and source verification record

Verification date: 2026-08-05

Session time reference: 2026-08-05 01:12:28 +03:00 during artifact assembly.

Scope: read-only evidence capture for a future four-language YOO Tel Aviv content package. All live-page checks, localized Google searches, language-URL checks, and key public-source openings were performed in the user's real Chrome browser. No WordPress content, page, code, media, URL, or existing language product was changed.

## Browser method

- Browser: user's real Google Chrome session.
- Search engine: Google.
- Country context: Israel through `gl=il`.
- Personalization suppression: `pws=0` where exposed.
- Target interface language: separate `hl=en`, `hl=fr`, `hl=ru`, and `hl=ar` searches.
- Location evidence: the results footer showed Israel and Tel Aviv or Tel Aviv-Yafo derived from the browser or IP context.
- Evidence surfaces: autocomplete, visible organic titles, People Also Ask, and visible competitor-title wording.
- AI summaries: read only to identify question vocabulary. No AI-generated project fact, price, legal answer, or availability claim was accepted.
- Source documents: opened directly in Chrome when accessible, including PDFs.

## Live page verification

### Main page

URL: https://nad-lan.co.il/projects/yoo-tel-aviv/

Observed:

- HTTP-rendered public page loaded.
- Document language was Hebrew and direction was right to left.
- Canonical pointed to the same Hebrew URL.
- Hreflang output contained only Hebrew and x-default pointing to Hebrew.
- One H1 existed, but nine headings preceded it.
- The early showroom used the wrong `רובע שדה דב · מול הים` label.
- Visible project statistics were zero for floors, units, and high floors.
- Apartment controls were exposed without inventory.
- A generic model and generic interior content appeared.
- Sde Dov projects appeared in the nearby-project area.
- The visible main region contained approximately 4,446 whitespace-delimited tokens; the legacy article wrapper contained approximately 3,687.
- No final H2 titled `מקורות` and no complete visible public-source ledger were found.

### Language suffixes

Each URL was opened in Chrome:

| Language | URL | Result |
|---|---|---|
| English | https://nad-lan.co.il/projects/yoo-tel-aviv-en/ | Page not found |
| French | https://nad-lan.co.il/projects/yoo-tel-aviv-fr/ | Page not found |
| Russian | https://nad-lan.co.il/projects/yoo-tel-aviv-ru/ | Page not found |
| Arabic | https://nad-lan.co.il/projects/yoo-tel-aviv-ar/ | Page not found |

### Head and schema evidence

- Title: `מגדלי YOO פארק צמרת - מגה יוקרה בעיצוב פיליפ סטארק · תצוגת פרויקטים`
- Meta description: `כל המידע על מגדלי YOO פארק צמרת - מגה יוקרה בעיצוב פיליפ סטארק בתל אביב-יפו: פרטי הפרויקט, דירות ויצירת קשר עם נדלן - לפני שמתקדמים בעסקה.`
- Repeated structured-data unit value: 300.
- Broken FAQ fragment: `ו-300 יחידות דיור.`
- FAQ capability claim: floor and apartment selection despite no usable inventory.
- Structured geo: 32.0853, 34.781806.
- Date inconsistency: Yoast graph showed 2026-07-03 while a custom Article object showed 2026-06-16.

The exact structured geo was separately searched and associated with an unrelated Afeka-area location. This establishes that the current page coordinate is not safe. A replacement exact coordinate was not accepted from secondary map results.

## Localized Google verification

### English capture

Query: `YOO Towers Tel Aviv apartments for sale`

Verified autocomplete:

- `yoo towers tel aviv apartments for sale`
- `yoo tower tel aviv`
- `yoo tower tel aviv for sale`
- `yoo building tel aviv`
- `yoo towers photos`
- `yoo tel aviv`

Verified organic-title examples:

- `Luxury Apartment | Yoo Tower - Tel Aviv`
- `Park Tzameret Yoo Towers a 2.5 rooms apartment for sale`
- `YOO TOWERS | PARK TZAMERET TEL AVIV - FOR SALE`
- `Massive Luxurious Apartment On High Floor For Sale In YOO TOWER, Tel Aviv`
- `19 Nissim Aloni Street Tel Aviv, Israel`
- `Luxury apartment for sale in Yoo Towers, Tel Aviv`
- `Apartment in YOO Towers`
- `Apartment for Sale in the Prestigious YOO Tower in Tel Aviv...`

Evidence decision: exact project, resale, room-count, floor, address, and apartment-for-sale language is strong. Competitor adjectives and unit claims remain competitor language, not accepted facts.

### French capture

Query: `tours YOO Tel Aviv appartement à vendre`

Verified autocomplete:

- `tour yoo tel aviv`
- `yoo tlv`
- `yoo towers`
- `tours you tel aviv`
- `yoo tel aviv`
- `photos de yoo tel aviv`

Verified organic-title examples:

- `Tour YOO - Park Tzameret - 4,5 pièces - Tel Aviv`
- `Appartement à vendre dans les Tours YOO au Park Tzameret à Tel-Aviv`
- `Tours de luxe à Tel Aviv`
- `Appartement à vendre dans la prestigieuse Tour YOO à Tel Aviv`
- `YOO TOWERS | PARK TZAMERET TEL AVIV - À VENDRE`
- `a vendre appartement 3.5 pièces tour yoo - park tzameret ...`
- `Tour Yoo, Vue sur la mer Terrasse 3.5 pièces 25e étage`
- `Vente Appartement / Penthouse de Luxe Tel Aviv-Yafo`

Evidence decision: French results emphasize specific resale apartments, room count, floor, terrace, and view. View and terrace remain unit-specific. The page must explain completed resale and must not use VEFA framing.

### Russian capture

Query: `башни YOO Тель-Авив квартиры на продажу`

Verified organic-title examples:

- `Квартира на продажу в престижной башне YOO в Тель-Авиве`
- `Роскошные башни в Тель-Авиве`
- `Элитные квартиры на продажу в Тель-Авиве`
- `Квартира 4 комнаты 188 м² Тель-Авив, Израиль`
- `Роскошные апартаменты 4,5 комнаты - башня YOO, с ...`
- `Эксклюзивная продажа, Башня YOO, Нисим Алони 19`

Verified Google-generated question wording, used only for intent:

- `цель покупки (для жизни или инвестиций)`
- `бюджет и количество комнат`

Limitation: autocomplete switched to Hebrew during the Russian query. No Russian autocomplete phrase was accepted or reconstructed.

Evidence decision: Russian content needs a clear resale price framework, living-versus-investment comparison, unit size and room-count explanation, parking and ongoing-cost checks, and no return promise.

### Arabic capture

Project query: `أبراج YOO تل أبيب`

Broad query: `شراء شقة في تل أبيب`

Verified project autocomplete:

- `أبراج yoo تل أبيب شقق للبيع`
- `yoo towers`
- `yoo tlv`
- `yoo tower tel aviv`
- `yoo tel aviv`
- `yoo towers tel aviv`

Verified broad organic-title examples:

- `شراء شقة تل أبيب : 421 عقارات للبيع حصريًا`
- `223 شقق سكنية للبيع في منطقة تل أبيب`
- `شراء عقار في منطقة تل أبيب: 749 شق ومنازل للبيع حصريًا`
- `جميع العقارات في تل ابيب - يافا، إسرائيل`
- `179 شقق سكنية للبيع في تل ابيب - يافا`
- `شراء عقار سكني في تل أبيب-يافا`

Verified People Also Ask:

- `هل يُسمح للأجانب بشراء عقارات في تل أبيب؟`
- `كم سعر شقة 100 متر؟`
- `هل يمكنني شراء شقة في إسرائيل؟`
- `ما هي الإجراءات المتبعة عند شراء شقة؟`

Google-generated project wording inspected only for intent included a question about preferred room count or area and a question about budget. No generated price or project claim was accepted.

Evidence decision: Arabic content needs native right-to-left presentation, verified availability, apartment area and family usability, total costs, buyer procedure, education and services, and unit-alteration checks. It must not promise Arabic service, school admission, a sea view, or foreign-buyer eligibility.

## Public source verification

### Habas 2007 annual report

URL: https://mayafiles.tase.co.il/RPdf/410001-411000/P410977-00.pdf

Chrome result: PDF opened successfully.

Verified document evidence:

- The YOO Tel Aviv project is described in Park Tzameret.
- The filing states up to 297 apartments in two residential towers.
- It gives 41 and 37 floors above ground and three underground parking levels.
- It identifies parcels 717 and 718 in block 6108, lots 1 and 2, plans 1750 and 1750a, and approximately nine dunams.
- It describes circular tower envelopes, an entrance floor, technical roof floors, parking and service spaces, and granite, aluminum, and glass cladding.
- It documents an original flexible-layout concept and common facilities.
- It names Classic, Nature, Culture, and Minimal design directions.
- It records 2004 permits, a December 2005 change permit, and staged 2007 construction and occupancy.

Accepted scope: original project facts and dated development status. Rejected scope: current inventory, current unit total, current operation of facilities, current charges, and current price.

### Official YOO portfolio

URL: https://www.yooresidences.com/property/yoo-tel-aviv/

Chrome result: page opened and rendered.

Verified fields:

- Designer: YOO Inspired by Starck
- Developer: Habas Group
- Location: Tel Aviv, Israel
- Type: Residential
- Status: Sold

Accepted scope: first-party brand attribution and sold project status. Rejected scope: live private resale availability or project-wide pricing.

### Tel Aviv municipal planning document

URL: https://www.tel-aviv.gov.il/Residents/Development/DocLib/%D7%A1%D7%93%D7%A8%20%D7%99%D7%95%D7%9D%2023-0007%20%D7%9E%D7%99%D7%95%D7%9D%203-5-2023.pdf

Chrome result: PDF opened successfully.

Verified evidence:

- Nissim Aloni 19.
- Building referred to in that document as YOO 2.
- Existing-condition description of 40 floors and 126 dwelling units.
- A planning matter concerning floors 36-37 and a unit combination or change.
- A plan maximum of 154 units for that building is not the same as its stated existing count.

Accepted scope: the specific municipal planning record. Rejected inference: definitive mapping of both YOO tower numbers and addresses.

### Alum Eshet project record

URL: https://www.alumeshet.co.il/en/projects/yoo-towers/

Chrome result: page opened and rendered.

Verified evidence:

- Approximately 25,000 square metres of curtain walls and windows.
- Circular profiles, glass, tilt-and-turn windows, and sliding terrace doors.
- Year 2009.
- Philippe Starck, Moore Yaski Sivan, Habas Group, and U. Dori named in project roles.
- The supplier page states 35 and 39 floors.

Accepted scope: contributor roles, facade scope, and professional project record. Conflict: its floor counts are not used as the master because they differ from the Habas filing.

### Ministry of Justice 2023 insolvency report

URL: https://www.gov.il/BlobFolder/reports/new_2023-report/he/REPORT2_2023.pdf

Chrome result: PDF opened successfully.

Verified evidence: the Habas group, including the parent and subsidiaries, is described as being handled wholly in liquidation.

Accepted scope: historical-developer status and present corporate context. Rejected inference: a generalized defect in title or condition of a privately owned YOO apartment.

### NTA M1 page

URL: https://www.nta.co.il/metro/%D7%A7%D7%95-m1/m1-%D7%91%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91/

Chrome result: page opened and rendered.

Verified evidence: official planned M1 Tel Aviv station naming includes Namir-Pinkas and Tel Aviv Center, and the page describes early works or planning context.

Accepted scope: planned transport context. Rejected inference: current operation, guaranteed completion date, or verified walk time.

### Tel Aviv municipal education page

URL: https://www.tel-aviv.gov.il/Pages/MainItemPage.aspx?ItemID=2427&ListID=81e17809-311d-4bba-9bf1-2363bb9debcd&WebID=3af57d92-807c-43c5-8d5f-6fd455eb2776

Chrome result: page opened and rendered.

Verified evidence: a dated 2024-2025 school-year update describes expansion of the Tzamarot Ayalon school.

Accepted scope: neighborhood education context at that date. Rejected inference: present admission, catchment, language service, or guarantee for a buyer's child.

### Globes 2023 completed sale

URL: https://www.globes.co.il/news/article.aspx?did=1001448036

Chrome result: article opened and rendered.

Publication date verified: 2023-06-03.

Verified reported transaction:

- Nissim Aloni 21.
- 3.5 rooms.
- 123 square metres.
- Floor 12 of 37.
- NIS 6.65 million completed sale.
- Three underground parking spaces and storage reported for that apartment.
- Building facilities reported in the article included a pool, club, and gym.

Accepted scope: one dated completed transaction and the article's description. Rejected inference: current average, current asking price, or rights attached to another unit.

### Globes 2026 one-apartment dispute

URL: https://www.globes.co.il/news/article.aspx?did=1001533787

Chrome result: article opened and rendered.

Publication date verified: 2026-02-03.

Verified report scope:

- One apartment at Nissim Aloni 21.
- A canceled sale or dispute involving alleged unpermitted renovation work.
- An expert opinion concerning removal of a protective wall associated with a safe room.
- Claims and counterclaims were reported.

Accepted use: a narrow example of why a resale buyer should compare approved plans, permits, and the apartment as built. Rejected use: project-wide defect, established liability, or final judicial finding.

### Ministry of Justice Land Registry Extract service

URL: https://www.gov.il/en/service/land_registration_extract

Chrome result: page opened and rendered.

Verified title: `Generation of a Land Registry Extract (Tabu Extract) from the Land Registers | Land Registry and Settlement of Rights`.

Verified service scope:

- Any person may order an official registration extract for a fee.
- The extract can show registered owners, liens, mortgages, attachments, court orders, and restrictions.
- Information is accurate as of the extract's generation date.
- A joint-house apartment requires the correct block, parcel, and sub-parcel.
- The sub-parcel is not necessarily the apartment number.
- The page was last updated on 2026-06-16 when verified.

Accepted use: the common apartment-rights verification process across all four future language pages. Rejected inference: a clean or complete title for an unidentified YOO apartment.

### Israel Tax Authority purchase-tax simulator

URL: https://www.gov.il/en/service/real_eatate_taxsimulator

Chrome result: page opened and rendered.

Verified title: `Simulator - Calculator for calculating property purchase tax | Israel Tax Authority`.

Verified service scope:

- It calculates purchase tax legally due when buying a property right.
- Inputs include the law effective on the purchase date, property type, eligibility or discount category, and transaction value.
- The calculation is anonymous and produces an amount in NIS.
- The page was last updated on 2026-08-03 when verified.

Accepted use: direct every buyer to a current transaction-specific calculation. Rejected use: hard-coded evergreen tax result or a category inferred from language, citizenship, residence, or relocation intent.

### Government real-estate information database

URL: https://www.nadlan.gov.il/

Chrome result: the government real-estate site opened and rendered.

Verified page language:

- The site describes itself as the home of government real-estate data.
- It says property and transaction data are aggregated, standardized, and filtered from government databases.
- It offers map, free-text, block and parcel, neighborhood, and address search.
- It invites users to inspect property details and transaction history and compare transaction and rental prices.

Accepted use: assemble dated transaction evidence and test an asking price. Rejected use: treat every nearby sale as a comparable without checking unit, building, rights, area, floor, condition, parking, storage, and transaction type.

### Bank of Israel mortgage guidance

URL: https://www.boi.org.il/en/information-and-service-to-the-public/banking-customer-service-information/financial-education/the-reform-to-increase-information-transparency-and-competition-in-mortgages/

Chrome result: page opened and rendered.

Verified title: `The reform to increase information transparency and competition in mortgages | Bank of Israel`.

Verified guidance:

- The page describes the approval-in-principle and mortgage-offer comparison process.
- It defines LTV as the approved facility relative to the property value recognized by the bank, with the relevant value not exceeding the lower of the appraisal and contract-cost framework.
- After opening the relevant FAQ, the page showed maximum LTV rates of 75 percent for a single dwelling, 70 percent for a replacement dwelling, and 50 percent for an investment dwelling or an all-purpose loan backed by a residence.

Accepted use: explain the regulatory framework and why buyers need a real lender process and appraisal. Rejected use: promise approval, a specific rate, or a universal financing percentage to non-resident or cross-border buyers.

## Secondary observations not promoted to facts

- Broker results showed changing asking prices and individual apartment details. These were retained as intent evidence only.
- Search-generated summaries surfaced price ranges and legal answers. These were rejected as evidence.
- Secondary maps placed Nissim Aloni 19-21 near 32.0906, 34.7965. This is sufficient to show the live schema is wrong when compared with the street location, but not sufficient for publication of exact authoritative geo coordinates.
- A professional contributor record at https://www.danielazerrad.com/yoo describes a 2001-2009 project period, two towers, 297 retail apartments, and approximately 58,000 square metres. The project and period can corroborate other sources, but the area scope is unclear and remains excluded from the factual baseline.

## Fact-status labels for future drafting

| Label | Meaning | Example |
|---|---|---|
| Original plan | Documented project intent or maximum, not current register | Up to 297 apartments |
| Historical stage | True as of a dated report | First-tower occupancy began by the end of 2007 |
| Current first-party status | Current state shown by the brand page | Sold |
| Municipal record | Fact within a specific planning document | Nissim Aloni 19 described as 40 floors and 126 existing units in that record |
| Completed transaction | Dated closed sale reported by a reputable outlet | NIS 6.65 million in June 2023 for the described unit |
| Asking price | Seller or broker request at capture time | Not accepted as a completed value |
| Estimate, non-binding | Transparent calculation, not a sourced fact | No such estimate was produced in this research pass |
| Unknown | Not published or not verified | Current management fee |

## Contradictions verified rather than resolved by guessing

- 297 original maximum versus 300 live-page shorthand versus unknown current registered total.
- 41 and 37 floors versus 35 and 39 supplier counts versus 40 in one municipal building record.
- Unstable tower-number mapping across addresses 19 and 21.
- Staged occupancy beginning in 2007 versus professional completion around 2009.
- Existing page's approximately 100,000 square metres versus a contributor's approximately 58,000 and a supplier's 25,000-square-metre facade scope.
- Live schema coordinate versus actual Nissim Aloni street location.

The editorial resolution for each contradiction is in `00-source-ledger.md`.

## Verification blockers and required future refreshes

No blocker prevented completion of this research package. The following claims remain blocked unless new evidence is obtained:

- Exact current registered apartment total.
- Definitive YOO 1 and YOO 2 address mapping.
- Current resale inventory.
- Current project-wide asking or completed price range.
- Current management charges and facility status.
- Exact authoritative geo coordinates.
- Current school catchment and admission.
- Apartment-level plan, alterations, parking, storage, view, and rights.

Before any future article is published, refresh all time-sensitive web sources and any cited current listing. Search-result wording and inventory can change after this dated capture.

## Change-control record

- Created research artifacts only inside `yoo-tel-aviv-content-package-2026-08-05`.
- Did not edit the live Hebrew YOO page.
- Did not create EN, FR, RU, or AR WordPress posts.
- Did not alter canonical or hreflang output.
- Did not edit code, models, maps, media, shared engines, or other project pages.
- Did not touch MEIER or any completed project package.
