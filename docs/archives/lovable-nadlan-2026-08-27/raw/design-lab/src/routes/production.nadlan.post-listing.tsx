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

export const Route = createFileRoute("/production/nadlan/post-listing")({
  head: () => ({
    meta: [
      { title: "פרסום נכס — אב טיפוס של מסלול ההיצע" },
      {
        name: "description",
        content:
          "אב טיפוס למסלול פרסום נכס אמיתי: ארבעה שלבים עתידיים, מסלולי בעלים/מתווך/יזם והבחנה בין פרופיל דמו לפרופיל מאומת.",
      },
      { property: "og:title", content: "פרסום נכס — אב טיפוס" },
      { property: "og:description", content: "מסלול ההיצע העתידי, מסומן בבירור כאב טיפוס לא מחובר." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "robots", content: "noindex, nofollow" },
    ],
  }),
  component: PostListing,
});

const steps = [
  { t: "פרטי הנכס", d: "כתובת, סוג עסקה, חדרים, שטח וקומה. טיוטה נשמרת ואינה מוצגת לאיש." },
  { t: "בעלות ומקור", d: "הצהרה מי מפרסם — בעלים, מיופה כוח, מתווך מורשה או יזם — וצירוף אסמכתה." },
  { t: "בדיקה ואימות", d: "בדיקה ידנית מול המסמכים לפני שהמודעה מסומנת כאמיתית, עם תאריך בדיקה." },
  { t: "תצוגה מקדימה ופרסום", d: "רואים בדיוק מה ייחשף לציבור ומה יישאר פרטי, ורק אז מאשרים." },
];

const branches = [
  { t: "בעלי נכס", d: "פרסום דירה אחת, ללא עלות בשלב זה, עם שליטה מלאה בהסרה." },
  { t: "מתווכים", d: "העלאת מלאי מרובה ואימות רישיון תיווך לפני סימון ״מאומת״." },
  { t: "יזמים", d: "הוספת פרויקט וקישורו לעמוד הפרויקט הקיים בארכיון." },
];

function PostListing() {
  return (
    <ProductionShell route="/production/nadlan/post-listing" impl={impl}>
      <main id="main">
        <div className="lab-container pt-5">
          <Crumbs
            trail={[{ label: "דף הבית", to: "/production/nadlan" }, { label: "פרסום נכס" }]}
          />
        </div>

        <Band className="pt-6" labelledBy="pl-h1">
          <Chip tone="copper">אב טיפוס — טרם מחובר</Chip>
          <h1 id="pl-h1" className="display mt-4 text-3xl leading-tight md:text-4xl">
            מסלול פרסום נכס אמיתי — שלד לאימות
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-muted-foreground">
            העמוד מציג את השלד המתוכנן של מסלול ההיצע. אין כאן טופס פעיל, אין קליטת
            נתונים ואין התחייבות לחשיפה, לפניות או לתמחור.
          </p>
          <button
            type="button"
            disabled
            aria-disabled="true"
            className="tap mt-6 inline-flex cursor-not-allowed items-center rounded-md bg-secondary px-5 py-3 text-sm font-bold text-secondary-foreground opacity-70"
          >
            אב טיפוס — טרם מחובר
          </button>
        </Band>

        <Band tone="surface" labelledBy="pl-steps">
          <BandHead id="pl-steps" eyebrow="ארבעה שלבים עתידיים" title="איך המסלול יעבוד" />
          <ol className="grid gap-4 md:grid-cols-2">
            {steps.map((s, i) => (
              <Panel as="li" key={s.t} className="border-dashed">
                <span className="text-xs font-bold uppercase tracking-wide text-muted-foreground">
                  שלב {i + 1}
                </span>
                <h3 className="display mt-1 text-lg">{s.t}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{s.d}</p>
              </Panel>
            ))}
          </ol>
        </Band>

        <Band labelledBy="pl-branches">
          <BandHead id="pl-branches" eyebrow="מסלולים" title="מי מפרסם" />
          <div className="grid gap-4 md:grid-cols-3">
            {branches.map((b) => (
              <Panel key={b.t}>
                <h3 className="display text-lg">{b.t}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{b.d}</p>
              </Panel>
            ))}
          </div>

          <h2 className="display mt-10 text-2xl">אנשי מקצוע: דמו מול מאומת</h2>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <Panel className="border-dashed">
              <DemoBadge label="פרופיל דמו" />
              <h3 className="display mt-2 text-lg">פרופיל דמו</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                נוצר להמחשת מבנה האינדקס. ללא רישיון שנבדק, ללא ותק וללא ביקורות, ואינו
                מוצג כספק פעיל.
              </p>
            </Panel>
            <Panel>
              <Chip tone="ink">פרופיל מאומת</Chip>
              <h3 className="display mt-2 text-lg">פרופיל מאומת</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                רישיון או תעודה שנבדקו ידנית, עם תאריך בדיקה, תחומי פעילות ואזורי שירות
                שהוצהרו על ידי בעל המקצוע.
              </p>
            </Panel>
          </div>

          <div className="mt-6 flex flex-wrap gap-4">
            <InlineLink to="/production/nadlan/properties">ארכיון הנכסים</InlineLink>
            <InlineLink to="/production/nadlan/projects">ארכיון הפרויקטים</InlineLink>
            <InlineLink to="/production/nadlan/meeting">מצגת הפגישה</InlineLink>
          </div>
        </Band>
      </main>
    </ProductionShell>
  );
}

const impl: Impl = {
  intent: "כוונה טרנזקציונית של צד ההיצע. בשלב האב טיפוס: הסבר מסלול בלבד, ללא טופס וללא קליטת נתונים.",
  keywords: {
    primary: "פרסום דירה למכירה",
    secondary: ["פרסום נכס חינם", "פרסום נכס למתווכים", "הוספת פרויקט יזם"],
  },
  meta: {
    title: "פרסום נכס — אב טיפוס של מסלול ההיצע",
    description:
      "ארבעה שלבים עתידיים לפרסום נכס אמיתי, מסלולי בעלים/מתווך/יזם והבחנה בין פרופיל דמו למאומת.",
    canonical: "https://nad-lan.co.il/post-listing/",
  },
  schema: ["BreadcrumbList בלבד", "ללא HowTo/Offer כל עוד המסלול אינו פעיל"],
  internalLinks: [
    "ארכיון נכסים ← /production/nadlan/properties",
    "ארכיון פרויקטים ← /production/nadlan/projects",
    "מצגת פגישה ← /production/nadlan/meeting",
  ],
  dataPolicy: [
    "כפתור ראשי מושבת ומסומן ״אב טיפוס — טרם מחובר״.",
    "אין הצגת לידים, צפיות, זמן מכירה או תמחור.",
    "פרופיל דמו מסומן בכל הופעה.",
  ],
  wordpress: [
    "Prototype notice → block: nadlan/prototype-banner",
    "Steps → block: nadlan/publish-steps (static until backend exists)",
    "Branches → core/columns + nadlan/branch-card",
  ],
};

