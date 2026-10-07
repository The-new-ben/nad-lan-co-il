# Patch: the "פרויקט חדש בתכנית ל" row in three live price lists (HAD-460, 7.10.2026)

Description only. The three files were NOT edited. The data is live (PriceGuide on the three project pages), so the fix
needs a release through the usual queue after it is applied.

Files: `scripts/project-stage/price_guide/rainbow-tel-aviv.json`, `dimri-yama-sde-dov.json`, `ashira-sde-dov.json`.

## What is wrong

All three files show a row "פרויקט חדש בתכנית ל" with 70,000-72,000 ₪/m² and the sub line "בקומות הנמוכות:
52,000-57,000". The source, ice 21.5.2026 (https://www.ice.co.il/realestate/news/article/1112481, re-read 7.10.2026 09:46
UTC), says two different things about two different projects:

- In Program L ("שכונה ל'", east of the quarter), a new project: low floors 52-57K/m²; 3 rooms of about 60 m² about 3.1M;
  4 rooms of 101 m² about 5.8M.
- In "הגוש הגדול" (a project with a two-floor 330 m² penthouse sold for 34.6M), a price cut announced from 75K to 59K, then
  most recent sales at 70-72K. That project is outside Sde Dov and outside Program L.

So 70-72K does not belong to Program L, and the calculator mode "פרויקט אחר ברובע" (60,000-72,000) takes its 72,000 upper
bound from it, with "ובתכנית ל" in its why line.

## The fix (identical in the three files)

1. The row keeps its place, its kind (deal), date (5.2026) and src (ICE2105); it gets the Program L figures only.
2. The mode keeps lo 60,000; hi becomes 71,000 (most Sde Dov projects about 70K in 5.2026, ICE2105; a new apartment in a
   new project 70-71K in 6.2026, ICE0606); "ובתכנית ל" leaves the why line; the source list gains ICE0606.
3. The ICE2105 source text is corrected and an ICE0606 source is added.

Dry run (scratch copies, not the repo files): all three patched files load, every src resolves, `render.html()` works
(rainbow 18,421 bytes, dimri 15,294, ashira 15,252) and `default_result()` is unchanged (the mode is not the first one).

### 1. The row (each file once)

Before (rainbow-tel-aviv.json lines 255-261, dimri-yama-sde-dov.json 193-199, ashira-sde-dov.json 183-189):

```json
    {
     "what": "פרויקט חדש בתכנית ל",
     "sub": "בקומות הנמוכות: 52,000-57,000 ₪ למ״ר",
     "m2": "70,000-72,000",
     "price": "",
     "kind": "deal",
     "date": "5.2026",
     "src": "ICE2105"
    }
```

After:

```json
    {
     "what": "פרויקט חדש בתכנית ל, ממזרח לרובע",
     "sub": "בקומות הנמוכות. 4 חדרים, 101 מ״ר: כ-5.8 מיליון ₪",
     "m2": "52,000-57,000",
     "price": "",
     "kind": "deal",
     "date": "5.2026",
     "src": "ICE2105"
    }
```

### 2. The calculator mode "פרויקט אחר ברובע" (each file once)

Before (rainbow lines 308-313, dimri 244-249, ashira 234-239):

```json
   {
    "id": "area",
    "label": "פרויקט אחר ברובע",
    "lo": 60000,
    "hi": 72000,
    "why": "רוב העסקאות של 2026 בפרויקטים אחרים ברובע שדה דב ובתכנית ל.",
    "src": "ICE2105 ICE0305"
   }
```

After:

```json
   {
    "id": "area",
    "label": "פרויקט אחר ברובע",
    "lo": 60000,
    "hi": 71000,
    "why": "ב-2026 רוב הפרויקטים ברובע מוכרים בכ-70,000-71,000 ₪ למ״ר, ובחלקם העסקאות האחרונות היו 60,000-63,000 ₪.",
    "src": "ICE2105 ICE0606 ICE0305"
   }
```

60,000-63,000 = a project in Eshkol, recent deals 60-62K (ICE2105, 5.2026) and four recent deals at 61,325-62,769
(ICE0305, ice 3.5.2026). 70,000-71,000 = ICE2105 (about 70K) and ICE0606 (70-71K).

### 3. The sources block

rainbow-tel-aviv.json, before (line 15):

```json
  "ICE2105": "https://www.ice.co.il/realestate/news/article/1112481 (ice 21.5.2026): most Sde Dov projects around 70K ILS/m2; a project east of Rainbow 60-62K; in Program L a new project's low floors 52-57K and most recent sales 70-72K",
```

dimri-yama-sde-dov.json (line 9) and ashira-sde-dov.json (line 9), before:

```json
  "ICE2105": "https://www.ice.co.il/realestate/news/article/1112481 (ice 21.5.2026): most Sde Dov projects around 70K ILS/m2, some sell at 60K; a new project in Program L: low floors 52-57K, most recent sales 70-72K",
```

After, in all three (the ICE2105 line replaced, and one new line after it):

```json
  "ICE2105": "https://www.ice.co.il/realestate/news/article/1112481 (ice 21.5.2026, re-read 7.10.2026 09:46 UTC): most Sde Dov projects around 70K ILS/m2, some sell at 60K; a project in Eshkol east of Rainbow ('זוהי תל אביב'): recent deals 60-62K; Program L (east of the quarter), a new project: low floors 52-57K, 4 rooms 101 m2 about 5.8M. The article's 'most recent sales 70-72K' belong to a project in 'הגוש הגדול' (not Sde Dov, not Program L) and are not used (correction 7.10.2026, HAD-460)",
  "ICE0606": "https://www.ice.co.il/realestate/news/article/1114418 (ice 6.6.2026, read 7.10.2026 about 09:50 UTC): in Sde Dov a new apartment in a new project is around 70-71K ILS/m2",
```

## Not changed, checked

- The tile and row "כ-70,000 ... ברוב הפרויקטים ברובע" (ICE2105) in the three files are correct and stay.
- The "תכנית ל, השכונה הסמוכה" median rows (GOVL) are official data and stay.
- The same misreading sits in two research notes, for the record: docs/research/2026-10-07-project-prices/README.md (the
  Rainbow table row "70,000-72,000; 52,000-57,000 (5.2026)" and the mode note "Program L recent 70-72K") and
  docs/research/2026-10-07-project-prices-2/README.md (the Dimri table row). Worth a one-line correction each when the
  JSON fix lands.
- scripts/project-stage/price_guide/sde-dov-prices.json already uses the corrected row ("פרויקט חדש בתכנית ל, ממזרח
  לרובע", 52,000-57,000) and has no 70-72K figure.

## Applying it

The three blocks are exact text from the files as of 7.10.2026 (working tree of claude/apartment-experience-b1). Each
"before" block occurs once per file. Apply as text replacements (keep the files' one-space indent and LF endings), then
run the usual check: `json.load`, every src in sources, `render.html(d)`, and a live spot-check of the three pages after
the release.
