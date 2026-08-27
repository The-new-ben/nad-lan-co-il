import { createFileRoute } from "@tanstack/react-router";
import { UrbanRenewalSection } from "@/components/sections/UrbanRenewalSection";
import renewalImage from "@/assets/sketch-urban-renewal.jpg";

export const Route = createFileRoute("/urban-renewal")({
  head: () => ({
    meta: [
      { title: "התחדשות עירונית · נדל״ן" },
      { name: "description", content: "חדר פרויקט לכל בניין בהתחדשות עירונית: מודל תלת־ממדי, מעקב הסכמות ותיק מסמכים." },
    ],
  }),
  component: UrbanRenewalPage,
});

function UrbanRenewalPage() {
  return (
    <>
      <section className="bg-paper hairline-b">
        <div className="mx-auto grid max-w-6xl gap-10 px-4 py-16 sm:px-6 sm:py-24 lg:grid-cols-[1fr_1fr] lg:items-center">
          <div>
            <p className="kicker">התחדשות עירונית</p>
            <h1 className="mt-3">המסלול מהבניין הישן לבניין החדש — על ציר זמן אחד.</h1>
            <p className="mt-4 text-muted-ink">חדר פרויקט לכל בניין: מעקב הסכמות דיירים, לוח שלבים גלוי, ותיק מסמכים אחד לכל הדיירים.</p>
            <div className="mt-6 flex flex-wrap gap-3">
              <a href="/my-renewal" className="btn-terracotta hover:btn-terracotta-hover">בדיקת כדאיות חינם</a>
              <a href="#steps" className="btn-gold-outline">איך זה עובד</a>
            </div>
          </div>
          <div className="hairline overflow-hidden rounded-2xl bg-band">
            <img src={renewalImage} alt="בניין ישן והבניין החדש המוצע מאחוריו" className="h-full w-full object-contain" />
          </div>
        </div>
      </section>
      <div id="steps">
        <UrbanRenewalSection />
      </div>
    </>
  );
}

