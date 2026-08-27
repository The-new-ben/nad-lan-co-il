import { createFileRoute } from "@tanstack/react-router";

const TERMS = [
  { term: "תמ״א 38", def: "תוכנית מתאר ארצית לחיזוק מבנים מפני רעידות אדמה. הוחלפה במסלולי התחדשות עירונית חדשים." },
  { term: "פינוי־בינוי", def: "מסלול התחדשות שבו מפנים בניין קיים, הורסים ובונים חדש עם יותר יחידות דיור." },
  { term: "היתר בנייה", def: "אישור הוועדה המקומית לתכנון ובנייה, בלעדיו אי אפשר להתחיל בבנייה." },
  { term: "טאבו", def: "רישום זכויות במקרקעין. הבעלות הרשומה בטאבו היא הראיה החזקה ביותר." },
  { term: "מס רכישה", def: "מס המשולם בקניית דירה, במדרגות משתנות לפי סוג הרוכש והמחיר." },
  { term: "היוון", def: "המרת תשלום מהוון של דמי חכירה בסכום חד־פעמי לרמ״י." },
];

export const Route = createFileRoute("/glossary")({
  head: () => ({
    meta: [
      { title: "מילון מונחים · נדל״ן" },
      { name: "description", content: "מילון מונחים בסיסי לקנייה, השכרה והתחדשות עירונית בישראל." },
    ],
  }),
  component: GlossaryPage,
});

function GlossaryPage() {
  return (
    <section className="mx-auto max-w-4xl px-4 py-16 sm:px-6 sm:py-24">
      <p className="kicker">מילון מונחים</p>
      <h1 className="mt-3">המילים שכדאי להכיר לפני שחותמים</h1>
      <p className="mt-4 text-muted-ink">הסברים קצרים, בעברית ברורה, בלי משפטית מיותרת.</p>

      <dl className="mt-10 grid gap-4">
        {TERMS.map((t) => (
          <div key={t.term} className="hairline rounded-xl bg-card p-5">
            <dt className="text-base font-semibold text-gold" style={{ fontFamily: "var(--font-serif-he)" }}>{t.term}</dt>
            <dd className="mt-2 text-sm text-ink">{t.def}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}

