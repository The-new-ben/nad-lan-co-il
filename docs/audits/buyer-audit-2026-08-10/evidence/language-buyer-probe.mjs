import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const OUT = path.dirname(fileURLToPath(import.meta.url));

const bases = [
  { key: "toha2", slug: "toha2-tel-aviv", urls: {
    he: "https://nad-lan.co.il/projects/toha2-tel-aviv/",
    en: "https://nad-lan.co.il/projects/toha2-tel-aviv-en/",
    fr: "https://nad-lan.co.il/projects/toha2-tel-aviv-fr/",
    ru: "https://nad-lan.co.il/projects/toha2-tel-aviv-ru/",
    ar: "https://nad-lan.co.il/projects/toha2-tel-aviv-ar/",
  } },
  { key: "park", slug: "the-park-bnei-brak", urls: {
    he: "https://nad-lan.co.il/projects/the-park-bnei-brak/",
    en: "https://nad-lan.co.il/projects/the-park-bnei-brak-en/",
    fr: "https://nad-lan.co.il/projects/the-park-bnei-brak-fr/",
    ru: "https://nad-lan.co.il/projects/the-park-bnei-brak-ru/",
    ar: "https://nad-lan.co.il/projects/the-park-bnei-brak-ar/",
  } },
];
const browser = await chromium.launch({ headless: true });
const results = [];
for (const base of bases) {
  for (const [locale, baseUrl] of Object.entries(base.urls)) {
    const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const page = await context.newPage();
    const url = `${baseUrl}?project=${encodeURIComponent(base.slug)}&lang=${locale}&unit=floor-20`;
    const response = await page.goto(url, { waitUntil: "domcontentloaded", timeout: 120000 });
    await page.waitForTimeout(2200);
    const data = await page.evaluate(() => {
      const clean = (text) => String(text || "").replace(/\s+/g, " ").trim();
      const text = document.body.innerText;
      const selected = document.querySelector(".nl-unit-screen,.nl-unit-summary")?.innerText || "";
      const schemaLanguages = [];
      for (const script of document.querySelectorAll("script[type='application/ld+json']")) {
        try {
          const json = JSON.parse(script.textContent);
          const queue = [json];
          while (queue.length) {
            const item = queue.shift();
            if (!item || typeof item !== "object") continue;
            if (item.inLanguage) schemaLanguages.push(item.inLanguage);
            queue.push(...(Array.isArray(item) ? item : Object.values(item)));
          }
        } catch {}
      }
      const links = [...document.querySelectorAll("a[href]")].map((a) => ({ text: clean(a.innerText), href: a.href })).filter((a) => a.text);
      return {
        statusText: document.readyState,
        htmlLang: document.documentElement.lang,
        dir: document.documentElement.dir,
        title: document.title,
        h1: clean(document.querySelector("h1")?.innerText),
        heroText: clean(document.querySelector(".nlpx-hero,.nl-hero,.entry-content")?.innerText).slice(0, 3000),
        selectedText: clean(selected).slice(0, 5000),
        selectedHebrewChars: (selected.match(/[\u0590-\u05FF]/g) || []).length,
        selectedArabicChars: (selected.match(/[\u0600-\u06FF]/g) || []).length,
        selectedCyrillicChars: (selected.match(/[\u0400-\u04FF]/g) || []).length,
        bodyHebrewChars: (text.match(/[\u0590-\u05FF]/g) || []).length,
        bodyArabicChars: (text.match(/[\u0600-\u06FF]/g) || []).length,
        bodyCyrillicChars: (text.match(/[\u0400-\u04FF]/g) || []).length,
        schemaLanguages: [...new Set(schemaLanguages.map(String))],
        languageLinks: links.filter((link) => /-(en|fr|ru|ar)\/?(?:\?|$)|\/projects\/(toha2-tel-aviv|the-park-bnei-brak)\/?(?:\?|$)/.test(link.href)).slice(0, 30),
        headerText: clean(document.querySelector("header")?.innerText).slice(0, 2000),
        footerText: clean(document.querySelector("footer:last-of-type")?.innerText).slice(0, 2000),
      };
    });
    results.push({ project: base.key, locale, url, status: response?.status() ?? null, ...data });
    console.log(`${base.key} ${locale}: ${response?.status()} ${data.htmlLang}/${data.dir}, selected Hebrew=${data.selectedHebrewChars}`);
    await context.close();
  }
}
await browser.close();
const output = path.join(OUT, "language-buyer-probe.json");
fs.writeFileSync(output, JSON.stringify({ generatedAt: new Date().toISOString(), results }, null, 2), "utf8");
console.log(output);
