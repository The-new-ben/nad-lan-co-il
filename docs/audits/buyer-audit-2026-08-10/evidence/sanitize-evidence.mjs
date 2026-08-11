/**
 * Creates portable copies of live JSON evidence for the handoff ZIP.
 * It removes public client tokens, ephemeral Mapbox SKU values and machine-local
 * paths while preserving observations and structure. Raw local captures remain
 * outside the packaged allowlist.
 */
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const target = path.join(here, "sanitized");
const files = [
  "journey-interaction-audit.json",
  "map-truth-probe.json",
  "live-dom-probe.json",
  "page-order-probe.json",
  "language-buyer-probe.json"
];

function sanitizeString(value) {
  return value
    .replace(/pk\.[A-Za-z0-9._-]+/g, "[REDACTED_PUBLIC_MAP_TOKEN]")
    .replace(/([?&]sku=)[^&#\s"]+/gi, "$1[REDACTED_EPHEMERAL_SKU]")
    .replace(/[A-Za-z]:\\Users\\[^\\]+\\justice\\deliverables\\nadlan-360-buyer-audit-2026-08-10\\/gi, "PACKAGE_ROOT\\")
    .replace(/[A-Za-z]:\/Users\/[^/]+\/justice\/deliverables\/nadlan-360-buyer-audit-2026-08-10\//gi, "PACKAGE_ROOT/")
    .replace(/[A-Za-z]:\/Users\/[^/]+\/.codex-worktrees\/[^/]+\//gi, "LOCAL_READ_ONLY_WORKTREE/");
}

function sanitizeValue(value) {
  if (typeof value === "string") return sanitizeString(value);
  if (Array.isArray(value)) return value.map(sanitizeValue);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value).map(([key, entry]) => [
        key,
        /(?:token|authorization|password|secret)/i.test(key)
          ? "[REDACTED_CLIENT_VALUE]"
          : sanitizeValue(entry)
      ])
    );
  }
  return value;
}

await fs.mkdir(target, { recursive: true });
const manifest = [];
for (const filename of files) {
  const sourcePath = path.join(here, filename);
  const outputPath = path.join(target, filename);
  const parsed = JSON.parse(await fs.readFile(sourcePath, "utf8"));
  const sanitized = sanitizeValue(parsed);
  const serialized = JSON.stringify(sanitized, null, 2) + "\n";
  await fs.writeFile(outputPath, serialized, "utf8");
  manifest.push({ filename, bytes: Buffer.byteLength(serialized), portable: true });
}
await fs.writeFile(
  path.join(target, "README.md"),
  "# Sanitized live evidence\n\nThese are structure-preserving copies of the live JSON captures. Public client tokens, ephemeral request SKUs and machine-local paths were redacted for the portable handoff. Screenshots and substantive observations are unchanged.\n",
  "utf8"
);
console.log(JSON.stringify({ files: manifest }, null, 2));
