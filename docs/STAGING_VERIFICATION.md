# NadLan Staging Verification

Last updated: 2026-05-27 Asia/Jerusalem

## Scope

- Site: `nad-lan.co.il`
- Staging: `nad-lan-co-il-rev.s1240.upress.link`
- Production status: untouched
- Theme deployed on staging: `nadlan-revenue`
- Active staging theme: `NadLan Revenue`

## References

- uPress staging/import workflow: https://support.upress.co.il/dev/import-to-sandbox/
- uPress File Manager Git workflow: https://support.upress.io/advanced/manage-git-via-file-manager/

## What Was Done

1. Created a uPress staging environment from the live site manager.
2. Imported live `nad-lan.co.il` content and database into the staging environment.
3. Deployed the code-first theme files into `/wp-content/themes/nadlan-revenue` through uPress File Manager editor:
   - `style.css`
   - `functions.php`
   - `front-page.php`
   - `header.php`
   - `footer.php`
   - `index.php`
   - `theme.json`
4. Created a staging-only WordPress admin user for operational checks. The password is stored DPAPI-encrypted outside the repo under `.codex-secrets/wordpress-staging-logins/`.
5. Activated `NadLan Revenue` on the staging WordPress admin.
6. Submitted an internal lead test from the staging front page.
7. Verified the private CRM custom post type list in WordPress admin.

## Verification Evidence

- Front page renders the Hebrew real-estate funnel on staging.
- Lead form submission redirected to `/?lead=received`.
- CRM list `NadLan Leads` contains the internal staging test:
  - Title: `בדיקת Codex סטייג׳ינג – בדיקה משפטית – 2026-05-26 23:46`
  - Phone: `050-000-0000`
  - Goal: `בדיקה משפטית`
  - City: `תל אביב`
  - Status: `New`

## Current Blocker

uPress File Manager Git can clone/pull from a Git URL, but the portfolio repos are private. Do not embed a personal GitHub token in a uPress clone URL until the deploy credential path is approved.

Decision needed before production Git sync:

- Create a public deploy mirror for theme-only code.
- Use a scoped read-only GitHub token in the uPress Git URL.
- Approve another secure credential path.

Until that is resolved, production should remain untouched and staging changes should be treated as the verified preview.
