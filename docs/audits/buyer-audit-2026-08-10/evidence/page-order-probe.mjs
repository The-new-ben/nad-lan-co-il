import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const OUT = path.dirname(fileURLToPath(import.meta.url));
const pages = [
  ["toha2", "https://nad-lan.co.il/projects/toha2-tel-aviv/"],
  ["park", "https://nad-lan.co.il/projects/the-park-bnei-brak/"],
];
const browser = await chromium.launch({ headless: true });
const results = [];
for (const [project, url] of pages) {
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await context.newPage();
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 120000 });
  await page.waitForTimeout(2500);
  const data = await page.evaluate(() => {
    const y = (el) => el ? Math.round(el.getBoundingClientRect().top + scrollY) : null;
    const desc = (el) => el ? `${el.tagName.toLowerCase()}${el.id ? `#${el.id}` : ""}${el.className && typeof el.className === "string" ? `.${el.className.trim().replace(/\s+/g, ".")}` : ""}` : null;
    const headings = [...document.querySelectorAll("h1,h2,h3,h4,h5,h6")].map((el) => ({
      level: el.tagName,
      text: el.innerText.replace(/\s+/g, " ").trim(),
      y: y(el),
      parent: desc(el.parentElement),
      ancestor: desc(el.closest("main,article,section,footer,#page,.site")),
    }));
    const landmarks = [...document.querySelectorAll("header,nav,main,article,aside,footer,[role='main'],[role='navigation'],[role='contentinfo']")].map((el) => ({
      node: desc(el), role: el.getAttribute("role"), ariaLabel: el.getAttribute("aria-label"), y: y(el), height: Math.round(el.getBoundingClientRect().height),
    }));
    const forms = [...document.forms].map((el) => ({ id: el.id, className: el.className, y: y(el), text: el.innerText.replace(/\s+/g, " ").trim().slice(0, 300) }));
    return {
      height: document.documentElement.scrollHeight,
      title: document.title,
      theaterY: y(document.querySelector("#nl-root")),
      inventoryY: y(document.querySelector(".nl-inventory")),
      firstFooterY: y(document.querySelector("footer")),
      headings,
      landmarks,
      forms,
      skipLinks: [...document.querySelectorAll("a[href^='#']")].map((a) => ({ text: a.innerText.trim(), href: a.getAttribute("href"), y: y(a) })).filter((a) => a.text),
      sticky: [...document.querySelectorAll("#nl-sticky,.nl-sticky,[class*='sticky']")].map((el) => ({ node: desc(el), text: el.innerText.replace(/\s+/g, " ").trim().slice(0, 500), y: y(el) })),
    };
  });
  results.push({ project, url, ...data });
  await context.close();
}
await browser.close();
const out = path.join(OUT, "page-order-probe.json");
fs.writeFileSync(out, JSON.stringify({ generatedAt: new Date().toISOString(), results }, null, 2), "utf8");
for (const result of results) {
  console.log(JSON.stringify({
    project: result.project,
    height: result.height,
    theaterY: result.theaterY,
    inventoryY: result.inventoryY,
    firstFooterY: result.firstFooterY,
    headings: result.headings.map((h) => ({ level: h.level, y: h.y, text: h.text.slice(0, 120) })),
    forms: result.forms,
  }, null, 2));
}
