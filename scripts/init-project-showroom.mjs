import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();

function usage() {
  return `Usage:
  node scripts/init-project-showroom.mjs <project-slug> [--post-id 123] [--out-root assets/projects] [--force]

Creates the project showroom source folder required by the NadLan project factory.
The generated files are safe placeholders. Replace them with sourced/developer-approved material
before publishing a sales-quality project page.`;
}

function parseArgs(argv) {
  const args = {
    slug: '',
    postId: 0,
    outRoot: path.join('assets', 'projects'),
    force: false,
  };
  for (let i = 2; i < argv.length; i += 1) {
    const a = argv[i];
    if (!args.slug && !a.startsWith('--')) args.slug = a;
    else if (a === '--post-id') args.postId = Number(argv[++i] || 0) || 0;
    else if (a === '--out-root') args.outRoot = argv[++i] || args.outRoot;
    else if (a === '--force') args.force = true;
    else if (a === '--help' || a === '-h') {
      console.log(usage());
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${a}`);
    }
  }
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(args.slug)) {
    throw new Error('Project slug is required and must be ASCII kebab-case, for example: migdalei-hayam-sde-dov');
  }
  return args;
}

function writeFile(file, content, force) {
  if (fs.existsSync(file) && !force) {
    throw new Error(`Refusing to overwrite ${file}. Re-run with --force if this is intentional.`);
  }
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, content.endsWith('\n') ? content : `${content}\n`, 'utf8');
}

function json(value) {
  return `${JSON.stringify(value, null, 2)}\n`;
}

function buildFiles(slug, postId) {
  const projectName = slug.split('-').map((part) => part[0].toUpperCase() + part.slice(1)).join(' ');
  const sourceNote = `# ${projectName} Source Notes

Status: draft intake

## Required Sources

- Official developer/project page:
- Official sales contact:
- Municipal/planning source:
- Licensed listing/source page:
- News/market source:
- Owner approval for public prices:
- Owner approval for public inventory:
- Permission for images/model/floor plans:

## Facts To Verify Before Publish

- Developer:
- Address/district:
- Project status:
- Floors/buildings:
- Units:
- Amenities:
- Transport/parks/schools:
- Price range or price-estimate source:
- Inventory status source:

## Public-Use Rule

Do not publish paid-source transaction rows, official-looking inventory, official prices, or
developer imagery until the owner confirms the publication rights. If data is illustrative, label it
as illustrative on the public page and in the payload.
`;

  const projectMeta = {
    project_3d_image: '',
    project_3d_viewbox: '0 0 1000 1000',
    project_3d_floor_height_m: 3.05,
    project_3d_ground_elevation_m: 0,
    project_3d_avg_price_per_sqm: '',
    project_3d_price_source_note: 'אומדן לא מחייב. יש להחליף בהערת מקור מאושרת לפני הצגת מחירים לציבור.',
    project_3d_model_type: 'facade',
    project_model_glb: '',
    project_model_usdz: '',
    project_model_poster: '',
    project_3d_video_url: '',
    project_3d_tour_url: '',
    project_3d_cesium_tiles_url: '',
    project_3d_demo: '1',
  };

  const unitMap = [
    {
      id: 'unit-demo-01',
      title: 'דירת הדגמה, קומה 10',
      label: 'דירה 10',
      building: projectName,
      floor: 10,
      rooms: 4,
      sqm: 110,
      balcony: 12,
      dir: 'מערב',
      line: 'A',
      view: 'יש להחליף בתיאור נוף מאומת',
      status: 'available',
      availability: 'להמחשה עד אישור מלאי מהיזם',
      price_estimate: '',
      price_note: 'אומדן לא מחייב בלבד. יש להחליף במקור מאושר לפני פרסום.',
      source_note: 'נתון פתיחה להמחשה. יש להחליף במלאי מאושר מהיזם.',
      plan: '',
      interior_url: '',
      tour_url: '',
      view_note: 'הערת נוף להמחשה. יש להחליף בנתוני קומה ונוף מאומתים.',
      points: '420,560 520,560 520,610 420,610',
      stage_x: 42,
      stage_y: 56,
      stage_w: 10,
      stage_h: 5,
      hotspot_position: '0 30 5',
      hotspot_normal: '0 0 1',
      camera_orbit: '35deg 65deg auto',
      recommended: true,
    },
  ];

  const drawings = {
    items: [
      {
        label: 'תרשים מיקום להמחשה',
        type: 'site_orientation',
        url: '',
        source: 'המחשה בלבד. יש להחליף בשרטוט מאושר או איור מקורי.',
      },
      {
        label: 'תוכנית קומה טיפוסית להמחשה',
        type: 'floor_plan',
        url: '',
        source: 'המחשה בלבד. יש להחליף בתוכנית קומה מאושרת.',
      },
    ],
  };

  const environment = {
    status: 'draft',
    updated: new Date().toISOString().slice(0, 10),
    project: {
      name: projectName,
      district: 'יש להשלים רובע',
      center: {
        lat: 0,
        lng: 0,
        precision: 'missing',
        source_note: 'יש להחליף בנקודת פרויקט מאומתת לפני פרסום.',
      },
    },
    source_policy: 'יש להשתמש רק במקורות ציבוריים או מורשים. פריטים מתוכננים חייבים סימון ברור.',
    layers: [
      {
        id: 'neighbor_projects',
        label: 'פרויקטים בסביבה',
        ui: 'clickable_project_chips',
        items: [],
      },
      {
        id: 'parks_and_coast',
        label: 'פארקים וסביבה',
        ui: 'context_cards',
        items: [],
      },
      {
        id: 'mobility',
        label: 'תחבורה ונגישות',
        ui: 'context_cards',
        items: [],
      },
    ],
  };

  const viewLayer = {
    project_slug: slug,
    post_id: postId,
    version: 1,
    status: 'draft',
    project_center: {
      lat: 0,
      lng: 0,
      precision: 'missing',
      source_note: 'Replace with verified project coordinates.',
    },
    cms_inputs: {
      lat: 0,
      lng: 0,
      project_3d_units: 'unit-map.json',
      project_3d_environment_json: 'environment.json',
      project_3d_cesium_tiles_url: '',
    },
    providers: {
      mapbox: {
        state: 'ready_when_token_and_coords_exist',
        load_policy: 'user_open_only',
        rtl_text_plugin_required: true,
        camera_formula: 'ground_elevation_m + 4.0 + (floor - 1) * floor_height_m + 1.55',
        ground_elevation_m: 0,
        floor_height_m: 3.05,
        camera_distance_m: 900,
        pitch_degrees: 65,
        bearing_source: 'unit direction -> bearing_degrees',
      },
      cesium: {
        state: 'ready_seam_pending_approved_tiles',
        load_policy: 'user_open_only',
        tiles_url: '',
        public_policy: 'Do not enable until token/cost governance and public-use rights are approved.',
      },
    },
    cost_controls: {
      instantiate_on_page_load: false,
      lazy_on_user_gesture: true,
      dedupe_per_session: true,
      static_preview_fallback: true,
    },
    unit_views: [],
    overlays: [],
    qa_requirements: [
      'Default page state remains building selector, not map/tiles.',
      'View layer opens only after buyer action.',
      'Unit selection carries floor, rooms, sqm, status and source-aware price note.',
      'No official price or availability appears without owner approval.',
    ],
  };

  const qa = `# ${projectName} Project Showroom QA

## Build Commands

\`\`\`powershell
node scripts/build-project-showroom-payload.mjs ${slug} --write
node scripts/validate-project-showroom-payload.mjs --payload assets/projects/${slug}/showroom-payload.json
\`\`\`

## Publish Gate

\`\`\`powershell
node scripts/qa-project-showroom-live.mjs --site https://nad-lan.co.il --slug ${slug} --post-id ${postId || '<post-id>'} --strict
node scripts/qa-project-template-gate.mjs --site https://nad-lan.co.il --slug ${slug} --post-id ${postId || '<post-id>'} --min-version 1.66.3 --visual --strict
\`\`\`

## Required Before Public Launch

- [ ] Official or original model/facade/poster asset.
- [ ] Approved source notes for inventory and price wording.
- [ ] At least one selectable unit with 44px+ mobile hit target.
- [ ] Buyer card shows status, floor, rooms, sqm, view and non-binding price note.
- [ ] Contact/developer CTA carries selected-unit context.
- [ ] One H1, self canonical, index/follow, FAQPage and ApartmentComplex schema.
- [ ] No internal words such as lead, funnel, CRM, monetization or paid placement in public copy.
- [ ] Visual screenshots stored for 1440, 768, 390 and Edge-mobile.
`;

  return {
    'source-notes.md': sourceNote,
    'project-meta-example.json': json(projectMeta),
    'unit-map.json': json(unitMap),
    'drawings.json': json(drawings),
    'environment.json': json(environment),
    'view-layer-config.json': json(viewLayer),
    'qa.md': qa,
  };
}

function main() {
  const args = parseArgs(process.argv);
  const outRoot = path.resolve(ROOT, args.outRoot);
  const target = path.join(outRoot, args.slug);
  const files = buildFiles(args.slug, args.postId);
  fs.mkdirSync(target, { recursive: true });
  for (const [name, content] of Object.entries(files)) {
    writeFile(path.join(target, name), content, args.force);
  }
  console.log(JSON.stringify({
    created: target,
    files: Object.keys(files),
    next: [
      `node scripts/build-project-showroom-payload.mjs ${args.slug} --write`,
      `node scripts/validate-project-showroom-payload.mjs --payload assets/projects/${args.slug}/showroom-payload.json`,
    ],
  }, null, 2));
}

main();
