# NadLan Source-of-Truth + Anti-Cannibalization System

Status: recommendation after current web/plugin review, 2026-06-21.

## Core decision

Do not rely on a normal WordPress editorial plugin as the only source of truth.

Use a two-layer system:

1. `01_Master` keyword registry is the authority.
2. WordPress admin enforces the registry before content can be written, reviewed, or published.

The “Bible” is not a folder of documents. It is a structured registry with required fields, ownership rules, statuses, and publish gates.

## Why this matters

Keyword cannibalization happens when multiple pages target the same or very similar keywords. Yoast describes the problem as pages competing with each other and making it harder for search engines to decide which URL should rank.

For NadLan, this is a money risk. A weak article can accidentally compete with:

- a city money page;
- a neighborhood money page;
- a project page;
- a professional directory page;
- a calculator/tool page;
- an international investor landing page.

## Recommended architecture

### Layer 1: master registry

Keep the master registry in the strategy workbook and CSV:

- `strategy/04-keyword-master-universe.csv`
- `strategy/lovable/nadlan-lovable-keyword-workbook.xlsx`
- sheet: `01_Master`

Required fields to add in the next workbook version:

- `keyword_id`
- `primary_keyword`
- `keyword_or_pattern`
- `language`
- `cluster`
- `coverage_class`
- `page_role`
- `canonical_url_owner`
- `parent_hub`
- `support_role`
- `money_or_support`
- `readiness_status`
- `legal_gate`
- `official_source_gate`
- `asset_gate`
- `cannibalization_owner`
- `allowed_support_pages`
- `internal_link_rule`
- `writer`
- `reviewer`
- `last_reviewed`
- `source_urls`
- `do_not_write_without_owner_approval`

Statuses:

- `backlog`
- `drafting`
- `review`
- `legal`
- `ready`
- `published`
- `holding`

### Layer 2: WordPress admin enforcement

Create a private WordPress admin area called `Keyword Registry` or `Content Bible`.

Implementation options:

1. Custom post type: `keyword_registry`
2. ACF/Secure Custom Fields fields for all required registry fields.
3. Admin Columns Pro to show, sort, filter, bulk edit, and export the important registry fields in wp-admin.
4. PublishPress Planner for calendar, Kanban, notifications, and workflow.
5. PublishPress Statuses/Capabilities for custom editorial statuses and role control.
6. Optional WP Project Manager only for implementation tasks and milestones, not as the SEO source of truth.

## Publish gate

No page/post/project/professional profile should be published unless:

1. It has a `keyword_id`.
2. It has exactly one `primary_keyword`.
3. It has a `canonical_url_owner`.
4. The canonical owner is not already assigned to another published page unless this page is a support page.
5. The `page_role` is defined: money, support, trust, data, directory, tool, local, project, or AEO.
6. If `legal_gate = required`, status cannot move past `legal` without approval.
7. If `official_source_gate = required`, at least one source URL must be attached.
8. If `asset_gate = required`, asset status must be official/licensed or the page must clearly label concept/missing state.
9. The internal-link rule points support pages to the money page, not the other way around.

## Recommended plugin stack

### PublishPress Planner

Use for editorial workflow:

- content calendar;
- Kanban board;
- editorial notifications;
- team collaboration.

Why: it is WordPress-native and designed for planning/scheduling content.

Source:
https://publishpress.com/planner/

### PublishPress Statuses + Capabilities

Use for custom workflow states and permissions:

- backlog;
- drafting;
- review;
- legal;
- ready;
- holding;
- published.

Source:
https://publishpress.com/knowledge-base/statuses-calendar/

### ACF / Secure Custom Fields

Use for structured registry fields inside WordPress edit screens.

Source:
https://www.advancedcustomfields.com/

### Admin Columns Pro

Use to make the registry visible and operational in wp-admin:

- show canonical URL owner;
- filter by cluster/status/gate;
- sort by priority;
- bulk edit status;
- export for review.

Source:
https://www.admincolumns.com/advanced-custom-fields/

### WP Project Manager

Use only for delivery tasks:

- implementation milestones;
- assignments;
- Kanban/Gantt;
- task reporting.

Do not use it as the SEO Bible.

Source:
https://wordpress.org/plugins/wedevs-project-manager/

## What not to do

- Do not let writers choose keywords freely.
- Do not create blog posts from AI prompts unless the keyword registry row already exists.
- Do not let Rank Math, Yoast, or SEOPress focus keywords become the source of truth. They are page-level SEO tools, not the content strategy registry.
- Do not rely on canonical tags alone to solve bad architecture. Canonical tags help, but the real control is page ownership before publishing.
- Do not put the Bible only in GitHub if the owner and writers cannot inspect it easily.

## Practical next implementation

1. Keep the current Excel workbook as the first master.
2. Add the missing governance columns listed above.
3. Add a private `keyword_registry` custom post type in WordPress.
4. Add ACF fields matching the workbook columns.
5. Add Admin Columns views for `P0`, `legal`, `official source required`, `asset required`, `holding`, and `published`.
6. Add PublishPress Planner statuses and notifications.
7. Add a small custom publish gate:
   - block publish if no `keyword_id`;
   - warn if another page owns the same primary keyword;
   - block if legal/source/asset gates are unresolved.
8. Import the 225 recovered Report 2 rows.
9. Import the expansion backlog as patterns, not final pages.
10. No public content assignment starts outside this system.

## Owner rule

If a page can make money or support a money page, it belongs in the registry.

If it is competitive, we stage it.

We do not delete it.
