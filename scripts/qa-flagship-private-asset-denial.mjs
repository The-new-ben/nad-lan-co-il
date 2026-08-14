import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import fs from "node:fs/promises";
import net from "node:net";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const router = path.join(root, "scripts/fixtures/flagship-private-asset-denial-router.php");
const sourcePath = path.join(root, "plugins/nadlan-config/inc/flagship-surface.php");
const php = process.env.PHP_BINARY || "php";
const expectedCache = "private, no-store, no-cache, max-age=0, must-revalidate";
const expectedRobots = "noindex, nofollow, noarchive";

async function reservePort() {
  const server = net.createServer();
  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolve);
  });
  const address = server.address();
  assert.ok(address && typeof address === "object" && address.port > 0, "fixture port allocation failed");
  await new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
  return address.port;
}

async function waitUntilReady(baseUrl, child, logs) {
  const deadline = Date.now() + 10_000;
  while (Date.now() < deadline) {
    if (child.exitCode !== null) throw new Error(`PHP fixture exited early (${child.exitCode}): ${logs.join("")}`);
    try {
      const response = await fetch(`${baseUrl}/fixture-health`, { redirect: "manual" });
      if (response.status === 204) return;
    } catch {}
    await new Promise((resolve) => setTimeout(resolve, 50));
  }
  throw new Error(`PHP fixture did not become ready: ${logs.join("")}`);
}

async function probe(baseUrl, requestPath, init = {}) {
  const response = await fetch(`${baseUrl}${requestPath}`, { redirect: "manual", ...init });
  const bytes = Buffer.from(await response.arrayBuffer());
  return {
    status: response.status,
    bytes,
    headers: Object.fromEntries(response.headers.entries()),
  };
}

function assertExactDenial(result, label) {
  assert.equal(result.status, 404, `${label}: exact HTTP 404`);
  assert.equal(result.bytes.length, 0, `${label}: exact zero-byte body`);
  assert.equal(result.headers["cache-control"]?.toLowerCase(), expectedCache, `${label}: exact private no-store/no-cache contract`);
  assert.equal(result.headers["x-robots-tag"]?.toLowerCase(), expectedRobots, `${label}: exact X-Robots contract`);
  assert.equal(result.headers["x-content-type-options"]?.toLowerCase(), "nosniff", `${label}: nosniff`);
  assert.equal(result.headers["referrer-policy"]?.toLowerCase(), "no-referrer", `${label}: no-referrer`);
  assert.equal(result.headers["content-length"], "0", `${label}: explicit zero Content-Length`);
}

const source = await fs.readFile(sourcePath, "utf8");
const helperStart = source.indexOf("function nadlan_flagship_v3_private_asset_deny() {");
const helperEnd = source.indexOf("if ( ! function_exists( 'nadlan_flagship_v3_private_asset_template' ) )", helperStart);
assert.ok(helperStart >= 0 && helperEnd > helperStart, "dedicated private-asset denial helper exists");
const dedicatedHelper = source.slice(helperStart, helperEnd);
assert.match(dedicatedHelper, /while \( ob_get_level\(\) > 0 \)/, "dedicated helper clears nested output buffers");
assert.match(dedicatedHelper, /Content-Length: 0/, "dedicated helper pins an empty body");
assert.match(dedicatedHelper, /\n\t\texit;/, "dedicated helper is terminal");
assert.doesNotMatch(dedicatedHelper, /wp_die\s*\(/, "private-asset denial never delegates to wp_die");
assert.equal((source.match(/nadlan_flagship_v3_private_asset_deny\(\);/g) || []).length, 2, "both private-asset rejection branches use the dedicated helper");
assert.match(source, /function nadlan_flagship_v3_fail_closed\(\) \{[\s\S]*?wp_die\s*\(/, "ordinary page validation retains wp_die semantics");
assert.match(source, /function nadlan_flagship_v3_template_guard\(\) \{[\s\S]*?nadlan_flagship_v3_fail_closed\(\);/, "ordinary template guard retains the shared page failure helper");

const port = await reservePort();
const baseUrl = `http://127.0.0.1:${port}`;
const logs = [];
const child = spawn(php, ["-d", "display_errors=0", "-S", `127.0.0.1:${port}`, router], {
  cwd: root,
  env: { ...process.env },
  stdio: ["ignore", "pipe", "pipe"],
  windowsHide: true,
});
child.stdout.on("data", (chunk) => logs.push(chunk.toString("utf8")));
child.stderr.on("data", (chunk) => logs.push(chunk.toString("utf8")));

try {
  await waitUntilReady(baseUrl, child, logs);
  assertExactDenial(await probe(baseUrl, "/flagship-private-asset"), "route-root parse denial");
  assertExactDenial(await probe(baseUrl, "/flagship-private-asset/einstein-tower-6885-32/model-hd.glb?token=forbidden"), "query parse denial");
  assertExactDenial(await probe(baseUrl, "/flagship-private-asset/einstein-tower-6885-32/model-hd.glb", { method: "POST" }), "method parse denial");
  assertExactDenial(await probe(baseUrl, "/flagship-private-asset/einstein-tower-6885-32/%2e%2e/model-hd.glb"), "encoded traversal parse denial");
  assertExactDenial(await probe(baseUrl, "/flagship-private-asset/einstein-tower-6885-32/model-hd.glb"), "descriptor denial");
  assertExactDenial(await probe(baseUrl, "/flagship-private-asset/einstein-tower-6885-32/model-hd.glb", { method: "HEAD" }), "HEAD descriptor denial");
  assertExactDenial(await probe(baseUrl, "/direct-private-wrapper"), "direct wrapper denial");

  const ordinary = await probe(baseUrl, "/ordinary-page-validation");
  assert.equal(ordinary.status, 404, "ordinary page validation remains a 404");
  assert.ok(ordinary.bytes.length > 0 && ordinary.bytes.toString("utf8").includes("Not found."), "ordinary page validation retains its wp_die body");
  console.log("PASS flagship private-asset denial: 7 exact empty 404 paths; ordinary wp_die unchanged");
} finally {
  child.kill();
  await Promise.race([
    new Promise((resolve) => child.once("exit", resolve)),
    new Promise((resolve) => setTimeout(resolve, 2_000)),
  ]);
}
