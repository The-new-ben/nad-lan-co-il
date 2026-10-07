# sde-dov-hub / ar: translation gate result (HAD-439 Stage A)

Written by Claude (Opus) in this session, under the owner's approval to write here instead of in ChatGPT, from
packets/prompt-sde-dov-hub-ar.md (all 4 messages), packets/sde-dov-hub-ar.json, claims.json, links.json, align-check.md
and docs/content/rova-4-2026-10/i18n-brief.md. The Hebrew source is the live page with align-edits.json applied
(check_translation.hebrew_source). Data only: no WordPress writes, no commit, no push.

## The checker's final output

Command (from this folder, PYTHONIOENCODING=utf-8), machine clock 2026-10-07 21:20 UTC:
`python check_translation.py out/sde-dov-hub-ar.html --page sde-dov-hub --lang ar --meta out/sde-dov-hub-ar.meta.txt`

```
== sde-dov-hub/ar | net words 5981 | H2 17 | numbers 151, unmatched 0 | errors 0 | warnings 0 | comparators 15 (live)
  RESULT: PASS
```

Exit code 0. Headings compared live; every internal link answered GET 200. A second run with
`--peer out/sde-dov-prices-ar.html` also PASSES (no H1/H2 shares its first 4 words with the Arabic prices page).
No banned words, no soft style words, no dashes, no "!", no Hebrew letters, no shortcodes; only the marker comment.

## Net words

5,981 (checker count; range 4,768 to 6,732, target 5,610). Every section is within 15% of its budget:

| section | words | budget | allowed |
|---|---:|---:|---|
| hub-what (with the H1) | 137 | 120 | 102 to 138 |
| hub-history | 262 | 250 | 212 to 288 |
| hub-land | 277 | 260 | 221 to 299 |
| hub-plan | 402 | 380 | 323 to 437 |
| hub-compounds | 382 | 380 | 323 to 437 |
| hub-projects | 651 | 610 | 518 to 702 |
| hub-developers | 227 | 230 | 196 to 264 |
| hub-prices | 620 | 580 | 493 to 667 |
| hub-transport | 272 | 260 | 221 to 299 |
| hub-affordable | 249 | 220 | 187 to 253 |
| hub-invest | 410 | 390 | 332 to 448 |
| hub-legal | 502 | 470 | 400 to 540 |
| hub-faq | 557 | 530 | 450 to 610 |
| hub-summary | 73 | 70 | 60 to 80 |
| hub-planning | 823 | 740 | 629 to 851 |
| hub-guide | 57 | 50 | 42 to 57 |
| hub-links | 80 | 70 | 60 to 80 |

The two link lists sit at the top of their range because each Hebrew-page link carries "(بالعبرية)" (16 of the 24 list links).

## SEO

- title (54 characters, English per the owner's ruling of 28.9.2026): Sde Dov, Tel Aviv: New Projects, Prices and Apartments
- description (144 characters): دليل حي سديه دوف في تل أبيب: نحو 16,000 شقة مخطّطة، المشاريع المعروضة للبيع ومطوّروها، متوسط نحو 83,000 ₪ للمتر، والفحوص قبل الشراء على الخارطة.
- url: https://nad-lan.co.il/ar/sde-dov/
- H1 exactly as the packet: Sde Dov, Tel Aviv: New Projects and Apartments for Sale

## Extra checks (beyond the script)

- Numbers section by section against the Hebrew source: identical multisets in all 17 sections. The only addition is the
  one dunam explanation (1,000 m², allowed once by G-02). Counts the Hebrew writes in words stay in words.
- Claim meanings kept: 2030 is Rainbow's expected last stage, not a contract date; 83,000 is an average of sold units;
  100 m² = 7 to 8.3 million is labelled a calculation; 6,900, 1,500 dunam, 41,000 residents and 80,000 are absent; the
  balcony of the 42-million deal is not added (the Hebrew hub does not give it). The Eshkol hotel cell reads "بلا رقم
  منفصل للفنادق" (claim SDH-06: no separate hotel figure); the Hebrew cell is an empty label.
- Marker `<!-- NLAM -->` once, right after the first paragraph of the first section.
- Links: 26. The 25 of the Hebrew page in place (Hebrew targets carry "(بالعبرية)"; seven project pages and
  /ar/new-projects/ go to their Arabic versions) plus 1 optional extra, /ar/guides/ ("أدلة المشتري") at the end of the
  legal section. The prices link stays Hebrew until /ar/sde-dov/prices/ is live (links.json swap_after_publish).
- Prompt-only banned words checked by hand: طبقة, نموذج, «النظام», تجربة, تقريباً (contains قريباً), محرّك: none.

## Cultural choices (5 lines)

1. The reader is an Arab family or investor in Israel first, a buyer abroad second; the page addresses them as «أنتم» in a warm, assured premium-guide voice, in the register of the Arab economic press.
2. Israeli terms are explained once each in the words Arab citizens use: الدونم (1,000 م²)، 4 غرف = صالون وثلاث غرف نوم، كفالة قانون البيع، فترة البِدِك، الأرنونا، ضريبة التحسين (هيتل هشبحاه)، مسار «ديرا لهسكير».
3. Typography per the prompt: Western digits, 83,000 ₪ and 9.45 مليون ₪, م², Levantine months (أيلول، تموز، آذار، نيسان، شباط), ranges with «إلى», no dashes.
4. Names follow the prompt list exactly (سديه دوف، تسوكي أفيف، نافيه يام، تخنيت لامد، كوخاف هتسافون، مجمع ريدينغ)؛ developers and projects stay in Latin script as the developers write them.
5. The "free consultation" tone and any source or media name are absent; the planning chapter keeps its seven H3s, the quote line and the five-item checklist, and the official-sources list is left out as instructed.
