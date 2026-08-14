/** Builds a portable URL inventory from the three cited research dossiers. */
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(here);
const inputs = [
  ["toha2-buyer-dossier.md", "ToHa2 public-source dossier"],
  ["the-park-buyer-dossier.md", "THE PARK public-source dossier"],
  ["competitor-benchmark.md", "Competitor UX benchmark"]
];

function csv(value) {
  const text = String(value ?? "");
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function authority(host, document) {
  if (/^(?:www\.)?(?:gov\.il|data\.gov\.il|e\.data\.gov\.il|nadlan\.gov\.il)$/i.test(host) ||
      /(?:\.gov\.il|\.muni\.il)$/i.test(host) ||
      /^(?:gisn|opendata)\.tel-aviv\.gov\.il$/i.test(host) ||
      /^(?:gtfs\.mot\.gov\.il|www\.nta\.co\.il|www\.rail\.co\.il|mayafiles\.tase\.co\.il)$/i.test(host)) {
    return "authority_or_statutory";
  }
  if (/^(?:www\.)?(?:amot\.co\.il|allied-re\.co\.il|alony-hetz\.com|gav-yam\.co\.il|toha\.gav-yam\.co\.il)$/i.test(host)) {
    return "owner_or_project";
  }
  if (document.includes("Competitor")) return "competitor_or_platform_documentation";
  return "third_party_or_project_team";
}

const rows = [];
for (const [filename, document] of inputs) {
  const body = await fs.readFile(path.join(here, filename), "utf8");
  const urls = [...body.matchAll(/https:\/\/[^\s\)\]\>\"`]+/g)]
    .map((match) => match[0].replace(/[.,;:]+$/g, ""));
  for (const url of [...new Set(urls)]) {
    let host = "invalid";
    try { host = new URL(url).host; } catch {}
    rows.push({ document, filename, host, source_class: authority(host, document), url });
  }
}

rows.sort((a, b) => a.host.localeCompare(b.host) || a.url.localeCompare(b.url));
const header = ["source_id", "document", "file", "host", "source_class", "accessed_date", "url"];
const lines = [header.join(",")];
rows.forEach((row, index) => {
  lines.push([
    `SRC-${String(index + 1).padStart(3, "0")}`,
    row.document,
    `research/${row.filename}`,
    row.host,
    row.source_class,
    "2026-08-10",
    row.url
  ].map(csv).join(","));
});
await fs.writeFile(path.join(root, "data", "source-url-register.csv"), lines.join("\n") + "\n", "utf8");

const counts = Object.entries(rows.reduce((acc, row) => {
  acc[row.source_class] = (acc[row.source_class] || 0) + 1;
  return acc;
}, {})).sort((a, b) => b[1] - a[1]);

const markdown = `# Source register and evidence policy

**Access date:** 10 August 2026  
**URL inventory:** \`data/source-url-register.csv\` (${rows.length} document/URL rows; ${new Set(rows.map((row) => row.url)).size} globally unique URLs)

## Canonical research files

- \`research/toha2-buyer-dossier.md\` — public-source project, location, transport, market, legal, delivery and technical due diligence; every material claim links directly to its source and labels contradictions/unknowns.
- \`research/the-park-buyer-dossier.md\` — the equivalent decision dossier for THE PARK.
- \`research/competitor-benchmark.md\` — live, indexed and official-documentation UX evidence, with blocked/paywalled observations explicitly separated.
- \`data/toha2-fact-matrix.csv\` and \`data/the-park-fact-matrix.csv\` — atomic claim/gap registers with answer owner and required artifact.
- \`data/competitor-pattern-matrix.csv\` — platform-by-pattern comparison.

## Inventory by broad source class

| Source class | Document/URL rows |
|---|---:|
${counts.map(([label, count]) => `| ${label.replaceAll("_", " ")} | ${count} |`).join("\n")}

The class is a routing aid, not a claim that every page on a domain proves the same thing. The dossier row and surrounding prose define the exact scope.

## Evidence hierarchy

1. **Authority/statutory:** lawfully published planning, municipal, transit, cadastral, government transaction or issuer filing evidence. It is authoritative only for its stated scope and date.
2. **Owner/project:** owner, developer or project-team statement. It is a claim until a certificate, signed schedule or executed document proves a decision-grade fact.
3. **Third-party/market:** broker, contractor, press, market report or listing. Useful for discovery and estimates; never a substitute for owner terms or statutory evidence.
4. **Observed live product:** the UI/DOM behavior directly measured on the access date.
5. **Derived:** transparent calculation from cited inputs. A derived value never identifies an unknown floor, tenant, availability state or contractual term.

## Required display rule

Every material fact promoted to the selected-floor UI must include value, evidence state, source identity, effective/observed date, verification date, scope, owner, confidence and caveat. Conflicting values remain side by side until reconciled. Unknowns remain unknown and expose a precise request.

## Access limitations

The competitor benchmark records anti-bot, paywall and indexed-only limitations per platform. No contact, callback, tour, alert, login or lead form was submitted. Public sources cannot establish the live landlord availability stack, signed commercial terms, exact floor measurement, final technical capacity or response routing; the two project matrices name the exact owner-controlled artifact needed for each such gap.
`;
await fs.writeFile(path.join(here, "source-register.md"), markdown, "utf8");
console.log(JSON.stringify({ rows: rows.length, uniqueUrls: new Set(rows.map((row) => row.url)).size, counts }));
