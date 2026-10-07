# sde-dov-prices / ar: translation gate result (HAD-439 Stage A)

Written by Claude (Opus) in this session, under the owner's approval to write here instead of in ChatGPT, from
packets/prompt-sde-dov-prices-ar.md (all 3 messages), packets/sde-dov-prices-ar.json, claims.json, links.json,
align-check.md and docs/content/rova-4-2026-10/i18n-brief.md. The Hebrew source is the live prices page (page 4758, aligned
earlier on 7.10 with 78 edits). Data only: no WordPress writes, no commit, no push.

## The checker's final output

Command (from this folder, PYTHONIOENCODING=utf-8), machine clock 2026-10-07 21:20 UTC:
`python check_translation.py out/sde-dov-prices-ar.html --page sde-dov-prices --lang ar --meta out/sde-dov-prices-ar.meta.txt --peer out/sde-dov-hub-ar.html`

```
== sde-dov-prices/ar | net words 5452 | H2 16 | numbers 318, unmatched 0 | errors 0 | warnings 0 | comparators 16 (live)
  RESULT: PASS
```

Exit code 0. Headings compared live against the 15 Arabic comparator pages plus the Arabic hub (--peer); every internal
link answered GET 200. No banned words, no soft style words, no dashes, no "!", no Hebrew letters, no shortcodes; only the
marker comment.

## Net words

5,452 (checker count; range 4,267 to 6,024, target 5,020). Every section is within 15% of its budget:

| section | words | budget | allowed |
|---|---:|---:|---|
| pr-lead (with the H1) | 160 | 140 | 119 to 161 |
| pr-m2 | 569 | 520 | 442 to 598 |
| pr-gaps | 259 | 230 | 196 to 264 |
| pr-rooms | 456 | 440 | 374 to 506 |
| pr-compounds | 431 | 410 | 348 to 471 |
| pr-sea | 375 | 340 | 289 to 391 |
| pr-records | 349 | 330 | 280 to 379 |
| pr-compare | 385 | 340 | 289 to 391 |
| pr-presale | 340 | 320 | 272 to 368 |
| pr-finance | 342 | 310 | 264 to 356 |
| pr-legal | 396 | 350 | 298 to 402 |
| pr-forecast | 441 | 410 | 348 to 471 |
| pr-offer | 288 | 270 | 230 to 310 |
| pr-investors | 194 | 180 | 153 to 207 |
| pr-faq | 393 | 350 | 298 to 402 |
| pr-abroad | 74 | 70 | 60 to 80 |

## SEO

- title (55 characters, English per the owner's ruling of 28.9.2026): Sde Dov Apartment Prices: per m², Deals and Comparisons
- description (136 characters): أسعار الشقق في حي سديه دوف بتل أبيب: متوسط نحو 83,000 ₪ للمتر، الأسعار حسب عدد الغرف والمجمّع، الصفقات القياسية، والمقارنة مع رمات أفيف.
- url: https://nad-lan.co.il/ar/sde-dov/prices/
- H1 exactly as the packet: Apartment Prices in Sde Dov, Tel Aviv: per m², Deals and Comparisons

## Extra checks (beyond the script)

- Numbers section by section against the Hebrew source: identical multisets in all 16 sections (318 tokens, no additions).
  Counts the Hebrew writes in words stay in words (ثلاث شقق، أربعة عوامل، الصفقات الثماني، ثلاث أسواق، عشرة معايير،
  عقد أو عقدين).
- Claim types kept: 83,000 is an average of sold units; 52,856 is a median of deals (written without «نحو», as the Hebrew);
  75,000 to 85,000 are list prices before financing benefits; 73,200 is a developer's estimate; 11.954 million is a price
  list, not a deal; 150,000 is a forecast. Park Tzameret has no figure; the Centre and the North have no separate average.
- Marker `<!-- NLPG -->` once, right after the first paragraph of the first section.
- Links: 2. The Hebrew page's one link (to the hub, Hebrew, with "(بالعبرية)" until /ar/sde-dov/ is live, per links.json
  swap_after_publish) plus 1 optional extra, /ar/new-projects/ ("المشاريع الجديدة") at the end of the comparison section.
- Room counts are written with digits ("شقة من 2 غرف"), as on the live Arabic Rova 4 page, so each Hebrew digit is kept.
- Prompt-only banned words checked by hand: طبقة (the Hebrew "layers of checks" became «فحوص إضافية»), نموذج (the
  Hebrew "internal economic model" became «حسابات اقتصادية داخلية»), «النظام», تجربة, تقريباً, محرّك (the Hebrew "price
  engines" became «العوامل التي تصنع السعر»): none.

## Cultural choices (5 lines)

1. The page reads as a price briefing for Arab families and investors in Israel and buyers abroad, in the register of the Arab economic press, addressing the reader as «أنتم».
2. Israeli terms are explained once: 4 غرف = صالون وثلاث غرف نوم، شقة من غرفة واحدة (ستوديو)، كفالة قانون البيع (the bank guarantee protecting the buyer's payments)، فترة البِدِك; ש"ח became ₪ and «شواكل» in prose.
3. Typography per the prompt: Western digits, 9.45 مليون ₪, م², every Hebrew range "54,000-57,000" written «54,000 إلى 57,000», Levantine months (كانون الأول، آذار، نيسان، أيار، حزيران، تموز، آب، تشرين الأول), no dashes.
4. Names as the prompt lists them: رمات أفيف، رمات أفيف غيمل، بارك تسامرت؛ FIRST and Hagag Group in Latin; the developer's forecast keeps his name as the Hebrew does (يغئال دمري), and the FAQ keeps "one developer" as the Hebrew FAQ does.
5. The last H2 is a reader's heading («الشراء في سديه دوف من خارج البلاد») instead of the Hebrew "foreign investors and international search words", as the packet asks; the multilingual keyword line and the sources line are not translated.
