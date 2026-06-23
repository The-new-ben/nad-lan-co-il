# Rainbow Tel Aviv — SEO Dossier (SERP, Intent, International) + Paste-Ready Assets
**Date:** 2026-06-12 · **Author:** Claude (live-page audit + SERP analysis + schema build v1.60.4)
**Goal:** rank the page top-3 for Rainbow/Sde-Dov commercial queries in Hebrew, and pre-pack international (EN/FR/RU/AR) investor intent so translations rank from day one.

## 1. Live-page audit (what is actually served today)
| Element | State | Verdict |
|---|---|---|
| Title | `Rainbow Tel Aviv - ריינבו תל אביב \| בחירת דירות, מבט מהדירה ושדה דב \| נדלן חכם` | ✗ wastes prime chars on FEATURE names; zero transactional keywords |
| Meta description | features list | ✗ same problem — no price hook, no CTA |
| H1 | one visible (`nlpf-name`) ✓ | OK |
| H2 structure | 16 H2s, wiki-grade sections ✓ | strong |
| Body | 3,055 Hebrew words ✓ | strong, but intent skew: "למכירה" ×0, "מחיר" ×6, "דירות יוקרה" ×1, "פנטהאוז" ×2 |
| Schema | WebPage graph + ApartmentComplex (name/url/units/address ONLY) + 2× BreadcrumbList | thin — fixed in v1.60.4 |
| FAQPage schema | none despite real FAQ section | fixed in v1.60.4 (meta-driven) |
| Canonical/OG | correct ✓ | OK |
| IndexNow | pinging ✓ | OK |

## 2. SERP reality (who owns the queries)
Query "ריינבו תל אביב פרויקט דירות" top-10: rainbowtlv.com (developer, #1 navigational — unbeatable), sdedov.co.il/project/rainbow, Madlan project page, Calcalist ×2, Ynet, Bizportal ×2, Nadlanews, Ashtrom (contractor). **nad-lan.co.il absent.**

**Citable market facts surfaced (use with attribution):**
- ~272/480 units sold ≈ ₪2.4B total, ≈ ₪85K/m² (Calcalist, Nov 2025)
- Average unit price ≈ ₪10M; earlier avg ₪10.3M (Calcalist, Nadlanews)
- 3-room entry from ≈ ₪5.5M (Bizportal)
- 6 boutique buildings (8 floors) + 40-floor tower; developer ישראל קנדה; contractor אשטרום
- Celebrity validation: נועה קירל mini-penthouse ₪10M (Calcalist), יוסי כהן ₪14M (Ynet)

**The gap we win:** the developer's site is marketing-thin (no prices, no neutral analysis); Madlan is data-thin on THIS project; news articles are stale snapshots. Nobody serves: *"ריינבו תל אביב מחיר"*, *"כמה עולה דירה בשדה דב"*, *"ריינבו תל אביב כדאי?"*, comparison content, or an interactive picker. That's our page.

## 3. Hebrew intent → keyword map
| Intent | Queries | Our answer |
|---|---|---|
| Navigational | ריינבו תל אביב / rainbow tlv | Can't beat developer at #1 — target #2-3 with richer snippet |
| **Price (money)** | ריינבו תל אביב מחיר · מחיר למ"ר שדה דב · כמה עולה דירה בשדה דב | NEW price section with cited figures (block B below) |
| **Transactional** | דירות למכירה שדה דב · דירות יוקרה למכירה תל אביב · פנטהאוז שדה דב | "דירות למכירה" phrasing in title/H2/body (block A) |
| Evaluation | ריינבו תל אביב ביקורות / כדאי / חוות דעת | "בדיקות מומלצות" section exists — add verdict framing |
| Comparison | פרויקטים חדשים שדה דב · שדה דב או פארק צמרת | Compound taxonomy page + comparison block (block C) |

## 4. INTERNATIONAL intent (owner directive: pack it pre-translation)
Target personas: diaspora investors (US/FR/UK), olim, Russian-speaking buyers, Gulf/Arabic prestige buyers. Keywords to seed NOW in Hebrew content structure so EN/FR/RU/AR translations inherit the intent (per the Polylang plan in docs/2026-06-12-multilingual-architecture-research.md):

**English:** tel aviv apartments for sale · sde dov new development · luxury apartments tel aviv beachfront · israel real estate investment 2026 · buy apartment tel aviv pre-construction · tel aviv penthouse price per sqm
**French (huge olim/investor segment):** acheter appartement tel aviv · immobilier israël bord de mer · appartement neuf tel aviv sde dov · investissement immobilier israël
**Russian:** купить квартиру в тель-авиве · новостройки тель-авив сде дов · элитная недвижимость израиль
**Arabic (prestige segment):** شقق فاخرة تل أبيب · عقارات إسرائيل للبيع

**Content blocks engineered to survive translation** (add to the page now in Hebrew; they translate into ranking sections):
1. **"מדריך לרוכש מחו״ל"** — foreign-buyer essentials: מס רכישה for non-residents (8% from first shekel — verify current bracket with owner-the-lawyer before publish), non-resident mortgage LTV ~50%, remote purchase via ייפוי כוח, currency considerations. This single section targets EVERY language's "buying property in Israel as a foreigner" query family — high-volume, low-competition, and we have a lawyer-owner for E-E-A-T.
2. **Price block always with ₪ AND m² figures** — international buyers think in $/€/m²; keep numbers in machine-readable form so `Intl.NumberFormat` localizes them later.
3. **Distance facts** (beach 300m, נתב"ג 25 min, פארק הירקון) — universal relocation-buyer signals.

## 5. PASTE-READY ASSETS (owner: Yoast SEO fields + content editor)

**Title tag (Yoast "SEO title"):**
```
דירות למכירה ב-Rainbow תל אביב | מחירים, תוכניות ובחירת דירה בשדה דב | נדל"ן חכם
```
(Rainbow + ריינבו both appear in H1; title now leads with transactional intent. 68 chars Hebrew — within pixel budget.)

**Meta description (Yoast):**
```
ריינבו תל אביב (Rainbow TLV) ברובע שדה דב: מחירים מעודכנים (3 חד׳ מ-5.5 מ׳ ₪, ממוצע כ-85 אלף ₪ למ"ר), תמהיל דירות, בחירת דירה אינטראקטיבית במודל תלת-ממד, ומדריך רכישה מלא — כולל לרוכשים מחו"ל.
```

**Content block A — insert after the opening section (transactional anchor):**
```
## דירות למכירה ב-Rainbow תל אביב — מה זמין עכשיו
בפרויקט ריינבו תל אביב נמכרות דירות 2-5 חדרים, מיני-פנטהאוזים ופנטהאוזים, בין שישה בנייני בוטיק
(8 קומות) ומגדל בן 40 קומות. נכון לסוף 2025 דווח על מכירת כ-272 מתוך 480 יחידות (כלכליסט).
הזמינות מתעדכנת מול היזם — בחרו דירה במודל האינטראקטיבי למעלה ושלחו בקשת בדיקה, ללא התחייבות.
```

**Content block B — price section (the money query):**
```
## מחירי דירות בריינבו תל אביב — נתונים מדווחים
- מחיר ממוצע למ"ר: כ-85,000 ₪ (דיווח כלכליסט, נוב׳ 2025)
- מחיר ממוצע לדירה: כ-10 מיליון ₪ (כלכליסט)
- דירות 3 חדרים: החל מכ-5.5 מיליון ₪ (Bizportal)
- עסקאות בולטות שדווחו: מיני-פנטהאוז בכ-10 מ׳ ₪, דירה בכ-14 מ׳ ₪ (כלכליסט, Ynet)
הנתונים מבוססים על דיווחים פומביים ואינם הצעת מחיר. מחיר עדכני זמינות ותנאים — בבדיקה מול היזם דרך הטופס.
```

**Content block C — foreign-buyer guide (international intent seed):**
```
## מדריך לרוכשים מחו"ל — Rainbow Tel Aviv לתושבי חוץ
שדה דב הוא מהיעדים המבוקשים לרוכשים מצרפת, ארה"ב ורוסיה. נקודות מפתח לתושב חוץ:
מס רכישה לתושבי חוץ, מימון בנקאי לתושב חוץ (בדרך כלל עד כ-50% מימון), רכישה מרחוק באמצעות
ייפוי כוח נוטריוני, וליווי עו"ד מקרקעין דובר השפה. צוות נדל"ן חכם מלווה רוכשי חוץ בכל שלבי
העסקה. [הערה לבעלים: לאשר ניסוח שיעורי המס לפני פרסום]
```

**Custom fields to fill on the Rainbow post (drives the new v1.60.4 schema):**
| Meta key | Value to paste |
|---|---|
| `amenities` | `בריכות שחייה, ספא, חדר כושר, בית קפה פרטי, חללי עבודה, חצר ריזורט` |
| `official_site_url` | `https://rainbowtlv.com/` |
| `price_range` | `דירות 3 חד׳ מ-5.5 מ׳ ₪; ממוצע כ-10 מ׳ ₪ (מקורות: כלכליסט, Bizportal)` |
| `price_min` | `5500000` |
| `price_max` | `30000000` |
| `project_faq_json` | `[{"q":"כמה עולה דירה בריינבו תל אביב?","a":"לפי דיווחים פומביים: ממוצע כ-10 מיליון ₪ לדירה וכ-85 אלף ₪ למ\"ר; דירות 3 חדרים החל מכ-5.5 מיליון ₪. מחיר מחייב נקבע מול היזם."},{"q":"מי היזם והקבלן של Rainbow תל אביב?","a":"היזם: ישראל קנדה. הקבלן המבצע: אשטרום."},{"q":"כמה דירות נותרו למכירה בריינבו?","a":"נכון לסוף 2025 דווח על כ-272 יחידות שנמכרו מתוך 480. הזמינות העדכנית נבדקת מול היזם."},{"q":"האם תושב חוץ יכול לקנות דירה בריינבו תל אביב?","a":"כן. רכישה לתושבי חוץ אפשרית, כולל מרחוק בייפוי כוח, בכפוף למס רכישה לתושב חוץ ולתנאי מימון בנקאיים."}]` |

## 6. Implementation map
- **v1.60.4 (shipped, this commit):** schema enrichment — geo/image/description/amenities/sameAs/containedInPlace/AggregateOffer + FAQPage, all meta-driven.
- **Owner (10 min):** paste Yoast title+description, 3 content blocks, 6 custom fields above; then re-ping IndexNow happens automatically on update.
- **Already working for us:** compound taxonomy page (internal-link hub for "פרויקטים שדה דב"), IndexNow, breadcrumbs schema, 3,055-word body.
- **With Polylang later:** hreflang + /en/ /fr/ /ru/ pages inherit blocks A-C intent; keep numbers language-neutral (research doc: 2026-06-12-multilingual-architecture-research.md).
- **Honesty rails:** every price carries source + date; no figure presented as an offer; tax rates flagged for owner-lawyer review before publish.
