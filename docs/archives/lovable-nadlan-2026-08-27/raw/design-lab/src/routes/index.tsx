import { createFileRoute, Link } from "@tanstack/react-router";
import { concepts } from "@/lib/lab-data";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "מעבדת עיצוב · השוואת שישה קונספטים לאתרי Justice ונדל״ן" },
      {
        name: "description",
        content:
          "מעבדה פנימית להשוואת שישה כיווני עיצוב מונחי SEO: שלושה ל‑jus-tice.co.il ושלושה לאתר הנדל״ן, כולל אפיון מסירה לוורדפרס.",
      },
      { property: "og:title", content: "מעבדת עיצוב · השוואת קונספטים" },
      {
        property: "og:description",
        content: "שישה קונספטים מלאים לעמוד בית, עם הערות SEO והיגיון המרה.",
      },
    ],
  }),
  component: LabHome,
});

const rules = [
  "אין נתונים מומצאים: ללא תוצאות, לקוחות, מחירים, המלצות או נתוני עסקאות.",
  "ערכי הדגמה מסומנים תמיד בתווית ״דוגמה״.",
  "כל קונספט: H1 יחיד בעברית, היררכיית H2/H3 עקבית, פריסת RTL סמנטית.",
  "כל הקישורים הפנימיים הקשריים — לא ״לחצו כאן״.",
  "אין חפיפה בין כוונת חיפוש של jus-tice.co.il לבין jus-tice.com.",
  "נגישות: פוקוס מקלדת גלוי, ניגודיות, יעדי מגע 44px, תמיכה בהפחתת תנועה.",
];

function LabHome() {
  const finals = concepts.filter((c) => c.final);
  const justice = concepts.filter((c) => c.brand === "justice" && !c.final);
  const nadlan = concepts.filter((c) => c.brand === "nadlan" && !c.final);

  return (
    <main id="main" className="min-h-screen bg-background text-foreground">
      <header className="border-b border-border bg-surface">
        <div className="lab-container py-12 md:py-16">
          <p className="inline-flex items-center rounded-full border-2 border-dashed border-ring px-3 py-1 text-xs font-bold">
            פרויקט פנימי · לא לפרסום
          </p>
          <h1 className="display mt-4 text-3xl leading-tight md:text-5xl">
            מעבדת עיצוב מונחית SEO — השוואת שישה קונספטים לעמוד בית
          </h1>
          <p className="mt-4 max-w-3xl text-lg leading-relaxed text-muted-foreground">
            אפיון עיצוב לוורדפרס, לא אתר חדש. שלושה כיוונים ל‑jus-tice.co.il ושלושה
            לאתר הנדל״ן. כל קונספט כולל תפריט מלא, מבנה כותרות, כרטיסי תוכן וכלים
            אמיתיים, בלוקי אמון, מגירת הערות פנימית ופאנל מסירה לוורדפרס.
          </p>
        </div>
      </header>

      <section className="lab-container py-12" aria-labelledby="final-set">
        <h2 id="final-set" className="display text-2xl md:text-3xl">
          כיווני הפקה סופיים
        </h2>
        <p className="mt-2 max-w-2xl text-muted-foreground">
          שני מסלולים מומלצים להפקה: Justice מוביל במוצר עם שכבת סמכות מתחתיו, ונדל״ן
          מוביל בכלים עם מנוע קישור פנימי וצ׳ק־ליסט לפי שלב.
        </p>
        <ul className="mt-6 grid gap-4 md:grid-cols-2">
          {finals.map((c) => (
            <ConceptCard key={c.id} code={c.code} name={c.name} tagline={c.tagline} path={c.path} />
          ))}
        </ul>
      </section>

      <section className="lab-container py-12" aria-labelledby="justice-set">
        <h2 id="justice-set" className="display text-2xl md:text-3xl">
          Justice · jus-tice.co.il
        </h2>
        <p className="mt-2 max-w-2xl text-muted-foreground">
          רכישת ביקוש חיפוש בעברית, הסברה והכשרה לקראת הליך — והובלה אל הסימולציה
          כשיא המוצר. המוצר המקצועי, השוק והבינלאומי נשארים ב‑jus-tice.com.
        </p>
        <ul className="mt-6 grid gap-4 md:grid-cols-3">
          {justice.map((c) => (
            <ConceptCard key={c.id} code={c.code} name={c.name} tagline={c.tagline} path={c.path} />
          ))}
        </ul>
      </section>

      <section className="lab-container py-12" aria-labelledby="nadlan-set">
        <h2 id="nadlan-set" className="display text-2xl md:text-3xl">
          נדל״ן
        </h2>
        <p className="mt-2 max-w-2xl text-muted-foreground">
          התועלת היא החפיר: נסח טאבו, מחשבון מס רכישה, סימולטור מס רכישה ומחשבון מס
          שבח — כל אחד עמוד עצמאי עם בעלות נפרדת על כוונת החיפוש.
        </p>
        <ul className="mt-6 grid gap-4 md:grid-cols-3">
          {nadlan.map((c) => (
            <ConceptCard key={c.id} code={c.code} name={c.name} tagline={c.tagline} path={c.path} />
          ))}
        </ul>
      </section>

      <section className="border-t border-border bg-surface py-12" aria-labelledby="rules">
        <div className="lab-container">
          <h2 id="rules" className="display text-2xl">
            כללי המעבדה
          </h2>
          <ul className="mt-4 grid gap-3 md:grid-cols-2">
            {rules.map((r) => (
              <li
                key={r}
                className="rounded-lg border border-border bg-card p-4 text-sm leading-relaxed text-card-foreground"
              >
                {r}
              </li>
            ))}
          </ul>
        </div>
      </section>

      <footer className="lab-container py-10 text-sm text-muted-foreground">
        מעבדה סטטית להשוואת עיצוב. אין חיבור למסד נתונים, תשלומים או שירותים חיצוניים.
      </footer>
    </main>
  );
}

function ConceptCard({
  code,
  name,
  tagline,
  path,
}: {
  code: string;
  name: string;
  tagline: string;
  path: string;
}) {
  return (
    <li className="rounded-xl border border-border bg-card p-5 text-card-foreground">
      <p className="font-mono text-xs font-bold text-muted-foreground">{code}</p>
      <h3 className="display mt-1 text-xl">{name}</h3>
      <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{tagline}</p>
      <Link
        to={path}
        className="tap mt-4 inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:bg-highlight hover:text-highlight-foreground"
      >
        פתחו את הקונספט
        <span aria-hidden="true">←</span>
      </Link>
    </li>
  );
}

