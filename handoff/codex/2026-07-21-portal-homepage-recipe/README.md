# NadLan Portal Recipe — START HERE

**Status:** review package only — not production
**Date:** 2026-07-21
**Branch:** `agent/portal-homepage-recipe-2026-07-21`
**Source commit:** `f16ca096b67a2e2077c7479c4e2e8ef33819b8eb`
**Public-site changes:** none
**WordPress changes:** none
**Theme/plugin/template changes:** none

## The decision in one sentence

NadLan should feel like a large, long-established Israeli property portal with premium restraint: abundant truthful project photography, familiar search and cards, deep project evidence, visible freshness and ownership, map/compare/save actions, and a first-class foreign-buyer layer — all powered by WordPress as the single source of truth.

## What this package contains

1. [Executive portal recipe](spec/portal-recipe.md)
2. [Competitor side-by-side corpus](research/competitor-corpus.md)
3. [Pattern-frequency matrix](research/pattern-frequency-matrix.csv)
4. [Research sources](research/sources.md)
5. [Homepage specification](spec/homepage-spec.md)
6. [Project-card specification](spec/project-card-spec.md)
7. [Project-page specification](spec/project-page-spec.md)
8. [WordPress content and governance contract](spec/wordpress-content-contract.md)
9. [Asset truth, rights and freshness standard](spec/asset-truth-and-freshness.md)
10. [Foreign-investor and 3D system](spec/foreign-investor-and-3d.md)
11. [Developer marketing plan — Hebrew](spec/developer-marketing-plan-he.md)
12. [Presentation-readiness gate](spec/presentation-readiness.md)
13. [Current repository gap inventory](spec/current-gap-inventory.md)
14. [Decision log](decision-log.md)
15. [Source manifest](source-manifest.md)

For a local, visual table of contents, open [START-HERE.html](START-HERE.html). The five review pages are under `preview/`. They are deliberately separate from the WordPress theme and are **not implementation code**.

## Five views of one canonical product

These are five screens in the same product system, not five disconnected styles:

| View | Question it answers | Review file |
| --- | --- | --- |
| 1. Homepage | Does this immediately feel like a serious, active portal? | [01-home.html](preview/01-home.html) |
| 2. Projects + map | Can a buyer scan, filter and compare inventory confidently? | [02-projects-list-map.html](preview/02-projects-list-map.html) |
| 3. Project page | Is there enough media, evidence and human contact to make a decision? | [03-project-detail.html](preview/03-project-detail.html) |
| 4. Foreign investor | Can an overseas buyer understand costs, process and remote viewing? | [04-foreign-investor.html](preview/04-foreign-investor.html) |
| 5. Developer completion | Can a developer complete and verify the project card without a detached CMS? | [05-developer-studio.html](preview/05-developer-studio.html) |

## Visual review — directly in GitHub

<table>
  <tr>
    <td><strong>Homepage · desktop 1440</strong><br><img src="screenshots/01-home--he--desktop-1440.png" width="520" alt="NadLan homepage review at 1440px"></td>
    <td><strong>Projects + map · desktop 1440</strong><br><img src="screenshots/02-projects-list-map--he--desktop-1440.png" width="520" alt="NadLan projects and map review at 1440px"></td>
  </tr>
  <tr>
    <td><strong>Project page · desktop 1440</strong><br><img src="screenshots/03-project-detail--he--desktop-1440.png" width="520" alt="NadLan project detail review at 1440px"></td>
    <td><strong>Foreign investor · desktop 1440</strong><br><img src="screenshots/04-foreign-investor--en--desktop-1440.png" width="520" alt="NadLan foreign investor review at 1440px"></td>
  </tr>
  <tr>
    <td><strong>Developer Studio · desktop 1440</strong><br><img src="screenshots/05-developer-studio--he--desktop-1440.png" width="520" alt="NadLan developer Studio review at 1440px"></td>
    <td><strong>Homepage + project · mobile 390</strong><br><img src="screenshots/01-home--he--mobile-390.png" width="190" alt="NadLan homepage mobile review at 390px"> <img src="screenshots/03-project-detail--he--mobile-390.png" width="190" alt="NadLan project detail mobile review at 390px"></td>
  </tr>
</table>

All five views also have 390px QA captures. See [the screenshot QA record](screenshots/QA.md).

## What is retained, and what is superseded

### Retained

- Cream, ink and restrained gold palette.
- Frank Ruhl Libre + Heebo for Hebrew; a compatible editorial/sans pairing for English.
- Fine rules, quiet motion, disciplined RTL and strong mobile behavior.
- WordPress block theme, existing CPTs, taxonomies, REST and `nadlan-config` ownership.
- Truthful media states, HE/EN parity, accessible interactions and a source-aware 3D contract.

### Superseded by the owner's new direction

- A sparse editorial homepage with only a few project cards.
- Sketch-led or abstract imagery as the dominant portal experience.
- The earlier rule that the product should never resemble a marketplace/listings portal.
- Long explanations of what the product may become.
- Public demo/test inventory, unsupported counts and stale price claims.

## What the preview media means

Every project-like image in the review pages comes from the repository's existing generated/prototype asset set. It is used only to demonstrate density, hierarchy and crop behavior. It is **not official developer media**, **not proof of availability**, and **not approved for an external sales presentation**.

Before the site is shown to developers or investors, the preview images must be replaced by licensed or developer-approved assets according to [the asset standard](spec/asset-truth-and-freshness.md).

## Owner approval boundary

This package recommends what to build; it does not authorize implementation. No production work should begin until the owner explicitly approves:

- the canonical homepage and card recipe;
- the content fields and freshness policy;
- the asset intake requirement;
- the five-page review direction;
- a separate implementation branch and deployment plan.

## Immediate recommendation

Do not invite external developers or investors into a sparse/demo storefront. First complete a minimum launch cohort of projects with approved hero/gallery media, complete structured facts, verified ownership/source, current availability language, English pages and working contact paths. Then launch outreach around a portal that visibly already works.
