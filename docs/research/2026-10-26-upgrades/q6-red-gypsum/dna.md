# Q6 /glossary/לוח-גבס-אדום/ : competitor DNA and build spec (research 25.10.2026, evening)

Page: https://nad-lan.co.il/glossary/לוח-גבס-אדום/ (live, assets 1.72.519; raw HTML read 25.10.2026 21:27 Israel with `?x=random`).
Research only: no site change, no Linear or Notion item.

Evidence: SERP JSON + `q6-summary.md`, `q6x-summary.md` ("גבס ורוד") in `C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\serp\`; raw HTML/text in `...\raw\q6\` (SII pages in `raw\q6\sii\`, supplier price pages in `raw\q6\prices\`, Fire and Rescue directives 505 and 523 + Tel Aviv design spec in `raw\q6\fire\`); GSC CSV and volumes as in the Q3 file; `proof-before.md` (this folder), `proof-before-corrected.md` (this folder).

---

## 0. Urgent finding
Google's AI overview for **"גבס אדום"** and **"לוח גבס אדום"** lists **our page** as a source and says red board gives "לפחות 60 דקות (תקן ישראלי ת"י 1142 / ת"י 755)". Our page says "EI60 בהתאם לתקן ישראלי 1142". **ת"י 1142 is "מעקים ומסעדים" (guardrails and handrails)** per its SII page (30/05/2019). Fire resistance of a wall is tested under **ת"י 931**; reaction to fire is classified under **ת"י 755**. Our error is being repeated by Google. Fix this sentence first, in the same release as anything else on this page (or alone, as a one-line correction, if the full rebuild waits).

---

## 1. Intents and keywords

### 1.1 GSC (90 days): 24 queries, 390 impressions, 0 clicks
| Query | Impr. | Pos. | Volume/mo (IL) |
|---|---|---|---|
| גבס אדום | 134 | 9.4 | 110 |
| לוח גבס כתום | 81 | 27.8 | 10 |
| לוח גבס אדום | 71 | 11.6 | 20 |
| לוח גבס נוגד בעירה | 37 | 37.8 | n/a |
| גבס אדום חסין אש | 21 | 22.2 | 10 |
| גבס צהוב | 5 | 33.4 | 90 |
| דיבל גבס אדום | 5 | 34.6 | n/a (an anchor, not a board) |
| בחירת לוח גבס / עובי לוח גבס / משקל לוח גבס | 4 / 4 / 3 | 26 / 10 / 10 | משקל 20 |
| גבס אדום עמידות אש / גבס ורוד עמידות אש | 3 / 3 | 20 / 60 | |
| לוח גבס ורוד / לוח גבס חסין אש / גבס עמיד בחום | 2 / 2 / 2 | 78 / 40 / 34 | ורוד 30, חסין אש 20 |
| גבס אדום מחיר, מידות לוח גבס, סוגי לוחות גבס, לוח גבס צהוב | 1 each | 11 to 93 | מידות 110, סוגים 40 |
Big synonym the page never uses: **"גבס ורוד" 90/mo** (our page has "ורוד" 0 times; Tambour, the manufacturer, calls the product "לוח גבס ורוד (FR)").

### 1.2 Owned intents
1. **What red board is**: גבס אדום, לוח גבס אדום, גבס ורוד, לוח גבס ורוד, פלטת גבס ורוד.
2. **Fire performance and standards**: גבס אדום חסין אש, עמידות אש, נוגד / מעכב בעירה, לוח גבס חסין אש, גבס עמיד בחום, ת"י 931, ת"י 755.
3. **Specs**: עובי, מידות, משקל.
4. **Price**: גבס אדום מחיר, מחיר לוח גבס ורוד.
5. **Choosing among colours** (as a comparison inside this page, not as a new owner): כתום, צהוב, כחול, ירוק, לבן, משולב.

### 1.3 "לוח גבס כתום": same product or different? (evidence)
- SERP for "לוח גבס כתום": rank 1 mercaz-hageves.co.il "לוח גבס אקסטרים בורד לחיפוי חיצוני"; Google's AI overview: "לוח גבס כתום (המוכר בשם אקסטרים בורד - EXTREME BOARD) הוא לוח ייעודי לחיפוי חיצוני", glass-fibre mesh on both faces instead of paper, weather and mould resistant. No fire-board page in its top 10.
- The importer's page (מרכז הגבס אור יהודה, "היבואן הרשמי"): gypsum core wrapped in glass fibre on both faces, water and mould resistant, thermal insulation, cut with a utility knife, for external walls without blocks or plaster.
- **Decision: a different product (exterior sheathing board), not a red fire board.** Our page gets 81 impressions at 28 because Google tests a gypsum page that names colours. Serve that searcher with one honest row in the colours table and one FAQ ("לוח גבס כתום הוא לוח חוץ, לא לוח אש"). Do not put "כתום" in the title, H1 or H2. No new URL (owner law; and 10 searches a month do not justify one).
- Same logic for "גבס צהוב" (DensGlass, Georgia Pacific glass-mat board for exterior and interior light construction, per probuilder.co.il) and "לוח גבס כחול" (Tambour סופרבורד: blue, antibacterial, exterior and wet rooms; 260/mo): rows in the table only.

### 1.4 Cannibalization
`url_word_audit.py --token גבס`: /glossary/לוח-גבס-אדום/, /glossary/טיח-גבס/, /glossary/לוח-גבס-ירוק/. `--token לוח`: red, green, /glossary/לוח-זמנים-חוזי/. `--token אדום`: this URL only. `--token כתום`: none. GSC overlaps: "לוח גבס" red 1@17 vs green 10@44; "סוגי לוחות גבס" red 1@93 vs green 2@68; "גבס" red 3@47 vs plaster 1@52. Rule: red page owns אדום / ורוד / נוגד בעירה / חסין אש; green page owns ירוק / עמיד מים; the generic "סוגי לוחות גבס" stays unowned (neither title targets it); the red page links to the green page in the colours table. No new URL, no redirect, no noindex.

---

## 2. SERP snapshot (DataForSEO live advanced, google.co.il, Israel, Hebrew, desktop; 25.10.2026 19:23 to 19:44 UTC)

### "גבס אדום" (110/mo)
AI overview **present** (position 2): "גבס אדום (המכונה לעיתים גם גבס ורוד) הוא לוח גבס ייעודי ... עמידות גבוהה בפני אש"; core with glass fibres and vermiculite; uses: stairwells, escape corridors, server rooms, lift shafts, steel walls, public buildings; "לפחות 60 דקות (תקן ישראלי ת"י 1142 / ת"י 755)"; 12.5 or 16 mm, 1.2 m wide, lengths 2.6 or 2.8 m.
AI sources: mercaz-hageves.co.il/סוגי-לוחות-הגבס-השונים/, midrag.co.il/Midragonim/Answer/25353, cnaanc.co.il/product/לוח-גבס-אדום/, mercaz-hageves.co.il/לוח-גבס-ורוד/, tambour.co.il/.../לוחות-גבס/, **nad-lan.co.il/glossary/לוח-גבס-אדום/**.
PAA: מה המחיר של פלטת גבס אקוסטית? / איזה סוג גבס עמיד במים? / האם ניתן להתקלח עם גבס קל? / מה המחיר של קיר גבס? / מהו העובי המינימלי של קיר גבס? / איך בונים גבס?
Image packs at positions 4 and 14.
| # | Domain | Title |
|---|---|---|
| 1 | mercaz-hageves.co.il | לפני שאתם בוחרים לוחות גבס אתם חייבים לראות את זה! |
| 2 | tagtech.co.il | לוח גבס אדום 2.60 מטר (product, 70 ₪) |
| 3 | youtube.com | סוגי דיבלים לגבס, חלק ד', דיבל רוזט אדום |
| 4 | rotenberg1929.co.il | לוחות גבס לבניית קיר גבס במחירים משתלמים (price catalogue) |
| 5 | my-gypsum.co.il | סוגי לוחות גבס – מדריך השוואה |
| 6 | d4design.co.il | מה זה גבס אדום? (a glossary entry) |
| 7 | mercaz-hageves.co.il | לוחות גבס: כל הסוגים, מחירים וקונסטרוקציה |
| 8 | tambour.co.il | בנייה בגבס |
| 9 | scenter.co.il | לוחות גבס (shop) |
| 10 | shiplus.co.il | לוחות גבס: סוגים, שימושים וחברות מובילות |
Related: לוח גבס כחול מחיר / ירוק מחיר / גבס כחול חסרונות / לבן מחיר / מחיר לוח גבס 3 מטר / לוחות גבס מחיר זאפ / לוח גבס 6 מ"מ / כחול מחיר זאפ.

### "לוח גבס אדום" (20/mo)
AI overview **present**, same text (again "ת"י 1142 / ת.י 755"), sources again include our page. PAA: מה המחיר של לוח גבס אדום? / איזה לוח גבס הכי חזק? / איזה סוג גבס עמיד למים? / מה המחיר של לוח גבס? / מהם המידות של לוח גבס לבן? / מה המחיר למטר של עבודת גבס?
Top 10: 1 mercaz-hageves סוגי לוחות הגבס; 2 tambour לוחות גבס; 3 cnaanc לוח גבס אדום; 4 mgeves "לוח גבס אדום חסין אש 120/280"; 5 knauf.com לוחות גבס; 6 mercaz-hageves "לוח גבס ורוד חסין אש אורבונד"; 7 midrag "גבס חסין אש, איזה מומלץ? שאלנו 27 קבלני גבס"; 8 YouTube "סוגי לוחות גבס"; 9 rotenberg "קירות ומחיצות מעכבי בעירה"; 10 peryltd. **15: ours.**

### "גבס אדום חסין אש"
AI overview **present**: red, often called pink; core gypsum + vermiculite + glass fibres, pink-red paper; thickness 12.5 to 15.9 mm, "מגן אש" series 18 to 24 mm; standards ת"י 931 (integrity, stability, insulation) and ת"י 755 (flame spread and smoke); **price: standard 2.6 m board around 45 to 58 ₪ before VAT and delivery**. Sources: midrag 28634, probuilder pink, noyman-wood, shiplus, rotenberg catalogue, golmat, harishon-labinyan, vakninpro.
Top 10: noyman-wood product; golmat; midrag סוגי לוחות; YouTube; harishon-labinyan product; mercaz-hageves tag; antifire; mercaz-hageves tag; vakninpro product; mercaz-hageves לוחות גבס.

### "לוח גבס נוגד בעירה"
AI overview **present**: fire-retardant board usually pink, red or silver (Silver Board combinations); additives such as glass fibres or chemically bound water; partitions from one hour to several hours by thickness and system; ת"י 931 = fire resistance test of building elements; ת"י 755 = behaviour of building materials in fire. Sources: shiplus, Instagram, cohentools (Tambour pink "מעכב בערה"), antifire "תקן 75 גבס", golmat.
Top 10: rotenberg catalogue; golmat; antifire; amrusi silver board; YouTube super board; antifire "תקן 75"; midrag; cohentools Tambour pink; scenter; shiplus. Related includes "לוח גבס כתום".

### "לוח גבס כתום" (10/mo) and "גבס ורוד" (90/mo)
Orange: see 1.3. Pink: AI overview present (pink fire-resistant board for partitions, linings, ceilings and shafts; "המחיר ללוח בסטנדרט של 12.5 מ"מ נע בדרך כלל בין 48 ..."); top 10: mgeves red 120/280; midrag; aacenter; rotenberg standards certificates; mercaz-hageves "לפני שאתם בוחרים"; shiplus; probuilder FirePlus Orbond; amrusi combined green/pink; archijob "מחיצת אש ל-60 דקות"; ynet "ורוד או ירוק: הכול על קירות גבס בבית". PAA: מה המחיר של גבס חסין אש? / מה המחיר למטר של עבודת גבס? / האם גבס כחול עמיד למים? / מהו העובי המינימלי של קיר גבס? / מה המחיר של לוחות גבס? / איך בונים גבס?

---

## 3. Competitor DNA (corrected depth counts)

| Page | Rank | Title / H1 | Words | Tables (cells) | FAQ | Dated |
|---|---|---|---|---|---|---|
| mercaz-hageves סוגי לוחות הגבס השונים | 1 (לוח גבס אדום), AI source | title ends "...לוח גבס ירוק \| לוח גבס אדום" / H1 "סוגי לוחות הגבס השונים" | 407 | 0 | 0 | 2013, mod. 2024 |
| my-gypsum.co.il/סוגי-לוחות-גבס/ | 5 | "סוגי לוחות גבס – מדריך השוואה" / H1 "סוגי לוחות גבס: לבן, ירוק, ורוד, כחול ומה מתאים לכם" | 1,224 | 1 (35) | 4 | 30.9.2026 |
| d4design.co.il/terms/גבס-אדום/ | 6 | "מה זה גבס אדום?" | 284 | 0 | 1 | 27.11.2022 |
| midrag Answer 25353 | 16 (לוח), AI source | "גבס אדום עמידות אש" | 278 | 0 | 1 (QAPage) | none |
| golmat.co.il pink fire board | 2 (חסין אש / נוגד) | "אודות לוח גבס ורוד חסין אש" | 458 | 0 | 0 | mod. 9.8.2026 |
| rotenberg fire partitions | 9 (לוח) | "קירות ומחיצות מעכבי בעירה חסיני אש עם לוחות גבס" (H1 dated 11.05.25) | 752 | 11 (76) | 0 | 11.5.2025 |
| tambour.co.il boards catalogue | 2 (לוח), AI source | "לוחות גבס ופלטות גבס" | 1,542 | 0 | 0 | mod. 27.7.2026 |
| nor-rahamim colours guide | 13 (לוח) | "לוח גבס: לבן, ירוק, אדום, כחול, מה ההבדל" | 492 | 1 (10) | 3 | mod. 17.10.2026 |
| mercaz-hageves orange page | 1 (כתום) | "לוח אקסטרים בורד לחיפוי חיצוני" | 328 | 0 | 2 | 2018, mod. 2019 |

**Mercaz HaGeves (retailer, Or Yehuda).** Old URLs with exact phrases in titles, short colour blurbs ("לוח גבס אדום מגיע לעתים גם בצבע ורוד"), product pages with Orbond technical data. **Why it ranks:** age, many internal pages on every board type, retailer authority; Google's AI uses it for definitions.
**My-Gypsum (30.9.2026).** "בקצרה" answer first, comparison table of six types (colour, main property, when to use, when not), cutting guide, FAQ schema. **Why it ranks:** answer-first plus a clean comparison table, fresh.
**D4Design.** A glossary entry with exact title "מה זה גבס אדום?". Thin. **Why it ranks:** exact-match glossary format, the same format as ours: we beat it only by depth.
**Midrag.** One Q&A paragraph plus contractor listings, QAPage schema. **Why it ranks:** domain authority and exact question.
**Golmat.** Pink fire board article that names ת"י 931 (integrity, stability, insulation) and ת"י 755. **Why it ranks:** exact "ורוד חסין אש" and the standards.
**Rotenberg (architects' info).** Tested fire partitions with layers, studs, wool density, minutes, ת"י 931 and 755, plus prices per m² of special boards. **Why it ranks:** the only data-rich page; architects' intent.
**Tambour (manufacturer).** 12 boards with codes (RE, FR, SB, FD, MRWR, FM, HD) and one-line purposes. **Why it ranks:** the brand; Google treats it as the product authority.

---

## 4. Union checklist and gaps

| Topic | MH | MYG | D4D | MID | GOL | ROT | TAM | NOR | Ours now |
|---|---|---|---|---|---|---|---|---|---|
| Red = pink naming | yes | yes | no | no | pink only | pink | pink (FR) | yes | **no "ורוד" at all** |
| Core composition | brief | brief | no | "תוספים" | brief | brief | no | brief | "סיבים סינתטיים" (wrong) |
| Interior only | no | no | no | no | no | no | yes | no | no |
| Thickness / sizes / weight | product page | partly | no | no | no | yes | no | 12.5 | weight "8 to 12 ק"ג" (unsourced) |
| Fire minutes belong to the wall system | no | no | no | "not absolute" | partly | yes (tested systems) | no | no | **no; gives "EI60" for the board** |
| Correct standards 931 / 755 / 1490 | no | no | no | no | 931, 755 | 931, 755 | 755 | no | **ת"י 1142 (wrong)** |
| Fire authority rules | no | no | no | no | no | no | no | no | no |
| Prices with dates | catalogue | no | no | no | no | per m², 11.5.25 | no | no | no |
| Colour comparison incl. orange, yellow, blue, combined | partly | 6 types | no | partly | no | no | products | 4 colours | no |
| Tool | no | no | no | no | no | no | no | no | no |
| FAQ | 0 | 4 | 1 | 1 | 0 | 0 | 0 | 3 | 0 |

**Nobody covers:** one page that says plainly that fire minutes are a property of the tested wall (ת"י 931 חלק 1.8 for non-load-bearing partitions), not of the board; the three standards with what each tests (931 / 755 / 1490 חלק 1); the Fire and Rescue directives' own definition; dated price comparison across suppliers; the full colour map including orange, yellow, blue and combined; a tool that turns a wall into boards, weight and cost with the documents to ask for.

---

## 5. What Google wants to show
Definition with the pink synonym, composition (glass fibres, vermiculite), uses, the standards, thickness and sizes, a price range (the AI overview already shows 45 to 58 ₪), and the difference from green and blue. For "כתום" it wants the exterior Extreme Board answer. Images matter (two image packs). The AI answer currently borrows our wrong standard number: a corrected, sourced page is the most direct way to change what Google says.

---

## 6. Verified facts (fetched 25.10.2026 21:2x to 21:5x Israel)

**Manufacturer and distributor data**
| Fact | Source |
|---|---|
| Tambour boards: לוח גבס ורוד (FR) מעכב בעירה, **לשימוש פנימי בלבד**, for partitions and suspended ceilings where a defined fire-resistance requirement exists; also 4-bevel FR | tambour.co.il/קטלוג-מוצרים/בנייה-בגבס/לוחות-גבס/ (mod. 27.7.2026) |
| Tambour: דיפנדר+ (FD) pink fire board 22 mm, interior; Superfire 250/24 exterior board classified A1 under ת"י 755; פיירדיפנדר (FD) special fire board for lift shafts, extraction shafts, concealed systems, ducts, partitions, columns and steel walls | same |
| Tambour: משולב (FM) green-pink board, fire-retardant plus water and moisture resistance, interior; ירוק (MRWR) water and moisture, interior; סופרבורד (SB) blue antibacterial for exterior and wet rooms; סילברבורד (HD) acoustic, impact-resistant; רגיל (RE) interior | same |
| Orbond pink board: core gypsum + vermiculite + glass fibres; thickness 12.5 or 16 mm; length 2,600 / 2,800 / 3,000 mm, up to 3,600 by special order; width 1,200 mm; weight about 9.2 kg/m² (12.5 mm) and 11.5 kg/m² (16 mm); edges straight, 2-side or 4-side bevel; SII standard mark and fire classification document available | mercaz-hageves.co.il/לוח-גבס-ורוד/ (distributor page with Orbond data, mod. 2019) |
| Board weights (Rotenberg table, page dated 14.10.26): 12.5 mm × 1.20 m: 2.00 m 21 kg, 2.60 m 27 kg, 2.80 m 29 kg, 3.00 m 31 kg; 16 mm: 2.60 m 34 kg, 2.80 m 37 kg, 3.00 m 40 kg; Fire Defender 24 mm 2.50×1.20 69 kg; Fireboard 25 mm 2.25×1.20 51 kg; Fire Plus 25 mm 2.25×1.20 49 kg | rotenberg1929.co.il/.../לוחות-גבס-מידות-ומשקלות |
| Tested partitions published by Rotenberg (page dated 11.05.25): 120 minutes with 4 pink fire boards 12.5 mm (2 per side) on 70 mm steel studs and 5 cm mineral wool 24 kg/m³, "מאפייני שריפה לפי ת"י 755, בדיקת מחיצה לפי ת"י 931"; 120 minutes with 2 Villa Board 9 mm + 2 fire gypsum 15.9 mm on 70 mm studs; 2 Fire Defender 24 mm on steel frame: insulation 157 min, stability and integrity 180 min; uses: lift shaft, steel frame protection, pipes, one-sided partitions | rotenberg1929.co.il/Information-for-architects/מחיצות-גבס-חסיני-אש-חתכים |
| Orange = EXTREME BOARD, exterior cladding, gypsum core with glass fibre on both faces; importer מרכז הגבס אור יהודה | mercaz-hageves.co.il/לוח-כתום-לחיפוי-חיצוני-extreme-board/ |
| Yellow = DensGlass (Georgia Pacific), glass-mat faced, exterior and interior light construction | probuilder.co.il/product/לוח-גבס-צהוב-densglass/ |

**Prices (supplier sites on 25.10.2026; this is the date of the source)**
| Supplier | Product | Price shown |
|---|---|---|
| רוטנברג (catalogue dated 17.09.26) | לוח גבס ורוד 12.5 מ"מ, 2.60×1.20 (מק"ט 10903) | 68.5 ₪ before VAT, 80.8 ₪ with VAT; 21.95 ₪/m² before VAT |
| רוטנברג | לוח גבס ורוד 12.5 מ"מ, 2.00×1.20 (10905) | 53.1 ₪ before VAT, 62.7 with VAT; 22.1 ₪/m² |
| רוטנברג | לוח גבס לבן 12.5 מ"מ, 2.60×1.20 (10904) | 52 ₪ before VAT, 61.4 with VAT; 16.6 ₪/m² |
| מרכז הגבס (mgeves) | לוח גבס אדום חסין אש 1.20×2.80, ORBOND / KNAUF (120289) | 71 ₪ |
| טגטק | לוח גבס אדום 2.60 מטר | 70 ₪ |
| ועקנין | פלטת גבס ורוד חסין אש 2.6 מטר | 58 ₪ |
| כהן כלים | לוח גבס ורוד מעכב בערה, טמבור | 53 ₪ |
| אמרוסי | לוח גבס ורוד חסין אש | from 52.50 ₪ |
| נוימן | פלטה גבס 2.60/1.20/12.50 חסין אש | 81.42 ₪ (free delivery) |
VAT status is stated only by Rotenberg; show the others "כפי שמופיע באתר". Board length is not stated on the כהן כלים and אמרוסי pages, so the 2.60 m range in Table A uses only רוטנברג (80.8 with VAT), טגטק, ועקנין and נוימן: 58 to 81.42 ₪. Derived: at Rotenberg the pink 2.60 board costs 32% more than the white one of the same size (68.5 vs 52).

**Standards (SII pages)**
| Standard | Title | Edition | What it does |
|---|---|---|---|
| ת"י 931 חלק 1.1 | עמידות אש של אלמנטי בניין, שיטות בדיקה: דרישות כלליות | 31/07/2014 (645.50 ₪) | test method; elements classified by how long they meet the criteria under standard fire |
| ת"י 931 חלק 1.8 | ...דרישות ספציפיות לאלמנטים לא-נושאים מפרידים אנכיים | 31/12/2012 (236 ₪) | non-load-bearing vertical separating elements (partitions), one face heated; not for curtain walls or walls with doors or glazing (doors: ת"י 1189 חלק 1; glazing: ת"י 931 חלק 3) |
| ת"י 755 | סיווג בשרפה של מוצרי בנייה ושל אלמנטי בניין: סיווג לפי נתוני בדיקות של תגובות בשרפה | 30/11/2023 (826 ₪) | reaction-to-fire classification of construction products |
| ת"י 1490 חלק 1 | מחיצות וחיפויי גבס: לוחות | 01/12/1993, status "רשמי חלקית", 2 amendment sheets (310.70 ₪) | gypsum boards up to 25 mm for partitions and internal linings of walls and ceilings |
| ת"י 1142 | מעקים ומסעדים | 30/05/2019 | guardrails and handrails; **not a fire standard** |

**Fire and Rescue Authority directives (gov.il PDFs)**
- הוראת נציב 505, fire safety in hospitals and health institutions (update December 2020): "אלמנט עמיד אש: חלק בנין בעל עמידות אש כמוגדר בתקן ישראלי ת"י 931, למשך 90 דקות או כל זמן אחר שנקבע בהוראות אלה".
- הוראת נציב 523, fire safety in educational institutions (update August 2022), 7.1.6: all ceilings and walls that separate parts of the building meet ת"י 931 and the fire resistance required by building legislation.
- Tel Aviv-Yafo municipality engineering design portal (pb-tlv.tel-aviv.gov.il): fire partitions follow the planning and building regulations, commissioner directives and ת"י 931; wall fire resistance not less than 60 minutes (municipal design guideline).

**Calculated:** gypsum (calcium sulphate dihydrate, CaSO4·2H2O) holds 20.9% chemically bound water by mass (2 × 18.02 / 172.17), which it releases when heated: this is why gypsum slows heat transfer.

**Unverified, keep out:** "EI60 for a single board"; minute ratings for any wall not published by a manufacturer or supplier; "8 to 12 kg/m²"; ממ"ד requirements; whether retail prices include VAT; the AI overview's 45 to 58 ₪ range (use our own dated table instead); "תקן 75" (antifire's term).

---

## 7. Our page today
- Title "לוח גבס אדום - נדלן" (19 chars); H1 "לוח גבס אדום"; meta = definition.
- Order: H1, empty "Written by / in", EN line "Fire resistant gypsum board · material", definition, **no H2** (7 H3: רקע, מנגנון טכני, מפרט טכני, הקשר ישראלי, בפרויקט אמיתי, דוגמה מספרית, טעויות נפוצות), related terms (ריצוף גרניט פורצלן, לוח גבס ירוק, טיח גבס, פרופיל פח מגולוון), "More posts".
- 739 words, 0 tables, 0 FAQ, **no BreadcrumbList schema** (Q3 and Q5 have it), datePublished 9.7.2026.
- **Errors:** "EI60 בהתאם לתקן ישראלי 1142" and "ת"י 1142, המפרט את דרישות העמידות לאש" (wrong standard); "סיבים סינתטיים" (manufacturer data: glass fibres and vermiculite); "שכבות הגנה נוספות" (unsupported); weight "8 עד 12 ק"ג למ"ר" (unsourced; Orbond: 9.2 and 11.5); the board itself credited with 60 minutes.
- The quantity example (3 m × 100 m wall, 1.2×3.0 boards, +10%) is arithmetic, keep it but move it into the tool and label the 10% as the reader's choice.
- Keep: H1, EN line, definition (corrected), the 7 topics (as H2, corrected), related terms, site bar, DefinedTerm schema.

---

## 8. BUILD SPEC

### 8.1 Strings
- **Title (57 chars incl. suffix):** `לוח גבס אדום (ורוד): עמידות אש, תקנים, מידות ומחיר - נדלן`
- **H1 (unchanged):** `לוח גבס אדום`
- **Meta (≤155):** `לוח גבס אדום, שנקרא גם לוח גבס ורוד: ממה הוא עשוי, מה בודקים לפי ת"י 931 ות"י 755, עוביים, משקל ומחירים אצל ספקים, והשוואה ללוח כתום, כחול וירוק.`
- **Answer paragraph (51 words):**
  > לוח גבס אדום, שהיצרנים קוראים לו גם לוח גבס ורוד או לוח מעכב בעירה, הוא לוח לשימוש פנימי שבליבתו יש סיבי זכוכית וורמיקוליט, כדי שהקיר יחזיק יותר זמן מול אש. את דקות העמידות מקבל הקיר כולו בבדיקה לפי ת"י 931, לא הלוח לבדו. העוביים הנפוצים 12.5 ו-16 מ"מ, ברוחב 1.20 מטר.

### 8.2 Section order
1. H1, EN line, answer paragraph, date line.
2. CTA "לקבלת פרטים נוספים בוואטסאפ" + anchor "חשבו כמה לוחות צריך".
3. **Box "לוח גבס אדום במספרים"** (Table A).
4. **The moat tool** (8.4).
5. H2 `צבעי לוחות הגבס: מה כל צבע אומר` (Table B, includes orange, yellow, blue, combined; links /glossary/לוח-גבס-ירוק/).
6. H2 `עמידות אש: למה בודקים את הקיר ולא את הלוח` (931 חלק 1.1 and 1.8; 755; 1490 חלק 1; the bound-water explanation; a one-line correction note is not needed on the page, just the right facts).
7. H2 `מחיצות אש שנבדקו: דוגמאות מספקים` (Table C, labelled "נתוני ספק").
8. H2 `מה דורשים כבאות והצלה` (directives 505 and 523, Tel Aviv guideline; "the required minutes come from the fire safety consultant and the permit"; link to a fire-safety-consultant term if one exists, else plain text).
9. H2 `מידות, עובי ומשקל של לוח גבס אדום` (Orbond data + Rotenberg weights; calculated board weight 12.5 mm × 2.60 × 1.20 ≈ 28.7 kg from 9.2 kg/m², labelled "חישוב").
10. H2 `מחיר לוח גבס אדום` (Table D with the date).
11. H2 `גבס אדום, ורוד, משולב או מיוחד לאש: איך בוחרים` (FR vs FM for wet areas with fire needs vs Defender/Fire Defender for shafts and steel; interior only; exterior: Superfire per Tambour).
12. Existing topics as H2, corrected: `רקע על לוחות גבס אדומים`, `מנגנון טכני` (glass fibres, vermiculite, bound water), `מפרט טכני` (verified numbers only), `הקשר ישראלי` (standards and directives), `בפרויקט אמיתי` (keep; add: ask for the 931 test report of the system you install), `דוגמה מספרית` (keep the arithmetic, link to the tool), `טעויות נפוצות` (keep + quoting minutes for a single board, using orange/yellow/blue as a fire board, using red outdoors, mixing a tested system with other studs or screws, citing ת"י 1142).
13. H2 `שאלות נפוצות על גבס אדום` (8.6) + FAQPage schema.
14. Related terms (existing) + add BreadcrumbList schema (parity).
15. One compact line "לבדיקה במקור": the two gov.il directives (official sources, no clutter).

### 8.3 Tables

**Table A. לוח גבס אדום במספרים**
| | |
|---|---|
| שמות נוספים | לוח גבס ורוד, לוח מעכב בעירה (FR) |
| שימוש | פנימי בלבד |
| מה יש בליבה | גבס, ורמיקוליט, סיבי זכוכית |
| עובי | 12.5 או 16 מ"מ (לוחות מיוחדים לאש: 22, 24, 25 מ"מ) |
| רוחב | 1.20 מטר |
| אורך | 2.60, 2.80, 3.00 מטר; עד 3.60 בהזמנה |
| משקל | כ-9.2 ק"ג למ"ר (12.5 מ"מ), כ-11.5 ק"ג למ"ר (16 מ"מ) |
| תקן ללוח | ת"י 1490 חלק 1 (לוחות גבס עד 25 מ"מ) |
| בדיקת אש לקיר | ת"י 931 חלק 1.8 (מחיצה לא נושאת) |
| סיווג תגובה באש | ת"י 755 |
| מחיר | 58 עד 81.42 ₪ ללוח 2.60 מטר אצל ארבעה ספקים, נבדק ב-25.10.2026 |

**Table B. צבעי לוחות הגבס**
| צבע | שם נפוץ | למה מיועד | איפה לא |
|---|---|---|---|
| לבן | לוח רגיל (RE) | מחיצות, חיפויים והנמכות בחדרים יבשים | חדר רטוב, דרישת אש |
| ירוק | עמיד מים ולחות (MRWR) | חדרים רטובים, פנימי | חוץ |
| אדום או ורוד | מעכב בעירה (FR) | מחיצות ותקרות עם דרישת עמידות אש, פנימי | חוץ |
| ירוק ורוד | משולב (FM) | אש יחד עם מים ולחות, פנימי | חוץ |
| ורוד עבה | דיפנדר+ 22 מ"מ, פיירדיפנדר | פירים, תעלות, עמודים וקירות פלדה | |
| כחול | סופרבורד (SB) | חוץ וחדרים רטובים, אנטיבקטריאלי | |
| כתום | אקסטרים בורד | חיפוי חיצוני, סיבי זכוכית בשני הצדדים | אינו לוח אש |
| צהוב | דנסגלאס | בנייה קלה בחוץ ובפנים, עמיד ברטיבות | אינו לוח אש |
| כסוף | סילברבורד (HD) | אקוסטי וחזק לנגיפה | |

**Table C. מחיצות שנבדקו (נתוני ספק, רוטנברג, 11.05.25)**
| מחיצה | שלד | בידוד | עמידות | בדיקה |
|---|---|---|---|---|
| 2 לוחות ורודים 12.5 מ"מ מכל צד | ניצבי פלדה 70 מ"מ | צמר 5 ס"מ, 24 ק"ג למ"ק | 120 דקות | ת"י 931, סיווג ת"י 755 |
| וילה בורד 9 מ"מ ולוח גבס חסין אש 15.9 מ"מ מכל צד | ניצבי פלדה 70 מ"מ | | 120 דקות | ת"י 931 |
| 2 לוחות מגן אש 24 מ"מ | שלד פלדה | | בידוד 157 דקות, יציבות ושלמות 180 דקות | |

**Table D. מחיר לוח גבס אדום (נבדק ב-25.10.2026)** : the price table of section 6, as is.

### 8.4 THE MOAT: "מחשבון קיר גבס אדום: כמה לוחות, כמה משקל, כמה עולה ומה לבקש"
A [nadlan_tool] mount. Inputs: מקום הקיר (מחיצה בבית / חדר רטוב / חדר מדרגות או מסדרון / פיר או צנרת / הגנה על פלדה / קיר חוץ), דרישת אש מהיועץ (אין / 30 / 60 / 90 / 120 דקות), אורך וגובה הקיר, צדדים (1 או 2), שכבות בכל צד (1 או 2), מידת לוח (2.00 / 2.60 / 2.80 / 3.00 × 1.20), עובי (12.5 / 16), פחת באחוזים (the reader sets it), מחיר ללוח (prefilled from Table D, editable).
Output: מספר לוחות, משקל כולל (9.2 / 11.5 ק"ג למ"ר), עלות משוערת, the board type from Table B (red, combined, special fire, or "לוח אש אינו מתאים לחוץ"), the matching tested example from Table C when one exists (labelled "דוגמה של ספק, לא אישור לקיר שלכם"), and a checklist of documents: תעודת בדיקה למחיצה כולה לפי ת"י 931, סיווג לפי ת"י 755, תו תקן ללוח לפי ת"י 1490 חלק 1.
Why a moat: zero tools in the SERP; it joins the three things searchers ask (what board, how many, how much) and the one thing nobody says (minutes belong to the tested wall).

### 8.5 Infographics
1. **"חתך מחיצה חסינת אש"**: exploded section of the tested 120-minute partition (board, board, stud 70 mm, wool, board, board) with the standard tags 931 / 755 / 1490. Design brief (owner law 13.10): drawn like a fire-safety plan sheet: white paper, black line work, fire-rated layers in red hatching with the minutes in a boxed label, insulation in the grey wavy hatch drafters use for wool; faces IBM Plex Sans Hebrew and IBM Plex Mono for minutes, thicknesses and standard numbers. Why not the default: it is the drawing a fire consultant hands a contractor, not a cream card or a dark background with one red pop.
2. **"מפת הצבעים"**: nine boards in a strip with one word each (רגיל, מים, אש, אש ומים, אש כבדה, חוץ, חוץ, חוץ, שקט).

### 8.6 FAQ (16)
1. מה זה גבס אדום?
2. מה ההבדל בין גבס אדום לגבס ורוד?
3. האם גבס אדום חסין אש?
4. כמה זמן לוח גבס אדום עומד באש?
5. לפי איזה תקן בודקים קיר גבס חסין אש?
6. מה העובי של לוח גבס אדום?
7. כמה שוקל לוח גבס אדום?
8. מה המידות של לוח גבס אדום?
9. כמה עולה לוח גבס אדום?
10. כמה יותר יקר לוח אדום מלוח לבן?
11. אפשר לשים לוח גבס אדום בחוץ?
12. מה לשים בחדר רטוב שצריך גם עמידות אש? (FM)
13. מה זה לוח גבס כתום?
14. מה זה גבס צהוב?
15. מה זה לוח גבס כחול?
16. למה גבס מעכב אש?

### 8.7 Honesty target (corrected competitor maxima)
| Metric | Ours now | Best competitor | Target |
|---|---|---|---|
| words | 739 | 1,542 (Tambour catalogue) | ≥ 2,000 |
| figures | 34 | 73 (Rotenberg) | ≥ 80 verified |
| tables | 0 | 11 (Rotenberg, small single-system tables) | 5 real tables; honesty statement names Rotenberg on table count |
| cells | 0 | 76 (Rotenberg) | ≥ 110 |
| tools | 0 | 0 | 1 |
| faq | 0 | 4 (my-gypsum) | 16 visible |
| headings | 12 | 38 (Tambour, product cards) | ≥ 39 |
| visuals | 0 | 168 (Tambour, product photos) | 2 infographics + product-type images only if real; statement names Tambour |
| sources (official domains) | 0 | 0 | ≥ 2 (the two gov.il directives in one line) |
| dated | none | 17.10.2026 (nor-rahamim) | visible date + dateModified; price table carries its own check date |
Zero invented minutes, weights or prices; the ת"י 1142 sentence is removed in the first release.
