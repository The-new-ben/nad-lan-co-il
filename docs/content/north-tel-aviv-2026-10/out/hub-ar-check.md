# hub / ar: translation gate result (HAD-460 Stage A, 7.10.2026)

Written by Claude in this session, under the owner's approval to write it here instead of in ChatGPT, from
packets/prompt-hub-ar.md (both messages), packets/hub-ar.json, claims.json, links.json, live-headings.json and
docs/content/rova-4-2026-10/i18n-brief.md. Data only: nothing published, nothing committed or pushed, no WordPress writes.

## The checker's final output

Command (from this folder, PYTHONIOENCODING=utf-8), run 2026-10-07 20:25 UTC:
`python check_translation.py out/hub-ar.html --page hub --lang ar --meta out/hub-ar.meta.txt`

```
== hub/ar | net words 4579 | numbers 88, unmatched 0 | errors 0 | warnings 0 | comparators 6 (live)
  RESULT: PASS
```

Exit code 0. The headings were compared live against /ar/new-projects/, /ar/guides/, /ar/brokers/, /ar/developer-deals/,
/ar/buy-property-in-israel/ and /projects/hamedina-ar/, and every internal link answered GET 200.
A second run with `--peer out/rova-4-ar.html` also PASSES: no H1 or H2 shares its first 4 words with the Arabic Rova 4 page.
The script found no banned words, no soft style words, no dashes, no "!", no Hebrew letters and no shortcodes.

## Net words

4,579 net words (the checker's count). The packet range is 3,493 to 4,932 and the target is 4,110. Every section is
within 15% of its budget:

| section | words | budget | allowed (15%) |
|---|---:|---:|---|
| hub-opening (with the H1 and eyebrow) | 399 | 350 | 298 to 402 |
| hub-areas | 585 | 530 | 451 to 609 |
| hub-life | 316 | 280 | 238 to 322 |
| hub-anchors | 411 | 380 | 323 to 437 |
| hub-projects | 534 | 470 | 400 to 540 |
| hub-prices | 570 | 500 | 425 to 575 |
| hub-compare | 343 | 300 | 255 to 345 |
| hub-transport | 236 | 210 | 179 to 241 |
| hub-fit | 304 | 270 | 230 to 310 |
| hub-legal | 382 | 340 | 289 to 391 |
| hub-faq | 343 | 330 | 281 to 379 |
| hub-abroad | 156 | 140 | 119 to 161 |

## SEO

- title (60 characters, English per the owner's ruling of 28.9.2026): North Tel Aviv: Neighborhoods, Projects and Apartment Prices
- description (136 characters, Arabic): دليل شمال تل أبيب: رمات أفيف ونافيه أفيفيم وبافلي وحي لامد وسدي دوف، أسعار شقق 4 غرف، مشاريع شارع أينشتاين، المواصلات والشراء من الخارج.
- url: https://nad-lan.co.il/ar/north-tel-aviv/
- The H1 is the packet's English H1, exactly. The title differs from the live English hub's title, as the Arabic Kikar
  page's title differs from the English one.

## Extra checks (beyond the script)

- **Numbers, section by section.** The number tokens in each Arabic section were compared with the matching Hebrew
  section, and they match one to one in all 12 sections (88 tokens).
  - The decades are written "سنوات الـ60 والـ70", the way the Arab press in Israel writes them, so they keep the
    Hebrew digits.
  - Counts the Hebrew writes in words (six buildings, five, three) stay in words.
- **Claim meanings.**
  - 515 always refers to the whole Hagag complex, and 215 always to EINSTEIN TOWER.
  - The completion in the third quarter of 2030 is the company's estimate.
  - The medians are whole-apartment prices, never per m².
  - No delivery date is given for Sde Dov, no rents or yields, and no per-m² price beyond the ones given.
- **Links.** The page has 21 links:
  - The 18 links of the Hebrew page, each in its place. Every link to a Hebrew page carries "(بالعبرية)" after it,
    outside the link.
  - 3 Arabic extras, the maximum: أبراج كيكار همدينا (/projects/hamedina-ar/) in the guides line, مشروع Rainbow في سدي دوف
    (/projects/rainbow-tel-aviv-ar/) in "who it suits", and المشاريع السكنية الجديدة في إسرائيل (/ar/new-projects/) in the
    projects section.
- **HTML.**
  - Only the allowed tags are used. There are no comments, div, span, br or inline style.
  - The classes come from the Hebrew page: nl-eyebrow, nl-cta, nl-cards, nl-note and nl-hub-guides.
  - There are 12 H2s and 8 H3s, as in the Hebrew, and the three tables have the same columns and rows.
- **Wording.**
  - The prompt's banned words were also checked by hand, beyond the script: طبقة, «النظام», «المنصة», نموذج, محرّك,
    تجربة رقمية.
  - "تقريباً" was avoided as well, because it contains the banned string "قريباً".
  - The page has no source or media names. "The municipality" and "the Tax Authority" appear only where the Hebrew has them.

## Cultural choices (5 lines)

1. **The reader.** The page is written first for Arab families in Israel, then for investors and for buyers living
   abroad. It puts schools, parking, the commute, the price per meter and financing up front. It addresses the reader as
   «أنتم», like the site's Arabic Kikar page, in a warm, confident voice of a premium guide.
2. **Israeli terms, explained once each,** in the words Arab citizens of Israel use: 4 غرف = صالون وثلاث غرف نوم,
   تاما 38, بينوي بينوي, ممّاد, «بنايات القطار», نسخة الطابو, ضريبة الشراء (مَس ريخيشا), ضريبة الربح العقاري (مَس شيفح),
   ضريبة التحسين (هيتل هشبحاه), كفالة قانون البيع, المرافقة البنكية, and القيمة الوسيطة.
3. **Typography as the prompt asks:**
   - Western digits, "5,370,100 ₪", م², and ranges written with "إلى".
   - Levantine month names (كانون الثاني، حزيران، آب), and no em or en dashes.
   - The English H1 and SEO title follow the owner's ruling; the body is Arabic, RTL.
4. **Names follow the prompt's list.** Places with no Arabic name in the source stay in Latin: Reading, Park Bavli and
   Miriam HaHashmonait. Companies are written in Latin (Hagag Group, Ashdar, Azorim, Shikun & Binui). The searched
   words appear where they fit: رمات أفيف, أحياء شمال تل أبيب, شراء شقة في شمال تل أبيب and أسعار الشقق في شمال تل أبيب.
5. **The buyer from abroad, in words only.**
   - Owning an apartment does not grant residency.
   - A power of attorney goes to a lawyer in Israel.
   - Managing the property remotely.
   - The page adds no new numbers and makes no claim about who is eligible to buy; that stays with the lawyer.

## Notes for the publisher

1. **The link to Rova 4.** The hub links to the Hebrew /north-tel-aviv/rova-4/ with "(بالعبرية)", as links.json requires
   today. When /ar/north-tel-aviv/rova-4/ is live, swap the link as links.json "swap_after_publish" says, and drop the
   marker.
2. **Neve Avivim's decades.** The Hebrew writes "שנות ה-60 וה-70", and the page writes "سنوات الـ60 والـ70" (claim H-02).
   The claim's own wording, "the 1960s and 1970s", would read as "الستينيات والسبعينيات" in Arabic, with no digits.

## Every number

| # | number | claims | context |
|---|---|---|---|
| 1 | 38 | H-09 | الارتفاع، تتقدّم في المنطقة مشاريع جديدة، ومشاريع تاما 38 (الخطة القطرية لتدعيم المباني القديمة، |
| 2 | 16,000 | H-01 | وإعادة البناء)، وتخطيط واسع في حي سدي دوف المخطّط لنحو 16,000 شقة. لذلك لا يكتفي أي دليل جادّ لعقارات |
| 3 | 515 | H-04 | المشروع الأبرز مشاريع Hagag Group في شارع أينشتاين: 515 شقة في ستة مبانٍ سكنية، من بينها EINSTE |
| 4 | 60 | H-02 | وزناً متزايداً. نافيه أفيفيم، التي بُنيت في سنوات الـ60 والـ70 من القرن الماضي، من أكثر الأحياء |
| 5 | 70 | H-02 | تزايداً. نافيه أفيفيم، التي بُنيت في سنوات الـ60 والـ70 من القرن الماضي، من أكثر الأحياء التصاق |
| 6 | 2023 | H-03 | طة للتجديد الحضري. ففي شارع يهودا هناسي مثلاً، صودق في 2023 على مخطط تحلّ بموجبه ثلاثة مبانٍ يصل ار |
| 7 | 14 | H-03 | 2023 على مخطط تحلّ بموجبه ثلاثة مبانٍ يصل ارتفاعها إلى 14 طابقاً وتضمّ 195 شقة محلّ خمسة مبانٍ في |
| 8 | 195 | H-03 | لّ بموجبه ثلاثة مبانٍ يصل ارتفاعها إلى 14 طابقاً وتضمّ 195 شقة محلّ خمسة مبانٍ فيها 80 شقة. مشاريع |
| 9 | 80 | H-03 | فاعها إلى 14 طابقاً وتضمّ 195 شقة محلّ خمسة مبانٍ فيها 80 شقة. مشاريع كهذه تجدّد مخزون الشقق خطوة |
| 10 | 16,000 | H-01 | عمل فيه المطار سابقاً يُخطَّط لحيّ مديني كبير يضمّ نحو 16,000 شقة، واستعمالات مختلطة، ومبانٍ عامة، وح |
| 11 | 3 | G-01, G-03, H-03, H-05, H-06, H-09 | اء شمال تل أبيب: الشمال القديم (بالعبرية)، وهو روفاع 3 غربي ابن جبيرول؛ و روفاع 4 (الشمال الجد |
| 12 | 4 | G-01, G-03, H-04, H-07, H-09 | قديم (بالعبرية)، وهو روفاع 3 غربي ابن جبيرول؛ و روفاع 4 (الشمال الجديد) (بالعبرية)، المنطقة ال |
| 13 | 38 | H-09 | ضري في شمال تل أبيب على ثلاث جبهات. الأولى مشاريع تاما 38 المنفردة في المباني القديمة، وأغلبها في |
| 14 | 2026 | H-04, H-07, H-08, H-10 | في المنطقة. فبحسب أرقام الشركة الصادرة في كانون الثاني 2026، تضمّ هذه المشاريع ستة مبانٍ سكنية فيها |
| 15 | 515 | H-04 | ون الثاني 2026، تضمّ هذه المشاريع ستة مبانٍ سكنية فيها 515 شقة، ومركزاً تجارياً بمساحة نحو 11,400 |
| 16 | 11,400 | H-04 | ة مبانٍ سكنية فيها 515 شقة، ومركزاً تجارياً بمساحة نحو 11,400 م²، ومبنى عاماً بمساحة نحو 3,950 م²، وم |
| 17 | 3,950 | H-04 | ً تجارياً بمساحة نحو 11,400 م²، ومبنى عاماً بمساحة نحو 3,950 م²، وموقف سيارات تحت الأرض يتّسع لـ957 |
| 18 | 957 | H-04 | اً بمساحة نحو 3,950 م²، وموقف سيارات تحت الأرض يتّسع لـ957 سيارة، وتُقدَّر قيمتها الإجمالية بنحو 4 |
| 19 | 4 | G-01, G-03, H-04, H-07, H-09 | لأرض يتّسع لـ957 سيارة، وتُقدَّر قيمتها الإجمالية بنحو 4 مليارات ₪. أما EINSTEIN TOWER، أحد المش |
| 20 | 215 | H-05 | ₪. أما EINSTEIN TOWER، أحد المشاريع في المجمّع، فيضمّ 215 شقة في برج من 28 طابقاً ومبنيين من 13 ط |
| 21 | 28 | H-05 | OWER، أحد المشاريع في المجمّع، فيضمّ 215 شقة في برج من 28 طابقاً ومبنيين من 13 طابقاً فوق قاعدة ت |
| 22 | 13 | H-05 | المجمّع، فيضمّ 215 شقة في برج من 28 طابقاً ومبنيين من 13 طابقاً فوق قاعدة تجارية، وتقدّر الشركة |
| 23 | 2030 | H-05 | قاعدة تجارية، وتقدّر الشركة إنجازه في الربع الثالث من 2030. التصميم المعماري للمهندس موشيه تسور. إ |
| 24 | 2021 | H-06 | نبها يضمّ مشروع Ashdar Einstein، الذي افتُتح تسويقه في 2021، ثلاثة مبانٍ من 8 طوابق فيها نحو 45 شقة |
| 25 | 8 | H-06, H-08 | r Einstein، الذي افتُتح تسويقه في 2021، ثلاثة مبانٍ من 8 طوابق فيها نحو 45 شقة. وتنشط في المنطقة |
| 26 | 45 | H-06 | افتُتح تسويقه في 2021، ثلاثة مبانٍ من 8 طوابق فيها نحو 45 شقة. وتنشط في المنطقة شركات أخرى أيضاً، |
| 27 | 515 | H-04 | NSTEIN TOWER شارع أينشتاين، رمات أفيف في المجمّع كله 515 شقة في ستة مبانٍ سكنية ومركز تجاري بمسا |
| 28 | 11,400 | H-04 | كله 515 شقة في ستة مبانٍ سكنية ومركز تجاري بمساحة نحو 11,400 م²؛ وفي EINSTEIN TOWER وحده 215 شقة، وب |
| 29 | 215 | H-05 | كز تجاري بمساحة نحو 11,400 م²؛ وفي EINSTEIN TOWER وحده 215 شقة، وبرج من 28 طابقاً ومبنيان من 13 طا |
| 30 | 28 | H-05 | حو 11,400 م²؛ وفي EINSTEIN TOWER وحده 215 شقة، وبرج من 28 طابقاً ومبنيان من 13 طابقاً مشروع واسع |
| 31 | 13 | H-05 | STEIN TOWER وحده 215 شقة، وبرج من 28 طابقاً ومبنيان من 13 طابقاً مشروع واسع النطاق يجمع السكن وا |
| 32 | 8 | H-06, H-08 | عار Ashdar Einstein شارع أينشتاين ثلاثة مبانٍ من 8 طوابق ونحو 45 شقة بناء جديد بحجم أقرب |
| 33 | 45 | H-06 | r Einstein شارع أينشتاين ثلاثة مبانٍ من 8 طوابق ونحو 45 شقة بناء جديد بحجم أقرب إلى الحي، يناس |
| 34 | 2023 | H-03 | ل تل أبيب تجديد حضري نشط؛ في شارع يهودا هناسي صودق في 2023 على مخطط لـ195 شقة بدل 80 إمكانات تجدي |
| 35 | 195 | H-03 | حضري نشط؛ في شارع يهودا هناسي صودق في 2023 على مخطط لـ195 شقة بدل 80 إمكانات تجديد واسعة، لكن يج |
| 36 | 80 | H-03 | ي شارع يهودا هناسي صودق في 2023 على مخطط لـ195 شقة بدل 80 إمكانات تجديد واسعة، لكن يجب فحص كل مب |
| 37 | 16,000 | H-01 | دوف غرب شمال تل أبيب، قرب الشاطئ وحي لامد مخطّط لنحو 16,000 شقة إضافة كبيرة إلى العرض على المدى ال |
| 38 | 38 | H-09 | احد تتّسع الفجوة بين شقة قديمة بلا مصعد، وشقة بعد تاما 38، وشقة في مبنى جديد، وشقة حديقة، وبنتهاو |
| 39 | 2026 | H-04, H-07, H-08, H-10 | ة حديقة، وبنتهاوس، وشقة في برج فاخر. في الربع الأول من 2026 بلغت القيمة الوسيطة لصفقات الشقق من 4 غ |
| 40 | 4 | G-01, G-03, H-04, H-07, H-09 | لربع الأول من 2026 بلغت القيمة الوسيطة لصفقات الشقق من 4 غرف (يحسب الإسرائيليون الصالون غرفةً، ف |
| 41 | 5,370,100 | H-07 | ب الإسرائيليون الصالون غرفةً، فهي صالون وثلاث غرف نوم) 5,370,100 ₪ في نافيه أفيفيم ومحيطها، و6,549,400 ₪ |
| 42 | 6,549,400 | H-07 | ن وثلاث غرف نوم) 5,370,100 ₪ في نافيه أفيفيم ومحيطها، و6,549,400 ₪ في بافلي، و8,425,800 ₪ في حي لامد («ت |
| 43 | 8,425,800 | H-07 | 100 ₪ في نافيه أفيفيم ومحيطها، و6,549,400 ₪ في بافلي، و8,425,800 ₪ في حي لامد («تخنيت لامد» في البيانات |
| 44 | 5,229,800 | H-07 | ₪ في حي لامد («تخنيت لامد» في البيانات الرسمية)، مقابل 5,229,800 ₪ في كل تل أبيب يافا. والقيمة الوسيطة س |
| 45 | 2026 | H-04, H-07, H-08, H-10 | ا بسعر المتر، فقد أُغلقت الصفقات في رمات أفيف في منتصف 2026 بمتوسط يقارب 55,000 ₪، وفي رمات أفيف غي |
| 46 | 55,000 | H-08 | أُغلقت الصفقات في رمات أفيف في منتصف 2026 بمتوسط يقارب 55,000 ₪، وفي رمات أفيف غيمل بنحو 51,000 إلى 5 |
| 47 | 51,000 | H-08 | صف 2026 بمتوسط يقارب 55,000 ₪، وفي رمات أفيف غيمل بنحو 51,000 إلى 53,000 ₪، وفي معظم المشاريع الجديدة |
| 48 | 53,000 | H-08 | وسط يقارب 55,000 ₪، وفي رمات أفيف غيمل بنحو 51,000 إلى 53,000 ₪، وفي معظم المشاريع الجديدة في سدي دوف |
| 49 | 70,000 | H-08 | إلى 53,000 ₪، وفي معظم المشاريع الجديدة في سدي دوف نحو 70,000 ₪. وتعكس الفجوات الموقع والطابق والإطلا |
| 50 | 38 | H-09 | كانات التجديد أيضاً: المبنى الذي يتقدّم فيه مشروع تاما 38 أو بينوي بينوي قد يُسعَّر بخلاف مبنى مش |
| 51 | 51,000 | H-08 | ف غيمل بناء راسخ، وطلب مرتفع، وشقق عائلية وجديدة نحو 51,000 إلى 53,000 ₪ للمتر في المتوسط (آب 2026) |
| 52 | 53,000 | H-08 | ء راسخ، وطلب مرتفع، وشقق عائلية وجديدة نحو 51,000 إلى 53,000 ₪ للمتر في المتوسط (آب 2026) الطابق، و |
| 53 | 2026 | H-04, H-07, H-08, H-10 | ة وجديدة نحو 51,000 إلى 53,000 ₪ للمتر في المتوسط (آب 2026) الطابق، والإطلالة، والموقف، وجودة الم |
| 54 | 55,000 | H-08 | هادئ وأخضر وعائلي، ومبانٍ قديمة إلى جانب التجديد نحو 55,000 ₪ للمتر في المتوسط في صفقات رمات أفيف ا |
| 55 | 2026 | H-04, H-07, H-08, H-10 | ₪ للمتر في المتوسط في صفقات رمات أفيف الأخيرة (حزيران 2026)، بحسب الشارع وحالة المبنى وضع التجديد |
| 56 | 60 | H-02 | الضجيج، والصيانة نافيه أفيفيم حي قديم من سنوات الـ60 والـ70، فيه مشاريع تجديد حضري نشطة الق |
| 57 | 70 | H-02 | والصيانة نافيه أفيفيم حي قديم من سنوات الـ60 والـ70، فيه مشاريع تجديد حضري نشطة القيمة الو |
| 58 | 4 | G-01, G-03, H-04, H-07, H-09 | 0 والـ70، فيه مشاريع تجديد حضري نشطة القيمة الوسيطة لـ4 غرف 5,370,100 ₪ (الربع الأول من 2026)، |
| 59 | 5,370,100 | H-07 | 70، فيه مشاريع تجديد حضري نشطة القيمة الوسيطة لـ4 غرف 5,370,100 ₪ (الربع الأول من 2026)، مع علاوة للشقق |
| 60 | 2026 | H-04, H-07, H-08, H-10 | طة القيمة الوسيطة لـ4 غرف 5,370,100 ₪ (الربع الأول من 2026)، مع علاوة للشقق المجدّدة أو في المباني |
| 61 | 4 | G-01, G-03, H-04, H-07, H-09 | قرب من البحر ومن سدي دوف، وطلب عائلي القيمة الوسيطة لـ4 غرف 8,425,800 ₪ (الربع الأول من 2026)، |
| 62 | 8,425,800 | H-07 | البحر ومن سدي دوف، وطلب عائلي القيمة الوسيطة لـ4 غرف 8,425,800 ₪ (الربع الأول من 2026)، بحسب القرب من |
| 63 | 2026 | H-04, H-07, H-08, H-10 | لي القيمة الوسيطة لـ4 غرف 8,425,800 ₪ (الربع الأول من 2026)، بحسب القرب من الشاطئ ومن المشاريع الج |
| 64 | 4 | G-01, G-03, H-04, H-07, H-09 | ة اليركون، وسوق فاخرة، ومشاريع جديدة القيمة الوسيطة لـ4 غرف 6,549,400 ₪ (الربع الأول من 2026)، |
| 65 | 6,549,400 | H-07 | كون، وسوق فاخرة، ومشاريع جديدة القيمة الوسيطة لـ4 غرف 6,549,400 ₪ (الربع الأول من 2026)، وفوق متوسط الم |
| 66 | 2026 | H-04, H-07, H-08, H-10 | دة القيمة الوسيطة لـ4 غرف 6,549,400 ₪ (الربع الأول من 2026)، وفوق متوسط المنطقة في سوق الفخامة ال |
| 67 | 16,000 | H-01 | الحديقة وطريق نمير حي سدي دوف حي جديد مخطّط لنحو 16,000 شقة نحو 70,000 ₪ للمتر في معظم المشاري |
| 68 | 70,000 | H-08 | مير حي سدي دوف حي جديد مخطّط لنحو 16,000 شقة نحو 70,000 ₪ للمتر في معظم المشاريع الجديدة (2026) |
| 69 | 2026 | H-04, H-07, H-08, H-10 | ,000 شقة نحو 70,000 ₪ للمتر في معظم المشاريع الجديدة (2026)، بحسب المرحلة والموقع والتخطيط التسلي |
| 70 | 4 | G-01, G-03, H-04, H-07, H-09 | من البحر والوسط، وشقق قديمة ومجدّدة القيمة الوسيطة لـ4 غرف 6,542,100 ₪ في قسمه الشمالي (الربع |
| 71 | 6,542,100 | H-07 | بحر والوسط، وشقق قديمة ومجدّدة القيمة الوسيطة لـ4 غرف 6,542,100 ₪ في قسمه الشمالي (الربع الأول من 2026) |
| 72 | 2026 | H-04, H-07, H-08, H-10 | طة لـ4 غرف 6,542,100 ₪ في قسمه الشمالي (الربع الأول من 2026)، مع تفاوت كبير بحسب الشارع والمبنى وال |
| 73 | 16,000 | H-01 | والمستثمرون على المدى البعيد، والمقيمون في الخارج نحو 16,000 شقة مخطّطة والبحر على مقربة الارتهان ل |
| 74 | 16,000 | H-01 | جزءاً لا يتجزّأ من نجاح الحي، لأن حياً جديداً بحجم نحو 16,000 شقة لا بدّ أن يعتمد على المواصلات العام |
| 75 | 38 | H-09 | أبيب قد يكون مبنى قديم يبدو عادياً جزءاً من عملية تاما 38 أو بينوي بينوي، لكن ليست كل عملية كهذه |
| 76 | 11,400 | H-04 | اعدة تجارية في مجمّع يُخطَّط فيه مركز تجاري بمساحة نحو 11,400 م²، تزداد أهمية فهم أثر التجارة على الس |
| 77 | 60 | H-02 | يف ب، أما نافيه أفيفيم فحيّ واحد قديم بُني في سنوات الـ60 والـ70، هادئ وأخضر وراسخ. وتتقدّم فيه ف |
| 78 | 70 | H-02 | ما نافيه أفيفيم فحيّ واحد قديم بُني في سنوات الـ60 والـ70، هادئ وأخضر وراسخ. وتتقدّم فيه في السنو |
| 79 | 2023 | H-03 | لأخيرة مشاريع تجديد حضري، مثل المخطط الذي صودق عليه في 2023 في شارع يهودا هناسي لـ195 شقة بدل 80، و |
| 80 | 195 | H-03 | ثل المخطط الذي صودق عليه في 2023 في شارع يهودا هناسي لـ195 شقة بدل 80، ولذلك يجمع بين سوق قديمة را |
| 81 | 80 | H-03 | ذي صودق عليه في 2023 في شارع يهودا هناسي لـ195 شقة بدل 80، ولذلك يجمع بين سوق قديمة راسخة وإمكانا |
| 82 | 515 | H-04 | تذب مشاريع جديدة. ومشاريع Hagag Group فيه مخطّطة لتضمّ 515 شقة في ستة مبانٍ سكنية ومركزاً تجارياً |
| 83 | 11,400 | H-04 | 515 شقة في ستة مبانٍ سكنية ومركزاً تجارياً بمساحة نحو 11,400 م²، ومن بينها EINSTEIN TOWER الذي يضمّ |
| 84 | 215 | H-05 | ساحة نحو 11,400 م²، ومن بينها EINSTEIN TOWER الذي يضمّ 215 شقة في برج من 28 طابقاً ومبنيين من 13 ط |
| 85 | 28 | H-05 | ، ومن بينها EINSTEIN TOWER الذي يضمّ 215 شقة في برج من 28 طابقاً ومبنيين من 13 طابقاً. وإلى جانبه |
| 86 | 13 | H-05 | TOWER الذي يضمّ 215 شقة في برج من 28 طابقاً ومبنيين من 13 طابقاً. وإلى جانبها تنشط في الشارع Ashd |
| 87 | 16,000 | H-01 | ياً: يُتوقَّع أن يضيف حي سدي دوف عرضاً كبيراً يبلغ نحو 16,000 شقة، لكن ذلك لا يعني هبوطاً آلياً في ال |
| 88 | 4 | G-01, G-03, H-04, H-07, H-09 | [SEO description] أفيف ونافيه أفيفيم وبافلي وحي لامد وسدي دوف، أسعار شقق 4 غرف، مشاريع شارع أينشتاين، المواصلات وا |

## Claims used

| claim | statement | source |
|---|---|---|
| G-01 | The Israeli room count includes the living room: '4 rooms' = a living room and 3 bedrooms; '2.5 rooms' has a half room. | convention |
| G-03 | Quarters: 'the first quarter of 2026' = January to March 2026 (Q1, 1-3.2026); 'the fourth / last quarter' = Q4. | convention |
| H-01 | The Sde Dov quarter, on the site of the former airfield in the north-west of the city, is planned for about 16,000 apartments, with mixed uses, public buildings, parks, commerce, hotels and transport. | TLVSD; NC2604 |
| H-02 | Neve Avivim: its first houses were built in the mid-1960s and most of the neighbourhood in the 1970s ('built in the 1960s and 1970s'). | HEWNA |
| H-03 | Urban renewal example in Neve Avivim: on Yehuda HaNasi Street a plan approved in 2023 replaces five buildings with 80 apartments by three buildings of up to 14 floors with 195 apartments. | NC2308 |
| H-04 | Hagag Group's projects on Einstein Street (Ramat Aviv), per the company's January 2026 figures: six residential buildings with 515 apartments, a shopping centre of about 11,400 m2, a public building of about 3,950 m2 and an underground car park of 957 spaces; total value estimated at about ₪4 billion. Architect: Moshe Tzur. | NC2601; NC2410 (older figures) |
| H-05 | EINSTEIN TOWER, one of the projects in Hagag's Einstein complex: 215 apartments in a 28-floor tower and two 13-floor buildings above a commercial base; the company estimates completion in the third quarter of 2030. | DOS (S001, S002, IVS008) |
| H-06 | Ashdar Einstein, on Einstein Street: marketing opened in 2021; three 8-floor buildings with about 45 apartments. | ICE2107 |
| H-07 | Official median deal prices (Tax Authority deals), 4 rooms, first quarter of 2026: Neve Avivim and surroundings ₪5,370,100; Bavli ₪6,549,400; Shikun Lamed (official name 'Tochnit Lamed') ₪8,425,800; the Old North, northern part ₪6,542,100; all of Tel Aviv-Yafo ₪5,229,800. | GOVN |
| H-08 | Prices per m2 in mid-2026: recent deals in Ramat Aviv averaged around ₪55,000 (June 2026); Ramat Aviv Gimel about ₪51,000 to ₪53,000 on average (August 2026); most new projects in Sde Dov around ₪70,000 (2026). | ICE0606; BZ2608; ICE2105 |
| H-09 | Names that carry numbers: TAMA 38 (the national plan for strengthening buildings, תמ״א 38); Rova 3 = the Old North (west of Ibn Gabirol); Rova 4 = the New North and Kikar HaMedina. | Hebrew source; rova-4 facts R1, R3, R11 |
| H-10 | The page was updated in October 2026. | THIS |
