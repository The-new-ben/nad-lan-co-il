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
import { justiceCards, justiceMenu } from "@/lib/lab-data";

export const Route = createFileRoute("/justice/dual-audience")({
  head: () => ({
    meta: [
      { title: "J3 · שני קהלים — קונספט עמוד בית ל‑jus-tice.co.il" },
      {
        name: "description",
        content:
          "קונספט עם כניסה מפוצלת לאנשים פרטיים ולעורכי דין וחברות, מפת מוצר אחידה והצגה כנה של יכולות בפיתוח מול יכולות זמינות.",
      },
      { property: "og:title", content: "J3 · שני קהלים — Justice" },
      {
        property: "og:description",
        content: "כניסה מפוצלת, מפת מוצר אחת, בלי להציג יכולות שאינן זמינות.",
      },
    ],
  }),
  component: J3,
});

const tracks = {
  people: {
    label: "אנשים פרטיים",
    title: "מתכוננים להליך שנוגע לכם אישית",
    lead: "מבינים את השלבים, מתרגלים את הרגעים המכריעים ויוצאים עם רשימת שאלות מסודרת.",
    items: [
      "מיפוי ההליך בשפה פשוטה",
      "סימולציה לתרגול דיון וחקירה",
      "סיכום אישי לפגישה מקצועית",
    ],
    cta: "התחילו סימולציה",
  },
  pros: {
    label: "עורכי דין וחברות",
    title: "כלי הכנה לצוותים ולגורמים מקצועיים",
    lead: "שימוש בסימולציה להכנת לקוחות, תיאום ציפיות ותהליכי גישור בארגון.",
    items: [
      "הכנת לקוח לפני דיון",
      "תרחישי גישור לצוותים",
      "אזור מקצועי — בפיתוח, נפתח בהדרגה",
    ],
    cta: "בקשו גישה מקצועית",
  },
} as const;

type TrackKey = keyof typeof tracks;

function J3() {
  const [track, setTrack] = useState<TrackKey>("people");
  const current = tracks[track];

  return (
    <ConceptFrame id="j3" annotation={annotation} handoff={handoff}>
      <SiteHeader
        brand="Justice"
        menu={justiceMenu}
        primaryCta="התחילו סימולציה"
        secondaryCta="מצאו את המסלול שלכם"
      />

      <main id="main">
        <div className="lab-container pt-6">
          <Breadcrumbs trail={["דף הבית", "בחירת מסלול", "אנשים פרטיים"]} />
        </div>

        <Section className="pt-8">
          <Tag>מערכת אחת, שתי נקודות כניסה</Tag>
          <h1 className="display mt-4 max-w-3xl text-3xl leading-tight md:text-5xl">
            מרחב הכנה משפטית — לאנשים פרטיים ולגורמים מקצועיים
          </h1>
          <p className="mt-4 max-w-2xl text-lg leading-relaxed text-muted-foreground">
            בוחרים נקודת כניסה, ומקבלים את המסלול שמתאים לצורך: תרגול אישי לפני הליך,
            או שימוש מקצועי בהכנת לקוחות ותהליכים.
          </p>

          <div
            role="tablist"
            aria-label="בחירת קהל"
            className="mt-8 inline-flex rounded-xl border border-border bg-card p-1"
          >
            {(Object.keys(tracks) as TrackKey[]).map((k) => (
              <button
                key={k}
                role="tab"
                type="button"
                id={`tab-${k}`}
                aria-selected={track === k}
                aria-controls={`panel-${k}`}
                onClick={() => setTrack(k)}
                className={
                  "tap rounded-lg px-5 py-2 text-sm font-semibold " +
                  (track === k
                    ? "bg-primary text-primary-foreground"
                    : "text-card-foreground hover:bg-secondary")
                }
              >
                {tracks[k].label}
              </button>
            ))}
          </div>

          <div
            role="tabpanel"
            id={`panel-${track}`}
            aria-labelledby={`tab-${track}`}
            className="mt-6 grid gap-6 lg:grid-cols-2"
          >
            <Card>
              <h2 className="display text-xl">{current.title}</h2>
              <p className="mt-2 text-muted-foreground">{current.lead}</p>
              <ul className="mt-4 space-y-2">
                {current.items.map((i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <span aria-hidden="true" className="mt-1 text-highlight">
                      ▪
                    </span>
                    {i}
                  </li>
                ))}
              </ul>
              <div className="mt-5 flex flex-wrap gap-3">
                <Cta>{current.cta}</Cta>
                <Cta variant="secondary">מצאו את המסלול שלכם</Cta>
              </div>
            </Card>
            <Card>
              <div className="flex items-center justify-between">
                <h2 className="display text-xl">מפת המוצר</h2>
                <ExampleBadge />
              </div>
              <ul className="mt-4 grid gap-3 sm:grid-cols-2">
                {[
                  { t: "סימולציה", s: "זמין", d: "תרגול מונחה לפי תרחיש" },
                  { t: "מדריכי הכנה", s: "זמין", d: "תוכן הסברתי לפי תחום" },
                  { t: "סביבת עבודה מקצועית", s: "בפיתוח", d: "מנוהל ב‑jus-tice.com" },
                  { t: "שוק שירותים", s: "בתכנון", d: "מנוהל ב‑jus-tice.com" },
                ].map((m) => (
                  <li key={m.t} className="rounded-lg border border-border bg-surface p-3">
                    <div className="flex items-center justify-between gap-2">
                      <span className="font-bold">{m.t}</span>
                      <span className="rounded-full bg-accent px-2 py-0.5 text-xs font-bold text-accent-foreground">
                        {m.s}
                      </span>
                    </div>
                    <p className="mt-1 text-xs text-muted-foreground">{m.d}</p>
                  </li>
                ))}
              </ul>
              <p className="mt-4 text-xs text-muted-foreground">
                סטטוס מוצג במפורש. יכולות שאינן פעילות אינן מוצגות כאילו הן פועלות.
              </p>
            </Card>
          </div>
        </Section>

        <Section tone="surface">
          <SectionHead
            eyebrow="נושאים וכלים"
            title="מה מחפשים אצלנו — ולאן זה ממשיך"
            lead="אותו מאגר תוכן משרת את שני הקהלים, אך הקישור ההקשרי משתנה לפי המסלול."
          />
          <ul className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
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
          <SectionHead eyebrow="איך זה עובד" title="אותו מנוע, שני מסלולי שימוש" />
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <h3 className="display text-lg">מסלול אישי</h3>
              <ol className="mt-3 space-y-2 text-sm text-muted-foreground">
                <li>1. מתארים את המצב</li>
                <li>2. מתרגלים תרחיש</li>
                <li>3. יוצאים עם סיכום ושאלות</li>
              </ol>
              <div className="mt-4">
                <ContextLink href="/justice/how-it-works">
                  ראו כיצד בנוי מסלול ההכנה האישי
                </ContextLink>
              </div>
            </Card>
            <Card>
              <h3 className="display text-lg">מסלול מקצועי</h3>
              <ol className="mt-3 space-y-2 text-sm text-muted-foreground">
                <li>1. מגדירים תרחיש ללקוח או לצוות</li>
                <li>2. משתפים את התרגול</li>
                <li>3. מקבלים סיכום לתיאום ציפיות</li>
              </ol>
              <div className="mt-4">
                <ContextLink href="/justice/for-lawyers">
                  קראו על השימוש המקצועי בסימולציה
                </ContextLink>
              </div>
            </Card>
          </div>
        </Section>

        <Section tone="surface">
          <SectionHead eyebrow="שקיפות" title="גבולות הכלי וניהול המידע" />
          <TrustBlocks
            reviewer="בדיקת תוכן על ידי עורך/ת דין, עם שם ותאריך — מציין מיקום לשיבוץ, טרם מולא."
            method="מוסבר כיצד נבנים התרחישים לשני הקהלים ומה ההבדל בין המסלולים."
            privacy="הפרדה בין שימוש אישי לשימוש מקצועי, כולל הרשאות שיתוף ומחיקה."
            sourceDate="לכל תרחיש ולכל מדריך מוצג תאריך עדכון ובדיקת מקורות."
            limits="הכלי אינו ייעוץ משפטי ואינו מחליף שיקול דעת מקצועי."
          />
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
    "הכניסה המפוצלת מפרידה שתי כוונות חיפוש שונות לחלוטין בלי לפצל את עמוד הבית לשני H1.",
    "מפת המוצר מקשרת אל jus-tice.com בלי לשכפל את התוכן שלו — הפניה, לא העתקה.",
    "H1 יחיד מכליל את שני הקהלים; ההתמחות מתרחשת בעמודי המשך ייעודיים.",
  ],
  keywordOwner: [
    "קהל פרטי: ביטויים בעברית סביב הכנה, עלויות ותהליכים — נשארים ב‑jus-tice.co.il.",
    "קהל מקצועי: ביטויים סביב כלי עבודה, סביבת ניהול ומרקטפלייס — נכסים של jus-tice.com.",
    "עמוד ״לעורכי דין״ בקו.איל מכוון לביטויי שיתוף פעולה בעברית בלבד, לא לביטויי מוצר.",
  ],
  menuLogic: [
    "התפריט נשאר זהה לשאר הקונספטים כדי לשמור על ארכיטקטורה אחידה בין הכיוונים.",
    "המיון נקבע לפי גודל הביקוש ולא לפי חשיבות פנימית: נושא, כלי, אמון, קהל משני, ארכיון.",
    "פיצול הקהלים מתרחש בגוף העמוד ולא בתפריט, כדי לא להכפיל ניווט.",
  ],
  conversionLogic: [
    "בחירת מסלול היא מיקרו־המרה שמאפשרת התאמת CTA בלי דפי נחיתה נפרדים.",
    "עבור מקצוענים ה‑CTA הוא בקשת גישה — הצהרה כנה על יכולת שנפתחת בהדרגה.",
    "סטטוס ״בפיתוח/בתכנון״ מוצג במפורש כדי למנוע ציפייה שגויה ופגיעה באמון.",
    "CTA ראשי ומשני נשארים זהים בכל הקונספטים לצורך השוואה נקייה.",
  ],
};

const handoff = {
  tokens: [
    { name: "--color-primary", value: "oklch(0.5 0.13 250)", usage: "כפתורים ולשוניות פעילות" },
    { name: "--color-accent", value: "oklch(0.93 0.04 190)", usage: "תגיות סטטוס" },
    { name: "--color-surface", value: "oklch(0.965 0.005 250)", usage: "רקע פריטים במפת המוצר" },
    { name: "--radius", value: "1rem", usage: "פינות רכות בסגנון מערכת" },
    { name: "--font-sans", value: "Heebo", usage: "ממשק וטקסט" },
  ],
  blocks: [
    { name: "Audience Switch", desc: "לשוניות נגישות עם tablist/tabpanel" },
    { name: "Product Map", desc: "רשת יכולות עם תגית סטטוס חובה" },
    { name: "Track Card", desc: "כרטיס מסלול עם רשימת יכולות ו‑CTA" },
    { name: "Dual Steps", desc: "שני טורי שלבים, אישי מול מקצועי" },
    { name: "Trust Stack", desc: "בלוקי אמון משותפים לכל התבניות" },
  ],
  menu: [
    { label: "תחומי משפט", children: ["משפחה", "פלילי", "אזרחי", "עבודה"] },
    { label: "כלים וסימולציות", children: ["סימולציה אישית", "תרחישים לצוותים"] },
    { label: "איך זה עובד", children: ["מסלול אישי", "מסלול מקצועי", "מגבלות"] },
    { label: "לעורכי דין", children: ["בקשת גישה", "שיתופי פעולה"] },
    { label: "ידע משפטי", children: ["מדריכים", "מונחים"] },
  ],
  schema: [
    "WebSite + Organization בעמוד הבית",
    "SoftwareApplication רק ליכולות שכבר זמינות בפועל",
    "BreadcrumbList בכל עמוד פנימי",
    "sameAs להפניה מסודרת בין הדומיינים",
    "ללא offers או price — אין תמחור מוצג",
  ],
  performance: [
    "מחליף הקהלים ברכיב קל ללא ספריית UI כבדה",
    "אין תמונות מעל הקיפול; המשקל העיקרי הוא טקסט",
    "טעינה עצלה לכל בלוק מתחת לקיפול",
    "יעד TBT נמוך: מינימום JS בעמוד הבית",
    "prefers-reduced-motion מכבד ומבטל מעברים",
  ],
};

