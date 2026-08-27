import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { ProductionShell, type Impl } from "@/components/production/ProductionShell";
import {
  Action,
  Band,
  BandHead,
  Chip,
  Crumbs,
  DemoBadge,
  FaqList,
  InlineLink,
  KeyValueGrid,
  MediaFrame,
  Panel,
  SourceStamp,
} from "@/components/production/ui";

export const Route = createFileRoute("/production/nadlan/properties/baka-demo")({
  head: () => ({
    meta: [
      { title: "נכס לדוגמה — דירת 4 חדרים בבקעה, ירושלים" },
      {
        name: "description",
        content:
          "מודעה לדוגמה להמחשת חוויית עמוד הנכס: גלריה, מפרט, מפת סביבה, עלויות חודשיות משוערות, מחשבון משכנתה ותיאום ביקור.",
      },
      { property: "og:title", content: "נכס לדוגמה — בקעה, ירושלים" },
      { property: "og:description", content: "עמוד מודעה לדוגמה. אינו נכס אמיתי ואינו הצעה." },
      { property: "og:type", content: "article" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "robots", content: "noindex, nofollow" },
    ],
  }),
  component: BakaDemo,
});

const specs = [
  { k: "עיר ושכונה", v: "ירושלים · בקעה" },
  { k: "סוג עסקה", v: "מכירה (דוגמה)" },
  { k: "חדרים", v: "4 (דוגמה)" },
  { k: "שטח", v: "96 מ״ר (דוגמה)" },
  { k: "קומה", v: "2 מתוך 4 (דוגמה)" },
  { k: "מקור הנתונים", v: "source = demo_seed" },
  { k: "מחיר", v: "דוגמה — לא מוצג" },
  { k: "תאריך עדכון", v: "דוגמה — טרם מולא" },
];

const costs = [
  { k: "ארנונה", v: "דוגמה — לא מחושב" },
  { k: "ועד בית", v: "דוגמה — לא מחושב" },
  { k: "אחזקה שוטפת", v: "דוגמה — לא מחושב" },
];

const history = [
  { k: "מודעה פורסמה", v: "דוגמה" },
  { k: "עדכון מחיר", v: "דוגמה" },
  { k: "הצעה שהוגשה", v: "דוגמה — אין מסחר פעיל" },
];

const faq = [
  {
    q: "אפשר לקנות את הנכס הזה?",
    a: "לא. זו מודעה לדוגמה שנועדה להמחיש את מבנה עמוד הנכס. אין בעלים, אין מחיר ואין הצעה מחייבת.",
  },
  {
    q: "למה כל ערך כתוב ״דוגמה״?",
    a: "כדי שלא ייווצר רושם של מחיר, זמינות או פעילות מסחר. ערכים אמיתיים יופיעו רק ממודעה שפורסמה ואומתה.",
  },
  {
    q: "אני בעל נכס בבקעה — מה עושים?",
    a: "אפשר לפרסם נכס אמיתי ללא עלות; המודעה תיבדק ותקבל מקור, תאריך עדכון וסטטוס אימות.",
  },
];

function BakaDemo() {
  const [amount, setAmount] = useState(1000000);
  const [years, setYears] = useState(25);
  const [rate, setRate] = useState(4.5);

  const monthly = (() => {
    const r = rate / 100 / 12;
    const n = years * 12;
    if (r === 0) return amount / n;
    return (amount * r) / (1 - Math.pow(1 + r, -n));
  })();

  return (
    <ProductionShell
      route="/production/nadlan/properties/baka-demo"
      impl={impl}
      headerPrimaryCta="פרסמו נכס אמיתי חינם"
    >
      <main id="main">
        <div className="lab-container pt-5">
          <Crumbs
            trail={[
              { label: "דף הבית", to: "/production/nadlan" },
              { label: "נכסים", to: "/production/nadlan/properties" },
              { label: "נכס לדוגמה · בקעה" },
            ]}
          />
        </div>

        <Band className="pt-6" labelledBy="bk-h1">
          <DemoBadge label="נכס לדוגמה — להמחשת חוויית המודעה" />
          <div className="mt-4 grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
            <div className="min-w-0">
              <h1 id="bk-h1" className="display text-3xl leading-tight md:text-4xl">
                דירת 4 חדרים בבקעה, ירושלים — מודעה לדוגמה
              </h1>
              <p className="mt-4 max-w-xl text-base leading-relaxed text-muted-foreground">
                העמוד מדגים איך תיראה מודעה אמיתית: גלריה, מפרט, סביבה, עלויות ומסלול
                יצירת קשר. כל ערך מספרי מסומן ״דוגמה״, ואין כאן הצעה, מכירה או מסחר פעיל.
              </p>
              <div className="mt-6 flex flex-wrap gap-3">
                <Action variant="copper" to="/production/nadlan/post-listing">
                  פרסמו נכס אמיתי חינם
                </Action>
                <Action variant="quiet" href="#visit">
                  תיאום ביקור (דוגמה)
                </Action>
              </div>
              <SourceStamp
                source="מקור: demo_seed"
                updated="עודכן: דוגמה — טרם מולא"
                verification="אימות: לא רלוונטי לדוגמה"
              />
            </div>
            <div className="grid gap-3">
              <MediaFrame label="מקום שמור לגלריית תמונות" note="תמונות רספונסיביות, טעינה עצלה, ממדים שמורים." />
              <MediaFrame label="מקום שמור לסיור תלת־ממד" ratio="16 / 9" note="נטען בלחיצה בלבד; ללא הפעלה אוטומטית." />
            </div>
          </div>
        </Band>

        <Band tone="surface" labelledBy="bk-specs">
          <BandHead id="bk-specs" eyebrow="מפרט" title="נתוני הנכס" />
          <Panel>
            <KeyValueGrid rows={specs} />
          </Panel>
        </Band>

        <Band labelledBy="bk-area">
          <BandHead
            id="bk-area"
            eyebrow="סביבה"
            title="בקעה — הקשר מרחבי"
            lead="שכבות התמצאות בלבד: תחבורה, חינוך ומרחק להליכה. ללא ציוני שכונה ממציאים."
          />
          <div className="grid gap-5 lg:grid-cols-[1.1fr_0.9fr]">
            <MediaFrame label="מקום שמור למפת סביבה סטטית" note="נטענת בלחיצה; ללא ספריית מפות כבדה." />
            <Panel>
              <h3 className="display text-lg">עלויות חודשיות משוערות</h3>
              <div className="mt-3">
                <KeyValueGrid rows={costs} />
              </div>
              <p className="mt-3 text-xs text-muted-foreground">
                בגרסה החיה החישוב יתבסס על נתוני רשות מקומית עם תאריך עדכון. כאן לא מוצג
                שום סכום.
              </p>
            </Panel>
          </div>
        </Band>

        <Band tone="surface" labelledBy="bk-mort">
          <BandHead
            id="bk-mort"
            eyebrow="כלי"
            title="מחשבון משכנתה"
            lead="החישוב מתבצע על הערכים שאתם מזינים בלבד. אין קשר למחיר הנכס לדוגמה."
          />
          <Panel>
            <div className="grid gap-4 sm:grid-cols-3">
              <label className="block text-sm font-bold">
                סכום ההלוואה (₪)
                <input
                  type="number"
                  min={0}
                  step={50000}
                  value={amount}
                  onChange={(e) => setAmount(Number(e.target.value))}
                  className="tap mt-2 w-full rounded-md border border-border bg-card px-3 py-3 text-sm font-semibold"
                />
              </label>
              <label className="block text-sm font-bold">
                שנים
                <input
                  type="number"
                  min={1}
                  max={35}
                  value={years}
                  onChange={(e) => setYears(Number(e.target.value))}
                  className="tap mt-2 w-full rounded-md border border-border bg-card px-3 py-3 text-sm font-semibold"
                />
              </label>
              <label className="block text-sm font-bold">
                ריבית שנתית (%)
                <input
                  type="number"
                  min={0}
                  step={0.1}
                  value={rate}
                  onChange={(e) => setRate(Number(e.target.value))}
                  className="tap mt-2 w-full rounded-md border border-border bg-card px-3 py-3 text-sm font-semibold"
                />
              </label>
            </div>
            <p className="mt-4 text-lg font-bold">
              החזר חודשי מחושב:{" "}
              {Number.isFinite(monthly) ? Math.round(monthly).toLocaleString("he-IL") : "—"} ₪
            </p>
            <p className="mt-1 text-xs text-muted-foreground">
              חישוב שפיצר על הקלט שלכם. אינו הצעת אשראי, אינו כולל ביטוחים ואינו מהווה
              ייעוץ.
            </p>
          </Panel>
        </Band>

        <Band id="visit" labelledBy="bk-actions">
          <BandHead
            id="bk-actions"
            eyebrow="פעולות"
            title="מסלולי המשך — כולם במצב דוגמה"
            lead="הכפתורים ממחישים את הזרימה ואינם שולחים דבר."
          />
          <div className="grid gap-4 md:grid-cols-3">
            <Panel className="border-dashed">
              <h3 className="display text-lg">תיאום ביקור</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                בחירת חלון זמן מול לוח הזמנים של המפרסם. בדוגמה אין לוח זמנים ואין נמען.
              </p>
              <button
                type="button"
                disabled
                aria-disabled="true"
                className="tap mt-4 w-full cursor-not-allowed rounded-md bg-secondary px-4 py-3 text-sm font-bold text-secondary-foreground opacity-70"
              >
                דוגמה — לא פעיל
              </button>
            </Panel>
            <Panel className="border-dashed">
              <h3 className="display text-lg">הצעה לא מחייבת</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                הבעת עניין בכתב, ללא מכרז וללא מסחר. אין הצגת הצעות אחרות ואין רמז לתחרות.
              </p>
              <button
                type="button"
                disabled
                aria-disabled="true"
                className="tap mt-4 w-full cursor-not-allowed rounded-md bg-secondary px-4 py-3 text-sm font-bold text-secondary-foreground opacity-70"
              >
                דוגמה — לא פעיל
              </button>
            </Panel>
            <Panel className="border-dashed">
              <h3 className="display text-lg">תביעת בעלות</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                בעל הנכס האמיתי בכתובת דומה יוכל לבקש להחליף את הדוגמה במודעה מאומתת.
              </p>
              <div className="mt-4">
                <Action variant="quiet" to="/production/nadlan/post-listing" className="w-full">
                  למסלול הפרסום
                </Action>
              </div>
            </Panel>
          </div>

          <h3 className="display mt-9 text-lg">היסטוריית המודעה</h3>
          <Panel className="mt-3 border-dashed">
            <KeyValueGrid rows={history} />
            <p className="mt-3 text-xs text-muted-foreground">
              אין מכירה פומבית, אין הצעות פעילות ואין מדד ביקוש.
            </p>
          </Panel>

          <div className="mt-8 flex flex-wrap items-center gap-4">
            <Action variant="copper" to="/production/nadlan/post-listing">
              פרסמו נכס אמיתי חינם
            </Action>
            <InlineLink to="/production/nadlan/properties">חזרה לארכיון הנכסים</InlineLink>
          </div>
        </Band>

        <Band tone="surface" labelledBy="bk-faq">
          <BandHead id="bk-faq" eyebrow="שאלות נפוצות" title="על המודעה לדוגמה" />
          <FaqList items={faq} />
          <p className="mt-5">
            <Chip tone="ink">source = demo_seed</Chip>
          </p>
        </Band>
      </main>
    </ProductionShell>
  );
}

const impl: Impl = {
  intent:
    "כוונה טרנזקציונית ברמת מודעה. בשלב הזה הרשומה היא זרע דמו, ולכן העמוד ממחיש חוויה ואינו מתחרה על שאילתות מסחריות.",
  keywords: {
    primary: "דירה 4 חדרים בקעה ירושלים",
    secondary: ["דירות למכירה בבקעה", "עמוד נכס", "מחשבון משכנתה"],
  },
  meta: {
    title: "נכס לדוגמה — דירת 4 חדרים בבקעה, ירושלים",
    description:
      "מודעה לדוגמה להמחשת חוויית עמוד הנכס: גלריה, מפרט, סביבה, עלויות, מחשבון משכנתה ותיאום ביקור.",
    canonical: "https://nad-lan.co.il/properties/baka-demo/",
  },
  schema: [
    "BreadcrumbList",
    "RealEstateListing — טיוטה בלבד, לא מוזרק כל עוד source=demo_seed",
    "ללא Offer/price/availability",
    "FAQPage לשאלות המוצגות בלבד",
  ],
  internalLinks: [
    "ארכיון נכסים ← /production/nadlan/properties",
    "פרסום נכס ← /production/nadlan/post-listing",
    "ארכיון פרויקטים ← /production/nadlan/projects",
  ],
  dataPolicy: [
    "תווית עליונה קבועה: ״נכס לדוגמה — להמחשת חוויית המודעה״.",
    "כל ערך היסטוריה/הצעה מסומן ״דוגמה״; אין רמז למסחר חי.",
    "source = demo_seed מוצג גלוי בעמוד ובמפרט.",
    "מחשבון המשכנתה מחשב רק על קלט המשתמש ואינו נגזר ממחיר נכס.",
  ],
  wordpress: [
    "single-listing.php עם post meta: source, demo_flag",
    "Gallery → core/gallery בתוך nadlan/listing-media (lazy)",
    "Specs → block: nadlan/spec-table",
    "Mortgage → block: nadlan/mortgage-calc (client-side)",
    "Schema → מוזרק רק כאשר demo_flag=false",
  ],
};

