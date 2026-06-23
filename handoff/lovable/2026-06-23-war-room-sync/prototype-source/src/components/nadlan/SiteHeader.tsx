import { Link } from "@tanstack/react-router";
import { Menu, X } from "lucide-react";
import { useState } from "react";
import { useLang } from "@/lib/lang-context";
import { Nadlan3DMark } from "./Nadlan3DMark";

export function SiteHeader() {
  const { t, lang, setLang } = useLang();
  const [open, setOpen] = useState(false);

  const links = [
    { to: "/", label: t("nav.home") },
    { to: "/listings", label: t("nav.listings") },
    { to: "/cities/tel-aviv", label: t("nav.cities") },
    { to: "/guides", label: t("nav.guides") },
    { to: "/professionals", label: t("nav.professionals") },
    { to: "/about", label: t("nav.about") },
    { to: "/contact", label: t("nav.contact") },
  ] as const;

  return (
    <header className="hairline-b sticky top-0 z-40 bg-background/85 backdrop-blur supports-[backdrop-filter]:bg-background/70">
      <div className="mx-auto grid max-w-6xl grid-cols-[auto_1fr_auto] items-center gap-4 px-4 py-3 sm:px-6">
        <Link to="/" className="text-foreground" aria-label="Nadlan3D">
          <Nadlan3DMark className="h-7 w-auto" />
        </Link>
        <nav className="hidden items-center justify-center gap-6 text-sm md:flex">
          {links.map((l) => (
            <Link
              key={l.to}
              to={l.to}
              activeProps={{ className: "text-foreground font-medium" }}
              inactiveProps={{ className: "text-muted-foreground hover:text-foreground transition-colors" }}
              activeOptions={{ exact: l.to === "/" }}
            >
              {l.label}
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-2 justify-self-end">
          <button
            type="button"
            onClick={() => setLang(lang === "he" ? "en" : "he")}
            className="hairline rounded-sm px-2 py-1 text-xs font-medium uppercase tracking-wider text-foreground hover:bg-secondary"
            aria-label="Toggle language"
          >
            {t("nav.lang")}
          </button>
          <button
            type="button"
            className="md:hidden rounded-sm p-2 hover:bg-secondary"
            onClick={() => setOpen((o) => !o)}
            aria-label="Menu"
          >
            {open ? <X size={18} /> : <Menu size={18} />}
          </button>
        </div>
      </div>
      {open && (
        <nav className="hairline-t flex flex-col gap-1 bg-background px-4 py-3 md:hidden">
          {links.map((l) => (
            <Link
              key={l.to}
              to={l.to}
              onClick={() => setOpen(false)}
              className="rounded-sm px-2 py-2 text-sm hover:bg-secondary"
            >
              {l.label}
            </Link>
          ))}
        </nav>
      )}
    </header>
  );
}
