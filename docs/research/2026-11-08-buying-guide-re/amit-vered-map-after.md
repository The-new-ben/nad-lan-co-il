# Amit Vered buying guide: re-grade after the new page (v3) against the 8.11.2026 map

- Date: 9.11.2026 (Linear HAD-686). Read-only re-grade; this is the only file written.
- Source guide: https://amitvered.co.il/קניית-דירה/ . The 365 information units and their paraphrases are copied from `amit-vered-map.md` (8.11.2026).
- Page graded: the new version `page-9-v3.txt` (3,262 lines, 18 stage H2s, builder and special-cases chapters, FAQ, glossary). The buyer-side chapters (stages 1 to 16, the tax, contract, payment, warning-note, handover and registration chapters) were read in full; the builder chapter, special cases, FAQ and glossary were searched for specific facts.
- Tool text also read: the ten existing tools from the old live extraction `42115af023.json` (tool sections, unchanged) and the five new tools from `buying.json` (keys `pay` = bpay, `sign` = bsign, `keys` = bkeys, `reg` = breg, `memo` = bmemo; also `visit`, `steps`, `stages`).
- Rules: YES only when the new page states the same fact (wording may differ). PARTIAL when the topic is touched but the specific fact, number or nuance is missing. NO when absent. YES (updated) when our page states the current official rule on the same point and it differs from their figure.
- Honesty notes: a unit counts YES when the fact is on the page even if one of their side numbers is not (for example #68, where our inspection range is 1,500 to 2,500 NIS, sourced, and theirs 1,500 to 2,000). Figures that Amit Vered gives with no official source and our page does not repeat stay PARTIAL. Web not used; no git.

## Full table

| # | Their section | Unit | Before | After | Where on the new page | Still missing |
|---|---|---|---|---|---|---|
| 1 | Pre-contract overview | Do every check before signing so you do not buy blind | PARTIAL | YES | ממה מתחילים כשרוצים לקנות דירה? (H3) | - |
| 2 | Pre-contract overview | Pre-checks cover three areas: legal, engineering/planning, economic | PARTIAL | YES | ממה מתחילים כשרוצים לקנות דירה? (H3) | - |
| 3 | Pre-contract overview | Early checks let you write protective commercial and legal terms into the contract | PARTIAL | YES | ממה מתחילים כשרוצים לקנות דירה? (H3) | - |
| 4 | Tip: price | Use the Tax Authority public deal database (by block/parcel or address) to anchor price in negotiation | YES | YES | איך בודקים מחיר דירה לפי כתובת? (H3); בחירת עיר ושכונה (H2) | - |
| 5 | Physical check | Visit the flat at least two or three times before deciding | YES | YES | מהי הדרך הטובה ביותר לבדוק דירה? (H3); כלי דף הביקור | - |
| 6 | Physical check | Visit at daylight, evening and weekend, since the flat looks different at night | YES | YES | בחירת עיר ושכונה (H2) | - |
| 7 | Physical check | Think as a future seller: is it attractive, quick to sell, a good investment | YES | YES | קונים למגורים או להשקעה (H3); לכמה שנים קדימה (H3) | - |
| 8 | Physical check | Buyers missed a noisy kindergarten, synagogue, community centre or rooftop cell antenna because they fell in love | PARTIAL | YES | איך בודקים רעש ומפגעים ליד הבית? (H3) | - |
| 9 | Physical check | Quiet daytime areas turn noisy at night (playground benches, teenagers); avoid being next to one | PARTIAL | YES | איך בודקים רעש ומפגעים ליד הבית? (H3) | - |
| 10 | Physical check | A nearby shopping centre helps but brings noise, smell, access and parking problems | PARTIAL | YES | איך בודקים רעש ומפגעים ליד הבית? (H3) | - |
| 11 | Physical check | Ask the sellers detailed questions about the flat | YES | YES | כלי דף הביקור: שאלות למוכר | - |
| 12 | Physical check | Test windows, shutters, AC, cabinets, taps, electric points | YES | YES | מהי הדרך הטובה ביותר לבדוק דירה? (H3) | - |
| 13 | Physical check | Look for wall cracks and damp signs showing leaks or rain entry | PARTIAL | YES | איך מזהים רטיבות, סדקים וצנרת ישנה? (H3) | - |
| 14 | Physical check | Old flats have more pipe and damp problems; ask when pipes were last replaced | PARTIAL | YES | איך מזהים רטיבות, סדקים וצנרת ישנה? (H3) | - |
| 15 | Physical check | Cosmetic paint can hide mould and damp, esp. in summer; only thermal imaging by an engineer finds it | PARTIAL | YES | איך מזהים רטיבות, סדקים וצנרת ישנה? (H3) | - |
| 16 | Physical check | Note orientation: street or rear, light and sun, warm or cold sides | YES | YES | כלי דף הביקור: אור יום וכיווני אוויר | - |
| 17 | Physical check | For newer flats research the builder: reputation, quality, defect suits; known builders can carry a 5-10% premium | PARTIAL | PARTIAL | האם יש אחריות על דירה יד שנייה? (H3); פנקס הקבלנים | פרמיית מחיר של 5% עד 10% לקבלן מוכר (חיפוש הקבלן בפנקס הקבלנים ושאלת הוועד אם תבע על ליקויים כן מופיעים) |
| 18 | Physical check | Inspect common parts: entrance door, intercom, mailboxes, lobby, stairwell, gate, fence, bin room | PARTIAL | YES | מה בודקים בבניין ובשטחים המשותפים? (H3) | - |
| 19 | Physical check | Ask other residents about quality of life, neighbours, acoustics, sanitation, crime, upkeep | PARTIAL | YES | איך בודקים רעש ומפגעים ליד הבית? (H3) | - |
| 20 | Physical check | Compare rented flats to owner-occupied flats in the building; it affects upkeep and cooperation | NO | YES | מה בודקים בבניין ובשטחים המשותפים? (H3) | - |
| 21 | Tip: neighbours | Stand outside the building at different hours to learn the neighbour mix and noise level | PARTIAL | YES | איך בודקים רעש ומפגעים ליד הבית? (H3) | - |
| 22 | Physical check | Check the building committee fee | YES | YES | בחירת עיר ושכונה (H2); כלי דף הביקור | - |
| 23 | Physical check | Check who may use common property (guest parking, storage, shared facilities) | PARTIAL | YES | מה בודקים בבניין ובשטחים המשותפים? (H3) | - |
| 24 | Physical check | Area differs between tabu, arnona bill and reality; cross-check them | NO | YES | השטח בנסח, בארנונה ובפועל לא זהה (H3) | - |
| 25 | Physical check | Location is the top real-estate factor: roads, industry, services, schools, clinics, shops | YES | YES | בחירת עיר ושכונה (H2) | - |
| 26 | Physical check | Plan with a horizon of at most about ten years | PARTIAL | PARTIAL | לכמה שנים קדימה מתכננים את הדירה? (H3) | אופק תכנון של עד כעשר שנים; הדף אומר 'לשנים שבהן תגורו בה' בלי מספר |
| 27 | Tip: heart | Trust your gut feeling about the flat, but do not decide on impulse | PARTIAL | YES | קונים למגורים או להשקעה (H3) | - |
| 28 | Land registry check | The tabu extract is the flat's ID | YES | YES | בדיקת זכויות ומסמכים (H2) | - |
| 29 | Land registry check | Ask sellers for the extract or the block and parcel numbers | YES | YES | מה עושים בשלב הזה (שלב 5); בדיקת טאבו לפי כתובת (H3) | - |
| 30 | Land registry check | Produce a current extract online in minutes for a fee of 18 NIS (2026) | YES | YES | איך מזמינים נסח טאבו, וכמה זה עולה? (H3) | - |
| 31 | Land registry check | Find block and parcel from the arnona bill, seller's contract or free lookup tools | PARTIAL | YES | בדיקת טאבו לפי כתובת: איך מוצאים גוש, חלקה ותת חלקה? (H3) | - |
| 32 | Land registry check | Extract shows whether the flat is registered in tabu at all | YES | YES | קניית דירה שלא רשומה בטאבו (H3); בדיקת מצב רישום (H3) | - |
| 33 | Land registry check | Extract shows separate unit/sub-parcel versus undivided share (mushaa) | NO | YES | דירה רשומה כתת חלקה או כחלק במושע? (H3) | - |
| 34 | Land registry check | Extract shows ownership versus leasehold | YES | YES | איך קוראים נסח טאבו, חלק אחרי חלק? (H3) | - |
| 35 | Land registry check | Extract shows whether the seller owns the whole flat | YES | YES | איך קוראים נסח טאבו, חלק אחרי חלק? (H3) | - |
| 36 | Land registry check | Extract shows how and when seller got title (purchase, gift, inheritance) | NO | YES | איך קוראים נסח טאבו, חלק אחרי חלק? (H3) | - |
| 37 | Land registry check | Extract shows a mortgage charge | YES | YES | משכנתה, עיקול והערת אזהרה בנסח (H3) | - |
| 38 | Land registry check | Extract shows third-party notes, liens, court or administrative orders, restrictions | YES | YES | משכנתה, עיקול והערת אזהרה בנסח (H3) | - |
| 39 | Warning: registry | Any lien, note or order must be professionally reviewed, provably removable, and covered by contract protections | YES | YES | משכנתה, עיקול והערת אזהרה בנסח (H3) | - |
| 40 | Land registry check | Have your lawyer read the extract early | YES | YES | בדיקת זכויות ומסמכים (H2): מה עושים בשלב הזה | - |
| 41 | Land registry check | If not in tabu, get a rights certificate from the relevant register (ILA, housing company, settlement division) | YES | YES | איזה אישור זכויות מזמינים? (H3) | - |
| 42 | Tip: seller marital status | Check if the seller is married or has a common-law partner who could claim rights | NO | YES | המוכר נשוי או ידוע בציבור (H3) | - |
| 43 | Tip: seller marital status | Mortgage bank demands the seller's spouse waiver; get spouse consent and a contract clause | NO | YES | המוכר נשוי או ידוע בציבור (H3) | - |
| 44 | Occupants | If rented, ask tenants about defects, pros and cons | NO | YES | קונים דירה עם שוכר (H3) | - |
| 45 | Occupants | Obtain the full lease and check end date and extension option | PARTIAL | YES | קונים דירה עם שוכר (H3) | - |
| 46 | Occupants | Make sure you can get the flat on the agreed evacuation date despite seller-tenant dispute | PARTIAL | YES | קונים דירה עם שוכר (H3) | - |
| 47 | Occupants | Non-owners may live there without a lease as licensees (friend, relative) | NO | YES | מי עוד גר בדירה? (H3) | - |
| 48 | Occupants | Tell your lawyer about tenants or other occupants and plan risk reduction | NO | YES | מי עוד גר בדירה? (H3) | - |
| 49 | Seller identity | Confirm the seller is the real owner; property fraud has grown in recent years | PARTIAL | YES | איך מוודאים שהמוכר הוא הבעלים? (H3) | - |
| 50 | Seller identity | Fraud pattern: impersonators with forged ID, power of attorney or probate papers, bargain price, elderly victims | NO | YES | איך מזהים הונאה במכירת דירה? (H3) | - |
| 51 | Seller identity | Match a clear current photo ID to the person presenting as owner | NO | YES | איך מוודאים שהמוכר הוא הבעלים? (H3); טבלת ההונאה | - |
| 52 | Seller identity | Ask for a second ID (passport), original purchase papers, neighbour confirmation, repeat visits; any doubt means no deal | NO | YES | איך מוודאים שהמוכר הוא הבעלים? (H3); טבלת ההונאה | - |
| 53 | Seller identity | If only one spouse is registered, the other must know, agree and cooperate; lawyer drafts spouse consent annex | NO | YES | המוכר נשוי או ידוע בציבור (H3) | - |
| 54 | Joint-house file | Review the joint-house (bayit meshutaf) file before buying | PARTIAL | YES | מה זה תיק בית משותף ואיך מזמינים אותו? (H3) | - |
| 55 | Joint-house file | Order it online from the gov services site; files arrive by email in about 24 hours | NO | YES | מה זה תיק בית משותף ואיך מזמינים אותו? (H3) | - |
| 56 | Joint-house file | Fee for the file is 39 NIS (2026) | NO | YES | מה זה תיק בית משותף ואיך מזמינים אותו? (H3) | - |
| 57 | Joint-house file | File types: registration (order, regulations, plan), amendment, cancellation | NO | YES | מה זה תיק בית משותף ואיך מזמינים אותו? (H3) | - |
| 58 | Joint-house file | Read the flat's plan and the plans of attachments (parking, storage, common areas) | NO | YES | איך קוראים תשריט בית משותף? (H3) | - |
| 59 | Joint-house file | The plan binds property-wise: registered area, boundaries, internal division, special additions | NO | YES | איך קוראים תשריט בית משותף? (H3) | - |
| 60 | Joint-house file | Use the plan to confirm the parking or storage shown to you is really attached | PARTIAL | YES | איך קוראים תשריט בית משותף? (H3); חניה, מחסן וגג (H3) | - |
| 61 | Joint-house file | Plan places the flat in the building and floor and ties it to block/parcel | NO | YES | איך קוראים תשריט בית משותף? (H3) | - |
| 62 | Joint-house file | Plan exposes unauthorised changes or encroachments | NO | YES | איך קוראים תשריט בית משותף? (H3) | - |
| 63 | Joint-house file | Banks require the plan for their appraiser; confirm it exists to avoid mortgage delays | NO | YES | איך קוראים תשריט בית משותף? (H3) | - |
| 64 | Joint-house file | Some lawyers skip this step; confirm yours orders and reviews it | NO | YES | מה השמאי בודק בחריגות? (H3); איך בוחרים עורך דין (H3) | - |
| 65 | Joint-house file | For unregistered newer flats, use the plans attached to the original developer contract | PARTIAL | YES | בדיקת מצב רישום (H3); מה זה תיק בית משותף (H3) | - |
| 66 | Engineer inspection | Hire an inspection as you would a car test before buying | YES | YES | מתי מזמינים מהנדס, ומה הבדיקה כוללת? (H3) | - |
| 67 | Engineer inspection | Inspection gives an objective full picture of the flat, building and surroundings | PARTIAL | YES | מתי מזמינים מהנדס, ומה הבדיקה כוללת? (H3) | - |
| 68 | Engineer inspection | Old flats: written report on structure, damp, plumbing, electrics, roofs, walls; cost 1,500-2,000 NIS | YES | YES | עלות כוללת: טבלת העלויות (בדק בית) | - |
| 69 | Engineer inspection | Report can also flag build defects, safety hazards, neighbours and area nuisances | PARTIAL | YES | מתי מזמינים מהנדס, ומה הבדיקה כוללת? (H3) | - |
| 70 | Planning check | Goal: confirm it is legally a dwelling with no violations or other planning problem | YES | YES | קניית דירה עם חריגות בנייה (H3); בטאבו כתוב דירה (H3) | - |
| 71 | Planning check | Local authority engineering department file is open to the public free | NO | PARTIAL | תיק בניין בוועדה המקומית (H3) | שתיק הבניין פתוח לעיון הציבור בחינם; הדף אומר איפה התיק ומה בו, לא שהעיון חינם |
| 72 | Planning check | Planning administration site of the local authority carries planning data | NO | YES | תוכניות בתוקף וזכויות בנייה שלא נוצלו (H3) | - |
| 73 | Planning check | First confirm a building permit exists and read it carefully | YES | YES | תיק בניין בוועדה המקומית: מה מחפשים בו? (H3) | - |
| 74 | Planning check | Define a permit: issued by local planning committee for building, demolition or change of use | NO | YES | תיק בניין בוועדה המקומית: מה מחפשים בו? (H3) | - |
| 75 | Planning check | Permit text lists what was approved and designated uses, with a signed plan (garmoshka) | PARTIAL | YES | תיק בניין בוועדה המקומית: מה מחפשים בו? (H3) | - |
| 76 | Planning check | Check physical match between the flat and the permit plan | YES | YES | מה עושים בשלב 7; מה השמאי בודק בחריגות (H3) | - |
| 77 | Planning check | Check that the approved use is residential (not storage, laundry, shelter, boiler room) | NO | YES | בטאבו כתוב דירה: האם מותר לגור בה? (H3) | - |
| 78 | Planning check | Tabu saying "apartment" does not prove planning approval for housing | NO | YES | בטאבו כתוב דירה: האם מותר לגור בה? (H3) | - |
| 79 | Planning check | Odd building-file entries (warnings, demolition order, inspection reports) or no permit: stop and consult lawyer | PARTIAL | YES | תיק בניין בוועדה המקומית (H3): התראות וצווים | - |
| 80 | Planning check | Permit and use check is the lawyer's duty, though many lawyers skip it | NO | YES | מה השמאי בודק בחריגות? (H3) | - |
| 81 | Planning check | Matching the flat to the permit needs an appraiser, engineer, architect or licensed surveyor on site | PARTIAL | YES | מה השמאי בודק בחריגות? (H3) | - |
| 82 | Planning check | A non-conforming flat hurts value and future resale | PARTIAL | YES | בטאבו כתוב דירה (H3); קניית דירה עם חריגות בנייה (H3) | - |
| 83 | Planning check | Mortgage banks may refuse loans on flats with building violations | YES | YES | בטאבו כתוב דירה (H3); קניית דירה עם חריגות בנייה (H3) | - |
| 84 | Planning check | Municipality may withhold the tabu certificate while violations exist | NO | YES | חריגת בנייה: מה החוק קובע ומה זה אומר לקונה? (H3) | - |
| 85 | Planning check | If the permit is lost, get a written municipal letter that it was not found and give it to the bank appraiser; confirm with the bank pre-signing | NO | YES | היתר הבנייה לא נמצא: מה עושים? (H3) | - |
| 86 | Planning check | Risk factors for use violations: very old building, ground/basement/pilotis, roof floor, commercial frontage | NO | YES | בטאבו כתוב דירה (H3) | - |
| 87 | Warning: planning | Violations are criminal offences under the Planning and Building Law 1965: fines, prison, demolition or injunction orders | NO | YES | חריגת בנייה: מה החוק קובע ומה זה אומר לקונה? (H3) | - |
| 88 | Warning: planning | Planning status affects purchase-tax relief and later capital-gains exemption, which apply to dwellings only | NO | YES | בטאבו כתוב דירה (H3); מי משלם מס שבח (H3) | - |
| 89 | Planning check | Read town plans for permitted uses and future building on neighbouring land | PARTIAL | YES | תוכניות בתוקף וזכויות בנייה שלא נוצלו (H3) | - |
| 90 | Planning check | Building file shows history; ask officials about demolition orders and dangerous-building notices | PARTIAL | YES | תיק בניין בוועדה המקומית (H3) | - |
| 91 | Planning check | Confirm the flat has a Form 4 (occupancy certificate) | YES | YES | תיק בניין בוועדה המקומית (H3) | - |
| 92 | Planning check | Check for unused building rights on the flat | NO | YES | תוכניות בתוקף וזכויות בנייה שלא נוצלו (H3) | - |
| 93 | Planning check | Check betterment-levy liability at the municipality; usually seller pays but add a contract mechanism | PARTIAL | YES | מתי משלמים היטל השבחה, ומה הקונה בודק? (H3) | - |
| 94 | Appraiser | A licensed appraiser values the flat to test economic sense | YES | YES | מה השמאי בודק מעבר למחיר? (H3) | - |
| 95 | Appraiser | Appraiser also reviews plans, building rights, applicable town plans, lawful uses, expropriations | PARTIAL | YES | מה השמאי בודק מעבר למחיר? (H3) | - |
| 96 | Appraiser | Violations affect value, use, mortgage, fines, demolition orders, extra arnona and levy | PARTIAL | YES | חריגת בנייה: מה החוק קובע (H3) | - |
| 97 | Appraiser | Examples of violations: basement, flat registered as storage or office, pergola, storage, closed balcony, living-room extension, extra room, parking, attic, bigger window, high fence, paving, pool | PARTIAL | YES | אילו חריגות בנייה נפוצות, ואיך מזהים אותן? (H3); בטאבו כתוב דירה (H3) | - |
| 98 | Appraiser | Risk factors for violations: old, ground or roof, garden flat, different openings, light construction, split layout | NO | YES | אילו חריגות בנייה נפוצות, ואיך מזהים אותן? (H3); בטאבו כתוב דירה (H3) | - |
| 99 | Appraiser | Significant violations may block bank loans, force restoration, or cause delay and disputes | YES | YES | קניית דירה עם חריגות בנייה (H3) | - |
| 100 | Appraiser | Lawyer explains consequences and refers you to the right experts | PARTIAL | YES | מה השמאי בודק בחריגות? (H3) | - |
| 101 | Budget and financing | Stay inside a budget set in advance; overshooting causes distress | YES | YES | לפני שמחפשים: מטרה, תקציב ומחיר נוח (H2) | - |
| 102 | Budget and financing | Define available budget and the extra costs of the process | YES | YES | לפני שמחפשים: מטרה, תקציב ומחיר נוח (H2) | - |
| 103 | Budget and financing | Map equity sources and how liquid they are (study fund, provident fund, savings, parental gifts) | YES | YES | כלי מקורות ההון העצמי (קניית דירה ללא הון עצמי); שאלות נפוצות | - |
| 104 | Budget and financing | Sync cash availability with instalments coming from selling the current flat | YES | YES | מה קורה כשהמימון תלוי במכירת הדירה הקיימת? (H3); כלי קנייה לפני מכירה | - |
| 105 | Budget and financing | If funding depends on a future sale, test the price is realistic or sell first | PARTIAL | YES | מה קורה כשהמימון תלוי במכירת הדירה הקיימת? (H3); כלי קנייה לפני מכירה | - |
| 106 | Budget and financing | Decide whether the purchase is own capital only or also a loan or mortgage | YES | YES | קודם המימון, אחר כך הדירה (H2) | - |
| 107 | Budget and financing | Ask how large a mortgage the bank will approve | YES | YES | קודם המימון, אחר כך הדירה (H2) | - |
| 108 | Budget and financing | Work out the monthly repayment | YES | YES | קודם המימון, אחר כך הדירה (H2) | - |
| 109 | Budget and financing | Test whether you can pay even if the rate rises | YES | YES | מה הבנק מחשב כהכנסה, ומה כהוצאה קבועה? (H3) | - |
| 110 | Budget and financing | Compute free income: net income minus living costs | YES | YES | מה הבנק מחשב כהכנסה, ומה כהוצאה קבועה? (H3) | - |
| 111 | Budget and financing | Ask whether income is stable (layoffs, business strength) | PARTIAL | YES | מה הבנק מחשב כהכנסה, ומה כהוצאה קבועה? (H3) | - |
| 112 | Budget and financing | Ask whether expenses may change (for example another child) | NO | YES | מה הבנק מחשב כהכנסה, ומה כהוצאה קבועה? (H3) | - |
| 113 | Ancillary costs | Learn ancillary liabilities precisely before the deal | YES | YES | עלות כוללת (H3); אילו הוצאות נלוות (H3) | - |
| 114 | Ancillary costs | Build a detailed spreadsheet of expected costs and add a safety margin of at least 5% | PARTIAL | PARTIAL | כמה עולה העסקה מעבר למחיר הדירה? (H3) | מרווח הביטחון של 5% לפחות; בדף מרווח ביטחון כשורה קבועה, בלי שיעור |
| 115 | Ancillary costs | Cost item: purchase tax | YES | YES | עלות כוללת: טבלת העלויות | - |
| 116 | Ancillary costs | Cost item: lawyer fee | YES | YES | עלות כוללת: טבלת העלויות | - |
| 117 | Ancillary costs | Cost item: land registry fees | YES | YES | עלות כוללת: טבלת העלויות | - |
| 118 | Ancillary costs | Cost item: broker commission, if any | YES | YES | עלות כוללת: טבלת העלויות | - |
| 119 | Ancillary costs | Cost item: appraiser | YES | YES | עלות כוללת: טבלת העלויות | - |
| 120 | Ancillary costs | Cost item: licensed surveyor | NO | YES | אילו הוצאות נלוות לרכישת דירה שוכחים? (H3): מודד מוסמך | - |
| 121 | Ancillary costs | Cost item: building inspection | YES | YES | עלות כוללת: טבלת העלויות | - |
| 122 | Ancillary costs | Cost item: mortgage set-up (file opening, registry fees, pledge registry, notary) | PARTIAL | YES | אילו הוצאות נלוות (H3): פתיחת תיק, אגרות לבנק, אימות ייפוי כוח | - |
| 123 | Ancillary costs | Cost item: packing, moving, crane | YES | YES | אילו הוצאות נלוות (H3); לפני שמחפשים (H2) | - |
| 124 | Ancillary costs | Cost item: dismantling and installing furniture and fixtures | NO | YES | אילו הוצאות נלוות (H3); לפני שמחפשים (H2) | - |
| 125 | Ancillary costs | Cost item: cleaning, painting, pest control, repairs, renovation | YES | YES | אילו הוצאות נלוות (H3); לפני שמחפשים (H2) | - |
| 126 | Ancillary costs | Cost item: lost workdays | NO | YES | אילו הוצאות נלוות (H3); לפני שמחפשים (H2) | - |
| 127 | Ancillary costs | Furniture, electronics and upgrades come on top | YES | YES | אילו הוצאות נלוות (H3); לפני שמחפשים (H2) | - |
| 128 | Ancillary costs | Renovation may cost more than planned; get a reliable contractor's estimate first | PARTIAL | YES | אילו הוצאות נלוות (H3): שיפוץ, הצעת מחיר כתובה | - |
| 129 | Ancillary costs | Keep some money aside for a rainy day | YES | YES | טעויות נפוצות בקניית דירה (H2) | - |
| 130 | Ancillary costs | Total ancillary costs can reach 15% or more of the price | NO | PARTIAL | כמה עולה העסקה מעבר למחיר הדירה? (H3) | הכלל 'הוצאות נלוות עד 15% ויותר'; הדף מציג במקומו חישוב מפורט (0.8% עד 1.5% בדירה יחידה, כ־9% בנוספת) וקובע שאחוז קבוע לא מתאים לכולם |
| 131 | Buyer mortgage | Get an in-principle approval before signing the contract | YES | YES | קודם המימון, אחר כך הדירה (H2) | - |
| 132 | Buyer mortgage | Mortgage is not instant, so prepare ahead | PARTIAL | YES | כמה זמן לוקח לקבל אישור עקרוני, ומה מביאים לבנק? (H3) | - |
| 133 | Buyer mortgage | In-principle approval means the bank agrees in principle, subject to documents | YES | YES | כמה זמן לוקח לקבל אישור עקרוני, ומה מביאים לבנק? (H3) | - |
| 134 | Buyer mortgage | Bank asks income, occupation, employee or self-employed, assets, savings, loans | PARTIAL | YES | כמה זמן לוקח לקבל אישור עקרוני, ומה מביאים לבנק? (H3) | - |
| 135 | Buyer mortgage | Approval is quick by bank phone centres or branches | NO | YES | כמה זמן לוקח לקבל אישור עקרוני, ומה מביאים לבנק? (H3) | - |
| 136 | Warning: mortgage | Used-flat contracts say failing to get a mortgage is no reason to cancel; breach means fixed damages | NO | YES | מה קורה אם לא מקבלים משכנתא אחרי החתימה? (H3) | - |
| 137 | Buyer mortgage | Approach several banks and negotiate terms | YES | YES | קודם המימון, אחר כך הדירה (H2) | - |
| 138 | Buyer mortgage | Mortgage track types: variable, fixed, graduated, shekel, dollar, bullet, equal principal, Spitzer | PARTIAL | YES | אילו מסלולים יש במשכנתא? (H3) | - |
| 139 | Buyer mortgage | Bank of Israel caps financing as share of value, set by appraiser | YES | YES | קודם המימון (H2); האם ניתן לקחת משכנתא עבור דירה שנייה? (H3) | - |
| 140 | Buyer mortgage | First-time buyer: maximum financing 75% | YES | YES | קודם המימון (H2); האם ניתן לקחת משכנתא עבור דירה שנייה? (H3) | - |
| 141 | Buyer mortgage | Single-flat upgrader: maximum financing 70% | YES | YES | קודם המימון (H2); האם ניתן לקחת משכנתא עבור דירה שנייה? (H3) | - |
| 142 | Buyer mortgage | Additional flat (investor): maximum financing 50% | YES | YES | קודם המימון (H2); האם ניתן לקחת משכנתא עבור דירה שנייה? (H3) | - |
| 143 | Tip: gifting | Gifting an owned flat to a child can turn an investor into a single-flat buyer: up to 20% more financing and lower purchase tax | NO | PARTIAL | האם ניתן לקחת משכנתא עבור דירה שנייה? (H3) | הנתון 'עד 20% מימון נוסף'; הדף מתאר את המהלך (מימון גבוה ומס נמוך) ואת מחירו בלי מספר |
| 144 | Seller mortgage | Seller mortgage check applies only if a mortgage is registered on the flat | YES | YES | מה בודקים במשכנתא של המוכר לפני החתימה? (H3); מה עושים כשעל הדירה רשומה משכנתא של המוכרים (H3) | - |
| 145 | Seller mortgage | Ask for the bank's official printout of the full payoff balance | NO | YES | מה בודקים במשכנתא של המוכר לפני החתימה? (H3); מה עושים כשעל הדירה רשומה משכנתא של המוכרים (H3) | - |
| 146 | Seller mortgage | Learn how and when the seller will clear it: payoff or dragging it to another property | PARTIAL | YES | מה בודקים במשכנתא של המוכר לפני החתימה? (H3); מה עושים כשעל הדירה רשומה משכנתא של המוכרים (H3) | - |
| 147 | Seller mortgage | Prefer early clearing; if from your payments, sync amounts and dates | PARTIAL | YES | מה בודקים במשכנתא של המוכר לפני החתימה? (H3); מה עושים כשעל הדירה רשומה משכנתא של המוכרים (H3) | - |
| 148 | Taxes overview | Both sides pay tax: buyer purchase tax; seller betterment tax and levy | YES | YES | המסים בעסקה מהצד של הקונה (H2); מי משלם מס שבח (H3) | - |
| 149 | Taxes overview | Learn taxes early to plan the budget | YES | YES | המסים בעסקה מהצד של הקונה (H2); מי משלם מס שבח (H3) | - |
| 150 | Taxes overview | Set a tax deposit in the contract for seller taxes | NO | YES | המסים בעסקה מהצד של הקונה (H2); מי משלם מס שבח (H3) | - |
| 151 | Taxes overview | Final tax approvals of both sides are needed to finish registration | PARTIAL | YES | המסים בעסקה מהצד של הקונה (H2); מי משלם מס שבח (H3) | - |
| 152 | Purchase tax | Buyer owes purchase tax under section 9(a) of the Land Taxation Law 1963 | PARTIAL | YES | כמה מס רכישה משלמים על דירה ראשונה? (H3) | - |
| 153 | Purchase tax | Purchase tax applies unless an exemption or relief applies | YES | YES | כמה מס רכישה משלמים על דירה ראשונה? (H3) | - |
| 154 | Purchase tax | Tax follows brackets by price and whether the buyer owns another flat | YES | YES | כמה מס רכישה משלמים על דירה ראשונה? (H3) | - |
| 155 | Purchase tax | Exemptions exist; check them before signing | YES | YES | מי זכאי להנחה במס רכישה? (H3) | - |
| 156 | Purchase tax | Plan tax with a lawyer who also knows land taxation | PARTIAL | YES | איך מקטינים את המס בדרך חוקית? (H3) | - |
| 157 | Purchase tax | Family-unit rule: spouses and minor children count as one buyer, so one spouse's flat can cancel the other's relief | NO | YES | האם בן הזוג נחשב לעניין דירה יחידה? (H3) | - |
| 158 | Purchase tax | Single-flat brackets: 0% to 1,978,745; 3.5% to 2,347,040; 5% to 6,055,070; 8% to 20,183,565; 10% above | YES | YES | כמה מס רכישה משלמים (H3); עלות כוללת: טבלת העלויות | - |
| 159 | Purchase tax | Additional flat: 8% to 6,055,070; 10% above | YES | YES | כמה מס רכישה משלמים (H3); עלות כוללת: טבלת העלויות | - |
| 160 | Purchase tax | Bracket amounts are updated periodically (they list validity to 15.1.2026) | YES | YES (updated) | כמה מס רכישה משלמים (H3); עלות כוללת: טבלת העלויות | (updated) הדף מציג את המצב הרשמי הנוכחי: המדרגות קפואות עד 15.1.2028 (הם מציינים תוקף שפג ב־15.1.2026) |
| 161 | Purchase tax | Reliefs for people with disabilities (disabled, blind, work-injured, IDF and terror-injured, child 100% disabled, Holocaust survivors) | PARTIAL | YES | מי זכאי להנחה במס רכישה? (H3) | - |
| 162 | Purchase tax | Reliefs for new immigrants | YES | YES | מי זכאי להנחה במס רכישה? (H3) | - |
| 163 | Purchase tax | Reliefs for bereaved families and families of terror victims | NO | YES | מי זכאי להנחה במס רכישה? (H3) | - |
| 164 | Tip: partial share | Share in another flat up to one third (one half if inherited) is not an additional flat for purchase tax | NO | YES | האם בן הזוג נחשב לעניין דירה יחידה? (H3) | - |
| 165 | Seller taxes | Seller pays betterment tax (mas shevach) on gain versus purchase price | YES | YES | מי משלם מס שבח, ולמה זה מעניין את הקונה? (H3) | - |
| 166 | Seller taxes | Betterment tax can be large, so buyers should know the expected amount pre-signing | PARTIAL | YES | מי משלם מס שבח, ולמה זה מעניין את הקונה? (H3) | - |
| 167 | Seller taxes | Lawyers run a simulation at maximum exposure to be sure the seller can pay and get the clearance | NO | YES | מי משלם מס שבח, ולמה זה מעניין את הקונה? (H3) | - |
| 168 | Seller taxes | Seller routes: full exemption (qualifying home), partial linear, or full tax (or zero if no gain) | PARTIAL | YES | מי משלם מס שבח, ולמה זה מעניין את הקונה? (H3) | - |
| 169 | Seller taxes | Check exemption entitlement against each statutory condition | PARTIAL | YES | מי משלם מס שבח, ולמה זה מעניין את הקונה? (H3) | - |
| 170 | Betterment levy | Levied on the seller by the local authority's levy department | YES | YES | מתי משלמים היטל השבחה, ומה הקונה בודק? (H3) | - |
| 171 | Betterment levy | Tax on the seller's benefit from approved plans that add unrealised building rights | YES | YES | מתי משלמים היטל השבחה, ומה הקונה בודק? (H3) | - |
| 172 | Betterment levy | Example: roof room right on a roof flat raises value through a municipal plan | NO | YES | מתי משלמים היטל השבחה, ומה הקונה בודק? (H3) | - |
| 173 | Betterment levy | Levy rate is half of the increase in value | YES | YES | מתי משלמים היטל השבחה, ומה הקונה בודק? (H3) | - |
| 174 | Betterment levy | Seller or lawyer can ask the municipality pre-signing; buyer's lawyer can use a power of attorney | NO | YES | מתי משלמים היטל השבחה, ומה הקונה בודק? (H3) | - |
| 175 | Betterment levy | Exemption: building or extending a home up to 140 sqm total | NO | YES | מה זה פטור 140 מטר מהיטל השבחה? (H3) | - |
| 176 | Betterment levy | Exemption: service areas added for accessibility | NO | YES | מה זה פטור 140 מטר מהיטל השבחה? (H3) | - |
| 177 | Betterment levy | Exemption: building a protected space (mamad) | NO | YES | מה זה פטור 140 מטר מהיטל השבחה? (H3) | - |
| 178 | Memorandum | A memorandum of understanding (zikaron devarim) is a short signed note of agreed basics after negotiation | NO | YES | מה זה זיכרון דברים, ומה כותבים בו? (H3) | - |
| 179 | Memorandum | Typical contents: flat ID, parties, price, payment schedule, handover date | NO | YES | מה זה זיכרון דברים, ומה כותבים בו? (H3) | - |
| 180 | Memorandum | Common error: believing a memo is not binding; courts judge substance, not title | NO | YES | האם זיכרון דברים מחייב? (H3) | - |
| 181 | Memorandum | A memo binds you while lacking detail you would have checked | NO | YES | למה לא לחתום על זיכרון דברים לפני הבדיקות? (H3) | - |
| 182 | Memorandum | Do not sign a memo; sign only a lawyer-prepared contract after checks | YES | YES | למה לא לחתום על זיכרון דברים (H3) | - |
| 183 | Memorandum | Land Law 1969 section 8 requires a writing for a land transaction commitment | NO | YES | האם זיכרון דברים מחייב? (H3) | - |
| 184 | Memorandum | Memo must meet finality (gmirut da'at) and definiteness (mesuyamut) | NO | YES | האם זיכרון דברים מחייב? (H3) | - |
| 185 | Memorandum | Court may fill missing terms of a memo | NO | YES | האם זיכרון דברים מחייב? (H3) | - |
| 186 | Memorandum | An unsigned memo can also form a deal; a signature usually proves intent | NO | YES | האם זיכרון דברים מחייב? (H3) | - |
| 187 | Memorandum | Memos are usually signed before legal advice and before the checks | PARTIAL | YES | למה לא לחתום על זיכרון דברים לפני הבדיקות? (H3) | - |
| 188 | Memorandum | Checks may expose gaps; leaving a memo can be impossible or costly | NO | YES | למה לא לחתום על זיכרון דברים לפני הבדיקות? (H3) | - |
| 189 | Memorandum | Memo date may be the trigger date for the 30 and 60 day tax duties, shortening your timetable | NO | YES | מתי מתחילים 30 הימים לדיווח לרשות המסים? (H3) | - |
| 190 | Memorandum | Bring a lawyer in at the start of negotiation | YES | YES | משא ומתן וזיכרון דברים (H2); תפקיד עורך הדין (H3) | - |
| 191 | Memorandum | If you insist on a memo, make it conditional on a signed contract within a fixed time, with automatic lapse | NO | YES | המוכר מתעקש על זיכרון דברים: איך מצמצמים את הסיכון? (H3) | - |
| 192 | Memorandum | Seller-side clause: memo gives no right to register a warning note | NO | YES | המוכר מתעקש על זיכרון דברים: איך מצמצמים את הסיכון? (H3) | - |
| 193 | Payment schedule | Payment schedule is the heart of the contract and balances both sides' protection | PARTIAL | YES | לוח התשלומים בעסקת יד שנייה (H2); איך בונים לוח תשלומים (H3) | - |
| 194 | Payment schedule | A wrong spread of payments puts the buyer's money at risk | PARTIAL | YES | לוח התשלומים בעסקת יד שנייה (H2); איך בונים לוח תשלומים (H3) | - |
| 195 | Payment schedule | Buyer's rationale: protect money while securing possession and registration, fitted to cash flow | PARTIAL | YES | לוח התשלומים בעסקת יד שנייה (H2); איך בונים לוח תשלומים (H3) | - |
| 196 | Lawyer | Never skip a lawyer who specialises in land and tax | YES | YES | תפקיד עורך הדין בקניית דירה (H3) | - |
| 197 | Lawyer | Lawyer checks registry status, liens, planning data, tax aspects | YES | YES | תפקיד עורך הדין בקניית דירה (H3) | - |
| 198 | Lawyer | Involve the lawyer from the negotiation stage | YES | YES | תפקיד עורך הדין בקניית דירה (H3) | - |
| 199 | Lawyer | Pick a lawyer with specific proven experience in property deals | PARTIAL | YES | איך בוחרים עורך דין לקניית דירה? (H3) | - |
| 200 | Lawyer | One lawyer for both sides saves a little but you should hire your own | YES | YES | תפקיד עורך הדין בקניית דירה (H3): כלל 14 | - |
| 201 | Lawyer | A broker may steer you to his own lawyer for a cut; avoid it | NO | YES | איך בוחרים עורך דין לקניית דירה? (H3) | - |
| 202 | Lawyer | Only your own lawyer represents you when a dispute arises | PARTIAL | YES | איך בוחרים עורך דין לקניית דירה? (H3) | - |
| 203 | Signing meeting | Signing is the buyer's first proprietary step | NO | YES | איך מתכוננים ליום החתימה על חוזה דירה? (H3) | - |
| 204 | Signing meeting | Review the final draft before the meeting; leave nothing open | PARTIAL | YES | איך מתכוננים ליום החתימה על חוזה דירה? (H3) | - |
| 205 | Signing meeting | After signing you are committed and there is in principle no way back | YES | YES | איך מתכוננים ליום החתימה על חוזה דירה? (H3) | - |
| 206 | Signing meeting | Attendees: both lawyers, the parties, companions, sometimes the broker | NO | YES | מי מגיע לחתימה, ואיפה היא נערכת? (H3) | - |
| 207 | Signing meeting | Raising new issues at the meeting can blow up the deal | NO | YES | איך מתכוננים ליום החתימה על חוזה דירה? (H3) | - |
| 208 | Signing meeting | Three parts: sign contract, sign accompanying documents, pay the first instalment | NO | YES | על מה חותמים ביום החתימה? (H3) | - |
| 209 | Signing meeting | Issue a rights certificate current to signing day and attach it to the contract | PARTIAL | YES | על מה חותמים ביום החתימה? (H3) | - |
| 210 | Signing meeting | Meeting takes about 1 to 1.5 hours, usually at the sellers' lawyer's office | NO | PARTIAL | מי מגיע לחתימה, ואיפה היא נערכת? (H3) | משך הפגישה (שעה עד שעה וחצי); המקום (משרד עורך הדין של המוכרים) כן מופיע |
| 211 | Contract | Opening: parties, date, place; recitals on the flat, register, seller rights, restrictions to clear | NO | YES | מה כולל חוזה קניית דירה יד שנייה? (H3): טבלת הפרקים | - |
| 212 | Contract | Representations: seller is sole lawful owner, clean title; buyer inspected and takes it as is | NO | YES | מה כולל חוזה קניית דירה יד שנייה? (H3): טבלת הפרקים | - |
| 213 | Contract | Transaction clause: sale of all rights with fixtures, exclusive possession, registration against full payment | NO | PARTIAL | מה כולל חוזה קניית דירה יד שנייה? (H3): טבלת הפרקים | סעיף העסקה במלואו (מכירת כל הזכויות עם המחוברים, חזקה בלעדית, רישום מול תשלום מלא); בטבלה רק 'הדירה וההצמדות' ו'החזקה' |
| 214 | Contract | Consideration chapter: schedule, how paid, warning note, trust cheque, clearing liens, handing documents on last payment | PARTIAL | YES | מה כולל חוזה (H3): המחיר והתשלומים; לוח התשלומים (H2) | - |
| 215 | Contract | Handover chapter: date, vacant flat, physical condition (systems work, normal wear) and clean legal title | NO | YES | מה כולל חוזה (H3): החזקה | - |
| 216 | Contract | Irrevocable powers of attorney: sellers to lawyers for registration; buyers to sellers' lawyer to delete notes on buyer breach | NO | YES | מה זה ייפוי כוח בלתי חוזר בעסקת דירה? (H3) | - |
| 217 | Contract | Buyer's mortgage chapter: sellers sign bank papers, allow appraiser access | NO | YES | מה כולל חוזה (H3): המשכנתא שלכם | - |
| 218 | Contract | Breach and remedies: notice and cure, definition of material breach, agreed damages without proof | PARTIAL | YES | מה זה פיצויים מוסכמים, ומה קורה כשצד אחד מפר? (H3) | - |
| 219 | Contract | Daily damages for delay and fixed 10% agreed damages on material breach | NO | PARTIAL | מה זה פיצויים מוסכמים, ומה קורה כשצד אחד מפר? (H3) | הפיצוי המוסכם של 10% והפיצוי היומי לאיחור; בדף 'פיצוי לכל יום או חודש' וסכום קבוע בלי שיעור |
| 220 | Contract | Miscellaneous: force majeure, written amendments, lawyer details, formal notices | NO | YES | מה כולל חוזה (H3): הוראות כלליות | - |
| 221 | Tip: organisation | Keep an organised binder of originals and copies of contract papers | NO | YES | מה לוקחים הביתה מהחתימה? (H3) | - |
| 222 | Tip: organisation | Set calendar reminders along the timeline | YES | YES | קניית דירה: המועדים אחרי החתימה (H3); כלי לוח הזמנים | - |
| 223 | Security mechanisms | Irrevocable power of attorney from sellers to register the transfer | NO | YES | אילו מנגנוני הגנה עורך הדין מכניס לחוזה? (H3) | - |
| 224 | Security mechanisms | Signed deeds of sale and other registration documents | NO | YES | אילו מנגנוני הגנה עורך הדין מכניס לחוזה? (H3) | - |
| 225 | Security mechanisms | Documents held in trust by the sellers' lawyer | NO | YES | אילו מנגנוני הגנה עורך הדין מכניס לחוזה? (H3) | - |
| 226 | Security mechanisms | Payment grace of 7-14 days without breach or damages | NO | PARTIAL | אילו מנגנוני הגנה עורך הדין מכניס לחוזה? (H3) | מספר ימי החסד (7 עד 14); בדף 'ימי חסד' בלי מספר |
| 227 | Security mechanisms | Clear clause for deleting the note and cancelling, with personal delivery notice and cure time | NO | YES | אילו מנגנוני הגנה עורך הדין מכניס לחוזה? (H3) | - |
| 228 | Security mechanisms | Agreed-compensation mechanism for breach or late handover | PARTIAL | YES | אילו מנגנוני הגנה עורך הדין מכניס לחוזה? (H3) | - |
| 229 | Security mechanisms | Sellers must sign buyer's mortgage papers, allow appraiser, spouse consent | NO | YES | אילו מנגנוני הגנה עורך הדין מכניס לחוזה? (H3) | - |
| 230 | Security mechanisms | Tax deposit in trust if tax approvals are missing at handover | NO | YES | אילו מנגנוני הגנה עורך הדין מכניס לחוזה? (H3) | - |
| 231 | Security mechanisms | Insure the flat at replacement value, all risks, from signing to handover | NO | YES | אילו מנגנוני הגנה עורך הדין מכניס לחוזה? (H3) | - |
| 232 | Security mechanisms | Force-majeure clause covering strikes at registry, tax office, bank | NO | YES | אילו מנגנוני הגנה עורך הדין מכניס לחוזה? (H3) | - |
| 233 | Annexes | Annexes are an integral part of the contract | NO | YES | מה כולל חוזה (H3): הנספחים | - |
| 234 | Annexes | Typical annexes: extract, payoff letter, plans or original contract, lease, probate or will order | NO | YES | מה כולל חוזה (H3): הנספחים | - |
| 235 | Accompanying documents | Parties also sign a set of accompanying documents that let lawyers execute the deal | NO | YES | על מה חותמים ביום החתימה? (H3) | - |
| 236 | Accompanying documents | Set includes: note request, irrevocable registration POA, irrevocable deletion POA, deeds of sale, transfer request, register-specific forms | NO | YES | על מה חותמים ביום החתימה? (H3) | - |
| 237 | Accompanying documents | Except note forms, the set stays with the sellers' lawyer until handover and last payment | NO | YES | על מה חותמים ביום החתימה? (H3) | - |
| 238 | Accompanying documents | Sign the declaration of correctness for the online Tax Authority report | PARTIAL | YES | על מה חותמים ביום החתימה? (H3); מה כוללת ההצהרה (H3) | - |
| 239 | First payment | First instalment is paid by bank cheque, which carries a fee of about 13-14 NIS | NO | NO | התשלום הראשון: איך מוסרים אותו בלי טעויות? (H3); איך בונים לוח תשלומים (H3) | עמלת הוצאת ההמחאה הבנקאית (כ־13 עד 14 ₪); בדף ההמחאה מוזכרת בלי עלות |
| 240 | First payment | First instalment is typically 10-20% of the price, sometimes 30-40% | NO | PARTIAL | התשלום הראשון: איך מוסרים אותו בלי טעויות? (H3); איך בונים לוח תשלומים (H3) | שיעור התשלום הראשון הנהוג (10% עד 20%); הדף אומר שאין שיעור בחוק והוא נקבע במשא ומתן |
| 241 | First payment | Cheque is held in trust by sellers' lawyer so the warning note can be registered first | YES | YES | התשלום הראשון: איך מוסרים אותו בלי טעויות? (H3) | - |
| 242 | First payment | Set in the contract a fixed number of days to register the note | PARTIAL | YES | התשלום הראשון: איך מוסרים אותו בלי טעויות? (H3) | - |
| 243 | First payment | Get a photo of the cheque and a signed receipt from the sellers' lawyer | NO | YES | התשלום הראשון: איך מוסרים אותו בלי טעויות? (H3) | - |
| 244 | First payment | Check exact spelling of seller's name; joint account; split cheques among several sellers | NO | YES | התשלום הראשון: איך מוסרים אותו בלי טעויות? (H3) | - |
| 245 | Cash deal | In a cash deal the full price is paid at signing and keys handed over, but all other steps still apply | NO | YES | קונים בלי משכנתא: מה משתנה בעסקה במזומן? (H3) | - |
| 246 | Warning note | Registering a warning note is the second proprietary step; do it as soon as possible | YES | YES | מה זה הערת אזהרה, ומפני מה היא מגינה? (H3) | - |
| 247 | Warning note | Purpose: stop the seller from making conflicting deals until final registration | PARTIAL | YES | מה זה הערת אזהרה, ומפני מה היא מגינה? (H3) | - |
| 248 | Warning note | Gives public notice and shields from third parties and attachments until deleted at final registration | NO | YES | מה זה הערת אזהרה, ומפני מה היא מגינה? (H3) | - |
| 249 | Warning note | The buyer's bank needs the note before lending | NO | YES | מתי רושמים הערת אזהרה (H3): מהשטח | - |
| 250 | Warning note | Flats registered with ILA or a housing company use a different, slower procedure | YES | YES | דירה שלא רשומה בטאבו: מה רושמים ברמ״י ובחברה משכנת? (H3) | - |
| 251 | Warning note | Two layers of protection: internal (registry blocks conflicting acts) and external (public sees it) | NO | YES | מה זה הערת אזהרה, ומפני מה היא מגינה? (H3) | - |
| 252 | Warning note | Tabu filing documents: IDs, request form, commitment document, fee proof, extras for company, POA, unregistered seller | NO | YES | מי יכול להגיש את הבקשה, ואילו מסמכים צריך? (H3) | - |
| 253 | Warning note | Lawyer files online through the Justice Ministry system with a lawyer's declaration form | NO | YES | מי יכול להגיש את הבקשה, ואילו מסמכים צריך? (H3) | - |
| 254 | Warning note | Online filing takes 1-2 working days; fee 150 NIS (2026) | PARTIAL | YES (updated) | כמה עולה רישום הערת אזהרה, וכמה זמן זה לוקח? (H3); מי יכול להגיש (H3) | (updated) האגרה הרשמית 2026 היא 188 ₪ ויעד הטיפול הרשמי עד 3 ימי עסקים (לא 150 ₪ ו־1 עד 2 ימים) |
| 255 | Warning note | In-person filing by courier with POA and lawyer card, or by the buyers; done on the spot; fee 188 NIS | PARTIAL | YES (updated) | כמה עולה רישום הערת אזהרה, וכמה זמן זה לוקח? (H3); מי יכול להגיש (H3) | (updated) הדף מציג הגשה בלשכה או בדואר, אגרה 188 ₪ (הודעת האגרות 2026) |
| 256 | Warning note | ILA or housing-company registration needs more forms and takes 7-14 days or longer | NO | PARTIAL | דירה שלא רשומה בטאבו: מה רושמים ברמ״י ובחברה משכנת? (H3) | זמן הטיפול ברמ״י או בחברה משכנת (7 עד 14 יום); הדף: 'לכל גוף זמן טיפול משלו' |
| 257 | Warning note | ILA note is usually free; housing company charges 150-500 NIS under the price-control order; some add 350 handling | NO | PARTIAL | דירה שלא רשומה בטאבו: מה רושמים ברמ״י ובחברה משכנת? (H3) | טווח אגרת החברה המשכנת (150 עד 500 ₪); הדף: 'לפי תעריף החברה'. הודעה חינמית של רמ״י על רישום זכויות כן מופיעה |
| 258 | Pledge registry | When registered only with a housing company, the buyer's lawyer may register a pledge on the seller's rights at the Pledge Registrar | NO | YES | דירה שלא רשומה בטאבו (H3): מהשטח, רשם המשכונות | - |
| 259 | Pledge registry | Pledge registration fee 38-190 NIS depending on period | NO | PARTIAL | דירה שלא רשומה בטאבו (H3): מהשטח, רשם המשכונות | סכום אגרת רישום המשכון (38 עד 190 ₪); בדף רק שהאגרה לפי תקופת המשכון, וזמני הטיפול |
| 260 | Warning note | After the note, order a fresh rights certificate to verify it and that nothing new was registered | PARTIAL | YES | איך בודקים שהערת האזהרה נרשמה? (H3) | - |
| 261 | Warning note | Add a clause: if registration is delayed for objective reasons, the cheque stays held until removed | NO | YES | מה אם הרישום מתעכב, או שהעסקה מתבטלת? (H3) | - |
| 262 | Tax report | Buyer must file a declaration within 30 days under section 73(c) of the Land Taxation Law | YES | YES | מה כוללת ההצהרה לרשות המסים, ומי מגיש אותה? (H3) | - |
| 263 | Tax report | Declaration contents: parties, right, block/parcel/date/features, price, tax and calculation, exemption claim | NO | YES | מה כוללת ההצהרה לרשות המסים, ומי מגיש אותה? (H3) | - |
| 264 | Tax report | Attach contract, extract, Form 7000A for several non-family buyers, exemption papers | NO | PARTIAL | מה כוללת ההצהרה לרשות המסים, ומי מגיש אותה? (H3) | הטופס לכמה קונים שאינם בני משפחה אחת (7000א); בדף חוזה, נסח וטופס חתימות מקוצר |
| 265 | Tax report | Sign the correctness declaration before your lawyer | PARTIAL | YES | מה כוללת ההצהרה לרשות המסים, ומי מגיש אותה? (H3) | - |
| 266 | Tax report | Filing is online via the representative system with a smart card | NO | YES | מה כוללת ההצהרה לרשות המסים, ומי מגיש אותה? (H3) | - |
| 267 | Tax report | After filing the Tax Authority sends a confirmation and payment voucher, also issuable online | NO | YES | איך משלמים את מס הרכישה, ומה קורה באיחור? (H3) | - |
| 268 | Tax report | Pay at bank branches by voucher or by card on the gov site | NO | YES | איך משלמים את מס הרכישה, ומה קורה באיחור? (H3) | - |
| 269 | Tax report | Pay purchase tax within 60 days of the deal | YES | YES | קניית דירה: המועדים אחרי החתימה (H3) | - |
| 270 | Tax report | Check the lawyer filed on time, or fines and interest follow | PARTIAL | YES | מה כוללת ההצהרה לרשות המסים (H3) | - |
| 271 | Tax report | If the Tax Authority's assessment is higher, pay the difference within 30 days of notice | NO | YES (updated) | איך משלמים את מס הרכישה, ומה קורה באיחור? (H3) | (updated) הדף קובע לפי סעיפים 90א ו־91(א): הפרש שומת המנהל בתוך 15 יום, והחלק שאינו במחלוקת בהשגה בתוך 30 יום (לא 30 יום להפרש) |
| 272 | Warning: late payment | Late sums collect linkage, interest and a penalty of 0.2% per week | NO | PARTIAL | איך משלמים את מס הרכישה, ומה קורה באיחור? (H3) | קנס הפיגורים של 0.2% לשבוע; בדף 'קנס פיגורים על כל שבוע' בלי השיעור (יש 310 ₪ לשבועיים, 5% קנס מנהלי, 2 פרומיל) |
| 273 | Tax report | Banks require a copy of the online declaration and the correctness form | NO | YES | מה כוללת ההצהרה לרשות המסים (H3) | - |
| 274 | Tip: reminders | Add reminders at 30 and 60 days from signing | YES | YES | קניית דירה: המועדים אחרי החתימה (H3); כלי לוח הזמנים | - |
| 275 | Betterment advance | Buyer must transfer an advance on seller's betterment tax under section 15(b) | YES | YES | מה זו מקדמה על חשבון מס השבח? (H3); המקדמה על מס השבח: מה קורה בה אחרי החתימה (H3) | - |
| 276 | Betterment advance | Advance rate 15% or 7.5% of the price depending on purchase date | YES | YES | מה זו מקדמה על חשבון מס השבח? (H3); המקדמה על מס השבח: מה קורה בה אחרי החתימה (H3) | - |
| 277 | Betterment advance | Advance is deemed paid by the seller and also counts as payment to the seller | NO | YES | מה זו מקדמה על חשבון מס השבח? (H3); המקדמה על מס השבח: מה קורה בה אחרי החתימה (H3) | - |
| 278 | Betterment advance | Tax Director stamp on the voucher serves as betterment-tax clearance for registration | NO | YES | מה זו מקדמה על חשבון מס השבח? (H3); המקדמה על מס השבח: מה קורה בה אחרי החתימה (H3) | - |
| 279 | Betterment advance | Transfer it only after paying the seller 40% of the price | YES | YES | מה זו מקדמה על חשבון מס השבח? (H3); המקדמה על מס השבח: מה קורה בה אחרי החתימה (H3) | - |
| 280 | Betterment advance | Advance does not apply to a qualifying-home exemption sale or non-cash consideration | PARTIAL | YES | מה זו מקדמה על חשבון מס השבח? (H3); המקדמה על מס השבח: מה קורה בה אחרי החתימה (H3) | - |
| 281 | Mortgage execution | Start the mortgage process right after signing because it is slow | PARTIAL | YES | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | - |
| 282 | Mortgage execution | Borrower papers: IDs, 3 months bank statements, loan list, payslips or tax assessments, guarantors | NO | PARTIAL | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | שלושה חודשי דפי חשבון (המספר 3); בדף 'דפי חשבון מהחודשים האחרונים' |
| 283 | Mortgage execution | Sign mortgage documents at the bank branch | NO | YES | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | - |
| 284 | Mortgage execution | Provide proof of building and life insurance | PARTIAL | YES | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | - |
| 285 | Mortgage execution | Bank appraiser from the bank's approved list values the flat | PARTIAL | YES | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | - |
| 286 | Mortgage execution | Sign a notarial power of attorney for the bank | NO | YES | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | - |
| 287 | Mortgage execution | Sign the bank's affidavit stating single or additional flat | NO | YES | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | - |
| 288 | Mortgage execution | Sellers sign confirmation of sums received and payment account instructions with proof of account | NO | YES | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | - |
| 289 | Mortgage execution | Sellers sign an undertaking to register a mortgage, creating a bank warning note | NO | YES | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | - |
| 290 | Mortgage execution | Bank wants interim protection until its mortgage is registered | NO | YES | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | - |
| 291 | Mortgage execution | Lawyer registers the bank's note, gives confirmation and a fresh extract for the bank | NO | YES | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | - |
| 292 | Tip: mortgage | Order the bank's papers right after signing; lawyers coordinate sellers' signatures | NO | YES | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | - |
| 293 | Tip: mortgage | Bank usually demands you pay your full equity to the sellers before releasing the loan | NO | YES | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | - |
| 294 | Mortgage execution | Sellers' document set: undertaking, note request, receipt confirmation, cancelled cheque, ID copies | NO | YES | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | - |
| 295 | Mortgage execution | Contract should bind sellers to return signed papers in a fixed time (for example 5 business days) | NO | PARTIAL | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | המועד הקבוע להחזרת המסמכים (5 ימי עסקים); בדף 'בתוך מספר ימים קבוע' |
| 296 | Mortgage execution | Bank pays sellers directly by transfer or banker's cheque | NO | YES | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | - |
| 297 | Mortgage execution | Paying off the sellers' mortgage: funds go to their loan account under a letter of intent with exact sum and date | NO | YES | מה הבנק מבקש כדי להעביר את כספי המשכנתא? (H3) | - |
| 298 | Seller mortgage clearing | Contract must provide a mechanism so you receive the flat clean | PARTIAL | YES | מה עושים כשעל הדירה רשומה משכנתא של המוכרים (H3); איך מוודאים שהמשכנתא של המוכר באמת נמחקה? (H3) | - |
| 299 | Seller mortgage clearing | Larger seller mortgage means an earlier clearing date in the schedule | NO | YES | מה עושים כשעל הדירה רשומה משכנתא של המוכרים (H3); איך מוודאים שהמשכנתא של המוכר באמת נמחקה? (H3) | - |
| 300 | Seller mortgage clearing | Three ways: drag the mortgage, freeze it, or pay it off | NO | YES | מה עושים כשעל הדירה רשומה משכנתא של המוכרים (H3); איך מוודאים שהמשכנתא של המוכר באמת נמחקה? (H3) | - |
| 301 | Seller mortgage clearing | Obtain an original, valid letter of intent with the exact payoff | NO | YES | מה עושים כשעל הדירה רשומה משכנתא של המוכרים (H3); איך מוודאים שהמשכנתא של המוכר באמת נמחקה? (H3) | - |
| 302 | Warning: payoff | Pay exactly per the letter, into the loan account not the current account | NO | YES | מה עושים כשעל הדירה רשומה משכנתא של המוכרים (H3); איך מוודאים שהמשכנתא של המוכר באמת נמחקה? (H3) | - |
| 303 | Seller mortgage clearing | After payoff get a clean extract and clean pledge-registry result; pay no further sums until then | NO | YES | מה עושים כשעל הדירה רשומה משכנתא של המוכרים (H3); איך מוודאים שהמשכנתא של המוכר באמת נמחקה? (H3) | - |
| 304 | Municipal certificate | Producing the municipal certificate is the seller's contractual duty | YES | YES | אישור עירייה לטאבו: מה הוא מכסה, ואיך מזמינים אותו? (H3) | - |
| 305 | Municipal certificate | It is needed to register the transfer along with the tax approvals | YES | YES | אישור עירייה לטאבו: מה הוא מכסה, ואיך מזמינים אותו? (H3) | - |
| 306 | Municipal certificate | It confirms the seller has no arnona or betterment-levy debt | YES | YES | אישור עירייה לטאבו: מה הוא מכסה, ואיך מזמינים אותו? (H3) | - |
| 307 | Municipal certificate | It can take time, so sellers should order early | NO | YES | אישור עירייה לטאבו: מה הוא מכסה, ואיך מזמינים אותו? (H3) | - |
| 308 | Municipal certificate | Municipalities Ordinance section 324 bars registration without the certificate | YES | YES | אישור עירייה לטאבו: מה הוא מכסה, ואיך מזמינים אותו? (H3) | - |
| 309 | Municipal certificate | Certificate covers arnona and betterment levy (plus fees and development levies) | PARTIAL | YES | אישור עירייה לטאבו: מה הוא מכסה, ואיך מזמינים אותו? (H3) | - |
| 310 | Municipal certificate | Order it after signing from the collections department by form, email or fax | NO | YES | אישור עירייה לטאבו: מה הוא מכסה, ואיך מזמינים אותו? (H3) | - |
| 311 | Municipal certificate | Attach full contract, rights certificate and both sides' IDs with appendices | NO | YES | אישור עירייה לטאבו: מה הוא מכסה, ואיך מזמינים אותו? (H3) | - |
| 312 | Municipal certificate | Some municipalities offer an online form | NO | YES | אישור עירייה לטאבו: מה הוא מכסה, ואיך מזמינים אותו? (H3) | - |
| 313 | Municipal certificate | Fee is about 100-200 NIS | NO | PARTIAL | אישור עירייה לטאבו: מה הוא מכסה, ואיך מזמינים אותו? (H3) | האגרה (100 עד 200 ₪); בדף 'האגרה וזמן הטיפול משתנים מרשות לרשות' |
| 314 | Municipal certificate | Processing takes up to 30 days, or 3-4 months where a levy may apply (roof flats, houses) | NO | PARTIAL | אישור עירייה לטאבו: מה הוא מכסה, ואיך מזמינים אותו? (H3) | זמן הטיפול (עד 30 יום, או 3 עד 4 חודשים כשיש היטל); בדף רק 'הבדיקה ארוכה יותר' בלי מספר |
| 315 | Municipal certificate | An inspector may measure the property | NO | YES | אישור עירייה לטאבו: מה הוא מכסה, ואיך מזמינים אותו? (H3) | - |
| 316 | Municipal certificate | In some small authorities two bodies issue it (council and local committee), so verify the full certificate | NO | PARTIAL | אישור עירייה לטאבו: מה הוא מכסה, ואיך מזמינים אותו? (H3) | שני גופים מנפיקים (מועצה וועדה מקומית) ביישובים קטנים; בדף רק שבחלק מהרשויות שני האישורים יוצאים יחד ובחלק בנפרד, ושבמועצה מקומית חל סעיף 21 |
| 317 | Tax approvals | Collect all tax approvals early | PARTIAL | YES | אישורי המסים לטאבו (H3); אישור עירייה לטאבו (H3) | - |
| 318 | Tax approvals | Two kinds: Land Taxation (purchase and betterment tax) and municipal | PARTIAL | YES | אישורי המסים לטאבו (H3); אישור עירייה לטאבו (H3) | - |
| 319 | Tax approvals | If no voluntary deal since 31.12.1999, a property-tax (mas rechush) clearance is required | NO | PARTIAL | אישורי המסים לטאבו (H3); אישור עירייה לטאבו (H3) | כלל 31.12.1999 (בלי עסקה מרצון מאז נדרש אישור מס רכוש); בדף רק שנדרש אישור שאין חוב במס רכוש |
| 320 | Tax approvals | Approvals take time; chase them | NO | YES | אישורי המסים לטאבו (H3); אישור עירייה לטאבו (H3) | - |
| 321 | Tax approvals | Buyer's bank wants all approvals before releasing the final loan sum | NO | YES | אישורי המסים לטאבו (H3); אישור עירייה לטאבו (H3) | - |
| 322 | Tax approvals | Check the approvals show full names, block/parcel and the right fraction | NO | YES | אישורי המסים לטאבו (H3); אישור עירייה לטאבו (H3) | - |
| 323 | Tax deposit | If sellers lack an approval at handover, a fixed sum of the last payment is held in trust | NO | YES | פיקדון מסים: מה עושים כשאישור חסר ביום המסירה? (H3) | - |
| 324 | Tax deposit | Deposit counts as payment to the sellers and secures later delivery of approvals | NO | YES | פיקדון מסים: מה עושים כשאישור חסר ביום המסירה? (H3) | - |
| 325 | Tax deposit | Sellers' lawyer gets irrevocable instruction to pay sellers' tax or levy debts from it | NO | YES | פיקדון מסים: מה עושים כשאישור חסר ביום המסירה? (H3) | - |
| 326 | Warning: tax deposit | Size it to cover maximum exposure plus a margin, held in a deal-specific trust account | NO | YES | פיקדון מסים: מה עושים כשאישור חסר ביום המסירה? (H3) | - |
| 327 | Tax approvals | Buyer's lawyer adds approvals to the "tabu file" | NO | YES | הרישום על שמכם (H2): למה הרישום חשוב (H3) | - |
| 328 | Mortgage deeds | Collect the mortgage deeds from the bank in time | PARTIAL | YES | שטרי משכנתא: מתי מזמינים, ואצל מי חותמים? (H3) | - |
| 329 | Mortgage deeds | Ordering deeds takes 7-10 business days | NO | PARTIAL | שטרי משכנתא: מתי מזמינים, ואצל מי חותמים? (H3) | זמן הזמנת השטרות (7 עד 10 ימי עסקים); בדף 'זה לוקח זמן' בלי מספר |
| 330 | Mortgage deeds | The bank's warning note is interim; the mortgage is registered with the transfer, and the note is then deleted | NO | YES | שטרי משכנתא: מתי מזמינים, ואצל מי חותמים? (H3) | - |
| 331 | Mortgage deeds | Sign deeds before your lawyer, who certifies them under regulation 14(b) of the 2011 land regulations | NO | YES | שטרי משכנתא: מתי מזמינים, ואצל מי חותמים? (H3) | - |
| 332 | Mortgage deeds | Order deeds early to avoid bank delays such as strikes | NO | YES | שטרי משכנתא: מתי מזמינים, ואצל מי חותמים? (H3) | - |
| 333 | Handover | Handover date is fixed in the contract | PARTIAL | YES | איך עושים את החילוף: התשלום האחרון מול המפתח והמסמכים? (H3) | - |
| 334 | Handover | Sellers give physical possession against the last payment and all legal documents | NO | YES | איך עושים את החילוף: התשלום האחרון מול המפתח והמסמכים? (H3) | - |
| 335 | Handover | Confirm with the lawyer that all documents are ready back to back with the last payment | NO | YES | איך עושים את החילוף: התשלום האחרון מול המפתח והמסמכים? (H3) | - |
| 336 | Handover | Routine: move meters (power, gas, arnona, water) and confirm no debts | PARTIAL | YES | חזקה פיזית או חזקה משפטית (H3); מה בודקים כשנפגשים בדירה (H3) | - |
| 337 | Handover | Physical handover means a clean vacant flat except fixtures and agreed contents | NO | YES | חזקה פיזית או חזקה משפטית (H3); מה בודקים כשנפגשים בדירה (H3) | - |
| 338 | Handover | Legal handover applies to a tenanted flat; buyer steps into seller's shoes and collects rent | NO | YES | חזקה פיזית או חזקה משפטית: מה מקבלים ביום המסירה? (H3) | - |
| 339 | Handover | Transfer the tenant's cheques and securities (cheques, promissory note, guarantee, deposit) | NO | YES | חזקה פיזית או חזקה משפטית: מה מקבלים ביום המסירה? (H3) | - |
| 340 | Handover | Meet at the flat; walk room by room testing AC, lights, boiler, taps, shutters, damp | PARTIAL | YES | מה בודקים כשנפגשים בדירה? (H3) | - |
| 341 | Handover | Pay the final balance at handover, or into the tax deposit if approvals are missing | NO | YES | איך עושים את החילוף (H3) | - |
| 342 | Handover protocol | Write a short handover protocol (handwritten is fine) with names, address, date and time | PARTIAL | YES | מה כותבים בפרוטוקול המסירה? (H3); כלי פרוטוקול ומפתחות | - |
| 343 | Handover protocol | Record seller-fixable defects, with photos or video | NO | YES | מה כותבים בפרוטוקול המסירה? (H3); כלי פרוטוקול ומפתחות | - |
| 344 | Handover protocol | Record meter readings and tenant cheque details | NO | YES | מה כותבים בפרוטוקול המסירה? (H3); כלי פרוטוקול ומפתחות | - |
| 345 | Handover protocol | Both sign and each keeps a copy | NO | YES | מה כותבים בפרוטוקול המסירה? (H3); כלי פרוטוקול ומפתחות | - |
| 346 | Utilities | Electric meter: call the power company (103) together; seller settles debt by card | NO | YES | איך מעבירים חשמל, מים, גז וארנונה על שמכם? (H3) | - |
| 347 | Utilities | Arnona and water: change names at the municipality and the water corporation | PARTIAL | YES | איך מעבירים חשמל, מים, גז וארנונה על שמכם? (H3) | - |
| 348 | Utilities | If tenanted, change owner names but not meters, since a separate occupier record exists | NO | YES | איך מעבירים חשמל, מים, גז וארנונה על שמכם? (H3) | - |
| 349 | Utilities | Gas: transfer the meter; the seller's deposit is refunded or swapped | NO | YES | איך מעבירים חשמל, מים, גז וארנונה על שמכם? (H3) | - |
| 350 | Utilities | Get a signed no-debt confirmation from the building committee | PARTIAL | YES | איך מעבירים חשמל, מים, גז וארנונה על שמכם? (H3): ועד הבית | - |
| 351 | Handover | Receive all keys (flat, building entrance and code, mailbox, storage, event room, shelter, parking remotes) | NO | YES | מה כותבים בפרוטוקול המסירה? (H3): רשימת מפתחות | - |
| 352 | Registration | Registration is the last step and completes the purchase in property terms | PARTIAL | YES | למה הרישום חשוב אם המפתח כבר אצלכם? (H3) | - |
| 353 | Registration | If financed, the buyer's mortgage is registered in parallel with the transfer | NO | YES | למה הרישום חשוב אם המפתח כבר אצלכם? (H3) | - |
| 354 | Registration | Why it matters: final legal protection against the world, enables the mortgage, eases resale | NO | YES | למה הרישום חשוב אם המפתח כבר אצלכם? (H3) | - |
| 355 | Registration | Land Law section 7(a): the deal completes when registered | NO | YES | למה הרישום חשוב אם המפתח כבר אצלכם? (H3) | - |
| 356 | Registration | Done by the buyer's lawyer, who assembles the file after handover | NO | YES | למה הרישום חשוב אם המפתח כבר אצלכם? (H3) | - |
| 357 | Registration | Three register types: tabu, Israel Land Authority, housing company | YES | YES | למה הרישום חשוב (H3); בדיקת זכויות ומסמכים (H2) | - |
| 358 | Registration | Required documents differ by register and change over time; check the current list | NO | YES | למה הרישום חשוב (H3); בדיקת זכויות ומסמכים (H2) | - |
| 359 | Registration | Registration takes from days to weeks depending on register and load | PARTIAL | YES | כמה זמן לוקח רישום בטאבו, וכמה הוא עולה? (H3) | - |
| 360 | Registration | The lawyer is notified and signed mortgage deeds come back | NO | YES | איך נרשמת המשכנתא שלכם יחד עם המכר? (H3) | - |
| 361 | Registration | Afterwards obtain a fresh extract or certificate to confirm registration | PARTIAL | YES | מה בודקים בנסח החדש, ואילו מסמכים שומרים? (H3) | - |
| 362 | Registration | Check names and ID numbers for typos that could block a later sale | NO | YES | מה בודקים בנסח החדש, ואילו מסמכים שומרים? (H3) | - |
| 363 | Registration | Keep an organised binder of all deal papers for years | NO | YES | מה בודקים בנסח החדש, ואילו מסמכים שומרים? (H3) | - |
| 364 | FAQ | Developer purchase is a paper or under-construction asset with harsher contract clauses than second-hand | YES | YES | יד שנייה, מקבלן או להשקעה: מה בודקים בכל סוג (H3) | - |
| 365 | FAQ | Lawyer fee averages about 0.5% plus VAT and is negotiable | YES | YES | שכר טרחה של עורך דין בקניית דירה: כמה, ומתי משלמים? (H3) | - |

## Counts

- Total units: 365
- YES (incl. updated): 341 (93%), of which YES (updated): 4
- PARTIAL: 23 (6%)
- NO: 1 (0%)

### Before and after

| Grade | Before (8.11.2026) | After (new page) | Change |
|---|---|---|---|
| YES (incl. updated) | 94 | 341 | +247 |
| PARTIAL | 90 | 23 | -67 |
| NO | 181 | 1 | -180 |
| Total | 365 | 365 | |

### Per their stage (units; YES / PARTIAL / NO before, then after)

| Stage | Units | YES before | PARTIAL before | NO before | YES after | PARTIAL after | NO after |
|---|---|---|---|---|---|---|---|
| השלב הטרום חוזי (intro) | 4 | 1 | 3 | 0 | 4 | 0 | 0 |
| בדיקות מקדמיות א: קנייניים ותכנוניים | 96 | 28 | 33 | 35 | 93 | 3 | 0 |
| בדיקות מקדמיות ב: כלכליים | 47 | 28 | 10 | 9 | 44 | 3 | 0 |
| בדיקות מקדמיות ג: מיסויים | 30 | 13 | 7 | 10 | 30 | 0 | 0 |
| משא ומתן וזיכרון דברים | 15 | 2 | 1 | 12 | 15 | 0 | 0 |
| בניית לוח תשלומים | 3 | 0 | 3 | 0 | 3 | 0 | 0 |
| עורך דין קניית דירה | 7 | 4 | 2 | 1 | 7 | 0 | 0 |
| שלב חתימת חוזה הרכישה | 43 | 3 | 7 | 33 | 37 | 5 | 1 |
| השלב שלאחר חתימת החוזה | 87 | 12 | 15 | 60 | 75 | 12 | 0 |
| שלב קבלת החזקה | 19 | 0 | 6 | 13 | 19 | 0 | 0 |
| שלב רישום הזכויות | 12 | 1 | 3 | 8 | 12 | 0 | 0 |
| שאלות נפוצות | 2 | 2 | 0 | 0 | 2 | 0 | 0 |

Stage ranges follow the unit order of the first map; the before columns reproduce its stage table.

## Units still not YES (24: 23 PARTIAL, 1 NO)

- #17 (PARTIAL): For newer flats research the builder: reputation, quality, defect suits; known builders can carry a 5-10% premium. Why: no official source for the premium; the builder search and defect-suit question are covered.
- #26 (PARTIAL): Plan with a horizon of at most about ten years. Why: simply missed (the ten years is advice, no source).
- #71 (PARTIAL): Local authority engineering department file is open to the public free. Why: simply missed.
- #114 (PARTIAL): Build a detailed spreadsheet of expected costs and add a safety margin of at least 5%. Why: simply missed (the 5% is advice, no source).
- #130 (PARTIAL): Total ancillary costs can reach 15% or more of the price. Why: deliberately different: we compute the ratio from official figures.
- #143 (PARTIAL): Gifting an owned flat to a child can turn an investor into a single-flat buyer: up to 20% more financing and lower purchase tax. Why: deliberately left without a number: it is a difference between the 50% and 70% caps and the move carries tax risk.
- #210 (PARTIAL): Meeting takes about 1 to 1.5 hours, usually at the sellers' lawyer's office. Why: no official source (practitioner estimate).
- #213 (PARTIAL): Transaction clause: sale of all rights with fixtures, exclusive possession, registration against full payment. Why: simply missed.
- #219 (PARTIAL): Daily damages for delay and fixed 10% agreed damages on material breach. Why: no official source; the page explains the legal test for agreed damages instead of a typical %.
- #226 (PARTIAL): Payment grace of 7-14 days without breach or damages. Why: no official source (drafting practice).
- #239 (NO): First instalment is paid by bank cheque, which carries a fee of about 13-14 NIS. Why: simply missed (a few shekels, bank tariff).
- #240 (PARTIAL): First instalment is typically 10-20% of the price, sometimes 30-40%. Why: no official source; the page says the law sets no rate.
- #256 (PARTIAL): ILA or housing-company registration needs more forms and takes 7-14 days or longer. Why: no official source for the time.
- #257 (PARTIAL): ILA note is usually free; housing company charges 150-500 NIS under the price-control order; some add 350 handling. Why: no official source; it is the housing company's own tariff.
- #259 (PARTIAL): Pledge registration fee 38-190 NIS depending on period. Why: simply missed (registrar fee table not quoted).
- #264 (PARTIAL): Attach contract, extract, Form 7000A for several non-family buyers, exemption papers. Why: simply missed.
- #272 (PARTIAL): Late sums collect linkage, interest and a penalty of 0.2% per week. Why: simply missed.
- #282 (PARTIAL): Borrower papers: IDs, 3 months bank statements, loan list, payslips or tax assessments, guarantors. Why: simply missed (the bank decides the period).
- #295 (PARTIAL): Contract should bind sellers to return signed papers in a fixed time (for example 5 business days). Why: no official source (drafting practice).
- #313 (PARTIAL): Fee is about 100-200 NIS. Why: no official source (varies by authority).
- #314 (PARTIAL): Processing takes up to 30 days, or 3-4 months where a levy may apply (roof flats, houses). Why: no official source (varies by authority).
- #316 (PARTIAL): In some small authorities two bodies issue it (council and local committee), so verify the full certificate. Why: simply missed (small-authority detail).
- #319 (PARTIAL): If no voluntary deal since 31.12.1999, a property-tax (mas rechush) clearance is required. Why: simply missed (the cut-off date rule).
- #329 (PARTIAL): Ordering deeds takes 7-10 business days. Why: no official source (bank practice).

The four YES (updated) units are #160, #254, #255 and #271: our page states the current official figure or rule (purchase-tax brackets frozen to 15.1.2028; 188 NIS warning-note fee with a 3-business-day target; the 15-day and 30-day payment rules of sections 90a and 91(a)).