import { createFileRoute } from "@tanstack/react-router";
import { ConceptFrame } from "@/components/lab/ConceptFrame";
import {
  Breadcrumbs,
  Card,
  ContextLink,
  Cta,
  Section,
  SectionHead,
  SiteHeader,
  Tag,
  TrustBlocks,
} from "@/components/lab/primitives";
import { nadlanMenu, nadlanPillars, nadlanTools } from "@/lib/lab-data";

export const Route = createFileRoute("/nadlan/authority-first")({
  head: () => ({
    meta: [
      { title: "N3 · סמכות תוכן — קונספט עמוד בית לאתר נדל״ן" },
      {
        name: "description",
        content:
          "קונספט עריכתי לאתר נדל״ן: עמודי תוכן חזקים, מילון מונחים שמקשר לכלים, ומחשבונים שמקודמים בהקשר ולא כבאנרים.",
      },
      { property: "og:title", content: "N3 · סמכות תוכן — נדל״ן" },
      {
        property: "og:description",
        content: "עמודי תוכן ומילון שמזינים את המחשבונים בקישור פנימי.",
      },
    ],
  }),
  component: N3,
});

const glossary = [
  { term: "מס רכישה", desc: "מס המשולם על ידי הקונה לפי מדרגות ומצב הדירה.", href: "/nadlan/tools/purchase-tax-calculator", link: "חשבו מס רכישה" },
  { term: "מס שבח", desc: "מס על הרווח במכירת זכות במקרקעין, עם פטורים אפשריים.", href: "/nadlan/tools/capital-gains-calculator", link: "חשבו מס שבח" },
  { term: "נסח רישום מקרקעין", desc: "מסמך המרכז את פרטי הזכויות וההערות על הנכס.", href: "/nadlan/tools/tabu-extract", link: "פתחו את מדריך נסח טאבו" },
  { term: "הערת אזהרה", desc: "רישום המסמן התחייבות קיימת ביחס לנכס.", href: "/nadlan/guides/due-diligence", link: "קראו על בדיקות רישום" },
];

function N3() {
  return (
    <ConceptFrame id="n3" annotation={annotation} handoff={handoff}>
      <SiteHeader
        brand="נדל״ן"
        menu={nadlanMenu}
        primaryCta="חשבו מס רכישה"
        secondaryCta="בדקו נכס לפני החלטה"
      />

      <main id="main">
        <div className="lab-container pt-6">
          <Breadcrumbs trail={["דף הבית", "מדריכים", "מיסוי מקרקעין"]} />
        </div>

        <Section className="pt-8">
          <div className="grid gap-10 lg:grid-cols-[1.2fr_0.8fr]">
            <div>
              <Tag>מדריכי נדל״ן בעברית</Tag>
              <h1 className="display mt-4 text-3xl leading-tight md:text-5xl">
                מדריכי נדל״ן ומיסוי מקרקעין — הסבר מסודר לפני כל החלטה
              </h1>
              <p className="mt-5 max-w-2xl text-lg leading-relaxed text-muted-foreground">
                כל נושא נכתב כך שיענה על השאלה בפועל: מה קובע הכלל, מה משפיע עליו,
                ואיפה בדיוק נכנס החישוב. מהמדריך אפשר לעבור ישירות לכלי המתאים.
              </p>
              <div className="mt-7 flex flex-wrap gap-3">
                <Cta>חשבו מס רכישה</Cta>
                <Cta variant="secondary">בדקו נכס לפני החלטה</Cta>
              </div>
            </div>
            <Card>
              <h2 className="display text-lg">כלים לפי נושא</h2>
              <ul className="mt-3 divide-y divide-border">
                {nadlanTools.map((t) => (
                  <li key={t.title} className="py-3">
                    <p className="font-bold">{t.title}</p>
                    <p className="mt-1 text-xs text-muted-foreground">{t.note}</p>
                    <div className="mt-2">
                      <ContextLink href={t.href}>{t.linkLabel}</ContextLink>
                    </div>
                  </li>
                ))}
              </ul>
            </Card>
          </div>
        </Section>

        <Section tone="surface">
          <SectionHead
            eyebrow="עמודי תוכן"
            title="ארבעה עמודי־אב שמחזיקים את האתר"
            lead="כל עמוד־אב מרכז תת־נושאים, ומקשר החוצה לכלי הרלוונטי בנקודה שבה נדרש חישוב."
          />
          <ul className="grid gap-4 md:grid-cols-2">
            {nadlanPillars.map((p) => (
              <Card as="li" key={p.title} className="flex flex-col">
                <h3 className="display text-lg">{p.title}</h3>
                <p className="mt-2 flex-1 text-sm leading-relaxed text-muted-foreground">
                  {p.desc}
                </p>
                <div className="mt-4">
                  <ContextLink href={p.href}>המשיכו לעמוד הנושא</ContextLink>
                </div>
              </Card>
            ))}
          </ul>
        </Section>

        <Section>
          <SectionHead
            eyebrow="מילון נדל״ן"
            title="מונח, הסבר קצר — ומעבר לכלי"
            lead="המילון הוא רשת קישור פנימי: כל ערך מסביר מונח אחד ומוביל לפעולה שמתאימה לו."
          />
          <dl className="grid gap-4 md:grid-cols-2">
            {glossary.map((g) => (
              <Card key={g.term}>
                <dt className="font-bold">{g.term}</dt>
                <dd className="mt-2 text-sm text-muted-foreground">{g.desc}</dd>
                <dd className="mt-3">
                  <ContextLink href={g.href}>{g.link}</ContextLink>
                </dd>
              </Card>
            ))}
          </dl>
          <div className="mt-6">
            <ContextLink href="/nadlan/glossary">עברו למילון המונחים המלא</ContextLink>
          </div>
        </Section>

        <Section tone="surface">
          <SectionHead
            eyebrow="עריכה"
            title="איך נכתב ונבדק התוכן"
          />
          <ol className="grid gap-4 md:grid-cols-4">
            {[
              { t: "זיהוי השאלה", d: "מה בדיוק מחפשים ובאיזה שלב של העסקה." },
              { t: "מקורות רשמיים", d: "חקיקה ופרסומים רשמיים, עם הפניה מדויקת." },
              { t: "בדיקה מקצועית", d: "בדיקת דיוק על ידי גורם מוסמך — שם ותאריך יוצגו." },
              { t: "עדכון תקופתי", d: "שינויי כללים מעדכנים גם את המחשבון וגם את המדריך." },
            ].map((s, i) => (
              <Card as="li" key={s.t}>
                <p className="font-mono text-sm text-muted-foreground">0{i + 1}</p>
                <h3 className="mt-1 font-bold">{s.t}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{s.d}</p>
              </Card>
            ))}
          </ol>
        </Section>

        <Section>
          <SectionHead eyebrow="שקיפות" title="גבולות התוכן והחישוב" />
          <TrustBlocks
            reviewer="שדה ״נבדק על ידי״ עם שם, תפקיד ותאריך בכל מדריך ובכל מחשבון — מציין מיקום, טרם מולא."
            method="מוסבר אילו מקרים נכללים בחישוב ואילו דורשים בדיקה פרטנית."
            privacy="קריאה ושימוש בכלים אינם דורשים מסירת פרטים אישיים."
            sourceDate="תאריך עדכון אחרון ותאריך בדיקת מקורות מוצגים בראש כל עמוד."
            limits="התוכן הוא הסבר כללי ואינו ייעוץ מס, ייעוץ משפטי או המלצת השקעה."
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
    "עמוד הבית משמש מפת נושאים: הוא מחלק סמכות לעמודי־האב, והם מזרימים אותה לכלים.",
    "המילון מייצר כמות גדולה של עמודים ממוקדי מונח, שכולם מקשרים אל אותם ארבעה כלים.",
    "המבנה מטפל בבעיית ״מדורג אך נמוך״: עומק נושאי אמיתי במקום מאמרים בודדים ומפוזרים.",
  ],
  keywordOwner: [
    "עמודי־אב מחזיקים ביטויים רחבים: קנייה ומכירה, משכנתאות, בדיקות נכס.",
    "נסח טאבו — עמוד כלי נפרד, לא סעיף בתוך מדריך.",
    "מחשבון מס רכישה, סימולטור מס רכישה ומחשבון מס שבח — שלושה עמודים נפרדים לחלוטין.",
    "ערכי מילון לא מתחרים בעמודי הכלי: הם קצרים ומקשרים אליהם.",
  ],
  menuLogic: [
    "כלים ומחשבונים נשאר ראשון גם בקונספט תוכני, כי שם נמצאת הכוונה הממירה.",
    "מדריכים ומילון נמצאים בסוף התפריט ומתפקדים כמנוע קישור פנימי.",
    "כל פריט בתפריט מייצג אשכול תוכן שלם, לא עמוד בודד.",
  ],
  conversionLogic: [
    "המחשבונים מקודמים בתוך ההקשר הטקסטואלי, בנקודה שבה נדרש מספר.",
    "אין באנרים דביקים או חלונות קופצים — הקידום נעשה בקישור הקשרי בלבד.",
    "כרטיס ״כלים לפי נושא״ מעל הקיפול נותן קיצור דרך למי שהגיע כבר עם כוונה.",
    "אין חיסכון מובטח, אין נתוני עסקאות ואין המלצות — האמון נבנה מדיוק ומעדכניות.",
  ],
};

const handoff = {
  tokens: [
    { name: "--color-background", value: "oklch(0.965 0.016 95)", usage: "רקע קרם" },
    { name: "--color-primary", value: "oklch(0.27 0.012 100)", usage: "פחם לכותרות וכפתורים" },
    { name: "--color-accent", value: "oklch(0.9 0.05 145)", usage: "מבטא ירוק לקישורי כלי" },
    { name: "--radius", value: "0.25rem", usage: "פינות חדות בסגנון עריכתי" },
    { name: "--font-display", value: "Frank Ruhl Libre", usage: "כותרות" },
  ],
  blocks: [
    { name: "Pillar Grid", desc: "רשת עמודי־אב עם קישור המשך" },
    { name: "Glossary Entry", desc: "מונח, הסבר קצר וקישור לכלי" },
    { name: "Tool Sidebar", desc: "כרטיס ״כלים לפי נושא״ לשימוש חוזר בכל מדריך" },
    { name: "Editorial Process", desc: "ארבעה שלבי כתיבה ובקרה" },
    { name: "Review Byline", desc: "נכתב / נבדק / עודכן" },
  ],
  menu: [
    { label: "כלים ומחשבונים", children: ["מס רכישה", "סימולטור מס רכישה", "מס שבח", "נסח טאבו"] },
    { label: "קנייה ומכירה", children: ["מדריך קנייה", "מדריך מכירה"] },
    { label: "משכנתאות", children: ["תמהיל", "מסמכים", "אישור עקרוני"] },
    { label: "בדיקות נכס", children: ["רישום", "תכנון ובנייה", "מצב פיזי"] },
    { label: "מדריכים", children: ["מיסוי מקרקעין", "תהליכי עסקה"] },
    { label: "מילון נדל״ן", children: ["מונחים לפי א׳-ב׳"] },
  ],
  schema: [
    "Article עם author, reviewedBy ו‑dateModified בכל מדריך",
    "DefinedTermSet למילון, DefinedTerm לכל ערך",
    "WebApplication בעמודי המחשבונים בלבד",
    "BreadcrumbList בכל עמוד",
    "ללא AggregateRating או Review — אין דירוגים ואין המלצות",
  ],
  performance: [
    "עמודי תוכן סטטיים עם קאשינג מלא ותמונות WebP",
    "שני משקלי גופן לכל היותר",
    "ללא סקריפטים של צד שלישי מעל הקיפול",
    "קישורים פנימיים כ‑HTML רגיל לסריקה מלאה",
    "יעד LCP מתחת ל‑2.5 שניות ו‑INP מתחת ל‑200ms",
  ],
};

