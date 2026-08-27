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
import { nadlanMenu, nadlanTools } from "@/lib/lab-data";

export const Route = createFileRoute("/nadlan/map-first")({
  head: () => ({
    meta: [
      { title: "N2 · מפה והחלטה — קונספט עמוד בית לאתר נדל״ן" },
      {
        name: "description",
        content:
          "קונספט מונחה מסע: ״איפה אתם בתהליך?״, אזור חיפוש ומפה, רשימת בדיקות נכס וכלים שמשובצים בדיוק ברגעי ההחלטה.",
      },
      { property: "og:title", content: "N2 · מפה והחלטה — נדל״ן" },
      {
        property: "og:description",
        content: "מסע החלטה עם בדיקות נכס וכלים ברגע הנכון.",
      },
    ],
  }),
  component: N2,
});

const stages = [
  {
    id: "explore",
    label: "בודקים אזור",
    task: "מבינים מה יש באזור, מה נבנה בסביבה ומה משפיע על שווי לאורך זמן.",
    tool: { label: "פתחו את מדריך בדיקות נכס", href: "/nadlan/guides/due-diligence" },
    checks: ["תוכניות בנייה בסביבה", "נגישות ותחבורה", "מגמות באזור"],
  },
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
    id: "sell",
    label: "מוכרים דירה",
    task: "בודקים חבות במס שבח, פטורים אפשריים והשפעת מועד המכירה.",
    tool: { label: "חשבו מס שבח", href: "/nadlan/tools/capital-gains-calculator" },
    checks: ["חישוב שבח", "בדיקת פטור", "מועד ותכנון מכירה"],
  },
];

function N2() {
  const [stage, setStage] = useState(stages[0]!);

  return (
    <ConceptFrame id="n2" annotation={annotation} handoff={handoff}>
      <SiteHeader
        brand="נדל״ן"
        menu={nadlanMenu}
        primaryCta="חשבו מס רכישה"
        secondaryCta="בדקו נכס לפני החלטה"
      />

      <main id="main">
        <div className="lab-container pt-6">
          <Breadcrumbs trail={["דף הבית", "בדיקות נכס", "בדיקה לפני חוזה"]} />
        </div>

        <Section className="pt-8">
          <Tag>מסע החלטה מלווה</Tag>
          <h1 className="display mt-4 max-w-3xl text-3xl leading-tight md:text-5xl">
            איפה אתם בתהליך? — כל שלב עם הבדיקות והכלים שלו
          </h1>
          <p className="mt-4 max-w-2xl text-lg leading-relaxed text-muted-foreground">
            בוחרים את השלב שבו אתם נמצאים ומקבלים רשימת בדיקות ממוקדת, יחד עם הכלי
            שמתאים בדיוק להחלטה הבאה.
          </p>

          <div className="mt-8 grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
            <div>
              <fieldset>
                <legend className="text-sm font-bold">בחרו שלב</legend>
                <ul className="mt-3 space-y-2">
                  {stages.map((s) => (
                    <li key={s.id}>
                      <button
                        type="button"
                        onClick={() => setStage(s)}
                        aria-pressed={stage.id === s.id}
                        className={
                          "tap w-full rounded-xl px-4 py-3 text-start text-sm font-semibold " +
                          (stage.id === s.id
                            ? "bg-primary text-primary-foreground"
                            : "border border-border bg-card text-card-foreground hover:bg-secondary")
                        }
                      >
                        {s.label}
                      </button>
                    </li>
                  ))}
                </ul>
              </fieldset>
              <div className="mt-4 flex flex-wrap gap-3">
                <Cta>חשבו מס רכישה</Cta>
                <Cta variant="secondary">בדקו נכס לפני החלטה</Cta>
              </div>
            </div>

            <Card>
              <div className="flex items-center justify-between gap-3">
                <h2 className="display text-lg">{stage.label}</h2>
                <ExampleBadge />
              </div>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{stage.task}</p>

              <div
                role="img"
                aria-label="תרשים סכמטי של אזור חיפוש עם סימוני נכסים — להמחשה בלבד"
                className="mt-4 h-40 rounded-xl border border-border bg-[repeating-linear-gradient(45deg,transparent,transparent_12px,color-mix(in_oklab,var(--highlight)_14%,transparent)_12px,color-mix(in_oklab,var(--highlight)_14%,transparent)_24px)]"
              />
              <p className="mt-2 text-xs text-muted-foreground">
                תצוגת מפה סכמטית. אין כאן נכסים אמיתיים או מחירים.
              </p>

              <h3 className="mt-5 font-bold">רשימת בדיקה לשלב זה</h3>
              <ul className="mt-2 space-y-2">
                {stage.checks.map((c) => (
                  <li
                    key={c}
                    className="flex items-start gap-2 rounded-lg bg-surface p-3 text-sm text-surface-foreground"
                  >
                    <span aria-hidden="true">☐</span>
                    {c}
                  </li>
                ))}
              </ul>
              <div className="mt-4">
                <ContextLink href={stage.tool.href}>{stage.tool.label}</ContextLink>
              </div>
            </Card>
          </div>
        </Section>

        <Section tone="surface">
          <SectionHead
            eyebrow="כלים"
            title="הכלים משובצים בתהליך — וכל אחד עומד בפני עצמו"
            lead="גם כשכלי מופיע בתוך שלב במסע, עמוד הבית שלו נשאר יעד עצמאי עם כוונת חיפוש נפרדת."
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
            eyebrow="בדיקות נכס"
            title="מה בודקים לפני שמתחייבים"
            lead="רשימה מלאה, מסודרת לפי תחומים, שאפשר לעבור איתה מול נכס אמיתי."
          />
          <div className="grid gap-4 md:grid-cols-3">
            {[
              { t: "רישום וזכויות", i: ["נסח רישום", "הערות אזהרה", "בעלות ושעבודים"] },
              { t: "תכנון ובנייה", i: ["היתרים", "חריגות", "תוכניות בסביבה"] },
              { t: "מצב פיזי וכספי", i: ["ליקויים", "חובות ועד ורשות", "עלויות צפויות"] },
            ].map((g) => (
              <Card key={g.t}>
                <h3 className="font-bold">{g.t}</h3>
                <ul className="mt-2 space-y-1 text-sm text-muted-foreground">
                  {g.i.map((x) => (
                    <li key={x}>· {x}</li>
                  ))}
                </ul>
              </Card>
            ))}
          </div>
          <div className="mt-6">
            <ContextLink href="/nadlan/guides/due-diligence">
              קראו את מדריך הבדיקות המלא לפני חתימה
            </ContextLink>
          </div>
        </Section>

        <Section tone="surface">
          <SectionHead eyebrow="שקיפות" title="מה הכלים כאן כן ולא עושים" />
          <TrustBlocks
            reviewer="בדיקת תוכן ונוסחאות על ידי גורם מקצועי — מציין מיקום לשיבוץ, טרם מולא."
            method="מוסבר כיצד נבנו רשימות הבדיקה ומאילו שלבים בעסקה הן נגזרות."
            privacy="אין צורך בהרשמה כדי להשתמש ברשימות ובמחשבונים."
            sourceDate="כל רשימה וכל מחשבון נושאים תאריך עדכון ובדיקת מקורות."
            limits="אין באתר נכסים למכירה, מחירי שוק או הבטחת חיסכון. הכלים מסייעים בהחלטה בלבד."
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
    "המסע ממפה כוונות לפי שלב בעסקה, ומייצר קישור פנימי מדויק מעמוד הבית אל הכלי הרלוונטי לכל שלב.",
    "רשימות הבדיקה הן תוכן ייחודי שקולט ביטויי ״מה בודקים לפני קניית דירה״.",
    "המפה היא המחשה בלבד — אין יומרה לתפוס כוונת חיפוש של לוח נכסים.",
  ],
  keywordOwner: [
    "בדיקות נכס — עמוד־אב עצמאי, לא חלק מעמוד מחשבון.",
    "נסח טאבו — עמוד כלי נפרד; במסע הוא מופיע כהפניה, לא כתוכן משוכפל.",
    "מחשבון מס רכישה וסימולטור מס רכישה — שני עמודים נפרדים עם כוונות שונות.",
    "מחשבון מס שבח — שייך לשלב המכירה בלבד ואינו מעורבב בשלב הרכישה.",
  ],
  menuLogic: [
    "התפריט משקף את סדר העסקה בפועל, מהכלי הממיר ביותר ועד לעומק התוכן.",
    "בדיקות נכס מקבל מקום בתפריט הראשי כי הוא נושא ביקוש עצמאי ולא רק שלב במסע.",
    "מילון נדל״ן אחרון: מזין קישור פנימי אך אינו יעד כניסה ראשי.",
  ],
  conversionLogic: [
    "בחירת שלב היא מיקרו־המרה שמצמצמת עומס ומגדילה סיכוי לשימוש בכלי.",
    "הכלי מוצג ברגע ההחלטה ולא כבאנר — ההקשר הוא שמייצר את הקליק.",
    "רשימת הבדיקה מייצרת ערך מיידי וסיבה לשוב לאתר לאורך העסקה.",
    "CTA ראשי נשאר ״חשבו מס רכישה״ בכל השלבים לצורך עקביות מדידה.",
  ],
};

const handoff = {
  tokens: [
    { name: "--color-primary", value: "oklch(0.42 0.09 205)", usage: "כפתורי שלב ו‑CTA ראשי" },
    { name: "--color-highlight", value: "oklch(0.58 0.11 160)", usage: "סימוני מפה ואישור" },
    { name: "--color-surface", value: "oklch(0.955 0.016 165)", usage: "פריטי רשימת בדיקה" },
    { name: "--radius", value: "1.1rem", usage: "כרטיסים רכים למסע" },
    { name: "--font-sans", value: "Heebo", usage: "כל הטקסט" },
  ],
  blocks: [
    { name: "Journey Selector", desc: "רשימת שלבים עם aria-pressed ופאנל תוכן" },
    { name: "Checklist", desc: "רשימת בדיקה לשלב, ניתנת לשכפול לכל עמוד מדריך" },
    { name: "Schematic Map", desc: "בלוק המחשה עם aria-label, ללא נתונים אמיתיים" },
    { name: "Tool Card", desc: "כרטיס כלי עם הבהרת בעלות" },
    { name: "Trust Stack", desc: "בלוקי אמון קבועים" },
  ],
  menu: [
    { label: "כלים ומחשבונים", children: ["מס רכישה", "סימולטור", "מס שבח", "נסח טאבו"] },
    { label: "קנייה ומכירה", children: ["שלבי קנייה", "שלבי מכירה"] },
    { label: "משכנתאות", children: ["תמהיל", "מסמכים"] },
    { label: "בדיקות נכס", children: ["רישום", "תכנון ובנייה", "מצב פיזי"] },
    { label: "מדריכים", children: ["לפני חתימה", "מיסוי"] },
    { label: "מילון נדל״ן", children: ["מונחים"] },
  ],
  schema: [
    "HowTo לרשימות הבדיקה לפי שלב",
    "ItemList למסע השלבים בעמוד הבית",
    "WebApplication לכל מחשבון בעמוד שלו",
    "BreadcrumbList בכל עמוד פנימי",
    "ללא Product או Offer — אין נכסים ואין מחירים",
  ],
  performance: [
    "המפה היא CSS/SVG בלבד; ללא ספריית מפות בעמוד הבית",
    "רשימות הבדיקה מוגשות כ‑HTML ולא נטענות בסקריפט",
    "טעינה עצלה לכל תוכן מתחת לקיפול",
    "יעד CLS מתחת ל‑0.1: גובה קבוע לאזור התצוגה",
    "אנימציות מבוטלות תחת prefers-reduced-motion",
  ],
};

