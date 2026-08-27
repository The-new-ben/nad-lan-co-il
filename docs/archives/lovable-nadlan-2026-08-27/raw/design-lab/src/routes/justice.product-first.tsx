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

export const Route = createFileRoute("/justice/product-first")({
  head: () => ({
    meta: [
      { title: "J1 · מוצר תחילה — קונספט עמוד בית ל‑jus-tice.co.il" },
      {
        name: "description",
        content:
          "קונספט עמוד בית ממוקד מוצר: בורר תרחישים מעל הקיפול, תצוגת סימולציה ומסלול הכנה מדורג, עם בלוקי אמון ומבנה תפריט מונחה כוונת חיפוש.",
      },
      { property: "og:title", content: "J1 · מוצר תחילה — Justice" },
      {
        property: "og:description",
        content: "בורר תרחישים אינטראקטיבי ותצוגת סימולציה כלב העמוד.",
      },
    ],
  }),
  component: J1,
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
    detail: "מבינים את מרכיבי ההליך, נקודות ההסכמה והמחלוקת לפני פגישה מקצועית.",
    steps: ["מפת ההליך", "סעיפי הסכם", "פערים פתוחים", "שאלות לעורך/ת דין"],
  },
  {
    id: "record",
    label: "מחיקת רישום פלילי",
    detail: "בודקים תנאי סף ומסלולים, ומכינים את המסמכים הנדרשים.",
    steps: ["תנאי סף", "בחירת מסלול", "מסמכים", "לוח זמנים"],
  },
];

function J1() {
  const [active, setActive] = useState<(typeof scenarios)[number]>(scenarios[0]!);

  return (
    <ConceptFrame id="j1" annotation={annotation} handoff={handoff}>
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
          <div className="grid items-start gap-10 lg:grid-cols-[1.05fr_1fr]">
            <div className="rise">
              <Tag>סימולציה מבוססת תרחיש</Tag>
              <h1 className="display mt-4 text-3xl leading-tight md:text-5xl">
                מתכוננים להליך משפטי בעברית — בתרגול, לא בניחוש
              </h1>
              <p className="mt-4 max-w-xl text-lg leading-relaxed text-muted-foreground">
                בוחרים את המצב שבו אתם נמצאים, ומקבלים סימולציה שמלווה שלב אחר שלב:
                מה נשאל, מה חשוב לומר ומה כדאי לברר לפני הפגישה הבאה.
              </p>
              <div className="mt-7 flex flex-wrap gap-3">
                <Cta>התחילו סימולציה</Cta>
                <Cta variant="secondary">מצאו את המסלול שלכם</Cta>
              </div>

              <fieldset className="mt-9">
                <legend className="text-sm font-bold">בחרו תרחיש כדי לראות תצוגה מקדימה</legend>
                <div className="mt-3 flex flex-wrap gap-2">
                  {scenarios.map((s) => (
                    <button
                      key={s.id}
                      type="button"
                      onClick={() => setActive(s)}
                      aria-pressed={active.id === s.id}
                      className={
                        "tap rounded-lg px-4 py-2 text-sm font-semibold transition-colors " +
                        (active.id === s.id
                          ? "bg-primary text-primary-foreground"
                          : "border border-border bg-card text-card-foreground hover:bg-secondary")
                      }
                    >
                      {s.label}
                    </button>
                  ))}
                </div>
              </fieldset>
            </div>

            <Card className="rise">
              <div className="flex items-center justify-between gap-3">
                <h2 className="display text-lg">תצוגת סימולציה · {active.label}</h2>
                <ExampleBadge />
              </div>
              <p className="mt-3 text-sm leading-relaxed text-muted-foreground">{active.detail}</p>
              <ol className="mt-5 space-y-3">
                {active.steps.map((step, i) => (
                  <li
                    key={step}
                    className="flex items-start gap-3 rounded-lg border border-border bg-surface p-3 text-surface-foreground"
                  >
                    <span
                      aria-hidden="true"
                      className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-highlight text-sm font-bold text-highlight-foreground"
                    >
                      {i + 1}
                    </span>
                    <span className="text-sm font-medium">{step}</span>
                  </li>
                ))}
              </ol>
              <p className="mt-4 text-xs leading-relaxed text-muted-foreground">
                תצוגה להמחשת מבנה המוצר. אין כאן ייעוץ משפטי ואין הבטחת תוצאה.
              </p>
              <div className="mt-4">
                <ContextLink href="/justice/simulation/start">
                  התחילו את הסימולציה עבור {active.label}
                </ContextLink>
              </div>
            </Card>
          </div>
        </Section>

        <Section tone="surface">
          <SectionHead
            eyebrow="כלים ותוכן"
            title="נושאים שאנשים מחפשים — וכל אחד מוביל לתרגול"
            lead="כל כרטיס הוא עמוד עצמאי עם כוונת חיפוש משלו, ומקשר פנימה אל השלב הרלוונטי בסימולציה."
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
            eyebrow="איך זה עובד"
            title="שלושה שלבים מהחיפוש ועד ההכנה"
          />
          <ol className="grid gap-4 md:grid-cols-3">
            {[
              {
                t: "מתארים את המצב",
                d: "כמה שאלות קצרות בעברית פשוטה, בלי מונחים מיותרים.",
              },
              {
                t: "מריצים סימולציה",
                d: "תרגול מונחה של הרגעים שבאמת קובעים: שאלות, תשובות והחלטות.",
              },
              {
                t: "יוצאים עם סיכום",
                d: "מסמך הכנה אישי ורשימת שאלות לפגישה עם גורם מקצועי.",
              },
            ].map((s, i) => (
              <Card as="li" key={s.t}>
                <p className="font-mono text-sm text-muted-foreground">0{i + 1}</p>
                <h3 className="display mt-1 text-lg">{s.t}</h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{s.d}</p>
              </Card>
            ))}
          </ol>
          <div className="mt-6">
            <ContextLink href="/justice/how-it-works">
              קראו בהרחבה כיצד נבנית הסימולציה
            </ContextLink>
          </div>
        </Section>

        <Section tone="surface">
          <SectionHead eyebrow="שקיפות" title="על מה הכלי נשען" />
          <TrustBlocks
            reviewer="תוכן מקצועי מיועד לבדיקה על ידי עורך/ת דין. מציין שם, תחום ותאריך בדיקה — מציין מיקום לשיבוץ, טרם מולא."
            method="מסבירים כיצד נבנו התרחישים, מאילו סוגי מקורות, ומה נמצא מחוץ לתחום הכלי."
            privacy="הנתונים שמוזנים משמשים להרצת התרגול בלבד. מוצגת מדיניות מחיקה ואפשרות שימוש ללא זיהוי."
            sourceDate="לכל עמוד תוכן מוצג תאריך עדכון אחרון ותאריך בדיקת המקורות."
            limits="הכלי אינו ייעוץ משפטי, אינו מחליף עורך/ת דין ואינו חוזה תוצאה בהליך."
          />
        </Section>

        <Section>
          <div className="rounded-2xl border border-border bg-card p-8 text-card-foreground">
            <h2 className="display text-2xl">מוכנים לתרגל את השלב הבא?</h2>
            <p className="mt-3 max-w-xl text-muted-foreground">
              מתחילים מהתרחיש שהכי קרוב אליכם, ואפשר לעצור ולחזור בכל שלב.
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
    "העמוד תופס כוונת חיפוש בעברית של ״הכנה לדיון״ ו״איך מתכוננים ל…״ ומעביר אותה למוצר, במקום להישאר בתוכן בלבד.",
    "בורר התרחישים יוצר קישור פנימי מובנה מעמוד הבית אל ארבעה אשכולות תוכן/כלי מרכזיים.",
    "H1 יחיד ממוקד תועלת; H2 לפי שלבי המסע: כלים ותוכן, איך זה עובד, שקיפות, המרה.",
  ],
  keywordOwner: [
    "jus-tice.co.il: ביטויי חיפוש עבריים של אנשים לפני הליך — הכנה לדיון, חקירת עדים, עלות גירושין, מחיקת רישום פלילי, הסכם גירושין.",
    "jus-tice.com: הסימולטור כמוצר, סביבת עבודה מקצועית, מרקטפלייס ובינלאומי — לא משוכפל כאן.",
    "כל כרטיס בעמוד הבית מקושר לעמוד יעד יחיד, כדי למנוע קניבליזציה בין נכסי תוכן.",
  ],
  menuLogic: [
    "תחומי משפט ראשון: הרחב ביותר, קולט חיפוש נושאי ומחזיק את מבנה האשכולות.",
    "כלים וסימולציות שני: הצומת שממיר תנועת מידע לתנועת מוצר.",
    "איך זה עובד שלישי: מסיר חסם אמון לפני ההרשמה.",
    "לעורכי דין רביעי: קהל משני, לא מתחרה על תשומת הלב של הקהל הראשי.",
    "ידע משפטי אחרון: ארכיון עומק לתמיכה בסמכות ובקישור פנימי.",
  ],
  conversionLogic: [
    "CTA ראשי אחיד ״התחילו סימולציה״ מופיע בכותרת, מעל הקיפול ובסיום — בלי וריאציות מתחרות.",
    "CTA משני ״מצאו את המסלול שלכם״ מיועד למי שעדיין לא יודע לאיזה תרחיש הוא שייך.",
    "בחירת תרחיש היא מיקרו־המרה: היא כבר מייצרת מחויבות לפני מסך ההרשמה.",
    "בלוקי אמון ממוקמים לפני ה‑CTA הסוגר, כמענה להתנגדות ״האם זה אמין״.",
  ],
};

const handoff = {
  tokens: [
    { name: "--color-primary", value: "oklch(0.78 0.14 200)", usage: "כפתור ראשי, קישורים הקשריים" },
    { name: "--color-background", value: "oklch(0.19 0.035 258)", usage: "רקע דיו כהה" },
    { name: "--color-card", value: "oklch(0.24 0.04 260)", usage: "כרטיסי תוכן ותצוגת מוצר" },
    { name: "--color-highlight", value: "oklch(0.83 0.15 195)", usage: "מצבי hover ומספור שלבים" },
    { name: "--radius", value: "0.9rem", usage: "רדיוס אחיד לכרטיסים ולכפתורים" },
    { name: "--font-sans", value: "Heebo", usage: "כל טקסט הממשק בעברית" },
  ],
  blocks: [
    { name: "Hero / בורר תרחישים", desc: "בלוק סינכרוני: כפתורי תרחיש + כרטיס תצוגה מקדימה" },
    { name: "Content Card Grid", desc: "כרטיס תוכן עם כותרת, כוונת חיפוש וקישור הקשרי" },
    { name: "Steps 1-2-3", desc: "בלוק שלבים ממוספר, נשלף גם לעמודי כלי" },
    { name: "Trust Stack", desc: "חמישה בלוקי אמון קבועים לכל תבנית" },
    { name: "CTA Band", desc: "פס סיום עם CTA ראשי ומשני" },
  ],
  menu: [
    { label: "תחומי משפט", children: ["משפחה", "פלילי", "אזרחי", "עבודה"] },
    {
      label: "כלים וסימולציות",
      children: ["חקירת עדים", "הכנה לדיון", "סימולציית משא ומתן"],
    },
    { label: "איך זה עובד", children: ["מתודולוגיה", "פרטיות ואבטחה", "מגבלות"] },
    { label: "לעורכי דין", children: ["שיתופי פעולה", "שימוש מקצועי"] },
    { label: "ידע משפטי", children: ["מדריכים", "מונחים", "שאלות נפוצות"] },
  ],
  schema: [
    "WebSite + SearchAction בעמוד הבית",
    "HowTo בעמודי הכנה לדיון וחקירת עדים",
    "FAQPage רק כשהשאלות מוצגות בפועל בעמוד",
    "BreadcrumbList בכל עמוד פנימי",
    "Article עם datePublished, dateModified ו‑reviewedBy לאחר מילוי הבודק",
  ],
  performance: [
    "טעינת גופנים דרך preconnect + font-display: swap; מקסימום שני משקלים לעמוד",
    "ללא סליידרים או ספריות אנימציה כבדות; מעברי CSS בלבד",
    "תמונות WebP עם width/height מפורשים ו‑lazy מתחת לקיפול",
    "יעד: LCP מתחת ל‑2.5 שניות במובייל, CLS מתחת ל‑0.1",
    "Critical CSS מוטבע לחלק העליון; שאר הסגנון נדחה",
  ],
};

