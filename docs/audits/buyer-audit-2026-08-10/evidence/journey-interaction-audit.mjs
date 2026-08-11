import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const OUT = path.dirname(fileURLToPath(import.meta.url));
const SHOTS = path.join(OUT, "screenshots");
fs.mkdirSync(SHOTS, { recursive: true });

const projects = [
  {
    key: "toha2",
    slug: "toha2-tel-aviv",
    unit: "floor-20",
    url: "https://nad-lan.co.il/projects/toha2-tel-aviv/?project=toha2-tel-aviv&lang=he&unit=floor-20",
  },
  {
    key: "park",
    slug: "the-park-bnei-brak",
    unit: "floor-20",
    url: "https://nad-lan.co.il/projects/the-park-bnei-brak/?project=the-park-bnei-brak&lang=he&unit=floor-20",
  },
];
const viewports = [
  { key: "mobile", width: 375, height: 812 },
  { key: "desktop", width: 1280, height: 800 },
];
const toolNames = ["area", "plan", "view", "tour", "studio", "compare", "contact"];

function safeFile(value) {
  return value.replace(/[^a-z0-9_-]+/gi, "-");
}

async function visibleLocator(page, selector) {
  const all = page.locator(selector);
  for (let i = 0; i < await all.count(); i += 1) {
    const item = all.nth(i);
    if (await item.isVisible().catch(() => false)) return item;
  }
  return null;
}

async function snapshot(page) {
  return page.evaluate(() => {
    const visible = (el) => {
      if (!el) return false;
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return !!r.width && !!r.height && cs.visibility !== "hidden" && cs.display !== "none";
    };
    const rect = (el) => {
      if (!el) return null;
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return {
        x: +r.x.toFixed(2), y: +r.y.toFixed(2), width: +r.width.toFixed(2), height: +r.height.toFixed(2),
        display: cs.display, visibility: cs.visibility, opacity: cs.opacity,
        overflowX: cs.overflowX, overflowY: cs.overflowY,
        clientWidth: el.clientWidth, clientHeight: el.clientHeight,
        scrollWidth: el.scrollWidth, scrollHeight: el.scrollHeight,
      };
    };
    const activeDialogs = [...document.querySelectorAll("dialog,[role='dialog']")]
      .filter(visible)
      .map((el) => ({
        id: el.id,
        className: el.className,
        role: el.getAttribute("role"),
        ariaModal: el.getAttribute("aria-modal"),
        text: el.innerText.slice(0, 8000),
        rect: rect(el),
        inputs: [...el.querySelectorAll("input,select,textarea")].map((field) => ({
          tag: field.tagName,
          type: field.type || null,
          name: field.name || null,
          label: field.labels ? [...field.labels].map((label) => label.innerText.trim()).join(" | ") : "",
          placeholder: field.placeholder || "",
          required: field.required,
          autocomplete: field.autocomplete || "",
        })),
        buttons: [...el.querySelectorAll("button")].filter(visible).map((button) => button.innerText.trim()),
        links: [...el.querySelectorAll("a[href]")].filter(visible).map((a) => ({ text: a.innerText.trim(), href: a.href })),
        maps: [...el.querySelectorAll(".mapboxgl-map,[data-role*='map'],canvas")].filter(visible).map((map) => ({
          tag: map.tagName, className: map.className, role: map.getAttribute("role"), ariaLabel: map.getAttribute("aria-label"), rect: rect(map),
        })),
        images: [...el.querySelectorAll("img")].filter(visible).map((img) => ({ src: img.currentSrc || img.src, alt: img.alt, naturalWidth: img.naturalWidth, naturalHeight: img.naturalHeight, rect: rect(img) })),
        iframes: [...el.querySelectorAll("iframe")].filter(visible).map((frame) => ({ src: frame.src, title: frame.title, rect: rect(frame) })),
        internalScrollers: [...el.querySelectorAll("*")].filter((node) => {
          const cs = getComputedStyle(node);
          return visible(node) && /(auto|scroll)/.test(`${cs.overflowX} ${cs.overflowY}`) && (node.scrollHeight > node.clientHeight + 1 || node.scrollWidth > node.clientWidth + 1);
        }).map((node) => ({ tag: node.tagName, id: node.id, className: node.className, rect: rect(node) })).slice(0, 100),
      }));
    const selected = document.querySelector(".nl-unit-screen,.nl-unit-summary");
    return {
      url: location.href,
      title: document.title,
      lang: document.documentElement.lang,
      dir: document.documentElement.dir,
      scrollY,
      bodyOverflow: getComputedStyle(document.body).overflow,
      htmlOverflow: getComputedStyle(document.documentElement).overflow,
      selectedText: selected?.innerText?.slice(0, 10000) || "",
      selectedRect: rect(selected),
      activeElement: {
        tag: document.activeElement?.tagName || null,
        id: document.activeElement?.id || null,
        text: document.activeElement?.textContent?.trim()?.slice(0, 160) || "",
      },
      activeDialogs,
      duplicates: [...new Set([...document.querySelectorAll("[id]")].map((el) => el.id).filter((id, index, ids) => id && ids.indexOf(id) !== index))],
      selectedInternalScrollers: selected ? [...selected.querySelectorAll("*")].filter((node) => {
        const cs = getComputedStyle(node);
        return visible(node) && /(auto|scroll)/.test(`${cs.overflowX} ${cs.overflowY}`) && (node.scrollHeight > node.clientHeight + 1 || node.scrollWidth > node.clientWidth + 1);
      }).map((node) => ({ tag: node.tagName, id: node.id, className: node.className, rect: rect(node) })).slice(0, 100) : [],
    };
  });
}

async function extractPageInventory(page) {
  return page.evaluate(() => {
    const clean = (text) => String(text || "").replace(/\s+/g, " ").trim();
    const visible = (el) => {
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return !!r.width && !!r.height && cs.visibility !== "hidden" && cs.display !== "none";
    };
    const schemas = [...document.querySelectorAll("script[type='application/ld+json']")].map((script) => {
      try { return JSON.parse(script.textContent); } catch { return { parseError: true, text: script.textContent.slice(0, 1000) }; }
    });
    const headings = [...document.querySelectorAll("h1,h2,h3,h4,h5,h6")].map((el) => ({ level: el.tagName, text: clean(el.innerText), visible: visible(el) }));
    const links = [...document.querySelectorAll("a[href]")].filter(visible).map((a) => ({ text: clean(a.innerText || a.getAttribute("aria-label")), href: a.href }));
    const forms = [...document.forms].map((form) => ({
      id: form.id, action: form.action, method: form.method,
      text: clean(form.innerText).slice(0, 3000),
      fields: [...form.elements].map((field) => ({ tag: field.tagName, type: field.type, name: field.name, required: field.required, placeholder: field.placeholder || "" })),
    }));
    const buttons = [...document.querySelectorAll("button,[role='button']")].filter(visible).map((el) => ({
      text: clean(el.innerText || el.getAttribute("aria-label")),
      tool: el.getAttribute("data-tool"), act: el.getAttribute("data-act"),
    }));
    const meta = [...document.querySelectorAll("meta")].map((m) => ({ name: m.name || m.getAttribute("property"), content: m.content })).filter((m) => m.name);
    return {
      bodyText: document.body.innerText,
      headings,
      links,
      forms,
      buttons,
      meta,
      schemas,
      showroomConfig: window.NADLAN_SHOWROOM ? JSON.parse(JSON.stringify(window.NADLAN_SHOWROOM)) : null,
    };
  });
}

const browser = await chromium.launch({ headless: true });
const report = { generatedAt: new Date().toISOString(), projects: [] };

for (const project of projects) {
  for (const viewport of viewports) {
    const context = await browser.newContext({ viewport });
    await context.route(/google-analytics|googletagmanager|stripe\.com\/v3|events\.mapbox/i, (route) => route.abort());
    const page = await context.newPage();
    const consoleMessages = [];
    const pageErrors = [];
    const failedRequests = [];
    page.on("console", (msg) => {
      if (["error", "warning"].includes(msg.type())) consoleMessages.push({ type: msg.type(), text: msg.text() });
    });
    page.on("pageerror", (error) => pageErrors.push(String(error)));
    page.on("requestfailed", (request) => {
      if (!/google-analytics|googletagmanager|stripe\.com\/v3|events\.mapbox/i.test(request.url())) {
        failedRequests.push({ url: request.url(), reason: request.failure()?.errorText || "unknown" });
      }
    });
    const response = await page.goto(project.url, { waitUntil: "domcontentloaded", timeout: 120000 });
    await page.waitForTimeout(3000);
    await page.locator("#nl-root").scrollIntoViewIfNeeded().catch(() => {});
    await page.waitForTimeout(1200);
    const inventory = await extractPageInventory(page);
    fs.writeFileSync(path.join(OUT, `${project.key}-${viewport.key}-visible-text.txt`), inventory.bodyText, "utf8");
    const selectedShot = path.join(SHOTS, `${project.key}-${viewport.key}-selected-floor-20.png`);
    await page.screenshot({ path: selectedShot, fullPage: false });
    const selectedState = await snapshot(page);
    const tools = [];
    for (const tool of toolNames) {
      const trigger = await visibleLocator(page, `[data-tool='${tool}']`);
      if (!trigger) {
        tools.push({ tool, found: false });
        continue;
      }
      const triggerText = await trigger.innerText().catch(() => "");
      await trigger.click({ force: false, timeout: 5000 }).catch(async () => trigger.click({ force: true }));
      await page.waitForTimeout(tool === "studio" || tool === "view" || tool === "area" ? 2200 : 1000);
      const openState = await snapshot(page);
      const shot = path.join(SHOTS, `${project.key}-${viewport.key}-${safeFile(tool)}.png`);
      await page.screenshot({ path: shot, fullPage: false });
      const back = await visibleLocator(page, "[data-act='close-tool'],[data-action='close'],.nl-unit-tool__back,.nlst-close,dialog button");
      let closeMethod = "none";
      if (back) {
        await back.click({ force: true }).catch(() => {});
        closeMethod = "button";
      }
      await page.waitForTimeout(800);
      if ((await snapshot(page)).activeDialogs.length) {
        await page.keyboard.press("Escape").catch(() => {});
        closeMethod = closeMethod === "button" ? "button+escape" : "escape";
        await page.waitForTimeout(800);
      }
      const closedState = await snapshot(page);
      tools.push({
        tool,
        found: true,
        triggerText,
        openState,
        screenshot: shot,
        closeMethod,
        closedState,
      });
    }
    report.projects.push({
      project: project.key,
      viewport,
      status: response?.status() ?? null,
      selectedShot,
      selectedState,
      inventory: {
        headings: inventory.headings,
        links: inventory.links,
        forms: inventory.forms,
        buttons: inventory.buttons,
        meta: inventory.meta,
        schemas: inventory.schemas,
        showroomConfig: inventory.showroomConfig,
        visibleTextPath: path.join(OUT, `${project.key}-${viewport.key}-visible-text.txt`),
      },
      tools,
      consoleMessages,
      pageErrors,
      failedRequests,
    });
    console.log(`${project.key} ${viewport.key}: ${tools.filter((tool) => tool.found).length}/${toolNames.length} tools inspected`);
    await context.close();
  }
}

await browser.close();
const output = path.join(OUT, "journey-interaction-audit.json");
fs.writeFileSync(output, JSON.stringify(report, null, 2), "utf8");
console.log(output);
