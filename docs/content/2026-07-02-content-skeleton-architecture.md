# Content Skeleton Architecture — gap-closer vs IL + abroad competitors
Created 2026-07-02 (Claude, owner-directed). Source data: `strategy/lovable/2026-06-21-report-2-keyword-master-universe.clean.csv` (Lovable keyword master), `skills/strategy-master.md` (Semrush IL volumes), `skills/internal-linking-hub-spoke.md` (LIVE cluster map — 42 pages already wired; DO NOT duplicate), the owner's competitive teardown (`docs/research/2026-07-01-listings-competitive-teardown.md`) and the 25-article hit-list (`handoff/antigravity/2026-07-01-holistic-sweep/`).

## The rules every writing agent MUST follow (anti-cannibalization contract)
1. **One keyword family = one URL.** Before writing, grep this doc + the live cluster map. If a keyword already belongs to a live page (e.g. tabu-extract-check, purchase-tax-calculator, property-value), you LINK to it — you never re-target it.
2. **One parent pillar per spoke** (strategy §5). Spoke ends with the back-to-pillar block (`<!-- nadlan-spoke-backlink-v1 -->` pattern) + 2 sibling links.
3. Keywords, intent and guidelines are IN THE DRAFT ITSELF (the gray writer-brief box at the top of every skeleton). Write in place of the outline; delete the brief box before publish.
4. Drafts stay **draft** (invisible to Google) until content passes: ≥1,200 words (HE) / ≥1,500 (EN pillar 2,500+), E-E-A-T (owner is a licensed Israeli lawyer — say so where legal topics appear), no invented data (official sources: CBS, רשות המסים, בנק ישראל), `copywriting-skill.md` voice, Yoast focus keyword set = primary keyword below.
5. EN pages: set hreflang alternates only when a real HE sibling exists; otherwise standalone EN. Slugs stay ASCII.

## NEW: English foreign-investor cluster (pillar + 7 spokes) — the monetization cluster
| # | Slug (draft) | Title | Primary keywords | Role |
|---|---|---|---|---|
| E0 | buy-property-israel-foreign-buyers | Buying Property in Israel: The Complete 2026 Guide for Foreign Buyers | buying property in israel, israel real estate for foreigners | **PILLAR** |
| E1 | israel-purchase-tax-foreign-residents | Israel Purchase Tax (Mas Rechisha) for Foreign Residents: 2026 Brackets | israel purchase tax foreigners, mas rechisha non resident | spoke→E0 |
| E2 | israel-mortgage-non-residents | Getting an Israeli Mortgage as a Non-Resident: Banks, LTV, Rates | israel mortgage for foreigners, non resident mortgage israel | spoke→E0 |
| E3 | transfer-money-to-israel-property | Transferring Money to Israel for a Property Purchase (AML rules) | transfer money to israel real estate, israel anti money laundering property | spoke→E0 |
| E4 | best-cities-israel-property-investment | Where Foreign Investors Buy in Israel: Tel Aviv vs Jerusalem vs the Coast | best city to buy property israel, tel aviv vs jerusalem real estate | spoke→E0 |
| E5 | buying-new-construction-israel | Buying New Construction in Israel: Bank Guarantees & the Sale Law | buying new apartment israel, israel bank guarantee chok mecher | spoke→E0 (links to /projects/) |
| E6 | manage-rental-property-israel-abroad | Managing an Israeli Rental Property from Abroad | manage rental property israel from abroad, israel property management | spoke→E0 |
| E7 | aliyah-housing-checklist | The Aliyah Housing Checklist: Renting & Buying When Moving to Israel | aliyah housing, moving to israel apartment | spoke→E0 |

## NEW: Hebrew gap spokes (attach to EXISTING live pillars — no new HE pillar)
| # | Slug | Title | Primary keywords | Parent pillar (live) |
|---|---|---|---|---|
| H1 | apartment-prices-2026 | מחירי הדירות בישראל 2026: נתוני הלמ"ס, מגמות ותחזית | מחירי דירות 2026, מחיר דירה ממוצע | buying-apartment |
| H2 | how-to-sell-apartment | איך מוכרים דירה בישראל: המדריך המלא שלב אחר שלב | איך למכור דירה | selling-apartment |
| H3 | rental-lease-template | חוזה שכירות לדוגמה: מה חייב להיות בו ומה אסור שיהיה | חוזה שכירות לדוגמא, חוזה שכירות דירה | buying-apartment* (renter intent; link from /rent when hub exists) |
| H4 | memorandum-of-understanding-apartment | זיכרון דברים לקניית דירה: למה עורכי דין מזהירים ממנו | זיכרון דברים דירה | buying-apartment |
| H5 | cancel-apartment-purchase | ביטול עסקת דירה: מתי אפשר, כמה זה עולה ואיך עושים את זה נכון | ביטול עסקת דירה, ביטול חוזה מכר | buying-apartment |
| H6 | building-cost-index-madad | מדד תשומות הבנייה: איך הוא מייקר את הדירה שלכם מהקבלן | מדד תשומות הבנייה, הצמדה למדד קבלן | buying-apartment |
| H7 | warning-note-tabu | הערת אזהרה בטאבו: מה זה, כמה עולה ולמה אסור לוותר עליה | הערת אזהרה, הערת אזהרה בטאבו | buying-apartment (sibling: tabu-extract-check — LINK, don't overlap) |
| H8 | hidden-costs-buying-apartment | העלויות הנסתרות בקניית דירה: עו"ד, מתווך, מס ומה שביניהם | עלויות קניית דירה, הוצאות נלוות קניית דירה | buying-apartment (links to apartment-purchase-cost-calculator) |

## Deferred to product (NOT article drafts — need supply/features first)
City buy/rent hubs (/buy/tel-aviv …) per Lovable P1 — now unblocked by the listings vertical but they are archive-page builds, not posts. Market data pages (price index) need the CBS ETL. Deal-finder pages need the estimator.

## Writing plan (hand this to any writing agent)
For each row above: open the WP **draft** with that slug → the gray brief box at the top holds keywords/intent/pillar/siblings → write per the rules block above → keep H2 outline order unless a better structure serves the reader → fill Yoast focus keyword = first primary keyword → internal links: parent pillar (1, exact-match anchor), 2 siblings, ≥1 tool/calculator, ≥1 money surface (/projects/, /properties/ or /professionals/) → owner review → publish (status change only; slug already reserved). Order of work: E0 first (pillar before spokes), then E2/E1 (highest commercial intent), then H1/H2 (volume), then the rest.

## Seeded 2026-07-02 — WP draft IDs (slug reserved, brief inside each draft)
E0=4960 E1=4961 E2=4962 E3=4963 E4=4964 E5=4965 E6=4966 E7=4967 ·
H1=4968 H2=4969 H3=4970 H4=4971 H5=4972 H6=4973 H7=4974 H8=4975.
Writers: wp-admin → Posts → Drafts, or REST GET /wp/v2/posts/<id>?context=edit.
