import { createFileRoute } from "@tanstack/react-router";
import { JusticeShell, Notice, StateBadge, type Impl } from "@/components/production/JusticeShell";
import {
  Band,
  BandHead,
  Chip,
  FaqList,
  InlineLink,
  Panel,
} from "@/components/production/ui";

export const Route = createFileRoute("/production/justice/")({
  head: () => ({
    meta: [
      { title: "Justice — הבינו את המצב המשפטי והחליטו על הצעד הבא" },
      {
        name: "description",
        content:
          "תארו מה קרה, קבלו מפת מצב בשפה פשוטה, התכוננו לדיון בסימולציה והחליטו מתי צריך עורך דין. מידע כללי, לא ייעוץ משפטי.",
      },
      { property: "og:title", content: "Justice — הבינו, התכוננו, החליטו" },
      {
        property: "og:description",
        content: "מסלול אחד ברור: הבנה של המצב, הכנה וסימולציה, ומעבר לעזרה מקצועית כשצריך.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "robots", content: "noindex, nofollow" },
    ],
  }),
  component: JusticeHome,
});

const chips = [
  "פוטרתי מהעבודה",
  "זומנתי לדיון בבית משפט",
  "אנחנו לקראת גירושין",
  "קיבלתי תביעה קטנה",
  "יש לי רישום פלילי ישן",
  "מחלוקת עם שכן",
];

const steps = [
  {
    n: "1",
    t: "מבינים מה קרה",
    d: "תיאור חופשי או מסמך שהעליתם הופכים לסיכום בשפה פשוטה: מה הסוגיה, מה דחוף ומה חסר.",
  },
  {
    n: "2",
    t: "מתכוננים ומתרגלים",
    d: "רשימת מסמכים, שאלות שצפויות לעלות, וסימולציית דיון שמאפשרת להתאמן לפני שנכנסים לאולם.",
  },
  {
    n: "3",
    t: "מחליטים על עזרה מקצועית",
    d: "כשהמצב מצדיק זאת — מעבר מסודר לאיש מקצוע, עם תיק מוכן ושאלות ברורות במקום דף ריק.",
  },
];

const intents = [
  {
    t: "הכנה לדיון",
    d: "מה קורה באולם, מי מדבר מתי, ואיך בונים ציר זמן עובדתי קצר.",
    k: "הכנה לדיון בבית משפט",
  },
  {
    t: "חקירת עדים",
    d: "מבנה שאלות, מה מותר לשאול, ואיפה נופלים בלי הכנה מוקדמת.",
    k: "חקירה נגדית · שאלות לעד",
  },
  {
    t: "עלות גירושין",
    d: "מרכיבי העלות והמשתנים שמזיזים אותה — בלי מחירון ובלי הבטחות.",
    k: "עלות הליך גירושין",
  },
  {
    t: "מחיקת רישום פלילי",
    d: "מה נרשם, מי רואה, ומהם המסלולים והתנאים העקרוניים.",
    k: "מחיקת רישום פלילי",
  },
  {
    t: "הסכם גירושין",
    d: "הסעיפים שמופיעים כמעט תמיד, ומה נדרש לאישור ההסכם.",
    k: "הסכם גירושין · אישור הסכם",
  },
];

const trust = [
  {
    t: "שיטת העריכה",
    d: "כל מדריך מסומן בסוג התוכן: הסבר כללי, סקירת הליך או כלי. אין המלצה אישית.",
  },
  {
    t: "מקורות ועדכון",
    d: "שדות מקור, תאריך עדכון ובודק מקצועי מוצגים גלויים — וריקים כל עוד לא מולאו.",
  },
  {
    t: "פרטיות ואבטחה",
    d: "אין להזין פרטים מזהים או מסמכים רגישים באב הטיפוס. אין שמירה, אין שליחה, אין עיבוד.",
  },
];

const faq = [
  {
    q: "האם זה ייעוץ משפטי?",
    a: "לא. המוצר מספק מידע כללי, הכנה וסימולציה. אין כאן חוות דעת, אין המלצה אישית ואין יחסי עורך דין–לקוח.",
  },
  {
    q: "מה ההבדל בין jus-tice.co.il ל‑jus-tice.com?",
    a: "‏.co.il הוא שכבת ההבנה, ההסבר וההכוונה בעברית. הסימולטור, מרחב העבודה המקצועי והמוצר הבין־לאומי יושבים ב‑.com.",
  },
  {
    q: "האם הסימולציה מחליפה עורך דין?",
    a: "לא. היא כלי הכנה. במצבים מורכבים או דחופים ההמלצה היא לפנות לאיש מקצוע.",
  },
];

function JusticeHome() {
  return (
    <JusticeShell route="/production/justice" impl={impl}>
      <main id="main">
        <section className="border-b border-border bg-surface py-14 text-surface-foreground md:py-20">
          <div className="lab-container grid gap-10 lg:grid-cols-[1.05fr_0.95fr]">
            <div className="min-w-0">
              <p className="text-xs font-bold uppercase tracking-[0.14em] text-muted-foreground">
                אב טיפוס פנימי · לא לפרסום
              </p>
              <h1 className="display mt-3 text-3xl leading-tight md:text-5xl">
                תבינו מה קרה, תתכוננו כמו שצריך, ותחליטו על הצעד הבא
              </h1>
              <p className="mt-4 max-w-xl text-base leading-relaxed text-muted-foreground md:text-lg">
                מתארים את המצב במילים שלכם ומקבלים מפת מצב בשפה פשוטה: מה הסוגיה, מה דחוף,
                אילו מסמכים נדרשים ומתי כדאי עורך דין. אפשר גם לתרגל דיון לפני שנכנסים אליו.
              </p>

              <div id="intake" className="mt-7 rounded-lg border border-border bg-card p-5 text-card-foreground">
                <label htmlFor="home-scenario" className="text-sm font-bold">
                  ספרו מה קרה
                </label>
                <textarea
                  id="home-scenario"
                  rows={3}
                  placeholder="לדוגמה: קיבלתי מכתב פיטורים בלי שימוע, ואני לא יודע מה הצעד הראשון."
                  className="mt-2 w-full rounded-md border border-input bg-background p-3 text-sm leading-relaxed"
                />
                <p className="mt-2 text-xs text-muted-foreground">
                  אב טיפוס — הטקסט לא נשמר, לא נשלח ולא מעובד. אל תזינו פרטים מזהים.
                </p>
                <ul className="mt-3 flex flex-wrap gap-2">
                  {chips.map((c) => (
                    <li key={c}>
                      <button
                        type="button"
                        className="tap inline-flex min-h-11 items-center rounded-full border border-border bg-background px-3 py-2 text-xs font-semibold hover:bg-secondary"
                      >
                        {c}
                      </button>
                    </li>
                  ))}
                </ul>
                <div className="mt-5 flex flex-wrap items-center gap-3">
                  <a
                    href="#journey"
                    className="tap inline-flex min-h-11 items-center rounded-md bg-primary px-5 py-3 text-sm font-bold text-primary-foreground hover:opacity-90"
                  >
                    מצאו את המסלול שלכם
                  </a>
                  <InlineLink to="/production/justice/legal-simulation">
                    עברו לסימולציה
                  </InlineLink>
                </div>
              </div>
            </div>

            <div className="min-w-0 space-y-4">
              <Notice tone="legal" title="מידע כללי, לא ייעוץ משפטי">
                אין כאן חוות דעת אישית, אין הבטחה לתוצאה ואין יחסי עורך דין–לקוח. בהליך פעיל
                או בלוח זמנים דחוף — פנו לאיש מקצוע.
              </Notice>
              <Panel>
                <h2 className="display text-lg">ציר הדיון — תצוגה מוקדמת</h2>
                <ol className="mt-4 space-y-3 border-s-2 border-border ps-4 text-sm text-muted-foreground">
                  {["פתיחה והצגת הצדדים", "עדות ראשית", "חקירה נגדית", "סיכומים", "החלטה או מועד המשך"].map(
                    (s, i) => (
                      <li key={s} className="relative">
                        <span
                          aria-hidden="true"
                          className="absolute -start-[1.32rem] top-1.5 inline-block h-2 w-2 rounded-full bg-primary"
                        />
                        <span className="font-semibold text-foreground">{i + 1}. </span>
                        {s}
                      </li>
                    ),
                  )}
                </ol>
                <p className="mt-4 text-xs text-muted-foreground">
                  מבנה עקרוני להמחשה. ההליך המדויק משתנה לפי סוג הדיון והערכאה.
                </p>
              </Panel>
            </div>
          </div>
        </section>

        <Band id="journey" labelledBy="j-journey">
          <BandHead
            id="j-journey"
            eyebrow="המסלול"
            title="שלושה שלבים, בלי לקפוץ לשלב האחרון"
            lead="רוב האנשים מגיעים באמצע סיפור. המוצר מסדר את הסיפור לפני שהוא מציע פעולה."
          />
          <ol className="grid gap-4 md:grid-cols-3">
            {steps.map((s) => (
              <Panel as="li" key={s.t}>
                <span className="text-xs font-bold uppercase tracking-wide text-muted-foreground">
                  שלב {s.n}
                </span>
                <h3 className="display mt-1 text-xl">{s.t}</h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{s.d}</p>
              </Panel>
            ))}
          </ol>
          <div className="mt-7">
            <InlineLink to="/production/justice/legal-ai-desk">
              התחילו בתיאור המצב בשולחן ה‑AI
            </InlineLink>
          </div>
        </Band>

        <Band tone="surface" labelledBy="j-intents">
          <BandHead
            id="j-intents"
            eyebrow="כוונות מובילות"
            title="חמש נקודות כניסה שאנשים באמת מחפשים"
            lead="כל כרטיס הוא אשכול תוכן עם מדריך ממוקד, כלי רלוונטי ומעבר לסימולציה — לא מאמר ענק אחד."
          />
          <ul className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {intents.map((i) => (
              <Panel as="li" key={i.t}>
                <Chip>{i.k}</Chip>
                <h3 className="display mt-3 text-xl">{i.t}</h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{i.d}</p>
                <div className="mt-4">
                  <InlineLink to="/production/justice/legal-ai-desk">
                    להתחלה מהירה עם שולחן ה‑AI
                  </InlineLink>
                </div>
              </Panel>
            ))}
          </ul>
        </Band>

        <Band labelledBy="j-fork">
          <BandHead
            id="j-fork"
            eyebrow="למי זה מיועד"
            title="שני קהלים, שני מסלולים — אחרי שהמוצר הוסבר"
          />
          <div className="grid gap-4 md:grid-cols-2">
            <Panel>
              <h3 className="display text-xl">אנשים פרטיים</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                הבנה של המצב, הכנה לדיון, מסמכים ושאלות — ואז החלטה מושכלת אם ומתי לפנות
                לעורך דין.
              </p>
              <div className="mt-4">
                <InlineLink to="/production/justice/legal-ai-desk">התחילו כאן</InlineLink>
              </div>
            </Panel>
            <Panel className="border-dashed">
              <h3 className="display text-xl">עורכי דין וחברות</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                פרופיל מקצועי, פניות ממוקדות יותר, וכלי הכנה וסימולציה במרחב העבודה — חלקם
                עדיין במפת הדרכים ומסומנים ככאלה.
              </p>
              <div className="mt-4">
                <InlineLink href="#j-trust">איך אנחנו בונים את האזור המקצועי</InlineLink>
              </div>
            </Panel>
          </div>
        </Band>

        <Band tone="surface" labelledBy="j-trust">
          <BandHead id="j-trust" eyebrow="שקיפות" title="איך התוכן נבנה ומה עוד חסר" />
          <div className="grid gap-4 md:grid-cols-3">
            {trust.map((t) => (
              <Panel key={t.t}>
                <h3 className="display text-lg">{t.t}</h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{t.d}</p>
              </Panel>
            ))}
          </div>
          <div className="mt-5 grid gap-3 md:grid-cols-3">
            {["מקור: —", "עודכן: —", "נבדק על ידי: —"].map((x) => (
              <p
                key={x}
                className="rounded-md border border-dashed border-border bg-card p-3 text-xs font-semibold text-muted-foreground"
              >
                {x}
              </p>
            ))}
          </div>
          <div className="mt-6 flex flex-wrap items-center gap-2">
            <StateBadge state="demo" />
            <StateBadge state="empty" />
            <StateBadge state="pending" />
            <StateBadge state="verified" />
          </div>
        </Band>

        <Band labelledBy="j-faq">
          <BandHead id="j-faq" eyebrow="שאלות נפוצות" title="מה המוצר כן, ומה הוא לא" />
          <FaqList items={faq} />
        </Band>
      </main>
    </JusticeShell>
  );
}

const impl: Impl = {
  intent:
    "כניסה מותגית וכניסת בעיה כללית בעברית: המשתמש יודע שקרה משהו משפטי ולא יודע מה הצעד הראשון. העמוד מקטלג את הכוונה ומעביר לשולחן ה‑AI או לאשכול תוכן.",
  keywords: {
    primary: "עזרה משפטית ראשונית · מה עושים כשמקבלים תביעה",
    secondary: [
      "הכנה לדיון בבית משפט",
      "סימולציה משפטית",
      "מדריכים משפטיים בעברית",
      "מתי צריך עורך דין",
    ],
  },
  meta: {
    title: "Justice — הבינו את המצב המשפטי והחליטו על הצעד הבא",
    description:
      "תארו מה קרה, קבלו מפת מצב בשפה פשוטה, התכוננו לדיון והחליטו מתי צריך עורך דין. מידע כללי, לא ייעוץ משפטי.",
    canonical: "https://jus-tice.co.il/ (באב הטיפוס: noindex,nofollow)",
  },
  schema: [
    "WebPage + Organization (ללא Review, ללא AggregateRating)",
    "FAQPage — רק על שלוש השאלות המוצגות בפועל בעמוד",
    "אין Person/Service עבור פרופילים זרעיים",
  ],
  internalLinks: [
    "שולחן AI ← /production/justice/legal-ai-desk (עוגן: ״התחילו בתיאור המצב״)",
    "סימולציה ← /production/justice/legal-simulation (עוגן: ״עברו לסימולציה״)",
    "אשכולות תחום (דיני משפחה, פלילי, עבודה) — עמודי ילד בשלב הבא, לא בטווח האב־טיפוס הזה",
    "אזור מקצועי לעורכי דין — מתוכנן, טרם נבנה באב הטיפוס",
  ],
  dataPolicy: [
    "אין נתוני משתמשים, אין תיקים, אין המלצות ואין שיעורי הצלחה.",
    "שדות מקור/עדכון/בודק מוצגים ריקים במפורש ולא ממולאים בערכי דמה.",
    "קלט המשתמש אינו נשמר ואינו נשלח באב הטיפוס.",
  ],
  wordpress: [
    "בלוקים: hero-intake, journey-steps, intent-cards, audience-fork, trust-method, faq-visible.",
    "CPT: guide, tool, practice_area; טקסונומיות: intent, audience.",
    "כל בלוק FAQ מזריק סכימה רק כשהשאלות גלויות בעמוד.",
    "אסור להציג כותרות טכניות מסוג Pods או Pods Debug Log — לחסום בתבנית.",
  ],
};

