# Design studio pages: edit report (11.11.2026)

Inputs: the three drafts in `docs/research/2026-11-10-apartment-designer/pages/*/content.html` (untouched), `market/listing/listing-copy.md`, `docs/design-lab/apartment-designer/tools/NOTES.md`.
Outputs: `hub/body.html`, `designer-cost/body.html`, `designers/body.html`. Nothing published.

## Hub, /design-studio/ (about 60 sentences rewritten or deleted for honesty)
- Answer, CTA area, engine note: "draw walls or open an existing plan", "open the flat from the project page", "plans labelled by source (sale plan / drawn from published data)" replaced by the truth: example flats of 3, 4, 5 rooms chosen with buttons, labelled "דירה לדוגמה". Engine written as `[nadlan_designer plans="example-3r,example-4r,example-5r"]` inside `#studio`.
- `#online-design`: plan and 3D "same model, always in sync, phone plan first"; fixed walls now include the shaft; partition rules generalised to "within rules" plus draw / remove / restore (the draft's specific rules about windows and minimum room size are not on the ship list); drawing legend (solid line, dashed safe room, coloured partitions) deleted; added rename rooms, undo/redo, autosave in the browser with no account, start over.
- `#free-3d`: "3D loads after the plan" replaced by "on a phone the plan first, 3D on demand"; Hebrew and English added; free list now matches the ship list.
- `#plan-render`: deleted "open the flat straight from the project page" and "draw walls by your plan"; rewritten to "pick the example flat closest to yours".
- `#by-measurements`: fit-check placeholder and its paragraph removed; text points to `#studio`; "every wall knows its length" removed.
- `#free-software`: software-compare placeholder removed (no other sentence described that tool); table row for our designer now says it works on example flats.
- `#ai-quick`, `#ai-free`, `#ai-designer`: removed every claim of AI on our page ("style applied to the room you built", "AI proposes changes you accept", design-ai-looks tool, "share with designer"). Now: what such tools generally do, the limit (a picture, not measurements), and what this page gives instead (designer by real measurements, style questionnaire). No AI product named.
- `#pro-designer`: added dsgwho (h=4); link text "מעצבי פנים מומלצים" changed to a neutral description of the list.
- `#online-designer`, `#online-consult`: "the designer joins on the same plan / the decision log shows the designer what was chosen / send her the worked plan" replaced by "prepare on an example flat and share your screen in any video meeting". dsgfee preset r4 at the end of `#online-designer`.
- `#budget` and its h3s: "the designer knows rooms, wall area, kitchen length and builds the budget without retyping" deleted; "the calculator works from your plan" deleted (dsgfurnish works by rooms and level); "the designer computes each room's area and the calculator multiplies" replaced by "area is shown next to each room; type it in the calculator"; "the designer knows wall area minus windows" deleted. True statement added: price range beside each piece and floor, budget sheet. Tools: dsgbudget, dsgfurnish, dsgkitchen, dsgfloor, dsgpaint, dsgcurtain (end).
- `#living-layout`: layout placeholder removed; "compare several layouts" replaced by drag, rotate, 3D, eye-height walk, undo. Sofa, rug, clearance texts rewritten to what dsgsofa, dsgrug, dsgdining do; "try both rug sizes in 3D" replaced by a tape-on-the-floor tip (rugs in the catalogue are not confirmed).
- `#lighting`: "the tool proposes points per room on your plan / prepares a plan to send to the electrician" replaced by dsglight (lumens, fittings, Kelvin) plus the designer's electrical points layer (see, add, move, remove, restore). dsgpoints at the end. "Filter the list by lighting specialty" removed (the list filters by region only).
- `#kitchen-plan`: "the designer shows kitchen walls and their lengths" removed; specialty filter claim removed.
- `#styles`: style quiz rewritten to dsgstyle (5 questions, 7 styles, palette, furniture list); "apply it straight to the flat" and "the board is saved with the design" removed; mood-board step 5 rewritten.
- `#room-online`: room-presets placeholder and "ready rooms by type and size" paragraph removed; replaced by a true paragraph (focus on one room of the example flat, rename, floor, furniture, price ranges). dsgbed under `#small-bedroom`, dsgtime under `#new-from-developer`.
- New-flat table: last column renamed to "what you can try in the designer, on an example flat" and each cell made true (two cells say plainly the designer does not do it).
- `#small-apartments`: "ready small flats by size" removed; "send the carpenter a real plan from the designer" removed; modular "place it open and closed in the plan" changed to "measure it in both states".
- FAQ: room software, AI room, AI render, kitchen software answers rewritten (no AI on the page, no cabinet planner).

## Cost page, /design-studio/designer-cost/ (about 23 sentences rewritten)
- Calculator: the draft's five questions (service, size, project type, experience, region) and "takes rooms and area from your plan" are not what dsgfee does; rewritten to "five pricing methods side by side".
- Contractor preset paragraph (asks rooms and scope, returns fee) replaced by dsgtime (timeline); "open the drawn plan of your flat in the designer" replaced by example-flat wording.
- Quote reader paragraph (sample quote section by section, no prices) replaced by dsgquote (checks a quote against published ranges, lists usual deliverables).
- Quote-compare placeholder and its sentence removed; the checklist stays with a plain lead.
- Package-compare paragraph ("mark what is in each package") replaced by dsgwho; the sourced package prices stay unchanged.
- dsgfurnish added at the end of `#apartment-designer-cost`, dsgbudget at the end of `#price-factors`.
- Links to the hub now point to `/design-studio/#studio`; "bring a plan with furniture" sentences reworded to example flats and screen sharing.

## Designers page, /profession/מעצב-פנים/ (about 55 sentences rewritten or deleted)
- h1 is now `מעצבת פנים`. Answer rewritten: neutral list from the businesses' own public websites, filterable by region, not partners, no ranking.
- Deleted every consent, partnership or self-marking claim: "ביקשו להופיע", "אישרו את הפרטים", "כל אחד כותב את הטקסט שלו", "סימנו את העיר / את סוג העבודה / מגזר", "in each card the pricing model as she gave it", "studio or solo is written on the card", the chooser that filters the list, the "also online" filter, every `designers-count` marker.
- Old `designers-list` block and old `list-rules` div replaced by the section 1 text of listing-copy.md (`p.list-rules`) and `[nadlan_designers]` on its own line. The section 2 line is not repeated.
- Region h3s: three true sentences each (filter by region, sourced or practical note, "מומלצת" means recommended by people you spoke with, not by this site). Netanya-under-Sharon claim removed. Ramat Gan duplicated sentence fixed.
- "יש לך כבר מעצב" kept only as: prepare the flat in the designer and show it in any video meeting (invite feature from listing-copy section 4 does not exist and was not used).
- `join-designers`: rewritten to update/removal by email (mailto as specified), removal without questions within 2 business days, and the professional join link `/firgun/?join=1`. designer-join placeholder removed.
- Tools: dsgwho (first), dsgtime under `#contractor-apartment`, dsgstyle under `#portfolio`, dsgfee preset new under `#budget-quote`, dsgquote under `#before-closing`.
- Footer: "only professionals who asked to appear" replaced by the neutral-list statement.

## Tool heading levels
Rule followed (h=3 under an h2, h=4 under an h3) except where the brief fixed h="3" for a tool placed at the END of a section that already contains h3s: hub dsgfee (end of `#online-designer`), dsgcurtain (end of `#budget`), dsgpoints (end of `#lighting`); cost dsgbudget (end of `#price-factors`). Kept as instructed.

## Sections that could not be made true
None removed. Every heading kept with text rewritten.

## Internal links (GET https://nad-lan.co.il<path>, browser UA, one request each, 11.11.2026)
All 200: /apartment-prices/, /architect-building-permit/, /guides/new-apartment-balcony/, /guides/new-apartment-buyer-changes/, /guides/new-apartment-mamad/, /guides/new-apartment-sale-specification/, /home-inspection/, /interior-design-trends-2026-israel/, /projects/, /renovation-contractor/, /firgun/?join=1. Not checked by design (exist after publishing): /design-studio/, /design-studio/designer-cost/, /profession/מעצב-פנים/ and their anchors. Dead links removed: none.

## Self-check output (scratchpad selfcheck.py)
```
hub            tools=dsgwho,dsgfee,dsgbudget,dsgfurnish,dsgkitchen,dsgfloor,dsgpaint,dsgcurtain,dsgsofa,dsgrug,dsgdining,dsglight,dsgpoints,dsgstyle,dsgbed,dsgtime
               headings=61 words: draft=6658 body=7118  OK
designer-cost  tools=dsgfee,dsgfurnish,dsgbudget,dsgtime,dsgquote,dsgwho
               headings=44 words: draft=4593 body=4653  OK
designers      tools=dsgwho,dsgtime,dsgstyle,dsgfee,dsgquote
               headings=52 words: draft=5018 body=5168  OK
ALL OK
```
Checks: no `design-` id, only the 17 real ids, no id twice per page, one `<h1`, no `<!--`, no em or en dash, no style or script, designer engine once on the hub only, `[nadlan_designers]` once, h1/h2/h3 texts and ids equal to the draft (designers h1 excepted), banned words absent. Word counts exclude shortcodes and tags.

## Open points
- The heading "ריהוט מודולרי וחכם" keeps the word מודולרי (furniture term, heading frozen).
- The mailto subject has unencoded spaces, as specified; most clients accept it.
- A rug, TV unit or wardrobe in the furniture catalogue was not confirmed, so no sentence relies on them. Two hub sentences (kitchen-plan intro, kitchen FAQ) assume the example flats show a kitchen space in plan and 3D; check on the live designer.
