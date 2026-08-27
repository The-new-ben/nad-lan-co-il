import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
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
  MediaFrame,
  Panel,
  SourceStamp,
  type DataState,
} from "@/components/production/ui";

export const Route = createFileRoute("/production/nadlan/properties/")({
  head: () => ({
    meta: [
      { title: "נכסים למכירה ולהשכרה — ארכיון מודעות" },
      {
        name: "description",
        content:
          "ארכיון נכסים עם סינון לפי עיר, סוג עסקה, חדרים ושטח. בשלב זה מוצגות מודעות לדוגמה מסומנות, עד לפרסום מלאי אמיתי.",
      },
      { property: "og:title", content: "ארכיון נכסים" },
      { property: "og:description", content: "סינון נכסים לפי עיר, עסקה וחדרים. מודעות לדוגמה מסומנות." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "robots", content: "noindex, nofollow" },
    ],
  }),
  component: PropertiesArchive,
});

type Listing = {
  id: string;
  title: string;
  city: string;
  area: string;
  deal: "מכירה" | "השכרה";
  rooms: number;
  size: number;
  to?: string;
};

const listings: Listing[] = [
  {
    id: "baka",
    title: "דירת 4 חדרים בבקעה",
    city: "ירושלים",
    area: "בקעה",
    deal: "מכירה",
    rooms: 4,
    size: 96,
    to: "/production/nadlan/properties/baka-demo",
  },
  { id: "l2", title: "דירת גן בפלורנטין", city: "תל אביב", area: "פלורנטין", deal: "השכרה", rooms: 3, size: 72 },
  { id: "l3", title: "פנטהאוז בכרמל הצרפתי", city: "חיפה", area: "כרמל", deal: "מכירה", rooms: 5, size: 140 },
  { id: "l4", title: "דירת 2 חדרים ברמת אביב", city: "תל אביב", area: "רמת אביב", deal: "השכרה", rooms: 2, size: 55 },
  { id: "l5", title: "בית פרטי ברמות", city: "באר שבע", area: "רמות", deal: "מכירה", rooms: 6, size: 180 },
  { id: "l6", title: "דירת 3 חדרים בקטמונים", city: "ירושלים", area: "קטמונים", deal: "מכירה", rooms: 3, size: 78 },
  { id: "l7", title: "סטודיו במרכז הכרמל", city: "חיפה", area: "מרכז הכרמל", deal: "השכרה", rooms: 1, size: 38 },
];

const faq = [
  {
    q: "האם המודעות כאן אמיתיות?",
    a: "לא. שבע המודעות המוצגות הן דוגמאות מסומנות שנועדו להמחיש את חוויית החיפוש עד שבעלי נכסים ומתווכים יפרסמו מלאי אמיתי.",
  },
  {
    q: "למה אין מחירים?",
    a: "מחיר יוצג רק כשיגיע ממודעה אמיתית שפורסמה על ידי בעל הנכס או מתווך מורשה. לא נמציא טווחי מחיר.",
  },
  {
    q: "מה קורה כשאין נתונים בעיר מסוימת?",
    a: "מוצג מצב ״אין עדיין נתונים״ עם קריאה לפרסום נכס, במקום למלא את המסך במודעות מומצאות.",
  },
];

function PropertiesArchive() {
  const [state, setState] = useState<DataState>("demo");
  const [city, setCity] = useState("הכול");
  const [deal, setDeal] = useState("הכול");
  const [rooms, setRooms] = useState("הכול");
  const [minSize, setMinSize] = useState(0);
  const [view, setView] = useState<"list" | "map">("list");
  const [compare, setCompare] = useState<string[]>([]);

  const cities = ["הכול", ...Array.from(new Set(listings.map((l) => l.city)))];

  const filtered = useMemo(
    () =>
      listings.filter(
        (l) =>
          (city === "הכול" || l.city === city) &&
          (deal === "הכול" || l.deal === deal) &&
          (rooms === "הכול" || l.rooms >= Number(rooms)) &&
          l.size >= minSize,
      ),
    [city, deal, rooms, minSize],
  );

  const toggleCompare = (id: string) =>
    setCompare((c) => (c.includes(id) ? c.filter((x) => x !== id) : [...c, id].slice(0, 3)));

  return (
    <ProductionShell
      route="/production/nadlan/properties"
      impl={impl}
      headerPrimaryCta="פרסמו נכס אמיתי חינם"
    >
      <main id="main">
        <div className="lab-container pt-5">
          <Crumbs trail={[{ label: "דף הבית", to: "/production/nadlan" }, { label: "נכסים" }]} />
        </div>

        <Band className="pt-6" labelledBy="pr-h1">
          <h1 id="pr-h1" className="display text-3xl leading-tight md:text-4xl">
            נכסים למכירה ולהשכרה — ארכיון מודעות
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-muted-foreground">
            שבע המודעות שמוצגות כאן הן <strong>דוגמאות מכוונות</strong> שממחישות את חוויית
            החיפוש, הסינון וההשוואה — עד שבעלי נכסים ומתווכים יוסיפו מלאי אמיתי. אין כאן
            מחירים, זמינות או פרטי קשר אמיתיים.
          </p>
          <div className="mt-6 flex flex-wrap items-center gap-4">
            <Action variant="copper" to="/production/nadlan/post-listing">
              פרסמו נכס אמיתי חינם
            </Action>
            <InlineLink to="/production/nadlan/projects">חיפוש לפי פרויקטים</InlineLink>
          </div>
          <div className="mt-6">
            <DataStateSwitch value={state} onChange={setState} />
          </div>
        </Band>

        <Band tone="surface" labelledBy="pr-filters">
          <BandHead
            id="pr-filters"
            eyebrow="סינון"
            title="צמצמו את התוצאות"
            lead="הסינון עובד על הדוגמאות כדי להדגים את ההיגיון והמהירות של החיפוש."
          />
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
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
              סוג עסקה
              <select
                value={deal}
                onChange={(e) => setDeal(e.target.value)}
                className="tap mt-2 w-full rounded-md border border-border bg-card px-3 py-3 text-sm font-semibold"
              >
                {["הכול", "מכירה", "השכרה"].map((d) => (
                  <option key={d}>{d}</option>
                ))}
              </select>
            </label>
            <label className="block text-sm font-bold">
              חדרים (מינימום)
              <select
                value={rooms}
                onChange={(e) => setRooms(e.target.value)}
                className="tap mt-2 w-full rounded-md border border-border bg-card px-3 py-3 text-sm font-semibold"
              >
                {["הכול", "2", "3", "4", "5"].map((r) => (
                  <option key={r}>{r}</option>
                ))}
              </select>
            </label>
            <label className="block text-sm font-bold">
              שטח מינימלי: {minSize} מ״ר
              <input
                type="range"
                min={0}
                max={180}
                step={10}
                value={minSize}
                onChange={(e) => setMinSize(Number(e.target.value))}
                className="mt-4 w-full"
              />
            </label>
          </div>

          <Panel className="mt-5 border-dashed">
            <p className="text-sm font-bold">מחיר</p>
            <p className="mt-1 text-sm text-muted-foreground">
              מסנן המחיר יופעל רק כשיהיו מודעות אמיתיות עם מחיר שפורסם. אין הצגת טווחי
              מחיר משוערים.
            </p>
          </Panel>

          <div className="mt-6 flex flex-wrap items-center justify-between gap-3">
            <p className="text-sm font-semibold">
              {state === "empty"
                ? "אין עדיין תוצאות"
                : `${state === "live" ? 0 : filtered.length} תוצאות · תצלום מצב מהדוגמאות, אינו מדד שוק`}
            </p>
            <div role="group" aria-label="תצוגת תוצאות" className="flex gap-1">
              {(["list", "map"] as const).map((v) => (
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
                  {v === "list" ? "רשימה" : "מפה"}
                </button>
              ))}
            </div>
          </div>

          {state === "empty" ? (
            <div className="mt-5">
              <EmptyState
                title="אין עדיין נכסים באזור הזה"
                body="כך ייראה המסך למשתמש בעיר שטרם פורסמו בה מודעות. לא מוצגות דוגמאות, ולא נטען מלאי ממקור אחר."
                ctaLabel="פרסמו נכס אמיתי חינם"
              />
            </div>
          ) : state === "live" ? (
            <Panel className="mt-5 border-dashed">
              <h2 className="display text-lg">נתונים אמיתיים</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                במצב זה מוצגות רק מודעות שפורסמו ואומתו. כרגע אין אף מודעה כזו, ולכן
                הרשימה ריקה בכוונה.
              </p>
              <SourceStamp />
              <div className="mt-4">
                <Action variant="copper" to="/production/nadlan/post-listing">
                  היו הראשונים לפרסם
                </Action>
              </div>
            </Panel>
          ) : view === "map" ? (
            <div className="mt-5">
              <MediaFrame
                label="מקום שמור למפת תוצאות סטטית"
                note="נטענת בלחיצה בלבד. סימוני המפה מייצגים דוגמאות ולא מלאי אמיתי."
              />
            </div>
          ) : (
            <ul className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {filtered.map((l) => (
                <Panel as="li" key={l.id} className="border-dashed">
                  <DemoBadge label="נכס לדוגמה" />
                  <h3 className="display mt-3 text-lg">
                    {l.to ? <InlineLink to={l.to}>{l.title}</InlineLink> : l.title}
                  </h3>
                  <p className="mt-1 text-sm font-semibold">
                    {l.city} · {l.area}
                  </p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    <Chip>{l.deal}</Chip>
                    <Chip>{l.rooms} חדרים</Chip>
                    <Chip>{l.size} מ״ר</Chip>
                  </div>
                  <p className="mt-3 text-xs text-muted-foreground">
                    מחיר: דוגמה — לא מוצג · פרטי קשר: לא זמינים בדוגמה
                  </p>
                  <label className="mt-4 flex items-center gap-2 text-sm font-semibold">
                    <input
                      type="checkbox"
                      checked={compare.includes(l.id)}
                      onChange={() => toggleCompare(l.id)}
                      className="h-5 w-5"
                    />
                    הוסיפו להשוואה
                  </label>
                </Panel>
              ))}
            </ul>
          )}
        </Band>

        {compare.length > 0 && state === "demo" ? (
          <div className="sticky bottom-0 z-30 border-t border-border bg-card">
            <div className="lab-container flex min-w-0 flex-wrap items-center justify-between gap-3 py-3">
              <p className="text-sm font-bold">
                בהשוואה: {compare.length} נכסים לדוגמה (עד 3)
              </p>
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

        <Band labelledBy="pr-supply">
          <BandHead
            id="pr-supply"
            eyebrow="היצע אמיתי"
            title="הדוגמאות נעלמות ברגע שיש מלאי"
            lead="ככל שיתווספו מודעות מאומתות, הן יחליפו את הדוגמאות ויקבלו מקור, תאריך עדכון וסטטוס אימות."
          />
          <div className="flex flex-wrap gap-3">
            <Action variant="copper" to="/production/nadlan/post-listing">
              פרסמו נכס אמיתי חינם
            </Action>
            <InlineLink to="/production/nadlan/properties/baka-demo">
              צפו במודעה לדוגמה במלואה
            </InlineLink>
          </div>
        </Band>

        <Band tone="surface" labelledBy="pr-faq">
          <BandHead id="pr-faq" eyebrow="שאלות נפוצות" title="על ארכיון הנכסים" />
          <FaqList items={faq} />
        </Band>
      </main>
    </ProductionShell>
  );
}

const impl: Impl = {
  intent:
    "כוונה מסחרית־חיפושית: משתמש שמחפש נכס לפי עיר, עסקה וחדרים. העמוד הוא צומת סינון, לא עמוד תוכן.",
  keywords: {
    primary: "דירות למכירה",
    secondary: ["דירות להשכרה", "דירות למכירה בירושלים", "דירות 4 חדרים", "נכסים למכירה"],
  },
  meta: {
    title: "נכסים למכירה ולהשכרה — ארכיון מודעות",
    description:
      "ארכיון נכסים עם סינון לפי עיר, סוג עסקה, חדרים ושטח. בשלב זה מוצגות מודעות לדוגמה מסומנות.",
    canonical: "https://nad-lan.co.il/properties/",
  },
  schema: [
    "BreadcrumbList",
    "CollectionPage + ItemList — רק כשיהיו מודעות אמיתיות",
    "FAQPage",
    "ללא Offer/Price כל עוד הרשומות הן דוגמאות",
  ],
  internalLinks: [
    "מודעה לדוגמה ← /production/nadlan/properties/baka-demo",
    "ארכיון פרויקטים ← /production/nadlan/projects",
    "פרסום נכס ← /production/nadlan/post-listing",
  ],
  dataPolicy: [
    "כל כרטיס דוגמה נושא תווית ״נכס לדוגמה״ גלויה.",
    "שלושה מצבי ממשק: דמו / אין עדיין נתונים / נתונים אמיתיים.",
    "אין מחירים, פרטי קשר, כמות צפיות או נתוני שוק.",
    "מונה התוצאות מנוסח כתצלום מצב של הדוגמאות, לא כמדד שוק.",
  ],
  wordpress: [
    "CPT: listing — taxonomies: city, area, deal_type",
    "Archive → block: nadlan/listing-archive (facets מוגבלות לאינדוקס)",
    "Card → block: nadlan/listing-card (demo flag = post meta)",
    "Compare tray → block: nadlan/compare-tray (localStorage)",
    "אינדוקס: עיר + סוג עסקה בלבד; שאר הפאסטים noindex,follow",
  ],
};

