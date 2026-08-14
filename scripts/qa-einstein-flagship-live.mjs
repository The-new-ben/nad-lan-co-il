#!/usr/bin/env node

/**
 * Real-Chromium acceptance for the password-protected Einstein flagship stage.
 *
 * Required: SANDBOX_URL, SANDBOX_POST_PASSWORD
 * Optional: OUTPUT_DIR, NL_EINSTEIN_CHROME_PATH
 *
 * The password, cookies, request bodies/headers and storage values are never
 * printed or serialized. The runner performs no lead/comment write.
 */
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { chromium } from "playwright";

const TARGET_RAW = String(process.env.SANDBOX_URL || "").trim();
const POST_PASSWORD = String(process.env.SANDBOX_POST_PASSWORD || "");
const EXPECTED_STAGE_POST_ID_RAW = String(process.env.EXPECTED_STAGE_POST_ID || "").trim();
const EXPECTED_PLUGIN_VERSION = String(process.env.EXPECTED_PLUGIN_VERSION || "").trim();
const EXPECTED_PROJECT_CONTRACT_ID = String(process.env.EXPECTED_PROJECT_CONTRACT_ID || "").trim();
const OUTPUT_DIR = path.resolve(process.cwd(), String(process.env.OUTPUT_DIR || "output/playwright/einstein-flagship-live").trim());
const SCREENSHOT_DIR = path.join(OUTPUT_DIR, "screenshots");
const CHROME_PATH = process.env.NL_EINSTEIN_CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const CONTRACT_ID = "einstein-tower-6885-32";
const ASSET_PREFIX = `/flagship-private-asset/${CONTRACT_ID}/`;
const EXPECTED_TOOLS = ["view", "interior", "design", "comments"];
const EXPECTED_SCENES = ["living", "bedroom", "arrival", "open-frame"];
const EXPECTED_ANCHORS = [
  { id: "representative-interior-concept", scene: "living" },
  { id: "facility-arrival-concept", scene: "arrival" },
  { id: "facility-landscaped-open-space-concept", scene: "open-frame" }
];
const EXPECTED_ASSETS = new Map([
  ["model-hd.glb", { bytes: 2420492, sha256: "71fcca8a0f58743b5f2257684c79957fbbff8e0169f5438bdc78231f27968a53", mime: "model/gltf-binary" }],
  ["model-lod.glb", { bytes: 32244, sha256: "485161974b6d343956d249d821c893b72a59678e8e8ee2810c90cee5f23079ce", mime: "model/gltf-binary" }],
  ["poster.webp", { bytes: 23996, sha256: "5588d09e28f95ac5d6655626027c3ad41f17c5c5c78153ecb2ba138821aa8c85", mime: "image/webp" }],
  ["experience/representative-apartment-living-v1.webp", { bytes: 103748, sha256: "1ad84512b5cb938450b5124c199ba09d00697da605ef46214434cef80649319b", mime: "image/webp" }],
  ["experience/representative-apartment-bedroom-v1.webp", { bytes: 79384, sha256: "1c4d71c6b1308867a2a9c9d1d03eec947ba6f85b9800fa1f88ae5028acf06aea", mime: "image/webp" }],
  ["experience/facility-arrival-gallery-v1.webp", { bytes: 170750, sha256: "cc50acc2570612165bf20442849ac9fcdf00658c0835f2130d6824d8b2c50e9a", mime: "image/webp" }],
  ["experience/facility-landscaped-terrace-v1.webp", { bytes: 264926, sha256: "717a33f6deb118e3d60539152147a7d1c791e84b69e77861f6086ae246cc8e0b", mime: "image/webp" }]
]);
const VIEWPORTS = [
  { name: "320x568", width: 320, height: 568, touch: true },
  { name: "390x844", width: 390, height: 844, touch: true },
  { name: "568x320", width: 568, height: 320, touch: true },
  { name: "1280x800", width: 1280, height: 800, touch: false }
];
const ACCESSIBILITY_VIEWPORTS = VIEWPORTS.filter(({ name }) => ["390x844", "568x320"].includes(name));
const REPORT_SCHEMA = "nadlan-einstein-flagship-live-acceptance/v2";
const EXPECTED_EVIDENCE_COUNTS = Object.freeze({
  keyboardViewports: ACCESSIBILITY_VIEWPORTS.length,
  keyboardToolChecks: ACCESSIBILITY_VIEWPORTS.length * EXPECTED_TOOLS.length,
  keyboardEscapeRestores: ACCESSIBILITY_VIEWPORTS.length * EXPECTED_TOOLS.length,
  browserHistoryTransitions: 2,
  textResizeViewports: ACCESSIBILITY_VIEWPORTS.length,
  textResizeDialogChecks: ACCESSIBILITY_VIEWPORTS.length * EXPECTED_TOOLS.length
});
const SENSITIVE_QUERY_KEY = /^(?:post_password|password|pass|token|access_token|api_key|key|nonce|email|phone|name|address)$/i;

function sha256(bytes) { return createHash("sha256").update(bytes).digest("hex"); }
function redact(value, secret = POST_PASSWORD) {
  let text = String(value == null ? "" : value);
  if (secret) {
    text = text.split(secret).join("[REDACTED]");
    text = text.split(encodeURIComponent(secret)).join("[REDACTED]");
  }
  return text.replace(/([?&](?:post_password|password|token|access_token|api_key|key|nonce)=)[^&\s]+/gi, "$1[REDACTED]");
}
function publicUrl(value) {
  const url = new URL(value);
  url.username = ""; url.password = ""; url.search = ""; url.hash = "";
  return url.href;
}
function safeError(error) { return redact(error && error.message ? error.message : error); }
function cacheIsPrivate(headers) {
  const value = String(headers["cache-control"] || "").toLowerCase();
  return value.includes("no-store") || value.includes("no-cache") || value.includes("max-age=0");
}
function privateAssetAnonymousContract(status, headers, bodyBytes) {
  return status === 404 && bodyBytes === 0 && cacheIsPrivate(headers) &&
    String(headers["x-robots-tag"] || "").toLowerCase().includes("noindex");
}
function findHealthVersion(payload) {
  if (Array.isArray(payload)) {
    for (const item of payload) { const found = findHealthVersion(item); if (found) return found; }
    return "";
  }
  if (!payload || typeof payload !== "object") return "";
  for (const [key, value] of Object.entries(payload)) {
    if (["version", "plugin_version", "nadlan_config_version"].includes(String(key).toLowerCase()) && ["string", "number"].includes(typeof value)) return String(value);
  }
  for (const value of Object.values(payload)) { const found = findHealthVersion(value); if (found) return found; }
  return "";
}
function parseGlbTriangles(buffer) {
  if (buffer.length < 20 || buffer.readUInt32LE(0) !== 0x46546c67) throw new Error("Not a GLB");
  let offset = 12, json = null;
  while (offset + 8 <= buffer.length) {
    const length = buffer.readUInt32LE(offset), type = buffer.readUInt32LE(offset + 4);
    if (type === 0x4e4f534a) json = JSON.parse(buffer.subarray(offset + 8, offset + 8 + length).toString("utf8").replace(/\0+$/, ""));
    offset += 8 + length;
  }
  if (!json) throw new Error("GLB JSON missing");
  return (json.meshes || []).flatMap((mesh) => mesh.primitives || []).reduce((sum, primitive) => {
    if (primitive.mode != null && primitive.mode !== 4) return sum;
    const accessor = primitive.indices == null ? json.accessors?.[primitive.attributes?.POSITION] : json.accessors?.[primitive.indices];
    return sum + Math.floor(Number(accessor?.count || 0) / 3);
  }, 0);
}

if (process.argv.includes("--self-test")) {
  assert.equal(redact("?password=swordfish", "swordfish"), "?password=[REDACTED]");
  assert.equal(publicUrl("https://example.test/private/?token=secret#x"), "https://example.test/private/");
  assert.equal(cacheIsPrivate({ "cache-control": "private, no-store" }), true);
  assert.equal(privateAssetAnonymousContract(404, { "cache-control": "private, no-store", "x-robots-tag": "noindex, nofollow" }, 0), true);
  assert.equal(privateAssetAnonymousContract(404, { "cache-control": "private, no-store", "x-robots-tag": "noindex, nofollow" }, 1), false);
  assert.equal(findHealthVersion({ data: { nadlan_config_version: "1.72.205" } }), "1.72.205");
  assert.deepEqual(EXPECTED_TOOLS, ["view", "interior", "design", "comments"]);
  assert.equal(REPORT_SCHEMA, "nadlan-einstein-flagship-live-acceptance/v2");
  assert.deepEqual(EXPECTED_EVIDENCE_COUNTS, { keyboardViewports: 2, keyboardToolChecks: 8, keyboardEscapeRestores: 8, browserHistoryTransitions: 2, textResizeViewports: 2, textResizeDialogChecks: 8 });
  console.log("PASS qa-einstein-flagship-live self-test");
  process.exit(0);
}

if (!TARGET_RAW || !POST_PASSWORD) {
  const missing = [!TARGET_RAW && "SANDBOX_URL", !POST_PASSWORD && "SANDBOX_POST_PASSWORD"].filter(Boolean);
  console.error(`Missing required environment variable(s): ${missing.join(", ")}`);
  process.exit(2);
}
const EXPECTED_STAGE_POST_ID = EXPECTED_STAGE_POST_ID_RAW ? Number(EXPECTED_STAGE_POST_ID_RAW) : null;
if ((EXPECTED_STAGE_POST_ID_RAW && (!Number.isSafeInteger(EXPECTED_STAGE_POST_ID) || EXPECTED_STAGE_POST_ID <= 0)) ||
    (EXPECTED_PLUGIN_VERSION && !/^\d+\.\d+\.\d+$/.test(EXPECTED_PLUGIN_VERSION)) ||
    (EXPECTED_PROJECT_CONTRACT_ID && EXPECTED_PROJECT_CONTRACT_ID !== CONTRACT_ID)) {
  console.error("EXPECTED_STAGE_POST_ID, EXPECTED_PLUGIN_VERSION or EXPECTED_PROJECT_CONTRACT_ID is invalid.");
  process.exit(2);
}

let target;
try {
  target = new URL(TARGET_RAW);
  if (!/^https?:$/.test(target.protocol) || target.username || target.password) throw new Error("invalid URL");
} catch {
  console.error("SANDBOX_URL must be an absolute HTTP(S) URL without userinfo.");
  process.exit(2);
}
target.search = ""; target.hash = "";
const TARGET_URL = target.href;
const SLUG = target.pathname.split("/").filter(Boolean).pop() || "";

const report = {
  schema: REPORT_SCHEMA,
  runner: "scripts/qa-einstein-flagship-live.mjs",
  target: { url: publicUrl(TARGET_URL), passwordProvided: true, projectContractId: CONTRACT_ID },
  startedAt: new Date().toISOString(), finishedAt: null,
  environment: { browser: "Google Chrome (Playwright control)", viewports: VIEWPORTS.map(({ name, width, height }) => ({ name, width, height })) },
  anonymous: null, discovery: null, health: null, unlocked: null, assets: [], matrix: [], browserBack: null, browserHistory: null,
  keyboard: { viewports: [], passed: false }, textResize200: { viewports: [], passed: false }, evidenceCounts: null,
  runtime: { pageErrors: [], consoleErrors: [], externalRequests: [], sensitiveQueryRequests: [], mutationRequestsAfterUnlock: [] },
  failures: [], warnings: [], screenshots: [], totals: null
};
function sanitized(value) {
  return JSON.parse(JSON.stringify(value == null ? {} : value, (_key, item) => typeof item === "string" ? redact(item) : item));
}
function fail(code, message, context = {}) { report.failures.push({ code, message: redact(message), context: sanitized(context) }); }
function warn(code, message, context = {}) { report.warnings.push({ code, message: redact(message), context: sanitized(context) }); }
async function settle(page, ms = 160) { await page.waitForTimeout(ms); await page.evaluate(() => new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)))).catch(() => {}); }
function screenshotName(name) { return path.join(SCREENSHOT_DIR, `${name}.png`); }
async function shot(page, name) { await page.screenshot({ path: screenshotName(name), fullPage: false }); report.screenshots.push(`screenshots/${name}.png`); }

function installNetworkAudit(page, phase) {
  const state = { requests: [], responseAssets: [] };
  page.on("request", (request) => {
    let url; try { url = new URL(request.url()); } catch { return; }
    const queryKeys = [...url.searchParams.keys()];
    const item = { phase, method: request.method(), origin: url.origin, pathname: url.pathname, queryKeys };
    state.requests.push(item);
    if (!/^(?:about:|data:|blob:)$/.test(url.protocol) && url.origin !== target.origin) report.runtime.externalRequests.push(item);
    if (queryKeys.some((key) => SENSITIVE_QUERY_KEY.test(key))) report.runtime.sensitiveQueryRequests.push(item);
    if (phase === "authorized" && !["GET", "HEAD", "OPTIONS"].includes(request.method()) && !/wp-login\.php$/.test(url.pathname)) report.runtime.mutationRequestsAfterUnlock.push(item);
  });
  page.on("response", (response) => {
    const url = new URL(response.url());
    if (url.origin !== target.origin || !url.pathname.startsWith(ASSET_PREFIX)) return;
    const relativeName = decodeURIComponent(url.pathname.slice(ASSET_PREFIX.length));
    if (!EXPECTED_ASSETS.has(relativeName)) return;
    state.responseAssets.push(response.body().then((bytes) => ({ relativeName, status: response.status(), headers: response.headers(), bytes })));
  });
  page.on("pageerror", (error) => report.runtime.pageErrors.push({ phase, message: safeError(error) }));
  page.on("console", (entry) => { if (entry.type() === "error") report.runtime.consoleErrors.push({ phase, message: redact(entry.text()) }); });
  return state;
}

async function inspectLockedPage(page, response, network) {
  const headers = response ? await response.allHeaders() : {};
  const dom = await page.evaluate(() => {
    const visible = (node) => { if (!node) return false; const s=getComputedStyle(node),r=node.getBoundingClientRect(); return s.display!=="none"&&s.visibility!=="hidden"&&r.width>0&&r.height>0; };
    return {
      formCount: document.querySelectorAll(".post-password-form,form[action*='wp-login.php?action=postpass']").length,
      flagshipCount: document.querySelectorAll('[data-nl-flagship="v3"],.nlfs,[data-nlfs-config]').length,
      payloadMarker: document.documentElement.innerHTML.includes("nadlan-flagship-runtime/v3"),
      robots: [...document.querySelectorAll('meta[name="robots"]')].map((node) => String(node.content || "").toLowerCase()),
      canonicalCount: document.querySelectorAll('link[rel="canonical"],link[rel="shortlink"]').length,
      discoveryCount: document.querySelectorAll('link[type="application/json+oembed"],link[type="text/xml+oembed"],link[rel="alternate"][type*="rss"]').length,
      h1Count: [...document.querySelectorAll("h1")].filter(visible).length
    };
  });
  const privateAssetRequests = network.requests.filter((item) => item.pathname.startsWith(ASSET_PREFIX));
  const flagshipStaticRequests = network.requests.filter((item) => item.pathname.includes("/wp-content/plugins/nadlan-config/assets/flagship-v3/"));
  report.anonymous = {
    status: response?.status() ?? null, passwordFormCount: dom.formCount, flagshipNodes: dom.flagshipCount,
    payloadPresent: dom.payloadMarker, privateAssetRequests: privateAssetRequests.length, flagshipStaticRequests: flagshipStaticRequests.length,
    robotsMetaNoindex: dom.robots.some((value) => value.includes("noindex")),
    xRobotsNoindex: String(headers["x-robots-tag"] || "").toLowerCase().includes("noindex"),
    privateCache: cacheIsPrivate(headers), referrerPolicy: String(headers["referrer-policy"] || "").toLowerCase(),
    canonicalOrShortlinkCount: dom.canonicalCount, discoveryLinkCount: dom.discoveryCount, passed: false
  };
  if (!response || response.status() !== 200) fail("anonymous.http", "Locked stage did not return HTTP 200.", { status: response?.status() ?? null });
  if (dom.formCount !== 1) fail("anonymous.password-form", "Locked stage must contain exactly one password form.", { count: dom.formCount });
  if (dom.flagshipCount || dom.payloadMarker || privateAssetRequests.length || flagshipStaticRequests.length) fail("anonymous.payload-leak", "Flagship DOM, payload or assets leaked before unlock.", { flagshipNodes: dom.flagshipCount, privateAssetRequests: privateAssetRequests.length, flagshipStaticRequests: flagshipStaticRequests.length });
  if (!report.anonymous.robotsMetaNoindex || !report.anonymous.xRobotsNoindex) fail("anonymous.noindex", "Locked response is missing noindex in HTML or headers.");
  if (!report.anonymous.privateCache) fail("anonymous.cache", "Locked response is not private/no-store.");
  if (report.anonymous.referrerPolicy !== "no-referrer") fail("anonymous.referrer", "Locked response must use Referrer-Policy: no-referrer.");
  if (dom.canonicalCount || dom.discoveryCount) fail("anonymous.discovery-links", "Canonical, shortlink, oEmbed or feed discovery links leaked.", { canonicalOrShortlinkCount: dom.canonicalCount, discoveryLinkCount: dom.discoveryCount });
  report.anonymous.passed = !report.failures.some((item) => item.code.startsWith("anonymous."));
}

async function unlock(page) {
  const form = page.locator(".post-password-form,form[action*='wp-login.php?action=postpass']").first();
  await form.locator("input[name='post_password']").fill(POST_PASSWORD);
  await Promise.all([
    page.waitForNavigation({ waitUntil: "domcontentloaded", timeout: 45_000 }).catch(() => null),
    form.locator("input[type='submit'],button[type='submit']").first().click()
  ]);
  await page.locator(`.nlfs[data-nl-flagship="v3"][data-project-contract-id="${CONTRACT_ID}"]`).waitFor({ state: "visible", timeout: 45_000 });
  await page.waitForFunction(() => document.querySelector('.nlfs[data-nl-flagship="v3"]')?.dataset.modelState === "ready", null, { timeout: 45_000 });
  await settle(page, 300);
}

async function unlockedIdentity(page, response) {
  const headers = response ? await response.allHeaders() : {};
  const data = await page.evaluate(() => {
    const root=document.querySelector('.nlfs[data-nl-flagship="v3"]');
    const raw=root?.querySelector("[data-nlfs-config]")?.textContent || "";
    let config=null; try { config=JSON.parse(raw); } catch {}
    const postClass=[...document.body.classList].find((name)=>/^postid-\d+$/.test(name));
    const visible=(node)=>{if(!node)return false;const s=getComputedStyle(node),r=node.getBoundingClientRect();return s.display!=="none"&&s.visibility!=="hidden"&&r.width>0&&r.height>0;};
    return {
      postId: Number((postClass || "").replace("postid-", "")) || 0,
      contractId: root?.dataset.projectContractId || "", configSchema: config?.schema || "",
      configContractId: config?.identity?.project_contract_id || "", mode: config?.mode || "",
      modelUrl: config?.model?.hd?.url || "", modelHash: config?.model?.hd?.sha256 || "", modelBytes: Number(config?.model?.hd?.bytes || 0),
      h1: [...document.querySelectorAll("h1")].filter(visible).map((node)=>node.textContent.trim()),
      robots: [...document.querySelectorAll('meta[name="robots"]')].map((node)=>String(node.content||"").toLowerCase()),
      canonicalCount: document.querySelectorAll('link[rel="canonical"],link[rel="shortlink"]').length,
      discoveryCount: document.querySelectorAll('link[type="application/json+oembed"],link[type="text/xml+oembed"]').length,
      writeCaps: config?.capabilities || null
    };
  });
  report.unlocked = {
    status: response?.status() ?? null, postIdResolved: data.postId > 0, contractId: data.contractId,
    expectedStagePostIdProvided: EXPECTED_STAGE_POST_ID !== null,
    stagePostIdMatched: EXPECTED_STAGE_POST_ID === null ? null : data.postId === EXPECTED_STAGE_POST_ID,
    configSchema: data.configSchema, mode: data.mode, h1Count: data.h1.length, h1: data.h1[0] || "",
    modelUrlQueryFree: false, privateCache: cacheIsPrivate(headers), xRobotsNoindex: String(headers["x-robots-tag"] || "").toLowerCase().includes("noindex"),
    robotsMetaNoindex: data.robots.some((value)=>value.includes("noindex")), canonicalOrShortlinkCount: data.canonicalCount, discoveryLinkCount: data.discoveryCount,
    writesDisabled: data.writeCaps?.writes_enabled === false && data.writeCaps?.lead_submission === false && data.writeCaps?.comment_submission === false,
    passed: false
  };
  let modelUrl=null; try { modelUrl=new URL(data.modelUrl, target.origin); } catch {}
  report.unlocked.modelUrlQueryFree = Boolean(modelUrl && modelUrl.origin===target.origin && modelUrl.pathname===ASSET_PREFIX+"model-hd.glb" && !modelUrl.search && !modelUrl.hash);
  if (data.contractId!==CONTRACT_ID || data.configContractId!==CONTRACT_ID || data.configSchema!=="nadlan-flagship-runtime/v3" || data.mode!=="private_sandbox") fail("unlocked.identity", "Unlocked runtime identity/mode mismatch.", { contractId: data.contractId, configContractId: data.configContractId, schema: data.configSchema, mode: data.mode });
  if (!data.postId) fail("unlocked.post-id", "Could not resolve the exact WordPress post ID from the unlocked page.");
  if (EXPECTED_STAGE_POST_ID !== null && data.postId !== EXPECTED_STAGE_POST_ID) fail("unlocked.post-id-mismatch", "Unlocked page is not the exact expected stage post ID.", { stagePostIdMatched: false });
  if (data.h1.length!==1) fail("unlocked.h1", "Unlocked stage must contain exactly one visible H1.", { count: data.h1.length });
  if (!report.unlocked.modelUrlQueryFree || data.modelHash!==EXPECTED_ASSETS.get("model-hd.glb").sha256 || data.modelBytes!==EXPECTED_ASSETS.get("model-hd.glb").bytes) fail("unlocked.model-contract", "HD model URL/hash/bytes do not match the frozen protected route.");
  if (!report.unlocked.privateCache || !report.unlocked.xRobotsNoindex || !report.unlocked.robotsMetaNoindex) fail("unlocked.privacy", "Unlocked response lost noindex/private-cache protection.");
  if (data.canonicalCount || data.discoveryCount) fail("unlocked.discovery-links", "Unlocked private stage emitted canonical/shortlink/oEmbed discovery.");
  if (!report.unlocked.writesDisabled) fail("unlocked.write-caps", "Unlocked demonstration does not fail closed on writes.");
  report.unlocked.passed = !report.failures.some((item)=>item.code.startsWith("unlocked."));
  return data;
}

async function auditHealth(context) {
  if (!EXPECTED_PLUGIN_VERSION) {
    report.health = { expectedVersionProvided: false, passed: true };
    return;
  }
  let response = null, payload = null, error = null;
  try {
    response = await context.request.get(new URL("/wp-json/nadlan/v1/healthcheck", target.origin).href, { timeout: 30_000, maxRedirects: 0 });
    payload = await response.json();
  } catch (caught) { error = safeError(caught); }
  const observedVersion = findHealthVersion(payload);
  const passed = !error && response?.status() === 200 && observedVersion === EXPECTED_PLUGIN_VERSION;
  report.health = { expectedVersionProvided: true, httpStatus: response?.status() ?? null, versionMatched: observedVersion === EXPECTED_PLUGIN_VERSION, passed };
  if (!passed) fail("health.plugin-version", "Live healthcheck did not report the exact expected plugin version.", { httpStatus: response?.status() ?? null, versionMatched: observedVersion === EXPECTED_PLUGIN_VERSION, error });
}

async function anonymousProbe(context, postId) {
  const exactPath=target.pathname.replace(/\/$/, "");
  const probes=[
    { label:"rest-id", path:`/wp-json/wp/v2/nadlan_project/${postId}`, statuses:[404] },
    { label:"rest-slug", path:`/wp-json/wp/v2/nadlan_project?slug=${encodeURIComponent(SLUG)}`, statuses:[200], emptyArray:true },
    { label:"oembed", path:`/wp-json/oembed/1.0/embed?url=${encodeURIComponent(TARGET_URL)}`, statuses:[404] },
    { label:"embed", path:`${exactPath}/embed/`, statuses:[404] },
    { label:"feed", path:`${exactPath}/feed/`, statuses:[404] },
    { label:"private-asset", path:`${ASSET_PREFIX}model-hd.glb`, statuses:[404], privateHeaders:true }
  ];
  const results=[];
  for (const probe of probes) {
    let response=null, body="", bodyBytes=0, error=null;
    try { response=await context.request.get(new URL(probe.path,target.origin).href,{timeout:30000,maxRedirects:0}); const bytes=await response.body(); bodyBytes=bytes.length; body=bytes.toString("utf8"); } catch(caught){error=safeError(caught);}
    const status=response?.status()??null, headers=response?response.headers():{};
    let emptyArray=false; try { const json=JSON.parse(body); emptyArray=Array.isArray(json)&&json.length===0; } catch {}
    const bodyLower=body.toLowerCase();
    const identityExposed=!probe.privateHeaders&&Boolean((SLUG&&bodyLower.includes(SLUG.toLowerCase())) || bodyLower.includes(CONTRACT_ID));
    const privateContractPassed=!probe.privateHeaders||privateAssetAnonymousContract(status,headers,bodyBytes);
    const passed=!error&&probe.statuses.includes(status)&&!identityExposed&&(!probe.emptyArray||emptyArray)&&privateContractPassed;
    results.push({label:probe.label,status,identityExposed:probe.privateHeaders?undefined:identityExposed,emptyArray:probe.emptyArray?emptyArray:undefined,privateCache:probe.privateHeaders?cacheIsPrivate(headers):undefined,xRobotsNoindex:probe.privateHeaders?String(headers["x-robots-tag"]||"").toLowerCase().includes("noindex"):undefined,bodyBytes:probe.privateHeaders?bodyBytes:undefined,passed});
    if(!passed) {
      const context=probe.privateHeaders?{status,privateCache:cacheIsPrivate(headers),xRobotsNoindex:String(headers["x-robots-tag"]||"").toLowerCase().includes("noindex"),bodyBytes,error}:{status,identityExposed,emptyArray,error};
      fail(`discovery.${probe.label}`,`Anonymous ${probe.label} probe violated non-enumerability.`,context);
    }
  }
  report.discovery={checks:results,passed:results.every((item)=>item.passed)};
}

async function verifyAssetResponses(assetPromises) {
  const settled=await Promise.all(assetPromises);
  const byName=new Map(); settled.forEach((item)=>{if(!byName.has(item.relativeName))byName.set(item.relativeName,item);});
  for(const [name,expected] of EXPECTED_ASSETS){
    const item=byName.get(name);
    if(!item) continue;
    const observed={name,status:item.status,bytes:item.bytes.length,sha256:sha256(item.bytes),contentType:String(item.headers["content-type"]||"").split(";")[0].toLowerCase(),privateCache:cacheIsPrivate(item.headers),queryFree:true};
    if (!report.assets.some((asset) => asset.name === name)) report.assets.push(observed);
    if(observed.status!==200||observed.bytes!==expected.bytes||observed.sha256!==expected.sha256||observed.contentType!==expected.mime||!observed.privateCache) fail("asset.integrity",`Protected asset failed exact integrity/response contract: ${name}`,observed);
    if(name==="model-hd.glb"){
      const triangles=parseGlbTriangles(item.bytes); observed.triangles=triangles;
      if(triangles!==39912) fail("asset.triangles","HD model triangle count changed.",{triangles});
    }
  }
}

async function auditAllProtectedAssets(context) {
  for (const [name, expected] of EXPECTED_ASSETS) {
    let response = null, bytes = null, error = null;
    try {
      response = await context.request.get(new URL(ASSET_PREFIX + name, target.origin).href, { timeout: 45_000, maxRedirects: 0 });
      bytes = await response.body();
    } catch (caught) { error = safeError(caught); }
    const headers = response ? response.headers() : {};
    const observed = {
      name,
      status: response?.status() ?? null,
      bytes: bytes?.length ?? 0,
      sha256: bytes ? sha256(bytes) : "",
      contentType: String(headers["content-type"] || "").split(";")[0].toLowerCase(),
      privateCache: cacheIsPrivate(headers),
      queryFree: true
    };
    if (bytes && name === "model-hd.glb") observed.triangles = parseGlbTriangles(bytes);
    const passed = !error && observed.status === 200 && observed.bytes === expected.bytes && observed.sha256 === expected.sha256 &&
      observed.contentType === expected.mime && observed.privateCache && (name !== "model-hd.glb" || observed.triangles === 39912);
    const prior = report.assets.findIndex((asset) => asset.name === name);
    if (prior >= 0) report.assets[prior] = observed;
    else report.assets.push(observed);
    if (!passed) fail("asset.integrity", `Protected asset failed exact authorized integrity/response contract: ${name}`, { ...observed, error });
  }
}

async function ensureToolVisible(page, toolId) {
  const tile=page.locator(`.nlvt-teaser[data-nlvt-tool="${toolId}"]`);
  for(let guard=0;guard<5&&!await tile.isVisible();guard+=1){await page.locator('[data-nlvt-page="next"]').click();await settle(page,50);}
  if(!await tile.isVisible()) throw new Error(`Tool tile not visible: ${toolId}`);
  return tile;
}

async function ensureToolVisibleKeyboard(page, toolId) {
  const tile=page.locator(`.nlvt-teaser[data-nlvt-tool="${toolId}"]`);
  for(let guard=0;guard<5&&!await tile.isVisible();guard+=1){const next=page.locator('[data-nlvt-page="next"]');await next.focus();await page.keyboard.press("Enter");await settle(page,50);}
  if(!await tile.isVisible()) throw new Error(`Keyboard could not reveal tool tile: ${toolId}`);
  return tile;
}

async function exactStageState(page) {
  const canvas=sha256(await page.locator("canvas[data-nlfs-model]").screenshot());
  const state=await page.evaluate(()=>{const root=document.querySelector('.nlfs[data-nl-flagship="v3"]'),active=document.activeElement,dialog=document.querySelector("body>dialog.nlvt-dialog");const focusToken=active?.dataset.nlvtOpen?`open:${active.dataset.nlvtOpen}`:active?.dataset.nlvtAction?`action:${active.dataset.nlvtAction}`:active?.dataset.nlvtExperienceScene?`scene:${active.dataset.nlvtExperienceScene}`:active?.tagName||"";return{scrollX,scrollY,focusToken,rootInert:Boolean(root?.inert),rootAria:root?.getAttribute("aria-hidden")??null,modelState:root?.dataset.modelState||"",dialogTool:dialog?.dataset.nlvtTool||"",dialogScene:dialog?.querySelector('[data-nlvt-experience-visual="interior"]')?.dataset.nlvtExperienceScene||"",bodyLocked:document.body.classList.contains("nlvt-tool-open"),htmlOverflow:getComputedStyle(document.documentElement).overflow,bodyOverflow:getComputedStyle(document.body).overflow,urlState:location.pathname+location.search+location.hash};});
  return {...state,canvas};
}

async function applyTextResize200(page, scopeSelector) {
  return page.evaluate((selector)=>{const scope=document.querySelector(selector);if(!scope)return{scaledTextCount:0,minimumScale:0};const visible=(node)=>{const style=getComputedStyle(node),rect=node.getBoundingClientRect();return style.display!=="none"&&style.visibility!=="hidden"&&style.opacity!=="0"&&rect.width>0&&rect.height>0&&!node.closest('[hidden],[aria-hidden="true"],.nlvt-visually-hidden,.nlfs-visually-hidden');};const nodes=[scope,...scope.querySelectorAll("*")].filter((node)=>visible(node)&&!node.dataset.nlqaTextResize200&&([...node.childNodes].some((child)=>child.nodeType===Node.TEXT_NODE&&child.textContent.trim())||node.matches("input,select,textarea")));const sizes=nodes.map((node)=>({node,size:parseFloat(getComputedStyle(node).fontSize)})).filter(({size})=>Number.isFinite(size)&&size>0);for(const {node,size} of sizes){node.dataset.nlqaTextResize200=String(size);node.style.setProperty("font-size",`${size*2}px`,"important");}const ratios=sizes.map(({node,size})=>parseFloat(getComputedStyle(node).fontSize)/size);return{scaledTextCount:sizes.length,minimumScale:ratios.length?Math.min(...ratios):0};},scopeSelector);
}

async function textResizeLayoutSnapshot(page, scopeSelector) {
  return page.evaluate((selector)=>{const scope=document.querySelector(selector);if(!scope)return{missing:true};const box=(node)=>{const rect=node.getBoundingClientRect();return{left:rect.left,right:rect.right,top:rect.top,bottom:rect.bottom,width:rect.width,height:rect.height};};const visible=(node)=>{const style=getComputedStyle(node),rect=node.getBoundingClientRect();return style.display!=="none"&&style.visibility!=="hidden"&&style.opacity!=="0"&&rect.width>0&&rect.height>0&&!node.closest('[hidden],[aria-hidden="true"],.nlvt-visually-hidden,.nlfs-visually-hidden');};const nodes=[scope,...scope.querySelectorAll("*")].filter(visible);const targets=nodes.filter((node)=>node.matches('button,a[href],input,select,textarea,[role="button"]')).map(box);const innerScrollers=nodes.filter((node)=>{const style=getComputedStyle(node);return((/auto|scroll/.test(style.overflowX)&&node.scrollWidth>node.clientWidth+1)||(/auto|scroll/.test(style.overflowY)&&node.scrollHeight>node.clientHeight+1));});const semantics=nodes.filter((node)=>node.matches('button,a[href],input,select,textarea,h1,h2,h3,p,li,strong,small,span,[role="button"]')&&([...node.childNodes].some((child)=>child.nodeType===Node.TEXT_NODE&&child.textContent.trim())||node.matches("input,select,textarea")));const semanticClip=semantics.filter((node)=>{const rect=node.getBoundingClientRect(),style=getComputedStyle(node),selfClips=/hidden|clip/.test(style.overflowX+style.overflowY)&&(node.scrollWidth>node.clientWidth+1||node.scrollHeight>node.clientHeight+1);let parent=node.parentElement,ancestorClips=false;while(parent&&scope.contains(parent)){const parentStyle=getComputedStyle(parent),parentRect=parent.getBoundingClientRect();if((/hidden|clip/.test(parentStyle.overflowX)&&(rect.left<parentRect.left-.75||rect.right>parentRect.right+.75))||(/hidden|clip/.test(parentStyle.overflowY)&&(rect.top<parentRect.top-.75||rect.bottom>parentRect.bottom+.75))){ancestorClips=true;break;}parent=parent.parentElement;}return selfClips||ancestorClips;});const horizontalClip=semantics.filter((node)=>{const rect=node.getBoundingClientRect();return rect.left<-.75||rect.right>innerWidth+.75;});const candidates=semantics.filter((node)=>!semantics.some((other)=>other!==node&&node.contains(other)));let overlapCount=0;for(let i=0;i<candidates.length;i+=1)for(let j=i+1;j<candidates.length;j+=1){const a=candidates[i],b=candidates[j];if(a.contains(b)||b.contains(a))continue;const ar=a.getBoundingClientRect(),br=b.getBoundingClientRect(),w=Math.min(ar.right,br.right)-Math.max(ar.left,br.left),h=Math.min(ar.bottom,br.bottom)-Math.max(ar.top,br.top);if(w>2&&h>2)overlapCount+=1;}const stage=document.querySelector("[data-nlfs-protected-stage]"),play=document.querySelector("[data-nlfs-playground]"),stageBox=stage?box(stage):null,playBox=play?box(play):null;return{missing:false,scaledTextCount:nodes.filter((node)=>node.dataset.nlqaTextResize200).length,documentOverflowX:document.documentElement.scrollWidth-document.documentElement.clientWidth,scopeOverflowX:scope.scrollWidth-scope.clientWidth,targetCount:targets.length,undersizedTargetCount:targets.filter((rect)=>rect.width<43.5||rect.height<43.5).length,innerScrollerCount:innerScrollers.length,semanticClipCount:semanticClip.length,horizontalClipCount:horizontalClip.length,overlapCount,modelOverlap:Boolean(stageBox&&playBox&&stageBox.left<playBox.right&&stageBox.right>playBox.left&&stageBox.top<playBox.bottom&&stageBox.bottom>playBox.top),modelReady:document.querySelector('.nlfs[data-nl-flagship="v3"]')?.dataset.modelState==="ready"};},scopeSelector);
}

async function geometrySnapshot(page) {
  return page.evaluate(() => {
    const root=document.querySelector('.nlfs[data-nl-flagship="v3"]'),stage=root.querySelector("[data-nlfs-protected-stage]"),play=root.querySelector("[data-nlfs-playground]");
    const box=(node)=>{const r=node.getBoundingClientRect();return{left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height};};
    const visible=(node)=>{const s=getComputedStyle(node),r=node.getBoundingClientRect();return s.display!=="none"&&s.visibility!=="hidden"&&r.width>0&&r.height>0&&!node.closest("[hidden]");};
    const targets=[...root.querySelectorAll('button,a[href],input,select,textarea,[role="button"]')].filter(visible).map((node)=>({tag:node.tagName,text:(node.getAttribute("aria-label")||node.textContent||"").trim().slice(0,60),...box(node)}));
    const smallText=[...root.querySelectorAll("*")].filter((node)=>visible(node)&&[...node.childNodes].some((child)=>child.nodeType===Node.TEXT_NODE&&child.textContent.trim())&&!node.closest(".nlvt-visually-hidden,.nlfs-visually-hidden")).map((node)=>({text:node.textContent.trim().slice(0,60),size:parseFloat(getComputedStyle(node).fontSize)})).filter((item)=>item.size<12);
    const innerScrollers=[...root.querySelectorAll("*")].filter((node)=>{const s=getComputedStyle(node);return ((/auto|scroll/.test(s.overflowX)&&node.scrollWidth>node.clientWidth+1)||(/auto|scroll/.test(s.overflowY)&&node.scrollHeight>node.clientHeight+1));}).map((node)=>node.className||node.tagName);
    const clipped=[...root.querySelectorAll('button,a[href],h1,h2,h3,p,strong,small')].filter(visible).filter((node)=>{const r=node.getBoundingClientRect();return r.left<-.75||r.right>innerWidth+.75;}).map((node)=>({text:(node.textContent||"").trim().slice(0,60),...box(node)}));
    const semanticClip=[...root.querySelectorAll('button,a[href],h1,h2,h3,p,strong,small,span')].filter(visible).filter((node)=>[...node.childNodes].some((child)=>child.nodeType===Node.TEXT_NODE&&child.textContent.trim())).filter((node)=>{const s=getComputedStyle(node),clips=/hidden|clip/.test(s.overflowX+s.overflowY);return clips&&(node.scrollWidth>node.clientWidth+1||node.scrollHeight>node.clientHeight+1);}).map((node)=>({text:node.textContent.trim().slice(0,60),clientWidth:node.clientWidth,scrollWidth:node.scrollWidth,clientHeight:node.clientHeight,scrollHeight:node.scrollHeight}));
    const s=box(stage),p=box(play),samples=[];
    for(const xp of [.2,.5,.8])for(const yp of [.2,.5,.8]){const x=s.left+s.width*xp,y=s.top+s.height*yp;if(x<0||x>innerWidth||y<0||y>innerHeight){samples.push({x:xp,y:yp,skipped:true,accepted:null,hit:"outside-current-viewport"});continue;}const node=document.elementFromPoint(x,y);samples.push({x:xp,y:yp,skipped:false,accepted:Boolean(node&&(node.matches("[data-nlfs-model]")||node.closest(".nlfs__model-hotspot"))) ,hit:node?.className||node?.tagName||""});}
    const demo=[...document.querySelectorAll("body *")].filter((node)=>visible(node)&&[...node.childNodes].some((child)=>child.nodeType===Node.TEXT_NODE&&/הדמיה/.test(child.textContent))).map((node)=>node.textContent.trim());
    return {dir:document.documentElement.dir||root.dir,lang:document.documentElement.lang||root.lang,root:box(root),stage:s,playground:p,stagePlayOverlap:s.left<p.right&&s.right>p.left&&s.top<p.bottom&&s.bottom>p.top,playAfterStage:p.top>=s.bottom-.5,docOverflowX:document.documentElement.scrollWidth-document.documentElement.clientWidth,targets,smallText,innerScrollers,clipped,semanticClip,samples,demo,h1:[...document.querySelectorAll("h1")].filter(visible).length,canvas:{count:root.querySelectorAll("canvas[data-nlfs-model]").length,width:root.querySelector("canvas[data-nlfs-model]")?.width||0,height:root.querySelector("canvas[data-nlfs-model]")?.height||0,state:root.dataset.modelState},tools:[...root.querySelectorAll(".nlvt-teaser")].map((node)=>node.dataset.nlvtTool),anchors:[...root.querySelectorAll(".nlfs__model-hotspot")].map((node)=>({id:node.dataset.nlfsSceneGroup,scene:node.dataset.nlfsScene,hidden:node.hidden}))};
  });
}

async function auditStageHitGrid(page) {
  const original = await page.evaluate(() => ({ x: scrollX, y: scrollY }));
  const results = [];
  for (const yRatio of [.15, .5, .85]) {
    await page.evaluate((ratio) => {
      const stage = document.querySelector("[data-nlfs-protected-stage]");
      const rect = stage.getBoundingClientRect();
      const absolutePoint = scrollY + rect.top + rect.height * ratio;
      const maximum = Math.max(0, document.documentElement.scrollHeight - innerHeight);
      scrollTo(0, Math.max(0, Math.min(maximum, absolutePoint - innerHeight / 2)));
    }, yRatio);
    await settle(page, 80);
    const row = await page.evaluate((ratio) => {
      const stage = document.querySelector("[data-nlfs-protected-stage]"), rect = stage.getBoundingClientRect();
      return [.2, .5, .8].map((xRatio) => {
        const x = rect.left + rect.width * xRatio, y = rect.top + rect.height * ratio;
        const node = x >= 0 && x <= innerWidth && y >= 0 && y <= innerHeight ? document.elementFromPoint(x, y) : null;
        return { xRatio, yRatio: ratio, inViewport: Boolean(node), accepted: Boolean(node && (node.matches("[data-nlfs-model]") || node.closest(".nlfs__model-hotspot"))), hit: node?.className || node?.tagName || "" };
      });
    }, yRatio);
    results.push(...row);
  }
  await page.evaluate((position) => scrollTo(position.x, position.y), original);
  await settle(page, 80);
  return results;
}

async function auditDialogGeometry(page, viewport, toolId) {
  const result=await page.evaluate(()=>{const d=document.querySelector("body>dialog.nlvt-dialog"),r=d.getBoundingClientRect();const visible=(n)=>{const s=getComputedStyle(n),b=n.getBoundingClientRect();return s.display!=="none"&&s.visibility!=="hidden"&&b.width>0&&b.height>0;};const box=(n)=>{const b=n.getBoundingClientRect();return{left:b.left,right:b.right,top:b.top,bottom:b.bottom,width:b.width,height:b.height};};const controls=[...d.querySelectorAll("button")].filter(visible).map((n)=>({text:(n.getAttribute("aria-label")||n.textContent||"").trim(),...box(n)}));const small=[...d.querySelectorAll("*")].filter((n)=>visible(n)&&[...n.childNodes].some((c)=>c.nodeType===Node.TEXT_NODE&&c.textContent.trim())&&!n.closest(".nlvt-visually-hidden")).map((n)=>({text:n.textContent.trim().slice(0,60),size:parseFloat(getComputedStyle(n).fontSize)})).filter((x)=>x.size<12);const scrollers=[...d.querySelectorAll("*")].filter((n)=>{const s=getComputedStyle(n);return((/auto|scroll/.test(s.overflowX)&&n.scrollWidth>n.clientWidth+1)||(/auto|scroll/.test(s.overflowY)&&n.scrollHeight>n.clientHeight+1));}).map((n)=>n.className||n.tagName);const header=[d.querySelector('[data-nlvt-action="back"]'),d.querySelector("h2"),d.querySelector(".nlvt-disclosure")].filter(Boolean).map(box);const overlap=(a,b)=>a.left<b.right-.5&&a.right>b.left+.5&&a.top<b.bottom-.5&&a.bottom>b.top+.5;return{rect:box(d),controls,small,scrollers,headerOverlap:header.some((a,i)=>header.slice(i+1).some((b)=>overlap(a,b))),disclosureCount:[...document.querySelectorAll(".nlvt-disclosure")].filter(visible).length,bodyClass:document.body.classList.contains("nlvt-tool-open"),htmlOverflow:getComputedStyle(document.documentElement).overflow,bodyOverflow:getComputedStyle(document.body).overflow};});
  if(Math.abs(result.rect.width-viewport.width)>1||Math.abs(result.rect.height-viewport.height)>1||Math.abs(result.rect.left)>1||Math.abs(result.rect.top)>1) fail("dialog.fullscreen",`${viewport.name}/${toolId}: dialog is not exact fullscreen.`,result.rect);
  if(result.controls.some((item)=>item.width<43.5||item.height<43.5)) fail("dialog.targets",`${viewport.name}/${toolId}: dialog has a target below 44px.`,{targets:result.controls.filter((item)=>item.width<43.5||item.height<43.5)});
  if(result.small.length) fail("dialog.text",`${viewport.name}/${toolId}: dialog has visible text below 12px.`,{smallText:result.small});
  if(result.scrollers.length) fail("dialog.inner-scroll",`${viewport.name}/${toolId}: dialog contains an inner scroller.`,{scrollers:result.scrollers});
  if(result.headerOverlap||result.disclosureCount!==1) fail("dialog.header",`${viewport.name}/${toolId}: Back/title/disclosure geometry is invalid.`,{headerOverlap:result.headerOverlap,disclosureCount:result.disclosureCount});
  if(!result.bodyClass||result.htmlOverflow!=="hidden"||result.bodyOverflow!=="hidden") fail("dialog.lock",`${viewport.name}/${toolId}: background lock is incomplete.`,result);
}

async function auditViewport(browser, cookies, viewport) {
  const context=await browser.newContext({viewport:{width:viewport.width,height:viewport.height},hasTouch:viewport.touch,locale:"he-IL",colorScheme:"light",reducedMotion:"reduce"});
  await context.addCookies(cookies);
  const page=await context.newPage(), network=installNetworkAudit(page,"authorized");
  const response=await page.goto(TARGET_URL,{waitUntil:"domcontentloaded",timeout:45000});
  await page.locator(`.nlfs[data-project-contract-id="${CONTRACT_ID}"]`).waitFor({state:"visible",timeout:45000});
  await page.waitForFunction(()=>document.querySelector('.nlfs[data-nl-flagship="v3"]')?.dataset.modelState==="ready",null,{timeout:45000});
  await settle(page,250);
  const base=await geometrySnapshot(page);
  const stageHitGrid=await auditStageHitGrid(page);
  const row={
    viewport:viewport.name,
    httpStatus:response?.status()??null,
    base:{
      dir:base.dir,lang:base.lang,canvas:base.canvas,tools:base.tools,anchorCount:base.anchors.length,
      documentOverflowX:base.docOverflowX,targetCount:base.targets.length,
      minimumTargetWidth:base.targets.length?Math.min(...base.targets.map((item)=>item.width)):null,
      minimumTargetHeight:base.targets.length?Math.min(...base.targets.map((item)=>item.height)):null,
      smallTextCount:base.smallText.length,innerScrollerCount:base.innerScrollers.length,
      clippedCount:base.clipped.length+base.semanticClip.length,demoDisclosureCount:base.demo.length,
      h1Count:base.h1,modelOverlap:base.stagePlayOverlap,modelHitPointsPassed:stageHitGrid.filter((item)=>item.accepted).length
    },
    tools:[],hotspots:[],passed:false
  };
  if(base.dir!=="rtl"||!String(base.lang).toLowerCase().startsWith("he")) fail("viewport.locale",`${viewport.name}: Hebrew RTL contract failed.`,{dir:base.dir,lang:base.lang});
  if(base.canvas.count!==1||base.canvas.width<1||base.canvas.height<1||base.canvas.state!=="ready") fail("viewport.canvas",`${viewport.name}: actual GLB canvas did not reach ready.`,base.canvas);
  if(JSON.stringify(base.tools)!==JSON.stringify(EXPECTED_TOOLS)) fail("viewport.tools",`${viewport.name}: permanent tool set/order changed.`,{tools:base.tools});
  if(base.anchors.length!==3||JSON.stringify(base.anchors.map((x)=>x.id))!==JSON.stringify(EXPECTED_ANCHORS.map((x)=>x.id))) fail("viewport.anchors",`${viewport.name}: exact three governed anchors changed.`,{anchors:base.anchors});
  if(base.stagePlayOverlap||!base.playAfterStage) fail("viewport.model-overlap",`${viewport.name}: visual tools overlap or precede the protected model.`,{stage:base.stage,playground:base.playground});
  if(base.docOverflowX>1||base.clipped.length||base.semanticClip.length||base.innerScrollers.length) fail("viewport.geometry",`${viewport.name}: overflow, clipping or nested scrolling detected.`,{docOverflowX:base.docOverflowX,clipped:base.clipped,semanticClip:base.semanticClip,innerScrollers:base.innerScrollers});
  if(base.targets.some((item)=>item.width<43.5||item.height<43.5)) fail("viewport.targets",`${viewport.name}: flagship target below 44px.`,{targets:base.targets.filter((item)=>item.width<43.5||item.height<43.5)});
  if(base.smallText.length) fail("viewport.text",`${viewport.name}: visible flagship text below 12px.`,{smallText:base.smallText});
  const testedSamples=base.samples.filter((item)=>!item.skipped);
  if(testedSamples.length<3||testedSamples.some((item)=>!item.accepted)) fail("viewport.stage-hit",`${viewport.name}: protected stage sample is obstructed.`,{samples:base.samples});
  if(stageHitGrid.length!==9||stageHitGrid.some((item)=>!item.inViewport||!item.accepted)) fail("viewport.stage-scroll-hit",`${viewport.name}: a scrolled region of the protected model is obstructed.`,{stageHitGrid});
  if(base.demo.length!==1||base.h1!==1) fail("viewport.landmarks",`${viewport.name}: expected one demo disclosure and one H1.`,{demoCount:base.demo.length,h1:base.h1});

  for(const anchor of EXPECTED_ANCHORS){
    const trigger=page.locator(`.nlfs__model-hotspot[data-nlfs-scene-group="${anchor.id}"]`);
    const visible=await trigger.isVisible();
    if(!visible){fail("hotspot.visible",`${viewport.name}/${anchor.id}: governed model anchor is not visible.`);row.hotspots.push({id:anchor.id,visible:false,passed:false});continue;}
    await trigger.focus(); const beforeScroll=await page.evaluate(()=>({x:scrollX,y:scrollY})); const beforeCanvas=sha256(await page.locator("canvas[data-nlfs-model]").screenshot());
    await trigger.click(); const dialog=page.locator('body>dialog.nlvt-dialog[data-nlvt-tool="interior"]'); await dialog.waitFor({state:"visible"});
    const actualScene=await dialog.locator('[data-nlvt-experience-visual="interior"]').getAttribute("data-nlvt-experience-scene");
    const actualAnchor=await dialog.getAttribute("data-mapping-hotspot-id");
    await dialog.locator('[data-nlvt-action="back"]').click(); await dialog.waitFor({state:"detached"}); await settle(page);
    const afterScroll=await page.evaluate(()=>({x:scrollX,y:scrollY,focus:document.activeElement?.dataset.nlfsSceneGroup||""})); const afterCanvas=sha256(await page.locator("canvas[data-nlfs-model]").screenshot());
    const passed=actualScene===anchor.scene&&actualAnchor===anchor.id&&beforeScroll.x===afterScroll.x&&beforeScroll.y===afterScroll.y&&afterScroll.focus===anchor.id&&beforeCanvas===afterCanvas;
    if(!passed) fail("hotspot.binding",`${viewport.name}/${anchor.id}: anchor did not open exact Interior scene or restore state.`,{expectedScene:anchor.scene,actualScene,actualAnchor,scrollRestored:beforeScroll.x===afterScroll.x&&beforeScroll.y===afterScroll.y,focus:afterScroll.focus,canvasRestored:beforeCanvas===afterCanvas});
    row.hotspots.push({id:anchor.id,scene:actualScene,passed});
  }

  for(const toolId of EXPECTED_TOOLS){
    await ensureToolVisible(page,toolId); const trigger=page.locator(`[data-nlvt-open="${toolId}"]`); await trigger.focus();
    const before={scroll:await page.evaluate(()=>({x:scrollX,y:scrollY,inert:document.querySelector('.nlfs').inert,aria:document.querySelector('.nlfs').getAttribute("aria-hidden")})),canvas:sha256(await page.locator("canvas[data-nlfs-model]").screenshot()),mutations:report.runtime.mutationRequestsAfterUnlock.length};
    await trigger.click(); const dialog=page.locator(`body>dialog.nlvt-dialog[data-nlvt-tool="${toolId}"]`); await dialog.waitFor({state:"visible"}); await auditDialogGeometry(page,viewport,toolId);
    let interactionPassed=true;
    if(toolId==="interior"){
      const scenes=await dialog.locator("button[data-nlvt-experience-scene]").evaluateAll((nodes)=>nodes.map((node)=>node.dataset.nlvtExperienceScene));
      if(JSON.stringify(scenes)!==JSON.stringify(EXPECTED_SCENES)){interactionPassed=false;fail("tool.interior-scenes",`${viewport.name}: Interior scene selector changed.`,{scenes});}
      for(const scene of EXPECTED_SCENES){
        await dialog.locator(`button[data-nlvt-experience-scene="${scene}"]`).click();
        const actual=await dialog.locator('[data-nlvt-experience-visual="interior"]').getAttribute("data-nlvt-experience-scene");
        if(actual!==scene){interactionPassed=false;fail("tool.interior-binding",`${viewport.name}: Interior failed to select ${scene}.`,{actual});}
        if(viewport.name==="390x844"&&scene==="living")await shot(page,"einstein-live-390x844-interior-living");
        if(viewport.name==="390x844"&&scene==="open-frame")await shot(page,"einstein-live-390x844-facility-open-frame");
      }
      const interior=dialog.locator("[data-nlvt-interior-state]");await interior.focus();await page.keyboard.press("ArrowUp");await page.keyboard.press("ArrowRight");await page.keyboard.press("Enter");await page.keyboard.press("l");
      const walk=await interior.evaluate((node)=>({state:node.dataset.nlvtInteriorState,turn:node.dataset.turn,door:node.dataset.doorOpen,light:node.dataset.lightOn}));
      if(walk.state!=="step-1"||walk.turn!=="1"||walk.door!=="true"||walk.light!=="true"){interactionPassed=false;fail("tool.interior-walk",`${viewport.name}: Interior walk controls failed.`,walk);}
    } else if(toolId==="design"){
      const sofa=dialog.locator("[data-nlvt-sofa]"),box=await sofa.boundingBox(); if(!box){interactionPassed=false;fail("tool.design",`${viewport.name}: design sofa missing.`);} else {await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.down();await page.mouse.move(box.x+box.width/2+20,box.y+box.height/2-10);await page.mouse.up();if(!await sofa.getAttribute("data-x")){interactionPassed=false;fail("tool.design",`${viewport.name}: design drag did not persist visually.`);}}
    } else if(toolId==="comments"){
      await dialog.locator('[data-nlvt-action="annotate"]').click();await dialog.locator('[data-nlvt-action="prepare"]').click();
      const comments=await dialog.evaluate((node)=>({state:node.dataset.commentState,status:node.querySelector("[data-nlvt-status]")?.textContent||""}));
      if(comments.state!=="prepared_no_write"||!/לא נשמר.*לא נשלח/.test(comments.status)){interactionPassed=false;fail("tool.comments",`${viewport.name}: comments are not explicit prepared-no-write state.`,comments);}
      if(viewport.name==="390x844") await shot(page,"einstein-live-390x844-comments-prepared");
    }
    await dialog.locator('[data-nlvt-action="back"]').click();await dialog.waitFor({state:"detached"});await settle(page);
    const after={scroll:await page.evaluate((id)=>({x:scrollX,y:scrollY,focus:document.activeElement?.dataset.nlvtOpen||"",inert:document.querySelector('.nlfs').inert,aria:document.querySelector('.nlfs').getAttribute("aria-hidden")}),toolId),canvas:sha256(await page.locator("canvas[data-nlfs-model]").screenshot()),mutations:report.runtime.mutationRequestsAfterUnlock.length};
    const restored=before.scroll.x===after.scroll.x&&before.scroll.y===after.scroll.y&&after.scroll.focus===toolId&&before.scroll.inert===after.scroll.inert&&before.scroll.aria===after.scroll.aria&&before.canvas===after.canvas&&before.mutations===after.mutations;
    if(!restored) fail("tool.restore",`${viewport.name}/${toolId}: Back did not restore exact focus/scroll/model/inert/write state.`,{scrollBefore:before.scroll,scrollAfter:after.scroll,focus:after.scroll.focus,canvasRestored:before.canvas===after.canvas,mutationsBefore:before.mutations,mutationsAfter:after.mutations});
    row.tools.push({id:toolId,interactionPassed,exactBackRestore:restored,passed:interactionPassed&&restored});
  }
  if(viewport.name==="390x844") await shot(page,"einstein-live-390x844");
  else await shot(page,`einstein-live-${viewport.name}`);
  row.passed=!report.failures.some((item)=>String(item.message).includes(viewport.name)); report.matrix.push(row);
  await verifyAssetResponses(network.responseAssets);
  await context.close();
}

async function auditKeyboardOnly(browser,cookies,viewport){
  const context=await browser.newContext({viewport:{width:viewport.width,height:viewport.height},hasTouch:false,locale:"he-IL",colorScheme:"light",reducedMotion:"reduce"});await context.addCookies(cookies);const page=await context.newPage(),network=installNetworkAudit(page,"authorized-keyboard");
  await page.goto(TARGET_URL,{waitUntil:"domcontentloaded",timeout:45000});await page.locator(`.nlfs[data-project-contract-id="${CONTRACT_ID}"]`).waitFor({state:"visible",timeout:45000});await page.waitForFunction(()=>document.querySelector('.nlfs[data-nl-flagship="v3"]')?.dataset.modelState==="ready",null,{timeout:45000});await settle(page,150);
  const row={viewport:viewport.name,tools:[],modelUnobstructed:false,passed:false};
  for(let index=0;index<EXPECTED_TOOLS.length;index+=1){const toolId=EXPECTED_TOOLS[index];await ensureToolVisibleKeyboard(page,toolId);const trigger=page.locator(`[data-nlvt-open="${toolId}"]`);await trigger.focus();const before=await exactStageState(page),mutationsBefore=report.runtime.mutationRequestsAfterUnlock.length,key=index%2===0?"Enter":"Space";await page.keyboard.press(key);const dialog=page.locator(`body>dialog.nlvt-dialog[data-nlvt-tool="${toolId}"]`);await dialog.waitFor({state:"visible"});const opened=await page.evaluate((id)=>{const dialog=document.querySelector(`body>dialog.nlvt-dialog[data-nlvt-tool="${id}"]`);return{exactTool:dialog?.dataset.nlvtTool===id,focusInside:Boolean(dialog?.contains(document.activeElement))};},toolId);await page.keyboard.press("Escape");await dialog.waitFor({state:"detached"});await settle(page,100);const after=await exactStageState(page),mutationsAfter=report.runtime.mutationRequestsAfterUnlock.length;const focusRestored=after.focusToken===`open:${toolId}`,scrollRestored=before.scrollX===after.scrollX&&before.scrollY===after.scrollY,modelRestored=before.canvas===after.canvas&&after.modelState==="ready",backgroundRestored=before.rootInert===after.rootInert&&before.rootAria===after.rootAria&&!after.bodyLocked,urlRestored=before.urlState===after.urlState,noWrite=mutationsBefore===mutationsAfter;const passed=opened.exactTool&&opened.focusInside&&focusRestored&&scrollRestored&&modelRestored&&backgroundRestored&&urlRestored&&noWrite;const evidence={tool:toolId,activationKey:key,openedExactTool:opened.exactTool,focusEnteredDialog:opened.focusInside,escapeClosed:true,focusRestored,scrollRestored,modelRestored,backgroundRestored,urlRestored,noWrite,passed};row.tools.push(evidence);if(!passed)fail("keyboard.escape-restore",`${viewport.name}/${toolId}: keyboard activation and Escape did not restore exact stage state.`,evidence);}
  const geometry=await geometrySnapshot(page),hitGrid=await auditStageHitGrid(page);row.modelUnobstructed=!geometry.stagePlayOverlap&&geometry.canvas.state==="ready"&&hitGrid.length===9&&hitGrid.every((item)=>item.inViewport&&item.accepted);if(!row.modelUnobstructed)fail("keyboard.model-obstruction",`${viewport.name}: keyboard journey left the protected model obstructed.`,{modelOverlap:geometry.stagePlayOverlap,ready:geometry.canvas.state==="ready",acceptedHitPoints:hitGrid.filter((item)=>item.inViewport&&item.accepted).length,totalHitPoints:hitGrid.length});row.passed=row.tools.every((item)=>item.passed)&&row.modelUnobstructed;report.keyboard.viewports.push(row);await verifyAssetResponses(network.responseAssets);await context.close();
}

async function auditTextResize200(browser,cookies,viewport){
  const context=await browser.newContext({viewport:{width:viewport.width,height:viewport.height},hasTouch:viewport.touch,locale:"he-IL",colorScheme:"light",reducedMotion:"reduce"});await context.addCookies(cookies);const page=await context.newPage(),network=installNetworkAudit(page,"authorized-text-resize-200");await page.goto(TARGET_URL,{waitUntil:"domcontentloaded",timeout:45000});await page.locator(`.nlfs[data-project-contract-id="${CONTRACT_ID}"]`).waitFor({state:"visible",timeout:45000});await page.waitForFunction(()=>document.querySelector('.nlfs[data-nl-flagship="v3"]')?.dataset.modelState==="ready",null,{timeout:45000});await settle(page,150);
  const baseScale=await applyTextResize200(page,'.nlfs[data-nl-flagship="v3"]');await settle(page,100);const base=await textResizeLayoutSnapshot(page,'.nlfs[data-nl-flagship="v3"]');const basePassed=baseScale.scaledTextCount>0&&baseScale.minimumScale>=1.99&&!base.missing&&base.documentOverflowX<=1&&base.scopeOverflowX<=1&&base.undersizedTargetCount===0&&base.innerScrollerCount===0&&base.semanticClipCount===0&&base.horizontalClipCount===0&&base.overlapCount===0&&!base.modelOverlap&&base.modelReady;const row={viewport:viewport.name,effectiveScale:baseScale.minimumScale,scaledTextCount:baseScale.scaledTextCount,base:{documentOverflowX:base.documentOverflowX,scopeOverflowX:base.scopeOverflowX,targetCount:base.targetCount,undersizedTargetCount:base.undersizedTargetCount,innerScrollerCount:base.innerScrollerCount,semanticClipCount:base.semanticClipCount,horizontalClipCount:base.horizontalClipCount,overlapCount:base.overlapCount,modelOverlap:base.modelOverlap,modelReady:base.modelReady,passed:basePassed},dialogs:[],modelUnobstructed:false,passed:false};if(!basePassed)fail("text-resize-200.base",`${viewport.name}: effective 200% text base layout failed reflow/geometry.`,row.base);
  for(const toolId of EXPECTED_TOOLS){await ensureToolVisible(page,toolId);const trigger=page.locator(`[data-nlvt-open="${toolId}"]`);await trigger.click();const dialog=page.locator(`body>dialog.nlvt-dialog[data-nlvt-tool="${toolId}"]`);await dialog.waitFor({state:"visible"});const scale=await applyTextResize200(page,`body>dialog.nlvt-dialog[data-nlvt-tool="${toolId}"]`);await settle(page,80);const layout=await textResizeLayoutSnapshot(page,`body>dialog.nlvt-dialog[data-nlvt-tool="${toolId}"]`);const rect=await dialog.boundingBox();const fullscreen=Boolean(rect&&Math.abs(rect.x)<=1&&Math.abs(rect.y)<=1&&Math.abs(rect.width-viewport.width)<=1&&Math.abs(rect.height-viewport.height)<=1);const passed=scale.scaledTextCount>0&&scale.minimumScale>=1.99&&!layout.missing&&layout.documentOverflowX<=1&&layout.scopeOverflowX<=1&&layout.undersizedTargetCount===0&&layout.innerScrollerCount===0&&layout.semanticClipCount===0&&layout.horizontalClipCount===0&&layout.overlapCount===0&&fullscreen;const evidence={tool:toolId,effectiveScale:scale.minimumScale,scaledTextCount:scale.scaledTextCount,fullscreen,documentOverflowX:layout.documentOverflowX,scopeOverflowX:layout.scopeOverflowX,targetCount:layout.targetCount,undersizedTargetCount:layout.undersizedTargetCount,innerScrollerCount:layout.innerScrollerCount,semanticClipCount:layout.semanticClipCount,horizontalClipCount:layout.horizontalClipCount,overlapCount:layout.overlapCount,passed};row.dialogs.push(evidence);if(!passed)fail("text-resize-200.dialog",`${viewport.name}/${toolId}: effective 200% text dialog failed reflow/geometry.`,evidence);await dialog.locator('[data-nlvt-action="back"]').click();await dialog.waitFor({state:"detached"});await settle(page,80);}
  const geometry=await geometrySnapshot(page),hitGrid=await auditStageHitGrid(page);row.modelUnobstructed=!geometry.stagePlayOverlap&&geometry.canvas.state==="ready"&&hitGrid.length===9&&hitGrid.every((item)=>item.inViewport&&item.accepted);if(!row.modelUnobstructed)fail("text-resize-200.model-obstruction",`${viewport.name}: effective 200% text journey obstructed the protected model.`,{modelOverlap:geometry.stagePlayOverlap,ready:geometry.canvas.state==="ready",acceptedHitPoints:hitGrid.filter((item)=>item.inViewport&&item.accepted).length,totalHitPoints:hitGrid.length});row.passed=row.base.passed&&row.dialogs.every((item)=>item.passed)&&row.modelUnobstructed;report.textResize200.viewports.push(row);await shot(page,`einstein-live-${viewport.name}-text-200`);await verifyAssetResponses(network.responseAssets);await context.close();
}

async function auditBrowserHistory(browser,cookies){
  const context=await browser.newContext({viewport:{width:390,height:844},hasTouch:true,locale:"he-IL"});await context.addCookies(cookies);const page=await context.newPage();installNetworkAudit(page,"authorized");
  await page.goto(TARGET_URL,{waitUntil:"domcontentloaded",timeout:45000});await page.locator(`.nlfs[data-project-contract-id="${CONTRACT_ID}"]`).waitFor({state:"visible",timeout:45000});await page.waitForFunction(()=>document.querySelector('.nlfs[data-nl-flagship="v3"]')?.dataset.modelState==="ready",null,{timeout:45000});
  const trigger=page.locator('[data-nlvt-open="view"]');await trigger.focus();const before=await exactStageState(page),mutationsBefore=report.runtime.mutationRequestsAfterUnlock.length;await trigger.click();const dialog=page.locator('body>dialog.nlvt-dialog[data-nlvt-tool="view"]');await dialog.waitFor({state:"visible"});const opened=await exactStageState(page);
  await page.goBack({waitUntil:"domcontentloaded",timeout:10000}).catch(()=>null);await settle(page,250);
  const rootPresent=await page.locator(`.nlfs[data-project-contract-id="${CONTRACT_ID}"]`).count()===1,dialogClosed=await page.locator("body>dialog.nlvt-dialog").count()===0,backState=rootPresent?await exactStageState(page):null;const back={sameDocument:Boolean(backState&&backState.urlState===before.urlState),dialogClosed,rootPresent,focusRestored:Boolean(backState&&backState.focusToken===before.focusToken),scrollRestored:Boolean(backState&&backState.scrollX===before.scrollX&&backState.scrollY===before.scrollY),modelRestored:Boolean(backState&&backState.canvas===before.canvas&&backState.modelState===before.modelState),backgroundRestored:Boolean(backState&&backState.rootInert===before.rootInert&&backState.rootAria===before.rootAria&&!backState.bodyLocked),passed:false};back.passed=Object.entries(back).filter(([key])=>key!=="passed").every(([,value])=>value===true);report.browserBack=back;if(!back.passed)fail("browser-history.back","Browser Back did not close the tool and restore exact stage state.",back);
  await page.goForward({waitUntil:"domcontentloaded",timeout:10000}).catch(()=>null);await dialog.waitFor({state:"visible",timeout:10000}).catch(()=>{});await settle(page,250);const forwardDialogVisible=await dialog.isVisible().catch(()=>false),forwardState=forwardDialogVisible?await exactStageState(page):null;const forward={sameDocument:Boolean(forwardState&&forwardState.urlState===opened.urlState),dialogRestored:forwardDialogVisible,exactTool:Boolean(forwardState&&forwardState.dialogTool===opened.dialogTool&&opened.dialogTool==="view"),focusRestored:Boolean(forwardState&&forwardState.focusToken===opened.focusToken),scrollRestored:Boolean(forwardState&&forwardState.scrollX===opened.scrollX&&forwardState.scrollY===opened.scrollY),modelRestored:Boolean(forwardState&&forwardState.canvas===opened.canvas&&forwardState.modelState===opened.modelState),backgroundRestored:Boolean(forwardState&&forwardState.rootInert===opened.rootInert&&forwardState.rootAria===opened.rootAria&&forwardState.bodyLocked===opened.bodyLocked&&forwardState.htmlOverflow===opened.htmlOverflow&&forwardState.bodyOverflow===opened.bodyOverflow),noWrite:report.runtime.mutationRequestsAfterUnlock.length===mutationsBefore,passed:false};forward.passed=Object.entries(forward).filter(([key])=>key!=="passed").every(([,value])=>value===true);if(!forward.passed)fail("browser-history.forward","Browser Forward did not restore the exact open tool state.",forward);report.browserHistory={tool:"view",transitions:[{direction:"back",...back},{direction:"forward",...forward}],passed:back.passed&&forward.passed};await context.close();
}

function markdown(){
  const pass=report.failures.length===0;const lines=["# Einstein flagship live acceptance","",`Result: **${pass?"PASS":"FAIL"}**`,`Target: ${report.target.url}`,`Contract: \`${CONTRACT_ID}\``,"","## Gates","",`- Anonymous password/privacy gate: ${report.anonymous?.passed?"PASS":"FAIL"}`,`- Anonymous discovery and private-asset denial: ${report.discovery?.passed?"PASS":"FAIL"}`,`- Expected plugin health/version: ${report.health?.passed?"PASS":"FAIL"}`,`- Authorized identity/privacy and exact-stage gate: ${report.unlocked?.passed?"PASS":"FAIL"}`,`- Keyboard activation + Escape exact restoration: ${report.keyboard?.passed?"PASS":"FAIL"}`,`- Browser Back + Forward exact tool restoration: ${report.browserHistory?.passed?"PASS":"FAIL"}`,`- Effective 200% text reflow/geometry: ${report.textResize200?.passed?"PASS":"FAIL"}`,`- Evidence-count contract: ${report.evidenceCounts?.matched?"PASS":"FAIL"}`,`- Viewport matrix: ${report.matrix.filter((row)=>row.passed).length}/${report.matrix.length}`,`- Exact protected assets observed: ${report.assets.length}/${EXPECTED_ASSETS.size}`,"","## Runtime","",`- Page errors: ${report.runtime.pageErrors.length}`,`- Console errors: ${report.runtime.consoleErrors.length}`,`- External requests: ${report.runtime.externalRequests.length}`,`- Sensitive-query requests: ${report.runtime.sensitiveQueryRequests.length}`,`- Mutating requests after unlock: ${report.runtime.mutationRequestsAfterUnlock.length}`,"","## Failures",""];
  if(!report.failures.length)lines.push("None.");else report.failures.forEach((item)=>lines.push(`- \`${item.code}\`: ${item.message}`));lines.push("","## Evidence","",...report.screenshots.map((item)=>`- \`${item}\``),"","Credentials, cookies, request bodies/headers, storage values and form values are excluded.","");return lines.join("\n");
}

let browser;
try{
  await mkdir(SCREENSHOT_DIR,{recursive:true});
  browser=await chromium.launch({headless:true,executablePath:CHROME_PATH,args:["--use-angle=swiftshader","--enable-webgl","--ignore-gpu-blocklist"]});
  const gateContext=await browser.newContext({viewport:{width:390,height:844},hasTouch:true,locale:"he-IL"});const gatePage=await gateContext.newPage();const gateNetwork=installNetworkAudit(gatePage,"anonymous");
  const lockedResponse=await gatePage.goto(TARGET_URL,{waitUntil:"domcontentloaded",timeout:45000});await settle(gatePage,250);await inspectLockedPage(gatePage,lockedResponse,gateNetwork);await shot(gatePage,"einstein-live-locked-390x844");
  await unlock(gatePage);const unlockedResponse=await gatePage.reload({waitUntil:"domcontentloaded",timeout:45000});await gatePage.locator(`.nlfs[data-project-contract-id="${CONTRACT_ID}"]`).waitFor({state:"visible",timeout:45000});await gatePage.waitForFunction(()=>document.querySelector('.nlfs[data-nl-flagship="v3"]')?.dataset.modelState==="ready",null,{timeout:45000});const identity=await unlockedIdentity(gatePage,unlockedResponse);
  const passwordCookies=(await gateContext.cookies(target.origin)).filter((cookie)=>/^wp-postpass_/i.test(cookie.name));if(!passwordCookies.length)fail("unlocked.cookie","WordPress post-password cookie was not set.");
  await auditAllProtectedAssets(gateContext);
  const anonymousContext=await browser.newContext({locale:"he-IL"});await auditHealth(anonymousContext);await anonymousProbe(anonymousContext,identity.postId);await anonymousContext.close();
  await gateContext.close();
  for(const viewport of VIEWPORTS)await auditViewport(browser,passwordCookies,viewport);
  for(const viewport of ACCESSIBILITY_VIEWPORTS)await auditKeyboardOnly(browser,passwordCookies,viewport);
  report.keyboard.passed=report.keyboard.viewports.length===ACCESSIBILITY_VIEWPORTS.length&&report.keyboard.viewports.every((row)=>row.passed);
  await auditBrowserHistory(browser,passwordCookies);
  for(const viewport of ACCESSIBILITY_VIEWPORTS)await auditTextResize200(browser,passwordCookies,viewport);
  report.textResize200.passed=report.textResize200.viewports.length===ACCESSIBILITY_VIEWPORTS.length&&report.textResize200.viewports.every((row)=>row.passed);
}catch(error){fail("runner.exception",safeError(error));process.exitCode=1;}finally{
  if(browser)await browser.close().catch(()=>{});
  if(report.runtime.externalRequests.length)fail("network.external","Authorized or anonymous page made external network requests.",{count:report.runtime.externalRequests.length,origins:[...new Set(report.runtime.externalRequests.map((item)=>item.origin))]});
  if(report.runtime.sensitiveQueryRequests.length)fail("network.pii-query","A request URL contained a credential/PII-like query key.",{count:report.runtime.sensitiveQueryRequests.length});
  if(report.runtime.mutationRequestsAfterUnlock.length)fail("network.mutation","The demonstration made a mutating request after unlock.",{count:report.runtime.mutationRequestsAfterUnlock.length});
  if(report.runtime.pageErrors.length||report.runtime.consoleErrors.length)fail("runtime.browser-errors","Browser page/console errors occurred.",{pageErrors:report.runtime.pageErrors.length,consoleErrors:report.runtime.consoleErrors.length});
  const observedEvidenceCounts={keyboardViewports:report.keyboard.viewports.length,keyboardToolChecks:report.keyboard.viewports.reduce((sum,row)=>sum+row.tools.length,0),keyboardEscapeRestores:report.keyboard.viewports.reduce((sum,row)=>sum+row.tools.filter((tool)=>tool.escapeClosed).length,0),browserHistoryTransitions:report.browserHistory?.transitions?.length||0,textResizeViewports:report.textResize200.viewports.length,textResizeDialogChecks:report.textResize200.viewports.reduce((sum,row)=>sum+row.dialogs.length,0)};const evidenceCountsMatched=Object.entries(EXPECTED_EVIDENCE_COUNTS).every(([key,value])=>observedEvidenceCounts[key]===value);report.evidenceCounts={expected:EXPECTED_EVIDENCE_COUNTS,observed:observedEvidenceCounts,matched:evidenceCountsMatched};if(!evidenceCountsMatched)fail("evidence.counts","Executable accessibility/history evidence count is incomplete.",report.evidenceCounts);
  report.finishedAt=new Date().toISOString();report.totals={passed:report.failures.length===0,failures:report.failures.length,warnings:report.warnings.length,viewports:report.matrix.length,assetsObserved:report.assets.length,keyboardToolChecks:observedEvidenceCounts.keyboardToolChecks,textResizeDialogChecks:observedEvidenceCounts.textResizeDialogChecks,historyTransitions:observedEvidenceCounts.browserHistoryTransitions};
  await mkdir(OUTPUT_DIR,{recursive:true});await writeFile(path.join(OUTPUT_DIR,"summary.json"),JSON.stringify(report,null,2)+"\n","utf8");await writeFile(path.join(OUTPUT_DIR,"summary.md"),markdown(),"utf8");
  console.log(`${report.totals.passed?"PASS":"FAIL"} Einstein flagship live acceptance: ${report.failures.length} failure(s), ${report.warnings.length} warning(s).`);console.log(`Sanitized reports: ${path.join(OUTPUT_DIR,"summary.json")} and ${path.join(OUTPUT_DIR,"summary.md")}`);if(!report.totals.passed)process.exitCode=1;
}
