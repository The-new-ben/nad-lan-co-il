# SKILL: the project factory - building a project page A to Z

Proven end to end on the two commercial towers, 2026-08-08/09. Read this before
building any project page; it replaces guesswork with a fixed pipeline.

## 0. Inputs (the drop)

Materials arrive as a folder or zip: per-language markdown, sources.csv, any
images/models. Convention: docs/content/<project-or-batch>/. If materials are
missing, FLOAT the gap - never invent, never fake a model or a photo.

## 1. Gate the content BEFORE any upload

Run the standard's section F on the files themselves (scratchpad/qa-commercial.py
is the reference): word count >= 2,500, exactly one H1, ZERO U+2012-2015 dashes,
Hebrew-leak scan on foreign files (allow bilingual legal terms), meta Title +
Description present, FAQ H3 count, lead-paragraph length.
FAQ EXTRACTION IS LANGUAGE-SPECIFIC: match on 'вопрос' and 'أسئلة', not on full
phrases - 'Часто задаваемые вопросы' / 'الأسئلة الشائعة' were missed once and
four pages nearly shipped without schema.

## 2. Convert

markdown -> html (extensions: tables, sane_lists). The H1 becomes the POST TITLE
and is stripped from the body (never two H1s). Extract FAQ pairs -> FAQPage
JSON-LD -> base64 -> meta _nl_faq_schema (base64 because update_post_meta
unslashes and corrupts gershayim escapes). Replace [PROJECT_LINK] with the
curated shelf link.

## 3. Seed

One snippet, HE first so variants can inherit. Variant slug is exactly
`<base>-<lang>`; the platform wires language context, hreflang and chrome from
the slug alone. Variants INHERIT the base project's showroom metas (model,
units, coords) so the theater is identical per language - but NEVER inherit
_nl_faq_schema, _yoast_*, or sandbox flags. Verify each save with a server-side
md5 read-back in the same request.

## 4. THE META TRAPS (each cost a real debugging cycle)

- **ASCII quote inside Hebrew meta text kills the whole write.** A unit note
  containing מ"ר silently emptied project_3d_units. Use gershayim U+05F4 (מ״ר).
  Applies to every meta string, not just schema.
- project_3d_units is sanitized and NORMALIZED (a 169-char unit comes back 512
  chars). Required per unit: id, label, floor, rooms, sqm, dir, status. `dir`
  should be the English enum (west, south-west...). 75 units store fine.
- Big values go through a MEDIA payload + snippet decode, never a REST param.
- Always read back and count inside the same request; a silent empty write
  looks identical to success from the client.

## 5. 3D when the developer gives nothing

tools/glb-gen-*.py builds a parametric massing GLB in pure python (no Blender,
no deps): rings -> bands -> caps, glTF binary writer at the bottom. The Park =
19,488 triangles at 186.7m; ToHa2 = 46,848 triangles at 298.2m (elliptical,
tapered, sky-lobby recess, 9-degree twist). Proportions must come from the
verified dossier. Mark it honestly: meta project_model_generic = 1 so the page
shows the generic-model chip. Ship the GLB as a b64 payload + snippet decode
(direct .glb upload 500s on the mime gate).

## 6. Turn on the unit journey (v2)

Per post: meta nl_unit_scene_v2 = on. That is the whole switch. Rollback =
delete the meta. Fleet rollout = flip it on every project post.

## 7. Sweep the LIVE pages (scratchpad/sweep-commercial.py)

Per page: HTTP 200, single H1, rendered words, CONTENT-FIRST opening (title and
lead before the notice), hreflang count, exactly ONE language switcher, ZERO
engine footer inside the page, FAQPage present, zero long dashes. Then the
mobile journey: hotspots > 0, scene shows, beam present, doors present, tool
dialog is a body child at exact viewport size, and nested scrollers = [].

## 8. Record

AGENT-LOG entry, board card with clickable links per language, preserve the
source package under docs/content/, commit and push (git fetch + rebase first -
other sessions push to this branch).
