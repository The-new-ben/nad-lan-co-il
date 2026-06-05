# Chunk F QA - Contextual Help Framework

Branch: `codex/chunk-f-contextual-help`
Version: `1.56.0`
Feature flag: `nadlan_feature_help` default `0`

## Scope

Chunk F adds a dark-launched in-app contextual help framework for Nadlan admin screens. The framework is intentionally admin-only and reusable:

- One PHP string store keyed by screen and field, filterable through `nadlan_help_strings`.
- Accessible field tooltips with `aria-describedby`, focusable trigger buttons, and tooltip elements using `role="tooltip"`.
- WP pointer tours using the native `wp.pointer` API and `dismissed_wp_pointers` user meta.
- Per-screen contextual help tabs through `get_current_screen()->add_help_tab()`.
- Reusable empty-state helper `nadlan_help_empty_state()`.
- Healthcheck block `help`.

## Acceptance Gate

| Gate | Expected result | Local proof |
| --- | --- | --- |
| G1 flag OFF | With `nadlan_feature_help` unset or `0`, no help UI, no scripts/styles, no pointers, and existing admin behavior remains unchanged. | `nadlan_help_enabled()` checks only the option and all render/enqueue/helper paths early-return when false. |
| G2 tooltips | With flag ON, targeted fields render focusable `?` triggers, `aria-describedby`, tooltip spans with `role="tooltip"`, hover/focus display, and Escape dismissal. | `inc/contextual-help.php` contains `aria-describedby`, `role="tooltip"`, `mouseenter focus click`, and Escape key handling. |
| G3 pointer dismiss | Pointer IDs are prefixed `nadlan_`; dismiss posts through nonce-protected AJAX and persists in `dismissed_wp_pointers`. | `wp_ajax_nadlan_help_dismiss_pointer`, `check_ajax_referer('nadlan_help_dismiss')`, `update_user_meta(..., 'dismissed_wp_pointers', ...)`. |
| G4 help tabs | Every string-store screen can receive an admin help tab from store HTML. | `current_screen` hook calls `$screen->add_help_tab()` with content built from `help_tab_html` entries. |
| G5 empty states | Empty list surfaces can render status, cue, and action button. | `nadlan_help_empty_state()` is wired into the lead inbox, admin-control card list, and admin-control audit list. |
| G6 Hebrew/RTL | Strings are Hebrew, wrappers use `dir="rtl"`, and helper font size is at least 14px with readable line-height. | CSS uses 14px/16px text and `nadlan_help_empty_state()` wraps output in `dir="rtl"`. |
| G7 security/perf | Assets load only on opted-in Nadlan admin screens when flag ON; AJAX dismiss uses nonce and logged-in user. | `admin_enqueue_scripts` checks `nadlan_help_enabled()` and `nadlan_help_screen_entries($screen_id)` before enqueue. |
| G8 package/version | Version, manifest, healthcheck, and ZIP align at `1.56.0`; ZIP is rootless and uses forward-slash paths. | See package verification commands below. |

## Local Commands

```powershell
git diff --check
```

```powershell
@'
import json, zipfile, pathlib
manifest = json.loads(pathlib.Path("plugin-dist/nadlan-config.json").read_text(encoding="utf-8"))
assert manifest["version"] == "1.56.0"
with zipfile.ZipFile("plugin-dist/nadlan-config-1.56.0.zip") as z:
    names = z.namelist()
    assert names
    assert all(n.startswith("nadlan-config/") for n in names)
    assert not any("\\" in n for n in names)
    assert "nadlan-config/inc/contextual-help.php" in names
print("manifest+zip ok", len(names))
'@ | python -
```

```powershell
@'
from pathlib import Path
p = Path("plugins/nadlan-config/inc/contextual-help.php")
s = p.read_text(encoding="utf-8")
for marker in [
    "nadlan_feature_help",
    "aria-describedby",
    "role=\"tooltip\"",
    "dismissed_wp_pointers",
    "add_help_tab",
    "nadlan_help_empty_state",
    "nadlan_config_healthcheck",
]:
    print(marker, s.count(marker))
assert "title=" not in s
'@ | python -
```

## PHP Lint

Local limitation: this Windows shell does not have `php`, WSL, or Docker available. Claude's deploy gate must run:

```bash
find plugins/nadlan-config -name '*.php' -print0 | xargs -0 -n1 php -l
```

Expected result: clean lint on `inc/contextual-help.php`, `inc/admin-control.php`, `inc/lead-inbox.php`, `inc/health.php`, and `nadlan-config.php`.

## Manual Browser Checks For Claude

1. Set `nadlan_feature_help=0`, open each Nadlan admin page, and confirm no `nadlan-contextual-help` style/script handles are enqueued.
2. Set `nadlan_feature_help=1`, open `settings_page_nadlan-lead-e2e`, and inspect one tooltip trigger:
   - trigger is a button
   - has `aria-describedby`
   - matching span has `role="tooltip"`
   - hover/focus shows it
   - Escape hides it
3. Dismiss a pointer and confirm the pointer ID is added once to `dismissed_wp_pointers`.
4. Open the Help tab and confirm content comes from `nadlan_help_strings`.
5. Empty a tested list surface in a sandbox and confirm `nadlan_help_empty_state()` emits status, cue, and a button.
