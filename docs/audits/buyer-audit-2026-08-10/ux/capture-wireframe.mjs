/** PROPOSAL EVIDENCE ONLY — captures and geometrically audits the local, offline wireframe. */
import { chromium } from "playwright";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const html = path.join(here, "commercial-decision-surface-wireframe.html");
const out = path.join(here, "screenshots");
await fs.mkdir(out, { recursive: true });

const browser = await chromium.launch({ headless: true });
const results = [];

for (const viewport of [
  { name: "mobile-375x812", width: 375, height: 812 },
  { name: "short-mobile-320x568", width: 320, height: 568 },
  { name: "landscape-568x320", width: 568, height: 320 },
  { name: "desktop-1280x800", width: 1280, height: 800 }
]) {
  const page = await browser.newPage({ viewport: { width: viewport.width, height: viewport.height } });
  const errors = [];
  page.on("pageerror", (error) => errors.push(`pageerror: ${String(error)}`));
  page.on("console", (message) => {
    if (message.type() === "error") errors.push(`console: ${message.text()}`);
  });
  await page.goto(pathToFileURL(html).href, { waitUntil: "load" });
  await page.screenshot({ path: path.join(out, `${viewport.name}-decision.png`), fullPage: false });

  const decision = await page.evaluate(() => {
    const tolerance = 1;
    const rectValue = (rect) => ({
      x: rect.x,
      y: rect.y,
      width: rect.width,
      height: rect.height,
      right: rect.right,
      bottom: rect.bottom
    });
    const visible = (node) => {
      const style = getComputedStyle(node);
      const rect = node.getBoundingClientRect();
      return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) !== 0 && rect.width > 0 && rect.height > 0;
    };
    const viewportRect = { left: 0, top: 0, right: innerWidth, bottom: innerHeight };
    const clips = (node, label) => {
      const rect = node.getBoundingClientRect();
      const violations = [];
      if (rect.left < viewportRect.left - tolerance || rect.top < viewportRect.top - tolerance || rect.right > viewportRect.right + tolerance || rect.bottom > viewportRect.bottom + tolerance) {
        violations.push({ label, against: "viewport", rect: rectValue(rect), bounds: viewportRect });
      }
      for (let ancestor = node.parentElement; ancestor; ancestor = ancestor.parentElement) {
        const style = getComputedStyle(ancestor);
        const clipsX = /(hidden|clip|auto|scroll)/.test(style.overflowX);
        const clipsY = /(hidden|clip|auto|scroll)/.test(style.overflowY);
        if (!clipsX && !clipsY) continue;
        const ancestorRect = ancestor.getBoundingClientRect();
        const bounds = {
          left: ancestorRect.left + ancestor.clientLeft,
          top: ancestorRect.top + ancestor.clientTop,
          right: ancestorRect.left + ancestor.clientLeft + ancestor.clientWidth,
          bottom: ancestorRect.top + ancestor.clientTop + ancestor.clientHeight
        };
        if ((clipsX && (rect.left < bounds.left - tolerance || rect.right > bounds.right + tolerance)) || (clipsY && (rect.top < bounds.top - tolerance || rect.bottom > bounds.bottom + tolerance))) {
          violations.push({ label, against: ancestor.className || ancestor.id || ancestor.tagName, rect: rectValue(rect), bounds });
        }
      }
      return violations;
    };
    const requiredSelectors = [".model", ".identity", ".exposure", ".facts", ".doors", ".quick", ".cta"];
    const boxes = Object.fromEntries(requiredSelectors.map((selector) => {
      const node = document.querySelector(selector);
      return [selector, node && visible(node) ? rectValue(node.getBoundingClientRect()) : null];
    }));
    const requiredNodes = requiredSelectors.flatMap((selector) => [...document.querySelectorAll(selector)].filter(visible).map((node, index) => ({ node, label: `${selector}[${index}]` })));
    const factLabelViolations = [...document.querySelectorAll(".fact")].filter(visible).flatMap((fact, index) => {
      const label = fact.querySelector("label");
      return !label || !visible(label) || !label.textContent.trim()
        ? [{ label: `.fact[${index}]`, issue: "missing_or_hidden_meaning_label" }]
        : [];
    });
    const controls = [...document.querySelectorAll("button,select,input,a[href]")].filter(visible);
    const targetViolations = controls
      .map((node) => ({ label: node.id || node.getAttribute("aria-label") || node.textContent.trim().slice(0, 60), rect: rectValue(node.getBoundingClientRect()) }))
      .filter(({ rect }) => rect.width < 44 - tolerance || rect.height < 44 - tolerance);
    const typographySelectors = [".identity h1", ".exposure h2", ".fact strong", ".door strong", ".cta"];
    const typographyViolations = typographySelectors
      .flatMap((selector) => [...document.querySelectorAll(selector)].filter(visible).map((node) => ({
        label: selector,
        text: node.textContent.trim().slice(0, 80),
        fontSize: Number.parseFloat(getComputedStyle(node).fontSize)
      })))
      .filter(({ fontSize }) => !Number.isFinite(fontSize) || fontSize < 12);
    const clippingViolations = [
      ...requiredNodes.flatMap(({ node, label }) => clips(node, label)),
      ...controls.flatMap((node, index) => clips(node, `control[${index}] ${node.id || node.textContent.trim().slice(0, 40)}`))
    ];
    const internalScrollers = [...document.querySelectorAll("body *")].filter((node) => {
      const style = getComputedStyle(node);
      return /(auto|scroll)/.test(`${style.overflowX} ${style.overflowY}`) &&
        (node.scrollHeight > node.clientHeight + tolerance || node.scrollWidth > node.clientWidth + tolerance);
    }).map((node) => node.className || node.id || node.tagName);
    const contentOverflows = [".app", ".model", ".rail", ".identity", ".exposure", ".facts", ".doors", ".quick"]
      .flatMap((selector) => [...document.querySelectorAll(selector)])
      .filter(visible)
      .filter((node) => node.scrollHeight > node.clientHeight + tolerance || node.scrollWidth > node.clientWidth + tolerance)
      .map((node) => ({
        label: node.className || node.id || node.tagName,
        client: { width: node.clientWidth, height: node.clientHeight },
        scroll: { width: node.scrollWidth, height: node.scrollHeight }
      }));
    const duplicateIds = [...document.querySelectorAll("[id]")]
      .map((node) => node.id)
      .filter((id, index, all) => all.indexOf(id) !== index);
    const orientationCompass = document.querySelector(".compass");
    const orientationTruthGate = orientationCompass ? {
      state: orientationCompass.dataset.evidenceState || "",
      claimedBeamCount: orientationCompass.querySelectorAll(".arc,[data-beam],[data-landmark]").length,
      neutralMarkerVisible: Boolean(orientationCompass.querySelector(".unknown-orientation") && visible(orientationCompass.querySelector(".unknown-orientation"))),
      backgroundImage: getComputedStyle(orientationCompass).backgroundImage,
      passed: orientationCompass.dataset.evidenceState === "unknown" &&
        orientationCompass.querySelectorAll(".arc,[data-beam],[data-landmark]").length === 0 &&
        Boolean(orientationCompass.querySelector(".unknown-orientation") && visible(orientationCompass.querySelector(".unknown-orientation"))) &&
        !/conic-gradient/i.test(getComputedStyle(orientationCompass).backgroundImage)
    } : { passed: false, reason: "missing_compass" };
    return {
      viewport: viewportRect,
      boxes,
      missingRequired: requiredSelectors.filter((selector) => !document.querySelector(selector)),
      factLabelViolations,
      clippingViolations,
      targetViolations,
      typographyViolations,
      internalScrollers,
      contentOverflows,
      duplicateIds,
      orientationTruthGate,
      documentOverflow: {
        horizontal: document.documentElement.scrollWidth > innerWidth + tolerance,
        vertical: document.documentElement.scrollHeight > innerHeight + tolerance,
        scrollWidth: document.documentElement.scrollWidth,
        scrollHeight: document.documentElement.scrollHeight
      }
    };
  });

  await page.getByRole("button", { name: /How does the team arrive/i }).click();
  await page.screenshot({ path: path.join(out, `${viewport.name}-tool.png`), fullPage: false });
  const tool = await page.evaluate(() => {
    const tolerance = 1;
    const dialog = document.querySelector("dialog");
    const rectValue = (rect) => ({
      x: rect.x,
      y: rect.y,
      width: rect.width,
      height: rect.height,
      right: rect.right,
      bottom: rect.bottom
    });
    const visible = (node) => {
      const style = getComputedStyle(node);
      const rect = node.getBoundingClientRect();
      return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) !== 0 && rect.width > 0 && rect.height > 0;
    };
    const dialogRect = dialog.getBoundingClientRect();
    const viewportRect = { left: 0, top: 0, right: innerWidth, bottom: innerHeight };
    const dialogBounds = { left: dialogRect.left, top: dialogRect.top, right: dialogRect.right, bottom: dialogRect.bottom };
    const descendants = [...dialog.querySelectorAll("*")].filter(visible);
    const clippingViolations = descendants.flatMap((node, index) => {
      const rect = node.getBoundingClientRect();
      const label = `${node.tagName.toLowerCase()}[${index}]${node.id ? `#${node.id}` : ""}${node.className ? `.${String(node.className).trim().replace(/\s+/g, ".")}` : ""}`;
      const violations = [];
      for (const [against, bounds] of [["viewport", viewportRect], ["dialog", dialogBounds]]) {
        if (rect.left < bounds.left - tolerance || rect.top < bounds.top - tolerance || rect.right > bounds.right + tolerance || rect.bottom > bounds.bottom + tolerance) {
          violations.push({ label, against, rect: rectValue(rect), bounds });
        }
      }
      for (let ancestor = node.parentElement; ancestor && ancestor !== dialog; ancestor = ancestor.parentElement) {
        const style = getComputedStyle(ancestor);
        const clipsX = /(hidden|clip|auto|scroll)/.test(style.overflowX);
        const clipsY = /(hidden|clip|auto|scroll)/.test(style.overflowY);
        if (!clipsX && !clipsY) continue;
        const ancestorRect = ancestor.getBoundingClientRect();
        const bounds = {
          left: ancestorRect.left + ancestor.clientLeft,
          top: ancestorRect.top + ancestor.clientTop,
          right: ancestorRect.left + ancestor.clientLeft + ancestor.clientWidth,
          bottom: ancestorRect.top + ancestor.clientTop + ancestor.clientHeight
        };
        if ((clipsX && (rect.left < bounds.left - tolerance || rect.right > bounds.right + tolerance)) || (clipsY && (rect.top < bounds.top - tolerance || rect.bottom > bounds.bottom + tolerance))) {
          violations.push({ label, against: ancestor.className || ancestor.id || ancestor.tagName, rect: rectValue(rect), bounds });
        }
      }
      return violations;
    });
    const controls = [...dialog.querySelectorAll("button,select,input,a[href]")].filter(visible);
    const targetViolations = controls
      .map((node) => ({ label: node.id || node.getAttribute("aria-label") || node.textContent.trim().slice(0, 60), rect: rectValue(node.getBoundingClientRect()) }))
      .filter(({ rect }) => rect.width < 44 - tolerance || rect.height < 44 - tolerance);
    const typographySelectors = [".tool-head h2", ".tool-card h3", ".tool-card p", ".tool-card button", ".basket"];
    const typographyViolations = typographySelectors
      .flatMap((selector) => [...dialog.querySelectorAll(selector)].filter(visible).map((node) => ({
        label: selector,
        text: node.textContent.trim().slice(0, 80),
        fontSize: Number.parseFloat(getComputedStyle(node).fontSize)
      })))
      .filter(({ fontSize }) => !Number.isFinite(fontSize) || fontSize < 12);
    const internalScrollers = descendants.filter((node) => {
      const style = getComputedStyle(node);
      return /(auto|scroll)/.test(`${style.overflowX} ${style.overflowY}`) &&
        (node.scrollHeight > node.clientHeight + tolerance || node.scrollWidth > node.clientWidth + tolerance);
    }).map((node) => node.className || node.id || node.tagName);
    const overflowContainers = [dialog, ...dialog.querySelectorAll(".tool-head,.tool-body,.tool-layout,.tool-visual,.tool-panel,.tabs,.tool-card,.basket")].filter(visible);
    const contentOverflows = overflowContainers
      .filter((node) => node.scrollHeight > node.clientHeight + tolerance || node.scrollWidth > node.clientWidth + tolerance)
      .map((node) => ({
        label: node.className || node.id || node.tagName,
        client: { width: node.clientWidth, height: node.clientHeight },
        scroll: { width: node.scrollWidth, height: node.scrollHeight }
      }));
    const duplicateIds = [...document.querySelectorAll("[id]")]
      .map((node) => node.id)
      .filter((id, index, all) => all.indexOf(id) !== index);
    const requiredSelectors = [
      ".tool-head", "#closeTool", "#toolContext", "#toolTitle", ".tool-body", ".tool-layout",
      ".tool-visual", ".tool-panel", ".tabs", ".tabs button", ".tool-card", ".tool-card h3",
      ".tool-card p", ".tool-card button", ".basket", ".basket span", ".basket button"
    ];
    const geometry = Object.fromEntries([".tool-head", ".tool-body", ".tool-layout", ".tool-visual", ".tool-panel", ".tabs", ".tool-card", ".tool-card button", ".basket", ".basket button"].map((selector) => {
      const nodes = [...dialog.querySelectorAll(selector)].filter(visible);
      return [selector, nodes.map((node) => rectValue(node.getBoundingClientRect()))];
    }));
    return {
      open: dialog.open,
      rect: rectValue(dialogRect),
      geometry,
      missingRequired: requiredSelectors.filter((selector) => !dialog.querySelector(selector)),
      bodyOverflow: getComputedStyle(document.body).overflow,
      clippingViolations,
      targetViolations,
      typographyViolations,
      internalScrollers,
      contentOverflows,
      duplicateIds,
      documentOverflow: {
        horizontal: document.documentElement.scrollWidth > innerWidth + tolerance,
        vertical: document.documentElement.scrollHeight > innerHeight + tolerance,
        scrollWidth: document.documentElement.scrollWidth,
        scrollHeight: document.documentElement.scrollHeight
      }
    };
  });
  await page.locator("#closeTool").click();

  const decisionPassed = !decision.missingRequired.length && !decision.clippingViolations.length &&
    !decision.factLabelViolations.length && !decision.targetViolations.length && !decision.typographyViolations.length && !decision.internalScrollers.length && !decision.contentOverflows.length &&
    !decision.duplicateIds.length && decision.orientationTruthGate.passed && !decision.documentOverflow.horizontal && !decision.documentOverflow.vertical;
  const toolPassed = tool.open && !tool.missingRequired.length && !tool.clippingViolations.length &&
    !tool.targetViolations.length && !tool.typographyViolations.length && !tool.internalScrollers.length && !tool.contentOverflows.length &&
    !tool.duplicateIds.length && !tool.documentOverflow.horizontal && !tool.documentOverflow.vertical;
  results.push({ viewport, decision, tool, errors, passed: decisionPassed && toolPassed && !errors.length });
  await page.close();
}

await browser.close();
const passed = results.every((row) => row.passed);
await fs.writeFile(path.join(here, "wireframe-qa.json"), JSON.stringify({ generatedAt: new Date().toISOString(), passed, results }, null, 2) + "\n");
console.log(JSON.stringify({ viewports: results.length, passed, failures: results.filter((row) => !row.passed).map((row) => row.viewport.name) }));
if (!passed) process.exitCode = 1;
