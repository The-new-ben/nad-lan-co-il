import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const REGISTRY = "plugins/nadlan-config/assets/flagship-v3/contracts/registry.json";
const CONTRACT_ID = "einstein-tower-6885-32";
const SOURCE_ROOT = "assets/projects/einstein-tower";
const LEGACY_PLUGIN_ROOT = "plugins/nadlan-config/assets/flagship-v3/projects/einstein-tower";
const STORAGE_PREFIX = "assets/flagship-v3/private-assets/einstein-tower/";
const WRAPPER_PREFIX = Buffer.from(
  "<?php\n" +
  "while ( ob_get_level() > 0 ) {\n" +
  "\tob_end_clean();\n" +
  "}\n" +
  "http_response_code( 404 );\n" +
  "header( 'Cache-Control: private, no-store, no-cache, max-age=0, must-revalidate' );\n" +
  "header( 'X-Robots-Tag: noindex, nofollow, noarchive' );\n" +
  "header( 'X-Content-Type-Options: nosniff' );\n" +
  "header( 'Referrer-Policy: no-referrer' );\n" +
  "header( 'Content-Length: 0' );\n" +
  "__halt_compiler();\n",
  "utf8",
);

const absolute = (relative) => path.join(ROOT, relative);
const sha256 = (value) => crypto.createHash("sha256").update(value).digest("hex");
const assert = (condition, message) => { if (!condition) throw new Error(message); };
const safeRelativeName = (value) => typeof value === "string"
  && /^[a-z0-9][a-z0-9._/-]*$/.test(value)
  && !value.includes("//")
  && !value.split("/").includes("..");

const registry = JSON.parse(fs.readFileSync(absolute(REGISTRY), "utf8"));
const contract = registry.contracts.find((candidate) => candidate.project_contract_id === CONTRACT_ID);
assert(contract && contract.public_release_enabled === false, "Private Einstein contract is missing or publicly enabled.");
assert(Array.isArray(contract.private_assets) && contract.private_assets.length === 7, "Exactly seven protected assets must be registered.");

const seenNames = new Set();
const seenStorage = new Set();
const results = [];

for (const descriptor of contract.private_assets) {
  const { requested_name: requestedName, storage_file: storageFile, bytes, sha256: expectedSha, mime } = descriptor;
  assert(safeRelativeName(requestedName), `Unsafe requested_name: ${requestedName}`);
  assert(typeof storageFile === "string" && storageFile.startsWith(STORAGE_PREFIX) && storageFile.endsWith(".asset.php"), `Unsafe storage_file: ${storageFile}`);
  assert(safeRelativeName(storageFile), `Invalid storage_file: ${storageFile}`);
  assert(!seenNames.has(requestedName) && !seenStorage.has(storageFile), `Duplicate private asset descriptor: ${requestedName}`);
  assert(Number.isSafeInteger(bytes) && bytes > 0, `Invalid byte count: ${requestedName}`);
  assert(/^[a-f0-9]{64}$/.test(expectedSha), `Invalid SHA-256: ${requestedName}`);
  assert(["model/gltf-binary", "image/webp"].includes(mime), `Invalid MIME: ${requestedName}`);
  seenNames.add(requestedName);
  seenStorage.add(storageFile);

  const sourceRelative = `${SOURCE_ROOT}/${requestedName}`;
  const source = fs.readFileSync(absolute(sourceRelative));
  assert(source.byteLength === bytes, `Canonical source size drift: ${requestedName}`);
  assert(sha256(source) === expectedSha, `Canonical source hash drift: ${requestedName}`);

  const outputRelative = `plugins/nadlan-config/${storageFile}`;
  const output = Buffer.concat([WRAPPER_PREFIX, source]);
  fs.mkdirSync(path.dirname(absolute(outputRelative)), { recursive: true });
  fs.writeFileSync(absolute(outputRelative), output);
  assert(fs.readFileSync(absolute(outputRelative)).equals(output), `Wrapper write drift: ${requestedName}`);

  const legacyRelative = `${LEGACY_PLUGIN_ROOT}/${requestedName}`;
  if (fs.existsSync(absolute(legacyRelative))) fs.rmSync(absolute(legacyRelative));
  results.push({
    requested_name: requestedName,
    source_file: sourceRelative,
    storage_file: outputRelative,
    payload_bytes: bytes,
    payload_sha256: expectedSha,
    wrapper_bytes: output.byteLength,
    wrapper_sha256: sha256(output),
    mime,
  });
}

for (const relative of [`${LEGACY_PLUGIN_ROOT}/experience`, LEGACY_PLUGIN_ROOT]) {
  const directory = absolute(relative);
  if (fs.existsSync(directory) && fs.readdirSync(directory).length === 0) fs.rmdirSync(directory);
}

console.log(JSON.stringify({
  ok: true,
  contract: CONTRACT_ID,
  wrapper_prefix_bytes: WRAPPER_PREFIX.byteLength,
  wrapper_prefix_sha256: sha256(WRAPPER_PREFIX),
  assets: results,
}));
