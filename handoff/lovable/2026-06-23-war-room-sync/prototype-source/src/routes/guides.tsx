import { createFileRoute } from "@tanstack/react-router";
import { useLang } from "@/lib/lang-context";

export const Route = createFileRoute("/guides")({
  head: () => ({
    meta: [
      { title: "מדריכים / Nadlan3D" },
      { name: "description", content: "מדריכי קנייה, מימון, מיסוי, ופינוי-בינוי. מבוסס מקורות, ללא ייעוץ מקצועי." },
      { property: "og:title", content: "Guides / Nadlan3D" },
      { property: "og:url", content: "/guides" },
    ],
    links: [{ rel: "canonical", href: "/guides" }],
  }),
  component: Guides,
});

const ITEMS = [
  { he: "מס רכישה 2026 לפי שלב חיים", en: "Purchase tax 2026 by life stage" },
  { he: "תמ\"א 38 מול פינוי-בינוי: מה נכון בשבילך", en: "TAMA-38 vs urban renewal: which fits you" },
  { he: "מימון משכנתה: מסלולים מצורפים", en: "Mortgage tracks: what to combine" },
  { he: "בדיקת קבלן: 7 דגלים אדומים", en: "Vetting a developer: 7 red flags" },
];

function Guides() {
  const { lang } = useLang();
  return (
    <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6">
      <h1 className="text-3xl sm:text-4xl">{lang === "he" ? "מדריכים" : "Guides"}</h1>
      <p className="mt-3 max-w-2xl text-sm text-muted-foreground">
        {lang === "he"
          ? "מדריכים עריכתיים. לא תחליף לייעוץ מקצועי, אבל מסבירים מה לבדוק לפני שמתקדמים."
          : "Editorial guides. Not a substitute for professional advice, but they explain what to check."}
      </p>
      <ul className="hairline mt-8 divide-y divide-border bg-card">
        {ITEMS.map((it) => (
          <li key={it.en} className="flex items-baseline justify-between gap-4 px-5 py-4">
            <span className="text-base">{lang === "he" ? it.he : it.en}</span>
            <span className="text-xs uppercase tracking-wider text-muted-foreground">
              {lang === "he" ? "בקרוב" : "Soon"}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
