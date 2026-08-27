import { Link } from "@tanstack/react-router";
import { useLang } from "@/lib/lang-context";
import { HE, EN } from "@/lib/nadlan-copy";

export function SiteHeader() {
  const { lang, setLang } = useLang();
  const isHe = lang === "he";
  const c = isHe ? HE : EN;

  const navItems = [
    { to: "/projects" as const, label: c.nav.projects },
    { to: "/listings" as const, label: c.nav.listings },
    { to: "/professionals" as const, label: c.nav.professionals },
    { to: "/urban-renewal" as const, label: c.nav.urbanRenewal },
    { to: "/my-rentals" as const, label: c.nav.rentals },
    { to: "/guides" as const, label: c.nav.guides },
  ];

  return (
    <header className="hairline-b bg-paper">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
        <Link to="/" className="text-2xl" style={{ fontFamily: "var(--font-serif-he)", fontWeight: 800 }}>
          {c.brand}
        </Link>

        <nav className="hidden gap-6 md:flex">
          {navItems.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className="text-sm text-ink/85 transition-colors hover:text-gold"
              activeProps={{ className: "text-gold" }}
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setLang(isHe ? "en" : "he")}
            className="hairline rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wider hover:bg-band"
            aria-label={isHe ? "Switch to English" : "מעבר לעברית"}
          >
            {isHe ? "EN" : "עב"}
          </button>
        </div>
      </div>
    </header>
  );
}

