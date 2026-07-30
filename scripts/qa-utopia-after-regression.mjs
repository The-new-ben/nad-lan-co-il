#!/usr/bin/env node

/**
 * Read-only live AFTER gate for UTOPIA and the mature showroom comparison set.
 *
 * The command:
 * - fails before capture unless production exposes the expected plugin version
 *   and all five exact UTOPIA routes return HTTP 200 without redirects;
 * - reuses the immutable mature-showroom journey runner in an isolated temporary
 *   working directory, with its opt-in all-language/all-viewport deep matrix;
 * - blocks every non-GET browser request;
 * - compares mature URL, REST and model evidence with the recorded BEFORE state;
 * - captures UTOPIA in five languages at desktop and mobile sizes;
 * - creates timestamped AFTER evidence and never writes into the BEFORE directory.
 *
 * Usage:
 *   node scripts/qa-utopia-after-regression.mjs
 *   node scripts/qa-utopia-after-regression.mjs --expected-version 1.72.135
 *   node scripts/qa-utopia-after-regression.mjs --preflight-only
 */

import crypto from "node:crypto";
import { spawn } from "node:child_process";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { chromium } from "playwright";

const ROOT = process.cwd();
const SITE = "https://nad-lan.co.il";
// 1.72.133 was aborted after an independent release advanced production to
// 1.72.134. UTOPIA therefore resumes on the next isolated version, 1.72.135.
const DEFAULT_EXPECTED_VERSION = "1.72.135";
const DEFAULT_CHILD_TIMEOUT_MS = 45 * 60 * 1000;
const BEFORE_DIR = path.join(
  ROOT,
  "docs",
  "qa",
  "screenshots",
  "mature-showroom-before-2026-07-30"
);
const BEFORE_REPORT_PATH = path.join(BEFORE_DIR, "report.json");
const BEFORE_MANIFEST_PATH = path.join(
  BEFORE_DIR,
  "artifact-manifest.sha256"
);
const BEFORE_STATE_PATH = path.join(
  ROOT,
  "docs",
  "qa",
  "utopia-before-state-2026-07-29.json"
);
const MATURE_RUNNER = path.join(
  ROOT,
  "scripts",
  "qa-mature-showroom-before-2026-07-30.mjs"
);
const SCREENSHOT_ROOT = path.join(ROOT, "docs", "qa", "screenshots");
const MODEL_URL =
  `${SITE}/wp-content/plugins/nadlan-config/assets/showroom-engine/models/utopia-rich-v1.glb`;
const MODEL_SHA256 =
  "ba267a241f7b5d943f5eebd6f32aae9241f14da420207ddadc4d5d74ac392f24";
const MODEL_BYTES = 309148;

const LANGUAGES = {
  he: { slug: "utopia-sde-dov", dir: "rtl", locale: "he-IL" },
  en: { slug: "utopia-sde-dov-en", dir: "ltr", locale: "en-US" },
  fr: { slug: "utopia-sde-dov-fr", dir: "ltr", locale: "fr-FR" },
  ru: { slug: "utopia-sde-dov-ru", dir: "ltr", locale: "ru-RU" },
  ar: { slug: "utopia-sde-dov-ar", dir: "rtl", locale: "ar" },
};
const VIEWPORTS = {
  desktop: {
    viewport: { width: 1440, height: 1000 },
    isMobile: false,
    hasTouch: false,
  },
  mobile: {
    viewport: { width: 390, height: 844 },
    isMobile: true,
    hasTouch: true,
  },
};
const FAMILY_KEYS = [
  "duo-tel-aviv",
  "rainbow-tel-aviv",
  "dimri-yama-sde-dov",
  "ashira-sde-dov",
];
const REQUIRED_DEEP_CAPABILITIES = [
  "trusted_unit_selection_cinematic",
  "apartment_studio",
  "unified_map",
  "model_to_map_bearing",
  "window_view",
];
const UNSAFE_CONTACT_PATTERNS = [
  /\bwa\.me\b/iu,
  /^mailto:/iu,
  /^tel:/iu,
  /(?:^|\/)(?:lead|leads|rfp|request-for-proposal)(?:\/|[?#]|$)/iu,
  /(?:^|\/)(?:cotour|video-call)(?:\/|[?#]|$)/iu,
];

function help() {
  console.log(`Usage:
  node scripts/qa-utopia-after-regression.mjs
  node scripts/qa-utopia-after-regression.mjs --expected-version 1.72.135
  node scripts/qa-utopia-after-regression.mjs --preflight-only
  node scripts/qa-utopia-after-regression.mjs --headed

Options:
  --expected-version <x.y.z>  Required live nadlan-config version (default 1.72.135)
  --preflight-only           Check health and exact UTOPIA routes, then stop
  --headed                   Show Chrome during the full AFTER capture
  --timeout-ms <10000..180000>
  --child-timeout-ms <300000..7200000>
                             Bound the mature matrix child (default 2700000)
  --self-test                Exercise local integrity and comparison contracts
  --help

The full command is public, read-only QA. It sends GET requests only, never fills
or submits a form, and creates a new timestamped directory below
docs/qa/screenshots/. It refuses to overwrite the immutable BEFORE evidence.`);
}

function parseArgs(argv) {
  const args = {
    expectedVersion: DEFAULT_EXPECTED_VERSION,
    preflightOnly: false,
    headed: false,
    timeoutMs: 60000,
    childTimeoutMs: DEFAULT_CHILD_TIMEOUT_MS,
    selfTest: false,
  };
  for (let index = 2; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--expected-version") {
      args.expectedVersion = argv[++index] || "";
    } else if (arg === "--preflight-only") {
      args.preflightOnly = true;
    } else if (arg === "--headed") {
      args.headed = true;
    } else if (arg === "--timeout-ms") {
      args.timeoutMs = Number(argv[++index] || 0);
    } else if (arg === "--child-timeout-ms") {
      args.childTimeoutMs = Number(argv[++index] || 0);
    } else if (arg === "--self-test") {
      args.selfTest = true;
    } else if (arg === "--help" || arg === "-h") {
      help();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  if (!/^\d+\.\d+\.\d+$/u.test(args.expectedVersion)) {
    throw new Error("--expected-version must be an x.y.z release version.");
  }
  if (
    !Number.isFinite(args.timeoutMs) ||
    args.timeoutMs < 10000 ||
    args.timeoutMs > 180000
  ) {
    throw new Error("--timeout-ms must be between 10000 and 180000.");
  }
  if (
    !Number.isFinite(args.childTimeoutMs) ||
    args.childTimeoutMs < 300000 ||
    args.childTimeoutMs > 7200000
  ) {
    throw new Error(
      "--child-timeout-ms must be between 300000 and 7200000."
    );
  }
  return args;
}

function sha256(bytes) {
  return crypto.createHash("sha256").update(bytes).digest("hex");
}

function runStamp() {
  return new Date()
    .toISOString()
    .replaceAll("-", "")
    .replaceAll(":", "")
    .replace(/\.\d{3}Z$/u, "Z");
}

function normalizeUrl(value) {
  try {
    const url = new URL(value);
    url.search = "";
    url.hash = "";
    if (!url.pathname.endsWith("/")) url.pathname += "/";
    return url.href;
  } catch {
    return "";
  }
}

function safeUrl(value) {
  try {
    const url = new URL(value);
    url.username = "";
    url.password = "";
    url.search = "";
    url.hash = "";
    return url.href;
  } catch {
    return String(value || "").slice(0, 500);
  }
}

function relativeToRoot(filePath) {
  return path.relative(ROOT, filePath).replaceAll("\\", "/");
}

function expectedUrls() {
  return Object.fromEntries(
    Object.entries(LANGUAGES).map(([lang, spec]) => [
      lang,
      `${SITE}/projects/${spec.slug}/`,
    ])
  );
}

function expectedHreflang() {
  const urls = expectedUrls();
  return {
    he: urls.he,
    en: urls.en,
    fr: urls.fr,
    ru: urls.ru,
    ar: urls.ar,
    "x-default": urls.he,
  };
}

function withCacheBust(value, token) {
  const url = new URL(value);
  url.searchParams.set("utopia_after_probe", token);
  return url.href;
}

async function getBytes(url, { timeoutMs = 60000, redirect = "manual" } = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, {
      method: "GET",
      redirect,
      signal: controller.signal,
      headers: {
        accept: "*/*",
        "cache-control": "no-cache",
        "user-agent": "NadLan-UTOPIA-AFTER-read-only-QA/1.0",
      },
    });
    const body = Buffer.from(await response.arrayBuffer());
    return {
      status: response.status,
      finalUrl: response.url,
      location: response.headers.get("location") || "",
      contentType: response.headers.get("content-type") || "",
      body,
      bytes: body.length,
      sha256: sha256(body),
    };
  } finally {
    clearTimeout(timer);
  }
}

async function mapLimit(rows, limit, inspect) {
  const results = new Array(rows.length);
  let next = 0;
  async function worker() {
    while (next < rows.length) {
      const index = next;
      next += 1;
      try {
        results[index] = await inspect(rows[index], index);
      } catch (error) {
        results[index] = {
          pass: false,
          error: String(error?.stack || error),
        };
      }
    }
  }
  await Promise.all(
    Array.from({ length: Math.min(limit, rows.length) }, () => worker())
  );
  return results;
}

async function preflight(args, { label = "start" } = {}) {
  const urls = expectedUrls();
  const cacheBust = `${label}-${Date.now()}-${crypto
    .randomBytes(4)
    .toString("hex")}`;
  const healthResult = await getBytes(
    withCacheBust(
      `${SITE}/wp-json/nadlan/v1/healthcheck`,
      cacheBust
    ),
    { timeoutMs: args.timeoutMs }
  );
  let health = null;
  let healthParseError = null;
  try {
    health = JSON.parse(healthResult.body.toString("utf8"));
  } catch (error) {
    healthParseError = String(error?.message || error);
  }
  const routes = await mapLimit(
    Object.entries(urls).map(([lang, url]) => ({ lang, url })),
    5,
    async (row) => {
      const requestedUrl = withCacheBust(row.url, cacheBust);
      const result = await getBytes(requestedUrl, {
        timeoutMs: args.timeoutMs,
      });
      const html = result.body.toString("utf8");
      const pass =
        result.status === 200 &&
        !result.location &&
        normalizeUrl(result.finalUrl) === normalizeUrl(row.url) &&
        /id=["']utopia-showroom["']/iu.test(html);
      return {
        ...row,
        requested_url: requestedUrl,
        status: result.status,
        final_url: normalizeUrl(result.finalUrl),
        redirect_location: result.location || null,
        bytes: result.bytes,
        source_sha256: result.sha256,
        utopia_root_in_source: /id=["']utopia-showroom["']/iu.test(html),
        pass,
        _body: result.body,
      };
    }
  );
  const modelFetchUrl = withCacheBust(MODEL_URL, cacheBust);
  const modelResult = await getBytes(modelFetchUrl, {
    timeoutMs: args.timeoutMs,
  });
  const model = {
    url: MODEL_URL,
    requested_url: modelFetchUrl,
    status: modelResult.status,
    final_url: safeUrl(modelResult.finalUrl),
    redirect_location: modelResult.location || null,
    bytes: modelResult.bytes,
    expected_bytes: MODEL_BYTES,
    sha256: modelResult.sha256,
    expected_sha256: MODEL_SHA256,
    pass:
      modelResult.status === 200 &&
      !modelResult.location &&
      safeUrl(modelResult.finalUrl) === MODEL_URL &&
      modelResult.bytes === MODEL_BYTES &&
      modelResult.sha256 === MODEL_SHA256,
  };
  const version = String(health?.version || "");
  const healthPass =
    healthResult.status === 200 &&
    !healthParseError &&
    health?.plugin === "nadlan-config" &&
    version === args.expectedVersion &&
    health?.reliability?.deps_ok === true;
  const pass =
    healthPass &&
    routes.length === 5 &&
    routes.every((row) => row.pass) &&
    model.pass;
  return {
    pass,
    label,
    cache_busted: true,
    cache_bust_token: cacheBust,
    expected_version: args.expectedVersion,
    health: {
      status: healthResult.status,
      plugin: health?.plugin || null,
      version: version || null,
      dependencies_ok: health?.reliability?.deps_ok ?? null,
      parse_error: healthParseError,
      pass: healthPass,
    },
    routes,
    model,
  };
}

async function verifyBeforeIntegrity() {
  const manifestBytes = await fs.readFile(BEFORE_MANIFEST_PATH);
  const reportBytes = await fs.readFile(BEFORE_REPORT_PATH);
  const lines = manifestBytes
    .toString("utf8")
    .split(/\r?\n/u)
    .filter(Boolean);
  const checks = [];
  for (const line of lines) {
    const match = line.match(/^([a-f0-9]{64}) {2}(.+)$/u);
    if (!match) {
      checks.push({ line, pass: false, reason: "malformed manifest row" });
      continue;
    }
    const expected = match[1];
    const relative = match[2].replaceAll("/", path.sep);
    const fullPath = path.resolve(BEFORE_DIR, relative);
    const inside =
      fullPath === BEFORE_DIR ||
      fullPath.startsWith(`${BEFORE_DIR}${path.sep}`);
    if (!inside) {
      checks.push({ file: match[2], pass: false, reason: "path escaped baseline" });
      continue;
    }
    try {
      const bytes = await fs.readFile(fullPath);
      const actual = sha256(bytes);
      checks.push({
        file: match[2],
        expected_sha256: expected,
        actual_sha256: actual,
        pass: actual === expected,
      });
    } catch (error) {
      checks.push({
        file: match[2],
        expected_sha256: expected,
        actual_sha256: null,
        pass: false,
        reason: String(error?.message || error),
      });
    }
  }
  return {
    directory: relativeToRoot(BEFORE_DIR),
    manifest_sha256: sha256(manifestBytes),
    report_sha256: sha256(reportBytes),
    entries: checks.length,
    verified: checks.filter((row) => row.pass).length,
    failures: checks.filter((row) => !row.pass),
    pass: checks.length > 0 && checks.every((row) => row.pass),
  };
}

function isProcessAlive(pid) {
  if (!Number.isInteger(pid) || pid <= 0) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    return error?.code === "EPERM";
  }
}

async function waitForProcessExit(pid, timeoutMs = 5000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (!isProcessAlive(pid)) return true;
    await new Promise((resolve) => setTimeout(resolve, 50));
  }
  return !isProcessAlive(pid);
}

function runTreeKillCommand(command, args, timeoutMs = 5000) {
  return new Promise((resolve) => {
    let settled = false;
    let stdout = "";
    let stderr = "";
    const killer = spawn(command, args, {
      windowsHide: true,
      stdio: ["ignore", "pipe", "pipe"],
    });
    const finish = (result) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      resolve({ ...result, stdout, stderr });
    };
    const timer = setTimeout(() => {
      killer.kill("SIGKILL");
      finish({
        code: -1,
        signal: "SIGKILL",
        error: `tree-kill command exceeded ${timeoutMs} ms`,
      });
    }, timeoutMs);
    killer.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });
    killer.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });
    killer.on("error", (error) => {
      finish({
        code: -1,
        signal: null,
        error: String(error?.stack || error),
      });
    });
    killer.on("close", (code, signal) => {
      finish({
        code: code == null ? -1 : Number(code),
        signal: signal || null,
        error: null,
      });
    });
  });
}

async function terminateProcessTree(pid, child = null) {
  const numericPid = Number(pid);
  if (!Number.isInteger(numericPid) || numericPid <= 0) {
    return {
      attempted: false,
      mode: null,
      pass: false,
      error: "missing child pid",
    };
  }
  if (process.platform === "win32") {
    const taskkill = await runTreeKillCommand(
      "taskkill.exe",
      ["/PID", String(numericPid), "/T", "/F"]
    );
    if (taskkill.code === 0 || !isProcessAlive(numericPid)) {
      return {
        attempted: true,
        mode: "windows-taskkill-tree-force",
        pass: true,
        command_exit: taskkill.code,
        error: taskkill.error,
      };
    }
    let directPass = false;
    let directError = null;
    try {
      directPass = child
        ? child.kill("SIGKILL")
        : process.kill(numericPid, "SIGKILL");
    } catch (error) {
      directError = String(error?.stack || error);
    }
    return {
      attempted: true,
      mode: "windows-taskkill-tree-force-with-direct-fallback",
      pass: Boolean(directPass) || !isProcessAlive(numericPid),
      command_exit: taskkill.code,
      error: directError || taskkill.error || taskkill.stderr.trim() || null,
    };
  }
  try {
    process.kill(-numericPid, "SIGKILL");
    return {
      attempted: true,
      mode: "posix-process-group-sigkill",
      pass: true,
      error: null,
    };
  } catch (groupError) {
    try {
      const directPass = child
        ? child.kill("SIGKILL")
        : process.kill(numericPid, "SIGKILL");
      return {
        attempted: true,
        mode: "posix-direct-sigkill-fallback",
        pass: Boolean(directPass) || !isProcessAlive(numericPid),
        error: String(groupError?.message || groupError),
      };
    } catch (directError) {
      return {
        attempted: true,
        mode: "posix-direct-sigkill-fallback",
        pass: !isProcessAlive(numericPid),
        error: [
          String(groupError?.message || groupError),
          String(directError?.message || directError),
        ].join("; "),
      };
    }
  }
}

function runChild(command, childArgs, options = {}) {
  return new Promise((resolve) => {
    const startedAt = Date.now();
    let settled = false;
    let timedOut = false;
    let terminationPromise = Promise.resolve(null);
    const child = spawn(command, childArgs, {
      cwd: options.cwd || ROOT,
      env: options.env || process.env,
      detached: process.platform !== "win32",
      windowsHide: true,
      stdio: ["ignore", "pipe", "pipe"],
    });
    let stdout = "";
    let stderr = "";
    const finish = (result) => {
      if (settled) return;
      settled = true;
      clearTimeout(watchdog);
      void terminationPromise
        .catch((error) => ({
          attempted: true,
          mode: "tree-termination-error",
          pass: false,
          error: String(error?.stack || error),
        }))
        .then((termination) => {
          resolve({
            ...result,
            timedOut,
            duration_ms: Date.now() - startedAt,
            termination,
          });
        });
    };
    const watchdog = setTimeout(() => {
      timedOut = true;
      stderr +=
        `\n[watchdog] child exceeded ${options.timeoutMs} ms; terminating\n`;
      terminationPromise = terminateProcessTree(child.pid, child);
    }, options.timeoutMs);
    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
      process.stdout.write(chunk);
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
      process.stderr.write(chunk);
    });
    child.on("error", (error) => {
      finish({
        code: -1,
        signal: null,
        stdout,
        stderr,
        error: String(error?.stack || error),
      });
    });
    child.on("close", (code, signal) => {
      finish({
        code: code == null ? -1 : Number(code),
        signal: signal || null,
        stdout,
        stderr,
        error: null,
      });
    });
  });
}

async function copyPngs(fromDir, toDir) {
  await fs.mkdir(toDir, { recursive: true });
  const entries = await fs.readdir(fromDir, { withFileTypes: true });
  for (const entry of entries) {
    if (!entry.isFile() || !entry.name.toLowerCase().endsWith(".png")) continue;
    await fs.copyFile(
      path.join(fromDir, entry.name),
      path.join(toDir, entry.name)
    );
  }
}

async function preserveChildDiagnostics(tempRoot, matureDir) {
  const diagnosticSource = path.join(
    tempRoot,
    "docs",
    "qa",
    "screenshots"
  );
  const diagnosticExists = await fs
    .stat(diagnosticSource)
    .then(() => true)
    .catch(() => false);
  if (!diagnosticExists) {
    return { copied: false, source_found: false, destination: null };
  }
  const destination = path.join(matureDir, "child-diagnostics");
  await fs.cp(diagnosticSource, destination, {
    recursive: true,
    force: false,
    errorOnExist: true,
  });
  return {
    copied: true,
    source_found: true,
    destination,
  };
}

async function withChildDiagnosticPreservation(
  tempRoot,
  matureDir,
  operation
) {
  try {
    return await operation();
  } catch (error) {
    try {
      const preservation = await preserveChildDiagnostics(tempRoot, matureDir);
      if (error && typeof error === "object") {
        error.childDiagnostics = preservation;
      }
    } catch (preservationError) {
      throw new AggregateError(
        [error, preservationError],
        "Child processing failed and its diagnostic evidence could not be preserved."
      );
    }
    throw error;
  }
}

function rewriteMaturePaths(report, runDir) {
  const oldPrefix =
    "docs/qa/screenshots/mature-showroom-before-2026-07-30/";
  const newPrefix = `${relativeToRoot(path.join(runDir, "mature"))}/`;
  const rewritten = JSON.parse(
    JSON.stringify(report).replaceAll(oldPrefix, newPrefix)
  );
  rewritten.schema = "nadlan-mature-showroom-after/v1";
  rewritten.phase = "AFTER";
  rewritten.derived_from_runner =
    "scripts/qa-mature-showroom-before-2026-07-30.mjs";
  rewritten.immutable_before_report = relativeToRoot(BEFORE_REPORT_PATH);
  rewritten.artifact_manifest = "../artifact-manifest.sha256";
  return rewritten;
}

function matureChildEnvironment(args) {
  return {
    ...process.env,
    NADLAN_MATURE_QA_DEEP_MATRIX: "all-viewports",
    NADLAN_MATURE_QA_HEADED: args.headed ? "1" : "0",
  };
}

async function runMatureCapture(runDir, args) {
  const tempRoot = await fs.mkdtemp(
    path.join(os.tmpdir(), "nadlan-utopia-after-")
  );
  const rawDir = path.join(
    tempRoot,
    "docs",
    "qa",
    "screenshots",
    "mature-showroom-before-2026-07-30"
  );
  const matureDir = path.join(runDir, "mature");
  try {
    const child = await runChild(process.execPath, [MATURE_RUNNER], {
      cwd: tempRoot,
      timeoutMs: args.childTimeoutMs,
      env: matureChildEnvironment(args),
    });
    await fs.mkdir(matureDir, { recursive: true });
    return await withChildDiagnosticPreservation(
      tempRoot,
      matureDir,
      async () => {
        await fs.writeFile(
          path.join(matureDir, "runner.stdout.log"),
          child.stdout,
          "utf8"
        );
        await fs.writeFile(
          path.join(matureDir, "runner.stderr.log"),
          child.stderr,
          "utf8"
        );
        await fs.writeFile(
          path.join(matureDir, "child-exit.json"),
          `${JSON.stringify(
            {
              code: child.code,
              signal: child.signal,
              timed_out: child.timedOut,
              duration_ms: child.duration_ms,
              watchdog_ms: args.childTimeoutMs,
              headed: args.headed,
              termination: child.termination,
              error: child.error,
            },
            null,
            2
          )}\n`,
          "utf8"
        );
        if (child.code !== 0) {
          throw new Error(
            `Mature showroom child gate exited ${child.code}${child.timedOut ? " after watchdog timeout" : ""}: ${child.error || child.stderr.slice(-1200)}`
          );
        }
        const rawReport = JSON.parse(
          await fs.readFile(path.join(rawDir, "report.json"), "utf8")
        );
        await copyPngs(rawDir, matureDir);
        const report = rewriteMaturePaths(rawReport, runDir);
        await fs.writeFile(
          path.join(matureDir, "report.json"),
          `${JSON.stringify(report, null, 2)}\n`,
          "utf8"
        );
        return report;
      }
    );
  } finally {
    await fs.rm(tempRoot, { recursive: true, force: true });
  }
}

function isFirstParty(url) {
  try {
    return new URL(url).origin === SITE;
  } catch {
    return false;
  }
}

function normalizeTelemetryEndpoint(row) {
  const method = String(row.method || "").toUpperCase();
  try {
    const url = new URL(row.url);
    const host = url.hostname.toLowerCase();
    const endpointPath = url.pathname || "/";
    return {
      method,
      host,
      path: endpointPath,
      key: `${method} ${host}${endpointPath}`,
    };
  } catch {
    return {
      method,
      host: null,
      path: null,
      key: `${method} [invalid-url]`,
    };
  }
}

function deriveTelemetryBaseline(beforeReport) {
  const rows = allMatureGuardBlocks(beforeReport)
    .filter((row) => !row.first_party && !isFirstParty(row.url))
    .map(normalizeTelemetryEndpoint);
  const byKey = new Map(rows.map((row) => [row.key, row]));
  const endpoints = [...byKey.values()].sort((a, b) =>
    a.key.localeCompare(b.key)
  );
  return {
    source: relativeToRoot(BEFORE_REPORT_PATH),
    normalization: "uppercase method + lowercase host + URL pathname; query ignored",
    endpoints,
    keys: new Set(endpoints.map((row) => row.key)),
    pass:
      endpoints.length > 0 &&
      endpoints.every(
        (row) =>
          row.method !== "GET" &&
          Boolean(row.host) &&
          Boolean(row.path)
      ),
  };
}

function publicTelemetryBaseline(baseline) {
  return {
    source: baseline.source,
    normalization: baseline.normalization,
    endpoints: baseline.endpoints,
    pass: baseline.pass,
  };
}

function classifyGuardBlocks(rows, telemetryBaseline) {
  const classified = {
    baseline_matched_third_party: [],
    new_third_party: [],
    first_party: [],
  };
  for (const row of rows) {
    if (row.first_party || isFirstParty(row.url)) {
      classified.first_party.push(row);
    } else {
      const normalized = normalizeTelemetryEndpoint(row);
      const enriched = { ...row, normalized_endpoint: normalized };
      if (telemetryBaseline.keys.has(normalized.key)) {
        classified.baseline_matched_third_party.push(enriched);
      } else {
        classified.new_third_party.push(enriched);
      }
    }
  }
  return {
    counts: {
      baseline_matched_third_party:
        classified.baseline_matched_third_party.length,
      new_third_party: classified.new_third_party.length,
      first_party: classified.first_party.length,
    },
    ...classified,
    pass:
      classified.first_party.length === 0 &&
      classified.new_third_party.length === 0,
  };
}

function allMatureGuardBlocks(report) {
  return [
    ...report.discovery.flatMap((row) => row.safety?.guard_blocks || []),
    ...report.matrix.flatMap((row) => row.events?.guard_blocks || []),
    ...report.deep.flatMap((row) => row.events?.guard_blocks || []),
  ];
}

function evaluateMatureCapture(report, telemetryBaseline) {
  const guards = classifyGuardBlocks(
    allMatureGuardBlocks(report),
    telemetryBaseline
  );
  const matrixChecks = report.matrix.map((row) => {
    const failed = row.health?.failed_assertions || [];
    const consoleOnly =
      failed.length === 1 &&
      failed[0] === "no console errors" &&
      (row.events?.console_errors || []).every((message) =>
        /ERR_BLOCKED_BY_CLIENT/iu.test(message)
      ) &&
      classifyGuardBlocks(
        row.events?.guard_blocks || [],
        telemetryBaseline
      ).pass;
    const pass =
      row.navigation?.status === 200 &&
      Boolean(row.state) &&
      (failed.length === 0 || consoleOnly) &&
      (row.first_party_failures || []).length === 0 &&
      (row.events?.first_party_non_get_attempts || []).length === 0;
    return {
      family: row.family,
      lang: row.lang,
      viewport: row.viewport,
      pass,
      original_status: row.health?.status || null,
      original_failed_assertions: failed,
      before_baseline_telemetry_console_only: consoleOnly,
    };
  });
  const deepChecks = report.deep.map((row) => {
    const byName = Object.fromEntries(
      (row.capabilities || []).map((capability) => [
        capability.name,
        capability.status,
      ])
    );
    const missingOrBroken = REQUIRED_DEEP_CAPABILITIES.filter(
      (name) => byName[name] !== "passed"
    );
    const guardClassification = classifyGuardBlocks(
      row.events?.guard_blocks || [],
      telemetryBaseline
    );
    const pass =
      row.navigation?.status === 200 &&
      missingOrBroken.length === 0 &&
      (row.first_party_failures || []).length === 0 &&
      (row.events?.first_party_non_get_attempts || []).length === 0 &&
      guardClassification.pass &&
      (row.events?.console_errors || []).every((message) =>
        /ERR_BLOCKED_BY_CLIENT/iu.test(message)
      ) &&
      (row.events?.page_errors || []).length === 0;
    return {
      family: row.family,
      lang: row.lang,
      viewport: row.viewport_name || "desktop",
      pass,
      capability_statuses: byName,
      missing_or_broken: missingOrBroken,
      guard_classification: guardClassification.counts,
    };
  });
  return {
    matrix: matrixChecks,
    deep: deepChecks,
    guard_classification: guards,
    matrix_passed: matrixChecks.filter((row) => row.pass).length,
    matrix_total: matrixChecks.length,
    deep_passed: deepChecks.filter((row) => row.pass).length,
    deep_total: deepChecks.length,
    pass:
      matrixChecks.length === 40 &&
      matrixChecks.every((row) => row.pass) &&
      deepChecks.length === 40 &&
      deepChecks.every((row) => row.pass) &&
      guards.pass,
  };
}

function sortedHreflang(rows) {
  return [...(rows || [])]
    .map((row) => ({
      lang: String(row.lang || "").toLowerCase(),
      href: normalizeUrl(row.href),
    }))
    .sort((a, b) => a.lang.localeCompare(b.lang));
}

async function captureComparisonEvidence(
  afterReport,
  beforeReport,
  beforeState
) {
  const urlRows = beforeReport.matrix.map((before) => {
    const after = afterReport.matrix.find(
      (row) =>
        row.family === before.family &&
        row.lang === before.lang &&
        row.viewport === before.viewport
    );
    const pass =
      Boolean(after) &&
      normalizeUrl(after.url) === normalizeUrl(before.url) &&
      after.navigation?.status === before.navigation?.status &&
      normalizeUrl(after.navigation?.final_url) ===
        normalizeUrl(before.navigation?.final_url) &&
      JSON.stringify(
        (after.state?.canonical || []).map(normalizeUrl).sort()
      ) ===
        JSON.stringify(
          (before.state?.canonical || []).map(normalizeUrl).sort()
        ) &&
      JSON.stringify(sortedHreflang(after.state?.hreflang)) ===
        JSON.stringify(sortedHreflang(before.state?.hreflang));
    return {
      family: before.family,
      lang: before.lang,
      viewport: before.viewport,
      expected_url: before.url,
      actual_url: after?.url || null,
      expected_final_url: before.navigation?.final_url || null,
      actual_final_url: after?.navigation?.final_url || null,
      canonical_unchanged:
        JSON.stringify(
          (after?.state?.canonical || []).map(normalizeUrl).sort()
        ) ===
        JSON.stringify(
          (before.state?.canonical || []).map(normalizeUrl).sort()
        ),
      hreflang_unchanged:
        JSON.stringify(sortedHreflang(after?.state?.hreflang)) ===
        JSON.stringify(sortedHreflang(before.state?.hreflang)),
      pass,
    };
  });
  const uniqueSources = [
    ...new Map(
      beforeReport.matrix.map((row) => [
        `${row.family}|${row.lang}`,
        { family: row.family, lang: row.lang, url: row.url },
      ])
    ).values(),
  ];
  const currentSourceRows = await mapLimit(uniqueSources, 4, async (row) => {
    const result = await getBytes(row.url, { redirect: "manual" });
    return {
      ...row,
      status: result.status,
      bytes: result.bytes,
      actual_sha256: result.sha256,
      before_sha256: null,
      evidence_role:
        "current-source availability only; immutable BEFORE source hash unavailable",
      proves_unchanged: false,
      pass:
        result.status === 200 &&
        !result.location &&
        normalizeUrl(result.finalUrl) === normalizeUrl(row.url),
    };
  });
  const restRows = await mapLimit(
    beforeState.comparison_rest_baseline || [],
    4,
    async (row) => {
      const url =
        `${SITE}/wp-json/wp/v2/nadlan_project/${row.id}?context=view`;
      const result = await getBytes(url, { redirect: "manual" });
      return {
        family: row.family,
        lang: row.lang,
        id: row.id,
        slug: row.slug,
        url,
        status: result.status,
        bytes: result.bytes,
        expected_sha256: row.sha256,
        actual_sha256: result.sha256,
        pass:
          result.status === 200 &&
          !result.location &&
          result.sha256 === row.sha256,
      };
    }
  );
  const modelRows = await mapLimit(
    beforeState.comparison_models || [],
    4,
    async (row) => {
      const result = await getBytes(row.url, { redirect: "manual" });
      return {
        family: row.family,
        url: row.url,
        status: result.status,
        expected_bytes: row.bytes,
        actual_bytes: result.bytes,
        expected_sha256: row.sha256,
        actual_sha256: result.sha256,
        pass:
          result.status === 200 &&
          !result.location &&
          result.bytes === row.bytes &&
          result.sha256 === row.sha256,
      };
    }
  );
  return {
    immutable_before_report: relativeToRoot(BEFORE_REPORT_PATH),
    immutable_hash_baseline: relativeToRoot(BEFORE_STATE_PATH),
    urls: urlRows,
    current_source_availability: {
      rows: currentSourceRows,
      available: currentSourceRows.filter((row) => row.pass).length,
      total: currentSourceRows.length,
      pass:
        currentSourceRows.length === 20 &&
        currentSourceRows.every((row) => row.pass),
      proves_unchanged: false,
      reason:
        "The immutable BEFORE evidence did not contain raw page-source hashes.",
    },
    rest_hashes: restRows,
    model_hashes: modelRows,
    pass:
      urlRows.length === 40 &&
      urlRows.every((row) => row.pass) &&
      currentSourceRows.length === 20 &&
      currentSourceRows.every((row) => row.pass) &&
      restRows.length === 20 &&
      restRows.every((row) => row.pass) &&
      modelRows.length === 4 &&
      modelRows.every((row) => row.pass),
  };
}

function makeEvents() {
  return {
    guard_blocks: [],
    first_party_non_get_attempts: [],
    console_errors: [],
    console_warnings: [],
    page_errors: [],
    response_failures: [],
    request_failures: [],
  };
}

function isUnsafeContactUrl(url) {
  return UNSAFE_CONTACT_PATTERNS.some((pattern) => pattern.test(String(url)));
}

async function installReadOnlyGuard(context, events) {
  await context.route("**/*", async (route) => {
    const request = route.request();
    const method = request.method().toUpperCase();
    const url = request.url();
    if (method !== "GET" || isUnsafeContactUrl(url)) {
      const row = {
        method,
        url: safeUrl(url),
        resource_type: request.resourceType(),
        first_party: isFirstParty(url),
        reason: method !== "GET" ? "non-GET request" : "unsafe contact URL",
      };
      events.guard_blocks.push(row);
      if (row.first_party && method !== "GET") {
        events.first_party_non_get_attempts.push(row);
      }
      await route.abort("blockedbyclient");
      return;
    }
    await route.continue();
  });
}

function wireEvents(page, events) {
  page.on("console", (message) => {
    if (message.type() === "error") events.console_errors.push(message.text());
    if (message.type() === "warning") events.console_warnings.push(message.text());
  });
  page.on("pageerror", (error) => {
    events.page_errors.push(String(error?.message || error));
  });
  page.on("response", (response) => {
    if (response.status() >= 400) {
      events.response_failures.push({
        status: response.status(),
        method: response.request().method(),
        first_party: isFirstParty(response.url()),
        url: safeUrl(response.url()),
      });
    }
  });
  page.on("requestfailed", (request) => {
    const guardBlocked = events.guard_blocks.some(
      (row) =>
        row.method === request.method() && row.url === safeUrl(request.url())
    );
    events.request_failures.push({
      method: request.method(),
      first_party: isFirstParty(request.url()),
      guard_blocked: guardBlocked,
      error: String(request.failure()?.errorText || ""),
      url: safeUrl(request.url()),
    });
  });
}

function assertion(name, pass, actual, expected) {
  return { name, pass: Boolean(pass), actual, expected };
}

async function runUtopiaCase(
  browser,
  runDir,
  lang,
  viewportName,
  args,
  telemetryBaseline
) {
  const spec = LANGUAGES[lang];
  const vp = VIEWPORTS[viewportName];
  const url = expectedUrls()[lang];
  const events = makeEvents();
  const context = await browser.newContext({
    viewport: vp.viewport,
    locale: spec.locale,
    isMobile: vp.isMobile,
    hasTouch: vp.hasTouch,
    deviceScaleFactor: 1,
    serviceWorkers: "block",
  });
  await installReadOnlyGuard(context, events);
  const page = await context.newPage();
  wireEvents(page, events);
  const prefix = `utopia-${lang}-${viewportName}`;
  const screenshots = {};
  try {
    const response = await page.goto(url, {
      waitUntil: "domcontentloaded",
      timeout: args.timeoutMs,
    });
    await page.waitForTimeout(500);
    await page.evaluate(() => window.scrollTo(0, 0));
    screenshots.top = path.join(runDir, "utopia", `${prefix}-top.png`);
    await page.screenshot({ path: screenshots.top, fullPage: false });

    const showroom = page.locator("#utopia-showroom");
    if ((await showroom.count()) === 1) {
      await showroom.scrollIntoViewIfNeeded();
      await page.waitForTimeout(350);
    }
    const modelLoaded = await page
      .waitForFunction(
        () => {
          const model = document.querySelector("#utopia-model-viewer");
          return Boolean(
            model &&
              (model.loaded === true ||
                model.classList.contains("loaded"))
          );
        },
        null,
        { timeout: Math.min(args.timeoutMs, 30000) }
      )
      .then(() => true)
      .catch(() => false);
    const building = page.locator("[data-utopia-building]").first();
    if ((await building.count()) === 1) {
      await building.click();
      await page.waitForTimeout(450);
    }
    screenshots.model = path.join(runDir, "utopia", `${prefix}-model.png`);
    await page.screenshot({ path: screenshots.model, fullPage: false });

    const firstReference = page.locator("[data-utopia-reference]").first();
    if ((await firstReference.count()) === 1) {
      await firstReference.scrollIntoViewIfNeeded();
      await firstReference.click();
      await page.waitForTimeout(350);
    }
    screenshots.reference = path.join(
      runDir,
      "utopia",
      `${prefix}-reference.png`
    );
    await page.screenshot({ path: screenshots.reference, fullPage: false });

    const mapHost = page.locator("#utopia-context-map");
    if ((await mapHost.count()) === 1) {
      await mapHost.scrollIntoViewIfNeeded();
      await page.waitForTimeout(700);
      await page
        .waitForFunction(
          () =>
            document.querySelectorAll("#utopia-context-map .mapboxgl-canvas")
              .length === 1 ||
            !document.querySelector(".utopia-map-fallback")?.hidden,
          null,
          { timeout: Math.min(args.timeoutMs, 30000) }
        )
        .catch(() => {});
    }
    screenshots.map = path.join(runDir, "utopia", `${prefix}-map.png`);
    await page.screenshot({ path: screenshots.map, fullPage: false });

    const state = await page.evaluate(() => {
      const normalize = (value) => String(value || "").replace(/\s+/gu, " ").trim();
      const model = document.querySelector("#utopia-model-viewer");
      const metrics = document.querySelector("#utopia-building-metrics");
      const contextText = normalize(
        document.querySelector("[data-utopia-form-context]")?.textContent
      );
      return {
        title: document.title,
        html_lang: document.documentElement.lang,
        html_dir:
          document.documentElement.dir ||
          getComputedStyle(document.documentElement).direction,
        canonical: [
          ...document.querySelectorAll('link[rel="canonical"][href]'),
        ].map((node) => node.href),
        hreflang: [
          ...document.querySelectorAll("link[hreflang][href]"),
        ].map((node) => ({
          lang: String(node.getAttribute("hreflang") || "").toLowerCase(),
          href: node.href,
        })),
        h1_count: document.querySelectorAll("h1").length,
        utopia_roots: document.querySelectorAll("#utopia-showroom").length,
        shared_roots: document.querySelectorAll(
          "#nl-root,#nl-app,#nlp3d,#nlv2"
        ).length,
        model_count: document.querySelectorAll("#utopia-model-viewer").length,
        model_src: model?.src || model?.getAttribute("src") || "",
        model_loaded: Boolean(
          model &&
            (model.loaded === true ||
              model.classList.contains("loaded"))
        ),
        building_buttons: document.querySelectorAll(
          "[data-utopia-building]"
        ).length,
        building_hotspots: document.querySelectorAll(
          ".utopia-model-hotspot[data-building]"
        ).length,
        metrics_visible: Boolean(metrics && !metrics.hidden),
        plan_cards: document.querySelectorAll("[data-plan-card]").length,
        references: document.querySelectorAll(
          "[data-utopia-reference]"
        ).length,
        active_references: document.querySelectorAll(
          "[data-utopia-reference].is-active"
        ).length,
        form_context: contextText,
        map_hosts: document.querySelectorAll("#utopia-context-map").length,
        map_canvases: document.querySelectorAll(
          "#utopia-context-map .mapboxgl-canvas"
        ).length,
        map_fallback_visible: (() => {
          const fallback = document.querySelector(".utopia-map-fallback");
          return Boolean(fallback && !fallback.hidden);
        })(),
        map_layer_controls: document.querySelectorAll(
          "[data-map-layer]"
        ).length,
        apartment_selectors: document.querySelectorAll(
          '[data-act="select"],[data-unit-id],[data-apartment-hotspot]'
        ).length,
        view_cones: document.querySelectorAll(
          "[data-view-cone],.nl-view-cone,.utopia-view-cone"
        ).length,
        horizontal_overflow_px: Math.max(
          0,
          document.documentElement.scrollWidth -
            document.documentElement.clientWidth
        ),
      };
    });
    const desiredHreflang = expectedHreflang();
    const actualHreflang = Object.fromEntries(
      state.hreflang.map((row) => [row.lang, normalizeUrl(row.href)])
    );
    const firstPartyFailures = [
      ...events.response_failures.filter((row) => row.first_party),
      ...events.request_failures.filter(
        (row) => row.first_party && !row.guard_blocked
      ),
    ];
    const guards = classifyGuardBlocks(
      events.guard_blocks,
      telemetryBaseline
    );
    const assertions = [
      assertion("HTTP 200", response?.status() === 200, response?.status() || 0, 200),
      assertion(
        "no redirect",
        normalizeUrl(page.url()) === normalizeUrl(url),
        page.url(),
        url
      ),
      assertion(
        "document language",
        state.html_lang.toLowerCase().split("-")[0] === lang,
        state.html_lang,
        lang
      ),
      assertion("document direction", state.html_dir === spec.dir, state.html_dir, spec.dir),
      assertion(
        "one self canonical",
        state.canonical.length === 1 &&
          normalizeUrl(state.canonical[0]) === normalizeUrl(url),
        state.canonical,
        [url]
      ),
      assertion(
        "exact six hreflang links",
        Object.keys(desiredHreflang).every(
          (code) =>
            actualHreflang[code] === normalizeUrl(desiredHreflang[code])
        ) && state.hreflang.length === 6,
        actualHreflang,
        desiredHreflang
      ),
      assertion("one H1", state.h1_count === 1, state.h1_count, 1),
      assertion("one UTOPIA root", state.utopia_roots === 1, state.utopia_roots, 1),
      assertion("no shared showroom root", state.shared_roots === 0, state.shared_roots, 0),
      assertion("one loaded model", modelLoaded && state.model_count === 1 && state.model_loaded, state, "one loaded #utopia-model-viewer"),
      assertion("exact UTOPIA model URL", safeUrl(state.model_src) === MODEL_URL, safeUrl(state.model_src), MODEL_URL),
      assertion("four building controls", state.building_buttons === 4 && state.building_hotspots === 4, { buttons: state.building_buttons, hotspots: state.building_hotspots }, { buttons: 4, hotspots: 4 }),
      assertion("building selection updates facts", state.metrics_visible, state.metrics_visible, true),
      assertion("seven published plan groups", state.plan_cards === 7, state.plan_cards, 7),
      assertion("29 published apartment/floor references", state.references === 29, state.references, 29),
      assertion("reference selection updates enquiry context", state.active_references === 1 && state.form_context.length > 0, { active: state.active_references, context: state.form_context }, "one active reference and non-empty context"),
      assertion("context map rendered", state.map_hosts === 1 && state.map_canvases === 1 && !state.map_fallback_visible, { hosts: state.map_hosts, canvases: state.map_canvases, fallback: state.map_fallback_visible }, { hosts: 1, canvases: 1, fallback: false }),
      assertion("nine map controls", state.map_layer_controls === 9, state.map_layer_controls, 9),
      assertion("no apartment hotspot mapping", state.apartment_selectors === 0, state.apartment_selectors, 0),
      assertion("no fabricated view cone", state.view_cones === 0, state.view_cones, 0),
      assertion("no horizontal overflow", state.horizontal_overflow_px === 0, state.horizontal_overflow_px, 0),
      assertion("no first-party failures", firstPartyFailures.length === 0, firstPartyFailures, []),
      assertion("no first-party non-GET attempts", events.first_party_non_get_attempts.length === 0, events.first_party_non_get_attempts, []),
      assertion(
        "no telemetry endpoint beyond immutable BEFORE baseline",
        guards.pass,
        guards.counts,
        { first_party: 0, new_third_party: 0 }
      ),
      assertion(
        "no unclassified console errors",
        events.console_errors.every((message) =>
          /ERR_BLOCKED_BY_CLIENT/iu.test(message)
        ),
        events.console_errors,
        "only guard-induced ERR_BLOCKED_BY_CLIENT messages"
      ),
      assertion("no page errors", events.page_errors.length === 0, events.page_errors, []),
    ];
    return {
      lang,
      viewport: viewportName,
      viewport_size: vp.viewport,
      url,
      status: response?.status() || 0,
      state,
      events,
      guard_classification: guards,
      screenshots: Object.fromEntries(
        Object.entries(screenshots).map(([key, value]) => [
          key,
          relativeToRoot(value),
        ])
      ),
      assertions,
      failures: assertions.filter((row) => !row.pass),
      pass: assertions.every((row) => row.pass),
    };
  } catch (error) {
    return {
      lang,
      viewport: viewportName,
      viewport_size: vp.viewport,
      url,
      events,
      screenshots: Object.fromEntries(
        Object.entries(screenshots).map(([key, value]) => [
          key,
          relativeToRoot(value),
        ])
      ),
      error: String(error?.stack || error),
      assertions: [],
      failures: [{ name: "case threw", error: String(error?.message || error) }],
      pass: false,
    };
  } finally {
    await context.close();
  }
}

async function captureUtopia(
  runDir,
  args,
  preflightResult,
  telemetryBaseline
) {
  const utopiaDir = path.join(runDir, "utopia");
  await fs.mkdir(utopiaDir, { recursive: true });
  const browser = await chromium.launch({
    channel: "chrome",
    headless: !args.headed,
    args: ["--disable-background-networking"],
  });
  const cases = [];
  try {
    for (const lang of Object.keys(LANGUAGES)) {
      for (const viewportName of Object.keys(VIEWPORTS)) {
        const row = await runUtopiaCase(
          browser,
          runDir,
          lang,
          viewportName,
          args,
          telemetryBaseline
        );
        cases.push(row);
        console.log(
          `[utopia] ${lang}/${viewportName}: ${row.pass ? "PASS" : "FAIL"}`
        );
      }
    }
  } finally {
    await browser.close();
  }
  const model = await getBytes(MODEL_URL, {
    timeoutMs: args.timeoutMs,
    redirect: "manual",
  });
  const modelResult = {
    url: MODEL_URL,
    status: model.status,
    bytes: model.bytes,
    expected_bytes: MODEL_BYTES,
    sha256: model.sha256,
    expected_sha256: MODEL_SHA256,
    pass:
      model.status === 200 &&
      !model.location &&
      model.bytes === MODEL_BYTES &&
      model.sha256 === MODEL_SHA256,
  };
  const currentSourceHashes = preflightResult.routes.map((row) => ({
    lang: row.lang,
    url: row.url,
    status: row.status,
    bytes: row.bytes,
    sha256: row.source_sha256,
    pass: row.pass,
  }));
  const report = {
    schema: "nadlan-utopia-five-language-after/v1",
    generated_at: new Date().toISOString(),
    expected_version: args.expectedVersion,
    cases,
    current_source_hashes: currentSourceHashes,
    model: modelResult,
    cases_passed: cases.filter((row) => row.pass).length,
    cases_total: cases.length,
    pass:
      cases.length === 10 &&
      cases.every((row) => row.pass) &&
      currentSourceHashes.length === 5 &&
      currentSourceHashes.every((row) => row.pass) &&
      modelResult.pass,
  };
  await fs.writeFile(
    path.join(utopiaDir, "report.json"),
    `${JSON.stringify(report, null, 2)}\n`,
    "utf8"
  );
  return report;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

async function imageDataUrl(filePath) {
  const bytes = await fs.readFile(filePath);
  return `data:image/png;base64,${bytes.toString("base64")}`;
}

async function renderContactSheet(browser, outputPath, title, rows) {
  const cards = [];
  for (const row of rows) {
    const images = [];
    for (const imageRow of row.images) {
      const src = await imageDataUrl(imageRow.path);
      images.push(
        `<figure><figcaption>${escapeHtml(imageRow.label)}</figcaption><img src="${src}" alt=""></figure>`
      );
    }
    cards.push(
      `<section><h2>${escapeHtml(row.label)}</h2><div class="pair">${images.join("")}</div></section>`
    );
  }
  const page = await browser.newPage({
    viewport: { width: 1240, height: 900 },
    deviceScaleFactor: 1,
  });
  try {
    await page.setContent(
      `<!doctype html><html><head><meta charset="utf-8"><style>
      *{box-sizing:border-box}body{margin:0;padding:24px;background:#f3f0e8;color:#17202a;font:15px Arial,sans-serif}
      h1{margin:0 0 20px;font-size:26px}section{background:white;border:1px solid #cfc8b8;border-radius:12px;margin:0 0 18px;padding:14px;break-inside:avoid}
      h2{font-size:16px;margin:0 0 10px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px}
      figure{margin:0;min-width:0}figcaption{font-weight:700;margin:0 0 6px}img{display:block;width:100%;height:auto;border:1px solid #ddd}
      </style></head><body><h1>${escapeHtml(title)}</h1>${cards.join("")}</body></html>`,
      { waitUntil: "load" }
    );
    await page.screenshot({ path: outputPath, fullPage: true });
  } finally {
    await page.close();
  }
}

async function createContactSheets(
  runDir,
  beforeReport,
  matureReport,
  utopiaReport
) {
  const outDir = path.join(runDir, "contact-sheets");
  await fs.mkdir(outDir, { recursive: true });
  const browser = await chromium.launch({
    channel: "chrome",
    headless: true,
    args: ["--disable-background-networking"],
  });
  const outputs = [];
  try {
    for (const family of FAMILY_KEYS) {
      for (const kind of ["top", "showroom"]) {
        const rows = [];
        for (const lang of Object.keys(LANGUAGES)) {
          for (const viewport of Object.keys(VIEWPORTS)) {
            const before = beforeReport.matrix.find(
              (row) =>
                row.family === family &&
                row.lang === lang &&
                row.viewport === viewport
            );
            const after = matureReport.matrix.find(
              (row) =>
                row.family === family &&
                row.lang === lang &&
                row.viewport === viewport
            );
            const beforePath = before?.screenshots?.[kind]
              ? path.resolve(ROOT, before.screenshots[kind])
              : null;
            const afterPath = after?.screenshots?.[kind]
              ? path.resolve(ROOT, after.screenshots[kind])
              : null;
            if (!beforePath || !afterPath) {
              throw new Error(
                `Missing ${kind} screenshot pair for ${family}/${lang}/${viewport}`
              );
            }
            rows.push({
              label: `${lang.toUpperCase()} - ${viewport}`,
              images: [
                { label: "BEFORE", path: beforePath },
                { label: "AFTER", path: afterPath },
              ],
            });
          }
        }
        const output = path.join(outDir, `${family}-${kind}-before-after.png`);
        await renderContactSheet(
          browser,
          output,
          `${family} - ${kind} - BEFORE vs AFTER`,
          rows
        );
        outputs.push(relativeToRoot(output));
      }
    }
    const utopiaRows = Object.keys(LANGUAGES).map((lang) => {
      const desktop = utopiaReport.cases.find(
        (row) => row.lang === lang && row.viewport === "desktop"
      );
      const mobile = utopiaReport.cases.find(
        (row) => row.lang === lang && row.viewport === "mobile"
      );
      if (!desktop?.screenshots?.model || !mobile?.screenshots?.model) {
        throw new Error(`Missing UTOPIA model screenshots for ${lang}`);
      }
      return {
        label: lang.toUpperCase(),
        images: [
          {
            label: "Desktop 1440x1000",
            path: path.resolve(ROOT, desktop.screenshots.model),
          },
          {
            label: "Mobile 390x844",
            path: path.resolve(ROOT, mobile.screenshots.model),
          },
        ],
      };
    });
    const utopiaOutput = path.join(
      outDir,
      "utopia-five-language-desktop-mobile.png"
    );
    await renderContactSheet(
      browser,
      utopiaOutput,
      "UTOPIA - five languages - desktop and mobile",
      utopiaRows
    );
    outputs.push(relativeToRoot(utopiaOutput));
  } finally {
    await browser.close();
  }
  return outputs;
}

function markdownReadout(report) {
  const lines = [
    `# UTOPIA live AFTER regression - ${report.expected_version}`,
    "",
    `Overall result: ${report.pass ? "PASS" : "FAIL"}`,
    "",
    `- Opening and terminal live-state stability: ${report.preflight.pass ? "PASS" : "FAIL"}`,
    `- Immutable BEFORE evidence unchanged: ${report.immutable_before.unchanged ? "YES" : "NO"}`,
    `- Mature static matrix: ${report.mature.matrix_passed}/${report.mature.matrix_total}`,
    `- Mature deep journeys: ${report.mature.deep_passed}/${report.mature.deep_total}`,
    `- Mature URL/REST/model regression gate: ${report.comparisons.pass ? "PASS" : "FAIL"}`,
    `- Current comparison sources available: ${report.comparisons.current_source_availability.available}/${report.comparisons.current_source_availability.total} (availability only, not unchanged proof)`,
    `- UTOPIA five-language desktop/mobile cases: ${report.utopia.cases_passed}/${report.utopia.cases_total}`,
    `- Contact sheets: ${report.contact_sheets.length}`,
    `- First-party non-GET attempts: ${report.safety.first_party_non_get_attempts}`,
    `- New third-party non-GET endpoints beyond BEFORE: ${report.safety.new_third_party_non_get_attempts}`,
    `- BEFORE-baseline telemetry requests blocked: ${report.safety.before_baseline_matched_telemetry_blocks}`,
    "",
    "## Evidence",
    "",
    `- Machine report: \`${report.paths.report}\``,
    `- Mature journey report: \`${report.paths.mature_report}\``,
    `- UTOPIA report: \`${report.paths.utopia_report}\``,
    `- SHA-256 manifest: \`${report.paths.manifest}\``,
    "",
    "The gate allowed GET requests only. It did not fill or submit forms and did not click contact, WhatsApp, RFP, video-call or co-tour controls.",
    "",
  ];
  return lines.join("\n");
}

async function writeManifest(runDir) {
  const manifestPath = path.join(runDir, "artifact-manifest.sha256");
  const entries = await fs.readdir(runDir, {
    recursive: true,
    withFileTypes: true,
  });
  const rows = [];
  for (const entry of entries) {
    if (!entry.isFile()) continue;
    const fullPath = path.join(entry.parentPath, entry.name);
    if (fullPath === manifestPath) continue;
    const bytes = await fs.readFile(fullPath);
    rows.push({
      relative: path.relative(runDir, fullPath).replaceAll("\\", "/"),
      hash: sha256(bytes),
    });
  }
  rows.sort((a, b) => a.relative.localeCompare(b.relative));
  await fs.writeFile(
    manifestPath,
    `${rows.map((row) => `${row.hash}  ${row.relative}`).join("\n")}\n`,
    "utf8"
  );
  return { path: manifestPath, entries: rows.length };
}

function publicPreflight(preflightResult) {
  return {
    ...preflightResult,
    routes: preflightResult.routes.map(({ _body, ...row }) => row),
  };
}

function compareTerminalPreflights(start, end) {
  const routeChecks = Object.keys(LANGUAGES).map((lang) => {
    const opening = start.routes.find((row) => row.lang === lang);
    const closing = end.routes.find((row) => row.lang === lang);
    const pass =
      Boolean(opening && closing) &&
      opening.status === 200 &&
      closing.status === 200 &&
      normalizeUrl(opening.url) === normalizeUrl(closing.url) &&
      normalizeUrl(opening.final_url) === normalizeUrl(closing.final_url) &&
      opening.source_sha256 === closing.source_sha256;
    return {
      lang,
      opening_status: opening?.status ?? null,
      closing_status: closing?.status ?? null,
      opening_url: opening?.final_url ?? null,
      closing_url: closing?.final_url ?? null,
      opening_source_sha256: opening?.source_sha256 ?? null,
      closing_source_sha256: closing?.source_sha256 ?? null,
      pass,
    };
  });
  const version = {
    expected: start.expected_version,
    opening: start.health?.version || null,
    closing: end.health?.version || null,
    pass:
      start.health?.version === start.expected_version &&
      end.health?.version === start.expected_version &&
      start.health?.version === end.health?.version,
  };
  const model = {
    opening_status: start.model?.status ?? null,
    closing_status: end.model?.status ?? null,
    opening_url: start.model?.final_url ?? null,
    closing_url: end.model?.final_url ?? null,
    opening_bytes: start.model?.bytes ?? null,
    closing_bytes: end.model?.bytes ?? null,
    opening_sha256: start.model?.sha256 ?? null,
    closing_sha256: end.model?.sha256 ?? null,
    pass:
      start.model?.pass === true &&
      end.model?.pass === true &&
      start.model?.status === end.model?.status &&
      start.model?.final_url === end.model?.final_url &&
      start.model?.bytes === end.model?.bytes &&
      start.model?.sha256 === end.model?.sha256,
  };
  return {
    opening_label: start.label,
    closing_label: end.label,
    cache_busted: start.cache_busted === true && end.cache_busted === true,
    version,
    routes: routeChecks,
    model,
    pass:
      start.pass &&
      end.pass &&
      version.pass &&
      routeChecks.length === 5 &&
      routeChecks.every((row) => row.pass) &&
      model.pass,
  };
}

async function runSelfTest(args) {
  const beforeIntegrity = await verifyBeforeIntegrity();
  const beforeReport = JSON.parse(
    await fs.readFile(BEFORE_REPORT_PATH, "utf8")
  );
  const telemetryBaseline = deriveTelemetryBaseline(beforeReport);
  const knownRows = telemetryBaseline.endpoints.map((row) => ({
    method: row.method,
    url: `https://${row.host}${row.path}?ignored=query`,
    first_party: false,
  }));
  const knownClassification = classifyGuardBlocks(
    knownRows,
    telemetryBaseline
  );
  const additionClassification = classifyGuardBlocks(
    [
      ...knownRows,
      {
        method: "PUT",
        url: "https://new-telemetry.invalid/collect",
        first_party: false,
      },
    ],
    telemetryBaseline
  );
  const opening = {
    pass: true,
    label: "opening",
    cache_busted: true,
    expected_version: args.expectedVersion,
    health: { version: args.expectedVersion },
    routes: Object.entries(expectedUrls()).map(([lang, url]) => ({
      lang,
      url,
      status: 200,
      final_url: url,
      source_sha256: sha256(Buffer.from(`${lang}-stable`)),
    })),
    model: {
      pass: true,
      status: 200,
      final_url: MODEL_URL,
      bytes: MODEL_BYTES,
      sha256: MODEL_SHA256,
    },
  };
  const identicalClosing = structuredClone(opening);
  identicalClosing.label = "terminal";
  const changedClosing = structuredClone(identicalClosing);
  changedClosing.routes[0].source_sha256 = sha256(
    Buffer.from("changed-source")
  );
  const stableComparison = compareTerminalPreflights(
    opening,
    identicalClosing
  );
  const changedComparison = compareTerminalPreflights(
    opening,
    changedClosing
  );
  const treeParentSource = [
    'const { spawn } = require("node:child_process");',
    'const grandchild = spawn(process.execPath, ["-e", "setInterval(() => {}, 1000)"], { stdio: "ignore" });',
    'process.stdout.write("grandchild_pid=" + grandchild.pid + "\\n");',
    "setInterval(() => {}, 1000);",
  ].join("\n");
  const watchdog = await runChild(
    process.execPath,
    ["-e", treeParentSource],
    { timeoutMs: 750 }
  );
  const grandchildPid = Number(
    watchdog.stdout.match(/grandchild_pid=(\d+)/u)?.[1] || 0
  );
  const childProcessTreeTerminated =
    grandchildPid > 0 && (await waitForProcessExit(grandchildPid, 5000));
  if (grandchildPid > 0 && !childProcessTreeTerminated) {
    await terminateProcessTree(grandchildPid);
    await waitForProcessExit(grandchildPid, 5000);
  }
  const diagnosticTestRoot = await fs.mkdtemp(
    path.join(os.tmpdir(), "nadlan-after-diagnostic-test-")
  );
  let childDiagnosticsPreserved = false;
  try {
    const partialSource = path.join(
      diagnosticTestRoot,
      "docs",
      "qa",
      "screenshots",
      ".partial-child",
      "partial-report.json"
    );
    const diagnosticDestination = path.join(
      diagnosticTestRoot,
      "durable",
      "mature"
    );
    await fs.mkdir(path.dirname(partialSource), { recursive: true });
    await fs.mkdir(diagnosticDestination, { recursive: true });
    await fs.writeFile(partialSource, '{"partial":true\n', "utf8");
    let ingestionRejected = false;
    try {
      await withChildDiagnosticPreservation(
        diagnosticTestRoot,
        diagnosticDestination,
        async () => JSON.parse(await fs.readFile(partialSource, "utf8"))
      );
    } catch {
      ingestionRejected = true;
    }
    childDiagnosticsPreserved =
      ingestionRejected &&
      (await fs
        .readFile(
          path.join(
            diagnosticDestination,
            "child-diagnostics",
            ".partial-child",
            "partial-report.json"
          ),
          "utf8"
        )
        .then((value) => value.includes('"partial":true'))
        .catch(() => false));
  } finally {
    await fs.rm(diagnosticTestRoot, { recursive: true, force: true });
  }
  const report = {
    schema: "nadlan-utopia-after-regression-self-test/v1",
    before_integrity: {
      pass: beforeIntegrity.pass,
      verified: beforeIntegrity.verified,
      entries: beforeIntegrity.entries,
    },
    telemetry_baseline: publicTelemetryBaseline(telemetryBaseline),
    telemetry_known_subset_passes: knownClassification.pass,
    telemetry_addition_fails:
      !additionClassification.pass &&
      additionClassification.counts.new_third_party === 1,
    identical_terminal_state_passes: stableComparison.pass,
    changed_terminal_source_fails: !changedComparison.pass,
    watchdog_times_out:
      watchdog.timedOut === true &&
      watchdog.duration_ms < 10000 &&
      watchdog.termination?.pass === true,
    child_process_tree_terminated: childProcessTreeTerminated,
    child_diagnostics_preserved: childDiagnosticsPreserved,
    headed_mode_propagates:
      matureChildEnvironment({ headed: true }).NADLAN_MATURE_QA_HEADED ===
        "1" &&
      matureChildEnvironment({ headed: false }).NADLAN_MATURE_QA_HEADED ===
        "0",
  };
  report.pass =
    report.before_integrity.pass &&
    report.telemetry_baseline.pass &&
    report.telemetry_known_subset_passes &&
    report.telemetry_addition_fails &&
    report.identical_terminal_state_passes &&
    report.changed_terminal_source_fails &&
    report.watchdog_times_out &&
    report.child_process_tree_terminated &&
    report.child_diagnostics_preserved &&
    report.headed_mode_propagates;
  console.log(JSON.stringify(report, null, 2));
  process.exitCode = report.pass ? 0 : 1;
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.selfTest) {
    await runSelfTest(args);
    return;
  }
  const openingPreflight = await preflight(args, { label: "opening" });
  console.log(
    JSON.stringify(
      {
        mode: args.preflightOnly ? "preflight-only" : "full-after",
        expected_version: args.expectedVersion,
        pass: openingPreflight.pass,
        health: openingPreflight.health,
        model: openingPreflight.model,
        routes: openingPreflight.routes.map((row) => ({
          lang: row.lang,
          status: row.status,
          pass: row.pass,
        })),
      },
      null,
      2
    )
  );
  if (args.preflightOnly) {
    process.exitCode = openingPreflight.pass ? 0 : 1;
    return;
  }
  if (!openingPreflight.pass) {
    throw new Error(
      `Fail-closed preflight: production is not nadlan-config ${args.expectedVersion} with five exact HTTP 200 UTOPIA routes. No AFTER evidence directory was created.`
    );
  }

  const beforeInitial = await verifyBeforeIntegrity();
  if (!beforeInitial.pass) {
    throw new Error(
      "Immutable BEFORE evidence failed its SHA-256 manifest before capture."
    );
  }
  const stamp = runStamp();
  const runDir = path.join(
    SCREENSHOT_ROOT,
    `mature-showroom-after-${args.expectedVersion}-${stamp}`
  );
  const runDirExists = await fs
    .stat(runDir)
    .then(() => true)
    .catch(() => false);
  if (runDirExists) {
    throw new Error(`Refusing to overwrite existing AFTER evidence: ${runDir}`);
  }
  await fs.mkdir(runDir, { recursive: false });
  let report;
  let terminalPreflight = null;
  let terminalStability = null;
  try {
    const beforeReport = JSON.parse(
      await fs.readFile(BEFORE_REPORT_PATH, "utf8")
    );
    const beforeState = JSON.parse(
      await fs.readFile(BEFORE_STATE_PATH, "utf8")
    );
    const telemetryBaseline = deriveTelemetryBaseline(beforeReport);
    if (!telemetryBaseline.pass) {
      throw new Error(
        "Could not derive a valid telemetry method/host/path baseline from immutable BEFORE evidence."
      );
    }
    const matureReport = await runMatureCapture(runDir, args);
    const matureGate = evaluateMatureCapture(
      matureReport,
      telemetryBaseline
    );
    const comparisons = await captureComparisonEvidence(
      matureReport,
      beforeReport,
      beforeState
    );
    const utopiaReport = await captureUtopia(
      runDir,
      args,
      openingPreflight,
      telemetryBaseline
    );
    const contactSheets = await createContactSheets(
      runDir,
      beforeReport,
      matureReport,
      utopiaReport
    );
    const beforeFinal = await verifyBeforeIntegrity();
    const unchanged =
      beforeInitial.pass &&
      beforeFinal.pass &&
      beforeInitial.manifest_sha256 === beforeFinal.manifest_sha256 &&
      beforeInitial.report_sha256 === beforeFinal.report_sha256;
    terminalPreflight = await preflight(args, { label: "terminal" });
    terminalStability = compareTerminalPreflights(
      openingPreflight,
      terminalPreflight
    );
    const allGuardCounts = {
      baselineMatched:
        matureGate.guard_classification.counts
          .baseline_matched_third_party +
        utopiaReport.cases.reduce(
          (sum, row) =>
            sum +
            (row.guard_classification?.counts
              ?.baseline_matched_third_party || 0),
          0
        ),
      additions:
        matureGate.guard_classification.counts.new_third_party +
        utopiaReport.cases.reduce(
          (sum, row) =>
            sum +
            (row.guard_classification?.counts?.new_third_party || 0),
          0
        ),
      firstParty:
        matureGate.guard_classification.counts.first_party +
        utopiaReport.cases.reduce(
          (sum, row) =>
            sum + (row.guard_classification?.counts?.first_party || 0),
          0
        ),
    };
    report = {
      schema: "nadlan-utopia-after-regression/v1",
      generated_at: new Date().toISOString(),
      run_stamp: stamp,
      site: SITE,
      expected_version: args.expectedVersion,
      read_only: true,
      deployment_performed: false,
      preflight: {
        opening: publicPreflight(openingPreflight),
        terminal: publicPreflight(terminalPreflight),
        stability: terminalStability,
        pass: terminalStability.pass,
      },
      immutable_before: {
        initial: beforeInitial,
        final: beforeFinal,
        unchanged,
      },
      mature: {
        matrix_passed: matureGate.matrix_passed,
        matrix_total: matureGate.matrix_total,
        deep_passed: matureGate.deep_passed,
        deep_total: matureGate.deep_total,
        guard_classification: matureGate.guard_classification.counts,
        pass: matureGate.pass,
        checks: {
          matrix: matureGate.matrix,
          deep: matureGate.deep,
        },
      },
      comparisons,
      telemetry_baseline: publicTelemetryBaseline(telemetryBaseline),
      utopia: {
        cases_passed: utopiaReport.cases_passed,
        cases_total: utopiaReport.cases_total,
        model: utopiaReport.model,
        pass: utopiaReport.pass,
      },
      safety: {
        request_methods_allowed: ["GET"],
        forms_filled: false,
        forms_submitted: false,
        contact_controls_clicked: false,
        before_baseline_matched_telemetry_blocks:
          allGuardCounts.baselineMatched,
        new_third_party_non_get_attempts: allGuardCounts.additions,
        first_party_non_get_attempts: allGuardCounts.firstParty,
      },
      contact_sheets: contactSheets,
      paths: {
        report: relativeToRoot(path.join(runDir, "report.json")),
        readout: relativeToRoot(path.join(runDir, "readout.md")),
        mature_report: relativeToRoot(
          path.join(runDir, "mature", "report.json")
        ),
        utopia_report: relativeToRoot(
          path.join(runDir, "utopia", "report.json")
        ),
        manifest: relativeToRoot(
          path.join(runDir, "artifact-manifest.sha256")
        ),
      },
      pass:
        openingPreflight.pass &&
        terminalStability.pass &&
        telemetryBaseline.pass &&
        unchanged &&
        matureGate.pass &&
        comparisons.pass &&
        utopiaReport.pass &&
        contactSheets.length === 9 &&
        allGuardCounts.additions === 0 &&
        allGuardCounts.firstParty === 0,
    };
    await fs.writeFile(
      path.join(runDir, "report.json"),
      `${JSON.stringify(report, null, 2)}\n`,
      "utf8"
    );
    await fs.writeFile(
      path.join(runDir, "readout.md"),
      markdownReadout(report),
      "utf8"
    );
    const manifest = await writeManifest(runDir);
    console.log(
      JSON.stringify(
        {
          pass: report.pass,
          expected_version: args.expectedVersion,
          evidence_directory: runDir,
          report: path.join(runDir, "report.json"),
          manifest_entries: manifest.entries,
          mature_matrix: `${report.mature.matrix_passed}/${report.mature.matrix_total}`,
          mature_deep: `${report.mature.deep_passed}/${report.mature.deep_total}`,
          utopia_cases: `${report.utopia.cases_passed}/${report.utopia.cases_total}`,
        },
        null,
        2
      )
    );
  } catch (error) {
    const fatal = {
      schema: "nadlan-utopia-after-regression/v1",
      generated_at: new Date().toISOString(),
      expected_version: args.expectedVersion,
      pass: false,
      fatal: String(error?.stack || error),
      preflight: {
        opening: publicPreflight(openingPreflight),
        terminal: terminalPreflight
          ? publicPreflight(terminalPreflight)
          : null,
        stability: terminalStability,
      },
      read_only: true,
      deployment_performed: false,
    };
    await fs.writeFile(
      path.join(runDir, "report.json"),
      `${JSON.stringify(fatal, null, 2)}\n`,
      "utf8"
    );
    await fs.writeFile(
      path.join(runDir, "readout.md"),
      `# UTOPIA live AFTER regression\n\nOverall result: FAIL\n\n${fatal.fatal}\n`,
      "utf8"
    );
    await writeManifest(runDir);
    throw error;
  }
  process.exitCode = report.pass ? 0 : 1;
}

main().catch((error) => {
  console.error(error?.stack || error);
  process.exit(1);
});
