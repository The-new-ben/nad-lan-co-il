# CompoundDecision

The repaired top of an urban renewal compound page, the ~950 pages imported from the government registry, plus a decision tool built from that compound's own registry row. An owner sees what they are likely to get and how many signatures are missing. A buyer sees what to check before buying in the compound. Everyone sees the compound's numbers against its city.

**Version 105 (31.10.2026, Ben's order: fix the government projects and give each one a tool).** Design only, not built and not released. Linear HAD-642. The sample is a real compound, הגפן 8-10 ברמת גן; every number in it comes from the registry file or from a source already accepted in UrbanRenewalHonesty.

## What is wrong today (sample of 80 compound pages, 31.10.2026)

- **The H1 comes after the stage strip and the tools bar** on 47 of 80 pages; on a phone it is not in the first screen. This breaks the intent-first law.
- **The tools bar says "סיור תלת ממדי ברובע" and "הדמיית כדור הארץ שלנו"** on 80 of 80 pages. The first is a blacklisted word, the second is tech talk, and both point to a Sde Dov tour that has nothing to do with Ramat Gan.
- **The video-call card promises "the model, the floors, the view and the published prices"** on 80 of 80 pages. A compound in planning has none of them.
- **The price comparison sets a Ramat Gan compound against Sde Dov towers** 2 to 3.6 km away in another city, with raw SEO names ("ASHIRA - פרויקט אשירה שדה דב תל אביב מחיר").
- **The area counts read 0** in every category, and "אין מקומות בטווח הזה". Iron law 3: an unknown is omitted, never shown as 0.
- **The page body is a median of 276 words**, with no answer paragraph at all.

## The repaired order (phone first)

1. **Breadcrumb**, then the **H1**: "<compound>, <city>: פינוי בינוי". The compound's own address words lead, because people search for the address ("הגפן 8 רמת גן", position 8 to 10 today).
2. **The answer paragraph**, written from the row: the type, the plan and its status, the units today and in the plan, and the sourced timeline line.
3. **One button:** "לקבלת עדכונים על המתחם בוואטסאפ". A link to "בדיקת מתחם".
4. **The tool**, with three tabs (below).
5. **The compound in data:** a plain table. One attribution line under it, no per-row source clutter (owner law 3.10).
6. **The city around it:** the city's registry numbers, then links to the pages that own the head topics.
7. The area map **only if it has places**; a category with no places is not shown.

**Removed from compound pages:** the tools bar (3D tour, Earth flight, designer), the video-call card, and the comparison with projects in another city.

## The tool

**"יש לי דירה כאן"** (owners):
- **Your apartment today:** a slider from 35 to 140 m². The result is a range for the new apartment: the size plus 12 m² (the 2020 policy, with a balcony) up to the size plus 25 m² (the authority calculator's default, within its 0 to 30 range).
- Under 52 m², the policy line reads "עד 25 מ״ר".
- It adds only "חניה, ובדרך כלל גם מחסן" from the same sources. Nothing else is promised.
- **Signatures:** a stepper for how many apartments have signed. It answers with the statute's two thirds of the compound's own count, as an exact fraction: 30 apartments need 20. The two building conditions are shown as text, and nothing claims the majority was reached.
- **Time:** only the sourced line: "בממוצע כ-4 שנים מאישור התכנית ועד ההיתר הראשון, לפי דוח הרשות לשנת 2025". No delivery year is ever computed.

**"שוקלים לקנות כאן"** (buyers):
- **Five checks,** worded for the compound's stage:
  - who the developer is and whether an agreement was signed;
  - how many have signed;
  - what the agreement gives the apartment you are buying;
  - the land-registry extract and any caveat in the developer's favour;
  - an appraiser's value today.
- **Links out:** to the owner pages for costs and for the step-by-step guide, and to the professionals in the city.

**"המתחם במספרים":**
- **The 30 → 78 squares.** The filled squares are today's apartments; the outlined ones are the plan's additions.
- **The compound's multiplier against two benchmarks:** 2.6, against 3.1 (the median of the 45 Ramat Gan compounds with an approved plan) and 4.1 (all 970 compounds in the registry).
- **Its rank** among the city's approved compounds.
- **The plan number as a stamp,** linked to the plan on מבא״ת.

## Data (from `data/renewal-stats.json` and each compound's meta)

- **Per compound:**
  - name, city;
  - status, track (when present);
  - existing and proposed units;
  - plan number and its מבא״ת link;
  - plan year, shown only on an approved plan.
- **Per city:**
  - compounds in the registry, approved, declared on the tax track;
  - units with permits;
  - the multiplier and the median multiplier of the approved compounds;
  - its rank among the 76 localities.
- **Sources:**
  - The registry file, dated (15.8.2026).
  - The authority's 2025 report.
  - The 2020 policy and the authority calculator.
  - The statute (two thirds).
  - All of these are accepted in UrbanRenewalHonesty.
- **Refreshing the registry** from data.gov.il needs Ben's word, because of the 19.8 law against pulling from government sites. Until then the page names the file's date.

## SEO and AI answers

- **Title:** "<compound>, <city>: פינוי בינוי, <N> דירות בתכנית | נדל״ן". It never uses "פרויקטים חדשים", which the city hubs own. Today city queries like "פרויקטים חדשים בצור יצחק" land on compound pages at positions 30 to 90. That is the cannibalization this title stops.
- **Head topics stay with their owner pages.** The tool links to them and never repeats their H1 words:
  - "פינוי בינוי" belongs to /pinui-binui/;
  - "עלויות רכישה" belongs to /apartment-purchase-cost-calculator/;
  - "דייר סרבן" belongs to the glossary.
- **What makes AI engines cite a page:** a direct answer first, numbers in plain HTML text, a data table, and a visible date. That is exactly the paragraph, the table and the attribution line here.
  - Schema: `Place` with `containedInPlace` (the city), and `Dataset` naming the registry and its date.
  - The city comparison numbers are our own computation from the registry. No competitor shows them, and that is what makes them worth citing.
- **Rollout pace:** a pilot of 10 compounds (the most impressions in Search Console), 3 weeks of measurement, then waves of up to 50 compounds a day on Ben's word (the no-mass-change law).

## Untouched

- The 3D project pages:
  - Rainbow, Dimri Yama, Ashira, DUO, H Infinity, Einstein, Kikar Hamedina;
  - every project whose `source` is not `urban_renewal`.
- The stage, the engine and the cone.

## Built from (when built)

- `inc/catalog-plus.php`: the compound card and the page top.
- `inc/project-stage.php`: the top-of-page order.
- `inc/urban-tools.php`: the two-thirds calculator, reused.
- `inc/urban-map-data.php` and `data/renewal-stats.json`: the city numbers.
- `inc/legal-notice.php`.
- New: `assets/urban/compound-tool.js` and `.css`.
