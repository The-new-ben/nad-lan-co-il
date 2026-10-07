# National PriceGuide: hook proposal for pg_helper.py (HAD-460, 7.10.2026)

Proposal only. `pg_helper.py` is NOT edited. The code below was run in memory against the real `pg_helper.helper()`
(both with `CITIES = ()` and with a city in `CITIES`): it builds the PHP, adds the case `apartment-prices|he`
(nowdoc label `NLPG_APARTMENT_PRICES_HE`), and `php -l` on the output reports no syntax errors.

## 1. The key (next to `KEYS` / `CITIES`)

```python
NATIONAL = "apartment-prices"  # the Israel page gets the national variant (national.py); "" turns it off
```

It is a separate key on purpose. `apartment-prices` must never sit in `CITIES` too: that would give the Israel page a
single-city calculator, which the CEO ruled out on 7.10.2026. The guard below stops the build if it happens.

## 2. `payloads()`: add this block before `return out`

```python
    if NATIONAL:
        import glob
        import national as NT
        if NATIONAL in CITIES:
            raise SystemExit("pg_helper: the national page is in CITIES too (it must not get a city calculator)")
        dn = json.load(io.open(os.path.join(HERE, "cities", NATIONAL + ".json"), encoding="utf-8"))
        cs = [json.load(io.open(f, encoding="utf-8")) for f in sorted(glob.glob(os.path.join(HERE, "cities", "*.json")))]
        cs = [c for c in cs if c.get("slug") != NATIONAL and c.get("page")]
        out[(NATIONAL, "he")] = NT.html(dn, cs, "{{WA}}")
```

Every city file with a `page` goes in the table, whatever the wave of the city calculators. All 23 city pages answered
HTTP 200 with no redirect on 7.10.2026. `NT.html(dn)` with no city list falls back to `dn["cities"]`, the summary inside
apartment-prices.json, which matched the 23 city files value for value on 7.10.2026.

## 3. `assets()`: add this block before `return css, js`

```python
    if NATIONAL:
        import national as NT
        css += "\n" + NT.CSS_N.strip()
        js += "\n" + NT.JS_N.strip()
```

`CSS_N` already went through `render.scope()` inside national.py (the same as `rooms.CSS_R`), and scoping twice changes
nothing (checked). Every rule starts with `.nlpg`. Rules that change base classes start with `.nlpg--national`, so the
project and city sections are unaffected. `JS_N` acts only on `.nlpg--national`. The base script returns early on it
because there is no `.nlpg__calc`, and the rooms script only reads `.nlpg--rooms`.

## 4. No PHP change

- The door already exists: `[nadlan_price_guide key="apartment-prices"]` (`sanitize_key` keeps the hyphen).
- WhatsApp: the button is `<a class="nlds-btn nlds-btn--primary nlpg__wa" ...>` with `{{WA}}` in the href and the
  message already in it. `nadlan_pg_wrap()` swaps the number. With no number, its regex removes the button: 1 anchor
  before, 0 anchors and 0 `{{WA}}` after (checked). The variant has no `data-cfg`, so the `&quot;wa&quot;` swap does
  nothing here.

## 5. Placement and title

- Put it on /apartment-prices/ with the shortcode, after the page's first real paragraph (as on the city pages).
- The H2 is "מחירון דירות לפי עיר: חציון לפי חדרים". On 7.10.2026 the live H1 was "מחירון הדירות של ישראל" and the
  live H2s were: תל אביב והשכונות המבוקשות, גוש דן והמרכז, השרון, ירושלים ומודיעין, יישובי הבתים הפרטיים, חיפה והצפון,
  השפלה והדרום, נדל"ן מסחרי: משרדים, חנויות ולוגיסטיקה, הכלים שממשיכים מכאן. The first 4 words match none of them.
  The first word "מחירון" is also the H1's first word. The phrase is not repeated.

## 6. Data rules the variant keeps

- Only stored values are shown, each with its quarter. A city cell from an older quarter (Kfar Saba 3 and 4 rooms
  10-12.2025, Modiin and Netanya 3 rooms 10-12.2025, Beer Sheva 5 rooms 7-9.2025) shows that quarter under the price.
- A missing change (Rehovot 3 rooms: no median a year earlier) shows the dot "·".
- One derived value: the "כל הארץ" comparison row uses the Israel medians of the cities' quarter (1-3.2026), and its
  change is computed by the files' own method from two stored medians (1-3.2026 against 1-3.2025): 3 rooms +4%,
  4 rooms -4.9%, 5 rooms 0% (-0.04%). The tiles above show the newest Israel quarter (4-6.2026) with the stored changes.

Preview and evidence: docs/qa/had-460/national/ (screenshots and measure.json).
