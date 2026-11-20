# Slice 1 hunks in existing files (not applied to the real files)

Each hunk is one old line that occurs exactly once in the file, and its replacement. The old text is a single line on purpose (the plugin files here have line endings as in the base file); a new text of several lines takes the line ending of the file it goes into. Checked and applied to LAB copies only by `python scripts/rentals/apply_hunks_lab.py` (copies in `docs/design-lab/rentals/slice1-patched/`, syntax-checked with `php -l` and `node --check`).

## 1. `plugins/nadlan-config/inc/rentals/page.php`: load the new scripts and the style

old (1 occurrence):
```
		foreach ( array( 'views', 'drawers', 'lease', 'import', 'portal', 'boot' ) as $f ) {
```
new:
```
		foreach ( array( 'views', 'drawers', 'lease', 'import', 'portal', 'plan2d', 'today', 'boot' ) as $f ) {
```

## 2. `plugins/nadlan-config/inc/rentals/page.php`: the style and the two faces

old (1 occurrence):
```
		wp_enqueue_style( 'nlrm', NLRM_URL_ASSETS . 'rm.css', array(), $v );
```
new:
```
		wp_enqueue_style( 'nlrm', NLRM_URL_ASSETS . 'rm.css', array(), $v );
		wp_enqueue_style( 'nlrm-plex', 'https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap', array(), null );
		wp_enqueue_style( 'nlrm-today', NLRM_URL_ASSETS . 'rm-today.css', array( 'nlrm' ), $v );
```

## 3. `plugins/nadlan-config/inc/rentals/page.php`: the setting (administrators only in the first release; the old today view stays reachable)

old (1 occurrence):
```
			'assets' => NLRM_URL_ASSETS, 'ver' => defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '',
```
new:
```
			'assets' => NLRM_URL_ASSETS, 'ver' => defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '',
			/* the new landing screen: on by default for administrators only (option nadlan_rentals_today2, default '1'); pilot landlords keep the old today view until it has been pressed live (option nadlan_rentals_today2_pilot, default '0'); also #/today-classic, ?today=classic */
			'today2' => current_user_can( 'manage_options' ) ? '0' !== (string) get_option( 'nadlan_rentals_today2', '1' ) : '1' === (string) get_option( 'nadlan_rentals_today2_pilot', '0' ),
```

## 4. `plugins/nadlan-config/inc/rentals-manager.php`: include the new server file

old (1 occurrence):
```
foreach ( array( 'store', 'money', 'billing', 'rest', 'portal', 'lease', 'legacy', 'page' ) as $nlrm_part ) {
```
new:
```
foreach ( array( 'store', 'money', 'billing', 'rest', 'today', 'portal', 'lease', 'legacy', 'page' ) as $nlrm_part ) {
```

## 5. `plugins/nadlan-config/assets/rentals/rm-boot.js`: mount the Today layer in the landlord's app

old (1 occurrence):
```
		base.adapter = adapter;
```
new:
```
		base.adapter = adapter;
		if (N.mountToday) { N.mountToday(root, { rest: cfg.rest, nonce: cfg.nonce, urls: cfg.urls, today2: cfg.today2 }); }
```

## Not a hunk, but to do at release
- Merge `strings-he.json` / `strings-en.json` (keys `t2_*` and `ev_index_confirmed`, 128 each) into the `ui` tables of `assets/rentals/i18n/he.json` and `en.json` as they are on the live server (the main checkout holds the 1.72.720 copies; do not overwrite them with the worktree ones).
- The lab page (`docs/design-lab/rentals/app.html`) makes the same `mountToday` call itself and merges the two string files in the browser.
