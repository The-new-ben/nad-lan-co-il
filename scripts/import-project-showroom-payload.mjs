import fs from 'node:fs';
import path from 'node:path';

const DEFAULT_SITE = 'https://nad-lan.co.il';
const MIN_PLUGIN_VERSION = '1.65.2';

function usage() {
  return `Usage:
  node scripts/import-project-showroom-payload.mjs --site https://nad-lan.co.il --post-id 4464 --payload assets/projects/rainbow-tel-aviv/showroom-payload.json --dry-run
  node scripts/import-project-showroom-payload.mjs --site https://nad-lan.co.il --post-id 4464 --payload assets/projects/rainbow-tel-aviv/showroom-payload.json --apply

Auth for --apply:
  WP_USER=<wordpress user> WP_APP_PASSWORD=<application password>

Notes:
  --dry-run validates the payload and checks health only.
  --apply refuses to write unless live healthcheck is ${MIN_PLUGIN_VERSION}+ and auth env vars exist.
  No secrets are read from files or printed.`;
}

function parseArgs(argv) {
  const out = {
    site: DEFAULT_SITE,
    postId: 0,
    payload: '',
    apply: false,
    dryRun: false,
  };
  for (let i = 2; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--site') out.site = argv[++i] || out.site;
    else if (a === '--post-id') out.postId = Number(argv[++i] || 0);
    else if (a === '--payload') out.payload = argv[++i] || '';
    else if (a === '--apply') out.apply = true;
    else if (a === '--dry-run') out.dryRun = true;
    else if (a === '--help' || a === '-h') {
      console.log(usage());
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${a}`);
    }
  }
  if (!out.payload) out.payload = 'assets/projects/rainbow-tel-aviv/showroom-payload.json';
  if (!out.postId) out.postId = 4464;
  if (!out.apply && !out.dryRun) out.dryRun = true;
  out.site = out.site.replace(/\/+$/, '');
  return out;
}

function readJsonFile(file) {
  const buf = fs.readFileSync(path.resolve(process.cwd(), file));
  let text = '';
  if (buf.length >= 2 && buf[0] === 0xff && buf[1] === 0xfe) {
    text = buf.toString('utf16le');
  } else if (buf.length >= 2 && buf[0] === 0xfe && buf[1] === 0xff) {
    const swapped = Buffer.alloc(buf.length - 2);
    for (let i = 2; i + 1 < buf.length; i += 2) {
      swapped[i - 2] = buf[i + 1];
      swapped[i - 1] = buf[i];
    }
    text = swapped.toString('utf16le');
  } else {
    text = buf.toString('utf8');
  }
  return JSON.parse(text.replace(/^\uFEFF/, ''));
}

function compareVersions(a, b) {
  const aa = String(a).split('.').map((n) => Number(n) || 0);
  const bb = String(b).split('.').map((n) => Number(n) || 0);
  for (let i = 0; i < Math.max(aa.length, bb.length); i += 1) {
    const d = (aa[i] || 0) - (bb[i] || 0);
    if (d !== 0) return d;
  }
  return 0;
}

function validateUrl(value, field, errors) {
  if (!value) return;
  try {
    const u = new URL(String(value));
    if (!['https:', 'http:'].includes(u.protocol)) errors.push(`${field} must be http(s)`);
  } catch {
    errors.push(`${field} is not a valid URL`);
  }
}

function validatePayload(payload) {
  const required = [
    'project_3d_image',
    'project_3d_viewbox',
    'project_3d_floor_height_m',
    'project_3d_ground_elevation_m',
    'project_3d_avg_price_per_sqm',
    'project_3d_price_source_note',
    'project_3d_model_type',
    'project_model_glb',
    'project_model_usdz',
    'project_model_poster',
    'project_3d_video_url',
    'project_3d_tour_url',
    'project_3d_cesium_tiles_url',
    'project_3d_drawings_json',
    'project_3d_environment_json',
    'project_3d_units',
    'project_3d_demo',
  ];
  const errors = [];
  if (!payload || payload.schema !== 'nadlan-project-showroom-payload/v1') {
    errors.push('schema must be nadlan-project-showroom-payload/v1');
  }
  if (!payload.meta || typeof payload.meta !== 'object' || Array.isArray(payload.meta)) {
    errors.push('payload.meta object is required');
    return { errors, required };
  }
  for (const key of required) {
    if (!(key in payload.meta)) errors.push(`missing meta field: ${key}`);
  }
  const units = payload.meta.project_3d_units;
  if (!Array.isArray(units) || units.length === 0) {
    errors.push('project_3d_units must be a non-empty array');
  } else {
    units.forEach((u, i) => {
      for (const key of ['id', 'title', 'floor', 'rooms', 'sqm', 'status', 'hotspot_position', 'hotspot_normal']) {
        if (u[key] === undefined || u[key] === '') errors.push(`unit ${i} missing ${key}`);
      }
      validateUrl(u.plan, `unit ${i} plan`, errors);
      validateUrl(u.interior_url, `unit ${i} interior_url`, errors);
      validateUrl(u.tour_url, `unit ${i} tour_url`, errors);
    });
  }
  for (const key of ['project_model_glb', 'project_model_poster', 'project_model_usdz', 'project_3d_image', 'project_3d_video_url', 'project_3d_tour_url', 'project_3d_cesium_tiles_url']) {
    validateUrl(payload.meta[key], key, errors);
  }
  const raw = JSON.stringify(payload);
  if (!/[\u0590-\u05FF]/.test(raw)) errors.push('payload contains no Hebrew characters');
  if (/[ï¿½]/.test(raw)) errors.push('payload contains Unicode replacement character');
  if (/Ãƒ|Ã‚|Ã—/.test(raw)) errors.push('payload may contain mojibake markers');
  if (/[\u0080-\u009F]/.test(raw)) errors.push('payload contains C1 control characters, often caused by mojibake');
  if (/×[\u0080-\u009F]/.test(raw)) errors.push('payload contains Windows-1252-style Hebrew mojibake');
  if (/\?\?\?\?/.test(raw)) errors.push('payload contains repeated question marks');
  return { errors, required };
}

async function getJson(url, options = {}) {
  const res = await fetch(url, options);
  const text = await res.text();
  let json = null;
  try {
    json = text ? JSON.parse(text) : null;
  } catch {
    throw new Error(`Non-JSON response from ${url}: ${text.slice(0, 160)}`);
  }
  if (!res.ok) {
    throw new Error(`HTTP ${res.status} from ${url}: ${JSON.stringify(json).slice(0, 300)}`);
  }
  return json;
}

function authHeader() {
  const user = process.env.WP_USER || '';
  const pass = process.env.WP_APP_PASSWORD || '';
  if (!user || !pass) return '';
  return `Basic ${Buffer.from(`${user}:${pass}`).toString('base64')}`;
}

async function main() {
  const args = parseArgs(process.argv);
  const payloadPath = path.resolve(process.cwd(), args.payload);
  const payload = readJsonFile(payloadPath);
  const { errors, required } = validatePayload(payload);
  if (errors.length) throw new Error(`Payload validation failed:\n${errors.map((e) => `- ${e}`).join('\n')}`);

  const health = await getJson(`${args.site}/wp-json/nadlan/v1/healthcheck?cb=${Date.now()}`);
  const liveVersion = String(health.version || '');
  const routeReady = !!(health.project_3d && health.project_3d.showroom_payload_api_v1652);
  const versionReady = compareVersions(liveVersion, MIN_PLUGIN_VERSION) >= 0;

  const summary = {
    mode: args.apply ? 'apply' : 'dry-run',
    site: args.site,
    post_id: args.postId,
    payload: args.payload,
    live_version: liveVersion,
    required_version: MIN_PLUGIN_VERSION,
    version_ready: versionReady,
    route_marker_ready: routeReady,
    meta_fields: Object.keys(payload.meta).length,
    expected_fields: required.length,
    units: payload.meta.project_3d_units.length,
    drawings: Array.isArray(payload.meta.project_3d_drawings_json) ? payload.meta.project_3d_drawings_json.length : 0,
    has_glb: !!payload.meta.project_model_glb,
  };

  if (!args.apply) {
    console.log(JSON.stringify(summary, null, 2));
    if (!versionReady || !routeReady) {
      process.exitCode = 2;
    }
    return;
  }

  if (!versionReady || !routeReady) {
    throw new Error(`Live plugin is not ready for showroom import. Healthcheck=${liveVersion}, route_marker=${routeReady}`);
  }
  const auth = authHeader();
  if (!auth) {
    throw new Error('Missing WP_USER or WP_APP_PASSWORD environment variable. Refusing to write.');
  }

  const endpoint = `${args.site}/wp-json/nadlan/v1/project-showroom/${args.postId}`;
  const before = await getJson(endpoint, { headers: { Authorization: auth } });
  const result = await getJson(endpoint, {
    method: 'POST',
    headers: {
      Authorization: auth,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ meta: payload.meta }),
  });
  const after = await getJson(endpoint, { headers: { Authorization: auth } });

  console.log(JSON.stringify({
    ...summary,
    before_units: before.units_count,
    updated_n: result.updated_n,
    after_units: after.units_count,
    after_has_glb: !!(after.meta && after.meta.project_model_glb),
  }, null, 2));
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
