# Ashira meeting prep (HAD-543), evidence of 15.10.2026

Nothing on the live site was changed. All checks are read-only.

## Five language pages (code check, raw HTML, 15.10.2026 ~22:20 Israel)
| page | status | lang | h1 | words | Google index (URL Inspection API) |
|---|---|---|---|---|---|
| /projects/ashira-sde-dov/ | 200 | he-IL | 1 | 4,857 | Submitted and indexed, crawled 1.10 |
| -en | 200 | en-US | 1 | 10,097 | indexed, crawled 14.9 |
| -fr | 200 | fr-FR | 1 | 10,212 | indexed, crawled 15.10 |
| -ru | 200 | ru-RU | 1 | 7,669 | indexed, crawled 14.10 |
| -ar | 200 | ar | 1 | 6,390 | indexed, crawled 15.8 |

## Language review
Gemini 3.8 Flash (High) via the Antigravity CLI (`agy`), prompt in `language-qa-prompt.txt`, full report in
`language-qa-gemini-3.8.md`. Grades: HE 8, EN 8.5, FR 8.5, RU 7.5, AR 7.5. Each finding was re-checked against the page text:
- CONFIRMED: facts card says "two 9-floor buildings" (line 32 in every language) while the article says 8 (needs the
  source checked: the 5.2023 design plan vs the approved composition).
- CONFIRMED: EN/FR/RU/AR neighbour table lists ASHIRA itself at "11 m".
- CONFIRMED: only the Hebrew page has the sales figures (125 of 406 sold by 7.2026, ~72,000 per m2 in Q2 2026) and the
  19.5M penthouse deal (8.2024); EN/FR/RU/AR say no price data and quote the old 25M asking price.
- CONFIRMED: rooms 2-5 (HE) vs 2-6 and penthouses (EN/FR/RU/AR).
- CONFIRMED: "collagen tanning" calque in all four foreign versions; RU/AR "small tower" calque for מגדלון.
- CONFIRMED: French area-map labels have no accents ("Prix a proximite", "Sante", "Cafes"); a shared component, so
  probably every French page.
- CONFIRMED (tone): EN "Walking away is a valid outcome of due diligence." on a sales page.
- CONFIRMED (minor): HE map label "אשכול לוי 29" (street is לוי אשכול).
- REJECTED: "truncated Hebrew sentence" (the full sentence exists); "עב" in the language switcher (native-script label, by design).

## Flagship gap check (code: module markers in raw HTML)
| module | Ashira | Rainbow | DUO | Kikar | Dimri |
|---|---|---|---|---|---|
| project film | no | yes | yes | yes | yes |
| price list table (nlpd) | no | yes | yes | yes | no |
| sold deals by floor | weak | yes | yes | yes | weak |
| 360 rooms tour | 1 marker | 7 | 9 | 1 | 1 |
| FAQPage schema | no | yes | no | yes | yes |
| costs to buy (purchase tax 2026, financing %, lawyer, new immigrants) | no | no | no | yes | no |
| rent section | no | no | no | yes | no |
| occupancy timeline (Form 4) | no | no | no | yes | no |
| walking minutes to places | no | no | no | yes | no |
The in-building journey (choose an apartment -> facilities) still needs a real pressed browser check.

## Search Console, 90 days (14.7-13.10.2026)
Name variants people use: אשירה שדה דב, אשירה שדה דב מחיר, אביסרור שדה דב, אשירה אביסרור (pos 9.2), פרויקט אשירה (10.2),
ashira שדה דב (8.6), אביסרור אשירה, אשירה תל אביב, ashira (11), ashira tel aviv (10), ashira by avisror, מגדלי אביסרור.
All of them land on /projects/ashira-sde-dov/ (+ -en, -ru). 198 impressions, 2 clicks on the Hebrew page.
Non-brand Sde Dov queries: 108 queries, 2,730 impressions, 10 clicks, mostly positions 30-50, split across /, /sde-dov/,
/sde-dov/prices/, /compound/sde-dov/, /sde-dov-luxury-projects-2026/, /sde-dov/merkaz/, /premium/ (internal split).

## Other findings
- Live health 1.72.461: the site's OpenAI connection answers 401 (key rejected), so lead AI scoring cannot work.
- Waiting PRs 495/496/497 target `live-truth` (7.10, 1.72.432); the local truth branch is 29 commits ahead.
