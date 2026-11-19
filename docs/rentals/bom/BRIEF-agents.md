# Brief for the research helpers (stage 2, HAD-795)

You fill part of the bill of materials of a rented home in Israel for nad-lan.co.il's landlord product. Read `docs/rentals/bom/README.md` in `C:\Users\777\nad-lan\nad-lan-co-il` first: it holds the node schema and the rules. Follow it exactly.

## What to produce
- One JSON file per branch you own, at `docs/rentals/bom/tree/NN-name.json`: a JSON array of node records (branch nodes and leaves, in tree order). Valid JSON (no comments). UTF-8.
- Depth: break every part into its own parts until each leaf is ONE thing a landlord can do with one tap. Expect roughly 25 to 70 leaves per branch, more for maintenance. Do not pad: every leaf must be a real job.
- Hebrew titles in natural Israeli landlord language (how people say it: "שכ\"ד", "ועד בית", "ארנונה", "פרוטוקול מסירה", "צ'קים לביטחון"). English titles plain.

## Law: primary text only, read today
- Fetch and read the primary text yourself. Good sources: he.wikisource.org copies of statutes (e.g. https://he.wikisource.org/wiki/חוק_השכירות_והשאילה), the Knesset (main.knesset.gov.il, fs.knesset.gov.il book-of-laws PDFs), nevo.co.il statute pages when they open, gov.il pages of the Tax Authority, the Ministry of Justice, the Ministry of Finance, the Ministry of Housing, the CBS.
- Kol Zchut (kolzchut.org.il) and law-firm pages may only POINT you to the section; cite the primary text, never them.
- `quote` = a few verbatim words from the section (under 25 words), `read_on` = 2026-11-20.
- If you cannot open a primary text, leave `law` empty and write in `if_skipped` only what you can support. Never guess a section number, an amount or a deadline.

## Product today
For `product_today`, check the existing product code (read-only):
- v2 (live for administrators): `C:\Users\777\nad-lan\nad-lan-co-il\.claude\worktrees\bold-cray-ad2cea\plugins\nadlan-config\inc\rentals\*.php` and `...\assets\rentals\rm-*.js`, string tables `...\assets\rentals\i18n\he.json`, the public guide `...\assets\rentals\guide\he.html`.
- v1 (live for everyone): `C:\Users\777\nad-lan\nad-lan-co-il\plugins\nadlan-config\inc\rentals-manager.php`, `...\assets\rentals\rental-manager.js`.
- "works" only if the code really does it; "partly" with one line on what is missing in `where`; "missing" otherwise.

## Rules you must keep
- No invented numbers or facts. Unknown = null.
- nad-lan is never a broker: no node in which the site finds tenants for a fee or takes a commission.
- No long dashes (the em dash and en dash characters) anywhere; use a comma, a colon or "to".
- Write only your own files. Do not touch any other file in the repo. Do not commit. Do not run any deploy script.
- No accounts, no payments, no captchas on any site.

## When done
Run `python docs/rentals/bom/build_bom.py --check tree/NN-name.json` if it exists (it may not yet; then just validate your JSON with `python -c "import json;json.load(open(...,encoding='utf-8'))"`). Reply with: files written, node count, leaf count, the list of primary sources you actually opened (URL + what section), and anything you could not verify.
