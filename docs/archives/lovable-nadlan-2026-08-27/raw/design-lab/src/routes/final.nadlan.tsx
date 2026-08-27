import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { ConceptFrame } from "@/components/lab/ConceptFrame";
import {
  Breadcrumbs,
  Card,
  ContextLink,
  Cta,
  ExampleBadge,
  Section,
  SectionHead,
  SiteHeader,
  Tag,
  TrustBlocks,
} from "@/components/lab/primitives";
import { nadlanMenu, nadlanPillars, nadlanTools } from "@/lib/lab-data";

export const Route = createFileRoute("/final/nadlan")({
  head: () => ({
    meta: [
      { title: "כיוון סופי · נדל״ן — כלים תחילה עם מנוע קישור פנימי" },
      {
        name: "description",
        content:
          "כיוון הפקה סופי לאתר הנדל״ן: משגר כלים מעל הקיפול, עמודי תוכן ומילון שמזינים את המחשבונים, וצ׳ק־ליסט לפי שלב בתהליך.",
      },
      { property: "og:title", content: "כיוון סופי · נדל״ן" },
      {
        property: "og:description",
        content: "N1 כלים תחילה, מנוע קישור פנימי מ‑N3 וצ׳ק־ליסט שלב מ‑N2.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "robots", content: "noindex, nofollow" },
    ],
  }),
  component: FinalNadlan,
});

const launcher = [
  { id: "purchase", label: "מחשבון מס רכישה", href: "/nadlan/tools/purchase-tax-calculator" },
  { id: "sim", label: "סימולטור מס רכישה", href: "/nadlan/tools/purchase-tax-simulator" },
  { id: "gains", label: "מחשבון מס שבח", href: "/nadlan/tools/capital-gains-calculator" },
  { id: "tabu", label: "נסח טאבו", href: "/nadlan/tools/tabu-extract" },
];

const glossary = [
  {
    term: "מס רכישה",
    desc: "מס שמשלם הקונה לפי מדרגות ולפי מצב הדירה.",
    href: "/nadlan/tools/purchase-tax-calculator",
    link: "חשבו מס רכישה",
  },
  {
    term: "מס שבח",
    desc: "מס על הרווח במכירת זכות במקרקעין, עם פטורים אפשריים.",
    href: "/nadlan/tools/capital-gains-calculator",
    link: "חשבו מס שבח",
  },
  {
    term: "נסח רישום מקרקעין",
    desc: "מסמך שמרכז את פרטי הזכויות וההערות על הנכס.",
    href: "/nadlan/tools/tabu-extract",
    link: "פתחו את מדריך נסח טאבו",
  },
  {
    term: "דירה יחידה מול דירה נוספת",
    desc: "הגדרה שמשנה את מדרגות המס ולכן את התוצאה בסימולטור.",
    href: "/nadlan/tools/purchase-tax-simulator",
    link: "השוו תרחישי מס רכישה",
  },
];

const stages = [
  {
    id: "budget",
    label: "מחשבים תקציב",
    task: "מרכיבים את העלות הכוללת: מחיר, מסים, עלויות נלוות והון עצמי.",
    tool: { label: "חשבו מס רכישה", href: "/nadlan/tools/purchase-tax-calculator" },
    checks: ["מס רכישה לפי מצב הדירה", "עלויות נלוות", "הון עצמי נדרש"],
  },
  {
    id: "verify",
    label: "בודקים נכס ספציפי",
    task: "מאמתים רישום, זכויות וחובות לפני שמתקדמים לחוזה.",
    tool: { label: "פתחו את מדריך נסח טאבו", href: "/nadlan/tools/tabu-extract" },
    checks: ["נסח רישום מקרקעין", "הערות אזהרה ושעבודים", "התאמה בין הרישום למציאות"],
  },
  {
    id: "compare",
    label: "משווים תרחישים",
    task: "בודקים איך מצב הדירה או מועד העסקה משנים את חבות המס.",
    tool: { label: "השוו תרחישי מס רכישה", href: "/nadlan/tools/purchase-tax-simulator" },
    checks: ["דירה יחידה מול נוספת", "שינוי מועד", "השפעה על התקציב"],
  },
  {
    id: "sell",
    label: "מוכרים דירה",
    task: "בודקים חבות במס שבח, פטורים אפשריים והשפעת מועד המכירה.",
    tool: { label: "חשבו מס שבח", href: "/nadlan/tools/capital-gains-calculator" },
    checks: ["חישוב שבח", "בדיקת פטור", "מועד ותכנון מכירה"],
  },
];

function FinalNadlan() {
  const [selected, setSelected] = useState(launcher[0]!.id);
  const [stage, setStage] = useState(stages[0]!);
  const active = launcher.find((l) => l.id === selected)!;

  return (
    <ConceptFrame id="fn" annotation={annotation} handoff={handoff}>
      <SiteHeader
        brand="נדל״ן"
        menu={nadlanMenu}
        primaryCta="חשבו מס רכישה"
        secondaryCta="בדקו נכס לפני החלטה"
      />

      <main id="main">
        <div className="lab-container pt-6">
          <Breadcrumbs trail={["דף הבית", "כלים ומחשבונים", "מס רכישה"]} />
        </div>

        <Section className="pt-8">
          <div className="grid gap-10 lg:grid-cols-2">
            <div className="min-w-0">
              <Tag>כיוון הפקה סופי · נדל״ן</Tag>
              <h1 className="display mt-4 text-3xl leading-tight md:text-5xl">
                מחשבונים וכלי בדיקה לנדל״ן — תשובה מדויקת לפני ההחלטה
              </h1>
              <p className="mt-4 max-w-xl text-lg leading-relaxed text-muted-foreground">
                כל כלי עומד בפני עצמו, מציג את הכללים שעליהם הוא נשען ואת מועד העדכון
                האחרון, ומחובר למדריך ולמונחים שמסבירים את התוצאה.
              </p>
              <div className="mt-7 flex flex-wrap gap-3">
                <Cta>חשבו מס רכישה</Cta>
                <Cta variant="secondary">בדקו נכס לפני החלטה</Cta>
              </div>
              <p className="mt-5 text-sm text-muted-foreground">
                מדרגות ונתוני חישוב מתעדכנים לפי הפרסום הרשמי; תאריך העדכון מוצג בכל כלי.
              </p>
            </div>

            <Card className="min-w-0">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <h2 className="display text-lg">משגר כלים</h2>
                <ExampleBadge />
              </div>
              <fieldset className="mt-4">
                <legend className="text-sm font-bold">בחרו כלי</legend>
                <div className="mt-3 grid gap-2 sm:grid-cols-2">
                  {launcher.map((l) => (
                    <button
                      key={l.id}
                      type="button"
                      onClick={() => setSelected(l.id)}
                      aria-pressed={selected === l.id}
                      className={
                        "tap rounded-lg px-4 py-3 text-start text-sm font-semibold " +
                        (selected === l.id
                          ? "bg-primary text-primary-foreground"
                          : "border border-border bg-surface text-surface-foreground hover:bg-secondary")
                      }
                    >
                      {l.label}
                    </button>
                  ))}
                </div>
              </fieldset>

              <div className="mt-5 rounded-lg border border-border bg-surface p-4 text-surface-foreground">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <h3 className="font-bold">תצוגת תוצאה · {active.label}</h3>
                  <span className="text-xs text-muted-foreground">עודכן: דוגמה</span>
                </div>
                <dl className="mt-3 grid gap-3 text-sm sm:grid-cols-2">
                  <div>
                    <dt className="text-muted-foreground">נתוני קלט</dt>
                    <dd className="font-medium">סכום, מצב דירה, מועד — דוגמה</dd>
                  </div>
                  <div>
                    <dt className="text-muted-foreground">פירוט מדרגות</dt>
                    <dd className="font-medium">שורה לכל מדרגה — דוגמה</dd>
                  </div>
                </dl>
                <p className="mt-3 text-xs text-muted-foreground">
                  התוצאה ניתנת לשמירה כקישור לשיתוף עם בן/בת זוג, יועץ או עורך/ת דין.
                </p>
                <div className="mt-3">
                  <ContextLink href={active.href}>פתחו את {active.label}</ContextLink>
                </div>
              </div>
            </Card>
          </div>
        </Section>

        <Section tone="surface">
          <SectionHead
            eyebrow="כלים"
            title="ארבעה כלים, ארבעה עמודים נפרדים"
            lead="כל כלי מחזיק כוונת חיפוש וכתובת משלו. אין עמוד ״מחשבון כללי״ שמאחד ביניהם."
          />
          <ul className="grid gap-4 md:grid-cols-2">
            {nadlanTools.map((t) => (
              <Card as="li" key={t.title} className="flex flex-col">
                <h3 className="display text-lg">{t.title}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{t.owns}</p>
                <p className="mt-2 flex-1 text-xs text-muted-foreground">{t.note}</p>
                <div className="mt-4">
                  <ContextLink href={t.href}>{t.linkLabel}</ContextLink>
                </div>
              </Card>
            ))}
          </ul>
        </Section>

        <Section>
          <SectionHead
            eyebrow="לפי שלב בתהליך"
            title="איפה אתם בתהליך?"
            lead="צ׳ק־ליסט אחד לכל שלב, שמוביל לכלי הרלוונטי בלבד."
          />
          <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
            <div
              role="tablist"
              aria-label="שלב בתהליך"
              className="no-scrollbar flex gap-2 overflow-x-auto px-1 pb-1 lg:flex-col lg:overflow-visible lg:px-0"
            >
              {stages.map((s) => (
                <button
                  key={s.id}
                  type="button"
                  role="tab"
                  id={`stage-tab-${s.id}`}
                  aria-selected={stage.id === s.id}
                  aria-controls="stage-panel"
                  onClick={() => setStage(s)}
                  className={
                    "tap shrink-0 whitespace-nowrap rounded-lg px-4 py-3 text-sm font-semibold lg:w-full lg:text-start " +
                    (stage.id === s.id
                      ? "bg-primary text-primary-foreground"
                      : "border border-border bg-card text-card-foreground hover:bg-secondary")
                  }
                >
                  {s.label}
                </button>
              ))}
            </div>

            <div
              id="stage-panel"
              role="tabpanel"
              aria-labelledby={`stage-tab-${stage.id}`}
              className="rounded-xl border border-border bg-card p-5 text-card-foreground"
            >
              <h3 className="display text-lg">{stage.label}</h3>
              <p className="mt-2 text-sm text-muted-foreground">{stage.task}</p>
              <ul className="mt-4 grid gap-2 text-sm">
                {stage.checks.map((c) => (
                  <li key={c} className="flex gap-2">
                    <span aria-hidden="true" className="text-primary">
                      ✓
                    </span>
                    <span>{c}</span>
                  </li>
                ))}
              </ul>
              <div className="mt-5">
                <ContextLink href={stage.tool.href}>{stage.tool.label}</ContextLink>
              </div>
            </div>
          </div>
        </Section>

        <Section tone="surface">
          <SectionHead
            eyebrow="עמודי תוכן"
            title="מנוע הקישור הפנימי: מדריך ← מונח ← כלי"
            lead="כל עמוד עומק מזין את הכלי המתאים, וכל מונח מקשר לכלי אחד בלבד."
          />
          <ul className="grid gap-4 md:grid-cols-2">
            {nadlanPillars.map((p) => (
              <Card as="li" key={p.title}>
                <h3 className="display text-lg">{p.title}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{p.desc}</p>
                <div className="mt-4">
                  <ContextLink href={p.href}>קראו את המדריך המלא</ContextLink>
                </div>
              </Card>
            ))}
          </ul>

          <h3 className="display mt-10 text-xl">מונחים שמובילים לכלי</h3>
          <dl className="mt-4 grid gap-4 md:grid-cols-2">
            {glossary.map((g) => (
              <div
                key={g.term}
                className="rounded-xl border border-border bg-card p-5 text-card-foreground"
              >
                <dt className="text-base font-bold">{g.term}</dt>
                <dd className="mt-2 text-sm text-muted-foreground">{g.desc}</dd>
                <dd className="mt-3">
                  <ContextLink href={g.href}>{g.link}</ContextLink>
                </dd>
              </div>
            ))}
          </dl>
          <div className="mt-6">
            <ContextLink href="/nadlan/glossary">
              עברו למילון המונחים המלא
            </ContextLink>
          </div>
        </Section>

        <Section>
          <SectionHead eyebrow="שקיפות" title="על מה החישוב נשען" />
          <TrustBlocks
            reviewer="בדיקה מקצועית של יועץ/ת מס מקרקעין — שם, תפקיד ותאריך בדיקה: מיקום לשיבוץ, טרם מולא."
            method="מוצגים הכללים והמדרגות שעליהם נשען כל חישוב, ומה נמצא מחוץ לתחום הכלי."
            privacy="נתוני החישוב נשמרים לצורך הצגת התוצאה בלבד; אפשר להשתמש בכלי ללא זיהוי."
            sourceDate="בכל כלי מוצג תאריך העדכון האחרון של הכללים ומקור הפרסום הרשמי."
            limits="הכלים אינם ייעוץ מס או ייעוץ משפטי, ואינם מחליפים בדיקה פרטנית מול רשות המסים."
          />
        </Section>

        <Section tone="surface">
          <div className="rounded-2xl border border-border bg-card p-6 text-card-foreground md:p-8">
            <h2 className="display text-2xl">מתחילים מהמספר שמעניין אתכם</h2>
            <p className="mt-3 max-w-xl text-muted-foreground">
              בוחרים כלי, מקבלים פירוט מלא של החישוב ואפשר לשמור את התוצאה לשיתוף.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <Cta>חשבו מס רכישה</Cta>
              <Cta variant="secondary">בדקו נכס לפני החלטה</Cta>
            </div>
          </div>
        </Section>

        <footer className="border-t border-border py-10">
          <div className="lab-container text-sm text-muted-foreground">
            כלים ומחשבונים · קנייה ומכירה · משכנתאות · בדיקות נכס · מדריכים · מילון נדל״ן
          </div>
        </footer>
      </main>
    </ConceptFrame>
  );
}

const annotation = {
  seoIntent: [
    "עמוד הבית הוא מרכז כלים: הוא מחזיק את הכוונה התועלתית ומחלק אותה לארבעה עמודי כלי נפרדים.",
    "צ׳ק־ליסט השלב מוסיף כוונת ״מה עושים עכשיו״ בלי ליצור עמוד תוכן מתחרה.",
    "שכבת המדריכים והמילון מזינה קישור פנימי יציב לכלים ומחזקת סמכות נושאית.",
  ],
  keywordOwner: [
    "נסח טאבו — עמוד כלי עצמאי ב‑/nadlan/tools/tabu-extract; לא ממוזג לתוך מחשבון מס.",
    "מחשבון מס רכישה — /nadlan/tools/purchase-tax-calculator: חישוב בודד לפי מדרגות.",
    "סימולטור מס רכישה — /nadlan/tools/purchase-tax-simulator: השוואת תרחישים, כוונה נפרדת מהמחשבון.",
    "מחשבון מס שבח — /nadlan/tools/capital-gains-calculator: עמוד נפרד לחלוטין מכלי מס הרכישה.",
    "מונחי המילון מקשרים כל אחד לכלי יחיד, כדי למנוע קניבליזציה בין ארבעת הכלים.",
  ],
  menuLogic: [
    "כלים ומחשבונים ראשון: הערך המרכזי של האתר.",
    "קנייה ומכירה ומשכנתאות: אשכולות התוכן שמזינים את הכלים.",
    "בדיקות נכס: כוונת אימות לפני חתימה, מקשרת לנסח טאבו.",
    "מדריכים ומילון בסוף: שכבת עומק וקישור פנימי.",
    "במובייל התפריט נפתח בכפתור עם aria-expanded; הלוגו וה‑CTA הראשי נשארים גלויים.",
  ],
  conversionLogic: [
    "CTA ראשי אחיד ״חשבו מס רכישה״ מופיע בכותרת, מעל הקיפול ובסיום.",
    "בחירת כלי במשגר היא מיקרו־המרה שמקצרת את הדרך לעמוד הכלי.",
    "התוצאה הניתנת לשיתוף היא מנגנון החזרה לאתר, לא טופס לידים.",
    "אין הצגת מחירים, עסקאות או חיסכון — רק מבנה חישוב ותאריך עדכון.",
  ],
};

const handoff = {
  tokens: [
    { name: "--color-primary", value: "oklch(0.48 0.12 235)", usage: "כפתור ראשי וקישורים הקשריים" },
    { name: "--color-background", value: "oklch(0.98 0.008 220)", usage: "רקע בהיר נקי" },
    { name: "--color-card", value: "oklch(1 0 0)", usage: "כרטיסי כלי ותוצאה" },
    { name: "--color-surface", value: "oklch(0.955 0.012 215)", usage: "רצועות תוכן" },
    { name: "--radius", value: "0.6rem", usage: "רדיוס אחיד" },
    { name: "--font-sans", value: "Heebo", usage: "כל טקסט הממשק בעברית" },
  ],
  blocks: [
    { name: "Tool Launcher", desc: "בורר כלי + כרטיס תצוגת תוצאה עם חותמת עדכון" },
    { name: "Tool Card Grid", desc: "כרטיס כלי עם בעלות על כוונת חיפוש וקישור ייעודי" },
    { name: "Stage Checklist", desc: "טאבים לפי שלב בתהליך עם רשימת בדיקות וקישור לכלי" },
    { name: "Pillar Grid", desc: "עמודי תוכן מרכזיים" },
    { name: "Glossary → Tool", desc: "ערך מילון עם קישור לכלי יחיד" },
    { name: "Trust Stack", desc: "חמישה בלוקי אמון קבועים" },
    { name: "Mobile Nav Drawer", desc: "כפתור תפריט נגיש ומגירת RTL" },
  ],
  menu: [
    { label: "כלים ומחשבונים", children: ["מס רכישה", "סימולטור מס רכישה", "מס שבח", "נסח טאבו"] },
    { label: "קנייה ומכירה", children: ["שלבי העסקה", "חוזה", "מסירה"] },
    { label: "משכנתאות", children: ["תמהיל", "אישור עקרוני", "מסמכים"] },
    { label: "בדיקות נכס", children: ["רישום", "תכנון ובנייה", "מצב פיזי"] },
    { label: "מדריכים", children: ["קונים", "מוכרים", "משקיעים"] },
    { label: "מילון נדל״ן", children: ["מונחי מיסוי", "מונחי רישום"] },
  ],
  schema: [
    "WebSite + SearchAction בעמוד הבית",
    "SoftwareApplication או WebApplication בכל עמוד מחשבון",
    "HowTo בעמוד נסח טאבו",
    "DefinedTermSet במילון, DefinedTerm בכל ערך",
    "BreadcrumbList בכל עמוד פנימי; Article עם dateModified במדריכים",
  ],
  performance: [
    "חישוב בצד הלקוח בלבד, ללא ספריות כבדות",
    "גופנים ב‑preconnect + font-display: swap",
    "טאבים ומשגר ללא אנימציה; מעברי CSS בלבד",
    "יעד: LCP מתחת ל‑2.5 שניות במובייל, INP נמוך, ללא גלילה אופקית ב‑320px",
    "טבלאות מדרגות עם overflow מקומי בלבד, לא ברמת העמוד",
  ],
};

