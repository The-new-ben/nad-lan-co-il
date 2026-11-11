# Apartment designer, server side: review notes (HAD-701)

11.11.2026. Draft only. Nothing is loaded, released or live. Files:

- `plugins/nadlan-config/inc/designer.php`: the module (switch, cleaner, anonymous save and read, plan resolver, shortcode).
- `docs/design-lab/apartment-designer/server/test_designer_unit.php`: offline test with WordPress stubs. Run:
  `C:/Users/777/tools/php-8.3/php.exe docs/design-lab/apartment-designer/server/test_designer_unit.php`. Result on 11.11.2026: 84 of 84 pass. The sample comes from `spike/dump-design.mjs` (falls back to a hand-built sample when node is missing). `php -l` is clean.

## 1. What the reviewer must check

1. **Switch.** `nadlan_dsg_on()`: option `nadlan_designer_enabled` = `'1'`, or `?designer=next`. The shortcode, both REST routes and the head import map all check it. `?designer=next` is a preview switch, not a security boundary: anyone who learns it can save designs. Is that acceptable during testing? (Each route is built to be safe for an anonymous visitor anyway.)
2. **Cleaner** `nadlan_dsg_clean_design()`: compare every key with `docs/architecture/apartment-designer/design.schema.json`. The input is refused when over 200 KB as UTF-8 JSON, not v2, or with a bad `geometry_revision`; everything else that is bad is dropped or capped (see the test list). Check the caps: items 200, notes 80 (400 characters), log 400 (the newest are kept), finishes 400, walls 400 (±1000 cm), coordinates ±10000 cm rounded to 0.1, rotation brought into [0, 360).
3. **No nonce, and what replaces it** (`nadlan_dsg_write_refusal`): header `X-NL-Designer: 1` (a form cannot send it; a cross-site fetch needs a CORS preflight WordPress does not grant), `Content-Type: application/json`, `Sec-Fetch-Site` same-origin when sent, `Origin` equal to the home host when sent, body at most 256 KB. Check that no CORS plugin or `rest_pre_serve_request` filter on the live site answers preflights with `Access-Control-Allow-Headers: *` for `/nadlan/v1/*`.
4. **Edit key.** `HMAC-SHA256('nadlan-dsg-edit|' . id, wp_salt('auth') . 'nadlan-designer-v2')`, 32 hex characters, compared with `hash_equals`, never stored. Rotating the WordPress salts makes every saved design read-only (reads still work).
5. **Rate limits.** 20 saves an hour and 120 reads a minute per visitor, plus a site-wide ceiling of 3,000 new designs a day (filter `nadlan_dsg_daily_cap`). The visitor is `REMOTE_ADDR`, hashed with HMAC under `wp_salt('nonce')` into the transient name only. **Check on uPress:** if a proxy or CDN sits in front, `REMOTE_ADDR` may be the proxy, which turns the per-visitor limit into a site-wide one. Do not switch to `X-Forwarded-For` without knowing which proxy sets it.
6. **Cache.** Both routes answer `Cache-Control: no-store` and `X-Robots-Tag: noindex`. Check that the host cache (Varnish/XBoost) does not cache `/wp-json/nadlan/v1/designer/*` anyway.
7. **Storage.** Post type `nadlan_design`: not public, not queryable, no UI, no REST of its own, no revisions. `post_status` private, `post_author` 0, `post_name` = the id. The design JSON sits in `post_content`, encoded with `JSON_HEX_*` so the kses filter WordPress applies for anonymous users finds nothing to change. Meta: `_dsg_project`, `_dsg_unit`, `_dsg_georev`, `_dsg_saves`, `_dsg_seen` (a day, not a time).
8. **Cron** `nadlan_dsg_cleanup`, daily: deletes designs whose `_dsg_seen` is older than 180 days, 200 a run. It is scheduled on `init` whether the switch is on or off, so the retention promise holds after the switch is turned off. (Deactivation does not unschedule it; the plugin has no deactivation hook for the other crons either.)
9. **Import map.** Printed only when the page has none from the stage (`nadlan_ps_current()` true means `inc/project-stage.php` printed `#nadlan-ps-importmap`). Preferred place: `wp_head` priority 30 on a singular page whose content has the shortcode. Fallback: the shortcode prints it in the body before its module script, once per page.
10. **Shortcode.** Without a project it shows the example flat (it labels itself "דירה לדוגמה"). With a project it shows only that project's indexed plan for that exact type, otherwise nothing (an HTML comment). All config from the filter is cleaned again; the JSON is printed with `JSON_HEX_TAG` so no value can close the script.
11. **Send button.** Today: anonymous save, the share link goes into the address bar and the clipboard and is shown in `designer.toast`. Filter `nadlan_dsg_send_handler` (marked in the code) may name a global JS function, for example `NadlanLead.sendDesign`, called with `(designer, receipt)` after the save. **No lead is created here.** Connecting to `/nadlan/v1/lead` then `/nadlan/v1/rfp` is a later, reviewed step, and `nadlan_rfp_clean_design` must learn v2 first (ARCHITECTURE section 6).

## 2. Loading the module: the one change in `nadlan-config.php`

Not applied. In the `foreach ( array( 'catalog-meta', 'project-mode', ... ) as $nadlan_mod )` module list near the top of `nadlan-config.php`, add the string `'designer'` as the last element, right after `'cta-sheet'`:

```
... 'pro-card', 'cta-sheet', 'designer' ) as $nadlan_mod ) {
```

The repo copy of `nadlan-config.php` is not the live text: the release must apply this as a hunk on the live file (read it through the bridge first), never by uploading the repo copy. The module also needs the asset folder `assets/designer/` live (designer.js, core.js, plan.js, space.js, catalog.js, strings.js, budget.js, designer.css, data/, plans/, models/).

## 3. Plans index (not created)

`assets/designer/plans/index.json` does not exist yet, so `nadlan_dsg_plan_url()` returns `''` for every project. Format:

```json
{ "plans": { "ashira": { "A4": "ashira-a4.json", "B5": "ashira-b5.json" } } }
```

Keys: project slug (`[a-z0-9-]`), unit type (`[A-Za-z0-9_-]`, exact match, case kept). Values: a plain file name in the same folder ending in `.json`; anything with a slash or `..`, or a file that does not exist, resolves to `''`. The parsed index is cached in a transient whose name carries the file's mtime and size.

## 4. What the client sends, and the share link

**Save** (`designer.js` needs no change; the shortcode's inline module does this):

```
POST /wp-json/nadlan/v1/designer/save[?designer=next]
Content-Type: application/json
X-NL-Designer: 1
credentials: omit

{ "design": <designer.getDesign()> }                                     -> 201 { ok, id, key, rev: 1 }
{ "design": ..., "id": "<id>", "key": "<key>", "base_rev": <rev> }       -> 200 { ok, id, rev }
```

Errors: 403 `header` / `json` / `site` / `origin` / `key`, 404 `gone` or `off`, 409 `other_unit` (project, unit or plan revision differ from the saved one) or `stale` (`base_rev` is not the server's save count, e.g. a second tab), 413 `size` / `design_size`, 422 `design_version` / `design_revision`, 429 `rate`. On 403, 404 or 409 for an update the inline module saves a new copy instead (new id).

**Read**: `GET /wp-json/nadlan/v1/designer/design/<id>` -> `{ design, project, unit_id, geometry_revision, saved, rev }`. The edit key is never returned.

**Share link**: the page that hosts the designer, plus `?design=<id>` (26 characters, a-z and 2-7). No new URL, no new slug. Example: `https://nad-lan.co.il/projects/ashira/?design=k3v7...`. On load the inline module reads the design, uses it only when its project matches the page and its `geometry_revision` matches the plan, else opens a fresh design. Whoever holds the link can read the design; only the browser that created it (edit key in `localStorage` key `nl-dsg-keys`, 20 newest) can update it; everyone else saving makes a copy.

Note for the client: the module URL carries `?v=<plugin version>`, but designer.js imports `./core.js` and the rest without a version, so those files are cached by their bare URLs. A release that changes core.js should also bump something designer.js imports, or add versions inside designer.js.

## 5. Data kept, and for how long (text for the privacy page)

Hebrew:

> **שמירת עיצוב דירה.** כשאתם שומרים עיצוב בכלי "מעצבים את הדירה" אנחנו שומרים רק את העיצוב עצמו: מיקום הרהיטים, הריצוף, הזזת מחיצות, ההערות שכתבתם ורשימת השינויים, יחד עם שם הפרויקט, מספר הדירה וגרסת התוכנית. אנחנו לא שומרים שם, טלפון, דוא״ל או כתובת IP. ברשימת השינויים מופיע רק התפקיד (רוכש, נציג, מעצב, משפחה), לא שם של אדם. כל מי שמחזיק בקישור לעיצוב יכול לצפות בו; רק הדפדפן ששמר אותו יכול לשנות אותו. עיצוב שלא נפתח 180 יום נמחק אוטומטית. לבקשת מחיקה מוקדמת: info@nad-lan.co.il, עם הקישור לעיצוב.

English:

> **Saved apartment designs.** When you save a design we keep only the design itself (furniture positions, flooring, moved partitions, your notes and the list of changes) with the project name, the unit number and the plan version. We do not keep a name, phone number, email or IP address. The list of changes records a role (buyer, representative, designer, family), never a person's name. Anyone holding the link can view the design; only the browser that saved it can change it. A design not opened for 180 days is deleted automatically. To delete one sooner, write to info@nad-lan.co.il with the link.

Technical detail behind the text: the IP address is used only to count requests, as a salted hash inside a temporary counter that expires within an hour; the "last opened" date is kept to the day. Free text in notes can still hold whatever a visitor types (a name or phone number written into a note); the cleaner strips tags, not meaning. The edit key in the visitor's own browser storage is not personal data.

## 6. Decisions a reviewer may disagree with

- An unknown author in `log[].by` or `notes[].by` becomes `buyer` (the core's own default) rather than dropping the line.
- A project with no indexed plan shows nothing rather than the example flat.
- An update may not change project, unit or plan revision (409); the client then saves a copy.
- `item.status` that is not in the enum is dropped (the key), not replaced by `decor`.
- The log keeps the newest 400 lines, not the first 400.
- The edit key is kept in `localStorage` so a visitor can return and keep editing (ARCHITECTURE says no personal details in `localStorage`; the key is not one).
- Project ids are ascii only (`[a-z0-9-]`); a project whose slug is percent-encoded Hebrew cannot carry a design.
- `?designer=next` also opens the REST routes, so the owner can test the whole loop before the option is set.

## 7. Open questions

1. Does uPress put a proxy in front, so that `REMOTE_ADDR` is not the visitor? (Decides whether the per-visitor limits work.)
2. Is `/wp-json/` excluded from the host cache for these routes?
3. Older Safari: a second import map in the body is ignored after any module has loaded. Pages that use WordPress script modules (the core prints `#wp-importmap`) could end up without `three`. The head hook covers singular pages with the shortcode; the Kikar cockpit sheet that opens the designer on tap must make sure the map is in the head (the stage page already does).
4. Who answers a deletion request by link (`info@nad-lan.co.il`), and is there an admin tool to find a design by id? (`show_ui` is off on purpose.)
5. Which pages host the designer first, and with which project and type (the Ashira types are the only real plans; none is in `plans/` yet)?
6. When the services layer arrives, `points[]` joins the design document: `nadlan_dsg_clean_points()` is ready and tested but not called, and design.schema.json has no `points` yet.
