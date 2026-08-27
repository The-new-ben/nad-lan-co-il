import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { JusticeShell, Notice, type Impl } from "@/components/production/JusticeShell";
import {
  Band,
  BandHead,
  Chip,
  Crumbs,
  FaqList,
  InlineLink,
  Panel,
  Tabs,
} from "@/components/production/ui";

export const Route = createFileRoute("/production/justice/legal-ai-desk")({
  head: () => ({
    meta: [
      { title: "עזרה עם AI — ספרו מה קרה וקבלו תמונת מצב ראשונית" },
      {
        name: "description",
        content:
          "תיאור חופשי של מה שקרה או העלאת מסמך, ובתמורה סיכום בשפה פשוטה, שאלות הבהרה, סוגיות רלוונטיות ומה הצעד הבא. מידע כללי, לא ייעוץ משפטי.",
      },
      { property: "og:title", content: "שולחן ה‑AI המשפטי — הבנת המצב לפני ההחלטה" },
      {
        property: "og:description",
        content: "אבחון כוונה ראשוני בעברית: סיכום, שאלות, מסמכים לאסוף וצעד הבא.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "robots", content: "noindex, nofollow" },
    ],
  }),
  component: LegalAiDesk,
});

const examples = [
  "פוטרתי בלי שימוע ואמרו לי לחתום על מכתב עזיבה",
  "יש לי דיון ראשון בענייני משפחה בעוד שבועיים",
  "קיבלתי תביעה קטנה על נזק לרכב",
  "אני רוצה לבדוק מחיקת רישום פלילי ישן",
];

const outputBlocks: { t: string; d: string; body: string[] }[] = [
  {
    t: "סיכום בשפה פשוטה",
    d: "מה הבנו מהתיאור שלכם, בלי ז׳רגון.",
    body: [
      "תיאור מנוסח מחדש בשלוש־ארבע שורות.",
      "מה מוגדר כאירוע המרכזי ומה נלווה לו.",
    ],
  },
  {
    t: "שאלות הבהרה",
    d: "מה חסר כדי להבין את התמונה.",
    body: ["תאריכים מדויקים", "האם קיים תיעוד בכתב", "האם נשלחה הודעה רשמית"],
  },
  {
    t: "סוגיות וזכויות רלוונטיות",
    d: "כותרות כלליות בלבד, עם קישור להסבר.",
    body: ["ההליך שסביר שרלוונטי", "מונחים שכדאי להכיר לפני פנייה"],
  },
  {
    t: "דחיפות ומועדים",
    d: "האם יש משהו שרץ מול שעון.",
    body: ["האם קיים מועד קרוב", "מה נהוג לעשות קודם", "בלי מתן ספירת ימים כעובדה"],
  },
  {
    t: "מסמכים לאסוף",
    d: "רשימה מעשית להכנה.",
    body: ["התכתבויות", "מסמכים רשמיים שהתקבלו", "אסמכתאות תשלום או נוכחות"],
  },
  {
    t: "הצעד הבא",
    d: "מסלול אחד מומלץ, לא ארבעה.",
    body: ["מדריך ממוקד, כלי, סימולציה — או פנייה לאיש מקצוע"],
  },
];

const nextActions = [
  {
    t: "מדריך ממוקד",
    d: "הסבר קצר על ההליך הרלוונטי, בלי קיר טקסט.",
    cta: "לקריאה",
    href: "#",
  },
  {
    t: "סימולציית דיון",
    d: "כשיש מועד דיון ורוצים להתאמן על שאלות וחקירה.",
    cta: "לעמוד הסימולציה",
    to: "/production/justice/legal-simulation" as const,
  },
  {
    t: "מחשבון או מסמך",
    d: "כשצריך אומדן עלות או טופס להכנה. הכלים עצמם עדיין לא נבנו.",
    cta: "אב טיפוס",
    disabled: true,
  },
  {
    t: "התאמת עורך/ת דין",
    d: "כשהמצב חורג ממידע כללי. אין רשימת עורכי דין פעילה באב הטיפוס.",
    cta: "אב טיפוס",
    disabled: true,
  },
];

const events = [
  { e: "scenario_started", d: "המשתמש התחיל לתאר מצב או בחר תרחיש מוכן." },
  { e: "intake_completed", d: "התיאור הושלם והוצגה תמונת המצב הראשונית." },
  { e: "simulation_bridge_clicked", d: "לחיצה על מעבר לסימולטור ב‑jus-tice.com." },
  { e: "lawyer_match_requested", d: "בקשה מפורשת להתאמת איש מקצוע." },
];

const faq = [
  {
    q: "זה ייעוץ משפטי?",
    a: "לא. זהו מידע כללי שנועד לעזור להבין את המצב ולהתכונן. אין כאן חוות דעת, אין התאמה לתיק ספציפי ולא נוצרים יחסי עורך דין–לקוח.",
  },
  {
    q: "מה קורה למה שאני כותב?",
    a: "באב הטיפוס הזה שום דבר לא נשלח ולא נשמר — הממשק אינו מחובר. במוצר, מדיניות השמירה והמחיקה תוצג בגלוי לפני הזנת טקסט.",
  },
  {
    q: "האם אפשר להעלות מסמך?",
    a: "הכרטיסייה קיימת כתצוגת ממשק בלבד. אין העלאה, אין קריאה ואין ניתוח מסמכים בשלב הזה.",
  },
];

function TellUsPanel() {
  const [text, setText] = useState("");
  return (
    <div className="grid gap-4 lg:grid-cols-[1.2fr_1fr]">
      <Panel>
        <label htmlFor="desk-text" className="text-sm font-bold">
          ספרו מה קרה — בלשון חופשית
        </label>
        <p className="mt-1 text-xs text-muted-foreground">
          בלי שמות מלאים, מספרי תיק או פרטי צד שלישי.
        </p>
        <textarea
          id="desk-text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={6}
          placeholder="לדוגמה: קיבלתי מכתב מהמעסיק ואני לא בטוח מה המשמעות שלו…"
          className="mt-3 w-full rounded-md border border-border bg-background p-3 text-sm leading-relaxed"
        />
        <div className="mt-3 flex flex-wrap gap-2">
          {examples.map((x) => (
            <button
              key={x}
              type="button"
              onClick={() => setText(x)}
              className="tap min-h-11 rounded-md border border-border bg-card px-3 py-2 text-xs font-semibold hover:bg-secondary"
            >
              {x}
            </button>
          ))}
        </div>
        <p className="mt-4 text-xs text-muted-foreground">
          אב טיפוס: הכפתור אינו מחובר ואינו שולח דבר.
        </p>
        <button
          type="button"
          className="tap mt-2 inline-flex min-h-11 items-center rounded-md bg-primary px-5 py-3 text-sm font-bold text-primary-foreground"
        >
          קבלו תמונת מצב ראשונית
        </button>
      </Panel>
      <Panel className="border-dashed">
        <h3 className="display text-lg">מה יקרה אחרי השליחה</h3>
        <ol className="mt-3 list-decimal space-y-2 ps-5 text-sm leading-relaxed text-muted-foreground">
          <li>ניסוח מחדש של מה שכתבתם, כדי לוודא שהובנתם.</li>
          <li>שאלות הבהרה קצרות במקום הנחות.</li>
          <li>הצגת הסוגיות הכלליות ומה שכדאי להכין.</li>
          <li>המלצה על מסלול המשך אחד.</li>
        </ol>
      </Panel>
    </div>
  );
}

function UploadPanel() {
  return (
    <div className="grid gap-4 lg:grid-cols-[1.2fr_1fr]">
      <Panel>
        <h3 className="display text-lg">העלו מסמך</h3>
        <div className="mt-3 rounded-lg border-2 border-dashed border-border bg-surface p-8 text-center">
          <p className="text-sm font-bold">גררו קובץ לכאן או בחרו מהמחשב</p>
          <p className="mt-1 text-xs text-muted-foreground">
            PDF או תמונה · תצוגת ממשק בלבד, אין העלאה בפועל
          </p>
          <button
            type="button"
            disabled
            className="tap mt-4 inline-flex min-h-11 cursor-not-allowed items-center rounded-md border border-border bg-card px-4 py-2 text-sm font-bold text-muted-foreground"
          >
            בחירת קובץ (לא פעיל)
          </button>
        </div>
        <div className="mt-4">
          <Notice tone="legal" title="לפני העלאה של מסמך אמיתי">
            אל תעלו מסמכים עם פרטים מזהים של צד שלישי. במוצר תוצג מדיניות שמירה, הצפנה
            ומחיקה לפני ההעלאה הראשונה.
          </Notice>
        </div>
      </Panel>
      <Panel className="border-dashed">
        <h3 className="display text-lg">דוגמאות למסמכים שמתאימים</h3>
        <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
          <li>מכתב פיטורים או זימון לשימוע</li>
          <li>כתב תביעה או הזמנה לדיון</li>
          <li>הסכם שנשלח לחתימה</li>
        </ul>
        <p className="mt-4 text-xs text-muted-foreground">
          ניתוח מסמכים אינו קיים בשלב זה ואינו מובטח כתכולה.
        </p>
      </Panel>
    </div>
  );
}

function LegalAiDesk() {
  return (
    <JusticeShell
      route="/production/justice/legal-ai-desk"
      impl={impl}
      headerPrimaryCta="ספרו מה קרה"
      headerPrimaryHref="#desk"
    >
      <main id="main">
        <section className="border-b border-border bg-surface py-12 text-surface-foreground md:py-16">
          <div className="lab-container">
            <Crumbs
              trail={[{ label: "בית", to: "/production/justice" }, { label: "עזרה עם AI" }]}
            />
            <h1 className="display mt-4 max-w-3xl text-3xl leading-tight md:text-4xl">
              עזרה עם AI — ספרו מה קרה, וקבלו תמונת מצב ראשונית
            </h1>
            <p className="mt-4 max-w-2xl text-base leading-relaxed text-muted-foreground md:text-lg">
              רוב האנשים לא יודעים איך לקרוא למצב שלהם, ולכן גם לא יודעים מה לחפש. כאן
              מתארים במילים רגילות מה קרה — והתוצאה היא סיכום ברור, שאלות הבהרה, מה להכין
              ומה הצעד הבא.
            </p>
            <div className="mt-6">
              <Notice tone="legal" title="מידע כללי, לא ייעוץ משפטי">
                השירות אינו נותן חוות דעת, אינו מעריך סיכויים ואינו יוצר יחסי עורך
                דין–לקוח. באב הטיפוס אין עיבוד, שליחה או שמירה של טקסט.
              </Notice>
            </div>
          </div>
        </section>

        <Band id="desk" labelledBy="d-intake">
          <BandHead
            id="d-intake"
            eyebrow="אבחון ראשוני"
            title="שתי דרכים להתחיל"
            lead="הממשק להמחשה בלבד — אין חיבור לשרת, אין מודל ואין שמירה."
          />
          <Tabs
            ariaLabel="דרכי פנייה"
            items={[
              { id: "tell", label: "ספרו מה קרה", content: <TellUsPanel /> },
              { id: "upload", label: "העלו מסמך", content: <UploadPanel /> },
            ]}
          />
        </Band>

        <Band tone="surface" labelledBy="d-output">
          <BandHead
            id="d-output"
            eyebrow="תצוגת פלט"
            title="מבנה התשובה — קבוע, צפוי וניתן לבדיקה"
            lead="הפלט תמיד באותו סדר, כדי שאפשר יהיה לבקר אותו עריכתית ולא להסתמך על ניסוח חופשי."
          />
          <ul className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {outputBlocks.map((b, i) => (
              <Panel as="li" key={b.t}>
                <Chip>{`שלב ${i + 1}`}</Chip>
                <h3 className="display mt-3 text-lg">{b.t}</h3>
                <p className="mt-1 text-sm text-muted-foreground">{b.d}</p>
                <ul className="mt-3 space-y-1.5 text-sm text-muted-foreground">
                  {b.body.map((x) => (
                    <li key={x} className="border-s-2 border-s-border ps-3">
                      {x}
                    </li>
                  ))}
                </ul>
              </Panel>
            ))}
          </ul>
        </Band>

        <Band labelledBy="d-next">
          <BandHead
            id="d-next"
            eyebrow="המשך"
            title="מסלול המשך אחד, לפי מה שסופר"
            lead="לא מציגים ארבעה כפתורים שווי־ערך. מסלול אחד מודגש, השאר משניים."
          />
          <ul className="grid gap-4 md:grid-cols-2">
            {nextActions.map((a) => (
              <Panel as="li" key={a.t} className={a.disabled ? "border-dashed" : ""}>
                <h3 className="display text-lg">{a.t}</h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{a.d}</p>
                <div className="mt-4">
                  {a.disabled ? (
                    <span className="inline-flex items-center rounded-md border border-dashed border-border px-3 py-2 text-xs font-bold text-muted-foreground">
                      {a.cta}
                    </span>
                  ) : a.to ? (
                    <InlineLink to={a.to}>{a.cta}</InlineLink>
                  ) : (
                    <InlineLink href={a.href}>{a.cta}</InlineLink>
                  )}
                </div>
              </Panel>
            ))}
          </ul>
        </Band>

        <Band tone="surface" labelledBy="d-events">
          <BandHead
            id="d-events"
            eyebrow="מדידה"
            title="אירועי משפך — הגדרה בלבד, ללא נתונים"
            lead="אין באב הטיפוס מספרי המרה, משתמשים או ביצועים. אלה שמות האירועים שיוגדרו במוצר."
          />
          <ul className="grid gap-3 md:grid-cols-2">
            {events.map((x) => (
              <li
                key={x.e}
                className="rounded-md border border-border bg-card p-4 text-card-foreground"
              >
                <code className="text-sm font-bold text-primary">{x.e}</code>
                <p className="mt-1 text-sm text-muted-foreground">{x.d}</p>
              </li>
            ))}
          </ul>
        </Band>

        <Band labelledBy="d-faq">
          <BandHead id="d-faq" eyebrow="שאלות נפוצות" title="גבולות, פרטיות ומה לא קיים" />
          <FaqList items={faq} />
          <div className="mt-6">
            <InlineLink to="/production/justice/legal-simulation">
              יש לכם כבר מועד דיון? עברו להכנה ולסימולציה
            </InlineLink>
          </div>
        </Band>
      </main>
    </JusticeShell>
  );
}

const impl: Impl = {
  intent:
    "כוונת חיפוש בעייתית־ראשונית: ״מה עושים אם…״, ״קיבלתי מכתב מ…״. העמוד מתרגם תיאור חופשי לכוונה מסווגת ומנתב הלאה — זהו שער הכשרה (qualification), לא עמוד תוכן.",
  keywords: {
    primary: "עזרה משפטית עם AI · ספרו מה קרה",
    secondary: [
      "מה עושים אחרי פיטורים",
      "קיבלתי תביעה קטנה מה עכשיו",
      "איך מבינים מכתב משפטי",
    ],
  },
  meta: {
    title: "עזרה עם AI — ספרו מה קרה וקבלו תמונת מצב ראשונית",
    description:
      "תיאור חופשי או מסמך, ובתמורה סיכום, שאלות הבהרה, סוגיות, מסמכים לאסוף וצעד הבא. מידע כללי בלבד.",
    canonical: "https://jus-tice.co.il/legal-ai-desk/ (אב טיפוס: noindex,nofollow)",
  },
  schema: [
    "WebPage + BreadcrumbList",
    "FAQPage על שלוש השאלות הגלויות בלבד",
    "ללא Review/Person/Service — אין אנשי מקצוע אמיתיים בעמוד",
  ],
  internalLinks: [
    "סימולציה משפטית ← /production/justice/legal-simulation (כשיש מועד דיון)",
    "בית המוצר ← /production/justice (הסבר המסע המלא)",
    "אשכולות תחום וכלים — יעדי המשך מתוכננים, מסומנים כאן כלא־קיימים",
  ],
  dataPolicy: [
    "אין מודל, אין שליחה ואין שמירה באב הטיפוס — נאמר במפורש ליד כל שדה.",
    "אין הצגת אחוזי דיוק, זמני מענה או כמות משתמשים.",
    "פרופילים מקצועיים אינם מוצגים כאן; כשיוצגו, כל רשומת זרע תסומן ״פרופיל דמו״.",
  ],
  wordpress: [
    "בלוק Intake (ACF): טקסט חופשי + צ׳יפים לדוגמה, מנוהל עריכתית.",
    "בלוק Output Skeleton: שישה שדות קבועים, כדי שהפלט יהיה ניתן לביקורת.",
    "בלוק Next Action: יעד יחיד דומיננטי + משניים; מצב disabled מנוהל בשדה.",
    "בלוק Legal Notice גלובלי, נעול לעורכי תוכן.",
    "אירועי dataLayer מוגדרים ברמת הבלוק; ללא כותרות Pods/Debug בפלט.",
  ],
};

