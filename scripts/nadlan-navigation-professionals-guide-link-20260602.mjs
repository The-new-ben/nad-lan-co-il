import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const apply = process.argv.includes("--apply");
const domain = "nad-lan.co.il";
const wpApi = "C:\\Users\\pro\\Documents\\websites\\tools\\wp-api.ps1";
const navId = 4;
const markerUrl = "https://nad-lan.co.il/real-estate-professionals-guide/";
const newLink = '<!-- wp:navigation-link {"label":"מדריך בחירת אנשי מקצוע","url":"https://nad-lan.co.il/real-estate-professionals-guide/","kind":"custom"} /-->';

function psQuote(value) {
  return `'${String(value).replace(/'/g, "''")}'`;
}

function runWp(route, method = "GET", body = undefined) {
  let dir;
  let bodyPath;
  if (body !== undefined) {
    dir = mkdtempSync(join(tmpdir(), "nadlan-nav-body-"));
    bodyPath = join(dir, "body.json");
    writeFileSync(bodyPath, JSON.stringify(body), "utf8");
  }

  const command = [
    "&",
    psQuote(wpApi),
    "-Domain",
    psQuote(domain),
    "-Route",
    psQuote(route),
    "-Method",
    psQuote(method),
    bodyPath ? `-BodyPath ${psQuote(bodyPath)}` : "",
    "| ConvertTo-Json -Depth 100 -Compress",
  ].filter(Boolean).join(" ");

  const result = spawnSync("powershell.exe", [
    "-NoProfile",
    "-ExecutionPolicy",
    "Bypass",
    "-Command",
    command,
  ], {
    encoding: "utf8",
    maxBuffer: 1024 * 1024 * 12,
  });

  if (dir) rmSync(dir, { recursive: true, force: true });
  if (result.status !== 0) {
    throw new Error(`wp-api failed for ${route}: ${result.stderr || result.stdout}`);
  }
  const out = result.stdout.trim();
  if (!out) return null;
  const parsed = JSON.parse(out);
  if (parsed && Array.isArray(parsed.value) && Number.isInteger(parsed.Count)) {
    return parsed.value;
  }
  return parsed;
}

async function inspectLiveNav() {
  const res = await fetch("https://nad-lan.co.il/", {
    headers: { "User-Agent": "Codex-Nadlan-Nav-Verify/2026-06-02" },
  });
  const html = await res.text();
  return {
    status: res.status,
    hasGuideLink: html.includes(markerUrl),
    linkOccurrences: (html.match(new RegExp(markerUrl.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "g")) || []).length,
  };
}

const nav = runWp(`/wp-json/wp/v2/navigation/${navId}?context=edit`);
const before = nav.content.raw;
let after = before;
let action = "already-present";

if (!before.includes(markerUrl)) {
  const target = '<!-- wp:navigation-link {"label":"אינדקס מקצוענים","url":"https://nad-lan.co.il/professionals/","kind":"custom"} /-->';
  if (!before.includes(target)) {
    throw new Error("Could not find professionals submenu insertion point.");
  }
  after = before.replace(target, `${target}\n${newLink}`);
  action = "insert-after-professionals-index";
}

let updated = null;
if (apply && after !== before) {
  updated = runWp(`/wp-json/wp/v2/navigation/${navId}`, "POST", {
    content: after,
  });
}

const live = await inspectLiveNav();

console.log(JSON.stringify({
  mode: apply ? "apply" : "dry-run",
  navId,
  action,
  changed: apply && after !== before,
  beforeHadGuideLink: before.includes(markerUrl),
  afterHasGuideLink: after.includes(markerUrl),
  updatedModified: updated?.modified || null,
  live,
}, null, 2));
