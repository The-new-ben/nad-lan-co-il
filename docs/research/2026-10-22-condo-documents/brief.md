# Condo documents for buyers (C12): research brief (page + tool)

Prepared 22.10.2026 by a research agent (Opus 5.5) for nad-lan.co.il. Read-only on every live site: nothing was written to WordPress, no form was submitted, no order was placed.
All times are Israel time (UTC+3) on 22.10.2026 unless stated.

Intent family: "תשריט בית משותף", "מסמכי בית משותף", "תיק בית משותף", "הזמנת תיק / מסמכי בית משותף", "תקנון בית משותף" (מצוי / מוסכם), "צו רישום בית משותף", הצמדות, and the unregistered-building question.

> Raw files live outside the repo: `C:/Users/777/nad-lan/_private-research/2026-10-22-condo-documents/raw/` (`gov-pages/` = official texts and PDFs, `competitors/` = competitor HTML and `structure.json`, `gsc-*.csv` = Search Console rows, `dfs-volume*.json` = DataForSEO answers). No competitor prose is copied here.

---

## 0. The short version

| Item | Value | Evidence |
|---|---|---|
| Official ordering service | https://www.gov.il/he/service/common_house_files (page updated 14.12.2025) → order button goes to https://fileextractor.justice.gov.il/tabu | read 22:43 |
| Fee | **39 NIS per order** (2026). Live system text: 39 NIS regardless of how many files of that building are ordered. Same 39 NIS in the official 2026 fee notice, item 7(ד1). Physical file inspection at an office with photocopy: **257 NIS** (item 8(2)). Fees change every 1 January by the CPI. | fileextractor 22:43; fee notice signed 21.12.2025, valid from 1.1.2026 (page https://www.gov.il/he/pages/fees-2026, published 23.12.2025, updated 24.12.2025) |
| What you get | Registration file: order + bylaws + drawing. Amendment file: amendment order or amended bylaws. Cancellation file: cancellation order. Scanned, e-signed, one ZIP; email link within 24 hours. | service page |
| URL | **/real-estate-lawyer/condo-documents/**: "condo" 0 owners, "documents" 0 owners (4,594 live URLs) | `url_word_audit.py` 22:39 |
| H1 | מסמכי בית משותף: איך מזמינים צו, תקנון ותשריט, ומה בודקים בהם לפני קנייה (72 chars) | `title_start_audit.py` OK |
| SEO title | תשריט בית משותף ותיק הבית המשותף: הזמנה, עלות וקריאת המסמכים (60 chars) | OK |
| Breadcrumb | מסמכי בית משותף | OK; trio OK |
| Demand | core family about **10,000 searches a month** (deduplicated); head term תשריט בית משותף 2,400. Top five terms: Jul to Sep 2026 is 13% below Oct to Dec 2025. | `keywords.csv` |
| AI overview | **present on all 7 SERPs** checked. Cites gov.il service, fileextractor, nadlancenter, dabullaw, tabu.co.il. | `serps.json` |
| nad-lan today | no page; 1 impression ("בדיקת רישום בית משותף" on /tabu-extract-check/) in 90 days | GSC 22:41 |
| jus-tice today | /condominium-registration-order/ 18 impressions, position 54, 0 clicks; the roof ruling page gets the most condo traffic (554 impressions, 8 clicks) | GSC 22:41 |
| DataForSEO spend | **about $0.20** (two volume calls $0.09 each + seven SERP calls $0.016) | API responses |

---

## 1. Official facts

### 1.1 Ordering the condo file (the buyer's path)

Source: https://www.gov.il/he/service/common_house_files ("updated 14.12.2025"), read 22:43; live system https://fileextractor.justice.gov.il/tabu read 22:43; user guide PDF https://fileextractor.justice.gov.il/TabuUserGuids.pdf (undated).

1. Find the file, one of two ways:
   - by block (גוש) and parcel (חלקה), plus a captcha; or
   - by file number: pick the land registry office, pick the registration year, type the file number that the land extract (נסח) shows as "תיק יוצר"; from 1975 on, the number shown as "שטר יוצר".
   - Block and parcel can be found on the Survey of Israel finder: https://www.gov.il/apps/mapi/parcel_address/parcel_address.html (linked from the service page).
   - **The official system has no search by street address.** Resellers sell "by address"; Google's AI overview says "sometimes by address". Do not promise address search.
2. Add the file to the basket. Up to three files of the same block and parcel in one order. One building may have several files (registration, each amendment, a cancellation and a re-registration), so the buyer should take all of them.
3. Pay by credit card and give an email address. No VAT on state fees.
4. A ready-notice arrives by email within 24 hours; download the ZIP from the link. Viewing needs Acrobat Reader.
5. Help: *8653, extension 7 then 1 (abroad 972-8-6831663), Sunday to Thursday 8:00 to 16:00; human chat; WhatsApp 073-3929983. The page carries a banner about phone changes on Tuesday 27.10.2026.

Notes printed on the service page:
- Files up to and including 1969 hold an agreement (הסכם) instead of bylaws, if any.
- Not every amendment file has a drawing.
- Not every condo has registered bylaws. Where none was registered, the model bylaws in the first schedule of the Land Law apply.

**Fee.** 39 NIS per order. Read on the live system ("עלות ההזמנה הינה 39 ₪ ללא תלות במספר התיקים שהוזמנו בגין הבית המשותף המבוקש") and in the official notice הודעת המקרקעין (אגרות), התשפ"ו-2025, item 7(ד1): inspection by receiving a copy of the scanned condo registration file, e-signed, online: 39. Notice PDF: https://www.gov.il/BlobFolder/news/fees-2026/he/files_fees-2026.pdf (signed 21.12.2025, valid from 1.1.2026). Base in the regulations: 33 NIS adjusted to 2016; amounts change every 1 January by the November CPI (Land Regulations (Fees) 1974, reg 2(ב)).
- Conflict to flag: the undated user guide says a fee is paid "for each file separately". The live page says 39 NIS regardless of the number of files. Publish the live wording and re-check on build day.
- Old figure still on competitor pages: 33 NIS (batim.org.il, gershon-catz 2021).

Other fees from the same notice (useful for the page, all 2026): electronic signed land extract 18; certified extract 88; concentrated extract of all condo apartments 154; physical condo file inspection with photocopy 257; condo registration application 163 + 98 per apartment; amendment application 163, objections 163, 98 per added apartment; registering agreed bylaws 163; registering a change in bylaws 163; request to appoint a house committee exempt.

### 1.2 The law: Land Law 1969, chapter 6 (בתים משותפים)

Text read on Wikisource (secondary copy of the official text), 22:44. Raw: `raw/gov-pages/land-law-wikisource.txt`.

| Section | What it says (plain English) | Use on the page |
|---|---|---|
| 52 | A condo is a building with two or more flats that is registered in the condo register. Common property = every part except the registered flats, incl. land, roofs, outer walls, foundation, stairwells, lifts, shelters, and shared heating or water installations even inside a flat. | "Is the roof mine?" answer: by default no. |
| 54 | Each flat is a separate unit of ownership. | |
| 55 | Each flat carries an undivided share of the common property; a deal in a flat includes that share; common property cannot be sold separately. The owners may set in the bylaws that a specific part of the common property is attached (צמוד) to a flat, except stairwells, lift, shelters and installations serving all. An attached part is treated like the flat. | Core of the tool: parking, storage, roof, yard become a flat's only through attachment. |
| 57 | Share in common property = flat floor area ÷ all flats' floor area, unless the bylaws set otherwise; balconies and outer walls not counted unless the bylaws say so. | "Share" row in the tool. |
| 58 | Each owner pays upkeep of common property by the same ratio, unless the bylaws set another rate. | "Who pays what" row. |
| 59 | Building with several structures or wings: the bylaws may attach each wing's common property to its flats and run it separately (separate committee). | FAQ (PAA asks about s.59). |
| 61 to 64 | The condo runs by bylaws. Agreed bylaws (תקנון מוסכם) are made or changed by owners holding two thirds of the common property; but attaching a part of the common property to a flat needs **all** owners' consent (62(א)). An attachment may move to another flat in the building without the others' consent through s.145 (62(א1)). Registered bylaws bind later buyers (62(ג)). Where no bylaws were registered, or they are silent, the model bylaws apply (64). | "מצוי מול מוסכם" table; red flag "use agreement not registered". |
| 71ב | Extension of flats: owners of three quarters of the flats holding two thirds of the common property may decide to take out parts of the common property and attach them for an extension, and divide the building rights; for a safe room (ממ"ד / ממ"ק), owners of 60% of the flats. Objections to the Supervisor within 30 days (71ג). | Majorities table; roof and building rights row. |
| 72 | Disputes between owners under the bylaws go to the Supervisor of Land Registration. | |
| 77א to 77ו (chapter 6.1) | Buildings with two flats or more that are **not** registered as a condo: many chapter 6 rules apply (77ב) and the building runs by the model bylaws (77ג). Applied by order region by region; per the Wikisource note every district is covered. | "Building not registered" branch. |
| 141 to 147 | Condo register in each office. A building with two or more identifiable flats can be registered (142). The Supervisor gives the order when asked by owners holding **more than half of the floor area** (143(א)); the order lists each flat's particulars (143(ב)). Amendment on a request by an owner, after notice and a chance to object to every owner (145). Cancellation (146-147). | Process facts; jus-tice handles the legal service. |
| Schedule (model bylaws) | s.2: an owner may not make changes in his flat that harm the common property (incl. the building's uniform outer look) without the general assembly's consent; s.12: decisions by majority, but no new duties or payments on an owner without his consent. | Balcony closing, roof works. |

### 1.3 Regulations: Land Regulations (Management and Registration) 2011, regs 54 to 63

Wikisource text, 22:44.
- 54: the registration request goes to the Supervisor of the area, with (1) a drawing approved by a planning institution, **or another drawing** that gives the Supervisor a faithful picture; (2) bylaws, or notice that the model bylaws are adopted; (3) a proposed temporary committee.
- 55(ב) and 56: the order states whether the condo was registered on a planning-approved drawing or on "another drawing", and the registrar records this for every parcel. **Buyer check:** it tells you whether the drawing was approved by the local committee.
- 58 and 59: an amendment request needs a planning-approved drawing (another drawing only for special reasons), copies for every owner and right-holder; objections within 15 days; the Supervisor decides on the papers.

### 1.4 What the drawing shows and how attachments are marked

Source: "הוראות עריכת תשריט בית משותף" page https://www.gov.il/he/pages/common-house (published 23.05.2021), PDF of 138 slides https://www.gov.il/BlobFolder/generalpage/common-house/he/common-house.pdf, read 22:46.

- Drafter: architect, licensed surveyor, engineer or certified technician; printed and signed.
- Header: block, parcel, parcel area, address of each structure or entrance.
- Building: structures (Roman numerals), wings (numbers), entrances (letters), floors.
- Sub-parcel table per flat: floor, description (flat, shop, storage...), sub-parcel number (parcel/flat), floor area (by the Sale specification order 2008, standard 9.0, for contracts from 24.5.2008), attachments with **letter marking**, area and **colour**. The flat and its attachments share one colour; black is not allowed. Shared attachments go in a separate table and may be striped in the owners' colours.
- Balconies: covered balcony = part of the flat; open, uncovered or sun balcony = an attachment.
- Storage: physically separate = attachment only; storage with direct access only from the flat = part of the flat; the description may not read "flat + storage".
- Parking: **no more than two parking spaces may be attached to one flat** without the local planning authority's approval (Planning and Building Law s.158א1, as quoted in the official instructions).
- Roof plan: dimensions; access to roof installations (solar heaters) over common property, or the agreed bylaws must give a right of passage.
- Laundry niche: three registration options (outside the flat area, attachment, or common property with an exclusive-use clause in the bylaws).
- Deviations from the parcel border or from the building permit are drawn in **dashed lines** with sizes, are not counted in the flat area, and are listed in the drafter's declaration "remarks".
- Scales: surroundings 1:1250, parcel 1:250, floors 1:100.
- **Validity: one year from the drafter's signature**; renewed by signing again. (nadlancenter says six months. That is wrong per this source.)

### 1.5 Changing the order (תיקון צו) and the bylaws

Sources: Land Law s.145; regs 58-59; procedure page https://www.gov.il/he/pages/common-house-amendment-inf (published 13.06.2021) and its PDF, read 22:45.
- Used for new building in a flat or the house (incl. under the bylaws or ss.71א-71ד), registering or changing agreed bylaws (s.62(א)), and moving an attachment between flats (s.62(א1)).
- Needs: application signed and verified by a lawyer; consents of owners and of right-holders (mortgage bank, receiver, holder of a warning note); a drawing by a qualified drafter approved by the local committee; agreed bylaws in two originals; approvals of no debts from land tax, the municipality and the local committee; fee. Owners who did not consent get notices; objections within 15 days.
- Majorities in one table (for the page):

| Act | Who must agree | Source |
|---|---|---|
| Ask to register the building as a condo | owners of more than half of the floor area | s.143(א) |
| Make or change agreed bylaws | owners holding 2/3 of the common property | s.62(א) |
| Attach part of the common property to one flat (parking, roof, yard) | all owners | s.62(א) |
| Move an existing attachment to another flat in the building | no other owners' consent; through an amendment of the order | s.62(א1), s.145 |
| Extension of a flat with attachment of common property | 3/4 of the flats holding 2/3 of the common property | s.71ב(א)(1) |
| Safe room extension | 60% of the flats | s.71ב(א)(1) |
| Changes in a flat that harm common property or the outer look | general assembly consent | model bylaws s.2(א) |

### 1.6 New building: when must the developer register?

Source: Sale (Apartments) Law 1973, s.6ב (added 2011), Wikisource text 22:44.
- The seller must act for registering the parcellation (חלוקה ואיחוד) as early as possible;
- **register the house as a condo within one year** from registering the parcellation, or from handing the flat to the buyer, whichever is later;
- **register the buyer's rights within six months** from the condo registration, or from handover, whichever is later;
- delays proven to be outside the seller's control are not counted (6ב(ג)).
- s.6: if the developer's bylaws change the model bylaws on taking out common property, the flat's share, expense shares or decision rules, the details must be in the specification or contract; if not, the model bylaws apply on that matter.
- s.6ג: caps the legal fees a developer may charge buyers for registration (amount set in regulations of 2014; not read).

### 1.7 Building not registered: housing company or Israel Land Authority

- Israel Land Authority service "בקשה לרישום, לתיקון או לביטול צו בית משותף", https://www.gov.il/he/service/guide-apartment-building-warrant (updated 29.10.2023), read 22:47: the request is filed by the housing company (גורם משכן) per the contract, or without one by the unit owners; registering the condo is a necessary step before rights are registered at the Land Registry; RMI checks and signs the papers, then they go to the Supervisor. RMI phone *5575 or 03-9533333.
- Until the building is registered, owners usually hold undivided shares (מושע) in the parcel, and the flat split and attachments rest on agreements (dabullaw describes this; consistent with s.77א's definition). Chapter 6.1 makes the model bylaws apply.
- What a buyer can do (for the page, wording to be checked by a lawyer): ask the housing company or RMI for the confirmation of rights; check the parcel extract for warning notes and a co-ownership agreement; for a new project, check the s.6ב deadlines in the contract.

### 1.8 Land Registry and Supervisor offices

gov.il branch finder (office id 7f339ddd-6295-4025-8991-2c5a3ea2a76f), read 22:48 to 22:52; all by appointment.
- Land registration offices: Jerusalem, Tel Aviv, Haifa, Be'er Sheva, Petah Tikva, Netanya, Rehovot, Holon, Rishon LeZion, Nof HaGalil; branch in Hadera.
- Supervisor offices: Jerusalem, Tel Aviv, Haifa (administrative), Haifa judicial (sits in Acre), Be'er Sheva, Petah Tikva, Rehovot, Holon, Netanya, Nof HaGalil; branches in Acre and Ashdod.
- Registration of a condo (lawyers): online with a smart card, or by hand or post, https://www.gov.il/he/service/common-house-registration-application (updated 18.09.2025).

### 1.9 Not verified (do not publish until checked)

1. Fee per order vs per file: live system says per order (39 NIS for the building); the undated user guide says each file separately. Re-check on build day.
2. Coverage: whether every registered condo file is scanned and online. The guide says some files sit under a different block/parcel; if not found, call *8653.
3. Law texts were read on Wikisource, not on Nevo or the Knesset site. Amendments after the last Wikisource edit could be missing.
4. Planning Law s.158א1 (more than two parking spaces) was read only as quoted in the official drawing instructions, not in the law text.
5. The cap on developers' legal fees (Sale law s.6ג, 2014 regulations): amount not read.
6. Typical waiting time at the Supervisor for registration or amendment: no official figure found.
7. Competitor claims not to repeat: drawing valid 6 months (official: one year); drawing made under the Planning and Building Law (it is under the Land Law and regs 54-55); "compare drawing area with arnona area" (no official basis); "130 NIS for a drawing" (that price is a five-extract bundle on tabu.co.il, see 3.3).

---

## 2. Our coverage and the sister site

### 2.1 Strings and URL (tools run 22:39 to 22:55)

- `url_word_audit.py --token condo` → 0 URLs; `--token documents` → 0 URLs (4,594 live URLs). Also 0 for condominium, registration, bylaws, document, shared. "lawyer" is the existing family head (/real-estate-lawyer/...), so the new slug extends a family.
- `title_start_audit.py --check`: H1 OK, SEO title OK, breadcrumb OK; `--trio` → "three different strings".
- SEO title is 60 characters, at the edge. Checked shorter fallback (56, OK): תשריט בית משותף ותיק הבית המשותף: איך מזמינים ומה בודקים. Keep the gap-map title; it carries "עלות", which matters because "חינם" (210) and "מחיר" are related searches.

### 2.2 Search Console (22.7 to 20.10.2026, pulled 22:41)

nad-lan (sc-domain:nad-lan.co.il, 9,557 query-page rows): 3 condo rows, 11 impressions, all off-topic except one ("בדיקת רישום בית משותף", 1 impression, /tabu-extract-check/, position 48). /tabu-extract-check/ as a page: 1,074 impressions, position 40.5, 0 clicks.

jus-tice (https://jus-tice.co.il/, 27,350 rows): 52 condo-query rows, 323 impressions, 0 clicks.

| jus-tice page | Impressions | Clicks | Position | Note |
|---|---|---|---|---|
| /building-rights-beit-hadar-ownership-roofs-ruling-7808/ | 554 | 8 | 26 | roof building rights (Beit Hadar ruling); queries "זכויות בניה על גג בית משותף" 161, "בנייה על גג בית משותף" 45 |
| /beit-hadar-ruling-new-roof-tenants-precedent/ | 72 | 4 | 14 | same topic |
| /shared-house-common-property/ | 30 | 0 | 63 | "רכוש משותף בבית משותף" |
| /condominium-registration-order/ | 18 | 0 | 54 | "מסמכי בית משותף" 3, "רישום בית משותף" 3, "תיק בית משותף" 2, "הזמנת תיק בית משותף" 1 |
| /supervisor-condominium-disputes/ | 8 | 0 | 61 | |
| /amending-condominium-order/ | 0 | 0 | | exists (200) |

Filtered rows: `raw/gsc-nad-lan-condo-filtered.csv`, `raw/gsc-jus-tice-condo-filtered.csv`, page totals `raw/gsc-justice-pages-*.csv`.

### 2.3 Split between the two sites

- **nad-lan (this page):** the buyer's job. Which document answers my question, how to order it in five minutes for 39 NIS, how to read the drawing, red flags before signing, what to do when the building is not registered. Owns "תשריט בית משותף", "מסמכי בית משותף", "תיק בית משותף", "הזמנת ..." and "תקנון בית משותף" for buyers.
- **jus-tice:** the legal service. Registering a condo, amending the order, disputes before the Supervisor, roof building rights rulings. Its /condominium-registration-order/ title already targets "רישום בית משותף: התנאים והאגרות 2026"; keep it there. Do not retitle jus-tice pages toward "מסמכי בית משותף" or "תשריט".
- **Links:** yes, nad-lan should link to jus-tice, two contextual links only, no sitewide block:
  1. In "the drawing does not match what you see" → https://jus-tice.co.il/amending-condominium-order/
  2. In the roof row of the tool ("building rights on the roof") → https://jus-tice.co.il/building-rights-beit-hadar-ownership-roofs-ruling-7808/ (jus-tice's strongest condo page).
  - Optional third, in "building not registered / new building": https://jus-tice.co.il/condominium-registration-order/.
  - Reverse: jus-tice /condominium-registration-order/ and /amending-condominium-order/ link once to the nad-lan tool ("איזה מסמך עונה על השאלה שלכם").

---

## 3. Demand, SERPs and competitors

### 3.1 Volumes (Google Ads via DataForSEO, Israel 2376, Hebrew, 22:35; `keywords.csv`, 86 keywords, 60 with volume)

| Keyword | Monthly | CPC USD |
|---|---|---|
| תשריט בית משותף | 2,400 | 2.52 |
| מסמכי בית משותף | 1,000 | 2.80 |
| תיק בית משותף | 1,000 | 2.37 |
| הזמנת תיק בית משותף | 880 | 2.69 |
| הזמנת מסמכי בית משותף | 590 | 2.25 |
| תקנון בית משותף | 390 | 1.98 |
| רישום בית משותף | 390 | 7.45 |
| הזמנת תשריט בית משותף | 390 | 1.87 |
| המפקח על בתים משותפים | 260 | 6.53 |
| המפקח על רישום מקרקעין (= המפקחת, one cluster) | 260 | 2.11 |
| תשריט בית משותף חינם | 210 | 1.12 |
| תקנון מצוי בית משותף | 170 | |
| חוק המקרקעין בתים משותפים | 170 | 1.67 |
| חברה משכנת | 170 | 11.90 |
| תקנון מצוי | 140 | |
| תשריט דירה | 140 | 1.60 |
| תיקון צו בית משותף | 110 | |
| צו בית משותף | 90 | 3.53 |
| הוצאת תשריט בית משותף | 90 | 2.56 |
| תשריט בית משותף להורדה | 70 | 1.51 |
| צו רישום בית משותף / תקנון מוסכם בית משותף | 50 each | |
| 10 to 40 each | תיק בית משותף טאבו, נסח בית משותף, תקנון מוסכם, שינוי תקנון בית משותף, תיקון צו רישום בית משותף, חניה / מחסן / סגירת מרפסת / בניה על הגג בבית משותף, דירה לא רשומה בטאבו | |

- Core family, Google's close-variant duplicates removed: **about 9,980 a month**.
- Adjacent, owned by other pages: נסח טאבו 49,500 (/tabu-extract-check/), טאבו 9,900, חוק המקרקעין 6,600, לשכת רישום מקרקעין 1,600 (+ city forms 450), רשם המקרקעין 720.
- No volume: הצמדת חניה / מחסן / גג / חצר, בית משותף לא רשום, תשריט בית משותף אונליין, עלות הזמנת תיק בית משותף. The questions exist inside the head terms, not as their own searches.
- Seasonality: peaks in May-June and Nov-Dec (2,900 for the head term); the top five terms sum to 16,700 in Jul-Sep 2026 against 19,170 in Oct-Dec 2025 (-13%).

### 3.2 SERPs (DataForSEO live advanced, desktop, Israel, Hebrew, 22:36; full lists in `serps.json`)

AI overview: **present on all seven** (five biggest terms + תקנון בית משותף + רישום בית משותף). All seven link the gov.il ordering service; five also link fileextractor. The "הזמנת מסמכי בית משותף" overview states 39 NIS, 24 hours, ZIP and *8653. The "תשריט בית משותף" overview repeats tabu.co.il's "130 NIS instead of 183" as if it were the drawing price. It is not (see 3.3).

| Keyword | Top 3 organic | Notes |
|---|---|---|
| תשריט בית משותף (2,400) | midrag video (2024), adrichalut (drafting service), efi-aharon (link list) | nadlancenter 5049 at 4, dabullaw 6, gov.il amendment guidelines 7; images pack of sample drawings |
| מסמכי בית משותף (1,000) | gov.il service, fileextractor, tabu.co.il | dabullaw 6, harel-vered 7, batim 8, gershon-catz (33 NIS, 2021) 9 |
| תיק בית משותף (1,000) | efi-aharon, kolzchut bylaws, adrichalut | gov.il amendment 5, midrag Q&A 6 |
| הזמנת תיק בית משותף (880) | poleg-law, ygoldlaw drawing guide, tabu.co.il guide | **gov.il service not in the top 10** |
| הזמנת מסמכי בית משותף (590) | kolzchut, lawx, lawyerhaifa | municipal committee pages (Rishon LeZion, Ramat HaSharon, Pardes Hanna), gov.il drawing rules 5 |
| תקנון בית משותף (390) | kolodnylaw (2021), mishpati ("2019"), batim sample bylaws | the only SERP with PAA |
| רישום בית משותף (390) | gov.il registration service, gov.il ordering service, nadlancenter 5049 | mor.law (27.9.2026), limorarbel, ygoldlaw |

People also ask (only on "תקנון בית משותף"): מהו תקנון בית משותף מצוי? · מה קובע סעיף 59 לחוק המקרקעין? · האם גג הוא רכוש משותף? · מהו הסכם שיתוף במקרקעין? · האם חובה לרשום הסכם שיתוף בטאבו? · איזה עורך דין יכול לעזור לי לפירוק שיתוף במקרקעין?

Related searches that matter: תשריט בית משותף חינם · תשריט בית משותף להורדה · תשריט בית משותף מחיר · תשריט בית משותף gov · הזמנת מסמכי בית משותף משרד המשפטים · הזמנת תיק בית משותף מקוון · איתור תשריט בית משותף · תשריט בית משותף דוגמא · תקנון מצוי בית משותף pdf / להורדה · תקנון מוסכם בית משותף · שינוי תקנון בית משותף · עיריית ירושלים / פתח תקווה / רמת גן / תל אביב תשריט בית משותף · רישום בית משותף רשות מקרקעי ישראל · צו רישום בית משותף.

AI-overview follow-up prompts (what Google thinks users want next): how to read the drawing, how to check attachments (parking, storage), what to do when the drawing does not match reality, how to find block and parcel, how to check if agreed bylaws exist.

### 3.3 Competitor pages read in full (22:47 to 22:54; HTML in `raw/competitors/`, structure in `raw/competitors/structure.json`)

| Page | Where it ranks | Words (main) | Tables / tools | FAQ / schema | Dates | What is wrong or missing |
|---|---|---|---|---|---|---|
| nadlancenter.co.il/article/2044 "תשריט בית משותף - המדריך השלם לשנת 2026" | cited in 3 AI overviews; its sister 5049 ranks 3-4 and is cited in a 4th | about 1,200 (JS-rendered; read in browser) | none | no FAQ; NewsArticle | shows 10.05.26; schema dateModified 11.3.2025 (re-dated) | says the drawing is made under the Planning and Building Law (wrong source), "3 copies", "valid 6 months" (official: one year); spends half the page on city master plans (TA/5000); no order link, no fee, no attachment rules |
| dabullaw.co.il "תשריט ותקנון בית משותף" (Netanya law firm) | in 4 of 7 SERPs (positions 5 to 7); cited in 2 AI overviews | about 3,500 | 4 tables + a 4-line checklist | 5 Q&A, FAQPage schema | published 1.12.2025, modified 19.10.2026 | the strongest page. No ordering steps, no fee, no link to the official service; local "Netanya" sections; majorities table misses the 3/4 extension and 60% safe-room rules; suggests comparing drawing area with arnona area (no official basis) |
| ygoldlaw.co.il ".../shared-house/script/" | 2 for הזמנת תיק בית משותף; AI cited | 514 | none | none | 2018, modified 12.3.2023 | thin, old; no order path, no fee |
| batim.org.il "תיק בית משותף" | 8 for מסמכי בית משותף; AI cited | about 1,300 | none | 6 Q&A headings, no FAQ schema | modified 23.4.2025 | quotes 33 NIS (old fee); generic |
| kolzchut "תקנון בית משותף (מושג)" | 1 to 4 on three SERPs; AI cited | about 600 | lists | none | 13.8.2025 | accurate but bylaws only; nothing on drawing, order or ordering |
| home.tabu.co.il "תשריט בניין" (paid reseller) | 3-4; cited in 5 AI overviews | about 1,200 incl. menus | order form (block, parcel, "+ bylaws"), "order by address" | none | none | the 183/130 NIS banner is a five-extract bundle, not the drawing; the drawing price appears only inside the order flow. The page itself says the official site charges only the regulated fee |
| efi-aharon.co.il | 1 to 4 on three SERPs | 283 | link list | none | 1.1.2025 | a list of links; ranks on exact-match title only |

Also seen: mor.law "רישום בית משותף" (modified 22.10.2026, FAQPage, short), jus-tice /condominium-registration-order/ (403 words, fees 163/98, s.6ב, modified 22.10.2026).

**Gaps none of them fill (our edge):**
1. The 2026 fee (39 NIS online; 257 NIS physical inspection) and the exact official steps: "תיק יוצר" vs "שטר יוצר" from 1975, up to three files per order, all files of one building, ZIP within 24 hours, no address search.
2. One tap from a buyer's question (parking, storage, roof, yard, balcony, building rights, expenses, area) to the right document, the place in it, what to look for and the red flag.
3. How attachments are actually marked in the drawing (letters + same colour, never black, shared attachments striped, covered vs open balcony, storage rule, more than two parking spaces needs committee approval, dashed deviations, drafter's remarks).
4. The "approved drawing or other drawing" record on the order (regs 55(ב), 56), which no competitor mentions.
5. A correct majorities table (1/2 floor area, 2/3, all owners, 3/4 + 2/3, 60%, 15-day objection).
6. The unregistered-building path: chapter 6.1, Sale law s.6ב deadlines (one year, six months), housing company and RMI route.
7. Correct drawing validity (one year).

---

## 4. Proposal

### 4.1 Where the page lives

**/real-estate-lawyer/condo-documents/** (new). Both new words are unowned; the head "real-estate-lawyer" is an existing family. Not on /tabu-extract-check/ (that page owns נסח טאבו, 49,500 searches; different document).

### 4.2 Strings (checked, all OK)

- H1: מסמכי בית משותף: איך מזמינים צו, תקנון ותשריט, ומה בודקים בהם לפני קנייה
- SEO title (60): תשריט בית משותף ותיק הבית המשותף: הזמנה, עלות וקריאת המסמכים (fallback 56: תשריט בית משותף ותיק הבית המשותף: איך מזמינים ומה בודקים)
- Breadcrumb: מסמכי בית משותף
- Meta description idea: קונים דירה בבית משותף? כך מזמינים את הצו, התקנון והתשריט באתר הממשלתי ב-39 ₪, ובודקים בדקה איזה מסמך מראה של מי החניה, המחסן, הגג והחצר.

### 4.3 Answer paragraph (directly under the H1; facts only)

> תיק הבית המשותף נשמר בלשכת רישום המקרקעין וכולל שלושה מסמכים: צו הרישום, שמפרט כל דירה כתת־חלקה; התקנון, שקובע את היחסים בין בעלי הדירות; והתשריט, שמסמן כל דירה וההצמדות שלה, כמו חניה, מחסן, גג או חצר, באות ובצבע של הדירה. מזמינים את התיק באתר הרשות לרישום והסדר זכויות מקרקעין לפי גוש וחלקה או לפי מספר התיק, משלמים 39 ₪ (תעריף 2026), ומקבלים קישור להורדה בדואר האלקטרוני תוך 24 שעות. אם לא נרשם תקנון, חל התקנון המצוי שבחוק המקרקעין. חניה או מחסן נפרד שלא רשומים כהצמדה לדירה הם חלק מהרכוש המשותף, גם אם המוכר משתמש בהם שנים.

Sources (kept here, not on the page): service page (14.12.2025) for contents, search methods and 24 hours; fileextractor live text and fee notice 7(ד1) for 39 NIS; Land Law ss.52, 55(ג), 64; drawing instructions for letters and colours.

### 4.4 The tool: "איזה מסמך עונה על השאלה שלי"

One tap on a chip; the answer card opens under it. No input needed. Optional second step: the order path.

Chips and what each card says (data for the builder; every line has its source):

| Chip | Document and where | What to look for | Red flags | Source |
|---|---|---|---|---|
| חניה | Drawing: sub-parcel table "תיאור ההצמדה" + the lettered spot on the floor plan; the order and the land extract list the attachment under the flat's sub-parcel | the spot carries the flat's letter and colour; area in the table | spot used for years but not in the table (then it is common property); more than 2 spots on one flat without committee approval; letter or colour does not match | Land Law 52, 55(ג), 62(א); drawing instructions slides 25-26 |
| מחסן | Drawing table and floor plan | separate storage = attachment with a letter; storage with access only from inside the flat = part of the flat | storage you were shown is not in the drawing; description "flat + storage" | drawing instructions slide 25 |
| גג | Roof plan in the drawing ("תרשים גג וגג עליון") + attachments table + agreed bylaws | is the roof attached to a flat? does the bylaws text give building rights or passage to solar heaters? | roof is common property unless attached; building on the roof needs bylaws or s.71ב majorities; heaters without access | Land Law 52, 55(ג), 71ב; drawing instructions slides 59-60 |
| חצר / גינה | Drawing: land attachment ("הצמדת קרקע") on the ground-floor plan + table | the yard area with the flat's letter and colour | fenced garden not attached; yard over a public expropriation strip (marked red) | drawing instructions slides 37-44 |
| מרפסת | Drawing: covered balcony inside the flat's area; open or sun balcony as an attachment | which balcony is yours and its area | closing a balcony changes the outer look: general assembly consent (model bylaws s.2) and a building permit | drawing instructions slides 24, 41; model bylaws s.2(א) |
| זכויות בנייה והרחבה | Agreed bylaws (if registered) + Land Law 71ב | does the bylaws text attach building rights to a flat? | no agreed bylaws = model bylaws; extension needs 3/4 of flats with 2/3 of common property, safe room 60% | Land Law 62(א), 64, 71ב |
| חלק ברכוש המשותף והוצאות ועד | The order (share per sub-parcel) + bylaws | share by floor area unless bylaws set otherwise; same for upkeep | bylaws with equal split or exemptions you did not expect | Land Law 57, 58 |
| שטח הדירה | Drawing table "שטח הרצפה במ"ר" | measured by the 2008 Sale specification rules for contracts from 24.5.2008 | dashed areas are deviations and are not counted | drawing instructions slides 11, 24, 31 |
| האם התשריט מאושר | The order: registered on a planning-approved drawing or "another drawing" | the word on the order | "other drawing" can hide deviations from the permit; ask for the permit file | regs 54(ב)(1), 55(ב), 56 |
| הבניין לא רשום | Land extract shows the parcel without sub-parcels (shares in the whole parcel) | who holds the rights: owners in shares, housing company, or RMI | for a new project: one year to register the condo and six months for your rights after it (s.6ב); building runs by the model bylaws meanwhile (77ג) | Sale law 6ב; Land Law 77ב-77ג; RMI service page |

Order path panel (same card, under the chip answer):
1. "מצאו גוש וחלקה" → Survey of Israel finder link.
2. "הזמינו את התיק" → https://fileextractor.justice.gov.il/tabu (or the gov.il service page). 39 NIS, credit card, link by email within 24 hours, ZIP of signed PDFs. Order every file of the building (registration + amendments).
3. "לא מצאתם?" → search by file number from the land extract ("תיק יוצר", from 1975 "שטר יוצר"), or call *8653 ext. 7.
- Footer line: "התעריף נכון ל-2026 ומתעדכן ב-1 בינואר. ההזמנה מתבצעת באתר הממשלתי בלבד; אנחנו לא מזמינים בשמכם." (No resale, no affiliate link, no form on our side.)

Data shape: a small static JSON (about 10 chips × 5 fields, under 10 KB) with `source` and `checked` date per row; the fee lives in one constant `{fee: 39, year: 2026, physical: 257, source: "fees-2026"}` updated each January. No user data collected.

Design note for Claude Design (design-first law): take the look of the official condo drawing itself. Drafting white with a fine 1:100 grid, registry ink near-black navy for text, each chip's answer card outlined in one of the drawing's flat colours (blue, red, yellow, green, never black, as the official rule says), dashed red outline for every red flag (the drawing's own sign for deviations), sub-parcel numbers and fees in a monospaced tabular face. Hebrew face chosen in Claude Design (for example a Plex-family Hebrew with Plex Mono for numbers), not the site default. Not cream, not terracotta, not gold.

### 4.5 Page order (rendered, phones first)

1. H1 → answer paragraph → the tool (chips) → order path panel (the main call to action).
2. "מה יש בכל מסמך": table of the order, the bylaws and the drawing: what each shows, where to look, the buyer's question it answers.
3. "איך קוראים תשריט בית משותף": header, sub-parcel table, letters and colours, balconies, storage, parking (max two), roof, yard, dashed deviations, drafter's remarks, one-year validity. One annotated sample drawing made by us (not copied).
4. "תקנון מצוי או מוסכם": what changes, how to see which one applies (bylaws in the file or not; files up to 1969 have an agreement).
5. "מי צריך להסכים": the majorities table (1.5).
6. "כשהתשריט לא תואם את המצב בשטח": amendment of the order in short; link to jus-tice /amending-condominium-order/.
7. "דירה בבניין שלא נרשם / דירה חדשה מקבלן": s.6ב deadlines, chapter 6.1, housing company / RMI.
8. "כמה זה עולה": fee table 2026 (39 online, 257 physical, extract 18 electronic, registration 163 + 98, amendment 163).
9. "לשכות רישום המקרקעין": list with a link to the official branch finder.
10. FAQ (4.6). 11. Links onward.

Language: Israeli real-estate buyer voice (language-DNA law); long text through the owner's ChatGPT flow (content-split law); this brief is the fact base.

### 4.6 FAQ (from PAA, related searches and AI-overview follow-ups; answers only from section 1)

1. כמה עולה להזמין תשריט בית משותף, ואפשר לקבל אותו בחינם? (related "חינם", "מחיר") → 39 NIS online for the order (2026); 257 NIS to inspect the physical file at an office; no free official copy.
2. איך מזמינים תיק בית משותף באינטרנט? (related "מקוון", "משרד המשפטים") → the three steps.
3. מה מקבלים בתיק הבית המשותף, ובאיזה פורמט? → order, bylaws, drawing; amendment files; ZIP of signed PDFs within 24 hours.
4. מהו תקנון בית משותף מצוי? (PAA) → the schedule to the Land Law; applies when no bylaws were registered or where they are silent (s.64).
5. האם גג הוא רכוש משותף? (PAA) → yes by the law's definition, unless attached to a flat (s.52, 55(ג)); how to see it in the roof plan.
6. מה קובע סעיף 59 לחוק המקרקעין? (PAA) → several structures or wings can be run separately with their own committee, by bylaws or by the Supervisor.
7. איך יודעים איזו חניה או איזה מחסן שייכים לדירה? (AI follow-up) → letter and colour in the drawing table and floor plan; the attachment in the land extract.
8. מה עושים כשהתשריט לא תואם את המצב בשטח? (AI follow-up) → amendment under s.145 with consents and a committee-approved drawing; objections 15 days.
9. אפשר לשנות תקנון בית משותף? (related "שינוי תקנון") → 2/3 of common property for agreed bylaws; attachments need all owners, except 71ב extensions (3/4 + 2/3) and safe rooms (60%).
10. מה עושים כשהבניין לא רשום כבית משותף? (PAA "הסכם שיתוף", related "רשות מקרקעי ישראל") → chapter 6.1 and model bylaws; for a new project s.6ב deadlines; housing company or RMI route.

Hold: "האם חובה לרשום הסכם שיתוף בטאבו?" (PAA) until the regulations on co-ownership agreements (regs ch.3 part 7) are read.

### 4.7 Internal links (every URL returned 200 at 22:55)

From the new page:
- /tabu-extract-check/ (the extract shows the sub-parcel and attachments) · /glossary/land-registry-extract/ · /real-estate-lawyer/ · /apartment-buying-checklist/ · /guides/new-project-parking/ (already explains parking in the drawing for new projects) · /guides/new-apartment-balcony/ · /property-value/building-rights-check/ · /real-estate-lawyer/sale-of-apartments-law/ (s.6ב) · /real-estate-lawyer/apartment-sale-contract/ · /real-estate-lawyer/form-4-occupancy-permit/ · /buying-apartment/buying-apartment-step-by-step/ · /buying-apartment/new-vs-second-hand/ · /urban-renewal/tama-38-rights-obligations/ (roof rights) · /real-estate-lawyer/partition-real-estate/ (undivided shares) · /glossary/perpetual-lease/ (RMI leasehold) · /home-inspection/ · /real-estate-appraiser/
- jus-tice: two contextual links (2.3).

To the new page (one release, a handful of pages, not a mass change): /tabu-extract-check/ (it already mentions "בית משותף" 8 times and attachments 12 times), /apartment-buying-checklist/, /real-estate-lawyer/, /guides/new-project-parking/, /guides/new-apartment-balcony/, /property-value/building-rights-check/, /real-estate-lawyer/sale-of-apartments-law/, /glossary/land-registry-extract/.

---

## 5. Files

- `brief.md`: this file.
- `keywords.csv`: 86 keywords, average and 12 monthly volumes (Oct 2025 to Sep 2026), competition, CPC.
- `serps.json`: seven SERPs with top 10, AI overview (present, cited URLs, claims), PAA, related searches.
- Private (`C:/Users/777/nad-lan/_private-research/2026-10-22-condo-documents/raw/`): `gov-pages/official-pages-read.txt` (what each official page says, with dates), law and regulation texts, `TabuUserGuids.pdf`, `amendment-guide.pdf`, `drawing-instructions.pdf`, `fees-2026-notice.pdf`; `competitors/*.html`, `fetch-log.json`, `structure.json`; `gsc-*.csv`; `dfs-volume*.json`.

## 6. Cost

DataForSEO: two Google Ads search-volume calls at $0.09 each (86 keywords), one rejected call (language code "he", no charge), seven live advanced SERP calls with AI overview and one PAA level ($0.002 to $0.004 each, $0.016 in all). Total **about $0.20**.
