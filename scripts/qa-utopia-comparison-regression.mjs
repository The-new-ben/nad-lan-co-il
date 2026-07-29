#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const root = process.cwd();
const baselinePath = path.join(root, "docs", "qa", "utopia-before-state-2026-07-29.json");
const outputPath = path.join(root, "docs", "qa", "utopia-comparison-regression-report.json");
const baseline = JSON.parse(fs.readFileSync(baselinePath, "utf8"));

function sha256(buffer) {
  return crypto.createHash("sha256").update(buffer).digest("hex");
}

async function fetchBytes(url, maxAttempts = 4) {
  let last;
  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    const response = await fetch(url, {
      headers: {
        "user-agent": "NadLan-UTOPIA-regression-QA/1.0",
        accept: "*/*"
      },
      redirect: "follow"
    });
    const bytes = Buffer.from(await response.arrayBuffer());
    last = {
      status: response.status,
      final_url: response.url,
      content_type: response.headers.get("content-type") || "",
      bytes,
      sha256: sha256(bytes),
      attempts: attempt
    };
    if (response.status === 200 || ![429, 500, 502, 503, 504].includes(response.status)) return last;
    if (attempt < maxAttempts) {
      await new Promise((resolve) => setTimeout(resolve, attempt * 750));
    }
  }
  return last;
}

async function mapLimit(rows, limit, inspect) {
  const results = new Array(rows.length);
  let next = 0;
  async function worker() {
    while (next < rows.length) {
      const index = next;
      next += 1;
      results[index] = await inspect(rows[index]);
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, rows.length) }, worker));
  return results;
}

async function inspectRest(row) {
  const url = `https://nad-lan.co.il/wp-json/wp/v2/nadlan_project/${row.id}?context=view`;
  try {
    const result = await fetchBytes(url);
    return {
      family: row.family,
      lang: row.lang,
      id: row.id,
      slug: row.slug,
      url,
      status: result.status,
      attempts: result.attempts,
      bytes: result.bytes.length,
      expected_sha256: row.sha256,
      actual_sha256: result.sha256,
      unchanged: result.status === 200 && result.sha256 === row.sha256,
      error: null
    };
  } catch (error) {
    return {
      family: row.family,
      lang: row.lang,
      id: row.id,
      slug: row.slug,
      url,
      status: 0,
      bytes: 0,
      expected_sha256: row.sha256,
      actual_sha256: null,
      unchanged: false,
      error: String(error?.message || error)
    };
  }
}

async function inspectModel(row) {
  try {
    const result = await fetchBytes(row.url);
    return {
      family: row.family,
      url: row.url,
      status: result.status,
      attempts: result.attempts,
      bytes: result.bytes.length,
      expected_bytes: row.bytes,
      expected_sha256: row.sha256,
      actual_sha256: result.sha256,
      unchanged: result.status === 200 && result.bytes.length === row.bytes && result.sha256 === row.sha256,
      error: null
    };
  } catch (error) {
    return {
      family: row.family,
      url: row.url,
      status: 0,
      bytes: 0,
      expected_bytes: row.bytes,
      expected_sha256: row.sha256,
      actual_sha256: null,
      unchanged: false,
      error: String(error?.message || error)
    };
  }
}

const rest = await mapLimit(baseline.comparison_rest_baseline, 4, inspectRest);
const models = await mapLimit(baseline.comparison_models, 4, inspectModel);
const report = {
  schema: "nadlan-utopia-comparison-regression/v1",
  generated_at: new Date().toISOString(),
  baseline: path.relative(root, baselinePath).replaceAll("\\", "/"),
  phase: process.argv.includes("--post-release") ? "post-release" : "pre-release",
  rest,
  models,
  rest_unchanged: rest.filter((row) => row.unchanged).length,
  rest_total: rest.length,
  models_unchanged: models.filter((row) => row.unchanged).length,
  models_total: models.length,
  pass: rest.every((row) => row.unchanged) && models.every((row) => row.unchanged)
};

fs.writeFileSync(outputPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(JSON.stringify(report, null, 2));
process.exit(report.pass ? 0 : 1);
