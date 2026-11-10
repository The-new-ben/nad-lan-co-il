# /projects/: the needs of a "פרויקטים חדשים" searcher, and what answers each one (10.11.2026)

Owner order, 10.11.2026: every related search Google shows under "פרויקטים חדשים" gets a strong presence on the one page
(text, a tool or a map), built on real research, so the page is the full answer to the whole intent.

## Method (what was measured, by whom, when)

| Layer | What | Where it is |
|---|---|---|
| Result pages read by hand | 14 queries in the owner's Chrome (google.co.il, hl=iw, gl=il), 10.11.2026 15:18 to 15:28: top 10, AI box, related searches, special blocks; 18 winning pages opened and read | `related-deep-2026-11-10.md` |
| Independent re-check | 2 of the 14 ("דירות חדשות עד 1.2 מיליון", "הלוואת קבלן") searched again by a second reader at 17:35: same winners, same AI box shape, same related searches. One difference: "דירות חדשות למכירה" also appeared as a product chip | this file |
| Typing suggestions | 242 calls to Google suggest (the address-bar feed): the head phrase typed letter by letter, 5 seeds with every letter, 56 single seeds on budget, financing, stage, neighbourhood and house type | `suggest-deep-2026-11-10.json` |
| Earlier layers (9.11) | 22 result pages, 1,315 suggestions, 86 related searches, Google Ads monthly volumes | `serp.md`, `autocomplete.md`, `related.md`, `volumes.md` |
| Our own visibility | 90 days of Search Console, query by page, grouped into need families | private, outside the repo |

Limits, said plainly: one day, one browser in Tel Aviv (Yad2 localises to the Tel Aviv area); six of the 14 result pages changed
order between two loads minutes apart; suggest shows wording, not volume; the Ads volumes are from the September and October pulls.

## 1. Same intent or not (the test that decides what lives on /projects/)

Count of top-10 URLs shared with the result page of "פרויקטים חדשים" (practitioners' bar: 3 to 4 shared URLs = one intent).

| Phrase | Shared URLs | Verdict | Where it lives |
|---|---|---|---|
| פרויקטים חדשים על הנייר | 6 of 8 | Same intent | /projects/, full section |
| בית פרטי חדש מקבלן | 4 of 8 | Google answers it with the head pages; almost no page is really about houses | /projects/, a property-type filter and a section once data exists |
| פריסייל תל אביב | 3 (5 sites); Google rewrote it to "פרויקטים תל אביב" | Same as the Tel Aviv query | /projects/, the Tel Aviv list with a presale filter |
| דירות חדשות עד 1.2 מיליון | 3 | Partly shared; the first places go to budget-titled pages and "where can I still buy" articles | /projects/, a budget section (see 3) |
| דירות חדשות עד 1.5 מיליון | 2 (+1 filter variant) | Partly shared, same pattern | /projects/, same section |
| פרויקטים חדשים 80 20 | 2 of 9 | Mostly a different intent: explainers, news, a forum | The list side on /projects/; the explanation on `/developer-deals/` |
| פרויקטים חדשים ברמת אביב | 0 (2 sites) | Neighbourhood intent: neighbourhood-filtered listings win | /projects/ neighbourhood filter; the area page keeps its own topic |
| הלוואת קבלן | 0 of 8 | Different intent: finance explainers by lenders, law firms, brokers, ynet | `/developer-deals/` only (it already holds this H2) |

Consequence: financing and loan EXPLANATIONS do not move into /projects/. `/developer-deals/` owns them and is already first or
second for "מבצעי קבלן". /projects/ carries the LIST side (which projects offer which terms today), a two-line definition of each
term, and a link to the guide. Putting the full explanation on both pages would make two of our pages compete.

## 2. What Google itself shows (the "signal" the owner asked to match)

- **The address bar is city first.** Typing the head phrase, "פרויקטים חדשים" first appears at the 7th letter ("פרויקטי"), together
  with: בתל אביב, ברמת גן, בתל אביב (bare "פרויקטים בתל אביב"), בהרצליה, ברמת השרון, בתל אביב מחירים, בגבעתיים. After the full phrase
  the first non-city completions are "מחירים" (with Tel Aviv) and "על הנייר". Tel Aviv is first on every prefix.
- **The budget ladder, in Google's own spelling:** עד מיליון · עד מיליון שקל · עד 1.2 מיליון · עד 1.3 מיליון · עד 1.5 מיליון ·
  עד מיליון וחצי · עד 2 מיליון · עד 2.5 מיליון · עד 3 מיליון. Carried by five stems: דירות חדשות עד, דירות חדשות למכירה עד,
  דירות חדשות מקבלן עד, פרויקטים חדשים עד, דירה חדשה עד. "דירות עד 1.2 מיליון במרכז" exists; no completion joins a budget to Tel Aviv.
- **Payment terms need a noun.** Bare "20 80" and "80 20" complete to a cosmetics brand and a charity. The living forms:
  קניית דירה 20 80 · דירה מקבלן 20 80 · דירה חדשה 20/80 · פרויקטים 20 80 · פרויקט 20 80 · מה זה מבצע 20 80 · בנק ישראל 20 80.
  Google completes "פרויקטים חדשים 80 20" to "פרויקטים חדשים 20 80": the 20 comes first.
- **The loan family is questions:** הלוואת קבלן מה זה · הסבר · חסרונות · ללא ריבית והצמדה · להון עצמי · 10 90 · 20 80 · בלון · בנק ישראל.
  Also: מבצעי מימון קבלנים · מבצעי מימון דירות · ללא הצמדה למדד תשומות הבניה · מה זה אומר ללא הצמדה למדד.
- **Presale is led by Tel Aviv:** the first completion of "פריסייל" is "פריסייל תל אביב"; then דירות פריסייל תל אביב,
  פרויקטים פריסייל תל אביב, פריסייל צפון תל אביב, and the Latin spelling "presale".
- **Tel Aviv modifiers:** מחירים · צפון · הצפון הישן · ליד הים / על הים · יפו · לב תל אביב · מרכז · דרום · בבלי · יד אליהו ·
  נווה שאנן; rooms: "דירות חדשות בתל אביב 3 חדרים", "2 חדרים". רמת אביב splits into ג, הירוקה, החדשה.
- **"במרכז" is two things:** "פרויקטים חדשים במרכז תל אביב" and "במרכז הארץ". The section must name both.
- **Houses are a family:** בית פרטי חדש למכירה מקבלן · בתים חדשים מקבלן · צמודי קרקע חדשים · קוטג חדש מקבלן.
- **The AI box** appeared on 6 of 14 queries (both budgets, presale Tel Aviv, Ramat Aviv, on paper, the loan), always in one
  shape: a one-line answer; two or three headings with places or projects and "החל מ" prices; where to search; an offer to narrow
  by area, by living or investment, and by side costs (מס רכישה, שכר טרחה, משכנתא). It cites Yad2 most. It never cites nad-lan.
- **"אנשים שאלו גם" was not shown on any of the 14.** The FAQ is therefore built from the question forms in suggest and from the
  AI box's own follow-up offers, not from a question block that Google does not show here.
- **Who wins the budget phrases:** every winner carries the number in its title and H1 (Yad2 "עד 1,500,000 ₪", "עד 1.5 מיליון",
  "1.2"). No list page anywhere carries "1.2", so Google sends that search to Yad2's 1.5 million filter, whose first cards are
  projects priced above 1.5 million. The honest, exact answer does not exist on any list page today.
- **nad-lan on page one:** /projects/ is 9th for "דירות חדשות עד 1.2 מיליון" (still shown with its previous title);
  `/developer-deals/` is first or second for "מבצעי קבלן". Nowhere else among the 14.

## 3. Needs matrix

Monthly volume = Google Ads average where measured (`volumes.md`); "n/m" = not measured. "We have" = `projects-market.json`, 10.11.2026.

| # | The need, in the searcher's words | Evidence | We have | What answers it on /projects/ | Linear |
|---|---|---|---|---|---|
| 1 | "תראו לי פרויקטים חדשים", Tel Aviv first | Head 390; Tel Aviv is the first completion on every prefix; our largest visible family | 564 projects | Photo cards right under the H1, opening on Tel Aviv | HAD-694, HAD-695 |
| 2 | "מה אפשר לקנות ב-1.2 מיליון" | 320 a month, nearly the head; a full ladder in suggest; AI box present; no exact list page exists | Priced: 344. Up to 1.2M: 1; up to 1.5M: 9; up to 2M: 50 | A budget section with Google's ladder as buttons; per budget a one-line honest answer, then cities with "החל מ" prices and a date, then the matching cards; the country map lights up | HAD-697 |
| 3 | "על הנייר / פריסייל", Tel Aviv first | About 1,400 a month for the family; same intent (6 of 8) | 39 presale, 12 in Tel Aviv | A stage strip (פריסייל, על הנייר, בשיווק, בבנייה, אכלוס קרוב, לאכלוס מיידי) and a "what you get at each stage" table; a presale alert | HAD-697 |
| 4 | "בשיווק / בבנייה" | "פרויקטים חדשים בשיווק" 50; "פרויקטים בבנייה / בבניה" is one of our largest visible groups and was missing from the plan | 392 marketing, 52 construction | The same stage strip; both spellings (בבנייה, בבניה) in the text | HAD-697 |
| 5 | "20/80, 10/90, ללא הצמדה": which projects | Suggest family; explainers win the bare term | 64 with a published deal, 20 of them 20/80-style | A deals board filtered by term, the developer's own wording with source and date; a two-line definition per term; link to `/developer-deals/`; "כמה שווה המבצע" on top of the existing indexation tool | HAD-698 |
| 6 | "הלוואת קבלן: מה זה, חסרונות" | 0 of 8 shared with the head | Guide exists (`/developer-deals/`) | Not on /projects/ beyond one line and a link. Strengthen the guide instead | new, on `/developer-deals/` |
| 7 | "במרכז / בצפון תל אביב / ברמת אביב / ליד הים" | Region and neighbourhood chips in suggest; neighbourhood listings win | Neighbourhood on 463 rows; 10+ in רמת אביב | Region tabs (naming both "מרכז תל אביב" and "מרכז הארץ"), neighbourhood chips for Tel Aviv, a "ליד הים" filter, all driving the map | HAD-696 |
| 8 | "מחירים" | "בתל אביב מחירים" is the first non-city completion | 344 priced; city prices from deals data | Price tables by rooms and city, lower on the page | HAD-697 |
| 9 | "3 חדרים / 4 חדרים" | Rooms completions; Madlan's room link block | Rooms on 481 rows | Rooms filter and a room-count link block | HAD-694 |
| 10 | "איזה חברות בונות" | The head AI box is organised by developer; long conversational searches ask it | Developer on all 564 | "לפי חברה" board with counts | HAD-698 |
| 11 | "בית פרטי / צמוד קרקע / פנטהאוז" | 4 of 8 shared; a suggest family; almost no real page | 2 rows; no property-type field | Property-type filter; a section only after the data is collected | HAD-697 (data first) |
| 12 | "מגורים או השקעה", "עלויות נלוות" | The AI box's own follow-up offers | Existing calculators | One row of links to the existing tools under the list | HAD-698 |
| 13 | Rentals ("להשכרה") riding the same words | Suggest | Other pages own it | One line that sends renters to the rentals pages | HAD-697 |

## 4. Rules for writing each section (from the evidence above)

1. Heading = the phrase as Google writes it ("דירות חדשות עד 1.2 מיליון", "פרויקטים חדשים על הנייר", "פרויקטים חדשים 20/80").
2. Under it, the AI-box shape: one honest sentence, then places or projects with "החל מ" prices and a "נכון ל־" date, then the list.
3. Honest inventory is the edge: where the answer is "almost none in the centre", say it, and show where it does exist.
4. Every fact is in the page's HTML. Tools and the map load when reached.
5. No new URL, no redirect. Whether filter states get their own title is the owner's decision (see 5).

## 5. Open decision for the owner

Yad2 takes the first two places on the budget searches with FILTER STATES of one listing page that carry the number in the title
and H1. Our city filter state (`/projects/?city=`) already appears in Google for one city search. Two ways to serve budget and
neighbourhood on one page:
- **A.** Sections with anchors inside the one address, one title for the page.
- **B.** The same page and the same address, but a chosen filter (a budget, a neighbourhood) also changes the title and H1, as Yad2 does.
B matches what wins today; it also creates many indexable variants of the page, which is an indexing decision and stays with the owner.
