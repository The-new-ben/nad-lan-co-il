#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const failures = [];
const passes = [];

function fail(message) {
  failures.push(message);
}

function pass(message) {
  passes.push(message);
}

function readJson(relativePath) {
  const absolutePath = path.join(root, relativePath);
  try {
    return JSON.parse(fs.readFileSync(absolutePath, 'utf8'));
  } catch (error) {
    fail(`${relativePath}: invalid JSON (${error.message})`);
    return null;
  }
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let quoted = false;

  for (let index = 0; index < text.length; index += 1) {
    const character = text[index];
    const next = text[index + 1];

    if (quoted && character === '"' && next === '"') {
      field += '"';
      index += 1;
    } else if (character === '"') {
      quoted = !quoted;
    } else if (!quoted && character === ',') {
      row.push(field);
      field = '';
    } else if (!quoted && (character === '\n' || character === '\r')) {
      if (character === '\r' && next === '\n') index += 1;
      row.push(field);
      if (row.some((value) => value !== '')) rows.push(row);
      row = [];
      field = '';
    } else {
      field += character;
    }
  }

  if (quoted) throw new Error('unclosed quoted field');
  if (field !== '' || row.length > 0) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

function csvObjects(relativePath) {
  try {
    const rows = parseCsv(fs.readFileSync(path.join(root, relativePath), 'utf8'));
    if (rows.length === 0) throw new Error('empty CSV');
    const [header, ...body] = rows;
    for (const [index, row] of body.entries()) {
      if (row.length !== header.length) {
        fail(`${relativePath}:${index + 2}: ${row.length} columns; expected ${header.length}`);
      }
    }
    pass(`${relativePath}: ${body.length} data rows, ${header.length} columns`);
    return body.map((row) => Object.fromEntries(header.map((key, index) => [key, row[index] ?? ''])));
  } catch (error) {
    fail(`${relativePath}: invalid CSV (${error.message})`);
    return [];
  }
}

function matchesType(value, type) {
  if (type === 'null') return value === null;
  if (type === 'array') return Array.isArray(value);
  if (type === 'object') return value !== null && typeof value === 'object' && !Array.isArray(value);
  if (type === 'integer') return Number.isInteger(value);
  return typeof value === type;
}

function validateSchema(value, schema, location = '$') {
  const allowedTypes = Array.isArray(schema.type) ? schema.type : schema.type ? [schema.type] : [];
  if (allowedTypes.length > 0 && !allowedTypes.some((type) => matchesType(value, type))) {
    fail(`${location}: expected ${allowedTypes.join('|')}`);
    return;
  }
  if (schema.enum && !schema.enum.some((item) => Object.is(item, value))) {
    fail(`${location}: value is not in enum`);
  }
  if (typeof value === 'string') {
    if (schema.minLength !== undefined && value.length < schema.minLength) fail(`${location}: string is too short`);
    if (schema.pattern && !new RegExp(schema.pattern).test(value)) fail(`${location}: pattern mismatch`);
    if (schema.format === 'date' && !/^\d{4}-\d{2}-\d{2}$/.test(value)) fail(`${location}: invalid date format`);
  }
  if (Array.isArray(value)) {
    if (schema.minItems !== undefined && value.length < schema.minItems) fail(`${location}: too few items`);
    if (schema.maxItems !== undefined && value.length > schema.maxItems) fail(`${location}: too many items`);
    if (schema.uniqueItems && new Set(value.map((item) => JSON.stringify(item))).size !== value.length) {
      fail(`${location}: items are not unique`);
    }
    if (schema.items) value.forEach((item, index) => validateSchema(item, schema.items, `${location}[${index}]`));
  }
  if (value !== null && typeof value === 'object' && !Array.isArray(value)) {
    for (const required of schema.required ?? []) {
      if (!Object.hasOwn(value, required)) fail(`${location}: missing required property ${required}`);
    }
    if (schema.additionalProperties === false) {
      for (const key of Object.keys(value)) {
        if (!Object.hasOwn(schema.properties ?? {}, key)) fail(`${location}: unexpected property ${key}`);
      }
    }
    for (const [key, childSchema] of Object.entries(schema.properties ?? {})) {
      if (Object.hasOwn(value, key)) validateSchema(value[key], childSchema, `${location}.${key}`);
    }
  }
}

const schema = readJson('schemas/project-content.schema.json');
const contentFiles = [
  'content/stricker-13-brandeis-14/content.he.json',
  'content/bnei-dan-54-56/content.he.json'
];
const contents = contentFiles.map((file) => ({file, value: readJson(file)}));

if (schema) {
  for (const {file, value} of contents) {
    if (!value) continue;
    const failuresBefore = failures.length;
    validateSchema(value, schema, file);
    if (failures.length === failuresBefore) pass(`${file}: schema valid`);
  }
}

const factRows = csvObjects('governance/fact-register.csv');
const factById = new Map();
const allowedStates = new Set([
  'VERIFIED_PRIMARY',
  'TIME_SENSITIVE',
  'DEVELOPER_CLAIM',
  'SECONDARY_CONFIRM',
  'CONFLICT',
  'MISSING',
  'BLOCKED_RIGHTS'
]);

for (const row of factRows) {
  if (!row.fact_id) fail('governance/fact-register.csv: missing fact_id');
  if (factById.has(row.fact_id)) fail(`governance/fact-register.csv: duplicate fact_id ${row.fact_id}`);
  factById.set(row.fact_id, row);
  if (!allowedStates.has(row.state)) fail(`governance/fact-register.csv: unknown state ${row.state}`);
}

const renderableStates = new Set(['VERIFIED_PRIMARY', 'TIME_SENSITIVE', 'DEVELOPER_CLAIM']);
for (const {file, value} of contents) {
  if (!value) continue;
  for (const factId of value.fact_register_ids ?? []) {
    if (!factById.has(factId)) fail(`${file}: unknown fact_register_id ${factId}`);
  }
  for (const [index, fact] of (value.facts ?? []).entries()) {
    const row = factById.get(fact.fact_id);
    if (!row) {
      fail(`${file}.facts[${index}]: unknown fact_id ${fact.fact_id}`);
      continue;
    }
    if (!renderableStates.has(row.state)) {
      fail(`${file}.facts[${index}]: ${fact.fact_id} has non-renderable state ${row.state}`);
    }
    if (row.project_id !== value.project_id && row.project_id !== 'shared') {
      fail(`${file}.facts[${index}]: ${fact.fact_id} belongs to ${row.project_id}`);
    }
  }
  for (const [index, item] of (value.faq ?? []).entries()) {
    for (const factId of item.fact_ids ?? []) {
      if (!factById.has(factId)) fail(`${file}.faq[${index}]: unknown fact_id ${factId}`);
    }
  }
  if (value.inventory !== null || value.price !== null || value.geo !== null || value.media?.length !== 0) {
    fail(`${file}: blocked inventory, price, geo or media data is populated`);
  }
}

const rightsRows = csvObjects('governance/media-rights-ledger.csv');
if (rightsRows.length === 0) pass('governance/media-rights-ledger.csv: intentionally empty; media gate remains red');

const requiredFiles = [
  'README.md',
  'manifest.yml',
  'claude-local-handoff.md',
  'governance/blockers-and-required-inputs.md',
  'localization/adaptation-matrices.md',
  'product/page-and-3d-spec.md',
  'product/schema-and-measurement.md',
  'product/benchmark-patterns.md',
  'qa/green-gates.md',
  'sources/source-ledger.md'
];
for (const relativePath of requiredFiles) {
  if (!fs.existsSync(path.join(root, relativePath))) fail(`missing required file ${relativePath}`);
}
if (requiredFiles.every((relativePath) => fs.existsSync(path.join(root, relativePath)))) {
  pass(`required package files present: ${requiredFiles.length}`);
}

for (const message of passes) console.log(`PASS ${message}`);
for (const message of failures) console.error(`FAIL ${message}`);

if (failures.length > 0) {
  console.error(`\nPackage validation failed with ${failures.length} error(s).`);
  process.exit(1);
}

console.log(`\nPackage validation passed with ${passes.length} checks.`);
