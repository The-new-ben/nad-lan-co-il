# The bill of materials of a rented home in Israel (HAD-795)

Ben, 20.11.2026: break the whole subject of renting, with the whole lifetime of maintenance around it, into a bill of materials, and every part again into its own bill of materials, until each leaf is one thing a landlord can do with one tap.

This folder is the product's spine, not only a document: `tree/*.json` is read by the build (stage 5) to draw the home as an object, the tenancy as a timeline, and the one-tap action list. `build_bom.py` checks every file against the schema and writes `BOM.md` (the readable tree) and `counts.json`.

## Branches (file per branch)

| # | File | Branch |
|---|---|---|
| 01 | tree/01-before.json | Before renting: is it worth it, the price, the home's readiness, insurance |
| 02 | tree/02-tenant.json | Finding and checking a tenant |
| 03 | tree/03-contract.json | The contract and the guarantees |
| 04 | tree/04-handover.json | Handover: protocol, meters, keys |
| 05 | tree/05-running.json | The running tenancy: rent collection, index linkage, bills, the house committee, municipal tax |
| 06 | tree/06-maintenance.json | Maintenance: every system and appliance, routine and breakdown, who pays by law |
| 07 | tree/07-paperwork.json | The year's paperwork: income tax tracks, receipts, the accountant |
| 08 | tree/08-renewal.json | Renewal, option, raise |
| 09 | tree/09-exit.json | Exit: notice, inspection, deposit, repairs, debts |
| 10 | tree/10-longview.json | The owner's long view: wear, renovation, selling with a tenant inside |

## Node record (every node, branch or leaf)

```json
{
  "id": "06.03.02",                 // dotted path, parent = id without the last part
  "kind": "branch | leaf",
  "title": {"he": "...", "en": "..."},
  "what": "one plain sentence",
  "who": ["landlord" | "tenant" | "both" | "professional" | "authority" | "house-committee"],
  "when": "the trigger or the due time, in words (\"before signing\", \"every January\", \"within 30 days of the tenant's demand\")",
  "proof": "the document or record that proves it was done, or null",
  "money": "who pays and on what basis; amounts ONLY when a primary source fixes them (with the source); else null",
  "law": [{"source": "חוק השכירות והשאילה, התשל\"א-1971", "section": "25ח(א)", "quote": "short verbatim words from the primary text", "url": "primary text URL", "read_on": "2026-11-20"}],
  "if_skipped": "what happens if nobody does it (legal or practical), or null if unknown",
  "product_today": {"status": "works | partly | missing", "where": "file/screen in the product, or null"},
  "thumb": {"he": "verb phrase on the button", "en": "...", "taps": 1}   // leaves only
}
```

## Rules

- A leaf is ONE thing a landlord can do with one tap (record, remind, send, sign, photograph, pay, schedule). If a leaf needs two decisions it is a branch.
- `law` only from the primary text (Knesset book of laws, Nevo/Wikisource copy of the statute, gov.il, the Tax Authority's own page), with the date it was read. Secondary sites (Kol Zchut, law firms) may point the way but are never cited as the source.
- Unknown facts are left out (null), never guessed. No invented amounts, no invented deadlines.
- The site is never a broker: no node says the site finds tenants for a fee.
- No long dashes anywhere.

## Language parity (coordinator, 20.11.2026)
`build_bom.py` adds `lang_missing` to every leaf: the language pages that lack it today. A leaf the product does not have is missing in all five; a leaf it has is missing in fr, ru and ar, because the product's string tables exist only in he and en (v2 `assets/rentals/i18n/{he,en}.json`, v1 inline he/en). `counts.json` carries the totals per language.
