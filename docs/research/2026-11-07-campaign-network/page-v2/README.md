# /marketing/ (he), page v2: "שיווק פרויקט נדל״ן: כמה זה עולה ואיך עושים את זה נכון" (HAD-678, 7.11.2026)

**LOCAL ONLY.** Nothing was published, created on the site, committed or sent. No existing repo file was edited. English (`/en/marketing/`)
comes later (Ben). Replaces the first draft in `../page/` (structure only was reused).

| File | What |
|---|---|
| `page_he.html` | WordPress post_content (block-free HTML), ~107 KB. Crumbs shortcode, the page's own `nlu1-css` block, H1, answer, CTAs, `[nadlan_tool id="nlbudget"]`, 11 chapters, plans, `[nadlan_tool id="nlcamp"]`, lead route, proof table, live pages, FAQ (20), related line. |
| `meta.json` | post title, slug `marketing`, parent 0, H1, SEO title (61 chars) and description (149 chars), crumbs, tools, FAQ list. |
| `build_page_he.py` | Writes `page_he.html` and `meta.json` from the copy in the file (`python build_page_he.py`). |
| `check_page_he.py` | All checks below (`python check_page_he.py`, or `--nolinks`). Exit 1 on any failure. |
| `nlu1-css.txt` | The `<style id="nlu1-css">` block copied from page 121 (backup `docs/research/2026-11-06-mortgage-universe/content/page-backup/page-121-20261106-200238.html`). |

Title tag: `כמה עולה לשווק פרויקט נדל״ן? פירוק התקציב ליזמים 2026 | נדל״ן` (61 chars, as briefed).
Slug: `url_word_audit.py --token marketing` found 0 URLs holding the token (7.11.2026); `/marketing/` and `/en/marketing/` answer 404.
kw_guard on title and H1: WARN only for נדל״ן (qualified, owner `/`), slug OK.

## Checks run (7.11.2026, `check_page_he.py`, all PASS)
- One `<h1>`.
- Blacklist (language-dna + meta forbid list, Hebrew word boundary with prefix letters): 0 hits. Words checked include ממשק, דמו, הדגמה,
  מודל, מנגנון, שכבה, אינטראקטיבי, מובייל, פיילוט, מערכת, פלטפורמה, טכנולוגיה, סימולציה, אלגוריתם, תלת ממד, בקרוב, בבדיקה, אטלס, אפס,
  מנוע, and 3D, demo, interface, engine, UI, UX, tile, prototype, MVP. (One hit, "המערכת של גוגל", was rewritten.)
- Long dashes (U+2012 to U+2015) anywhere in the file: 0.
- `[nadlan_tool id="nlbudget"]` once, `[nadlan_tool id="nlcamp"]` once, both quoted; one crumbs shortcode; nlu1-css present.
- FAQ: the h2 `שאלות נפוצות של יזמים על שיווק פרויקט ותקציב` matches the `nadlan_nli_faq()` regex; 20 Q&A parsed; answers 42 to 51
  words; the related-links line sits after `</section>` so it is not read into the last answer.
- No heading leads with פרסום פרויקט נדל״ן or פרסום נדל״ן. `tools/seo/kw_guard.py`: no BLOCK on 79 headings and 19 internal anchors
  (one H3 "דירות אחרונות..." was blocked, owner `/properties/`, and renamed "סוף המלאי: דירות אחרונות והשקה מחודשת").
- Internal links, browser user agent, no redirect followed: all 19 answer 200. Every `#anchor` has its id.
- Words: 8,620 in the visible text, 7,995 with Hebrew letters (target 6,000 to 9,000). 16 H2, 62 H3. HTML tag balance: clean.
- NOT checked: rendering on the live theme (a local file preview was refused by the browser pane). Check phone and desktop at release.

## Open points
1. **`nlbudget` does not exist yet.** It is not in `nadlan_nli_tools()`; the shortcode prints nothing until it is built (design:
   `Budget.dc.html`). The page's tables carry the same data meanwhile. The FAQPage schema prints only when a registered tool is on the
   page; `nlcamp` is registered locally (release 1.72.599 in preparation), so FAQ schema depends on that release.
2. No min-height reserve style for the two tools (the `nlmq-reserve` pattern of page 121): heights unknown until both are built and measured.
3. Lead context: the page claims only what works today. On project pages the WhatsApp text carries the project, the floor and the
   direction, in the page language (`assets/project-stage/bridge.js`, `waUrl`). Time in tour, source campaign and units opened are NOT
   built (PLAN.md §7 step 4) and are not claimed. The WhatsApp number per project (`cfg.wa`) must route to the developer for a paying client.
4. Plans, inclusions, the 7-day timeline and the 18,000 ₪ first payment come from Ben's approved prices (PLAN.md §5), the approved design
   (`Main.dc.html`) and PLAN.md §1b (Morning's 20,000 ₪ ceiling). When Morning raises the ceiling, the first-payment line changes.
   Prices written "₪ לשנה" with no VAT wording (accountant).
5. Legal chapter is general information and needs a lawyer's read before publishing. Marked uncertain on the page: content of the 1991
   price-advertising regulations; how the spam rule applies to WhatsApp; whether a marketing company paid by commission needs a broker
   licence; which lead databases need notice to the Privacy Authority. The gov.il notice page answered 403 to a direct read; the
   30-day notice and the amendment 13 points come from the gov.il service page and the Authority's guide as indexed. Meta, Google and
   TikTok rules are from `competitors/services.json` (`platform_rules`), not re-read today.
6. The six project pages in "מה כבר פועל באתר" are our editorial pages on other developers' projects; the page says plainly they are
   not a client list. Ben may want to confirm naming them on a B2B page. The Globes ad-spend table names five developers (press data).
7. The AI chapter uses the coordinator's repeat-run figures (10 of 11 runs, five project price questions) and also lists the six
   misses, including "כוכב הצפון תל אביב פנטהאוז מחיר" (single run, not cited), so the record stays complete.
8. The page is not linked from anywhere yet. PLAN.md says link it from the three B2B pages and the footer; that is an edit to existing
   pages and was not done. Linear HAD-678 and the Notion row were not updated from this session (coordinator's).

## Sources map (all read 7.11.2026 unless noted)
Agency guides are not named on the page (short source lines say "מדריכי משרדי שיווק", flagged as claims); exact URLs are here.
IDs are the `teardown/pages.json` ids.

| ID | URL | Used for |
|---|---|---|
| B01, B01b, B01c, B01d, B01e, B01f | https://semerenkogroup.com/he/real-estate-marketing/... (cost, project-marketing, how-to-market-new-project, google-meta-ads, real-estate-lead-management-roi, qualified-real-estate-leads) | 1% anchor, 60 x 2.4M example, 12 to 24 months, presale 15% to 20%, CPL 90 to 150 and 300 to 800, funnel examples, hidden costs, fee methods, CRM points |
| B02 | https://swipeup.co.il/עלות-שיווק-פרויקט-נדלן/ | 20,000 ₪ proposal, 20 x 5 x 250 = 25,000, Google daily x 30.4 |
| B03 | https://www.brandytlv.com/blog/real-estate-campaign-cost | 42 and 200 ₪ leads |
| B04 | https://www.mirai.co.il/post/real-estate-marketing-budget | back-calculation 12 / 6 / 72 / 8 / 576 / 100 / 57,600 / 432; data ownership |
| B05b | https://pixel-nadlan.co.il/2026/08/27/שיווק-פרויקט-נדלן-מדריך-ליזמים/ | stage durations 4-8 / 4-8 / 4-8 / 2-6 weeks / one week |
| B06 | https://start-point.co.il/real-estate-project-marketing/ | 2% to 4%, 3,000 to 23,000 per apartment, 7x (Bizportal 238717), lead price list 173 to 128 and 230 to 170 (4.11.2026), 4 to 12 ₪ click, 150 ₪ response example, broker 1% to 2% |
| B07b, B07c | https://www.baranesgroup.com/שיווק-פרויקטים-למגורים/... | misleading-ad examples (our recommendation line), privacy points |
| B08a | https://wedomedia.co.il/פרסום-נדלן/ | 1% with 0.75% digital, LinkedIn over 1,000, YouTube agorot, banners |
| B10 | https://www.globes.co.il/news/article.aspx?did=1001546786 (1.7.2026) | Ifat spend table, campaign totals, 85 thousand unsold, 51PARK, "no offer, no sale" |
| H02a | https://sistermarketing.co.il/real-estate/ | below 100 ₪ per lead |
| F01h | https://semerenkogroup.com/he/real-estate-marketing/foreign-buyers/ | audiences, assets for foreign buyers |
| F02 | https://semerenkogroup.com/selling-to-foreign-buyers-israel/ | resale ~2% + VAT; 45 to 90 days pre-approval |
| F05 | https://klikatnadlan.co.il/realestateabroadil/ | source countries USA, Canada, France, UK, South Africa |
| A01 | https://www.theurbandeveloper.com/articles/how-much-to-spend-on-off-the-plan-marketing | 1% to 2% (Australia) |
| A02 | https://www.feasly.com.au/guides/project-marketing-costs-off-the-plan-australia | 0.75%-2% / 3%-5%, no government benchmark, delay 720k to 880k (1.2% to 1.47%, 19.5% to 19.1%), 530k of 720k before launch, display suite 150k to 700k+, 320k + 90k for 18 months, commission 2%-3% and 4%-8%, $3,000-$10,000 per still |
| A03 | https://localiq.com/blog/real-estate-search-advertising-benchmarks/ | US CPC $3.22, CPL $102.51, 894 campaigns, Apr 2025 to Mar 2026 |
| A05 | https://www.bisnow.com/news/south-florida/multifamily/luxury-condo-developers-spending-millions-on-sales-galleries-to-stand-out-crowded-miami-market-135534 | $5M to $8M sales centre, 2-5 year leases |
| A06 | https://maverickframe.com/blog/real-estate-developer-marketing/ | 1% to 5% |
| A07 | https://www.probuilder.com/business-management/article/55195799/control-sales-marketing-costs (2004) | 6%, 8% to 10%, 1.5% (2%), 2% |
| R01 | https://mabatim.com/pricing/ | render, sales-plan and film prices, 5-7 working days, 2-3 weeks |
| R02 | https://realitech.co.il/architectural-rendering-price-guide/ | video from 3,000 ₪ |
| R03 | https://www.midrag.co.il/Content/Price/9879 | 800-3,000 per image, 3,000-5,000 for 6, 1,500-3,000 / 1,000-2,500, film 2,000-7,000 |
| services.json | `competitors/services.json` (sources inside) | OnMap 899 / 2,427 / 3,820 + VAT, 5 business days; immobilier from 69 ₪, FR 60% EN 40%, setup 5-7 days, 4-6 weeks, 8 languages, free replacement; ImmoIsrael 500 ₪/month; Juwai USD 15,000 / 18,000, Live 5,500 + 4 weeks; Rightmove GBP 2,135 ARPA 2025; Kyero EUR 3,200; LocaliQ Meta $13.74 (23.9.2026); Rex UK GBP 17.60; Kolonell EUR 80-150; Yad2 fair ~18,000 visitors, ~40 developers (nadlancenter 9.9.2024); Katz 15-20 stops (ynet ~15.3.2025); Icube 95th salon 15.11.2026; IBC NY 28-29.5.2026, Jerusalem 30.9.2026; Russian at 4 Israeli services, Arabic at none; platform rules (Meta housing US 12.2019, Canada 12.2020, Europe 12.2021, 18-65+, 25 km / 15 miles, 15 km; Meta sensitive topics 19.1.2022; Google housing US/Canada; TikTok HEC 4.2026) |
| geo-test | `geo-test-2026-11-07.md` (incl. repeat runs ~12:40) | 10 of 11; 3/3, 3/3, 2/3, 1/1, 1/1; the six misses and who was cited |
| our page | https://nad-lan.co.il/israel-purchase-tax-foreign-residents/ (reviewed 2.7.2026) | 8% / 10% / 6,055,070 ₪, 16.1.2024 to 31.12.2026, 4M -> 320,000 vs 95,538, VAT included for developer price, form 7000 30 days, pay 60 days, banks do not finance the tax, retroactive resident brackets, 487 foreign purchases Q1 2026 +18% (Chief Economist, published 13.5.2026) |
| our page | https://nad-lan.co.il/israel-mortgage-non-residents/ | 50% for a non-citizen, 75% citizen abroad or oleh first home, directive 329 |
| our page | https://nad-lan.co.il/projects/duo-tel-aviv/ | 83,800 ₪ per m² incl. VAT, contracts 1-6.2026, developer reports (the figure Google quoted) |
| our pages | project pages' meta descriptions (7.11.2026) | "two towers", "three towers", "four buildings" in the live-pages table |
| Kol Zchut | https://www.kolzchut.org.il/he/חוק_הגנת_הצרכן (updated 17.8.2026) | Consumer Protection Law 1981, main subject deception; 1991 price-advertising regulations in its list |
| Kol Zchut | https://www.kolzchut.org.il/he/מתן_בטוחות_לרוכש_דירה_מקבלן (25.5.2026) | Sale Law 1974, 7%, five securities |
| Kol Zchut | https://www.kolzchut.org.il/he/פיצוי_בגין_משלוח_דברי_פרסומת_ללא_הסכמה_של_הנמען_(חוק_הספאם) (17.2.2026) | section 30A, channels, consent forms, refusal, up to 1,000 ₪ per message; WhatsApp not mentioned |
| Kol Zchut | https://www.kolzchut.org.il/he/זכותון_ללקוחות_של_מתווכי_דירות_ומקרקעין (26.8.2026) | licence + written order + effective cause, exclusivity up to 6 months |
| gov.il | https://www.gov.il/he/service/notice-obligation (403 to direct read; indexed text), https://www.gov.il/he/pages/rishom_tikon13, the Authority's amendment 13 guide | amendment 13: wider duty to inform, notice for some databases within 30 days |
| Ben / product | PLAN.md §1b, §5; `plans-products.json`; `build/build-nlcamp/README.md`; design `Main.dc.html`, `Budget.dc.html` | 36,000 / 72,000 / 144,000 ₪ a year; first payment 18,000, parts up to 18,000; ad budget 3,000 to 60,000 ₪ a month; split 55 / 25 / 15 / 5; 10 markets; 5 steps; days 0, 1-3, 3-5, 7; page in 5 languages, campaign in 3 |

## Numbers computed by us (arithmetic on the sources above)
144,000,000 x 1% = 1,440,000 (24,000 per apartment); x 0.75% = 1,080,000 (18,000); x 2% = 2,880,000 (48,000); x 4% = 5,760,000
(96,000); monthly = divided by 12 to 24 months (60,000-120,000; 45,000-90,000; 120,000-240,000; 240,000-480,000). 487 / 3 = about 162 a
month. 530 / 720 = about three quarters before launch. 50,000 / 2,400,000 = 2.1%; 20,000 / 2,400,000 = 0.8%; 50,000 / 20,000 = 2.5
("פי שניים וחצי"). 30,400 / 30.4 = 1,000 ₪ a day. About half of the 24 budget-sheet rows have no published Israeli price (12 of 24).
