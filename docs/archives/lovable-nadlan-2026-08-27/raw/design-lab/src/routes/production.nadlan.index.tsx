import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { ProductionShell, type Impl } from "@/components/production/ProductionShell";
import {
  Action,
  Band,
  BandHead,
  Chip,
  DataStateSwitch,
  DemoBadge,
  EmptyState,
  FaqList,
  InlineLink,
  KeyValueGrid,
  LiveState,
  MediaFrame,
  Panel,
  SourceStamp,
  type DataState,
} from "@/components/production/ui";

export const Route = createFileRoute("/production/nadlan/")({
  head: () => ({
    meta: [
      { title: "נדל״ן — פרויקטים, נכסים ובדיקת מחיר לפני חתימה" },
      {
        name: "description",
        content:
          "מצאו פרויקט או נכס, בדקו מחיר והקשר אזורי והבינו את השכונה לפני חתימה. כלים, מפה ומדריכים במקום אחד. מודעות דמו מסומנות בבירור.",
      },
      { property: "og:title", content: "נדל״ן — הצעד הבא בעסקה שלכם" },
      {
        property: "og:description",
        content: "פרויקטים חדשים, נכסים, בדיקת מחיר, מפה ומחשבונים — עם שקיפות מקורות.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "robots", content: "noindex, nofollow" },
    ],
  }),
  component: ProductionNadlanHome,
});

const tasks = [
  { label: "פרויקטים חדשים", desc: "ארכיון פרויקטים לפי עיר, יזם וסטטוס", to: "/production/nadlan/projects" },
  { label: "נכסים", desc: "מודעות דירות למכירה ולהשכרה", to: "/production/nadlan/properties" },
  { label: "בדיקת מחיר", desc: "הקשר מחירים באזור לפי מקור מוצהר", href: "#prices" },
  { label: "מפה", desc: "חיפוש מרחבי לפי שכונה ורדיוס", href: "#map" },
  { label: "מחשבונים", desc: "מס רכישה, מס שבח, נסח טאבו", href: "#tools" },
];

const journeys = [
  {
    title: "קניית דירה חדשה מקבלן",
    steps: ["איתור פרויקט מתאים", "בדיקת יזם, סטטוס והיתרים", "השוואת טיפוסים והכיוונים", "בדיקת עלות כוללת כולל מסים"],
    link: { label: "עברו לארכיון הפרויקטים", to: "/production/nadlan/projects" },
  },
  {
    title: "קניית דירה יד שנייה",
    steps: ["הגדרת אזור ותקציב", "השוואת מודעות רלוונטיות", "בדיקת רישום וזכויות", "תיאום ביקור ומשא ומתן"],
    link: { label: "עברו לארכיון הנכסים", to: "/production/nadlan/properties" },
  },
  {
    title: "בדיקת עסקה לפני חתימה",
    steps: ["בדיקת נסח רישום מקרקעין", "התאמה בין רישום למצב בפועל", "חישוב מס רכישה או מס שבח", "צ׳ק־ליסט מסמכים"],
    link: { label: "פתחו את משגר הכלים", href: "#tools" },
  },
];

const tools = [
  { title: "נסח טאבו", intent: "הפקה וקריאה של נסח רישום מקרקעין", href: "/nadlan/tools/tabu-extract", cta: "פתחו את מדריך נסח טאבו" },
  { title: "מחשבון מס רכישה", intent: "כמה מס רכישה אשלם על הדירה", href: "/nadlan/tools/purchase-tax-calculator", cta: "חשבו מס רכישה" },
  { title: "סימולטור מס רכישה", intent: "השוואת תרחישים: דירה יחידה מול נוספת", href: "/nadlan/tools/purchase-tax-simulator", cta: "השוו תרחישי מס" },
  { title: "מחשבון מס שבח", intent: "מס שבח במכירה, פטורים וחישוב ליניארי", href: "/nadlan/tools/capital-gains-calculator", cta: "חשבו מס שבח" },
];

const demoListings = [
  { title: "3 חדרים, בקעה, ירושלים", meta: "78 מ״ר · קומה 2 · מעלית", to: "/production/nadlan/properties/baka-demo" },
  { title: "4 חדרים, רמת אביב, תל אביב", meta: "104 מ״ר · קומה 5 · חניה" },
  { title: "2 חדרים, מרכז חיפה", meta: "56 מ״ר · קומה 1 · מרפסת" },
];

const cityHubs = ["תל אביב", "ירושלים", "חיפה", "באר שבע", "רמת גן", "נתניה", "ראשון לציון", "פתח תקווה"];

const glossary = [
  { term: "היתר בנייה", desc: "אישור סטטוטורי להתחלת בנייה; משפיע על לוח הזמנים בפרויקט.", href: "#guides", link: "קראו מה בודקים בפרויקט לפני רכישה" },
  { term: "מס רכישה", desc: "מס שמשלם הקונה לפי מדרגות ולפי מצב הדירה.", href: "/nadlan/tools/purchase-tax-calculator", link: "חשבו מס רכישה" },
  { term: "נסח רישום מקרקעין", desc: "מסמך שמרכז זכויות, שעבודים והערות אזהרה.", href: "/nadlan/tools/tabu-extract", link: "פתחו את מדריך נסח טאבו" },
  { term: "מס שבח", desc: "מס על הרווח במכירת זכות במקרקעין.", href: "/nadlan/tools/capital-gains-calculator", link: "חשבו מס שבח" },
];

const pros = [
  { name: "עו״ד מקרקעין · פרופיל דמו", area: "תל אביב והמרכז", note: "ליווי חוזי מכר ובדיקות רישום" },
  { name: "יועץ/ת משכנתאות · פרופיל דמו", area: "ארצי", note: "בניית תמהיל והכנה לאישור עקרוני" },
  { name: "שמאי/ת מקרקעין · פרופיל דמו", area: "ירושלים והסביבה", note: "הערכת שווי ובדיקת פערי רישום" },
];

const faq = [
  {
    q: "למה חלק מהמודעות מסומנות כדוגמה?",
    a: "המוצר בשלב בנייה והמלאי האמיתי נאסף כעת. מודעות הדמו ממחישות את חוויית החיפוש והמודעה, ואינן מלאי פעיל, הצעה או נתון שוק.",
  },
  {
    q: "מה ההבדל בין פרויקטים לנכסים?",
    a: "פרויקטים הם מתחמים חדשים מיזמים, עם טיפוסים וסטטוס בנייה. נכסים הם מודעות ספציפיות למכירה או השכרה. כל אחד מהם אשכול חיפוש נפרד עם כתובות נפרדות.",
  },
  {
    q: "איך נקבע תאריך העדכון של נתון?",
    a: "כל נתון מוצג עם מקור ותאריך עדכון. כשאין מקור מאומת, השדה נשאר ריק ומסומן ״טרם מולא״ במקום להציג הערכה.",
  },
  {
    q: "כמה עולה לפרסם נכס?",
    a: "פרסום נכס אמיתי בשלב זה ללא עלות. הפרסום עובר בדיקה לפני שהוא מופיע כמודעה אמיתית.",
  },
];

function ProductionNadlanHome() {
  const [supply, setSupply] = useState<DataState>("demo");

  return (
    <ProductionShell route="/production/nadlan" impl={impl}>
      <main id="main">
        {/* HERO */}
        <section className="border-b border-border bg-surface text-surface-foreground">
          <div className="lab-container grid gap-10 py-12 md:py-16 lg:grid-cols-[1.1fr_0.9fr]">
            <div className="min-w-0">
              <Chip tone="copper">אב טיפוס מוצר · נתוני דמו מסומנים</Chip>
              <h1 className="display mt-4 text-3xl leading-[1.15] md:text-5xl">
                מוצאים פרויקט או נכס, בודקים מחיר והקשר, ומבינים את האזור לפני שחותמים
              </h1>
              <p className="mt-4 max-w-xl text-base leading-relaxed text-muted-foreground md:text-lg">
                מערכת אחת שמחברת בין פרויקטים חדשים, מודעות נכסים, נתוני מחיר, מפה
                וכלי מיסוי — עם מקור ותאריך עדכון על כל נתון.
              </p>

              <div id="hero-tasks" className="mt-7">
                <h2 className="text-sm font-bold uppercase tracking-wide text-muted-foreground">
                  מה תרצו לעשות עכשיו?
                </h2>
                <ul className="mt-3 grid gap-2 sm:grid-cols-2">
                  {tasks.map((t) =>
                    t.to ? (
                      <li key={t.label}>
                        <Action variant="quiet" to={t.to} className="w-full justify-start text-start">
                          <span className="min-w-0">
                            <span className="block font-bold">{t.label}</span>
                            <span className="block text-xs font-normal text-muted-foreground">{t.desc}</span>
                          </span>
                        </Action>
                      </li>
                    ) : (
                      <li key={t.label}>
                        <Action variant="quiet" href={t.href} className="w-full justify-start text-start">
                          <span className="min-w-0">
                            <span className="block font-bold">{t.label}</span>
                            <span className="block text-xs font-normal text-muted-foreground">{t.desc}</span>
                          </span>
                        </Action>
                      </li>
                    ),
                  )}
                </ul>
              </div>

              <div className="mt-7 flex flex-wrap gap-3">
                <Action to="/production/nadlan/projects">מצאו את הצעד הבא</Action>
                <Action variant="copper" to="/production/nadlan/post-listing">
                  פרסמו נכס אמיתי
                </Action>
              </div>
            </div>

            <Panel className="min-w-0 self-start">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <h2 className="display text-lg">חיפוש מהיר</h2>
                <Chip>מצב דמו</Chip>
              </div>
              <form className="mt-4 grid gap-3" onSubmit={(e) => e.preventDefault()}>
                <div>
                  <label htmlFor="q-city" className="block text-sm font-semibold">
                    עיר או שכונה
                  </label>
                  <input
                    id="q-city"
                    type="text"
                    placeholder="לדוגמה: תל אביב, בקעה"
                    className="tap mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  />
                </div>
                <div className="grid gap-3 sm:grid-cols-2">
                  <div>
                    <label htmlFor="q-type" className="block text-sm font-semibold">
                      סוג חיפוש
                    </label>
                    <select
                      id="q-type"
                      className="tap mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    >
                      <option>פרויקט חדש</option>
                      <option>דירה למכירה</option>
                      <option>דירה להשכרה</option>
                    </select>
                  </div>
                  <div>
                    <label htmlFor="q-rooms" className="block text-sm font-semibold">
                      חדרים
                    </label>
                    <select
                      id="q-rooms"
                      className="tap mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    >
                      <option>הכול</option>
                      <option>2+</option>
                      <option>3+</option>
                      <option>4+</option>
                    </select>
                  </div>
                </div>
                <Action variant="primary" href="#results-preview" className="w-full">
                  הציגו תוצאות
                </Action>
                <p className="text-xs text-muted-foreground">
                  התוצאות בשלב זה כוללות מודעות דמו לצד פרויקטים אמיתיים מסומנים במקור.
                </p>
              </form>
            </Panel>
          </div>
        </section>

        {/* JOURNEYS */}
        <Band labelledBy="journeys-h">
          <BandHead
            id="journeys-h"
            eyebrow="שלושה מסלולי החלטה"
            title="בחרו את המסלול שמתאים למצב שלכם"
            lead="כל מסלול מוביל לשלב הבא בפועל, לא לעמוד תדמית."
          />
          <ul className="grid gap-4 md:grid-cols-3">
            {journeys.map((j) => (
              <Panel as="li" key={j.title} className="flex min-w-0 flex-col">
                <h3 className="display text-lg">{j.title}</h3>
                <ol className="mt-3 flex-1 space-y-2 text-sm text-muted-foreground">
                  {j.steps.map((s, i) => (
                    <li key={s} className="flex gap-2">
                      <span
                        aria-hidden="true"
                        className="mt-0.5 inline-flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-secondary text-[0.7rem] font-bold text-secondary-foreground"
                      >
                        {i + 1}
                      </span>
                      <span>{s}</span>
                    </li>
                  ))}
                </ol>
                <div className="mt-4">
                  {j.link.to ? (
                    <InlineLink to={j.link.to}>{j.link.label}</InlineLink>
                  ) : (
                    <InlineLink href={j.link.href}>{j.link.label}</InlineLink>
                  )}
                </div>
              </Panel>
            ))}
          </ul>
        </Band>

        {/* REAL PROJECTS */}
        <Band tone="surface" labelledBy="projects-h">
          <BandHead
            id="projects-h"
            eyebrow="פרויקטים אמיתיים"
            title="פרויקטים עם עובדות פומביות בלבד"
            lead="מוצגים רק פרטים שקיימים בפרסום פומבי. זמינות, מחירון ומועדי מסירה אינם מוצגים ללא אימות."
          />
          <div className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
            <Panel className="min-w-0">
              <div className="flex flex-wrap items-center gap-2">
                <Chip tone="ink">פרויקט אמיתי</Chip>
                <Chip>תל אביב</Chip>
              </div>
              <h3 className="display mt-3 text-xl">Rainbow תל אביב</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                מתחם מגורים באזור שדה דב בתל אביב, 480 יחידות דיור. הנתונים מבוססים על
                מידע פומבי קיים; שדות המקור והעדכון ממתינים לאימות לפני פרסום חי.
              </p>
              <div className="mt-4">
                <KeyValueGrid
                  rows={[
                    { k: "עיר", v: "תל אביב — שדה דב" },
                    { k: "יחידות דיור", v: "480" },
                    { k: "סטטוס", v: "מיקום לשיבוץ — טרם אומת" },
                    { k: "יזם", v: "מיקום לשיבוץ — טרם אומת" },
                  ]}
                />
              </div>
              <SourceStamp
                source="מקור: מידע פומבי קיים — קישור לשיבוץ"
                updated="עודכן: טרם מולא"
                verification="אימות מול היזם: ממתין"
              />
              <div className="mt-4 flex flex-wrap gap-3">
                <Action to="/production/nadlan/projects/rainbow-tel-aviv">
                  לעמוד הפרויקט המלא
                </Action>
                <Action variant="quiet" to="/production/nadlan/projects">
                  כל הפרויקטים
                </Action>
              </div>
            </Panel>
            <div className="grid min-w-0 gap-4">
              <MediaFrame
                label="תמונת פרויקט — מידות שמורות, טעינה עצלה"
                note="תמונות מקור מהיזם בלבד; אין הדמיות שיווקיות ללא ציון מקור."
              />
              <Panel>
                <h3 className="text-base font-bold">איך פרויקט הופך למוצג באתר</h3>
                <ol className="mt-3 space-y-2 text-sm text-muted-foreground">
                  <li>1. איסוף עובדות פומביות והצגתן עם מקור.</li>
                  <li>2. פנייה ליזם להשלמת טיפוסים, סטטוס ולוחות זמנים.</li>
                  <li>3. סימון ״מאומת״ רק לאחר קבלת מקור רשמי.</li>
                </ol>
                <div className="mt-4">
                  <InlineLink to="/production/nadlan/post-listing">
                    הוסיפו פרויקט כיזם
                  </InlineLink>
                </div>
              </Panel>
            </div>
          </div>
        </Band>

        {/* SEEDED SUPPLY */}
        <Band id="results-preview" labelledBy="demo-h">
          <BandHead
            id="demo-h"
            eyebrow="מלאי לדוגמה"
            title="כך תיראה מודעת נכס — לפני שיש מלאי אמיתי"
            lead="המודעות כאן נוצרו כדי להמחיש את חוויית החיפוש, ההשוואה והמודעה. הן אינן מלאי פעיל ואינן הצעות."
          />
          <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
            <DataStateSwitch value={supply} onChange={setSupply} />
            <Action variant="copper" to="/production/nadlan/post-listing">
              פרסמו נכס אמיתי חינם
            </Action>
          </div>

          {supply === "demo" ? (
            <ul className="grid gap-4 md:grid-cols-3">
              {demoListings.map((l) => (
                <Panel as="li" key={l.title} className="flex min-w-0 flex-col">
                  <MediaFrame label="תמונת נכס — מקום שמור" ratio="4 / 3" />
                  <div className="mt-3">
                    <DemoBadge label="נכס לדוגמה" />
                  </div>
                  <h3 className="display mt-2 text-base">{l.title}</h3>
                  <p className="mt-1 flex-1 text-sm text-muted-foreground">{l.meta}</p>
                  <p className="mt-2 text-xs text-muted-foreground">
                    מחיר: לא מוצג במודעת דמו
                  </p>
                  <div className="mt-3">
                    {l.to ? (
                      <InlineLink to={l.to}>צפו במודעה לדוגמה</InlineLink>
                    ) : (
                      <InlineLink href="/production/nadlan/properties">
                        צפו בכל מודעות הדמו
                      </InlineLink>
                    )}
                  </div>
                </Panel>
              ))}
            </ul>
          ) : null}

          {supply === "empty" ? (
            <EmptyState
              title="אין עדיין מודעות אמיתיות באזור הזה"
              body="כשאין מלאי מאומת אנחנו מציגים מצב ריק מפורש, לא מודעות ממולאות. אפשר לקבל התראה כשמלאי אמיתי מתפרסם."
              ctaLabel="פרסמו נכס אמיתי חינם"
            />
          ) : null}

          {supply === "live" ? (
            <LiveState
              title="תצוגת מודעה אמיתית"
              body="במצב אמיתי כל מודעה מציגה בעל רישום, מקור, תאריך עדכון וסטטוס אימות. עד לקבלת מקור, השדות נשארים ריקים ומסומנים."
            />
          ) : null}
        </Band>

        {/* TOOLS */}
        <Band id="tools" tone="surface" labelledBy="tools-h">
          <BandHead
            id="tools-h"
            eyebrow="כלים"
            title="ארבעה כלים, ארבע כתובות נפרדות"
            lead="כל כלי מחזיק כוונת חיפוש משלו ואינו ממוזג לעמוד ״מחשבון כללי״."
          />
          <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {tools.map((t) => (
              <Panel as="li" key={t.title} className="flex min-w-0 flex-col">
                <h3 className="display text-base">{t.title}</h3>
                <p className="mt-2 flex-1 text-sm text-muted-foreground">{t.intent}</p>
                <p className="mt-2 font-mono text-[0.65rem] text-muted-foreground">{t.href}</p>
                <div className="mt-3">
                  <InlineLink href={t.href}>{t.cta}</InlineLink>
                </div>
              </Panel>
            ))}
          </ul>
        </Band>

        {/* MAP + PRICES */}
        <Band id="map" labelledBy="map-h">
          <BandHead
            id="map-h"
            eyebrow="מפה ונתוני מחיר"
            title="חיפוש מרחבי והקשר מחירים באזור"
            lead="המפה והנתונים משמשים להבנת הסביבה: מה קרוב, מה מתוכנן ומה טווח המחירים המדווח."
          />
          <div className="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
            <div className="min-w-0">
              <MediaFrame
                label="מפה אינטראקטיבית — נטענת בלחיצה, ללא הפעלה אוטומטית"
                ratio="16 / 10"
                note="שכבות: פרויקטים, מודעות, מוסדות חינוך, תחבורה, תוכניות בנייה."
              />
            </div>
            <div id="prices" className="grid min-w-0 gap-4">
              <Panel>
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <h3 className="display text-lg">הקשר מחירים באזור</h3>
                  <DemoBadge label="מבנה תצוגה — ללא נתון" />
                </div>
                <dl className="mt-3 grid gap-3 text-sm sm:grid-cols-2">
                  <div>
                    <dt className="text-muted-foreground">טווח מחירים מדווח</dt>
                    <dd className="font-semibold">ממתין למקור נתונים</dd>
                  </div>
                  <div>
                    <dt className="text-muted-foreground">מספר עסקאות בתקופה</dt>
                    <dd className="font-semibold">ממתין למקור נתונים</dd>
                  </div>
                </dl>
                <SourceStamp
                  source="מקור מתוכנן: פרסום עסקאות רשמי"
                  updated="תדירות עדכון: לשיבוץ"
                  verification="בדיקת איכות נתונים: לשיבוץ"
                />
              </Panel>
              <Panel>
                <h3 className="text-base font-bold">ערי חיפוש מרכזיות</h3>
                <ul className="mt-3 flex flex-wrap gap-2">
                  {cityHubs.map((c) => (
                    <li key={c}>
                      <a
                        href="#"
                        className="tap inline-flex items-center rounded-md border border-border bg-card px-3 py-2 text-xs font-semibold hover:bg-secondary"
                      >
                        נדל״ן ב{c}
                      </a>
                    </li>
                  ))}
                </ul>
                <p className="mt-3 text-xs text-muted-foreground">
                  רק עמודי עיר מתוחזקים נכנסים לאינדקס; שילובי פילטרים נשארים noindex.
                </p>
              </Panel>
            </div>
          </div>
        </Band>

        {/* PROS */}
        <Band id="pros" tone="surface" labelledBy="pros-h">
          <BandHead
            id="pros-h"
            eyebrow="אנשי מקצוע"
            title="אינדקס בעלי מקצוע — בבנייה"
            lead="הפרופילים המוצגים הם פרופילי דמו להמחשת מבנה הכרטיס. אין כרגע ספירת מאומתים ואין דירוגים."
          />
          <ul className="grid gap-4 md:grid-cols-3">
            {pros.map((p) => (
              <Panel as="li" key={p.name} className="min-w-0 border-dashed">
                <DemoBadge label="פרופיל דמו" />
                <h3 className="display mt-2 text-base">{p.name}</h3>
                <p className="mt-1 text-sm text-muted-foreground">{p.area}</p>
                <p className="mt-2 text-sm">{p.note}</p>
                <p className="mt-3 text-xs text-muted-foreground">
                  רישיון, ותק וביקורות: יוצגו רק לאחר אימות מסמכים.
                </p>
              </Panel>
            ))}
          </ul>
          <div className="mt-5 flex flex-wrap gap-3">
            <Action variant="copper" to="/production/nadlan/post-listing">
              תבעו בעלות על פרופיל
            </Action>
            <Action variant="quiet" href="#methodology">
              איך נראה פרופיל מאומת
            </Action>
          </div>
        </Band>

        {/* GUIDES / GLOSSARY */}
        <Band id="guides" labelledBy="guides-h">
          <BandHead
            id="guides-h"
            eyebrow="מדריכים ומונחים"
            title="מנוע הקישור הפנימי: מדריך ← מונח ← כלי"
            lead="כל מונח מקשר לכלי אחד בלבד, כדי לשמור על הפרדת כוונות חיפוש."
          />
          <dl className="grid gap-4 md:grid-cols-2">
            {glossary.map((g) => (
              <div key={g.term} className="rounded-lg border border-border bg-card p-5">
                <dt className="text-base font-bold">{g.term}</dt>
                <dd className="mt-2 text-sm text-muted-foreground">{g.desc}</dd>
                <dd className="mt-3">
                  <InlineLink href={g.href}>{g.link}</InlineLink>
                </dd>
              </div>
            ))}
          </dl>
        </Band>

        {/* METHODOLOGY */}
        <Band id="methodology" tone="surface" labelledBy="method-h">
          <BandHead
            id="method-h"
            eyebrow="שקיפות"
            title="מתודולוגיה: מאיפה מגיע כל נתון"
            lead="שלושה מצבי נתונים גלויים למשתמש, ללא ערבוב ביניהם."
          />
          <ul className="grid gap-4 md:grid-cols-3">
            <Panel as="li">
              <Chip tone="copper">דמו</Chip>
              <h3 className="display mt-2 text-base">תוכן להמחשה</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                נוצר על ידינו כדי להראות את המבנה. מסומן בכל כרטיס, לא נספר כמלאי ולא מופיע
                בספירות תוצאה אמיתיות.
              </p>
            </Panel>
            <Panel as="li">
              <Chip>אין עדיין נתונים</Chip>
              <h3 className="display mt-2 text-base">מצב ריק מפורש</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                כשאין מקור, מוצג מצב ריק עם הסבר וקריאה להוספת מלאי — לא תוצאה ממולאת.
              </p>
            </Panel>
            <Panel as="li">
              <Chip tone="ink">נתונים אמיתיים</Chip>
              <h3 className="display mt-2 text-base">מקור, תאריך, אימות</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                כל רשומה נושאת מקור, תאריך עדכון וסטטוס אימות. שדה שלא מולא נשאר ריק וגלוי.
              </p>
            </Panel>
          </ul>
        </Band>

        {/* FAQ */}
        <Band labelledBy="faq-h">
          <BandHead id="faq-h" eyebrow="שאלות נפוצות" title="מה חשוב לדעת לפני שמתחילים" />
          <FaqList items={faq} />
          <div className="mt-8 rounded-lg border border-border bg-card p-6">
            <h2 className="display text-xl">מוכנים לצעד הבא?</h2>
            <p className="mt-2 max-w-xl text-sm text-muted-foreground">
              התחילו מפרויקט, ממודעה או מבדיקת מס — ואם יש לכם נכס אמיתי, פרסמו אותו
              והיו חלק מהמלאי הראשון.
            </p>
            <div className="mt-5 flex flex-wrap gap-3">
              <Action to="/production/nadlan/projects">מצאו את הצעד הבא</Action>
              <Action variant="copper" to="/production/nadlan/post-listing">
                פרסמו נכס אמיתי חינם
              </Action>
            </div>
          </div>
        </Band>
      </main>
    </ProductionShell>
  );
}

const impl: Impl = {
  intent: "כוונה מעורבת: גילוי פרויקטים ונכסים, בדיקת מחיר והקשר, וכניסה לכלי מיסוי. עמוד הבית מחלק כוונות ואינו מתחרה בעמודי הארכיון.",
  keywords: {
    primary: "נדל״ן בישראל — חיפוש פרויקטים ונכסים",
    secondary: ["פרויקטים חדשים", "דירות למכירה", "בדיקת מחיר דירה", "מחשבון מס רכישה", "מפת נדל״ן"],
  },
  meta: {
    title: "נדל״ן — פרויקטים, נכסים ובדיקת מחיר לפני חתימה",
    description:
      "מצאו פרויקט או נכס, בדקו מחיר והקשר אזורי והבינו את השכונה לפני חתימה. כלים, מפה ומדריכים במקום אחד.",
    canonical: "https://nad-lan.co.il/",
  },
  schema: [
    "WebSite + SearchAction",
    "Organization (ללא הצהרות שלא אומתו)",
    "FAQPage — רק לשאלות המוצגות בעמוד",
    "ItemList לפרויקטים אמיתיים בלבד; מודעות דמו אינן נכנסות ל‑schema",
  ],
  internalLinks: [
    "ארכיון פרויקטים ← /production/nadlan/projects",
    "ארכיון נכסים ← /production/nadlan/properties",
    "עמוד פרויקט Rainbow ← /production/nadlan/projects/rainbow-tel-aviv",
    "ארבעה כלים ← כתובות נפרדות תחת /nadlan/tools/*",
    "פרסום נכס ← /production/nadlan/post-listing",
  ],
  dataPolicy: [
    "מודעות דמו: badge ״נכס לדוגמה״, ללא מחיר, ללא schema, לא נספרות במונה תוצאות אמיתי.",
    "פרויקט אמיתי: עובדות פומביות בלבד + שדות מקור/עדכון/אימות גלויים גם כשריקים.",
    "פרופילי מקצוע: ״פרופיל דמו״ עד לאימות מסמכים; אין ספירת מאומתים.",
    "אין מחירים, חיסכון, לידים, ביקורות או נתוני שוק מומצאים.",
  ],
  wordpress: [
    "Hero Task Launcher → block: nadlan/hero-tasks",
    "Journey Cards → block: nadlan/journey-grid",
    "Project Card (real) → block: nadlan/project-card עם ACF source/updated/verified",
    "Demo Listing Card → block: nadlan/listing-card (state=demo)",
    "Tool Launcher → block: nadlan/tool-grid",
    "Map Block → block: nadlan/map (lazy init on click)",
    "Glossary→Tool → block: nadlan/term-link",
    "FAQ → core/details בתוך nadlan/faq",
  ],
};

