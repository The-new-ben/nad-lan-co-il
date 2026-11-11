# White space: where no product is good today (HAD-701)

Date: 2026-11-10. **Source:** `features.csv`, `evidence/best-per-parameter.csv`, and the teardown in `products.md`.

**Definition used.** A parameter is white space when the best score of any deep product is below 75 out of 100. That holds **even when vendor claims are accepted at face value**. 32 of 78 parameters meet that bar. The ten below have the highest buyer weight and the clearest gap. Each one ends with a concrete, measurable definition of "first in the world" and the rubric test that proves it.

**Caution before any public "first in the world" claim.** "First" here means first among the 21 products reviewed. Four of the six deep editors were behind sign-up walls, so features may be hidden there. Before anything is published:

1. Open trial accounts and re-check items 1, 2, 3 and 8.
2. Run an extended search of Kujiale's China-only edition, Korean and Japanese developer "model house" apps, and Gulf developer portals.

Until then, the honest phrasing is "no product among the 21 we tested does X".

---

## 1. K04: video call built into the design space

| | |
|---|---|
| **Best today** | 0 of 100 among the deep products. Outside the set, Floorfy runs video calls inside 360 property tours with no design editing [VC] https://floorfy.com/products/videocall. Planner 5D, Coohom and Rayon co-edit with no video [VC]. |
| **Why buyers care** | A tenant-change meeting with the sales rep and an interior designer is today an office visit with AutoCAD prints. Israeli developer job ads describe this coordination as manual [RV] https://www.drushim.co.il/job/38949395/e622195e/ |
| **First in the world means** | A WebRTC call with at least 3 participants (buyer, rep, designer) opens **inside** the designer from a link. Nobody installs anything, and it works on a phone and a desktop. Video tiles never cover the 3D or plan canvas: they dock to the side on desktop and to the bottom sheet on a phone. |
| **Proof** | K04 = 100 [LT] on two real phones plus a desktop, run by an outside tester. Companion measures: join time from link tap to A/V of 6 s or less on IL-4G, and A/V that survives a 2D/3D switch with no reload. |

## 2. K05: follow-me camera and control handover

| | |
|---|---|
| **Best today** | 0 across all products. The only claim of shared control comes from CPQ3D, where both parties edit an outdoor-structure configuration during a call [VC]. |
| **Why buyers care** | "Look where I'm looking" is the whole point of a design meeting. Without it, three people describe the same wall in words. |
| **First in the world means** | **Presenter mode:** all participants' cameras and plan markers follow the presenter. **Control:** a single "take control / give control" button. **Edit locks:** an edit lock shows who holds the pen. **Performance targets:** state sync of 150 ms or less at p95 between Tel Aviv clients, and handover completes in 300 ms or less. Every edit made during the call is attributed to a person (this feeds item 5). |
| **Proof** | K05 = 100 [LT]. Latency is measured with synthetic clients over 100 handovers, and both p50 and p95 are reported. |

## 3. A01, A02, A03: Hebrew-native right-to-left designer

| | |
|---|---|
| **Best today** | No product offers Hebrew. That holds for all 16 landing pages we checked through hreflang [LT] and all vendor language lists. Homestyler offers Arabic on its marketing site, and whether its editor mirrors for right-to-left is unknown [LT]. |
| **Why buyers care** | It is a Hebrew-first market, and Ben's audience also reads English, Russian, French and Arabic. Mixed Hebrew and number labels (for example סלון 24.5 מ"ר, or ממ"ד, the safe room) break in left-to-right tools. |
| **First in the world means** | A full Hebrew interface: mirrored panels and rails, Hebrew number entry, and correct bidirectional text on the 2D plan, on 3D labels and in the PDF spec. The six bidi checks in A03 all pass (room names with numbers, units, the ממ"ד abbreviation, ₪ amounts, dimension chains, and a mixed Hebrew/English brand name). Arabic is the second right-to-left locale. A Hebrew accessibility statement is published under IS 5568 (A07). |
| **Proof** | A01 = 100, A02 = 100 and A03 = 100% [LT], verified by a native Hebrew tester and an Arabic tester. |

## 4. C04, C05, S05: Israeli priced catalogue with honest provenance

| | |
|---|---|
| **Best today** | C04 and C05 are 0 everywhere. Planner 5D and Coohom bill subscriptions in ₪ [VC], but their catalogues are not Israeli. Coohom's public product list shows no prices, and item names appear in Chinese on an English link [LT]. No product discloses VAT, labour or a validity date (S05 = 0 or unknown). |
| **Why buyers care** | A buyer compares a developer's upgrade price against a shop price. Without a supplier, a date and the VAT basis, every number is suspect. |
| **First in the world means** | Every selectable finish or fixture shows a ₪ price, and the VAT status is printed in plain words. On tap, the item shows its supplier, the date the price was captured, its valid-until date and whether installation is included. At least 95% of the items in a developer's option list carry a price. Prices without fresh provenance are visibly marked "estimate", never shown as fact. |
| **Proof** | C04 = 100, C05 at 95% or above of sampled items, and S05 at 4 of 4 [LT], all checked by a person outside the build team. |

## 5. S03, S04: מפרט-native spec sheet and delta against the base specification

| | |
|---|---|
| **Best today** | 50 at most. Higharc labels options "Upgrade to…" against a standard and claims option pricing [LT and VC]. GBuilder claims an extra cost per option and an e-signed selection [VC]. Nobody offers credits (זיכויים) for standard items the buyer drops, or a document in the structure of the Israeli מפרט. |
| **Why buyers care** | The מפרט and the price appendix are what the buyer actually signs. Today that reconciliation is done by hand, line by line. |
| **First in the world means** | One click produces a Hebrew PDF laid out room by room in the מפרט structure: flooring, wall cladding, sanitary ware, kitchen, joinery, electrical and communication points, AC and safe-room items. Each line is marked standard, upgrade, credit or decor-only, with its ₪ delta and a net total. The PDF is versioned, can be signed by the buyer, and carries the decision log from item 2. Tenant-change deadlines per category (I07) are printed on it. |
| **Proof** | S03 = 100 and S04 = 100 [LT]. Three real developer מפרט documents are reproduced line for line, and a developer's tenant-change coordinator signs off that the output is usable without retyping. |

## 6. P06, with I04: structural and buildability rules for Israeli apartments

| | |
|---|---|
| **Best today** | 50. Higharc and GBuilder lock everything because they are options-only [VC]. The consumer tools lock nothing; Floorplanner's demo invites "Drag a wall to enlarge the room" [LT]. Nobody offers **free design of non-structural elements together with enforced structural rules**. |
| **Why buyers care** | In a tower, load-bearing walls, shafts, the safe room (ממ"ד), wet zones and the façade cannot move. A buyer who designs an impossible kitchen loses weeks and trust. |
| **First in the world means** | The developer's unit model carries a structural layer. Its rules cover: (a) load-bearing walls and columns, (b) MEP shafts, (c) ממ"ד walls, door and window (Home Front Command rules), (d) wet-zone limits for moving toilets and showers relative to the drains, (e) the façade and window line. Any attempt to break a rule is blocked at the moment of the edit, with a one-line Hebrew reason and a link to the developer's tenant-change policy. Partitions, finishes and furniture stay free. |
| **Proof** | P06 = 100 [LT]. The I04 check is 20 known-invalid edits on two developer plans, and all 20 must be blocked with a reason; zero false blocks are allowed on 20 valid edits. |

## 7. T01, T02: honesty labels on every visual

| | |
|---|---|
| **Best today** | T01 is 50 (Higharc distinguishes standard from upgrade in its option text [LT]). T02 is 0 everywhere we could see [LT]. AI tools market the opposite of caution: Interior AI's headline is "Fire your interior designer" [LT]. |
| **Why buyers care** | Renders sell, and a rendered sofa that the price doesn't include becomes a dispute after delivery. Ben's projects require honesty labels. |
| **First in the world means** | Every object in 3D, in the plan and in the spec carries one of four badges: included in the base price, paid upgrade, decoration not included, or AI suggestion. A filter "show only what I'm paying for" re-renders the apartment without decor. Shared images and PDFs carry a visible line, in plain words, saying the image is an illustration and not part of the contract. |
| **Proof** | T01 = 100 and T02 = 100 [LT]. An audit of 20 random objects finds 100% correctly badged, and every share artefact (image, link, PDF) is checked. |

## 8. P03, with T03: measured plan-recognition accuracy, published

| | |
|---|---|
| **Best today** | No vendor publishes an accuracy figure. Planner 5D says measurements are "approximate" [VC], Homestyler labels its auto-generate "Beta" [VC], and Archilogic "cannot guarantee" accuracy without a scale [VC]. |
| **Why buyers care** | On the general "עיצוב דירה" page, buyers will upload their own plans, and a 3% wall error ruins a kitchen. |
| **First in the world means** | A public benchmark of 30 Israeli plans: developer sales PDFs, scanned paper plans and CAD exports, with ground-truth dimensions. Median wall-length error is 1% or less and room-area error 2% or less. The editor shows a ± tolerance next to every recognised dimension until the user confirms or corrects it. The benchmark set and the results are published. |
| **Proof** | P03 = 100 and T03 = 100 [LT]. Competitor numbers are measured the same way once trial accounts exist. |

## 9. G03: generation that respects structure, allowed options and budget

| | |
|---|---|
| **Best today** | 0 among the deep products. ReimagineHome (light coverage) claims to restyle "without touching walls, windows, or doors" with real products "within budget" [VC], but its output is an image, not a model. |
| **Why buyers care** | A buyer types "a warm kitchen up to ₪40,000", and today they get either a fantasy picture or a manual hunt through options. |
| **First in the world means** | A Hebrew text or voice request generates up to three editable 3D variants. Each variant uses only items in the developer's allowed option list plus free decor, never violates the structural layer from item 6, and stays at or below the stated ₪ cap. The cost delta is shown side by side (G04). |
| **Proof** | G03 = 100 (3 of 3 constraints) on 20 prompts, so 60 variants, with zero violations [LT]. |

## 10. F04, F05, M06: first interior 3D on a phone that is light and fast

| | |
|---|---|
| **Best today** | Every first interior 3D view we could open cost 12–21 MB: Floorplanner 21.1 MB, Coohom 15.2 MB, Higharc at least 11.8 MB and over 1,200 requests, still loading [LT]. The fastest canvas was Floorplanner at 5.6 s on desktop [LT]. |
| **Why buyers care** | The designer lives inside every project page, and most visitors come from a phone. Heavy payloads lose them before the first frame. |
| **First in the world means** | From a project page on a mid-range Android over IL-4G: the first interactive interior frame in 4 s or less at p50 (8 s or less on Slow 4G), with 5 MB or less transferred and 60 requests or fewer. Progressive detail streams after that. The project page's own LCP stays at 2.5 s or less with the designer embedded (CLS 0.1 or less). |
| **Proof** | F04 = 100, F05 = 100 and M06 at 75 or above [LT]. Five cold runs on real devices, and our worst run must beat every competitor's best run. |

---

## Runners-up (white space, lower weight or partly covered)

| Parameter | Gap today | First-in-world target |
|---|---|---|
| K07 decision log, with I07 tenant-change deadlines | Undo only, or unknown [LT/UNK] | A per-person, timestamped change log exported with the spec. Each category locks when its developer deadline passes. |
| T04 data consistency | Higharc: 2,830 ft² on the plan page against 2,889 sqft in the configurator [LT]. Coohom: Chinese item names on an English link [LT]. | One data source per unit. An automated nightly check covers area, rooms, prices and labels across the project page, the designer and the PDF, with 0 mismatches. |
| T05 true orientation and window view | Floorplanner has a manual sun dial only [LT]. GBuilder claims real views [VC]. REALS (Israel) shows views and shading without design. | A geolocated sun path for the actual floor, date and hour, plus the real window view (a photo or a 3D city model at the unit's height). |
| M02, M05 thumb-zone 3D | Every primary CTA sits at 44–49% of screen height or at the top [LT]. Coohom's tour controls are top-right [LT]. | Primary actions in the bottom 40% of the screen, tap-to-walk, and one-thumb operation of all 3D navigation (buyer-gaze rules). |
| A07 accessibility statement | 404 for all seven products [LT] | A Hebrew IS 5568 statement plus a WCAG 2.2 AA audit of the designer itself, not just the page. |
