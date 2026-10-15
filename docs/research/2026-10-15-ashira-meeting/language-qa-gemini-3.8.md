# Editorial QA Audit: ASHIRA Sde Dov (nad-lan.co.il)

---

## 1. Language Evaluations & Concrete Problems

### Hebrew
**Grade: 8/10** — Authentic native industry prose and authoritative local market framing, but degraded by spacing glitches around hyphens/percentages, raw UI artifacts, and internal contradictions.

1. **Inverted Street Name**
   * *Quote:* `באתר הבנייה באשכול לוי 29, 39 מ׳`
   * *Fix:* `באתר הבנייה ברחוב לוי אשכול 29 (39 מ׳)`
2. **Internal Height Contradiction**
   * *Quote:* `מגדלון של 16 ושני בניינים של 9, לפי תכנית העיצוב`
   * *Fix:* `מגדלון של 16 ושני בניינים של 8 קומות, לפי תכנית העיצוב` (matches line 30).
3. **Clunky Word Order & Hyphen Spacing**
   * *Quote:* `נמכרו ב- 2025 31 דירות`
   * *Fix:* `נמכרו 31 דירות בשנת 2025`
4. **Detached Punctuation & Date Notation**
   * *Quote:* `ב- 2025 , כ- 64,500 ₪ למ״ר, לבין ממוצע הרבעון השני של 2026 , כ- 72,000 ₪.`
   * *Fix:* `ב-2025 (כ-64,500 ₪ למ״ר) לבין ממוצע הרבעון השני של 2026 (כ-72,000 ₪).`
5. **Broken Percentage Formatting**
   * *Quote:* `הנחה של 6 %- 8 % מהמחיר הרשום`
   * *Fix:* `הנחה של 6%–8% מהמחיר הנקוב`
6. **Truncated Sentence / UI Artifact**
   * *Quote:* `השיחה היא עם צוות נדל״ן, פלטפורמה עצמאית: היא אינה מטעם היזם ואינה מחליפה`
   * *Fix:* `...ואינה מחליפה את נציגי המכירות של היזם.`
7. **Slangy Shorthand Dates**
   * *Quote:* `עד 7.2026 נמכרו 125 מתוך 406 הדירות, והפנטהאוז בקומה 15 של המגדלון נמכר ב- 8.2024`
   * *Fix:* `עד יולי 2026 נמכרו 125 מתוך 406 הדירות, והפנטהאוז בקומה 15 של המגדלון נמכר באוגוסט 2024`
8. **Incomplete Room Range**
   * *Quote:* `עם דירות בתמהיל של 2 עד 5 חדרים`
   * *Fix:* `עם דירות בתמהיל של 2 עד 6 חדרים ופנטהאוזים`

---

### English
**Grade: 8.5/10** — Sophisticated, high-register UK/Commonwealth advisory English. Excellent due-diligence structure, but contains severe UI bugs, self-referential distance errors, and an overly dissuasive tone.

1. **Self-Referential Distance Bug in Table**
   * *Quote:* `ASHIRA Sde Dov ~75,000 11 m`
   * *Fix:* Remove ASHIRA from the neighboring projects table or label as `Subject Property (0 m)`.
2. **Floor Count Contradiction**
   * *Quote:* `A 16-floor mid-rise and two 9-floor buildings, per the design plan`
   * *Fix:* `A 16-storey mid-rise and two 8-storey buildings, per the approved design plan` (matches line 99).
3. **Overly Dissuasive Advisory Tone**
   * *Quote:* `Walking away is a valid outcome of due diligence.`
   * *Fix:* `Rigorous due diligence ensures buyers commit only when project terms fully align with their criteria.`
4. **Pseudo-Scientific Wellness Calque**
   * *Quote:* `spa with salt room and collagen tanning`
   * *Fix:* `spa with a salt room and collagen light therapy lounge`
5. **Untranslated UI Language Switcher**
   * *Quote:* `עב EN FR RU AR`
   * *Fix:* `HE EN FR RU AR`
6. **Truncated Breadcrumb String**
   * *Quote:* `Home › Projects › ASHIRA Sde Dov - New apartments Tel Aviv: pr…`
   * *Fix:* `Home › Projects › ASHIRA Sde Dov - New apartments Tel Aviv: prices, buildings and buyer guide`
7. **Omission of Disclosed Sales Velocity**
   * *Quote:* `No current official public price list found`
   * *Fix:* `While developer reports show 125 units sold by mid-2026 (~72,000 NIS/m² in Q2 2026), a live public unit inventory remains unpublished.`
8. **Raw Dot-Date UI Artifact**
   * *Quote:* `Each project's status per its page on the site, 9.2026.`
   * *Fix:* `Project status as displayed on site, September 2026.`

---

### French
**Grade: 8.5/10** — Natural, elegant French tailored brilliantly to francophone buyers (comparing Israeli purchases to French VEFA), marred by unaccented UI strings, the 11m table glitch, and a literal wellness calque.

1. **Self-Referential Table Glitch**
   * *Quote:* `ASHIRA Sde Dov ~75,000 11 m`
   * *Fix:* Supprimer ASHIRA du tableau comparatif des projets voisins.
2. **Floor Count Discrepancy**
   * *Quote:* `Une petite tour de 16 étages et deux immeubles de 9 étages, selon le plan d'aménagement`
   * *Fix:* `Un bâtiment intermédiaire de 16 étages et deux immeubles de 8 étages, selon le plan d'aménagement approuvé` (matches line 84).
3. **Nonsensical Wellness Calque**
   * *Quote:* `un espace de bronzage au collagène`
   * *Fix:* `un espace de luminothérapie au collagène` (collagen regenerates skin; it does not tan).
4. **Missing French Accents in Interactive Map UI**
   * *Quote:* `₪ Prix a proximite Education Parcs Transports Commerces Sante Cafes`
   * *Fix:* `₪ Prix à proximité`, `Éducation`, `Santé`, `Cafés`
5. **Untranslated Hebrew UI Tag**
   * *Quote:* `עב EN FR RU AR`
   * *Fix:* `HE EN FR RU AR`
6. **Truncated Breadcrumb**
   * *Quote:* `Accueil › Projets › ASHIRA Sde Dov - appartement neuf Tel Aviv,…`
   * *Fix:* `Accueil › Projets › ASHIRA Sde Dov - appartement neuf Tel Aviv : prix et guide d’achat`
7. **Omission of Developer Disclosures**
   * *Quote:* `Au moment de la recherche, aucune liste officielle, complète et actualisée des prix et disponibilités d’ASHIRA n’a été trouvée`
   * *Fix:* `Bien qu'aucun barème public ne soit diffusé, les rapports financiers indiquent 125 logements vendus à l'été 2026 (~72 000 ₪/m² au T2 2026).`
8. **Raw Numeric Date Notation**
   * *Quote:* `selon le plan d'aménagement (5.2023)`
   * *Fix:* `selon le plan d'aménagement (mai 2023)`

---

### Russian
**Grade: 7.5/10** — Grammatically sound and legally comprehensive, but riddled with literal Hebrew calques, bureaucratic stiffness, and unpolished interface elements.

1. **Self-Referencing Distance Bug**
   * *Quote:* `ASHIRA Sde Dov ~75,000 11 м`
   * *Fix:* Удалить ASHIRA из таблицы соседних проектов.
2. **Height Conflict**
   * *Quote:* `16-этажная малая башня и два 9-этажных здания, по архитектурному плану`
   * *Fix:* `16-этажный корпус и два 8-этажных здания согласно утвержденному плану`
3. **Literal Calque of "Migdalon"**
   * *Quote:* `16-этажная малая башня`
   * *Fix:* `16-этажный корпус` или `корпус средней этажности (16 этажей)`
4. **Machine-Translated Wellness Feature**
   * *Quote:* `коллагеновый солярий`
   * *Fix:* `коллагенарий` или `зал световой коллагенотерапии`
5. **Awkward Legal Calque**
   * *Quote:* `Словарь терминов ТАМА, «Пинуй-Бинуй», предупредительная запись`
   * *Fix:* `...предупредительная запись в Табу (Хеарат Азхара)`
6. **Untranslated Language Switcher**
   * *Quote:* `עב EN FR RU AR`
   * *Fix:* `HE EN FR RU AR`
7. **Truncated Breadcrumb**
   * *Quote:* `Главная › Проекты › ASHIRA Sde Dov - купить квартиру в Тель-Авив…`
   * *Fix:* `Главная › Проекты › ASHIRA Sde Dov - купить квартиру в Тель-Авиве: цены, новостройка и выбор`
8. **Total Price Blind Spot**
   * *Quote:* `Актуального официального полного прайс-листа и списка квартир по состоянию на дату исследования в открытом доступе не найдено.`
   * *Fix:* `По отчетам девелопера, к июлю 2026 года продано 125 квартир из 406 (средняя цена во II кв. 2026 г. — ~72 000 ₪/м²), однако поквартирный прайс-лист не публикуется.`

---

### Arabic
**Grade: 7.5/10** — Professional Modern Standard Arabic syntax, but heavily burdened by direct Hebrew loan-translations, repetitive disclaimers, and UI truncation.

1. **Self-Referencing Distance Bug**
   * *Quote:* `ASHIRA Sde Dov ~75,000 11 م`
   * *Fix:* حذف سطر المشروع من جدول مقارنة المشاريع المجاورة.
2. **Height Contradiction**
   * *Quote:* `برج صغير من 16 طابقاً ومبنيان من 9 طوابق، بحسب مخطط التصميم`
   * *Fix:* `مبنى متوسط من 16 طابقاً ومبنيان من 8 طوابق، بحسب مخطط التصميم المعتمد`
3. **Literal Calque of "Migdalon"**
   * *Quote:* `برج صغير من 16 طابقاً`
   * *Fix:* `مبنى متوسط الارتفاع من 16 طابقاً`
4. **Nonsensical Wellness Translation**
   * *Quote:* `غرفة ملح وتسمير بالكولاجين`
   * *Fix:* `غرفة ملح وعلاج ضوئي بالكولاجين`
5. **Literal Real Estate Calque**
   * *Quote:* `ملاحظة تحذيرية`
   * *Fix:* `إشارة تحذيرية في الطابو (حفظ الحقوق العقارية)`
6. **Untranslated Language Switcher**
   * *Quote:* `עב EN FR RU AR`
   * *Fix:* `HE EN FR RU AR`
7. **Truncated Breadcrumb**
   * *Quote:* `الرئيسية › المشاريع › ASHIRA Sde Dov - شقق جديدة للبيع في تل أبيب…`
   * *Fix:* `الرئيسية › المشاريع › ASHIRA Sde Dov - شقق جديدة للبيع في تل أبيب والأسعار ودليل الشراء`
8. **Disclosed Sales Omission**
   * *Quote:* `السعر الحالي: لم تنشر قائمة أسعار عامة شاملة ومؤرخة`
   * *Fix:* `رغم عدم توفر لائحة أسعار حية، تفيد تقارير المطور ببيع 125 شقة حتى يوليو 2026 بمتوسط 72,000 شيكل/م² في الربع الثاني من 2026.`

---

## 2. Facts That Differ Between Languages

1. **Actual Sales Figures & Pricing Transparency**
   * *Hebrew (Lines 34, 37):* Discloses exact financial report sales: `באשירה שדה דב נמכרו ב- 2025 31 דירות במחיר ממוצע של כ- 64,500 ₪ למ״ר, וברבעון השני של 2026 הממוצע עלה לכ- 72,000 ₪ למ״ר... עד 7.2026 נמכרו 125 מתוך 406 הדירות`
   * *EN / FR / RU / AR:* Claim zero current sales data or prices exist:
     * *EN (Line 120):* `No current official public price list found`
     * *FR (Line 188):* `aucune liste officielle, complète et actualisée des prix et disponibilités d’ASHIRA n’a été trouvée`
     * *RU (Line 149):* `Актуального официального полного прайс-листа и списка квартир... не найдено.`
     * *AR (Line 93):* `السعر الحالي: لم تنشر قائمة أسعار عامة شاملة ومؤرخة.`

2. **Penthouse Benchmark (Transaction vs. Asking)**
   * *Hebrew (Line 43):* Cites an actual closed transaction: `פנטהאוז, 141 מ״ר ומרפסת 95 מ״ר חצי קומה 15 במגדלון של 16 קומות... 19.5 מיליון עסקה 8.2024` (19.5M NIS for 141 sqm + 95 sqm terrace).
   * *EN / FR / RU / AR:* Cite an unverified historical launch marketing ask from Ynet:
     * *EN (Line 231):* `160-square-metre penthouse with a 67-square-metre terrace at NIS 25 million.` (also FR Line 197, RU Line 150, AR Line 154).

3. **Building Heights Discrepancy (Within & Across Versions)**
   * *Hebrew (Line 92), EN (Line 32), FR (Line 32), RU (Line 32), AR (Line 32):* Report `two 9-floor buildings` (`שני בניינים של 9` / `deux immeubles de 9 étages` / `два 9-этажных здания` / `ومبنيان من 9 طوابق`).
   * *Hebrew (Line 30), EN (Line 99), FR (Line 84), RU (Line 100), AR (Line 86):* Report `two 8-storey buildings` (`שני בניינים של 8 קומות` / `deux immeubles de 8 étages` / `двух зданиях на 8 этажей` / `مبنيان من 8 طوابق`).

4. **Competitor Distances in Comparison Table**
   * *Hebrew (Lines 228–246):* Excludes ASHIRA; lists DIMRI YAMA at `330 מ׳`, ZOHI at `373 מ׳`, Rainbow at `411 מ׳`, GINDI VOGUE at `677 מ׳`, FIRST at `995 מ׳`, and Kikar Hamedina at `2.1 ק״מ`.
   * *EN (Lines 450–470) / FR / RU / AR:* Include ASHIRA at `11 m`; list DIMRI YAMA at `321 m`, ZOHI at `363 m`, Rainbow at `400 m`, GINDI VOGUE at `680 m`, FIRST at `1.0 km`; and omit Kikar Hamedina entirely.

5. **Infrastructure & Transit Walking Distances**
   * *Hebrew (Lines 138, 140):* Provides concrete measurements: `רכבת קלה תחנת זהרה לביטוב מאושרת, 581 מ׳` and construction site at `39 מ׳`.
   * *EN / FR / RU / AR:* Specifically assert that no project-to-station walking distance is verified:
     * *EN (Line 406):* `No exact project-to-station walk time has been verified.`
     * *FR (Line 136):* `aucune durée de marche précise depuis ASHIRA n’a été validée`
     * *AR (Line 117):* `ولا يثبت مسافة مشي من مدخل محدد.`

6. **Bank Financing Consortium**
   * *EN (Line 268), FR (Line 240), RU (Line 156), AR (Line 171):* Explicitly name `Mizrahi-Tefahot and First International Bank` with financing exceeding `NIS 2.5 billion`.
   * *Hebrew:* Completely omits bank names and financing amounts.

7. **Marketed Room Mix**
   * *Hebrew (Line 147):* States `2 עד 5 חדרים` (2 to 5 rooms).
   * *EN (Line 177), FR (Line 156), RU (Line 17), AR (Line 130):* State `2 to 6 rooms and penthouses` (`2 à 6 pièces`, `2-6 комнат`, `غرفتان إلى ست غرف`).

---

## 3. Developer Readiness Verdict

* **Hebrew:** **No** — Ruined by the street name error ("אשכול לוי"), a cut-off sentence in line 268, detached hyphens, and the 8 vs. 9 floor conflict.
* **English:** **No** — Disqualified by the absurd table bug listing ASHIRA 11m from itself, internal height contradictions, and the omission of published developer sales figures.
* **French:** **No** — Disqualified by unaccented map labels, the 11m table bug, the 8 vs. 9 floor conflict, and the awkward "bronzage au collagène."
* **Russian:** **No** — Disqualified by literal Hebrew calques ("малая башня", "коллагеновый солярий"), the 11m table bug, and floor contradictions.
* **Arabic:** **No** — Disqualified by machine calques ("تسمير بالكولاجين", "برج صغير"), the 11m table bug, and floor contradictions.
