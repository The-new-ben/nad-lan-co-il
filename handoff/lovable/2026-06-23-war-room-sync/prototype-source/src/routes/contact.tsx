import { createFileRoute } from "@tanstack/react-router";
import { useLang } from "@/lib/lang-context";

export const Route = createFileRoute("/contact")({
  head: () => ({
    meta: [
      { title: "צור קשר / Nadlan3D" },
      { name: "description", content: "צרו קשר עם צוות Nadlan3D: קבלנים, רוכשים ויועצים." },
      { property: "og:title", content: "Contact / Nadlan3D" },
      { property: "og:url", content: "/contact" },
    ],
    links: [{ rel: "canonical", href: "/contact" }],
  }),
  component: Contact,
});

function Contact() {
  const { lang } = useLang();
  return (
    <div className="mx-auto max-w-2xl px-4 py-12 sm:px-6">
      <h1 className="text-3xl sm:text-4xl">{lang === "he" ? "צור קשר" : "Contact"}</h1>
      <p className="mt-3 text-sm text-muted-foreground">
        {lang === "he" ? "בגרסת ההדגמה הטופס אינו נשלח בפועל." : "In this demo, the form does not send yet."}
      </p>
      <form
        className="hairline mt-8 grid gap-4 bg-card p-5"
        onSubmit={(e) => { e.preventDefault(); alert(lang === "he" ? "תודה! דמו בלבד." : "Thanks! Demo only."); }}
      >
        <label className="grid gap-1 text-sm">
          <span className="text-muted-foreground">{lang === "he" ? "שם" : "Name"}</span>
          <input required className="hairline rounded-sm bg-background px-3 py-2" />
        </label>
        <label className="grid gap-1 text-sm">
          <span className="text-muted-foreground">{lang === "he" ? "אימייל / WhatsApp" : "Email / WhatsApp"}</span>
          <input required className="hairline rounded-sm bg-background px-3 py-2" />
        </label>
        <label className="grid gap-1 text-sm">
          <span className="text-muted-foreground">{lang === "he" ? "הודעה" : "Message"}</span>
          <textarea rows={4} className="hairline rounded-sm bg-background px-3 py-2" />
        </label>
        <button className="rounded-sm bg-foreground px-4 py-2 text-sm text-background hover:bg-foreground/90">
          {lang === "he" ? "שלח" : "Send"}
        </button>
      </form>
    </div>
  );
}
