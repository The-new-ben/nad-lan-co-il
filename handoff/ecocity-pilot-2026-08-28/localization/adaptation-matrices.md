# Localization adaptation matrices

The Hebrew source-of-truth files are canonical. The four additional languages are editorial adaptations for different buyer questions, not sentence-by-sentence translations. A fact can move between sections or receive more explanation, but it cannot gain a number, promise or benefit that is absent from the Hebrew truth and fact register.

## Shared locale contract

| Locale | Direction | Primary reader job | Editorial voice | Required adaptation |
|---|---:|---|---|---|
| `en` | LTR | Understand a Tel Aviv new-development purchase from abroad | Precise, calm, internationally legible | Explain Israeli “rooms,” NIS/sqm, project stage, independent-site status and local buyer checks |
| `fr` | LTR | Evaluate a possible primary/second home and family use | Refined but restrained; practical before aspirational | Explain the acquisition path in Israel and avoid treating “pièces” as bedrooms without clarification |
| `ru` | LTR | Verify specifications, legal status and practical usability | Direct, evidence-led, low on ornament | Surface source dates, missing fields, plan/spec checks and exact status labels |
| `ar` | RTL | Assess family life, urban access and transaction clarity | Modern Standard Arabic, clear and respectful | Preserve Hebrew street names in consistent transliteration, explain local processes and keep future transit distinct |

### URL and technical rules

- Use separate, crawlable URLs for each language. Do not swap language by cookie or client-only state.
- Every language page is self-canonical. Add reciprocal `hreflang` links for `he-IL`, `en`, `fr`, `ru`, `ar` and `x-default` to the Hebrew page or a genuine language selector.
- The visible language and the HTML `lang` attribute must agree. Use `dir="rtl"` for Hebrew and Arabic and `dir="ltr"` for English, French and Russian.
- Mark a foreign-language phrase inside another language with a correct nested `lang` value when needed.
- Keep the same verified project entities and stable IDs across locales. Localize labels, not identifiers.
- Do not auto-canonicalize localized pages to Hebrew. Google recommends separate localized URLs with reciprocal `hreflang`: [Google Search Central](https://developers.google.com/search/docs/specialty/international/localized-versions).

### Numbers, areas and legal meaning

- Use square metres as the primary unit in all five languages. English may optionally show square feet secondarily after a deterministic conversion.
- Use NIS/ILS consistently only when a public, current price exists. Do not convert currencies in static copy.
- Israeli “3 rooms” usually counts the living room; it must not silently become “3 bedrooms.” Use “3-room apartment (Israeli convention)” until bedroom data is supplied.
- “Planned occupancy 2028” is not “guaranteed delivery in 2028.” Every locale must preserve the qualification.
- “Park-facing” or “open frontage” is not “permanent unobstructed view.”
- The independent-site disclosure appears near the first conversion action, not only in the footer.

## English adaptation

### Audience and intent matrix

| Module | International reader question | English treatment | Avoid |
|---|---|---|---|
| Hero | What is this, where is it and who is behind it? | Lead with address, EcoCity, verified configuration and check date | “Exclusive opportunity,” “guaranteed,” “official sales site” |
| Project facts | Can I trust the stage and numbers? | Use dated status labels and source chips; link to “What is verified” | Hiding unknowns behind “contact us” |
| Residences | How do Israeli room counts and areas work? | Explain room convention and show sqm first | Translating rooms as bedrooms |
| Location | What does this part of north Tel Aviv offer? | Explain streets, park and future Green Line in plain terms | Unmeasured “minutes from” claims |
| Buyer journey | What must a foreign buyer check? | Add lawyer, tax, finance, payment security, contract and registration checklist, as general information | Legal or tax advice; residency assumptions |
| Lead form | What will happen to my details? | State destination, response owner and marketing consent separately | Implying EcoCity follow-up without an approved lead route |

### Stricker 13-Brandeis 14 English copy set

**H1:** Stricker 13-Brandeis 14, Tel Aviv: Two Boutique Residential Buildings by EcoCity

**Title:** Stricker 13-Brandeis 14 Tel Aviv | EcoCity Project Guide

**Meta description:** An independent guide to Stricker 13 and Brandeis 14 in Tel Aviv: two buildings with 26 residences each, according to EcoCity, plus verified status, location and buyer checks.

**Hero headline:** Two addresses, one clear way to compare

**Hero summary:** EcoCity describes two residential buildings with 26 homes in each and full-floor penthouses. The project was marketed as pre-construction with planned occupancy in 2028 when checked on 28 August 2026. Availability and pricing are shown only from an approved current feed.

**Primary CTA before inventory:** Request current project information

**Secondary CTA:** Prepare for the sales meeting

**FAQ emphasis:** total homes; dated project stage; planned occupancy versus contract date; Israeli room convention; future Green Line; independent status; 3D simulation limitations.

**Search-intent language:** “Stricker 13 Tel Aviv new development,” “Brandeis 14 apartments,” “EcoCity Tel Aviv project,” “new apartments near Yehuda HaMaccabi.” Use only where natural. Do not create a separate page for each address if the product is one project, because that would split intent and duplicate content.

### Bnei Dan 54-56 English copy set

**H1:** Bnei Dan 54-56, Tel Aviv: Boutique Living on Yarkon Park

**Title:** Bnei Dan 54-56 Tel Aviv | EcoCity Park-Front Project Guide

**Meta description:** An independent guide to Bnei Dan 54-56 on Yarkon Park. EcoCity describes an eight-storey boutique building with open frontages and deep balconies. Facts, gaps and buyer checks.

**Hero headline:** A home shaped around daily park life

**Hero summary:** EcoCity presents Bnei Dan 54-56 as an eight-storey boutique residential project on the edge of Yarkon Park, with open frontages, deeper balconies and conventional parking. Unit-level details require approved plans and a current inventory feed.

**Primary CTA before inventory:** Request current project information

**Secondary CTA:** Open the buyer checklist

**FAQ emphasis:** park-facing versus guaranteed view; unknown total unit count; balcony dimensions; parking per residence; status and occupancy date; formal neighborhood label; beach is not the project frontage.

**Search-intent language:** “Bnei Dan 54-56 Tel Aviv,” “new apartments by Yarkon Park,” “EcoCity Bnei Dan,” “park-front apartment Tel Aviv.” Do not use “waterfront” or “beachfront.”

## French adaptation

### Audience and intent matrix

| Module | Question du lecteur | Traitement éditorial | À éviter |
|---|---|---|---|
| Accroche | S’agit-il d’une résidence principale, secondaire ou d’un investissement? | Présenter d’abord l’adresse, le cadre de vie et les faits vérifiés; laisser le lecteur définir son usage | Promesse de rendement ou de plus-value |
| Typologies | Que signifie “3 ou 4 pièces” en Israël? | Ajouter une note sur la convention israélienne et attendre le nombre de chambres | Traduire automatiquement par “3 chambres” |
| Acquisition | Comment se déroule un achat en Israël? | Ajouter un parcours de vérification: avocat indépendant, fiscalité, financement, garanties, contrat, enregistrement | Conseil juridique personnalisé |
| Quartier | Quels repères facilitent la vie quotidienne? | Expliquer le parc, les rues et les services; liens de carte dynamiques | “À deux pas” ou durées non mesurées |
| Formulaire | Qui répondra et à quoi je consens? | Séparer demande d’information et consentement marketing | Case précochée ou destinataire implicite |

### Stricker 13-Brandeis 14: jeu de contenus français

**H1:** Stricker 13-Brandeis 14 à Tel-Aviv: deux résidences boutique signées EcoCity

**Title:** Stricker 13-Brandeis 14 à Tel-Aviv | Guide du projet EcoCity

**Meta description:** Guide indépendant de Stricker 13 et Brandeis 14 à Tel-Aviv: deux bâtiments de 26 logements chacun selon EcoCity, état du projet, environnement et points à vérifier.

**Accroche:** Deux adresses, une comparaison claire

**Résumé:** EcoCity présente deux bâtiments résidentiels de 26 logements chacun, avec des penthouses occupant un étage entier. Lors de notre vérification du 28 août 2026, le projet était commercialisé avant travaux, avec une livraison envisagée en 2028. Les disponibilités et les prix restent absents sans source officielle à jour.

**CTA principal:** Demander les informations à jour

**CTA secondaire:** Préparer le rendez-vous commercial

**Intentions de recherche:** “programme neuf Stricker Tel Aviv,” “Brandeis 14 appartement neuf,” “EcoCity Tel Aviv,” “immobilier neuf nord Tel Aviv.” Le mot “prestige” n’est utilisé que si une caractéristique concrète le justifie.

### Bnei Dan 54-56: jeu de contenus français

**H1:** Bnei Dan 54-56 à Tel-Aviv: une résidence boutique face au parc HaYarkon

**Title:** Bnei Dan 54-56 Tel-Aviv | Guide du projet EcoCity face au parc

**Meta description:** Guide indépendant de Bnei Dan 54-56 face au parc HaYarkon. EcoCity décrit un bâtiment de huit étages, des façades ouvertes et des terrasses profondes. Faits et vérifications.

**Accroche:** Le parc au rythme de la vie quotidienne

**Résumé:** EcoCity présente Bnei Dan 54-56 comme une résidence boutique de huit étages le long du parc HaYarkon, avec des appartements en façade ouverte, des terrasses plus profondes et des places de stationnement classiques. Les caractéristiques doivent être confirmées logement par logement.

**CTA principal:** Demander les informations à jour

**CTA secondaire:** Consulter la liste des vérifications

**Intentions de recherche:** “Bnei Dan 54-56 Tel Aviv,” “appartement neuf parc HaYarkon,” “EcoCity Bnei Dan,” “résidence face au parc Tel Aviv.” Éviter “vue garantie,” “bord de mer” et tout vocabulaire de rendement.

## Russian adaptation

### Audience and intent matrix

| Модуль | Вопрос читателя | Редакционная подача | Не использовать |
|---|---|---|---|
| Первый экран | Что подтверждено на дату проверки? | Адрес, застройщик, конфигурация, статус и дата источника | Эмоциональные обещания без спецификации |
| Квартиры | Какие параметры доступны по каждой квартире? | Таблица с площадью, этажом, экспозицией, балконом и парковкой только из утвержденного фида | Данные из макета или старой страницы |
| Документы | Что нужно проверить до сделки? | Разрешение, банковское сопровождение, гарантии, договор, индексацию, регистрацию | Выдавать общий материал за юридическую консультацию |
| Район | Что реально находится вокруг? | Разделять существующее и планируемое; показывать дату карты | Непроверенные расстояния и время в пути |
| 3D | Насколько модель точна? | Версия модели, источники геометрии, режим симуляции | “Точный вид из окна” без съемки и координат |

### Stricker 13-Brandeis 14: русская версия

**H1:** Штрикер 13 - Брандейс 14, Тель-Авив: два клубных дома EcoCity

**Title:** Штрикер 13 - Брандейс 14 в Тель-Авиве | Гид по проекту EcoCity

**Meta description:** Независимый гид по проекту Штрикер 13 и Брандейс 14: два дома по 26 квартир по данным EcoCity, актуальный статус, район и список проверок покупателя.

**Заголовок первого экрана:** Два адреса, единая система выбора

**Краткое описание:** EcoCity сообщает о двух жилых домах, по 26 квартир в каждом, и пентхаусах на полный этаж. На 28 августа 2026 года проект находился в продаже на предстроительной стадии, а заселение планировалось на 2028 год. Цены и наличие не публикуются без официального обновляемого источника.

**Основной CTA:** Запросить актуальную информацию

**Вторичный CTA:** Подготовиться к встрече с отделом продаж

**Поисковые формулировки:** “Штрикер 13 Тель-Авив,” “Брандейс 14 новостройка,” “EcoCity Тель-Авив,” “квартиры рядом с Йехуда ха-Маккаби.” Названия улиц должны иметь один утвержденный вариант транслитерации.

### Bnei Dan 54-56: русская версия

**H1:** Бней-Дан 54-56, Тель-Авив: клубный дом у парка Яркон

**Title:** Бней-Дан 54-56 в Тель-Авиве | Гид по проекту EcoCity у парка

**Meta description:** Независимый гид по Бней-Дан 54-56 у парка Яркон. EcoCity описывает восьмиэтажный клубный дом с открытыми фасадами и глубокими балконами. Факты и пробелы.

**Заголовок первого экрана:** Дом, ориентированный на повседневную жизнь у парка

**Краткое описание:** EcoCity представляет Бней-Дан 54-56 как восьмиэтажный жилой проект непосредственно вдоль парка Яркон, с открытыми фасадами, более глубокими балконами и обычными парковочными местами. Параметры подтверждаются отдельно по каждой квартире.

**Основной CTA:** Запросить актуальную информацию

**Вторичный CTA:** Открыть список проверок покупателя

**Поисковые формулировки:** “Бней Дан 54-56 Тель-Авив,” “квартира у парка Яркон,” “EcoCity Бней Дан,” “новостройка север Тель-Авива.” Не использовать “вечный вид,” “первая линия моря” или гарантии роста стоимости.

## Arabic adaptation

### مصفوفة الجمهور والهدف

| الوحدة | سؤال القارئ | المعالجة التحريرية | ما يجب تجنبه |
|---|---|---|---|
| الواجهة الأولى | ما المشروع وما الذي تم التحقق منه؟ | العنوان، المطور، التكوين، تاريخ التحقق وحالة المشروع | ادعاء أن الصفحة رسمية أو معتمدة من المطور |
| الشقق | ما المساحات والتقسيمات المتاحة؟ | عرض البيانات من ملف معتمد فقط وشرح طريقة عد الغرف في إسرائيل | تحويل عدد الغرف إلى عدد غرف نوم |
| الموقع | كيف ترتبط الحياة اليومية بالشارع والحديقة؟ | خريطة حسب الاحتياج مع فصل القائم عن المخطط | مسافات أو أزمنة وصول غير موثقة |
| الشراء | ما الفحوص المطلوبة قبل التوقيع؟ | محام مستقل، تمويل، ضمانات، مواصفات، موعد تعاقدي وتسجيل | تقديم إرشاد عام على أنه استشارة قانونية |
| النموذج ثلاثي الأبعاد | هل المنظر حقيقي؟ | بيان واضح: صورة أو تصور أو محاكاة، مع التاريخ والمصدر | “المنظر الحقيقي” أو “منظر دائم” بلا إثبات |

### شتريكر 13 وبرانديس 14: مجموعة النصوص العربية

**H1:** شتريكر 13 وبرانديس 14 في تل أبيب: مبنيان سكنيان بطابع بوتيك من EcoCity

**Title:** شتريكر 13 وبرانديس 14 في تل أبيب | دليل مشروع EcoCity

**Meta description:** دليل مستقل لمشروع شتريكر 13 وبرانديس 14: مبنيان يضم كل منهما 26 شقة بحسب EcoCity، مع حالة المشروع والبيئة المحيطة وفحوص المشتري.

**عنوان الواجهة:** عنوانان ومسار واحد واضح للمقارنة

**الملخص:** تعرض EcoCity مشروعاً من مبنيين سكنيين، يضم كل مبنى 26 شقة، إضافة إلى بنتهاوسات تمتد على طابق كامل. عند التحقق في 28 أغسطس 2026 كان المشروع معروضاً للبيع قبل بدء التنفيذ، مع إشغال مخطط في 2028. لا تظهر الأسعار أو الوحدات المتاحة دون مصدر رسمي محدث.

**الزر الرئيسي:** اطلبوا معلومات محدثة عن المشروع

**الزر الثانوي:** جهزوا أسئلتكم لاجتماع المبيعات

**نوايا البحث:** “شتريكر 13 تل أبيب”، “برانديس 14 شقق جديدة”، “EcoCity تل أبيب”، “شقق قرب يهودا همكابي”. يجب اعتماد تهجئة عربية واحدة لأسماء الشوارع مع إظهار الاسم اللاتيني عند الحاجة.

### بني دان 54-56: مجموعة النصوص العربية

**H1:** بني دان 54-56 في تل أبيب: سكن بوتيك بمحاذاة حديقة اليركون

**Title:** بني دان 54-56 في تل أبيب | دليل مشروع EcoCity عند حديقة اليركون

**Meta description:** دليل مستقل لبني دان 54-56 بمحاذاة حديقة اليركون. تصف EcoCity مبنى من ثمانية طوابق بواجهات مفتوحة وشرفات عميقة. حقائق وفحوص قبل الشراء.

**عنوان الواجهة:** عندما تصبح الحديقة جزءاً من الحياة اليومية

**الملخص:** تقدم EcoCity مشروع بني دان 54-56 كمبنى سكني بطابع بوتيك من ثمانية طوابق بمحاذاة حديقة اليركون، مع واجهات مفتوحة وشرفات أعمق ومواقف سيارات عادية. يجب تأكيد التفاصيل لكل شقة من المخططات والملف المحدث.

**الزر الرئيسي:** اطلبوا معلومات محدثة عن المشروع

**الزر الثانوي:** افتحوا قائمة فحوص المشتري

**نوايا البحث:** “بني دان 54-56 تل أبيب”، “شقق جديدة قرب حديقة اليركون”، “EcoCity بني دان”، “سكن شمال تل أبيب”. يمنع استخدام “إطلالة مضمونة”، “على البحر” أو أي ضمان للاستثمار.

## Per-section adaptation rules

| Hebrew source section | English | French | Russian | Arabic |
|---|---|---|---|---|
| Story | Add quick context for north Tel Aviv and explain local room convention | Emphasize use as a home and acquisition clarity | Move verified facts and source date before lifestyle prose | Explain street/park relationship and local terms in MSA |
| Architecture | Use “residences” sparingly; specs over luxury adjectives | Use “résidence” and “logement”; define pièces | Prefer tables and explicit unknowns | Use clear residential terms; avoid ornate sales language |
| Transport | “planned Green Line,” never operational tense | “ligne verte en projet / en construction” | “планируемая Зеленая линия” | “الخط الأخضر المخطط له” |
| Education | Explain annual municipal assignment | Explain that proximity does not determine sector allocation | Highlight school-year validity | State that registration zones can change yearly |
| Park and beach | Park-front is valid only for Bnei Dan; neither is beachfront | Do not turn park access into seaside positioning | Keep park and beach as separate map layers | Separate حديقة اليركون from شاطئ البحر clearly |
| Buyer journey | Add foreign-buyer preparation module | Add Israel purchase-process explainer | Surface document checklist early | Add process and consent clarity |
| FAQ | Use concise direct answers | Slightly more explanatory legal/process context | Put dates and missing fields in first sentence | Avoid untranslated Hebrew acronyms; spell out once |
| CTA | “Request current information” before official routing | “Demander les informations à jour” | “Запросить актуальную информацию” | “اطلبوا معلومات محدثة” |

## Localization QA

- A bilingual reviewer must compare every localized factual sentence to a `fact_id`.
- Run a number diff: every number in a localized file must also exist in the Hebrew source and fact register.
- Run a named-entity diff for addresses, EcoCity, Yarkon Park, Yehuda HaMaccabi and Milano Square.
- Check punctuation, line wrapping and focus order in both RTL locales at mobile widths.
- Verify screen-reader pronunciation with correct page language and language-of-parts markup.
- Confirm that translated CTAs describe the actual lead destination and do not imply an official relationship.
- Do not publish a locale with placeholder English, machine-translated disclaimers or missing legal/privacy links.

