# U3 · /en/israel-mortgage-non-residents/ · competitor DNA, verified facts and build spec

Research only (owner order, Ben 25.10.2026). Nothing on the live site was changed; no Linear or Notion item was created.
Prepared 25.10.2026, evening Israel time, by the U3 research lead (Claude Opus 5.5).

Evidence classes: **code** = raw HTML or an official data file read by script; **SERP** = DataForSEO Google organic live advanced,
desktop, English, depth 20, 25.10.2026 20:03 to 20:05 UTC (22:03 to 22:05 Israel; Israel moved to UTC+2 this morning);
**GSC** = Search Console API, sc-domain:nad-lan.co.il, 25.7 to 23.10.2026; **eyes** = read in the owner's Chrome (gmktec);
**primary** = law, regulator or official data; **bank page** = a bank's own page (all undated); **unverified** = kept out of the spec.

Raw files: `C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\raw\u3\` (competitors `c-*.html`, bank pages `b-*.html`,
our pages `ours-*.html`, text extracts in `extract\`, official files in `boi\`: Directive 329 v13 `329_13.pdf`, BoI letter
`201802_en.pdf`, Land Taxation Law `land-tax-law.wiki`, money-laundering order for banks `aml-order.wiki`, SDMX extracts `mrtg.csv`,
`fx_USD.csv`, `fx_EUR.csv`, `fx_GBP.csv`, `boirate.csv`; hashes in `fetch-log-u3.json`). SERP JSON: `..\serp\u3-*.json`, summary
`..\serp\u3-summary.md`. U1 files reused (same day, same folder tree): `raw\u1\boi\` (Directive 329 v12, BoI Q&A `111598`, Directive 451
circular 2694, `mashfix.xls`, `pribmash.xls`). Baseline depth proof: `proof-before.md` (this folder).

---

## 0. Headline findings

1. **The page we call "Hebrew" is English.** `/israel-mortgage-non-residents/` serves an English article (18,831 Latin letters against
   86 Hebrew characters, the Hebrew being site chrome and "more posts") inside `<html lang="he-IL" dir="rtl">` with `og:locale he_IL`
   (code, `ours-he.html`). That is why English queries land there (GSC: "israel mortgage for foreigners" 181 impressions, position 63).
   Publishing `/en/israel-mortgage-non-residents/` as "the English version" while the root stays English creates **two English pages on
   one intent**. Recommended path (owner decision, see 8.1): in the same release, publish the English page at `/en/` and rewrite the root
   page as a real Hebrew page, then pair them with hreflang. Hebrew demand exists (Google Ads, Israel, Hebrew): "משכנתא לתושבי חוץ" 40 a
   month, "משכנתא לעולים חדשים" 30, "משכנתא לעולה חדש" 30, "משכנתא לתושב חוץ" 10. No redirect, no noindex. The same mislabel sits on three
   more root pages with English content and `lang="he-IL"`: `/israel-purchase-tax-foreign-residents/`, `/buy-property-israel-foreign-buyers/`,
   `/buying-real-estate-israel-foreign-investor/`; these three also carry hreflang tags that point to the `/new-projects/` cluster, not
   to themselves (finding only).
2. **Our current page contradicts itself.** The opening paragraph uses August 2026 rates and the 21.10 exchange rate, while the meta
   description, two tables and two FAQ answers still say prime 5.25%, Bank of Israel rate 3.75% and "next decision 6 July 2026". It also
   says the 75% cap is for an "Israeli resident"; Directive 329 says citizen. Google's US AI overview for "israel mortgage for non
   residents" cites our page anyway (for the track list and the one-third fixed rule).
3. **Google shows an AI overview on all 9 queries**, and it repeats wrong numbers taken from the ranking pages: payment cap "40%" or
   "33% to 40%" (the legal cap is 50%), prime "5.0%" (it is 4.75%), VAT "17%" (18%), purchase tax "8% up to roughly 5 million" (the
   bracket is ₪6,055,070), LIBOR (discontinued). A page that is correct and dated has room to become the cited source.
4. **Mizrahi-Tefahot's English Q&A is #1 on 6 of 9 SERPs with 974 words, no date and no schema**, and it states a 40% payment cap.
   Bank and organisation authority (Mizrahi, Nefesh B'Nefesh, Discount, Bank of Israel) beats depth on this SERP. The deepest page is
   Semerenko (4,324 words, updated 24.10.2026).
5. **Only one page (Gottlib, a law firm) explains that Directive 329 turns on citizenship.** Nobody quotes the Bank of Israel's own
   answer that a foreign resident's first home is "necessarily" an investment home (Q&A 2.4), nobody has the rule for mixed buyers
   (weighted by share, Q&A on joint buyers), and nobody cites the foreign currency exemption from the two-thirds variable cap (s.12.3).
6. **Nobody combines the two rulebooks**: the Bank of Israel sizes the loan by citizenship, the Tax Authority sizes the purchase tax by
   residency. On a ₪4,000,000 home the cash to close is ₪2,344,610 for a non-citizen, ₪1,344,610 for an Israeli citizen living abroad
   (75% loan, but 8% tax) and ₪1,034,716 for a new oleh resident in Israel (our arithmetic on the verified caps and brackets, 8.4 T5).
7. **Nobody publishes the Bank of Israel's average rates by track with the month**, and nobody has the average on foreign currency
   housing loans (4.86% in August 2026) or its share of volume (0.1%).
8. **Demand is long tail and split across intents.** Google Ads monthly volumes are small (US: "israel mortgage rates" 70,
   "israel mortgage calculator" 40, "mortgage in israel" 30; Israel, English: "israel mortgage calculator" 260, "israel prime rate" 110,
   "mortgage in israel" 70, "mashkanta" 50). The page has to own the head question, the English calculator and the "rates today" intent
   together. Spanish (83 impressions), Italian (12) and Portuguese searchers also land here.
9. **The only rival calculator in English (Israel Property Hub) has four sliders and says prime is 4.5%.** No rival sets the loan cap by
   status, tests the payment against income in the buyer's currency, stresses the exchange rate, or answers "what can my cash buy".

---

## 1. Intents, keyword set and ownership

### 1.1 Intent map

| # | Intent (what the searcher wants) | Queries (GSC 90 days impressions@position; Google Ads monthly volume) | Owner URL |
|---|---|---|---|
| I1 | Can I get an Israeli mortgage as a foreigner, and how much | israel mortgage for foreigners 181@63 · israel mortgage for non residents (SERP) · mortgage in israel 10@94; Ads US 30, IL-en 70 · mortgages in israel 1@73 · hipoteca en israel para extranjeros 83@77 · mutuo in israele per stranieri 12@63 · prêt immobilier israël étranger 1@82 · financiamento imobiliário israel estrangeiro 1@80 · bank of israel mortgage ltv first home 75% official 1@9 | **/en/israel-mortgage-non-residents/** |
| I2 | Today's rates | israel mortgage rates (Ads US 70, IL-en 90) · israel prime rate (IL-en 110) · bank of israel interest rate (IL-en 90) · PAA "What are the current interest rates for Israeli mortgages?" on 6 SERPs | same page (rates section and strip) |
| I3 | A mortgage calculator in English | israel mortgage calculator (IL-en 260, US 40) · related search "Israel mortgage for foreigners calculator" | same page (the calculator) |
| I4 | Mortgage for olim | mortgage for olim israel (SERP) · zakaut mortgage (related search) · משכנתא לעולים חדשים 30 (Hebrew) | same page, one section (no new URL) |
| I5 | Documents, bank account, signing from abroad, approval time | PAA "Can I open a bank account in Israel as a non-resident?", "Which banks allow non-resident accounts?" · mashkanta israel english 3@49 | same page |
| I6 | The buying process from abroad | buying apartment in israel from usa / uk / abroad 153@56 · how to buy an apartment in israel 121@77 · buying property in israel from usa 54@59 · comprar apartamento em israel sendo estrangeiro 201@62 | **/en/buy-property-in-israel/** |
| I7 | Purchase tax for foreign residents | (SERP "purchase tax israel foreign resident") | /israel-purchase-tax-foreign-residents/ (English content at the Hebrew root, see finding 1) |

### 1.2 Ownership split (mortgage vs buying process), so they never compete
- **/en/israel-mortgage-non-residents/** owns financing: loan caps by status, income test, tracks, rates, foreign currency loans,
  documents and account for the loan, approval timeline, signing from abroad, olim loan rules, the calculator. It shows purchase tax
  only as one line inside "cash to close" and links out. It has **no** step-by-step buying process (offer, lawyer, due diligence,
  registration); it links to the buying page with the anchor "how to buy a home in Israel from abroad".
- **/en/buy-property-in-israel/** (today a family-home decision guide, 6,168 words, no mortgage section; FAQ "Will an Israeli bank fund
  the purchase?") keeps a two to three sentence financing paragraph and that FAQ answer short, both linking to the mortgage page with
  the anchor "Israeli mortgage for non-residents". It should not add rates, LTV tables or a calculator.
- **Root English pages that overlap** (finding only, no change in this task): `/buy-property-israel-foreign-buyers/` mentions
  "mortgage" 11 times, `/buying-real-estate-israel-foreign-investor/` 18 times. When they are next edited, their mortgage paragraphs
  should shrink to a summary plus a link to the new page.
- **URL word audit** (`tools/gsc/url_word_audit.py`, 4,598 URLs, 25.10.2026): token `mortgage` is held by 18 URLs, **none under /en/**;
  `non` is held only by `/israel-mortgage-non-residents/`; `residents` by that page and `/israel-purchase-tax-foreign-residents/`. The
  new slug repeats no word inside itself. Under the owner's reading (same path in another language = the same page), the slug is clear.

### 1.3 Keyword placement for our page
Head term "Israel mortgage for foreigners" in the title, the first words of the answer paragraph and one H2; "non-residents" in the H1
and the slug; "Israeli mortgage calculator" in the calculator H2; "mortgage rates in Israel" in the rates H2; "olim" and "aliyah" in
one H2; "mashkanta" once in the answer area and in the glossary. Spanish, Italian and Portuguese searchers are served by x-default (8.1).

---

## 2. SERP snapshot (25.10.2026, 20:03 to 20:05 UTC)

DataForSEO task ids: IL foreigners `10252003-2646-0139-0000-2f19e2c92266` · US foreigners `...-5adc58344097` · UK foreigners
`...-058e453cbd39` · IL non residents `...-8e00a3ccf380` · US non residents `10252005-...-7292edef4706` · IL mortgage in israel
`...-c565e8d5e97d` · US mortgage in israel `...-8372d96bae6e` · IL olim `10252005-...-f8275df280ac` · US buying from usa `...-6a4814bd3f9b`.
**nad-lan.co.il is not in the top 20 of any of the nine.** It is cited once, inside the US AI overview for "israel mortgage for non residents".

### 2.1 "israel mortgage for foreigners"

| # | Israel (gl=IL) | United States | United Kingdom |
|---|---|---|---|
| 1 | Mizrahi-Tefahot, Q&A for new immigrants | Mizrahi-Tefahot Q&A | Mizrahi-Tefahot Q&A |
| 2 | Nefesh B'Nefesh, types of mortgages | Semerenko, Mortgages for foreigners | Semerenko |
| 3 | Discount Bank, mortgage (international private banking) | Nefesh B'Nefesh, types | Nefesh B'Nefesh, types |
| 4 | Semerenko | welcome-israel.com | wise.com, buying property as a UK foreigner (26.2.2026) |
| 5 | First Israel Mortgages (home page) | Noam Homes (updated 20.10.2026) | Buyitinisrael, mortgage from abroad |
| 6 | Noam Homes | First Israel (home page) | Noam Homes |
| 7 | Even Sapir, mortgage rates 2026 | Buyitinisrael | IsraelStart, 2026 guide |
| 8 | Buyitinisrael | Ynet News, "Before you borrow from your bank outside Israel" (17.8.2026) | First Israel |
| 9 | Bank of Israel, interest rate comparisons, housing loans | homeinisrael-il.com FAQs | welcome-israel.com |
| 10 | financim.co.il | IsraelStart | Discount Bank |
| 11 to 19 | mortgageisrael.com, gov.il olim benefits (2021), welcome-israel, israelpropertyhub, aliyahnet, creditcare, do-israel, First Israel aliyah, israelhomes.net | aliyahnet, lendabroad, sandsofwealth, Discount, gov.il, ronkin-list, YouTube, scoutrbot, aliyahadvisors | lendabroad, ronkin-list, gov.il, Ynet, aliyahnet, mortgageisrael, aliyahadvisors, YouTube, homeinisrael-il |

### 2.2 Other head queries (top 10)
- **"israel mortgage for non residents", IL:** Mizrahi · Semerenko · Walty (fresh, 6.10.2026) · financim · NBN types · Buyitinisrael ·
  Gottlib (law firm, Directive 329) · Noam Homes · First Israel blog "More Financing Than You Think" (10.7.2026) · bauhouse.
- **Same, US:** Mizrahi · Semerenko · welcome-israel · Buyitinisrael · IsraelStart · NBN types · Noam Homes · homeinisrael-il ·
  sandsofwealth · israel-mortgage-pro.
- **"mortgage in israel", IL:** NBN types · Mizrahi · Discount · First Israel · Altshuler law · BoI comparisons · NBN "Israel vs the US" ·
  mortgageisrael · (local pack) · Semerenko · gov.il mortgage registration (Hebrew).
- **Same, US:** NBN types · Mizrahi · Semerenko · NBN vs US · aliyahnet · Buyitinisrael mortgage types · welcome-israel · Discount ·
  Noam Homes (twice) · BoI comparisons at 11.
- **"mortgage for olim israel", IL:** NBN mortgage benefits (10.5.2026) · mortgageisrael olim · Mizrahi · gov.il olim benefits · Gottlib ·
  Semerenko olim guide (16.10.2026) · easyaliyah · Buyitinisrael olim benefits · NBN "when to take a mortgage" · First Israel aliyah.
- **"buying property in israel from usa", US (for the split):** Buyitinisrael podcast on US tax · immoisrael · jjlaw "mortgage process
  Israel vs US" · LinkedIn · IsraelStart · lawoffices.co.il · mfreg taxes · Levin law · Quora · mytelavivrealestate. Our
  `/en/buy-property-in-israel/` is not in the top 20.

---

## 3. What Google shows

### 3.1 AI overview (present on all 9; summary, not quoted)
- **Foreigners (IL, US, UK):** foreigners can borrow from major Israeli banks, typically up to 50% (75% for Israeli first-home buyers and
  olim); rates "4% to 5.5%" (IL) or "4% to 6.5%" (UK); terms 20 to 30 years; tracks fixed, CPI, prime ("currently 4.75%" in the IL
  answer); mandatory life and property insurance; documents: passport, income proof, home-country credit report, bank statements,
  contract; remote process via adviser and lawyer, signing by Zoom, consulate or power of attorney; approval "48 hours to a couple of
  weeks" (IL) or "4 to 8 weeks" (US). UK answer adds foreign currency loans as a hedge and a "UK citizen" angle.
- **Non residents (IL):** 50% / 75%; "4.5% to 6.5%"; **"payments generally cannot exceed 40% of net income"** (from Mizrahi); banks named:
  Hapoalim, Leumi, Mizrahi, Discount, FIBI; ends by asking: citizen or foreign national, first home or investment, aliyah planned.
  **Non residents (US):** PTI "33% to 40%"; tracks section **cites nad-lan.co.il/israel-mortgage-non-residents/**; documents incl. ishur ekroni.
- **Mortgage in Israel (IL):** multi-track; **"benchmark mortgage prime rate stands at 5.0%"**; fixed unlinked "4.7% (15 years) to 4.85%
  (30 years)" and CPI fixed "3.15% to 3.3%" (both from Even Sapir); one-third fixed; terms to age 80 to 85. **(US):** LTV by status table,
  tracks incl. foreign currency loans "using LIBOR plus a fixed margin".
- **Olim (IL):** zakaut loan for 15 years after the oleh certificate, "up to 200,000 NIS", up to 30 years, "around 3% to 4.5%", no
  prepayment penalty, points system, teudat zakaut via a mortgage bank; olim LTV 75%.
- **Buying from USA (US):** no residency needed; purchase tax **"8% up to roughly 5 million ₪"**, **"17% VAT"**, arnona example, agent 2% +
  VAT, lawyer 0.5% to 1.5% + VAT.
- **AI overview sources (union):** noamhomes.com (most cited), firstisrael.com (home, blog, FAQ), mizrahi-tefahot.co.il (Q&A, mortgages),
  nbn.org.il (3 pages), buyitinisrael.com, israelstart.com, evensapir.co.il, israelpropertyhub.com (calculator), walty.co.il,
  gottlibfirm.com, ronkin-list.com (2), israelhomes.net, mortgageisrael.com, discountbank.co.il, wise.com, homeinisrael-il.com,
  israel-mortgage-pro.com, bhii.co.il, epsteinlaw.co.il, altshuler-law.co.il, ynetnews.com, israfinance.com, an Instagram reel, a Facebook
  group, two YouTube videos, **nad-lan.co.il** (US non residents only).
- **Errors in the AI overviews that our page can correct with primary sources:** payment cap 40% / 33 to 40% (Directive 329 s.5: 50%);
  prime 5.0% (4.75%); VAT 17% (18%); "8% up to roughly 5 million" (₪6,055,070); LIBOR (discontinued); "up to 200,000 NIS" zakaut
  (unverified, no official figure found today); unsourced rate ranges and approval times.

### 3.2 People also ask (union, deduplicated; how many of the 9 SERPs showed it)
Which bank in Israel is best for foreigners? (6) · What are the current interest rates for Israeli mortgages? (8, several wordings) ·
What is the minimum down payment required for a mortgage in Israel? (5) · Do Jews pay interest on mortgage loans? (4) · Can a US citizen
buy a home in Israel? (3) · Can foreigners buy property in Israel? (2) · Can I open a bank account in Israel as a non-resident? ·
Which banks allow non-resident accounts? · Which foreign banks are operating in Israel? · Can I get a mortgage from a foreign bank? ·
How much would I pay in monthly mortgage payments for a $500,000 loan for 30 years? · How much do you have to earn to qualify for a
$200,000 mortgage? · How much would a 100,000-pound mortgage cost per month? (2) · What's the minimum down payment for a $300,000 house? ·
Can an UK citizen buy property in Israel? · Who has the lowest mortgage rates in the world? · How much is an average house in Israel? (2) ·
Are real estate prices dropping in Israel? · Is it cheaper to live in Israel or the US? (2) · Can anyone get a sharia compliant mortgage? ·
salary questions on the olim SERP (top 1%, doctors, good salary). PAA answers were not expanded in the API output (absent).

### 3.3 Related searches (union)
Israel mortgage for foreigners calculator · Israel mortgage for foreigners interest rate · Best israel mortgage for foreigners · Israel
mortgage rates · Mortgage Israel calculator · First Israel mortgage · Mortgage calculator · Zakaut mortgage · Israel prime rate · Israel
bond calculator · Cheapest mortgage in israel · Best mortgage in israel · Mortgage meaning · Israel mortgage for non residents calculator ·
Zakaut mortgage for olim israel · Mortgage for olim israel calculator · Olim mortgage · Buying property in israel from usa tax / calculator.

---

## 4. Competitor DNA and why each ranks

Counts from raw HTML as Google gets it (no scripts run); words = visible words in main text (code).

| Page (rank seen) | Title / H1 | Words · updated · schema | Structure and data | Calculator | Errors and gaps | Why it ranks |
|---|---|---|---|---|---|---|
| **Mizrahi-Tefahot Q&A** (#1 on 6 of 9) | "All you need to know about the Mortgage but were too overwhelmed to ask!" / "New immigrant? All you need to know about the Mortgage" | 974 · no date · no schema | 10 questions: olim get 75% "instead of 50% as a foreign citizen" (if citizen or "entitled to Israeli citizenship"); 75/70/50; olim state loan "up to two hundred thousand shekels", up to 30 years; income from Israel or abroad incl. investment income; prime limited to two thirds; process: approval in principle, then contract, then collateral; "the bank is legally obligated to check the origins of your funds"; life insurance a prerequisite; service in English, French, Spanish, Russian | none | PTI "40%" (329 says 50%); "up to 8%" purchase tax (8% and 10%); prime-only framing of the variable cap; no date | Largest mortgage bank, entity authority; plain answer to the citizen/foreigner question; English bank page |
| **Semerenko Group** (#2 to #4) | "Mortgages In Israel For Foreigners: Rates And Rules" / "Israel Mortgages in 2026: The Rules Behind the Rates" | 4,324 · 24.10.2026 · Article, FAQPage (5), Dataset, Organization with licence credential | Quick answer; 14 question H2s (pre-approval, income, foreign income, down payment, documents, appraisal, tracks, risks, rate moves, refinancing, timing, signing risk, checklist, Hebrew terms); one 7-row track table with fees and limits; worked examples (₪3M at 75% and 50%; appraisal gap ₪150,000; +0.25 point on ₪1.5M = ₪217 a month); prime 4.75%; zakaut "average CPI fixed rate minus 0.5 points, capped at 3%"; sources list; broker licence | none | non-residents "about 50% in practice (sometimes less)" without the citizenship rule; no average rates by track; FX exceptions only as "ask the bank"; says the BoI cut on "1 September 2026" (SDMX shows 3.25% in force from 3.9.2026) | Fresh date, depth, FAQ schema, hub-and-spoke internal links, named licence |
| **Nefesh B'Nefesh, types of mortgages** (#1 to #3) | "A Guide to Different Types of Mortgages in Israel" | 865 · modified 18.1.2022 · Article | Shekel prime, madad, foreign exchange (LIBOR), fixed loans; guest post by Mortgage Israel | none | LIBOR; "fixed loans up to 20 years" (30 years allowed); stale | Aliyah organisation authority; exact topic title |
| **Noam Homes** (AI overview lead source; #5 to #8) | "Can Foreigners Buy Property in Israel? 2026 Guide" | 1,681 · 20.10.2026 · BlogPosting | Quick answer; Tabu vs ILA; tax table (8% / 10%) with ₪3M and ₪7M examples; cost table (8 rows); mortgage bullets (50%, one-third fixed, 20 to 25 years for non-residents, Israeli account required, documents); steps; taxes after buying; Efrat and Gush Etzion; 8 FAQs in text; "Last verified October 2026" | none | mortgage section generic; FAQ not marked up | Fresh, list-shaped quick answers the AI overview can lift |
| **Buyitinisrael** (#5 to #8) | "Can I Get a Mortgage in Israel if I'm Abroad?" | 545 · 4.10.2025 · Breadcrumb | Remote process; signing by Zoom, branch or power of attorney; "up to 50%"; use a broker; "a few weeks" | none | thin | Anglo niche authority; title is the exact question |
| **welcome-israel.com** (#3 to #16) | "Mortgage in Israel: Rates, Interests and Tips for Foreigners" | 1,918 · 6.11.2023 · Article | Translated from Russian; "repatriates" | none | many errors (fee "up to €15", "45% US dollar exchange rate" loan parts, "75% for non-residents" in one place) | Exact-match title only |
| **First Israel Mortgages** (home #4 to #8; blog in AI overview) | home / "More Financing Than You Think" (10.7.2026) | 1,221 home; blog 1,407 | Blog: an Israeli citizen living abroad buying a first home may get 75%; someone "not yet an Israeli citizen but intends to make aliyah within the next two years may also qualify" for 75%; bridge loans for upgraders; non-bank lenders up to 85% | home page widget (not read; script-built) | aliyah-intent claim not in the directive text | Broker brand, long-standing domain |
| **Even Sapir, rates** (#7 IL; AI overview rates source) | "Mortgage Rates in Israel 2026 \| Compare Every Track" | 2,858 · 12.10.2026 (page says "Updated July 9, 2026") · Article, FinancialService | Rates table by track and term (15/20/25/30 years), "Source: Bank of Israel benchmark data, updated 2026" | none | prime shown 4.75% on a page "updated July 9" when prime was 5.0% to 5.25% | The only rates-by-term table in English |
| **Walty** (#3 IL non residents) | "Mortgage in Israel for Non-Residents \| Walty" | 1,369 · reviews "as of 6 October 2026" · WebPage; hreflang en, fr, it, ru, uk | Four buyer profiles (abroad, Israelis overseas, aliyah or return, home vs investment); "combined financing of up to 85%" with non-bank credit; documents by theme; 5-step process; 8 FAQs | Hebrew client area shown as a picture | no numbers on LTV by status | Fresh, five languages, review counts |
| **Israel Property Hub calculator** (AI overview source; #14 to #18) | "Israeli Mortgage Calculator in English (2026)" | 581 · no date · WebApplication, FAQPage (8) | Sliders: price, down payment, term, rate; outputs monthly, loan, total interest | yes, single rate | "prime is currently 4.5%" | Exact match for "israel mortgage calculator english" |
| **Gottlib law firm** (#5 to #7 IL) | "Mortgages for Olim and Foreign Residents in Israel" / "The number that decides your mortgage is not your income. It is your citizenship." | 1,062 (EN) · "updated July 2026" · LegalService, FAQPage (3); hreflang he, en, fr, de | Directive 329 definitions; "₪500,000 difference on a ₪2,000,000 property, decided by a date"; time the contract to your status; 50% income cap; source of funds; FX conversion clause | none | no rates, no tool | The only page with the legal mechanism |
| **Bank of Israel, interest rate comparisons** (#6 to #11) | official page with a Power BI report | 14 words in HTML (eyes: per-bank track rates and IRR) | Per-bank rate by track and portfolio IRR | report | **English report's last period is 31.10.2025** (eyes) | Regulator authority |
| **Discount Bank** (#3 IL, #8 to #14) | "mortgage \| Discount" | 2,092 · no date | Rules: 30 years, 75/70/50 ("applies only to Israeli residents"), value = lower of price and appraisal, one-third fixed, two-thirds variable, PTI 50% legal and one third in practice; tracks; approval in principle in 3 stages; later documents: appraisal, life and property insurance, mortgage deeds, notarized documents; named English-speaking advisers | none | "residents" instead of citizens | Bank authority, clean rules text |
| **Ynet News, Noah Sander** (#8 to #14, 17.8.2026) | "Before you borrow from your bank outside Israel read this" | 1,291 | "Foreigners can get the same mortgage rates as Israelis"; 20 to 30 year fixed tracks; 50% with "exceptions" up to 75% for intending olim | none | claims not sourced | News domain |

Also read: Mizrahi International Mortgage Center (`/en/mortgages/`, bank page: shekel mortgages to international clients, loans up to 30
years, "up to 50% of the property value", fixed or variable); Bank of Jerusalem non-resident account page (8.4 T7); financim (2025),
mortgageisrael.com, NBN "Israel vs the US" (2021); IsraelStart serves a French home page to a plain fetch (content built by script).

**Why the SERP looks like this:** (1) entity authority wins first places (two banks, an aliyah organisation, the regulator); (2) exact
question titles win the middle; (3) fresh broker guides with dates, FAQ markup and quick answers feed the AI overview; (4) depth alone
(Semerenko) reaches #2 to #4 but not #1. Our page has to add authority signals it can actually earn: primary sources linked line by line,
a named licensed author, dated data blocks refreshed monthly, unique official numbers nobody else shows, and a calculator people use.

---

## 5. Union checklist and the gaps nobody covers

### 5.1 Union (everything any ranking page has)
Loan caps 75/70/50 · non-resident 50% · olim 75% · citizenship as the test (Gottlib) · payment-to-income 50% legal, one third in practice
(Discount, Semerenko) · one-third fixed, two-thirds variable · prime = BoI rate + 1.5 · track table with risks and fees · foreign currency
loans as a hedge · value = lower of price and appraisal · approval in principle before signing · documents list · source of funds checks ·
power of attorney, consulate, apostille · Israeli bank account · life and property insurance · remote process · broker or direct · approval
time · refinancing and early repayment fees · Hebrew glossary · worked examples · cost table · purchase tax 8% / 10% · non-bank top-up to
85% · 30-year term · olim state loan (zakaut) · bridge loans for upgraders · a single-rate calculator · sources list · visible dates ·
FAQ markup · reviews and named advisers · multiple languages.

### 5.2 Gaps nobody covers (each is a reason for us to outrank)
1. Bank of Israel average rates by track for the latest month, dated (August 2026) and by term (September 2026 reporting month).
2. The average rate on foreign currency housing loans (4.86%, August 2026) and its share of volume (0.1%).
3. The Bank of Israel's own answer: a foreign resident's first home is "necessarily" an investment home, 50% (Q&A 2.4).
4. Mixed buyers: the cap is weighted by each buyer's share when the Tax Authority treats them as separate buyers (Q&A, joint buyers).
5. The two rulebooks side by side: citizenship for the loan, residency for the tax (Israeli citizen abroad: 75% loan, 8% tax).
6. The foreign currency exemption from the two-thirds variable cap for foreign residents (Directive 329 s.12.3) and its portfolio condition.
7. The income test computed in the buyer's own currency at the Bank of Israel rate of the day.
8. What a 10% move in the shekel does to the payment in dollars, euros or pounds.
9. "What can my cash buy" by status (price from cash, including tax and fees).
10. Directive 451 rights: a decision on approval in principle within 5 business days (7 in predefined cases), the document list given with
    it, three uniform baskets in every approval, an outside insurance policy allowed with a 14-day answer, a listed appraiser's report
    usable for 90 days.
11. The know-your-customer rule for foreign residents (passport plus a second photo ID; source of funds; connection to Israel; foreign
    public figure question) and who may identify you face to face abroad (an Israeli lawyer, an Israeli consul, an apostille authority).
12. The Bank of Israel letter that an oleh certificate counts as an ID for 30 days from issue when opening an account.
13. The legal rule that a bank may not unreasonably refuse a shekel current account with a positive balance.
14. The next rate decision date (23.11.2026) and the Bank of Israel's October forecast.
15. Banks' own English pages summarised side by side, with what each actually says.
16. Prices in shekels with conversions labelled by the Bank of Israel rate and its date.
17. Correct, dated prime (4.75% since 3.9.2026), where rivals and the AI overview say 4.5% or 5.0%.

---

## 6. Verified facts (primary unless marked), with sources and dates

| Fact | Value | Source (date read) |
|---|---|---|
| Directive 329 version | (13) 06/26 | `https://www.boi.org.il/media/ez4npagt/329.pdf` (code, 25.10.2026) |
| Loan to value caps | single home 75% · replacement home 70% · investment home 50% | 329 s.2 |
| Who gets "single home" | a home that is the buyer's only home in Israel and the Area (Land Taxation Law s.9), bought by an **individual Israeli citizen**; "replacement home" likewise; "investment home" = any home that is neither; "foreign resident" = anyone who is not an Israeli citizen | 329 s.1 definitions |
| "Israeli citizen" (as 329 defines it) | Land Taxation Law s.16A(a)(1) to (1b): (1) registered or required to be registered in the Population Registry; (1a) an individual who is an Israeli resident; (1b) a person entitled to make aliyah under the Law of Return who is a resident of the Area | 329 s.1; Land Taxation Law, Wikisource (code, 25.10.2026) |
| Household counted as one buyer | the buyer and spouse (unless living permanently apart) and children under 18 (unless married) count as one buyer for the single-home test | Land Taxation Law s.9 |
| BoI's own answer for foreigners | "single" and "replacement" homes are defined only for an Israeli citizen, so a home bought by a foreign resident "is necessarily an investment home" with a 50% cap | BoI Q&A on Directive 329, q.2.4 (update 4.12.2012), document dated 8.2.2026 / 10.5.2026 (code) |
| Joint buyers of different status | follow the Tax Authority's practice; if they are separate buyers for tax, the cap is the average weighted by each buyer's share (e.g. 50/50 of 75% and 50% = 62.5%, our arithmetic) | same Q&A (update 17.7.2014) |
| BoI on interpreting "citizen" | BoI adopts the Land Taxation Law definitions as written and declines to interpret them | same Q&A (update 4.12.2012) |
| Payment to income | at most **50%** of disposable income; above 40% the loan carries a 100% risk weight | 329 s.5, s.6 |
| Disposable income | net income minus fixed commitments running more than 18 months (Annex A) | 329 Annex A (via U1, `329_12.txt`) |
| Variable share | variable part at most **66.66%** of the loan | 329 s.7 |
| Term | at most **30 years** | 329 s.8 |
| Foreign currency exemption | a bank may leave out of s.7 "housing loans in foreign currency or linked to foreign currency given to a foreign resident", provided all its variable housing loans approved in principle in the calendar quarter stay within 66.66%; a bank that does not normally give housing credit, with negligible volume, need not meet even the portfolio test for a foreign-resident client | 329 s.12, s.12.3; Q&A 8.1 (update 26.6.2011) |
| Bank of Israel rate | **3.25%** in force since **3.9.2026** (previous 3.50%); still 3.25% on 25.10.2026 | BoI series MNT_RIB_BOI_D (code, 25.10.2026 20:11 UTC) |
| Prime | **4.75%** = BoI rate + 1.5 | convention stated on Discount Bank's English page ("the Bank of Israel rate + 1.5%"), bank page |
| 2026 rate path | 4.00% from 8.1 · 3.75% from 28.5 · 3.50% from 9.7 · 3.25% from 3.9 | BoI series via U1 `boi-rate.json` and today's extract |
| Next rate decision | **23.11.2026** | BoI press page (eyes, U1 25.10.2026) |
| BoI forecast, October 2026 | BoI rate 3.0% average in Q3 2027; inflation 2.0% over the next four quarters | BoI press release 21.10.2026 (eyes, U1) |
| CPI, 12 months to September 2026 | 1.6% | CBS series 120010 (U1) |
| Average rate, new housing loans, **August 2026** (latest; September not yet published on 25.10.2026) | fixed not linked **4.62%** (May 4.77, Jun 4.73, Jul 4.63) · fixed CPI-linked **3.29%** (3.31, 3.27, 3.22) · variable CPI-linked **3.19%** (benchmark 1.64 + margin 1.55) · all CPI-linked 3.26% · **foreign currency linked 4.86%** (5.05, 4.46, 4.98), of which variable: benchmark 2.93 + margin 1.92 · fixed foreign currency: no loans | BoI dataflow BIR_MRTG_99, series 467, 1492, 1489, 1488, 1485, 689, 692, 691, 694 (code, 25.10.2026) |
| Average rate by term, not linked (fixed and variable, effective annual), reporting month 9/2026, in force from 19.10.2026 | average 4.55% · up to 1 year (incl. loans whose rate can change at unknown dates, i.e. prime) 4.35% · 1 to 5y 4.51% · 5 to 10y 4.59% · 10 to 15y 4.61% · 15 to 20y 4.74% · 20 to 25y 4.79% · over 25y 4.89% | BoI `mashfix.xls` updated 18.10.2026 (code, U1) |
| Same, CPI-linked | average 3.49% · up to 5y 3.50% · 5 to 10y 3.49% · 10 to 15y 3.24% · 15 to 20y 3.46% · 20 to 25y 3.37% · over 25y 3.53% | BoI `pribmash.xls` (code, U1) |
| New mortgages, August 2026 | 10,272 loans, ₪10.90 billion (about ₪1.06 million each); investment homes 694 loans, ₪0.89 billion (about ₪1.28 million each); shares of volume: variable not linked incl. prime 54.3%, fixed not linked 35.8%, fixed CPI 6.6%, variable CPI 3.2%, **foreign currency 0.1%**; average payment-to-income 29.23%; average term (not linked) 23.8 years | BoI BIR_MRTG_99 (code, U1) |
| Representative exchange rates, **23.10.2026** (last before today; no rate on Sunday) | **USD 3.112 · EUR 3.4844 · GBP 4.1624** ₪; 30 days from 23.9: USD 3.017 to 3.112, EUR 3.4291 to 3.4919, GBP 4.0068 to 4.1624; also CAD 2.2204, AUD 2.1843, ZAR 0.1879 | BoI series RER_xxx_ILS (code, 25.10.2026; CAD/AUD/ZAR from lang-dna-en, same day) |
| Purchase tax, foreign resident (anyone who is not an individual Israeli resident) and additional home | 8% up to ₪6,055,070, 10% above, from the first shekel; temporary order **extended to 10.2.2027 inclusive** | Tax Authority notice 12.10.2026, `gov.il/he/pages/pa121026-2` (eyes, lang-dna-en) |
| Purchase tax, Israeli resident, single home | 0% to ₪1,978,745 · 3.5% to 2,347,040 · 5% to 6,055,070 · 8% to 20,183,565 · 10% above; frozen to 15.1.2028 | Tax Authority instruction 1/2026 (18.1.2026); `ptax.json` |
| Purchase tax, oleh (reg. 12A, single home, from 1 year before to 7 years after aliyah) | 0% to ₪1,978,745 · 0.5% to 6,055,070 · 8% to 20,183,565; no relief above | instruction 1/2026 s.2c |
| Foreign resident who becomes an Israeli resident within 2 years | can be treated as a resident for the single-home test (refund route) | Tax Authority 2026 buyer guide p.50 (lang-dna-en F6) |
| Purchase tax filing | declaration within 30 days; payment not before 60 days from the deal | lang-dna-en F10, F11 |
| Directive 451, approval in principle | the bank must answer in writing within **5 business days**; in cases defined in advance in its credit policy, 7 business days with a reasoned notice; with the approval it gives the applicant the **list of documents** needed for the loan | circular 2694 (31.1.2022) s.4 (code) |
| Directive 451, uniform baskets | every approval in principle shows three uniform baskets (all fixed not linked · thirds: fixed not linked, prime, 5-year variable CPI-linked · half fixed not linked, half prime) with expected total interest, total repayment and highest expected payment | circular 2694 addendum 5 (U1) |
| Directive 451, appraisal | an appraisal by an appraiser on the bank's list can be used if not more than **90 days** have passed since the valuation | circular 2694 (code, line read) |
| Directive 451, outside insurance | a borrower may bring outside property or life insurance; the bank confirms receipt and must tell the borrower and insurer **within 14 days** if the policy does not meet its requirements | circular 2694 (code) |
| Early repayment (Banking Order 2002) | no capitalization fee on loans whose rate changes at least yearly or at unknown dates (prime); operational fee up to ₪60; 0.1% if notice is under 10 days; capitalization fee on fixed tracks reduced 20% after 3 years and 30% after 5 | U1 verified, `order-116.pdf` |
| Know your customer (banks) | no account opened without identification and a know-your-customer process: source of funds, occupation, purpose, planned activity; **for a foreign resident also his connection to Israel and whether he is a foreign public figure** | Money Laundering Prohibition Order (banks) 2001 s.2A (Wikisource, code) |
| ID for a foreign resident | foreign passport or travel document (or certified copy), compared with an additional document bearing a photo and ID number | same Order s.3(a)(2) |
| Face-to-face identification | required before the first action; may be done by the bank's representative, **an Israeli-licensed lawyer, an Israeli diplomatic or consular representative abroad, an authority under the Apostille Convention**, or other means the Supervisor approves | same Order s.6(a) |
| Beneficiary declaration | signed declaration on opening whether there is a beneficiary | same Order s.4(a) |
| Oleh certificate as ID | counts as an ID card for up to 30 days from issue when opening an account | BoI letter 793-17-BC, 22.3.2018 (`201802_en.pdf`, page updated 30.11.2023) (code) |
| Refusing an account | "a bank may not refuse unreasonably to open a current account in domestic currency" with a positive balance; reasonable grounds include suspected money laundering | Banking (Customer Service) Law 1981 s.2(a), as explained on BoI Q&A "Current Account, General Information" (page updated 15.11.2022) (eyes) |
| Notarization at Israeli missions | in person before a consular representative; missions do not prepare legal documents; also for "a foreign citizen who needs a notarized signature on a document that needs to be submitted in Israel" | MFA, gov.il notary_authorization (eyes, lang-dna-en) |
| Prices in foreign currency | a dealer may publish an asset's price only as the total price and only in Israeli currency (real estate included) | Consumer Protection Law s.17D (lang-dna-en) |
| VAT | 18% | facts.md 2d |
| Bank page: Mizrahi International Mortgage Center | shekel mortgages to international clients, loans up to 30 years, "up to 50% of the property value", fixed or variable | mizrahi-tefahot.co.il/en/mortgages/ (bank page, undated, read 25.10.2026) |
| Bank page: Mizrahi Q&A | olim "up to 75% LTV instead of 50% as a foreign citizen" if Israeli citizen "or entitled to Israeli citizenship"; olim state loan "up to two hundred thousand shekels", up to 30 years; income from Israel or abroad, incl. investment income; bank checks origin of funds; life insurance a prerequisite | mizrahi-tefahot.co.il/en/about-mizrahi-tefahot/qa-mortgages-in-israel/ (bank page, undated) |
| Bank page: Discount | value = lower of contract price and appraisal; PTI 50% legal, "most banks" offer up to one third; documents after approval in principle: appraisal, life insurance, property insurance, mortgage deeds, notarized documents | discountbank.co.il/en/private-banking/international-private-banking/mortgage-private-banking/ (bank page, undated) |
| Bank page: Bank of Jerusalem non-resident account | conditions: Israel is not your or your family's permanent residence; no business in or tied to Israel; opened only at Private Banking, Tel Aviv, Ashdod or Netanya branches, **not by proxy**; non-resident declaration renewed every three years | bankjerusalem.co.il/en/forex/non-resident-account (bank page, undated) |

**Unverified (kept out of the page until checked):** that intending olim "within two years" get 75% (First Israel, Ynet; not in the
directive text); Mizrahi's "or entitled to Israeli citizenship" wording versus the directive's definition; how banks treat a non-citizen
who is an Israeli resident under s.16A(a)(1a); how the Tax Authority, and so the bank, treats a married couple with one foreign spouse;
the olim state loan amount, rate and terms for 2026 (Mizrahi "up to ₪200,000", Semerenko "minus 0.5 points, capped at 3%");
"approval in principle valid 24 days" (Semerenko); a foreign rate premium or its absence (Ynet); any prime spread average (BoI has no
series; the English per-bank report stops at 31.10.2025); appraiser fee ₪650 and file fee "0.25% up to ₪360" now in `nrm.json`; lawyer
fee 0.5% to 1% + VAT (market practice); bank age limits; non-bank top-up loans to 85% (brokers' claims) and the rules that govern them;
approval times in weeks; which banks lend in foreign currency today and for how long (our page says Bank of Jerusalem up to 20 years; its
English mortgage page now has 177 words and does not show it); heter iska wording per bank.

---

## 7. Baseline depth proof and the honesty target

`proof-before.md` (read 25.10.2026 22:07 Israel, raw HTML): our current page `/israel-mortgage-non-residents/`: 3,827 words · 142 figures ·
3 tables · 72 cells · 1 calculator · 5 FAQ · 19 headings · 1 visual · 1 official source · Article, FAQPage, SoftwareApplication · 21.10.2026.
Ahead of us today: Semerenko words 4,481, headings 29, visuals 5, figures 112; Noam Homes FAQ 8; Walty headings 27, visuals 9, FAQ 8;
welcome-israel visuals 9; Even Sapir headings 20, figures 71, 35-cell table; Israel Property Hub FAQ 8.

Top six combined (Mizrahi, Semerenko, NBN, Noam, Buyitinisrael, welcome-israel): words 10,307 · figures 259 · tables 4 · cells 74 ·
FAQ 15 · official sources 2 · calculators 0 · visuals 20.

**Targets for the English page (measured with the same tool after release):**

| Metric | Best single rival | Top six combined | Target | Beats |
|---|---|---|---|---|
| Words (visible English) | 4,481 | 10,307 | ≥ 4,900 | each rival; not the combined sum (no padding) |
| Figures | 112 | 259 | ≥ 280 | combined |
| Tables | 2 | 4 | ≥ 8 | combined |
| Table cells | 42 | 74 | ≥ 220 | combined |
| Calculators | 1 (single rate) | 1 | 1, status-aware | each |
| FAQ (FAQPage) | 8 | 15 | 25 | combined |
| Headings h2+h3 | 29 | | ≥ 34 | each |
| Visuals (real charts and infographics, no icon padding) | 9 | 20 | ≥ 10 | each; combined not claimed |
| Official sources linked (boi.org.il, gov.il, Wikisource law text) | 1 | 2 | ≥ 14 | combined |
| Data dated to the month | Even Sapir "July 2026" | | every number dated; rates August/September 2026; FX 23.10.2026 | each |

Honesty statement to publish under the sources: what we compared (the pages Google ranked on 25.10.2026 for these queries, read as
Google gets them), what we counted, where a rival is still ahead (entity authority of banks and of Nefesh B'Nefesh; backlinks, which we
did not measure; Semerenko's network of linked guides; the combined word count of all rivals), and that bank offers differ from averages.

---

## 8. BUILD SPEC (English page for foreign buyers: US, UK, France-based English readers, olim)

### 8.1 URL, language, pairing (owner decision needed on the root page)
- URL `/en/israel-mortgage-non-residents/`, `<html lang="en" dir="ltr">`, `og:locale en_US`, self canonical, breadcrumb Home (`/en/`) >
  Buying in Israel > Israeli mortgage for non-residents.
- **Root page:** today English content labelled Hebrew. Recommended: in the same release, rewrite `/israel-mortgage-non-residents/` in
  Hebrew for "משכנתא לתושבי חוץ / לתושב חוץ / לעולים חדשים / לישראלים בחו"ל" (Hebrew brief to follow the page and article research law),
  with `lang="he"`. Only then add the pair on both pages:
  `hreflang="he"` → `/israel-mortgage-non-residents/` · `hreflang="en"` → `/en/israel-mortgage-non-residents/` ·
  `hreflang="x-default"` → **the English page** (Spanish, Italian and Portuguese searchers are better served in English than in Hebrew;
  this departs from the site's x-default = Hebrew convention on purpose). No redirect, no noindex, no sitemap withdrawal.
- If the owner keeps the root page English: do not publish a second English page; upgrade the root in place and fix its `lang`.
- Expect the English impressions to move from the root to `/en/` over weeks; there is little to lose (position 63, 0 clicks), and the US AI
  overview citation may lapse until Google re-reads the new page.

### 8.2 Head of page
- **SEO title (59 characters):** `Israel Mortgage for Foreigners 2026: Rates, LTV, Calculator`
- **Meta description (≈150):** `How much an Israeli bank lends foreigners, Israelis abroad and new olim: Bank of Israel caps, August 2026 average rates, cash to close in $, € or £.`
- **H1:** `Israel Mortgage for Foreigners and Non-Residents: What You Can Borrow`
- **Answer paragraph (53 words, head term first):**
  "An Israel mortgage for foreigners is capped at 50% of the home's value: Bank of Israel Directive 329 treats any buyer without Israeli
  citizenship as buying an investment home. Israeli citizens living abroad and registered new olim can borrow up to 75% for a first Israeli
  home. Average fixed rate: 4.62% (August 2026)."
- Byline: Adv. Ben Betesh, Israeli real estate lawyer, Israel Bar licence 29020 (as on the current page) · "Rates checked 25 October 2026;
  next Bank of Israel decision 23 November 2026".
- Numbers strip (each with its date): Bank of Israel rate 3.25% · prime 4.75% · fixed not linked 4.62% (Aug 2026) · foreign currency
  loans 4.86% (Aug 2026) · max loan for a non-citizen 50% · $1 = ₪3.112, €1 = ₪3.4844, £1 = ₪4.1624 (Bank of Israel, 23 Oct 2026).
- CTA row inside two viewports: the site's WhatsApp "ייעוץ חינם" bar (owner law) plus in-page "Check my numbers with a lawyer on WhatsApp".

### 8.3 Section order (content first: H1, answer, CTAs, then the calculator)
1. H1, answer paragraph, byline, numbers strip, CTAs.
2. **H2 "Israeli mortgage calculator for foreign buyers"** (the extended calculator, 8.6).
3. **H2 "How much an Israeli bank can lend you, by status"** (T1, infographic 1).
4. **H2 "Two rulebooks: citizenship sets your loan, residency sets your tax"** (T2 status matrix; the Israeli citizen abroad example).
5. **H2 "The income test: 50% by law, about one third in practice, in your currency"** (T3).
6. **H2 "Mortgage rates in Israel today, by track and by term"** (T4a, T4b; small chart of the 2026 rate path).
7. **H2 "Tracks and the one-third fixed rule"** (T6 track table with early repayment rules).
8. **H2 "Borrowing in dollars, euros or pounds"** (foreign currency loans: average, share, s.12.3, the 10% shekel test).
9. **H2 "Cash to close on a ₪4,000,000 home, by status"** (T5, infographic 2).
10. **H2 "Documents, the Israeli bank account and identification from abroad"** (T7, T8).
11. **H2 "From approval in principle to the money: the timeline"** (T9, infographic 3).
12. **H2 "Signing from abroad and insurance"** (power of attorney, consulate, apostille check; outside insurance with the 14-day answer).
13. **H2 "Olim and returning Israelis"** (75% once registered; purchase tax 12A; state-assisted loan described without figures until verified).
14. **H2 "Above 50%: what exists and what it costs"** (no bank above 50% for a non-citizen; bridge loans for upgraders; non-bank top-ups
    named as brokers' offers with "ask for the full cost"; no figures until verified).
15. **H2 "What Israeli banks say on their own English pages"** (T10).
16. **H2 "Hebrew terms you will hear"** (mashkanta, ishur ekroni, maslul, kalatz, katz, prime, madad, shamai, teudat zakaut, toshav chutz, ezrach yisraeli).
17. **H2 "Questions buyers ask"** (25 FAQ, 8.8).
18. **H2 "Sources and how we checked"** (dated list, honesty statement).
19. Related: `/en/buy-property-in-israel/` (how to buy from abroad) · `/israel-purchase-tax-foreign-residents/` · `/en/projects/` (the
    English catalog, which already carries the calculator) · `/en/new-projects/`.

### 8.4 Tables (real data, each with source and date under it)
- **T1 Loan cap by buyer status** (Directive 329 s.1, s.2; BoI Q&A 2.4 and joint buyers): Not an Israeli citizen, any home: 50% · Israeli
  citizen (incl. registered oleh), only home in Israel: 75% · Israeli citizen replacing a home he will sell: 70% · Israeli citizen who already
  owns an Israeli home: 50% · Mixed buyers counted separately for tax: weighted by share (50/50 → 62.5%) · Reduced-price programmes
  (Mechir Lamishtaken): own money at least ₪100,000 (329 s.4A, via U1). Column "what decides it", column "source".
- **T2 Status matrix (the two rulebooks)**: rows = Non-citizen living abroad · Israeli citizen living abroad, no Israeli home · Israeli citizen
  living abroad who owns an Israeli home · New oleh living in Israel, first home · Couple, one citizen and one not. Columns = loan cap (329) ·
  purchase tax track (8%/10% to 10.2.2027; resident single-home brackets; oleh 12A) · what to ask the bank in writing.
- **T3 Income test in your currency** (329 s.5; Discount page for one third; BoI rates 23.10.2026): loans of ₪1,000,000, ₪2,000,000,
  ₪3,000,000 over 25 years at 4.62%: monthly ₪5,627 / ₪11,253 / ₪16,880; net income needed at the 50% cap and at one third, in ₪, $, €, £
  (₪2,000,000: ₪22,507 ≈ $7,232 at the cap; ₪33,760 ≈ $10,848 at one third).
- **T4a Average rates on new housing loans, May to August 2026** (BoI): fixed not linked 4.77 / 4.73 / 4.63 / 4.62 · fixed CPI-linked 3.31 /
  3.27 / 3.22 / 3.29 · variable CPI-linked 3.43 / 3.28 / 3.17 / 3.19 (benchmark + margin) · foreign currency linked 5.05 / 4.46 / 4.98 / 4.86 ·
  prime 4.75 today (BoI rate + 1.5; banks add or subtract their own spread).
- **T4b Average rates by term, reporting month September 2026** (BoI, in force from 19.10.2026): not linked 8 buckets and CPI-linked 7
  buckets from 6 above, with the note "effective annual averages; your offer depends on your file".
- **T5 Cash to close on a ₪4,000,000 home, 25 years, fixed not linked 4.62%** (our arithmetic; caps 329; tax per 6; lawyer 0.5% + 18% VAT;
  appraiser and file fee shown as "typical, check your bank's tariff" until verified):
  Non-citizen: loan ₪2,000,000 · tax ₪320,000 · cash ₪2,344,610 (≈ $753,409 / €672,888 / £563,283) · payment ₪11,253 (≈ $3,616).
  Israeli citizen abroad, first home: loan ₪3,000,000 · tax ₪320,000 · cash ₪1,344,610 (≈ $432,073) · payment ₪16,880 (≈ $5,424).
  New oleh resident, 12A: loan ₪3,000,000 · tax ₪10,106 · cash ₪1,034,716 (≈ $332,492).
  Israeli resident, single home: loan ₪3,000,000 · tax ₪95,538 · cash ₪1,120,148 (≈ $359,945).
- **T6 Tracks**: fixed not linked · fixed CPI-linked · prime · variable every 5 years (not linked / CPI-linked) · foreign currency; columns:
  what moves the payment, average rate (T4a), counts toward the two-thirds variable cap (yes/no; foreign currency exempt for non-citizens,
  s.12.3), early repayment fee (none on prime; possible on fixed, reduced after 3 and 5 years).
- **T7 Documents, who asks and why**: passport plus a second photo ID (Order s.3) · source of funds, occupation, purpose, connection to Israel,
  foreign public figure question (Order s.2A) · beneficiary declaration (s.4) · income from abroad: payslips, tax returns or accountant letter,
  translated as the bank requires (bank pages; exact list comes with the approval in principle, Directive 451) · bank statements · contract and
  property papers for the appraiser · life and property insurance (Mizrahi, Discount pages) · notarized signatures or power of attorney.
- **T8 The Israeli bank account**: why you need it · the legal rule on refusal (s.2(a)) · who can identify you face to face abroad (Order s.6) ·
  one bank's own conditions for non-resident accounts (Bank of Jerusalem: in branch, no proxy, declaration every 3 years) · olim: oleh
  certificate as ID for 30 days (BoI letter).
- **T9 Timeline with the rule behind each step**: account and identification · approval in principle (decision within 5 business days, 7 in
  predefined cases; three baskets; document list) · appraisal (listed appraiser, 90 days) · contract (sign after approval; align payment dates
  with the bank's releases) · insurance (outside policy allowed; bank answers within 14 days) · purchase tax declaration (30 days) and payment
  (from day 60) · liens and warning note · release of funds.
- **T10 Banks on their own English pages**: Mizrahi-Tefahot (International Mortgage Center: shekel loans to international clients, up to
  50%, up to 30 years; Q&A on olim) · Discount (international private banking: rules, named English-speaking advisers) · Bank of Jerusalem
  (non-resident account conditions) · Leumi and Hapoalim: no English mortgage page found on 25.10.2026 (say so). Plus a pointer to the Bank
  of Israel per-bank comparison, noting its English version's last period (October 2025).

### 8.5 Three infographics (design brief per the owner's design law)
Palette and faces: **passport navy #1E2B47, visa-stamp violet #5B3FA0, security-print teal #0F7C7A, cool paper white #F6F8FA, slate text
#2B3440; faces Public Sans (headings and copy, a public-forms typeface) and IBM Plex Mono for figures (bank statement world).** Why not the
default: no cream, brass or terracotta, no Inter or Space Grotesk, no acid accent on black; the colours come from passports, visa stamps and
banknote security print, the actual world of a cross-border buyer. Made in Claude Design, light and dark.
1. **"Two rulebooks" grid**: citizenship (yes / no) by residency (Israel / abroad), four cells, each with the loan cap and the purchase tax
   track, plus a strip "already own an Israeli home: 50% for everyone (70% if you will sell it)".
2. **"Where ₪4,000,000 comes from"**: four stacked bars (non-citizen, Israeli citizen abroad, oleh resident, Israeli resident): loan, your
   cash for the price, purchase tax, fees; labels in ₪ with $ underneath "at the Bank of Israel rate of 23 Oct 2026".
3. **"From approval to money"**: a horizontal timeline with the legal clocks (5 business days, 90 days, 14 days, 30 days, 60 days) and the
   points where documents are asked for.
Optional small chart: Bank of Israel rate 2026 (4.00 → 3.75 → 3.50 → 3.25) with the average fixed rate May to August.

### 8.6 The calculator: extend `nrm` (keep the key and the current English block; backward compatible on `/en/projects/`)
**Add inputs:**
- **Your status** (radio): Not an Israeli citizen · Israeli citizen, no home in Israel · Israeli citizen, already own a home in Israel ·
  Israeli citizen, selling my Israeli home · New oleh living in Israel · Couple: one Israeli citizen, one not (share %, with the note that a
  bank answer in writing is needed).
- **Mode**: "What can I borrow?" (default) · "What can my cash buy?" (cash in your currency → highest price, after tax and fees).
- **Net monthly household income** and **fixed monthly commitments** (in your currency).
- **Bank appraisal compared with price** (100% default, down to 85%).
- **Track mix** presets taken from the Bank of Israel uniform baskets: all fixed not linked · thirds (fixed not linked / prime / CPI-linked) ·
  half fixed not linked, half prime · foreign currency loan (only for non-citizens). Prime = 4.75% plus an editable "your bank's spread"
  (default 0, labelled); CPI-linked tracks add the Bank of Israel's 2.0% inflation forecast as a stated assumption.
- More currencies: CAD, AUD, ZAR at the same Bank of Israel date.
**Add outputs:**
- Loan cap for your status (329) · loan cap from your income at 50% and at one third · **the lower of the two, in one sentence** ("Your income,
  not the 50% cap, limits you to ₪...").
- First payment and the payment if prime rises 1 point (only the variable part reprices) and, for CPI tracks, after one year of forecast inflation.
- Cash to close with purchase tax on the right track for your residency (foreign 8%/10%, resident single home, oleh 12A) and the validity
  date of that track (10.2.2027 / 15.1.2028).
- **Your payment if the shekel moves 10% either way** (₪2,000,000 example: $3,616 today, $3,287 if the shekel weakens 10%, $4,018 if it
  strengthens 10%) and the 30-day Bank of Israel range.
- Warnings: variable share above 66.66% (except foreign currency for non-citizens), term above 30 years, loan above the status cap, payment
  above 50% of income.
- Sources line under the result with dates; formula line.
**Data file `nrm.json` (fix and extend):** replace `rates_source` funder.co.il with the Bank of Israel data (series and month); replace
"Variable, not linked (approx.) 4.42" with the Bank of Israel term table's "up to 1 year incl. prime" 4.35% (September 2026) or with prime
4.75% plus spread; add `ltv_by_status`, `fx_track` 4.86, `cpi_track` 3.29, `cpi_forecast` 2.0, `rate_by_term`, `next_decision` 23.11.2026;
point `ltv_source` to the PDF and the Q&A; label `appraiser` 650 and the file-fee rule as unverified until a bank tariff is read; refresh monthly
with `tools/instruments/build_boi_data.py` and `build_fx_data.py`. Replace the validation message "Between 0% and 50% for a non-resident" with
the status cap.

### 8.7 The moat (one practical thing nobody has)
**"Your Israeli borrowing limit by passport and paycheck"**: one answer that combines the Bank of Israel's citizenship rule (Directive 329
and its Q&A), the Tax Authority's residency rule, your income in your own currency at the Bank of Israel rate of the day, and the Bank of
Israel's average rates for the latest month, and returns three numbers: the most you can borrow (and which limit binds), the most home your
cash can buy, and your monthly payment in your currency with a 10% shekel swing. Every number on it is dated and linked to the regulator's
own text. No rival has status-aware caps, foreign-currency income tests, the two rulebooks together, or the official averages.

### 8.8 FAQ (25, natural English; FAQPage markup; each answer 40 to 90 words with its source)
1. **Can a foreigner get a mortgage in Israel?** Yes. Israeli banks lend to buyers without Israeli citizenship, mostly in shekels, up to 50% of
   the home's value. Directive 329 treats any home a non-citizen buys as an investment home, so 50% applies even to your first and only home here.
2. **How much will an Israeli bank lend me?** Two limits apply and the lower wins: the value cap by status (50%, 70% or 75%) and the income cap
   (payment at most 50% of disposable income). Banks count value as the lower of price and appraisal.
3. **What is the minimum down payment?** For a non-citizen, half the price plus purchase tax and fees. A $300,000 home (≈ ₪933,600 at the Bank
   of Israel rate of 23 Oct 2026) needs ₪466,800 down plus ₪74,688 purchase tax; an Israeli citizen's only home needs 25%, ₪233,400.
4. **I am an Israeli citizen living abroad. Can I borrow 75%?** Yes for your only home in Israel: the directive's "Israeli citizen" includes
   anyone registered or required to be registered in the Population Registry, wherever you live. Your purchase tax is still the non-resident 8%/10%.
5. **I am making aliyah. When does 75% start?** When you count as an Israeli citizen under the directive, in practice once you are registered.
   Some banks and brokers offer 75% to buyers planning aliyah; the directive does not say so, so get it in writing before you sign.
6. **My spouse is Israeli and I am not. What can we borrow?** The Bank of Israel follows the Tax Authority: if you are separate buyers, the cap is
   weighted by your shares (50/50 of 75% and 50% is 62.5%). Spouses usually count as one buyer for tax, so ask the bank in writing.
7. **What are mortgage rates in Israel now?** August 2026 averages on new loans: fixed not linked 4.62%, fixed CPI-linked 3.29% plus inflation,
   foreign currency loans 4.86%. Prime is 4.75% (Bank of Israel rate 3.25% since 3 Sep 2026). Next decision: 23 Nov 2026.
8. **Do foreigners pay higher rates than Israelis?** The Bank of Israel does not publish rates by citizenship, so there is no official figure
   either way. What changes for you is the loan size and the paperwork. Compare written offers against the official averages.
9. **Which bank in Israel is best for foreigners?** There is no official ranking. Mizrahi-Tefahot runs an International Mortgage Center (shekel
   loans, up to 50%, up to 30 years); Discount and Bank of Jerusalem have English pages for clients abroad. The Bank of Israel publishes per-bank rates.
10. **Can I borrow in dollars, euros or pounds?** Yes, foreign currency loans exist: their average rate was 4.86% in August 2026, and they were 0.1%
    of new lending. For non-citizens they sit outside the two-thirds variable cap. They suit you only if you earn in that currency.
11. **Should I borrow at home instead?** Compare the total cost in the currency you earn. A shekel loan moves with the exchange rate: on a
    ₪2,000,000 loan, a 10% move in the shekel changes a $3,616 payment to $3,287 or $4,018.
12. **How much do I need to earn?** The payment may not pass 50% of disposable income; most banks prefer about one third. On ₪2,000,000 over 25
    years at 4.62% (₪11,253 a month) that is ₪22,507 net (≈ $7,232) at the cap and ₪33,760 (≈ $10,848) at one third.
13. **How do banks count income earned abroad?** Each bank sets its own policy; the directive counts net income minus commitments running more
    than 18 months. Expect translated payslips or tax returns, an accountant letter if self-employed, and source-of-funds checks.
14. **What documents do I need?** Passport and a second photo ID, proof of income, bank statements, source-of-funds evidence, the contract and
    property papers, life and property insurance, and signatures or a power of attorney. The bank must give you its list with the approval in principle.
15. **Do I need an Israeli bank account, and can I open one as a non-resident?** In practice yes. A bank may not unreasonably refuse a shekel
    current account in credit. You can be identified face to face by an Israeli lawyer or consul abroad; each bank decides its own process.
16. **How long does approval take?** The bank must answer a request for approval in principle within 5 business days (7 in cases it defines in
    advance). Appraisal, insurance and liens come after; there is no official figure for the whole process.
17. **Can I do it all without flying to Israel?** Often, with a power of attorney to an Israeli lawyer and signatures before an Israeli consul or
    a notary with an apostille. Each bank decides which signatures it accepts, so confirm before you book anything.
18. **Is life insurance required, and can I use my own policy?** Banks require life and property insurance assigned to them. You may bring an
    outside policy; the bank must tell you within 14 days if it does not meet its requirements.
19. **What is the longest mortgage term?** 30 years under Directive 329. Age limits are each bank's policy.
20. **Does part of the loan have to be fixed?** Yes. The variable part may not pass 66.66% of the loan, so at least one third is fixed. Foreign
    currency loans to non-citizens are the exception.
21. **What if the appraisal comes in below the price?** The bank lends on the lower figure and you cover the gap in cash. A report by an appraiser
    on the bank's list can be used for 90 days.
22. **How much purchase tax does a foreign buyer pay?** 8% up to ₪6,055,070 and 10% above, from the first shekel, for purchases until 10 Feb 2027.
    On ₪3,000,000 that is ₪240,000; on ₪4,000,000, ₪320,000.
23. **Can I repay early, and what does it cost?** Prime and other tracks whose rate changes at least yearly carry no capitalization fee. Fixed
    tracks can, when market rates have fallen; the fee drops 20% after 3 years and 30% after 5.
24. **Can I borrow more than 50% as a foreigner?** Not from an Israeli bank while you are not a citizen. Brokers offer extra loans from non-bank
    lenders on top, at higher rates and outside Directive 329; ask for the full cost in writing.
25. **What is the monthly payment on a $500,000 loan over 30 years?** $500,000 is ₪1,556,000 at the Bank of Israel rate of 23 Oct 2026. At the
    August 2026 average fixed rate of 4.62%, the payment is ₪7,995 a month, about $2,569.
(Optional 26, only with a bank's own published text: "Do Israeli banks charge Jewish borrowers interest?" with the heter iska answer.)

### 8.9 Copy and data rules for the build
- Shekels are the price; every $ / € / £ figure is labelled "approx., Bank of Israel rate of 23 Oct 2026" (Consumer Protection Law s.17D:
  conversions are calculations, not prices).
- Every rate carries its month; every rule carries its section; refresh rates monthly and FX daily from the existing data jobs.
- No em or en dashes; no technology words on the page ("data series", "algorithm", "API" stay in the research); no invented numbers; unknown =
  omitted (nothing from the unverified list goes live without a source).
- Fix on publication: the 75% wording is "Israeli citizen", never "Israeli resident"; prime 4.75%; payment cap 50%.
- Schema: Article (author, dateModified), FAQPage (25), SoftwareApplication or WebApplication for the calculator, BreadcrumbList; Dataset only
  for the rates tables, with the Bank of Israel as source and the months as temporal coverage.
- Internal links in: from `/en/buy-property-in-israel/` (financing paragraph and FAQ), `/en/projects/` (calculator card), `/en/new-projects/`,
  the English purchase tax page, and the two root English buyer guides; anchors "Israeli mortgage for non-residents" and "Israel mortgage
  calculator for foreigners".

### 8.10 Decisions only the owner makes
1. Root page: rewrite in Hebrew in the same release (recommended), or keep it English and skip the `/en/` page.
2. x-default to the English page for this pair (recommended) instead of the site's Hebrew default.
3. Whether the three other English-at-root buyer pages get the same treatment later (finding only today).
