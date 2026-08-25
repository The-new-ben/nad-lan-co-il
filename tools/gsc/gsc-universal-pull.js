#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const fs = require('fs');
const fsp = fs.promises;
const http = require('http');
const os = require('os');
const path = require('path');
const { google } = require('googleapis');

const SCRIPT_VERSION = '1.0.0';
const READONLY_SCOPE = 'https://www.googleapis.com/auth/webmasters.readonly';
const ROW_LIMIT = 25000;
const MAX_RETRIES = 5;

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;
    const eq = token.indexOf('=');
    const rawKey = token.slice(2, eq === -1 ? undefined : eq);
    const key = rawKey.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
    if (eq !== -1) {
      args[key] = token.slice(eq + 1);
    } else if (argv[i + 1] && !argv[i + 1].startsWith('--')) {
      args[key] = argv[i + 1];
      i += 1;
    } else {
      args[key] = true;
    }
  }
  return args;
}

function usage() {
  return [
    'GSC universal read-only pull',
    '',
    'Required for a data pull:',
    '  --site=<exact property id> --start=YYYY-MM-DD --end=YYYY-MM-DD',
    '',
    'Options:',
    '  --type=web --data-state=final --output-dir=<absolute path>',
    '  --daily-shards --resume --list-sites --help',
    '',
    'Credentials are read only from GSC_OAUTH_CLIENT_PATH and GSC_TOKEN_PATH.',
  ].join('\n');
}

function assertDate(value, name) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value || '')) throw new Error(`${name} must be YYYY-MM-DD.`);
  const parsed = new Date(`${value}T00:00:00Z`);
  if (Number.isNaN(parsed.getTime()) || parsed.toISOString().slice(0, 10) !== value) {
    throw new Error(`${name} is not a valid calendar date.`);
  }
}

function enumerateDates(start, end) {
  const dates = [];
  const cursor = new Date(`${start}T00:00:00Z`);
  const finish = new Date(`${end}T00:00:00Z`);
  while (cursor <= finish) {
    dates.push(cursor.toISOString().slice(0, 10));
    cursor.setUTCDate(cursor.getUTCDate() + 1);
  }
  return dates;
}

async function ensureDir(dir) {
  await fsp.mkdir(dir, { recursive: true });
}

async function readJson(file) {
  return JSON.parse(await fsp.readFile(file, 'utf8'));
}

async function writeJsonAtomic(file, value) {
  await ensureDir(path.dirname(file));
  const temp = `${file}.tmp-${process.pid}`;
  await fsp.writeFile(temp, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
  await fsp.rename(temp, file);
}

async function appendJsonLine(file, value) {
  await ensureDir(path.dirname(file));
  await fsp.appendFile(file, `${JSON.stringify(value)}\n`, 'utf8');
}

function csvEscape(value) {
  if (value === null || value === undefined) return '';
  const text = String(value);
  return /[",\r\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

async function writeCsv(file, columns, rows) {
  await ensureDir(path.dirname(file));
  const lines = [columns.join(',')];
  for (const row of rows) lines.push(columns.map((column) => csvEscape(row[column])).join(','));
  await fsp.writeFile(file, `\uFEFF${lines.join('\r\n')}\r\n`, 'utf8');
}

async function sha256(file) {
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash('sha256');
    const input = fs.createReadStream(file);
    input.on('error', reject);
    input.on('data', (chunk) => hash.update(chunk));
    input.on('end', () => resolve(hash.digest('hex')));
  });
}

function normalizeApiRows(rows) {
  return (rows || []).map((row) => ({
    keys: Array.isArray(row.keys) ? row.keys.map(String) : [],
    clicks: Number(row.clicks || 0),
    impressions: Number(row.impressions || 0),
    ctr: Number(row.ctr || 0),
    position: Number(row.position || 0),
  }));
}

function cleanError(error) {
  const status = Number(error?.response?.status || error?.code || 0) || null;
  const message = String(error?.message || 'Unknown API error').replace(/[\r\n]+/g, ' ').slice(0, 400);
  return { status, message };
}

function isTransient(error) {
  const status = Number(error?.response?.status || error?.code || 0);
  return status === 429 || (status >= 500 && status <= 599);
}

async function withRetry(operation, context, batchLogFile) {
  for (let attempt = 1; attempt <= MAX_RETRIES; attempt += 1) {
    try {
      return await operation();
    } catch (error) {
      const info = cleanError(error);
      await appendJsonLine(batchLogFile, {
        timestamp: new Date().toISOString(),
        event: 'api_error',
        attempt,
        context,
        ...info,
        transient: isTransient(error),
      });
      if (!isTransient(error) || attempt === MAX_RETRIES) throw error;
      const delayMs = Math.min(30000, 1000 * (2 ** (attempt - 1)) + Math.floor(Math.random() * 500));
      await new Promise((resolve) => setTimeout(resolve, delayMs));
    }
  }
  throw new Error('Retry loop exhausted unexpectedly.');
}

function getCredentialPaths() {
  const oauthClientPath = process.env.GSC_OAUTH_CLIENT_PATH;
  const tokenPath = process.env.GSC_TOKEN_PATH;
  if (!oauthClientPath) throw new Error('GSC_OAUTH_CLIENT_PATH is not set.');
  if (!tokenPath) throw new Error('GSC_TOKEN_PATH is not set.');
  if (!fs.existsSync(oauthClientPath)) throw new Error('OAuth client file does not exist at GSC_OAUTH_CLIENT_PATH.');
  const tokenParent = path.dirname(tokenPath);
  if (!fs.existsSync(tokenParent)) throw new Error('The parent directory of GSC_TOKEN_PATH does not exist.');
  return { oauthClientPath: path.resolve(oauthClientPath), tokenPath: path.resolve(tokenPath) };
}

async function loadClientDefinition(oauthClientPath) {
  const parsed = await readJson(oauthClientPath);
  const client = parsed.installed || parsed.web;
  if (!client?.client_id || !client?.client_secret) {
    throw new Error('OAuth client JSON is missing the expected Desktop client fields.');
  }
  return { clientId: client.client_id, clientSecret: client.client_secret };
}

async function saveTokens(tokenPath, tokens, previous = {}) {
  const merged = { ...previous, ...tokens };
  if (!merged.refresh_token && previous.refresh_token) merged.refresh_token = previous.refresh_token;
  await writeJsonAtomic(tokenPath, merged);
  return merged;
}

async function newOAuthFlow(clientDefinition, tokenPath) {
  const state = crypto.randomBytes(24).toString('hex');
  let oauth2Client;
  let resolveAuth;
  let rejectAuth;
  const completion = new Promise((resolve, reject) => { resolveAuth = resolve; rejectAuth = reject; });

  const server = http.createServer(async (req, res) => {
    try {
      const address = server.address();
      const incoming = new URL(req.url, `http://127.0.0.1:${address.port}`);
      if (incoming.pathname !== '/oauth2callback') {
        res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end('Not found');
        return;
      }
      if (incoming.searchParams.get('state') !== state) throw new Error('OAuth state mismatch.');
      const oauthError = incoming.searchParams.get('error');
      if (oauthError) throw new Error(`OAuth authorization failed: ${oauthError}`);
      const code = incoming.searchParams.get('code');
      if (!code) throw new Error('OAuth callback did not include an authorization code.');
      const { tokens } = await oauth2Client.getToken(code);
      const saved = await saveTokens(tokenPath, tokens);
      oauth2Client.setCredentials(saved);
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end('<!doctype html><meta charset="utf-8"><title>GSC connected</title><h1>החיבור הושלם</h1><p>אפשר לחזור ל-ChatGPT.</p>');
      resolveAuth(oauth2Client);
    } catch (error) {
      res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end('<!doctype html><meta charset="utf-8"><title>GSC error</title><h1>החיבור לא הושלם</h1><p>חזור ל-ChatGPT.</p>');
      rejectAuth(error);
    } finally {
      server.close();
    }
  });

  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolve);
  });
  const address = server.address();
  const redirectUri = `http://127.0.0.1:${address.port}/oauth2callback`;
  oauth2Client = new google.auth.OAuth2(clientDefinition.clientId, clientDefinition.clientSecret, redirectUri);
  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    prompt: 'consent select_account',
    scope: [READONLY_SCOPE],
    state,
  });
  const open = (await import('open')).default;
  await open(authUrl, { wait: false });
  console.log('OAuth opened in the local browser. Waiting for Google approval...');
  return completion;
}

async function authenticate(paths) {
  const definition = await loadClientDefinition(paths.oauthClientPath);
  if (!fs.existsSync(paths.tokenPath)) return newOAuthFlow(definition, paths.tokenPath);

  const existing = await readJson(paths.tokenPath);
  const oauth2Client = new google.auth.OAuth2(definition.clientId, definition.clientSecret);
  oauth2Client.setCredentials(existing);
  oauth2Client.on('tokens', async (tokens) => {
    try { await saveTokens(paths.tokenPath, tokens, existing); } catch (_) { /* surfaced by the active request if material */ }
  });
  try {
    await oauth2Client.getAccessToken();
    return oauth2Client;
  } catch (error) {
    const info = cleanError(error);
    throw new Error(`Saved OAuth token could not be refreshed (status ${info.status || 'unknown'}). A new authorization is required.`);
  }
}

async function paginatedQuery({ sc, siteUrl, requestBody, checkpointDir, resume, label, batchLogFile }) {
  await ensureDir(checkpointDir);
  const stateFile = path.join(checkpointDir, 'state.json');
  let state = { label, nextStartRow: 0, batchFiles: [], complete: false, rowCount: 0, metadata: [] };
  if (resume && fs.existsSync(stateFile)) state = await readJson(stateFile);
  const allRows = [];
  for (const batchFile of state.batchFiles || []) {
    const batch = await readJson(path.join(checkpointDir, batchFile));
    allRows.push(...batch.rows);
  }
  if (resume && state.complete) return { rows: allRows, metadata: state.metadata || [], lastBatchSize: state.lastBatchSize || 0 };

  let startRow = Number(state.nextStartRow || 0);
  let batchNumber = (state.batchFiles || []).length + 1;
  while (true) {
    const startedAt = new Date().toISOString();
    const response = await withRetry(
      () => sc.searchanalytics.query({
        siteUrl,
        requestBody: { ...requestBody, rowLimit: ROW_LIMIT, startRow },
      }),
      { label, startRow, siteUrl },
      batchLogFile,
    );
    const rows = normalizeApiRows(response.data.rows || []);
    const metadata = response.data.metadata || response.data.responseMetadata || null;
    const batchName = `batch-${String(batchNumber).padStart(4, '0')}.json`;
    await writeJsonAtomic(path.join(checkpointDir, batchName), { startRow, rows });
    allRows.push(...rows);
    if (metadata) state.metadata = [...(state.metadata || []), metadata];
    state.batchFiles = [...(state.batchFiles || []), batchName];
    state.rowCount = allRows.length;
    state.lastBatchSize = rows.length;
    state.nextStartRow = startRow + rows.length;
    state.complete = rows.length < ROW_LIMIT;
    state.updatedAt = new Date().toISOString();
    await writeJsonAtomic(stateFile, state);
    await appendJsonLine(batchLogFile, {
      timestamp: state.updatedAt,
      event: 'api_batch',
      label,
      batchNumber,
      startRow,
      returnedRows: rows.length,
      cumulativeRows: allRows.length,
      startedAt,
    });
    if (state.complete) break;
    startRow += rows.length;
    batchNumber += 1;
  }
  return { rows: allRows, metadata: state.metadata || [], lastBatchSize: state.lastBatchSize || 0 };
}

function toMetricObjects(rows, dimensions, extra = {}) {
  return rows.map((row) => {
    const out = { ...extra };
    dimensions.forEach((dimension, index) => { out[dimension] = row.keys[index] || ''; });
    out.clicks = row.clicks;
    out.impressions = row.impressions;
    out.ctr = row.ctr;
    out.position = row.position;
    return out;
  });
}

function dedupeDirect(rows) {
  const map = new Map();
  const duplicates = [];
  for (const row of rows) {
    const key = `${row.query}\u0000${row.page}`;
    if (map.has(key)) {
      duplicates.push({ key, first: map.get(key), duplicate: row });
      continue;
    }
    map.set(key, row);
  }
  return { map, duplicates };
}

function aggregateDaily(rows) {
  const map = new Map();
  const seenPerDay = new Set();
  const duplicates = [];
  for (const row of rows) {
    const key = `${row.query}\u0000${row.page}`;
    const dayKey = `${row.date}\u0000${key}`;
    if (seenPerDay.has(dayKey)) {
      duplicates.push(row);
      continue;
    }
    seenPerDay.add(dayKey);
    const current = map.get(key) || { query: row.query, page: row.page, clicks: 0, impressions: 0, positionNumerator: 0 };
    current.clicks += row.clicks;
    current.impressions += row.impressions;
    current.positionNumerator += row.position * row.impressions;
    map.set(key, current);
  }
  for (const value of map.values()) {
    value.ctr = value.impressions ? value.clicks / value.impressions : 0;
    value.position = value.impressions ? value.positionNumerator / value.impressions : 0;
    delete value.positionNumerator;
  }
  return { map, duplicates };
}

function metricsMatch(a, b) {
  return a.clicks === b.clicks
    && a.impressions === b.impressions
    && Math.abs(a.ctr - b.ctr) < 1e-10
    && Math.abs(a.position - b.position) < 1e-8;
}

function reconcile(directMap, dailyMap) {
  const primary = dailyMap.size > directMap.size ? 'daily_aggregate' : 'direct_full_range';
  const keys = new Set([...directMap.keys(), ...dailyMap.keys()]);
  const rows = [];
  let matchCount = 0;
  let metricDifferenceCount = 0;
  let onlyDirectCount = 0;
  let onlyDailyCount = 0;
  for (const key of keys) {
    const direct = directMap.get(key);
    const daily = dailyMap.get(key);
    let status;
    if (direct && daily) {
      status = metricsMatch(direct, daily) ? 'MATCH' : 'METRIC_DIFFERENCE';
      if (status === 'MATCH') matchCount += 1; else metricDifferenceCount += 1;
    } else if (direct) {
      status = 'ONLY_DIRECT';
      onlyDirectCount += 1;
    } else {
      status = 'ONLY_DAILY';
      onlyDailyCount += 1;
    }
    const selected = primary === 'daily_aggregate' ? (daily || direct) : (direct || daily);
    rows.push({
      query: selected.query,
      page: selected.page,
      direct_clicks: direct?.clicks ?? null,
      direct_impressions: direct?.impressions ?? null,
      direct_ctr: direct?.ctr ?? null,
      direct_position: direct?.position ?? null,
      daily_clicks: daily?.clicks ?? null,
      daily_impressions: daily?.impressions ?? null,
      daily_ctr: daily?.ctr ?? null,
      daily_position: daily?.position ?? null,
      clicks: selected.clicks,
      impressions: selected.impressions,
      ctr: selected.ctr,
      position: selected.position,
      metric_source: selected === daily ? 'daily_aggregate' : 'direct_full_range',
      reconciliation_status: status,
    });
  }
  rows.sort((a, b) => a.query.localeCompare(b.query, 'he') || a.page.localeCompare(b.page));
  return {
    rows,
    primary,
    stats: { matchCount, metricDifferenceCount, onlyDirectCount, onlyDailyCount },
  };
}

function metadataFirstIncomplete(metadataList) {
  const dates = [];
  for (const metadata of metadataList || []) {
    const value = metadata?.firstIncompleteDate || metadata?.first_incomplete_date;
    if (value) dates.push(value);
  }
  return dates.sort()[0] || null;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log(usage());
    return;
  }

  if (!args.listSites) {
    if (!args.site) throw new Error('--site is required for a data pull.');
    assertDate(args.start, '--start');
    assertDate(args.end, '--end');
    if (args.start > args.end) throw new Error('--start must be on or before --end.');
  }
  const searchType = String(args.type || 'web');
  const dataState = String(args.dataState || 'final');
  if (!['final', 'all'].includes(dataState)) throw new Error('--data-state must be final or all.');

  const outputDir = path.resolve(args.outputDir || path.join(os.homedir(), 'Documents', 'GSC-Data', '_registry'));
  const dirs = {
    raw: path.join(outputDir, 'raw'),
    aggregated: path.join(outputDir, 'aggregated'),
    analysis: path.join(outputDir, 'analysis'),
    workbook: path.join(outputDir, 'workbook'),
    logs: path.join(outputDir, 'logs'),
    checkpoints: path.join(outputDir, 'logs', 'checkpoints'),
  };
  await Promise.all(Object.values(dirs).map(ensureDir));
  const batchLogFile = path.join(dirs.logs, 'api-batches.jsonl');
  const manifestFile = path.join(outputDir, 'gsc-run-manifest.json');
  const paths = getCredentialPaths();

  const manifest = {
    script: 'gsc-universal-pull.js',
    scriptVersion: SCRIPT_VERSION,
    nodeVersion: process.version,
    startedAt: new Date().toISOString(),
    status: 'RUNNING',
    readonlyScope: READONLY_SCOPE,
    credentialPaths: { oauthClientPath: paths.oauthClientPath, tokenPath: paths.tokenPath },
    parameters: {
      site: args.site || null,
      start: args.start || null,
      end: args.end || null,
      type: searchType,
      dataState,
      outputDir,
      dailyShards: Boolean(args.dailyShards),
      resume: Boolean(args.resume),
      listSites: Boolean(args.listSites),
    },
  };
  await writeJsonAtomic(manifestFile, manifest);

  try {
    const auth = await authenticate(paths);
    const sc = google.searchconsole({ version: 'v1', auth });
    const sitesResponse = await sc.sites.list();
    const sites = (sitesResponse.data.siteEntry || []).map((site) => ({
      siteUrl: site.siteUrl,
      permissionLevel: site.permissionLevel,
      verifiedAt: new Date().toISOString(),
    }));
    await writeJsonAtomic(path.join(outputDir, 'property-registry-private.json'), { sites });
    manifest.siteCount = sites.length;

    if (args.listSites) {
      console.log(`Found ${sites.length} Search Console properties:`);
      for (const site of sites) console.log(`  ${site.siteUrl} (${site.permissionLevel})`);
      manifest.status = 'COMPLETE';
      manifest.completedAt = new Date().toISOString();
      await writeJsonAtomic(manifestFile, manifest);
      return;
    }

    const selectedSite = sites.find((site) => site.siteUrl === args.site);
    if (!selectedSite) {
      console.error('Requested property was not found. Exact accessible property IDs:');
      for (const site of sites) console.error(`  ${site.siteUrl}`);
      throw new Error(`No exact Search Console property match for ${args.site}.`);
    }
    manifest.property = selectedSite;

    const availabilityFinal = await paginatedQuery({
      sc,
      siteUrl: args.site,
      requestBody: { startDate: args.start, endDate: args.end, dimensions: ['date'], type: searchType, dataState: 'final' },
      checkpointDir: path.join(dirs.checkpoints, 'availability-final'),
      resume: Boolean(args.resume),
      label: 'availability-final',
      batchLogFile,
    });
    const availabilityAll = await paginatedQuery({
      sc,
      siteUrl: args.site,
      requestBody: { startDate: args.start, endDate: args.end, dimensions: ['date'], type: searchType, dataState: 'all' },
      checkpointDir: path.join(dirs.checkpoints, 'availability-all'),
      resume: Boolean(args.resume),
      label: 'availability-all',
      batchLogFile,
    });
    const finalDates = availabilityFinal.rows.map((row) => row.keys[0]).filter(Boolean).sort();
    const allDates = availabilityAll.rows.map((row) => row.keys[0]).filter(Boolean).sort();
    const firstIncompleteDate = metadataFirstIncomplete(availabilityAll.metadata);
    const partialDates = firstIncompleteDate
      ? allDates.filter((date) => date >= firstIncompleteDate)
      : allDates.filter((date) => !finalDates.includes(date));
    const requestedDates = enumerateDates(args.start, args.end);
    manifest.availability = {
      requestedRange: { start: args.start, end: args.end },
      returnedAllRange: { first: allDates[0] || null, last: allDates.at(-1) || null },
      returnedFinalRange: { first: finalDates[0] || null, last: finalDates.at(-1) || null },
      lastFinalDate: finalDates.at(-1) || null,
      firstIncompleteDate,
      partialDates,
      missingDates: requestedDates.filter((date) => !allDates.includes(date)),
    };

    const direct = await paginatedQuery({
      sc,
      siteUrl: args.site,
      requestBody: {
        startDate: args.start,
        endDate: args.end,
        dimensions: ['query', 'page'],
        type: searchType,
        aggregationType: 'auto',
        dataState,
      },
      checkpointDir: path.join(dirs.checkpoints, 'query-page-full-range'),
      resume: Boolean(args.resume),
      label: 'query-page-full-range',
      batchLogFile,
    });
    const directObjects = toMetricObjects(direct.rows, ['query', 'page']);
    const directDeduped = dedupeDirect(directObjects);
    const directRows = [...directDeduped.map.values()];
    const directCsv = path.join(dirs.raw, 'raw-query-page-full-range.csv');
    await writeCsv(directCsv, ['query', 'page', 'clicks', 'impressions', 'ctr', 'position'], directRows);

    const dailyRows = [];
    const dailyStates = [];
    if (args.dailyShards) {
      for (const date of requestedDates) {
        const daily = await paginatedQuery({
          sc,
          siteUrl: args.site,
          requestBody: {
            startDate: date,
            endDate: date,
            dimensions: ['query', 'page'],
            type: searchType,
            aggregationType: 'auto',
            dataState,
          },
          checkpointDir: path.join(dirs.checkpoints, 'daily', date),
          resume: Boolean(args.resume),
          label: `query-page-${date}`,
          batchLogFile,
        });
        const dayObjects = toMetricObjects(daily.rows, ['query', 'page'], { date });
        dailyRows.push(...dayObjects);
        dailyStates.push({ date, rows: dayObjects.length, lastBatchSize: daily.lastBatchSize });
        console.log(`Daily shard ${date}: ${dayObjects.length} rows`);
      }
    }
    const dailyCsv = path.join(dirs.raw, 'raw-query-page-daily.csv');
    await writeCsv(dailyCsv, ['date', 'query', 'page', 'clicks', 'impressions', 'ctr', 'position'], dailyRows);
    const dailyAggregated = aggregateDaily(dailyRows);
    const reconciled = reconcile(directDeduped.map, dailyAggregated.map);
    const reconciledCsv = path.join(dirs.aggregated, 'query-page-reconciled.csv');
    const reconciledColumns = [
      'query', 'page',
      'direct_clicks', 'direct_impressions', 'direct_ctr', 'direct_position',
      'daily_clicks', 'daily_impressions', 'daily_ctr', 'daily_position',
      'clicks', 'impressions', 'ctr', 'position', 'metric_source', 'reconciliation_status',
    ];
    await writeCsv(reconciledCsv, reconciledColumns, reconciled.rows);

    const controls = [
      { name: 'pages', dimensions: ['page'], columns: ['page', 'clicks', 'impressions', 'ctr', 'position'] },
      { name: 'queries', dimensions: ['query'], columns: ['query', 'clicks', 'impressions', 'ctr', 'position'] },
      { name: 'dates', dimensions: ['date'], columns: ['date', 'clicks', 'impressions', 'ctr', 'position'] },
      { name: 'totals', dimensions: [], columns: ['clicks', 'impressions', 'ctr', 'position'] },
    ];
    manifest.controls = {};
    for (const control of controls) {
      const body = {
        startDate: args.start,
        endDate: args.end,
        dimensions: control.dimensions,
        type: searchType,
        dataState,
      };
      if (control.dimensions.includes('page')) body.aggregationType = 'auto';
      const result = await paginatedQuery({
        sc,
        siteUrl: args.site,
        requestBody: body,
        checkpointDir: path.join(dirs.checkpoints, `control-${control.name}`),
        resume: Boolean(args.resume),
        label: `control-${control.name}`,
        batchLogFile,
      });
      const objects = toMetricObjects(result.rows, control.dimensions);
      const file = path.join(dirs.raw, `control-${control.name}.csv`);
      await writeCsv(file, control.columns, objects);
      manifest.controls[control.name] = { rows: objects.length, file };
    }

    manifest.rowCounts = {
      directApiRows: directObjects.length,
      directUniqueKeys: directDeduped.map.size,
      directDuplicateKeys: directDeduped.duplicates.length,
      dailyApiRows: dailyRows.length,
      dailyUniqueKeys: dailyAggregated.map.size,
      dailyDuplicateDayKeys: dailyAggregated.duplicates.length,
      reconciledKeys: reconciled.rows.length,
    };
    manifest.dailyShards = dailyStates;
    manifest.reconciliation = { primarySource: reconciled.primary, ...reconciled.stats };
    manifest.outputFiles = { directCsv, dailyCsv, reconciledCsv, batchLogFile };
    manifest.hashes = {};
    for (const file of [directCsv, dailyCsv, reconciledCsv, ...Object.values(manifest.controls).map((item) => item.file)]) {
      manifest.hashes[path.relative(outputDir, file)] = await sha256(file);
    }
    manifest.status = 'COMPLETE';
    manifest.completedAt = new Date().toISOString();
    await writeJsonAtomic(manifestFile, manifest);
    await fsp.writeFile(`${manifestFile}.sha256`, `${await sha256(manifestFile)}  ${path.basename(manifestFile)}\n`, 'utf8');
    console.log(`GSC pull complete. Output: ${outputDir}`);
  } catch (error) {
    manifest.status = 'FAILED';
    manifest.failedAt = new Date().toISOString();
    manifest.error = cleanError(error);
    await writeJsonAtomic(manifestFile, manifest);
    throw error;
  }
}

main().catch((error) => {
  const info = cleanError(error);
  console.error(`FATAL: ${info.message}`);
  process.exitCode = 1;
});
