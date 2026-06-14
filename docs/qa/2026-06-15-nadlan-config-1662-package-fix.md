# NadLan Config 1.66.2 package-path hotfix QA

## Why this patch exists

Live WordPress admin showed `NadLan Config` active at `1.65.6` while GitHub main and the update manifest already advertised `1.66.1`.

During the deploy audit, the `1.66.1` ZIP downloaded from the raw GitHub manifest was found to contain Windows backslash archive paths such as:

```text
nadlan-config\nadlan-config.php
```

That is unsafe for the Linux WordPress updater. This release does not change showroom behavior. It rebuilds the package as `1.66.2` with forward-slash ZIP paths and aligns every version surface.

## Local checks

```text
manifest_version=1.66.2
download_url=https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/plugin-dist/nadlan-config-1.66.2.zip
ZIP entries=130
ZIP backslash_count=0
ZIP root_count=130
ZIP marker Version: 1.66.2=True
ZIP marker healthcheck version=True
node --check scripts/qa-project-showroom-visual.mjs passed
git diff --check passed with only normal Windows CRLF warnings
```

PHP lint was not run locally because this Windows shell has no `php` binary.

## Live deploy gate

After merge:

1. Pull/sync the UPress server Git copy.
2. Update `NadLan Config` in WordPress to `1.66.2`.
3. Clear UPress cache.
4. Verify `https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck` returns `version: 1.66.2`.
5. Hard-refresh `https://nad-lan.co.il/projects/rainbow-tel-aviv/` and verify the page contains `nlp3d`, `is-dual-showroom`, and visible apartment cells.

