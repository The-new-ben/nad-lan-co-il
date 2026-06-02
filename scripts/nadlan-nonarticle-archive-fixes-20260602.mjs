import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const apply = process.argv.includes("--apply");
const domain = "nad-lan.co.il";
const wpApi = "C:\\Users\\pro\\Documents\\websites\\tools\\wp-api.ps1";
const base = "https://nad-lan.co.il";

const archiveTemplates = [
  {
    slug: "archive-nadlan_professional",
    title: "Professionals Archive",
    heading: "אנשי מקצוע בנדל״ן",
    kicker: "בחירה מסודרת לפני עסקה גדולה",
    intro:
      "בעסקת נדל״ן יש שלבים שבהם עורך דין, שמאי, יועץ משכנתאות, מתווך, מהנדס או אדריכל יכולים לשנות את איכות ההחלטה. כאן אפשר להתחיל מסינון מסודר לפי תחום ועיר, לקרוא כרטיסי מידע ולבדוק אילו שאלות לשאול לפני התקשרות.",
    trust:
      "לפני בחירת איש מקצוע כדאי לבדוק ניסיון בעסקאות דומות, רישוי כאשר נדרש, הצעת מחיר כתובה, זמינות ומסמכים. הכרטיסים באתר מיועדים להשוואה ראשונית ואינם מחליפים בדיקה עצמאית.",
    links: [
      ["מדריך בחירת אנשי מקצוע", "/real-estate-professionals-guide/"],
      ["עורך דין מקרקעין", "/real-estate-lawyer/"],
      ["שמאי מקרקעין", "/real-estate-appraiser/"],
      ["בדק בית", "/home-inspection/"],
    ],
  },
  {
    slug: "archive-nadlan_project",
    title: "Projects Archive",
    heading: "פרויקטים חדשים והתחדשות עירונית",
    kicker: "בדיקת פרויקט לפני פנייה ליזם או קבלן",
    intro:
      "רכישה מקבלן, תמ״א, פינוי בינוי ופרויקט חדש דורשים בדיקה שונה מדירה יד שנייה. בעמוד הזה מרכזים כרטיסי פרויקטים כדי להשוות מיקום, סטטוס, סוג פרויקט, פרטי יזם ומידע בסיסי לפני שממשיכים לבדיקה משפטית, פיננסית ותכנונית.",
    trust:
      "כרטיס פרויקט הוא נקודת פתיחה בלבד. לפני חתימה יש לבדוק היתר, בטוחות, מפרט, לוח תשלומים, מועד מסירה, רישום זכויות וחוזה מכר עם אנשי מקצוע מתאימים.",
    links: [
      ["דירה מקבלן", "/new-projects/"],
      ["התחדשות עירונית", "/urban-renewal/"],
      ["חוק המכר", "/tax-legal/sale-of-apartments-law/"],
      ["בחירת יזם", "/urban-renewal/choosing-urban-renewal-developer/"],
    ],
  },
  {
    slug: "archive-nadlan_property",
    title: "Properties Archive",
    heading: "מאגר נכסים להשוואה ראשונית",
    kicker: "בודקים מחיר, אזור ופרטי נכס לפני החלטה",
    intro:
      "מאגר נכסים טוב עוזר להבין טווחי מחיר, סוגי דירות, אזורי ביקוש ונקודות בדיקה לפני פנייה. המטרה כאן היא לתת שכבת השוואה ראשונית, עם קישורים למדריכי קנייה, מכירה, משכנתא ושווי דירה כדי שהבדיקה לא תישאר רק ברמת מודעה.",
    trust:
      "מחיר מבוקש אינו תמיד מחיר עסקה. לפני החלטה כדאי להשוות עסקאות רשומות, מצב נכס, זכויות, הוצאות נלוות, מסים ואפשרויות מימון.",
    links: [
      ["קניית דירה", "/buying-apartment/"],
      ["הערכת שווי דירה", "/property-value/"],
      ["מחשבון משכנתא", "/mortgage-calculator/"],
      ["עלויות רכישה", "/apartment-purchase-cost-calculator/"],
    ],
  },
  {
    slug: "archive-nadlan_term",
    title: "Glossary Archive",
    heading: "מילון נדל״ן ומושגים חשובים",
    kicker: "הסברים קצרים למונחים שמופיעים בעסקאות",
    intro:
      "מונחי נדל״ן, מימון, רישום ומיסוי חוזרים כמעט בכל עסקה. המילון מרכז מושגים כדי לעזור להבין מסמכים, שאלות מקצועיות והבדלים בין נושאים כמו טאבו, הערת אזהרה, מס רכישה, היטל השבחה, בטוחות, תשריט וזכויות בנייה.",
    trust:
      "המילון נועד להסבר כללי. כאשר מושג משפיע על חוזה, מס, משכנתא או זכויות בנכס, צריך לבדוק את המסמך הספציפי ואת המקור הרשמי הרלוונטי.",
    links: [
      ["בדיקת טאבו", "/tabu-extract-check/"],
      ["מס רכישה", "/purchase-tax-calculator/"],
      ["מיסוי מקרקעין", "/real-estate-tax-advisor/"],
      ["קניית דירה", "/buying-apartment/"],
    ],
  },
];

function psQuote(value) {
  return `'${String(value).replace(/'/g, "''")}'`;
}

function runWp(route, method = "GET", body = undefined) {
  let dir;
  let bodyPath;
  if (body !== undefined) {
    dir = mkdtempSync(join(tmpdir(), "nadlan-wp-body-"));
    bodyPath = join(dir, "body.json");
    writeFileSync(bodyPath, JSON.stringify(body), "utf8");
  }

  const command = [
    "&",
    psQuote(wpApi),
    "-Domain",
    psQuote(domain),
    "-Route",
    psQuote(route),
    "-Method",
    psQuote(method),
    bodyPath ? `-BodyPath ${psQuote(bodyPath)}` : "",
    "| ConvertTo-Json -Depth 100 -Compress",
  ].filter(Boolean).join(" ");

  const result = spawnSync("powershell.exe", [
    "-NoProfile",
    "-ExecutionPolicy",
    "Bypass",
    "-Command",
    command,
  ], {
    encoding: "utf8",
    maxBuffer: 1024 * 1024 * 24,
  });

  if (dir) rmSync(dir, { recursive: true, force: true });
  if (result.status !== 0) {
    throw new Error(`wp-api failed for ${route}: ${result.stderr || result.stdout}`);
  }

  const out = result.stdout.trim();
  if (!out) return null;
  const parsed = JSON.parse(out);
  if (parsed && Array.isArray(parsed.value) && Number.isInteger(parsed.Count)) {
    return parsed.value;
  }
  return parsed;
}

function htmlLinks(links) {
  return links
    .map(([label, href]) => `<a href="${href}">${label}</a>`)
    .join("");
}

function archiveContent(item) {
  return `<!-- wp:template-part {"slug":"header","theme":"nadlan-revenue"} /-->

<!-- wp:group {"tagName":"main","className":"nl-archive-hub","style":{"spacing":{"margin":{"top":"0"},"padding":{"top":"var:preset|spacing|50","bottom":"var:preset|spacing|60","right":"var:preset|spacing|40","left":"var:preset|spacing|40"}}},"layout":{"type":"constrained","contentSize":"1120px"}} -->
<main class="wp-block-group nl-archive-hub" style="margin-top:0;padding-top:var(--wp--preset--spacing--50);padding-right:var(--wp--preset--spacing--40);padding-bottom:var(--wp--preset--spacing--60);padding-left:var(--wp--preset--spacing--40)">
<!-- wp:html -->
<style>
.nl-archive-hub{direction:rtl}
.nl-archive-hero{border:1px solid rgba(27,26,23,.12);background:#FAF7F1;padding:28px 30px;margin:0 auto 26px;box-shadow:0 16px 40px rgba(27,26,23,.06)}
.nl-archive-hero .kicker{display:inline-block;font-size:13px;font-weight:700;color:#9C7A3C;margin-bottom:10px}
.nl-archive-hero h1{font-size:clamp(34px,5vw,58px);line-height:1.04;margin:0 0 14px;color:#1B1A17;font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-weight:500}
.nl-archive-hero p{max-width:820px;font-size:18px;line-height:1.8;color:#2E332F;margin:0 0 14px}
.nl-archive-links{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.nl-archive-links a{display:inline-flex;align-items:center;min-height:38px;padding:8px 13px;border:1px solid rgba(27,26,23,.14);background:#fff;color:#1B1A17;text-decoration:none;font-size:14px}
.nl-archive-links a:hover{border-color:#9C7A3C;color:#9C7A3C}
.nl-card{border:1px solid rgba(27,26,23,.10);background:#fff;padding:18px;min-height:145px;box-shadow:0 10px 24px rgba(27,26,23,.04)}
.nl-card h2,.nl-card h3{font-family:var(--font-sans,Heebo,sans-serif);font-size:20px;line-height:1.35;margin:0 0 8px}
.nl-card p{font-size:15px;line-height:1.7;color:#3f4641}
.nl-archive-note{border-inline-start:3px solid #9C7A3C;background:#fff;padding:14px 18px;margin:18px 0 26px;color:#3f3420;font-size:15px;line-height:1.75}
.nl-archive-hub .wp-block-query-pagination{margin-top:28px}
@media(max-width:720px){.nl-archive-hero{padding:22px 18px}.nl-archive-hero p{font-size:16px}.nl-archive-links a{font-size:13px}}
</style>
<section class="nl-archive-hero" aria-label="${item.heading}">
  <span class="kicker">${item.kicker}</span>
  <h1>${item.heading}</h1>
  <p>${item.intro}</p>
  <div class="nl-archive-links">${htmlLinks(item.links)}</div>
</section>
<div class="nl-archive-note">${item.trust}</div>
<!-- /wp:html -->

<!-- wp:query {"query":{"perPage":12,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","author":"","search":"","exclude":[],"sticky":"","inherit":true},"align":"wide","layout":{"type":"default"}} -->
<div class="wp-block-query alignwide">
<!-- wp:post-template {"layout":{"type":"grid","columnCount":3}} -->
<!-- wp:group {"className":"nl-card","layout":{"type":"constrained"}} -->
<div class="wp-block-group nl-card">
<!-- wp:post-title {"isLink":true,"level":2} /-->
<!-- wp:post-excerpt {"moreText":"","excerptLength":30} /-->
</div>
<!-- /wp:group -->
<!-- /wp:post-template -->

<!-- wp:query-pagination {"paginationArrow":"arrow","layout":{"type":"flex","justifyContent":"space-between","flexWrap":"wrap"}} -->
<!-- wp:query-pagination-previous {"label":"עמוד קודם"} /-->
<!-- wp:query-pagination-numbers /-->
<!-- wp:query-pagination-next {"label":"עמוד הבא"} /-->
<!-- /wp:query-pagination -->

<!-- wp:query-no-results -->
<!-- wp:paragraph -->
<p>לא נמצאו תוצאות להצגה כרגע. אפשר לחזור לעמודי המדריכים או לשנות סינון.</p>
<!-- /wp:paragraph -->
<!-- /wp:query-no-results -->
</div>
<!-- /wp:query -->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","theme":"nadlan-revenue"} /-->`;
}

async function inspectUrl(url) {
  const res = await fetch(url, {
    headers: { "User-Agent": "Codex-Nadlan-Archive-Fixes/2026-06-02" },
  });
  const html = await res.text();
  const text = html
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  const h1 = [...html.matchAll(/<h1\b[^>]*>([\s\S]*?)<\/h1>/gi)]
    .map((m) => m[1].replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim());
  const title = (html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || "";
  const canonical = (html.match(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)/i) || [])[1] || "";
  const robots = (html.match(/<meta[^>]+name=["']robots["'][^>]+content=["']([^"']+)/i) || [])[1] || "";
  return {
    url,
    status: res.status,
    title: title.trim(),
    viewport: /<meta[^>]+name=["']viewport["']/i.test(html),
    canonical,
    robots,
    h1Count: h1.length,
    h1,
    words: text.split(/\s+/).filter(Boolean).length,
    hasArchiveText: /ארכיון|Archive|NadLan Professionals|NadLan Projects|NadLan Properties/.test(text + title),
    hasInternalTerms: ["SEO", "CRM", "lead", "money page", "supplier", "Lovable", "ChatGPT", "Gemini", "Codex"].filter((term) => text.includes(term)),
  };
}

async function main() {
  const report = {
    mode: apply ? "apply" : "dry-run",
    timestamp: new Date().toISOString(),
    professionalsGuide: null,
    templates: [],
    verification: [],
  };

  const professionalsPages = runWp("/wp-json/wp/v2/pages?slug=professionals&_fields=id,slug,link,title,status");
  if (professionalsPages.length) {
    const page = professionalsPages[0];
    report.professionalsGuide = {
      before: page,
      action: "rename hidden page slug to real-estate-professionals-guide",
      changed: apply,
    };
    if (apply) {
      const updated = runWp(`/wp-json/wp/v2/pages/${page.id}`, "POST", {
        slug: "real-estate-professionals-guide",
      });
      report.professionalsGuide.after = {
        id: updated.id,
        slug: updated.slug,
        link: updated.link,
        status: updated.status,
      };
    }
  }

  for (const item of archiveTemplates) {
    const existing = runWp(`/wp-json/wp/v2/templates/lookup?slug=${encodeURIComponent(item.slug)}&template_prefix=wp_template`);
    const lookupId = existing?.id || null;
    const body = {
      slug: item.slug,
      theme: "nadlan-revenue",
      type: "wp_template",
      title: item.title,
      status: "publish",
      content: archiveContent(item),
    };
    report.templates.push({
      slug: item.slug,
      lookupId,
      lookupSource: existing?.source || null,
      action: lookupId && lookupId !== "nadlan-revenue//index" ? "update" : "create",
      changed: apply,
    });
    if (apply) {
      if (lookupId && lookupId !== "nadlan-revenue//index") {
        runWp(`/wp-json/wp/v2/templates/${encodeURIComponent(lookupId)}`, "POST", body);
      } else {
        runWp("/wp-json/wp/v2/templates", "POST", body);
      }
    }
  }

  for (const url of [
    `${base}/professionals/`,
    `${base}/projects/`,
    `${base}/properties/`,
    `${base}/glossary/`,
    `${base}/real-estate-professionals-guide/`,
  ]) {
    report.verification.push(await inspectUrl(url));
  }

  console.log(JSON.stringify(report, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
