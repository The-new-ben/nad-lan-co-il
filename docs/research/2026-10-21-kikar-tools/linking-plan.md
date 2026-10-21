# Tool pages: footer and in-content linking plan (21.10.2026)

Research and plan only. Nothing on the site was changed, nothing committed. Owner order (Ben): link the six tools that went live on 21.10.2026 from the site footer and from the related pages, without pages clashing. No 301, no noindex, no deletion is proposed anywhere.

**Inputs:** gsc: sc-domain:nad-lan.co.il, 2026-07-21..2026-10-19, query+page (9,545 rows) and page (3,400 rows), pulled 21.10.2026 ~19:10 UTC with tools/gsc_api.py; sitemap: https://nad-lan.co.il/sitemap_index.xml (post 17, page 453, glossary 144); rest: /wp-json/wp/v2/pages|posts|nadlan_term (ids, titles, content.rendered of 82 candidate pages), /wp-json/wp/v2/search; live_html: /, /en/, /fr/, the six tool pages and 9 other templates, 21.10.2026; live_version: nadlan-config 1.72.485 (/wp-json/nadlan/v1/health).

## A. Footer

| Question | Answer |
|---|---|
| Where it lives | `themes/nadlan-platform-child/parts/footer.html (block-theme part "footer", one wp:html block; nav.nlpc-footer-links = lines 14-36, three <div> columns)`. https://nad-lan.co.il/wp-content/themes/nadlan-platform-child/parts/footer.html fetched 21.10.2026: identical to the repo file except line endings (live LF, local checkout CRLF). |
| What else touches it | Legal links: `plugins/nadlan-config/inc/legal-links.php, render_block filter lines 14-26 (adds span.nlpc-footer-legal into div.nlpc-footer-bottom); its CSS is the wp_head style#nadlan-legal-links, lines 28-30`. Labels on language pages: plugins/nadlan-config/inc/lang-pages.php output pass (exact Hebrew strings) with plugins/nadlan-config/i18n/lang-pages.json (built by scripts/i18n/build_lang_pages.py) + nadlan_i18n_theme_map() in plugins/nadlan-config/inc/i18n.php:326. Hrefs are never changed, only labels. |
| CSS | `themes/nadlan-platform-child/assets/css/platform.css:238-242 .nlpc-footer-links{grid-template-columns:repeat(3,minmax(0,1fr))}; :420 one column under max-width 760px` |
| Columns today | **פרויקטים**: כל הפרויקטים, Ashira Sde Dov, Rainbow Tel Aviv, Dimri Yama. **בדיקה לפני קנייה**: מחשבון משכנתא, מס רכישה, מדריך קנייה, בדיקה משפטית. **מערכת NadLan**: אנשי מקצוע, רובע שדה דב, אודות, צור קשר. Bottom line: © 2026 NadLan, terms, privacy, accessibility statement, disclaimer. |
| Calculators linked today | 2: /mortgage-calculator/ and /purchase-tax-calculator/. Not linked: home value, total cost, arnona, non-resident mortgage, affordability. |
| Same on every page and language? | Yes, one part on every template that prints a footer (checked he home, /en/, /fr/, tool pages, project he + /projects/hamedina-en/, glossary term, /professionals/, a broker page, English guides). Tours (/tour/sde-dov/) print no footer. On /en/ /fr/ /ru/ /ar/ pages and project language pages the labels are translated; English root posts (/israel-mortgage-non-residents/, /luxury-apartments-israel-guide/) show the HEBREW footer. |
| Homepage extra | plugins/nadlan-config/inc/home-v2.php:1005 section.nlhv2-mfoot (homepage mega-footer) already has a "מחשבונים ומדריכים" column with mortgage, purchase tax, total cost, home value. Not part of this edit. |

**Recommended edit point**

- File: `plugins/nadlan-config/inc/legal-links.php`, after line 26 (the end of the existing render_block filter), before the wp_head style.
- What: a second render_block filter, same pattern: return unchanged unless the HTML contains class="nlpc-footer-links" and does not yet contain nlpc-footer-tools; language = nadlan_plang_suffix() if not empty, else nadlan_current_lang(); "he" -> Hebrew column, "en" -> English column, fr/ru/ar -> no column for now; insert `<div class="nlpc-footer-tools">...</div>` just before the first `</nav>` after `nlpc-footer-links` (preg_replace, limit 1, fail open on null).
- CSS: `append to style#nadlan-legal-links: @media (min-width:761px){.nlpc-footer-links{grid-template-columns:repeat(4,minmax(0,1fr))}} @media (max-width:760px){.nlpc-footer-tools{grid-template-columns:1fr 1fr}.nlpc-footer-tools strong{grid-column:1/-1}}`
- Why not the theme file: A new `<div>` in parts/footer.html (after line 28) would reach /en/ pages as translated labels on Hebrew-only calculators, could not carry the English-only non-resident tool, would need 9 new strings x 4 languages in lang-pages.json, and needs a theme-file swap. The filter also survives a possible database copy of the footer part.
- Release checks: php -l; source_audit.py before/after on /, /en/, /purchase-tax-calculator/, /arnona/, /projects/rainbow-tel-aviv/, /projects/h-infinity/ (or the fleet controls in use); eyes on desktop and 390px; no other footer link removed (additive law).
- Scope: this is the one sitewide change Ben asked for. The footer reuses the existing footer styles; if the design-first rule (Claude Design before any page change) applies to a new column, run it before release.

| Hebrew pages: «מחשבונים וכלים» | URL |
|---|---|
| מחשבון שווי דירה | /property-value-estimator/ |
| מחשבון מס רכישה | /purchase-tax-calculator/ |
| עלות רכישה כוללת | /apartment-purchase-cost-calculator/ |
| כושר החזר משכנתא | /mortgage-calculator/mortgage-repayment-capacity/ |
| מחשבון ארנונה תל אביב | /arnona/ |
| ריבית משכנתא ופריים | /mortgage-calculator/mortgage-interest-rates/ |
| מחשבון הצמדה למדד | /cpi-calculator/ |
| מדד תשומות הבנייה | /new-projects/construction-input-index/ |

The purchase-tax link also stays in "בדיקה לפני קנייה" (additive law: nothing is removed).

| English pages: «Tools» | URL |
|---|---|
| Mortgage calculator for non-residents | /israel-mortgage-non-residents/ |
| Purchase tax for foreign residents | /israel-purchase-tax-foreign-residents/ |
| Buying property from abroad | /en/buy-property-in-israel/ |

Only the non-resident page is a calculator in English; the Hebrew calculators have no English version yet, so they are not sent to English readers. fr/ru/ar pages get no new column until there is something in those languages to link (Ben can decide otherwise).

## B. In-content links (41 lines on 35 pages, at most 2 per page)

Rule used: only pages that do NOT link the tool yet (checked in content.rendered of 82 candidate pages); the line goes right after the named paragraph, in the page body (not in a "related" block); anchors are plain Hebrew, no slogans, no long dash, no banned language-DNA words. "impr" = Search Console impressions of the source page, 21.7-19.10.2026.

### Affordability: /mortgage-calculator/mortgage-repayment-capacity/ (id 519) - 8 links

| From (id, type, impr) | After | Sentence (anchor in bold) | Note |
|---|---|---|---|
| /mortgage-calculator/ (121, page, 8302) | H2 "מהו יחס החזר מהכנסה?" > after the paragraph that starts "יחס החזר מהכנסה הוא החלק מההכנסה החודשית" | כדי לבדוק **כמה משכנתא אפשר לקחת לפי ההכנסה**, ואיזה מחיר דירה זה מאפשר, עברו למחשבון כושר ההחזר. | OVERLAP FIX: this page holds "כמה משכנתא אפשר לקחת" (287 impr, pos 64.4) and "כושר החזר משכנתא" (53, pos 52.6). It already links the tool once, under "מדריכים חדשים"; this adds the in-body link with the head phrase. |
| /buying-apartment/ (9, page, 1382) | H2 "משכנתא ואישור עקרוני" > after the paragraph that starts "רוכשים רבים מתחילים לראות דירות ורק אחר כך בודקים משכנתא" | את טווח המחיר הזה, לפי ההכנסה וההון העצמי, אפשר לחשב ב**מחשבון כושר החזר: איזו דירה אפשר לקנות**. | 1,382 impr. Already links pval, ptax and pcost. |
| /investment-property-mortgage/ (114, page, 659) | H2 "מה הבנק בודק לפני אישור משכנתא להשקעה?" > after the paragraph that starts "הבנק בודק הכנסה, התחייבויות, היסטוריית אשראי" | לבדיקה ראשונה של המחיר שאפשר לממן לפי ההכנסה, עם מימון של עד 50% בדירה להשקעה, היעזרו ב**מחשבון כושר החזר**. | 659 impr. Second link on this page (with pcost). |
| /new-projects/ (17, page, 160) | H3 "שלב 1: מגדירים תקציב ותאריך" > after the paragraph that starts "חשבו הון עצמי נזיל, הכנסה פנויה, התחייבויות" | כמה דירה ההכנסה וההון העצמי שלכם מאפשרים, אפשר לבדוק ב**מחשבון כושר החזר משכנתא**. | /new-projects/ is the big guide (160 impr); it links only ptax today. Second link on this page (with pcost). |
| /mortgage-calculator/mortgage-ltv-ratio/ (513, page, 80) | H3 "האם אפשר לקבל יותר מהמימון המרבי אם יש הכנסה גבוהה?" > after the paragraph that starts "הכנסה גבוהה יכולה לשפר את סיכויי האישור" | מה ההכנסה שלכם מאפשרת בתוך התקרה הזאת, אפשר לבדוק ב**מחשבון כושר החזר משכנתא**. | Second link on this page (with pcost). |
| /mortgage-calculator/mortgage-interest-rates/ (514, page, 110) | H2 "מה משפיע על הריבית שתקבלו" > after the paragraph that starts "גם יחס ההחזר משפיע על המחיר" | כמה משכנתא ההכנסה שלכם מאפשרת לפי מגבלת ההחזר של בנק ישראל, בדקו ב**מחשבון כושר החזר**. |  |
| /new-projects/presale-apartment/ (4445, page, 112) | H3 "מה קורה אם לא אקבל משכנתא בעתיד?" > after the paragraph that starts "החוזה מול הקבלן אינו מתבטל אוטומטית" | לפני שחותמים על 20/80, בדקו לפי ההכנסה של היום ב**מחשבון כושר החזר** אם המשכנתא שתידרש במסירה אפשרית. | Second link on this page (with ptax). |
| /glossary/payment-to-income-ratio/ (1508, nadlan_term, 1) | H2 "מה זה אומר בפועל" > after the paragraph that starts "בפועל, יחס החזר חודשי מתרגם את שאלת המשכנתא" | איזה מחיר דירה מתאים להכנסה שלכם כשההחזר נשאר עד 50% ממנה, אפשר לבדוק ב**מחשבון כושר החזר משכנתא**. | Glossary term "יחס החזר חודשי": the exact concept, few impressions. |

### Home value: /property-value-estimator/ (id 129) - 8 links

| From (id, type, impr) | After | Sentence (anchor in bold) | Note |
|---|---|---|---|
| /selling-apartment/pricing-apartment-for-sale/ (567, page, 13) | H2 "כלים אונליין להערכת שווי ומאגר רשות המסים" > after the paragraph that starts "כלים אונליין יכולים לעזור למוכר לקבל נקודת פתיחה לתמחור" | כדי לראות את המחיר החציוני של דירות דומות בשכונה לפי נתוני רשות המסים, התחילו ב**מחשבון שווי דירה** והשוו אותו למחיר שאתם שוקלים לבקש. | The section names outside tools (yadata, dirobot) and not ours; the page does not link the tool today. |
| /new-projects/new-projects-tel-aviv/ (4484, page, 1036) | H3 "איך בודקים אם מחיר הפרויקט סביר?" > after the paragraph that starts "משווים מחיר למ"ר, עסקאות רשות המסים" | להשוואה מהירה מול דירות יד שנייה באותה שכונה, בדקו את המחיר החציוני לפי חדרים ב**מחשבון שווי דירה**. | 1,036 impr. Second link on this page (with pcost). |
| /investment-apartment/tel-aviv-investment-neighborhoods/ (4489, page, 312) | H3 "איך בודקים מחיר למ"ר בתל אביב לפי שכונה?" > after the paragraph that starts "משווים לפחות 8 עד 12 עסקאות דומות" | נקודת פתיחה טובה היא החציון הרשמי לפי מספר חדרים בשכונה, שמופיע ב**מחשבון שווי דירה**. | 312 impr. |
| /investment/ (421, page, 6864) | H2 "איפה כדאי להשקיע בישראל 2026 לפי נתוני עסקאות" > after the paragraph that starts "השאלה איפה כדאי להשקיע בישראל היא שאלה מורכבת" | לפני שבוחרים עיר, כדאי לבדוק את המחיר החציוני של דירות דומות בשכונה עצמה ב**מחשבון שווי דירה**, לפי נתוני רשות המסים. | 6,864 impr (pillar); it ranks for "עסקאות נדלן" phrases at pos 50-64. |
| /north-tel-aviv/ (4866, page, 62) | H2 "מחירים לפי שכונה" > after the paragraph that starts "מחירי הדירות בצפון תל אביב אינם אחידים" | כדי לבדוק כמה שווה דירה מסוימת בצפון תל אביב לפי העסקאות שנסגרו בשכונה שלה, היעזרו ב**מחשבון שווי דירה**. |  |
| /ramat-aviv/neve-avivim/ (4871, page, 128) | H2 "מחירים בשכונה" > after the paragraph that starts "רוכש שבוחן דירה בנווה אביבים צריך להפריד בין מחיר מבוקש לבין שווי כלכלי" | את השווי לפי עסקאות שנסגרו בנווה אביבים אפשר לבדוק ב**מחשבון שווי דירה**, ואז להשוות למחיר המבוקש. | Second link on this page (with arnona). |
| /glossary/shamai-pinui-binui/ (5456, nadlan_term, 201) | (the definition paragraph, the only one) > after the paragraph that starts "שמאי מקרקעין שבוחן את הכדאיות הכלכלית של עסקת התחדשות" | לפני הפגישה עם השמאי, אפשר לבדוק את שווי הדירה הנוכחית לפי עסקאות בשכונה ב**מחשבון שווי דירה**. | Glossary term with 201 impr on appraiser queries; very short body. |
| /glossary/שווי-שוק/ (5225, nadlan_term, 0) | H3 "ההקשר הישראלי" > after the paragraph that starts "בישראל, שווי השוק משחק תפקיד מרכזי בשוק הנדל"ן" | לאומדן ראשון של שווי שוק לפי עסקאות שנסגרו בשכונה, ראו את **מחשבון שווי דירה**. הוא אינו מחליף שמאי מוסמך. | Glossary "שווי שוק": the definition page, no impressions yet. |

### Purchase tax: /purchase-tax-calculator/ (id 6) - 4 links

| From (id, type, impr) | After | Sentence (anchor in bold) | Note |
|---|---|---|---|
| /real-estate-tax-advisor/gift-transfer-apartment/ (4431, page, 52) | H2 "מס רכישה למקבל המתנה - שליש מס, דירה יחידה ודירה נוספת" > after the paragraph that starts "מס רכישה בעסקת מתנה מוטל על מקבל הדירה" | את המס המלא שממנו נגזר החישוב אפשר לבדוק לפי שווי הדירה ב**מחשבון מס רכישה**; ההקלה בהעברה לקרוב נבדקת לפי תקנה 20, כפי שמוסבר כאן. | OVERLAP: "חישוב מס רכישה בהעברה ללא תמורה" (65 impr, pos 74.5) lands on the calculator, which has no gift track. The guide keeps the gift intent; the link sends only the full-tax step to the tool. |
| /new-projects/presale-apartment/ (4445, page, 112) | H3 "מה לבדוק במס רכישה?" > after the paragraph that starts "מס רכישה נקבע לפי מצב הרוכש, מספר הדירות" | את המס לפי המסלול שלכם, דירה יחידה, דירה נוספת, עולה חדש או תושב חוץ, אפשר לחשב ב**מחשבון מס רכישה**. | 112 impr. |
| /new-projects/purchasing-group/ (4443, page, 62) | H2 "מיסוי בקבוצת רכישה: מס רכישה, מע"מ ודיווחים" > after the paragraph that starts "מס רכישה יכול להיקבע לפי מדרגות דירת מגורים" | להערכה ראשונה של מס הרכישה לפי מדרגות רשות המסים, היעזרו ב**מחשבון מס רכישה**. |  |
| /sde-dov/prices/ (4758, page, 1596) | H2 "הזווית המשפטית והמיסויית" > after the paragraph that starts "מס רכישה הוא רכיב מרכזי, במיוחד כאשר מחיר הדירה גבוה" | בדירה בשדה דב גם הבדל קטן במסלול משנה סכום גדול, ולכן כדאי לחשב את המס במסלול שלכם ב**מחשבון מס רכישה**. | 1,596 impr; the page links pcost only. |

### Total purchase cost: /apartment-purchase-cost-calculator/ (id 125) - 8 links

| From (id, type, impr) | After | Sentence (anchor in bold) | Note |
|---|---|---|---|
| /new-projects/new-projects-tel-aviv/ (4484, page, 1036) | H2 "מחיר דירה חדשה בתל אביב: חדרים, מטר, הצמדה ותשלומים" > after the paragraph that starts "מחיר דירה חדשה בתל אביב מורכב מיותר מהמספר שמופיע בפרסום" | כמה כסף צריך בפועל מעבר למחיר החוזה, אפשר לחשב ב**מחשבון עלות רכישה כוללת**. | 1,036 impr. Second link on this page (with pval). |
| /investment-property-mortgage/ (114, page, 659) | H2 "כמה הון עצמי צריך להכין?" > after the paragraph that starts "בדירה להשקעה לא מספיק לחשב את ההפרש" | לחישוב ההון העצמי האמיתי בדירה להשקעה, עם מס רכישה של דירה נוספת ומימון של עד 50%, היעזרו ב**מחשבון עלות רכישה כוללת**. | 659 impr. |
| /michraz-dirot/ (5830, page, 347) | H3 "6. מסים ועלויות נלוות" > after the paragraph that starts "מחיר הזכייה אינו התקציב הכולל" | את התקציב הכולל, עם מס רכישה, עורך דין, שמאי ומעבר, אפשר לחשב ב**מחשבון עלות רכישה כוללת**. | 347 impr. |
| /selling-apartment/who-pays-broker-fees/ (565, page, 160) | H2 "מה הם דמי תיווך וכמה נהוג לשלם" > after the paragraph that starts "כאשר מדברים על 2%, הכוונה היא בדרך כלל לשיעור" | לקונה, דמי התיווך הם חלק אחד מעלות הקנייה; את כל ההוצאות יחד, עם מס רכישה ועורך דין, אפשר לחשב ב**מחשבון עלות רכישה כוללת**. | 160 impr. |
| /new-projects/ (17, page, 160) | H3 "כמה הון עצמי צריך לדירה מקבלן" > after the paragraph that starts "אין מחשבים הון עצמי רק כאחוז ממחיר החוזה" | את ההפרש הזה בין העלות הכוללת למימון אפשר לחשב ב**מחשבון עלות רכישה כוללת**. | 160 impr. |
| /mortgage-calculator/mortgage-ltv-ratio/ (513, page, 80) | H2 "ההון העצמי הנדרש בכל מדרגה" > after the paragraph that starts "יש להבחין בין הון עצמי מינימלי לצורך עמידה בכללי המימון" | כמה הון עצמי אמיתי תצטרכו אחרי מס רכישה, עורך דין ותיווך, אפשר לבדוק ב**מחשבון עלות רכישה כוללת**. | 80 impr. |
| /real-estate-tax-advisor/purchase-tax-first-home/ (529, page, 26) | H2 "מהו מס רכישה ומתי משלמים אותו" > after the paragraph that starts "מועד התשלום בפועל תלוי בהליכי הדיווח והשומה" | כדי לראות את מס הרכישה לצד שאר העלויות, עורך דין, תיווך, שמאי ומעבר, השתמשו ב**מחשבון עלות רכישה כוללת**. |  |
| /apartment-buying-checklist/ (8, page, 9) | H2 "בדיקת תקציב ועלות כוללת" > after the paragraph that starts "הבדיקה הכספית מתחילה במחיר הדירה" | את כל ההוצאות האלה ביחד, וגם את ההון העצמי שנשאר אחרי המשכנתא, אפשר לחשב ב**מחשבון עלות רכישה כוללת**. | The section already has a link "בדיקת מס רכישה ועלויות עסקה" that goes to the purchase-tax tool. |

### Tel Aviv arnona: /arnona/ (id 8517) - 8 links

| From (id, type, impr) | After | Sentence (anchor in bold) | Note |
|---|---|---|---|
| /sde-dov/ (4730, page, 5349) | H2 "השקעה בשדה דב: יתרונות, סיכונים ומה לבדוק" > after the paragraph that starts "בדיקת השקעה נכונה בשדה דב צריכה לכלול" | לאומדן הארנונה הצפויה לפי שטח הדירה והמרפסות, היעזרו ב**מחשבון ארנונה תל אביב**. | 5,349 impr, the top content page: source audit before and after. Name no zone or class for Sde Dov until the order confirms it. |
| /tel-aviv-apartment-prices/ (135, page, 233) | H2 "מה משפיע במיוחד על מחירי דירות בתל אביב?" > after the paragraph that starts "לבסוף, צריך להסתכל על עלויות החזקה" | את הארנונה לדירה מסוימת בתל אביב אפשר לחשב ב**מחשבון ארנונה תל אביב**, לפי האזור ושטח הדירה. | 233 impr. |
| /luxury-apartments-israel-guide-he/ (5118, post, 103) | H3 "עלויות האחזקה השוטפות: ארנונה, ועד בית וניהול" > after the paragraph that starts "מחיר הכניסה הוא רק ההתחלה" | בדירה בתל אביב אפשר לחשב את הארנונה השנתית והדו־חודשית לפי צו הארנונה של העירייה ב**מחשבון ארנונה תל אביב**. | 103 impr. |
| /urban-renewal/pinui-binui-tel-aviv/ (4599, page, 97) | H3 "האם יש הנחה בארנונה אחרי קבלת הדירה החדשה?" > after the paragraph that starts "עיריית תל אביב-יפו פרסמה מידע על הנחות בארנונה" | כמה תהיה הארנונה על הדירה החדשה לפי האזור, השטח והמרפסות, אפשר לבדוק ב**מחשבון ארנונה תל אביב 2026**. | 97 impr. |
| /ramat-aviv/neve-avivim/ (4871, page, 128) | H2 "למי מתאימה השכונה" > after the paragraph that starts "לא כל רוכש ימצא בנווה אביבים את אותה הזדמנות" | משקיע שבודק תשואה נטו בנווה אביבים יכול לחשב את הארנונה לדירה ב**מחשבון ארנונה תל אביב**. | 128 impr. |
| /tel-aviv-penthouse-prices/ (250, page, 87) | H2 "איך קונה צריך לנתח מחיר פנטהאוז?" > after the paragraph that starts "לאחר ההשוואה צריך לחשב עלות כוללת" | בפנטהאוז עם מרפסות גדולות כדאי לחשב את הארנונה מראש ב**מחשבון ארנונה תל אביב**. | 87 impr. |
| /tel-aviv-luxury-apartment-prices/ (234, page, 30) | H2 "איך קונה צריך לנתח מחיר בדירת יוקרה?" > after the paragraph that starts "לאחר ההשוואה צריך לחשב עלות כוללת" | את רכיב הארנונה אפשר לחשב מראש ב**מחשבון ארנונה תל אביב**. | 30 impr. |
| /guides/remote-new-apartment-handover-israel/ (6162, page, 14) | H2 "מונים, חשמל, מים, גז, ארנונה וחברת ניהול" > after the paragraph that starts "ארנונה קשורה לרישום המחזיק לפי הליך הרשות" | בדירה בתל אביב אפשר לדעת מראש כמה תשלמו בכל חשבון דו־חודשי ב**מחשבון ארנונה תל אביב**. | 14 impr. |

### Non-resident mortgage (EN): /israel-mortgage-non-residents/ (id 4962) - 5 links

| From (id, type, impr) | After | Sentence (anchor in bold) | Note |
|---|---|---|---|
| /en/buy-property-in-israel/ (5154, page, 711) | H3 "Treat financing as a property-specific dependency" > after the paragraph that starts "When borrowing is necessary, obtain the lender's position" | To see what the 50% non-resident cap means for your budget, with the monthly payment in dollars, euros or pounds, try our **Israeli mortgage calculator for non-residents**. | 711 impr, the biggest English page; it does not link the tool today. |
| /buying-real-estate-israel-foreign-investor/ (4945, post, 103) | H2 "Financing as a non-resident: the 50% mortgage" > after the paragraph that starts "Foreign buyers can borrow from Israeli banks" | You can run these numbers for a specific price, including the foreign-resident purchase tax and closing costs, in our **mortgage calculator for non-residents**. | 103 impr. |
| /investing-israel-real-estate-vs-dubai-cyprus/ (4946, post, 97) | H2 "Foreign buyer mortgages in Israel" > after the paragraph that starts "Financing is where the non-resident rules bite hardest" | Our **Israeli mortgage calculator for non-residents** shows the loan, the monthly payment at the average rate by track and the cash you need to close, in your own currency. | 97 impr. |
| /en/new-projects/ (5974, page, 74) | H3 "Mortgages for non-residents" > after the paragraph that starts "Mortgage availability is buyer-specific" | For a first estimate of the loan and the cash you need for a new-build apartment, use the **mortgage calculator for non-residents**. | 74 impr. |
| /en/developer-deals/ (7215, page, 45) | H2 "What Foreign Buyers Are Really Searching For" > after the paragraph that starts "A person typing "new apartments in Israel for sale"" | If that is your question, the **Israeli mortgage calculator for non-residents** gives a first answer for a specific price before you speak to a bank. | 45 impr. |

Pages already linking a tool were left out on purpose. Examples: every city price page already links home value and total cost from its "מחשבון מחיר דירה ב..." block; /buying-apartment/, /selling-apartment/, /property-value/, /real-estate-appraiser/ already link home value; the purchase-tax tool is already linked from 30+ guides; the five English guides /buy-property-israel-foreign-buyers/, /israel-purchase-tax-foreign-residents/, /affordable-apartments-israel-2026/, /luxury-apartments-israel-guide/, /en/north-tel-aviv/ already link the non-resident page.

## C. Overlap check (same head query)

| Tool | Query | Other page | Its GSC | Tool GSC | Recommendation |
|---|---|---|---|---|---|
| afford | כמה משכנתא אפשר לקחת / כושר החזר משכנתא / כמה משכנתא אפשר לקבל | /mortgage-calculator/ (id 121) | 287 impr pos 64.4 / 53 impr pos 52.6 / 11 impr pos 63.2 | /mortgage-calculator/mortgage-repayment-capacity/ 14 impr total, none on these queries | LINK: in-body link from /mortgage-calculator/ with the anchor "כמה משכנתא אפשר לקחת לפי ההכנסה" (first row of links). Keep the afford page off the words that /mortgage-calculator/ owns: "מחשבון החזר משכנתא" 273, "מחשבון משכנתא לפי החזר חודשי" 289, "מחשבון משכנתא החזר חודשי" 178. |
| ptax | חישוב מס רכישה בהעברה ללא תמורה | /purchase-tax-calculator/ (the tool itself) vs the guide /real-estate-tax-advisor/gift-transfer-apartment/ (id 4431) | tool 65 impr pos 74.5; guide 52 impr total, 0 on this query | the tool has four tracks (single home, additional home, new immigrant, foreign resident), no gift track | LINK from the guide to the tool (gift row). The guide keeps the gift intent; do not claim a gift track in the tool. |
| pcost | מחשבון קניית דירה | /buy-or-rent/ 117 impr pos 82.2; /mortgage-calculator/ 71 pos 80.8; /purchase-tax-calculator/ 69 pos 67.7; /property-value-estimator/ 18 pos 33.0; /buy-vs-rent/ 2 | see competing_page | /apartment-purchase-cost-calculator/ 142 impr pos 51.1 | LEAVE ALONE: /buy-or-rent/ and /mortgage-calculator/ already link the tool with the anchor "מחשבון קניית דירה"; the purchase-tax tool links it in its related list. |
| pcost | עלויות רכישת דירה מקבלן | /buying-apartment/ (id 9) | 35 impr pos 44.6 | 67 impr pos 61.4 | LEAVE ALONE: /buying-apartment/ already links the tool twice ("מחשבון עלויות רכישת דירה", "עלויות רכישת דירה"). |
| pval | הערכת שווי דירה (head of the tool) | /property-value/ (id 76), title "הערכת שווי דירה: איך בודקים מחיר לפני קנייה או מכירה" | 47 impr total; 0 on the head; "הערכת שווי נכס לפני קניה" 34 pos 42 | 480 impr pos 20.6 on the head; 6,344 impr page total | LEAVE ALONE: Google already picks the tool, and the guide links it twice. |
| ptax | מחשבון מס רכישה דירה ראשונה | /real-estate-tax-advisor/purchase-tax-first-home/ (id 529) | 26 impr total, single-impression rows only | 95 impr pos 53.2 | LEAVE ALONE: guide vs calculator intent; the guide already links the tool twice. |
| arnona | ארנונה תל אביב / מחשבון ארנונה | none. Only commercial pages touch business arnona: /commercial-real-estate/shop-prices-tel-aviv/ ("הנחת ארנונה על מרתפים בתל אביב" 2 impr pos 7.5), /commercial-real-estate/commercial-property-management-fees/ (5 impr) | no rows for the head queries | /arnona/ has no GSC rows yet (published 21.10.2026) | LEAVE the commercial pages alone and do not link them to /arnona/ (the tool is residential). |
| nrm | israel mortgage for foreigners / israel mortgage calculator | /mortgage-calculator/ (Hebrew) | "israel mortgage calculator" 7 impr pos 70; "מחשבון משכנתא לעולים" 68 impr pos 58 | "israel mortgage for foreigners" 168 impr pos 64.9; page total 548 impr | LEAVE ALONE: new immigrants are residents (75% cap), not the non-resident tool. |

The only real clash is affordability: /mortgage-calculator/ collects all "how much can I borrow" queries (351 impr) while the page that owns that H1 has 14. The fix is a link with the head phrase, nothing else.

## Pace (owner law: no mass change in one day)

- Owner law 14.10: no sitewide mass change in one day without Ben's OK. 41 hand-written lines on 35 pages, each different, max 2 per page.
- Wave 1, overlap fixes and the pages with most impressions: ids 121, 4431, 9, 421, 4730, 4758, 4484, 114, 5154, 135, 4489.
- Wave 2, the other Hebrew pages: ids 567, 4866, 4871, 4445, 4443, 5830, 565, 17, 513, 529, 8, 514, 5118, 4599, 250, 234, 6162.
- Wave 3, English pages and glossary terms: ids 4945, 4946, 5974, 7215, 1508, 5225, 5456.
- Each wave: source_audit.py snapshot before and after on the touched pages + controls; eyes on one page per tool; Linear HAD-575 + Notion row.

## Findings to report (no action proposed here)

1. English root posts render Hebrew chrome: /israel-mortgage-non-residents/ (id 4962) prints <html dir="rtl" lang="he-IL"> with the Hebrew header and footer; /luxury-apartments-israel-guide/ prints lang="en-US" but the Hebrew footer. The English footer (and the new Tools column) appears only on /en/... pages and -en project pages. Report only; a language signal for root English posts is a separate fix.
2. /mortgage-calculator/ also takes "מחשבון משכנתא הפוכה" (429 impr pos 54.6) while /mortgage-calculator/reverse-mortgage/ exists (296 impr total). Outside the six tools; report only. /buy-or-rent/ vs /buy-vs-rent/ is already waiting for Ben (plan.md).
3. Five guides link the purchase-tax tool with the bare anchor "למחשבון": ids 564, 565, 567, 572, 573. Can be reworded later; not in this plan.
4. The header mega-menu "מחשבונים" (plugins/nadlan-config/inc/home-v3.php:163) and the homepage mega-footer (inc/home-v2.php:1021-1028) list 4 tools, without arnona and affordability. Not asked; report only.
5. Of the 82 pages scanned, none links /arnona/ and only 3 link the affordability page (/mortgage-calculator/, /mortgage-calculator/mortgage-refusal/, /mortgage-calculator/mortgage-pre-approval/). The tool registry inc/instruments.php has no related link to /arnona/ or to the affordability page from the other tools; adding them to the "related" arrays is a small optional code change.

Machine-readable copy: linking-plan.json (footer edit point, the 41 links with from_url, from_id, type, tool_url, after_heading_or_text, anchor_sentence, anchor_text, overlap, findings, pace).
