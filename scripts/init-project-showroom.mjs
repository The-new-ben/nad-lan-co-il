import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();

function parseArgs(argv) {
  const out = {
    slug: '',
    postId: 0,
    title: '',
    force: false,
  };
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!out.slug && !arg.startsWith('--')) out.slug = arg;
    else if (arg === '--post-id') out.postId = Number(argv[++i] || 0) || 0;
    else if (arg === '--title') out.title = argv[++i] || '';
    else if (arg === '--force') out.force = true;
    else if (arg === '--help' || arg === '-h') {
      console.log(`Usage:
  node scripts/init-project-showroom.mjs <project-slug> --post-id <id> --title "Project Name"

Creates a safe project showroom asset folder under assets/projects/<project-slug>/.
The slug must be ASCII lowercase with hyphens. Existing folders are not overwritten unless
--force is passed.`);
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  if (!out.slug) throw new Error('Missing <project-slug>.');
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(out.slug)) {
    throw new Error('Project slug must be ASCII lowercase words separated by hyphens.');
  }
  if (!out.title) {
    out.title = out.slug.split('-').map((part) => part.charAt(0).toUpperCase() + part.slice(1)).join(' ');
  }
  return out;
}

function writeFile(file, value, force) {
  if (fs.existsSync(file) && !force) throw new Error(`Refusing to overwrite existing file: ${file}`);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, value, 'utf8');
}

function writeJson(file, value, force) {
  writeFile(file, `${JSON.stringify(value, null, 2)}\n`, force);
}

function main() {
  const args = parseArgs(process.argv);
  const dir = path.join(ROOT, 'assets', 'projects', args.slug);
  if (fs.existsSync(dir) && !args.force) {
    throw new Error(`Project folder already exists: ${dir}. Use --force only when intentionally regenerating placeholders.`);
  }
  fs.mkdirSync(path.join(dir, 'plans'), { recursive: true });

  const rawBase = `https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/assets/projects/${args.slug}`;
  const titleHe = `${args.title} - פרויקט לדוגמה`;
  const sourceNote = 'אומדן לא מחייב. להחלפה במידע רשמי מהיזם לפני פרסום מסחרי.';

  writeFile(path.join(dir, 'source-notes.md'), `# ${args.title} Source Notes

Status: scaffold only.

Replace this file before publication with:

- official developer page;
- municipal/planning source;
- approved unit inventory source;
- approved price or price-range source;
- drawing/model permission notes;
- date checked for every fact.

Do not publish paid-source rows, copied renders, fake availability or official-sounding prices from
this starter folder.
`, args.force);

  writeJson(path.join(dir, 'unit-map.json'), [
    {
      id: 'demo-0101',
      title: 'דירת הדגמה 4 חדרים',
      label: 'דמו',
      floor: 10,
      rooms: 4,
      sqm: 105,
      balcony: 12,
      dir: 'מערב',
      view: 'נוף פתוח',
      building: args.title,
      status: 'demo',
      availability: 'להחלפה במלאי רשמי',
      recommended: true,
      price_estimate: '',
      price_note: sourceNote,
      source_note: 'שורת הדגמה בלבד.',
      plan: '',
      interior_url: '',
      tour_url: '',
      view_note: 'יש להחליף בתיאור נוף מאושר.',
      hotspot_position: '0 10 0',
      hotspot_normal: '0 0 1',
      camera_orbit: '30deg 65deg auto',
      points: '420,420 520,420 520,480 420,480',
    },
  ], args.force);

  writeJson(path.join(dir, 'drawings.json'), {
    items: [
      {
        label: 'תוכנית הדגמה',
        type: 'floor_plan',
        url: '',
        source: 'להחלפה בתוכנית מאושרת מהיזם.',
      },
    ],
  }, args.force);

  writeJson(path.join(dir, 'environment.json'), {
    source_note: 'שכבת סביבה התחלתית. להחלפה במקורות עירוניים/יזם.',
    layers: [
      {
        id: 'nearby-projects',
        label: 'פרויקטים סמוכים',
        items: [
          {
            label: 'פרויקט סמוך לדוגמה',
            type: 'project',
            note: 'להחלפה במידע מאומת.',
            source: 'placeholder',
          },
        ],
      },
    ],
  }, args.force);

  writeJson(path.join(dir, 'view-layer-config.json'), {
    post_id: args.postId,
    providers: {
      mapbox: {
        floor_height_m: 3.05,
        ground_elevation_m: 0,
        note: 'Configure coordinates and bearing after the project location is verified.',
      },
    },
  }, args.force);

  writeJson(path.join(dir, 'project-meta-example.json'), {
    project_3d_image: '',
    project_3d_viewbox: '0 0 1000 1000',
    project_3d_floor_height_m: '3.05',
    project_3d_ground_elevation_m: '0',
    project_3d_avg_price_per_sqm: '',
    project_3d_price_source_note: sourceNote,
    project_3d_model_type: 'procedural',
    project_model_glb: '',
    project_model_usdz: '',
    project_model_poster: '',
    project_3d_video_url: '',
    project_3d_tour_url: '',
    project_3d_cesium_tiles_url: '',
    project_3d_demo: '1',
  }, args.force);

  writeJson(path.join(dir, 'material-intake-template.json'), {
    project_slug: args.slug,
    project_title: args.title,
    required_before_publication: [
      'official developer source',
      'approved model or facade/elevation',
      'approved unit inventory',
      'approved price wording or estimate policy',
      'official floor plans/drawings',
      'sales contact and WhatsApp',
      'image/model publication permission',
    ],
  }, args.force);

  writeFile(path.join(dir, 'qa.md'), `# ${args.title} QA

This folder is a scaffold. It is not publication proof.

Before publishing:

1. Replace placeholder sources and unit data.
2. Run:

   \`\`\`powershell
   node scripts/build-project-showroom-payload.mjs ${args.slug} --write
   node scripts/validate-project-showroom-payload.mjs --payload assets/projects/${args.slug}/showroom-payload.json
   \`\`\`

3. Import the payload only after the live plugin supports the payload route.
4. Run visual QA at 1440, 768, 390 and Edge-mobile.
5. Store screenshots and the template gate JSON in docs/qa/.
`, args.force);

  const payload = {
    $schema: 'docs/templates/project-showroom-payload.schema.json',
    schema: 'nadlan-project-showroom-payload/v1',
    project_slug: args.slug,
    post_id: args.postId,
    generated_from: [
      'project-meta-example.json',
      'unit-map.json',
      'drawings.json',
      'environment.json',
      'view-layer-config.json',
    ],
    public_use_policy: 'Starter scaffold only. Replace placeholder GLB, drawings, prices and inventory with approved material before publication.',
    meta: {
      project_3d_image: '',
      project_3d_viewbox: '0 0 1000 1000',
      project_3d_floor_height_m: '3.05',
      project_3d_ground_elevation_m: '0',
      project_3d_avg_price_per_sqm: '',
      project_3d_price_source_note: sourceNote,
      project_3d_model_type: 'procedural',
      project_model_glb: '',
      project_model_usdz: '',
      project_model_poster: '',
      project_3d_video_url: '',
      project_3d_tour_url: '',
      project_3d_cesium_tiles_url: '',
      project_3d_drawings_json: [
        {
          label: 'תוכנית הדגמה',
          type: 'floor_plan',
          url: '',
          source: 'להחלפה בתוכנית מאושרת מהיזם.',
        },
      ],
      project_3d_environment_json: {
        source_note: 'שכבת סביבה התחלתית. להחלפה במקורות עירוניים/יזם.',
        layers: [],
      },
      project_3d_units: [
        {
          id: 'demo-0101',
          title: titleHe,
          floor: 10,
          rooms: 4,
          sqm: 105,
          status: 'demo',
          hotspot_position: '0 10 0',
          hotspot_normal: '0 0 1',
          label: 'דמו',
          recommended: true,
          price_note: sourceNote,
        },
      ],
      project_3d_demo: '1',
    },
  };
  writeJson(path.join(dir, 'showroom-payload.json'), payload, args.force);

  console.log(JSON.stringify({
    ok: true,
    slug: args.slug,
    post_id: args.postId,
    folder: path.relative(ROOT, dir).replace(/\\/g, '/'),
    files: [
      'source-notes.md',
      'unit-map.json',
      'drawings.json',
      'environment.json',
      'view-layer-config.json',
      'project-meta-example.json',
      'material-intake-template.json',
      'showroom-payload.json',
      'qa.md',
      'plans/',
    ],
    next: [
      `node scripts/build-project-showroom-payload.mjs ${args.slug} --write`,
      `node scripts/validate-project-showroom-payload.mjs --payload assets/projects/${args.slug}/showroom-payload.json`,
    ],
  }, null, 2));
}

try {
  main();
} catch (err) {
  console.error(err.message);
  process.exit(1);
}
