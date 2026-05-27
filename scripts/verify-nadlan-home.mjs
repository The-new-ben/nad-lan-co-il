import { spawn } from "node:child_process";
import { mkdir, rm, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";

const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const url = process.argv[2] || "https://nad-lan.co.il/";
const width = Number(process.argv[3] || 1366);
const height = Number(process.argv[4] || 900);
const outPrefix = process.argv[5] || "verification-screenshots/nadlan-home-check";
const port = 9440 + Math.floor(Math.random() * 500);
const userDataDir = join(tmpdir(), `codex-nadlan-chrome-${Date.now()}`);

await mkdir(userDataDir, { recursive: true });

const chrome = spawn(chromePath, [
  "--headless=new",
  "--disable-gpu",
  "--hide-scrollbars",
  "--no-first-run",
  "--no-default-browser-check",
  `--remote-debugging-port=${port}`,
  `--user-data-dir=${userDataDir}`,
  `--window-size=${width},${height}`,
  "about:blank",
], { stdio: "ignore" });

async function wait(ms) {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitForJson(path) {
  const endpoint = `http://127.0.0.1:${port}${path}`;
  for (let i = 0; i < 60; i++) {
    try {
      const res = await fetch(endpoint);
      if (res.ok) return await res.json();
    } catch {}
    await wait(250);
  }
  throw new Error(`Chrome CDP did not become ready: ${endpoint}`);
}

function connect(wsUrl) {
  const ws = new WebSocket(wsUrl);
  let id = 0;
  const pending = new Map();

  ws.addEventListener("message", (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && pending.has(msg.id)) {
      const { resolve, reject } = pending.get(msg.id);
      pending.delete(msg.id);
      if (msg.error) reject(new Error(JSON.stringify(msg.error)));
      else resolve(msg.result);
    }
  });

  return new Promise((resolve, reject) => {
    ws.addEventListener("open", () => {
      resolve({
        ws,
        send(method, params = {}) {
          const nextId = ++id;
          ws.send(JSON.stringify({ id: nextId, method, params }));
          return new Promise((res, rej) => pending.set(nextId, { resolve: res, reject: rej }));
        },
      });
    }, { once: true });
    ws.addEventListener("error", reject, { once: true });
  });
}

let browserClient;
try {
  const version = await waitForJson("/json/version");
  browserClient = await connect(version.webSocketDebuggerUrl);
  const created = await browserClient.send("Target.createTarget", { url: "about:blank" });
  const targets = await waitForJson("/json/list");
  const pageTarget = targets.find((target) => target.id === created.targetId) || targets.find((target) => target.type === "page");
  const page = await connect(pageTarget.webSocketDebuggerUrl);

  await page.send("Page.enable");
  await page.send("Runtime.enable");
  await page.send("Emulation.setDeviceMetricsOverride", {
    width,
    height,
    deviceScaleFactor: 1,
    mobile: width <= 520,
  });
  await page.send("Page.navigate", { url });
  await wait(4500);

  const expression = `(() => {
    const visible = el => !!el && getComputedStyle(el).display !== 'none' && getComputedStyle(el).visibility !== 'hidden' && el.getBoundingClientRect().width > 0 && el.getBoundingClientRect().height > 0;
    const pseudoText = el => {
      const content = getComputedStyle(el, '::after').content;
      return content && content !== 'none' ? content.replace(/^"|"$/g, '') : '';
    };
    const navLinks = Array.from(document.querySelectorAll('header.wp-block-template-part .wp-block-navigation a'))
      .filter(visible)
      .map(a => ({
        rawText: a.textContent.trim(),
        renderedLabel: pseudoText(a) || a.textContent.trim(),
        href: a.href,
        width: Math.round(a.getBoundingClientRect().width),
      }));
    const pageNav = document.querySelector('.nadlan-page-nav');
    const pageNavLabels = pageNav
      ? Array.from(pageNav.querySelectorAll('a')).filter(visible).map(a => a.textContent.trim())
      : [];
    const text = document.body.innerText || '';
    const bad = ['SEO','CRM','לידים','כוונת חיפוש','מסלולי כסף','מוניטיזציה','ספקים'];
    const firstImage = document.querySelector('.nadlan-photo-card img');
    return {
      url: location.href,
      title: document.title,
      viewport: { width: innerWidth, height: innerHeight },
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      hasHorizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 2,
      h1Texts: Array.from(document.querySelectorAll('h1')).filter(visible).map(h => h.textContent.trim()),
      headerLabels: navLinks.map(l => l.renderedLabel),
      pageNavVisible: visible(pageNav),
      pageNavLabels,
      hiddenLongHeaderText: navLinks.some(l => l.rawText.length > 28 && l.renderedLabel.length <= 12),
      customFooterVisible: visible(document.querySelector('.nadlan-footer')),
      heroVisible: visible(document.querySelector('.nadlan-hero-shell')),
      firstImageComplete: firstImage ? { complete: firstImage.complete, naturalWidth: firstImage.naturalWidth, naturalHeight: firstImage.naturalHeight } : null,
      internalVisible: bad.filter(w => text.includes(w)),
      styleMarkerPresent: Array.from(document.querySelectorAll('style')).some(s => s.textContent.includes('nadlan-header-short-labels-20260528')),
    };
  })()`;

  const metrics = await page.send("Runtime.evaluate", { expression, returnByValue: true });
  const topShot = await page.send("Page.captureScreenshot", { format: "png", fromSurface: true });
  await writeFile(`${outPrefix}-top.png`, Buffer.from(topShot.data, "base64"));
  await page.send("Runtime.evaluate", {
    expression: "document.querySelector('.nadlan-footer')?.scrollIntoView({block:'start'});",
    returnByValue: true,
  });
  await wait(800);
  const footerShot = await page.send("Page.captureScreenshot", { format: "png", fromSurface: true });
  await writeFile(`${outPrefix}-footer.png`, Buffer.from(footerShot.data, "base64"));

  console.log(JSON.stringify({
    url,
    width,
    height,
    metrics: metrics.result.value,
    screenshots: {
      top: `${outPrefix}-top.png`,
      footer: `${outPrefix}-footer.png`,
    },
  }, null, 2));
} finally {
  try { browserClient?.ws?.close(); } catch {}
  chrome.kill();
  await new Promise((resolve) => {
    chrome.once("exit", resolve);
    setTimeout(resolve, 1000);
  });
  await rm(userDataDir, { recursive: true, force: true }).catch(() => {});
}
