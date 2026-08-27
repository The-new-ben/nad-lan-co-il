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
import { justiceCards, justiceMenu } from "@/lib/lab-data";

export const Route = createFileRoute("/final/justice")({
  head: () => ({
    meta: [
      { title: "כיוון סופי · Justice — מוצר תחילה עם שכבת סמכות" },
      {
        name: "description",
        content:
          "כיוון הפקה סופי ל‑jus-tice.co.il: בורר תרחישים וסימולציה מעל הקיפול, מתחתיו שיטת עריכה גלויה, כרטיסי נושא משפטיים ופיצול קהלים מרוסן.",
      },
      { property: "og:title", content: "כיוון סופי · Justice" },
      {
        property: "og:description",
        content: "J1 מוצר תחילה עם רכיבי הסמכות החזקים של J2, בלי שכפול כוונת חיפוש.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "robots", content: "noindex, nofollow" },
    ],
  }),
  component: FinalJustice,
});

const scenarios = [
  {
    id: "hearing",
    label: "דיון קרוב בבית משפט",
    detail: "בונים סדר יום לדיון, מזהים שאלות צפויות ומתרגלים תשובות קצרות.",
    steps: ["מיפוי ההליך", "שאלות צפויות", "תרגול מונחה", "סיכום להדפסה"],
  },
  {
    id: "cross",
    label: "חקירת עדים",
    detail: "מפרקים את העדות לרכיבים ומתרגלים שורת שאלות אחת בכל פעם.",
    steps: ["בניית קו חקירה", "ניסוח שאלה סגורה", "התמודדות עם התחמקות", "מסקנות"],
  },
  {
    id: "family",
    label: "הליך גירושין",
    detail: "מבינים את מרכיבי ההליך ואת נקודות המחלוקת לפני פגישה מקצועית.",
    steps: ["מפת ההליך", "סעיפי הסכם", "פערים פתוחים", "שאלות לעורך/ת דין"],
  },
  {
    id: "record",
    label: "מחיקת רישום פלילי",
    detail: "בודקים תנאי סף ומסלולים, ומכינים את המסמכים הנדרשים.",
    steps: ["תנאי סף", "בחירת מסלול", "מסמכים", "לוח זמנים"],
  },
];

const methodSteps = [
  {
    t: "מיפוי כוונת החיפוש",
    d: "כל עמוד נפתח בשאלה אחת שהמשתמש חיפש, ולא בהצהרה שיווקית.",
  },
  {
    t: "כתיבה על בסיס מקורות ראשוניים",
    d: "חקיקה, תקנות ופרסומים רשמיים. מציינים איזה סוג מקור עומד מאחורי כל טענה.",
  },
  {
    t: "בדיקה מקצועית",
    d: "מיקום לשיבוץ שם עורך/ת דין בודק/ת, תחום ותאריך בדיקה — טרם מולא.",
  },
  {
    t: "עדכון תקופתי",
    d: "מוצג תאריך פרסום ותאריך עדכון אחרון. שינוי מהותי מסומן ביומן שינויים.",
  },
];

const audiences = [
  {
    t: "אנשים פרטיים לפני הליך",
    d: "רוצים להבין מה צפוי, איך להתכונן ואיזה שאלות לשאול. המסלול נשאר הסימולציה.",
    href: "/justice/guides/first-steps",
    link: "קראו מה קורה בשלב הראשון של ההליך",
  },
  {
    t: "עורכי דין וחברות",
    d: "שימוש מקצועי, הכנת לקוח ועבודה בצוות. הפירוט המלא של המוצר המקצועי נמצא ב‑jus-tice.com.",
    href: "/justice/for-lawyers",
    link: "עברו לעמוד השימוש המקצועי",
  },
];

function FinalJustice() {
  const [active, setActive] = useState<(typeof scenarios)[number]>(scenarios[0]!);

  return (
    <ConceptFrame id="fj" annotation={annotation} handoff={handoff}>
      <SiteHeader
        brand="Justice"
        menu={justiceMenu}
        primaryCta="התחילו סימולציה"
        secondaryCta="מצאו את המסלול שלכם"
      />

      <main id="main">
        <div className="lab-container pt-6">
          <Breadcrumbs trail={["דף הבית", "כלים וסימולציות", "בחירת תרחיש"]} />
        </div>

        <Section className="pt-8">
          <div className="grid gap-10 lg:grid-cols-[1.05fr_0.95fr]">
            <div className="min-w-0">
              <Tag>כיוון הפקה סופי · Justice</Tag>
              <h1 className="display mt-4 text-3xl leading-tight md:text-5xl">
                מתכוננים להליך המשפטי שלכם בתרגול, לא בניחוש
              </h1>
              <p className="mt-4 max-w-xl text-lg leading-relaxed text-muted-foreground">
                בוחרים תרחיש, מקבלים מפת שלבים ומתרגלים את הרגעים שבאמת קובעים —
                בקצב שלכם, לפני הפגישה עם עורך/ת דין.
              </p>
              <div className="mt-7 flex flex-wrap gap-3">
                <Cta>התחילו סימולציה</Cta>
                <Cta variant="secondary">מצאו את המסלול שלכם</Cta>
              </div>
              <p className="mt-5 text-sm text-muted-foreground">
                הכלי אינו ייעוץ משפטי ואינו מחליף עורך/ת דין.
              </p>
            </div>

            <Card className="min-w-0">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <h2 className="display text-lg">בורר תרחישים</h2>
                <ExampleBadge />
              </div>
              <fieldset className="mt-4">
                <legend className="text-sm font-bold">בחרו את המצב שלכם</legend>
                <div className="mt-3 grid gap-2 sm:grid-cols-2">
                  {scenarios.map((s) => (
                    <button
                      key={s.id}
                      type="button"
                      onClick={() => setActive(s)}
                      aria-pressed={active.id === s.id}
                      className={
                        "tap rounded-lg px-4 py-3 text-start text-sm font-semibold " +
                        (active.id === s.id
                          ? "bg-primary text-primary-foreground"
                          : "border border-border bg-surface text-surface-foreground hover:bg-secondary")
                      }
                    >
                      {s.label}
                    </button>
                  ))}
                </div>
              </fieldset>

              <div className="mt-5 rounded-lg border border-border bg-surface p-4 text-surface-foreground">
                <h3 className="font-bold">תצוגת סימולציה · {active.label}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{active.detail}</p>
                <ol className="mt-3 grid gap-2 text-sm">
                  {active.steps.map((st, i) => (
                    <li key={st} className="flex gap-2">
                      <span className="font-mono text-xs text-highlight">
                        {String(i + 1).padStart(2, "0")}
                      </span>
                      <span>{st}</span>
                    </li>
                  ))}
                </ol>
                <p className="mt-3 text-xs text-muted-foreground">
                  תצוגה מקדימה של מבנה התרגול. תוכן ההדגמה מסומן ״דוגמה״.
                </p>
              </div>
            </Card>
          </div>
        </Section>

        <Section tone="surface">
          <SectionHead
            eyebrow="איך זה עובד"
            title="שלושה שלבים מהחיפוש ועד התרגול"
            lead="ההסבר בא מיד אחרי המוצר, כדי להסיר חסם אמון לפני ההרשמה."
          />
          <ol className="grid gap-4 md:grid-cols-3">
            {[
              { t: "בוחרים תרחיש", d: "מזהים את המצב הקרוב אליכם מתוך רשימה סגורה." },
              { t: "מקבלים מפת שלבים", d: "רואים מה צפוי בכל שלב ומה נדרש להכין." },
              { t: "מתרגלים ומסכמים", d: "מריצים תרגול ומקבלים סיכום להדפסה או לשיתוף." },
            ].map((s, i) => (
              <Card as="li" key={s.t}>
                <p className="font-mono text-xs text-muted-foreground">
                  שלב {i + 1}
                </p>
                <h3 className="display mt-1 text-lg">{s.t}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{s.d}</p>
              </Card>
            ))}
          </ol>
        </Section>

        <Section>
          <SectionHead
            eyebrow="שיטת העריכה"
            title="איך נכתב ונבדק התוכן כאן"
            lead="שכבת הסמכות מ‑J2, ממוקמת מתחת להסבר המוצר ולא מעליו."
          />
          <ol className="grid gap-4 md:grid-cols-2">
            {methodSteps.map((m) => (
              <Card as="li" key={m.t}>
                <h3 className="text-base font-bold">{m.t}</h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                  {m.d}
                </p>
              </Card>
            ))}
          </ol>
          <div className="mt-6 rounded-xl border border-dashed border-border p-5">
            <h3 className="text-base font-bold">מיקומי ציון גלויים בכל עמוד תוכן</h3>
            <ul className="mt-3 grid gap-2 text-sm text-muted-foreground md:grid-cols-3">
              <li>נכתב על ידי: ‏[שם] — מיקום לשיבוץ, טרם מולא</li>
              <li>נבדק על ידי: ‏[עורך/ת דין, תחום] — מיקום לשיבוץ, טרם מולא</li>
              <li>עודכן לאחרונה: ‏[תאריך] — מיקום לשיבוץ, טרם מולא</li>
            </ul>
            <div className="mt-4">
              <ContextLink href="/justice/editorial-policy">
                קראו את מדיניות העריכה והבדיקה המלאה
              </ContextLink>
            </div>
          </div>
        </Section>

        <Section tone="surface">
          <SectionHead
            eyebrow="נושאים בעלי ערך"
            title="הנושאים שאנשים מחפשים לפני הליך"
            lead="כל כרטיס מקושר לעמוד יעד יחיד, כדי לשמור בעלות נפרדת על כוונת החיפוש."
          />
          <ul className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {justiceCards.map((c) => (
              <Card as="li" key={c.title} className="flex flex-col">
                <h3 className="display text-lg">{c.title}</h3>
                <p className="mt-2 flex-1 text-sm leading-relaxed text-muted-foreground">
                  {c.intent}
                </p>
                <div className="mt-4">
                  <ContextLink href={c.href}>{c.linkLabel}</ContextLink>
                </div>
              </Card>
            ))}
          </ul>
        </Section>

        <Section>
          <SectionHead
            eyebrow="נתיב מותאם"
            title="למי מיועד השימוש"
            lead="פיצול מרוסן, אחרי הסבר המוצר: הוא מנתב, אך אינו מתחרה ב‑CTA הראשי."
          />
          <ul className="grid gap-4 md:grid-cols-2">
            {audiences.map((a) => (
              <Card as="li" key={a.t}>
                <h3 className="display text-lg">{a.t}</h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                  {a.d}
                </p>
                <div className="mt-4">
                  <ContextLink href={a.href}>{a.link}</ContextLink>
                </div>
              </Card>
            ))}
          </ul>
        </Section>

        <Section tone="surface">
          <SectionHead eyebrow="שקיפות" title="על מה הכלי נשען" />
          <TrustBlocks
            reviewer="תוכן מקצועי מיועד לבדיקה על ידי עורך/ת דין. שם, תחום ותאריך בדיקה — מיקום לשיבוץ, טרם מולא."
            method="מוסבר כיצד נבנו התרחישים, מאילו סוגי מקורות, ומה נמצא מחוץ לתחום הכלי."
            privacy="הנתונים שמוזנים משמשים להרצת התרגול בלבד, עם מדיניות מחיקה ואפשרות שימוש ללא זיהוי."
            sourceDate="בכל עמוד תוכן מוצגים תאריך עדכון אחרון ותאריך בדיקת המקורות."
            limits="הכלי אינו ייעוץ משפטי, אינו מחליף עורך/ת דין ואינו חוזה תוצאה בהליך."
          />
        </Section>

        <Section>
          <div className="rounded-2xl border border-border bg-card p-6 text-card-foreground md:p-8">
            <h2 className="display text-2xl">מוכנים לתרגל את השלב הבא?</h2>
            <p className="mt-3 max-w-xl text-muted-foreground">
              מתחילים מהתרחיש הקרוב אליכם, ואפשר לעצור ולחזור בכל שלב.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <Cta>התחילו סימולציה</Cta>
              <Cta variant="secondary">מצאו את המסלול שלכם</Cta>
            </div>
          </div>
        </Section>

        <footer className="border-t border-border py-10">
          <div className="lab-container text-sm text-muted-foreground">
            תחומי משפט · כלים וסימולציות · איך זה עובד · לעורכי דין · ידע משפטי
          </div>
        </footer>
      </main>
    </ConceptFrame>
  );
}

const annotation = {
  seoIntent: [
    "עמוד הבית תופס כוונת חיפוש עברית מוקדמת (״איך מתכוננים ל…״) ומעביר אותה ישירות למוצר, במקום להסתיים בתוכן.",
    "שכבת הסמכות ממוקמת מתחת להסבר המוצר: היא מחזקת E-E-A-T בלי לדחוק את הסימולציה מתחת לקיפול.",
    "H1 יחיד; H2 לפי סדר המסע: מוצר, איך זה עובד, שיטת עריכה, נושאים, קהלים, שקיפות, המרה.",
  ],
  keywordOwner: [
    "jus-tice.co.il: רכישה, הסברה והכשרה בעברית — הכנה לדיון, חקירת עדים, עלות גירושין, מחיקת רישום פלילי, הסכם גירושין.",
    "jus-tice.com: הסימולטור כמוצר, סביבת העבודה, המרקטפלייס והפעילות הבינלאומית — אין כאן שכפול של אותה כוונה בעברית.",
    "כרטיס הקהל המקצועי מקשר לעמוד שימוש מקצועי אחד בלבד, כדי לא ליצור אשכול מתחרה בעברית.",
  ],
  menuLogic: [
    "תחומי משפט ראשון: הרחב ביותר, מחזיק את מבנה האשכולות.",
    "כלים וסימולציות שני: הצומת שממיר תנועת מידע לתנועת מוצר.",
    "איך זה עובד שלישי: מסיר חסם אמון לפני ההרשמה.",
    "לעורכי דין רביעי: קהל משני בלבד.",
    "ידע משפטי אחרון: ארכיון עומק לקישור פנימי.",
    "במובייל התפריט נפתח בכפתור ייעודי; הלוגו וה‑CTA הראשי נשארים גלויים תמיד.",
  ],
  conversionLogic: [
    "CTA ראשי אחיד ״התחילו סימולציה״ בכותרת, מעל הקיפול ובסיום — ללא וריאציות מתחרות.",
    "פיצול הקהלים מופיע רק אחרי הסבר המוצר ומנוסח כקישור הקשרי, לא ככפתור מתחרה.",
    "בחירת תרחיש היא מיקרו־המרה שמייצרת מחויבות לפני מסך ההרשמה.",
    "בלוקי אמון ממוקמים לפני ה‑CTA הסוגר, כמענה להתנגדות ״האם זה אמין״.",
  ],
};

const handoff = {
  tokens: [
    { name: "--color-primary", value: "oklch(0.78 0.14 200)", usage: "כפתור ראשי וקישורים הקשריים" },
    { name: "--color-background", value: "oklch(0.19 0.035 258)", usage: "רקע דיו כהה" },
    { name: "--color-card", value: "oklch(0.24 0.04 260)", usage: "כרטיסים ותצוגת מוצר" },
    { name: "--color-surface", value: "oklch(0.22 0.04 259)", usage: "רצועות סמכות ותוכן" },
    { name: "--radius", value: "0.9rem", usage: "רדיוס אחיד" },
    { name: "--font-sans", value: "Heebo", usage: "כל טקסט הממשק בעברית" },
  ],
  blocks: [
    { name: "Hero / בורר תרחישים", desc: "בלוק סינכרוני: כפתורי תרחיש + כרטיס תצוגה מקדימה" },
    { name: "Steps 1-2-3", desc: "בלוק שלבים ממוספר, נשלף גם לעמודי כלי" },
    { name: "Editorial Method", desc: "בלוק שיטת עריכה עם מיקומי כותב/בודק/תאריך" },
    { name: "Topic Card Grid", desc: "כרטיס נושא עם כוונת חיפוש וקישור הקשרי" },
    { name: "Audience Fork", desc: "שני כרטיסי קהל עם קישור הקשרי בלבד" },
    { name: "Trust Stack", desc: "חמישה בלוקי אמון קבועים" },
    { name: "Mobile Nav Drawer", desc: "כפתור תפריט עם aria-expanded ומגירת RTL" },
  ],
  menu: [
    { label: "תחומי משפט", children: ["משפחה", "פלילי", "אזרחי", "עבודה"] },
    { label: "כלים וסימולציות", children: ["חקירת עדים", "הכנה לדיון", "סימולציית משא ומתן"] },
    { label: "איך זה עובד", children: ["מתודולוגיה", "פרטיות ואבטחה", "מגבלות"] },
    { label: "לעורכי דין", children: ["שימוש מקצועי", "שיתופי פעולה"] },
    { label: "ידע משפטי", children: ["מדריכים", "מונחים", "שאלות נפוצות"] },
  ],
  schema: [
    "WebSite + SearchAction בעמוד הבית",
    "HowTo בעמודי הכנה לדיון וחקירת עדים",
    "FAQPage רק כשהשאלות מוצגות בפועל",
    "BreadcrumbList בכל עמוד פנימי",
    "Article עם datePublished, dateModified ו‑reviewedBy — רק לאחר מילוי הבודק בפועל",
  ],
  performance: [
    "גופנים ב‑preconnect + font-display: swap; עד שני משקלים לעמוד",
    "ללא סליידרים או ספריות אנימציה; מעברי CSS בלבד",
    "תמונות WebP עם width/height מפורשים ו‑lazy מתחת לקיפול",
    "יעד: LCP מתחת ל‑2.5 שניות במובייל, CLS מתחת ל‑0.1, ללא גלילה אופקית ב‑320px",
    "Critical CSS מוטבע לחלק העליון",
  ],
};

