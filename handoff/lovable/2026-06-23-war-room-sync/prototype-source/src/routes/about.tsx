import { createFileRoute } from "@tanstack/react-router";
import { useLang } from "@/lib/lang-context";

export const Route = createFileRoute("/about")({
  head: () => ({
    meta: [
      { title: "אודות · Nadlan3D" },
      { name: "description", content: "Nadlan3D: showroom תלת־ממדי לכל פרויקט בישראל. אמת חזותית, היררכיית דירוג שקופה." },
      { property: "og:title", content: "About · Nadlan3D" },
      { property: "og:url", content: "/about" },
    ],
    links: [{ rel: "canonical", href: "/about" }],
  }),
  component: About,
});

function About() {
  const { lang } = useLang();
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6">
      <h1 className="text-3xl sm:text-4xl">{lang === "he" ? "אודות" : "About"}</h1>
      <div className="mt-6 space-y-5 text-base leading-relaxed text-foreground">
        {lang === "he" ? (
          <>
            <p>Nadlan3D הוא נסיון לפתור בעיה אחת: רוכש פוטנציאלי בישראל לא יודע באמת מה הוא קונה לפני שהוא קונה.</p>
            <p>פתרנו אותה עם <strong>showroom תלת־ממדי</strong> לכל פרויקט. כשהיזם נותן GLB אמיתי — מציגים אותו. כשאין — מציגים חזות סכמטית מסומנת. כשאין שום דבר — מציגים מצב ריק עם בקשה ליזם להעלות חזות. בלי לרמות.</p>
            <p>שם המותג <code>Nadlan3D</code> הוא כיוון אב־טיפוס — לא ניקוי חוקי או דומיין סופי.</p>
            <p>האתר הוא <strong>פרוטוטייפ</strong> — לא תחליף לייעוץ משפטי, מימוני או מקצועי.</p>
          </>
        ) : (
          <>
            <p>Nadlan3D answers one question: in Israel, a buyer rarely knows what they're buying before signing.</p>
            <p>We answer it with a <strong>3D showroom for every project</strong>. When the developer supplies a real GLB, we render it. When they don't, we render a labelled schematic facade. When nothing exists, we render an empty state and ask the developer to upload. No fakes.</p>
            <p>The <code>Nadlan3D</code> brand is a working direction — not legal clearance or a confirmed domain.</p>
            <p>This site is a <strong>prototype</strong> — not legal, financial or professional advice.</p>
          </>
        )}
      </div>
    </div>
  );
}
