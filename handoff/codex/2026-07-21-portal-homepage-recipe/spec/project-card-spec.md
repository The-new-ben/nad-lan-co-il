# Project Card Specification

## Purpose

The card must let a buyer understand, compare and trust a project in a few seconds. It is not a miniature brochure and not a poster with vague luxury copy.

## Canonical desktop anatomy

1. **4:3 media frame**
   - approved hero image;
   - top-start lifecycle badge;
   - top-end save button;
   - bottom image count/media indicators;
   - visible `המחשה בלבד` overlay when applicable.
2. **Identity**
   - project name, maximum two lines;
   - developer name, text first; approved logo optional;
   - city + neighborhood/compound.
3. **Commercial line**
   - approved `החל מ־…` or `מחיר עדכני לפי פנייה`;
   - never an unlabelled estimate.
4. **Comparable facts**
   - unit/room range;
   - size range when current;
   - construction stage;
   - handover/occupancy when current.
5. **Proof row**
   - maximum three: verified, floorplans, 3D, foreign-ready;
   - `+N` disclosure for additional facilities/media.
6. **Freshness/source**
   - `נבדק 18.7.2026` or a concise equivalent;
   - source/owner available in accessible disclosure.
7. **Actions**
   - primary: `לפרויקט`;
   - secondary: compare/save;
   - contact/WhatsApp may be direct only when routing and consent are approved.

## Mobile anatomy

- Full-width 4:3 media.
- Identity and price directly under image.
- One compact facts row, wrapping without truncating meaning.
- Maximum two visible proof badges.
- Full-width primary action or a clear card-level link.
- Save target at least 44×44px by internal standard.
- No hover dependency and no horizontal card overflow.

## Required fields to render a public project card

| Field | Rule | Missing behavior |
| --- | --- | --- |
| Project title | canonical approved name | draft/private |
| Developer | verified text identity | draft unless explicitly unknown legacy record |
| Location | city + neighborhood/compound or approved address | draft/private |
| Hero media | approved/rights-cleared or visible illustrative state | neutral missing state allowed only outside featured rails |
| Project lifecycle | controlled vocabulary | `מידע בהשלמה`; no lifecycle badge |
| Price policy | approved current price/range, explicit estimate or request-current-price | show request-current-price |
| Unit/room range | structured and dated | omit row, never invent |
| Source | internal/official/public source class + URL/record | cannot receive verified badge |
| Verified date | successful check time | no recently-verified placement |
| Contact owner | named route, not necessarily public name | cannot be lead-ready |
| Demo flag | must be false | never public |
| Data quality | at least basic-verified | draft/noindex |

## Optional structured fields

- size range;
- building/floor/unit counts;
- completion/handover;
- payment plan;
- gallery/video/plan/3D availability;
- facility set;
- foreign-buyer readiness;
- developer logo;
- sponsored placement;
- availability policy and unit-level data.

## Badge evidence contract

| Badge | Exact evidence required | Automatic removal condition |
| --- | --- | --- |
| מידע מאומת | ownership/source verified + required facts checked + `verified_at` within policy | verification expires or source conflict opens |
| 3D | working public approved tour/model URL + poster + asset state not demo | media fails, rights expire or `project_3d_demo=1` |
| תוכניות | at least one approved current plan with type/version | file removed, rights/version unknown |
| מוכן לרוכשים מחו״ל | EN parity + currency/units + remote contact + process content + tested route | any readiness component fails |
| מסלול תשלומים | approved current terms with source/date | terms expire or are not rechecked |
| בבנייה / שיווק / אכלוס | approved controlled status and date | recheck overdue or conflict exists |
| מקודם / ממומן | active placement record | placement expires |

“Verified” is never purchasable. “Sponsored” is never rendered with a trust color/icon.

## Facility layer

Cards show at most three high-value facility/proximity signals. The full project page may show the complete taxonomy.

Recommended controlled groups:

- residence: balcony, parking, storage, accessibility;
- building: lobby, residents' club, coworking/library, bike room;
- wellness: gym, pool, spa/sauna, yoga;
- family: children's room, garden/courtyard;
- context: sea/open view, park, education, shopping, transit;
- specification: shutters, intercom, smart-home, green-building standard.

Every facility has value, label_HE, label_EN, evidence source, approval state and optional map relationship. A marketing paragraph alone is not sufficient evidence for a card badge until it is reviewed and structured.

## Price wording rules

| State | Public wording |
| --- | --- |
| Approved current starting price | `החל מ־₪…` + checked date |
| Approved range | `₪…–₪…` + unit scope/date |
| Licensed indicative estimate | `אומדן: ₪…` + visible methodology/source note |
| Price unavailable/volatile | `מחיר עדכני לפי פנייה` |
| Unit-level price | appears only after the unit is selected and verified |

Do not use “starting at” when only one historical/example unit supports the figure.

## Ranking and placement

Quality eligibility happens before ranking. A card may enter public/featured queries only if it passes the minimum public state. Within the eligible set:

1. user relevance;
2. freshness;
3. completeness;
4. editorial curation;
5. paid placement, visibly disclosed.

Paid tier may not promote a demo, stale, rights-incomplete or broken-contact record.

## Accessible card behavior

- One primary linked heading/image relationship; avoid nested competing links.
- Save/compare are real buttons with labels and state (`aria-pressed` where applicable).
- Badges are text, not icon-only.
- Image alt identifies the project and image type; illustrative state is also in visible text.
- Keyboard focus order follows visual order in RTL and LTR.
- Truncated descriptions are avoided; cards use structured facts instead.

## Acceptance examples

### Good

> Rainbow Tel Aviv · Israel Canada · Sde Dov, Tel Aviv · current price by inquiry · marketing · plans · 3D · information checked 18.7.2026 · illustrative concept image.

### Not acceptable

> Luxury dream by the sea · best deal · limited units · verified · 3D

The second example has no comparable facts, no evidence, no source/date and unsupported scarcity.
