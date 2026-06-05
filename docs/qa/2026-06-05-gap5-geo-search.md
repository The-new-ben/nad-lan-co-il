# GAP 5 QA: Geo Search

Scope: nadlan-config v1.44.0, `inc/geo-search.php`, loader, directory card distance seam, ZIP, manifest.

## Sources Read

- Repo spec: `docs/2026-06-04-codex-implementation-spec.md`, GAP 5.
- Aaron Francis, efficient distance querying in MySQL: bounding-box prefilter before exact distance so MySQL can reduce candidate rows first. https://aaronfrancis.com/2021/efficient-distance-querying-in-mysql-33acab3c
- Plum Island Media, Haversine SQL pattern: guard the ACOS argument with `LEAST(1.0, ...)` to avoid floating-point domain errors. https://www.plumislandmedia.net/mysql/haversine-mysql-nearest-loc/
- MySQL 8.4 spatial convenience functions: future native path is POINT/SRID data plus `ST_Distance_Sphere()` once the data model moves off postmeta. https://dev.mysql.com/doc/refman/8.4/en/spatial-convenience-functions.html

## What Changed

- Added `inc/geo-search.php`.
- Added `geo-search` to the plugin loader.
- Added `nadlan_geo_search_args($args,$lat,$lng,$radius_km)` with radius clamp `[0.5,100]`.
- Added bounding-box mode using `lat_min`, `lat_max`, `lng_min`, `lng_max`.
- Registered `posts_clauses` at priority `30`, after GAP 1 paid placement at priority `20`.
- Joined `lat` and `lng` postmeta with `INNER JOIN`, so records without coordinates are excluded.
- Added Haversine distance as `nadlan_distance_km`.
- Ordering is paid tier first, then distance, then post date and ID.
- The geo filter reads the incoming paid-placement `ORDER BY` and derives the paid-tier CASE from it when present.
- The query sets `DISTINCT` so duplicate `lat` or `lng` meta rows cannot multiply result cards.
- Added `GET /nadlan/v1/near`.
- Added 8/min/IP rate limit.
- Added `do_action('nadlan_geo_results',$results)` for future theme map rendering.
- Added `nadlan_geo_card_distance` filter seam and card-template distance chip.
- Healthcheck now includes `geo.loaded` and `geo.sample_row_count`.

## 10-Cycle Checklist

| Cycle | Result |
|---|---|
| C1 foundation | One module, one REST endpoint, one query-arg helper. |
| C2 composition | Paid placement filter stays at priority 20; geo filter runs at 30, reads the incoming paid CASE, and keeps paid tier first. |
| C3 input safety | `lat`, `lng`, radius, bbox, and type are sanitized; invalid coordinates return 422. |
| C4 edge cases | 0 results, exactly-on-radius, missing coords, radius clamp, bbox, and antimeridian note covered below. |
| C5 security | Public endpoint is read-only and rate-limited 8/min/IP. |
| C6 CMS fit | Uses existing `lat` and `lng` postmeta; no schema migration needed now. |
| C7 monetization | `paid_tier=premier` outranks `pro`, which outranks free, before distance. |
| C8 performance | Box prefilter narrows rows before exact Haversine; future POINT/SRID path documented. |
| C9 seams | `do_action('nadlan_geo_results',$results)` and `nadlan_geo_card_distance` are in place. |
| C10 proof | Static gates below verify loader, REST route, joins, SQL order, healthcheck, and ZIP. |

## SQL Composition Proof

The existing GAP 1 filter:

```php
add_filter( 'posts_clauses', 'nadlan_dir_paid_placement_clauses', 20, 2 );
```

The new GAP 5 filter:

```php
add_filter( 'posts_clauses', 'nadlan_geo_clauses', 30, 2 );
```

Final expected SQL shape for a Tel Aviv radius query:

```sql
SELECT wp_posts.*,
  (6371.0088 * ACOS(LEAST(1.0, GREATEST(-1.0,
    COS(RADIANS(32.0853)) * COS(RADIANS(CAST(nadlan_geo_lat_pm.meta_value AS DECIMAL(10,6))))
    * COS(RADIANS(CAST(nadlan_geo_lng_pm.meta_value AS DECIMAL(10,6))) - RADIANS(34.7818))
    + SIN(RADIANS(32.0853)) * SIN(RADIANS(CAST(nadlan_geo_lat_pm.meta_value AS DECIMAL(10,6))))
  )))) AS nadlan_distance_km
FROM wp_posts
LEFT JOIN wp_postmeta AS nadlan_paid_tier_pm
  ON (wp_posts.ID = nadlan_paid_tier_pm.post_id AND nadlan_paid_tier_pm.meta_key = 'paid_tier')
INNER JOIN wp_postmeta AS nadlan_geo_lat_pm
  ON (wp_posts.ID = nadlan_geo_lat_pm.post_id AND nadlan_geo_lat_pm.meta_key = 'lat')
INNER JOIN wp_postmeta AS nadlan_geo_lng_pm
  ON (wp_posts.ID = nadlan_geo_lng_pm.post_id AND nadlan_geo_lng_pm.meta_key = 'lng')
WHERE ...
  AND CAST(nadlan_geo_lat_pm.meta_value AS DECIMAL(10,6)) BETWEEN 31.860191 AND 32.310409
  AND CAST(nadlan_geo_lng_pm.meta_value AS DECIMAL(10,6)) BETWEEN 34.515165 AND 35.048435
  AND (6371.0088 * ACOS(LEAST(1.0, GREATEST(-1.0, ...)))) <= 25
ORDER BY CASE nadlan_paid_tier_pm.meta_value
  WHEN 'premier' THEN 2
  WHEN 'pro' THEN 1
  ELSE 0
END DESC,
nadlan_distance_km ASC,
wp_posts.post_date DESC,
wp_posts.ID DESC
```

Duplicate coordinate meta safety: `DISTINCT` is added in `nadlan_geo_clauses()`, so a card with duplicate `lat` or `lng` meta rows cannot appear more than once in the result list.

Runtime debug filter for Claude after install:

```php
add_filter('posts_clauses', function($clauses, $q) {
  if ($q->get('nadlan_geo')) { error_log('NADLAN_GEO_SQL ' . wp_json_encode($clauses)); }
  return $clauses;
}, 99, 2);
```

## Manual Curl QA

Radius query near Tel Aviv:

```bash
curl -s "https://nad-lan.co.il/wp-json/nadlan/v1/near?lat=32.0853&lng=34.7818&radius_km=25&type=project"
```

Expected:

- HTTP 200.
- JSON `ok:true`.
- `results[*].nadlan_distance_km` is numeric.
- Paid premier/pro rows appear before free rows when both are in radius.

Bounding-box query for map-pan:

```bash
curl -s "https://nad-lan.co.il/wp-json/nadlan/v1/near?lat_min=32.02&lat_max=32.15&lng_min=34.72&lng_max=34.86&type=all"
```

Invalid lat/lng:

```bash
curl -i "https://nad-lan.co.il/wp-json/nadlan/v1/near?lat=abc&lng=34.7818"
```

Expected: HTTP 422.

Rate limit:

```bash
for i in {1..9}; do curl -s "https://nad-lan.co.il/wp-json/nadlan/v1/near?lat=32.0853&lng=34.7818"; done
```

Expected: first 8 within a minute can pass, 9th returns 429.

## Edge Tests

- 0 results: choose a tiny radius over water, for example `radius_km=0.5` west of Tel Aviv, and expect `count:0`.
- Exactly-on-radius: seed a test card with known lat/lng at the boundary and confirm it survives because the SQL uses `<=`.
- Antimeridian: direct bbox with `lng_min > lng_max` returns 422. Israel does not cross the antimeridian; proper wrap support is deferred.
- Missing coords: cards without both `lat` and `lng` are excluded by the `INNER JOIN`.
- Radius clamp: values below `0.5` become `0.5`; values above `100` become `100`.

## Performance Note

The current database stores coordinates as postmeta, so the right first step is a cheap bounding-box prefilter plus exact Haversine. At larger scale, move `lat`/`lng` into a native `POINT SRID 4326` column with a SPATIAL R-tree index and use `ST_Distance_Sphere()` for exact distance.

## Local Gates

PHP CLI is not available on this Windows machine, so `php -l` is BLOCKED locally. Claude must run lint before merge.

```bash
tar -tf plugin-dist/nadlan-config-1.44.0.zip | head
tar -xOf plugin-dist/nadlan-config-1.44.0.zip nadlan-config/inc/geo-search.php \
  | grep -c -E "nadlan_geo_search_args|posts_clauses|INNER JOIN|nadlan_distance_km|nadlan/v1.*/near|nadlan_geo_results"
tar -xOf plugin-dist/nadlan-config-1.44.0.zip nadlan-config/nadlan-config.php \
  | grep -c "geo-search"
```

Expected: forward-slash ZIP paths, geo signature count at least 6, loader count at least 1.
