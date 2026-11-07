# The buyer's bill of materials: everything an Israeli buyer decides, pays, checks, signs, risks and feels

Three levels: **branch → node → leaf**. For each leaf:
- **Phrasings:** exact Hebrew searches seen on 7.11.2026 (autocomplete = AC, related = REL, people-also-ask = PAA, AI answer wording = AI). "—" means no search phrasing was seen; the leaf comes from the competitors' structure or the process itself.
- **Who ranks:** observed in this pass or the first pass (`../serp-buying.md`). "not searched" when the leaf was not searched.
- **nad-lan owner:** from the live sitemap (`sitemap_index.xml`, read 7.11.2026, 4,665 URLs). A leaf with an owner gets a link from the hub, never a rival section or URL. **"Hub"** = no owner: the hub covers it as a section, FAQ item or tool (no new URLs are proposed in this research).

---

## 0. Should I buy at all, and when
| Node | Leaf | Phrasings | Who ranks | nad-lan owner |
|---|---|---|---|---|
| 0.1 Buy or rent | buy vs rent over time | לקנות דירה או לשכור · או לגור בשכירות (AC) | not searched; taxo.co.il (first pass) | /buy-vs-rent/ and /buy-or-rent/ (**two URLs, one intent: a finding for the owner**) |
| | buy vs invest the money | לקנות דירה או להשקיע בשוק ההון · או להשקיע (AC) · דירה להשקעה מול תיק השקעות (gurgroup title) | gurgroup | Hub (one paragraph + link to /buy-vs-rent/) |
| | buy to live vs buy to let | ערבוב מטרות הרכישה (AI, "טעויות") · איפה כדאי לקנות דירה למגורים (REL) | yonilevy | Hub; investment → /investment/ |
| 0.2 Timing | now or wait | האם לקנות דירה עכשיו (או לחכות) · לקנות דירה עכשיו (AC) · תחזית מחירי הדירות 2026 (REL) | TheMarker, kopel, Madlan blog, mdfinance, lazyinvestor | /israel-housing-market-buyers-2026/ (+ prices hub) |
| | buy before or after selling | קניית דירה לפני מכירה · לפני מכירת דירה קיימת (AC) · איך מוכרים וקונים דירה · הלוואת גישור (REL) | mashcantaman, ygoldlaw, midrag, ofekm | /mortgage-calculator/bridge-loan-apartment/ (bridge loan); the sequence decision → Hub |
| | life events | לפני החתונה (AC) · זוג צעיר · בגיל צעיר (AC) | kolzchut, 555, wecheck, yeda-kesef | Hub |
| | faith and luck | בספירת העומר · בשלושת השבועות (AC) · סגולה לקנות דירה (AC) · מכונס נכסים לפי ההלכה (AC) | not searched | Hub (one respectful FAQ) |
| | war and security | האם כדאי למכור דירה בזמן מלחמה (REL) | not searched | Hub (FAQ; safe room links) |
| 0.3 Readiness | "am I ready" | בשביל לקנות דירה כמה הון עצמי צריך · רוצה לקנות דירה אין לי הון עצמי (AC) | not searched | Hub (readiness tool) |
| | job and income stability | AI: "יציבות תעסוקתית", "ותק בעבודה" | yeda-kesef, TheMarker | Hub |

## 1. Money
| Node | Leaf | Phrasings | Who ranks | nad-lan owner |
|---|---|---|---|---|
| 1.1 Equity | how much is needed (by status) | הון עצמי לדירה · הון עצמי למשכנתא (REL) · אחוז מימון | Mizrahi, lazyinvestor | /mortgage-calculator/mortgage-ltv-ratio/ |
| | no or low equity | ללא / בלי הון עצמי · עם הון עצמי נמוך · ב-100 אחוז מימון · בארץ עם 100 אלף ש"ח · הון עצמי 100 אלף (AC, REL) | lazyinvestor, nahala, powercouple, Mizrahi, nitzanm, credit360, a developer's own page | **Hub (H2 + tool)** |
| | second flat with no equity | קניית דירה שניה ללא הון עצמי (AC, REL) | evensapir, hb-adv, lazyinvestor | Hub |
| | parents' help | משכון דירה של ההורים לטובת משכנתא (REL) · "הלוואת נדוניה" (AI) | nahala, Mashcantaman | Hub |
| | loans against savings | AI: "הלוואה… כנגד קרנות השתלמות, קופות גמל" | midrag | Hub |
| | general-purpose loans | משכנתא לכל מטרה (REL) | banks | /mortgage-calculator/mortgage-for-any-purpose/ |
| | equity calculator | מחשבון הון עצמי (REL) | not opened (CAPTCHA) | Hub tool |
| 1.2 Mortgage | pre-approval | אישור עקרוני (AI) | banks | /mortgage-calculator/mortgage-pre-approval/ |
| | repayment capacity | יחס החזר (AI) · מה התנאים ללקיחת משכנתא (REL) | banks, wecheck | /mortgage-calculator/mortgage-repayment-capacity/ |
| | rates and mix | ריבית קבועה / פריים (AI) | banks | /mortgage-calculator/mortgage-interest-rates/ |
| | refusal | — | — | /mortgage-calculator/mortgage-refusal/ |
| | advisor | — | — | /mortgage-advisor/ |
| | insurance (life, structure) | ביטוח חיים וביטוח מבנה (AI) | — | /mortgage-home-insurance/ |
| | eligibility loan (זכאות) | זכאות משכנתא לזוגות צעירים · משכנתא מועדפת · זכאות חוק הנגב (REL) | kolzchut, gov.il, Hapoalim | Hub section (zakaut.json data exists) |
| | buyer with no tabu: mortgage | משכנתא על דירה שלא רשומה בטאבו (REL) | not opened | Hub (tabu-status tool) |
| 1.3 Purchase tax | brackets by status | מס רכישה · מדרגות מס קניית דירה ראשונה · שניה מס (AC) | kolzchut, gov.il simulator | /purchase-tax-calculator/; /real-estate-tax-advisor/purchase-tax-first-home/; /real-estate-tax-advisor/purchase-tax-investor/ |
| | foreign resident / oleh | מס רכישה תושב חוץ · מס רכישה עולה חדש (REL) | y-tax, amitvered | /israel-purchase-tax-foreign-residents/ |
| | partners and shares | בשותפות מס רכישה · שליש דירה מס רכישה · רבע דירה מס רכישה · מס רכישה 1/3 דירה (AC, REL) | din.co.il forum, brikman-law | Hub (ownership-structure tool) |
| | on-paper timing | מתי משלמים מס רכישה על דירה על הנייר · מס רכישה דירה על הנייר (REL) | alev-law | Hub FAQ → purchase-tax pages |
| | avoiding tax legally | איך לא לשלם מס רכישה על דירה שניה (REL) | not opened | /real-estate-tax-advisor/ |
| | deadlines | "תוך 60 יום" / "30 יום" / "כ-40 יום" (AI, inconsistent) | AI only | Hub (deadline tool, verified) |
| 1.4 Professionals and fees | lawyer | עורך דין קניית דירה מחיר · שכר טרחה עורך דין אחוזים (REL) | doron-aharoni, midrag, kolzchut, hb-adv | /real-estate-lawyer/; /real-estate-lawyer/when-real-estate-lawyer-required/ |
| | developer's lawyer cap | שכר טרחת עורך דין קבלן (REL) · "כ-5,915 ש"ח… או 0.5%" (AI) | kolzchut | Hub line (orechdin.json) → /real-estate-lawyer/ |
| | broker | ללא תיווך · מתיווך (AC) | — | /selling-apartment/who-pays-broker-fees/ (seller side); Hub line |
| | appraiser | שמאי | — | /real-estate-appraiser/ |
| | inspection | בדק בית | laad-eng, shahar-bedek | /home-inspection/ |
| | registration fees | מהי אגרת רישום מכר בטאבו? (PAA) · שכר טרחה עורך דין רישום בטאבו (REL) | not opened | Hub line (condo.json, rishum.json) |
| | all costs together | עלויות · הוצאות נלוות (AC) · אקסל קניית דירה (AC, REL) · סימולטור קניית דירה (AC) | Osim Nadlan, fingrow | /apartment-purchase-cost-calculator/ |
| 1.5 New-build money | VAT inside the price | — | — | /new-projects/ pages (anatomy.json) |
| | index linkage | מדד תשומות הבנייה (AI) | elkayamlaw (calculator) | /new-projects/construction-input-index/ |
| | 20/80 and 10/90 deals | דירה מקבלן 20 80 · מבצעי 20 80 · דירות למכירה 90 10 · מבצעי קבלן (REL) | ynet, yasmint-law, bizportal, evensapir | /developer-deals/ (check its title); comparator → Hub tool |
| | "0% equity" developer offers | — (Globes 6.11.2026) | lazyinvestor, avivmelisron project page | Hub (risk tool) |
| 1.6 Payment schedule | second-hand | פריסת תשלומים בקניית דירה יד שניה (REL) | amitvered | Hub tool |
| | developer, by construction stage | קניית דירה מקבלן תשלומים · חוק המכר תשלומים לקבלן · חוק המכר תשלום לפי התקדמות הבנייה (REL) | s-sarfati, gelberglaw, kolzchut | Hub tool (payment-cap checker) |
| | Sale Law guarantee | ערבות בנקאית בקניית דירה מקבלן · נוסח ערבות חוק המכר (REL) | kolzchut, lt-law, doron-aharoni | /investment/bank-guarantee-purchase/; /real-estate-lawyer/sale-of-apartments-law/ |
| 1.7 Government help | discounted housing | דירה בהנחה · מחיר למשתכן (REL, AC) · לאחר זכייה במחיר למשתכן (AC) | not opened (CAPTCHA) | /dira-behanacha/ |
| | second-hand grant | מענק לרכישת דירה ראשונה למחוסרי דיור (REL) · "עד 50,000 ש"ח" (AI) | btl.gov.il, kolzchut, gov.il | Hub (benefits finder) |
| | disability | סיוע ברכישת דירה נכות כללית · מענק לרכישת דירה לנכים · לילד נכה (REL, AC) | btl.gov.il, kolzchut, gov.il | Hub (benefits finder, official links) |
| | IDF and security forces | אגף השיקום · משרד הביטחון · נכי צה"ל · לאנשי קבע · מילואים (AC) | shikum.mod.gov.il | Hub (benefits finder) |
| | discharged soldiers, olim | חייל משוחרר · לחיילים משוחררים · עולה חדש · לעולים חדשים (AC) | not searched | Hub (benefits finder) |
| | periphery | זכאות חוק הנגב (REL) · "מענקים בפריפריה" (AI) | broker-re | Hub (benefits finder) |
| | public housing purchase | מעמידר · דיור ציבורי · חלמיש (AC) | gov.il, amidar, knesset | Hub FAQ (law status) |
| 1.8 After the deal | moving | מה צריך לקנות כשעוברים דירה (AC) · הובלה (AI) | not searched | Hub (moving checklist) |
| | renovation | שיפוצים (AI) | — | /renovation-contractor/ |
| | arnona and utilities | ארנונה | — | /arnona/ |
| | house committee | ועד בית (AI) | — | Hub line |

## 2. Choices
| Node | Leaf | Phrasings | Who ranks | nad-lan owner |
|---|---|---|---|---|
| 2.1 Where | cheapest places / budget bands | איפה הכי זול לקנות דירה בישראל? (PAA) · איפה אפשר למצוא דירות למכירה עד מיליון שקל? (PAA ×3) · דירות עד 800 / 600 / 500 / 300 אלף (REL) · בזול · זולה (AC) | Yad2, Madlan (first pass) | /affordable-apartments-israel-2026/ |
| | a named city (about 70 seen) | לקנות דירה ב<עיר> (AC) | listing boards | city price pages (/<city>-apartment-prices/) and /properties/ |
| | investment cities | איפה כדאי לקנות דירה להשקעה (PAA, REL) | nadlanmaster | /investment/where-to-buy-investment-apartment/ + city investment pages |
| | abroad | בקפריסין · ביוון · בדובאי… (AC) | — | out of scope |
| 2.2 Neighbourhood and surroundings | schools, parks, clinics | AI: "מוסדות חינוך… מבני ציבור… פארקים" (Madlan tips) | Madlan | Hub (surroundings check) |
| | noise, visit at different hours | AI: "ביקור בסביבת הדירה בשעות שונות… בדיקת רעש, חניה" | yonilevy, ygoldlaw | Hub (visit scorecard) |
| | plans nearby (תב"ע) | AI: "תכניות עתידיות" | gov.il, Madlan | /guides/neighboring-development-check/ |
| | environmental hazards | — (AI mentions "בדיקה סביבתית") | — | /environmental-hazards/; /asbestos/ |
| 2.3 Type | second-hand vs new | מה ההבדל בין קניית דירה יד שניה לבין קניית דירה מקבלן? (Amit Vered FAQ) | amitvered | /buying-apartment/new-vs-second-hand/ |
| | on paper / presale | על הנייר · פריסייל (AC) · דירה על הנייר למכירה (REL) | socity, nadlanmaster, hadif, prlaw | /new-projects/presale-apartment/; /projects/ |
| | sell on paper later | לקנות דירה על הנייר ולמכור · מס שבח דירה על הנייר (REL) | — | Hub FAQ → capital-gains pages |
| | urban renewal unit | לפני פינוי בינוי · בפרויקט תמ"א 38 · עם פינוי ארוך · האם כדאי לקנות דירה פינוי בינוי (AC) | shorfinancy | /urban-renewal/ and children |
| | purchase group, kibbutz, sheltered housing | קבוצת רכישה · בקיבוץ · בדיור מוגן (AC) | — | Hub FAQ |
| 2.4 The unit | rooms, size, weighted area | 3 / 4 / 5 חדרים (AC) | listing boards | /apartment-prices/ (₪/m²) |
| | floor, view, orientation | AI: "הקומה, כיווני האוויר" | — | Hub (factor map, prices hub A2) |
| | parking, storage, roof (attached) | AI: "חניה, מחסן או גג… רשומים" | ygoldlaw | /guides/new-project-parking/; condo documents page |
| | safe room | ממ"ד (AI) | — | /guides/new-apartment-mamad/ |
| | balcony | — | — | /guides/new-apartment-balcony/ |
| | acoustics | — | — | /guides/new-apartment-acoustics/ |
| | elevator and maintenance fees | — | — | /guides/residential-tower-elevators/; /guides/new-project-management-fees/ |
| 2.5 Ownership structure | whose name | על שם אחד מבני הזוג · ידועים בציבור · הסכם ממון (AC, REL) | gov.il, kolzchut, family-law firms | Hub (ownership tool) |
| | for a child / minor | על שם הילד / הילדים / קטין · בנאמנות עבור קטין (AC) | not searched | Hub |
| | through a company | על שם חברה · כחברה · על ידי חברה מע"מ · עוסק מורשה (AC) | not searched | /investment/investment-via-company/ |
| | with partners, shares | עם שותף / שותפים · 3 שותפים · חצי / שליש דירה (AC) | yonilevy, brikman-law, ashlaw, calcalist, TheMarker | Hub (ownership tool) |
| 2.6 Seller type | private seller | — | — | (default) |
| | developer | מקבלן (AC) | elkayamlaw, gov.il | /projects/; /developers/ |
| | receiver / execution office | מכונס נכסים · מהוצאה לפועל · כונס נכסים איך זה עובד (AC, REL) | kones2, prlaw, nadlancenter, gelberglaw, amitvered | Hub (process + risks) |
| | heirs | קניית דירה בירושה | seller-side pages | Hub FAQ |
| | foreign-resident seller | — | none | Hub FAQ (withholding) |
| | Amidar / public housing | מעמידר · של עמידר (AC) | gov.il, amidar | Hub FAQ |
| | key money | דמי מפתח (AC) | not searched | Hub FAQ |
| | through a friend, no broker | דרך חבר · ללא תיווך (AC) | — | Hub line |

## 3. Checks
| Node | Leaf | Phrasings | Who ranks | nad-lan owner |
|---|---|---|---|---|
| 3.1 Title (legal) | land-registry extract | נסח טאבו (AI) · בדיקת רישום בטאבו חינם (REL) | — | /tabu-extract-check/ |
| | not registered / housing company / ILA | שלא רשומה בטאבו · ללא טאבו (AC) · דירה רשומה במנהל · חברה משכנת (REL) | yonilevy, luach-nadlan, doron-aharoni, gelberglaw, shovalilaw | Hub (tabu-status tool) |
| | no parcellation | ללא פרצלציה (AC) | not searched | Hub |
| | condominium file and plan | AI: "תשריט ותקנון הבית המשותף" | ygoldlaw, prlaw | /real-estate-lawyer/condo-documents/ |
| | liens, attachments, warning notes | עיקולים, שעבודים (AI) | ygoldlaw | /tabu-extract-check/ |
| | seller identity and capacity | AI: "זהות המוכר… מצבו המשפחתי… ייפוי כוח" | ygoldlaw | Hub line |
| | tenant in place | AI: "שוכרים עם חוזה מוגן או רגיל" | prlaw | Hub FAQ |
| 3.2 Planning | permit vs reality, deviations | עם חריגות בנייה · איך בודקים חריגות בניה · אישור עירייה לטאבו חריגות בנייה (AC, REL) | eliavlaw, yasmint-law, lb-arc, partouche | /real-estate-lawyer/building-permit-citizen-guide/; risk score → Hub tool |
| | building rights | — | — | /property-value/building-rights-check/ |
| | Form 4 | לפני טופס 4 · ללא טופס 4 (AC) | not searched | /real-estate-lawyer/form-4-occupancy-permit/ |
| | betterment levy | היטל השבחה (AI) | — | /real-estate-tax-advisor/betterment-levy/ |
| 3.3 Engineering | home inspection | בדק בית (AI) | laad-eng | /home-inspection/ |
| | asbestos, soil, hazards | — | — | /asbestos/; /environmental-hazards/ |
| | building age and systems | AI: "לחץ מים, חשמל, מיזוג… רטיבות או עובש" | ygoldlaw | /construction-engineering-guide/; Hub visit scorecard |
| 3.4 Building and neighbours | debts (arnona, water, committee) | AI: "בדיקת חובות קודמים (ארנונה, מים, היטל השבחה וועד בית)" | AI only | Hub (who-pays-what) |
| | neighbours and house committee | AI: "מצב ועד הבית" | yonilevy | Hub (visit scorecard) |
| 3.5 Urban renewal | status of the building | — | — | /urban-renewal/check/; /urban-renewal/map/ |
| | buy before pinui-binui | לפני פינוי בינוי (AC) | — | /urban-renewal/pinui-binui/ |
| 3.6 Developer | licence, class, register | AI: "בדיקת רישיון הקבלן, הסיווג" · פנקס רשם הקבלנים (gov.il link) | gov.il, Madlan tips | /developers/ (developer pages); Hub (developer card) |
| | financial strength, bank accompaniment | AI: "ליווי בנקאי סגור" | yasmint-law, tw-law | Hub (developer card) |
| | registration track record | "חברות קבלניות סרבניות רישום" (gov.il link) | gov.il | Hub (developer card) |
| | previous projects, residents | AI: "לבקר בפרויקטים קודמים ולשוחח עם דיירים" | yasmint-law | Hub (developer card) |
| 3.7 Price | is the price right | הערכת שווי (first pass) | yadata, Madlan | /property-value-estimator/ |
| | sold prices nearby | מחירי דירות שנמכרו (first pass) | nadlan.gov.il | /apartment-prices/ |

## 4. The deal
| Node | Leaf | Phrasings | Who ranks | nad-lan owner |
|---|---|---|---|---|
| 4.1 Negotiation | second-hand offer | הצעת מחיר לרכישת דירה (REL) · משא ומתן לרכישת דירה יד שניה (swslaw title) | swslaw | Hub (offer helper) |
| | developer haggling | איך להתמקח על מחיר דירה מקבלן (REL) | not opened | /buying-new-apartment-developer-2026-negotiation/ |
| 4.2 Before the contract | memorandum | זכרון דברים (AC) · "אין לחתום על זיכרון דברים" (AI on 6 searches) | ygoldlaw, sgdlawyer | /real-estate-lawyer/apartment-memorandum/ |
| | developer registration form | טופס הרשמה לרכישת דירה מקבלן · טופס בקשת רכישה (REL) | yonilevy, rmslaw, law-nadlan | Hub (form risk check) |
| | option period | — | — | /real-estate-lawyer/option-period-real-estate/ |
| 4.3 Contract | second-hand contract | חוזה קניית דירה יד שניה · חוזה קניית דירה סטנדרטי (AC, REL) | doron-aharoni, toledano, garnai, prlaw, limorarbel | /real-estate-lawyer/apartment-sale-contract/ |
| | sample contract download | הסכם מכר דירה להורדה · pdf · doc · חוזה מכר לדוגמא (REL) | toledano | link only (no sample contract from us; a lawyer's job) |
| | developer contract and changes annex | חוזה קניית דירה מקבלן · הסכם רכישת דירה מקבלן (AC, REL) | yonilevy, kolodnylaw, doron-aharoni, gelberglaw | /real-estate-lawyer/sale-of-apartments-law/ + Hub (clause list) |
| | cancelling after signing | ביטול חוזה קניית דירה אחרי חתימה · ביטול רכישת דירה מקבלן (AC) | not searched | /real-estate-lawyer/breach-apartment-sale-contract/ |
| | combination deal | — | — | /real-estate-lawyer/combination-deal/ |
| 4.4 Signing day | what to bring, power of attorney | חתימת חוזה קניית דירה (REL) · "לגזור ולשמור! מה להביא ליום החתימה?" (Elkayam H3) | elkayamlaw | /real-estate-lawyer/power-of-attorney-real-estate/ + Hub (signing kit) |
| 4.5 Securities and money flow | trust and warning note | "התשלום הראשון (10%–15%) מופקד בנאמנות עד לרישום הערת אזהרה" (AI) | amitvered, limorarbel | Hub (payment builder) |
| | seller's mortgage release | AI: "סילוק משכנתת המוכרים מול מכתב כוונות" | prlaw | Hub |
| | section 15 capital-gains withholding | — (ygoldlaw body) | ygoldlaw | Hub (who-pays-what) |
| 4.6 Reporting | purchase-tax declaration | דיווח רכישת דירה · אישור רכישת דירה (AC) | not searched | Hub (deadline tool) → /purchase-tax-calculator/ |
| | warning-note form | טופס בקשה לרישום הערת אזהרה · לביטול הערת אזהרה לפי סעיף 126 (REL) | gov.il forms | Hub line (official form link) |

## 5. After the deal
| Node | Leaf | Phrasings | Who ranks | nad-lan owner |
|---|---|---|---|---|
| 5.1 Possession | handover protocol | פרוטוקול מסירה pdf (REL) · "פרוטוקול מסירה, קריאת מוני חשמל, מים וגז" (AI) | elkayamlaw | /guides/remote-new-apartment-handover-israel/; /guides/common-property-handover/; Hub (protocol builder) |
| | developer delay | "איחור במסירה מעבר ל-60 יום" (AI) | elkayamlaw | /new-projects/contractor-delay-compensation/ |
| 5.2 Defects | warranty periods and claims | מהי האחריות של קבלן על דירה לפי חוק המכר? (PAA) | — | /real-estate-lawyer/construction-defects-lawsuit/; bedek.json |
| | buyer changes | שינויי דיירים (Elkayam H3) | elkayamlaw | /guides/new-apartment-buyer-changes/ |
| 5.3 Registration | registering in the land registry | איך רושמים דירה בטאבו · מי עושה רישום בטאבו? (REL, PAA) · מתי רושמים את הדירה בטאבו? (Elkayam H3) | not opened | Hub section (rishum.json covers mortgage registration fees) |
| | housing company to tabu | חברה משכנת (REL) | shovalilaw | Hub (tabu-status tool) |
| 5.4 Running costs | arnona, committee, insurance | ארנונה | — | /arnona/; /mortgage-home-insurance/ |
| 5.5 Moving in | moving checklist | מה צריך לקנות כשעוברים דירה (AC) | not searched | Hub (moving checklist) |
| 5.6 Selling later | capital gains on a new flat | מתי אפשר למכור את הדירה? מס שבח (Elkayam H3) · מס שבח דירה על הנייר (REL) | elkayamlaw | /real-estate-tax-advisor/capital-gains-tax-guide/ |

## 6. Feelings and family (what people type when they are worried)
| Node | Leaf | Phrasings | Treatment |
|---|---|---|---|
| 6.1 Fear | being cheated | איך לקנות דירה בלי לצאת פראייר (AC) · "כבדהו וחשדהו – הבטחות של אנשי מכירות" (Elkayam H3) | the opening paragraph and the red-flag check |
| | drowning in debt | איך לקנות דירה ולהישאר בחיים (AC) · "החזר חודשי כבד" (AI) | the readiness tool shows the monthly payment against income |
| | buying at the top / a crash | "מה שקורה עכשיו זו רק תחילת המפולת" (TheMarker title) | link the prices hub; no forecast |
| | pressure to close fast | "רצון 'לסגור מהר'… מחשש לפספס הזדמנות" (Yoni Levy "טיפ זהב") | a "slow down" line before the memorandum stage |
| 6.2 Family | parents' money and fairness between siblings | משכון דירה של ההורים · "איך אפשר לקנות דירות לכל ילד?" (a Facebook post title) | the equity tool lists the parents' lien and its risk; an FAQ on gift vs loan |
| | couple and marriage | לפני החתונה · על שם אחד מבני הזוג · ידועים בציבור (AC) | the ownership tool |
| | children | על שם הילד / קטין (AC) | the ownership tool |
| | disability in the family | לילד נכה · נכות כללית (AC, REL) | the benefits finder |
| 6.3 Belief and luck | calendar and blessings | בספירת העומר · בשלושת השבועות · סגולה לקנות דירה (AC) | one respectful FAQ: the law and the bank do not care about the date; the deadlines do |
| 6.4 Security | war | האם כדאי למכור דירה בזמן מלחמה (REL) | FAQ + safe-room guide link |

---

## Coverage count
- **Leaves:** 147 rows in the tree (branch 0: 10 · money: 46 · choices: 32 · checks: 24 · deal: 16 · after: 9 · feelings: 10).
- **With a nad-lan owner page:** 72 (the hub links them and never competes).
- **Hub-only (no owner):** 74, of which the 10 "feelings" rows are treatments inside other sections. They fall into six clusters, which become the hub's sections and tools: **(1) no or low equity, (2) government help and eligibility, (3) ownership structure, (4) seller and status special cases (receiver, heirs, no tabu, deviations, Amidar, foreign seller), (5) developer-deal mechanics (registration form, payment caps, 20/80, developer card), (6) the human layer (visit scorecard, signing kit, moving, fears and family).**
- **Out of scope:** 1 row (buying abroad; Cyprus belongs to cy-prus.co.il), covering about 18 countries seen in autocomplete.
- **Overlap finding for the owner (no action proposed):** /buy-vs-rent/ and /buy-or-rent/ serve the same intent.
