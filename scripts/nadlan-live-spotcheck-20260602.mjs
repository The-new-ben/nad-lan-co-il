const homepage = await fetch("https://nad-lan.co.il/");
const homepageHtml = await homepage.text();

const currentHeaderLabels = [
  "קניית דירה",
  "מכירת דירה",
  "השקעה",
  "משכנתא",
  "משפט ומיסוי",
  "כלים",
  "אנשי מקצוע",
  "בדיקת עסקה",
];

const oldHeaderLabels = [
  "Airbnb בחו״ל",
  "התחדשות עירונית",
  "דירה מקבלן",
  "נדל\"ן להשקעה",
];

const pageUrls = [
  "https://nad-lan.co.il/commercial-real-estate/store-for-rent/",
  "https://nad-lan.co.il/investment/",
  "https://nad-lan.co.il/urban-renewal/tama-38-rights-obligations/",
];

const pages = [];
for (const url of pageUrls) {
  const res = await fetch(url);
  const html = await res.text();
  pages.push({
    url,
    status: res.status,
    h1Count: [...html.matchAll(/<h1\b/gi)].length,
    brokenPrefixVisible: html.includes("נח נכתב"),
    internalTerms: ["SEO", "CRM", "לידים", "ספקים"].filter((term) => html.includes(term)),
  });
}

console.log(JSON.stringify({
  homepage: {
    status: homepage.status,
    currentHeaderLabelsPresent: currentHeaderLabels.filter((label) => homepageHtml.includes(label)),
    oldHeaderLabelsStillPresent: oldHeaderLabels.filter((label) => homepageHtml.includes(label)),
    brokenPrefixVisible: homepageHtml.includes("נח נכתב"),
    htmlLength: homepageHtml.length,
  },
  pages,
}, null, 2));
