# /sde-dov/prices/ (page 4758): alignment edits check (HAD-460, 7.10.2026)

Companion to align-edits.json in this folder. Data only: nothing was applied, nothing published, nothing committed.
Audit behind it: docs/qa/had-460/sde-dov-prices-audit.md. Data file: scripts/project-stage/price_guide/sde-dov-prices.json.

## 1. Method

- Content: public `GET https://nad-lan.co.il/wp-json/wp/v2/pages/4758?_fields=id,link,title,content,yoast_head_json`
  (content.rendered), retrieved 2026-10-07 10:02:45 UTC, 29,521 characters, no HTML entities in it.
- 78 edits. A script applied them in order to content.rendered: 74 match exactly once; 3 are `replace_all` cells that
  match exactly twice (the same cell text sits in two tables: the 70,000-100,000 range, the 53,500 boutique price, the
  "מחיר עסקה ממוצע צפוי" label) and get one replacement for both; 1 (`spans_tags`) is the whole rooms `<table>`. Every
  other old string sits inside one paragraph, list item or cell (cell edits carry their own `<td>...</td>` because the
  same words also appear in running text). No new text contains an em dash, an en dash, "!" or an HTML entity.
- Kept as is: the title, the H1 "מחירי דירות בשדה דב", the URL, every H2 and H3 (the FAQ h3 "האם המחירים יכולים להגיע
  ל-150,000 ש״ח למ״ר?" carries a sourced number), the Yoast title and description (no numbers). No newspaper is named in
  the new text; dates carry the evidence ("לפי סקר דוחות היזמים מאפריל 2026"). Developer names are not added (the page
  already names two; they stay).
- The FAQ answers were rewritten from the same facts as the body: FAQ 1 "כמה עולה דירה בשדה דב?" = edit 74 (same facts
  as edits 3, 23-28); FAQ 2 "מה המחיר למ״ר" = edit 75 (as edits 1, 2, 4, 5); FAQ 3 "רמת אביב" = edit 76 (as edits 56,
  60); FAQ 6 "150,000" = edit 77 (as edit 69).
- Remaining-number check (script, after all edits): every number in the page text was extracted and matched to a
  source key. Years, room counts ("4 חדרים") and floor numbers are counted apart as structure.

## 2. Counts

| | before (audit) | after the edits |
|---|---|---|
| price claims in CONFLICT with a dated source | 8 | 0 |
| price claims with NO source | 9 | 0 |
| number tokens with no source key | 71 (script, before) | **0** |
| number tokens matched to a source key | | 151 (65 distinct values) |
| structural tokens (years / room counts / floors) | | 75 / 44 / 16 |

Edits by audit verdict: 41 CONFLICT, 31 UNSOURCED, 5 CONSISTENT (date or period added only), 1 DATE (footer "עודכן יוני
2026" to "עודכן אוקטובר 2026").

The rooms table: replaced (edit 26), not removed. The new table has five columns (סוג דירה, מה פורסם, מחיר, מחיר למ״ר,
מועד) and seven sourced rows: 2 rooms 2.8-3.1M (5.2026) and 54 m² at 3.665M (2026); 3 rooms 82-83 m² 4.6-4.8M (5.2026);
4 rooms average about 9.45M (survey 4.2026); 4-5 rooms 104-126 m² 6.49-7.73M (2026); 5 rooms 132 m² 7.16-7.57M (3.2026);
5 rooms 139.7 m² on one price list 11.954M (10.2025). The averages it replaces (46.8 m², 3.81M, 81,410, 6.86M, 11.61M)
had no source.

## 3. Source keys

Keys in `sde-dov-prices.json` (its sources block holds the URL, what it says and when it was read): NC2604, ICE1904,
ICE0305, ICE2105, BZ2606, ICE0606, ICE2510, NC2506, NC2507, BZ2512, NC2604F, ICE2512, TA. Extra keys used only here:

| key | source | read (UTC) | used for |
|---|---|---|---|
| GL2311 | https://www.globes.co.il/news/article.aspx?did=1001463064 (Globes 29.11.2023, Tax Authority data): a 1-room, 32 m² unit on floor 4 of the Rainbow tower, 3.1M, 7.2023. Reused from rainbow-tel-aviv.json | not re-read | the 32 m² deal (replaces "2.3M") |
| BZ2608 | https://www.bizportal.co.il/realestates/news/article/20036053 (Bizportal 2.8.2026): Ramat Aviv Gimmel average about 51-53K ILS/m2 | 7.10.2026 about 09:50 | Ramat Aviv |
| NC2503 | https://www.nadlancenter.co.il/article/11668 (Merkaz HaNadlan 3.3.2025): Yigal Dimri at a conference, in a decade or two prices can reach 150K ILS/m2 | 7.10.2026 09:48 | the 150,000 forecast |
| ICE0606 | https://www.ice.co.il/realestate/news/article/1114418 (ice 6.6.2026): Ramat Aviv recent deals average around 55K; new Sde Dov projects about 70-71K | 7.10.2026 about 09:50 | Ramat Aviv, 70,000 |

## 4. Every edit

Numbers = price and size figures in the old and the new text (years, room counts left out).

| n | section | where | numbers before | numbers after | source keys | verdict |
|---|---|---|---|---|---|---|
| 1 | מחירי דירות בשדה דב: תמונת שוק עדכנית | text | 81,000, 70,000, 100,000 | 1,280, 83,000, 70,000 | NC2604 ICE1904 ICE2105 ICE0606 | CONFLICT |
| 2 | מחירי דירות בשדה דב: תמונת שוק עדכנית | text | 90,000, 100,000 | 38, 43, 107,700, 119,200, 54,000-57,000 | BZ2512 ICE0305 | CONFLICT |
| 3 | מחירי דירות בשדה דב: תמונת שוק עדכנית | text | 7 | 9.45 | NC2604 | UNSOURCED |
| 4 | מחיר למ״ר ברובע שדה דב | text | 81,000 | 83,000, 52,856 | NC2604 TA | CONFLICT |
| 5 | מחיר למ״ר ברובע שדה דב | text | 70,000, 100,000 | 60,200, 138,000 | NC2604 | CONFLICT |
| 6 | מחיר למ״ר ברובע שדה דב | text | 64,700, 81,600 | 64,700, 81,600 | BZ2606 | CONSISTENT+DATE |
| 7 | מחיר למ״ר ברובע שדה דב | text | 64,000, 75,000 | 73,200, 82,500 | BZ2606 | UNSOURCED |
| 8 | מחיר למ״ר ברובע שדה דב | cell | (text) | (text) | NC2604 | CONFLICT |
| 9 | מחיר למ״ר ברובע שדה דב | cell | 81,000 | 83,000 | NC2604 ICE1904 | CONFLICT |
| 10 | מחיר למ״ר ברובע שדה דב | cell | (text) | (text) | ICE2105 ICE0606 BZ2606 | CONFLICT |
| 11 | מחיר למ״ר ברובע שדה דב | cell | 70,000, 100,000 | 70,000, 75,000-85,000 | ICE2105 ICE0606 BZ2606 | CONFLICT (x2) |
| 12 | מחיר למ״ר ברובע שדה דב | cell | (text) | 38-43 | BZ2512 | CONFLICT |
| 13 | מחיר למ״ר ברובע שדה דב | cell | 100,000 | 107,700-119,200 | BZ2512 | CONFLICT |
| 14 | מחיר למ״ר ברובע שדה דב | cell | (text) | (text) | ICE2512 | CONFLICT |
| 15 | מחיר למ״ר ברובע שדה דב | cell | 90,000 | 90,000-100,000 | ICE2512 | CONFLICT |
| 16 | מחיר למ״ר ברובע שדה דב | cell | (text) | (text) | ICE0305 | UNSOURCED |
| 17 | מחיר למ״ר ברובע שדה דב | cell | 53,500 | 54,000-57,000 | ICE0305 | UNSOURCED (x2) |
| 18 | מחיר למ״ר ברובע שדה דב | cell | (text) | (text) | BZ2606 | UNSOURCED |
| 19 | מחיר למ״ר ברובע שדה דב | cell | 64,000, 75,000 | 73,200 | BZ2606 | UNSOURCED |
| 20 | מחיר למ״ר ברובע שדה דב | cell | (text) | (text) | BZ2606 | UNSOURCED |
| 21 | מחיר למ״ר ברובע שדה דב | cell | (text) | (text) | NC2604 | UNSOURCED (x2) |
| 22 | מחיר למ״ר ברובע שדה דב | cell | 7, 75,000 | 9.45 | NC2604 | UNSOURCED |
| 23 | מה מסביר את פערי המחירים בתוך הרובע | text | 3.81 | 2.8, 3.7 | ICE2105 ICE0305 | UNSOURCED |
| 24 | מה מסביר את פערי המחירים בתוך הרובע | text | 11.61 | 7.2, 7.7, 11.95 | ICE0305 ICE2510 | UNSOURCED |
| 25 | מחירים לפי גודל דירה | text | 46.8, 3.81, 81,410, 3 | 9.45 | NC2604 ICE0305 ICE2105 ICE2510 | UNSOURCED |
| 26 | מחירים לפי גודל דירה | whole table | 46.8, 3.81, 81,410, 6.86, 9.45, 11.61 | 2.8-3.1, 54, 9, 3.665, 67,900, 82-83, 4.6-4.8, 9.45, 104-126, 10-13, 6.49-7.73, 61,300-62,800, 132, 7.16-7.57, 54,200-57,300, 139.7, 18, 11.954, 85,600 | NC2604 ICE0305 ICE2105 ICE2510 | UNSOURCED |
| 27 | מחירים לפי גודל דירה | text | 11.61 | 7.2, 12 | ICE0305 ICE2510 | UNSOURCED |
| 28 | מחירים לפי גודל דירה | text | 2.3, 32 | 2.8, 3.1, 2.4, 2.7 | ICE2105 | CONFLICT |
| 29 | מחירים לפי גודל דירה | text | 43.75, 508 | 390, 200, 38, 42 | BZ2512 NC2604F ICE1904 | CONFLICT |
| 30 | מחירים לפי מתחם | text | 11,000 | 1,280 | NC2604 | UNSOURCED |
| 31 | מחירים לפי מתחם | text | 43.75, 508, 2.3, 32 | 63,400, 82,600 | ICE1904 NC2604 ICE2105 GL2609 | CONFLICT |
| 32 | מחירים לפי מתחם | text | 94, 8, 853, 8.4 | 94, 8, 853, 8.4, 75,500 | NC2507 BZ2512 NC2604 ICE1904 | CONSISTENT+DATE |
| 33 | מחירים לפי מתחם | cell | 43.75, 508, 2.3, 32 | 63,400, 82,600, 60,000-62,000 | NC2604 ICE2105 | CONFLICT |
| 34 | פרמיית קו ראשון לים ונוף | text | 90,000, 100,000 | 90,000-100,000, 38-43, 107,700, 119,200 | ICE2512 BZ2512 | CONFLICT |
| 35 | פרמיית קו ראשון לים ונוף | cell | (text) | (text) | ICE2512 | CONFLICT |
| 36 | פרמיית קו ראשון לים ונוף | cell | 90,000 | 90,000-100,000 | ICE2512 | CONFLICT |
| 37 | פרמיית קו ראשון לים ונוף | cell | (text) | 38-43 | BZ2512 | CONFLICT |
| 38 | פרמיית קו ראשון לים ונוף | cell | 100,000 | 107,700-119,200 | BZ2512 | CONFLICT |
| 39 | פרמיית קו ראשון לים ונוף | cell | (text) | (text) | BZ2512 NC2604 | CONFLICT |
| 40 | פרמיית קו ראשון לים ונוף | cell | (text) | (text) | ICE0305 | UNSOURCED |
| 41 | פרמיית קו ראשון לים ונוף | text | 81,000 | 83,000 | NC2604 | CONFLICT |
| 42 | עסקאות שיא ועסקאות שפל | text | 2.3, 32, 43.75, 508 | 2.8, 3.1, 32, 4, 390, 200, 38, 42 | ICE2105 GL2311 BZ2512 NC2604F | CONFLICT |
| 43 | עסקאות שיא ועסקאות שפל | text | 508, 43.75 | 390, 42 | BZ2512 | CONFLICT |
| 44 | עסקאות שיא ועסקאות שפל | cell | (text) | 4 | GL2311 | CONFLICT |
| 45 | עסקאות שיא ועסקאות שפל | cell | 2.3 | 3.1 | GL2311 | CONFLICT |
| 46 | עסקאות שיא ועסקאות שפל | cell | (text) | (text) | GL2311 | CONFLICT |
| 47 | עסקאות שיא ועסקאות שפל | cell | (text) | (text) | ICE2105 | UNSOURCED |
| 48 | עסקאות שיא ועסקאות שפל | cell | 3.81 | 2.8-3.1 | ICE2105 | UNSOURCED |
| 49 | עסקאות שיא ועסקאות שפל | cell | 46.8 | (text) | ICE2105 | UNSOURCED |
| 50 | עסקאות שיא ועסקאות שפל | cell | (text) | (text) | ICE2105 | UNSOURCED |
| 51 | עסקאות שיא ועסקאות שפל | cell | 7 | 9.45 | NC2604 | UNSOURCED |
| 52 | עסקאות שיא ועסקאות שפל | cell | 75,000 | (text) | NC2604 | UNSOURCED |
| 53 | עסקאות שיא ועסקאות שפל | cell | (text) | 38 | BZ2512 NC2604F | CONFLICT |
| 54 | עסקאות שיא ועסקאות שפל | cell | 43.75 | 42 | BZ2512 | CONFLICT |
| 55 | עסקאות שיא ועסקאות שפל | cell | 508 | 390, 200 | BZ2512 | CONFLICT |
| 56 | השוואת מחירים מול שכונות יוקרה בתל אביב | text | 55,000, 60,000, 70,000, 90,000, 120,000, 81,000, 100,000 | 52,856, 55,000, 51,000, 53,000, 83,000, 70,000 | TA ICE0606 BZ2608 NC2604 ICE2105 | CONFLICT |
| 57 | השוואת מחירים מול שכונות יוקרה בתל אביב | cell | 81,000, 70,000, 100,000 | 83,000, 70,000 | NC2604 ICE2105 ICE0606 | CONFLICT |
| 58 | השוואת מחירים מול שכונות יוקרה בתל אביב | cell | (text) | (text) | TA | CONFLICT |
| 59 | השוואת מחירים מול שכונות יוקרה בתל אביב | cell | 55,000, 60,000 | 52,856 | TA | CONFLICT |
| 60 | השוואת מחירים מול שכונות יוקרה בתל אביב | cell | 55,000, 70,000 | 55,000, 51,000-53,000 | ICE0606 BZ2608 | CONFLICT |
| 61 | השוואת מחירים מול שכונות יוקרה בתל אביב | cell | 90,000, 120,000 | (text) | - | UNSOURCED |
| 62 | השוואת מחירים מול שכונות יוקרה בתל אביב | cell | (text) | (text) | - | UNSOURCED |
| 63 | דינמיקת פריסייל מול אכלוס | text | 70,000, 100,000 | 70,000, 75,000-85,000 | ICE2105 ICE0606 BZ2606 | CONFLICT |
| 64 | דינמיקת פריסייל מול אכלוס | text | 64,700, 81,600 | 64,700, 81,600 | BZ2606 | CONSISTENT+DATE |
| 65 | מימון, לוח תשלומים וליווי בנקאי | text | 7 | 9.45 | NC2604 | UNSOURCED |
| 66 | מימון, לוח תשלומים וליווי בנקאי | cell | 7 | 9.45 | NC2604 | UNSOURCED |
| 67 | הזווית המשפטית והמיסויית | text | 7, 9.45, 11.61 | 6.5, 12 | ICE0305 ICE2510 NC2604 | UNSOURCED |
| 68 | תחזית והערכת שווי עתידי | text | 11,000 | 1,280 | NC2604 | UNSOURCED |
| 69 | תחזית והערכת שווי עתידי | text | 150,000, 81,000 | 150,000, 83,000 | NC2503 NC2604 | CONFLICT |
| 70 | תחזית והערכת שווי עתידי | text | 9.45, 11.61 | 6.5, 12 | ICE0305 ICE2510 NC2604 | UNSOURCED |
| 71 | איך לקרוא הצעת מחיר בשדה דב | text | 94, 8 | 94, 8 | NC2507 BZ2512 | CONSISTENT+DATE |
| 72 | איך לקרוא הצעת מחיר בשדה דב | cell | 81,000 | 70,000 | ICE2105 ICE0606 NC2604 | CONFLICT |
| 73 | משמעות המחירים למשקיעים | text | 32, 2.3, 3.81 | 2.8, 3.7 | ICE2105 ICE0305 | UNSOURCED |
| 74 | כמה עולה דירה בשדה דב? | text | 7, 75,000, 3.81, 6.86, 9.45, 11.61 | 9.45, 83,000, 2.8, 3.7, 82-83, 4.6, 4.8, 126-132, 7.2, 7.7 | NC2604 ICE2105 ICE0305 | UNSOURCED |
| 75 | מה המחיר למ״ר בשדה דב? | text | 81,000, 70,000, 100,000, 90,000 | 83,000, 70,000, 54,000-57,000, 90,000-100,000, 38-43, 107,700, 119,200 | NC2604 ICE2105 ICE0606 ICE0305 ICE2512 BZ2512 | CONFLICT |
| 76 | האם שדה דב יקרה יותר מרמת אביב? | text | 55,000, 70,000, 81,000 | 55,000, 83,000, 70,000 | ICE0606 NC2604 ICE2105 | CONFLICT |
| 77 | האם המחירים יכולים להגיע ל-150,000 ש״ח למ״ר? | text | 150,000 | 150,000 | NC2503 | CONSISTENT+DATE |
| 78 | משקיעים זרים ומילות חיפוש בינלאומיות | text | (text) | (text) | - | DATE |

## 5. Notes for whoever applies it

- Re-fetch content.rendered right before applying; check each `old` against it (another session may have edited the page).
- Edit 26 (`spans_tags`): if the rendered table does not match the raw post content byte for byte (newlines between tags),
  replace the whole `<table>` element that contains `<th>סוג דירה</th>` with `new`.
- After applying: the page's numbers match the PriceGuide data (83,000 average, about 70,000 in 2026, 52,856 Tel Aviv,
  9.45M for 4 rooms). If the PriceGuide shortcode goes on the page in the same release, both say the same thing.
- Left without a number, on purpose: Park Tzameret (no dated source found; the table cell now says "תלוי במגדל ובקומה"),
  the Central and North compound rows ("אין נתון ממוצע נפרד אחיד למתחם בלבד", true, no number).
- Qualitative claims with no number were not in scope and stay, for example "ומתקרב בחלק מהמוצרים לטווחי יוקרה של
  פארק צמרת" and the line "מקורות לעיון: ..." (a list of source names at the bottom, against the research law; the
  owner's call).
