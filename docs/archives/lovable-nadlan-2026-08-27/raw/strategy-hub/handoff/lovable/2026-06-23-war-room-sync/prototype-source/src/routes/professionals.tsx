import { createFileRoute } from "@tanstack/react-router";
import { useLang } from "@/lib/lang-context";

export const Route = createFileRoute("/professionals")({
  head: () => ({
    meta: [
      { title: "אנשי מקצוע · Nadlan3D" },
      { name: "description", content: "אדריכלים, מעצבי פנים, שמאים, עורכי דין ויועצי מימון." },
      { property: "og:title", content: "Professionals · Nadlan3D" },
      { property: "og:url", content: "/professionals" },
    ],
    links: [{ rel: "canonical", href: "/professionals" }],
  }),
  component: Pros,
});

function Pros() {
  const { lang } = useLang();
  const groups = lang === "he"
    ? ["אדריכלים", "מעצבי פנים", "שמאים", "עו״ד נדל״ן", "יועצי משכנתה", "מהנדסים"]
    : ["Architects", "Interior designers", "Appraisers", "Real-estate lawyers", "Mortgage advisors", "Engineers"];

  return (
    <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6">
      <h1 className="text-3xl sm:text-4xl">{lang === "he" ? "אנשי מקצוע" : "Professionals"}</h1>
      <p className="mt-3 max-w-2xl text-sm text-muted-foreground">
        {lang === "he"
          ? "הרשמה מקצועית תיפתח בגרסה הבאה. אין כאן כרגע ייעוץ מקצועי בפועל."
          : "Professional onboarding ships in the next release. No live professional advice here yet."}
      </p>
      <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {groups.map((g) => (
          <div key={g} className="hairline bg-card p-5">
            <h3 className="text-base">{g}</h3>
            <p className="mt-2 text-xs uppercase tracking-wider text-muted-foreground">
              {lang === "he" ? "בקרוב" : "Coming soon"}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

