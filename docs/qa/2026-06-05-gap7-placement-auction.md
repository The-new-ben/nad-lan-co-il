# GAP 7 placement auction QA - v1.47.0

Branch: `codex/gap7-placement-auction`  
Scope: plugin lane only, `plugins/nadlan-config/**` and `docs/**`

## What changed

- Added `inc/placement-auction.php`.
- Added per-card auction meta:
  - `auction_bid`
  - `auction_area`
  - `auction_category`
  - `auction_bid_at`
  - `auction_rank`
  - `auction_clearing_price`
  - `_nadlan_auction_winner`
  - `auction_next_cycle_amount`
  - `auction_proration_policy=next_cycle`
- Added `nadlan_auction_area_key( $card_id )`:
  - explicit `auction_area` wins
  - then `city`
  - then coarse `lat/lng`
  - then `sitewide`
  - filterable by `nadlan_auction_area_key`
- Added `nadlan_auction_category_key( $card_id )`:
  - explicit `auction_category` wins
  - then `professional`, `project`, or `property`
  - filterable by `nadlan_auction_category_key`
- Added rank engine:
  - order by `auction_bid DESC`
  - then paid tier weight `premier > pro`
  - then `data_quality=enriched`
  - then older bid wins ties
- Defaults:
  - 3 slots per area/category
  - reserve NIS 0
  - increment NIS 50
  - second-price clearing
  - 1 reserved quality slot, so paid auction slots are `slots - 1` while enabled
  - charge policy is next-cycle, not immediate proration
- Added `POST /nadlan/v1/auction/bid`.
- Added 5 minute per-card/user bid cooldown.
- Added good-standing guard: cards in `retrying` or `lapsed` dunning, or not on `pro|premier`, cannot win.
- Added `nadlan_auction_outbid` action for displaced winners.
- Added `nadlan_auction_settled` action after recompute.
- Added `nadlan_revenue_event( 'auction_bid_commitment', ... )` seam.
- Added Settings -> NadLan Auction for enabled flag, slots, reserve, increment, category toggles, quality floor, and slot overrides.
- Added healthcheck `auction.enabled`, `auction.active_contests`, `auction.avg_winning_bid`.

## SQL composition

Existing GAP1 paid placement sets:

```sql
CASE nadlan_paid_tier_pm.meta_value WHEN 'premier' THEN 2 WHEN 'pro' THEN 1 ELSE 0 END DESC,
wp_posts.menu_order ASC,
wp_posts.post_date DESC,
wp_posts.ID DESC
```

GAP7 adds its `posts_clauses` filter at priority 25, after paid placement priority 20. It prepends:

```sql
CASE nadlan_auction_winner_pm.meta_value WHEN '1' THEN 1 ELSE 0 END DESC
```

Final expected order for featured directory queries:

```sql
auction winner DESC,
paid tier CASE DESC,
menu_order ASC,
post_date DESC,
ID DESC
```

This means an auction winner outranks a flat Premier, but regular paid placement still works for every non-auction card.

## Curl walkthrough

Prerequisites:

- Two owned cards in the same area/category.
- Both are `paid_tier=pro` or `paid_tier=premier`.
- Both are not in dunning.
- The logged-in user has a nonce/session or use an authenticated Application Password.

Bidder A:

```bash
curl -X POST "https://nad-lan.co.il/wp-json/nadlan/v1/auction/bid" \
  -u "USER:APP_PASSWORD" \
  -H "Content-Type: application/json" \
  --data '{"card_id":111,"bid":100}'
```

Expected:

```json
{"ok":true,"card_id":111,"bid":100,"rank":1,"winner":true,"clearing_price":50}
```

Bidder B raises:

```bash
curl -X POST "https://nad-lan.co.il/wp-json/nadlan/v1/auction/bid" \
  -u "USER:APP_PASSWORD" \
  -H "Content-Type: application/json" \
  --data '{"card_id":222,"bid":200}'
```

Expected:

- Bidder B becomes rank 1.
- If paid auction slots are already full, Bidder A receives `do_action( 'nadlan_auction_outbid', 111, $area )`.
- Clearing price for Bidder B becomes next bid + increment, subject to reserve.
- `_nadlan_auction_winner=1` is written to winning cards only.

## Edge tests

| Case | Expected |
| --- | --- |
| Tie bids | Older `auction_bid_at` wins |
| Single bidder | Pays reserve or next-bid+increment, whichever is higher |
| Zero bidders | No winners, normal paid placement continues |
| Bid below clearing + increment | `422 bid_too_low` |
| Bid from non-owner | `403 forbidden` |
| Bid from free card | `402 not_in_good_standing` |
| Bid from dunning/lapsed card | `402 not_in_good_standing` |
| Category disabled | `403 category_disabled` |
| Rapid second raise | `429 rate_limited` |
| Displaced winner | `nadlan_auction_outbid` fires |
| Recompute called twice | Same winner metadata, no duplicate side effects |
| Previous winner no longer eligible | `_nadlan_auction_winner` is cleared before current winners are written |

## Admin settings QA

- `nadlan_auction_enabled` toggles auction ordering and REST bidding.
- `nadlan_auction_slots_default` clamps to 1-20.
- `nadlan_auction_reserve` clamps to >=0.
- `nadlan_auction_increment` clamps to >=1.
- Enabled categories are stored as an array of `professional|project|property`.
- Slot overrides accept one line per rule: `area|category|slots`.

## C1-C10 checklist

- C1 scope: plugin/docs only, no theme files.
- C2 versioning: plugin header, healthcheck, manifest, and ZIP bumped to `1.47.0`.
- C3 loader: `placement-auction` added after `advertiser-orders`.
- C4 edge cases: listed above.
- C5 security: REST bid requires login, ownership through `current_user_can( 'edit_post', $card_id )`, and 5 minute cooldown.
- C6 data model: auction data is postmeta on the card.
- C7 lifecycle: bid writes next-cycle commitment only; charging stays with the recurring rail.
- C8 performance: rank results are cached for 5 minutes and recomputed on bid changes.
- C9 copy: admin-only English controls; no public marketing strings added.
- C10 seams: emits `nadlan_auction_outbid`, `nadlan_auction_settled`, and `nadlan_revenue_event`.

## Local verification

Local PHP is not installed in this Windows environment, so `php -l` could not run here. Claude should run:

```bash
find plugins/nadlan-config -name '*.php' -print0 | xargs -0 -n1 php -l
```

Static gates:

```bash
rg -n "add_filter\\( 'posts_clauses', 'nadlan_auction_clauses', 25|register_rest_route\\( 'nadlan/v1', '/auction/bid'|current_user_can\\( 'edit_post', \\$card_id \\)|nadlan_auction_outbid|nadlan_auction_settled|nadlan_revenue_event|auction_next_cycle_amount|auction_proration_policy" plugins/nadlan-config/inc/placement-auction.php
tar -tf plugin-dist/nadlan-config-1.47.0.zip | grep '^nadlan-config/inc/placement-auction.php$'
```
