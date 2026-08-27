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
import { justiceCards, justiceMenu } from "@/lib/lab-data";

export const Route = createFileRoute("/justice/authority-first")({
  head: () => ({
    meta: [
      { title: "J2 · סמכות תוכן — קונספט עמוד בית ל‑jus-tice.co.il" },
      {
        name: "description",
        content:
          "קונספט עריכתי לעמוד הבית: סמכות מקצועית גלויה מעל הקיפול, מבנה תוכן ידידותי לתוצאות חיפוש והובלה מסודרת אל הכלים והסימולציה.",
      },
      { property: "og:title", content: "J2 · סמכות תוכן — Justice" },
      {
        property: "og:description",
        content: "אמינות ו‑E-E-A-T גלויים מעל הקיפול, ומשם אל הכלים.",
      },
    ],
  }),
  component: J2,
});

const domains = [
  { t: "דיני משפחה", d: "גירושין, הסכמים, משמורת ומזונות — מה נקבע ומתי." },
  { t: "פלילי", d: "מהליך החקירה ועד רישום פלילי ואפשרויות מחיקה." },
  { t: "אזרחי וכספי", d: "תביעות, חוזים והתנהלות מול בית המשפט." },
  { t: "עבודה", d: "סיום העסקה, זכויות, שימוע וטענות נפוצות." },
];

function J2() {
  return (
    <ConceptFrame id="j2" annotation={annotation} handoff={handoff}>
      <SiteHeader
        brand="Justice"
        menu={justiceMenu}
        primaryCta="התחילו סימולציה"
        secondaryCta="מצאו את המסלול שלכם"
      />

      <main id="main">
        <div className="lab-container pt-6">
          <Breadcrumbs trail={["דף הבית", "ידע משפטי", "מדריכי הכנה"]} />
        </div>

        <Section className="pt-8">
          <div className="grid gap-10 lg:grid-cols-[1.15fr_0.85fr]">
            <div>
              <Tag>מרכז ידע משפטי בעברית</Tag>
              <h1 className="display mt-4 text-3xl leading-tight md:text-5xl">
                מדריכי הכנה משפטית בעברית — כתובים לבירור, לא לשיווק
              </h1>
              <p className="mt-5 max-w-2xl text-lg leading-relaxed text-muted-foreground">
                כל מדריך מסביר מה קורה בפועל בהליך, אילו החלטות עומדות בפניכם ומה כדאי
                לברר לפני שמתקדמים. בסוף כל נושא נמצא התרגול המתאים — סימולציה שמאפשרת
                לתרגל את מה שקראתם.
              </p>
              <dl className="mt-7 grid gap-3 sm:grid-cols-3">
                {[
                  { k: "בדיקה מקצועית", v: "עורך/ת דין — מציין מיקום לשיבוץ" },
                  { k: "עדכון אחרון", v: "מוצג בראש כל מדריך" },
                  { k: "מקורות", v: "חקיקה ופסיקה, עם תאריך בדיקה" },
                ].map((i) => (
                  <div key={i.k} className="rounded-md border border-border bg-card p-3">
                    <dt className="text-xs font-bold text-muted-foreground">{i.k}</dt>
                    <dd className="mt-1 text-sm font-medium">{i.v}</dd>
                  </div>
                ))}
              </dl>
              <div className="mt-7 flex flex-wrap gap-3">
                <Cta>התחילו סימולציה</Cta>
                <Cta variant="secondary">מצאו את המסלול שלכם</Cta>
              </div>
            </div>

            <Card>
              <h2 className="display text-lg">התחילו מהנושא שלכם</h2>
              <ul className="mt-4 divide-y divide-border">
                {domains.map((d) => (
                  <li key={d.t} className="py-3">
                    <a
                      href="#"
                      className="tap block rounded-md px-1 py-1 hover:bg-secondary hover:text-secondary-foreground"
                    >
                      <span className="font-bold">{d.t}</span>
                      <span className="mt-1 block text-sm text-muted-foreground">{d.d}</span>
                    </a>
                  </li>
                ))}
              </ul>
              <p className="mt-3 text-xs text-muted-foreground">
                כל תחום הוא עמוד עמוד־אב, ומתחתיו מדריכים ממוקדים.
              </p>
            </Card>
          </div>
        </Section>

        <Section tone="surface">
          <SectionHead
            eyebrow="מדריכים מובילים"
            title="הנושאים שהכי מחפשים — עם המשך תרגול"
            lead="כל מדריך עומד בפני עצמו בתוצאות החיפוש, ומקשר פנימה לשלב הרלוונטי בסימולציה."
          />
          <ul className="grid gap-4 md:grid-cols-2">
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
            eyebrow="עריכה ובקרה"
            title="איך נכתב התוכן כאן"
            lead="שרשרת הכתיבה גלויה, כדי שאפשר יהיה לשפוט את התוכן לפי מה שעומד מאחוריו."
          />
          <ol className="grid gap-4 md:grid-cols-4">
            {[
              { t: "מיפוי שאלה", d: "מזהים מה בדיוק מחפשים ובאיזה שלב של ההליך." },
              { t: "כתיבה מבוססת מקור", d: "מסתמכים על חקיקה ופסיקה, עם הפניה מדויקת." },
              { t: "בדיקה מקצועית", d: "עורך/ת דין בודק/ת את הדיוק — שם ותאריך יוצגו." },
              { t: "עדכון תקופתי", d: "כל מדריך נבדק שוב ומקבל תאריך עדכון חדש." },
            ].map((s, i) => (
              <Card as="li" key={s.t}>
                <p className="font-mono text-sm text-muted-foreground">0{i + 1}</p>
                <h3 className="mt-1 font-bold">{s.t}</h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{s.d}</p>
              </Card>
            ))}
          </ol>
          <div className="mt-6">
            <ContextLink href="/justice/editorial-policy">
              קראו את מדיניות העריכה המלאה
            </ContextLink>
          </div>
        </Section>

        <Section tone="surface">
          <SectionHead eyebrow="שקיפות" title="מה חשוב לדעת לפני שמסתמכים על התוכן" />
          <TrustBlocks
            reviewer="כל מדריך נושא שדה ״נבדק על ידי״ עם שם, תחום התמחות ותאריך — מציין מיקום, טרם מולא."
            method="מוסבר כיצד נבחרים הנושאים, אילו מקורות נכללים ומה נשאר מחוץ להיקף."
            privacy="קריאה אינה דורשת הרשמה. שימוש בסימולציה מוסבר בנפרד, כולל שמירה ומחיקה."
            sourceDate="בראש כל מדריך מוצגים תאריך פרסום, תאריך עדכון ותאריך בדיקת מקורות."
            limits="התוכן הוא הסבר כללי ואינו ייעוץ משפטי פרטני להליך שלכם."
          />
        </Section>

        <Section>
          <div className="rounded-md border-2 border-primary bg-card p-8 text-card-foreground">
            <h2 className="display text-2xl">קראתם — עכשיו אפשר לתרגל</h2>
            <p className="mt-3 max-w-xl text-muted-foreground">
              הסימולציה לוקחת את מה שלמדתם והופכת אותו לתרגול של רגעי ההחלטה עצמם.
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
    "עמוד הבית מתפקד כצומת סמכות: הוא מקשר לעמודי־אב נושאיים ולמדריכים, ומחזק את הרלוונטיות הנושאית של הדומיין.",
    "אותות E-E-A-T (בודק מקצועי, תאריך עדכון, מקורות) מוצגים מעל הקיפול ולא נקברים בפוטר.",
    "טקסט עשיר ומובנה מעל הקיפול משפר התאמה לתקצירי תוצאות חיפוש בעברית.",
  ],
  keywordOwner: [
    "jus-tice.co.il מחזיק כאן את הביטויים ההסברתיים: ״מה זה…״, ״כמה עולה…״, ״איך מתכוננים ל…״.",
    "מונחי מוצר (סימולטור, סביבת עבודה, מרקטפלייס) שייכים ל‑jus-tice.com בלבד.",
    "עמוד־אב אחד לכל תחום משפט; מדריכים ממוקדים לא מתחרים בו על אותו ביטוי.",
  ],
  menuLogic: [
    "תחומי משפט פותח את התפריט כי הוא שער הכניסה הנושאי הרחב.",
    "כלים וסימולציות מיד אחריו, כדי שקורא תוכן ימצא את המעבר למוצר בלי חיפוש.",
    "איך זה עובד מספק הצדקה מתודולוגית לתוכן ולכלי כאחד.",
    "לעורכי דין מופרד כדי לא לבלבל קהל פרטי.",
    "ידע משפטי סוגר כארכיון עומק שמאכלס קישור פנימי לעמודי־האב.",
  ],
  conversionLogic: [
    "ההמרה נבנית אחרי אמון: המדריך משכנע, והקישור ההקשרי מעביר לתרגול בנקודה הרלוונטית.",
    "CTA ראשי חוזר בראש ובסוף בלבד — בלי באנרים חוזרים שמפריעים לקריאה.",
    "CTA משני משרת מבקרים ללא נושא ברור ומונע נטישה.",
    "אין מספרים או עדויות: האמון נשען על מקורות, תאריכים ובדיקה מקצועית.",
  ],
};

const handoff = {
  tokens: [
    { name: "--color-background", value: "oklch(0.975 0.014 90)", usage: "רקע שנהב חם" },
    { name: "--color-primary", value: "oklch(0.28 0.06 262)", usage: "כותרות וכפתור ראשי" },
    { name: "--color-highlight", value: "oklch(0.62 0.1 75)", usage: "מבטא פליז מאופק" },
    { name: "--radius", value: "0.35rem", usage: "פינות עריכתיות מרוסנות" },
    { name: "--font-display", value: "Frank Ruhl Libre", usage: "כותרות H1/H2" },
    { name: "--font-sans", value: "Heebo", usage: "גוף הטקסט" },
  ],
  blocks: [
    { name: "Editorial Hero", desc: "H1, פסקת פתיחה ושורת אותות אמון" },
    { name: "Topic Index", desc: "רשימת עמודי־אב עם תיאור קצר" },
    { name: "Guide Card", desc: "כרטיס מדריך עם כוונת חיפוש וקישור הקשרי" },
    { name: "Editorial Process", desc: "ארבעה שלבי כתיבה ובקרה" },
    { name: "Review Byline", desc: "נכתב על ידי / נבדק על ידי / עודכן בתאריך" },
  ],
  menu: [
    { label: "תחומי משפט", children: ["משפחה", "פלילי", "אזרחי", "עבודה"] },
    { label: "כלים וסימולציות", children: ["הכנה לדיון", "חקירת עדים"] },
    { label: "איך זה עובד", children: ["מדיניות עריכה", "מקורות", "מגבלות"] },
    { label: "לעורכי דין", children: ["בדיקת תוכן", "שיתופי פעולה"] },
    { label: "ידע משפטי", children: ["מדריכים", "מונחים", "עדכוני חקיקה"] },
  ],
  schema: [
    "Organization + WebSite בעמוד הבית",
    "Article עם author, reviewedBy, datePublished, dateModified בכל מדריך",
    "BreadcrumbList לכל עמוד־אב ומדריך",
    "FAQPage רק כשהשאלות מופיעות בעמוד",
    "ללא Review או AggregateRating — אין דירוגים באתר",
  ],
  performance: [
    "עמודי תוכן סטטיים עם קאשינג מלא בשרת",
    "גופן כותרת במשקל אחד בלבד, טעינה עם swap",
    "ללא סקריפטים חיצוניים מעל הקיפול; אנליטיקה נדחית",
    "תוכן טקסטואלי מוגש ב‑HTML ולא נבנה בג׳אווהסקריפט",
    "יעד INP מתחת ל‑200ms; קישורים אמיתיים ולא כפתורים מדומים",
  ],
};

