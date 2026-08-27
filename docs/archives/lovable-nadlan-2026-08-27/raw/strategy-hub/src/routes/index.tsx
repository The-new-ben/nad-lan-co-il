import { createFileRoute } from "@tanstack/react-router";
import { HeroSection } from "@/components/sections/HeroSection";
import { TheaterSection } from "@/components/sections/TheaterSection";
import { MapSection } from "@/components/sections/MapSection";
import { RentalsSection } from "@/components/sections/RentalsSection";
import { UrbanRenewalSection } from "@/components/sections/UrbanRenewalSection";
import { ListingsGridSection } from "@/components/sections/ListingsGridSection";
import { ToolsSection } from "@/components/sections/ToolsSection";
import { MagazineSection } from "@/components/sections/MagazineSection";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "נדל״ן — מוצאים דירה, בודקים מחיר, מכירים את הסביבה" },
      { name: "description", content: "כל פרויקט הוא מודל תלת־ממדי חי: קומות, דירות, שמש ונוף מהחלון. פרויקטים חדשים, דירות למכירה, התחדשות עירונית וניהול השכרות." },
      { property: "og:title", content: "נדל״ן — מוצאים דירה, בודקים מחיר, מכירים את הסביבה" },
      { property: "og:description", content: "כל פרויקט הוא מודל תלת־ממדי חי — לפני שחותמים." },
    ],
  }),
  component: HomePage,
});

function HomePage() {
  return (
    <>
      <HeroSection />
      <TheaterSection />
      <MapSection />
      <RentalsSection />
      <UrbanRenewalSection />
      <ListingsGridSection />
      <ToolsSection />
      <MagazineSection />
    </>
  );
}

