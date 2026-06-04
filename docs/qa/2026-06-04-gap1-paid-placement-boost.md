# GAP 1 QA: Paid Placement Boost

Scope: nadlan-config v1.42.8, `plugins/nadlan-config/inc/directory.php`.

## What Changed

Featured sort now ranks directory cards by paid tier before ordinary recency:

1. `paid_tier=premier`
2. `paid_tier=pro`
3. free or missing `paid_tier`
4. `menu_order ASC` as the secondary tiebreaker inside each tier
5. `post_date DESC`
6. `ID DESC`

The boost is scoped to the featured sort only. `name`, `newest`, and project `units` sorts are unchanged.

## WP-CLI Proof

Run in a WordPress environment after installing v1.42.8. This creates two temporary projects, makes the older one Premier, and proves it ranks above the newer free card on `sort=featured`.

```bash
wp eval '
require_once WP_PLUGIN_DIR . "/nadlan-config/inc/directory.php";
$token = "gap1-" . wp_generate_password(8, false);

$free = wp_insert_post(array(
  "post_type" => "nadlan_project",
  "post_status" => "publish",
  "post_title" => "QA free newest " . $token,
  "post_date" => gmdate("Y-m-d H:i:s"),
));

$premier = wp_insert_post(array(
  "post_type" => "nadlan_project",
  "post_status" => "publish",
  "post_title" => "QA premier older " . $token,
  "post_date" => gmdate("Y-m-d H:i:s", time() - DAY_IN_SECONDS),
));

update_post_meta($free, "paid_tier", "free");
update_post_meta($premier, "paid_tier", "premier");

$q = nadlan_dir_project_query(array("q" => $token, "sort" => "featured", "per_page" => 10));
$ids = wp_list_pluck($q->posts, "ID");
echo "free={$free} premier={$premier}\n";
echo "first ids=" . implode(",", array_slice($ids, 0, 6)) . "\n";

if (array_search($premier, $ids, true) === false || array_search($free, $ids, true) === false) {
  throw new Exception("QA records not present in query");
}
if (array_search($premier, $ids, true) > array_search($free, $ids, true)) {
  throw new Exception("Premier did not rank above newer free record");
}

wp_delete_post($free, true);
wp_delete_post($premier, true);
echo "PASS: premier ranks above newer free record\n";
'
```

## REST Smoke

After the owner updates live:

```bash
curl -s "https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?cb=$(date +%s)" | python3 -m json.tool | grep '"version": "1.42.8"'

curl -s "https://nad-lan.co.il/wp-json/nadlan/v1/projects?sort=featured&per_page=6" \
  | python3 - <<'PY'
import json, re, sys
data = json.load(sys.stdin)
cards = re.findall(r'<a class="nldc([^"]*)"', data.get("html", ""))
print("top6 featured flags:", ["is-featured" in c for c in cards[:6]])
assert any("is-featured" in c for c in cards[:6]), "No paid card in top 6"
PY
```

## Expected Result

- `/wp-json/nadlan/v1/projects?sort=featured` puts paid project cards before free cards.
- `/wp-json/nadlan/v1/directory?sort=featured` uses the same paid-tier ordering for professionals.
- Non-featured sorts keep their old behavior.
