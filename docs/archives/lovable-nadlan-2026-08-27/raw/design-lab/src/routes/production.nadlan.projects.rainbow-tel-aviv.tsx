import { createFileRoute } from "@tanstack/react-router";
import { ProductionShell, type Impl } from "@/components/production/ProductionShell";
import {
  Action,
  Band,
  BandHead,
  Chip,
  Crumbs,
  EmptyState,
  FaqList,
  InlineLink,
  KeyValueGrid,
  MediaFrame,
  Panel,
  SourceStamp,
  Tabs,
} from "@/components/production/ui";

export const Route = createFileRoute("/production/nadlan/projects/rainbow-tel-aviv")({
  head: () => ({
    meta: [
      { title: "Rainbow תל אביב — פרויקט שדה דב, 480 יחידות דיור" },
      {
        name: "description",
        content:
          "עמוד פרויקט Rainbow בשדה דב תל אביב: 480 יחידות דיור, מיקום, שלבים ומסמכים ציבוריים. מקור ותאריך עדכון מסומנים.",
      },
      { property: "og:title", content: "Rainbow תל אביב — שדה דב" },
      { property: "og:description", content: "480 יחידות דיור בשדה דב. עובדות ציבוריות בלבד." },
      { property: "og:type", content: "article" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "robots", content: "noindex, nofollow" },
    ],
  }),
  component: RainbowProject,
});

const facts = [
  { k: "עיר", v: "תל אביב–יפו" },
  { k: "מתחם", v: "שדה דב" },
  { k: "היקף", v: "480 יחידות דיור" },
  { k: "סוג", v: "מגורים — בנייה חדשה" },
  { k: "מקור הנתונים", v: "פרסום ציבורי — קישור לשיבוץ" },
  { k: "תאריך עדכון", v: "לשיבוץ — טרם מולא" },
];

const timeline = [
  { title: "תכנון וסטטוס תב״ע", body: "פרטי הליך התכנון — לשיבוץ מתוך מקור ציבורי." },
  { title: "היתרים", body: "מספרי היתר ותאריכים — לשיבוץ מתוך מקור ציבורי." },
  { title: "בנייה", body: "שלב הבנייה בפועל — לשיבוץ, כולל תאריך העדכון האחרון." },
  { title: "אכלוס צפוי", body: "מועד אכלוס — יוצג רק אם פורסם רשמית." },
];

const faq = [
  {
    q: "כמה יחידות דיור בפרויקט?",
    a: "480 יחידות דיור, לפי מידע ציבורי הקיים היום. הנתון יוצג עם קישור מקור ותאריך עדכון בגרסה החיה.",
  },
  {
    q: "איפה הפרויקט ממוקם?",
    a: "במתחם שדה דב בתל אביב–יפו. תרשים המיקום מציג הקשר עירוני בלבד ואינו מפה מסחרית.",
  },
  {
    q: "אפשר לראות דירות למכירה בפרויקט?",
    a: "עדיין לא. לא נאספו מודעות אמיתיות בפרויקט, ולכן מוצג מצב ריק עם קריאה לפרסום נכס במקום רשומות מומצאות.",
  },
  {
    q: "מה לא מוצג כאן בכוונה?",
    a: "מחירים, טווחי מחיר, קצב מכירות, ביקוש, ביקורות או התחייבות למועדים — אין לנו מקור מאומת לכך.",
  },
];

function RainbowProject() {
  return (
    <ProductionShell
      route="/production/nadlan/projects/rainbow-tel-aviv"
      impl={impl}
      headerPrimaryCta="פרסמו נכס בפרויקט"
    >
      <main id="main">
        <div className="lab-container pt-5">
          <Crumbs
            trail={[
              { label: "דף הבית", to: "/production/nadlan" },
              { label: "פרויקטים", to: "/production/nadlan/projects" },
              { label: "Rainbow תל אביב" },
            ]}
          />
        </div>

        <Band className="pt-6" labelledBy="rb-h1">
          <div className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
            <div className="min-w-0">
              <div className="flex flex-wrap gap-2">
                <Chip tone="ink">פרויקט אמיתי</Chip>
                <Chip>עובדות ציבוריות בלבד</Chip>
              </div>
              <h1 id="rb-h1" className="display mt-4 text-3xl leading-tight md:text-4xl">
                Rainbow תל אביב — מתחם שדה דב, 480 יחידות דיור
              </h1>
              <p className="mt-4 max-w-xl text-base leading-relaxed text-muted-foreground">
                עמוד הפרויקט מרכז את מה שידוע בפרסום ציבורי: היקף, מיקום ושלבים.
                כל נתון שאין לו מקור מזוהה מסומן כלא מולא, ואין כאן מחירים או
                הבטחות שיווקיות.
              </p>
              <div className="mt-6 flex flex-wrap gap-3">
                <Action variant="primary" href="#facts">
                  לעובדות הפרויקט
                </Action>
                <Action variant="quiet" to="/production/nadlan/post-listing">
                  פרסמו נכס בפרויקט
                </Action>
              </div>
              <SourceStamp
                source="מקור: פרסום ציבורי — קישור לשיבוץ"
                updated="עודכן: תאריך לשיבוץ"
                verification="אימות: נבדק מול מקור ציבורי אחד"
              />
            </div>
            <MediaFrame
              label="מקום שמור לתצלום הדמיה / תרשים מתחם"
              ratio="4 / 3"
              note="תמונה רספונסיבית עם ממדים שמורים; ללא וידאו אוטומטי."
            />
          </div>
        </Band>

        <Band id="facts" tone="surface" labelledBy="facts-h">
          <BandHead
            id="facts-h"
            eyebrow="נתוני יסוד"
            title="עובדות הפרויקט"
            lead="שדות ללא מקור מוצגים ריקים במפורש ולא מנוחשים."
          />
          <Panel>
            <KeyValueGrid rows={facts} />
          </Panel>
        </Band>

        <Band labelledBy="tl-h">
          <BandHead id="tl-h" eyebrow="ציר זמן" title="שלבי הפרויקט" />
          <Tabs
            ariaLabel="שלבי הפרויקט"
            items={timeline.map((t, i) => ({
              id: `stage-${i}`,
              label: t.title,
              content: (
                <Panel className="mt-4">
                  <h3 className="display text-lg">{t.title}</h3>
                  <p className="mt-2 text-sm text-muted-foreground">{t.body}</p>
                  <SourceStamp />
                </Panel>
              ),
            }))}
          />
        </Band>

        <Band tone="surface" labelledBy="loc-h">
          <BandHead
            id="loc-h"
            eyebrow="מיקום והקשר"
            title="הסביבה של שדה דב"
            lead="שכבות מרחביות להתמצאות — לא מפת שיווק ולא נתוני שוק."
          />
          <div className="grid gap-5 lg:grid-cols-[1.1fr_0.9fr]">
            <MediaFrame label="מקום שמור למפת מיקום סטטית" note="נטענת רק בלחיצה; ללא סקריפט מפה כבד." />
            <Panel>
              <h3 className="display text-lg">מה יוצג כאן בגרסה החיה</h3>
              <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
                <li>גבולות המתחם והרחובות הסמוכים.</li>
                <li>מוסדות חינוך ותחבורה ציבורית — מנתוני רשות פתוחים, עם תאריך.</li>
                <li>פרויקטים סמוכים באותו ארכיון, כקישור פנימי.</li>
                <li>ללא ציוני איכות שכונה ממציאים וללא דירוגים.</li>
              </ul>
            </Panel>
          </div>
        </Band>

        <Band labelledBy="units-h">
          <BandHead
            id="units-h"
            eyebrow="נכסים בפרויקט"
            title="דירות למכירה בפרויקט"
            lead="עדיין לא נאספו מודעות אמיתיות בפרויקט. במקום למלא בדמו — מצב ריק כן."
          />
          <EmptyState
            title="אין עדיין מודעות בפרויקט הזה"
            body="כשתפורסם מודעה אמיתית שאומתה, היא תופיע כאן עם תאריך עדכון וסטטוס אימות."
            ctaLabel="פרסמו נכס אמיתי חינם"
          />
          <div className="mt-6 flex flex-wrap gap-3">
            <InlineLink to="/production/nadlan/properties">כל הנכסים בארכיון</InlineLink>
            <InlineLink to="/production/nadlan/projects">חזרה לארכיון הפרויקטים</InlineLink>
          </div>
        </Band>

        <Band tone="surface" labelledBy="rb-faq">
          <BandHead id="rb-faq" eyebrow="שאלות נפוצות" title="על פרויקט Rainbow" />
          <FaqList items={faq} />
        </Band>
      </main>
    </ProductionShell>
  );
}

const impl: Impl = {
  intent:
    "כוונה ניווטית־מחקרית ברמת ישות: חיפוש שם הפרויקט או המתחם. העמוד הוא ה‑canonical של הישות ״Rainbow שדה דב״.",
  keywords: {
    primary: "Rainbow תל אביב",
    secondary: ["פרויקט שדה דב", "דירות חדשות שדה דב", "480 יחידות דיור תל אביב"],
  },
  meta: {
    title: "Rainbow תל אביב — פרויקט שדה דב, 480 יחידות דיור",
    description:
      "עמוד פרויקט Rainbow בשדה דב תל אביב: היקף, מיקום, שלבים ומסמכים ציבוריים, עם מקור ותאריך עדכון.",
    canonical: "https://nad-lan.co.il/projects/rainbow-tel-aviv/",
  },
  schema: [
    "BreadcrumbList",
    "Place / ApartmentComplex לעובדות בלבד",
    "FAQPage",
    "ללא Offer, ללא AggregateRating, ללא Review",
  ],
  internalLinks: [
    "ארכיון פרויקטים ← /production/nadlan/projects",
    "ארכיון נכסים ← /production/nadlan/properties",
    "פרסום נכס בפרויקט ← /production/nadlan/post-listing",
  ],
  dataPolicy: [
    "רק עובדות ציבוריות קיימות (480 יחידות, שדה דב, תל אביב).",
    "שדות מקור/תאריך/אימות מוצגים ריקים במפורש עד למילוי.",
    "אין מחירים, קצב מכירות, ביקוש או מועדי אכלוס לא רשמיים.",
    "מקטע הנכסים בפרויקט במצב ריק — לא מוזרקות מודעות דמו.",
  ],
  wordpress: [
    "CPT: project · single-project.php",
    "Facts → block: nadlan/fact-table (ACF fields + source/date)",
    "Timeline → block: nadlan/project-timeline",
    "Static map → block: nadlan/static-map (click-to-load)",
    "Units → block: nadlan/listing-loop (empty-state template)",
  ],
};

