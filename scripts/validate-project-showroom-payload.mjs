import fs from 'node:fs';
import path from 'node:path';

const DEFAULT_SCHEMA = 'docs/templates/project-showroom-payload.schema.json';
const DEFAULT_PAYLOAD = 'assets/projects/rainbow-tel-aviv/showroom-payload.json';
const URL_FIELDS = [
  'project_3d_image',
  'project_model_glb',
  'project_model_usdz',
  'project_model_poster',
  'project_3d_video_url',
  'project_3d_tour_url',
  'project_3d_cesium_tiles_url',
];

function parseArgs(argv) {
  const out = {
    schema: DEFAULT_SCHEMA,
    payload: DEFAULT_PAYLOAD,
  };
  for (let i = 2; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--schema') out.schema = argv[++i] || out.schema;
    else if (a === '--payload') out.payload = argv[++i] || out.payload;
    else if (a === '--help' || a === '-h') {
      console.log(`Usage:
  node scripts/validate-project-showroom-payload.mjs --payload assets/projects/rainbow-tel-aviv/showroom-payload.json

Validates against docs/templates/project-showroom-payload.schema.json using Node built-ins.`);
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${a}`);
    }
  }
  return out;
}

function readJson(file) {
  const buf = fs.readFileSync(path.resolve(process.cwd(), file));
  let text = '';
  if (buf.length >= 2 && buf[0] === 0xff && buf[1] === 0xfe) {
    text = buf.toString('utf16le');
  } else if (buf.length >= 2 && buf[0] === 0xfe && buf[1] === 0xff) {
    // Very small fallback for big-endian UTF-16 JSON files.
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

function isObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function typeOk(value, allowed) {
  const actual = Array.isArray(value) ? 'array' : value === null ? 'null' : typeof value;
  if (allowed.includes('integer') && typeof value === 'number' && Number.isInteger(value)) return true;
  return allowed.includes(actual);
}

function checkUrl(value, label, errors) {
  if (value === '') return;
  try {
    const u = new URL(String(value));
    if (!['http:', 'https:'].includes(u.protocol)) errors.push(`${label} must use http(s)`);
  } catch {
    errors.push(`${label} is not a valid URL`);
  }
}

function validateScalarTypes(schema, value, pathLabel, errors) {
  if (schema.const !== undefined && value !== schema.const) {
    errors.push(`${pathLabel} must be ${JSON.stringify(schema.const)}`);
  }
  if (schema.enum && !schema.enum.includes(value)) {
    errors.push(`${pathLabel} must be one of ${schema.enum.join(', ')}`);
  }
  if (schema.type) {
    const allowed = Array.isArray(schema.type) ? schema.type : [schema.type];
    if (!typeOk(value, allowed)) {
      errors.push(`${pathLabel} has type ${Array.isArray(value) ? 'array' : value === null ? 'null' : typeof value}; expected ${allowed.join('|')}`);
    }
  }
  if (schema.pattern && typeof value === 'string') {
    const re = new RegExp(schema.pattern);
    if (!re.test(value)) errors.push(`${pathLabel} does not match ${schema.pattern}`);
  }
  if (schema.minLength && typeof value === 'string' && value.length < schema.minLength) {
    errors.push(`${pathLabel} must not be empty`);
  }
  if (schema.minimum !== undefined && typeof value === 'number' && value < schema.minimum) {
    errors.push(`${pathLabel} must be >= ${schema.minimum}`);
  }
}

function validateObject(schema, value, pathLabel, errors, rootSchema) {
  validateScalarTypes(schema, value, pathLabel, errors);
  if (!isObject(value)) return;
  const required = schema.required || [];
  for (const key of required) {
    if (!(key in value)) errors.push(`${pathLabel}.${key} is required`);
  }
  if (schema.additionalProperties === false && schema.properties) {
    for (const key of Object.keys(value)) {
      if (!(key in schema.properties)) errors.push(`${pathLabel}.${key} is not allowed by schema`);
    }
  }
  for (const [key, childSchema] of Object.entries(schema.properties || {})) {
    if (key in value) validateAny(childSchema, value[key], `${pathLabel}.${key}`, errors, rootSchema);
  }
}

function resolveRef(schema, ref) {
  if (ref === '#/$defs/unit') return schema.$defs.unit;
  throw new Error(`Unsupported schema ref ${ref}`);
}

function validateAny(schemaNode, value, pathLabel, errors, rootSchema = null) {
  const schema = rootSchema || schemaNode;
  if (schemaNode.$ref) {
    return validateAny(resolveRef(schema, schemaNode.$ref), value, pathLabel, errors, schema);
  }
  if (schemaNode.type === 'object' || (Array.isArray(schemaNode.type) && schemaNode.type.includes('object')) || schemaNode.properties) {
    validateObject(schemaNode, value, pathLabel, errors, schema);
  } else if (schemaNode.type === 'array' || (Array.isArray(schemaNode.type) && schemaNode.type.includes('array'))) {
    validateScalarTypes(schemaNode, value, pathLabel, errors);
    if (Array.isArray(value)) {
      if (schemaNode.minItems && value.length < schemaNode.minItems) errors.push(`${pathLabel} must have at least ${schemaNode.minItems} items`);
      if (schemaNode.items) value.forEach((item, index) => validateAny(schemaNode.items, item, `${pathLabel}[${index}]`, errors, schema));
    }
  } else {
    validateScalarTypes(schemaNode, value, pathLabel, errors);
  }
}

function validatePayload(schema, payload) {
  const errors = [];
  validateAny(schema, payload, '$', errors, schema);

  if (payload.meta) {
    for (const field of URL_FIELDS) checkUrl(payload.meta[field], `meta.${field}`, errors);
    if (Array.isArray(payload.meta.project_3d_units)) {
      payload.meta.project_3d_units.forEach((unit, index) => {
        checkUrl(unit.plan || '', `unit[${index}].plan`, errors);
        checkUrl(unit.interior_url || '', `unit[${index}].interior_url`, errors);
        checkUrl(unit.tour_url || '', `unit[${index}].tour_url`, errors);
      });
    }
  }

  const raw = JSON.stringify(payload);
  if (!/[\u0590-\u05FF]/.test(raw)) errors.push('payload contains no Hebrew characters');
  if (/[�]/.test(raw)) errors.push('payload contains Unicode replacement character');
  if (/Ã|Â|×/.test(raw)) errors.push('payload may contain mojibake markers');
  if (/\?\?\?\?/.test(raw)) errors.push('payload contains repeated question marks');
  return errors;
}

const args = parseArgs(process.argv);
const schema = readJson(args.schema);
const payload = readJson(args.payload);
const errors = validatePayload(schema, payload);
const summary = {
  payload: args.payload,
  schema: args.schema,
  schema_id: schema.$id || '',
  meta_fields: payload.meta ? Object.keys(payload.meta).length : 0,
  expected_fields: schema.properties.meta.required.length,
  units: payload.meta && Array.isArray(payload.meta.project_3d_units) ? payload.meta.project_3d_units.length : 0,
  drawings: payload.meta && Array.isArray(payload.meta.project_3d_drawings_json) ? payload.meta.project_3d_drawings_json.length : 0,
  errors,
};

console.log(JSON.stringify(summary, null, 2));
if (errors.length) process.exit(1);
