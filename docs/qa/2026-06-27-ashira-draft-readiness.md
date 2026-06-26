# Ashira V2 WordPress Draft Readiness

Date: 2026-06-27
Branch: `codex/ashira-showroom-v2-clean`

## Scope

This slice proves that the clean Ashira v2 theme pattern can become a safe WordPress REST draft
payload before anyone imports it into the live CMS.

It does not contact WordPress, publish a page, deploy a plugin, or update production.

## Commands

Build the draft payload:

```powershell
node scripts\build-project-showroom-draft.mjs --pattern patterns\project-showroom-ashira-v2.php --slug ashira-sde-dov --title "דירות למכירה באשירה שדה דב" --yoast-title "דירות למכירה באשירה שדה דב | בחירת דירה, נוף ואומדן" --yoast-description "אשירה שדה דב: בדקו דירות לפי קומה, חדרים, שטח, נוף וזמינות, עם מודל תלת ממד, חזית לבחירת דירה ואומדן לא מחייב עד אימות מול היזם." --focus-keyword "דירות למכירה באשירה שדה דב" --out docs\wp-drafts\ashira-sde-dov-v2-draft.json
```

Validate the draft payload:

```powershell
npm run qa:ashira-draft-readiness
```

Dry-run the WordPress apply wrapper:

```powershell
node scripts\apply-wp-draft-payload.mjs --payload docs\wp-drafts\ashira-sde-dov-v2-draft.json --dry-run
```

## Gate Results

| Check | Result |
|---|---|
| Draft status | PASS, `draft` |
| Endpoint | PASS, NadLan WordPress REST project endpoint |
| Slug | PASS, `ashira-sde-dov` |
| Supported showroom root | PASS, `data-nlv2-showroom` |
| One H1 | PASS |
| Clickable unit cells | PASS, `5` |
| Payload unit sync | PASS, draft units `5`, payload units `5`, missing `0` |
| Visible buyer copy | PASS |
| Yoast title/description buyer copy | PASS |
| Mojibake | PASS, none |
| Internal wording in visible copy | PASS, none |
| Apply wrapper dry-run | PASS |

Machine report:

`docs/qa/ashira-v2-draft-readiness-report.json`

## Buyer-Language Boundary

The public title and Yoast metadata now speak to the buyer:

- title: `דירות למכירה באשירה שדה דב`
- SEO title: `דירות למכירה באשירה שדה דב | בחירת דירה, נוף ואומדן`
- meta description: apartment choice, floor, rooms, sqm, view, availability, 3D model, facade picker
  and non-binding estimate.

No public wording describes our CMS, SEO process, factory, build system or lead-routing logic.

## Honest Limits

This is still only a draft payload proof. It is ready for a controlled import attempt later, after
the owner approves the source material and the live workflow is deliberately opened.
