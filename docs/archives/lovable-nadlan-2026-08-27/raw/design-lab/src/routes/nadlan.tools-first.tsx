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

export const Route = createFileRoute("/nadlan/tools-first")({
  head: () => ({
    meta: [
      { title: "N1 · כלים תחילה — קונספט עמוד בית לאתר נדל״ן" },
      {
        name: "description",
        content:
          "קונספט עמוד בית כמרכז כלים: משגר מחשבונים מעל הקיפול, חותמת עדכון כללים, תוצאה הניתנת לשיתוף ובעלות נפרדת לכל כלי.",
      },
      { property: "og:title", content: "N1 · כלים תחילה — נדל״ן" },
      {
        property: "og:description",
        content: "משגר מחשבונים, חותמת עדכון ותוצאה לשיתוף.",
      },
    ],
  }),
  component: N1,
});

const launcher = [
  { id: "purchase", label: "מס רכישה", href: "/nadlan/tools/purchase-tax-calculator" },
  { id: "sim", label: "סימולטור מס רכישה", href: "/nadlan/tools/purchase-tax-simulator" },
  { id: "gains", label: "מס שבח", href: "/nadlan/tools/capital-gains-calculator" },
  { id: "tabu", label: "נסח טאבו", href: "/nadlan/tools/tabu-extract" },
];

function N1() {
  const [selected, setSelected] = useState(launcher[0]!.id);
  const active = launcher.find((l) => l.id === selected)!;

  return (
    <ConceptFrame id="n1" annotation={annotation} handoff={handoff}>
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
          <div className="grid gap-10 lg:grid-cols-[1fr_1fr]">
            <div>
              <Tag>מרכז כלים לנדל״ן בישראל</Tag>
              <h1 className="display mt-4 text-3xl leading-tight md:text-5xl">
                מחשבונים וכלי בדיקה לנדל״ן — תשובה מדויקת לפני ההחלטה
              </h1>
              <p className="mt-4 max-w-xl text-lg leading-relaxed text-muted-foreground">
                כל כלי עומד בפני עצמו, מציג את הכללים שעליהם הוא מסתמך ואת מועד העדכון
                האחרון, כדי שתדעו בדיוק על מה מבוסס החישוב.
              </p>
              <div className="mt-7 flex flex-wrap gap-3">
                <Cta>חשבו מס רכישה</Cta>
                <Cta variant="secondary">בדקו נכס לפני החלטה</Cta>
              </div>
              <p className="mt-5 text-sm text-muted-foreground">
                מדרגות ונתוני חישוב מתעדכנים לפי הפרסום הרשמי. תאריך העדכון מוצג בכל כלי.
              </p>
            </div>

            <Card>
              <div className="flex items-center justify-between gap-3">
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
                        "tap rounded-lg px-4 py-3 text-sm font-semibold " +
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
                <div className="flex items-center justify-between">
                  <h3 className="font-bold">תצוגת תוצאה · {active.label}</h3>
                  <span className="text-xs text-muted-foreground">עודכן: דוגמה</span>
                </div>
                <dl className="mt-3 grid grid-cols-2 gap-3 text-sm">
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
            lead="כל כלי מחזיק כוונת חיפוש משלו. אין עמוד ״מחשבון כללי״ שמאחד ביניהם."
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
            eyebrow="הקשר"
            title="מדריכים שמסבירים את מה שהמחשבון מחשב"
            lead="הכלי נותן מספר; המדריך מסביר מה עומד מאחוריו ואיך זה משפיע על ההחלטה."
          />
          <ul className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {nadlanPillars.map((p) => (
              <Card as="li" key={p.title}>
                <h3 className="font-bold">{p.title}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{p.desc}</p>
                <div className="mt-3">
                  <ContextLink href={p.href}>קראו את המדריך</ContextLink>
                </div>
              </Card>
            ))}
          </ul>
        </Section>

        <Section tone="surface">
          <SectionHead eyebrow="שקיפות" title="על מה מבוססים החישובים" />
          <TrustBlocks
            reviewer="בדיקת נוסחאות ומדרגות על ידי גורם מקצועי בתחום המיסוי — מציין מיקום לשיבוץ, טרם מולא."
            method="כל כלי מציג את שיטת החישוב, ההנחות והמקרים שאינם נתמכים."
            privacy="החישוב מתבצע ללא צורך בהרשמה; שמירת תוצאה היא בחירה של המשתמש."
            sourceDate="חותמת ״כללים נכונים לתאריך״ מוצגת בראש כל מחשבון."
            limits="התוצאה היא הערכה ואינה תחליף לבדיקה מול רשות המסים או יועץ מוסמך."
          />
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
    "עמוד הבית מוצב כצומת כלים: הוא מעביר סמכות פנימית ישירות לארבעת עמודי הכלי בעלי הביקוש הגבוה.",
    "כל כלי מקבל עמוד עצמאי כדי לא לפצל סיגנלים בין ביטויים שונים באותו עמוד.",
    "חותמת עדכון וטבלת מדרגות מספקות רעננות ותוכן ייחודי שקשה להעתיק.",
  ],
  keywordOwner: [
    "נסח טאבו — עמוד כלי משלו, כוונה: הפקה וקריאה של נסח.",
    "מחשבון מס רכישה — כוונת חישוב בודדת.",
    "סימולטור מס רכישה — כוונת השוואת תרחישים, נפרדת מהמחשבון.",
    "מחשבון מס שבח — כוונת מכירה, פטורים וחישוב ליניארי; לעולם לא ממוזג עם מס רכישה.",
    "המדריכים מחזיקים ביטויי ״מה זה / איך״ ומזינים את הכלים בקישור פנימי.",
  ],
  menuLogic: [
    "כלים ומחשבונים ראשון: הביקוש הגבוה והכוונה הממירה ביותר.",
    "קנייה ומכירה שני: הקשר העסקה שממנו נגזרים כל הכלים.",
    "משכנתאות שלישי: שלב מימון שמגיע אחרי הבנת העלות.",
    "בדיקות נכס רביעי: שלב האימות לפני חתימה.",
    "מדריכים ומילון בסוף: עומק תוכן שתומך בקישור פנימי אל הכלים.",
  ],
  conversionLogic: [
    "ההמרה היא שימוש בכלי, לא ליד: משגר הכלים מעל הקיפול מקצר את הדרך לפעולה.",
    "תוצאה הניתנת לשיתוף מייצרת חזרה לאתר ושימוש חוזר.",
    "CTA משני ״בדקו נכס לפני החלטה״ קולט מבקרים שעדיין לא בשלב החישוב.",
    "אין באנרים פרסומיים; הכלי עצמו הוא ההצעה.",
  ],
};

const handoff = {
  tokens: [
    { name: "--color-primary", value: "oklch(0.48 0.12 235)", usage: "כפתורי כלי וכפתור ראשי" },
    { name: "--color-highlight", value: "oklch(0.6 0.11 190)", usage: "מבטא טורקיז לתוצאות" },
    { name: "--color-surface", value: "oklch(0.96 0.012 218)", usage: "רקע לוחות תוצאה" },
    { name: "--radius", value: "0.6rem", usage: "פינות ממשק כלי" },
    { name: "--font-mono", value: "IBM Plex Mono", usage: "מספרים וטבלאות מדרגות" },
  ],
  blocks: [
    { name: "Tool Launcher", desc: "בורר כלים + כרטיס תצוגת תוצאה" },
    { name: "Rule Timestamp", desc: "שורת ״כללים נכונים לתאריך״ לשימוש בכל מחשבון" },
    { name: "Tool Card", desc: "כרטיס כלי עם כוונת חיפוש והבהרת בעלות" },
    { name: "Bracket Table", desc: "טבלת מדרגות רספונסיבית עם גלילה אופקית" },
    { name: "Shareable Result", desc: "בלוק תוצאה עם קישור שיתוף" },
  ],
  menu: [
    {
      label: "כלים ומחשבונים",
      children: ["מחשבון מס רכישה", "סימולטור מס רכישה", "מחשבון מס שבח", "נסח טאבו"],
    },
    { label: "קנייה ומכירה", children: ["שלבי עסקה", "חוזה ומסמכים"] },
    { label: "משכנתאות", children: ["תמהיל", "אישור עקרוני"] },
    { label: "בדיקות נכס", children: ["רישום", "תכנון ובנייה", "מצב פיזי"] },
    { label: "מדריכים", children: ["מיסוי", "תהליכים"] },
    { label: "מילון נדל״ן", children: ["מונחים לפי א׳-ב׳"] },
  ],
  schema: [
    "WebApplication או SoftwareApplication לכל עמוד מחשבון בנפרד",
    "HowTo בעמוד נסח טאבו",
    "BreadcrumbList בכל עמוד כלי ומדריך",
    "DefinedTerm בערכי המילון, עם קישור לכלי",
    "dateModified אמיתי בכל עמוד מחשבון",
  ],
  performance: [
    "חישוב בצד הלקוח בלבד; ללא קריאות שרת לכל הקלדה",
    "טעינת לוגיקת המחשבון רק בעמוד הכלי ולא בעמוד הבית",
    "טבלאות מדרגות ב‑HTML סטטי, נגישות לסריקה",
    "יעד LCP מתחת ל‑2.5 שניות במובייל בחיבור סלולרי",
    "ללא ספריות תרשימים כבדות; SVG פשוט בלבד",
  ],
};

