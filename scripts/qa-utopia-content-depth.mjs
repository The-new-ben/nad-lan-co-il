#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const root = process.cwd();
const contentDir = path.join(root, "content", "projects", "utopia-sde-dov");
const pluginContentDir = path.join(root, "plugins", "nadlan-config", "assets", "showroom-engine", "projects", "utopia-sde-dov");
const outputPath = path.join(root, "docs", "qa", "utopia-content-depth-report.json");

const sourceUrls = [
  "https://utopiatlv.co.il/",
  "https://www.nahmias-group.co.il/project/utopia-%D7%A9%D7%93%D7%94-%D7%93%D7%91-%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91/",
  "https://www.nahmias-group.co.il/en/project/utopia/",
  "https://apps.land.gov.il/IturTabotData/takanonim/telmer/5050215.pdf",
  "https://apps.land.gov.il/IturTabotData/nispachim/telmer/5050215/20.pdf",
  "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/772/query?where=request_num%3D20250165&outFields=*&returnGeometry=false&f=pjson",
  "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/772/query?where=request_num%3D20250165&outFields=*&returnGeometry=true&outSR=4326&f=json",
  "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/772/query?where=request_num%3D20250403&outFields=*&returnGeometry=false&f=pjson",
  "https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx",
  "https://www.tel-aviv.gov.il/Residents/Development/DocLib/%D7%9E%D7%92%D7%A8%D7%A9%20103%20%D7%93%D7%99%D7%95%D7%9F%20%D7%91%D7%A2%D7%99%D7%A6%D7%95%D7%91.pdf",
  "https://utopiatlv.co.il/wp-content/uploads/2025/07/UTOPIA-N1-4A-21222-copy.pdf",
  "https://utopiatlv.co.il/wp-content/uploads/2025/07/UTOPIA-N1-5G-62-copy.pdf",
  "https://utopiatlv.co.il/wp-content/uploads/2025/07/5G-S1-204.pdf",
  "https://utopiatlv.co.il/wp-content/uploads/2025/07/3P-S18094108122136150164.pdf",
  "https://utopiatlv.co.il/wp-content/uploads/2025/07/UTOPIA-N1-3A-81828-copy.pdf",
  "https://utopiatlv.co.il/wp-content/uploads/2025/07/4D-S156708498112126140154.pdf",
  "https://utopiatlv.co.il/wp-content/uploads/2025/07/UTOPIA-N1-5E-404448525660-copy.pdf",
  "https://en.globes.co.il/news/article.aspx?did=1001526410",
  "https://www.globes.co.il/news/article.aspx?did=1001515692",
  "https://www.bizportal.co.il/realestates/news/article/20033505",
  "https://www.calcalist.co.il/article/r12n2qiowx",
  "https://www.calcalist.co.il/real-estate/article/rybd6fiz9",
  "https://www.globes.co.il/news/article.aspx?did=1001497375"
];

const internalUrls = [
  "https://nad-lan.co.il/mortgage-calculator/",
  "https://nad-lan.co.il/purchase-tax-calculator/",
  "https://nad-lan.co.il/new-projects/",
  "https://nad-lan.co.il/tel-aviv-apartment-prices/",
  "https://nad-lan.co.il/cities/%d7%aa%d7%9c-%d7%90%d7%91%d7%99%d7%91-%d7%99%d7%a4%d7%95/",
  "https://nad-lan.co.il/sde-dov/"
];

const specs = {
  he: {
    locale: "he-IL",
    dir: "rtl",
    title: "UTOPIA שדה דב תל אביב - מחירים, דירות ובחירה מהבניין",
    h2: [
      "סקירה",
      "מיקום וסביבה",
      "הבניינים והדירות",
      "מחירים ואומדנים",
      "היזם",
      "שלבי הפרויקט",
      "למי זה מתאים",
      "שאלות נפוצות",
      "מקורות"
    ],
    opening: [/UTOPIA/u, /תל אביב/u, /דירות/u, /מחיר/u, /קנייה/u],
    facts: [
      /\b337\b/u,
      /5(?:,|\s|\u202f)203/u,
      /\b34\b/u,
      /\b15\b/u,
      /\b353\b/u,
      /20250165/u,
      /20250403/u,
      /20250566/u,
      /(2025-06-18|18\s+ביוני\s+2025)/u,
      /(2025-09-14|14\s+בספטמבר\s+2025)/u
    ],
    estimate: "אומדן, לא מחייב",
    banned: ["בעידן שבו", "חשוב לציין", "לסיכום", "אין ספק"]
  },
  en: {
    locale: "en-US",
    dir: "ltr",
    title: "UTOPIA Sde Dov Tel Aviv - Apartments for Sale, Prices and Choosing a Home",
    h2: [
      "Overview",
      "Location and surroundings",
      "The buildings and apartments",
      "Prices and estimates",
      "The developer",
      "Project stages",
      "Who the project suits",
      "Frequently asked questions",
      "Sources"
    ],
    opening: [/UTOPIA/i, /Tel Aviv/i, /apartments?/i, /price/i, /(buy|purchase)/i],
    facts: [
      /\b337\b/,
      /5(?:,|\s|\u202f)203/u,
      /\b34\b/,
      /\b15\b/,
      /\b353\b/,
      /20250165/,
      /20250403/,
      /20250566/,
      /(2025-06-18|(?:June\s+18|18\s+June),?\s+2025)/i,
      /(2025-09-14|(?:September\s+14|14\s+September),?\s+2025)/i
    ],
    estimate: "estimate, non-binding",
    banned: ["in today's fast-paced world", "it is important to note", "in conclusion", "there is no doubt"]
  },
  fr: {
    locale: "fr-FR",
    dir: "ltr",
    title: "UTOPIA Sde Dov Tel Aviv - Appartements à vendre, prix et choix d'un logement",
    h2: [
      "Vue d'ensemble",
      "Emplacement et environnement",
      "Les bâtiments et les appartements",
      "Prix et estimations",
      "Le promoteur",
      "Étapes du projet",
      "À qui ce projet convient-il",
      "Questions fréquentes",
      "Sources"
    ],
    opening: [/UTOPIA/i, /Tel Aviv/i, /appartements?/i, /prix/i, /(acheter|achat)/i],
    facts: [
      /\b337\b/,
      /5(?:,|\s|\u202f)203/u,
      /\b34\b/,
      /\b15\b/,
      /\b353\b/,
      /20250165/,
      /20250403/,
      /20250566/,
      /(2025-06-18|18\s+juin\s+2025)/i,
      /(2025-09-14|14\s+septembre\s+2025)/i
    ],
    estimate: "estimation, non contractuelle",
    banned: ["il est important de noter", "en conclusion", "il ne fait aucun doute"]
  },
  ru: {
    locale: "ru-RU",
    dir: "ltr",
    title: "UTOPIA Sde Dov Тель-Авив - квартиры на продажу, цены и выбор квартиры",
    h2: [
      "Обзор",
      "Расположение и окружение",
      "Здания и квартиры",
      "Цены и оценки",
      "Девелопер",
      "Этапы проекта",
      "Кому подходит проект",
      "Частые вопросы",
      "Источники"
    ],
    opening: [/UTOPIA/i, /Тель-Авив/iu, /квартир/iu, /цен/iu, /(купить|покупк)/iu],
    facts: [
      /\b337\b/u,
      /5(?:,|\s|\u202f)203/u,
      /\b34\b/u,
      /\b15\b/u,
      /\b353\b/u,
      /20250165/u,
      /20250403/u,
      /20250566/u,
      /(2025-06-18|18\s+июня\s+2025)/iu,
      /(2025-09-14|14\s+сентября\s+2025)/iu
    ],
    estimate: "оценка, не является обязательной",
    banned: ["важно отметить", "в заключение", "нет сомнений"]
  },
  ar: {
    locale: "ar",
    dir: "rtl",
    title: "UTOPIA Sde Dov تل أبيب - شقق للبيع والأسعار واختيار الشقة",
    h2: [
      "نظرة عامة",
      "الموقع والبيئة المحيطة",
      "المباني والشقق",
      "الأسعار والتقديرات",
      "المطور",
      "مراحل المشروع",
      "لمن يناسب المشروع",
      "أسئلة شائعة",
      "المصادر"
    ],
    opening: [/UTOPIA/i, /تل أبيب/u, /شقق/u, /سعر/u, /شراء/u],
    facts: [
      /\b337\b/u,
      /5(?:,|\s|\u202f)203/u,
      /\b34\b/u,
      /\b15\b/u,
      /\b353\b/u,
      /20250165/u,
      /20250403/u,
      /20250566/u,
      /(2025-06-18|18\s+يونيو\s+2025)/u,
      /(2025-09-14|14\s+سبتمبر\s+2025)/u
    ],
    estimate: "تقدير غير ملزم",
    banned: ["من المهم ملاحظة", "في الختام", "لا شك"]
  }
};

function decodeEntities(value) {
  return value
    .replace(/&nbsp;|&#160;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&quot;/gi, "\"")
    .replace(/&#39;|&apos;/gi, "'")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">");
}

function textFromHtml(html) {
  return decodeEntities(
    html
      .replace(/<!--[\s\S]*?-->/g, " ")
      .replace(/<script\b[\s\S]*?<\/script>/gi, " ")
      .replace(/<style\b[\s\S]*?<\/style>/gi, " ")
      .replace(/<[^>]+>/g, " ")
  )
    .replace(/\s+/gu, " ")
    .trim();
}

function wordsFromText(text) {
  return text
    .replace(/https?:\/\/\S+/g, " ")
    .split(/\s+/u)
    .map((word) => word.replace(/^[\p{P}\p{S}]+|[\p{P}\p{S}]+$/gu, ""))
    .filter(Boolean);
}

function tagTexts(html, tag) {
  const matches = [];
  const re = new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)<\\/${tag}>`, "gi");
  let match;
  while ((match = re.exec(html)) !== null) matches.push(textFromHtml(match[1]));
  return matches;
}

function hrefs(html) {
  return [...html.matchAll(/<a\b[^>]*\bhref=(?:"([^"]+)"|'([^']+)')[^>]*>/gi)]
    .map((match) => decodeEntities(match[1] || match[2]));
}

function sectionAfterFinalH2(html, expectedTitle) {
  const re = /<h2\b[^>]*>([\s\S]*?)<\/h2>/gi;
  let match;
  let start = -1;
  while ((match = re.exec(html)) !== null) {
    if (textFromHtml(match[1]) === expectedTitle) start = re.lastIndex;
  }
  return start >= 0 ? html.slice(start) : "";
}

function inspect(lang, spec) {
  const file = path.join(contentDir, `article-${lang}.html`);
  const errors = [];
  if (!fs.existsSync(file)) {
    return { lang, file: path.relative(root, file), errors: ["missing file"], pass: false };
  }

  const html = fs.readFileSync(file, "utf8");
  const pluginFile = path.join(pluginContentDir, `article-${lang}.html`);
  const contentSha256 = crypto.createHash("sha256").update(html).digest("hex");
  let pluginSha256 = "";
  if (!fs.existsSync(pluginFile)) {
    errors.push("missing plugin article copy");
  } else {
    const pluginHtml = fs.readFileSync(pluginFile, "utf8");
    pluginSha256 = crypto.createHash("sha256").update(pluginHtml).digest("hex");
    if (pluginHtml !== html) errors.push("plugin article copy differs from the reviewed content file");
  }
  const fullText = textFromHtml(html);
  const words = wordsFromText(fullText);
  const h1s = tagTexts(html, "h1");
  const h2s = tagTexts(html, "h2");
  const article = html.match(/<article\b([^>]*)>/i);
  const firstP = html.match(/<p\b[^>]*>([\s\S]*?)<\/p>/i);
  const openingWords = wordsFromText(firstP ? textFromHtml(firstP[1]) : "").slice(0, 150);
  const openingText = openingWords.join(" ");

  if (words.length < 5000) errors.push(`word count ${words.length} is below 5000`);
  if (h1s.length !== 1) errors.push(`expected one H1, found ${h1s.length}`);
  if (h1s[0] !== spec.title) errors.push(`H1 mismatch: ${JSON.stringify(h1s[0] || "")}`);
  if (!article) {
    errors.push("missing article element");
  } else {
    const attrs = article[1];
    if (!new RegExp(`\\blang=["']${spec.locale}["']`, "i").test(attrs)) errors.push(`article lang must be ${spec.locale}`);
    if (!new RegExp(`\\bdir=["']${spec.dir}["']`, "i").test(attrs)) errors.push(`article dir must be ${spec.dir}`);
  }
  if (!firstP) errors.push("missing opening paragraph");
  if (openingWords.length > 150) errors.push("opening paragraph extraction exceeded 150 words");
  for (const pattern of spec.opening) {
    if (!pattern.test(openingText)) errors.push(`opening paragraph misses ${pattern}`);
  }
  for (const heading of spec.h2) {
    if (!h2s.includes(heading)) errors.push(`missing required H2: ${heading}`);
  }
  const ordered = spec.h2.map((heading) => h2s.indexOf(heading));
  if (ordered.some((index) => index < 0) || ordered.some((index, i) => i > 0 && index <= ordered[i - 1])) {
    errors.push("required H2 chapters are not in the locked order");
  }
  for (const url of internalUrls) {
    if (!html.includes(`href="${url}"`) && !html.includes(`href='${url}'`)) errors.push(`missing internal link: ${url}`);
  }
  for (const factPattern of spec.facts) {
    if (!factPattern.test(fullText)) errors.push(`missing locked factual pattern: ${factPattern}`);
  }
  if (!fullText.includes(spec.estimate)) errors.push(`missing required estimate label: ${spec.estimate}`);
  if (/[\u2010\u2011\u2012\u2013\u2014\u2015\u2212]/u.test(html)) errors.push("contains a non-ASCII dash");
  for (const phrase of spec.banned) {
    if (fullText.toLocaleLowerCase().includes(phrase.toLocaleLowerCase())) errors.push(`contains banned phrase: ${phrase}`);
  }

  const publicText = fullText.slice(0, Math.max(0, fullText.lastIndexOf(spec.h2.at(-1))));
  for (const signal of [/\bSEO\b/i, /\bsearch intent\b/i, /\bkeyword(?:s)?\b/i, /\bAI-generated\b/i, /source ledger/i]) {
    if (signal.test(publicText)) errors.push(`contains internal-facing language: ${signal}`);
  }

  const sourceSection = sectionAfterFinalH2(html, spec.h2.at(-1));
  const sourceSet = new Set(hrefs(sourceSection));
  const expectedSet = new Set(sourceUrls);
  const missingSources = sourceUrls.filter((url) => !sourceSet.has(url));
  const extraSources = [...sourceSet].filter((url) => !expectedSet.has(url));
  if (missingSources.length) errors.push(`missing source links: ${missingSources.join(", ")}`);
  if (extraSources.length) errors.push(`unexpected links in Sources chapter: ${extraSources.join(", ")}`);

  return {
    lang,
    file: path.relative(root, file).replaceAll("\\", "/"),
    word_count: words.length,
    h1: h1s,
    h2_count: h2s.length,
    opening_word_count: openingWords.length,
    source_link_count: sourceSet.size,
    internal_link_count: internalUrls.filter((url) => html.includes(url)).length,
    content_sha256: contentSha256,
    plugin_sha256: pluginSha256,
    plugin_copy_match: pluginSha256 === contentSha256,
    errors,
    pass: errors.length === 0
  };
}

const results = Object.entries(specs).map(([lang, spec]) => inspect(lang, spec));
const report = {
  schema: "nadlan-utopia-content-depth/v1",
  generated_at: new Date().toISOString(),
  threshold_words_per_language: 5000,
  source_link_contract_count: sourceUrls.length,
  languages: results,
  pass: results.every((result) => result.pass)
};

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(JSON.stringify(report, null, 2));
process.exit(report.pass ? 0 : 1);
