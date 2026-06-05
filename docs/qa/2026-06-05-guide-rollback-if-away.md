# Guide D - If Something Breaks While I Am Away

Use this if the v1.51.0 update causes a problem. Start with the least destructive step.

## Phone-Friendly Check

Open:

```text
https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?cb=<current-time>
```

`[SCREENSHOT: healthcheck on phone]`

Expected: JSON with `"version":"1.51.0"`.

## Normal Rollback If WP Admin Works

1. Open WordPress admin.
   `[SCREENSHOT: wp-admin dashboard]`

2. Go to Plugins -> Installed Plugins.
   `[SCREENSHOT: Installed Plugins page]`

3. Find NadLan Config.
   `[SCREENSHOT: NadLan Config plugin row]`

4. Click Deactivate.
   `[SCREENSHOT: Deactivate link]`

5. Reopen the homepage.
   `[SCREENSHOT: homepage after deactivation]`

6. Tell Claude the exact error and time it happened.
   `[SCREENSHOT: message to Claude with time and symptom]`

## Worst-Case Rollback If WP Admin Is Locked Out

1. Log into the hosting file manager or SFTP.
   `[SCREENSHOT: hosting file manager login]`

2. Open the WordPress files.
   `[SCREENSHOT: WordPress root folder]`

3. Go to:

```text
wp-content/plugins/
```

`[SCREENSHOT: wp-content/plugins folder]`

4. Find:

```text
nadlan-config
```

`[SCREENSHOT: nadlan-config plugin folder]`

5. Rename it to:

```text
nadlan-config-disabled
```

`[SCREENSHOT: renamed folder]`

6. Reload `/wp-admin`.
   `[SCREENSHOT: wp-admin loads again]`

7. Reload the homepage.
   `[SCREENSHOT: homepage loads after plugin disabled]`

8. Tell Claude: "Plugin disabled by folder rename. Need forward rollback."
   `[SCREENSHOT: message to Claude]`

## WP-CLI Rollback If Available

Run:

```bash
wp plugin deactivate nadlan-config
```

`[SCREENSHOT: terminal output showing plugin deactivated]`

## Forward Rollback

WordPress auto-updates normally move forward, not backward. The safest real fix is:

1. Claude creates a new higher plugin version, for example `1.51.1`.
2. The new version reverts or disables the broken feature.
3. Owner clicks Update again in wp-admin.
4. Healthcheck confirms the new version.

## What Counts As Emergency

| Symptom | Emergency? | Action |
|---|---|---|
| `/wp-admin` white screen | Yes | Folder rename rollback. |
| Homepage 500 | Yes | Deactivate plugin if admin works; otherwise folder rename. |
| Healthcheck 404/500 | Yes | Deactivate plugin and report. |
| GI IPN returns 401 | No, unless recurring is live | Fix Morning secret/signature. |
| AI chat says maintenance | No | Fix AI key/provider. |
| `/health` says version 1.50.0 but `/healthcheck` says 1.51.0 | No | Known monitoring bug; ask Claude to patch. |
