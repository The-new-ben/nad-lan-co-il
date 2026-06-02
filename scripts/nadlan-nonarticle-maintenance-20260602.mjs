import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const apply = process.argv.includes("--apply");
const domain = "nad-lan.co.il";
const wpApi = "C:\\Users\\pro\\Documents\\websites\\tools\\wp-api.ps1";
const report = {
  mode: apply ? "apply" : "dry-run",
  timestamp: new Date().toISOString(),
  nav: { updated: false, id: 4 },
  excerpts: [],
};

function runWp(route, method = "GET", body = undefined) {
  const psQuote = (value) => `'${String(value).replace(/'/g, "''")}'`;

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
    maxBuffer: 1024 * 1024 * 12,
  });

  if (dir) rmSync(dir, { recursive: true, force: true });
  if (result.status !== 0) {
    throw new Error(`wp-api failed for ${route}: ${result.stderr || result.stdout}`);
  }

  const out = result.stdout.trim();
  if (!out) return null;
  try {
    const parsed = JSON.parse(out);
    if (parsed && Array.isArray(parsed.value) && Number.isInteger(parsed.Count)) {
      return parsed.value;
    }
    return parsed;
  } catch {
    return out;
  }
}

function decodeEntities(value) {
  return String(value || "")
    .replace(/&hellip;/g, "...")
    .replace(/&#8211;/g, "-")
    .replace(/&quot;/g, '"')
    .replace(/&#8220;|&#8221;/g, '"')
    .replace(/&#8217;/g, "'")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">");
}

function stripHtml(value) {
  return decodeEntities(value)
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function cleanExcerptFromContent(page) {
  const title = stripHtml(page?.title?.rendered || "");
  const customExcerpts = {
    "store-for-rent": "מדריך לבעלי עסקים ושוכרים: איך בודקים חוזה שכירות לחנות, מיקום, שילוט, בלעדיות, דמי ניהול וביטחונות לפני חתימה.",
    "office-for-rent": "מדריך לשוכרי משרד: מה חשוב לבדוק בחוזה שכירות מסחרי, עלויות נלוות, ביטחונות, תקופת שכירות, התאמות ומועד יציאה.",
    "new-vs-second-hand": "מדריך לרוכשי דירה: איך משווים דירה חדשה מקבלן מול דירה יד שנייה לפי מחיר, מועד כניסה, אחריות, מימון וסיכון.",
    "buying-apartment-step-by-step": "מדריך שלב אחר שלב לקניית דירה: תקציב, משכנתא, בדיקת זכויות, מצב הנכס, חוזה, מסים ולוח זמנים לפני חתימה.",
    "airbnb-israel-regulation": "מדריך לבעלי דירות ומשקיעים: מה לבדוק לפני השכרה לטווח קצר בישראל, שימוש חורג, רישוי, מיסוי, שכנים וסיכון משפטי.",
    "real-estate-leverage": "מדריך למשקיעים: איך בודקים מינוף בנדל\"ן, יחס מימון, תשואה על ההון, החזר חודשי, ריבית וסיכון לפני רכישת נכס.",
    "investment-via-company": "מדריך למשקיעי נדל\"ן: איך משווים השקעה פרטית מול השקעה דרך חברה בע\"מ לפי מס, מימון, ניהול, סיכון ועלויות.",
    "reduced-capital-gains-sale": "מדריך למוכרי דירה: איך בודקים מס שבח, חישוב לינארי מוטב, יום המעבר 2014, פטורים, הוצאות ומסמכים לפני מכירה.",
    "pricing-apartment-for-sale": "מדריך למוכרי דירה: איך מתמחרים נכס לפי עסקאות דומות, מצב הדירה, שכונה, תזמון, משא ומתן ועלויות מכירה.",
    "selling-without-broker": "מדריך למוכר העצמאי: איך מוכרים דירה בלי מתווך, מה להכין לפרסום, איך מנהלים ביקורים ומשא ומתן ומתי לערב עורך דין.",
    "who-pays-broker-fees": "מדריך לקונים, מוכרים ושוכרים: מי משלם דמי תיווך, מתי נוצרת זכאות לתשלום, מה כתוב בהזמנת שירות ומה חשוב לבדוק לפני חתימה.",
    "when-real-estate-lawyer-required": "מדריך לקונים ומוכרים: מתי פונים לעורך דין מקרקעין, אילו בדיקות משפטיות נדרשות ומה להכין לפני חתימה על חוזה.",
    "building-permit-citizen-guide": "מדריך לבעלי נכסים ומשפצים: מתי צריך היתר בנייה, איך עובד רישוי זמין, מה נחשב חריגה ומה בודקים לפני עבודה.",
    "form-4-occupancy-permit": "מדריך לרוכשי דירה חדשה: מהו טופס 4, למה הוא חשוב לאכלוס, אילו מסמכים לבדוק ומה לשאול לפני מסירה.",
    "option-period-real-estate": "מדריך לעסקאות אופציה במקרקעין: מהי תקופת אופציה, מה בודקים בחוזה, אילו סיכונים קיימים ואיך מתכוננים למימוש.",
    "sale-of-apartments-law": "מדריך לרוכשי דירה מקבלן: מה כולל חוק המכר דירות, אחריות ובדק, ערבויות, פיצוי על איחור ומה חשוב לבדוק בחוזה.",
    "choosing-urban-renewal-developer": "מדריך לדיירים: איך בוחרים יזם להתחדשות עירונית, מה בודקים במכרז, ערבויות, ניסיון, שקיפות וליווי משפטי.",
    "tama-38-contract-checklist": "מדריך לדיירים לפני חתימה על חוזה תמא 38: ערבויות, לוחות זמנים, ליווי בנקאי, תמורות, פינוי וסעיפי הגנה.",
    "pinui-binui-tenant-guide": "מדריך לדיירים בפינוי בינוי: מה בודקים לפני הסכמה, איך בוחרים יזם ונציגות, מה חשוב בחוזה ואילו ערבויות לבקש.",
    "tama-38-rights-obligations": "מדריך לבעלי דירות: מה מצב תמא 38 בשנת 2026, אילו חלופות קיימות, מהן זכויות הדיירים ומה לבדוק לפני החלטה.",
    "mortgage-repayment-capacity": "מדריך לרוכשי דירה: איך בודקים כושר החזר משכנתא, יחס החזר מהכנסה, רגישות לריבית ויכולת תשלום לאורך זמן.",
    "reverse-mortgage": "מדריך לבעלי דירה בגיל מבוגר: איך בודקים משכנתא הפוכה, עלויות, ריבית, ירושה, סיכונים וחלופות לפני החלטה.",
    "investment": "מדריך למשקיעים בנדל\"ן בישראל: איך בודקים תשואה, מימון, מסים, שכירות, סיכון, ניהול נכס ויציאה לפני רכישה.",
  };
  if (customExcerpts[page.slug]) return customExcerpts[page.slug];

  let text = stripHtml(page?.content?.rendered || page?.excerpt?.rendered || "");
  text = text
    .replace(/^נח\s+/u, "")
    .replace(/נכתב ונערך על ידי צוות נדל"ן חכם/u, "")
    .replace(/צוות התוכן והמחקר של נדל"ן חכם/u, "")
    .replace(/צוות נדל"ן חכםצוות התוכן והמחקר של נדל"ן חכם/u, "")
    .replace(/·?\s*עודכן:\s*2026/u, "")
    .replace(/\s+/g, " ")
    .trim();

  if (!text || text.length < 70) {
    text = `מדריך מעשי בנושא ${title}: מה חשוב לבדוק, אילו מסמכים להכין ואיך לקבל החלטה זהירה לפני חתימה.`;
  }

  const firstBreak = text.search(/[.!?؟]|[.?!]/u);
  let excerpt = firstBreak > 80 ? text.slice(0, firstBreak + 1) : text.slice(0, 220);
  excerpt = excerpt.replace(/\s+[^\s]*$/, "").trim();
  if (excerpt.length < 80) excerpt = text.slice(0, 180).replace(/\s+[^\s]*$/, "").trim();
  return excerpt;
}

function isBrokenExcerpt(page) {
  const text = stripHtml(page?.excerpt?.rendered || "");
  return (
    /^נח\s+נכתב/u.test(text) ||
    text.includes("צוות נדל\"ן חכםצוות") ||
    text.includes("נכתב ונערך על ידי צוות נדל\"ן חכםצוות")
  );
}

async function main() {
  const navHtml = [
    '<li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/buying-apartment/"><span class="wp-block-navigation-item__label">קניית דירה</span></a></li>',
    '<li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/selling-apartment/"><span class="wp-block-navigation-item__label">מכירת דירה</span></a></li>',
    '<li class="wp-block-navigation-item has-child wp-block-navigation-submenu"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/investment-apartment/"><span class="wp-block-navigation-item__label">השקעה</span></a><ul class="wp-block-navigation__submenu-container wp-block-navigation-submenu"><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/investment-apartment/"><span class="wp-block-navigation-item__label">בדיקת עסקה</span></a></li><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/investment-property-cashflow-calculator/"><span class="wp-block-navigation-item__label">מחשבון תשואה</span></a></li><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/investment-property-mortgage/"><span class="wp-block-navigation-item__label">מימון להשקעה</span></a></li><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/property-management/"><span class="wp-block-navigation-item__label">ניהול נכסים</span></a></li></ul></li>',
    '<li class="wp-block-navigation-item has-child wp-block-navigation-submenu"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/mortgage-calculator/"><span class="wp-block-navigation-item__label">משכנתא</span></a><ul class="wp-block-navigation__submenu-container wp-block-navigation-submenu"><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/mortgage-calculator/"><span class="wp-block-navigation-item__label">מחשבון משכנתא</span></a></li><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/mortgage-advisor/"><span class="wp-block-navigation-item__label">יועץ משכנתאות</span></a></li><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/mortgage-refinance/"><span class="wp-block-navigation-item__label">מחזור משכנתא</span></a></li><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/mortgage-home-insurance/"><span class="wp-block-navigation-item__label">ביטוח דירה</span></a></li></ul></li>',
    '<li class="wp-block-navigation-item has-child wp-block-navigation-submenu"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/real-estate-lawyer/"><span class="wp-block-navigation-item__label">משפט ומיסוי</span></a><ul class="wp-block-navigation__submenu-container wp-block-navigation-submenu"><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/real-estate-lawyer/"><span class="wp-block-navigation-item__label">עורך דין מקרקעין</span></a></li><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/real-estate-tax-advisor/"><span class="wp-block-navigation-item__label">מיסוי מקרקעין</span></a></li><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/purchase-tax-calculator/"><span class="wp-block-navigation-item__label">מחשבון מס רכישה</span></a></li><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/tabu-extract-check/"><span class="wp-block-navigation-item__label">בדיקת טאבו</span></a></li></ul></li>',
    '<li class="wp-block-navigation-item has-child wp-block-navigation-submenu"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/property-value-estimator/"><span class="wp-block-navigation-item__label">כלים</span></a><ul class="wp-block-navigation__submenu-container wp-block-navigation-submenu"><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/property-value-estimator/"><span class="wp-block-navigation-item__label">שווי דירה</span></a></li><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/apartment-purchase-cost-calculator/"><span class="wp-block-navigation-item__label">עלויות רכישה</span></a></li><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/property-value/"><span class="wp-block-navigation-item__label">הערכת שווי</span></a></li><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/catalog/"><span class="wp-block-navigation-item__label">קטלוג נכסים</span></a></li></ul></li>',
    '<li class="wp-block-navigation-item has-child wp-block-navigation-submenu"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/professionals/"><span class="wp-block-navigation-item__label">אנשי מקצוע</span></a><ul class="wp-block-navigation__submenu-container wp-block-navigation-submenu"><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/professionals/"><span class="wp-block-navigation-item__label">אינדקס מקצוענים</span></a></li><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/real-estate-appraiser/"><span class="wp-block-navigation-item__label">שמאי מקרקעין</span></a></li><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/home-inspection/"><span class="wp-block-navigation-item__label">בדק בית</span></a></li><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/real-estate-broker/"><span class="wp-block-navigation-item__label">מתווך נדל"ן</span></a></li><li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/join-pro/"><span class="wp-block-navigation-item__label">הצטרפו כמקצוען</span></a></li></ul></li>',
    '<li class="wp-block-navigation-item wp-block-navigation-link"><a class="wp-block-navigation-item__content" href="https://nad-lan.co.il/apartment-buying-checklist/"><span class="wp-block-navigation-item__label">בדיקת עסקה</span></a></li>',
  ].join("\n");

  const topLink = (label, url) =>
    `<!-- wp:navigation-link ${JSON.stringify({ label, url, kind: "custom", isTopLevelLink: true })} /-->`;
  const childLink = (label, url) =>
    `<!-- wp:navigation-link ${JSON.stringify({ label, url, kind: "custom" })} /-->`;
  const submenu = (label, url, children) =>
    `<!-- wp:navigation-submenu ${JSON.stringify({ label, url, kind: "custom" })} -->\n${children.join("\n")}\n<!-- /wp:navigation-submenu -->`;

  const navBlocks = [
    topLink("קניית דירה", "https://nad-lan.co.il/buying-apartment/"),
    topLink("מכירת דירה", "https://nad-lan.co.il/selling-apartment/"),
    submenu("השקעה", "https://nad-lan.co.il/investment-apartment/", [
      childLink("בדיקת עסקה", "https://nad-lan.co.il/investment-apartment/"),
      childLink("מחשבון תשואה", "https://nad-lan.co.il/investment-property-cashflow-calculator/"),
      childLink("מימון להשקעה", "https://nad-lan.co.il/investment-property-mortgage/"),
      childLink("ניהול נכסים", "https://nad-lan.co.il/property-management/"),
    ]),
    submenu("משכנתא", "https://nad-lan.co.il/mortgage-calculator/", [
      childLink("מחשבון משכנתא", "https://nad-lan.co.il/mortgage-calculator/"),
      childLink("יועץ משכנתאות", "https://nad-lan.co.il/mortgage-advisor/"),
      childLink("מחזור משכנתא", "https://nad-lan.co.il/mortgage-refinance/"),
      childLink("ביטוח דירה", "https://nad-lan.co.il/mortgage-home-insurance/"),
    ]),
    submenu("משפט ומיסוי", "https://nad-lan.co.il/real-estate-lawyer/", [
      childLink("עורך דין מקרקעין", "https://nad-lan.co.il/real-estate-lawyer/"),
      childLink("מיסוי מקרקעין", "https://nad-lan.co.il/real-estate-tax-advisor/"),
      childLink("מחשבון מס רכישה", "https://nad-lan.co.il/purchase-tax-calculator/"),
      childLink("בדיקת טאבו", "https://nad-lan.co.il/tabu-extract-check/"),
    ]),
    submenu("כלים", "https://nad-lan.co.il/property-value-estimator/", [
      childLink("שווי דירה", "https://nad-lan.co.il/property-value-estimator/"),
      childLink("עלויות רכישה", "https://nad-lan.co.il/apartment-purchase-cost-calculator/"),
      childLink("הערכת שווי", "https://nad-lan.co.il/property-value/"),
      childLink("קטלוג נכסים", "https://nad-lan.co.il/catalog/"),
    ]),
    submenu("אנשי מקצוע", "https://nad-lan.co.il/professionals/", [
      childLink("אינדקס מקצוענים", "https://nad-lan.co.il/professionals/"),
      childLink("שמאי מקרקעין", "https://nad-lan.co.il/real-estate-appraiser/"),
      childLink("בדק בית", "https://nad-lan.co.il/home-inspection/"),
      childLink("מתווך נדל\"ן", "https://nad-lan.co.il/real-estate-broker/"),
      childLink("הצטרפו כמקצוען", "https://nad-lan.co.il/join-pro/"),
    ]),
    topLink("בדיקת עסקה", "https://nad-lan.co.il/apartment-buying-checklist/"),
  ].join("\n");

  report.nav.beforeTopLevelCount = 13;
  report.nav.afterTopLevelCount = 8;
  if (apply) {
    runWp("/wp-json/wp/v2/navigation/4", "POST", { content: navBlocks });
    report.nav.updated = true;
  }

  let page = 1;
  while (true) {
    let pages;
    try {
      pages = runWp(`/wp-json/wp/v2/pages?per_page=100&page=${page}&_fields=id,link,title,slug,excerpt,content`);
    } catch (error) {
      if (page > 1 && /400/.test(String(error.message))) break;
      throw error;
    }
    if (!Array.isArray(pages) || pages.length === 0) break;
    for (const item of pages) {
      if (!isBrokenExcerpt(item)) continue;
      const before = stripHtml(item.excerpt.rendered);
      const after = cleanExcerptFromContent(item);
      report.excerpts.push({
        id: item.id,
        slug: item.slug,
        link: item.link,
        before: before.slice(0, 180),
        after,
        changed: apply,
      });
      if (apply) {
        runWp(`/wp-json/wp/v2/pages/${item.id}`, "POST", { excerpt: after });
      }
    }
    page += 1;
  }

  console.log(JSON.stringify(report, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
