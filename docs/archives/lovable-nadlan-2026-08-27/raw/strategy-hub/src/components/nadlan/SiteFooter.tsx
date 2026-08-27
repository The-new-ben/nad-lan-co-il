import { Link } from "@tanstack/react-router";
import { useLang } from "@/lib/lang-context";
import { Nadlan3DMark } from "./Nadlan3DMark";

export function SiteFooter() {
  const { t, lang } = useLang();
  return (
    <footer className="hairline-t mt-16 bg-background">
      <div className="mx-auto grid max-w-6xl gap-8 px-4 py-10 sm:grid-cols-3 sm:px-6">
        <div>
          <Nadlan3DMark className="h-7 w-auto text-foreground" />
          <p className="mt-3 max-w-xs text-sm text-muted-foreground">{t("brand.tagline")}</p>
        </div>
        <div className="text-sm">
          <h4 className="mb-3 text-xs uppercase tracking-wider text-muted-foreground">
            {t("nav.listings")}
          </h4>
          <ul className="space-y-2">
            <li><Link to="/listings" className="hover:text-foreground text-muted-foreground">{t("nav.listings")}</Link></li>
            <li><Link to="/cities/tel-aviv" className="hover:text-foreground text-muted-foreground">{t("nav.cities")}</Link></li>
            <li><Link to="/guides" className="hover:text-foreground text-muted-foreground">{t("nav.guides")}</Link></li>
            <li><Link to="/professionals" className="hover:text-foreground text-muted-foreground">{t("nav.professionals")}</Link></li>
          </ul>
        </div>
        <div className="text-sm">
          <h4 className="mb-3 text-xs uppercase tracking-wider text-muted-foreground">
            {lang === "he" ? "משפטי" : "Legal"}
          </h4>
          <p className="text-muted-foreground leading-relaxed">{t("footer.disclaim")}</p>
          <p className="mt-3 text-xs text-muted-foreground">© {new Date().getFullYear()} Nadlan3D / demo</p>
        </div>
      </div>
    </footer>
  );
}

