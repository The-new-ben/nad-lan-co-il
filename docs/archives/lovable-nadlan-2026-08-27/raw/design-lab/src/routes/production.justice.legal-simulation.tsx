import { createFileRoute } from "@tanstack/react-router";
import { JusticeShell, Notice, type Impl } from "@/components/production/JusticeShell";
import {
  Band,
  BandHead,
  Chip,
  Crumbs,
  FaqList,
  InlineLink,
  Panel,
} from "@/components/production/ui";

export const Route = createFileRoute("/production/justice/legal-simulation")({
  head: () => ({
    meta: [
      { title: "סימולציה משפטית — להתכונן לדיון לפני שנכנסים אליו" },
      {
        name: "description",
        content:
          "מה זו סימולציית דיון, מה היא כן נותנת ומה לא, ואיך מתכוננים נכון. הסימולטור עצמו פועל ב‑jus-tice.com.",
      },
      { property: "og:title", content: "סימולציה משפטית — הכנה מעשית לדיון" },
      {
        property: "og:description",
        content: "תרחישים, הכנת עובדות ושאלות, ומעבר מסודר לסימולטור. מידע כללי, לא ייעוץ משפטי.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "robots", content: "noindex, nofollow" },
    ],
  }),
  component: LegalSimulation,
});

const hearingTypes = ["דיון בבית משפט לענייני משפחה", "דיון בבית דין לעבודה", "תביעה קטנה", "דיון מעצר/שחרור"];
const roles = ["תובע/ת", "נתבע/ת", "עד/ה", "מלווה של בן משפחה"];

const prep = [
  { t: "עובדות", d: "ציר זמן קצר: מה קרה, מתי, ומי היה נוכח. בלי פרשנות ובלי רגש." },
  { t: "ראיות", d: "מה קיים בכתב, מה חסר, ומה אפשר להשיג לפני המועד." },
  { t: "שאלות", d: "מה סביר שישאלו אתכם, ומה אתם רוצים שיישאל." },
];

const agents = [
  { t: "שופט/ת", d: "מנהל את הדיון, קוטע, מבקש התמקדות ומברר סתירות." },
  { t: "עורך/ת דין שכנגד", d: "חוקר נגדית, מחפש אי־דיוקים ומנסה לצמצם את התשובות." },
  { t: "עד/ה", d: "מוסר גרסה שאינה זהה לשלכם, כדי לתרגל התמודדות עם פערים." },
];

const limits = [
  "הסימולציה אינה חיזוי תוצאה ואינה מעריכה סיכויי הצלחה.",
  "התסריטים כלליים ואינם מותאמים לתיק ספציפי או לערכאה מסוימת.",
  "אין להזין שמות, מספרי תיק, מסמכים רגישים או פרטי צד שלישי.",
  "המוצר אינו מחליף ייצוג משפטי ואינו נותן ייעוץ.",
];

const faq = [
  {
    q: "למה הסימולטור יושב בדומיין אחר?",
    a: "‏jus-tice.co.il מסביר, מכשיר ומכוון בעברית. הסימולטור, מרחב העבודה והמוצר הבין־לאומי הם מוצר נפרד ב‑jus-tice.com, כדי לא לפצל את אותה כוונת חיפוש בין שני דומיינים.",
  },
  {
    q: "מה נשמר מהסימולציה?",
    a: "באב הטיפוס — כלום. במוצר, מצב רציני ומצב סנדבוקס קלילי מופרדים לחלוטין, וכל שיתוף הוא בבחירה מפורשת.",
  },
  {
    q: "האם AI יכול להחליף עורך דין?",
    a: "לא. הסימולציה היא אימון ותרגול. החלטות משפטיות דורשות איש מקצוע שמכיר את התיק.",
  },
];

function LegalSimulation() {
  return (
    <JusticeShell
      route="/production/justice/legal-simulation"
      impl={impl}
      headerPrimaryCta="עברו לסימולציה"
      headerPrimaryHref="#bridge"
    >
      <main id="main">
        <section className="border-b border-border bg-surface py-12 text-surface-foreground md:py-16">
          <div className="lab-container">
            <Crumbs
              trail={[
                { label: "בית", to: "/production/justice" },
                { label: "סימולציה משפטית" },
              ]}
            />
            <h1 className="display mt-4 max-w-3xl text-3xl leading-tight md:text-4xl">
              סימולציה משפטית — להתאמן על הדיון לפני שנכנסים אליו
            </h1>
            <p className="mt-4 max-w-2xl text-base leading-relaxed text-muted-foreground md:text-lg">
              רוב האנשים נכנסים לדיון בפעם הראשונה בחייהם. הסימולציה נותנת חזרה מבוקרת: מה
              נשאל, איך עונים בקצרה, ואיפה הגרסה מתפרקת. העמוד הזה מסביר ומכין; הסימולטור
              עצמו פועל ב‑jus-tice.com.
            </p>
            <div className="mt-6">
              <Notice tone="legal" title="גבולות המוצר">
                מידע כללי והכנה בלבד. אין ייעוץ, אין חיזוי תוצאה ואין יחסי עורך דין–לקוח.
              </Notice>
            </div>
          </div>
        </section>

        <Band labelledBy="s-preview">
          <BandHead
            id="s-preview"
            eyebrow="תצוגה מוקדמת"
            title="איך נראית סימולציה — ממשק לא פעיל"
            lead="הרכיבים כאן מדגימים את זרימת המוצר. אין חישוב, אין שמירה ואין חיבור לשרת."
          />
          <div className="grid gap-4 lg:grid-cols-3">
            <Panel>
              <h3 className="display text-lg">1. סוג דיון ותפקיד</h3>
              <fieldset className="mt-3">
                <legend className="text-xs font-bold text-muted-foreground">סוג הדיון</legend>
                <ul className="mt-2 space-y-2">
                  {hearingTypes.map((h) => (
                    <li key={h}>
                      <label className="flex min-h-11 items-center gap-2 rounded-md border border-border bg-background px-3 py-2 text-sm">
                        <input type="radio" name="hearing" disabled />
                        <span>{h}</span>
                      </label>
                    </li>
                  ))}
                </ul>
              </fieldset>
              <fieldset className="mt-4">
                <legend className="text-xs font-bold text-muted-foreground">התפקיד שלכם</legend>
                <ul className="mt-2 flex flex-wrap gap-2">
                  {roles.map((r) => (
                    <li key={r}>
                      <span className="inline-flex items-center rounded-full border border-border bg-card px-3 py-1 text-xs font-semibold">
                        {r}
                      </span>
                    </li>
                  ))}
                </ul>
              </fieldset>
            </Panel>

            <Panel>
              <h3 className="display text-lg">2. הכנת החומר</h3>
              <ul className="mt-3 space-y-3">
                {prep.map((p) => (
                  <li key={p.t} className="rounded-md border border-border bg-background p-3">
                    <p className="text-sm font-bold">{p.t}</p>
                    <p className="mt-1 text-sm text-muted-foreground">{p.d}</p>
                  </li>
                ))}
              </ul>
            </Panel>

            <Panel>
              <h3 className="display text-lg">3. סוכני הדיון</h3>
              <ul className="mt-3 space-y-3">
                {agents.map((a) => (
                  <li key={a.t} className="rounded-md border border-border bg-background p-3">
                    <p className="text-sm font-bold">{a.t}</p>
                    <p className="mt-1 text-sm text-muted-foreground">{a.d}</p>
                  </li>
                ))}
              </ul>
              <p className="mt-3 text-xs text-muted-foreground">
                דמויות תרגול מבוססות תסריט. אינן מייצגות אדם אמיתי, שופט אמיתי או תיק אמיתי.
              </p>
            </Panel>
          </div>
        </Band>

        <Band tone="surface" labelledBy="s-modes">
          <BandHead
            id="s-modes"
            eyebrow="שני מצבים"
            title="מצב רציני ומצב סנדבוקס — מופרדים לגמרי"
          />
          <div className="grid gap-4 md:grid-cols-2">
            <Panel>
              <Chip tone="ink">מצב רציני · פרטי או מקצועי</Chip>
              <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                הכנה לדיון אמיתי. פרטי, ללא שיתוף, ללא לוח מובילים ובלי אלמנטים משחקיים.
                עורך דין יכול להריץ אותו עם לקוח כחלק מהכנה.
              </p>
            </Panel>
            <Panel className="border-dashed">
              <Chip tone="copper">סנדבוקס קליל · חברים</Chip>
              <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                תרחישים בדיוניים לתרגול ולסקרנות, עם הזמנה ושיתוף. מסומן בבירור כשעשוע ואינו
                מציג את עצמו כהכנה לתיק אמיתי.
              </p>
            </Panel>
          </div>
        </Band>

        <Band labelledBy="s-limits">
          <BandHead id="s-limits" eyebrow="מגבלות ופרטיות" title="מה חשוב לדעת לפני שמתחילים" />
          <ul className="grid gap-3 md:grid-cols-2">
            {limits.map((l) => (
              <li
                key={l}
                className="rounded-md border-s-4 border-s-highlight bg-card p-4 text-sm leading-relaxed text-card-foreground"
              >
                {l}
              </li>
            ))}
          </ul>
        </Band>

        <Band id="bridge" tone="surface" labelledBy="s-bridge">
          <BandHead
            id="s-bridge"
            eyebrow="מעבר לסימולטור"
            title="מה עובר ל‑jus-tice.com"
            lead="העמוד הזה מסביר ומכשיר. ההרצה עצמה, החשבון והמרחב המקצועי הם מוצר נפרד."
          />
          <div className="grid gap-4 md:grid-cols-2">
            <Panel>
              <h3 className="display text-lg">נשאר כאן (.co.il)</h3>
              <ul className="mt-2 space-y-2 text-sm text-muted-foreground">
                <li>הסבר ההליך, מדריכי הכנה ומונחים.</li>
                <li>אשכולות תוכן לפי תחום וכוונת חיפוש.</li>
                <li>הכוונה: מתי סימולציה מספיקה ומתי צריך עורך דין.</li>
              </ul>
            </Panel>
            <Panel>
              <h3 className="display text-lg">עובר לשם (.com)</h3>
              <ul className="mt-2 space-y-2 text-sm text-muted-foreground">
                <li>הרצת הסימולציה עם סוכני הדיון.</li>
                <li>חשבון, שמירת הכנה ומרחב עבודה מקצועי.</li>
                <li>מצב סנדבוקס עם הזמנת חברים.</li>
              </ul>
            </Panel>
          </div>
          <div className="mt-7 flex flex-wrap items-center gap-3">
            <button
              type="button"
              className="tap inline-flex min-h-11 items-center rounded-md bg-primary px-5 py-3 text-sm font-bold text-primary-foreground"
            >
              התחילו סימולציה ב‑jus-tice.com
            </button>
            <span className="text-xs font-semibold text-muted-foreground">
              אב טיפוס — הקישור אינו מחובר
            </span>
          </div>
          <div className="mt-5">
            <InlineLink to="/production/justice/legal-ai-desk">
              עוד לא בטוחים מה הסוגיה? התחילו בתיאור המצב
            </InlineLink>
          </div>
        </Band>

        <Band labelledBy="s-faq">
          <BandHead id="s-faq" eyebrow="שאלות נפוצות" title="סימולציה, פרטיות ושני הדומיינים" />
          <FaqList items={faq} />
        </Band>
      </main>
    </JusticeShell>
  );
}

const impl: Impl = {
  intent:
    "כוונה מחקרית־מוצרית: ״סימולציה של דיון״, ״איך מתכוננים לדיון״. העמוד בבעלות .co.il ומשמש גשר המרה אל הסימולטור ב‑.com, בלי לשכפל את כוונת החיפוש בשני הדומיינים.",
  keywords: {
    primary: "סימולציה משפטית · תרגול דיון בבית משפט",
    secondary: ["הכנה לחקירה נגדית", "מה קורה בדיון ראשון", "איך להתכונן לעדות"],
  },
  meta: {
    title: "סימולציה משפטית — להתכונן לדיון לפני שנכנסים אליו",
    description:
      "מה זו סימולציית דיון, מה היא נותנת ומה לא, ואיך מתכוננים. ההרצה עצמה ב‑jus-tice.com.",
    canonical: "https://jus-tice.co.il/legal-simulation/ (אב טיפוס: noindex,nofollow)",
  },
  schema: [
    "WebPage + BreadcrumbList",
    "FAQPage על שלוש השאלות הגלויות בלבד",
    "ללא SoftwareApplication עד שהמוצר ב‑.com זמין וניתן לתיאור מדויק",
  ],
  internalLinks: [
    "שולחן AI ← /production/justice/legal-ai-desk (״לא בטוחים מה הסוגיה״)",
    "אשכול דיני משפחה (הכנה לדיון) — מתוכנן, מחוץ לטווח האב־טיפוס הנוכחי",
    "יעד חיצוני יחיד: jus-tice.com/simulator — קישור אחד דומיננטי, לא חוזר בכל סקשן",
  ],
  dataPolicy: [
    "אין סוכנים אמיתיים, אין תיקים ואין ציטוט פסיקה ללא מקור.",
    "אין הצגת שיעורי הצלחה או השוואת תוצאות.",
    "מצב רציני ומצב סנדבוקס מסומנים בנפרד בכל מסך.",
  ],
  wordpress: [
    "בלוקים: bridge-hero, product-preview (סטטי), mode-split, limits-list, domain-handoff, faq-visible.",
    "כפתור ה‑CTA הוא בלוק יחיד עם יעד מוגדר ב‑ACF, כדי שלא יתרבו CTA מתחרים.",
    "מדיניות: אין רינדור של Pods/Pods Debug Log בשום תבנית.",
  ],
};

