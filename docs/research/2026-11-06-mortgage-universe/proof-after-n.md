# Proof after round N, 6.11.2026: the whole mortgage universe on /mortgage-calculator/

Ben's order (6.11.2026, voice): do not split; the bare word משכנתא / משכנתה is the head keyword; manual Google only; full reverse
engineering of the SERP, of Kol Zchut and of the state sites; tools for registration, the registration fee and form, the
capitalization fee ("היוון משכנתא"), non-payment and freezing, loans against an existing home; state data that AI engines quote;
a map so everything is reachable from everywhere; Claude Design; a recursive loop.

Evidence folders (this directory): `serp-manual.md`, `serp-dna-mashkanta.md` (manual SERP, 80 results for משכנתא, 20 for משכנתה,
20 more queries), `kolzchut-portal-manual.md` + `kolzchut/` (125 pages, 3,258 facts, every quote checked), `gov/` (100 official
facts, 89 verified; the BoI fee files; bank lines), `competitors/` (108 pages, delta, heading DNA), `build/` (four tools, tests,
screenshots), `content/` (page writer, preview, press). Design board v20: https://claude.ai/artifact/VzwKJdV9HgRxRXDaAuLV7M

## What the SERP and the sources have, and where it is on our page now

| # | Component (who has it) | Before | Now | Where |
|---|---|---|---|---|
| N1 | Definition sentence in the AI-quoted shape, both spellings (Wikipedia, Kol Zchut, Bank Jerusalem) | no ("משכנתה" once on the page) | yes | lead + chapter "מה זה משכנתא, ומשכנתא או משכנתה"; DefinedTerm JSON-LD |
| N2 | The law: Land Law ss. 4, 88, 90, 91 (Wikipedia, lawyers) | no | yes | same chapter, quoted |
| N3 | Types of mortgages table (AI overview, Mizrahi, Kol Zchut) | partly | yes | same chapter, each type linked to its tool or guide |
| N4 | Dated national numbers (BoI): 1,156,467 loans, 673.3 bn, 0.61% 90+ days, 10,272 new loans in 8.2026 | no | yes | same chapter |
| N5 | The correct payment cap (the AI overview says one third; BoI says 50%) | partly | yes, in a quotable sentence | same chapter + "ארבע טעויות" |
| N6 | How to take a mortgage, 7 steps (Kol Zchut "שלבי הליך קבלת משכנתא") | no | yes | same chapter, each step linked to a tool |
| N7 | Mortgage registration at the Land Registry (gov.il #7 for משכנתה) | no | yes | chapter "רישום משכנתה בטאבו" + tool `mrishum` |
| N8 | Registration fee 2026 and exemptions (gov.il, Kol Zchut, MoD) | no | yes | chapter "אגרת רישום משכנתא 2026" (table) + `mrishum` exemption checker |
| N9 | The request form (gov.il forms page) | no | yes, linked + checklist | `mrishum` "טופס רישום משכנתא" checklist, links only |
| N10 | ILA commitment to register a mortgage (gov.il guide-mortgage, read by hand) | no | yes | `mrishum` ILA path |
| N11 | Registrar of Pledges for unregistered homes (official notice) | no | yes | registration chapter + `mrishum` |
| N12 | Cancellation after payoff: 30 days, at the bank's cost (law s.9A) | no | yes | chapter "ביטול משכנתא אחרי הסילוק" + `mrishum` + link to jus-tice (ranks #9 for מחיקת משכנתא) |
| N13 | Capitalization fee explained (Kol Zchut, banks, hon calculator) | partly (mexit) | yes | chapter "עמלת היוון" with the BoI averages table in force 19.10.2026 |
| N14 | A whole-mortgage capitalization-fee calculator with partial prepayment and the cheapest month | no one | yes | tool `mhivun` |
| N15 | Non-payment: stages from the first missed payment to the receiver (lawyers, Kol Zchut) | no | yes | chapter "אי תשלום משכנתא" (table) + `mkashe` timeline |
| N16 | Freeze / deferral cost calculator ("מחשבון הקפאת משכנתא") | no one | yes | tool `mkashe` |
| N17 | Wartime programs with dates (BoI outlines, Kol Zchut) | no | yes, labelled ended | chapter + `mkashe` |
| N18 | Borrower rights in law (14) + Kol Zchut rights (16) | partly | yes | chapter "זכויות במשכנתא שכדאי להכיר", every item with its section or link |
| N19 | Loans against an existing home (WeCheck, Menora, Harel, Leumi) | no (child page only) | yes | chapter + tool `mneches`, exact link to the child "משכנתא לכל מטרה" |
| N20 | The BoI any-purpose rate (6.61% vs 4.62%) and the 120,000 ₪ exemption | no one | yes | chapter + `mneches` |
| N21 | Bank directory: BoI average by bank + mortgage site + phone (navigational demand) | partly (rates only) | yes | chapter "הבנקים למשכנתאות" |
| N22 | 2026 law and rules with dates ("חוק משכנתא" 2,400/mo) | no | yes | chapter "מה השתנה במשכנתאות ב־2026" |
| N23 | Payment for every amount, 200 thousand to 5 million (60+ autocomplete phrasings) | 4 amounts | 32 amounts | fold "החזר משכנתא לכל סכום" |
| N24 | A map of every topic, reachable from the top and from every chapter | no | yes | section "כל נושאי המשכנתא, לפי השלב" + CTA + back-links (never floating) |
| N25 | FAQ in the searchers' words | 41 | 54 | FAQ |

Not done, and why:
- A named lawyer as reviewer (competitor proposal 14): Ben's decision.
- Kol Zchut's "פתיחת תיק משכנתא" fee up to 360 ₪: the law indexes it every January; today's amount was not verified.
- The current eligibility-loan rate: gov.il blocked to scripts; only the formula (2026 Economic Plan Law) is stated.
- Swords of Iron 2023 terms, an arrears-interest cap, a reservist mortgage-advice refund: no official source found.
- The housing-company commitment process: not read.
