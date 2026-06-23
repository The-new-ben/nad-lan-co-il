# Admin War Room Execution Packet

Date: 2026-06-23

Status: build-ready specification, not an implemented WordPress admin feature.

## Purpose

This packet closes the next governance gap in the war room: the owner needs one controlled place that prevents keyword cannibalization, tracks page ownership, keeps screenshots and evidence visible, and gives future agents a repeatable system.

The recommendation is not to install a generic project-management plugin and call it done. The system needs two layers:

1. Repository layer: current source of truth while fields and decisions are still changing.
2. WordPress admin layer: controlled registry/dashboard after the fields are stable enough to enforce.

## Core Decision

Build a private WordPress registry around keyword and page ownership. The registry should not be public. It should appear in the admin, support revisions, have controlled permissions, and connect to the page/content workflow.

The registry should hold:

- canonical keyword owner
- URL owner
- page template
- funnel role
- language
- current workflow state
- writer gate
- source gate
- legal gate
- asset truth gate
- internal-link targets
- screenshot evidence
- last review date
- owner notes

## Why Not A Generic Task Board

A task board can track work, but it cannot safely decide which page owns a money keyword. If a writer sees only a task such as "write about apartments in Tel Aviv", they can still create a page that cannibalizes the actual money page.

The registry must be the authority. A project-management plugin can sit beside it for delivery tasks, milestones, Kanban boards, and assignments, but every task must link back to the registry row and page id.

## WordPress Implementation Shape

### Private Registry

Use a private admin content type such as `ndl_keyword_registry`.

Required behavior:

- visible in WordPress admin
- not indexed
- no public archive
- no public single page
- revisions enabled
- controlled capabilities
- stable row ids
- CSV import/export
- REST only if needed for admin tooling

WordPress supports custom post types and built-in features such as custom fields, post statuses, revisions, and admin UI controls. See the official `register_post_type()` reference: https://developer.wordpress.org/reference/functions/register_post_type/

### Fields

Use registered meta or ACF field groups. Each field must have sanitization and permission handling. The official WordPress `register_meta()` reference includes `sanitize_callback`, `auth_callback`, and `show_in_rest`: https://developer.wordpress.org/reference/functions/register_meta/

ACF is also suitable for an editor-friendly registry because it adds custom content fields to WordPress edit screens: https://www.advancedcustomfields.com/resources/

### Admin Table

The registry needs filtered list views:

- money pages
- city hubs
- project pages
- professional pages
- foreign investor pages
- guides
- missing pages
- stale pages
- blocked pages

Admin Columns Pro can expose ACF fields in list tables with filtering, sorting, inline edit, bulk edit, and export support: https://www.admincolumns.com/advanced-custom-fields/

### Workflow

Use custom statuses for:

- idea
- assigned
- writing
- source check
- legal check
- asset check
- owner review
- ready to build
- published
- refresh needed
- blocked

PublishPress Statuses supports custom statuses and integrates with Planner calendar views: https://wordpress.org/plugins/publishpress-statuses/

PublishPress Planner can provide calendar and overview screens for planned and published content: https://publishpress.com/planner/

### Delivery Tasks

WP Project Manager can help with Kanban, milestones, Gantt-style planning, and task reporting: https://wordpress.org/plugins/wedevs-project-manager/

Use it only for execution delivery. Do not use it as the canonical keyword registry.

## Publish Gate

Before a money page, project, listing, guide, or professional page is published, the admin should validate:

- keyword owner exists
- URL owner exists
- no competing canonical page exists
- source notes exist
- legal gate is completed where relevant
- asset truth is completed
- internal links are defined
- required screenshots are attached or linked

If the page fails, the system should block publishing or show a hard warning depending on role and severity.

## Screenshot And Evidence Rule

Every important page or registry row should connect to:

- desktop screenshot
- mobile 390px screenshot
- visual QA note
- source/evidence row
- date captured
- known limitations
- next verification action

This follows the current owner requirement: no verbal completion claims without visual proof.

## Analytics And KPI Layer

Do not build the KPI dashboard before the event dictionary is stable.

First define event names and required parameters for:

- project open
- unit select
- map interaction
- phone tap
- WhatsApp tap
- form start
- form submit
- consultant request
- interior request
- investor-language switch
- contractor-intake submit

Then build the owner dashboard with real sources only:

- traffic
- leads
- project engagement
- unit interest
- language interest
- source quality
- contractor pipeline
- revenue status

No invented numbers.

## Reusable System For Future Sites

After NadLan stabilizes, package this into a reusable starter:

- folder structure
- registry CSV template
- owner HTML template
- screenshot gate template
- admin field schema
- import/export instructions
- role and permissions model
- first-run checklist

This keeps the process independent from external design credits and usable on other WordPress real-estate projects.

## Acceptance Gate

The admin war room is ready to implement only when:

- owner approves registry fields
- keyword ownership map is reviewed
- screenshot paths are stable
- first analytics event dictionary is approved
- roles and permissions are confirmed
- no runtime files are changed by this documentation packet

## Files In This Packet

- `admin-war-room-execution-packet.csv`
- `admin-war-room-execution-packet.md`
- `admin-war-room-execution-packet-rtl.html`
- `admin-war-room-execution-packet-preview.png`
- `admin-war-room-execution-packet-preview-mobile.png`
- `admin-war-room-execution-packet-visual-qa.md`
