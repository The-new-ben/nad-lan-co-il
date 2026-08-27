import { createFileRoute } from "@tanstack/react-router";
import { ProductionShell, type Impl } from "@/components/production/ProductionShell";
import {
  Band,
  BandHead,
  Chip,
  Crumbs,
  DemoBadge,
  InlineLink,
  Panel,
} from "@/components/production/ui";

export const Route = createFileRoute("/production/nadlan/meeting")({
  head: () => ({
    meta: [
      { title: "נרטיב פגישה — חמש דקות על מוצר נדל״ן" },
      {
        name: "description",
        content:
          "אינדקס פגישה: מה חי, מה אב טיפוס, מה נבדק בהמשך, מקרא מצבי נתונים, בעלות SEO, גלגל ההיצע וצ׳קליסט יישום.",
      },
      { property: "og:title", content: "נרטיב פגישה — חמש דקות" },
      { property: "og:description", content: "מסלול הצגה מסודר בין עמודי חבילת המוצר." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "robots", content: "noindex, nofollow" },
    ],
  }),
  component: MeetingIndex,
});

const stops = [
  {
    to: "/production/nadlan/properties",
    label: "1 · ארכיון נכסים",
    d: "חוויית החיפוש והסינון, ושלושת מצבי הנתונים כפי שמשתמש יראה אותם.",
  },
  {
    to: "/production/nadlan/properties/baka-demo",
    label: "2 · נכס לדוגמה",
    d: "עומק עמוד המודעה: מפרט, סביבה, עלויות, משכנתה ומסלולי המשך — הכול מסומן דוגמה.",
  },
  {
    to: "/production/nadlan/projects",
    label: "3 · ארכיון פרויקטים",
    d: "שכבת ה‑SEO הרחבה: ערים, יזמים וסטטוסים, עם מדיניות אינדוקס מפורשת.",
  },
  {
    to: "/production/nadlan/projects/rainbow-tel-aviv",
    label: "4 · Rainbow תל אביב",
    d: "עמוד ישות אמיתי על בסיס עובדות ציבוריות: שדה דב, 480 יחידות דיור.",
  },
];

const live = [
  "עמוד הבית של המוצר, ארכיון הנכסים וארכיון הפרויקטים — ניווט, סינון והשוואה עובדים.",
  "עמוד פרויקט Rainbow עם עובדות ציבוריות בלבד.",
  "מחשבון משכנתה שמחשב על קלט המשתמש.",
];

const proto = [
  "מסלול פרסום נכס — שלד שלבים, ללא טופס פעיל.",
  "תיאום ביקור והצעה לא מחייבת — מושבתים ומסומנים דוגמה.",
  "מפות ותלת־ממד — מסגרות שמורות שנטענות בלחיצה.",
];

const next = [
  "האם בעלי נכסים ומתווכים מוכנים לפרסם מלאי ראשון ללא עלות.",
  "האם עובדות פרויקט ציבוריות ניתנות לתחזוקה עם מקור ותאריך.",
  "אילו פאסטים מצדיקים אינדוקס לפי ביקוש חיפוש אמיתי.",
];

const flywheel = [
  { t: "תוכן ועובדות", d: "עמודי פרויקטים ומדריכים מביאים תנועה מחקרית מוקדמת." },
  { t: "כלים", d: "מחשבונים ובדיקות מחזיקים משתמשים לפני שיש מלאי." },
  { t: "היצע", d: "בעלים ומתווכים מפרסמים חינם ומחליפים את הדוגמאות." },
  { t: "ביקוש", d: "מלאי אמיתי מצדיק אינדוקס פאסטים ומייצר חיפוש חוזר." },
];

const checklist = [
  "CPT: project, listing, professional + טקסונומיות עיר/אזור/סוג עסקה.",
  "דגלי מקור בכל רשומה: source, updated_at, verified_at.",
  "סכימה מוזרקת רק כשה‑demo_flag כבוי.",
  "מדיניות אינדוקס פאסטים: עיר וסוג עסקה בלבד; השאר noindex,follow.",
  "ביצועים: תמונות רספונסיביות, ממדים שמורים, ללא וידאו אוטומטי, מפה בלחיצה.",
  "נגישות: H1 יחיד, מבנה כותרות, יעדי מגע 44px, ניווט מקלדת ו‑RTL מלא.",
];

function MeetingIndex() {
  return (
    <ProductionShell route="/production/nadlan/meeting" impl={impl}>
      <main id="main">
        <div className="lab-container pt-5">
          <Crumbs trail={[{ label: "דף הבית", to: "/production/nadlan" }, { label: "מצגת פגישה" }]} />
        </div>

        <Band className="pt-6" labelledBy="mt-h1">
          <Chip tone="copper">חמש דקות</Chip>
          <h1 id="mt-h1" className="display mt-4 text-3xl leading-tight md:text-4xl">
            נרטיב הפגישה — מחקר, גילוי, מודעה, היצע
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-muted-foreground">
            מסלול הצגה מסודר בין ארבעת העמודים המרכזיים, עם הבחנה מפורשת בין מה שכבר
            עובד, מה אב טיפוס ומה עוד צריך אימות. אין כאן מדדים, יעדים או תחזיות.
          </p>
          <div className="mt-6 flex flex-wrap gap-4">
            <InlineLink to="/production/nadlan">פתיחה: עמוד הבית של המוצר</InlineLink>
            <InlineLink to="/production/nadlan/post-listing">סגירה: מסלול ההיצע</InlineLink>
          </div>
        </Band>

        <Band tone="surface" labelledBy="mt-stops">
          <BandHead id="mt-stops" eyebrow="מסלול" title="ארבע תחנות" />
          <ol className="grid gap-4 md:grid-cols-2">
            {stops.map((s) => (
              <Panel as="li" key={s.to}>
                <h3 className="display text-lg">
                  <InlineLink to={s.to}>{s.label}</InlineLink>
                </h3>
                <p className="mt-2 text-sm text-muted-foreground">{s.d}</p>
              </Panel>
            ))}
          </ol>
        </Band>

        <Band labelledBy="mt-status">
          <BandHead id="mt-status" eyebrow="סטטוס" title="מה חי, מה אב טיפוס, מה נבדק בהמשך" />
          <div className="grid gap-4 md:grid-cols-3">
            <Panel>
              <Chip tone="ink">חי</Chip>
              <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
                {live.map((x) => (
                  <li key={x}>{x}</li>
                ))}
              </ul>
            </Panel>
            <Panel className="border-dashed">
              <Chip tone="copper">אב טיפוס</Chip>
              <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
                {proto.map((x) => (
                  <li key={x}>{x}</li>
                ))}
              </ul>
            </Panel>
            <Panel className="border-dashed">
              <Chip>לאימות</Chip>
              <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
                {next.map((x) => (
                  <li key={x}>{x}</li>
                ))}
              </ul>
            </Panel>
          </div>
        </Band>

        <Band tone="surface" labelledBy="mt-legend">
          <BandHead id="mt-legend" eyebrow="מקרא" title="מצבי נתונים" />
          <div className="grid gap-4 md:grid-cols-3">
            <Panel className="border-dashed">
              <DemoBadge label="דמו" />
              <p className="mt-3 text-sm text-muted-foreground">
                רשומות זרע לצורך המחשה. מסומנות תמיד, לא נספרות כמלאי ולא נכנסות לסכימה.
              </p>
            </Panel>
            <Panel>
              <Chip>אין עדיין נתונים</Chip>
              <p className="mt-3 text-sm text-muted-foreground">
                מצב ריק כן, עם קריאה לפרסום נכס במקום מילוי מלאכותי.
              </p>
            </Panel>
            <Panel>
              <Chip tone="ink">נתונים אמיתיים</Chip>
              <p className="mt-3 text-sm text-muted-foreground">
                רק רשומות שאומתו, עם מקור, תאריך עדכון וסטטוס אימות — גם כשהם ריקים.
              </p>
            </Panel>
          </div>
        </Band>

        <Band labelledBy="mt-seo">
          <BandHead
            id="mt-seo"
            eyebrow="SEO"
            title="בעלות על כוונות חיפוש"
            lead="לכל שכבה כוונה נפרדת, כדי שלא תיווצר כפילות בין ארכיון, ישות ומודעה."
          />
          <div className="grid gap-4 md:grid-cols-2">
            <Panel>
              <h3 className="display text-lg">ארכיונים</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                ״דירות למכירה ב…״ ו״פרויקטים חדשים ב…״ — סינון, השוואה וניווט.
              </p>
            </Panel>
            <Panel>
              <h3 className="display text-lg">עמודי ישות</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                שם פרויקט או מתחם — עובדות, שלבים ומיקום; canonical יחיד לישות.
              </p>
            </Panel>
            <Panel>
              <h3 className="display text-lg">עמודי מודעה</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                כוונה טרנזקציונית; נכנסים לאינדקס רק כשהם אמיתיים ומאומתים.
              </p>
            </Panel>
            <Panel>
              <h3 className="display text-lg">כלים ומדריכים</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                מילות מפתח נפרדות לכל כלי, עם קישור פנימי לארכיונים הרלוונטיים.
              </p>
            </Panel>
          </div>
        </Band>

        <Band tone="surface" labelledBy="mt-fly">
          <BandHead id="mt-fly" eyebrow="גלגל תנופה" title="איך היצע אמיתי נכנס פנימה" />
          <ol className="grid gap-4 md:grid-cols-4">
            {flywheel.map((f, i) => (
              <Panel as="li" key={f.t}>
                <span className="text-xs font-bold uppercase tracking-wide text-muted-foreground">
                  {i + 1}
                </span>
                <h3 className="display mt-1 text-lg">{f.t}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{f.d}</p>
              </Panel>
            ))}
          </ol>
        </Band>

        <Band labelledBy="mt-check">
          <BandHead id="mt-check" eyebrow="יישום" title="צ׳קליסט למעבר לוורדפרס" />
          <ul className="grid gap-2 text-sm text-muted-foreground md:grid-cols-2">
            {checklist.map((c) => (
              <li key={c} className="rounded-md border border-border bg-card p-3 text-card-foreground">
                {c}
              </li>
            ))}
          </ul>
        </Band>
      </main>
    </ProductionShell>
  );
}

const impl: Impl = {
  intent: "עמוד פנימי לפגישה. אינו מיועד לחיפוש ואינו נכנס לאינדקס בשום מצב.",
  keywords: { primary: "—", secondary: ["עמוד פנימי", "ללא כוונת חיפוש"] },
  meta: {
    title: "נרטיב פגישה — חמש דקות על מוצר נדל״ן",
    description: "אינדקס פנימי לפגישה: סטטוס, מקרא מצבי נתונים, בעלות SEO וצ׳קליסט יישום.",
    canonical: "ללא canonical ציבורי — עמוד פנימי, noindex",
  },
  schema: ["ללא סכימה — עמוד פנימי"],
  internalLinks: [
    "בית המוצר ← /production/nadlan",
    "ארכיון נכסים ← /production/nadlan/properties",
    "ארכיון פרויקטים ← /production/nadlan/projects",
    "פרסום נכס ← /production/nadlan/post-listing",
  ],
  dataPolicy: [
    "אין מדדים, יעדים, תחזיות או נתוני שוק.",
    "כל אמירה מסווגת חי / אב טיפוס / לאימות.",
  ],
  wordpress: ["עמוד פנימי בלבד — לא מועבר לוורדפרס הציבורי"],
};

