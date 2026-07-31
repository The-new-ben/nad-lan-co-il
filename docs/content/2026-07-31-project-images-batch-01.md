# Project images — Batch 01 (the 10 worst offender cards)

Source batch: Google Drive `NadLan-Projects-Batch-01-10-Worst-2026-07-31`
(`00-BATCH-MANIFEST-HE.md`, `00-GALLERY-MAP.csv`, `00-RESEARCH-SOURCES.md`).
Wired into the site by `inc/project-image-batch.php` on 2026-07-31.

## The bug this batch fixes

An audit of the first **144 archive cards** found **77 of them** showing one of
just three generic images:

| Generic file | Occurrences |
|---|---|
| `architectural-model.jpg` | 26 |
| `sea-view-interior.jpg` | 26 |
| `tel-aviv-coast-skyline.jpg` | 25 |

Cause: `plugins/nadlan-config/inc/directory.php` (~line 713) rotates five theme
images by `post_id % 5` whenever a project has no featured image and no
`photos_csv`. Across all ten batch projects, `featured_media = 0` and
`project_model_poster` was empty, so every one of them fell through to the
rotation. The result is a Haifa project illustrated with a Tel Aviv coastline,
and a Be'er Sheva project illustrated with a sea-view interior.

## How it is wired (no wp-admin work needed)

20 images (`*-photo.webp` + `*-sketch.webp`, 1440x1080, sRGB) live in
`assets/projects/batch-01/`. A single `get_post_metadata` filter in
`inc/project-image-batch.php` supplies `photos_csv` and `project_model_poster`
for these 10 post IDs, which every consumer already reads. Deploys with the
normal theme git pull.

Non-destructive by design: a real featured image wins (both consumers check
`has_post_thumbnail()` first), and a real stored meta value wins (checked in the
filter). The batch image only fills a gap and steps aside when real developer
material arrives.

## Provenance — read before treating these as developer material

These are **concept visualisations produced for NadLan from planning data**.
They are not photographs of a built building and not official developer
material. Badge text on the sketch variants is limited to figures verified
against a planning, municipal, or developer source; where a figure was
uncertain it was left off the image entirely.

| # | Project | City | WP ID | Basis | Confidence |
|---|---|---|---|---|---|
| 1 | הגנה/סלוודור | חיפה | 5591 | plan `304-1391424`, Kiryat Eliezer compound 21a | medium-high |
| 2 | אחד העם 33-35 | נהריה | 5590 | plan `210-1229053` | medium-high |
| 3 | מעלה געתון | נהריה | 5588 | plan `210-1214170` | medium (heights unverified) |
| 4 | ביאליק–שמעוני | באר שבע | 5586 | plan `605-1354968` | high |
| 5 | בן צבי | רמלה | 5585 | plan `415-1231919`, 2026 iteration | high (see conflict) |
| 6 | העצמאות | קריית ביאליק | 5583 | plan `352-1525575` + Aura project page | high (see conflict) |
| 7 | לב העיר – סוקולוב | רמת השרון | 3556 | plan `553-0849612`, approved | very high |
| 8 | שבטי ישראל 30-34 | חיפה | 3551 | plan `304-1455583` | medium-high (masses may change) |
| 9 | מתחם ריינס | ירושלים | 3545 | plan-based | medium-high |
| 10 | מתחם ירושלים | נס ציונה | 3543 | general concept | medium (see conflict) |

## Data conflicts — do NOT publish these numbers until resolved

1. **העצמאות, קריית ביאליק (5583).** The site record says **603 units**. Aura's
   current project page says **1,728 units, 9 towers, 30 floors**. The NadLan
   record is inconsistent with the developer's own material and needs
   correcting. No unit-count badge was placed on this image.
2. **מתחם ירושלים, נס ציונה (3543).** Site record **286 units**; current planning
   material **299**. Number deliberately kept off the image.
3. **בן צבי, רמלה (5585).** 2025 municipal material showed ~**1,370 units**; the
   2026 iteration shows **1,706**. The image follows the 2026 iteration and is
   marked as a concept visualisation.

## Still open (not fixed by this batch)

- **Hagana/Salvador (5591) public hero renders `<img>` with no `src`** at a
  natural size of 0x0. Separate template bug; this batch fixes the card image,
  not that hero.
- **Same page shows the template string "רובע שדה דב · מול הים"** although the
  project is in Haifa. The Sde Dov strings in the repo live in the Ashira and
  Dimri patterns, where they are correct, so this page appears to be pulling a
  pattern it should not. Needs investigation rather than a blind string edit.
- **67 more affected cards.** This batch covers 10 of the ~77 found in the first
  144 cards. The same wiring accepts more entries: drop the images into
  `assets/projects/batch-01/` (or a batch-02 folder) and extend the map.
