import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { ProductionShell, type Impl } from "@/components/production/ProductionShell";
import {
  Action,
  Band,
  BandHead,
  Chip,
  Crumbs,
  DataStateSwitch,
  DemoBadge,
  EmptyState,
  FaqList,
  InlineLink,
  LiveState,
  MediaFrame,
  Panel,
  SourceStamp,
  type DataState,
} from "@/components/production/ui";

export const Route = createFileRoute("/production/nadlan/projects/")({
  head: () => ({
    meta: [
      { title: "פרויקטים חדשים בישראל — ארכיון פרויקטים" },
      {
        name: "description",
        content:
          "ארכיון פרויקטים חדשים לפי עיר, שלב בנייה וסוג יזמות. כל פרויקט עם עובדות ציבוריות, מקור ותאריך עדכון גלויים.",
      },
      { property: "og:title", content: "ארכיון פרויקטים חדשים" },
      { property: "og:description", content: "פרויקטים לפי עיר ושלב בנייה, עם מקור ותאריך עדכון." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "robots", content: "noindex, nofollow" },
    ],
  }),
  component: ProjectsArchive,
});

const cities = ["הכול", "תל אביב", "ירושלים", "חיפה", "באר שבע"];
const stages = ["הכול", "לפני שיווק", "בשיווק", "בבנייה", "אכלוס"];

type Project = {
  name: string;
  city: string;
  developer: string;
  stage: string;
  units: string;
  note: string;
  real: boolean;
  to?: string;
};

const projects: Project[] = [
  {
    name: "Rainbow תל אביב",
    city: "תל אביב",
    developer: "יזם — לשיבוץ ממקור ציבורי",
    stage: "בשיווק",
    units: "480 יחידות דיור",
    note: "מתחם שדה דב, תל אביב. עובדות ציבוריות בלבד.",
    real: true,
    to: "/production/nadlan/projects/rainbow-tel-aviv",
  },
  {
    name: "פרויקט לדוגמה · צפון העיר",
    city: "חיפה",
    developer: "יזם לדוגמה",
    stage: "בבנייה",
    units: "מספר יחידות — לא מולא",
    note: "רשומה לדוגמה להמחשת מבנה הארכיון.",
    real: false,
  },
  {
    name: "פרויקט לדוגמה · התחדשות עירונית",
    city: "ירושלים",
    developer: "יזם לדוגמה",
    stage: "לפני שיווק",
    units: "מספר יחידות — לא מולא",
    note: "רשומה לדוגמה. אין קשר ליזם או למגרש אמיתי.",
    real: false,
  },
  {
    name: "פרויקט לדוגמה · שכונה מתפתחת",
    city: "באר שבע",
    developer: "יזם לדוגמה",
    stage: "אכלוס",
    units: "מספר יחידות — לא מולא",
    note: "רשומה לדוגמה להצגת מצב ״אכלוס״.",
    real: false,
  },
];

const developers = ["הכול", ...Array.from(new Set(projects.map((p) => p.developer)))];

const cityHubs = ["תל אביב", "ירושלים", "חיפה", "באר שבע"];

const faq = [
  {
    q: "כמה פרויקטים אמיתיים יש כרגע?",
    a: "פרויקט אחד עם עובדות ציבוריות מאומתות (Rainbow תל אביב). שאר הרשומות הן דוגמאות מסומנות להמחשת המבנה.",
  },
  {
    q: "מאיפה מגיעים הנתונים?",
    a: "מפרסומים ציבוריים של היזם או הרשות. בכל רשומה יופיעו שדות מקור ותאריך עדכון; היום הם ריקים בכוונה.",
  },
  {
    q: "אני יזם — איך מוסיפים פרויקט?",
    a: "דרך מסלול הוספת פרויקט. הפרויקט מסומן כטיוטה עד לבדיקת המסמכים.",
  },
  {
    q: "למה אין מחירים או זמינות?",
    a: "אין לנו מקור מאומת למחירים או ליתרת דירות. נציג נתון כזה רק כשיגיע מפרסום רשמי, עם תאריך.",
  },
];

function ProjectsArchive() {
  const [city, setCity] = useState("הכול");
  const [stage, setStage] = useState("הכול");
  const [developer, setDeveloper] = useState("הכול");
  const [state, setState] = useState<DataState>("demo");
  const [view, setView] = useState<"cards" | "list" | "map">("cards");
  const [compare, setCompare] = useState<string[]>([]);

  const filtered = projects.filter(
    (p) =>
      (city === "הכול" || p.city === city) &&
      (stage === "הכול" || p.stage === stage) &&
      (developer === "הכול" || p.developer === developer),
  );
  const visible = state === "demo" ? filtered : filtered.filter((p) => p.real);
  const toggleCompare = (name: string) =>
    setCompare((c) => (c.includes(name) ? c.filter((x) => x !== name) : [...c, name].slice(0, 3)));


  return (
    <ProductionShell route="/production/nadlan/projects" impl={impl} headerPrimaryCta="הוסיפו פרויקט">
      <main id="main">
        <div className="lab-container pt-5">
          <Crumbs trail={[{ label: "דף הבית", to: "/production/nadlan" }, { label: "פרויקטים" }]} />
        </div>

        <Band className="pt-6" labelledBy="pj-h1">
          <h1 id="pj-h1" className="display text-3xl leading-tight md:text-4xl">
            פרויקטים חדשים — ארכיון לפי עיר ושלב בנייה
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-muted-foreground">
            כל רשומה מציגה עובדות ציבוריות בלבד, עם שדות מקור, תאריך עדכון וסטטוס אימות
            גלויים. רשומות דמו מסומנות ואינן מייצגות מלאי פעיל.
          </p>
          <div className="mt-6">
            <DataStateSwitch value={state} onChange={setState} />
          </div>
        </Band>

        <Band tone="surface" labelledBy="filters-h">
          <BandHead id="filters-h" eyebrow="סינון" title="צמצמו לפי עיר, יזם ושלב" />
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <label className="block text-sm font-bold">
              עיר
              <select
                value={city}
                onChange={(e) => setCity(e.target.value)}
                className="tap mt-2 w-full rounded-md border border-border bg-card px-3 py-3 text-sm font-semibold"
              >
                {cities.map((c) => (
                  <option key={c}>{c}</option>
                ))}
              </select>
            </label>
            <label className="block text-sm font-bold">
              יזם
              <select
                value={developer}
                onChange={(e) => setDeveloper(e.target.value)}
                className="tap mt-2 w-full rounded-md border border-border bg-card px-3 py-3 text-sm font-semibold"
              >
                {developers.map((d) => (
                  <option key={d}>{d}</option>
                ))}
              </select>
            </label>
            <label className="block text-sm font-bold">
              סטטוס
              <select
                value={stage}
                onChange={(e) => setStage(e.target.value)}
                className="tap mt-2 w-full rounded-md border border-border bg-card px-3 py-3 text-sm font-semibold"
              >
                {stages.map((s) => (
                  <option key={s}>{s}</option>
                ))}
              </select>
            </label>
          </div>

          <div className="mt-8 flex flex-wrap items-center justify-between gap-3">
            <h2 className="display text-2xl">
              {state === "empty" ? "אין עדיין נתונים" : `${visible.length} פרויקטים`}
            </h2>
            <div role="group" aria-label="תצוגת תוצאות" className="flex gap-1">
              {(
                [
                  ["cards", "כרטיסים"],
                  ["list", "רשימה"],
                  ["map", "מפה"],
                ] as const
              ).map(([v, label]) => (
                <button
                  key={v}
                  type="button"
                  onClick={() => setView(v)}
                  aria-pressed={view === v}
                  className={
                    "tap rounded-md px-4 py-2.5 text-xs font-bold " +
                    (view === v
                      ? "bg-primary text-primary-foreground"
                      : "border border-border bg-card text-card-foreground hover:bg-secondary")
                  }
                >
                  {label}
                </button>
              ))}
            </div>
          </div>
          <p className="mt-1 text-xs text-muted-foreground">
            תצלום מצב של הרשומות שנאספו עד כה — אינו מדד היצע או נתח שוק.
          </p>

          {state === "empty" ? (
            <div className="mt-4">
              <EmptyState
                title="אין עדיין פרויקטים בסינון הזה"
                body="במצב ״אין עדיין נתונים״ לא מוצגות רשומות דמו. זהו המצב שבו יראה משתמש בעיר שטרם נאספו בה פרויקטים."
                ctaLabel="הוסיפו פרויקט"
              />
            </div>
          ) : view === "map" ? (
            <div className="mt-4">
              <MediaFrame
                label="מקום שמור למפת פרויקטים סטטית"
                note="נטענת בלחיצה בלבד; סימונים מוצגים רק לרשומות עם מיקום מאומת."
              />
            </div>
          ) : (
            <ul
              className={
                "mt-4 grid gap-4 " + (view === "cards" ? "md:grid-cols-2" : "max-w-3xl")
              }
            >
              {visible.map((p) => (
                <Panel as="li" key={p.name} className={p.real ? "" : "border-dashed"}>
                  <div className="flex flex-wrap items-center gap-2">
                    {p.real ? <Chip tone="ink">פרויקט אמיתי</Chip> : <DemoBadge />}
                    <Chip>{p.stage}</Chip>
                  </div>
                  <h3 className="display mt-3 text-xl">
                    {p.to ? <InlineLink to={p.to}>{p.name}</InlineLink> : p.name}
                  </h3>
                  <p className="mt-1 text-sm font-semibold">
                    {p.city} · {p.units}
                  </p>
                  <p className="mt-1 text-sm text-muted-foreground">{p.developer}</p>
                  {view === "cards" ? (
                    <p className="mt-2 text-sm text-muted-foreground">{p.note}</p>
                  ) : null}
                  <SourceStamp
                    {...(p.real
                      ? {
                          source: "מקור: פרסום ציבורי — לשיבוץ קישור",
                          updated: "עודכן: תאריך לשיבוץ",
                          verification: "אימות: עובדות ציבוריות בלבד",
                        }
                      : {})}
                  />
                  <label className="mt-4 flex items-center gap-2 text-sm font-semibold">
                    <input
                      type="checkbox"
                      checked={compare.includes(p.name)}
                      onChange={() => toggleCompare(p.name)}
                      className="h-5 w-5"
                    />
                    הוסיפו להשוואה
                  </label>
                </Panel>
              ))}
            </ul>
          )}

          {state === "live" ? (
            <div className="mt-4">
              <LiveState
                title="מצב נתונים אמיתיים"
                body="מוצגים רק פרויקטים עם מקור ציבורי מזוהה. שדות המקור והתאריך נשארים ריקים עד למילוי אמיתי."
              />
            </div>
          ) : null}

          <nav aria-label="עימוד" className="mt-8">
            <ol className="flex flex-wrap items-center gap-2 text-sm font-bold">
              <li>
                <span
                  aria-current="page"
                  className="inline-flex rounded-md bg-primary px-4 py-2.5 text-primary-foreground"
                >
                  1
                </span>
              </li>
              <li className="text-muted-foreground">
                עמודים נוספים ייווצרו כקישורים ניתנים לסריקה (‎/projects/page/2/‎) כשיהיו
                מספיק רשומות — ללא טעינה אינסופית בלבד.
              </li>
            </ol>
          </nav>
        </Band>

        {compare.length > 0 && state !== "empty" ? (
          <div className="sticky bottom-0 z-30 border-t border-border bg-card">
            <div className="lab-container flex min-w-0 flex-wrap items-center justify-between gap-3 py-3">
              <p className="text-sm font-bold">בהשוואה: {compare.length} פרויקטים (עד 3)</p>
              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  onClick={() => setCompare([])}
                  className="tap rounded-md border border-border px-4 py-2.5 text-xs font-bold"
                >
                  ניקוי
                </button>
                <span className="tap inline-flex items-center rounded-md bg-secondary px-4 py-2.5 text-xs font-bold text-secondary-foreground">
                  ההשוואה נשמרת מקומית בדפדפן
                </span>
              </div>
            </div>
          </div>
        ) : null}

        <Band labelledBy="hubs-h">
          <BandHead
            id="hubs-h"
            eyebrow="עמודי צומת"
            title="ערים ויזמים"
            lead="רק צמתים עם מספיק רשומות אמיתיות נכנסים לאינדקס; השאר נשארים סינון פנימי."
          />
          <div className="grid gap-4 md:grid-cols-2">
            <Panel>
              <h3 className="display text-lg">פרויקטים לפי עיר</h3>
              <ul className="mt-3 flex flex-wrap gap-2">
                {cityHubs.map((c) => (
                  <li key={c}>
                    <button
                      type="button"
                      onClick={() => setCity(c)}
                      className="tap rounded-md border border-border bg-card px-3 py-2 text-xs font-bold hover:bg-secondary"
                    >
                      פרויקטים ב{c}
                    </button>
                  </li>
                ))}
              </ul>
            </Panel>
            <Panel>
              <h3 className="display text-lg">פרויקטים לפי יזם</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                עמוד יזם ייפתח רק כשיהיו לו שני פרויקטים ומעלה עם מקור ציבורי מזוהה. עד
                אז, סינון בלבד.
              </p>
            </Panel>
          </div>
        </Band>


        <Band labelledBy="why-h">
          <BandHead
            id="why-h"
            eyebrow="מבנה SEO"
            title="למה לכל פרויקט עמוד משלו"
            lead="ארכיון הפרויקטים תופס שאילתות רחבות; עמוד הפרויקט תופס שם מותג ושאילתות ספציפיות. אין כפילות כוונה."
          />
          <div className="grid gap-4 md:grid-cols-3">
            <Panel>
              <h3 className="display text-lg">ארכיון</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                ״פרויקטים חדשים בתל אביב״ — סינון, השוואה וניווט.
              </p>
            </Panel>
            <Panel>
              <h3 className="display text-lg">עמוד פרויקט</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                ״Rainbow שדה דב״ — עובדות, שלבים, מיקום ומסמכים ציבוריים.
              </p>
            </Panel>
            <Panel>
              <h3 className="display text-lg">נכסים בפרויקט</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                מודעות אמיתיות בלבד; היום ריק, עם קריאה לפרסום נכס.
              </p>
            </Panel>
          </div>
          <div className="mt-6">
            <MediaFrame
              label="מקום שמור לתצלום אווירה / תרשים מתחם"
              note="ממדים שמורים מראש, טעינה עצלה, ללא וידאו אוטומטי."
            />
          </div>
          <div className="mt-6 flex flex-wrap gap-3">
            <Action variant="copper" to="/production/nadlan/post-listing">
              הוסיפו פרויקט
            </Action>
            <InlineLink to="/production/nadlan/properties">מעבר לארכיון הנכסים</InlineLink>
          </div>
        </Band>

        <Band tone="surface" labelledBy="pj-faq">
          <BandHead id="pj-faq" eyebrow="שאלות נפוצות" title="על ארכיון הפרויקטים" />
          <FaqList items={faq} />
        </Band>
      </main>
    </ProductionShell>
  );
}

const impl: Impl = {
  intent:
    "כוונה מחקרית־ניווטית: גילוי פרויקטים לפי עיר ושלב. לא עמוד המרה ולא עמוד מודעה בודדת.",
  keywords: {
    primary: "פרויקטים חדשים",
    secondary: ["פרויקטים חדשים בתל אביב", "דירות מקבלן", "התחדשות עירונית", "פרויקטים בבנייה"],
  },
  meta: {
    title: "פרויקטים חדשים בישראל — ארכיון פרויקטים",
    description:
      "ארכיון פרויקטים חדשים לפי עיר, שלב בנייה וסוג יזמות, עם מקור ותאריך עדכון גלויים.",
    canonical: "https://nad-lan.co.il/projects/",
  },
  schema: [
    "BreadcrumbList",
    "CollectionPage + ItemList (רק רשומות אמיתיות)",
    "FAQPage",
    "ללא Offer — אין מחירים",
  ],
  internalLinks: [
    "עמוד פרויקט ← /production/nadlan/projects/rainbow-tel-aviv",
    "ארכיון נכסים ← /production/nadlan/properties",
    "הוספת פרויקט ← /production/nadlan/post-listing",
  ],
  dataPolicy: [
    "רשומת דמו מסומנת ואינה נכללת ב‑ItemList של הסכימה.",
    "מצב ״אין עדיין נתונים״ מציג CTA לאיסוף היצע במקום למלא בדמו.",
    "עובדות Rainbow מוגבלות למידע ציבורי; שדות מקור/תאריך מסומנים כלא מולאו.",
  ],
  wordpress: [
    "CPT: project — taxonomies: city, stage, developer",
    "Archive → block: nadlan/project-archive (facets = pre-rendered links)",
    "Card → block: nadlan/project-card",
    "State switch → block: nadlan/data-state (dev-only in production)",
  ],
};

