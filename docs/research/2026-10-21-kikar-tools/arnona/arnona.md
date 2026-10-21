# Tel Aviv-Yafo residential arnona 2026: official data for the calculator

Research only, 21.10.2026. Nothing on the site or in plugins/ was changed; nothing was committed.
The data file is `arnona-tlv-2026.json` in this folder. Every value in it has a source URL, a clause, a page and the retrieval date.

## Source

- **The order:** "ארנונה כללית לשנת 2026" (the city council approved it on 16.6.2025). It is 37 pages long. The minister's exceptional approval (11/12/2025) is page 37 of the same PDF.
  - URL: https://www.tel-aviv.gov.il/Residents/Arnona/Documents/חוברת צו הארנונה לשנת 2026.pdf
  - Retrieved 2026-10-21 18:00:31 UTC. Saved as `source/tlv-arnona-order-2026.pdf` (sha256 f0e5dd06…3325).
- **Supporting files**, saved in `source/`:
  - the 2026 explanatory notes (rates = 2025 + 1.626%)
  - the separate ministers' approval
  - the 2027 order, approved by the council 22.06.2026 and still subject to the ministers' approval, kept for reference only
  - the city's discount records (JSON)
  - the city GIS zone query for Kikar HaMedina (JSON)
  - the order-listing JSON
- **Nothing blocked access.** There was no login and no CAPTCHA. The links on the city's order page are drawn by JavaScript, so the PDF list was read through the page's own public endpoint (`TlvList.svc/GetTables`). The discount texts were read the same way (`TlvItem.svc/GetItemByViewForEvent`).

## Rates 2026 (ILS per m² per year, order clause 2.3, printed p.8 / PDF p.12)

| Type | Z1 villa or apt >140 | Z1 apt ≤140 | Z2 villa or apt >140 | Z2 apt ≤140 | Z3 all | Z4-5 all |
|---|---|---|---|---|---|---|
| אא | 139.60 | 112.99 | 108.98 | 90.71 | 78.39 | 64.42 |
| כא | 138.97 | 112.49 | 108.49 | 90.29 | 78.06 | 64.13 |
| א+ח | 132.35 | 107.12 | 103.33 | 86.01 | 74.34 | 61.09 |
| ב+ג | 112.16 | 90.78 | 87.56 | 72.89 | 63.01 | 54.05 |
| ד | 97.54 | 78.94 | 76.14 | 63.38 | 54.79 | 49.15 |
| ה+ו | 84.81 | 68.64 | 66.21 | 55.10 | 47.65 | 46.64 |

- **Building type (clause 2.1)** depends on the building description and its completion year. The full 6×9 matrix is in the JSON. Any building with 2 or more apartments completed in 2022 or later is type אא; one completed 2010-2021 is type כא.
- **Apartment in a hotel building:** 132.35.
- **The 140 m² band:**
  - It exists only in zones 1 and 2.
  - The order sets one rate per apartment class ("דירות עד 140 מ"ר" / "דירות מעל 140 מ"ר"; villas always take the higher column). It has **no clause for a marginal, split-by-band computation**.
  - Our reading is that the whole area is charged at one rate. That gives a cliff: 140 m² = ₪15,818.60, 141 m² = ₪19,683.60 (zone 1, אא). No city worked example or real bill confirmed this reading.

## Area (clause 1.3.1, PDF pp.5-6)

- **Counted:** everything inside the unit, including the gallery, any covered area, **balconies**, sheds and pools.
  - A garden balcony is charged in full if it is covered, or has a railing or wall on 3 sides (יא).
  - A pergola is charged in full if it has 2 or more walls (יב).
- **Not counted:**
  - outer and inner walls
  - **parking** (covered or open, used only for parking, in a residential building) (ד)
  - common areas, except pools and game rooms, which are charged at the residential rate (ו; 2.3 notes 1-2)
- **Roof:** a private paved roof counts at up to 30% of the area of the apartment below it (ה).
- **Rounding:** to the nearest whole m²; half a m² rounds down.
- **Storage room:** the order has no residential clause on it (not found).

## Discounts

The discounts are in order section 6 (printed pp.26-32, PDF pp.30-36). The statutory discounts are on the city page https://www.tel-aviv.gov.il/Residents/Arnona/Pages/PrivateDiscounts.aspx.

- **Seniors:**
  - NII old-age or survivors' pension: 12.5% on 100 m²
  - the same plus income support: 100% on 100 m²
  - Senior Citizens Law income test: 30% on 100 m², if income is at most ₪14,058 living alone or ₪21,087 per household
  - aged 75+ and paying the year in January: 2%
- **Disability:**
  - earning incapacity of 75% or more: 80% of the whole area
  - medical disability of 90% or more: 40%
  - disabled child: 33% on 100 m² per child, up to 90% in total
  - blind: 90%
  - IDF disabled: 2/3 on 70 m² (90 m² for 5 or more persons)
- **Single parent:** 10% of the whole area.
- **New immigrant:** 50% on 100 m² for 12 months within the first 24 months; returning residents are excluded.
- **Soldier:** compulsory service and up to 4 months after discharge: 100% on 70 m² (90 m² for 5 or more persons). This one is statutory and appears only on the city page.
- **Low income:** 20-90% of the whole area, by an income table for 1 to 10+ persons (full table in the JSON).
- **Reservists:** 5%; reserve commanders: 25% on 100 m².
- **Empty property:** 100% for up to 6 cumulative months (each empty spell must last 30 or more days).
- **New building, first owner, empty:** 100% for up to 12 months.
- **Student:** there is no separate student discount; the city sends students to the low-income test.
- **Rules:**
  - only one discount, the highest
  - one property only
  - pro rata to the months held
  - the discount is cancelled if the year is not paid in full by 31.12

## Payment (clause 1.4, PDF p.7, and the city payments page)

- **Due date:** 1.1.2026.
- **Instalments:** 6 bi-monthly payments (1 Jan, Mar, May, Jul, Sep, Nov). Each is linked to the CPI from the October 2025 index.
- **Missed payments:** missing 2 instalments lets the city demand the whole year.
- **Paying the whole year by 31 January** only avoids the CPI linkage. **No percentage discount for the general public is published.**

## Kikar HaMedina: zone 1

1. On the order's zone map (PDF p.9, dated 10.07.2025), the ring street "ה' באייר" is inside the zone 1 area.
2. Neither exceptions list (PDF pp.10-11) mentions it.
3. The city GIS layer 589 "אזורי ארנונה למגורים" puts the centre and four points on the ring in zone 1. All 38 blocks around the square are zone 1 (queried 21.10 18:08 UTC).
   - Caveat: the layer is labelled with the 2025 order date.
   - The binding map is the one held at the billing department (clause 1.3.2.ב).

## Method

- I downloaded the order and read it with PyMuPDF.
- Every rate table, type matrix, exceptions list and income table was checked against renders of the PDF pages.
- The discount wording was cross-checked against the city's own discount records, fetched through the city's public JSON endpoints.

## Not found or not covered

- a marginal-band rule
- a storage-room rule
- a student discount
- a general prepayment percentage
- the official consolidated text of the 1993 discount regulations
- the guard levy (היטל שמירה)
- the completion year and class of the Kikar towers
