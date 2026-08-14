# Advertiser Journey QA Matrix

Date: 2026-06-04
Purpose: concrete QA evidence required before calling the advertiser monetization system production-ready.
Mode: docs-only. This file describes tests; it does not implement fixes.

## Live Smoke Checks Already Run

| Check | Result |
| --- | --- |
| `curl -s -o NUL -w "join-pro %{http_code}" https://nad-lan.co.il/join-pro/` | `200` |
| `curl -s -o NUL -w "advertiser-center %{http_code}" https://nad-lan.co.il/advertiser-center/` | `302` logged-out redirect |
| `curl -s -o NUL -w "advertise %{http_code}" https://nad-lan.co.il/advertise/` | `404`, correct while parked |
| `curl -i https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck` | Original PR evidence was `1.41.2`; refreshed evidence after 1.42.2 is below |

## Post-1.42.2 Evidence Refresh

| Check | Result |
| --- | --- |
| `curl https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck` | `200`; version `1.42.2`; `advertiser_center` and `advertiser_order_bridge` reported live |
| `curl https://nad-lan.co.il/join-pro/` | `200`; canonical `/join-pro/`; source still contains monthly/traffic-oriented metadata and Wikimedia `og:image` |
| `/advertiser-center/` logged-out status | Earlier PR evidence said `302`; post-1.42.2 command-line probes were inconsistent from this machine. Claude should rerun before merge. |
| `/advertise/` parked status | Earlier PR evidence said `404`; post-1.42.2 command-line probes were inconsistent from this machine. Claude should rerun before merge. |

Healthcheck invariants observed:

- `activation_hook = woocommerce_payment_complete`
- `uses_paid_tier = true`
- `card_meta = campaign_end, paid_order_id, paid_product_id`
- `daily_downgrade_cron = true`
- `durations_days = 476:30, 477:30, 489:180, 490:60`

## Test Data Needed

Claude/owner should create or identify:

- Test customer user: `advertiser-test@nad-lan.co.il`
- Owned professional card attached to the test user.
- Owned project card attached to the test user.
- Owned property card attached to the test user if product 490 is in scope.
- One paid order with product 489 and no card_id, for no-context purchase QA.
- Gateway test mode or owner-approved real low-risk payment/refund flow.
- Access to WordPress admin order notes and `nadlan_lead` entries.

## QA Matrix

### 1. Canonical Package Page

| Item | Expected | Evidence |
| --- | --- | --- |
| `/join-pro/` loads | HTTP 200 | Curl status plus browser screenshot |
| `/advertise/` remains parked | 404 unless owner/Claude approve URL | Curl status |
| Product CTAs exist | 476, 477, 489, 490 add-to-cart paths visible | Source search or browser click |
| Product copy matches duration | 476/477 are 30 days, 489 is 180 days, 490 is 60 days unless product decision changes | Screenshot of package copy plus healthcheck/product map |
| No traffic guarantee | Copy promises asset/placement/duration/reporting, not guaranteed views | Screenshot and copy excerpt |
| Metadata matches offer | Title, meta description, OG description, Product schema, and `og:image` match the approved paid model and non-stock visual standard | Source fetch plus browser/social preview |

### 2. Logged-Out Advertiser Center

| Item | Expected | Evidence |
| --- | --- | --- |
| `/advertiser-center/` logged out | Redirect to login with return URL | Curl `302` and `Location` header |
| Login return | After login, user returns to center | Browser video/screenshot |
| No private data leak | Logged-out page does not expose card/order data | Source check |

### 3. Logged-In Center With Owned Cards

| Item | Expected | Evidence |
| --- | --- | --- |
| Owned cards visible | User sees owned professional/project/property cards | Screenshot |
| Completion score | Score and missing fields reflect real meta | Screenshot plus meta sample |
| Studio link | `/studio/?id=<card_id>` opens for owned card | Browser screenshot |
| Public preview link | Opens public profile in new tab | Browser screenshot |
| Upgrade CTA | Free card upgrade includes correct `card_id` and product | URL capture |
| Recent orders | Paid products appear with order status/total/date | Screenshot |

### 4. Checkout With `card_id`

| Scenario | Expected | Evidence |
| --- | --- | --- |
| Professional Pro | Product 476 with professional `card_id` activates `paid_tier=pro` for 30 days | Order note, card meta, healthcheck optional |
| Professional Premier | Product 477 with professional `card_id` activates `paid_tier=premier` for 30 days | Order note, card meta |
| Project campaign | Product 489 with project `card_id` activates `paid_tier=premier` for 180 days | Order note, card meta |
| Property promo | Product 490 with property `card_id` activates `paid_tier=pro` for 60 days | Order note, card meta |
| Wrong card type | Product/card mismatch is rejected, not activated | Order note or UI error |
| Ownership mismatch | Paid order from another user does not activate card | Order note: ownership mismatch |

### 5. Checkout Without `card_id`

| Item | Expected | Evidence |
| --- | --- | --- |
| Purchase allowed | Order can be created/paid without context if public CTA has no card | Woo order |
| No silent activation | Card meta is unchanged until attached | Card meta before/after |
| Center surfaces order | User sees "unlinked purchase" box | Screenshot |
| Attach picker | Matching owned cards are listed | Screenshot |
| No matching card | UI clearly says to find/claim/create/request a matching card | Screenshot |
| Attach after paid | Once attached, paid order applies immediately | Order note and card meta |

### 6. Expiry And Editorial Guard

| Item | Expected | Evidence |
| --- | --- | --- |
| Expired paid campaign | `campaign_end < now`, `paid_order_id > 0`, tier pro/premier -> `paid_tier=free` | Cron run result |
| Editorial showcase | `paid_tier=premier` and no `paid_order_id` is not downgraded | Before/after meta |
| Trial card | Claim/trial without paid order is not downgraded by advertiser cron | Before/after meta |
| Renewal state | Center shows active/expired/renew next action | Screenshot |

### 7. Lead Attribution

| Item | Expected | Evidence |
| --- | --- | --- |
| REST lead with valid `card_id` | Lead stores `lead_card_id=<exact card id>` | `nadlan_lead` meta |
| REST lead with invalid `card_id` | No `lead_card_id` is stored | `nadlan_lead` meta |
| Admin-post lead with valid card | Same exact meta behavior | `nadlan_lead` meta |
| Lead count | Advertiser center counts only exact numeric `lead_card_id`, not text LIKE matches | Create card #5 and unrelated lead containing `5`; count must not increment |
| CTA sources | Studio quote, claim prompt, and featured upsell pass `card_id` to `/nadlan/v1/lead` | Browser/network capture |

### 8. Studio And Media

| Item | Expected | Evidence |
| --- | --- | --- |
| Open Studio for owned card | 200 and editable | Screenshot |
| Unauthorized card | Denied or redirected | Screenshot |
| Description save | Persists and public page updates | Before/after screenshot |
| Contact save | Phone/email/social save if fields exist | Meta/public check |
| Image upload | Uploaded image appears in Studio and public profile/gallery | Screenshot |
| Map pin | Lat/lng save and public map uses it | Screenshot |
| Missing field | If a necessary advertiser field is absent, document it for Claude instead of faking data | Gap note |

### 9. Reporting

| Item | Expected | Evidence |
| --- | --- | --- |
| Views | Center shows per-card views | Screenshot and meta sample |
| Leads | Center shows exact attributed inquiries | Screenshot and lead meta sample |
| Orders | Center shows paid orders and linked card | Screenshot |
| Campaign dates | Active until date visible for paid campaigns | Screenshot |
| Period report | Monthly or campaign-period report can be exported or at least rendered | Screenshot/PDF if implemented |
| Recommendation | Center tells advertiser next best action: complete profile, add photos, renew, upgrade | Screenshot |

### 10. Mobile 390px

| Surface | Expected | Evidence |
| --- | --- | --- |
| `/join-pro/` | No horizontal overflow, product cards readable, CTAs 44px+ | 390px screenshot and scrollWidth check |
| `/advertiser-center/` | Metrics/cards/orders are readable, no clipped buttons | 390px logged-in screenshot |
| `/studio/?id=<card_id>` | Upload/save/map controls usable | 390px screenshot |
| Checkout | Cart/checkout/gateway fields usable in RTL | 390px screenshot |

### 11. Premium Trust Pass

| Surface | Expected | Evidence |
| --- | --- | --- |
| `/join-pro/` | Looks like a premium paid product, not a generic WordPress pricing page | 390px and 1440px screenshots |
| Public catalogs | No raw sprite IDs such as `profession-developer`, no low-contrast hero text, no abandoned blank cards | PR #45 issues resolved and screenshots |
| Single profiles/projects | Desktop first viewport renders real content, no blank capture, no duplicate H1/theme noise | Browser screenshots and H1 count |
| Internal center | Buttons, chips, empty states, order panels, attach picker, and upload controls match the public premium language | Logged-in screenshot set |
| Media policy | No fake faces, no stock-photo copy, no misleading non-Israeli defaults | Asset/source audit |

## Release Verdict Template

Use this after a QA run:

```md
## Advertiser QA Verdict

Date:
Tester:
Build/plugin version:
User:

Pass:
- ...

Blockers:
- ...

Majors:
- ...

Minors:
- ...

Evidence:
- Healthcheck:
- Screenshots:
- Orders:
- Lead ids:
- Card ids:

Ship decision:
- [ ] Ready
- [ ] Not ready
```

## What This Matrix Does Not Cover

- Legal approval of sponsored-content wording.
- Actual payment settlement/refund accounting in Morning/Green Invoice.
- Final internal advertiser UX polish. Public premium UI shipped in 1.42.2, but authenticated center/studio screens still need their own visual QA pass.
