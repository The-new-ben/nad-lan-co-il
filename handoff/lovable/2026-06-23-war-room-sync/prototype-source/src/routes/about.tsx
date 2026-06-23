import { createFileRoute } from "@tanstack/react-router";
import { useLang } from "@/lib/lang-context";

export const Route = createFileRoute("/about")({
  head: () => ({
    meta: [
      { title: "אודות / Nadlan3D" },
      { name: "description", content: "Nadlan3D מציג פרויקטים חדשים בצורה חזותית, שקופה ונוחה לרוכשים בישראל ולמשקיעים מחו״ל." },
      { property: "og:title", content: "About / Nadlan3D" },
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
            <p>Nadlan3D נבנה כדי לפתור בעיה אחת: רוכש פוטנציאלי צריך להבין מה הוא קונה לפני שהוא מתקדם לשיחה, ביקור או חתימה.</p>
            <p>אנחנו מציגים לכל פרויקט חוויה חזותית ברורה, עם סימון מלא למה שמבוסס על חומרים קיימים ומה שמוצג להמחשה בלבד.</p>
            <p>המודל העסקי מיועד ליזמים, קבלנים ומשווקים שרוצים להציג פרויקטים ברמה גבוהה לקונים בישראל ולמשקיעים מחו״ל.</p>
            <p>המידע באתר אינו תחליף לייעוץ משפטי, מימוני או מקצועי.</p>
          </>
        ) : (
          <>
            <p>Nadlan3D answers one question: buyers need to understand what they are considering before they move to a call, visit or signature.</p>
            <p>Each project gets a clear visual experience, with visible labels for supplied assets and illustrative material.</p>
            <p>The business model is built for developers, contractors and marketers who need a premium way to reach Israeli buyers and international investors.</p>
            <p>This site is not legal, financial or professional advice.</p>
          </>
        )}
      </div>
    </div>
  );
}
