# Flagship v3 WordPress integration seams

Status: **integrated in the local working tree only**. This document records the two reviewed, surgical shared-file edits used to activate the isolated module. No deployment or public release is authorized.

## Preconditions

- The staged post is a password-protected `nadlan_project`, has the private marker `private-unit-journey-v2`, and points back to canonical post `4867` through `_nadlan_flagship_source_post_id`.
- `project_surface_version` is exactly `flagship-v3`.
- All v3 contract meta validates through `nadlan_flagship_v3_validate_post()`.
- The registry still has `public_release_enabled: false`; therefore post `4867` fails closed.
- The standard authenticated WordPress REST meta route can round-trip the isolated v3 fields registered by `nadlan_flagship_v3_register_meta()`. Anonymous item responses strip every v3/shared `project_model_*` and `project_3d_*` field, catalog/source/privacy markers, body media and featured-media discovery; anonymous REST collection/search excludes the private-stage marker entirely. The custom showroom payload endpoint does not need to own the v3 fields.

## Shared edit 1 — load the module before the showroom engine

File: `plugins/nadlan-config/nadlan-config.php`

In the module list at line 33, insert `flagship-surface` immediately before `showroom-engine`:

```diff
- ..., 'lead-nurture', 'showroom-engine', 'bulk-project-seo', ...
+ ..., 'lead-nurture', 'flagship-surface', 'showroom-engine', 'bulk-project-seo', ...
```

This only defines the generic gates and renderer. The module remains inert unless a post explicitly selects `flagship-v3`.

## Shared edit 2 — dispatch selected posts at both content-composition passes

File: `plugins/nadlan-config/inc/showroom-engine.php`

### Priority-8 composer

Immediately after the password-form early return and before legacy article slicing, select the v3 renderer once. The staged clone contains the new reviewed Hebrew dossier marker `data-nlfs-dossier="nadlan-einstein-he-dossier-v1"`; it must not contain the raw canonical/legacy post 4867 body. Read the staged clone's own raw `post_content` and pass it into the v3 dispatcher. Do not pass `$content`, because earlier project filters may already have prepended a profile/price/H1 surface. Do not call `the_content`, `apply_filters( 'the_content' )`, `do_shortcode`, or dynamic blocks from this branch. The v3 allow-list sanitizer owns the safe static HTML composition.

```diff
	if ( post_password_required( $pid ) ) {
		return $content;
	}
+	$nl_flagship_v3_selected = function_exists( 'nadlan_flagship_v3_is_selected' )
+		&& nadlan_flagship_v3_is_selected( $pid );
+	if ( $nl_flagship_v3_selected ) {
+		$nl_flagship_v3_article = (string) get_post_field( 'post_content', $pid, 'raw' );
+		$nl_flagship_v3_surface = function_exists( 'nadlan_flagship_v3_dispatch' )
+			? nadlan_flagship_v3_dispatch( $pid, $nl_flagship_v3_article )
+			: '';
+		return $nl_flagship_v3_surface;
+	}
```

The module's `template_redirect` guard rejects an invalid selected contract before content rendering. The dispatcher also returns an empty value instead of falling back to the legacy engine if a selected contract is rejected.

### Private-lab final pass

Inside the existing `PHP_INT_MAX` content callback, keep the fresh core password form as the pre-auth body. After that password check, dispatch v3 with the priority-8 result already present in `$content`; if it already contains the v3 main, return it unchanged. This avoids recomposition/recursion and never calls `the_content` or `do_shortcode` from the renderer:

```diff
		if ( post_password_required( $pid ) ) {
			return get_the_password_form( get_post( $pid ) );
		}
+		if ( function_exists( 'nadlan_flagship_v3_is_selected' ) && nadlan_flagship_v3_is_selected( $pid ) ) {
+			if ( false !== strpos( (string) $content, 'data-nl-flagship="v3"' ) ) {
+				return $content;
+			}
+			$nl_flagship_v3_article = (string) get_post_field( 'post_content', $pid, 'raw' );
+			$nl_flagship_v3_surface = function_exists( 'nadlan_flagship_v3_dispatch' )
+				? nadlan_flagship_v3_dispatch( $pid, $nl_flagship_v3_article )
+				: '';
+			return $nl_flagship_v3_surface;
+		}
```

The existing unselected legacy return remains unchanged below this insertion. The v3 branch preserves exactly one **visible** page-level H1 owned by v3, the existing password boundary, and the late private-lab de-stacking behavior. The dossier sanitizer rejects H1/main/script/style/iframe/form/event-handler/showroom-root injection and requires exactly one reviewed dossier marker. Unselected projects keep the current engine unchanged.

## Activation/readback gates

1. Independently review the two shared edits above before any package or deployment step.
2. Build or update a password-protected sandbox clone, never canonical post `4867`.
3. Read back post type, status, password presence, slug, source-post crosswalk, surface version, all JSON contracts, zero units, and the three model URLs.
4. Verify pre-auth: core password form only, `noindex`, `nofollow`, `noarchive`, `no-store`, no project payload or asset enqueue.
5. Verify post-auth: one H1; one global demo label; no `#nl-root`; first-party WebGL2 viewer and same-origin media/GLB only; exactly four top-level playground doors; exact scenes `living`, `bedroom`, `arrival`, `open-frame`; exact GLB anchors `representative-interior-concept`, `facility-arrival-concept`, `facility-landscaped-open-space-concept`; facilities remain selectable inside the Interior experience; owner-authorized illustrative mapping remains distinct from the future verified `source_cited_mapping` lane; body fullscreen and exact Back restoration; no form, endpoint, lead, comment write, or internal delivery terminology.
6. Keep `public_release_enabled` false until the private acceptance evidence is independently reviewed.

## Cleanup/lifecycle

- Removing `project_surface_version` from the staged post immediately returns it to the unselected path.
- Removing the two shared edits fully deactivates the new module without deleting project data.
- `nadlan:flagship-v3:teardown` destroys mounted instances, closes a body-level scene, restores scroll/model/focus, and releases event listeners.
- No cron, option, table, route, form handler, or external storage is created by this seam.
