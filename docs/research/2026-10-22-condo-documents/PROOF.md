# Proof: /real-estate-lawyer/condo-documents/ against the pages that rank (22.10.2026)

The method is the same as for the Greece price list and the contractor register:
- `tools/fact_coverage.py` checks 35 buyer facts (`coverage-facts.json`, written from the official sources and from Google's questions);
- `tools/depth_proof.py` counts the same things on every page.

The competitors are the content pages from the seven SERPs in `serps.json`, plus jus-tice's registration page. Read on 22.10.2026, close to midnight.

## Facts covered (of 35)

| Page | Facts |
|---|---|
| **nad-lan.co.il/real-estate-lawyer/condo-documents/** | **34 at the first run; the missing fact was added the same night** |
| dabullaw.co.il (the strongest, about 4,400 words) | 12 |
| kolzchut (תקנון בית משותף) | 5 |
| jus-tice.co.il/condominium-registration-order/ | 5 |
| ygoldlaw, batim.org.il, home.tabu.co.il | 3 each |
| nadlancenter 2044 (cited by Google's AI answer) | 2 |
| poleg-law | 1 |
| mor.law | 0 |

**Only we state:**
- the 2026 fee (₪39 to order; ₪257 to inspect the paper file);
- how to find the file: by block and parcel, or by the file number on the land extract;
- that the official site has no search by address;
- how the drawing marks attachments: letter and colour, never black;
- the two-parking-space limit;
- the one-year validity of the drawing;
- "approved drawing" versus "other drawing" on the order;
- the 15-day objection period;
- the developer's deadlines: one year, then six months.

## Depth

| | Words | Figures | Tables | Tools | FAQ |
|---|---|---|---|---|---|
| **ours** | 2,178 | 57 | 5 | 2 | 10 |
| dabullaw | **4,395** | 53 | 4 | 0 | (5 in schema) |
| mor.law | **6,503** | 980 | 0 | 0 | 0 |
| home.tabu.co.il | 2,768 | 74 | 6 | an order form | 0 |
| poleg-law | 2,042 | 22 | 0 | 0 | **13** |

## Honesty statement

1. **Words.** dabullaw and mor.law have more words. mor.law's count includes long lists from the rest of its site (980 figures on one page). We did not pad.
2. **FAQ.** poleg-law lists 13 questions against our 10.
3. **Tables.** tabu.co.il counts 6 tables. They are an order form and price lists of a paid reseller, not information.
4. **Not published until checked again:**
   - whether ₪39 is per order or per file (the live system says per order; an undated guide says per file);
   - the cap on developers' registration fees.
5. The sample drawing in the tool is ours and says so. It is not a real building.

## What only this page has

- One tap on a buyer's question lights the answer on a sample condo drawing. The card then says which document, where in it, what to look for, the red flag, and the law section.
- The order path in three steps, with the official links and the 2026 fee.
- A majority calculator: pick an act and the number of flats, and it shows how many owners must agree, with the exact two-thirds rule.
