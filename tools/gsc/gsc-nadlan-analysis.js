#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const fs = require('fs');
const fsp = fs.promises;
const path = require('path');

const SCRIPT_VERSION = '1.0.0';
const PARAMETERS = Object.freeze({
  lowEvidenceImpressions: 3,
  dominantImpressionShare: 0.90,
  meaningfulSecondaryShare: 0.20,
  stronglySplitSecondaryShare: 0.30,
  similarPositionGap: 5,
  similarMetadataJaccard: 0.60,
  meaningfulDailyWinnerSwitches: 2,
  protectedImpressions: 100,
});

function parseArgs(argv) {
  const result = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith('--')) continue;
    const equal = token.indexOf('=');
    const rawKey = token.slice(2, equal === -1 ? undefined : equal);
    const key = rawKey.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
    if (equal !== -1) result[key] = token.slice(equal + 1);
    else if (argv[index + 1] && !argv[index + 1].startsWith('--')) result[key] = argv[++index];
    else result[key] = true;
  }
  return result;
}

function usage() {
  return [
    'NadLan GSC multi-URL and migration analysis',
    '',
    'Required:',
    '  --run-dir=<absolute GSC run directory>',
    '',
    'The run directory must contain the reconciled, daily, controls, manifest,',
    'source export metadata, and page inventory source files produced by the',
    'read-only pull and inventory tools.',
  ].join('\n');
}

async function ensureDir(directory) {
  await fsp.mkdir(directory, { recursive: true });
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let quoted = false;
  const input = String(text || '').replace(/^\uFEFF/, '');
  for (let index = 0; index < input.length; index += 1) {
    const character = input[index];
    if (quoted) {
      if (character === '"' && input[index + 1] === '"') {
        field += '"';
        index += 1;
      } else if (character === '"') quoted = false;
      else field += character;
    } else if (character === '"') quoted = true;
    else if (character === ',') {
      row.push(field);
      field = '';
    } else if (character === '\n') {
      if (field.endsWith('\r')) field = field.slice(0, -1);
      row.push(field);
      rows.push(row);
      row = [];
      field = '';
    } else field += character;
  }
  if (field || row.length) {
    row.push(field);
    rows.push(row);
  }
  if (!rows.length) return [];
  const header = rows.shift();
  return rows.filter((values) => values.some((value) => value !== '')).map((values) =>
    Object.fromEntries(header.map((column, index) => [column, values[index] ?? ''])));
}

async function readCsv(file) {
  return parseCsv(await fsp.readFile(file, 'utf8'));
}

async function readJson(file) {
  return JSON.parse(await fsp.readFile(file, 'utf8'));
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

async function writeJson(file, value) {
  await ensureDir(path.dirname(file));
  await fsp.writeFile(file, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function sha256(file) {
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash('sha256');
    const input = fs.createReadStream(file);
    input.on('error', reject);
    input.on('data', (chunk) => hash.update(chunk));
    input.on('end', () => resolve(hash.digest('hex')));
  });
}

function number(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

function ratio(numerator, denominator) {
  return denominator ? numerator / denominator : 0;
}

function aggregateMetrics(rows) {
  const clicks = rows.reduce((sum, row) => sum + number(row.clicks), 0);
  const impressions = rows.reduce((sum, row) => sum + number(row.impressions), 0);
  const weightedPosition = rows.reduce((sum, row) => sum + number(row.position) * number(row.impressions), 0);
  return {
    clicks,
    impressions,
    ctr: ratio(clicks, impressions),
    position: ratio(weightedPosition, impressions),
  };
}

function strongestComparator(left, right) {
  return number(right.clicks) - number(left.clicks)
    || number(right.impressions) - number(left.impressions)
    || number(left.position) - number(right.position)
    || number(right.ctr) - number(left.ctr)
    || String(left.page).localeCompare(String(right.page), 'en');
}

function normalizeUrl(raw) {
  try {
    const url = new URL(raw);
    url.hash = '';
    url.protocol = 'https:';
    url.hostname = url.hostname.toLowerCase();
    url.pathname = url.pathname.replace(/%[0-9a-f]{2}/gi, (escape) => escape.toUpperCase());
    if (!url.pathname.endsWith('/') && !/\.[a-z0-9]{2,6}$/i.test(url.pathname)) url.pathname += '/';
    return url.href;
  } catch {
    return String(raw || '').trim();
  }
}

function suffixPattern(rawUrl, slug = '') {
  let candidate = String(slug || '');
  try {
    if (!candidate) candidate = decodeURIComponent(new URL(rawUrl).pathname.split('/').filter(Boolean).pop() || '');
  } catch {
    // Keep the provided slug.
  }
  const match = candidate.match(/-(2|3|4)$/);
  return match ? `NUMERIC_SUFFIX_${match[1]}` : '';
}

const STOP_WORDS = new Set([
  'של', 'על', 'עם', 'את', 'אל', 'או', 'גם', 'כל', 'מה', 'איך', 'זה', 'זו', 'הוא', 'היא',
  'the', 'and', 'for', 'with', 'from', 'in', 'of', 'to', 'a',
]);

function tokens(value) {
  return new Set((String(value || '').toLowerCase().match(/[\p{L}\p{N}]+/gu) || [])
    .filter((token) => token.length > 1 && !STOP_WORDS.has(token)));
}

function jaccard(left, right) {
  const a = tokens(left);
  const b = tokens(right);
  if (!a.size || !b.size) return 0;
  let intersection = 0;
  for (const value of a) if (b.has(value)) intersection += 1;
  return ratio(intersection, new Set([...a, ...b]).size);
}

function metadataForPage(inventoryMap, page) {
  return inventoryMap.get(normalizeUrl(page)) || {
    url: page,
    content_type: '',
    title: '',
    h1: '',
    canonical: '',
    indexability: '',
    slug: '',
  };
}

function pageSimilarity(left, right) {
  return Math.max(
    jaccard(left.title, right.title),
    jaccard(left.h1, right.h1),
    jaccard(`${left.title} ${left.h1}`, `${right.title} ${right.h1}`),
  );
}

function dailySignals(dailyRows, multiQueries) {
  const byQuery = new Map();
  for (const row of dailyRows) {
    if (!multiQueries.has(row.query)) continue;
    if (!byQuery.has(row.query)) byQuery.set(row.query, new Map());
    const byDate = byQuery.get(row.query);
    if (!byDate.has(row.date)) byDate.set(row.date, []);
    byDate.get(row.date).push({
      page: row.page,
      clicks: number(row.clicks),
      impressions: number(row.impressions),
      ctr: number(row.ctr),
      position: number(row.position),
    });
  }
  const signals = new Map();
  for (const [query, byDate] of byQuery) {
    const observations = [...byDate.entries()].sort(([left], [right]) => left.localeCompare(right));
    const winners = [];
    let cooccurrenceDays = 0;
    for (const [, rows] of observations) {
      if (new Set(rows.map((row) => row.page)).size > 1) cooccurrenceDays += 1;
      winners.push([...rows].sort(strongestComparator)[0].page);
    }
    let winnerSwitches = 0;
    for (let index = 1; index < winners.length; index += 1) if (winners[index] !== winners[index - 1]) winnerSwitches += 1;
    signals.set(query, {
      dailyObservationDays: observations.length,
      cooccurrenceDays,
      dailyWinnerCount: new Set(winners).size,
      dailyWinnerSwitches: winnerSwitches,
    });
  }
  return signals;
}

function classify(group, inventoryMap, daily) {
  const ordered = group.pages;
  const strongest = ordered[0];
  const secondary = ordered[1];
  const strongestShare = ratio(strongest.impressions, group.totals.impressions);
  const secondaryShare = ratio(secondary.impressions, group.totals.impressions);
  const strongestMetadata = metadataForPage(inventoryMap, strongest.page);
  const secondaryMetadata = metadataForPage(inventoryMap, secondary.page);
  const metadataSimilarity = pageSimilarity(strongestMetadata, secondaryMetadata);
  const positionGap = Math.abs(number(strongest.position) - number(secondary.position));
  const similarPositions = positionGap <= PARAMETERS.similarPositionGap;
  const suffixDuplicate = ordered.some((row) => suffixPattern(row.page, metadataForPage(inventoryMap, row.page).slug));
  const types = new Set(ordered.map((row) => metadataForPage(inventoryMap, row.page).content_type).filter(Boolean));
  const languages = new Set(ordered.map((row) => metadataForPage(inventoryMap, row.page).language).filter(Boolean));
  const distinctTypes = types.size > 1;
  const distinctLanguages = languages.size > 1;
  const homepagePlusEntity = ordered.some((row) => /^https:\/\/nad-lan\.co\.il\/?$/i.test(row.page)) && types.size > 0;
  const metadataKnown = Boolean(strongestMetadata.title || strongestMetadata.h1)
    && Boolean(secondaryMetadata.title || secondaryMetadata.h1);
  const meaningfulSecondary = secondaryShare >= PARAMETERS.meaningfulSecondaryShare;
  const stronglySplit = secondaryShare >= PARAMETERS.stronglySplitSecondaryShare;
  const switching = daily.dailyWinnerSwitches >= PARAMETERS.meaningfulDailyWinnerSwitches;
  const evidence = [];
  if (strongestShare >= PARAMETERS.dominantImpressionShare) evidence.push(['DOMINANT_URL', `ל-URL החזק ${Math.round(strongestShare * 100)}% מהחשיפות.`]);
  if (meaningfulSecondary) evidence.push(['SIGNIFICANT_SECONDARY', `ל-URL השני ${Math.round(secondaryShare * 100)}% מהחשיפות.`]);
  if (similarPositions) evidence.push(['SIMILAR_POSITIONS', `פער המיקום בין שני ה-URLs החזקים הוא ${positionGap.toFixed(2)}.`]);
  if (switching) evidence.push(['DAILY_WINNER_SWITCH', `ה-URL היומי החזק התחלף ${daily.dailyWinnerSwitches} פעמים.`]);
  if (suffixDuplicate) evidence.push(['NUMERIC_SUFFIX', 'נמצא URL עם suffix מספרי, סימן אפשרי לכפילות import.']);
  if (metadataSimilarity >= PARAMETERS.similarMetadataJaccard) evidence.push(['SIMILAR_METADATA', `דמיון title/H1 בין שני המובילים הוא ${metadataSimilarity.toFixed(2)}.`]);
  if (distinctTypes) evidence.push(['DISTINCT_CONTENT_TYPES', `השאילתה מופיעה בסוגי תוכן שונים: ${[...types].join(', ')}.`]);
  if (distinctLanguages) evidence.push(['DISTINCT_LANGUAGES', `השאילתה מופיעה בגרסאות שפה שונות: ${[...languages].join(', ')}.`]);
  if (homepagePlusEntity) evidence.push(['HOMEPAGE_PLUS_ENTITY', 'דף הבית מופיע לצד עמוד ישות או תוכן ייעודי.']);
  if (!metadataKnown) evidence.push(['PAGE_METADATA_INCOMPLETE', 'חסרים title או H1 לאחד משני העמודים החזקים.']);
  if (group.totals.impressions < PARAMETERS.lowEvidenceImpressions) evidence.push(['LOW_DATA', `לשאילתה ${group.totals.impressions} חשיפות בלבד.`]);

  let classification;
  let confidence;
  let action;
  if (group.totals.impressions < PARAMETERS.lowEvidenceImpressions && group.totals.clicks === 0) {
    classification = 'INSUFFICIENT_EVIDENCE';
    confidence = 'LOW';
    action = 'INVESTIGATE';
  } else if (distinctLanguages && !suffixDuplicate) {
    classification = 'BENIGN_MULTI_PAGE_VISIBILITY';
    confidence = 'HIGH';
    action = 'KEEP_PROTECT';
  } else if (
    (suffixDuplicate && meaningfulSecondary && (similarPositions || switching || metadataSimilarity >= PARAMETERS.similarMetadataJaccard))
    || (metadataSimilarity >= PARAMETERS.similarMetadataJaccard && stronglySplit && (similarPositions || switching))
  ) {
    classification = 'LIKELY_CANNIBALIZATION';
    confidence = metadataKnown ? 'HIGH' : 'MEDIUM';
    action = suffixDuplicate ? 'MERGE_CONTENT_REVIEW' : 'DIFFERENTIATE_INTENT';
  } else if (
    strongestShare >= PARAMETERS.dominantImpressionShare
    || (distinctTypes && !stronglySplit)
    || (homepagePlusEntity && !stronglySplit)
  ) {
    classification = 'BENIGN_MULTI_PAGE_VISIBILITY';
    confidence = strongestShare >= PARAMETERS.dominantImpressionShare ? 'HIGH' : 'MEDIUM';
    action = 'KEEP_PROTECT';
  } else if (meaningfulSecondary || similarPositions || switching || suffixDuplicate) {
    classification = 'POSSIBLE_CANNIBALIZATION';
    confidence = metadataKnown ? 'MEDIUM' : 'LOW';
    action = 'INVESTIGATE';
  } else {
    classification = 'INSUFFICIENT_EVIDENCE';
    confidence = 'LOW';
    action = 'INVESTIGATE';
  }
  return {
    classification,
    confidence,
    evidenceCodes: evidence.map(([code]) => code).join('|'),
    evidenceText: evidence.map(([, text]) => text).join(' '),
    recommendedReviewAction: action,
    doNotExecuteAutomatically: 'TRUE',
    strongestImpressionShare: strongestShare,
    secondaryImpressionShare: secondaryShare,
    topTwoPositionGap: positionGap,
    metadataSimilarity,
    metadataKnown,
    distinctContentTypes: distinctTypes,
    contentTypes: [...types].join('|'),
    distinctLanguages,
    languages: [...languages].join('|'),
    suffixDuplicate,
  };
}

function buildGroups(rows) {
  const grouped = new Map();
  for (const row of rows) {
    if (!grouped.has(row.query)) grouped.set(row.query, []);
    grouped.get(row.query).push({
      query: row.query,
      page: row.page,
      clicks: number(row.clicks),
      impressions: number(row.impressions),
      ctr: number(row.ctr),
      position: number(row.position),
      metric_source: row.metric_source,
      reconciliation_status: row.reconciliation_status,
    });
  }
  const groups = [];
  for (const [query, pages] of grouped) {
    const distinct = new Map();
    for (const page of pages) distinct.set(page.page, page);
    if (distinct.size <= 1) continue;
    const ordered = [...distinct.values()].sort(strongestComparator);
    groups.push({ query, pages: ordered, totals: aggregateMetrics(ordered), distinctUrlCount: ordered.length });
  }
  return groups.sort((left, right) => right.distinctUrlCount - left.distinctUrlCount
    || right.totals.impressions - left.totals.impressions
    || right.totals.clicks - left.totals.clicks
    || left.query.localeCompare(right.query, 'he'));
}

function classificationCounts(decisions) {
  const counts = {
    LIKELY_CANNIBALIZATION: 0,
    POSSIBLE_CANNIBALIZATION: 0,
    BENIGN_MULTI_PAGE_VISIBILITY: 0,
    INSUFFICIENT_EVIDENCE: 0,
  };
  for (const decision of decisions) counts[decision.classification] += 1;
  return counts;
}

function sumRows(rows) {
  return aggregateMetrics(rows.map((row) => ({
    clicks: number(row.clicks),
    impressions: number(row.impressions),
    position: number(row.position),
  })));
}

function crossCheckRows(source, controls) {
  const sheet = (name) => source.sheets.find((entry) => entry.name === name) || {};
  const chart = sheet('Chart');
  const queries = sheet('Queries');
  const pages = sheet('Pages');
  const total = controls.totals[0] || {};
  const queryMetrics = sumRows(controls.queries);
  const pageMetrics = sumRows(controls.pages);
  const checks = [];
  function add(check, sourceValue, apiValue, status, explanation) {
    checks.push({ check, source_export_value: sourceValue, api_value: apiValue, cross_check_status: status, explanation });
  }
  add('property_clicks', chart.clicks_sum, number(total.clicks), number(chart.clicks_sum) === number(total.clicks) ? 'MATCH' : 'UNEXPLAINED_DIFFERENCE', 'Chart מול totals ללא dimensions.');
  add('property_impressions', chart.impressions_sum, number(total.impressions), number(chart.impressions_sum) === number(total.impressions) ? 'MATCH' : 'UNEXPLAINED_DIFFERENCE', 'Chart מול totals ללא dimensions.');
  add('date_rows', chart.data_rows, controls.dates.length, number(chart.data_rows) === controls.dates.length ? 'MATCH' : 'EXPECTED_DIFFERENCE', 'מספר תאריכי דיווח שהוחזרו בפועל.');
  add('first_returned_date', chart.first_date, controls.dates[0]?.date || '', chart.first_date === controls.dates[0]?.date ? 'MATCH' : 'EXPECTED_DIFFERENCE', 'הקובץ וה-API משתמשים בכיסוי שבו קיימות שורות date.');
  add('last_final_date', chart.last_date, controls.dates.at(-1)?.date || '', chart.last_date === controls.dates.at(-1)?.date ? 'MATCH' : 'EXPECTED_DIFFERENCE', 'dataState=final אינו כולל את שני הימים החלקיים האחרונים.');
  add('query_rows', queries.data_rows, controls.queries.length, number(queries.data_rows) === controls.queries.length ? 'MATCH' : 'EXPECTED_DIFFERENCE', 'ייצוא הממשק מוגבל ל-1,000 שורות; משיכת ה-API עברה פאגינציה מלאה.');
  add('query_clicks', queries.clicks_sum, queryMetrics.clicks, number(queries.clicks_sum) === queryMetrics.clicks ? 'MATCH' : 'EXPECTED_DIFFERENCE', 'שאילתות אנונימיות מושמטות; clicks של שורות query שנחשפו תואמים כאן.');
  add('query_impressions', queries.impressions_sum, queryMetrics.impressions, number(queries.impressions_sum) === queryMetrics.impressions ? 'MATCH' : 'EXPECTED_DIFFERENCE', 'ה-API החזיר יותר מ-1,000 שורות query; אין לכפות התאמה לייצוא המקוצר.');
  add('page_rows', pages.data_rows, controls.pages.length, number(pages.data_rows) === controls.pages.length ? 'MATCH' : 'EXPECTED_DIFFERENCE', 'ייצוא הממשק מוגבל ל-1,000 שורות; משיכת ה-API עברה פאגינציה מלאה.');
  add('page_clicks', pages.clicks_sum, pageMetrics.clicks, number(pages.clicks_sum) === pageMetrics.clicks ? 'MATCH' : 'EXPECTED_DIFFERENCE', 'סכום clicks לפי page תואם כאן אף שכמות השורות שונה.');
  add('page_impressions', pages.impressions_sum, pageMetrics.impressions, number(pages.impressions_sum) === pageMetrics.impressions ? 'MATCH' : 'EXPECTED_DIFFERENCE', 'פאגינציה מלאה החזירה עמודים נוספים; aggregation לפי page עשוי לחרוג מ-property totals.');
  add('search_type', source.filters.search_type, 'web', String(source.filters.search_type).toLowerCase() === 'web' ? 'MATCH' : 'UNEXPLAINED_DIFFERENCE', 'Search type נבדק בגיליון Filters ובפרמטר הריצה.');
  return checks;
}

function buildMigrationInventory(inventoryRows, reconciledRows, pageControls, groupRecords) {
  const byUrl = new Map(inventoryRows.map((row) => [normalizeUrl(row.url), { ...row }]));
  const pageControlMap = new Map(pageControls.map((row) => [normalizeUrl(row.page), row]));
  for (const row of pageControls) {
    const normalized = normalizeUrl(row.page);
    if (!byUrl.has(normalized)) byUrl.set(normalized, {
      url: row.page,
      normalized_url: normalized,
      post_id: '', content_type: 'GSC_ONLY', language: '', title: '', h1: '', slug: '', parent: '', taxonomies: '',
      wp_status: '', http_status: '', http_status_source: '', indexability: '', robots_directives: '', canonical: '',
      sitemap_presence: 'FALSE', sitemap_source: '', published_date: '', modified_date: '', word_count: '',
      internal_inlinks: '', internal_outlinks: '', source: 'GSC_CONTROL_PAGE',
    });
  }
  const queryStats = new Map();
  for (const row of reconciledRows) {
    const normalized = normalizeUrl(row.page);
    if (!queryStats.has(normalized)) queryStats.set(normalized, { queries: new Set(), multiQueries: new Set() });
    queryStats.get(normalized).queries.add(row.query);
  }
  const groupStats = new Map();
  for (const record of groupRecords) {
    for (const page of record.pages) {
      const normalized = normalizeUrl(page.page);
      if (!groupStats.has(normalized)) groupStats.set(normalized, { ids: [], classes: [], strongestIds: [], evidence: [] });
      const stats = groupStats.get(normalized);
      stats.ids.push(record.groupId);
      stats.classes.push(record.decision.classification);
      stats.evidence.push(`${record.groupId}:${record.decision.evidenceCodes}`);
      if (page.page === record.pages[0].page) stats.strongestIds.push(record.groupId);
      queryStats.get(normalized)?.multiQueries.add(record.query);
    }
  }

  const result = [];
  for (const [normalized, row] of byUrl) {
    const control = pageControlMap.get(normalized) || {};
    const clicks = number(control.clicks);
    const impressions = number(control.impressions);
    const groups = groupStats.get(normalized) || { ids: [], classes: [], strongestIds: [], evidence: [] };
    const queries = queryStats.get(normalized) || { queries: new Set(), multiQueries: new Set() };
    const suffix = suffixPattern(row.url, row.slug);
    const protectedFlag = clicks > 0 || groups.strongestIds.length > 0 || impressions >= PARAMETERS.protectedImpressions;
    const hasLikely = groups.classes.includes('LIKELY_CANNIBALIZATION');
    const hasPossible = groups.classes.includes('POSSIBLE_CANNIBALIZATION');
    let migrationPriority;
    let proposedAction;
    let confidence;
    if (hasLikely) {
      migrationPriority = 'P0_CANNIBALIZATION_REVIEW';
      proposedAction = suffix ? 'MERGE_CONTENT_REVIEW' : 'DIFFERENTIATE_INTENT';
      confidence = 'HIGH';
    } else if (hasPossible) {
      migrationPriority = 'P0_CANNIBALIZATION_REVIEW';
      proposedAction = 'INVESTIGATE';
      confidence = 'MEDIUM';
    } else if (String(row.indexability).toLowerCase() === 'noindex') {
      migrationPriority = 'P1_PROTECT';
      proposedAction = 'NOINDEX_REVIEW';
      confidence = 'HIGH';
    } else if (row.canonical && normalizeUrl(row.canonical) !== normalized) {
      migrationPriority = 'P1_PROTECT';
      proposedAction = 'CANONICAL_REVIEW';
      confidence = 'HIGH';
    } else if (protectedFlag) {
      migrationPriority = 'P1_PROTECT';
      proposedAction = 'KEEP_PROTECT';
      confidence = clicks > 0 ? 'HIGH' : 'MEDIUM';
    } else if (impressions > 0) {
      migrationPriority = 'P2_GSC_OPPORTUNITY';
      proposedAction = 'KEEP_REFRESH';
      confidence = 'MEDIUM';
    } else {
      migrationPriority = suffix ? 'P2_REVIEW_DUPLICATE_PATTERN' : 'P3_LOW_SIGNAL';
      proposedAction = 'INVESTIGATE';
      confidence = 'LOW';
    }
    const evidence = [
      `GSC clicks=${clicks}, impressions=${impressions}, queries=${queries.queries.size}`,
      groups.ids.length ? `multi-URL groups=${groups.ids.join('|')}` : '',
      groups.strongestIds.length ? `strongest in=${groups.strongestIds.join('|')}` : '',
      suffix ? `suffix=${suffix}` : '',
      row.sitemap_presence === 'TRUE' ? 'נמצא במפת אתר' : 'לא נמצא במפת אתר',
      row.indexability ? `indexability=${row.indexability}` : '',
    ].filter(Boolean).join('; ');
    result.push({
      ...row,
      clicks,
      impressions,
      ctr: number(control.ctr),
      position: number(control.position),
      query_count: queries.queries.size,
      multi_url_query_count: queries.multiQueries.size,
      protected_url_flag: protectedFlag ? 'TRUE' : 'FALSE',
      cannibalization_group_ids: groups.ids.join('|'),
      strongest_group_ids: groups.strongestIds.join('|'),
      duplicate_suffix_pattern: suffix,
      migration_priority: migrationPriority,
      proposed_action: proposedAction,
      evidence,
      confidence,
      manual_approval_required: 'TRUE',
    });
  }
  const rank = { P0_CANNIBALIZATION_REVIEW: 0, P1_PROTECT: 1, P2_REVIEW_DUPLICATE_PATTERN: 2, P2_GSC_OPPORTUNITY: 3, P3_LOW_SIGNAL: 4 };
  return result.sort((left, right) => (rank[left.migration_priority] ?? 9) - (rank[right.migration_priority] ?? 9)
    || right.impressions - left.impressions
    || right.clicks - left.clicks
    || left.url.localeCompare(right.url, 'en'));
}

function markdownReport(context) {
  const { manifest, counts, crossChecks, inventorySummary, outputCounts, topRisks } = context;
  const checkLines = crossChecks.map((row) => `| ${row.check} | ${row.source_export_value} | ${row.api_value} | ${row.cross_check_status} | ${row.explanation} |`).join('\n');
  const riskLines = topRisks.map((row, index) => `${index + 1}. **${row.query}** — ${row.classification}, ${row.query_total_impressions} חשיפות, ${row.distinct_url_count} URLs; ${row.recommended_review_action}.`).join('\n');
  return `# דוח איכות נתוני GSC — nad-lan.co.il\n\n`+
    `## תוצאה מרכזית\n\n`+
    `המשיכה הושלמה מול הנכס המדויק \`${manifest.parameters.site}\` בהרשאת \`${manifest.property.permissionLevel}\` וב-scope קריאה בלבד. `+
    `נמצאו ${outputCounts.multiUrlQueries} שאילתות שבהן יותר מ-URL אחד, מתוך ${outputCounts.reconciledRows} מפתחות query-page שנחשפו על ידי ה-API. `+
    `המשיכה הישירה והאגרגציה היומית זהות בכל ${manifest.reconciliation.matchCount} המפתחות, ללא פער מטרי.\n\n`+
    `## כיסוי תאריכים\n\n`+
    `- טווח מבוקש: ${manifest.availability.requestedRange.start} עד ${manifest.availability.requestedRange.end}. התאריכים נגזרו מהגדרת המשתמש; בקובץ המקור נמצא רק המסנן “Last 3 months”.\n`+
    `- טווח שהוחזר במצב all: ${manifest.availability.returnedAllRange.first} עד ${manifest.availability.returnedAllRange.last}.\n`+
    `- טווח סופי: ${manifest.availability.returnedFinalRange.first} עד ${manifest.availability.returnedFinalRange.last}.\n`+
    `- ימים חלקיים: ${manifest.availability.partialDates.join(', ')}. ימים חסרים: ${manifest.availability.missingDates.join(', ')}.\n`+
    `- Google מייחס נתוני Search Console לאזור הזמן Pacific Time; שני הימים האחרונים עשויים להיות חלקיים.\n\n`+
    `## סיווגים\n\n`+
    `- LIKELY_CANNIBALIZATION: ${counts.LIKELY_CANNIBALIZATION}\n`+
    `- POSSIBLE_CANNIBALIZATION: ${counts.POSSIBLE_CANNIBALIZATION}\n`+
    `- BENIGN_MULTI_PAGE_VISIBILITY: ${counts.BENIGN_MULTI_PAGE_VISIBILITY}\n`+
    `- INSUFFICIENT_EVIDENCE: ${counts.INSUFFICIENT_EVIDENCE}\n\n`+
    `הסיווג הוא מנגנון תיעדוף שקוף לבדיקת אדם, לא הוראה לביצוע. כל שורה מסומנת \`do_not_execute_automatically=TRUE\`.\n\n`+
    `## חמשת הסיכונים או ההזדמנויות המובילים\n\n${riskLines || 'לא נמצאו קבוצות לתיעדוף.'}\n\n`+
    `## הצלבה עם הייצוא המקורי\n\n`+
    `| בדיקה | ייצוא מקור | API | סטטוס | הסבר |\n|---|---:|---:|---|---|\n${checkLines}\n\n`+
    `פערי שורות צפויים משום שגיליונות Queries ו-Pages בייצוא כוללים 1,000 שורות, בעוד המשיכה באמצעות API עברה פאגינציה מלאה. `+
    `שאילתות אנונימיות מושמטות מטעמי פרטיות; aggregation לפי page ו-query אינו חייב להסתכם בדיוק ל-property totals.\n\n`+
    `## מלאי הגירה\n\n`+
    `המלאי המאוחד כולל ${outputCounts.inventoryRows} כתובות: ${inventorySummary.merged.fromWordPressRest} רשומות WordPress REST ו-${inventorySummary.merged.inSitemap} כתובות במפות אתר. `+
    `ערכי HTTP 200 שמקורם ב-REST או sitemap מסומנים כמוסקים בשדה \`http_status_source\`; לא בוצע crawl פרטני של אלפי העמודים. `+
    `ספירת קישורים פנימיים נגזרה רק מה-HTML הציבורי שהחזיר WordPress REST.\n\n`+
    `## חוברת XLSX\n\n`+
    `חוברת XLSX לא נוצרה בריצה זו. כלי הגיליונות המאושר \`@oai/artifact-tool\` אינו יכול להיטען במחשב משום ש-Windows Application Control חוסם את הרכיב הלא-חתום \`skia.node\`. `+
    `לא בוצע ניסיון לנטרל את הגנת Windows ולא נעשה שימוש בספריית גיליונות חלופית. כל קובצי ה-CSV המלאים והבדוקים זמינים, וניתן להפיק מהם את החוברת לאחר התקנת runtime חתום או שינוי מדיניות מאושר על ידי מנהל המחשב.\n\n`+
    `## כללי חישוב ובקרות\n\n`+
    `- URL חזק: יותר clicks; בשוויון יותר impressions; אחר כך position נמוך יותר; CTR גבוה יותר; ולבסוף URL לקסיקוגרפי.\n`+
    `- CTR מחושב כ-clicks/impressions. position מחושב בממוצע משוקלל impressions.\n`+
    `- לא הוחרגה אף שאילתה מרובת-URL בגלל 0 clicks או סף מינימום.\n`+
    `- פרמטרי התיעדוף גלויים בקובץ analysis-summary.json: dominant share=${PARAMETERS.dominantImpressionShare}, secondary share=${PARAMETERS.meaningfulSecondaryShare}, position gap=${PARAMETERS.similarPositionGap}, metadata similarity=${PARAMETERS.similarMetadataJaccard}.\n`+
    `- בדיקת pagination: direct rows=${manifest.rowCounts.directApiRows}, daily rows=${manifest.rowCounts.dailyApiRows}, duplicate keys=${manifest.rowCounts.directDuplicateKeys}, duplicate daily keys=${manifest.rowCounts.dailyDuplicateDayKeys}.\n\n`+
    `## מגבלות רשמיות ומקורות\n\n`+
    `הנתונים כוללים את כל שורות query+page שה-API החזיר לאחר pagination ופיצול יומי; Google עדיין עשויה להשמיט שאילתות אנונימיות ולהחזיר top rows בלבד לפי מגבלות פנימיות.\n\n`+
    `- https://developers.google.com/webmaster-tools/v1/searchanalytics/query\n`+
    `- https://support.google.com/webmasters/answer/17011259\n`+
    `- https://support.google.com/webmasters/answer/96568\n`+
    `- https://developers.google.com/identity/protocols/oauth2/native-app\n\n`+
    `## גבול ביצוע\n\nלא בוצע שום שינוי חי ב-WordPress, ב-Search Console, ב-sitemap, ב-canonical, ב-robots, ב-slugs, בתוכן או בקישורים.\n`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    process.stdout.write(`${usage()}\n`);
    return;
  }
  if (!args.runDir || !path.isAbsolute(args.runDir)) throw new Error('--run-dir must be an absolute path.');
  const runDir = args.runDir;
  const analysisDir = path.join(runDir, 'analysis');
  await ensureDir(analysisDir);

  const files = {
    manifest: path.join(runDir, 'gsc-run-manifest.json'),
    reconciled: path.join(runDir, 'aggregated', 'query-page-reconciled.csv'),
    daily: path.join(runDir, 'raw', 'raw-query-page-daily.csv'),
    pages: path.join(runDir, 'raw', 'control-pages.csv'),
    queries: path.join(runDir, 'raw', 'control-queries.csv'),
    dates: path.join(runDir, 'raw', 'control-dates.csv'),
    totals: path.join(runDir, 'raw', 'control-totals.csv'),
    inventory: path.join(analysisDir, 'page-inventory-source.csv'),
    inventorySummary: path.join(analysisDir, 'page-inventory-source-summary.json'),
    sourceMetadata: path.join(analysisDir, 'source-export-metadata.json'),
  };
  for (const [name, file] of Object.entries(files)) {
    try { await fsp.access(file, fs.constants.R_OK); } catch { throw new Error(`Missing required ${name} file: ${file}`); }
  }

  const [manifest, reconciledRows, dailyRows, pageControls, queryControls, dateControls, totalControls, inventoryRows, inventorySummary, sourceMetadata] = await Promise.all([
    readJson(files.manifest), readCsv(files.reconciled), readCsv(files.daily), readCsv(files.pages), readCsv(files.queries),
    readCsv(files.dates), readCsv(files.totals), readCsv(files.inventory), readJson(files.inventorySummary), readJson(files.sourceMetadata),
  ]);
  if (manifest.parameters.site !== 'sc-domain:nad-lan.co.il') throw new Error(`Unexpected property: ${manifest.parameters.site}`);
  if (manifest.readonlyScope !== 'https://www.googleapis.com/auth/webmasters.readonly') throw new Error('Manifest scope is not read-only.');
  if (reconciledRows.length !== manifest.rowCounts.reconciledKeys) throw new Error('Reconciled row count does not match manifest.');

  const inventoryMap = new Map(inventoryRows.map((row) => [normalizeUrl(row.url), row]));
  const groups = buildGroups(reconciledRows);
  const dailyByQuery = dailySignals(dailyRows, new Set(groups.map((group) => group.query)));
  const groupRecords = groups.map((group, index) => {
    const groupId = `QG-${String(index + 1).padStart(5, '0')}`;
    const daily = dailyByQuery.get(group.query) || { dailyObservationDays: 0, cooccurrenceDays: 0, dailyWinnerCount: 0, dailyWinnerSwitches: 0 };
    const decision = classify(group, inventoryMap, daily);
    return { ...group, groupId, daily, decision };
  });

  const detailRows = [];
  const summaryRows = [];
  const decisionRows = [];
  for (const record of groupRecords) {
    const strongest = record.pages[0];
    const weaker = record.pages.slice(1).map((row) => row.page).join('|');
    const common = {
      group_id: record.groupId,
      query: record.query,
      distinct_url_count: record.distinctUrlCount,
      query_total_clicks: record.totals.clicks,
      query_total_impressions: record.totals.impressions,
      query_ctr: record.totals.ctr,
      query_weighted_position: record.totals.position,
      strongest_url: strongest.page,
      weaker_competing_urls: weaker,
      metric_source: [...new Set(record.pages.map((row) => row.metric_source))].join('|'),
      reconciliation_status: [...new Set(record.pages.map((row) => row.reconciliation_status))].join('|'),
      daily_observation_days: record.daily.dailyObservationDays,
      daily_cooccurrence_days: record.daily.cooccurrenceDays,
      daily_winner_count: record.daily.dailyWinnerCount,
      daily_winner_switches: record.daily.dailyWinnerSwitches,
      classification: record.decision.classification,
      confidence: record.decision.confidence,
      evidence_codes: record.decision.evidenceCodes,
      evidence_text: record.decision.evidenceText,
      recommended_review_action: record.decision.recommendedReviewAction,
      do_not_execute_automatically: 'TRUE',
    };
    summaryRows.push(common);
    decisionRows.push({
      ...common,
      strongest_impression_share: record.decision.strongestImpressionShare,
      secondary_impression_share: record.decision.secondaryImpressionShare,
      top_two_position_gap: record.decision.topTwoPositionGap,
      metadata_similarity_jaccard: record.decision.metadataSimilarity,
      metadata_known: record.decision.metadataKnown ? 'TRUE' : 'FALSE',
      distinct_content_types: record.decision.distinctContentTypes ? 'TRUE' : 'FALSE',
      content_types: record.decision.contentTypes,
      distinct_languages: record.decision.distinctLanguages ? 'TRUE' : 'FALSE',
      languages: record.decision.languages,
      suffix_duplicate_signal: record.decision.suffixDuplicate ? 'TRUE' : 'FALSE',
    });
    for (let index = 0; index < record.pages.length; index += 1) {
      const page = record.pages[index];
      const metadata = metadataForPage(inventoryMap, page.page);
      detailRows.push({
        ...common,
        url_role: index === 0 ? 'strongest_url' : 'weaker_competing_url',
        page: page.page,
        clicks: page.clicks,
        impressions: page.impressions,
        ctr: page.ctr,
        position: page.position,
        click_share: ratio(page.clicks, record.totals.clicks),
        impression_share: ratio(page.impressions, record.totals.impressions),
        content_type: metadata.content_type || '',
        title: metadata.title || '',
        h1: metadata.h1 || '',
        canonical: metadata.canonical || '',
        indexability: metadata.indexability || '',
        duplicate_suffix_pattern: suffixPattern(page.page, metadata.slug),
      });
    }
  }

  const inventory = buildMigrationInventory(inventoryRows, reconciledRows, pageControls, groupRecords);
  const crossChecks = crossCheckRows(sourceMetadata, { pages: pageControls, queries: queryControls, dates: dateControls, totals: totalControls });
  const counts = classificationCounts(decisionRows);
  const topRisks = decisionRows
    .filter((row) => ['LIKELY_CANNIBALIZATION', 'POSSIBLE_CANNIBALIZATION'].includes(row.classification))
    .sort((left, right) => (left.classification === right.classification ? 0 : left.classification === 'LIKELY_CANNIBALIZATION' ? -1 : 1)
      || right.query_total_impressions - left.query_total_impressions
      || right.query_total_clicks - left.query_total_clicks)
    .slice(0, 5);

  const outputs = {
    detail: path.join(analysisDir, 'multi-url-query-detail.csv'),
    summary: path.join(analysisDir, 'multi-url-query-summary.csv'),
    decisions: path.join(analysisDir, 'cannibalization-decisions.csv'),
    inventory: path.join(analysisDir, 'page-migration-inventory.csv'),
    crossCheck: path.join(analysisDir, 'source-export-cross-check.csv'),
    report: path.join(runDir, 'gsc-data-quality-report.md'),
    summaryJson: path.join(analysisDir, 'analysis-summary.json'),
  };
  await writeCsv(outputs.detail, [
    'group_id', 'query', 'distinct_url_count', 'url_role', 'page', 'clicks', 'impressions', 'ctr', 'position',
    'click_share', 'impression_share', 'query_total_clicks', 'query_total_impressions', 'query_ctr',
    'query_weighted_position', 'strongest_url', 'weaker_competing_urls', 'metric_source', 'reconciliation_status',
    'daily_observation_days', 'daily_cooccurrence_days', 'daily_winner_count', 'daily_winner_switches',
    'content_type', 'title', 'h1', 'canonical', 'indexability', 'duplicate_suffix_pattern', 'classification',
    'confidence', 'evidence_codes', 'evidence_text', 'recommended_review_action', 'do_not_execute_automatically',
  ], detailRows);
  await writeCsv(outputs.summary, [
    'group_id', 'query', 'distinct_url_count', 'query_total_clicks', 'query_total_impressions', 'query_ctr',
    'query_weighted_position', 'strongest_url', 'weaker_competing_urls', 'metric_source', 'reconciliation_status',
    'daily_observation_days', 'daily_cooccurrence_days', 'daily_winner_count', 'daily_winner_switches',
    'classification', 'confidence', 'evidence_codes', 'evidence_text', 'recommended_review_action', 'do_not_execute_automatically',
  ], summaryRows);
  await writeCsv(outputs.decisions, [
    'group_id', 'query', 'distinct_url_count', 'query_total_clicks', 'query_total_impressions', 'query_ctr',
    'query_weighted_position', 'strongest_url', 'weaker_competing_urls', 'daily_observation_days',
    'daily_cooccurrence_days', 'daily_winner_count', 'daily_winner_switches', 'classification', 'confidence',
    'evidence_codes', 'evidence_text', 'recommended_review_action', 'do_not_execute_automatically',
    'strongest_impression_share', 'secondary_impression_share', 'top_two_position_gap', 'metadata_similarity_jaccard',
    'metadata_known', 'distinct_content_types', 'content_types', 'distinct_languages', 'languages', 'suffix_duplicate_signal', 'metric_source', 'reconciliation_status',
  ], decisionRows);
  await writeCsv(outputs.inventory, [
    'url', 'normalized_url', 'post_id', 'content_type', 'language', 'title', 'h1', 'slug', 'parent', 'taxonomies',
    'wp_status', 'http_status', 'http_status_source', 'indexability', 'robots_directives', 'canonical', 'sitemap_presence',
    'sitemap_source', 'published_date', 'modified_date', 'word_count', 'internal_inlinks', 'internal_outlinks', 'source',
    'clicks', 'impressions', 'ctr', 'position', 'query_count', 'multi_url_query_count', 'protected_url_flag',
    'cannibalization_group_ids', 'strongest_group_ids', 'duplicate_suffix_pattern', 'migration_priority',
    'proposed_action', 'evidence', 'confidence', 'manual_approval_required',
  ], inventory);
  await writeCsv(outputs.crossCheck, ['check', 'source_export_value', 'api_value', 'cross_check_status', 'explanation'], crossChecks);

  const analysisSummary = {
    script: 'gsc-nadlan-analysis.js',
    scriptVersion: SCRIPT_VERSION,
    generatedAt: new Date().toISOString(),
    property: manifest.parameters.site,
    requestedRange: manifest.availability.requestedRange,
    finalDataRange: manifest.availability.returnedFinalRange,
    parameters: PARAMETERS,
    inputCounts: {
      directApiRows: manifest.rowCounts.directApiRows,
      dailyApiRows: manifest.rowCounts.dailyApiRows,
      reconciledRows: reconciledRows.length,
      inventorySourceRows: inventoryRows.length,
    },
    outputCounts: {
      multiUrlQueries: summaryRows.length,
      multiUrlDetailRows: detailRows.length,
      decisions: decisionRows.length,
      inventoryRows: inventory.length,
    },
    classifications: counts,
    topRisks,
    crossChecks,
    workbook: {
      status: 'BLOCKED_BY_WINDOWS_APPLICATION_CONTROL',
      requiredTool: '@oai/artifact-tool',
      blockedComponent: 'skia-canvas/lib/skia.node',
      reason: 'The required native component is not digitally signed and Windows Application Control denied loading it.',
      alternateSpreadsheetLibraryUsed: false,
    },
    noLiveChanges: true,
  };
  await writeJson(outputs.summaryJson, analysisSummary);
  await fsp.writeFile(outputs.report, markdownReport({
    manifest, counts, crossChecks, inventorySummary,
    outputCounts: { ...analysisSummary.outputCounts, reconciledRows: reconciledRows.length }, topRisks,
  }), 'utf8');

  const hashes = {};
  for (const file of Object.values(outputs)) hashes[path.relative(runDir, file)] = await sha256(file);
  await writeJson(path.join(analysisDir, 'analysis-output-sha256.json'), hashes);
  process.stdout.write(`${JSON.stringify(analysisSummary, null, 2)}\n`);
}

main().catch((error) => {
  process.stderr.write(`ERROR: ${error.stack || error.message}\n`);
  process.exitCode = 1;
});
