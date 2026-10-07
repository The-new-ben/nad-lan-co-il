# hub / en: translation gate result (HAD-460 Stage A, 7.10.2026)

Written by Claude in this session, under the owner's approval to write it here instead of in ChatGPT. Data only: nothing published or committed, and no WordPress writes.

## The checker's final output

Command (from this folder, PYTHONIOENCODING=utf-8), run 2026-10-07 19:59 UTC:
`python check_translation.py out/hub-en.html --page hub --lang en --meta out/hub-en.meta.txt`

```
== hub/en | net words 5332 | numbers 89, unmatched 0 | errors 0 | warnings 0 | comparators 6 (live)
  RESULT: PASS
```

Exit code 0. Heading comparators were fetched live: /en/new-projects/, /en/guides/, /en/brokers/, /en/developer-deals/, /en/buy-property-in-israel/ and /projects/hamedina-en/. Every internal link answered GET 200. No soft style words were found.

## Net words

5,332 net words. The packet range is 4,190 to 5,916, and the target is 4,930. Every section is within 15% of its budget:

| section | words | budget |
|---|---:|---:|
| hub-opening | 470 | 420 |
| hub-areas | 666 | 640 |
| hub-life | 359 | 340 |
| hub-anchors | 482 | 460 |
| hub-projects | 611 | 570 |
| hub-prices | 664 | 610 |
| hub-compare | 409 | 370 |
| hub-transport | 269 | 250 |
| hub-fit | 351 | 330 |
| hub-legal | 439 | 410 |
| hub-faq | 423 | 390 |
| hub-abroad | 189 | 170 |

## Extra checks (beyond the script)

- **Numbers.** Each number in each Hebrew section appears in the matching English section, one to one. There are only two differences, both required by the brief:
  - "the 60s and 70s" is written as "1960s and 1970s" (the write_as of H-02).
  - One "3" was added in the room-count gloss "a living room and 3 bedrooms" (G-01).
- **Claim meanings.** All 89 number tokens were checked against what their claim means:
  - 515 always refers to the whole Hagag complex, and 215 always to EINSTEIN TOWER.
  - The medians are whole-apartment prices.
  - The completion date in the third quarter of 2030 is given as the company's estimate.
- **Links.** The page has 21 links:
  - The 18 links of the Hebrew page, each in its place. Every link to a Hebrew page has "(in Hebrew)" after it, outside the link.
  - 3 optional English extras: Kikar HaMedina Towers, Rainbow in Sde Dov, and buying a home in Israel from abroad.
- **HTML.** Only the allowed tags are used. The page has no comments, no div, span or br, and no inline style.
  - The classes come from the Hebrew page: nl-eyebrow, nl-cta, nl-cards, nl-note and nl-hub-guides.
- **Wording.** None of the prompt's banned words appears, including "layer", "the system" and "according to". The text has no em or en dash, no "!", no Hebrew letters and no British spelling.

## Cultural choices (5 lines)

1. **Israeli terms are explained once each, where they first appear:** the room count ("4 rooms" = a living room and 3 bedrooms), TAMA 38, pinui-binui, mamad (safe room), purchase tax (mas rechisha), mas shevach, the Tabu extract, the Sale Law guarantee and the median deal price.
2. **The foreign buyer's angle is added in words only, with no new numbers:**
   - foreign residents can buy, but owning does not give residency;
   - a power of attorney for an Israeli lawyer;
   - managing the property remotely;
   - "buyers living abroad" in the profiles where the Hebrew says "foreign residents".
3. **Search wording is used in natural places:**
   - SEO title and opening paragraphs: "North Tel Aviv real estate" and "Tel Aviv neighborhoods";
   - opening: "buy an apartment in North Tel Aviv";
   - anchors section: "luxury apartments in Tel Aviv";
   - Rova 4 at first mention: Kikar HaMedina with "State Square".
4. **US spelling and US real-estate words:** neighborhood, center, parking garage, move-up buyers, sidewalk, kindergarten, condominium bylaws. Prices are written as ₪5,370,100, ranges use "to", and dates are written as month and year.
5. **The tone is a premium guide, not a warning leaflet.** It is warm and specific, and it addresses the reader directly ("If you are looking to buy..."). It has no caveat chapter and no source names; dates carry the evidence, and the developer's figures are attributed as the company's own.
