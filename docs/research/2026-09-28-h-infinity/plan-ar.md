# Plan: the Arabic article on H Infinity (not a translation)

Base: facts.md, serp-ar.md. Target: 5,000+ net words, 11 unique H2s, Modern Standard Arabic that reads naturally to
Israeli Arabic speakers, with the Hebrew term in brackets on first use.
Suggested URL per the fleet pattern: `/projects/h-infinity-somail-tel-aviv-ar/` (like `/projects/duo-tel-aviv-ar/`).
Not created yet; run `tools/gsc/url_word_audit.py` first.

## 1. Who reads it and what they want
- **Israeli Arabic-speaking buyers** (citizens and residents): professionals who work in central Tel Aviv, families
  upgrading, and investors buying an additional apartment. They are Israeli residents, so the rules are the resident
  rules: single-apartment brackets or 8% for an additional apartment, mortgages up to 75%/70%/50% by buyer type.
- They type project names in Hebrew or Latin; the Arabic SERP for "برج انفينيتي" is Egypt's Infinity Tower. There is
  **no Arabic competitor**. The page must pin the entity every time: "في تل أبيب، شارع ابن جبيرول 128".
- The village history (السُّمَيل / المسعودية) is known to part of the audience: tell it briefly, factually and
  respectfully, from the cited source, without political framing.

## 2. Names, title, meta, H1
- Names: **برج H Infinity (برج إنفينيتي)**, **مجموعة حجاج (Hagag Group)**, **شارع ابن جبيرول 128**, **مجمّع سومييل
  (السُّمَيل)**, area **كيكار همدينا (ساحة الدولة)**. The Hebrew name once in brackets: (מגדל אינפיניטי).
- **Title (≤60):** `برج H Infinity في تل أبيب: الأسعار والصفقات ودليل الشراء` (56)
- **Meta (≤155):** `برج إنفينيتي (H Infinity) لمجموعة حجاج، ابن جبيرول 128 في مجمّع سومييل: 53 طابقاً، نحو 278 شقة، أسعار صفقات حقيقية، عرض 2026 وضريبة الشراء.` (139)
- **H1:** `برج H Infinity لمجموعة حجاج في مجمّع سومييل، تل أبيب`

## 3. The answer paragraph
> يُبنى برج H Infinity (برج إنفينيتي) التابع لمجموعة حجاج في شارع ابن جبيرول 128 في تل أبيب، في القسم الشمالي من مجمّع
> سومييل بين شارعي أرلوزوروف وجابوتنسكي، على بُعد دقائق سيراً من ساحة كيكار همدينا. بحسب التقرير السنوي للشركة لعام
> 2025، تسمح رخص البناء ببرج من 53 طابقاً ومبنى من 6 طوابق سكنية فوق طابق تجاري، بمجموع نحو 278 شقة من غرفتين إلى 6
> غرف، من تصميم البروفيسور موشيه تسور وتنفيذ شركة إلكترا للبناء. تعلن الشركة عن أسعار تبدأ من 65,000 شيكل للمتر المربع،
> بينما تراوحت الصفقات المسجلة في المشروع عام 2025 بين نحو 72 و95 ألف شيكل للمتر (مدلان، وفق بيانات سلطة الضرائب).
> وتتوقع الشركة انتهاء البناء في الربع الأخير من عام 2026.

## 4. Outline (H2/H3, words, keywords)
| # | H2 (Arabic) | H3 | Intent | Words | Keywords here |
|---|---|---|---|---|---|
| 1 | برج H Infinity باختصار: ماذا تبني مجموعة حجاج في ابن جبيرول 128 | العنوان وقطعة الأرض · كم طابقاً وكم شقة ولماذا تختلف الأرقام | what/where | 500 | برج إنفينيتي تل أبيب، مجموعة حجاج، ابن جبيرول 128، شقق للبيع في تل أبيب |
| 2 | أسعار الشقق في برج H Infinity: الأسعار المعلنة مقابل الصفقات الحقيقية | أسعار الشركة · الصفقات المسجلة 2024-2026 · لماذا الفرق · مقارنة بمشروع DUO والمنطقة | price | 850 | سعر المتر المربع، صفقات، شقق فاخرة للبيع في تل أبيب |
| 3 | عرض مجموعة حجاج 2026: مليون شيكل عند التوقيع و"إيجار مضمون" | ما الذي عُرض · ماذا تعني نسبة "24%-52%" بالأرقام · لمن يناسب وماذا نفحص | investor/upgrader | 600 | العائد، الإيجار، دفع مؤجل (حسابنا) |
| 4 | الشقق والمرافق: ما هو معروف وما لم يُنشر | عدد الغرف بالطريقة الإسرائيلية · المسبح واللوبي والنادي الرياضي · الغرفة الآمنة (ממ"ד) | product | 450 | شقق من غرفتين إلى 6 غرف، مسبح، ממ"ד |
| 5 | موعد التسليم: أين وصل البناء في أيلول 2026 | نسبة إنجاز مالية 86.3% · متى المفاتيح · شرط البلدية للإسكان | timing | 450 | التسليم، نموذج 4 (טופס 4) |
| 6 | مجمّع سومييل والحيّ: كيكار همدينا والشمال القديم | لمحة تاريخية عن السُّمَيل · ما الذي يُبنى حوله · المسافات سيراً · القطار الخفيف: البنفسجي 2028 والأخضر 2030 | neighbourhood | 700 | مجمّع سومييل، تل أبيب الشمالية، القطار الخفيف |
| 7 | مجموعة حجاج والمهندس موشيه تسور وشركة إلكترا | المطوّر · المهندس والمقاول · من مجموعة شراء إلى مشروع مطوّر | trust | 450 | مجموعة شراء (קבוצת רכישה)، كفالة قانون البيع |
| 8 | قبل التوقيع: ثمانية أمور يجب فحصها | numbered list | risk | 550 | كفالة بنكية، المواصفات (מפרט)، ربط بالمؤشر، رسوم الإدارة |
| 9 | ضريبة الشراء والقرض السكني لمن يشتري في البرج | شقة وحيدة أو إضافية (جدول) · القرض السكني: 75% / 70% / 50% · حساب مثال | "ضريبة الشراء"، "قرض سكني" (Israeli terms) | 550 | ضريبة الشراء (מס רכישה)، المشكنتا (משכנתא)؛ every rate [يُراجع من قبل صاحب الموقع، محامٍ] |
| 10 | أسئلة شائعة عن برج H Infinity | 12 FAQ | PAA | 650 | all names |
| 11 | المصادر وتواريخ الفحص | - | trust | 150 | - |
| | **Total** | | | **~5,900** | |

## 5. FAQ (Arabic)
1. أين يقع برج H Infinity في تل أبيب، وما عنوانه؟
2. كم طابقاً في البرج: 51 أم 52 أم 53؟
3. كم شقة في المشروع، وكم بقي للبيع؟
4. كم سعر الشقة وسعر المتر المربع في البرج؟
5. متى موعد التسليم؟
6. من المطوّر والمهندس والمقاول؟
7. ما هو عرض "مليون شيكل عند التوقيع"، وما العائد الحقيقي؟
8. هل في البرج مسبح؟ وهل في كل شقة غرفة آمنة (ממ"ד)؟
9. ما هو مجمّع سومييل، وما الذي يُبنى فيه أيضاً؟
10. كم ضريبة الشراء على شقة إضافية؟
11. ما نسبة القرض السكني التي يمكن الحصول عليها؟
12. متى يصل القطار الخفيف إلى المنطقة؟

## 6. Internal links (all HTTP 200 on 28.9.2026)
`/ar/` · `/ar/new-projects/` · `/ar/guides/` · `/ar/guides/remote-new-apartment-handover-israel/` · `/ar/guides/new-apartment-mamad/` ·
`/ar/guides/new-project-management-fees/` · `/ar/guides/new-apartment-sale-specification/` · `/ar/guides/neighboring-development-check/` ·
`/ar/guides/mixed-use-residential-project/` · `/ar/guides/common-property-handover/` · `/projects/duo-tel-aviv-ar/`.
Hebrew tools (label "بالعبرية"): `/tour/somail/`, `/purchase-tax-calculator/`, `/mortgage-calculator/`, and the Hebrew page
`/projects/h-infinity-somail-tel-aviv/`.

## 7. Audience notes (why this is not a translation)
- The reader is an Israeli resident: the foreign-resident block of the other languages is replaced by the resident
  rules (single apartment, additional apartment, upgrader) and the mortgage tiers.
- Keep Israeli Hebrew terms in brackets on first use; many readers deal with the bank and the lawyer in Hebrew.
- Western digits, ₪ as "شيكل". Dates in the Gregorian calendar with Levantine month names (أيلول، آب).
- History: two or three sentences with the cited figures (population 1945, the date the residents left: 25.12.1947),
  no judgement words.
- Tone: respectful, practical, no hype; no "حصري"، no "آخر الشقق".
