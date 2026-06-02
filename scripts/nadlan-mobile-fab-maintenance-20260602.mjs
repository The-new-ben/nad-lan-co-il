import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const apply = process.argv.includes("--apply");
const domain = "nad-lan.co.il";
const wpApi = "C:\\Users\\pro\\Documents\\websites\\tools\\wp-api.ps1";
const footerRoute = "/wp-json/wp/v2/template-parts/nadlan-revenue%2F%2Ffooter";

function runWp(route, method = "GET", body = undefined) {
  const psQuote = (value) => `'${String(value).replace(/'/g, "''")}'`;
  let dir;
  let bodyPath;
  if (body !== undefined) {
    dir = mkdtempSync(join(tmpdir(), "nadlan-wp-body-"));
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
    maxBuffer: 1024 * 1024 * 10,
  });

  if (dir) rmSync(dir, { recursive: true, force: true });
  if (result.status !== 0) throw new Error(result.stderr || result.stdout);
  return JSON.parse(result.stdout.trim());
}

const footer = runWp(`${footerRoute}?_fields=id,content,status`);
const raw = footer.content.raw;
const oldRule = "@media(max-width:600px){.nlfab-btn span.t{display:none}}";
const previousRule = "@media(max-width:600px){body{padding-bottom:74px}.nlfab{inset-inline-start:auto!important;inset-inline-end:auto!important;left:14px!important;right:auto!important;bottom:14px!important;inset-block-end:14px!important;align-items:flex-start;gap:8px}.nlfab-btn{min-width:44px;min-height:44px;padding:11px 13px;border-radius:6px}.nlfab-btn span.t{display:none}.nlfab-btn:last-child span.t{display:inline;font-size:12px;white-space:nowrap}.nlfab-btn:last-child{max-width:168px}.nlmodal{padding:12px}.nlmodal-box{padding:28px 20px}}";
const newRule = "@media(max-width:600px){body{padding-bottom:72px}.nlfab{inset-inline-start:auto!important;inset-inline-end:auto!important;left:12px!important;right:auto!important;bottom:12px!important;inset-block-end:12px!important;display:flex;flex-direction:row;align-items:center;gap:6px}.nlfab-btn{min-width:42px;min-height:42px;padding:10px 11px;border-radius:6px;font-size:11px;line-height:1}.nlfab-btn span.t{display:inline;font-size:11px;white-space:nowrap}.nlfab-btn:last-child span.t{display:none}.nlfab-btn:last-child::after{content:\"ייעוץ\";font-size:11px;white-space:nowrap}.nlmodal{padding:12px}.nlmodal-box{padding:28px 20px}}";

let next = raw;
let status = "unchanged";
if (raw.includes(newRule)) {
  status = "already-patched";
} else if (raw.includes(previousRule)) {
  next = raw.replace(previousRule, newRule);
  status = "patched";
} else if (raw.includes(oldRule)) {
  next = raw.replace(oldRule, newRule);
  status = "patched";
} else {
  throw new Error("Footer mobile FAB rule not found; refusing blind update.");
}

if (apply && next !== raw) {
  runWp(footerRoute, "POST", { content: next });
}

console.log(JSON.stringify({
  mode: apply ? "apply" : "dry-run",
  footerId: footer.id,
  status,
  changed: apply && next !== raw,
}, null, 2));
