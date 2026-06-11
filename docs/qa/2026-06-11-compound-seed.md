# v1.58.1 Compound Seed QA

## Scope

Small seed for the Sde Dov compound map. This PR does not create project posts and does not change the public map module. It only ensures the CMS relationship exists when `nadlan_feature_compound_map` is enabled:

- term: `nadlan_compound` slug `sde-dov`, name `רובע שדה דב`
- project assignment: existing Rainbow project only
- fallback ID: `4464`, only after confirming the post type is `nadlan_project`

## Expected Live Result

After Claude deploys v1.58.1 and the owner has `nadlan_feature_compound_map=1`, the next admin page load should run the seed once.

Expected healthcheck delta:

```json
{
  "version": "1.58.1",
  "compounds": { "count": 1 },
  "compound_map": { "pins_count": 1 }
}
```

## Gate Mapping

| Gate | Expected behavior | Local proof |
| --- | --- | --- |
| Flag off | `nadlan_compound_seed()` returns before term/project work | code checks `nadlan_feature_compound_map !== '1'` first |
| Idempotent | second run returns once `nadlan_compound_seeded >= NADLAN_COMPOUND_SEED_VERSION` | option gate in `nadlan_compound_seed()` |
| Existing term | if `sde-dov` already exists, it reuses the term ID | `get_term_by('slug','sde-dov','nadlan_compound')` |
| Missing term | creates only the compound term, not a post | `wp_insert_term('רובע שדה דב', 'nadlan_compound', ['slug'=>'sde-dov'])` |
| Existing Rainbow | finds existing project by title/meta markers `Rainbow`, `ריינבו`, `קשת` | `nadlan_compound_seed_find_rainbow_project()` |
| Fallback safety | fallback `4464` is used only if `get_post(4464)->post_type === 'nadlan_project'` | explicit post-type check |
| Do not touch other terms | assignment uses append mode | `wp_set_object_terms($project_id, [$term_id], 'nadlan_compound', true)` |
| Rainbow absent | no assignment and no seed version write | `if ( ! $project_id ) { return; }` before `update_option` |

## Local Checks

PowerShell/static checks to run before PR:

```powershell
git diff --check
Select-String -Path plugins\nadlan-config\inc\compounds.php -Pattern "NADLAN_COMPOUND_SEED_VERSION|nadlan_compound_seeded|wp_insert_term|wp_set_object_terms|admin_init"
tar -tf plugin-dist\nadlan-config-1.58.1.zip | Select-String "\\"
tar -tf plugin-dist\nadlan-config-1.58.1.zip | Select-String "nadlan-config/inc/compounds.php"
```

## Local Limitation

This Windows shell does not have `php`, WSL or Docker available, so `php -l` must run in Claude's deploy gate.
